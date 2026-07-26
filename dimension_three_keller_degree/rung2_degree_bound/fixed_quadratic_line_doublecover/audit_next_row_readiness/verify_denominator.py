#!/usr/bin/env python3
"""Dependency-free consistency check for the readiness denominator.

This verifies the finite combinatorics recorded in ``denominator.json``.
It is not a proof of the Hilbert--Burch theorem or of any lower exclusion.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "denominator.json").read_text())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


require(DATA["row"] == "Q2-E2-A1-B2-D1-N2", "wrong parent row")

strata = DATA["stable_strata"]
require([item["id"] for item in strata] == [f"L{i:02d}" for i in range(9)],
        "stable IDs are not exactly L00--L08")
require(len({item["condition"] for item in strata}) == 9,
        "duplicate stable condition")

statuses = Counter(item["status"] for item in strata)
require(statuses == {"covered": 3, "provisional": 3, "open": 3},
        f"unexpected readiness counts: {statuses}")

# Independently enumerate the nonexceptional Hilbert--Burch shapes:
# unordered pairs 0 <= k2 <= k1 <= 2, grouped by delta=k1+k2.
hb_shapes = sorted(
    (k1 + k2, (k1, k2))
    for k1 in range(3)
    for k2 in range(k1 + 1)
)
require(
    hb_shapes
    == [
        (0, (0, 0)),
        (1, (1, 0)),
        (2, (1, 1)),
        (2, (2, 0)),
        (3, (2, 1)),
        (4, (2, 2)),
    ],
    f"wrong Hilbert--Burch shape list: {hb_shapes}",
)

expected_conditions = {
    "delta=0, k={0,0}",
    "delta=1, k={1,0}",
    "delta=2, k={2,0}",
    "delta=2, k={1,1}",
    "delta=3, k={2,1}",
    "delta=4, k={2,2}",
}
for suffix in expected_conditions:
    require(sum(suffix in item["condition"] for item in strata) == 1,
            f"missing or repeated shape {suffix}")

fixed = DATA["fixed_divisor_charts"]
require(len(fixed) == 4, "binary quadratic quotient must have four charts")
require(len({item["id"] for item in fixed}) == 4,
        "duplicate fixed-divisor chart")

# The local valuation bookkeeping at exact delta=2 yields, by fixed-divisor
# orbit, 2+2+5+4+2 shape-{1,1} mechanism families.  Three exceptional
# subloci have shape {2,0}.
d2 = DATA["delta2_chart_families"]
shape11 = d2["shape_11"]
require(
    shape11["total"]
    == sum(
        shape11[key]
        for key in (
            "branch_square",
            "two_branch",
            "one_branch",
            "squarefree_interior",
            "doubled_nonbranch",
        )
    )
    == 15,
    "wrong exact-delta=2 shape-{1,1} chart count",
)
require(shape11["provisional"] + shape11["open"] == shape11["total"],
        "shape-{1,1} status count does not close")

shape20 = d2["shape_20"]
require(shape20["total"] == 3, "wrong shape-{2,0} chart count")
require(shape20["provisional"] + shape20["open"] == shape20["total"],
        "shape-{2,0} status count does not close")
require(shape11["total"] + shape20["total"] == 18,
        "wrong terminal exact-delta=2 chart-family count")

print("NEXT_ROW_DENOMINATOR_PASS_9_STRATA_18_DELTA2_CHARTS")
