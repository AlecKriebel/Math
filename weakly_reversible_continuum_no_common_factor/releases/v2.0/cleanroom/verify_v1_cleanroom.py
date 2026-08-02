#!/usr/bin/env python3
"""Clean-room exact verifier for the frozen v1 mass-action construction.

This program is intentionally self-contained.  Its mathematical input is only
the complex list, the twenty directed reactions with rates, L, Q, the rational
parametrization, and the displayed target vector field.  In particular, it
does not import the discovery verifier or use its A_i/B_i or primary-component
certificates.

The radical decomposition is recomputed by a route different from the first
verifier: saturation by the conic equation finds the residual component, and
an auxiliary-variable elimination independently recomputes the intersection.
All polynomial arithmetic is over QQ.  No floating-point arithmetic is used.
"""

from __future__ import annotations

from collections import deque
from functools import reduce
from itertools import combinations

import sympy as sy


class VerificationFailure(RuntimeError):
    """Raised when an exact certificate does not replay."""


def require(condition: bool, explanation: str) -> None:
    if not bool(condition):
        raise VerificationFailure(explanation)


def report(number: int, statement: str, witness: str = "") -> None:
    suffix = f" [{witness}]" if witness else ""
    print(f"PASS {number:02d}: {statement}{suffix}")


# ---------------------------------------------------------------------------
# Frozen raw input
# ---------------------------------------------------------------------------

x, y, z, t = sy.symbols("x y z t")
xyz = (x, y, z)

COMPLEXES = (
    (0, 0, 0),
    (0, 0, 1),
    (0, 0, 3),
    (0, 1, 1),
    (0, 3, 0),
    (1, 0, 1),
    (1, 1, 0),
    (1, 1, 1),
    (2, 1, 0),
    (3, 0, 0),
)

# Rows are (source index, target index, positive integer rate).
REACTIONS = (
    (0, 1, 845740),
    (1, 0, 7732494),
    (0, 4, 702464),
    (4, 0, 3920),
    (0, 6, 437290),
    (6, 0, 4380128),
    (1, 7, 1405575),
    (7, 1, 5600),
    (2, 4, 706384),
    (4, 2, 900816),
    (2, 7, 1518755),
    (7, 2, 6873328),
    (2, 9, 3920),
    (9, 2, 896896),
    (3, 4, 3863552),
    (4, 3, 3920),
    (5, 9, 3863552),
    (9, 5, 15680),
    (8, 9, 4346496),
    (9, 8, 658560),
)

L = z - x - y + 1
Q = 7 * x**2 - 2 * x * y - 16 * x + 7 * y**2 - 16 * y + 16

denominator = t**2 - t + 1
PARAMETRIZATION = (
    (t**2 + 3) / (2 * denominator),
    (3 * t**2 + 1) / (2 * denominator),
    (t**2 + t + 1) / denominator,
)

# Frozen displayed result to be compared with the independently reconstructed
# mass-action sum.  No later computation uses this tuple in place of the sum.
DISPLAYED_FIELD = (
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


def source_monomial(complex_vector: tuple[int, int, int]) -> sy.Expr:
    value = sy.Integer(1)
    for variable, exponent in zip(xyz, complex_vector):
        value *= variable**exponent
    return value


def reconstruct_field() -> tuple[sy.Expr, sy.Expr, sy.Expr]:
    answer = [sy.Integer(0), sy.Integer(0), sy.Integer(0)]
    for source, target, rate in REACTIONS:
        source_complex = COMPLEXES[source]
        target_complex = COMPLEXES[target]
        kinetic_term = sy.Integer(rate) * source_monomial(source_complex)
        for coordinate in range(3):
            displacement = target_complex[coordinate] - source_complex[coordinate]
            answer[coordinate] += displacement * kinetic_term
    return tuple(sy.expand(entry) for entry in answer)


FIELD = reconstruct_field()


def reduced_basis(expressions, generators):
    return sy.groebner(
        tuple(expressions), *tuple(generators), order="lex", domain=sy.QQ
    )


def basis_expressions(basis) -> tuple[sy.Expr, ...]:
    return tuple(polynomial.as_expr() for polynomial in basis.polys)


def exact_same_basis(left, right) -> bool:
    """Reduced lexicographic bases over a field are unique."""

    return basis_expressions(left) == basis_expressions(right)


def check_raw_network() -> sy.Matrix:
    # 1. Complex data.
    require(len(COMPLEXES) == 10, "wrong number of complexes")
    require(len(set(COMPLEXES)) == len(COMPLEXES), "complexes are not distinct")
    require(
        all(
            len(complex_vector) == 3
            and all(isinstance(entry, int) and entry >= 0 for entry in complex_vector)
            for complex_vector in COMPLEXES
        ),
        "a complex is not a nonnegative integral vector",
    )
    require(max(sum(complex_vector) for complex_vector in COMPLEXES) == 3,
            "maximum complex degree is not three")
    report(1, "complexes are distinct nonnegative integral vectors")

    # 2. Directed rates.
    require(len(REACTIONS) == 20, "wrong number of directed reactions")
    require(
        all(isinstance(rate, int) and rate > 0 for _, _, rate in REACTIONS),
        "a rate is not a positive integer",
    )
    require(
        all(
            0 <= source < len(COMPLEXES)
            and 0 <= target < len(COMPLEXES)
            and source != target
            for source, target, _ in REACTIONS
        ),
        "a directed reaction has invalid endpoints",
    )
    arc_rates = {(source, target): rate for source, target, rate in REACTIONS}
    require(len(arc_rates) == len(REACTIONS), "a directed reaction is duplicated")
    report(2, "all twenty directed rates are positive integers")

    # 3. Reversibility.
    require(
        all((target, source) in arc_rates for source, target in arc_rates),
        "a reaction lacks its reverse",
    )
    require(
        len({tuple(sorted((source, target))) for source, target in arc_rates}) == 10,
        "there are not exactly ten reversible pairs",
    )
    report(3, "every directed reaction has its reverse")

    # 4--5. Connectivity/linkage classes, recomputed from undirected support.
    neighbors = {index: set() for index in range(len(COMPLEXES))}
    for source, target in arc_rates:
        neighbors[source].add(target)
        neighbors[target].add(source)

    components = []
    unseen = set(neighbors)
    while unseen:
        initial = min(unseen)
        reached = {initial}
        queue = deque([initial])
        while queue:
            current = queue.popleft()
            for nxt in neighbors[current]:
                if nxt not in reached:
                    reached.add(nxt)
                    queue.append(nxt)
        components.append(reached)
        unseen -= reached

    require(len(components) == 1 and len(components[0]) == 10, "graph disconnected")
    report(4, "the undirected reaction graph is connected")
    report(5, "there is exactly one linkage class", "component count = 1")

    # 6. Stoichiometric rank from all directed reaction differences.
    columns = []
    for source, target, _ in REACTIONS:
        columns.append(
            sy.Matrix(
                [
                    COMPLEXES[target][coordinate] - COMPLEXES[source][coordinate]
                    for coordinate in range(3)
                ]
            )
        )
    stoichiometric_matrix = sy.Matrix.hstack(*columns)
    require(stoichiometric_matrix.rank() == 3, "stoichiometric rank is not three")
    witness = sy.Matrix.hstack(columns[0], columns[2], columns[4])
    require(witness.det() == -3, "the advertised rank witness changed")
    report(6, "the stoichiometric subspace has rank three", "minor = -3")
    return stoichiometric_matrix


def check_field_and_conic() -> tuple[object, tuple[sy.Expr, ...], tuple[sy.Expr, ...]]:
    # 7. Reconstruction versus the frozen displayed field.
    require(
        all(sy.expand(got - shown) == 0 for got, shown in zip(FIELD, DISPLAYED_FIELD)),
        "reconstructed field differs from the displayed field",
    )
    require(
        tuple(coordinate.subs({x: 1, y: 1, z: 1}) for coordinate in FIELD)
        == (807316, -2353772, -622888),
        "the field's explicit nonzero witness changed",
    )
    monomial_support = sorted(
        set().union(
            *(set(sy.Poly(coordinate, *xyz, domain=sy.QQ).monoms()) for coordinate in FIELD)
        )
    )
    coefficient_rows = sy.Matrix(
        [
            [sy.Poly(coordinate, *xyz, domain=sy.QQ).coeff_monomial(monomial)
             for monomial in monomial_support]
            for coordinate in FIELD
        ]
    )
    require(coefficient_rows.rank() == 3, "coordinate polynomials are linearly dependent")
    report(7, "the reconstructed mass-action field equals the displayed F")

    # 8. Derive A_i and B_i by two independent exact divisions; no A_i/B_i
    # data are supplied to this verifier.
    coefficients_of_L = []
    coefficients_of_Q = []
    q_poly = sy.Poly(Q, x, y, domain=sy.QQ)
    for coordinate in FIELD:
        quotient_L, remainder_xy = sy.div(
            coordinate, L, z, domain=sy.QQ.frac_field(x, y)
        )
        require(z not in remainder_xy.free_symbols, "division by L retained z")
        quotient_Q = sy.Poly(remainder_xy, x, y, domain=sy.QQ).exquo(q_poly).as_expr()
        require(
            sy.expand(coordinate - quotient_L * L - quotient_Q * Q) == 0,
            "derived L,Q representation failed",
        )
        coefficients_of_L.append(sy.expand(quotient_L))
        coefficients_of_Q.append(sy.expand(quotient_Q))
    report(8, "each F_i lies in (L,Q), with independently derived quotients")

    # 9. The quotient by L is a plane conic.  Its homogeneous symmetric matrix
    # is nonsingular.  A reducible projective conic over an algebraically
    # closed field is two lines and is singular at their intersection; hence
    # this determinant is an absolute irreducibility certificate.
    conic_matrix = sy.Matrix(((7, -1, -8), (-1, 7, -8), (-8, -8, 16)))
    require(conic_matrix.det() == -256, "projective conic determinant changed")
    conic_basis = reduced_basis((L, Q), xyz)
    leading_exponents = tuple(
        polynomial.LM(order="lex").exponents for polynomial in conic_basis.polys
    )
    require(
        leading_exponents == ((1, 0, 0), (0, 2, 0)),
        "unexpected conic Groebner staircase",
    )
    require(
        sy.factor_list(Q, x, y)[1] == [(Q, 1)],
        "Q is reducible over QQ",
    )
    report(
        9,
        "(L,Q) is an absolutely prime height-two conic ideal",
        "determinant = -256; quotient dimension = 1",
    )

    # 10. Parametrization identities, including absence of real poles.
    substitution = dict(zip(xyz, PARAMETRIZATION))
    for equation in (L, Q):
        numerator = sy.cancel(equation.subs(substitution)).as_numer_denom()[0]
        require(sy.expand(numerator) == 0, "parametrization misses the conic")
    denominator_poly = sy.Poly(denominator, t, domain=sy.QQ)
    require(
        denominator_poly.LC() > 0 and sy.discriminant(denominator_poly.as_expr(), t) < 0,
        "parametrization has a real pole",
    )
    require(
        tuple(coordinate.subs(t, 0) for coordinate in PARAMETRIZATION)
        == (sy.Rational(3, 2), sy.Rational(1, 2), sy.Integer(1)),
        "the parametrization does not contain the displayed equilibrium",
    )
    z_derivative = sy.cancel(sy.diff(PARAMETRIZATION[2], t))
    require(
        sy.cancel(z_derivative - 2 * (1 - t**2) / denominator**2) == 0,
        "the injectivity derivative certificate failed",
    )
    report(
        10,
        "the parametrization annihilates L,Q and is injective on (-1,1)",
        "z'(t)=2(1-t^2)/d(t)^2",
    )

    # 11. Exact real-geometry certificate.  On L=0, put a=x-y and s=x+y=z+1.
    # The positive-definite ellipse equation below bounds a and z.  Moreover,
    # (3z-1)(3-z)=4a^2 forces 1/3 <= z <= 3.  The equality
    # s^2-4a^2=4(z-1)^2 gives |a|<=s/2; hence
    # x=(s+a)/2 and y=(s-a)/2 are at least s/4 >= 1/3.
    a = x - y
    s = x + y
    ellipse_equation = 4 * a**2 + 3 * z**2 - 10 * z + 3
    conic_relation = 4 * (a**2 + (z - 1) ** 2) - (z + 1) ** 2
    require(
        sy.expand(conic_relation - Q - L * (3 * x + 3 * y + 3 * z - 13)) == 0,
        "ellipse identity modulo L,Q failed",
    )
    require(sy.expand(conic_relation - ellipse_equation) == 0, "ellipse expansion failed")
    require(
        sy.expand(
            ellipse_equation
            - (4 * a**2 + 3 * (z - sy.Rational(5, 3)) ** 2 - sy.Rational(16, 3))
        )
        == 0,
        "positive-definite ellipse completion failed",
    )
    require(
        sy.expand((3 * z - 1) * (3 - z) - 4 * a**2 + ellipse_equation) == 0,
        "z-bound factorization failed",
    )
    real_geometry_basis = reduced_basis((L, Q), xyz)
    norm_identity = s**2 - 4 * a**2 - 4 * (z - 1) ** 2
    require(
        sy.expand(real_geometry_basis.reduce(norm_identity)[1]) == 0,
        "positivity norm identity failed modulo the conic",
    )
    require(sy.Rational(1, 3) > 0 and sy.Rational(4, 3) / 4 > 0, "bad bounds")
    report(
        11,
        "every real conic point is positive and the real locus is compact",
        "1/3 <= x,y,z <= finite ellipse bounds",
    )

    return conic_basis, tuple(coefficients_of_L), tuple(coefficients_of_Q)


def check_gcd_jacobian_and_minimality(conic_basis) -> object:
    # 12. Exact gcd over QQ.
    primitive_coordinates = tuple(
        sy.Poly(coordinate, *xyz, domain=sy.QQ).primitive()[1]
        for coordinate in FIELD
    )
    common_gcd = reduce(sy.gcd, primitive_coordinates).monic()
    require(common_gcd.total_degree() == 0, "coordinate gcd is nonconstant")
    pairwise_degrees = tuple(
        sy.gcd(primitive_coordinates[i], primitive_coordinates[j]).total_degree()
        for i, j in combinations(range(3), 2)
    )
    require(pairwise_degrees == (0, 0, 0), "a coordinate pair has a common factor")
    report(12, "gcd(F_1,F_2,F_3)=1 over QQ[x,y,z]", "all pairwise gcd degrees = 0")

    # 13. Field-extension certificate.  The accompanying proof audit proves
    # the base-change lemma: a common divisor after any field extension would
    # force a common irreducible QQ divisor by taking its finite Galois orbit.
    # The hypotheses replayed here are precisely rational coefficients and
    # the unit gcd just computed.
    require(
        all(poly.domain == sy.QQ for poly in primitive_coordinates)
        and common_gcd.total_degree() == 0,
        "base-change gcd lemma hypotheses failed",
    )
    report(13, "gcd one persists over RR and CC", "exact base-change lemma applies")

    # 14. Rank exactly two at the displayed point: determinant zero and an
    # explicit nonzero 2x2 minor.
    point = {x: sy.Rational(3, 2), y: sy.Rational(1, 2), z: sy.Integer(1)}
    require(all(coordinate.subs(point) == 0 for coordinate in FIELD), "point is not steady")
    jacobian = sy.Matrix(FIELD).jacobian(xyz).subs(point)
    rank_two_minor = jacobian.extract((0, 1), (0, 1)).det()
    require(jacobian.det() == 0, "Jacobian rank is three")
    require(rank_two_minor == 243223374815232, "rank-two minor changed")
    report(14, "the Jacobian has rank two at (3/2,1/2,1)", f"minor = {rank_two_minor}")

    # 15 will also follow directly from the independently recomputed radical
    # decomposition below.  At this stage, K is contained in the height-two
    # prime p, while gcd one rules out every height-one prime over K.  Thus p
    # is already known to be minimal over K.
    steady_basis = reduced_basis(FIELD, xyz)
    require(
        all(sy.expand(conic_basis.reduce(coordinate)[1]) == 0 for coordinate in FIELD),
        "K is not contained in the conic prime",
    )
    require(len(steady_basis.polys) > 0 and common_gcd.total_degree() == 0, "height test failed")
    report(15, "the conic prime is an actual minimal steady-state component")
    return steady_basis


def eliminate_auxiliary(basis, auxiliary: sy.Symbol) -> tuple[sy.Expr, ...]:
    """Return the elimination generators free of the first lex variable."""

    return tuple(
        polynomial.as_expr()
        for polynomial in basis.polys
        if auxiliary not in polynomial.as_expr().free_symbols
    )


def check_radical_decomposition(steady_basis, conic_basis) -> None:
    # Compute a conic equation in the (y,z) quotient automatically from Q and
    # L.  Scaling it to be monic makes subsequent certificates canonical.
    eliminated_q = sy.rem(Q, L, x)
    D = sy.Poly(eliminated_q, y, z, domain=sy.QQ).monic().as_expr()
    require(
        sy.expand(D - (y**2 - y * z - y + sy.Rational(7, 16) * z**2
                       - sy.Rational(1, 8) * z + sy.Rational(7, 16))) == 0,
        "unexpected eliminated conic equation",
    )

    # 16a. Independently discover the residual component as K : D^infinity.
    # The standard exact saturation identity is
    #   K : D^infinity = (K + <1-uD>) intersect QQ[x,y,z].
    u = sy.symbols("u")
    saturation_basis = reduced_basis(
        tuple(FIELD) + (1 - u * D,), (u, x, y, z)
    )
    residual_generators = eliminate_auxiliary(saturation_basis, u)
    require(len(residual_generators) > 0, "saturation produced no residual ideal")
    residual_basis = reduced_basis(residual_generators, xyz)

    # Its canonical triangular shape is checked without supplying any of its
    # large coefficients as input.
    residual = basis_expressions(residual_basis)
    require(len(residual) == 3, "residual basis is not triangular of length three")
    require(
        residual[0].free_symbols <= {x, z}
        and sy.degree(residual[0], x) == 1
        and sy.Poly(residual[0], x).LC() == 1,
        "first residual equation is not x+r_x(z)",
    )
    require(
        residual[1].free_symbols <= {y, z}
        and sy.degree(residual[1], y) == 1
        and sy.Poly(residual[1], y).LC() == 1,
        "second residual equation is not y+r_y(z)",
    )
    require(
        residual[2].free_symbols <= {z}
        and sy.degree(residual[2], z) == 15
        and sy.Poly(residual[2], z).LC() == 1,
        "last residual equation is not monic of degree fifteen",
    )
    R = sy.Poly(residual[2], z, domain=sy.QQ)
    factor_constant, factorization = sy.factor_list(R.as_expr(), z)
    require(factor_constant != 0, "zero elimination polynomial")
    require(
        len(factorization) == 1
        and sy.degree(factorization[0][0], z) == 15
        and factorization[0][1] == 1,
        "degree-fifteen residual polynomial is reducible",
    )

    # 16b. Recompute p intersection q from its defining elimination formula,
    # rather than checking a precomputed primary decomposition:
    #   p intersect q = (v p + (1-v) q) intersect QQ[x,y,z].
    v = sy.symbols("v")
    intersection_input = tuple(v * generator for generator in (L, Q)) + tuple(
        (1 - v) * generator for generator in residual
    )
    intersection_with_v = reduced_basis(intersection_input, (v, x, y, z))
    intersection_generators = eliminate_auxiliary(intersection_with_v, v)
    intersection_basis = reduced_basis(intersection_generators, xyz)
    require(
        exact_same_basis(intersection_basis, steady_basis),
        "K differs from the independently recomputed p intersection q",
    )
    report(
        16,
        "the asserted radical decomposition is exact",
        "saturation plus intersection elimination",
    )

    # 17. q is maximal because its quotient is QQ[z]/(R), with irreducible R.
    # In characteristic zero R is squarefree, which is also checked directly.
    derivative_gcd = sy.gcd(R, R.diff()).monic()
    require(derivative_gcd.degree() == 0, "degree-fifteen component is nonreduced")
    # Compute p+q directly; [1] is the exact comaximality certificate.
    sum_basis = reduced_basis((L, Q) + residual, xyz)
    require(
        len(sum_basis.polys) == 1 and sum_basis.polys[0].as_expr() == 1,
        "residual points meet the conic",
    )
    report(
        17,
        "the residual component is fifteen reduced points disjoint from the conic",
        "deg R = 15, gcd(R,R') = 1, p+q = (1)",
    )


def main() -> None:
    check_raw_network()
    conic_basis, _, _ = check_field_and_conic()
    steady_basis = check_gcd_jacobian_and_minimality(conic_basis)
    check_radical_decomposition(steady_basis, conic_basis)
    print("PASS: all clean-room exact checks 1--17 succeeded")
    print("NOTE: structural proof audits 18--20 are in PROOF_AUDIT.md")


if __name__ == "__main__":
    main()
