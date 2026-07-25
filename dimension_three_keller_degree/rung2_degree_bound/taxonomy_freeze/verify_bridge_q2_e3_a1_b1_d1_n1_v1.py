#!/usr/bin/env python3
"""Fail-closed exact replay for the frozen fixed-cubic-line bridge.

This verifier checks the post-freeze coverage algebra. It does not certify
the row by itself and does not replace the independent hostile audit still
required by BRIDGE_Q2_E3_A1_B1_D1_N1_v1.md.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
RUNG = HERE.parent

EXPECTED_HASHES = {
    HERE / "FROZEN_TAXONOMY_v1.md":
        "41fccc44d23fab125819990a2b27526771fbfb62293910b98cfcf1821576d03d",
    HERE / "frozen_manifest_v1.json":
        "5a2bdd57438e9ebcca18d04c53ebc98ced2b61209e2de99674aede501c615c23",
    RUNG / "WORKING_FIXED_CUBIC_LINE_ROW.md":
        "9a10c1c103b60eb21405518074086168330a435bb5aa1770d51463a881a926ca",
    RUNG / "WORKING_BINARY_FIXED_CUBIC_LINE_ROW.md":
        "51818647fa7f57942761ca31ed80dc9dde4363ebe83166d87fc80f07861a9607",
    RUNG / "verify_fixed_cubic_line_sympy.py":
        "fdcf31dc44bda116c0e81da6a9d96abf0b92798eb8d56ec25d6c124b31d4b8b8",
    RUNG / "verify_fixed_cubic_line_pari.gp":
        "aeded24439435f5db31d2e702fe357ec0799b62a326761e514727ff77dcc61e1",
    RUNG / "verify_fixed_cubic_line_pari_strict.sh":
        "0d2003acef22b541161230fe1d3ed21399897ee443a6df9b6fc278be99dba464",
    RUNG / "verify_binary_fixed_cubic_complete.py":
        "5c570a002f93c5583618baf615419419e4ee55b2ab3f961cde9bca6f6cc56340",
    RUNG / "verify_binary_fixed_cubic_complete_pari.gp":
        "5568acae07db33984d11e4bb5fa824339faade90828a1f642f33486fa425da1b",
    RUNG / "audit_binary_fixed_cubic_hostile" / "REPORT.md":
        "4cea6002ca7639cf8e04aea80b86daa76655c7359e041e2e7707e50418fa7fc4",
    RUNG / "audit_binary_fixed_cubic_hostile" /
    "audit_orbits_lower_exact.py":
        "45195a94af63ad4d268d951a84a769965ef0821fb90e024f22bf4739620ed334",
    RUNG / "audit_binary_fixed_cubic_hostile" /
    "audit_exceptional_branches_exact.py":
        "4040c2999d790edb96ee20492bc7afbc9c7b98fb11b297ca07c96e5329f0eb58",
    RUNG / "audit_binary_fixed_cubic_hostile" / "test_fail_closed.sh":
        "474d073c3ef62afa34546e3292ada02c5267e19575be5917b6db9f02c6c0a803",
    RUNG / "VERIFICATION.md":
        "71190f6e6b68fb7e3837c76bb944fac2e85a7c92ed938f471d05e9497b6eb9e8",
}

EXPECTED_MONOMIALS = [
    "x^4", "x^3*y", "x^3*z", "x^2*y^2", "x^2*y*z",
    "x^2*z^2", "x*y^3", "x*y^2*z", "x*y*z^2", "x*z^3",
    "y^4", "y^3*z", "y^2*z^2", "y*z^3", "z^4",
]

QUARTIC_EXPONENTS = [
    (4, 0, 0), (3, 1, 0), (3, 0, 1), (2, 2, 0), (2, 1, 1),
    (2, 0, 2), (1, 3, 0), (1, 2, 1), (1, 1, 2), (1, 0, 3),
    (0, 4, 0), (0, 3, 1), (0, 2, 2), (0, 1, 3), (0, 0, 4),
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    require(path.is_file(), f"missing pinned input: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matrix_is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.expand(entry) == 0 for entry in matrix)


def polynomial_rank_at_least_two(jacobian: sp.Matrix) -> bool:
    for rows in itertools.combinations(range(3), 2):
        for columns in itertools.combinations(range(3), 2):
            if sp.expand(jacobian.extract(rows, columns).det()) != 0:
                return True
    return False


def main() -> None:
    require(__debug__, "refusing optimized Python: fail-closed checks required")

    for path, expected in EXPECTED_HASHES.items():
        require(digest(path) == expected, f"pinned-input hash mismatch: {path}")

    manifest = json.loads((HERE / "frozen_manifest_v1.json").read_text())
    require(manifest["version"] == 1, "wrong freeze version")
    require(manifest["frozen_row_count"] == 14, "wrong frozen denominator")
    require(
        manifest["coefficient_order"]["degree_four_monomials"]
        == EXPECTED_MONOMIALS,
        "wrong frozen monomial order",
    )
    pivots = [f"C{i:02d}" for i in range(45)]
    require(manifest["pivot_ids"] == pivots, "wrong frozen pivot IDs")

    matches = [
        row for row in manifest["rows"]
        if row["id"] == "Q2-E3-A1-B1-D1-N1"
    ]
    require(len(matches) == 1, "target frozen row missing or duplicated")
    row = matches[0]
    require(row["rank"] == 2, "target row has wrong rank")
    require(row["tuple"] == [3, 1, 1, 1, 1], "target tuple mismatch")

    x, y, z = sp.symbols("x y z")
    variables = (x, y, z)
    quartic_monomials = [
        x**exponents[0] * y**exponents[1] * z**exponents[2]
        for exponents in QUARTIC_EXPONENTS
    ]

    # The exact target normalization is covered by the three nonzero
    # 2-by-2 minors of the 3-by-2 coefficient matrix of A.
    target_symbols = sp.symbols("a0:3") + sp.symbols("b0:3")
    avec = sp.Matrix(target_symbols[:3])
    bvec = sp.Matrix(target_symbols[3:])
    target_charts = ((0, 1, 2), (0, 2, 1), (1, 2, 0))
    for i, j, k in target_charts:
        complement = sp.eye(3).col(k)
        basis = sp.Matrix.hstack(avec, bvec, complement)
        minor = avec[i] * bvec[j] - avec[j] * bvec[i]
        determinant = sp.expand(basis.det())
        require(
            sp.expand(determinant**2 - minor**2) == 0,
            f"target chart determinant is not the selected minor: {(i, j)}",
        )
        require(
            matrix_is_zero(
                basis.adjugate() * avec
                - determinant * sp.Matrix([1, 0, 0])
            ),
            f"target chart does not send the first column to e1: {(i, j)}",
        )
        require(
            matrix_is_zero(
                basis.adjugate() * bvec
                - determinant * sp.Matrix([0, 1, 0])
            ),
            f"target chart does not send the second column to e2: {(i, j)}",
        )

    # The source normalization has the same three-minor cover for the
    # coefficient rows of p and q.
    source_symbols = sp.symbols("p0:3") + sp.symbols("q0:3")
    prow = sp.Matrix(1, 3, source_symbols[:3])
    qrow = sp.Matrix(1, 3, source_symbols[3:])
    for i, j, k in target_charts:
        complement = sp.eye(3).row(k)
        basis = sp.Matrix.vstack(prow, qrow, complement)
        minor = prow[i] * qrow[j] - prow[j] * qrow[i]
        determinant = sp.expand(basis.det())
        require(
            sp.expand(determinant**2 - minor**2) == 0,
            f"source chart determinant is not the selected minor: {(i, j)}",
        )
        require(
            matrix_is_zero(
                basis * basis.adjugate() - determinant * sp.eye(3)
            ),
            f"source chart adjugate identity failed: {(i, j)}",
        )

    # Reconstruct the rank-two minor for h(x,y,z)*(x,y,0). Euler's identity
    # gives h*(4h-z*h_z), and the second factor cannot vanish for a nonzero
    # cubic because its z-degree eigenvalues are 4,3,2,1.
    cubic_exponents = [
        (3, 0, 0), (2, 1, 0), (1, 2, 0), (0, 3, 0), (2, 0, 1),
        (1, 1, 1), (0, 2, 1), (1, 0, 2), (0, 1, 2), (0, 0, 3),
    ]
    cubic_monomials = [
        x**exponents[0] * y**exponents[1] * z**exponents[2]
        for exponents in cubic_exponents
    ]
    h_coefficients = sp.symbols("h0:10")
    h = sum(
        coefficient * monomial
        for coefficient, monomial in zip(h_coefficients, cubic_monomials)
    )
    first = x * h
    second = y * h
    leading_minor = sp.expand(
        sp.diff(first, x) * sp.diff(second, y)
        - sp.diff(first, y) * sp.diff(second, x)
    )
    euler_factor = sp.expand(h * (4 * h - z * sp.diff(h, z)))
    require(
        sp.expand(leading_minor - euler_factor) == 0,
        "fixed-cubic-line rank-two identity failed",
    )
    transformed_h = sp.Poly(4 * h - z * sp.diff(h, z), *variables)
    for coefficient, monomial, exponents in zip(
        h_coefficients, cubic_monomials, cubic_exponents
    ):
        require(
            transformed_h.coeff_monomial(monomial)
            == (4 - exponents[2]) * coefficient,
            "rank-two Euler operator has the wrong eigenvalue",
        )
        require(4 - exponents[2] != 0, "rank-two Euler operator lost a cubic")

    # Membership in the binary cubic subspace is invariant under GL2. The
    # exact determinant of Sym^3 is (det M)^6.
    u, v = sp.symbols("u v")
    a, b, c, d = sp.symbols("a b c d")
    binary_basis = (u**3, u**2 * v, u * v**2, v**3)
    transformed_basis = (
        (a * u + b * v) ** 3,
        (a * u + b * v) ** 2 * (c * u + d * v),
        (a * u + b * v) * (c * u + d * v) ** 2,
        (c * u + d * v) ** 3,
    )
    sym3 = sp.Matrix([
        [
            sp.Poly(image, u, v).coeff_monomial(monomial)
            for image in transformed_basis
        ]
        for monomial in binary_basis
    ])
    require(
        sp.expand(sym3.det() - (a * d - b * c) ** 6) == 0,
        "symmetric-cube determinant identity failed",
    )
    binary_indices = tuple(range(4))
    nonbinary_indices = tuple(range(4, 10))
    require(
        set(binary_indices).isdisjoint(nonbinary_indices)
        and set(binary_indices + nonbinary_indices) == set(range(10)),
        "binary/nonbinary coefficient split is not exhaustive",
    )

    # Construct a leading-tuple witness for every potential pivot C00--C29.
    # These are not asserted to admit lower terms satisfying all Keller
    # equations; their role is to show that the frozen leading invariants
    # alone do not force any additional pivot to be empty.
    leading_witness_pivots: set[str] = set()
    for index, exponents in enumerate(QUARTIC_EXPONENTS):
        if index <= 9:
            ell_index, transverse_index = 0, 1
        elif index <= 13:
            ell_index, transverse_index = 1, 0
        else:
            ell_index, transverse_index = 2, 0

        h_exponents = list(exponents)
        require(
            h_exponents[ell_index] > 0,
            f"selected linear form does not divide monomial {index}",
        )
        h_exponents[ell_index] -= 1
        h_witness = (
            x**h_exponents[0] * y**h_exponents[1] * z**h_exponents[2]
        )
        ell = variables[ell_index]
        transverse = variables[transverse_index]
        monomial = quartic_monomials[index]
        require(sp.expand(h_witness * ell - monomial) == 0, "bad witness factor")

        for block, components in (
            (0, (monomial, h_witness * transverse, sp.Integer(0))),
            (1, (sp.Integer(0), monomial, h_witness * transverse)),
        ):
            coefficient_vector = [
                sp.Poly(component, *variables).coeff_monomial(term)
                for component in components
                for term in quartic_monomials
            ]
            nonzero_positions = [
                position
                for position, coefficient in enumerate(coefficient_vector)
                if coefficient != 0
            ]
            require(nonzero_positions, "witness leading triple vanished")
            expected_pivot = 15 * block + index
            require(
                nonzero_positions[0] == expected_pivot,
                f"witness has wrong pivot: expected C{expected_pivot:02d}",
            )

            nonzero_components = [entry for entry in components if entry != 0]
            component_gcd = nonzero_components[0]
            for entry in nonzero_components[1:]:
                component_gcd = sp.gcd(component_gcd, entry)
            require(
                sp.Poly(component_gcd, *variables).total_degree() == 3,
                f"witness component gcd does not have degree three: {index}",
            )

            coefficient_matrix = sp.Matrix([
                [
                    sp.Poly(component, *variables).coeff_monomial(term)
                    for term in quartic_monomials
                ]
                for component in components
            ])
            require(
                coefficient_matrix.rank() == 2,
                f"witness component span does not have rank two: {index}",
            )
            jacobian = sp.Matrix(components).jacobian(variables)
            require(
                polynomial_rank_at_least_two(jacobian),
                f"witness Jacobian does not have rank two: {index}",
            )
            leading_witness_pivots.add(f"C{expected_pivot:02d}")

    require(
        leading_witness_pivots == set(pivots[:30]),
        "leading-tuple witnesses do not cover exactly C00--C29",
    )

    # If both first component blocks vanish, the Jacobian has at most one
    # nonzero row. This exact generic calculation is the division-free
    # emptiness certificate for C30--C44.
    quartic_coefficients = sp.symbols("g0:15")
    generic_quartic = sum(
        coefficient * monomial
        for coefficient, monomial in zip(quartic_coefficients, quartic_monomials)
    )
    late_pivot_triple = sp.Matrix([0, 0, generic_quartic])
    late_jacobian = late_pivot_triple.jacobian(variables)
    for rows in itertools.combinations(range(3), 2):
        for columns in itertools.combinations(range(3), 2):
            require(
                sp.expand(late_jacobian.extract(rows, columns).det()) == 0,
                "late-pivot rank-one certificate failed",
            )
    forced_empty = set(pivots[30:])
    require(len(forced_empty) == 15, "wrong number of forced-empty pivots")
    require(
        leading_witness_pivots.isdisjoint(forced_empty)
        and leading_witness_pivots | forced_empty == set(pivots),
        "nonempty/empty pivot ledger is not a partition",
    )

    # Exact determinant transfer under independent GL3 source and target
    # transformations.
    transfer_symbols = sp.symbols("m0:27")
    target = sp.Matrix(3, 3, transfer_symbols[:9])
    formal_jacobian = sp.Matrix(3, 3, transfer_symbols[9:18])
    source = sp.Matrix(3, 3, transfer_symbols[18:])
    require(
        sp.expand(
            (target * formal_jacobian * source).det()
            - target.det() * formal_jacobian.det() * source.det()
        ) == 0,
        "GL3 Keller determinant transfer failed",
    )

    bridge = (HERE / "BRIDGE_Q2_E3_A1_B1_D1_N1_v1.md").read_text()
    for token in (
        "R/\\mathrm C_{00}",
        "R/\\mathrm C_{29}",
        "R/\\mathrm C_{30}",
        "R/\\mathrm C_{44}",
        "\\det(\\operatorname{Sym}^3 M)=(\\det M)^6",
        "does not promote the row",
        "hostile reconstruction",
    ):
        require(token in bridge, f"bridge coverage token missing: {token}")

    print(
        "PASS: frozen fixed-cubic-line bridge candidate; "
        "30 covered potential + 15 forced-empty pivots"
    )


if __name__ == "__main__":
    main()
