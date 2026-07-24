#!/usr/bin/env python3
"""Generate the exact reduced CNF for circulant (5,5;43) colorings."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter
from pathlib import Path


GENERATOR_ID = "ramsey55_circulant43_exact_cnf_generator_v1"
ORDER = 43
CLIQUE_SIZE = 5
DISTANCE_COUNT = (ORDER - 1) // 2


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def circular_distance(left: int, right: int) -> int:
    forward = (right - left) % ORDER
    backward = (left - right) % ORDER
    return min(forward, backward)


def distance_signatures() -> tuple[tuple[int, ...], ...]:
    signatures: set[tuple[int, ...]] = set()
    for vertices in itertools.combinations(range(ORDER), CLIQUE_SIZE):
        signature = tuple(
            sorted(
                {
                    circular_distance(left, right)
                    for left, right in itertools.combinations(vertices, 2)
                }
            )
        )
        if not signature or not all(1 <= value <= DISTANCE_COUNT for value in signature):
            raise AssertionError("invalid circular-distance signature")
        signatures.add(signature)
    return tuple(sorted(signatures))


def write_cnf(path: Path, signatures: tuple[tuple[int, ...], ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="ascii", newline="\n") as stream:
        stream.write(f"p cnf {DISTANCE_COUNT} {2 * len(signatures)}\n")
        for signature in signatures:
            stream.write(" ".join(str(variable) for variable in signature) + " 0\n")
            stream.write(" ".join(str(-variable) for variable in signature) + " 0\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()

    signatures = distance_signatures()
    write_cnf(args.cnf, signatures)
    histogram = Counter(len(signature) for signature in signatures)
    source = Path(__file__).resolve()
    metadata = {
        "generator": GENERATOR_ID,
        "order": ORDER,
        "clique_size": CLIQUE_SIZE,
        "variable_count": DISTANCE_COUNT,
        "variable_semantics": (
            "variable d is true iff every unordered vertex pair at circular "
            "distance d in Z_43 is a graph edge"
        ),
        "five_set_count": math.comb(ORDER, CLIQUE_SIZE),
        "unreduced_ramsey_clause_count": 2 * math.comb(ORDER, CLIQUE_SIZE),
        "unique_distance_signature_count": len(signatures),
        "clause_count": 2 * len(signatures),
        "signature_size_histogram": {
            str(size): histogram[size] for size in sorted(histogram)
        },
        "reduction_justification": (
            "A five-set is a clique exactly when all distinct circular-distance "
            "variables occurring among its ten pairs are true, and is independent "
            "exactly when they are all false. Duplicate five-sets with the same "
            "distance signature therefore induce identical positive/negative "
            "clauses and may be deduplicated without changing satisfiability."
        ),
        "cnf_path": str(args.cnf.resolve()),
        "cnf_sha256": sha256_file(args.cnf),
        "cnf_bytes": args.cnf.stat().st_size,
        "generator_path": str(source),
        "generator_sha256": sha256_file(source),
    }
    args.metadata.parent.mkdir(parents=True, exist_ok=True)
    args.metadata.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(metadata, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
