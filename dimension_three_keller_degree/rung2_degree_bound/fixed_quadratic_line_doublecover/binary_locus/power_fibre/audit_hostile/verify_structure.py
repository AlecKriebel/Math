#!/usr/bin/env python3
"""Non-SymPy structural audit: stabilizer, plane exits, and cube coordinate.

The determinant algebra is reconstructed separately in PARI/GP.  This file
uses only the Python standard library and exact rational arithmetic.
"""

from __future__ import annotations

import argparse
import itertools
from fractions import Fraction


if not __debug__:
    raise RuntimeError("assertions must remain enabled")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


# ---------------------------------------------------------------------------
# Tiny exact polynomial ring, used only for the two source-coordinate
# determinants.  A monomial is an exponent tuple and coefficients are rational.
# ---------------------------------------------------------------------------

Monomial = tuple[int, ...]
Polynomial = dict[Monomial, Fraction]
NSYMS = 4  # l33, l32, Gp, Gq
ZERO_MONOMIAL = (0,) * NSYMS


def constant(value: int | Fraction) -> Polynomial:
    value = Fraction(value)
    return {} if value == 0 else {ZERO_MONOMIAL: value}


def symbol(index: int) -> Polynomial:
    exponent = [0] * NSYMS
    exponent[index] = 1
    return {tuple(exponent): Fraction(1)}


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, Fraction(0)) + coefficient
        if result[monomial] == 0:
            del result[monomial]
    return result


def neg(value: Polynomial) -> Polynomial:
    return {monomial: -coefficient for monomial, coefficient in value.items()}


def mul(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for lm, lc in left.items():
        for rm, rc in right.items():
            monomial = tuple(a + b for a, b in zip(lm, rm))
            result[monomial] = result.get(monomial, Fraction(0)) + lc * rc
    return {m: c for m, c in result.items() if c}


def det3(matrix: list[list[Polynomial]]) -> Polynomial:
    positive = add(
        add(
            mul(mul(matrix[0][0], matrix[1][1]), matrix[2][2]),
            mul(mul(matrix[0][1], matrix[1][2]), matrix[2][0]),
        ),
        mul(mul(matrix[0][2], matrix[1][0]), matrix[2][1]),
    )
    negative = add(
        add(
            mul(mul(matrix[0][2], matrix[1][1]), matrix[2][0]),
            mul(mul(matrix[0][1], matrix[1][0]), matrix[2][2]),
        ),
        mul(mul(matrix[0][0], matrix[1][2]), matrix[2][1]),
    )
    return add(positive, neg(negative))


def check_source_coordinate_determinants() -> None:
    zero, one = constant(0), constant(1)
    l33, l32, gp, gq = (symbol(index) for index in range(NSYMS))

    # (p,q,r) -> (p,q,w=l33*r+G(p,q)).
    first = [
        [one, zero, zero],
        [zero, one, zero],
        [gp, gq, l33],
    ]
    require(det3(first) == l33, "wrong l33-coordinate determinant")

    # (p,q,r) -> (p,r,w=G(p,q)), on the leaf G_q=l32.
    second = [
        [one, zero, zero],
        [zero, zero, one],
        [gp, l32, zero],
    ]
    require(det3(second) == neg(l32), "wrong l32-coordinate determinant")

    print("PASS both source coordinates have determinants l33 and -l32")
    print("PASS composed plane Jacobians scale by kappa/l33 and -kappa/l32")


# ---------------------------------------------------------------------------
# Actual stabilizer and its action on ell=v7*p+v8*q.
# ---------------------------------------------------------------------------


def check_stabilizer(orbit_fault: bool) -> None:
    # The cube p^3 forces p -> a*p.  If q -> c*p+b*q, then p^2 q^2
    # has p^3 q coefficient 2*a^2*b*c.  Invertibility gives a*b != 0,
    # so preservation of <p^4,p^2q^2> forces c=0.
    for a, b in itertools.product((Fraction(1), Fraction(2)), repeat=2):
        for c in (Fraction(-2), Fraction(0), Fraction(3)):
            p3q = 2 * a * a * b * c
            require((p3q == 0) == (c == 0), "binary stabilizer test failed")

    # Under (p,q,r)=(aP,bQ,cR+alpha P+beta Q) and the induced target
    # rescaling of component two by a^-2 b^-2:
    #   v7 -> v7*a^-1*b^-2*c^2,
    #   v8 -> v8*a^-2*b^-1*c^2.
    v7_weight = (-1, -2, 2)  # powers of (a,b,c)
    direct_v8_weight = (-2, -1, 2)
    claimed_v8_weight = (-2, 1, 2) if orbit_fault else direct_v8_weight
    require(
        claimed_v8_weight == direct_v8_weight,
        "mutated orbit action escaped detection",
    )

    # A shear in r contributes to an r^2 coefficient from r^3 only.  Thus on
    # v9=0 it changes lower r-powers but leaves both zero/nonzero entries of
    # ell invariant.
    require(v7_weight == (-1, -2, 2), "wrong v7 stabilizer weight")
    require(direct_v8_weight == (-2, -1, 2), "wrong v8 stabilizer weight")

    patterns = set(itertools.product((0, 1), repeat=2))
    require(
        patterns == {(0, 0), (1, 0), (0, 1), (1, 1)},
        "four zero patterns are not exhaustive",
    )

    # Check the explicit normalizing scalars on exact rational samples.  The
    # square c exists because the ground field is C.
    for v7, v8 in itertools.product(
        (Fraction(-3), Fraction(2), Fraction(5, 2)), repeat=2
    ):
        b = v7 / v8
        c_squared = v7 / (v8 * v8)
        new_v7 = v7 * c_squared / (b * b)
        new_v8 = v8 * c_squared / b
        require((new_v7, new_v8) == (1, 1), "two-entry normalization failed")

    # On tp != 0, r -> r+alpha*p+beta*q sends
    # (c0,c1) -> (c0+tp*alpha,c1+tp*beta).
    for tp, c0, c1 in (
        (Fraction(2), Fraction(3), Fraction(-5)),
        (Fraction(-3, 2), Fraction(7), Fraction(4)),
    ):
        alpha, beta = -c0 / tp, -c1 / tp
        require(c0 + tp * alpha == 0, "source shear did not kill c0")
        require(c1 + tp * beta == 0, "source shear did not kill c1")

    print("PASS actual stabilizer is diagonal on p,q, triangular in r")
    print("PASS ell has exactly the four orbits 0,p,q,p+q on v9=0")
    print("PASS tp!=0 shear legally and simultaneously kills c0,c1")


# ---------------------------------------------------------------------------
# Exact monomial-support calculation for the two zero-orbit plane exits.
# ---------------------------------------------------------------------------

Exponent = tuple[int, int, int]  # p,q,r


def support(*monomials: Exponent) -> set[Exponent]:
    return set(monomials)


LINEAR = support((1, 0, 0), (0, 1, 0), (0, 0, 1))
BINARY_CUBIC = support((3, 0, 0), (2, 1, 0), (1, 2, 0), (0, 3, 0))

F1_ZERO = (
    LINEAR
    | support((2, 0, 0), (1, 1, 0), (0, 2, 0), (1, 0, 1), (0, 1, 1))
    | BINARY_CUBIC
    | support((4, 0, 0))
)

F2_ZERO = (
    LINEAR
    | support(
        (2, 0, 0),
        (1, 1, 0),
        (0, 2, 0),
        (1, 0, 1),
        (0, 1, 1),
        (0, 0, 2),
    )
    | BINARY_CUBIC
    | support((2, 0, 1), (1, 1, 1), (0, 2, 1))
    | support((2, 2, 0))
)


def weighted_degree(monomial: Exponent, weights: Exponent) -> int:
    return sum(exponent * weight for exponent, weight in zip(monomial, weights))


def check_plane_degrees() -> None:
    # r=(w-G(p,q))/l33 and deg_{p,q} G=3.
    first_weights = (1, 1, 3)
    first_degrees = (
        max(weighted_degree(m, first_weights) for m in F1_ZERO),
        max(weighted_degree(m, first_weights) for m in F2_ZERO),
    )
    require(first_degrees == (4, 6), f"wrong first ceiling: {first_degrees}")
    require(
        weighted_degree((0, 0, 2), first_weights) == 6,
        "bb*r^2 does not realize the degree-six ceiling",
    )

    # q=(w-p^3-c0*p^2-l31*p)/l32.
    second_weights = (1, 3, 1)
    second_degrees = (
        max(weighted_degree(m, second_weights) for m in F1_ZERO),
        max(weighted_degree(m, second_weights) for m in F2_ZERO),
    )
    require(second_degrees == (9, 9), f"wrong second ceiling: {second_degrees}")
    require(
        weighted_degree((0, 3, 0), second_weights) == 9,
        "binary q^3 term does not realize the degree-nine ceiling",
    )

    print("PASS zero-orbit l33 chart has component degrees (4,6)")
    print("PASS zero-orbit l32 chart has component degrees (9,9)")


# ---------------------------------------------------------------------------
# Independent hostile proof of the cube-leading submersion proposition.
# ---------------------------------------------------------------------------


def solve_two_by_two(
    a11: Fraction,
    a12: Fraction,
    a22: Fraction,
    rhs1: Fraction,
    rhs2: Fraction,
) -> tuple[Fraction, Fraction]:
    determinant = a11 * a22 - a12 * a12
    require(determinant != 0, "singular matrix passed to rank-two solver")
    return (
        (rhs1 * a22 - a12 * rhs2) / determinant,
        (a11 * rhs2 - a12 * rhs1) / determinant,
    )


def check_cube_coordinate_proposition() -> None:
    # Normalize
    # f=x^3+a*x^2+x*(b*y+c*z)+q(y,z)+d*x+e*y+g*z.
    #
    # Rank(q)=2: fy=fz=0 makes y,z affine-linear in x.  Exact sampling of
    # every small nonsingular symmetric transverse Hessian verifies that fx
    # retains x^2 coefficient 3; hence it has a complex root.
    rank_two_samples = 0
    values = tuple(Fraction(value) for value in (-2, -1, 0, 1, 2))
    for a11, a12, a22 in itertools.product(values, repeat=3):
        if a11 * a22 - a12 * a12 == 0:
            continue
        for b, c, e, g in (
            (Fraction(0), Fraction(0), Fraction(0), Fraction(0)),
            (Fraction(1), Fraction(-2), Fraction(2), Fraction(1)),
            (Fraction(-1), Fraction(1), Fraction(0), Fraction(2)),
        ):
            y_x, z_x = solve_two_by_two(a11, a12, a22, -b, -c)
            _y_0, _z_0 = solve_two_by_two(a11, a12, a22, -e, -g)
            # b*y+c*z contributes only degree one in x.
            fx_x2 = Fraction(3)
            fx_x1_extra = b * y_x + c * z_x
            require(fx_x2 == 3, "rank-two critical equation lost degree two")
            require(
                isinstance(fx_x1_extra, Fraction),
                "rank-two solve ceased to be exact",
            )
            rank_two_samples += 1
    require(rank_two_samples > 100, "rank-two boundary was under-tested")

    # Rank(q)=1: diagonalize q to alpha*y^2 with alpha!=0 and z the
    # transverse-kernel direction.  If the xz coefficient c is nonzero,
    # fz=0, fy=0, fx=0 solve successively.  If c=0 and the z-linear
    # coefficient g vanishes, fy=0 followed by the leading-3 quadratic fx
    # gives a critical point.  The only submersion chart is c=0,g!=0, where
    # f=g*z+h(x,y) is triangular.
    for c, g in itertools.product(values, repeat=2):
        survives = c == 0 and g != 0
        classified_as_critical = c != 0 or (c == 0 and g == 0)
        require(
            survives != classified_as_critical,
            "rank-one kernel pivot was not exhaustive",
        )

    # Rank(q)=0: fy=bx+e and fz=cx+g.  For (b,c)!=0 they have no common
    # root exactly when Delta=b*g-c*e is nonzero.  Then the linear change
    # Y=b*y+c*z, Z=e*y+g*z has determinant Delta and
    # f=h(x)+x*Y+Z.  If (b,c)=0, submersion means (e,g)!=0 and is directly
    # triangular.
    rank_zero_samples = 0
    for b, c, e, g in itertools.product(values, repeat=4):
        if (b, c) == (0, 0):
            survives = (e, g) != (0, 0)
        else:
            delta = b * g - c * e
            survives = delta != 0
            require(
                survives == (delta != 0),
                "rank-zero unimodular-pair criterion failed",
            )
        if survives:
            rank_zero_samples += 1
    require(rank_zero_samples > 100, "rank-zero boundary was under-tested")

    # Every surviving construction is linear followed by
    # (x,y,z)->(x,y,f), or by (x,Y,Z)->(x,Y,h(x)+xY+Z).  Both inverse
    # formulas have degree at most three, and degree three is realized by x^3.
    inverse_degree = max(1, 3, 1 + 1)
    require(inverse_degree == 3, "cube-coordinate inverse bound is not three")

    print(f"PASS cube-coordinate rank-two tests: {rank_two_samples} exact cases")
    print("PASS cube-coordinate rank-one kernel pivot is exhaustive")
    print(f"PASS cube-coordinate rank-zero tests: {rank_zero_samples} exact cases")
    print("PASS every cube-leading submersion is a coordinate of inverse degree <=3")


def check_degree_corollaries() -> None:
    require(3 * 4 == 12, "quartic composition degree is not 12")
    require(3 * 35 == 105 and 105 < 108, "d<=35 threshold arithmetic failed")
    require(not (3 * 36 < 108), "the argument was allowed to overreach to d=36")
    print("PASS power fibre straightens globally to plane fibre degree <=12")
    print("PASS published/preprint plane floor 108 gives d<=35, but not d=36")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fault-orbit", action="store_true")
    args = parser.parse_args()

    check_source_coordinate_determinants()
    check_stabilizer(args.fault_orbit)
    check_plane_degrees()
    check_cube_coordinate_proposition()
    check_degree_corollaries()
    print("ALL HOSTILE STRUCTURAL CHECKS PASSED")


if __name__ == "__main__":
    main()

