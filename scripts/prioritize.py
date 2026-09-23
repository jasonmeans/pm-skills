#!/usr/bin/env python3
"""Score and rank backlog items (RICE, ICE, weighted) and classify Kano survey
responses.

The prioritize-features skill does the judgment (estimates and rationale); this
script does the arithmetic, so rankings are reproducible and auditable.

    python3 scripts/prioritize.py rice backlog.csv [--sensitivity] [-o ranked.md]
    python3 scripts/prioritize.py ice backlog.csv
    python3 scripts/prioritize.py weighted backlog.csv --weights value=3,fit=2,ease=1
    python3 scripts/prioritize.py kano responses.csv

CSV columns (case-insensitive):
  rice      item, reach, impact, confidence, effort    confidence as 0-100 or 0-1
  ice       item, impact, confidence, ease             1-10 each
  weighted  item + one column per --weights criterion  higher is better
  kano      feature, functional, dysfunctional         one row per respondent answer pair
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path

RICE_IMPACT_SCALE = (0.25, 0.5, 1, 2, 3)  # minimal, low, medium, high, massive
PERTURBATION = 0.2                        # "what if any one estimate is 20% off?"

# Kano evaluation table: functional answer x dysfunctional answer -> category.
# A attractive, O one-dimensional (performance), M must-be, I indifferent,
# R reverse, Q questionable (contradictory answers).
KANO_ANSWERS = ("like", "expect", "neutral", "tolerate", "dislike")
KANO_TABLE = {
    "like": "QAAAO",
    "expect": "RIIIM",
    "neutral": "RIIIM",
    "tolerate": "RIIIM",
    "dislike": "RRRRQ",
}
KANO_SYNONYMS = {
    "like": ("like", "i like it", "i like it that way", "delighted", "1"),
    "expect": ("expect", "must-be", "must be", "i expect it", "it must be that way", "2"),
    "neutral": ("neutral", "i am neutral", "i'm neutral", "don't care", "3"),
    "tolerate": ("tolerate", "live with", "live-with", "i can live with it", "i can tolerate it", "4"),
    "dislike": ("dislike", "i dislike it", "i dislike it that way", "5"),
}
KANO_NAMES = {"A": "Attractive", "O": "Performance", "M": "Must-be", "I": "Indifferent",
              "R": "Reverse", "Q": "Questionable"}


def read_csv(path: str) -> list:
    with open(path, newline="", encoding="utf-8-sig") as handle:
        return [{re.sub(r"[\s-]+", "_", (k or "").strip().lower()): (v or "").strip()
                 for k, v in row.items()} for row in csv.DictReader(handle)]


def number(row: dict, column: str, errors: list) -> float:
    raw = row.get(column, "").replace(",", "").rstrip("%")
    try:
        return float(raw)
    except ValueError:
        errors.append(f"{label(row)}: '{column}' is not a number ({row.get(column, '')!r})")
        return float("nan")


def label(row: dict) -> str:
    return row.get("item") or row.get("feature") or row.get("name") or "?"


def ranks(scores: list) -> list:
    """Competition ranking (1, 2, 2, 4) for scores, highest first."""
    return [1 + sum(other > score for other in scores) for score in scores]


def rice_score(reach: float, impact: float, confidence: float, effort: float) -> float:
    return reach * impact * confidence / effort


def rice(rows: list, sensitivity: bool) -> tuple:
    errors, warnings, items = [], [], []
    for row in rows:
        reach, impact = number(row, "reach", errors), number(row, "impact", errors)
        confidence, effort = number(row, "confidence", errors), number(row, "effort", errors)
        if confidence > 1:
            confidence /= 100
        if effort <= 0:
            errors.append(f"{label(row)}: effort must be > 0 (person-months)")
            continue
        if impact not in RICE_IMPACT_SCALE:
            warnings.append(f"{label(row)}: impact {impact:g} is off the 0.25/0.5/1/2/3 scale")
        if confidence < 0.5:
            warnings.append(f"{label(row)}: confidence {confidence:.0%} is a moonshot; gather evidence first")
        items.append({"item": label(row), "reach": reach, "impact": impact,
                      "confidence": min(confidence, 1.0), "effort": effort})
    if errors:
        return errors, warnings, []
    scores = [rice_score(i["reach"], i["impact"], i["confidence"], i["effort"]) for i in items]
    for item, score, rank in zip(items, scores, ranks(scores)):
        item.update(score=score, rank=rank)
    if sensitivity:
        for index, item in enumerate(items):
            seen = {item["rank"]}
            for factor in ("reach", "impact", "confidence", "effort"):
                for scale in (1 - PERTURBATION, 1 + PERTURBATION):
                    changed = dict(item, **{factor: item[factor] * scale})
                    changed["confidence"] = min(changed["confidence"], 1.0)
                    trial = list(scores)
                    trial[index] = rice_score(changed["reach"], changed["impact"],
                                              changed["confidence"], changed["effort"])
                    seen.add(ranks(trial)[index])
            item["rank_range"] = (min(seen), max(seen))
    return errors, warnings, sorted(items, key=lambda i: (i["rank"], i["item"]))


def render_rice(items: list, sensitivity: bool) -> str:
    head = "| Rank | Item | Reach | Impact | Confidence | Effort | RICE |"
    rule = "|---|---|---|---|---|---|---|"
    if sensitivity:
        head, rule = head + " Rank if one estimate is ±20% off |", rule + "---|"
    lines = ["RICE = Reach × Impact × Confidence ÷ Effort", "", head, rule]
    for i in items:
        row = (f"| {i['rank']} | {i['item']} | {i['reach']:,.0f} | {i['impact']:g} | {i['confidence']:.0%} "
               f"| {i['effort']:g} | {i['score']:,.1f} |")
        if sensitivity:
            low, high = i["rank_range"]
            note = f"{low}" if low == high else f"{low}–{high}" + (" (fragile)" if high - low >= 2 else "")
            row += f" {note} |"
        lines.append(row)
    if sensitivity and items:
        top = items[0]
        verdict = "holds under every ±20% change" if top["rank_range"] == (1, 1) else \
            "is not robust: a single ±20% estimate change can move it"
        lines += ["", f"Top item '{top['item']}' {verdict}."]
    return "\n".join(lines)


def ice(rows: list) -> tuple:
    errors, warnings, items = [], [], []
    for row in rows:
        values = [number(row, c, errors) for c in ("impact", "confidence", "ease")]
        if any(not 1 <= v <= 10 for v in values if v == v):
            warnings.append(f"{label(row)}: ICE inputs should be 1-10")
        items.append({"item": label(row), "impact": values[0], "confidence": values[1],
                      "ease": values[2], "score": values[0] * values[1] * values[2]})
    if errors:
        return errors, warnings, []
    for item, rank in zip(items, ranks([i["score"] for i in items])):
        item["rank"] = rank
    return errors, warnings, sorted(items, key=lambda i: (i["rank"], i["item"]))


def render_ice(items: list) -> str:
    lines = ["ICE = Impact × Confidence × Ease (each 1-10)", "",
             "| Rank | Item | Impact | Confidence | Ease | ICE |", "|---|---|---|---|---|---|"]
    lines += [f"| {i['rank']} | {i['item']} | {i['impact']:g} | {i['confidence']:g} | {i['ease']:g} "
              f"| {i['score']:g} |" for i in items]
    return "\n".join(lines)


def weighted(rows: list, spec: str) -> tuple:
    errors, warnings, items = [], [], []
    weights = {}
    for part in filter(None, spec.split(",")):
        name, _, value = part.partition("=")
        try:
            weights[re.sub(r"[\s-]+", "_", name.strip().lower())] = float(value)
        except ValueError:
            errors.append(f"bad weight {part!r}; use criterion=number")
    if not weights or any(w <= 0 for w in weights.values()):
        errors.append("--weights needs positive numbers, e.g. value=3,fit=2,ease=1")
    missing = [c for c in weights if rows and c not in rows[0]]
    if missing:
        errors.append(f"columns not found: {', '.join(missing)}")
    if errors:
        return errors, warnings, [], weights
    total = sum(weights.values())
    for row in rows:
        values = {c: number(row, c, errors) for c in weights}
        items.append({"item": label(row), **values,
                      "score": sum(weights[c] * values[c] for c in weights) / total})
    if errors:
        return errors, warnings, [], weights
    for item, rank in zip(items, ranks([i["score"] for i in items])):
        item["rank"] = rank
    return errors, warnings, sorted(items, key=lambda i: (i["rank"], i["item"])), weights


def render_weighted(items: list, weights: dict) -> str:
    total = sum(weights.values())
    shares = ", ".join(f"{c} {w / total:.0%}" for c, w in weights.items())
    cols = list(weights)
    lines = [f"Weighted score = Σ weight × score, weights normalized ({shares})", "",
             "| Rank | Item | " + " | ".join(cols) + " | Score |",
             "|---|---|" + "---|" * len(cols) + "---|"]
    for i in items:
        lines.append(f"| {i['rank']} | {i['item']} | " + " | ".join(f"{i[c]:g}" for c in cols)
                     + f" | {i['score']:.2f} |")
    return "\n".join(lines)


def kano_answer(raw: str) -> str:
    text = raw.strip().lower().rstrip(".")
    return next((k for k, words in KANO_SYNONYMS.items() if text in words), "")


def kano(rows: list) -> tuple:
    errors, warnings, tallies = [], [], {}
    for n, row in enumerate(rows, 2):
        functional, dysfunctional = kano_answer(row.get("functional", "")), kano_answer(row.get("dysfunctional", ""))
        if not functional or not dysfunctional:
            errors.append(f"row {n}: unrecognized answer pair ({row.get('functional')!r}, {row.get('dysfunctional')!r})")
            continue
        category = KANO_TABLE[functional][KANO_ANSWERS.index(dysfunctional)]
        tallies.setdefault(label(row), Counter())[category] += 1
    results = []
    for feature, counts in tallies.items():
        n = sum(counts.values())
        top = max(counts.values())
        winners = "/".join(sorted(c for c, v in counts.items() if v == top))
        base = counts["A"] + counts["O"] + counts["M"] + counts["I"] or 1
        results.append({"feature": feature, "n": n, "counts": counts, "category": winners,
                        "better": (counts["A"] + counts["O"]) / base,
                        "worse": -(counts["O"] + counts["M"]) / base})
        if counts["Q"] / n > 0.1:
            warnings.append(f"{feature}: {counts['Q'] / n:.0%} questionable answers; check the question wording")
    return errors, warnings, sorted(results, key=lambda r: (-r["better"], r["feature"]))


def render_kano(results: list) -> str:
    lines = ["Kano categories from functional/dysfunctional answer pairs. Better = (A+O)/(A+O+M+I), "
             "Worse = −(O+M)/(A+O+M+I).", "",
             "| Feature | n | A | O | M | I | R | Q | Category | Better | Worse |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        c = r["counts"]
        name = " / ".join(KANO_NAMES[x] for x in r["category"].split("/"))
        lines.append(f"| {r['feature']} | {r['n']} | {c['A']} | {c['O']} | {c['M']} | {c['I']} | {c['R']} "
                     f"| {c['Q']} | {name} | {r['better']:.2f} | {r['worse']:.2f} |")
    return "\n".join(lines)


def main(argv: list = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("method", choices=("rice", "ice", "weighted", "kano"))
    parser.add_argument("csv", help="input CSV")
    parser.add_argument("--weights", default="", help="weighted: criterion=weight,... (higher score = better)")
    parser.add_argument("--sensitivity", action="store_true", help="rice: rank range if any one estimate is ±20%% off")
    parser.add_argument("-o", "--out", help="write the Markdown table here")
    args = parser.parse_args(argv)

    rows = read_csv(args.csv)
    if args.method == "rice":
        errors, warnings, items = rice(rows, args.sensitivity)
        table = render_rice(items, args.sensitivity)
    elif args.method == "ice":
        errors, warnings, items = ice(rows)
        table = render_ice(items)
    elif args.method == "weighted":
        errors, warnings, items, weights = weighted(rows, args.weights)
        table = render_weighted(items, weights) if items else ""
    else:
        errors, warnings, items = kano(rows)
        table = render_kano(items)

    for message in errors:
        print(f"ERROR {message}", file=sys.stderr)
    if errors:
        return 1
    report = table + ("\n\nWarnings:\n" + "\n".join(f"- {w}" for w in warnings) if warnings else "") + "\n"
    if args.out:
        Path(args.out).write_text(report, encoding="utf-8")
        print(f"Wrote {args.out}: {len(items)} rows ranked by {args.method}")
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
