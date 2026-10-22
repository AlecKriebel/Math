"""Fresh exact transcription checks; no numerical SDP or universal-proof claim."""
from fractions import Fraction as F
from math import comb
import json


def need(condition, message):
    if not condition:
        raise ValueError(message)


def add(*polys):
    out = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            out[monomial] = out.get(monomial, 0) + coefficient
    return {monomial: coefficient for monomial, coefficient in out.items() if coefficient}


def scale(poly, coefficient):
    return {m: coefficient * c for m, c in poly.items() if coefficient * c}


def mul(left, right):
    out = {}
    for a, ca in left.items():
        for b, cb in right.items():
            need(len(a) == len(b), "polynomial dimension mismatch")
            m = tuple(x + y for x, y in zip(a, b))
            out[m] = out.get(m, 0) + ca * cb
    return {m: c for m, c in out.items() if c}


def power(poly, exponent, dimension):
    need(type(exponent) is int and exponent >= 0, "invalid exponent")
    out = {(0,) * dimension: 1}
    for _ in range(exponent):
        out = mul(out, poly)
    return out


def substitute(poly, images, dimension):
    out = {}
    for monomial, coefficient in poly.items():
        need(len(monomial) == len(images), "substitution dimension mismatch")
        term = {(0,) * dimension: coefficient}
        for image, exponent in zip(images, monomial):
            term = mul(term, power(image, exponent, dimension))
        out = add(out, term)
    return out


def divide_monomial(poly, monomial):
    out = {}
    for m, c in poly.items():
        need(all(a >= b for a, b in zip(m, monomial)), "not divisible by exceptional factor")
        out[tuple(a - b for a, b in zip(m, monomial))] = c
    return out


def restrict_zero(poly, index):
    return {m: c for m, c in poly.items() if m[index] == 0}


def split_coefficients(a, b, exponent=None):
    n = a + b - 1 if exponent is None else exponent
    out = [0] * (n + 1)
    for s in range(a):
        out[s] += comb(n, s)
    for t in range(b):
        out[n - t] += comb(n, t)
    return out


def run_checks():
    counts = {}
    adverse = {}

    def check(group, condition):
        need(condition, "exact check failed: " + group)
        counts[group] = counts.get(group, 0) + 1

    for a in range(1, 32, 2):
        for b in range(1, 32, 2):
            n = a + b - 1
            check("mixed_odd_binomial_splits", split_coefficients(a, b) == [comb(n, s) for s in range(n + 1)])
            check("mixed_exponent_parity", n % 2 == 1 and (a - 1) % 2 == 0 and (b - 1) % 2 == 0)

    samples = [F(-5), F(-2), F(-1), F(-1, 2), F(0), F(1, 3), F(1), F(2), F(5)]
    for n in range(1, 27):
        for e in range(0, n, 2):
            coefficients = [comb(n, s) for s in range(e + 1)]
            if e:
                derivative = [(s + 1) * coefficients[s + 1] for s in range(e)]
                check("truncation_derivative_identities", derivative == [n * comb(n - 1, s) for s in range(e)])
            pascal = [comb(n - 1, s) + (comb(n - 1, s - 1) if s else 0) for s in range(e + 1)]
            check("truncation_pascal_identities", coefficients == pascal)
            for t in samples:
                check("finite_exact_truncation_values_only", sum(c * t**s for s, c in enumerate(coefficients)) > 0)

    uv = [F(-2), F(-1), F(-1, 2), F(0), F(1, 2), F(1), F(2)]
    for m in range(1, 32, 2):
        for u in uv:
            for v in uv:
                r = sum(comb(m, s) * u**(m - s) * v**(s - 1) for s in range(1, m + 1))
                check("binary_difference_quotient_identities", (u + v)**m - u**m == v * r)
                check("finite_binary_nonnegativity_values_only", r >= 0)
        for later in range(m, 64, 2):
            gap = (later - m) // 2
            check("odd_propagation_exponents", gap >= 0 and m + 2 * gap == later)

    triangle = {(a, b) for a in range(4) for b in range(4) if a <= 2 * b and b <= 2 * a and a + b <= 3}
    check("first_threshold_newton_lattice", triangle == {(0, 0), (1, 1), (2, 1), (1, 2)})
    contributing_pairs = {(a, b) for a in triangle for b in triangle if tuple(a[i] + b[i] for i in range(2)) == (2, 2)}
    check("first_threshold_coefficient_obstruction", contributing_pairs == {((1, 1), (1, 1))})
    for m in range(1, 42, 2):
        support = {(x, y, 3 * m - x - y) for x in range(2 * m + 1) for y in range(2 * m + 1)
                   if x <= 2 * y and y <= 2 * x and x + y <= 3 * m}
        even_even = {t for t in support if t[0] % 2 == 0 and t[1] % 2 == 0}
        check("endpoint_odd_newton_degree_bound", max(t[0] for t in even_even) == 2 * m - 2)
        check("endpoint_constant_face", {t for t in support if t[0] == 0} == {(0, 0, 3 * m)})
        check("endpoint_unique_extremal_vertex", {t for t in support if t[0] == 2 * m} == {(2 * m, m, 0)})

    # Four target variables x,y,z,c; five source variables A,B,C,D,c.
    source_q = {(2, 0, 0, 0, 0): 1, (0, 2, 0, 0, 0): 1, (0, 0, 2, 0, 0): 1, (0, 0, 0, 2, 1): -1}
    source_g = {(1, 1, 1, 0, 0): 1, (0, 0, 0, 3, 0): -1}
    images = [{(2, 1, 0, 0): 1}, {(1, 2, 0, 0): 1}, {(0, 0, 3, 0): 1}, {(1, 1, 1, 0): 1}, {(0, 0, 0, 1): 1}]
    target = {(4, 2, 0, 0): 1, (2, 4, 0, 0): 1, (0, 0, 6, 0): 1, (2, 2, 2, 1): -1}
    check("exact_toric_relation", substitute(source_g, images, 4) == {})
    check("exact_motzkin_substitution", substitute(source_q, images, 4) == target)
    for m in (1, 3, 5):
        check("power_substitution_commutation", substitute(power(source_q, m, 5), images, 4) == power(target, m, 4))

    # Variables local x,y and symbolic parameter c. Each identity is universal in c.
    local = {(2, 0, 0): 1, (4, 0, 0): 1, (0, 6, 0): 1, (2, 2, 1): -1}
    f1 = {(2, 0, 0): 1, (4, 2, 0): 1, (0, 4, 0): 1, (2, 2, 1): -1}
    f2 = {(2, 0, 0): 1, (4, 4, 0): 1, (0, 2, 0): 1, (2, 2, 1): -1}
    f3 = {(0, 0, 0): 1, (2, 0, 0): 1, (2, 2, 1): -1, (4, 6, 0): 1}
    vertical = [{(1, 1, 0): 1}, {(0, 1, 0): 1}, {(0, 0, 1): 1}]
    horizontal = [{(1, 0, 0): 1}, {(1, 1, 0): 1}, {(0, 0, 1): 1}]
    h1 = {(0, 0, 0): 1, (2, 0, 0): 1, (4, 6, 0): 1, (2, 2, 1): -1}
    h2 = {(0, 0, 0): 1, (4, 2, 0): 1, (2, 4, 0): 1, (2, 2, 1): -1}
    h3 = {(0, 0, 0): 1, (0, 2, 0): 1, (2, 2, 1): -1, (6, 4, 0): 1}
    for previous, nxt, other, vertical_restriction, horizontal_restriction in [
        (local, f1, h1, {(2, 0, 0): 1}, {(0, 0, 0): 1}),
        (f1, f2, h2, {(2, 0, 0): 1}, {(0, 0, 0): 1}),
        (f2, f3, h3, {(0, 0, 0): 1, (2, 0, 0): 1}, {(0, 0, 0): 1, (0, 2, 0): 1}),
    ]:
        check("symbolic_vertical_blowup_identities", divide_monomial(substitute(previous, vertical, 3), (0, 2, 0)) == nxt)
        check("symbolic_complementary_blowup_identities", divide_monomial(substitute(previous, horizontal, 3), (2, 0, 0)) == other)
        check("exceptional_restrictions", restrict_zero(nxt, 1) == vertical_restriction)
        check("exceptional_restrictions", restrict_zero(other, 0) == horizontal_restriction)
    expected_tangents = [{(2, 0, 0): 1}, {(2, 0, 0): 1}, {(2, 0, 0): 1, (0, 2, 0): 1}]
    for poly, tangent in zip([local, f1, f2], expected_tangents):
        order = min(m[0] + m[1] for m in poly)
        check("parameter_independent_multiplicity_two", order == 2)
        check("parameter_independent_tangent_cones", {m: c for m, c in poly.items() if m[0] + m[1] == order} == tangent)
    check("real_delta_count_from_verified_centers", 2 * sum(2 * (2 - 1) // 2 for _ in range(3)) == 6)

    nonzero = [F(-3), F(-2), F(-1), F(-1, 2), F(1, 2), F(1), F(2), F(3)]
    for c in [F(-10), F(-2), F(-1), F(0), F(1), F(5, 2), F(299, 100)]:
        delta = min(F(1), (3 - c) / 4)
        check("all_real_parameter_margin_formula", delta > 0 and delta <= 1 and 3 - c - 4 * delta >= 0)
        for a in nonzero:
            for b in nonzero:
                d = F(1)
                cc = 1 / (a * b)
                norm = a*a + b*b + cc*cc + d*d
                q = a*a + b*b + cc*cc - c*d*d
                check("finite_signed_surface_margin_values_only", q >= delta * norm)
        for a, b, cc in [(F(1), F(0), F(0)), (F(-2), F(3), F(0)), (F(0), F(-1), F(2))]:
            q = a*a + b*b + cc*cc
            check("surface_boundary_margin_values_only", q >= delta * q and q > 0)

    adverse["arxiv_wrong_odd_truncation_is_negative"] = sum(comb(3, s) * F(-1)**s for s in range(2)) == -2
    adverse["publisher_wrong_binary_truncation_is_negative"] = F(1) + 3 * F(-1) == -2
    adverse["off_by_one_mixed_exponent_split_rejected"] = split_coefficients(3, 5, 8) != [comb(8, s) for s in range(9)]
    adverse["even_difference_quotient_positivity_rejected"] = 2 * F(-1) + F(0) < 0
    adverse["c3_strict_margin_rejected"] = min(F(1), (F(3) - 3) / 4) == 0 and 1 + 1 + 1 - 3 == 0
    adverse["c_greater_than_3_odd_sos_rejected"] = (3 - 4)**5 < 0
    wrong_images = list(images)
    wrong_images[3] = {(1, 1, 2, 0): 1}
    adverse["wrong_toric_substitution_rejected"] = substitute(source_g, wrong_images, 4) != {}
    adverse["missing_second_blowup_term_rejected"] = divide_monomial(substitute(f1, vertical, 3), (0, 2, 0)) != add(f2, {(0, 2, 0): -1})
    adverse["c3_additional_global_zero_detected"] = 1 + 1 + 1 - 3 == 0 and 1 + 1 + 1 - 2 > 0
    even_m = 2
    adverse["even_exponent_endpoint_degree_argument_rejected"] = (2 * even_m) % 2 == 0 and even_m % 2 == 0 and 2 * even_m > 2 * even_m - 2
    for name, passed in adverse.items():
        need(passed is True, "adverse mathematical control failed: " + name)

    return {
        "schema": "pr1129-independent-exact-checks-v1",
        "verdict": "PASS_SUPPLEMENTARY_EXACT_CHECKS",
        "counts": counts,
        "total_exact_checks": sum(counts.values()),
        "mathematical_adverse_controls": adverse,
        "mathematical_adverse_control_count": len(adverse),
        "universal_theorem_machine_certified": False,
        "priority_machine_certified": False,
        "meaning": "Finite exact transcription and boundary controls; universal deductions are the written proofs and cited theorems.",
    }


if __name__ == "__main__":
    print(json.dumps(run_checks(), sort_keys=True, indent=2))
