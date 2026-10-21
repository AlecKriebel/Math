#!/usr/bin/env python3
"""Independent Cartesian billiard and actual-outer-side audit of PR 210.

No submitted program is imported or executed. No Jacobi function is used.
Default output is JSON on stdout; --output writes the same deterministic JSON.
All floating arithmetic is uncertified arbitrary precision, not interval arithmetic.
Exact SymPy identities and exact algebraic triangles are labeled separately.
Run with the audit-specified interpreter and -B. Only an explicit output file is written.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path

import mpmath as mp
import sympy as sp


def add(u, v):
    return (u[0] + v[0], u[1] + v[1])


def sub(u, v):
    return (u[0] - v[0], u[1] - v[1])


def mul(t, u):
    return (t * u[0], t * u[1])


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1]


def det(u, v):
    return u[0] * v[1] - u[1] * v[0]


def norm(u):
    return mp.sqrt(dot(u, u))


def unit(u):
    return mul(1 / norm(u), u)


def area(points):
    return sum(det(points[j], points[(j + 1) % len(points)])
               for j in range(len(points))) / 2


def reflect(d, p, aa, bb):
    n = (p[0] / aa, p[1] / bb)
    return sub(d, mul(2 * dot(d, n) / dot(n, n), n))


def next_impact(p, d, aa, bb):
    # The nonzero root of (p+t*d)^T diag(1/aa,1/bb)(p+t*d)=1.
    t = -2 * (p[0] * d[0] / aa + p[1] * d[1] / bb) / (
        d[0] ** 2 / aa + d[1] ** 2 / bb)
    if t <= 0:
        raise ArithmeticError("Physical ray did not enter the ellipse")
    return add(p, mul(t, d))


def trace(p, d, aa, bb, count):
    points = [p]
    for _ in range(count):
        p = next_impact(p, d, aa, bb)
        points.append(p)
        d = reflect(d, p, aa, bb)
    return points


def angle_lift(points, a, b):
    total = mp.mpf(0)
    for p, q in zip(points, points[1:]):
        pp, qq = (p[0] / a, p[1] / b), (q[0] / a, q[1] / b)
        t = mp.atan2(det(pp, qq), dot(pp, qq))
        if t < 0:
            t += 2 * mp.pi
        total += t
    return total


def closure_caustic(a, b, n, turn, iterations=455):
    """Shoot from the top and bisect physical lifted winding, not elliptic phase.

    The confocal caustic is x^2/(a^2-lambda)+y^2/(b^2-lambda)=1.
    Its tangent from (0,b) has direction (-sqrt(a^2-lambda),-sqrt(lambda)).
    """
    aa, bb = a * a, b * b
    target = 2 * mp.pi * turn
    lo, hi = mp.mpf(0), bb
    for _ in range(iterations):
        lam = (lo + hi) / 2
        d = (-mp.sqrt(aa - lam) / a, -mp.sqrt(lam) / a)
        value = angle_lift(trace((mp.mpf(0), b), d, aa, bb, n), a, b)
        if value < target:
            lo = lam
        else:
            hi = lam
    return (lo + hi) / 2


def caustic_tangent_direction(p, aa, bb, lam):
    # Pull the caustic back to the unit circle, obtain both tangent contacts,
    # and choose the one whose chord advances counterclockwise.
    alpha, beta = mp.sqrt(aa - lam), mp.sqrt(bb - lam)
    z = (p[0] / alpha, p[1] / beta)
    rr = dot(z, z)
    h = mp.sqrt(rr - 1)
    for sign in (1, -1):
        contact = ((z[0] - sign * h * z[1]) / rr,
                   (z[1] + sign * h * z[0]) / rr)
        d = sub((alpha * contact[0], beta * contact[1]), p)
        if det(p, d) > 0:
            return unit(d)
    raise ArithmeticError("No forward caustic tangent")


def intersect_tangents(p, q, aa, bb):
    n, m = (p[0] / aa, p[1] / bb), (q[0] / aa, q[1] / bb)
    den = det(n, m)
    if den == 0:
        raise ArithmeticError("Parallel adjacent tangent lines")
    return ((m[1] - n[1]) / den, (n[0] - m[0]) / den)


def actual_outer_pedals(points, foci, aa, bb):
    """Build actual outer vertices, then use their literal side directions."""
    n = len(points)
    outer = [intersect_tangents(points[j], points[(j + 1) % n], aa, bb)
             for j in range(n)]
    pedals = []
    for focus in foci:
        feet = []
        for j in range(n):
            base = outer[(j - 1) % n]
            d = sub(outer[j], base)
            feet.append(add(base, mul(dot(sub(focus, base), d) / dot(d, d), d)))
        pedals.append(feet)
    return outer, pedals


def tangent_pedals(points, foci, aa, bb):
    output = []
    for f in foci:
        feet = []
        for p in points:
            n = (p[0] / aa, p[1] / bb)
            feet.append(add(f, mul((1 - dot(n, f)) / dot(n, n), n)))
        output.append(feet)
    return output


def sfloat(x):
    return mp.nstr(x, 48)


def maxabs(values):
    return max((abs(v) for v in values), default=mp.mpf(0))


def validate_orbit(points_with_closure, a, b, lam, turn):
    aa, bb, n = a * a, b * b, len(points_with_closure) - 1
    points = points_with_closure[:-1]
    c = mp.sqrt(aa - bb)
    foci = [(c, mp.mpf(0)), (-c, mp.mpf(0))]
    outer, pedals = actual_outer_pedals(points, foci, aa, bb)
    direct = tangent_pedals(points, foci, aa, bb)
    boundary = maxabs(p[0] ** 2 / aa + p[1] ** 2 / bb - 1 for p in points)
    tangent_errors, reflection_errors, side_errors, projection_errors = [], [], [], []
    minimum_adjacent_determinant = mp.inf
    for j, p in enumerate(points):
        q = points[(j + 1) % n]
        d = sub(q, p)
        # l dot X = h is the billiard CHORD, used only to check its caustic.
        ell = (d[1], -d[0])
        h = dot(ell, p)
        tangent_errors.append((h * h - (aa - lam) * ell[0] ** 2
                               - (bb - lam) * ell[1] ** 2) / (aa * dot(ell, ell)))
        incoming = unit(sub(p, points[(j - 1) % n]))
        outgoing = unit(d)
        reflection_errors.append(norm(sub(outgoing, reflect(incoming, p, aa, bb))))
        normal = (p[0] / aa, p[1] / bb)
        side_errors.extend([dot(normal, outer[j]) - 1,
                            dot(normal, outer[(j - 1) % n]) - 1])
        m = (q[0] / aa, q[1] / bb)
        minimum_adjacent_determinant = min(minimum_adjacent_determinant,
                                           abs(det(normal, m)) * a * b)
        for which in (0, 1):
            projection_errors.append(norm(sub(pedals[which][j], direct[which][j])) / a)
    circle = maxabs((dot(q, q) - aa) / aa for feet in pedals for q in feet)
    separation = min(norm(sub(points[i], points[j])) / a
                     for i in range(n) for j in range(i))
    values = [area(feet) for feet in pedals]
    winding = angle_lift(points_with_closure, a, b) / (2 * mp.pi)
    return {
        "B_plus": values[0], "B_minus": values[1], "product": values[0] * values[1],
        "closure": norm(sub(points_with_closure[-1], points[0])) / a,
        "boundary": boundary, "caustic_tangency": maxabs(tangent_errors),
        "reflection": maxabs(reflection_errors), "outer_side": maxabs(side_errors),
        "independent_projection_agreement": maxabs(projection_errors),
        "auxiliary_circle": circle, "winding_error": abs(winding - turn),
        "min_pair_separation": separation,
        "min_adjacent_tangent_det": minimum_adjacent_determinant,
        "points": points, "foci": foci, "outer": outer, "pedals": pedals,
    }


def isometry_control(v, a, b):
    # A nontrivial rotation followed by translation. Project again on the
    # transformed actual outer sides; do not use a tangent formula afterward.
    co, si, shift = mp.mpf(3) / 5, mp.mpf(4) / 5, (mp.mpf(7) / 3, -mp.mpf(5) / 7)
    def trans(p):
        return add((co * p[0] - si * p[1], si * p[0] + co * p[1]), shift)
    outer = [trans(p) for p in v["outer"]]
    values = []
    for f in map(trans, v["foci"]):
        feet = []
        for j in range(len(outer)):
            base = outer[(j - 1) % len(outer)]
            d = sub(outer[j], base)
            feet.append(add(base, mul(dot(sub(f, base), d) / dot(d, d), d)))
        values.append(area(feet))
    return abs(values[0] * values[1] - v["product"]) / max(a ** 4, abs(v["product"]))


def numeric_case(a_text, n, turn, label, count=9):
    a, b = mp.mpf(a_text), mp.mpf(1)
    aa, bb = a * a, b * b
    if math.gcd(n, turn) != 1:
        raise ValueError("Theorem test must be primitive")
    lam = closure_caustic(a, b, n, turn)
    # Fixed deterministic phases cover both axes, asymmetric vertices and
    # points very close to an axis. No sampled phase is an elliptic phase.
    phases = [mp.mpf(0), mp.mpf("0.000000000000000001"), mp.mpf("0.13"),
              mp.mpf("0.47"), mp.mpf("0.91"), mp.mpf("1.4"), mp.pi / 2,
              mp.mpf("2.17"), mp.mpf("3.81")][:count]
    records, raw = [], []
    for phase in phases:
        p = (a * mp.cos(phase), b * mp.sin(phase))
        d = caustic_tangent_direction(p, aa, bb, lam)
        v = validate_orbit(trace(p, d, aa, bb, n), a, b, lam, turn)
        raw.append(v)
        record = {key: sfloat(value) for key, value in v.items()
                  if key not in ("points", "foci", "outer", "pedals")}
        record["eccentric_angle"] = sfloat(phase)
        records.append(record)
    products = [v["product"] for v in raw]
    scale = max(a ** 4, maxabs(products))
    product_spread = (max(products) - min(products)) / scale
    focus_equality = maxabs(v["B_plus"] - v["B_minus"] for v in raw) / (a * a)
    plus_spread = (max(v["B_plus"] for v in raw) - min(v["B_plus"] for v in raw)) / (a * a)
    keys = ["closure", "boundary", "caustic_tangency", "reflection", "outer_side",
            "independent_projection_agreement", "auxiliary_circle", "winding_error"]
    maxima = {key: maxabs(v[key] for v in raw) for key in keys}
    # Focus pairing by central symmetry is checked using newly traced orbits.
    p = mul(-1, raw[3 if len(raw) > 3 else 0]["points"][0])
    d = caustic_tangent_direction(p, aa, bb, lam)
    paired = validate_orbit(trace(p, d, aa, bb, n), a, b, lam, turn)
    original = raw[3 if len(raw) > 3 else 0]
    pairing_error = abs(paired["B_plus"] - original["B_minus"]) / (a * a)
    reversed_values = [area(list(reversed(feet))) for feet in original["pedals"]]
    reversal_error = maxabs(reversed_values[i] + original["B_plus" if i == 0 else "B_minus"]
                            for i in (0, 1)) / (a * a)
    cyclic_error = maxabs(area(feet[2:] + feet[:2]) - area(feet)
                         for feet in original["pedals"]) / (a * a)
    sf = mp.mpf(7) / 3
    _, scaled = actual_outer_pedals([mul(sf, p) for p in original["points"]],
                                   [mul(sf, f) for f in original["foci"]],
                                   aa * sf * sf, bb * sf * sf)
    scaling_error = abs(area(scaled[0]) * area(scaled[1]) / sf ** 4 - original["product"]) / scale
    isometry_error = isometry_control(original, a, b)
    tol = mp.mpf("1e-48")
    passed = all(value < tol for value in maxima.values())
    passed = passed and max(pairing_error, reversal_error, cyclic_error, scaling_error,
                            isometry_error) < tol
    passed = passed and min(v["min_pair_separation"] for v in raw) > mp.mpf("1e-40")
    if n % 2:
        passed = passed and product_spread < tol
    else:
        passed = passed and focus_equality < tol
    return {
        "label": label, "a": str(a_text), "b": "1", "N": n, "turn": turn,
        "lambda": sfloat(lam), "caustic_beta_squared": sfloat(bb - lam),
        "strictly_nested_elliptic": bool(0 < lam < bb),
        "phase_count": len(phases), "max_errors": {k: sfloat(v) for k, v in maxima.items()},
        "product_spread_normalized": sfloat(product_spread),
        "plus_area_spread_normalized": sfloat(plus_spread),
        "focus_area_difference_normalized": sfloat(focus_equality),
        "focus_pairing_error": sfloat(pairing_error), "orientation_reversal_error": sfloat(reversal_error),
        "cyclic_shift_error": sfloat(cyclic_error), "scaling_degree_four_error": sfloat(scaling_error),
        "isometry_error": sfloat(isometry_error), "passed": bool(passed), "phases": records,
    }


def exact_geometry():
    simp = sp.simplify
    def ss(u, v):
        return tuple(simp(x - y) for x, y in zip(u, v))
    def smul(t, u):
        return tuple(simp(t * x) for x in u)
    a, c, u = sp.symbols("a c u", positive=True)
    b = sp.sqrt(a * a - c * c)
    cs, sn = (1 - u * u) / (1 + u * u), 2 * u / (1 + u * u)
    normal = (cs / a, sn / b)
    q = add((c, 0), smul((1 - c * normal[0]) / dot(normal, normal), normal))
    expected = (a * (c + a * cs) / (a + c * cs), a * b * sn / (a + c * cs))
    foot_identity = ss(q, expected)
    circle_identity = simp(dot(expected, expected) - a * a)
    # The rational circle coordinate is d*u with d=b/(a+c).
    d = b / (a + c)
    circle_parameter = (a * (1 - d * d * u * u) / (1 + d * d * u * u),
                        2 * a * d * u / (1 + d * d * u * u))
    rational_identity = ss(expected, circle_parameter)
    # N=3 has ONE regular vertex shared by the two singly singular incident
    # edges. Check that coincidence literally instead of assuming N>=5.
    eps = sp.symbols("eps", nonzero=True)
    rx, ry, ax, ay, bx, by, cx, cy = sp.symbols("rx ry ax ay bx by cx cy")
    residue, finite_a, finite_b, regular = (rx, ry), (ax, ay), (bx, by), (cx, cy)
    q0 = add(smul(1 / eps, residue), finite_a)
    q1 = add(smul(-1 / eps, residue), finite_b)
    three_area = sp.expand((det(q0, q1) + det(q1, regular) + det(regular, q0)) / 2)
    n3_double = simp(sp.expand(three_area * eps * eps).subs(eps, 0))
    n3_simple = simp(sp.expand(three_area).coeff(eps, -1)
                     - det(residue, ss(add(finite_a, finite_b), smul(2, regular))) / 2)
    sx, sy = sp.symbols("sx sy")
    noncollinear_double = simp(sp.expand(det(add(smul(1 / eps, residue), finite_a),
                                             add(smul(1 / eps, (sx, sy)), finite_b)))
                               .coeff(eps, -2) - (rx * sy - ry * sx))
    aa, bb = sp.Integer(21), sp.Integer(16)
    a, b, c, lam = sp.sqrt(aa), sp.sqrt(bb), sp.sqrt(5), sp.Rational(336, 25)
    triangles = [
        [(a, sp.Integer(0)), (-3 * a / 5, sp.Rational(16, 5)),
         (-3 * a / 5, -sp.Rational(16, 5))],
        [(sp.Integer(0), b), (-sp.Rational(21, 5), -sp.Rational(8, 5)),
         (sp.Rational(21, 5), -sp.Rational(8, 5))],
    ]
    results = []
    for points in triangles:
        n = len(points)
        outer = [tuple(simp(x) for x in intersect_tangents(points[j], points[(j + 1) % n], aa, bb))
                 for j in range(n)]
        feet_list = []
        for focus in [(c, 0), (-c, 0)]:
            feet = []
            for j in range(n):
                base = outer[(j - 1) % n]
                direction = ss(outer[j], base)
                foot = add(base, smul(simp(dot(ss(focus, base), direction) / dot(direction, direction)), direction))
                feet.append(tuple(simp(x) for x in foot))
            feet_list.append(feet)
        checks = []
        for j, p in enumerate(points):
            pp, qq = points[(j - 1) % n], points[(j + 1) % n]
            incoming, outgoing = ss(p, pp), ss(qq, p)
            incoming = smul(1 / sp.sqrt(simp(dot(incoming, incoming))), incoming)
            outgoing = smul(1 / sp.sqrt(simp(dot(outgoing, outgoing))), outgoing)
            normal = (p[0] / aa, p[1] / bb)
            ref = ss(incoming, smul(2 * simp(dot(incoming, normal) / dot(normal, normal)), normal))
            checks.extend(ss(ref, outgoing))
            chord = ss(qq, p)
            ell = (chord[1], -chord[0])
            checks.append(simp(dot(ell, p) ** 2 - (aa - lam) * ell[0] ** 2 - (bb - lam) * ell[1] ** 2))
            checks.append(simp(p[0] ** 2 / aa + p[1] ** 2 / bb - 1))
            checks.extend(simp(dot(normal, endpoint) - 1)
                          for endpoint in (outer[(j - 1) % n], outer[j]))
            for feet in feet_list:
                checks.append(simp(dot(feet[j], feet[j]) - aa))
        values = [simp(area(feet)) for feet in feet_list]
        results.append({"vertices": [[str(x) for x in p] for p in points],
                        "B_plus": str(values[0]), "B_minus": str(values[1]),
                        "product": str(simp(values[0] * values[1])),
                        "all_exact_boundary_reflection_tangency_outer_side_circle_checks_zero": all(v == 0 for v in checks)})
    passed = all(v == 0 for v in foot_identity + rational_identity
                 + (circle_identity, n3_double, n3_simple, noncollinear_double))
    passed = passed and all(r["all_exact_boundary_reflection_tangency_outer_side_circle_checks_zero"] for r in results)
    passed = passed and all(r["product"] == "12544/25" for r in results)
    return {"symbolic_projection_identity": list(map(str, foot_identity)),
            "symbolic_auxiliary_circle_identity": str(circle_identity),
            "symbolic_rational_circle_parameter_identity": list(map(str, rational_identity)),
            "N3_shared_regular_neighbor_double_pole_coefficient": str(n3_double),
            "N3_simple_coefficient_identity_residual": str(n3_simple),
            "N3_simple_coefficient_formula": "det(R,A+B-2C)/2",
            "noncollinear_residue_double_coefficient_identity_residual": str(noncollinear_double),
            "triangle_a_squared": "21", "triangle_b_squared": "16", "triangle_lambda": str(lam),
            "triangle_caustic_alpha_squared": str(aa - lam),
            "triangle_caustic_beta_squared": str(bb - lam),
            "two_exact_distinct_family_triangles": results, "passed": bool(passed)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--quick", action="store_true", help="Six primary cases instead of the full boundary grid")
    args = parser.parse_args()
    mp.mp.dps = 170
    exact = exact_geometry()
    specs = [
        ("2", 3, 1, "triangle"), ("2", 5, 1, "convex_pentagon"),
        ("2", 5, 2, "pentagram"), ("2", 7, 3, "seven_star"),
        ("2", 4, 1, "even_control_quadrilateral"), ("2", 8, 3, "even_control_star"),
    ]
    if not args.quick:
        specs += [
            ("1.000000000001", 3, 1, "near_circle_triangle"),
            ("1.000000000001", 5, 2, "near_circle_pentagram"),
            ("1.1", 9, 4, "near_circle_nine_star"),
            ("3", 9, 2, "noncoprime_looking_but_primitive_nine_star"),
            ("10", 3, 1, "eccentric_triangle"), ("10", 5, 1, "eccentric_convex_pentagon"),
            ("10", 5, 2, "eccentric_pentagram"), ("10", 7, 3, "eccentric_seven_star"),
            ("1000", 3, 1, "very_eccentric_triangle"),
            ("1000", 5, 2, "very_eccentric_pentagram"),
            ("1000", 11, 5, "very_eccentric_near_collapsed_caustic_star"),
            ("2", 101, 1, "near_boundary_caustic_long_primitive_orbit"),
            ("2", 17, 8, "near_half_turn_star"),
            ("1", 5, 2, "circle_limit_control_outside_strict_ellipse_domain"),
            ("10", 6, 1, "eccentric_even_control"), ("3", 10, 3, "even_control_primitive_star"),
        ]
    cases = [numeric_case(a, n, turn, label, count=5 if n > 30 else 9)
             for a, n, turn, label in specs]
    even_controls = [c for c in cases if c["N"] % 2 == 0]
    # A working negative control must vary materially, not merely roundoff.
    even_nonconstancy_detected = all(mp.mpf(c["product_spread_normalized"]) > mp.mpf("1e-8")
                                    for c in even_controls)
    result = {"program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "method": "Cartesian reflection, physical closure bisection, actual outer intersections, Euclidean line projection; no Jacobi functions",
              "floating_evidence_is_uncertified": True, "mpmath_dps": mp.mp.dps,
              "mpmath_version": mp.__version__, "sympy_version": sp.__version__,
              "exact": exact, "case_count": len(cases), "cases": cases,
              "even_product_nonconstancy_detected_in_every_even_control": even_nonconstancy_detected,
              "all_passed": bool(exact["passed"] and all(c["passed"] for c in cases) and even_nonconstancy_detected)}
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")
    if not result["all_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
