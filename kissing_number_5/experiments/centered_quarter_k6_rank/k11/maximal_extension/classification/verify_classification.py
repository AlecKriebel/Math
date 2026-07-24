#!/usr/bin/env python3
"""Verify exact Gram/coordinate classifications of the thirteen K40 witnesses."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
MAXIMAL = HERE.parent
MAXIMAL_VERIFIER_PATH = MAXIMAL / "verify_certificate.py"
CERTIFICATE_PATH = HERE / "completion_classification.json"
CERTIFICATE_SHA256 = (
    "ccabd04602c5481d40fa16d5979a7cbcb04fa3ece357f3c97d39e881f1bef0a0"
)
SCHEMA = "kissing5.k11_k40_completion_classification.v1"
EXPECTED_ATOMS = (6, 7, 9, 10, 18, 23, 27, 41, 43, 44, 47, 49, 50)
EXPECTED_D5 = (6, 23)
EXPECTED_L5 = (7, 9, 10, 18, 27, 41, 43, 44, 47, 49, 50)
EXPECTED_HISTOGRAMS = {
    "D5": {"-4": 20, "-2": 240, "0": 280, "2": 240},
    "L5": {"-4": 12, "-3": 32, "-2": 192, "-1": 32, "0": 272, "2": 240},
    "Q5": {
        "-4": 10,
        "-16/5": 30,
        "-2": 180,
        "-6/5": 60,
        "0": 250,
        "4/5": 10,
        "2": 240,
    },
    "R5": {
        "-4": 6,
        "-16/5": 30,
        "-3": 20,
        "-2": 144,
        "-6/5": 60,
        "-1": 28,
        "0": 242,
        "4/5": 10,
        "2": 240,
    },
}


class ClassificationError(RuntimeError):
    """Raised when an exact classification witness fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ClassificationError(message)


def load_maximal_verifier():
    spec = importlib.util.spec_from_file_location(
        "maximal_extension_verifier",
        MAXIMAL_VERIFIER_PATH,
    )
    require(
        spec is not None and spec.loader is not None,
        "could not load maximal-extension verifier",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def known_codes() -> dict[str, tuple[tuple[Fraction, ...], ...]]:
    d5 = []
    for first, second in itertools.combinations(range(5), 2):
        for first_sign in (-1, 1):
            for second_sign in (-1, 1):
                point = [Fraction(0)] * 5
                point[first] = first_sign
                point[second] = second_sign
                d5.append(tuple(point))

    l5 = [point for point in d5 if point[4] != 1]
    for signs in itertools.product((-1, 1), repeat=4):
        if sum(sign < 0 for sign in signs) % 2 == 1:
            l5.append(
                tuple(Fraction(sign, 2) for sign in signs) + (Fraction(1),)
            )

    q5 = [point for point in d5 if sum(point) != 2]
    q5.extend(
        tuple(coordinate + Fraction(4, 5) for coordinate in point)
        for point in d5
        if sum(point) == -2
    )

    r5 = [point for point in l5 if sum(point) != 2]
    r5.extend(
        tuple(coordinate + Fraction(4, 5) for coordinate in point)
        for point in l5
        if sum(point) == -2
    )
    result = {
        "D5": tuple(d5),
        "L5": tuple(l5),
        "Q5": tuple(q5),
        "R5": tuple(r5),
    }
    require(
        all(len(points) == 40 and len(set(points)) == 40 for points in result.values()),
        "known-code construction failed",
    )
    return result


def scaled_gram(points) -> tuple[tuple[Fraction, ...], ...]:
    gram = tuple(
        tuple(
            2 * sum(
                left * right
                for left, right in zip(first, second, strict=True)
            )
            for second in points
        )
        for first in points
    )
    require(
        all(gram[index][index] == 4 for index in range(len(gram))),
        "known code has wrong norm",
    )
    require(
        all(
            gram[first][second] <= 2
            for first in range(len(gram))
            for second in range(first)
        ),
        "known code violates the kissing inequality",
    )
    return gram


def pair_histogram(gram) -> Counter:
    return Counter(
        gram[first][second]
        for first in range(len(gram))
        for second in range(first)
    )


def histogram_json(histogram: Counter) -> dict[str, int]:
    return {
        str(value): multiplicity
        for value, multiplicity in sorted(histogram.items())
    }


def reconstruct_completion(verifier, source, maximal, atom_index):
    gram, determinant_base, adj = verifier.reconstruct_gram(
        source["atoms"][atom_index],
        atom_index,
    )
    candidates = verifier.enumerate_candidates(gram, determinant_base, adj)
    clique = maximal["entries"][atom_index]["clique_candidate_indices"]
    rows = tuple(tuple(row[:5]) for row in gram) + tuple(
        candidates[index] for index in clique
    )
    require(len(rows) == 40, f"atom {atom_index}: completion is not K40")
    completed = []
    for first in rows:
        completed_row = []
        for second in rows:
            numerator = verifier.bilinear(first, adj, second)
            require(
                numerator % determinant_base == 0,
                f"atom {atom_index}: nonintegral completed Gram entry",
            )
            completed_row.append(numerator // determinant_base)
        completed.append(tuple(completed_row))
    result = tuple(completed)
    require(
        all(result[index][index] == 4 for index in range(40)),
        f"atom {atom_index}: wrong completed norm",
    )
    require(
        all(
            result[first][second] in verifier.VALUE_SET
            for first in range(40)
            for second in range(first)
        ),
        f"atom {atom_index}: completed off-diagonal value outside grid",
    )
    return result


def integer_list(value: Any, label: str) -> list[int]:
    require(type(value) is list, f"{label} is not a list")
    result = []
    for index, item in enumerate(value):
        require(type(item) is int, f"{label}[{index}] is not an integer")
        result.append(item)
    return result


def verify(
    certificate_path: Path = CERTIFICATE_PATH,
    expected_certificate_sha256: str = CERTIFICATE_SHA256,
) -> dict[str, Any]:
    require(
        hashlib.sha256(certificate_path.read_bytes()).hexdigest()
        == expected_certificate_sha256,
        "classification certificate SHA-256 mismatch",
    )
    verifier = load_maximal_verifier()
    maximal_result = verifier.verify()
    require(maximal_result["status"] == "PASS", "maximal certificate failed")
    source = json.loads(verifier.SOURCE_PATH.read_text())
    maximal = json.loads(verifier.CERTIFICATE_PATH.read_text())
    certificate = json.loads(certificate_path.read_text())
    require(type(certificate) is dict, "classification certificate is not an object")
    require(certificate.get("schema") == SCHEMA, "wrong classification schema")
    require(
        certificate.get("source_k11_sha256") == verifier.SOURCE_SHA256,
        "wrong embedded K11 source hash",
    )
    require(
        certificate.get("maximal_extension_sha256")
        == verifier.CERTIFICATE_SHA256,
        "wrong embedded maximal-extension hash",
    )

    codes = known_codes()
    known_grams = {name: scaled_gram(points) for name, points in codes.items()}
    known_histograms = {
        name: histogram_json(pair_histogram(gram))
        for name, gram in known_grams.items()
    }
    require(
        known_histograms == EXPECTED_HISTOGRAMS,
        "known-code pair histograms do not match the exact reference values",
    )
    require(
        certificate.get("known_pair_histograms_scaled_by_four")
        == EXPECTED_HISTOGRAMS,
        "stored known-code histograms are wrong",
    )

    entries = certificate.get("entries")
    require(type(entries) is list and len(entries) == 13, "wrong entry count")
    require(
        tuple(entry.get("atom_index") for entry in entries) == EXPECTED_ATOMS,
        "wrong classified atom list",
    )
    classified: dict[str, list[int]] = {
        "D5": [],
        "L5": [],
        "Q5": [],
        "R5": [],
    }
    for entry in entries:
        require(type(entry) is dict, "classification entry is not an object")
        atom_index = entry["atom_index"]
        known_type = entry.get("known_type")
        require(known_type in codes, f"atom {atom_index}: unknown classification")
        gram = reconstruct_completion(verifier, source, maximal, atom_index)

        stored_upper = integer_list(
            entry.get("upper_triangle_gram_scaled_by_four"),
            f"atom {atom_index} stored Gram",
        )
        expected_upper = [
            gram[first][second]
            for first in range(40)
            for second in range(first, 40)
        ]
        require(
            stored_upper == expected_upper,
            f"atom {atom_index}: stored Gram does not match its exact completion",
        )

        permutation = integer_list(
            entry.get("completion_to_known_permutation"),
            f"atom {atom_index} permutation",
        )
        require(
            len(permutation) == 40 and set(permutation) == set(range(40)),
            f"atom {atom_index}: classification map is not a permutation",
        )
        target_gram = known_grams[known_type]
        require(
            all(
                Fraction(gram[first][second])
                == target_gram[permutation[first]][permutation[second]]
                for first in range(40)
                for second in range(40)
            ),
            f"atom {atom_index}: claimed exact isometry fails",
        )

        coordinate_data = entry.get("coordinates_numerator_over_sqrt2")
        require(
            type(coordinate_data) is list and len(coordinate_data) == 40,
            f"atom {atom_index}: wrong coordinate row count",
        )
        coordinates = []
        for row_index, row in enumerate(coordinate_data):
            require(
                type(row) is list and len(row) == 5,
                f"atom {atom_index}: coordinate row {row_index} has wrong length",
            )
            try:
                coordinates.append(tuple(Fraction(value) for value in row))
            except (ValueError, ZeroDivisionError) as error:
                raise ClassificationError(
                    f"atom {atom_index}: invalid rational coordinate"
                ) from error
        require(
            tuple(coordinates)
            == tuple(codes[known_type][index] for index in permutation),
            f"atom {atom_index}: exported coordinates do not match the isometry",
        )
        coordinate_gram = scaled_gram(tuple(coordinates))
        require(
            all(
                coordinate_gram[first][second] == gram[first][second]
                for first in range(40)
                for second in range(40)
            ),
            f"atom {atom_index}: exported coordinates do not realize the Gram matrix",
        )

        histogram = histogram_json(pair_histogram(gram))
        require(
            entry.get("pair_histogram_scaled_by_four") == histogram,
            f"atom {atom_index}: stored pair histogram is wrong",
        )
        require(
            histogram == EXPECTED_HISTOGRAMS[known_type],
            f"atom {atom_index}: histogram does not match its known type",
        )
        require(
            all(
                histogram != EXPECTED_HISTOGRAMS[other]
                for other in codes
                if other != known_type
            ),
            f"atom {atom_index}: histogram does not exclude another known type",
        )
        classified[known_type].append(atom_index)

    require(tuple(classified["D5"]) == EXPECTED_D5, "wrong D5 classification")
    require(tuple(classified["L5"]) == EXPECTED_L5, "wrong L5 classification")
    require(not classified["Q5"] and not classified["R5"], "unexpected Q5/R5")
    require(
        certificate.get("classification_summary") == classified,
        "stored classification summary is wrong",
    )
    return {
        "status": "PASS",
        "completions_checked": len(entries),
        "D5_atoms": classified["D5"],
        "L5_atoms": classified["L5"],
        "Q5_atoms": classified["Q5"],
        "R5_atoms": classified["R5"],
        "exact_gram_entries_checked": len(entries) * 40 * 40,
        "exact_coordinates_checked": len(entries) * 40,
        "certificate_sha256": expected_certificate_sha256,
    }


def main() -> None:
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
