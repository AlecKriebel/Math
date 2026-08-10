#!/usr/bin/env python3
"""Verify that every local atlas invariant descends through arm scaling."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path

from jc_tensor import invariant_orbit, jc_representatives, parse_literal


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
TEMPLATES = PROJECT / "strong_level2_phylo_identifiability" / "src" / "jc_root_spanning_atlas_data.py"
SEVENTH = HERE / "seventh_invariant.json"
OUT = HERE / "certificates" / "invariant_multihomogeneity.json"


def main() -> None:
    templates = parse_literal(TEMPLATES, "INVARIANT_TEMPLATES")
    seventh = json.loads(SEVENTH.read_text())["invariant"]
    seventh = tuple(
        (tuple(int(index) + 1 for index in monomial), int(coefficient))
        for coefficient, monomial in seventh
    )
    orbit = invariant_orbit((*templates, seventh))
    coordinates = jc_representatives()
    rows = []
    failures = []
    degree_counts = Counter()
    for index, invariant in enumerate(orbit):
        degrees = {
            tuple(sum(coordinates[coordinate][port] != 0 for coordinate in monomial) for port in range(4))
            for monomial, _coefficient in invariant
        }
        if len(degrees) != 1:
            failures.append({"invariant": index, "degrees": sorted(degrees)})
            continue
        degree = next(iter(degrees))
        degree_counts[degree] += 1
        rows.append({
            "index": index,
            "port_arm_multidegree": degree,
            "invariant_sha256": hashlib.sha256(repr(invariant).encode()).hexdigest(),
        })
    payload = {
        "schema": 1,
        "invariant_count": len(orbit),
        "all_multihomogeneous": not failures and len(rows) == len(orbit),
        "degree_distribution": {repr(key): value for key, value in sorted(degree_counts.items())},
        "records": rows,
        "failures": failures,
        "consequence": "zero/nonzero and strict-sign status is invariant under every positive port-incidence scaling",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    if not payload["all_multihomogeneous"]:
        raise SystemExit("multihomogeneity failed")
    print(json.dumps({"output": str(OUT), "invariants": len(orbit)}, sort_keys=True))


if __name__ == "__main__":
    main()
