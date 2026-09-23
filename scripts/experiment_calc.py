#!/usr/bin/env python3
"""Experiment math for hypothesis validation: sample size, duration and
significance for A/B tests. Stdlib only.

    python3 scripts/experiment_calc.py sample-size --baseline 0.12 --mde 0.02
    python3 scripts/experiment_calc.py sample-size --baseline 0.12 --mde 10% --daily-traffic 4000
    python3 scripts/experiment_calc.py sample-size-mean --sd 42 --mde 5
    python3 scripts/experiment_calc.py significance --control 120/1000 --variant 150/1000

--mde is absolute (0.02 = +2 percentage points) unless it ends in % (relative lift).
Two-sided tests at alpha 0.05 and power 0.8 unless you say otherwise.
"""
from __future__ import annotations

import argparse
import math
import sys
from statistics import NormalDist

Z = NormalDist()


def z_alpha(alpha: float, one_sided: bool) -> float:
    return Z.inv_cdf(1 - alpha if one_sided else 1 - alpha / 2)


def parse_mde(raw: str, baseline: float) -> float:
    """Absolute effect size; '10%' means a 10% relative lift on the baseline."""
    raw = raw.strip()
    return baseline * float(raw[:-1]) / 100 if raw.endswith("%") else float(raw)


def sample_size_proportions(p1: float, p2: float, alpha: float, power: float, one_sided: bool) -> int:
    """Per-variant n for a two-proportion z-test (pooled null variance, no continuity correction)."""
    pbar = (p1 + p2) / 2
    numerator = (z_alpha(alpha, one_sided) * math.sqrt(2 * pbar * (1 - pbar))
                 + Z.inv_cdf(power) * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return math.ceil(numerator / (p2 - p1) ** 2)


def sample_size_means(sd: float, delta: float, alpha: float, power: float, one_sided: bool) -> int:
    """Per-variant n to detect a difference in means of `delta` with common SD `sd`."""
    return math.ceil(2 * ((z_alpha(alpha, one_sided) + Z.inv_cdf(power)) * sd / delta) ** 2)


def duration_days(per_variant: int, variants: int, daily_traffic: float, allocation: float) -> int:
    return math.ceil(per_variant * variants / (daily_traffic * allocation))


def two_proportion_test(c_conv: int, c_n: int, v_conv: int, v_n: int, alpha: float) -> dict:
    p1, p2 = c_conv / c_n, v_conv / v_n
    pooled = (c_conv + v_conv) / (c_n + v_n)
    se_pooled = math.sqrt(pooled * (1 - pooled) * (1 / c_n + 1 / v_n))
    z = (p2 - p1) / se_pooled if se_pooled else 0.0
    p_value = 2 * (1 - Z.cdf(abs(z)))
    se_diff = math.sqrt(p1 * (1 - p1) / c_n + p2 * (1 - p2) / v_n)
    margin = Z.inv_cdf(1 - alpha / 2) * se_diff
    return {"p1": p1, "p2": p2, "diff": p2 - p1, "relative": (p2 - p1) / p1 if p1 else float("inf"),
            "z": z, "p_value": p_value, "ci": (p2 - p1 - margin, p2 - p1 + margin),
            "significant": p_value < alpha}


def ratio(raw: str) -> tuple:
    conversions, _, total = raw.partition("/")
    try:
        return int(conversions), int(total)
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected CONVERSIONS/TOTAL such as 120/1000, got {raw!r}")


def main(argv: list = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--alpha", type=float, default=0.05)
    common.add_argument("--power", type=float, default=0.8)
    common.add_argument("--one-sided", action="store_true")
    common.add_argument("--comparisons", type=int, default=1,
                        help="variants compared against control; alpha is Bonferroni-split across them")
    common.add_argument("--daily-traffic", type=float, default=0, help="eligible users per day, for a duration estimate")
    common.add_argument("--allocation", type=float, default=1.0, help="share of traffic in the experiment (0-1)")

    p = sub.add_parser("sample-size", parents=[common], help="conversion-rate metrics")
    p.add_argument("--baseline", type=float, required=True, help="control conversion rate, e.g. 0.12")
    p.add_argument("--mde", required=True, help="minimum detectable effect: 0.02 absolute or 10%% relative")
    m = sub.add_parser("sample-size-mean", parents=[common], help="continuous metrics (time, revenue)")
    m.add_argument("--sd", type=float, required=True, help="standard deviation of the metric")
    m.add_argument("--mde", type=float, required=True, help="smallest difference in means worth detecting")
    s = sub.add_parser("significance", help="two-proportion z-test on observed results")
    s.add_argument("--control", required=True, type=ratio, metavar="CONV/N", help="e.g. 120/1000")
    s.add_argument("--variant", required=True, type=ratio, metavar="CONV/N", help="e.g. 150/1000")
    s.add_argument("--alpha", type=float, default=0.05)
    args = parser.parse_args(argv)

    if args.command == "significance":
        (c_conv, c_n), (v_conv, v_n) = args.control, args.variant
        if not (0 <= c_conv <= c_n and 0 <= v_conv <= v_n and c_n and v_n):
            parser.error("use CONVERSIONS/TOTAL with 0 <= conversions <= total")
        r = two_proportion_test(c_conv, c_n, v_conv, v_n, args.alpha)
        low, high = r["ci"]
        print(f"Control {r['p1']:.2%} vs variant {r['p2']:.2%}: {r['diff'] * 100:+.2f} pts "
              f"({r['relative']:+.1%} relative)")
        print(f"z = {r['z']:.2f}, two-sided p = {r['p_value']:.4f}; "
              f"{1 - args.alpha:.0%} CI for the difference: {low * 100:+.2f} to {high * 100:+.2f} pts")
        verdict = "Significant" if r["significant"] else "Not significant"
        print(f"{verdict} at alpha {args.alpha:g}. Valid only if the sample size was fixed before "
              "looking; stopping when p first dips below alpha inflates false positives.")
        return 0

    if args.comparisons < 1:
        parser.error("--comparisons must be at least 1")
    if not 0 < args.allocation <= 1:
        parser.error("--allocation must be between 0 and 1")
    alpha = args.alpha / args.comparisons
    variants = args.comparisons + 1
    if args.command == "sample-size":
        if not 0 < args.baseline < 1:
            parser.error("--baseline must be between 0 and 1")
        effect = parse_mde(args.mde, args.baseline)
        target = args.baseline + effect
        if effect == 0 or not 0 < target < 1:
            parser.error("baseline + mde must stay between 0 and 1, and mde must be non-zero")
        n = sample_size_proportions(args.baseline, target, alpha, args.power, args.one_sided)
        print(f"Detect {args.baseline:.2%} → {target:.2%} ({effect * 100:+.2f} pts, "
              f"{effect / args.baseline:+.1%} relative)")
    else:
        if args.sd <= 0 or args.mde == 0:
            parser.error("--sd must be > 0 and --mde non-zero")
        n = sample_size_means(args.sd, abs(args.mde), alpha, args.power, args.one_sided)
        print(f"Detect a difference of {args.mde:g} in means (SD {args.sd:g})")
    sides = "one-sided" if args.one_sided else "two-sided"
    split = f" (alpha {args.alpha:g} split across {args.comparisons} comparisons)" if args.comparisons > 1 else ""
    print(f"Needs {n:,} per variant, {n * variants:,} total, at alpha {alpha:.4g} {sides}, "
          f"power {args.power:.0%}{split}")
    if args.daily_traffic:
        days = duration_days(n, variants, args.daily_traffic, args.allocation)
        print(f"At {args.daily_traffic:,.0f} eligible users/day with {args.allocation:.0%} allocated: "
              f"~{days} days (run at least one full week to cover weekday cycles)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
