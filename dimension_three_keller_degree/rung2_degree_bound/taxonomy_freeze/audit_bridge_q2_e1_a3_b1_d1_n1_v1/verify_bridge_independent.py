#!/usr/bin/env python3
"""Independent fail-closed replay of the frozen fixed-linear bridge.

This checker was written after the pre-comparison route in RESEARCH_LOG.md
was sealed.  It uses only the Python standard library.  In particular it
does not import the candidate checker or SymPy.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import os
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path
from typing import Iterable


if not __debug__:
    raise SystemExit("FAIL: refusing optimized Python")

HERE = Path(__file__).resolve().parent
TAXONOMY = HERE.parent
RUNG = TAXONOMY.parent
MUTATION = os.environ.get("BRIDGE_AUDIT_MUTATION", "")

TARGET_ROW = "Q2-E1-A3-B1-D1-N1"
PIVOTS = [f"C{i:02d}" for i in range(45)]
MONOMIAL_NAMES = [
    "x^4",
    "x^3*y",
    "x^3*z",
    "x^2*y^2",
    "x^2*y*z",
    "x^2*z^2",
    "x*y^3",
    "x*y^2*z",
    "x*y*z^2",
    "x*z^3",
    "y^4",
    "y^3*z",
    "y^2*z^2",
    "y*z^3",
    "z^4",
]
QUARTIC_EXPONENTS = [
    (4, 0, 0),
    (3, 1, 0),
    (3, 0, 1),
    (2, 2, 0),
    (2, 1, 1),
    (2, 0, 2),
    (1, 3, 0),
    (1, 2, 1),
    (1, 1, 2),
    (1, 0, 3),
    (0, 4, 0),
    (0, 3, 1),
    (0, 2, 2),
    (0, 1, 3),
    (0, 0, 4),
]

# Every theorem and hostile report used by a terminal is pinned.  The
# quadratic-component report hash is filled only after the standalone audit
# has completed with PASS.
EXPECTED_HASHES = {
    "taxonomy_freeze/FROZEN_TAXONOMY_v1.md":
        "41fccc44d23fab125819990a2b27526771fbfb62293910b98cfcf1821576d03d",
    "taxonomy_freeze/frozen_manifest_v1.json":
        "5a2bdd57438e9ebcca18d04c53ebc98ced2b61209e2de99674aede501c615c23",
    "taxonomy_freeze/BRIDGE_Q2_E1_A3_B1_D1_N1_v1.md":
        "51f864184ac0eddea9ff8b4e0ab9f635ced58d02c7a42dfdb1b03141f727f740",
    "taxonomy_freeze/verify_bridge_q2_e1_a3_b1_d1_n1_v1.py":
        "700e6e487a91920f6292a4c89dadc1133e7949a0a9546a1b194deaa3006b718f",
    "WORKING_QUADRATIC_COMPONENT_EXIT.md":
        "f8a7c92c1631f4efbc5b452d76c8f5ae2121c730173f374ffb736eda37f627de",
    "VERIFICATION.md":
        "71190f6e6b68fb7e3837c76bb944fac2e85a7c92ed938f471d05e9497b6eb9e8",
    "audit_quadratic_component_exit/REPORT.md":
        "8ee4a3ce87c3045b6f4dde58c5e20466e75e1ac4cecc5167a3853933d04aeb32",
    "audit_quadratic_component_exit/verify_quadratic_component_exit_exact.py":
        "83895187f49fb2d8a79f086c334d1e634c84769f9733d3293f7a633f4601bf41",
    "fixed_linear_cubic_pencil/WORKING_HORIZONTAL_FIXED_LINEAR_CUBIC_PENCIL.md":
        "b034cfb8770870336ec24809467e0ed2f56fa89491d349dcc8c8f2a67ea45a03",
    "fixed_linear_cubic_pencil/audit_hostile/REPORT.md":
        "4566cda4c40b6065f38d6e85cda9004dceff57e21db9295677dc163ba24ee651",
    "fixed_linear_cubic_pencil/vertical_locus/WORKING_VERTICAL_FIXED_LINEAR_CUBIC_PENCIL.md":
        "707320e8658972cbc459131ccb41f8fd2524cde2621c4461f627895518260ef7",
    "fixed_linear_cubic_pencil/vertical_locus/audit_vertical_hostile/REPORT.md":
        "e4cb1ca80daa0eb30a2429b0410852feb7190cc9365a7947f869e9b32c0da35f",
    "fixed_linear_cubic_pencil/vertical_locus/E8_E4_RANK_LEDGER.md":
        "53ce0d8d8c99d60f3fd22b45672414ccf9f17a67ce576949fb51b37c5452301f",
    "fixed_linear_cubic_pencil/vertical_locus/NONVERTICAL_NONTRIPLE_LEMMA.md":
        "9e30f4351627947da09a4078c784812c3d0d4c59b34503b22368926939ecfd95",
    "fixed_linear_cubic_pencil/vertical_locus/NONVERTICAL_TRIPLE_ROOT_LEMMA.md":
        "fa050695842947653c254d3c1e3eff8136369bc0fd1d0fa7404f1aa634000383",
    "fixed_linear_cubic_pencil/vertical_locus/audit_nonvertical_companion/REPORT.md":
        "d3bab04b66f9f74573d4de7b2e57347b28b4f8fb7dcc7b685671eb46acf81df3",
    "fixed_linear_cubic_pencil/vertical_locus/VERTICAL_ELL_ZERO_NONTRIPLE_LEMMA.md":
        "5e4f4c4f4f7e3b89eb868f8d42cfe27d38a134340e2623f36cef3c5fb566eefc",
    "fixed_linear_cubic_pencil/vertical_locus/audit_vertical_ell_zero_nontriple/REPORT.md":
        "1c30086082a2871d4fb1bce62bd9bd0a743306bd5a48132e2b136d13105e032f",
    "fixed_linear_cubic_pencil/vertical_locus/VERTICAL_NONZERO_ELL_NONTRIPLE_LEMMA.md":
        "47b7730afb582f1422517dbd7e08ec8bbdb79ca2a837f317a828a859efdd81e6",
    "fixed_linear_cubic_pencil/vertical_locus/audit_vertical_nonzero_ell_nontriple/REPORT.md":
        "41075ac6bf35c686947546773627e115be4eb05959db0ee9c2ff31ebb598d135",
    "fixed_linear_cubic_pencil/vertical_locus/VERTICAL_TRIPLE_GAMMA0_REDUCTION.md":
        "28a3cd191bb1e74cd4e8ae5ebf7dcaa938602b318c2f49b006838641c6979e58",
    "fixed_linear_cubic_pencil/vertical_locus/audit_vertical_triple_gamma0_reduction/REPORT.md":
        "40f4830bd4603e7a8e1bae97b57b8a113af4f4ecbcadc65000a605380a414842",
    "fixed_linear_cubic_pencil/vertical_locus/VERTICAL_TRIPLE_GAMMA0_ELL0_LEMMA.md":
        "b11f1c320a5bd6a347112daf7359bf91576c529046d3e2718fcfc92f5f5db2d5",
    "fixed_linear_cubic_pencil/vertical_locus/audit_vertical_triple_gamma0_ell0/REPORT.md":
        "d2e8e1bd798b0cf1448a6254e0e68e5c55aa44552978421b0ed6fc58415c55ec",
    "fixed_linear_cubic_pencil/vertical_locus/VERTICAL_TRIPLE_GAMMA_NONZERO_EXCLUSION.md":
        "e04782d2b2ecacbbfded9be4558145e9601d5b4e6fc914ad26444c40cfe86a7b",
    "fixed_linear_cubic_pencil/vertical_locus/audit_vertical_triple_gamma_nonzero/REPORT.md":
        "4410f0561b4b894739851d4a80b539855b369012be207998b7d135d89e830137",
    "fixed_linear_cubic_pencil/vertical_locus/VERTICAL_A0_W0_ZERO_EXCLUSION.md":
        "d1f0889a54d9185a4f899d7ca6f5eb702a040a8cfdcb1733a4427896940eb09c",
    "fixed_linear_cubic_pencil/vertical_locus/audit_vertical_a0_w0_zero/REPORT.md":
        "d8d291d03e269d0ee769bc96dded535abd5f9df11cd79d1994a19b6318700587",
    "fixed_linear_cubic_pencil/vertical_locus/a0_w0_nonzero_attack/NOTE.md":
        "b38459777db826a3c17fa74aaf7472cc654ae0ba0d7ca96a9cbc14cc56229cda",
    "fixed_linear_cubic_pencil/vertical_locus/audit_a0_w0_nonzero/REPORT.md":
        "c77abb4a2bf845614a6a1c320afcb916b7bf0477075e38469faebc5bc4dd0547",
}

Q = "WORKING_QUADRATIC_COMPONENT_EXIT.md"
QA = "audit_quadratic_component_exit/REPORT.md"
V = "fixed_linear_cubic_pencil/vertical_locus/"
C = "fixed_linear_cubic_pencil/"

# Candidate-level terminals.  Some terminals use a chain of two audited
# theorems; every listed audit is mandatory.
ROUTES = {
    "horizontal": {
        "theorems": (C + "WORKING_HORIZONTAL_FIXED_LINEAR_CUBIC_PENCIL.md",),
        "audits": (C + "audit_hostile/REPORT.md",),
    },
    "vertical_m1_G0": {
        "theorems": (V + "WORKING_VERTICAL_FIXED_LINEAR_CUBIC_PENCIL.md", Q),
        "audits": (V + "audit_vertical_hostile/REPORT.md", QA),
    },
    "vertical_m2_G0": {
        "theorems": (V + "WORKING_VERTICAL_FIXED_LINEAR_CUBIC_PENCIL.md", Q),
        "audits": (V + "audit_vertical_hostile/REPORT.md", QA),
    },
    "vertical_m3_G0": {
        "theorems": (V + "WORKING_VERTICAL_FIXED_LINEAR_CUBIC_PENCIL.md", Q),
        "audits": (V + "audit_vertical_hostile/REPORT.md", QA),
    },
    "vertical_m3_nonvertical_squarefree": {
        "theorems": (V + "NONVERTICAL_NONTRIPLE_LEMMA.md",),
        "audits": (V + "audit_nonvertical_companion/REPORT.md",),
    },
    "vertical_m3_nonvertical_double": {
        "theorems": (V + "NONVERTICAL_NONTRIPLE_LEMMA.md",),
        "audits": (V + "audit_nonvertical_companion/REPORT.md",),
    },
    "vertical_m3_nonvertical_triple": {
        "theorems": (V + "NONVERTICAL_TRIPLE_ROOT_LEMMA.md",),
        "audits": (V + "audit_nonvertical_companion/REPORT.md",),
    },
    "vertical_m3_vertical_s_nonzero_squarefree_ell_zero": {
        "theorems": (V + "VERTICAL_ELL_ZERO_NONTRIPLE_LEMMA.md",),
        "audits": (V + "audit_vertical_ell_zero_nontriple/REPORT.md",),
    },
    "vertical_m3_vertical_s_nonzero_squarefree_ell_nonzero": {
        "theorems": (V + "VERTICAL_NONZERO_ELL_NONTRIPLE_LEMMA.md",),
        "audits": (V + "audit_vertical_nonzero_ell_nontriple/REPORT.md",),
    },
    "vertical_m3_vertical_s_nonzero_double_ell_zero": {
        "theorems": (V + "VERTICAL_ELL_ZERO_NONTRIPLE_LEMMA.md",),
        "audits": (V + "audit_vertical_ell_zero_nontriple/REPORT.md",),
    },
    "vertical_m3_vertical_s_nonzero_double_ell_nonzero": {
        "theorems": (V + "VERTICAL_NONZERO_ELL_NONTRIPLE_LEMMA.md",),
        "audits": (V + "audit_vertical_nonzero_ell_nontriple/REPORT.md",),
    },
    "vertical_m3_vertical_s_nonzero_triple_gamma_nonzero": {
        "theorems": (V + "VERTICAL_TRIPLE_GAMMA_NONZERO_EXCLUSION.md",),
        "audits": (V + "audit_vertical_triple_gamma_nonzero/REPORT.md",),
    },
    "vertical_m3_vertical_s_nonzero_triple_gamma_zero": {
        "theorems": (
            V + "VERTICAL_TRIPLE_GAMMA0_REDUCTION.md",
            V + "VERTICAL_TRIPLE_GAMMA0_ELL0_LEMMA.md",
        ),
        "audits": (
            V + "audit_vertical_triple_gamma0_reduction/REPORT.md",
            V + "audit_vertical_triple_gamma0_ell0/REPORT.md",
        ),
    },
    "vertical_m3_vertical_s_zero_W0_zero": {
        "theorems": (V + "VERTICAL_A0_W0_ZERO_EXCLUSION.md",),
        "audits": (V + "audit_vertical_a0_w0_zero/REPORT.md",),
    },
    "vertical_m3_vertical_s_zero_W0_nonzero": {
        "theorems": (V + "a0_w0_nonzero_attack/NOTE.md",),
        "audits": (V + "audit_a0_w0_nonzero/REPORT.md",),
    },
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def digest(path: Path) -> str:
    require(path.is_file(), f"missing pinned input: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


# Sparse exact polynomials.  Exponent tuples may have any fixed length.
Poly = dict[tuple[int, ...], int]


def clean(poly: Poly) -> Poly:
    return {monomial: coefficient for monomial, coefficient in poly.items()
            if coefficient}


def constant(value: int, variables: int) -> Poly:
    return {} if value == 0 else {(0,) * variables: value}


def variable(variables: int, index: int) -> Poly:
    exponent = [0] * variables
    exponent[index] = 1
    return {tuple(exponent): 1}


def monomial(exponent: tuple[int, ...], coefficient: int = 1) -> Poly:
    return {} if coefficient == 0 else {exponent: coefficient}


def add(left: Poly, right: Poly) -> Poly:
    result = dict(left)
    for exponent, coefficient in right.items():
        result[exponent] = result.get(exponent, 0) + coefficient
    return clean(result)


def scale(poly: Poly, scalar: int) -> Poly:
    return clean({exponent: scalar * coefficient
                  for exponent, coefficient in poly.items()})


def subtract(left: Poly, right: Poly) -> Poly:
    return add(left, scale(right, -1))


def multiply(left: Poly, right: Poly) -> Poly:
    if not left or not right:
        return {}
    result: Poly = {}
    for exponent_left, coefficient_left in left.items():
        for exponent_right, coefficient_right in right.items():
            exponent = tuple(
                a + b for a, b in zip(exponent_left, exponent_right)
            )
            result[exponent] = (
                result.get(exponent, 0)
                + coefficient_left * coefficient_right
            )
    return clean(result)


def derivative(poly: Poly, index: int) -> Poly:
    result: Poly = {}
    for exponent, coefficient in poly.items():
        if exponent[index] == 0:
            continue
        lowered = list(exponent)
        lowered[index] -= 1
        result[tuple(lowered)] = coefficient * exponent[index]
    return clean(result)


def determinant(matrix: list[list[Poly]], variables: int) -> Poly:
    size = len(matrix)
    require(size > 0 and all(len(row) == size for row in matrix),
            "determinant requires a square matrix")
    result: Poly = {}
    for permutation in itertools.permutations(range(size)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(size)
            for j in range(i + 1, size)
        )
        term = constant(-1 if inversions % 2 else 1, variables)
        for row, column in enumerate(permutation):
            term = multiply(term, matrix[row][column])
        result = add(result, term)
    return result


def minor_matrix(matrix: list[list[Poly]], row: int, column: int) -> list[list[Poly]]:
    return [
        [entry for j, entry in enumerate(source_row) if j != column]
        for i, source_row in enumerate(matrix)
        if i != row
    ]


def adjugate(matrix: list[list[Poly]], variables: int) -> list[list[Poly]]:
    size = len(matrix)
    return [
        [
            scale(
                determinant(minor_matrix(matrix, column, row), variables),
                -1 if (row + column) % 2 else 1,
            )
            for column in range(size)
        ]
        for row in range(size)
    ]


def matrix_vector_product(matrix: list[list[Poly]], vector_: list[Poly]) -> list[Poly]:
    return [
        sum_polynomials(multiply(entry, value)
                        for entry, value in zip(row, vector_))
        for row in matrix
    ]


def sum_polynomials(polynomials: Iterable[Poly]) -> Poly:
    result: Poly = {}
    for poly in polynomials:
        result = add(result, poly)
    return result


def rational_rank(matrix: list[list[int]]) -> int:
    rows = [[Fraction(value) for value in row] for row in matrix]
    if not rows:
        return 0
    row_count = len(rows)
    column_count = len(rows[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count)
             if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        pivot_value = rows[pivot_row][column]
        rows[pivot_row] = [value / pivot_value for value in rows[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(rows[row], rows[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def verify_hashes() -> None:
    for relative, expected in EXPECTED_HASHES.items():
        actual = digest(RUNG / relative)
        require(actual == expected, f"pinned input hash mismatch: {relative}")


def verify_manifest() -> None:
    manifest = json.loads(
        (TAXONOMY / "frozen_manifest_v1.json").read_text(encoding="utf-8")
    )
    require(manifest["version"] == 1, "wrong freeze version")
    require(manifest["frozen_row_count"] == 14, "wrong frozen row count")
    require(manifest["pivot_strata_per_row"] == 45, "wrong pivot count")
    require(manifest["pivot_ids"] == PIVOTS, "wrong exact frozen pivot IDs")
    require(
        manifest["coefficient_order"]["target_components"] == [1, 2, 3],
        "wrong target-component order",
    )
    require(
        manifest["coefficient_order"]["degree_four_monomials"]
        == MONOMIAL_NAMES,
        "wrong monomial order",
    )
    rows = [row for row in manifest["rows"] if row["id"] == TARGET_ROW]
    require(len(rows) == 1, "target row missing or duplicated")
    require(rows[0]["rank"] == 2, "target row rank changed")
    require(rows[0]["tuple"] == [1, 3, 1, 1, 1],
            "target row tuple changed")


def verify_target_normalization() -> None:
    variables = 6
    avec = [variable(variables, index) for index in range(3)]
    bvec = [variable(variables, 3 + index) for index in range(3)]
    zero = constant(0, variables)
    one = constant(1, variables)
    charts = [(0, 1, 2), (0, 2, 1), (1, 2, 0)]
    if MUTATION == "drop_normalization_chart":
        charts.pop()
    require(len(charts) == 3, "normalization charts incomplete")
    observed_pairs: set[tuple[int, int]] = set()
    for i, j, k in charts:
        standard = [zero, zero, zero]
        standard[k] = one
        basis = [
            [avec[row], bvec[row], standard[row]]
            for row in range(3)
        ]
        determinant_ = determinant(basis, variables)
        delta = subtract(multiply(avec[i], bvec[j]),
                         multiply(avec[j], bvec[i]))
        require(determinant_ in (delta, scale(delta, -1)),
                f"normalization chart determinant mismatch: {(i, j)}")
        adj = adjugate(basis, variables)
        first = matrix_vector_product(adj, avec)
        second = matrix_vector_product(adj, bvec)
        require(first == [determinant_, zero, zero],
                f"first target vector not normalized on {(i, j)}")
        require(second == [zero, determinant_, zero],
                f"second target vector not normalized on {(i, j)}")
        observed_pairs.add((i, j))
    require(observed_pairs == {(0, 1), (0, 2), (1, 2)},
            "rank-two target-minor cover incomplete")


def coefficient_vector(components: tuple[Poly, Poly, Poly]) -> list[int]:
    return [
        component.get(exponent, 0)
        for component in components
        for exponent in QUARTIC_EXPONENTS
    ]


def jacobian_rank_at_least_two(components: tuple[Poly, Poly, Poly]) -> bool:
    jacobian = [
        [derivative(component, column) for column in range(3)]
        for component in components
    ]
    for rows in itertools.combinations(range(3), 2):
        for columns in itertools.combinations(range(3), 2):
            two_minor = subtract(
                multiply(jacobian[rows[0]][columns[0]],
                         jacobian[rows[1]][columns[1]]),
                multiply(jacobian[rows[0]][columns[1]],
                         jacobian[rows[1]][columns[0]]),
            )
            if two_minor:
                return True
    return False


def verify_pivots() -> tuple[set[str], set[str]]:
    coordinate_variables = [variable(3, index) for index in range(3)]
    fermat = {
        (3, 0, 0): 1,
        (0, 3, 0): 1,
        (0, 0, 3): 1,
    }

    quadratic_basis = [
        (2, 0, 0), (1, 1, 0), (1, 0, 1),
        (0, 2, 0), (0, 1, 1), (0, 0, 2),
    ]
    gradient_matrix = [
        [derivative(fermat, index).get(exponent, 0)
         for exponent in quadratic_basis]
        for index in range(3)
    ]
    require(rational_rank(gradient_matrix) == 3,
            "Fermat witness has fewer than three essential variables")

    routed: set[str] = set()
    for index, exponent in enumerate(QUARTIC_EXPONENTS):
        divisor_index = next(i for i, value in enumerate(exponent) if value)
        h = coordinate_variables[divisor_index]
        residual_exponent = list(exponent)
        residual_exponent[divisor_index] -= 1
        p = monomial(tuple(residual_exponent))
        quartic = monomial(exponent)
        require(multiply(h, p) == quartic, "bad pivot witness factorization")

        # Since p is a monomial, gcd(p, Fermat)=1 iff no coordinate divides
        # every Fermat term.  This exact exponent check avoids a CAS gcd.
        common_exponent = tuple(
            min(residual_exponent[coordinate],
                *(term[coordinate] for term in fermat))
            for coordinate in range(3)
        )
        require(common_exponent == (0, 0, 0),
                "pivot witness residual cubics are not coprime")
        h_fermat = multiply(h, fermat)
        for block, components in (
            (0, (quartic, h_fermat, {})),
            (1, ({}, quartic, h_fermat)),
        ):
            vector_ = coefficient_vector(components)
            nonzero = [position for position, value in enumerate(vector_)
                       if value]
            expected = 15 * block + index
            require(nonzero and nonzero[0] == expected,
                    f"wrong witness pivot C{expected:02d}")
            require(jacobian_rank_at_least_two(components),
                    f"witness rank dropped at C{expected:02d}")
            routed.add(f"C{expected:02d}")

    empty = set(PIVOTS[30:])
    if MUTATION == "drop_pivot":
        routed.remove("C29")
    elif MUTATION == "overlap_pivot":
        routed.add("C30")
    require(routed == set(PIVOTS[:30]),
            "potential frozen pivots are not exactly C00--C29")
    require(empty == {f"C{i:02d}" for i in range(30, 45)},
            "forced-empty pivots are not exactly C30--C44")
    require(routed.isdisjoint(empty), "routed and empty pivots overlap")
    require(routed | empty == set(PIVOTS), "45-pivot coverage has a gap")

    # A first pivot at 30 or later makes target rows 1 and 2 identically
    # zero in the frozen component-major order.  A one-row Jacobian has no
    # nonzero 2x2 minor, contradicting rank two.
    require(all(index // 15 == 2 for index in range(30, 45)),
            "late-pivot rank certificate uses a wrong target block")
    return routed, empty


def make_state(**entries: str) -> tuple[tuple[str, str], ...]:
    return tuple(sorted(entries.items()))


def atomic_states() -> list[tuple[tuple[str, str], ...]]:
    states = [make_state(scope="horizontal")]
    states.extend([
        make_state(scope="vertical", m="1"),
        make_state(scope="vertical", m="2"),
        make_state(scope="vertical", m="3", companion="zero"),
    ])

    q_charts = (
        ("squarefree", "-"),
        ("double", "-"),
        ("triple", "C"),
        ("triple", "B"),
        ("triple", "E"),
    )
    for root, chart in q_charts:
        states.append(make_state(
            scope="vertical", m="3", companion="q",
            root=root, chart=chart,
        ))

    ell_positions = {
        "squarefree": (
            "zero", "generic", "root_x", "root_y", "root_x_minus_y",
        ),
        "double": ("zero", "generic", "double_root_x", "simple_root_y"),
    }
    for root, positions in ell_positions.items():
        for ell in positions:
            states.append(make_state(
                scope="vertical", m="3", companion="z3", s="nonzero",
                root=root, ell=ell,
            ))

    for chart in ("C", "B", "E"):
        states.append(make_state(
            scope="vertical", m="3", companion="z3", s="nonzero",
            root="triple", chart=chart, gamma="nonzero",
        ))
        for ell in ("zero", "nonzero"):
            states.append(make_state(
                scope="vertical", m="3", companion="z3", s="nonzero",
                root="triple", chart=chart, gamma="zero", ell=ell,
            ))

    for root, chart in q_charts:
        states.append(make_state(
            scope="vertical", m="3", companion="z3", s="zero",
            W0="zero", root=root, chart=chart,
        ))

    incidence = {
        ("rank2", "squarefree"): ("none", "one", "both"),
        ("rank2", "double"): (
            "none", "double_root", "simple_root", "both",
        ),
        ("rank2", "triple"): ("none", "triple_root"),
        ("rank1", "squarefree"): ("m0", "m1"),
        ("rank1", "double"): ("m0", "m1_simple", "m2_double"),
        ("rank1", "triple"): ("m0", "m3"),
    }
    for (w_rank, root), positions in incidence.items():
        for position in positions:
            states.append(make_state(
                scope="vertical", m="3", companion="z3", s="zero",
                W0="nonzero", W0_rank=w_rank,
                root=root, incidence=position,
            ))

    if MUTATION == "drop_atom":
        states.pop()
    require(len(states) == 48, f"expected 48 audit atoms, got {len(states)}")
    require(len(states) == len(set(states)), "duplicate audit atom")
    return states


def terminal_predicates(
    state_: tuple[tuple[str, str], ...],
) -> dict[str, bool]:
    cell = dict(state_)
    scope = cell["scope"]
    m = cell.get("m")
    companion = cell.get("companion")
    root = cell.get("root")
    s = cell.get("s")
    ell = cell.get("ell")
    gamma = cell.get("gamma")
    w0 = cell.get("W0")
    predicates = {
        "horizontal": scope == "horizontal",
        "vertical_m1_G0": scope == "vertical" and m == "1",
        "vertical_m2_G0": scope == "vertical" and m == "2",
        "vertical_m3_G0": (
            scope == "vertical" and m == "3" and companion == "zero"
        ),
        "vertical_m3_nonvertical_squarefree": (
            companion == "q" and root == "squarefree"
        ),
        "vertical_m3_nonvertical_double": (
            companion == "q" and root == "double"
        ),
        "vertical_m3_nonvertical_triple": (
            companion == "q" and root == "triple"
        ),
        "vertical_m3_vertical_s_nonzero_squarefree_ell_zero": (
            companion == "z3" and s == "nonzero"
            and root == "squarefree" and ell == "zero"
        ),
        "vertical_m3_vertical_s_nonzero_squarefree_ell_nonzero": (
            companion == "z3" and s == "nonzero"
            and root == "squarefree" and ell not in (None, "zero")
        ),
        "vertical_m3_vertical_s_nonzero_double_ell_zero": (
            companion == "z3" and s == "nonzero"
            and root == "double" and ell == "zero"
        ),
        "vertical_m3_vertical_s_nonzero_double_ell_nonzero": (
            companion == "z3" and s == "nonzero"
            and root == "double" and ell not in (None, "zero")
        ),
        "vertical_m3_vertical_s_nonzero_triple_gamma_nonzero": (
            companion == "z3" and s == "nonzero"
            and root == "triple" and gamma == "nonzero"
        ),
        "vertical_m3_vertical_s_nonzero_triple_gamma_zero": (
            companion == "z3" and s == "nonzero"
            and root == "triple" and gamma == "zero"
        ),
        "vertical_m3_vertical_s_zero_W0_zero": (
            companion == "z3" and s == "zero" and w0 == "zero"
        ),
        "vertical_m3_vertical_s_zero_W0_nonzero": (
            companion == "z3" and s == "zero" and w0 == "nonzero"
        ),
    }
    if MUTATION == "overlap_terminal" and m == "1":
        predicates["horizontal"] = True
    return predicates


def verify_routes() -> tuple[int, int]:
    routes = {
        terminal: {
            "theorems": tuple(data["theorems"]),
            "audits": tuple(data["audits"]),
        }
        for terminal, data in ROUTES.items()
    }
    if MUTATION == "drop_terminal":
        routes.pop("vertical_m3_vertical_s_nonzero_triple_gamma_zero")
    elif MUTATION == "unaudit_a0":
        routes["vertical_m3_vertical_s_zero_W0_nonzero"]["audits"] = ()
    elif MUTATION == "unaudit_quadratic":
        for terminal in ("vertical_m1_G0", "vertical_m2_G0", "vertical_m3_G0"):
            routes[terminal]["audits"] = tuple(
                audit for audit in routes[terminal]["audits"] if audit != QA
            )

    states = atomic_states()
    used: set[str] = set()
    for state_ in states:
        matches = [
            terminal for terminal, matches_
            in terminal_predicates(state_).items()
            if matches_
        ]
        require(len(matches) == 1,
                f"audit atom has {len(matches)} routes: {dict(state_)}")
        terminal = matches[0]
        require(terminal in routes, f"terminal lacks route record: {terminal}")
        used.add(terminal)
    require(used == set(routes), "terminal ledger has unused or missing routes")
    require(len(routes) == 15, f"expected 15 terminals, got {len(routes)}")

    for terminal, data in routes.items():
        require(data["theorems"], f"terminal lacks theorem: {terminal}")
        require(data["audits"], f"terminal lacks hostile audit: {terminal}")
        for relative in data["theorems"] + data["audits"]:
            require(relative in EXPECTED_HASHES,
                    f"terminal input is not hash-pinned: {relative}")
            require((RUNG / relative).is_file(),
                    f"terminal input is missing: {relative}")

    # The three G=0 terminals must use the *standalone* hostile report, not
    # only the aggregate prose in VERIFICATION.md.
    for terminal in ("vertical_m1_G0", "vertical_m2_G0", "vertical_m3_G0"):
        require(QA in routes[terminal]["audits"],
                f"quadratic-component provenance gap at {terminal}")

    # Pin-based checking is primary.  These markers give a readable guard
    # against accidentally pinning a non-PASS report under the right name.
    audit_markers = {
        C + "audit_hostile/REPORT.md": "**PASS**",
        QA: "PASS",
        V + "audit_vertical_hostile/REPORT.md": "Verdict: PASS",
        V + "audit_nonvertical_companion/REPORT.md": "**PASS**",
        V + "audit_vertical_ell_zero_nontriple/REPORT.md": "**PASS**",
        V + "audit_vertical_nonzero_ell_nontriple/REPORT.md": "**PASS**",
        V + "audit_vertical_triple_gamma0_reduction/REPORT.md": "**PASS**",
        V + "audit_vertical_triple_gamma0_ell0/REPORT.md": "**PASS**",
        V + "audit_vertical_triple_gamma_nonzero/REPORT.md": "**PASS**",
        V + "audit_vertical_a0_w0_zero/REPORT.md": "**PASS**",
        V + "audit_a0_w0_nonzero/REPORT.md": "Verdict: PASS",
    }
    for relative, marker in audit_markers.items():
        text = (RUNG / relative).read_text(encoding="utf-8")
        require(marker in text, f"hostile report lacks PASS marker: {relative}")
    return len(states), len(routes)


def verify_candidate_status() -> int:
    bridge = (
        TAXONOMY / "BRIDGE_Q2_E1_A3_B1_D1_N1_v1.md"
    ).read_text(encoding="utf-8")
    candidate_checker = (
        TAXONOMY / "verify_bridge_q2_e1_a3_b1_d1_n1_v1.py"
    ).read_text(encoding="utf-8")
    required_current_markers = (
        "PASS as an unconditional candidate",
        "audit_a0_w0_nonzero/REPORT.md",
        "audit_quadratic_component_exit/REPORT.md",
        "Status labels repaired",
    )
    for marker in required_current_markers:
        require(marker in bridge, f"current candidate marker missing: {marker}")
    require(
        '"vertical_m3_vertical_s_zero_W0_nonzero": False'
        in candidate_checker,
        "candidate checker does not close the final terminal",
    )
    require(
        ": True" not in candidate_checker[
            candidate_checker.index("EXPECTED_TERMINALS = {"):
            candidate_checker.index("}\n\n\ndef require")
        ],
        "candidate checker retains a conditional terminal",
    )

    repaired_headers = {
        V + "WORKING_VERTICAL_FIXED_LINEAR_CUBIC_PENCIL.md":
            "independent hostile audit\npassed",
        V + "NONVERTICAL_NONTRIPLE_LEMMA.md":
            "hostile audit passed",
        V + "NONVERTICAL_TRIPLE_ROOT_LEMMA.md":
            "hostile audit passed",
        V + "E8_E4_RANK_LEDGER.md":
            "complete audited exclusion",
        V + "a0_w0_nonzero_attack/NOTE.md":
            "independent hostile audit passed",
        Q:
            "standalone\nhostile report",
    }
    for relative, marker in repaired_headers.items():
        require(marker in (RUNG / relative).read_text(encoding="utf-8"),
                f"repaired status header missing: {relative}")
    return 0


def probe_original_checker() -> None:
    """Confirm that the repaired supplied checker rejects text mutations."""

    with tempfile.TemporaryDirectory(prefix="fixed-linear-bridge-audit-") as tmp:
        shadow_rung = Path(tmp) / "rung2_degree_bound"
        shutil.copytree(RUNG, shadow_rung)
        shadow_taxonomy = shadow_rung / "taxonomy_freeze"
        fake_bridge = "\n".join([
            r"R/\mathrm C_{00}",
            r"R/\mathrm C_{29}",
            r"R/\mathrm C_{30}",
            r"R/\mathrm C_{44}",
            r"\operatorname{rank}\rho_h=2",
            r"\operatorname{rank}\rho_h=1",
            "VERTICAL_TRIPLE_GAMMA_NONZERO_EXCLUSION.md",
            "a0_w0_nonzero_attack/NOTE.md",
            "does **not** promote",
            "sole conditional theorem input",
        ])
        bridge_path = shadow_taxonomy / "BRIDGE_Q2_E1_A3_B1_D1_N1_v1.md"
        bridge_path.write_text(fake_bridge, encoding="utf-8")

        candidate = (
            shadow_taxonomy / "verify_bridge_q2_e1_a3_b1_d1_n1_v1.py"
        )
        supplied = subprocess.run(
            [sys.executable, str(candidate)],
            cwd=shadow_rung,
            text=True,
            capture_output=True,
            timeout=60,
            check=False,
        )
        require(
            supplied.returncode != 0
            and "pinned-input hash mismatch" in supplied.stderr,
            "supplied checker accepted the semantic bridge mutation",
        )

        independent = (
            shadow_taxonomy
            / "audit_bridge_q2_e1_a3_b1_d1_n1_v1"
            / "verify_bridge_independent.py"
        )
        hostile = subprocess.run(
            [sys.executable, str(independent)],
            cwd=shadow_rung,
            text=True,
            capture_output=True,
            timeout=60,
            check=False,
        )
        require(
            hostile.returncode != 0
            and "pinned input hash mismatch" in hostile.stderr,
            "independent checker accepted the semantic bridge mutation",
        )

        pinned_input = (
            shadow_rung
            / "fixed_linear_cubic_pencil"
            / "WORKING_HORIZONTAL_FIXED_LINEAR_CUBIC_PENCIL.md"
        )
        pinned_input.write_bytes(pinned_input.read_bytes() + b"\n")
        supplied_hash = subprocess.run(
            [sys.executable, str(candidate)],
            cwd=shadow_rung,
            text=True,
            capture_output=True,
            timeout=60,
            check=False,
        )
        require(
            supplied_hash.returncode != 0
            and "pinned-input hash mismatch" in supplied_hash.stderr,
            "supplied checker accepted a pinned theorem mutation",
        )

    print("CANDIDATE_CHECKER_SEMANTIC_MUTATION=REJECTED")
    print("INDEPENDENT_CHECKER_SEMANTIC_MUTATION=REJECTED")
    print("CANDIDATE_CHECKER_PINNED_INPUT_MUTATION=REJECTED")


def main() -> None:
    allowed_mutations = {
        "",
        "drop_normalization_chart",
        "drop_pivot",
        "overlap_pivot",
        "drop_atom",
        "overlap_terminal",
        "drop_terminal",
        "unaudit_a0",
        "unaudit_quadratic",
    }
    require(MUTATION in allowed_mutations, f"unknown mutation: {MUTATION}")
    verify_hashes()
    verify_manifest()
    verify_target_normalization()
    routed, empty = verify_pivots()
    atoms, terminals = verify_routes()
    stale_count = verify_candidate_status()
    print(f"FROZEN_PIVOTS={len(PIVOTS)}")
    print(f"POTENTIAL_ROUTED={len(routed)}")
    print(f"FORCED_EMPTY={len(empty)}")
    print(f"ROUTE_ATOMS={atoms}")
    print(f"INTRINSIC_TERMINALS={terminals}")
    print(f"AUDITED_TERMINALS={terminals}")
    print("QUADRATIC_PROVENANCE=STANDALONE_HOSTILE_PASS")
    print(f"STALE_STATUS_MARKERS={stale_count}")
    print("CANDIDATE_STATUS=UNCONDITIONAL")
    print("BRIDGE_Q2_E1_A3_B1_D1_N1_INDEPENDENT_PASS_F4A93C")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--probe-original-checker":
        probe_original_checker()
    elif len(sys.argv) == 1:
        main()
    else:
        fail("usage: verify_bridge_independent.py [--probe-original-checker]")
