#!/usr/bin/env python3
"""Independent exact replay of the serialized Gate 1 separator witnesses.

This program reads the invariant templates and frozen network records only as
data.  It imports no historical graph, Fourier, invariant, rank, or atlas
module.  Its scope is deliberately narrower than the historical crosscheck:
the frozen JSON serializes one network per signature class, so this program
can replay all 356 selected representative-pair witnesses but cannot recover
the omitted parameterizations in each class from that JSON alone.
"""

from __future__ import annotations

import argparse
import ast
import itertools
import json
import math
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import sympy as sp

from exact_poly import Polynomial, strict_bernstein_sign


DEFAULT_PROJECT = Path(
    "/Users/alec/Documents/Math/strong_level2_phylo_identifiability"
)

JC4 = (
    (0, 0, 0, 0),
    (0, 0, 1, 1),
    (0, 1, 0, 1),
    (0, 1, 1, 0),
    (0, 1, 2, 3),
    (1, 0, 0, 1),
    (1, 0, 1, 0),
    (1, 0, 2, 3),
    (1, 1, 0, 0),
    (1, 1, 1, 1),
    (1, 1, 2, 2),
    (1, 2, 0, 3),
    (1, 2, 1, 2),
    (1, 2, 2, 1),
    (1, 2, 3, 0),
)


def file_hash(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_template_data(path: Path):
    module = ast.parse(path.read_text(), filename=str(path))
    for node in module.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(
            isinstance(target, ast.Name) and target.id == "INVARIANT_TEMPLATES"
            for target in node.targets
        ):
            return ast.literal_eval(node.value)
    raise ValueError("INVARIANT_TEMPLATES assignment not found")


def canonical_character(assignment: Sequence[int]) -> tuple[int, ...]:
    return min(
        tuple(0 if value == 0 else permutation[value - 1] for value in assignment)
        for permutation in itertools.permutations((1, 2, 3))
    )


def normalize_invariant(candidate) -> tuple[tuple[tuple[int, ...], int], ...]:
    combined: dict[tuple[int, ...], Fraction] = defaultdict(Fraction)
    for monomial, coefficient in candidate:
        combined[tuple(sorted(int(value) for value in monomial))] += Fraction(
            coefficient
        )
    combined = {monomial: value for monomial, value in combined.items() if value}
    denominator = math.lcm(*(value.denominator for value in combined.values()))
    integers = {
        monomial: int(value * denominator) for monomial, value in combined.items()
    }
    divisor = math.gcd(*(abs(value) for value in integers.values()))
    result = tuple(
        sorted((monomial, value // divisor) for monomial, value in integers.items())
    )
    if result[0][1] < 0:
        result = tuple((monomial, -coefficient) for monomial, coefficient in result)
    return result


def coordinate_permutation(permutation: Sequence[int]) -> tuple[int, ...]:
    result = []
    for assignment in JC4:
        positioned = tuple(assignment[label - 1] for label in permutation)
        result.append(JC4.index(canonical_character(positioned)))
    return tuple(result)


def invariant_orbit(templates) -> tuple[tuple[tuple[tuple[int, ...], int], ...], ...]:
    result = []
    for template in templates:
        images = set()
        for permutation in itertools.permutations((1, 2, 3, 4)):
            mapping = coordinate_permutation(permutation)
            images.add(
                normalize_invariant(
                    (
                        tuple(mapping[index] for index in monomial),
                        coefficient,
                    )
                    for monomial, coefficient in template
                )
            )
        result.extend(sorted(images))
    if len(result) != 60 or len(set(result)) != 60:
        raise AssertionError("the six templates must have 60 listed orbit images")
    return tuple(result)


def cube_actions() -> tuple[tuple[int, ...], ...]:
    choices = tuple(itertools.product((0, 1), repeat=2))
    lookup = {choice: index for index, choice in enumerate(choices)}
    actions = set()
    for order in itertools.permutations((0, 1)):
        for flips in itertools.product((0, 1), repeat=2):
            actions.add(
                tuple(
                    lookup[
                        tuple(
                            choice[order[index]] ^ flips[index]
                            for index in range(2)
                        )
                    ]
                    for choice in choices
                )
            )
    return tuple(sorted(actions))


CUBE_ACTIONS = cube_actions()


def degree_maps(
    arcs: Sequence[tuple[str, str]],
) -> tuple[Counter[str], Counter[str]]:
    indegree: Counter[str] = Counter()
    outdegree: Counter[str] = Counter()
    for tail, head in arcs:
        outdegree[tail] += 1
        indegree[head] += 1
        indegree.setdefault(tail, 0)
        outdegree.setdefault(head, 0)
    return indegree, outdegree


def record_network(record: Mapping[str, object]):
    network = record["network"]
    labels = {
        str(leaf): int(label)
        for leaf, label in network.get(
            "selected_leaf_labels", network.get("leaf_labels", {})
        ).items()
    }
    return (
        tuple((str(tail), str(head)) for tail, head in network["arcs"]),
        labels,
    )


def quartet_tensor(
    arcs: Sequence[tuple[str, str]],
    labels: Mapping[str, int],
    quartet: Sequence[int],
) -> tuple[tuple[int, ...], ...]:
    label_to_leaf = {label: leaf for leaf, label in labels.items()}
    selected = {
        label_to_leaf[global_label]: local_label
        for local_label, global_label in enumerate(quartet, 1)
    }
    indegree, outdegree = degree_maps(arcs)
    reticulations = tuple(
        sorted(
            vertex
            for vertex in set(indegree) | set(outdegree)
            if (indegree[vertex], outdegree[vertex]) == (2, 1)
        )
    )
    if len(reticulations) not in {1, 2}:
        raise AssertionError("Gate 1 representatives must have one or two reticulations")
    incoming = {
        vertex: tuple(
            index for index, (_tail, head) in enumerate(arcs) if head == vertex
        )
        for vertex in reticulations
    }
    displayed_edge_masks: list[dict[int, int]] = []
    for choice in itertools.product((0, 1), repeat=len(reticulations)):
        excluded = {
            incoming[vertex][1 - bit]
            for vertex, bit in zip(reticulations, choice)
        }
        children: dict[str, list[str]] = defaultdict(list)
        for index, (tail, head) in enumerate(arcs):
            if index not in excluded:
                children[tail].append(head)
        memo: dict[str, int] = {}

        def descendant_mask(vertex: str) -> int:
            if vertex in memo:
                return memo[vertex]
            value = 1 << (selected[vertex] - 1) if vertex in selected else 0
            for child in children[vertex]:
                value |= descendant_mask(child)
            memo[vertex] = value
            return value

        displayed_edge_masks.append(
            {
                index: descendant_mask(head)
                for index, (_tail, head) in enumerate(arcs)
                if index not in excluded
            }
        )
    signatures = []
    for edge_index in range(len(arcs)):
        row = tuple(masks.get(edge_index, 0) for masks in displayed_edge_masks)
        if len(row) == 2:
            row = (row[0], row[0], row[1], row[1])
        if any(row):
            signatures.append(row)
    signatures = tuple(sorted(set(signatures)))
    return min(
        tuple(
            sorted(tuple(row[index] for index in action) for row in signatures)
        )
        for action in CUBE_ACTIONS
    )


def xor_on_mask(assignment: Sequence[int], mask: int) -> int:
    result = 0
    for position, character in enumerate(assignment):
        if mask & (1 << position):
            result ^= character
    return result


def coordinate_polynomials(tensor: tuple[tuple[int, ...], ...]):
    width = len(tensor) + 2
    variables = [Polynomial.variable(width, index) for index in range(width)]
    edges = variables[:-2]
    inheritances = variables[-2:]
    choices = ((0, 0), (0, 1), (1, 0), (1, 1))
    coordinates = []
    for assignment in JC4:
        total = Polynomial.constant(width, 0)
        for displayed_index, choice in enumerate(choices):
            term = Polynomial.constant(width, 1)
            for bit, inheritance in zip(choice, inheritances):
                term *= inheritance if bit == 0 else 1 - inheritance
            for edge, row in zip(edges, tensor):
                if xor_on_mask(assignment, row[displayed_index]):
                    term *= edge
            total += term
        coordinates.append(total)
    return tuple(coordinates)


def invariant_pullback(
    tensor: tuple[tuple[int, ...], ...],
    invariant: Sequence[tuple[Sequence[int], int]],
) -> Polynomial:
    coordinates = coordinate_polynomials(tensor)
    result = Polynomial.constant(coordinates[0].width, 0)
    for monomial, coefficient in invariant:
        term = Polynomial.constant(coordinates[0].width, coefficient)
        for coordinate in monomial:
            term *= coordinates[int(coordinate)]
        result += term
    return result


def to_sympy(polynomial: Polynomial, names: Sequence[str]) -> sp.Poly:
    symbols = sp.symbols(" ".join(names))
    if len(names) == 1:
        symbols = (symbols,)
    return sp.Poly.from_dict(
        {
            monomial: sp.Rational(coefficient.numerator, coefficient.denominator)
            for monomial, coefficient in polynomial.terms
        },
        *symbols,
        domain=sp.QQ,
    )


def from_sympy(polynomial: sp.Poly, width: int) -> Polynomial:
    return Polynomial.from_dict(
        width,
        {
            tuple(int(value) for value in monomial): Fraction(
                int(coefficient.p), int(coefficient.q)
            )
            for monomial, coefficient in polynomial.terms()
        },
    )


def polynomial_digest(polynomial: Polynomial) -> str:
    payload = {
        "width": polynomial.width,
        "terms": [
            [list(monomial), str(coefficient)]
            for monomial, coefficient in polynomial.terms
        ],
    }
    return sha256(
        json.dumps(payload, separators=(",", ":")).encode()
    ).hexdigest()


def factor_and_sign(
    polynomial: Polynomial,
    factor_cache: dict[tuple[tuple[tuple[int, ...], Fraction], ...], tuple[int | None, dict[str, object]]],
) -> dict[str, object]:
    names = tuple(f"p{index}" for index in range(polynomial.width))
    sympy_polynomial = to_sympy(polynomial, names)
    constant, factors = sp.factor_list(sympy_polynomial)
    constant_fraction = Fraction(int(constant.p), int(constant.q))
    product = Polynomial.constant(polynomial.width, constant_fraction)
    total_bernstein = 0
    maximum_bernstein = 0
    rows = []
    for sympy_factor, exponent in factors:
        factor = from_sympy(sympy_factor, polynomial.width)
        product *= factor ** int(exponent)
        if factor.terms not in factor_cache:
            factor_cache[factor.terms] = strict_bernstein_sign(factor)
        sign, metadata = factor_cache[factor.terms]
        if sign not in {-1, 1}:
            raise AssertionError("irreducible factor is not certified nonzero on the open cube")
        total_bernstein += int(metadata["coefficient_count"])
        maximum_bernstein = max(maximum_bernstein, int(metadata["coefficient_count"]))
        rows.append(
            {
                "exponent": int(exponent),
                "terms": len(factor.terms),
                "strict_sign": sign,
                "bernstein_coefficient_count": int(metadata["coefficient_count"]),
            }
        )
    if product != polynomial:
        raise AssertionError("factorization did not multiply back")
    return {
        "constant": str(constant_fraction),
        "factor_count": len(factors),
        "factors": rows,
        "total_bernstein_coefficients": total_bernstein,
        "maximum_factor_bernstein_coefficients": maximum_bernstein,
    }


def audit(project: Path) -> dict[str, object]:
    frozen_path = (
        project
        / "AUDIT/INDEPENDENT_IMPLEMENTATION/gate1_root_full_completion_audit.json"
    )
    template_path = project / "src/jc_root_spanning_atlas_data.py"
    frozen = json.loads(frozen_path.read_text())
    invariants = invariant_orbit(parse_template_data(template_path))
    pair_failures = []
    pair_counts = Counter()
    unique_polynomials: dict[str, dict[str, object]] = {}
    witness_keys: set[tuple[tuple[tuple[int, ...], ...], int]] = set()
    factor_cache: dict[
        tuple[tuple[tuple[int, ...], Fraction], ...],
        tuple[int | None, dict[str, object]],
    ] = {}
    total_bernstein = 0
    maximum_bernstein = 0

    for port_count in (6, 7, 8):
        level = frozen["levels"][str(port_count)]
        source_map = {
            str(record["signature_sha256"]): record
            for record in level["source"]["signature_class_representatives"]
        }
        target_map = {
            str(record["signature_sha256"]): record
            for record in level["target"]["signature_class_representatives"]
        }
        rows = level["strict_directed_filters"]["source_subset_target_rows"]
        for row_index, row in enumerate(rows):
            try:
                certificate = row["source_zero_target_nonzero_certificate"]
                bit_index = int(certificate["bit_index"])
                quartet_index, invariant_index = divmod(bit_index, 60)
                if quartet_index != int(certificate["quartet_index"]):
                    raise AssertionError("quartet index disagrees with bit index")
                if invariant_index != int(certificate["invariant_index"]):
                    raise AssertionError("invariant index disagrees with bit index")
                quartet = tuple(
                    itertools.combinations(range(1, port_count + 1), 4)
                )[quartet_index]
                source_record = source_map[str(row["source_signature_sha256"])]
                target_record = target_map[str(row["target_signature_sha256"])]
                source_arcs, source_labels = record_network(source_record)
                target_arcs, target_labels = record_network(target_record)
                source_tensor = quartet_tensor(source_arcs, source_labels, quartet)
                target_tensor = quartet_tensor(target_arcs, target_labels, quartet)
                source_polynomial = invariant_pullback(
                    source_tensor, invariants[invariant_index]
                )
                target_polynomial = invariant_pullback(
                    target_tensor, invariants[invariant_index]
                )
                witness_keys.add((target_tensor, invariant_index))
                if source_polynomial:
                    raise AssertionError("claimed source-zero pullback is nonzero")
                if not target_polynomial:
                    raise AssertionError("claimed target-nonzero pullback is zero")
                if len(target_polynomial.terms) != int(
                    certificate["target_polynomial_terms"]
                ):
                    raise AssertionError("target term count mismatch")
                digest = polynomial_digest(target_polynomial)
                if digest not in unique_polynomials:
                    metadata = factor_and_sign(target_polynomial, factor_cache)
                    total_bernstein += int(metadata["total_bernstein_coefficients"])
                    maximum_bernstein = max(
                        maximum_bernstein,
                        int(metadata["maximum_factor_bernstein_coefficients"]),
                    )
                    unique_polynomials[digest] = {
                        "canonical_polynomial_sha256": digest,
                        "terms": len(target_polynomial.terms),
                        "variables": target_polynomial.width,
                        **metadata,
                    }
                pair_counts[str(port_count)] += 1
            except Exception as error:
                pair_failures.append(
                    {
                        "ports": port_count,
                        "row_index": row_index,
                        "source_signature_sha256": row.get("source_signature_sha256"),
                        "target_signature_sha256": row.get("target_signature_sha256"),
                        "error": f"{type(error).__name__}: {error}",
                    }
                )
        print(
            f"Gate 1 representative separator replay {port_count}: {len(rows)} rows",
            file=sys.stderr,
            flush=True,
        )

    expected_pairs = {"6": 44, "7": 192, "8": 120}
    exact = (
        not pair_failures
        and dict(pair_counts) == expected_pairs
        and len(witness_keys) == 50
    )
    return {
        "inputs": {
            str(frozen_path): file_hash(frozen_path),
            str(template_path): file_hash(template_path),
        },
        "invariant_template_orbit_size": len(invariants),
        "representative_pairs_replayed": dict(sorted(pair_counts.items())),
        "representative_pairs_total": sum(pair_counts.values()),
        "distinct_target_tensor_invariant_witnesses": len(witness_keys),
        "distinct_coefficient_arrays_up_to_parameter_renaming": len(unique_polynomials),
        "distinct_irreducible_factors": len(factor_cache),
        "total_factor_bernstein_coefficients": total_bernstein,
        "maximum_factor_bernstein_coefficients": maximum_bernstein,
        "failures": pair_failures,
        "scope_limit": (
            "EXACTLY COMPUTED only for the one serialized representative of each "
            "signature class.  The frozen JSON omits the other complete target "
            "parameterization encodings, so its claimed 408/1252/468 concrete "
            "target-model coverage cannot be replayed from the final certificates."
        ),
        "direction": (
            "For each row the polynomial is identically zero on the source and "
            "strictly nonzero at every point of the representative target open "
            "cube.  This excludes every common point, hence source containment "
            "in that target; the direction is correct."
        ),
        "status": "EXACTLY COMPUTED" if exact else "FALSE",
        "safe_for_arbitrary_root_closure_by_itself": False,
        "polynomials": [unique_polynomials[key] for key in sorted(unique_polynomials)],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, default=DEFAULT_PROJECT)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    result = audit(arguments.project.resolve())
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in ("status", "representative_pairs_total", "distinct_target_tensor_invariant_witnesses", "distinct_coefficient_arrays_up_to_parameter_renaming", "failures")}, indent=2))


if __name__ == "__main__":
    main()
