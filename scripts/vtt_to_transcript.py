#!/usr/bin/env python3
"""Turn a WebVTT meeting transcript (Zoom, Teams, Meet) into a compact,
speaker-merged Markdown transcript plus a speaker summary.

Raw VTT spends a large share of its characters on cue numbers and timestamps.
Reading the cleaned file instead saves tokens and replaces the manual clean-up
step in the analyze-user-interview and convert-meeting-notes skills.

    python3 scripts/vtt_to_transcript.py call.vtt -o call.md
    python3 scripts/vtt_to_transcript.py call.vtt -o call.md --rename "Room 4B=Dana Lee"
    python3 scripts/vtt_to_transcript.py call.vtt --json     # summary only, as JSON

The summary (speakers, labels that look like rooms or devices, size reduction)
prints to stdout. The transcript goes to -o, or to stdout when -o is omitted.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TIMING = re.compile(r"^(?:(\d+):)?(\d{1,2}):(\d{2})[.,](\d{3})\s+-->")
VOICE = re.compile(r"<v(?:\.[^\s>]+)?\s+([^>]+)>")
TAG = re.compile(r"</?[^>]+>")
SPEAKER = re.compile(r"^([^:]{1,60}?):\s+(.*)$")
NOT_SPEAKERS = {"q", "a", "note", "notes", "see", "fyi", "ps", "tip", "warning", "update", "edit",
                "question", "answer", "example", "summary", "agenda", "decision", "action", "todo"}
ROOM_HINTS = re.compile(
    r"\b(room|conference|boardroom|huddle|zoom ?rooms?|iphone|ipad|android|galaxy|pixel"
    r"|h\.?323|sip|polycom|cisco|webex|teams ?room|meeting ?space)\b|^speaker ?\d+$|^unknown",
    re.IGNORECASE,
)


def seconds(match: re.Match) -> float:
    hours, minutes, secs, millis = match.groups()
    return int(hours or 0) * 3600 + int(minutes) * 60 + int(secs) + int(millis) / 1000


def clock(total: float) -> str:
    total = int(total)
    return f"{total // 3600:02d}:{total % 3600 // 60:02d}:{total % 60:02d}"


def parse_cues(text: str) -> list:
    """Return cues as (start_seconds, speaker, text); speaker is '' if unlabeled."""
    cues = []
    for block in re.split(r"\n\s*\n", text.replace("\r\n", "\n").replace("\r", "\n")):
        lines = [line for line in block.strip().split("\n") if line.strip()]
        timing_index = next((i for i, line in enumerate(lines[:2]) if TIMING.match(line)), None)
        if timing_index is None:
            continue  # WEBVTT header, NOTE, STYLE or REGION block
        start = seconds(TIMING.match(lines[timing_index]))
        raw = " ".join(lines[timing_index + 1:]).strip()
        voice = VOICE.search(raw)
        body = re.sub(r"\s+", " ", TAG.sub("", raw)).strip()
        speaker = voice.group(1).strip() if voice else ""
        if not speaker:
            labelled = SPEAKER.match(body)
            label = labelled.group(1).strip() if labelled else ""
            if labelled and len(label) > 1 and label.lower() not in NOT_SPEAKERS and len(label.split()) <= 6:
                speaker, body = label, labelled.group(2).strip()
        if body:
            cues.append((start, speaker, body))
    return cues


def merge_turns(cues: list, renames: dict) -> list:
    turns = []
    for start, speaker, body in cues:
        speaker = renames.get(speaker, speaker)
        if turns and turns[-1]["speaker"] == speaker:
            turns[-1]["text"] += " " + body
        else:
            turns.append({"start": start, "speaker": speaker, "text": body})
    return turns


def summarize(turns: list, cues: list, chars_in: int, chars_out: int) -> dict:
    stats = {}
    for turn in turns:
        entry = stats.setdefault(turn["speaker"] or "(unlabeled)", {"turns": 0, "words": 0})
        entry["turns"] += 1
        entry["words"] += len(turn["text"].split())
    total_words = sum(s["words"] for s in stats.values()) or 1
    speakers = [
        {
            "name": name,
            "turns": s["turns"],
            "words": s["words"],
            "share": round(100 * s["words"] / total_words),
            "looks_like_room_or_device": name != "(unlabeled)" and bool(ROOM_HINTS.search(name)),
        }
        for name, s in sorted(stats.items(), key=lambda item: -item[1]["words"])
    ]
    return {
        "duration": clock(cues[-1][0]) if cues else "00:00:00",
        "cues": len(cues),
        "turns": len(turns),
        "speakers": speakers,
        "flagged_labels": [s["name"] for s in speakers if s["looks_like_room_or_device"]],
        "chars_in": chars_in,
        "chars_out": chars_out,
    }


def render(turns: list, source: str, summary: dict) -> str:
    named = [s for s in summary["speakers"] if s["name"] != "(unlabeled)"]
    lines = [
        f"# Transcript: {Path(source).stem}",
        f"Source: {Path(source).name} · Duration {summary['duration']} · {len(named)} speakers",
        "",
    ]
    for turn in turns:
        who = f"{turn['speaker']}: " if turn["speaker"] else ""
        lines += [f"[{clock(turn['start'])}] {who}{turn['text']}", ""]
    return "\n".join(lines)


def describe(summary: dict, out_path: str) -> str:
    reduction = 100 - round(100 * summary["chars_out"] / max(summary["chars_in"], 1))
    lines = [
        f"Transcript: {out_path or 'stdout'} ({summary['chars_out']:,} chars, "
        f"{reduction}% smaller than the {summary['chars_in']:,}-char VTT)",
        f"Duration: {summary['duration']} · {summary['cues']} cues merged into {summary['turns']} turns",
        "Speakers (by words):",
    ]
    for s in summary["speakers"]:
        flag = "  <- looks like a room or device; ask who it was" if s["looks_like_room_or_device"] else ""
        lines.append(f"  {s['name']}: {s['words']:,} words ({s['share']}%), {s['turns']} turns{flag}")
    return "\n".join(lines)


def main(argv: list = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("vtt", help="path to the .vtt file")
    parser.add_argument("-o", "--out", help="write the Markdown transcript here")
    parser.add_argument("--rename", action="append", default=[], metavar="OLD=NEW",
                        help="replace a speaker label (repeatable), e.g. 'Room 4B=Dana Lee'")
    parser.add_argument("--json", action="store_true", help="print the summary as JSON")
    args = parser.parse_args(argv)

    renames = {}
    for pair in args.rename:
        if "=" not in pair:
            parser.error(f"--rename expects OLD=NEW, got {pair!r}")
        old, new = pair.split("=", 1)
        renames[old.strip()] = new.strip()

    source = Path(args.vtt)
    text = source.read_text(encoding="utf-8-sig", errors="replace")
    cues = parse_cues(text)
    if not cues:
        print(f"No cues found in {source}; is it a WebVTT file?", file=sys.stderr)
        return 1
    turns = merge_turns(cues, renames)
    transcript = render(turns, str(source), summarize(turns, cues, len(text), 0))
    summary = summarize(turns, cues, len(text), len(transcript))

    if args.out:
        Path(args.out).write_text(transcript, encoding="utf-8")
    if args.json:
        print(json.dumps(summary, indent=2))
    elif args.out:
        print(describe(summary, args.out))
    else:
        print(transcript)
        print(describe(summary, ""), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
