"""Tests for the stdlib helper scripts. Run: python3 -m unittest discover -s scripts/tests"""
from __future__ import annotations

import contextlib
import csv
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import experiment_calc  # noqa: E402
import feedback_tally  # noqa: E402
import lint_skills  # noqa: E402
import pr_review_stats  # noqa: E402
import prioritize  # noqa: E402
import token_audit  # noqa: E402
import vtt_to_transcript  # noqa: E402


def run(main, *args) -> tuple:
    """Call a script's main() and capture (exit code, stdout)."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
        code = main(list(args))
    return code, out.getvalue()


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def csv_rows(path: Path) -> list:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def skill(root: Path, name: str, description: str, body: str = "") -> Path:
    return write(root / ".claude" / "skills" / name / "SKILL.md",
                 f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n{body}")


class TmpCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()


class TokenAuditTests(TmpCase):
    def test_frontmatter_handles_quotes_and_block_scalars(self):
        meta = token_audit.parse_frontmatter('---\nname: "a-b"\ndescription: >\n  One\n  two.\n---\nbody')
        self.assertEqual(meta, {"name": "a-b", "description": "One two."})

    def test_indented_dashes_inside_block_scalar_do_not_end_frontmatter(self):
        meta = token_audit.parse_frontmatter("---\nname: x\ndescription: >\n  First.\n  ---\n  Second.\n---\n")
        self.assertEqual(meta["description"], "First. --- Second.")

    def test_orphan_check_follows_symlinks(self):
        real = write(self.tmp / "elsewhere" / "deep" / "SKILL.md", "---\nname: deep\ndescription: x\n---\n")
        (self.tmp / ".claude/skills/linked").mkdir(parents=True)
        os.symlink(real.parent, self.tmp / ".claude/skills/linked/deep")
        self.assertEqual(token_audit.orphan_folders(self.tmp / ".claude/skills"), [])

    def test_flags_placeholders_mismatches_and_nested_skills(self):
        skill(self.tmp, "real-skill", "Do a thing. Use when asked.")
        skill(self.tmp, "todo-later", "Someday.", "\n> **Placeholder** - not built\n")
        write(self.tmp / ".claude/skills/wrong/SKILL.md", "---\nname: other\ndescription: x\n---\n")
        write(self.tmp / ".claude/skills/library/deep-skill/SKILL.md", "---\nname: deep\ndescription: x\n---\n")
        report = token_audit.audit(self.tmp, include_global=False)
        text = "\n".join(report["warnings"])
        self.assertIn("todo-later: placeholder", text)
        self.assertIn("wrong: name!=folder", text)
        self.assertEqual(report["listings"][0]["count"], 3)
        self.assertEqual(report["on_demand"][0]["count"], 1)

    def test_codex_symlink_to_tree_with_nested_skills_warns(self):
        skill(self.tmp, "top", "Top skill. Use when asked.")
        write(self.tmp / ".claude/skills/library/deep/SKILL.md", "---\nname: deep\ndescription: x\n---\n")
        (self.tmp / ".agents").mkdir()
        os.symlink("../.claude/skills", self.tmp / ".agents" / "skills")
        report = token_audit.audit(self.tmp, include_global=False)
        codex = [l for l in report["listings"] if l["harness"] == "Codex"][0]
        self.assertEqual(codex["count"], 2)
        self.assertTrue(any("nested skill folders" in w for w in report["warnings"]))

    def test_claude_md_imports_count_toward_size(self):
        write(self.tmp / "extra.md", "x" * 400)
        write(self.tmp / "CLAUDE.md", "Rules\n@extra.md\n")
        surface = token_audit.audit(self.tmp, include_global=False)["always"][0]
        self.assertGreater(surface["chars"], 400)
        self.assertIn("imports extra.md", surface["note"])

    def test_agents_md_reading_another_file_is_reported(self):
        write(self.tmp / "AGENTS.md", "Read `CLAUDE.md` at the\nstart of every session.\n")
        report = token_audit.audit(self.tmp, include_global=False)
        self.assertTrue(any("extra tool call" in i for i in report["info"]))

    def test_strict_exit_code(self):
        skill(self.tmp, "todo-x", "Later.")
        code, out = run(token_audit.main, "--repo", str(self.tmp), "--strict")
        self.assertEqual(code, 1)
        self.assertIn("## Warnings (1)", out)


class LintSkillsTests(TmpCase):
    BODY = ("\n## Inputs\n- a\n## Output Contract\n- b\n## Steps\n1. c\n## Examples\n- d\n"
            "## Guardrails\n- e\n")

    def test_clean_skill_passes(self):
        skill(self.tmp, "good-skill", "Does X. Use when Y.", self.BODY)
        write(self.tmp / "README.md", "`good-skill`\n")
        code, out = run(lint_skills.main, "--repo", str(self.tmp))
        self.assertEqual(code, 0, out)
        self.assertIn("0 errors, 0 warnings", out)

    def test_errors_for_contract_breaks(self):
        skill(self.tmp, "bad-skill", "Does X.", "See [ref](references/missing.md) and `scripts/nope.py`.")
        write(self.tmp / "README.md", "nothing here\n")
        code, out = run(lint_skills.main, "--repo", str(self.tmp))
        self.assertEqual(code, 1)
        for expected in ("broken link", "scripts/nope.py", "not listed in README.md",
                         "never says when", "no section for"):
            self.assertIn(expected, out)

    def test_readme_match_is_exact(self):
        skill(self.tmp, "create-prd", "Write a PRD. Use when asked.", self.BODY)
        write(self.tmp / "README.md", "`create-prd-one-pager` only\n")
        code, out = run(lint_skills.main, "--repo", str(self.tmp))
        self.assertIn("not listed in README.md", out)


class VttTests(TmpCase):
    ZOOM = ("WEBVTT\n\n1\n00:00:01.000 --> 00:00:03.000\nDana Lee: Thanks for joining.\n\n"
            "2\n00:00:03.500 --> 00:00:05.000\nDana Lee: Let's start.\n\n"
            "3\n00:01:05.000 --> 00:01:09.000\nConference Room 4B: The export is slow.\n\n"
            "NOTE this is a comment\n\n")
    TEAMS = ("WEBVTT\n\n00:00:00.000 --> 00:00:02.000\n<v Sam Ortiz>Hello there.</v>\n\n"
             "00:00:02.000 --> 00:00:04.000\n<v Sam Ortiz>Second line.</v>\n")

    def test_merges_turns_flags_rooms_and_shrinks(self):
        vtt = write(self.tmp / "call.vtt", self.ZOOM)
        out = self.tmp / "call.md"
        code, stdout = run(vtt_to_transcript.main, str(vtt), "-o", str(out))
        self.assertEqual(code, 0)
        transcript = out.read_text()
        self.assertIn("[00:00:01] Dana Lee: Thanks for joining. Let's start.", transcript)
        self.assertIn("[00:01:05] Conference Room 4B: The export is slow.", transcript)
        self.assertIn("looks like a room or device", stdout)
        self.assertNotIn("-->", transcript)

    def test_rename_and_teams_voice_tags(self):
        vtt = write(self.tmp / "call.vtt", self.ZOOM)
        code, stdout = run(vtt_to_transcript.main, str(vtt), "--json", "--rename", "Conference Room 4B=Priya Shah")
        summary = json.loads(stdout)
        self.assertEqual(summary["flagged_labels"], [])
        self.assertIn("Priya Shah", [s["name"] for s in summary["speakers"]])
        cues = vtt_to_transcript.parse_cues(self.TEAMS)
        self.assertEqual([c[1] for c in cues], ["Sam Ortiz", "Sam Ortiz"])
        self.assertEqual(len(vtt_to_transcript.merge_turns(cues, {})), 1)

    def test_lead_ins_like_q_and_note_are_not_speakers(self):
        cues = vtt_to_transcript.parse_cues("WEBVTT\n\n00:01.000 --> 00:02.000\nQ: What about pricing?\n\n"
                                            "00:02.000 --> 00:03.000\nNote: three tiers.\n")
        self.assertEqual([(c[1], c[2]) for c in cues],
                         [("", "Q: What about pricing?"), ("", "Note: three tiers.")])

    def test_non_vtt_input_fails(self):
        path = write(self.tmp / "notes.vtt", "just text\n")
        self.assertEqual(run(vtt_to_transcript.main, str(path))[0], 1)


class FeedbackTests(TmpCase):
    def test_prep_merges_dedupes_and_samples(self):
        write(self.tmp / "survey.csv", "Date,Comment,Rating\n2026-08-01,Export is slow,2\n"
                                       "2026-08-02,export is SLOW!,2\n2026-08-03,,4\n2026-08-04,Love it,5\n")
        write(self.tmp / "notes.md", "- Search misses old tickets\n\n- Pricing unclear\n")
        out = self.tmp / "feedback.csv"
        code, stdout = run(feedback_tally.main, "prep", str(self.tmp / "survey.csv"),
                           str(self.tmp / "notes.md"), "-o", str(out), "--sample", "2")
        self.assertEqual(code, 0)
        rows = csv_rows(out)
        self.assertEqual([r["id"] for r in rows], ["F0001", "F0002", "F0003", "F0004"])
        self.assertEqual(rows[0]["duplicates"], "1")
        self.assertIn("1 empty dropped", stdout)
        sample = csv_rows(self.tmp / "feedback-sample.csv")
        self.assertEqual(len(sample), 2)
        self.assertEqual({r["source"] for r in sample}, {"survey", "notes"})

    def test_non_english_and_short_items_survive(self):
        write(self.tmp / "intl.csv", "comment\n导出太慢了\nエクスポートが遅い\nЭкспорт медленный\nNo\n\" \"\n")
        out = self.tmp / "o.csv"
        code, stdout = run(feedback_tally.main, "prep", str(self.tmp / "intl.csv"), "-o", str(out))
        self.assertEqual(code, 0)
        self.assertEqual(len(csv_rows(out)), 4)
        self.assertIn("1 empty dropped", stdout)

    def test_unknown_text_column_is_an_error(self):
        write(self.tmp / "a.csv", "x,y\n1,2\n")
        with self.assertRaises(SystemExit):
            run(feedback_tally.main, "prep", str(self.tmp / "a.csv"), "-o", str(self.tmp / "o.csv"),
                "--text-col", "comment")

    def test_tally_counts_weights_and_validates(self):
        write(self.tmp / "items.csv", "id,source,date,rating,segment,duplicates,text\n"
                                      "F0001,survey,,2,,2,Export slow\nF0002,survey,,5,,0,Love it\n"
                                      "F0003,notes,,,,0,Pricing\n")
        write(self.tmp / "codes.csv", "id,theme,sentiment\nF0001,Export;Speed,negative\n"
                                      "F0002,Delight,positive\nF9999,Ghost,negative\n")
        code, out = run(feedback_tally.main, "tally", str(self.tmp / "items.csv"), str(self.tmp / "codes.csv"))
        self.assertEqual(code, 0)
        self.assertIn("Coded 2 of 3 items", out)
        self.assertIn("| Export | 1 | 3 | 50% | 1 | 0 | 0 | 0 | 2.0 | survey |", out)
        self.assertIn("Uncoded (1): F0003", out)
        self.assertIn("unknown ids (1): F9999", out)

    def test_margin_of_error(self):
        self.assertAlmostEqual(feedback_tally.margin_of_error(0.5, 400), 4.9, places=1)
        self.assertLess(feedback_tally.margin_of_error(0.5, 400, population=500), 4.9)


class PrioritizeTests(TmpCase):
    def test_rice_scores_ranks_and_sensitivity(self):
        rows = [{"item": "A", "reach": "2,000", "impact": "2", "confidence": "80%", "effort": "2"},
                {"item": "B", "reach": "500", "impact": "3", "confidence": "100", "effort": "3"},
                {"item": "C", "reach": "480", "impact": "1", "confidence": "1", "effort": "1"}]
        errors, warnings, items = prioritize.rice(rows, sensitivity=True)
        self.assertEqual(errors, [])
        self.assertEqual([(i["item"], i["score"]) for i in items], [("A", 1600.0), ("B", 500.0), ("C", 480.0)])
        self.assertEqual(items[0]["rank_range"], (1, 1))
        self.assertEqual(items[1]["rank_range"], (2, 3))

    def test_rice_rejects_zero_effort_and_ties_share_rank(self):
        errors, _, _ = prioritize.rice([{"item": "X", "reach": "1", "impact": "1", "confidence": "1",
                                         "effort": "0"}], False)
        self.assertTrue(errors)
        self.assertEqual(prioritize.ranks([5, 7, 7, 1]), [3, 1, 1, 4])

    def test_kano_table_and_coefficients(self):
        rows = [{"feature": "Export", "functional": "I expect it", "dysfunctional": "dislike"},
                {"feature": "Export", "functional": "like", "dysfunctional": "dislike"},
                {"feature": "Emoji", "functional": "like", "dysfunctional": "neutral"}]
        errors, _, results = prioritize.kano(rows)
        self.assertEqual(errors, [])
        by_name = {r["feature"]: r for r in results}
        self.assertEqual(by_name["Emoji"]["category"], "A")
        self.assertEqual(by_name["Export"]["category"], "M/O")
        self.assertEqual(by_name["Export"]["worse"], -1.0)

    def test_weighted_needs_known_columns(self):
        errors, _, _, _ = prioritize.weighted([{"item": "A", "value": "3"}], "value=2,cost=1")
        self.assertIn("columns not found: cost", errors[0])


class ExperimentTests(unittest.TestCase):
    def test_sample_size_matches_hand_calculation(self):
        self.assertEqual(experiment_calc.sample_size_proportions(0.10, 0.12, 0.05, 0.8, False), 3841)
        self.assertEqual(experiment_calc.parse_mde("20%", 0.10), 0.02)
        self.assertEqual(experiment_calc.sample_size_means(42, 5, 0.05, 0.8, False), 1108)
        self.assertEqual(experiment_calc.duration_days(3841, 2, 1000, 1.0), 8)

    def test_two_proportion_test(self):
        result = experiment_calc.two_proportion_test(120, 1000, 150, 1000, 0.05)
        self.assertAlmostEqual(result["p_value"], 0.0496, places=3)
        self.assertTrue(result["significant"])

    def test_bad_flags_are_usage_errors_not_crashes(self):
        for args in (("sample-size", "--baseline", "0.1", "--mde", "0.02", "--comparisons", "0"),
                     ("sample-size", "--baseline", "0.1", "--mde", "0.02", "--daily-traffic", "10", "--allocation", "0"),
                     ("significance", "--control", "120", "--variant", "150/1000")):
            with self.assertRaises(SystemExit) as caught:
                run(experiment_calc.main, *args)
            self.assertEqual(caught.exception.code, 2)

    def test_bonferroni_split_increases_sample(self):
        code, out = run(experiment_calc.main, "sample-size", "--baseline", "0.1", "--mde", "0.02",
                        "--comparisons", "2")
        self.assertEqual(code, 0)
        self.assertIn("split across 2 comparisons", out)
        self.assertNotIn("3,841 per variant", out)


class PrReviewStatsTests(TmpCase):
    def test_metrics_exclude_self_and_bot_reviews(self):
        prs = [
            {"number": 1, "createdAt": "2026-09-01T00:00:00Z", "mergedAt": "2026-09-01T10:00:00Z",
             "additions": 40, "deletions": 10, "author": {"login": "pm"},
             "reviews": [{"author": {"login": "pm"}, "state": "COMMENTED", "submittedAt": "2026-09-01T01:00:00Z"},
                         {"author": {"login": "review-bot"}, "state": "COMMENTED", "submittedAt": "2026-09-01T02:00:00Z"},
                         {"author": {"login": "eng"}, "state": "CHANGES_REQUESTED", "submittedAt": "2026-09-01T04:00:00Z"}]},
            {"number": 2, "createdAt": "2026-09-02T00:00:00Z", "mergedAt": "2026-09-02T01:00:00Z",
             "additions": 2000, "deletions": 0, "author": {"login": "pm"}, "reviews": []},
        ]
        rows = [pr_review_stats.pr_metrics(p, exclude_bots=True) for p in prs]
        self.assertEqual(rows[0]["first_review_h"], 4.0)
        self.assertEqual(rows[0]["change_requests"], 1)
        self.assertEqual(rows[1]["size"], "XL (1000+)")
        self.assertEqual(pr_review_stats.summarize(rows)["unreviewed_merges"], 0.5)
        path = write(self.tmp / "prs.json", json.dumps(prs))
        code, out = run(pr_review_stats.main, str(path))
        self.assertEqual(code, 0)
        self.assertIn("| All | 2 | 2.0 |", out)

    def test_percentile_nearest_rank(self):
        self.assertEqual(pr_review_stats.percentile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 90), 9)


if __name__ == "__main__":
    unittest.main()
