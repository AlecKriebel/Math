#!/usr/bin/env python3
"""Independent exact audit using direct ordered extension-pair loops.

This intentionally does not import the optimized verifier.  It rechecks the
53-atom K7 polynomial obstruction and the coarse (h,g)=(4,1) value by a
different enumeration.
"""

from fractions import Fraction as Q
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "experiments"
    / "four_point_depth_projection"
    / "k7_product_audit"
    / "candidate_k7_product_extension.json"
)
EXPECTED_HASH = (
    "1b5e262592e1872cfe9f26b344d82da5066d8332efc5104a34a433d9d5564b00"
)
EXPECTED_POLYNOMIAL = Q(
    -565503106948015359233029224262655736908483321351617,
    1351434081754645134666142095360000000000000000,
)
EXPECTED_HG = Q(-746187, 5)


class VerificationError(Exception):
    """Raised when the independent exact audit fails."""


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def polynomial_audit(source=SOURCE) -> Q:
    require(
        hashlib.sha256(source.read_bytes()).hexdigest() == EXPECTED_HASH,
        "source hash mismatch",
    )
    data = json.loads(source.read_text())
    atoms = data["atoms"]
    key = next(key for key in atoms[0] if key.startswith("edge_color_indices"))
    ps = tuple(itertools.combinations(range(7), 2))
    pair_index = {pair: index for index, pair in enumerate(ps)}
    coefficients = {
        union_size: Q(math.comb(39, union_size), math.comb(5, union_size))
        for union_size in (2, 3, 4)
    }

    def scaled_edge(edges, first, second):
        # Four times the inner product on the quarter grid.
        return edges[pair_index[tuple(sorted((first, second)))]] - 4

    total_scaled = Q(0)
    for atom in atoms:
        edges = tuple(atom[key])
        atom_value = Q(0)
        for first_root, second_root in itertools.permutations(range(7), 2):
            residual = [
                vertex
                for vertex in range(7)
                if vertex not in (first_root, second_root)
            ]
            extensions = tuple(itertools.combinations(residual, 2))
            values = []
            for first, second in extensions:
                scaled_e = scaled_edge(edges, first, second)
                scaled_a = scaled_edge(edges, first_root, first)
                scaled_c = scaled_edge(edges, first_root, second)
                values.append(scaled_e * (8 - 3 * (scaled_a + scaled_c)))
            for left, first_extension in enumerate(extensions):
                for right, second_extension in enumerate(extensions):
                    union_size = len(
                        set(first_extension) | set(second_extension)
                    )
                    atom_value += (
                        coefficients[union_size]
                        * values[left]
                        * values[right]
                    )
        total_scaled += Q(atom["weight"]) * atom_value
    return total_scaled / 256


def coarse_hg_audit() -> Q:
    types = ("G", "H", "H", "H", "H")
    extensions = tuple(itertools.combinations(range(5), 2))
    values = []
    for first, second in extensions:
        if {types[first], types[second]} == {"H", "G"}:
            values.append(1)
        elif types[first] == types[second] == "H":
            values.append(-3)
        else:
            values.append(0)
    total = Q(0)
    for left, first_extension in enumerate(extensions):
        for right, second_extension in enumerate(extensions):
            union_size = len(set(first_extension) | set(second_extension))
            coefficient = Q(
                math.comb(39, union_size), math.comb(5, union_size)
            )
            total += coefficient * values[left] * values[right]
    return total


def abstract_sampling_audit():
    """Exhaust a small integer table and verify coefficient cancellation."""

    # One root, R=6 residual vertices, and m=4 sampled residual vertices.
    residual_count = 6
    sample_count = 4
    extensions = tuple(itertools.combinations(range(residual_count), 2))
    values = {
        extension: (extension[0] + 2) * (3 - extension[1])
        for extension in extensions
    }
    global_square = sum(values.values()) ** 2
    accumulated = Q(0)
    samples = tuple(
        itertools.combinations(range(residual_count), sample_count)
    )
    for sample in samples:
        local_extensions = tuple(itertools.combinations(sample, 2))
        local = Q(0)
        for first in local_extensions:
            for second in local_extensions:
                union_size = len(set(first) | set(second))
                local += (
                    Q(
                        math.comb(residual_count, union_size),
                        math.comb(sample_count, union_size),
                    )
                    * values[first]
                    * values[second]
                )
        accumulated += local
    require(
        accumulated / len(samples) == global_square,
        "abstract finite-sampling identity failed",
    )


def verify(source=SOURCE):
    abstract_sampling_audit()
    polynomial = polynomial_audit(source)
    coarse = coarse_hg_audit()
    require(
        polynomial == EXPECTED_POLYNOMIAL and polynomial < 0,
        "K7 polynomial audit value mismatch or nonnegative",
    )
    require(
        coarse == EXPECTED_HG and coarse < 0,
        "coarse H/G audit value mismatch or nonnegative",
    )
    return {
        "status": "PASS",
        "abstract_sampling_identity": "PASS",
        "K7_product_53_polynomial_row": str(polynomial),
        "continuous_counteratom_H_G_row": str(coarse),
    }


def main():
    require(
        len(sys.argv) <= 2,
        "usage: independent_flag_audit.py [K7-source]",
    )
    source = Path(sys.argv[1]) if len(sys.argv) == 2 else SOURCE
    print(json.dumps(verify(source), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
