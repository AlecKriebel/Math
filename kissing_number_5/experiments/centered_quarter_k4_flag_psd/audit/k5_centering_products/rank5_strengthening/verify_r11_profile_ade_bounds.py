#!/usr/bin/env python3
"""Exact arithmetic application of the ADE defect bounds to all r11 profiles."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterable


PROFILE_NAME = "r11_quarter_grid_global_profiles.json"
PROFILE_SHA256 = (
    "b94c2a9757ca43a9a1bac2bf315877843e94c174e1e5c523b7902ebec7b2d612"
)
EDGE_COLORS = (-4, -3, -2, -1, 0, 1, 2)
EXPECTED_GROUP_SIZES = {
    2362: 10,
    2363: 9,
    2364: 9,
    2365: 4,
    2366: 4,
    2367: 1,
    2368: 1,
}


def load_profiles(path: Path) -> dict:
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != PROFILE_SHA256:
        raise ValueError(f"profile SHA-256 mismatch: {digest}")
    return json.loads(raw)


def validate_profile(profile: Iterable[int], q: int) -> tuple[int, ...]:
    counts = tuple(profile)
    if len(counts) != len(EDGE_COLORS):
        raise ValueError("an edge profile must have seven entries")
    if any(not isinstance(value, int) or value < 0 for value in counts):
        raise ValueError("edge counts must be nonnegative integers")
    if sum(counts) != 820:
        raise ValueError("edge counts must sum to 820")
    if counts[0] != 11:
        raise ValueError("r11 profile must have eleven antipodal edges")
    observed_q = sum(
        color * color * count
        for color, count in zip(EDGE_COLORS, counts)
    )
    if observed_q != q:
        raise ValueError(f"profile has Q={observed_q}, expected {q}")
    if counts[5] > 6:
        raise ValueError("ADE audit requires the certified m_{+1} <= 6")
    return counts


def verify_ade_arithmetic(m_plus_one: int) -> None:
    """Check every possible line-line defect count allowed by this profile."""

    max_defects = m_plus_one // 2
    if max_defects > 3:
        raise AssertionError("more than three line-line defects are possible")

    for defects in range(max_defects + 1):
        if defects:
            # A minimum vertex cover has 1 <= d <= e.  If the integral
            # remainder had rank four, character supports would force at
            # least d(5-d) crossing defects.
            for cover_size in range(1, defects + 1):
                forced_crossing = cover_size * (5 - cover_size)
                if forced_crossing <= defects:
                    raise AssertionError(
                        "rank-four defect-cover contradiction failed"
                    )

        # If the integral remainder has rank five, its norm-two dual shell
        # has at most 20 antipodal lines.  With k=11-d selected lines and
        # at most 6-2e exceptional residuals, the worst case is d=e.
        worst_rank_five_residual = 15 - defects
        if worst_rank_five_residual >= 19:
            raise AssertionError("rank-five residual bound failed")

    # In the sole rank-four case e=0, every exceptional residual consumes
    # at least five +1 edges.
    max_exceptional = m_plus_one // 5
    if max_exceptional > 1:
        raise AssertionError("too many rank-four exceptional residuals")
    ordinary = 19 - max_exceptional
    # At most one ordinary vector has height zero.  The rest split over the
    # two height signs, each of which has capacity eight.
    forced_one_layer = (ordinary - 1 + 1) // 2
    if forced_one_layer <= 8:
        raise AssertionError("rank-four layer contradiction failed")


def verify_export(data: dict) -> dict[str, int]:
    if data.get("schema") != "quarter-grid-r11-global-edge-profiles-v1":
        raise ValueError("unexpected profile schema")
    if tuple(data["normalization"]["edge_order"]) != EDGE_COLORS:
        raise ValueError("unexpected edge order")
    grouped = data.get("profiles")
    if not isinstance(grouped, dict):
        raise ValueError("profiles must be grouped by Q")

    observed_sizes = {int(q): len(rows) for q, rows in grouped.items()}
    if observed_sizes != EXPECTED_GROUP_SIZES:
        raise ValueError((observed_sizes, EXPECTED_GROUP_SIZES))

    seen = set()
    maximum_plus_one = 0
    for q_text, rows in grouped.items():
        q = int(q_text)
        for row in rows:
            counts = validate_profile(row, q)
            if counts in seen:
                raise ValueError("global profile export contains a duplicate")
            seen.add(counts)
            maximum_plus_one = max(maximum_plus_one, counts[5])
            verify_ade_arithmetic(counts[5])
    if len(seen) != 38:
        raise AssertionError(f"expected 38 profiles, found {len(seen)}")
    if maximum_plus_one != 6:
        raise AssertionError(
            f"expected maximum m_+1=6, found {maximum_plus_one}"
        )
    return {
        "profiles": len(seen),
        "maximum_plus_one": maximum_plus_one,
        "q_groups": len(grouped),
    }


def self_test() -> dict[str, int]:
    path = Path(__file__).with_name(PROFILE_NAME)
    summary = verify_export(load_profiles(path))

    bad_total = [11, 41, 186, 54, 271, 0, 256]
    try:
        validate_profile(bad_total, 2367)
    except ValueError:
        pass
    else:
        raise AssertionError("wrong-total tamper was not rejected")

    # This tamper preserves total mass and Q=2363 by moving one edge from
    # color -1 to color +1, but violates the certified +1 cap.
    bad_plus_one = [11, 41, 184, 59, 264, 7, 254]
    try:
        validate_profile(bad_plus_one, 2363)
    except ValueError:
        pass
    else:
        raise AssertionError("+1-budget tamper was not rejected")
    return summary


def main() -> None:
    summary = self_test()
    print(
        "PASS: r11 ADE bounds cover "
        f"{summary['profiles']} profiles in {summary['q_groups']} Q-groups; "
        f"max m_+1={summary['maximum_plus_one']}"
    )


if __name__ == "__main__":
    main()
