#!/usr/bin/env python3
"""Independent direct-loop audit of the root-triangle catalog dual.

Unlike the primary verifier, this checker takes the monomial orbits from the
authenticated certificate, independently proves that they partition the
degree-at-most-three invariant monomials, expands the eight polynomials
coefficient-by-coefficient, and uses a literal ordered extension-pair loop.
"""

from fractions import Fraction as Q
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    ROOT
    / "experiments"
    / "root_triangle_k7_overlap"
    / "root_triangle_degree3_catalog_dual.json"
)
EXPECTED_SHA256 = (
    "855b236959d64bda50f84eca95afc227b24d463e648e317925dc7766fad2285d"
)
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


class VerificationError(Exception):
    """Raised when the independent exact audit fails."""


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_integers(values):
    payload = "".join(f"{value}\n" for value in values).encode()
    return hashlib.sha256(payload).hexdigest()


def exponent_from_multiset(multiset):
    exponent = [0] * 10
    for index in multiset:
        exponent[index] += 1
    return tuple(exponent)


def edge_actions():
    result = []
    for root_permutation in itertools.permutations((0, 1, 2)):
        for swap_extensions in (False, True):
            vertex_image = {
                0: root_permutation[0],
                1: root_permutation[1],
                2: root_permutation[2],
                3: 4 if swap_extensions else 3,
                4: 3 if swap_extensions else 4,
            }
            result.append(
                tuple(
                    LOCAL_EDGE_INDEX[
                        tuple(
                            sorted(
                                (
                                    vertex_image[first],
                                    vertex_image[second],
                                )
                            )
                        )
                    ]
                    for first, second in LOCAL_EDGES
                )
            )
    return tuple(result)


def act_on_exponent(exponent, action):
    image = [0] * 10
    for old_index, new_index in enumerate(action):
        image[new_index] = exponent[old_index]
    return tuple(image)


def verify_orbit_partition(raw_orbits):
    orbits = tuple(
        tuple(tuple(map(int, exponent)) for exponent in orbit)
        for orbit in raw_orbits
    )
    all_monomials = {
        exponent_from_multiset(multiset)
        for degree in range(4)
        for multiset in itertools.combinations_with_replacement(
            range(10), degree
        )
    }
    flattened = [exponent for orbit in orbits for exponent in orbit]
    require(len(orbits) == 48, "wrong number of feature orbits")
    require(len(flattened) == len(set(flattened)), "feature orbits overlap")
    require(set(flattened) == all_monomials, "feature orbits are incomplete")
    actions = edge_actions()
    for orbit in orbits:
        orbit_set = set(orbit)
        require(
            all(
                act_on_exponent(exponent, action) in orbit_set
                for exponent in orbit
                for action in actions
            ),
            "a stored feature orbit is not invariant",
        )
    return orbits


def rank(matrix):
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
        for entry in range(column, len(work[0])):
            work[pivot_row][entry] /= pivot_value
        for row in range(pivot_row + 1, len(work)):
            scale = work[row][column]
            if scale == 0:
                continue
            for entry in range(column, len(work[0])):
                work[row][entry] -= scale * work[pivot_row][entry]
        pivot_row += 1
    return pivot_row


def make_expanded_polynomials(orbits, factor):
    coefficients = {}
    for row, orbit in enumerate(orbits):
        for exponent in orbit:
            coefficients[exponent] = tuple(factor[row])

    @lru_cache(maxsize=None)
    def evaluate(values):
        result = [0] * 8
        for exponent, coefficient in coefficients.items():
            monomial = 1
            for value, power in zip(values, exponent):
                if power:
                    monomial *= value**power
            for column in range(8):
                result[column] += coefficient[column] * monomial
        return tuple(result)

    return evaluate


def scaled_edge(edges, first, second):
    return edges[PAIR_INDEX7[tuple(sorted((first, second)))]] - 4


def direct_atom_projection(edges, evaluate):
    total = 0
    for root in itertools.combinations(range(7), 3):
        residual = tuple(vertex for vertex in range(7) if vertex not in root)
        extensions = tuple(itertools.combinations(residual, 2))
        values = []
        for extension in extensions:
            vertices = root + extension
            local_values = tuple(
                scaled_edge(edges, vertices[first], vertices[second])
                for first, second in LOCAL_EDGES
            )
            values.append(evaluate(local_values))
        for left, first_extension in enumerate(extensions):
            for right, second_extension in enumerate(extensions):
                coefficient = KERNEL[
                    len(set(first_extension) | set(second_extension))
                ]
                total += coefficient * sum(
                    values[left][column] * values[right][column]
                    for column in range(8)
                )
    return total


def verify(certificate_path=CERTIFICATE):
    require(
        sha256(certificate_path) == EXPECTED_SHA256,
        "certificate hash mismatch",
    )
    data = json.loads(certificate_path.read_text())
    orbits = verify_orbit_partition(data["feature_orbits"])
    factor = tuple(tuple(map(int, row)) for row in data["factor_B"])
    require(
        len(factor) == 48 and all(len(row) == 8 for row in factor),
        "factor has wrong shape",
    )
    require(rank(factor) == 8, "factor does not have rank eight")
    dual = tuple(map(int, data["triangle_dual_Y"]))
    require(len(dual) == 52, "dual has wrong length")
    evaluate = make_expanded_polynomials(orbits, factor)

    source_path = ROOT / data["source"]
    catalog_path = ROOT / data["catalog"]
    require(
        sha256(source_path) == SOURCE_SHA256,
        "source hash mismatch",
    )
    require(
        sha256(catalog_path) == CATALOG_SHA256,
        "catalog hash mismatch",
    )
    projections = []
    slacks = []
    for atom_index, line in enumerate(
        catalog_path.read_text().splitlines()[1:]
    ):
        fields = tuple(map(int, line.split(",")))
        require(len(fields) == 56, "wrong catalog row width")
        projection = direct_atom_projection(fields[:21], evaluate)
        counts = [0] * 51
        for triangle in fields[21:]:
            counts[triangle] += 1
        slack = (
            dual[0]
            + sum(
                dual[triangle + 1] * counts[triangle]
                for triangle in range(51)
            )
            - projection
        )
        require(slack >= 0, f"negative slack at catalog atom {atom_index}")
        projections.append(projection)
        slacks.append(slack)

    require(
        digest_integers(projections) == data["atom_projection_sha256"],
        "independent projection digest mismatch",
    )
    require(
        digest_integers(slacks) == data["atom_slack_sha256"],
        "independent slack digest mismatch",
    )

    source = json.loads(source_path.read_text())
    target = [Q(1)] + [
        Q(7) * Q(value) / 312 for value in source["nu"]
    ]
    objective = sum(
        coefficient * value
        for coefficient, value in zip(dual, target)
    )
    require(objective == Q(data["target_objective"]), "objective mismatch")
    require(objective < 0, "objective is not negative")

    return {
        "status": "PASS",
        "catalog_atoms": len(projections),
        "orbit_partition": "48 orbits partition 286 monomials",
        "direct_ordered_pair_recomputation": "PASS",
        "minimum_atom_slack": min(slacks),
        "target_objective": str(objective),
        "projected_feature_cache_entries": evaluate.cache_info().currsize,
    }


def main():
    require(
        len(sys.argv) <= 2,
        "usage: independent_catalog_dual_audit.py [certificate]",
    )
    path = Path(sys.argv[1]) if len(sys.argv) == 2 else CERTIFICATE
    print(json.dumps(verify(path), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
