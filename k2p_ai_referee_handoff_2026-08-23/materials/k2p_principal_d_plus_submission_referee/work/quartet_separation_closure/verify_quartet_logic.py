#!/usr/bin/env python3
"""Finite logical replay of the displayed-quartet sign separation theorem."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
TOPOLOGIES = ("12|34", "13|24", "14|23")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def separating_witness(left: frozenset[str], right: frozenset[str]) -> dict[str, object]:
    require(left and right and left != right, "sets must be distinct and nonempty")
    if len(left) == 1:
        singleton = next(iter(left))
        if not right <= left:
            return {"orientation": "left_zero_right_positive", "family": "F", "zero_set": [singleton]}
    if len(right) == 1:
        singleton = next(iter(right))
        if not left <= right:
            return {"orientation": "right_zero_left_positive", "family": "F", "zero_set": [singleton]}
    present_only_right = sorted(right - left)
    if present_only_right:
        chosen = present_only_right[0]
        return {
            "orientation": "left_zero_right_positive",
            "family": "G",
            "positive_topology": chosen,
            "zero_set": sorted(set(TOPOLOGIES) - {chosen}),
        }
    chosen = sorted(left - right)[0]
    return {
        "orientation": "right_zero_left_positive",
        "family": "G",
        "positive_topology": chosen,
        "zero_set": sorted(set(TOPOLOGIES) - {chosen}),
    }


def main() -> None:
    if not __debug__:
        raise SystemExit("QUARTET_LOGIC_OPTIMIZED_MODE_FORBIDDEN")
    sets = [
        frozenset(TOPOLOGIES[index] for index in range(3) if mask >> index & 1)
        for mask in range(1, 8)
    ]
    rows = []
    for left, right in itertools.combinations(sets, 2):
        witness = separating_witness(left, right)
        zero = set(witness["zero_set"])
        if witness["orientation"] == "left_zero_right_positive":
            require(left <= zero and bool(right - zero), "witness does not separate in stated direction")
        else:
            require(right <= zero and bool(left - zero), "witness does not separate in stated direction")
        rows.append({"left": sorted(left), "right": sorted(right), **witness})
    require(len(rows) == 21, "did not cover every unordered pair of displayed sets")
    payload = {
        "schema": "k2p-displayed-quartet-sign-logic-v1",
        "domain": "positive inheritance weights and 0<all K2P nonzero edge eigenvalues<1",
        "source_theorem": "Englander et al. (2026), Propositions 2.9-2.10 and Theorem 2.11",
        "displayed_set_count": 7,
        "unequal_pair_count": 21,
        "rows": rows,
    }
    payload_hash = hashlib.sha256(canonical(payload)).hexdigest()
    cert = dict(payload)
    cert["payload_sha256"] = payload_hash
    output = HERE / "quartet_logic_certificate.json"
    output.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    print("K2P_QUARTET_SIGN_LOGIC_PASS")
    print(json.dumps({"payload_sha256": payload_hash, "pairs": len(rows)}, sort_keys=True))


if __name__ == "__main__":
    main()
