#!/usr/bin/env python3
"""Independent exact verifier for the 10-complex construction.

The script reconstructs the mass-action field from the reaction table.  It
then checks the graph, rates, stoichiometric rank, displayed field, curve
identities, rational parametrization, injectivity certificate, ideal
membership, irreducibility of the conic, Jacobian rank, and multivariate gcd.
No floating-point arithmetic is used.
"""

from __future__ import annotations

import csv
from collections import deque
from functools import reduce
from pathlib import Path

import sympy as sp


x, y, z, t = sp.symbols("x y z t")
variables = (x, y, z)
data_directory = Path(__file__).resolve().parent

# Complex i is the exponent vector in row i.  All entries are nonnegative.
complexes = (
    (0, 0, 0),  # 0
    (0, 0, 1),  # 1: Z
    (0, 0, 3),  # 2: 3Z
    (0, 1, 1),  # 3: Y + Z
    (0, 3, 0),  # 4: 3Y
    (1, 0, 1),  # 5: X + Z
    (1, 1, 0),  # 6: X + Y
    (1, 1, 1),  # 7: X + Y + Z
    (2, 1, 0),  # 8: 2X + Y
    (3, 0, 0),  # 9: 3X
)

# Each row is (i, j, rate i->j, rate j->i).
reversible_pairs = (
    (0, 1, 845740, 7732494),
    (0, 4, 702464, 3920),
    (0, 6, 437290, 4380128),
    (1, 7, 1405575, 5600),
    (2, 4, 706384, 900816),
    (2, 7, 1518755, 6873328),
    (2, 9, 3920, 896896),
    (3, 4, 3863552, 3920),
    (5, 9, 3863552, 15680),
    (8, 9, 4346496, 658560),
)


def monomial(exponent):
    return sp.prod(variable**power for variable, power in zip(variables, exponent))


def reconstruct_field():
    field = [sp.Integer(0), sp.Integer(0), sp.Integer(0)]
    for source, target, forward_rate, reverse_rate in reversible_pairs:
        source_complex = complexes[source]
        target_complex = complexes[target]
        net_flux = (
            forward_rate * monomial(source_complex)
            - reverse_rate * monomial(target_complex)
        )
        for coordinate in range(3):
            field[coordinate] += net_flux * (
                target_complex[coordinate] - source_complex[coordinate]
            )
    return tuple(sp.expand(polynomial) for polynomial in field)


field = reconstruct_field()

# Independently displayed coordinate polynomials.
expected_field = (
    -3380608 * x**3
    + 4346496 * x**2 * y
    - 6878928 * x * y * z
    - 4380128 * x * y
    + 7727104 * x * z
    + 1530515 * z**3
    + 1405575 * z
    + 437290,
    658560 * x**3
    - 4346496 * x**2 * y
    - 6878928 * x * y * z
    - 4380128 * x * y
    - 2722048 * y**3
    + 7727104 * y * z
    + 3637907 * z**3
    + 1405575 * z
    + 2544682,
    2706368 * x**3
    + 13746656 * x * y * z
    - 3863552 * x * z
    + 2706368 * y**3
    - 3863552 * y * z
    - 5168422 * z**3
    - 7732494 * z
    + 845740,
)


def verify_network():
    assert len(complexes) == 10
    assert len(set(complexes)) == len(complexes)
    assert all(len(c) == 3 and all(entry >= 0 for entry in c) for c in complexes)

    assert max(sum(c) for c in complexes) == 3

    directed = {}
    adjacency = {index: set() for index in range(len(complexes))}
    undirected_edges = set()
    reaction_differences = []
    for source, target, forward_rate, reverse_rate in reversible_pairs:
        assert 0 <= source < len(complexes) and 0 <= target < len(complexes)
        assert source != target
        assert isinstance(forward_rate, int) and forward_rate > 0
        assert isinstance(reverse_rate, int) and reverse_rate > 0
        assert (source, target) not in directed
        assert (target, source) not in directed
        directed[source, target] = forward_rate
        directed[target, source] = reverse_rate
        edge = tuple(sorted((source, target)))
        assert edge not in undirected_edges
        undirected_edges.add(edge)
        adjacency[source].add(target)
        adjacency[target].add(source)
        reaction_differences.append(
            tuple(complexes[target][i] - complexes[source][i] for i in range(3))
        )

    assert len(directed) == 20
    assert all((target, source) in directed for source, target in directed)

    # The machine-readable directed table must agree exactly with the raw
    # reversible-pair data used to reconstruct the field.
    expected_csv_rows = []
    for source, target, forward_rate, reverse_rate in reversible_pairs:
        expected_csv_rows.extend(
            ((source, target, forward_rate), (target, source, reverse_rate))
        )
    with (data_directory / "network.csv").open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames == ["source_index", "target_index", "rate"]
        actual_csv_rows = [
            (int(row["source_index"]), int(row["target_index"]), int(row["rate"]))
            for row in reader
        ]
    assert actual_csv_rows == expected_csv_rows

    reached = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for neighbor in sorted(adjacency[vertex]):
            if neighbor not in reached:
                reached.add(neighbor)
                queue.append(neighbor)
    assert reached == set(range(len(complexes)))
    assert len(undirected_edges) - len(complexes) + 1 == 1  # one undirected cycle

    difference_matrix = sp.Matrix(reaction_differences)
    stoichiometric_rank = difference_matrix.rank()
    assert stoichiometric_rank == 3
    assert len(complexes) - 1 - stoichiometric_rank == 6
    # A compact rank certificate from 0->1, 0->4, and 0->6.
    rank_witness = sp.Matrix([(0, 0, 1), (0, 3, 0), (1, 1, 0)])
    assert rank_witness.det() == -3


def verify_polynomials_and_curve():
    assert all(sp.expand(got - wanted) == 0 for got, wanted in zip(field, expected_field))
    assert all(polynomial != 0 for polynomial in field)
    assert tuple(polynomial.subs({x: 1, y: 1, z: 1}) for polynomial in field) == (
        807316,
        -2353772,
        -622888,
    )
    supports = sorted(
        set().union(*(set(sp.Poly(polynomial, variables).monoms()) for polynomial in field))
    )
    coefficient_matrix = sp.Matrix(
        [[sp.Poly(polynomial, variables).coeff_monomial(term) for term in supports]
         for polynomial in field]
    )
    assert coefficient_matrix.rank() == 3

    # Prime conic ideal.  L has the sign convention z-x-y+1.
    L = z - x - y + 1
    Q = 7 * x**2 - 2 * x * y - 16 * x + 7 * y**2 - 16 * y + 16

    homogenized_conic_matrix = sp.Matrix(
        ((7, -1, -8), (-1, 7, -8), (-8, -8, 16))
    )
    assert homogenized_conic_matrix.det() == -256

    conic_circle_form = 4 * ((x - y) ** 2 + (z - 1) ** 2) - (z + 1) ** 2
    assert sp.expand(conic_circle_form - Q - L * (3 * x + 3 * y + 3 * z - 13)) == 0

    A = (
        1530515 * x**2
        - 3817898 * x * y
        + 1530515 * x * z
        + 4666074 * x
        + 1530515 * y**2
        + 1530515 * y * z
        - 3061030 * y
        + 1530515 * z**2
        - 1530515 * z
        + 2936090,
        3637907 * x**2
        + 396886 * x * y
        + 3637907 * x * z
        - 7275814 * x
        + 3637907 * y**2
        + 3637907 * y * z
        + 451290 * y
        + 3637907 * z**2
        - 3637907 * z
        + 5043482,
        -98
        * (
            52739 * x**2
            - 34794 * x * y
            + 52739 * x * z
            - 66054 * x
            + 52739 * y**2
            + 52739 * y * z
            - 66054 * y
            + 52739 * z**2
            - 52739 * z
            + 131642
        ),
    )
    B = (
        -264299 * x + 218645 * y - 156175,
        613781 * x + 130837 * y - 156175,
        -98 * (3589 * x + 3589 * y - 8767),
    )
    assert all(
        sp.expand(polynomial - coefficient_L * L - coefficient_Q * Q) == 0
        for polynomial, coefficient_L, coefficient_Q in zip(field, A, B)
    )

    # Irreducibility certificate for Q: exact factorization has one degree-2 factor.
    constant, factors = sp.factor_list(Q, x, y)
    assert constant != 0
    assert factors == [(Q, 1)]
    assert sp.Poly(Q, x, y).total_degree() == 2

    denominator = t**2 - t + 1
    parametrization = (
        (t**2 + 3) / (2 * denominator),
        (3 * t**2 + 1) / (2 * denominator),
        (t**2 + t + 1) / denominator,
    )
    substitution = dict(zip(variables, parametrization))
    assert sp.factor(L.subs(substitution)) == 0
    assert sp.factor(Q.subs(substitution)) == 0
    for polynomial in field:
        numerator, _ = sp.together(polynomial.subs(substitution)).as_numer_denom()
        assert sp.Poly(sp.expand(numerator), t).is_zero

    # Exact positivity and injectivity certificates on -1 < t < 1.
    positive_quadratics = (
        denominator,
        t**2 + 3,
        3 * t**2 + 1,
        t**2 + t + 1,
    )
    for quadratic in positive_quadratics:
        polynomial = sp.Poly(quadratic, t, domain=sp.QQ)
        assert polynomial.degree() == 2
        assert polynomial.LC() > 0
        assert sp.discriminant(polynomial.as_expr(), t) < 0
    assert sp.expand(denominator - ((t - sp.Rational(1, 2)) ** 2 + sp.Rational(3, 4))) == 0
    assert sp.expand(t**2 + t + 1 - ((t + sp.Rational(1, 2)) ** 2 + sp.Rational(3, 4))) == 0
    derivative = sp.factor(sp.diff(parametrization[2], t))
    assert sp.cancel(derivative - 2 * (1 - t**2) / denominator**2) == 0
    assert tuple(value.subs(t, 0) for value in parametrization) == (
        sp.Rational(3, 2),
        sp.Rational(1, 2),
        sp.Integer(1),
    )
    assert tuple(value.subs(t, sp.Rational(1, 2)) for value in parametrization) == (
        sp.Rational(13, 6),
        sp.Rational(7, 6),
        sp.Rational(7, 3),
    )

    primitive = [sp.Poly(polynomial, variables, domain=sp.QQ).primitive()[1] for polynomial in field]
    polynomial_gcd = reduce(sp.gcd, primitive)
    assert polynomial_gcd.total_degree() == 0
    assert all(
        sp.gcd(primitive[i], primitive[j]).total_degree() == 0
        for i in range(3)
        for j in range(i + 1, 3)
    )
    # An independent exact factorization route: every primitive coordinate is irreducible.
    for polynomial in primitive:
        _, factorization = sp.factor_list(polynomial.as_expr(), *variables)
        assert len(factorization) == 1
        assert factorization[0][1] == 1
        assert sp.Poly(factorization[0][0], variables).total_degree() == 3

    equilibrium_point = {x: sp.Rational(3, 2), y: sp.Rational(1, 2), z: 1}
    jacobian = sp.Matrix(field).jacobian(variables).subs(equilibrium_point)
    assert jacobian.rank() == 2


def verify_complete_radical_decomposition():
    """Certify that the full steady ideal is radical and find both components."""

    L = z - x - y + 1
    D = (
        y**2
        - y * z
        - y
        + sp.Rational(7, 16) * z**2
        - sp.Rational(1, 8) * z
        + sp.Rational(7, 16)
    )

    # The reduced lex basis is unique, so the factors below are canonical
    # exact data derived from the raw reaction table rather than copied
    # certificate coefficients.
    steady_basis = sp.groebner(field, x, y, z, order="lex", domain=sp.QQ)
    assert len(steady_basis.polys) == 3
    basis_expressions = tuple(polynomial.as_expr() for polynomial in steady_basis.polys)

    common_conic = sp.gcd(
        sp.Poly(basis_expressions[1], variables, domain=sp.QQ),
        sp.Poly(basis_expressions[2], variables, domain=sp.QQ),
    ).monic()
    assert sp.expand(common_conic.as_expr() - D) == 0

    H = sp.Poly(
        basis_expressions[1], variables, domain=sp.QQ
    ).exquo(common_conic).as_expr()
    R = sp.Poly(
        basis_expressions[2], variables, domain=sp.QQ
    ).exquo(common_conic).as_expr()

    assert sp.degree(basis_expressions[0], x) == 1
    assert sp.expand(sp.Poly(basis_expressions[0], x).LC() - 1) == 0
    assert sp.degree(H, x) == 0 and sp.degree(H, y) == 1
    H_leading_coefficient = sp.Poly(H, y).LC()
    assert H_leading_coefficient.free_symbols == set()
    assert H_leading_coefficient != 0
    assert R.free_symbols <= {z} and sp.degree(R, z) == 15
    _, R_factors = sp.factor_list(R, z)
    assert len(R_factors) == 1
    assert sp.degree(R_factors[0][0], z) == 15 and R_factors[0][1] == 1

    # q=(G0,H,R) has a triangular reduced basis and quotient Q[z]/(R),
    # hence is a degree-15 maximal ideal because R is irreducible.
    isolated_basis = sp.groebner(
        (basis_expressions[0], H, R), x, y, z, order="lex", domain=sp.QQ
    )
    assert len(isolated_basis.polys) == 3
    isolated_expressions = tuple(
        polynomial.as_expr() for polynomial in isolated_basis.polys
    )
    assert isolated_expressions[0].free_symbols <= {x, z}
    assert sp.Poly(isolated_expressions[0], x).degree() == 1
    assert sp.Poly(isolated_expressions[0], x).LC() == 1
    assert isolated_expressions[1].free_symbols <= {y, z}
    assert sp.Poly(isolated_expressions[1], y).degree() == 1
    assert sp.Poly(isolated_expressions[1], y).LC() == 1
    assert isolated_expressions[2].free_symbols <= {z}
    assert sp.degree(isolated_expressions[2], z) == 15
    _, isolated_factors = sp.factor_list(isolated_expressions[2], z)
    assert len(isolated_factors) == 1
    assert sp.degree(isolated_factors[0][0], z) == 15
    assert isolated_factors[0][1] == 1

    # K is contained in q, and D is not in q.  Since q is maximal and D is
    # in the conic prime p=(L,D), this proves p+q=(1).
    assert all(
        sp.expand(isolated_basis.reduce(polynomial)[1]) == 0
        for polynomial in basis_expressions
    )
    assert sp.expand(isolated_basis.reduce(D)[1]) != 0

    # K is already known to lie in p from the displayed A_i L+B_i Q
    # identities, and (L,D)=(L,Q).  The following six exact reductions prove
    # p*q is contained in K.  Comaximality gives p*q=p intersection q, while
    # the preceding containments give the reverse inclusion.  Both p and q
    # are prime, so K is radical.
    Q = 7 * x**2 - 2 * x * y - 16 * x + 7 * y**2 - 16 * y + 16
    assert sp.rem(Q - 16 * D, L, x) == 0
    assert all(
        sp.expand(steady_basis.reduce(conic_generator * isolated_generator)[1])
        == 0
        for conic_generator in (L, D)
        for isolated_generator in isolated_expressions
    )


def main():
    verify_network()
    verify_polynomials_and_curve()
    verify_complete_radical_decomposition()
    print("PASS: all exact construction checks succeeded")
    print("  complexes: 10")
    print("  directed reactions: 20")
    print("  linkage classes: 1 (connected reversible graph)")
    print("  stoichiometric rank: 3")
    print("  deficiency: 6")
    print("  coordinate gcd over Q[x,y,z]: 1")
    print("  steady ideal: radical of dimension 1")
    print("  complex variety: the conic plus 15 reduced isolated points")


if __name__ == "__main__":
    main()
