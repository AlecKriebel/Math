#!/usr/bin/env python3
"""Exhaustive exact minimality certificate within the unweighted G(c,m) family."""

from __future__ import annotations

import argparse
import hashlib

from verify_clique_pendant_product import complete_baselines, exact_fixation


def normalized_ratios(c, m):
    n = c + m + 1
    bd = exact_fixation(c, m, "Bd")[0]
    db = exact_fixation(c, m, "dB")[0]
    base_bd, base_db = complete_baselines(n)
    return bd / base_bd, db / base_db


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--witness-n", type=int, default=36)
    args = parser.parse_args()
    witness_n = args.witness_n
    assert witness_n == 36, "the checked theorem below is specifically n=36"

    transcript = []
    global_best = None
    smallest_one_third_slack = None
    for n in range(3, witness_n + 1):
        level_best = None
        positives = []
        for m in range(1, n - 1):
            c = n - m - 1
            x, y = normalized_ratios(c, m)
            gap = x * y - 1
            one_third_slack = 1 - (x + 2 * y) / 3
            assert one_third_slack > 0
            if (
                smallest_one_third_slack is None
                or one_third_slack < smallest_one_third_slack[0]
            ):
                smallest_one_third_slack = (one_third_slack, n, c, m)
            record = (gap, c, m)
            if level_best is None or gap > level_best[0]:
                level_best = record
            if gap > 0:
                positives.append((c, m, gap))
            transcript.append(
                f"{n},{c},{m},{gap.numerator}/{gap.denominator},"
                f"{one_third_slack.numerator}/{one_third_slack.denominator}\n"
            )

        assert level_best is not None
        if n < witness_n:
            assert not positives
        else:
            assert len(positives) == 1
            assert positives[0][0:2] == (31, 4)
        if global_best is None or level_best[0] > global_best[0]:
            global_best = (level_best[0], n, level_best[1], level_best[2])
        print(
            f"n={n:2d}: max gap={float(level_best[0]): .12g} "
            f"at G({level_best[1]},{level_best[2]})"
        )

    certificate_hash = hashlib.sha256("".join(transcript).encode()).hexdigest()
    assert global_best[1:] == (36, 31, 4)
    print("PASS exact exhaustive minimality in the unweighted G(c,m) family")
    print("PASS exact lambda=1/3 separator on every checked pair")
    print(
        "smallest lambda=1/3 slack:",
        float(smallest_one_third_slack[0]),
        "at",
        f"G({smallest_one_third_slack[2]},{smallest_one_third_slack[3]})",
    )
    print("checked parameter pairs:", len(transcript))
    print("exact transcript SHA256:", certificate_hash)


if __name__ == "__main__":
    main()
