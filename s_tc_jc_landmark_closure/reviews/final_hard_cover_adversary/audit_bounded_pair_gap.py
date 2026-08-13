#!/usr/bin/env python3
"""Fail-closed audit of the missing unequal bounded-atlas relation records.

The hard-cover streams refine only equal selected invariant decks.  A complete
directed-containment atlas also needs a graph-bound separator for every
unequal necessary direction.  This verifier independently rebuilds those
signature directions at n=3 and n=4 and then checks for the advertised
pair-level relation and sign-library artifacts.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import time

from audit_hard_cover import PROJECT, build_inventory, file_sha
from cleanroom_core import stable_hash


HERE = Path(__file__).resolve().parent


def necessary_pairs(sources: tuple[int, ...], targets: tuple[int, ...]):
    rows = tuple(
        (source, target)
        for source in sources
        for target in targets
        if source & ~target == 0
    )
    equal = tuple(row for row in rows if row[0] == row[1])
    unequal = tuple(row for row in rows if row[0] != row[1])
    return rows, equal, unequal


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "bounded_pair_gap_certificate.json")
    args = parser.parse_args()
    started = time.monotonic()
    rows = []
    failures = []
    for n in (3, 4):
        inventory = build_inventory(
            selected_outgoing=n,
            recompute_all_descriptor_bits=False,
        )
        pairs, equal, unequal = necessary_pairs(
            inventory.source_signature_values,
            inventory.target_signature_values,
        )
        relation_path = PROJECT / f"primary/certificates/bounded_relations_n{n}.jsonl.gz"
        sign_path = PROJECT / f"primary/certificates/bounded_sign_library_n{n}.json"
        relation_exists = relation_path.exists()
        sign_exists = sign_path.exists()
        if unequal and not relation_exists:
            failures.append({
                "type": "missing_pair_level_relation_stream",
                "n": n,
                "required_unequal_directions": len(unequal),
                "path": str(relation_path.relative_to(PROJECT)),
            })
        if unequal and not sign_exists:
            failures.append({
                "type": "missing_pair_level_sign_library",
                "n": n,
                "required_unequal_directions": len(unequal),
                "path": str(sign_path.relative_to(PROJECT)),
            })
        rows.append({
            "selected_outgoing": n,
            "source_signatures": len(inventory.source_signature_values),
            "target_signatures": len(inventory.target_signature_values),
            "necessary_directed_signature_pairs": len(pairs),
            "equal_pairs": len(equal),
            "unequal_pairs_requiring_exact_separator": len(unequal),
            "pair_commitment_sha256": stable_hash([
                (str(source), str(target)) for source, target in pairs
            ]),
            "unequal_pair_commitment_sha256": stable_hash([
                (str(source), str(target)) for source, target in unequal
            ]),
            "unequal_pair_examples": [
                {
                    "source_signature": str(source),
                    "target_signature": str(target),
                    "source_sha256": __import__("hashlib").sha256(str(source).encode()).hexdigest(),
                    "target_sha256": __import__("hashlib").sha256(str(target).encode()).hexdigest(),
                }
                for source, target in unequal[:10]
            ],
            "required_relation_path": str(relation_path.relative_to(PROJECT)),
            "required_relation_exists": relation_exists,
            "required_relation_sha256": file_sha(relation_path) if relation_exists else None,
            "required_sign_library_path": str(sign_path.relative_to(PROJECT)),
            "required_sign_library_exists": sign_exists,
            "required_sign_library_sha256": file_sha(sign_path) if sign_exists else None,
        })

    payload = {
        "schema": "bounded-unequal-pair-gap-clean-room-v1",
        "status": "FALSE" if failures else "VERIFIED",
        "scope": "all necessary directed signature pairs at selected outgoing sizes three and four",
        "interpretation": (
            "A bit-subset direction is only a necessary containment candidate. "
            "An unequal signature count is not itself a separation proof. Each "
            "direction requires a graph-derived pullback and exact open-domain "
            "separator bound to the fixed source/target presentations."
        ),
        "runs": rows,
        "failures": failures,
        "elapsed_seconds": time.monotonic() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": payload["status"],
        "counts": [
            (row["selected_outgoing"], row["necessary_directed_signature_pairs"], row["unequal_pairs_requiring_exact_separator"])
            for row in rows
        ],
        "failure_count": len(failures),
        "output": str(args.output),
        "sha256": file_sha(args.output),
        "elapsed_seconds": payload["elapsed_seconds"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
