#!/usr/bin/env python3
"""Generate exact D5/L5 classifications for the thirteen K40 witnesses."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import importlib.util
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
MAXIMAL = HERE.parent
VERIFY_PATH = MAXIMAL / "verify_certificate.py"
OUTPUT = HERE / "completion_classification.json"


def load_verifier():
    spec = importlib.util.spec_from_file_location("maximal_verifier", VERIFY_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load maximal-extension verifier")
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
    answer = {
        "D5": tuple(d5),
        "L5": tuple(l5),
        "Q5": tuple(q5),
        "R5": tuple(r5),
    }
    if any(len(points) != 40 for points in answer.values()):
        raise RuntimeError("known-code construction did not yield 40 points")
    return answer


def scaled_gram(
    points: tuple[tuple[Fraction, ...], ...],
) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(
        tuple(
            2 * sum(left * right for left, right in zip(first, second, strict=True))
            for second in points
        )
        for first in points
    )


def completion(verifier, source, maximal, atom_index):
    atom = source["atoms"][atom_index]
    entry = maximal["entries"][atom_index]
    gram, determinant_base, adj = verifier.reconstruct_gram(atom, atom_index)
    candidates = verifier.enumerate_candidates(gram, determinant_base, adj)
    selected = tuple(
        candidates[index] for index in entry["clique_candidate_indices"]
    )
    rows = tuple(tuple(row[:5]) for row in gram) + selected
    completed_gram = tuple(
        tuple(
            verifier.bilinear(first, adj, second) // determinant_base
            for second in rows
        )
        for first in rows
    )
    return completed_gram


def pair_histogram(gram) -> Counter:
    return Counter(
        gram[first][second]
        for first in range(len(gram))
        for second in range(first)
    )


def isometry(first, second) -> list[int] | None:
    """Find a permutation p satisfying first[i,j] = second[p[i],p[j]]."""

    size = len(first)
    colors = sorted(
        {
            value
            for gram in (first, second)
            for row in gram
            for value in row
            if value != 4
        }
    )
    signatures = []
    for gram in (first, second):
        signatures.append(
            [
                tuple(
                    Counter(
                        gram[vertex][other]
                        for other in range(size)
                        if other != vertex
                    )[color]
                    for color in colors
                )
                for vertex in range(size)
            ]
        )
    candidate_sets = [
        {
            other
            for other in range(size)
            if signatures[0][vertex] == signatures[1][other]
        }
        for vertex in range(size)
    ]
    mapping: dict[int, int] = {}
    used: set[int] = set()

    def recurse() -> list[int] | None:
        if len(mapping) == size:
            return [mapping[index] for index in range(size)]
        best_vertex = None
        best_options = None
        for vertex in range(size):
            if vertex in mapping:
                continue
            options = [
                other
                for other in candidate_sets[vertex] - used
                if all(
                    first[vertex][mapped_vertex]
                    == second[other][mapped_other]
                    for mapped_vertex, mapped_other in mapping.items()
                )
            ]
            if not options:
                return None
            if best_options is None or len(options) < len(best_options):
                best_vertex = vertex
                best_options = options
        if best_vertex is None or best_options is None:
            raise RuntimeError("isometry recursion lost its next vertex")
        for other in sorted(best_options):
            mapping[best_vertex] = other
            used.add(other)
            result = recurse()
            if result is not None:
                return result
            used.remove(other)
            del mapping[best_vertex]
        return None

    return recurse()


def fraction_string(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def main() -> None:
    verifier = load_verifier()
    verifier.verify()
    source = json.loads(verifier.SOURCE_PATH.read_text())
    maximal = json.loads(verifier.CERTIFICATE_PATH.read_text())
    codes = known_codes()
    known_grams = {name: scaled_gram(points) for name, points in codes.items()}
    known_histograms = {
        name: {
            fraction_string(value): multiplicity
            for value, multiplicity in sorted(pair_histogram(gram).items())
        }
        for name, gram in known_grams.items()
    }

    entries = []
    for atom_index in maximal["atoms_reaching_40"]:
        gram = completion(verifier, source, maximal, atom_index)
        matching_histograms = [
            name
            for name, known_gram in known_grams.items()
            if pair_histogram(gram) == pair_histogram(known_gram)
        ]
        if len(matching_histograms) != 1:
            raise RuntimeError(
                f"atom {atom_index}: histogram classification is not unique"
            )
        known_type = matching_histograms[0]
        permutation = isometry(gram, known_grams[known_type])
        if permutation is None:
            raise RuntimeError(f"atom {atom_index}: no exact known-code isometry")
        coordinates = tuple(codes[known_type][index] for index in permutation)
        entries.append(
            {
                "atom_index": atom_index,
                "known_type": known_type,
                "completion_to_known_permutation": permutation,
                "pair_histogram_scaled_by_four": {
                    fraction_string(value): multiplicity
                    for value, multiplicity in sorted(pair_histogram(gram).items())
                },
                "upper_triangle_gram_scaled_by_four": [
                    gram[first][second]
                    for first in range(40)
                    for second in range(first, 40)
                ],
                "coordinates_numerator_over_sqrt2": [
                    [fraction_string(value) for value in point]
                    for point in coordinates
                ],
            }
        )
        print(atom_index, known_type, flush=True)

    certificate = {
        "schema": "kissing5.k11_k40_completion_classification.v1",
        "source_k11_sha256": verifier.SOURCE_SHA256,
        "maximal_extension_sha256": verifier.CERTIFICATE_SHA256,
        "coordinate_semantics": (
            "each listed rational row q represents the unit vector q/sqrt(2)"
        ),
        "known_pair_histograms_scaled_by_four": known_histograms,
        "entries": entries,
        "classification_summary": {
            "D5": [
                entry["atom_index"]
                for entry in entries
                if entry["known_type"] == "D5"
            ],
            "L5": [
                entry["atom_index"]
                for entry in entries
                if entry["known_type"] == "L5"
            ],
            "Q5": [],
            "R5": [],
        },
        "scope_warning": (
            "This classifies the particular maximum cliques stored in the "
            "maximal-extension certificate, not every maximum completion of "
            "each K11 atom."
        ),
    }
    OUTPUT.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
