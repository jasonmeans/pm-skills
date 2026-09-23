#!/usr/bin/env python3
"""Normalize raw feedback exports and tally coded themes.

The analyze-user-feedback skill uses this for the parts a model should not do
by hand: merging files, de-duplicating, sampling and counting.

    # 1. Merge exports (CSV, TSV, JSONL, TXT, MD) into one numbered file
    python3 scripts/feedback_tally.py prep survey.csv tickets.csv notes.md -o feedback.csv
    python3 scripts/feedback_tally.py prep big.csv -o feedback.csv --sample 400 --seed 7

    # 2. After coding items into codes.csv (id,theme,sentiment[,severity])
    python3 scripts/feedback_tally.py tally feedback.csv codes.csv -o themes.md [--moe]

In codes.csv an item may carry several themes: repeat the id on several rows or
separate themes with ';'. Sentiment is positive, negative, neutral or mixed.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

TEXT_COLUMNS = ("feedback", "comment", "comments", "text", "response", "message", "body",
                "description", "verbatim", "answer", "review", "content")
DATE_COLUMNS = ("date", "created", "created_at", "createdat", "timestamp", "submitted",
                "submitted_at", "time")
RATING_COLUMNS = ("rating", "score", "nps", "csat", "stars", "satisfaction")
SEGMENT_COLUMNS = ("segment", "plan", "tier", "team", "persona", "role", "customer_type")
SENTIMENTS = ("negative", "neutral", "positive", "mixed")
FIELDS = ("id", "source", "date", "rating", "segment", "duplicates", "text")


def norm_header(name: str) -> str:
    return re.sub(r"[\s-]+", "_", name.strip().lower())


def pick(columns: dict, candidates: tuple) -> str:
    return next((columns[c] for c in candidates if c in columns), "")


def read_rows(path: Path, text_col: str, per_line: bool) -> tuple:
    """Return (records, note) where each record has text/date/rating/segment/source."""
    suffix = path.suffix.lower()
    if suffix in (".csv", ".tsv"):
        with path.open(newline="", encoding="utf-8-sig", errors="replace") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t" if suffix == ".tsv" else ","))
        return from_table(rows, path, text_col)
    if suffix in (".jsonl", ".ndjson"):
        rows = []
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.strip():
                value = json.loads(line)
                rows.append({k: v if isinstance(v, str) else "" if v is None else json.dumps(v)
                             for k, v in value.items()})
        return from_table(rows, path, text_col)
    text = path.read_text(encoding="utf-8", errors="replace")
    chunks = text.splitlines() if per_line or not re.search(r"\n\s*\n", text) else re.split(r"\n\s*\n", text)
    records = []
    for chunk in chunks:
        chunk = re.sub(r"(?m)^\s*(?:[-*+]|\d+[.)])\s+", "", chunk)
        chunk = "\n".join(line for line in chunk.splitlines() if not line.lstrip().startswith("#"))
        records.append({"text": chunk, "source": path.stem})
    return records, ""


def from_table(rows: list, path: Path, text_col: str) -> tuple:
    if not rows:
        return [], ""
    columns = {norm_header(c): c for c in rows[0].keys() if c}
    note = ""
    if text_col:
        text_key = columns.get(norm_header(text_col))
        if not text_key:
            raise SystemExit(f"{path.name}: no column named {text_col!r}; columns: {', '.join(columns.values())}")
    else:
        text_key = pick(columns, TEXT_COLUMNS)
    if not text_key:
        text_key = max(columns.values(), key=lambda c: statistics.mean(len(r.get(c) or "") for r in rows))
        note = f"{path.name}: no obvious text column, used '{text_key}' (override with --text-col)"
    keys = {"date": pick(columns, DATE_COLUMNS), "rating": pick(columns, RATING_COLUMNS),
            "segment": pick(columns, SEGMENT_COLUMNS), "source": columns.get("source", "")}
    records = []
    for row in rows:
        record = {k: (row.get(v) or "").strip() if v else "" for k, v in keys.items()}
        record["text"] = row.get(text_key) or ""
        record["source"] = record["source"] or path.stem
        records.append(record)
    return records, note


def prep(args: argparse.Namespace) -> int:
    records, notes, files = [], [], 0
    for name in args.inputs:
        rows, note = read_rows(Path(name), args.text_col, args.per_line)
        records.extend(rows)
        notes.append(note)
        files += 1
    kept, seen, empty = [], {}, 0
    for record in records:
        text = re.sub(r"\s+", " ", record["text"]).strip()
        key = " ".join(re.findall(r"\w+", text.lower()))  # Unicode-aware: keeps non-English feedback
        if not key:
            empty += 1
            continue
        if key in seen:
            seen[key]["duplicates"] += 1
            continue
        record = dict(record, text=text, duplicates=0)
        seen[key] = record
        kept.append(record)
    width = max(4, len(str(len(kept))))
    for index, record in enumerate(kept, 1):
        record["id"] = f"F{index:0{width}d}"

    out = Path(args.out)
    write_items(out, kept)
    print(f"Wrote {out}: {len(kept):,} items from {files} file(s) "
          f"({sum(r['duplicates'] for r in kept):,} duplicates merged, {empty:,} empty dropped)")
    for note in filter(None, notes):
        print(f"Note: {note}")
    print("By source: " + " · ".join(f"{s} {n:,}" for s, n in Counter(r["source"] for r in kept).most_common()))
    dates = sorted(r["date"][:10] for r in kept if r.get("date"))
    if dates:
        print(f"Dates: {dates[0]} → {dates[-1]} ({len(dates):,} dated)")
    ratings = [float(r["rating"]) for r in kept if re.fullmatch(r"-?\d+(\.\d+)?", r.get("rating", ""))]
    if ratings:
        counts = Counter(int(x) if x.is_integer() else x for x in ratings)
        spread = " ".join(f"{k}:{v}" for k, v in sorted(counts.items()))
        print(f"Ratings: n={len(ratings):,} mean {statistics.mean(ratings):.2f} ({spread})")
    words = [len(r["text"].split()) for r in kept] or [0]
    total_tokens = math.ceil(sum(len(r["text"]) for r in kept) / 4)
    print(f"Text: median {statistics.median(words):.0f} words · ~{total_tokens:,} tokens in total")
    if not args.sample and (len(kept) > 600 or total_tokens > 60000):
        print("Tip: too much to code in one pass; rerun with --sample 400 and report estimates")
    if args.sample:
        sample = stratified_sample(kept, args.sample, args.seed)
        sample_path = out.with_name(f"{out.stem}-sample{out.suffix}")
        write_items(sample_path, sample)
        print(f"Wrote {sample_path}: {len(sample):,}-item sample, stratified by source (seed {args.seed})")
    return 0


def stratified_sample(records: list, size: int, seed: int) -> list:
    """Proportional allocation by source (largest remainder), random within source."""
    if size >= len(records):
        return list(records)
    groups = defaultdict(list)
    for record in records:
        groups[record["source"]].append(record)
    quotas = {s: size * len(g) / len(records) for s, g in groups.items()}
    counts = {s: int(q) for s, q in quotas.items()}
    for source in sorted(quotas, key=lambda s: quotas[s] - counts[s], reverse=True)[: size - sum(counts.values())]:
        counts[source] += 1
    rng = random.Random(seed)
    picked = [r for s, g in sorted(groups.items()) for r in rng.sample(g, min(counts[s], len(g)))]
    return sorted(picked, key=lambda r: r["id"])


def write_items(path: Path, records: list) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)


def tally(args: argparse.Namespace) -> int:
    with open(args.items, newline="", encoding="utf-8-sig") as handle:
        items = {row["id"]: row for row in csv.DictReader(handle)}
    themes, moods_by_theme, unknown, odd = defaultdict(set), defaultdict(dict), set(), Counter()
    severity = defaultdict(Counter)
    with open(args.codes, newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            row = {norm_header(k): (v or "").strip() for k, v in row.items() if k}
            item_id = row.get("id", "")
            if item_id not in items:
                unknown.add(item_id)
                continue
            mood = row.get("sentiment", "").lower()
            if mood and mood not in SENTIMENTS:
                odd[mood] += 1
                mood = ""
            for theme in filter(None, (t.strip() for t in re.split(r"[;|]", row.get("theme", "")))):
                themes[theme].add(item_id)
                if mood:
                    moods_by_theme[theme][item_id] = mood
                if row.get("severity"):
                    severity[theme][row["severity"].upper()] += 1
    coded = set().union(*themes.values()) if themes else set()
    n = len(coded)
    if not n:
        print("No coded items matched the items file.", file=sys.stderr)
        return 1

    lines = [f"Coded {n:,} of {len(items):,} items ({100 * n / len(items):.0f}%). "
             "An item can carry several themes, so shares can sum past 100%.", ""]
    moe_header = " ±95% |" if args.moe else ""
    lines.append(f"| Theme | Items | Weighted | Share |{moe_header} Neg | Neu | Pos | Mixed | Avg rating | Top sources |")
    lines.append("|---" * (10 + bool(args.moe)) + "|")
    rows = []
    for theme, ids in themes.items():
        weighted = sum(1 + int(items[i].get("duplicates") or 0) for i in ids)
        rows.append((weighted, len(ids), theme, ids))
    for weighted, count, theme, ids in sorted(rows, key=lambda r: (-r[0], -r[1], r[2])):
        share = count / n
        moods = Counter(moods_by_theme[theme].get(i, "") for i in ids)
        ratings = [float(items[i]["rating"]) for i in ids
                   if re.fullmatch(r"-?\d+(\.\d+)?", items[i].get("rating") or "")]
        avg = f"{statistics.mean(ratings):.1f}" if ratings else ""
        sources = ", ".join(s for s, _ in Counter(items[i]["source"] for i in ids).most_common(2))
        moe = f" {margin_of_error(share, n, args.population):.1f} pts |" if args.moe else ""
        lines.append(f"| {theme} | {count} | {weighted} | {100 * share:.0f}% |{moe} {moods['negative']} "
                     f"| {moods['neutral']} | {moods['positive']} | {moods['mixed']} | {avg} | {sources} |")
    if severity:
        lines += ["", "Severity by theme: " + "; ".join(
            f"{t} " + " ".join(f"{k}:{v}" for k, v in sorted(c.items())) for t, c in sorted(severity.items()))]
    uncoded = sorted(set(items) - coded)
    if uncoded:
        lines += ["", f"Uncoded ({len(uncoded)}): " + ", ".join(uncoded[:15]) + (" …" if len(uncoded) > 15 else "")]
    if unknown:
        lines += ["", f"Codes with unknown ids ({len(unknown)}): " + ", ".join(sorted(unknown)[:15])]
    if odd:
        lines += ["", "Unrecognized sentiment values (ignored): " + ", ".join(f"{k} ×{v}" for k, v in odd.items())]
    report = "\n".join(lines) + "\n"
    if args.out:
        Path(args.out).write_text(report, encoding="utf-8")
        print(f"Wrote {args.out}: {len(themes)} themes across {n:,} coded items")
    else:
        print(report, end="")
    return 0


def margin_of_error(share: float, n: int, population: int = 0) -> float:
    """95% margin of error in percentage points, with finite-population correction."""
    moe = 1.96 * math.sqrt(share * (1 - share) / n)
    if population and population > n:
        moe *= math.sqrt((population - n) / (population - 1))
    return 100 * moe


def main(argv: list = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prep", help="merge, de-duplicate and number raw feedback")
    p.add_argument("inputs", nargs="+", help="CSV, TSV, JSONL, TXT or MD files")
    p.add_argument("-o", "--out", required=True, help="output CSV path")
    p.add_argument("--text-col", default="", help="column holding the feedback text")
    p.add_argument("--per-line", action="store_true", help="TXT/MD: one item per line, not per paragraph")
    p.add_argument("--sample", type=int, default=0, help="also write an N-item stratified sample")
    p.add_argument("--seed", type=int, default=7)
    t = sub.add_parser("tally", help="count coded themes")
    t.add_argument("items", help="the CSV written by prep (or its sample)")
    t.add_argument("codes", help="CSV with id,theme[,sentiment][,severity]")
    t.add_argument("-o", "--out", help="write the Markdown table here")
    t.add_argument("--moe", action="store_true", help="add a 95%% margin-of-error column (for samples)")
    t.add_argument("--population", type=int, default=0, help="full item count, for the finite-population correction")
    args = parser.parse_args(argv)
    return prep(args) if args.command == "prep" else tally(args)


if __name__ == "__main__":
    sys.exit(main())
