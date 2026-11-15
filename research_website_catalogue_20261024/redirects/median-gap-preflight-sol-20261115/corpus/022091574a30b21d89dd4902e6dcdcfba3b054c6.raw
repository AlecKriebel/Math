#!/usr/bin/env python3
"""Exact finite checks for the OWR-4136-011 equality argument.

Python standard library only. No random sampling and no floating-point tests.
This checks examples and identities; it does not prove the infinite geometric
decomposition, the general equality theorem, or a claim of priority.
"""

from fractions import Fraction as Q
from itertools import combinations
from math import factorial
import json


CHECKS = 0


def require(condition, message):
    """Do not use assert: checks must also run under python -O."""
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError(message)


def point(*coordinates):
    return tuple(Q(x) for x in coordinates)


def norm2(v):
    return sum((x * x for x in v), Q(0))


def determinant(matrix):
    a = [list(map(Q, row)) for row in matrix]
    value = Q(1)
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None:
            return Q(0)
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            value = -value
        divisor = a[j][j]
        value *= divisor
        for i in range(j + 1, len(a)):
            multiplier = a[i][j] / divisor
            for k in range(j + 1, len(a)):
                a[i][k] -= multiplier * a[j][k]
    return value


def polynomial_product(left, right):
    result = {}
    for a, c in left.items():
        for b, d in right.items():
            exponent = tuple(x + y for x, y in zip(a, b))
            result[exponent] = result.get(exponent, Q(0)) + c * d
    return result


def standard_simplex_integral(polynomial, n):
    """Integrate monomials on {t_i>=0, sum t_i<=1} by factorials.

    The monomial formula follows by iterating the one-variable beta integral:
    integral t^a dt = product(a_i!)/(n+sum(a_i))!.
    """
    total = Q(0)
    for exponent, coefficient in polynomial.items():
        numerator = 1
        for power in exponent:
            numerator *= factorial(power)
        total += coefficient * Q(numerator, factorial(n + sum(exponent)))
    return total


def simplex_integrals(vertices):
    """Return volume, unnormalized first moments, and integral |x|^2.

    This path expands affine coordinate polynomials, squares them, and
    integrates their monomials. It does not invoke the vertex-sum identity
    being checked.
    """
    n = len(vertices[0])
    require(len(vertices) == n + 1, "simplex vertex count")
    require(all(len(v) == n for v in vertices), "coordinate dimensions")
    origin = vertices[0]
    edge_matrix = [[vertices[j + 1][i] - origin[i] for j in range(n)]
                   for i in range(n)]
    jacobian = abs(determinant(edge_matrix))
    require(jacobian > 0, "nondegenerate simplex")
    zero = (0,) * n
    coordinates = []
    for i in range(n):
        polynomial = {zero: origin[i]}
        for j in range(n):
            exponent = tuple(int(k == j) for k in range(n))
            polynomial[exponent] = edge_matrix[i][j]
        coordinates.append(polynomial)
    volume = jacobian * standard_simplex_integral({zero: Q(1)}, n)
    first = tuple(jacobian * standard_simplex_integral(p, n)
                  for p in coordinates)
    second = jacobian * sum((standard_simplex_integral(
        polynomial_product(p, p), n) for p in coordinates), Q(0))
    return volume, first, second


def normalized(integrals):
    volume, first, second = integrals
    return tuple(x / volume for x in first), second / volume


def add_integrals(integrals):
    n = len(integrals[0][1])
    return (sum((a[0] for a in integrals), Q(0)),
            tuple(sum((a[1][i] for a in integrals), Q(0)) for i in range(n)),
            sum((a[2] for a in integrals), Q(0)))


def check_simplex_identity(vertices):
    integrals = simplex_integrals(vertices)
    center, moment = normalized(integrals)
    n = len(center)
    expected_center = tuple(sum((v[i] for v in vertices), Q(0)) / (n + 1)
                            for i in range(n))
    mean_vertex_norm = sum((norm2(v) for v in vertices), Q(0)) / (n + 1)
    expected_moment = (mean_vertex_norm + (n + 1) * norm2(center)) / (n + 2)
    require(center == expected_center, "simplex centroid identity")
    require(moment == expected_moment, "simplex second-moment identity")
    return integrals


def check_deficit(simplices, radius2, body_integrals=None, equality=False):
    n = len(simplices[0][0])
    pieces = [check_simplex_identity(s) for s in simplices]
    combined = add_integrals(pieces)
    if body_integrals is not None:
        require(combined == body_integrals, "independent body integrals agree")
    else:
        body_integrals = combined
    volume = body_integrals[0]
    center, moment = normalized(body_integrals)
    lhs = moment - (radius2 + (n + 1) * norm2(center)) / (n + 2)
    radial = Q(0)
    centroid_variance = Q(0)
    for vertices, integrals in zip(simplices, pieces):
        require(all(norm2(v) >= radius2 for v in vertices), "vertex norm bound")
        weight = integrals[0] / volume
        piece_center, _ = normalized(integrals)
        average = sum((norm2(v) for v in vertices), Q(0)) / (n + 1)
        radial += weight * (average - radius2) / (n + 2)
        difference = tuple(a - b for a, b in zip(piece_center, center))
        centroid_variance += Q(n + 1, n + 2) * weight * norm2(difference)
    require(lhs == radial + centroid_variance, "exact deficit identity")
    require(radial >= 0 and centroid_variance >= 0, "nonnegative deficit terms")
    require((lhs == 0) if equality else (lhs > 0), "expected equality/strictness")
    return {"dimension": n, "volume": str(volume),
            "centroid": [str(x) for x in center], "second_moment": str(moment),
            "deficit": str(lhs), "radial_term": str(radial),
            "centroid_variance_term": str(centroid_variance)}


def check_retained_pair(first, second, body_integrals, radius2):
    """Check the independent finite-approximation strictness bound."""
    a_data, b_data = simplex_integrals(first), simplex_integrals(second)
    a, b, volume = a_data[0], b_data[0], body_integrals[0]
    p, _ = normalized(a_data)
    q, _ = normalized(b_data)
    z, moment = normalized(body_integrals)
    n = len(z)
    difference2 = norm2(tuple(x-y for x, y in zip(p, q)))
    require(difference2 > 0, "retained simplices have distinct centroids")
    weighted_center = tuple((a*x+b*y)/(a+b) for x, y in zip(p, q))
    lhs = a*norm2(tuple(x-y for x, y in zip(p, z))) + b*norm2(
        tuple(x-y for x, y in zip(q, z)))
    rhs = a*b/(a+b)*difference2 + (a+b)*norm2(
        tuple(x-y for x, y in zip(weighted_center, z)))
    require(lhs == rhs, "retained-pair completed-square identity")
    bound = Q(n+1, n+2)*a*b/(volume*(a+b))*difference2
    deficit = moment - (radius2+(n+1)*norm2(z))/(n+2)
    require(0 < bound <= deficit, "positive retained-pair strictness bound")
    return str(bound)


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def hull(points):
    ordered = sorted(set(points))
    lower, upper = [], []
    for p in ordered:
        while len(lower) >= 2 and orient(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(ordered):
        while len(upper) >= 2 and orient(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    result = lower[:-1] + upper[:-1]
    require(len(result) >= 3, "nondegenerate polygon hull")
    return result


def edges(polygon):
    return zip(polygon, polygon[1:] + polygon[:1])


def polygon_integrals(polygon):
    """Green's theorem edge sums, independent of simplex integration."""
    area, first_x, first_y, second = Q(0), Q(0), Q(0), Q(0)
    for (x, y), (u, v) in edges(polygon):
        cross = x * v - u * y
        area += cross / 2
        first_x += (x + u) * cross / 6
        first_y += (y + v) * cross / 6
        second += (x*x + x*u + u*u + y*y + y*v + v*v) * cross / 12
    require(area > 0, "CCW polygon with positive area")
    return area, (first_x, first_y), second


def disjoint_interiors(left, right):
    """Exact separating-axis criterion for convex CCW polygons."""
    return any(all(orient(a, b, p) <= 0 for p in other)
               for polygon, other in ((left, right), (right, left))
               for a, b in edges(polygon))


def visible_update(polygon, new_point, expect_coplanar=False):
    edge_signs = [orient(a, b, new_point) for a, b in edges(polygon)]
    require(any(sign < 0 for sign in edge_signs), "new point outside old hull")
    if expect_coplanar:
        require(any(sign == 0 for sign in edge_signs), "coplanar edge exercised")
    triangles = [hull([new_point, a, b])
                 for (a, b), sign in zip(edges(polygon), edge_signs) if sign < 0]
    updated = hull(polygon + [new_point])
    for triangle in triangles:
        require(disjoint_interiors(polygon, triangle), "shell avoids old interior")
        require(all(orient(a, b, p) >= 0 for a, b in edges(updated)
                    for p in triangle), "shell lies in updated convex hull")
    for a, b in combinations(triangles, 2):
        require(disjoint_interiors(a, b), "shell simplex interiors disjoint")
    independent = polygon_integrals(updated)
    require(add_integrals([polygon_integrals(polygon)] +
                          [polygon_integrals(t) for t in triangles]) == independent,
            "visible shell conserves polygon area and moments")
    require(add_integrals([polygon_integrals(polygon)] +
                          [simplex_integrals(t) for t in triangles]) == independent,
            "independent simplex/polygon shell integrations agree")
    return updated, triangles


def main():
    cases = {}
    triangle = [point(5, 0), point(3, 4), point(-5, 0)]
    cases["nonregular_triangle_nonzero_centroid"] = check_deficit(
        [triangle], Q(25), equality=True)
    require(len({norm2(tuple(a-b for a, b in zip(v, w)))
                 for v, w in combinations(triangle, 2)}) > 1,
            "triangle is nonregular")
    require(norm2(normalized(simplex_integrals(triangle))[0]) > 0,
            "triangle centroid is nonzero")

    cases["interval_equality"] = check_deficit(
        [[point(-1), point(1)]], Q(1), equality=True)
    cases["interval_strict"] = check_deficit(
        [[point(1), point(3)]], Q(1))

    square = [point(-1, -1), point(1, -1), point(1, 1), point(-1, 1)]
    square_pieces = [[square[0], square[1], square[2]],
                     [square[0], square[2], square[3]]]
    require(disjoint_interiors(*square_pieces), "square triangle interiors disjoint")
    cases["square_strict"] = check_deficit(
        square_pieces, Q(2), polygon_integrals(square))
    cases["square_strict"]["retained_pair_bound"] = check_retained_pair(
        *square_pieces, polygon_integrals(square), Q(2))

    sphere_points = [point(5, 0), point(3, 4), point(-3, 4), point(-5, 0),
                     point(-3, -4), point(3, -4)]
    current = hull([sphere_points[i] for i in (0, 2, 4)])
    decomposition = [current]
    for index in (1, 3, 5):
        current, new_pieces = visible_update(current, sphere_points[index])
        decomposition.extend(new_pieces)
    require(len(current) == len(sphere_points), "all chosen points are final extremes")
    for a, b in combinations(decomposition, 2):
        require(disjoint_interiors(a, b), "entire decomposition interiors disjoint")
    cases["extreme_vertex_hexagon_strict"] = check_deficit(
        decomposition, Q(25), polygon_integrals(current))
    cases["extreme_vertex_hexagon_strict"]["retained_pair_bound"] = check_retained_pair(
        decomposition[0], decomposition[1], polygon_integrals(current), Q(25))

    # In 2D three collinear distinct points cannot all be extreme in one body.
    # This is an auxiliary boundary case for the finite shell identity only.
    auxiliary_square = [point(0, 0), point(2, 0), point(2, 2), point(0, 2)]
    auxiliary, pieces = visible_update(auxiliary_square, point(3, 2),
                                        expect_coplanar=True)
    require(len(pieces) == 1, "coplanar facet contributes no full-dimensional simplex")
    cases["auxiliary_coplanar_visible_update"] = {
        "area": str(polygon_integrals(auxiliary)[0]),
        "new_simplices": len(pieces), "scope": "finite shell identity only"}

    # n+1 rational hypercube vertices, all of squared norm n; det=2**n.
    # The resulting simplex is generally nonregular and has nonzero centroid.
    for n in range(1, 7):
        base = tuple(Q(1) for _ in range(n))
        vertices = [base] + [tuple(Q(-1 if i == j else 1) for i in range(n))
                             for j in range(n)]
        cases[f"sphere_simplex_dimension_{n}"] = check_deficit(
            [vertices], Q(n), equality=True)
        require(simplex_integrals(vertices)[0] == Q(2**n, factorial(n)),
                "hypercube-corner simplex volume")
        # A simplex in a positive orthant with unequal vertex norms.
        unequal = [base] + [tuple(Q(2 if i == j else 1) for i in range(n))
                            for j in range(n)]
        cases[f"unequal_norm_simplex_dimension_{n}"] = check_deficit(
            [unequal], Q(n))

    report = {"status": "passed", "arithmetic": "exact rational (fractions.Fraction)",
              "checks": CHECKS, "cases": cases,
              "limitations": ["Finite checks do not prove the countable decomposition.",
                              "Finite checks do not prove the universal equality theorem.",
                              "No claim of mathematical priority is checked by this script."]}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
