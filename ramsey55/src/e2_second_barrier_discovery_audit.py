#!/usr/bin/env python3
"""Audit and quotient E=2 endpoints from the second-barrier search."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from e2_low_closure_isomorphism_audit import (  # noqa: E402
    ORDER,
    canonicalize,
    graph6_lines,
    normalized_labels,
    partition,
    sha256_file,
    size_histogram,
)
from graph_io import complement, decode_graph6, encode_graph6  # noqa: E402


SCHEMA = "ramsey55.e2_second_barrier_discovery_audit.v1"
FULL_MASK = (1 << ORDER) - 1


def five_cliques(adjacency: list[int]) -> list[tuple[int, ...]]:
    result: list[tuple[int, ...]] = []

    def recurse(
        candidates: int, selected: tuple[int, ...]
    ) -> None:
        needed = 5 - len(selected)
        if candidates.bit_count() < needed:
            return
        if needed == 0:
            result.append(selected)
            return
        while candidates:
            low = candidates & -candidates
            vertex = low.bit_length() - 1
            candidates ^= low
            recurse(
                candidates & adjacency[vertex],
                selected + (vertex,),
            )

    recurse(FULL_MASK, ())
    return result


def e2_geometry(graph: str) -> tuple[str, list[tuple[int, ...]], list[tuple[int, ...]]]:
    adjacency = decode_graph6(graph)
    cliques = five_cliques(adjacency)
    independent = five_cliques(complement(adjacency))
    if len(cliques) + len(independent) != 2:
        raise ValueError(
            f"endpoint has objective {len(cliques) + len(independent)}, not two"
        )
    if len(cliques) == 2:
        overlap = len(set(cliques[0]) & set(cliques[1]))
        geometry = f"same_colour_pair;overlap={overlap}"
    elif len(independent) == 2:
        overlap = len(set(independent[0]) & set(independent[1]))
        geometry = f"same_colour_pair;overlap={overlap}"
    else:
        overlap = len(set(cliques[0]) & set(independent[0]))
        geometry = f"1,1;cross_overlap={overlap}"
    return geometry, cliques, independent


def write_stream(path: Path, graphs: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(graph + "\n" for graph in graphs), encoding="ascii"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--discoveries", type=Path, required=True)
    parser.add_argument("--known-directory", type=Path, required=True)
    parser.add_argument("--labelg", type=Path, required=True)
    parser.add_argument("--representatives", type=Path, required=True)
    parser.add_argument("--novel-representatives", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    discoveries = graph6_lines(args.discoveries)
    known_paths = sorted(args.known_directory.glob("line_*.g6"))
    if len(known_paths) != 22:
        raise ValueError(
            f"expected 22 known E=2 seed files, found {len(known_paths)}"
        )
    known = [
        graph6_lines(path)[0]
        for path in known_paths
    ]

    geometry_by_input: list[str] = []
    geometry_counts: Counter[str] = Counter()
    for graph in discoveries:
        geometry, _cliques, _independent = e2_geometry(graph)
        geometry_by_input.append(geometry)
        geometry_counts[geometry] += 1
    for graph in known:
        e2_geometry(graph)

    all_graphs = discoveries + known
    all_duals = [
        # The graph I/O implementation validates simplicity while complementing.
        encode_graph6(complement(decode_graph6(graph)))
        for graph in all_graphs
    ]
    with tempfile.TemporaryDirectory(
        prefix="ramsey55-e2-second-barrier-audit."
    ) as directory:
        temporary = Path(directory)
        dense = canonicalize(
            all_graphs,
            labelg=args.labelg,
            sparse=False,
            directory=temporary,
            tag="dense",
        )
        dense_duals = canonicalize(
            all_duals,
            labelg=args.labelg,
            sparse=False,
            directory=temporary,
            tag="dense_dual",
        )
        sparse = canonicalize(
            all_graphs,
            labelg=args.labelg,
            sparse=True,
            directory=temporary,
            tag="sparse",
        )
        sparse_duals = canonicalize(
            all_duals,
            labelg=args.labelg,
            sparse=True,
            directory=temporary,
            tag="sparse_dual",
        )

    dense_normalized = normalized_labels(dense, dense_duals)
    sparse_normalized = normalized_labels(sparse, sparse_duals)
    if partition(dense) != partition(sparse):
        raise AssertionError("dense/sparse ordinary partitions disagree")
    if partition(dense_normalized) != partition(sparse_normalized):
        raise AssertionError(
            "dense/sparse complement partitions disagree"
        )

    discovery_count = len(discoveries)
    dense_known = set(dense_normalized[discovery_count:])
    sparse_known = set(sparse_normalized[discovery_count:])
    dense_novel_flags = [
        label not in dense_known
        for label in dense_normalized[:discovery_count]
    ]
    sparse_novel_flags = [
        label not in sparse_known
        for label in sparse_normalized[:discovery_count]
    ]
    if dense_novel_flags != sparse_novel_flags:
        raise AssertionError("dense/sparse novelty decisions disagree")

    discovery_labels = dense_normalized[:discovery_count]
    representatives = sorted(set(discovery_labels))
    novel_representatives = sorted(
        {
            label
            for label, novel in zip(
                discovery_labels, dense_novel_flags, strict=True
            )
            if novel
        }
    )
    representative_geometry: dict[str, set[str]] = {}
    for label, geometry in zip(
        discovery_labels, geometry_by_input, strict=True
    ):
        representative_geometry.setdefault(label, set()).add(geometry)
    if any(len(values) != 1 for values in representative_geometry.values()):
        raise AssertionError(
            "one complement-isomorphism class has inconsistent geometry"
        )

    # Recount the canonical labels themselves, rather than trusting that labelg
    # preserved the semantic objective.
    representative_geometry_counts: Counter[str] = Counter()
    for graph in representatives:
        geometry, _cliques, _independent = e2_geometry(graph)
        representative_geometry_counts[geometry] += 1

    write_stream(args.representatives, representatives)
    write_stream(args.novel_representatives, novel_representatives)
    result = {
        "schema": SCHEMA,
        "status": (
            "REPRODUCIBLE_E2_ENDPOINT_CLASSIFICATION_"
            "NO_CONSTRUCTION_CLAIM"
        ),
        "evidence_label": "REPRODUCIBLE COMPUTATIONAL OBSERVATION",
        "valid": True,
        "source_sha256": sha256_file(Path(__file__)),
        "discovery_path": str(args.discoveries.resolve()),
        "discovery_sha256": sha256_file(args.discoveries),
        "discovery_count": discovery_count,
        "known_seed_count": len(known),
        "known_seed_corpus_sha256": hashlib.sha256(
            b"".join(path.read_bytes() for path in known_paths)
        ).hexdigest(),
        "all_endpoints_independently_recounted_to_E2": True,
        "labeled_geometry_counts": dict(sorted(geometry_counts.items())),
        "dense_sparse_ordinary_partition_match": True,
        "dense_sparse_complement_partition_match": True,
        "dense_sparse_novelty_decisions_match": True,
        "known_complement_isomorphism_class_count": len(dense_known),
        "discovery_ordinary_isomorphism_class_count": len(
            partition(dense[:discovery_count])
        ),
        "discovery_complement_isomorphism_class_count": len(
            representatives
        ),
        "discovery_complement_class_size_histogram": size_histogram(
            discovery_labels
        ),
        "novel_labeled_endpoint_count": sum(dense_novel_flags),
        "novel_complement_isomorphism_class_count": len(
            novel_representatives
        ),
        "representative_geometry_counts": dict(
            sorted(representative_geometry_counts.items())
        ),
        "representative_path": str(args.representatives.resolve()),
        "representative_sha256": sha256_file(args.representatives),
        "novel_representative_path": str(
            args.novel_representatives.resolve()
        ),
        "novel_representative_sha256": sha256_file(
            args.novel_representatives
        ),
        "labelg_path": str(args.labelg.resolve()),
        "labelg_sha256": sha256_file(args.labelg),
        "claim_boundary": (
            "This classifies only the 1,670 retained E=2 endpoints and "
            "compares them with the supplied 22 known near misses. It is "
            "not a classification of all E=2 graphs and makes no Ramsey "
            "existence or nonexistence claim."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
