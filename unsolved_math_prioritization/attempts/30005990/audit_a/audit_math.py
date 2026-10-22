#!/usr/bin/env python3
"""Independent exact finite controls; these do not certify the analytic theorem."""
from fractions import Fraction as F
from itertools import product
import json


def point(axis, radius):
    return (axis if radius else -1, F(radius))


def distance(a, b):
    return abs(a[1] - b[1]) if a[0] == b[0] else a[1] + b[1]


def geodesic(a, b, s):
    if a[0] == b[0]:
        return point(a[0], (1-s)*a[1] + s*b[1])
    r = (1-s)*a[1] - s*b[1]
    return point(a[0], r) if r >= 0 else point(b[0], -r)


def euclidean_squared(a, b):
    return (a[1]-b[1])**2 if a[0] == b[0] else a[1]**2 + b[1]**2


def main():
    # For h=x^p t^k and lift h/t into m radial coordinates, the x term
    # agrees identically. The radial coefficient differs by (k-1)(m-3).
    monomials = 0
    wrong_dimension_detected = 0
    for p, k in product(range(7), range(1, 8)):
        rhs = k*(k-1)
        assert (k-1)*(k+3-3) == rhs
        monomials += 1
        for m in (1, 2, 4, 5):
            residual = (k-1)*(k+m-3) - rhs
            assert residual == (k-1)*(m-3)
            wrong_dimension_detected += bool(residual)
    assert wrong_dimension_detected
    # The exact weak identity differs by d_t(h*a), independently of the
    # tangential derivatives: h_t*(a+t*a_t)-(t*h_t-h)*a_t = h_t*a+h*a_t.
    weak_identities = 0
    for h, ht, a, at, t in product(range(-2, 3), repeat=5):
        assert ht*(a+t*at) - (t*ht-h)*at == ht*a+h*at
        weak_identities += 1
    # Check the concrete star-tree geodesic used in the boundary cutoff.
    points = [point(-1, 0)] + [point(i, r) for i in range(3) for r in (F(1,2), F(1), F(2))]
    parameters = [F(j,4) for j in range(5)]
    metric_checks = geodesic_speed_checks = convexity_checks = 0
    for a, b in product(points, repeat=2):
        d2 = distance(a,b)**2
        e2 = euclidean_squared(a,b)
        assert e2 <= d2 <= 2*e2
        metric_checks += 1
        for s, t in product(parameters, repeat=2):
            assert distance(geodesic(a,b,s),geodesic(a,b,t)) == abs(s-t)*distance(a,b)
            geodesic_speed_checks += 1
    for a, b, c, d in product(points, repeat=4):
        for s in parameters:
            assert distance(geodesic(a,b,s),geodesic(c,d,s)) <= (1-s)*distance(a,c)+s*distance(b,d)
            convexity_checks += 1
    # An intrinsic interpolation stays on the tree. Euclidean averaging
    # provides an explicit negative control: distinct positive axes mix.
    a, b = (F(1),F(0),F(0)), (F(0),F(1),F(0))
    midpoint = tuple((x+y)/2 for x,y in zip(a,b))
    assert midpoint[0]*midpoint[1] > 0
    return {
        "status": "pass",
        "analytic_proof_certified_by_computation": False,
        "lift_monomials": monomials,
        "wrong_dimension_nonzero_residuals": wrong_dimension_detected,
        "weak_test_identities": weak_identities,
        "tree_metric_checks": metric_checks,
        "tree_constant_speed_checks": geodesic_speed_checks,
        "tree_endpoint_convexity_checks": convexity_checks,
        "euclidean_interpolation_negative_control": "detected",
    }

if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
