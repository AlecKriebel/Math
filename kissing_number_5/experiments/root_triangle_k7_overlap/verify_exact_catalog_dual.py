#!/usr/bin/env python3
"""Dependency-free exact verifier for the root-triangle K7 catalog dual."""

from __future__ import annotations

from fractions import Fraction as Q
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "root_triangle_degree3_catalog_dual.json"
SOURCE_SHA256 = (
    "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
)
CATALOG_SHA256 = (
    "16cee0b4f7b6b7655990a74f7ffef104c4aef43d5074696cbbb1bcf413d1a623"
)
KERNEL = {2: 703, 3: 12654, 4: 442890}

PAIRS7 = tuple(itertools.combinations(range(7), 2))
PAIR_INDEX7 = {pair: index for index, pair in enumerate(PAIRS7)}
LOCAL_EDGES = (
    (0, 1),
    (0, 2),
    (1, 2),
    (0, 3),
    (0, 4),
    (1, 3),
    (1, 4),
    (2, 3),
    (2, 4),
    (3, 4),
)
LOCAL_EDGE_INDEX = {pair: index for index, pair in enumerate(LOCAL_EDGES)}
EXTENSION_PAIRS4 = tuple(itertools.combinations(range(4), 2))
EXTENSION_PAIR_INDEX4 = {
    pair: index for index, pair in enumerate(EXTENSION_PAIRS4)
}
TRIPLE_EDGE_INDICES4 = tuple(
    tuple(
        EXTENSION_PAIR_INDEX4[pair]
        for pair in itertools.combinations(triple, 2)
    )
    for triple in itertools.combinations(range(4), 3)
)


class VerificationError(Exception):
    """Raised when an exact certificate check fails."""


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_integers(values):
    payload = "".join(f"{value}\n" for value in values).encode()
    return hashlib.sha256(payload).hexdigest()


def rational_rank(matrix):
    work = [[Q(value) for value in row] for row in matrix]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(work))
                if work[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [
            value / pivot_value for value in work[pivot_row]
        ]
        for row in range(len(work)):
            if row == pivot_row or work[row][column] == 0:
                continue
            scale = work[row][column]
            work[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(
                    work[row], work[pivot_row]
                )
            ]
        pivot_row += 1
    return pivot_row


def weak_compositions(total, length):
    if length == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total - first, length - 1):
            yield (first,) + rest


def group_actions():
    actions = []
    for root_permutation in itertools.permutations(range(3)):
        for extension_permutation in ((3, 4), (4, 3)):
            permutation = tuple(root_permutation) + extension_permutation
            actions.append(
                tuple(
                    LOCAL_EDGE_INDEX[
                        tuple(
                            sorted(
                                (
                                    permutation[first],
                                    permutation[second],
                                )
                            )
                        )
                    ]
                    for first, second in LOCAL_EDGES
                )
            )
    return tuple(actions)


def invariant_monomial_orbits():
    actions = group_actions()
    exponents = tuple(
        exponent
        for degree in range(4)
        for exponent in weak_compositions(degree, 10)
    )
    seen = set()
    orbits = []
    for exponent in exponents:
        if exponent in seen:
            continue
        orbit = set()
        for action in actions:
            image = [0] * 10
            for old_index, new_index in enumerate(action):
                image[new_index] = exponent[old_index]
            orbit.add(tuple(image))
        seen.update(orbit)
        orbits.append(tuple(sorted(orbit)))
    require(len(orbits) == 48, "invariant basis does not have dimension 48")
    return tuple(orbits)


ORBITS = invariant_monomial_orbits()


def monomial_value(values, exponent):
    result = 1
    for value, power in zip(values, exponent):
        if power:
            result *= value**power
    return result


def make_projector(factor):
    @lru_cache(maxsize=None)
    def projected_feature(values):
        features = tuple(
            sum(
                monomial_value(values, exponent)
                for exponent in orbit
            )
            for orbit in ORBITS
        )
        return tuple(
            sum(
                features[row] * factor[row][column]
                for row in range(48)
            )
            for column in range(8)
        )

    return projected_feature


def scaled_edge(edges, first, second):
    return edges[PAIR_INDEX7[tuple(sorted((first, second)))]] - 4


def union_quadratic(values):
    degree_two = sum(value * value for value in values)
    degree_three = 0
    for indices in TRIPLE_EDGE_INDICES4:
        local = [values[index] for index in indices]
        degree_three += sum(local) ** 2 - sum(
            value * value for value in local
        )
    degree_four = 2 * (
        values[0] * values[5]
        + values[1] * values[4]
        + values[2] * values[3]
    )
    return (
        KERNEL[2] * degree_two
        + KERNEL[3] * degree_three
        + KERNEL[4] * degree_four
    )


def atom_projection(edges, projected_feature):
    total = 0
    for root in itertools.combinations(range(7), 3):
        residual = tuple(vertex for vertex in range(7) if vertex not in root)
        extension_values = []
        for local_first, local_second in EXTENSION_PAIRS4:
            extension = (
                residual[local_first],
                residual[local_second],
            )
            vertices = root + extension
            local_values = tuple(
                scaled_edge(edges, vertices[first], vertices[second])
                for first, second in LOCAL_EDGES
            )
            extension_values.append(projected_feature(local_values))
        for column in range(8):
            total += union_quadratic(
                tuple(value[column] for value in extension_values)
            )
    return total


def verify(certificate_path=CERTIFICATE):
    data = json.loads(certificate_path.read_text())
    require(
        data.get("schema")
        == "kissing5.root_triangle_degree3_catalog_dual.v1",
        "unexpected certificate schema",
    )
    require(data.get("target_cardinality") == 41, "wrong target size")
    require(data.get("local_size") == 7, "wrong local size")
    require(data.get("root_size") == 3, "wrong root size")
    require(data.get("extension_size") == 2, "wrong extension size")
    require(data.get("feature_degree") == 3, "wrong feature degree")
    require(data.get("feature_dimension") == 48, "wrong feature dimension")
    require(data.get("sum_of_squares_rank") == 8, "wrong SOS rank")
    require(
        tuple(
            tuple(tuple(exponent) for exponent in orbit)
            for orbit in data.get("feature_orbits", ())
        )
        == ORBITS,
        "stored invariant feature orbits mismatch",
    )
    require(
        {int(key): value for key, value in data[
            "integer_kernel_by_union_size"
        ].items()}
        == KERNEL,
        "exchangeability kernel mismatch",
    )

    source_path = ROOT / data["source"]
    catalog_path = ROOT / data["catalog"]
    require(
        sha256(source_path) == SOURCE_SHA256 == data["source_sha256"],
        "source hash mismatch",
    )
    require(
        sha256(catalog_path) == CATALOG_SHA256 == data["catalog_sha256"],
        "catalog hash mismatch",
    )

    factor = tuple(tuple(map(int, row)) for row in data["factor_B"])
    require(
        len(factor) == 48 and all(len(row) == 8 for row in factor),
        "factor B has wrong shape",
    )
    require(rational_rank(factor) == 8, "factor B does not have rank eight")
    dual = tuple(map(int, data["triangle_dual_Y"]))
    require(len(dual) == 52, "triangle dual has wrong length")
    projected_feature = make_projector(factor)

    lines = catalog_path.read_text().splitlines()
    require(lines[0] == data["catalog_header"], "catalog header mismatch")
    require(len(lines) - 1 == data["catalog_atoms"], "wrong catalog size")
    projections = []
    slacks = []
    zero_indices = []
    for atom_index, line in enumerate(lines[1:]):
        fields = tuple(map(int, line.split(",")))
        require(len(fields) == 56, "catalog row has wrong width")
        edges = fields[:21]
        require(
            all(0 <= color <= 6 for color in edges),
            "catalog edge color is outside the quarter grid",
        )
        counts = [0] * 51
        for triangle in fields[21:]:
            require(0 <= triangle < 51, "invalid triangle orbit index")
            counts[triangle] += 1
        projection = atom_projection(edges, projected_feature)
        slack = (
            dual[0]
            + sum(
                dual[1 + triangle] * counts[triangle]
                for triangle in range(51)
            )
            - projection
        )
        require(slack >= 0, f"negative dual slack at atom {atom_index}")
        projections.append(projection)
        slacks.append(slack)
        if slack == 0:
            zero_indices.append(atom_index)

    require(
        digest_integers(projections) == data["atom_projection_sha256"],
        "atom projection digest mismatch",
    )
    require(
        digest_integers(slacks) == data["atom_slack_sha256"],
        "atom slack digest mismatch",
    )
    require(min(slacks) == data["minimum_atom_slack"], "wrong minimum slack")
    require(
        zero_indices == data["zero_slack_catalog_indices"],
        "wrong zero-slack atom list",
    )

    source = json.loads(source_path.read_text())
    target = [Q(1)] + [
        Q(7) * Q(value) / 312 for value in source["nu"]
    ]
    objective = sum(
        coefficient * target_value
        for coefficient, target_value in zip(dual, target)
    )
    require(
        objective == Q(data["target_objective"]),
        "stored target objective mismatch",
    )
    require(objective < 0, "dual target objective is not negative")

    return {
        "status": "PASS",
        "catalog_atoms": len(projections),
        "feature_dimension": 48,
        "sum_of_squares_rank": 8,
        "minimum_atom_slack": min(slacks),
        "target_objective": str(objective),
        "certificate_sha256": sha256(certificate_path),
        "projected_feature_cache_entries": projected_feature.cache_info().currsize,
    }


def main():
    require(
        len(sys.argv) <= 2,
        "usage: verify_exact_catalog_dual.py [certificate]",
    )
    path = Path(sys.argv[1]) if len(sys.argv) == 2 else CERTIFICATE
    print(json.dumps(verify(path), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
