#!/usr/bin/env python3
"""Baseline code-review health from GitHub pull requests.

Gives the automate-review-process skill measured numbers instead of anecdotes:
time to first review, time to merge, change-request rounds and unreviewed
merges, split by PR size.

    gh pr list --state merged --limit 200 \\
      --json number,createdAt,mergedAt,additions,deletions,author,reviews > prs.json
    python3 scripts/pr_review_stats.py prs.json [--exclude-bots] [-o review-baseline.md]

Times are wall-clock hours (no business-hours adjustment). Draft time counts
toward time to first review because GitHub's PR list does not expose when a
draft became ready.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime
from pathlib import Path

SIZE_BUCKETS = ((10, "XS (<10 lines)"), (100, "S (10-99)"), (400, "M (100-399)"),
                (1000, "L (400-999)"), (math.inf, "XL (1000+)"))


def when(stamp: str) -> datetime:
    return datetime.fromisoformat(stamp.replace("Z", "+00:00"))


def hours(start: str, end: str) -> float:
    return (when(end) - when(start)).total_seconds() / 3600


def is_bot(author: dict) -> bool:
    login = (author or {}).get("login", "")
    return bool((author or {}).get("is_bot")) or login.endswith("[bot]") or login.endswith("-bot")


def percentile(values: list, pct: float) -> float:
    """Nearest-rank percentile; deterministic and easy to explain."""
    if not values:
        return float("nan")
    ordered = sorted(values)
    return ordered[max(0, math.ceil(pct / 100 * len(ordered)) - 1)]


def bucket(lines: int) -> str:
    return next(name for limit, name in SIZE_BUCKETS if lines < limit)


def pr_metrics(pr: dict, exclude_bots: bool) -> dict:
    author = (pr.get("author") or {}).get("login", "")
    reviews = [r for r in pr.get("reviews") or []
               if r.get("submittedAt") and (r.get("author") or {}).get("login") != author
               and not (exclude_bots and is_bot(r.get("author")))]
    first = min((r["submittedAt"] for r in reviews), default=None)
    size = (pr.get("additions") or 0) + (pr.get("deletions") or 0)
    return {
        "number": pr.get("number"),
        "size": bucket(size),
        "first_review_h": hours(pr["createdAt"], first) if first else None,
        "merge_h": hours(pr["createdAt"], pr["mergedAt"]) if pr.get("mergedAt") else None,
        "reviewed": bool(reviews),
        "change_requests": sum(r.get("state") == "CHANGES_REQUESTED" for r in reviews),
    }


def summarize(rows: list) -> dict:
    first = [r["first_review_h"] for r in rows if r["first_review_h"] is not None]
    merge = [r["merge_h"] for r in rows if r["merge_h"] is not None]
    merged = [r for r in rows if r["merge_h"] is not None]
    return {
        "prs": len(rows),
        "first_median": percentile(first, 50), "first_p90": percentile(first, 90),
        "merge_median": percentile(merge, 50), "merge_p90": percentile(merge, 90),
        "unreviewed_merges": sum(not r["reviewed"] for r in merged) / len(merged) if merged else float("nan"),
        "with_changes": sum(r["change_requests"] > 0 for r in rows) / len(rows) if rows else float("nan"),
        "mean_rounds": sum(r["change_requests"] for r in rows) / len(rows) if rows else float("nan"),
    }


def fmt(value: float, kind: str) -> str:
    if value != value:  # NaN
        return "–"
    return f"{value:.0%}" if kind == "pct" else f"{value:.1f}"


def render(rows: list, exclude_bots: bool) -> str:
    who = "human reviews only" if exclude_bots else "all reviewers, bots included"
    lines = [f"Review baseline for {len(rows)} PRs ({who}; wall-clock hours; self-reviews ignored).", "",
             "| Size | PRs | First review p50 | p90 | Merge p50 | p90 | Merged unreviewed | Changes requested | Rounds/PR |",
             "|---|---|---|---|---|---|---|---|---|"]
    groups = [("All", rows)] + [(name, [r for r in rows if r["size"] == name]) for _, name in SIZE_BUCKETS]
    for name, group in groups:
        if not group:
            continue
        s = summarize(group)
        lines.append(f"| {name} | {s['prs']} | {fmt(s['first_median'], 'h')} | {fmt(s['first_p90'], 'h')} "
                     f"| {fmt(s['merge_median'], 'h')} | {fmt(s['merge_p90'], 'h')} "
                     f"| {fmt(s['unreviewed_merges'], 'pct')} | {fmt(s['with_changes'], 'pct')} "
                     f"| {fmt(s['mean_rounds'], 'n')} |")
    return "\n".join(lines) + "\n"


def main(argv: list = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("json", help="output of `gh pr list --json number,createdAt,mergedAt,additions,deletions,author,reviews`")
    parser.add_argument("--exclude-bots", action="store_true", help="ignore bot and AI reviewers when timing first review")
    parser.add_argument("-o", "--out", help="write the Markdown table here")
    args = parser.parse_args(argv)

    prs = json.loads(Path(args.json).read_text(encoding="utf-8"))
    missing = [f for f in ("createdAt", "reviews") if prs and f not in prs[0]]
    if missing:
        print(f"ERROR input lacks {', '.join(missing)}; rerun gh with those --json fields", file=sys.stderr)
        return 1
    rows = [pr_metrics(pr, args.exclude_bots) for pr in prs]
    report = render(rows, args.exclude_bots)
    if args.out:
        Path(args.out).write_text(report, encoding="utf-8")
        print(f"Wrote {args.out}: {len(rows)} PRs")
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
