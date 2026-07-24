#!/usr/bin/env python3
"""Dependency-free arithmetic checks for antipodal/deep-graph branches."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CERTIFICATE = (
    ROOT / "certificates" / "antipodal_deep_graph_branches.json"
)


class VerificationError(Exception):
    """Raised when a certificate field fails an exact check."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def verify(path: Path = DEFAULT_CERTIFICATE) -> dict[str, object]:
    data = json.loads(path.read_text())
    require(
        data.get("schema")
        == "kissing5.antipodal_deep_graph_branches.v1",
        "unexpected schema",
    )
    order = data.get("order")
    independence = data.get("independence_upper")
    require(order == 41, "unexpected graph order")
    require(independence == 20, "unexpected independence bound")
    branches = data.get("branches")
    require(isinstance(branches, list), "branches must be a list")
    require(len(branches) == 19, "expected branches r=0,...,18")

    for expected_r, branch in enumerate(branches):
        require(branch.get("r") == expected_r, "branch order mismatch")
        residual_vertices = order - 2 * expected_r
        residual_independence = independence - expected_r
        deep_edge_upper = (
            expected_r + residual_independence * residual_independence + 1
        )
        require(
            branch.get("residual_vertices") == residual_vertices,
            f"wrong residual vertex count at r={expected_r}",
        )
        require(
            branch.get("residual_independence_upper")
            == residual_independence,
            f"wrong residual independence bound at r={expected_r}",
        )
        require(
            branch.get("deep_edge_upper") == deep_edge_upper,
            f"wrong deep-edge bound at r={expected_r}",
        )

    require(
        branches[18]["deep_edge_upper"] == 23,
        "r=18 endpoint must meet the universal 23-edge lower bound",
    )
    return {
        "status": "PASS",
        "branches_checked": len(branches),
        "r15_deep_edge_upper": branches[15]["deep_edge_upper"],
        "r16_deep_edge_upper": branches[16]["deep_edge_upper"],
        "r17_deep_edge_upper": branches[17]["deep_edge_upper"],
        "r18_deep_edge_upper": branches[18]["deep_edge_upper"],
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
