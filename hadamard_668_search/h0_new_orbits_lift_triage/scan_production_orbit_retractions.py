#!/usr/bin/env python3
"""Rank completed production orbits by exact lift/retraction invariants.

The scanner is read-only with respect to production output.  It accepts
individual result JSON files, result directories, or a strict aggregate,
extracts every enumerated exact orbit, deduplicates by digest, and derives its
first two ternary lift layers.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import itertools
import json
from pathlib import Path
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
THEORY = SEARCH / "h0_orbit2_quadric_theory"
sys.path[:0] = [str(HERE), str(THEORY), str(SEARCH)]

import search_retracted_newton as lift  # noqa: E402
from verify_lp333_order3_phase_transfer import (  # noqa: E402
    catalog_phase_sum_intersection,
)
from verify_quadric_character_compression import (  # noqa: E402
    nullspace_mod3,
    rank_mod3,
    scalar_value_counts,
)


def parse_int_tuple(value: str) -> tuple[int, ...]:
    return tuple(map(int, value.split(",")))


def result_files(paths: list[Path]) -> tuple[Path, ...]:
    files = []
    for path in paths:
        if path.is_dir():
            files.extend(sorted(path.glob("*.json")))
        else:
            files.append(path)
    return tuple(files)


def extract_records(paths: list[Path]) -> tuple[dict[str, object], ...]:
    by_digest: dict[str, dict[str, object]] = {}
    for path in result_files(paths):
        try:
            payload = path.read_bytes()
            stored = json.loads(payload)
        except (OSError, json.JSONDecodeError):
            continue
        if stored.get("schema") == "dense-shell-production-aggregate-v2":
            shell = stored["shells"]["h0"]
            if (
                not shell.get("complete")
                or shell.get("burnside_weighted_partition_check") != "PASS"
            ):
                raise AssertionError("strict aggregate is incomplete")
            exact_orbits = shell["exact_profile_orbits"]
            if (
                len(exact_orbits)
                != shell["distinct_canonical_exact_profile_orbits"]
            ):
                raise AssertionError("strict aggregate orbit count changed")
            provenance = {
                "aggregate_schema": stored["schema"],
                "aggregate_file_sha256": sha256(payload).hexdigest(),
                "source_sha256": stored["source_sha256"],
                "binary_sha256": stored["binary_sha256"],
                "prefix_shards": shell["prefix_shards"],
                "upper_exact_scope": shell["upper_exact_scope"],
            }
            for exact in exact_orbits:
                if not exact["canonical"] or not exact["exact_zero"]:
                    raise AssertionError("aggregate retained a nonexact orbit")
                record = {
                    "digest": exact["digest"],
                    "ids_a": tuple(map(int, exact["ids_a"])),
                    "ids_b": tuple(map(int, exact["ids_b"])),
                    "target": tuple(map(int, exact["target"])),
                    "target_index": int(exact["target_index"]),
                    "source_shards": tuple(exact["source_shards"]),
                    "production": provenance,
                }
                old = by_digest.get(record["digest"])
                if old is not None and (
                    old["ids_a"],
                    old["ids_b"],
                    old["target"],
                ) != (
                    record["ids_a"],
                    record["ids_b"],
                    record["target"],
                ):
                    raise AssertionError("one digest names two profile records")
                by_digest[record["digest"]] = record
            continue
        if not stored.get("complete") or int(stored.get("returncode", -1)):
            continue
        parsed = stored.get("parsed")
        if not isinstance(parsed, dict):
            continue
        count = int(parsed.get("exact_orbit_count", 0))
        for index in range(count):
            prefix = f"exact_orbit_{index:06d}_"
            if parsed.get(prefix + "present") != "1":
                raise AssertionError("enumerated orbit lost its presence flag")
            digest = str(parsed[prefix + "digest"])
            record = {
                "digest": digest,
                "ids_a": parse_int_tuple(parsed[prefix + "ids_a"]),
                "ids_b": parse_int_tuple(parsed[prefix + "ids_b"]),
                "target": parse_int_tuple(parsed[prefix + "target"]),
                "target_index": int(parsed[prefix + "target_index"]),
                "production": {
                    "path": str(path),
                    "file_sha256": sha256(payload).hexdigest(),
                    "shard_id": stored["shard_id"],
                    "source_sha256": stored["source_sha256"],
                    "binary_sha256": stored["binary_sha256"],
                },
            }
            old = by_digest.get(digest)
            if old is not None:
                if (
                    old["ids_a"],
                    old["ids_b"],
                    old["target"],
                ) != (
                    record["ids_a"],
                    record["ids_b"],
                    record["target"],
                ):
                    raise AssertionError("one digest names two profile records")
                continue
            by_digest[digest] = record
    return tuple(by_digest[key] for key in sorted(by_digest))


def projective_vectors(dimension: int):
    for first in range(dimension):
        for tail in itertools.product(
            range(3), repeat=dimension - first - 1
        ):
            yield (0,) * first + (1,) + tuple(tail)


def structured_character_audit(
    constants: np.ndarray,
    linears: np.ndarray,
    polars: np.ndarray,
) -> dict[str, object]:
    histogram: Counter[tuple[int, int]] = Counter()
    exceptions = []
    zero_numerator = 3**36
    for coordinates in projective_vectors(6):
        coefficient = np.array(coordinates, dtype=np.int16)
        polar = np.einsum("e,eij->ij", coefficient, polars) % 3
        linear = coefficient @ linears % 3
        polar_rank = rank_mod3(polar)
        augmented_rank = rank_mod3(
            np.column_stack((polar, linear))
        )
        histogram[(polar_rank, augmented_rank)] += 1
        if augmented_rank == polar_rank:
            counts, replayed_rank, balanced = scalar_value_counts(
                int(coefficient @ constants % 3), linear, polar
            )
            if replayed_rank != polar_rank or balanced:
                raise AssertionError("exceptional character replay failed")
            exceptions.append(
                {
                    "representative": coordinates,
                    "polar_rank": polar_rank,
                    "value_counts": counts,
                }
            )
            zero_numerator += 3 * counts[0] - 3**36
        elif augmented_rank != polar_rank + 1:
            raise AssertionError("an augmented rank jumped by more than one")
    if zero_numerator % 3**6:
        raise AssertionError("character inversion lost integrality")
    return {
        "projective_characters": 364,
        "rank_histogram": {
            f"{left},{right}": count
            for (left, right), count in sorted(histogram.items())
        },
        "exceptional_projective_lines": len(exceptions),
        "exceptions": exceptions,
        "six_equation_zero_fiber": zero_numerator // 3**6,
    }


def retraction_audit(
    linears: np.ndarray, polars: np.ndarray
) -> dict[str, object]:
    full_radical = nullspace_mod3(polars.reshape(-1, 36))
    full_restriction_rank = rank_mod3(
        linears @ full_radical.T % 3
    )

    coordinate_subsets: dict[str, list[dict[str, object]]] = {}
    for size in range(1, 6):
        records = []
        for subset in itertools.combinations(range(6), size):
            radical = nullspace_mod3(
                polars[list(subset)].reshape(-1, 36)
            )
            restriction_rank = rank_mod3(
                linears[list(subset)] @ radical.T % 3
            )
            if restriction_rank == size:
                records.append(
                    {
                        "subset": subset,
                        "common_radical_dimension": len(radical),
                    }
                )
        coordinate_subsets[str(size)] = records

    hyperplanes = []
    for normal in projective_vectors(6):
        normal_array = np.array(normal, dtype=np.int16)
        equation_basis = nullspace_mod3(normal_array.reshape(1, 6))
        if equation_basis.shape != (5, 6):
            raise AssertionError("a projective normal lost its hyperplane")
        combined_polars = np.einsum(
            "ae,eij->aij", equation_basis, polars
        ) % 3
        combined_linears = equation_basis @ linears % 3
        radical = nullspace_mod3(combined_polars.reshape(-1, 36))
        restriction_rank = rank_mod3(
            combined_linears @ radical.T % 3
        )
        if restriction_rank == 5:
            hyperplanes.append(
                {
                    "normal": normal,
                    "common_radical_dimension": len(radical),
                    "equation_basis": tuple(
                        tuple(map(int, row)) for row in equation_basis
                    ),
                }
            )

    maximum = (
        6
        if full_restriction_rank == 6
        else 5
        if hyperplanes
        else max(
            (
                int(size)
                for size, records in coordinate_subsets.items()
                if records
            ),
            default=0,
        )
    )
    qualification = (
        "The reported maximum is exhaustive in the full six-dimensional "
        "structured span."
        if maximum >= 5
        else (
            "No five- or six-form retraction exists in the full structured "
            "span; the lower bound uses coordinate subsets only."
        )
    )
    return {
        "criterion": (
            "For forms f_i=c_i+l_i x+2 x^T B_i x, a radical-translation "
            "retraction exists exactly when R=intersection ker(B_i) has "
            "rank(l_i restricted to R)=k; equivalently there is V with "
            "B_i V=0 and L V=I_k."
        ),
        "six_form_common_radical_dimension": len(full_radical),
        "six_form_linear_restriction_rank": full_restriction_rank,
        "six_form_retraction": full_restriction_rank == 6,
        "five_hyperplanes_exhausted": 364,
        "retractable_five_hyperplanes": hyperplanes,
        "retractable_five_hyperplane_count": len(hyperplanes),
        "coordinate_retractable_subsets": coordinate_subsets,
        "maximum_retraction_dimension": maximum,
        "maximum_qualification": qualification,
    }


def audit_record(record: dict[str, object], transfer: bool) -> dict[str, object]:
    ids_a = tuple(map(int, record["ids_a"]))
    ids_b = tuple(map(int, record["ids_b"]))
    (
        _,
        origin,
        basis,
        constants,
        linears,
        polars,
    ) = lift.exact_forms_record(ids_a, ids_b)
    polar_ranks = tuple(rank_mod3(matrix) for matrix in polars)
    flattened = np.array(
        [
            [
                polars[equation, left, right]
                for left in range(36)
                for right in range(left, 36)
            ]
            for equation in range(18)
        ],
        dtype=np.int16,
    )
    g_constants, g_linears, g_polars = lift.structured_forms(
        constants, linears, polars
    )
    result = {
        **record,
        "first_layer": {
            "rank": 18,
            "nullity": len(basis),
            "origin": origin,
        },
        "second_layer": {
            "active_equation_rows": lift.ACTIVE_ROWS,
            "equations": 18,
            "polar_rank_histogram": dict(
                sorted(Counter(polar_ranks).items())
            ),
            "quadratic_span_rank": rank_mod3(flattened),
        },
        "structured_characters": structured_character_audit(
            g_constants, g_linears, g_polars
        ),
        "structured_retraction": retraction_audit(
            g_linears, g_polars
        ),
    }
    if transfer:
        joined = catalog_phase_sum_intersection(ids_a, ids_b)
        result["row_margin_transfer"] = {
            "catalog_rows": joined["catalog_rows"],
            "compatible_catalog_rows": joined[
                "compatible_catalog_rows"
            ],
            "accepted_raw_assignments": joined[
                "accepted_assignments"
            ],
            "phase_sum_corpus_sha256": joined[
                "phase_sum_corpus_sha256"
            ],
        }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", type=Path, nargs="+")
    parser.add_argument(
        "--output",
        type=Path,
        help="write the frozen JSON atomically instead of printing it",
    )
    parser.add_argument(
        "--skip-transfer",
        action="store_true",
        help="omit the exact 1,756-row catalog intersection",
    )
    args = parser.parse_args()
    records = extract_records(args.paths)
    audited = [
        audit_record(record, transfer=not args.skip_transfer)
        for record in records
    ]
    result = {
        "schema": "h668-production-orbit-lift-retraction-scan-v1",
        "scope": (
            "Exact first/second-layer and structured-retraction invariants "
            "for completed enumerated production orbit records."
        ),
        "input_paths": tuple(map(str, args.paths)),
        "exact_orbits": len(audited),
        "orbits": audited,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        temporary = args.output.with_suffix(args.output.suffix + ".tmp")
        temporary.write_text(rendered, encoding="utf-8")
        temporary.replace(args.output)


if __name__ == "__main__":
    main()
