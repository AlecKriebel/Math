#!/usr/bin/env python3
"""Independent exact contour/Fourier mechanism checks, not a proof certificate.

No imported review code. All algebraic checks use fractions, including complex
arithmetic. Every guard uses explicit exceptions and survives python -O.
"""
import argparse
import json
from fractions import Fraction as F


class Q:
    def __init__(self, x=0, y=0):
        self.x, self.y = F(x), F(y)

    def __add__(self, other):
        if not isinstance(other, Q):
            other = Q(other)
        return Q(self.x + other.x, self.y + other.y)

    __radd__ = __add__

    def __neg__(self):
        return Q(-self.x, -self.y)

    def __sub__(self, other):
        return self + (-other if isinstance(other, Q) else -Q(other))

    def __mul__(self, other):
        if not isinstance(other, Q):
            other = Q(other)
        return Q(self.x * other.x - self.y * other.y,
                 self.x * other.y + self.y * other.x)

    __rmul__ = __mul__

    def __truediv__(self, other):
        if not isinstance(other, Q):
            other = Q(other)
        norm = other.x**2 + other.y**2
        return self * Q(other.x / norm, -other.y / norm)

    def __eq__(self, other):
        if not isinstance(other, Q):
            other = Q(other)
        return self.x == other.x and self.y == other.y

    def norm(self):
        return self.x**2 + self.y**2

    def out(self):
        return [str(self.x), str(self.y)]


def require(predicate, message):
    if not predicate:
        raise ValueError(message)


def contour_residues(center, radius_squared, z):
    """Integral_D (w-z)^-2 dA / pi from complex Green and residues.

    On the circle bar(w)=bar(center)+q/(w-center). The constant
    term has zero residue. Pole at center contributes q/(center-z)^2;
    an interior z contributes -q/(z-center)^2, hence cancellation.
    Interior formula means L2/pv; our exterior tests are ordinary.
    """
    delta = z - center
    require(delta.norm() != radius_squared, "boundary excluded")
    if delta == 0:
        return Q(0)
    center_residue = Q(radius_squared) / (delta * delta)
    z_residue = -Q(radius_squared) / (delta * delta)
    return center_residue + (z_residue if delta.norm() < radius_squared else Q(0))


def run(wrong):
    checks = []
    cases = [
        (Q(0), F(1), Q(2, 1)),
        (Q(5, -3), F(1, 1000000), Q(-7, 4)),
        (Q(-1000, 2000), F(7, 11), Q(0, 1)),
        (Q(0), F(1, 2), Q(F(1, 10), F(1, 20))),
    ]
    for center, q, z in cases:
        value = contour_residues(center, q, z)
        if (z-center).norm() > q:
            field = Q(q) / ((z-center)*(z-center))
            transformed = -value
            claimed = field if wrong == 'sign' else -field
            require(transformed == claimed, "Beurling exterior sign guard")
            mass = q * (2 if wrong == 'mass' else 1)
            require(value == Q(mass) / ((z-center)*(z-center)), "pi-times-mass guard")
        else:
            require(value == 0, "interior residue cancellation")
        checks.append({'center':center.out(),'q':str(q),'z':z.out(),'integral_over_pi':value.out()})

    # Annulus 1<|w|<2 has area 3pi. Exterior field matches a mass 3pi
    # at zero, but this identity MUST NOT be continued through its hole.
    z_outer, z_hole = Q(3, 1), Q(F(1, 2), F(1, 3))
    outer = contour_residues(Q(0), F(4), z_outer) - contour_residues(Q(0), F(1), z_outer)
    hole = contour_residues(Q(0), F(4), z_hole) - contour_residues(Q(0), F(1), z_hole)
    require(outer == Q(3)/(z_outer*z_outer), 'annulus exterior identity')
    require(hole == 0, 'annulus hole cancellation')
    purported_hole = Q(3)/(z_hole*z_hole)
    require(hole == purported_hole if wrong == 'hole' else hole != purported_hole,
            'exterior-only continuation guard')

    # Exact four-point angular sampling, with the finite aliasing correction
    # retained. This checks the minus sign in rho^2-r^2 independently of
    # any floating quadrature or formal logarithm expansion.
    angular = []
    for q in [F(1,1000000),F(1,10),F(1,3),F(1,2),F(9,10),F(999,1000)]:
        sample_mean = (F(1)/(1-q)**2 + F(1)/(1+q)**2 + F(2)/(1+q*q))/4
        base = 1 + q*q if wrong == 'angular' else 1 - q*q
        formula = (1+q**4)/(base*(1-q**4))
        require(sample_mean == formula, 'angular denominator guard')
        angular.append({'q':str(q),'four_point_mean':str(sample_mean),
                        'continuous_mean':str(1/(1-q*q)),
                        'alias_ratio':str((1+q**4)/(1-q**4))})
    return {'status':'PASS','arithmetic':'exact rational complex residues and exact 4-point Fourier sampling',
            'disk_cases':checks,'annulus':{'outer':outer.out(),'hole':hole.out(),'false_point_field_in_hole':purported_hole.out()},
            'angular':angular,'scope':'finite mechanism diagnostics; universal theorem uses independent analytic derivation'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--wrong', choices=['sign','mass','hole','angular'])
    args = parser.parse_args()
    print(json.dumps(run(args.wrong),indent=2))
