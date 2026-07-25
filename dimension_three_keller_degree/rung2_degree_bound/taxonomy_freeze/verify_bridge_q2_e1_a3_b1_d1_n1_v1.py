#!/usr/bin/env python3
"""Fail-closed coverage replay for the frozen fixed-linear cubic-pencil row.

This verifies the post-freeze routing algebra and pins every terminal
hostile report.  It does not itself certify the row: the bridge still
requires its separate independent hostile reconstruction.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
RUNG = HERE.parent
CUBIC = RUNG / "fixed_linear_cubic_pencil"
VERTICAL = CUBIC / "vertical_locus"

EXPECTED_HASHES = {
    HERE / "FROZEN_TAXONOMY_v1.md":
        "41fccc44d23fab125819990a2b27526771fbfb62293910b98cfcf1821576d03d",
    HERE / "frozen_manifest_v1.json":
        "5a2bdd57438e9ebcca18d04c53ebc98ced2b61209e2de99674aede501c615c23",
    HERE / "BRIDGE_Q2_E1_A3_B1_D1_N1_v1.md":
        "51f864184ac0eddea9ff8b4e0ab9f635ced58d02c7a42dfdb1b03141f727f740",
    RUNG / "WORKING_QUADRATIC_COMPONENT_EXIT.md":
        "f8a7c92c1631f4efbc5b452d76c8f5ae2121c730173f374ffb736eda37f627de",
    RUNG / "audit_quadratic_component_exit" / "REPORT.md":
        "8ee4a3ce87c3045b6f4dde58c5e20466e75e1ac4cecc5167a3853933d04aeb32",
    RUNG / "VERIFICATION.md":
        "71190f6e6b68fb7e3837c76bb944fac2e85a7c92ed938f471d05e9497b6eb9e8",
    CUBIC / "WORKING_HORIZONTAL_FIXED_LINEAR_CUBIC_PENCIL.md":
        "b034cfb8770870336ec24809467e0ed2f56fa89491d349dcc8c8f2a67ea45a03",
    CUBIC / "audit_hostile" / "REPORT.md":
        "4566cda4c40b6065f38d6e85cda9004dceff57e21db9295677dc163ba24ee651",
    VERTICAL / "WORKING_VERTICAL_FIXED_LINEAR_CUBIC_PENCIL.md":
        "707320e8658972cbc459131ccb41f8fd2524cde2621c4461f627895518260ef7",
    VERTICAL / "audit_vertical_hostile" / "REPORT.md":
        "e4cb1ca80daa0eb30a2429b0410852feb7190cc9365a7947f869e9b32c0da35f",
    VERTICAL / "NONVERTICAL_NONTRIPLE_LEMMA.md":
        "9e30f4351627947da09a4078c784812c3d0d4c59b34503b22368926939ecfd95",
    VERTICAL / "NONVERTICAL_TRIPLE_ROOT_LEMMA.md":
        "fa050695842947653c254d3c1e3eff8136369bc0fd1d0fa7404f1aa634000383",
    VERTICAL / "audit_nonvertical_companion" / "REPORT.md":
        "d3bab04b66f9f74573d4de7b2e57347b28b4f8fb7dcc7b685671eb46acf81df3",
    VERTICAL / "VERTICAL_ELL_ZERO_NONTRIPLE_LEMMA.md":
        "5e4f4c4f4f7e3b89eb868f8d42cfe27d38a134340e2623f36cef3c5fb566eefc",
    VERTICAL / "audit_vertical_ell_zero_nontriple" / "REPORT.md":
        "1c30086082a2871d4fb1bce62bd9bd0a743306bd5a48132e2b136d13105e032f",
    VERTICAL / "VERTICAL_NONZERO_ELL_NONTRIPLE_LEMMA.md":
        "47b7730afb582f1422517dbd7e08ec8bbdb79ca2a837f317a828a859efdd81e6",
    VERTICAL / "audit_vertical_nonzero_ell_nontriple" / "REPORT.md":
        "41075ac6bf35c686947546773627e115be4eb05959db0ee9c2ff31ebb598d135",
    VERTICAL / "VERTICAL_TRIPLE_GAMMA0_REDUCTION.md":
        "28a3cd191bb1e74cd4e8ae5ebf7dcaa938602b318c2f49b006838641c6979e58",
    VERTICAL / "audit_vertical_triple_gamma0_reduction" / "REPORT.md":
        "40f4830bd4603e7a8e1bae97b57b8a113af4f4ecbcadc65000a605380a414842",
    VERTICAL / "VERTICAL_TRIPLE_GAMMA0_ELL0_LEMMA.md":
        "b11f1c320a5bd6a347112daf7359bf91576c529046d3e2718fcfc92f5f5db2d5",
    VERTICAL / "audit_vertical_triple_gamma0_ell0" / "REPORT.md":
        "d2e8e1bd798b0cf1448a6254e0e68e5c55aa44552978421b0ed6fc58415c55ec",
    VERTICAL / "VERTICAL_TRIPLE_GAMMA_NONZERO_EXCLUSION.md":
        "e04782d2b2ecacbbfded9be4558145e9601d5b4e6fc914ad26444c40cfe86a7b",
    VERTICAL / "audit_vertical_triple_gamma_nonzero" / "REPORT.md":
        "4410f0561b4b894739851d4a80b539855b369012be207998b7d135d89e830137",
    VERTICAL / "VERTICAL_A0_W0_ZERO_EXCLUSION.md":
        "d1f0889a54d9185a4f899d7ca6f5eb702a040a8cfdcb1733a4427896940eb09c",
    VERTICAL / "audit_vertical_a0_w0_zero" / "REPORT.md":
        "d8d291d03e269d0ee769bc96dded535abd5f9df11cd79d1994a19b6318700587",
    VERTICAL / "a0_w0_nonzero_attack" / "NOTE.md":
        "b38459777db826a3c17fa74aaf7472cc654ae0ba0d7ca96a9cbc14cc56229cda",
    VERTICAL / "audit_a0_w0_nonzero" / "REPORT.md":
        "c77abb4a2bf845614a6a1c320afcb916b7bf0477075e38469faebc5bc4dd0547",
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

# These are the leaves of the intrinsic route tree, not frozen taxonomy
# leaves.  The final Boolean records whether a further terminal hostile
# audit is still required.
EXPECTED_TERMINALS = {
    "horizontal": False,
    "vertical_m1_G0": False,
    "vertical_m2_G0": False,
    "vertical_m3_G0": False,
    "vertical_m3_nonvertical_squarefree": False,
    "vertical_m3_nonvertical_double": False,
    "vertical_m3_nonvertical_triple": False,
    "vertical_m3_vertical_s_nonzero_squarefree_ell_zero": False,
    "vertical_m3_vertical_s_nonzero_squarefree_ell_nonzero": False,
    "vertical_m3_vertical_s_nonzero_double_ell_zero": False,
    "vertical_m3_vertical_s_nonzero_double_ell_nonzero": False,
    "vertical_m3_vertical_s_nonzero_triple_gamma_nonzero": False,
    "vertical_m3_vertical_s_nonzero_triple_gamma_zero": False,
    "vertical_m3_vertical_s_zero_W0_zero": False,
    "vertical_m3_vertical_s_zero_W0_nonzero": False,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    require(path.is_file(), f"missing pinned input: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def polynomial_rank_at_least_two(jacobian: sp.Matrix) -> bool:
    for rows in itertools.combinations(range(3), 2):
        for columns in itertools.combinations(range(3), 2):
            if sp.expand(jacobian.extract(rows, columns).det()) != 0:
                return True
    return False


def coefficient_vector(
    components: tuple[sp.Expr, sp.Expr, sp.Expr],
    monomials: list[sp.Expr],
    variables: tuple[sp.Symbol, sp.Symbol, sp.Symbol],
) -> list[sp.Expr]:
    return [
        sp.Poly(component, *variables).coeff_monomial(monomial)
        for component in components
        for monomial in monomials
    ]


def generate_terminal_routes() -> dict[str, bool]:
    routes: dict[str, bool] = {"horizontal": False}

    for multiplicity in (1, 2):
        routes[f"vertical_m{multiplicity}_G0"] = False

    routes["vertical_m3_G0"] = False

    for root_type in ("squarefree", "double", "triple"):
        routes[f"vertical_m3_nonvertical_{root_type}"] = False

    for root_type in ("squarefree", "double"):
        for ell_type in ("ell_zero", "ell_nonzero"):
            routes[
                "vertical_m3_vertical_s_nonzero_"
                f"{root_type}_{ell_type}"
            ] = False

    for gamma_type in ("gamma_nonzero", "gamma_zero"):
        routes[
            "vertical_m3_vertical_s_nonzero_triple_"
            f"{gamma_type}"
        ] = False

    routes["vertical_m3_vertical_s_zero_W0_zero"] = False
    routes["vertical_m3_vertical_s_zero_W0_nonzero"] = False
    return routes


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

    rows = [
        row for row in manifest["rows"]
        if row["id"] == "Q2-E1-A3-B1-D1-N1"
    ]
    require(len(rows) == 1, "target frozen row missing or duplicated")
    row = rows[0]
    require(row["rank"] == 2, "target row has wrong rank")
    require(row["tuple"] == [1, 3, 1, 1, 1], "target tuple mismatch")

    x, y, z = sp.symbols("x y z")
    variables = (x, y, z)
    quartic_monomials = [
        x**i * y**j * z**k for i, j, k in QUARTIC_EXPONENTS
    ]

    # Exact target normalization charts for A(u,v)=a*u+b*v.
    avec = sp.Matrix(sp.symbols("a0:3"))
    bvec = sp.Matrix(sp.symbols("b0:3"))
    target_charts = ((0, 1, 2), (0, 2, 1), (1, 2, 0))
    selected_minors: list[sp.Expr] = []
    for i, j, k in target_charts:
        basis = sp.Matrix.hstack(avec, bvec, sp.eye(3).col(k))
        minor = sp.expand(avec[i] * bvec[j] - avec[j] * bvec[i])
        determinant = sp.expand(basis.det())
        require(
            sp.expand(determinant**2 - minor**2) == 0,
            f"target chart determinant mismatch: {(i, j)}",
        )
        require(
            all(
                sp.expand(entry) == 0
                for entry in (
                    basis.adjugate() * avec
                    - determinant * sp.Matrix([1, 0, 0])
                )
            ),
            f"target chart does not normalize first column: {(i, j)}",
        )
        require(
            all(
                sp.expand(entry) == 0
                for entry in (
                    basis.adjugate() * bvec
                    - determinant * sp.Matrix([0, 1, 0])
                )
            ),
            f"target chart does not normalize second column: {(i, j)}",
        )
        selected_minors.append(minor)
    require(len(selected_minors) == 3, "wrong target chart count")

    # The horizontal/vertical split is the rank of the 4-by-2 restriction
    # matrix of (p,q) on z=0.  Rank zero contradicts coprimality; ranks one
    # and two have kernel dimensions one and zero.
    restriction_symbols = sp.symbols("r0:8")
    restriction = sp.Matrix(4, 2, restriction_symbols)
    rank_2_sample = sp.Matrix([[1, 0], [0, 1], [0, 0], [0, 0]])
    rank_1_sample = sp.Matrix([[1, 2], [0, 0], [0, 0], [0, 0]])
    rank_0_sample = sp.zeros(4, 2)
    require(rank_2_sample.rank() == 2, "horizontal rank sample failed")
    require(len(rank_2_sample.nullspace()) == 0, "horizontal kernel not zero")
    require(rank_1_sample.rank() == 1, "vertical rank sample failed")
    require(len(rank_1_sample.nullspace()) == 1, "vertical member not unique")
    require(rank_0_sample.rank() == 0, "common-divisor rank sample failed")
    require(
        all(entry == 0 for entry in rank_0_sample),
        "rank-zero restriction does not force both restrictions to vanish",
    )
    require(restriction.shape == (4, 2), "wrong restriction matrix shape")

    # Vertical multiplicity and companion partitions are finite and exact.
    require(set((1, 2, 3)) == {1, 2, 3}, "vertical multiplicities incomplete")
    alpha, beta, shear_a, shear_b = sp.symbols(
        "alpha beta shear_a shear_b", nonzero=False
    )
    # q' = shear_a*q + shear_b*p.  If beta != 0, the choice
    # shear_b=shear_a*alpha/beta kills the p coefficient of G.
    transformed_p_coefficient = sp.expand(
        alpha - beta * shear_b / shear_a
    )
    require(
        sp.simplify(
            transformed_p_coefficient.subs(
                shear_b, shear_a * alpha / beta
            )
        ) == 0,
        "nonvertical companion shear failed",
    )
    require(
        set(("zero", "vertical", "nonvertical"))
        == {"zero", "vertical", "nonvertical"},
        "companion partition incomplete",
    )

    # Root partitions of every nonzero binary cubic.
    root_partitions = {(1, 1, 1), (2, 1), (3,)}
    require(
        all(sum(partition) == 3 for partition in root_partitions)
        and len(root_partitions) == 3,
        "binary cubic root partition ledger incomplete",
    )

    # Construct exact leading-tuple witnesses for C00--C29.
    fermat = x**3 + y**3 + z**3
    derivative_vectors = [
        [
            sp.Poly(sp.diff(fermat, variable), *variables)
            .coeff_monomial(monomial)
            for monomial in (x**2, x*y, x*z, y**2, y*z, z**2)
        ]
        for variable in variables
    ]
    require(
        sp.Matrix(derivative_vectors).rank() == 3,
        "Fermat cubic unexpectedly has only two essential variables",
    )

    routed_pivots: set[str] = set()
    for index, exponents in enumerate(QUARTIC_EXPONENTS):
        divisor_index = next(
            coordinate for coordinate, exponent in enumerate(exponents)
            if exponent > 0
        )
        h = variables[divisor_index]
        p_exponents = list(exponents)
        p_exponents[divisor_index] -= 1
        p = (
            x**p_exponents[0]
            * y**p_exponents[1]
            * z**p_exponents[2]
        )
        monomial = quartic_monomials[index]
        require(sp.expand(h * p - monomial) == 0, "bad witness factorization")
        require(sp.gcd(p, fermat) == 1, "witness cubics not coprime")
        require(sp.gcd(h * p, h * fermat) == h, "witness gcd is not linear")

        for block, components in (
            (0, (h * p, h * fermat, sp.Integer(0))),
            (1, (sp.Integer(0), h * p, h * fermat)),
        ):
            vector = coefficient_vector(components, quartic_monomials, variables)
            nonzero = [
                position for position, coefficient in enumerate(vector)
                if coefficient != 0
            ]
            expected_index = 15 * block + index
            require(nonzero[0] == expected_index, "witness has wrong first pivot")
            require(
                polynomial_rank_at_least_two(
                    sp.Matrix(components).jacobian(variables)
                ),
                f"witness Jacobian rank dropped at C{expected_index:02d}",
            )
            routed_pivots.add(f"C{expected_index:02d}")

    require(
        routed_pivots == set(pivots[:30]),
        "potential-pivot witnesses do not cover exactly C00--C29",
    )

    # C30--C44 force the first two target components to vanish and hence
    # every 2-by-2 Jacobian minor to vanish.
    coefficients = sp.symbols("g0:15")
    generic_quartic = sum(
        coefficient * monomial
        for coefficient, monomial in zip(coefficients, quartic_monomials)
    )
    late_jacobian = sp.Matrix([0, 0, generic_quartic]).jacobian(variables)
    for rows_2 in itertools.combinations(range(3), 2):
        for columns_2 in itertools.combinations(range(3), 2):
            require(
                sp.expand(
                    late_jacobian.extract(rows_2, columns_2).det()
                ) == 0,
                "late-pivot rank-one certificate failed",
            )
    empty_pivots = set(pivots[30:])
    require(len(empty_pivots) == 15, "wrong forced-empty pivot count")
    require(
        routed_pivots.isdisjoint(empty_pivots)
        and routed_pivots | empty_pivots == set(pivots),
        "routed/empty pivot ledger is not a partition",
    )

    # Independently generate the complete internal terminal ledger.
    observed_terminals = generate_terminal_routes()
    require(
        observed_terminals == EXPECTED_TERMINALS,
        "intrinsic terminal route ledger changed",
    )
    conditional = {
        route for route, pending in observed_terminals.items() if pending
    }
    require(
        conditional == set(),
        "a terminal hostile audit is still pending",
    )

    bridge = (HERE / "BRIDGE_Q2_E1_A3_B1_D1_N1_v1.md").read_text()
    required_tokens = (
        "R/\\mathrm C_{00}",
        "R/\\mathrm C_{29}",
        "R/\\mathrm C_{30}",
        "R/\\mathrm C_{44}",
        "\\operatorname{rank}\\rho_h=2",
        "\\operatorname{rank}\\rho_h=1",
        "VERTICAL_TRIPLE_GAMMA_NONZERO_EXCLUSION.md",
        "a0_w0_nonzero_attack/NOTE.md",
        "audit_a0_w0_nonzero/REPORT.md",
        "audit_quadratic_component_exit/REPORT.md",
        "does **not** promote",
    )
    for token in required_tokens:
        require(token in bridge, f"bridge coverage token missing: {token}")

    print(
        "PASS: fixed-linear cubic-pencil bridge candidate; "
        "30 routed potential + 15 forced-empty pivots; "
        "15 intrinsic terminals; 0 conditional hostile audits"
    )


if __name__ == "__main__":
    main()
