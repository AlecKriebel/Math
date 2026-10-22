#!/usr/bin/env python3
"""Exact configuration controls, independently written for the PR293 audit.

Uses point bases for lines, truncated polynomial jets in complementary vectors,
and forward elimination. No point evaluation or derivative membership shortcut.
Requires Python 3.8+ and only its standard library.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations, product
from math import comb
from pathlib import Path
import argparse
import hashlib
import json
import time

ROOT = Path(__file__).resolve().parent
CHECKS = Counter()


def check(test, label):
    if not test:
        raise AssertionError(label)
    CHECKS[label] += 1


@lru_cache(None)
def exponents(degree, variables=4):
    if variables == 1:
        return ((degree,),)
    return tuple((j,) + rest for j in range(degree + 1)
                 for rest in exponents(degree - j, variables - 1))


def echelon(rows, p, reduced=False):
    basis = {}
    for incoming in rows:
        row = [v % p for v in incoming]
        for pivot in sorted(basis):
            factor = row[pivot]
            if factor:
                row = [(x - factor * y) % p for x, y in zip(row, basis[pivot])]
        pivot = next((i for i, v in enumerate(row) if v), None)
        if pivot is not None:
            inv = pow(row[pivot], -1, p)
            basis[pivot] = [(v * inv) % p for v in row]
    if reduced:
        for pivot in sorted(basis, reverse=True):
            for earlier in sorted(basis):
                if earlier >= pivot:
                    break
                factor = basis[earlier][pivot]
                if factor:
                    basis[earlier] = [(x - factor * y) % p
                                      for x, y in zip(basis[earlier], basis[pivot])]
    return tuple(tuple(basis[i]) for i in sorted(basis))


def rank(rows, p):
    return len(echelon(rows, p))


def bit_rank(rows):
    pivots = {}
    for x in rows:
        while x:
            pivot = x.bit_length() - 1
            if pivot in pivots:
                x ^= pivots[pivot]
            else:
                pivots[pivot] = x
                break
    return len(pivots)


def nullspace(rows, p, width=4):
    rr = echelon(rows, p, reduced=True)
    pivots = [next(i for i, x in enumerate(row) if x) for row in rr]
    out = []
    for free in range(width):
        if free not in pivots:
            v = [0] * width
            v[free] = 1
            for pivot, row in zip(pivots, rr):
                v[pivot] = -row[free] % p
            out.append(tuple(v))
    return tuple(out)


def line_basis(vectors, p):
    rr = echelon(vectors, p, reduced=True)
    check(len(rr) == 2, "valid_line_point_bases")
    return rr


def plane_line(a, b, p):
    return line_basis(nullspace((a, b), p), p)


def pair_arrangement(planes, p):
    return tuple(sorted({plane_line(a, b, p) for a, b in combinations(planes, 2)}))


def polynomial_multiply(f, g, p, jet_order=None):
    out = {}
    for ef, cf in f.items():
        for eg, cg in g.items():
            exponent = tuple(x + y for x, y in zip(ef, eg))
            if jet_order is not None and exponent[2] + exponent[3] >= jet_order:
                continue
            out[exponent] = (out.get(exponent, 0) + cf * cg) % p
    return {e: c for e, c in out.items() if c}


@lru_cache(None)
def jets(line, degree, multiplicity, p):
    """Coefficient matrix of F(s*u+t*v+r*w+q*z) mod (r,q)^m."""
    vectors = list(line)
    for j in range(4):
        v = tuple(int(i == j) for i in range(4))
        if rank(vectors + [v], p) > len(vectors):
            vectors.append(v)
        if len(vectors) == 4:
            break
    check(rank(vectors, p) == 4, "complement_basis_invertible")
    powers = []
    for coordinate in range(4):
        f = {tuple(int(i == j) for i in range(4)): vectors[j][coordinate]
             for j in range(4) if vectors[j][coordinate]}
        current = {(0, 0, 0, 0): 1}
        pp = [current]
        for _ in range(degree):
            current = polynomial_multiply(current, f, p, multiplicity)
            pp.append(current)
        powers.append(pp)
    targets = [e for e in exponents(degree) if e[2] + e[3] < multiplicity]
    expansions = []
    for exponent in exponents(degree):
        current = {(0, 0, 0, 0): 1}
        for variable, power in enumerate(exponent):
            current = polynomial_multiply(current, powers[variable][power], p, multiplicity)
        expansions.append(current)
    return tuple(tuple(poly.get(target, 0) for poly in expansions) for target in targets)


@lru_cache(None)
def bit_jets(line, degree, multiplicity):
    return tuple(sum(c << j for j, c in enumerate(row))
                 for row in jets(line, degree, multiplicity, 2))


def ideal_dimension(lines, degree, multiplicity, p):
    if p == 2:
        conditions = (row for line in lines for row in bit_jets(line, degree, multiplicity))
        codim = bit_rank(conditions)
    else:
        conditions = (row for line in lines for row in jets(line, degree, multiplicity, p))
        codim = rank(conditions, p)
    return comb(degree + 3, 3) - codim


def initial_degree(lines, multiplicity, p, bound=10):
    for degree in range(1, bound + 1):
        if ideal_dimension(lines, degree, multiplicity, p):
            return degree
    raise AssertionError(("insufficient_bound", len(lines), multiplicity, p, bound))


def normalize(v, p):
    a = next(x for x in v if x)
    return tuple(x * pow(a, -1, p) % p for x in v)


def projective_points(p):
    return tuple(sorted({normalize(v, p) for v in product(range(p), repeat=4) if any(v)}))


def all_lines(p):
    return tuple(sorted({echelon((a, b), p, reduced=True)
                         for a, b in combinations(projective_points(p), 2)}))


def coplanar(lines, p):
    return rank([vector for line in lines for vector in line], p) < 4


def recognize_pseudostar(lines, p):
    n = len(lines)
    ds = [d for d in range(3, n + 2) if d * (d - 1) // 2 == n]
    if not ds:
        return None
    d = ds[0]
    candidate_planes = set()
    for left, right in combinations(lines, 2):
        span = echelon(left + right, p, reduced=True)
        if len(span) == 3:
            plane = normalize(nullspace(span, p)[0], p)
            contained = sum(all(sum(x * y for x, y in zip(v, plane)) % p == 0
                                for v in line) for line in lines)
            if contained >= d - 1:
                candidate_planes.add(plane)
    target = set(lines)
    for planes in combinations(sorted(candidate_planes), d):
        if any(rank(triple, p) < 3 for triple in combinations(planes, 3)):
            continue
        if set(pair_arrangement(planes, p)) == target:
            return planes
    return None


def classify(lines, p):
    if coplanar(lines, p):
        return "coplanar"
    if recognize_pseudostar(lines, p) is not None:
        return "pseudostar"
    return "neither"


def exhaustive_f2(maximum_size=6):
    lines = all_lines(2)
    check(len(lines) == 35, "PG3_F2_has_35_lines")
    distribution = Counter()
    classes = Counter()
    representatives = {}
    digest = hashlib.sha256()
    total = 0
    # Cubics contain any four lines: 20 - 4*4 > 0. Quartics contain
    # any six lines: 35 - 6*5 > 0. Squaring bounds the symbolic degree.
    # Thus every reported initial degree has a proved finite cutoff.
    check(1 <= maximum_size <= 6, "valid_exhaustion_size_limit")
    for size in range(1, maximum_size + 1):
        start = time.monotonic()
        for indices in combinations(range(len(lines)), size):
            selected = tuple(lines[i] for i in indices)
            a = initial_degree(selected, 1, 2, 3 if size <= 4 else 4)
            b = initial_degree(selected, 2, 2, 2 * a)
            check(b > a, "strict_symbolic_initial_degree_gap_in_exhaustion")
            category = classify(selected, 2) if b == a + 1 else "negative_gap"
            check(b != a + 1 or category != "neither", "exhaustive_gap_one_classification")
            distribution[(size, a, b)] += 1
            if b == a + 1:
                classes[(size, category)] += 1
            representatives.setdefault((size, a, b, category), list(indices))
            digest.update((json.dumps([indices, a, b, category], separators=(",", ":")) + "\n").encode())
            total += 1
        print(json.dumps({"progress": "F2_exhaustion", "size_finished": size,
                          "seconds": round(time.monotonic() - start, 3),
                          "cumulative_configurations": total}), flush=True)
    check(total == sum(comb(35, r) for r in range(1, maximum_size + 1)), "exhaustion_configuration_count")
    # PG(3,2) has 15 planes, each containing 7 lines. Every set of at
    # least two distinct coplanar lines determines its containing plane.
    expected_positive = {(1, "coplanar"): 35, (2, "coplanar"): 315,
                         (3, "coplanar"): 15 * comb(7, 3), (3, "pseudostar"): 420,
                         (4, "coplanar"): 15 * comb(7, 4),
                         (5, "coplanar"): 15 * comb(7, 5),
                         (6, "coplanar"): 15 * comb(7, 6),
                         # Four points in dual PG(3,2) have no collinear triple
                         # in C(15,4)-35*12=945 cases. Each determines a unique
                         # complete six-line pseudostar.
                         (6, "pseudostar"): comb(15, 4) - 35 * 12}
    expected_positive = {key: value for key, value in expected_positive.items()
                         if key[0] <= maximum_size}
    check(dict(classes) == expected_positive, "independent_finite_geometry_positive_counts")
    return {"field": "F2", "ambient": "PG(3,2)", "maximum_size": maximum_size,
            "line_catalog_point_bases": lines,
            "configuration_count": total,
            "distribution": [{"lines": n, "alpha": a, "alpha_square": b, "count": c}
                             for (n, a, b), c in sorted(distribution.items())],
            "gap_one_classes": [{"lines": n, "class": category, "count": c}
                                for (n, category), c in sorted(classes.items())],
            "state_representatives": [{"lines": n, "alpha": a, "alpha_square": b,
                                       "class": category, "line_indices": indices}
                                      for (n, a, b, category), indices in sorted(representatives.items())],
            "stream_sha256": digest.hexdigest(), "classification_exceptions": []}


def polynomial_product(forms, p):
    poly = {(0, 0, 0, 0): 1}
    for form in forms:
        linear = {tuple(int(i == j) for i in range(4)): c
                  for j, c in enumerate(form) if c}
        poly = polynomial_multiply(poly, linear, p)
    return poly


def evaluate_constraints(poly, lines, multiplicity, p):
    degree = sum(next(iter(poly)))
    coeff = [poly.get(exponent, 0) for exponent in exponents(degree)]
    return all(sum(x * y for x, y in zip(row, coeff)) % p == 0
               for line in lines for row in jets(line, degree, multiplicity, p))


def generator_span_dimension(planes, degree, p):
    d = len(planes)
    if degree < d - 1:
        return 0
    mons = exponents(degree)
    index = {e: i for i, e in enumerate(mons)}
    rows = []
    for omit in range(d):
        generator = polynomial_product(planes[:omit] + planes[omit + 1:], p)
        for multiplier in exponents(degree - d + 1):
            row = [0] * len(mons)
            for e, c in generator.items():
                row[index[tuple(x + y for x, y in zip(e, multiplier))]] = c
            rows.append(row)
    if p == 2:
        return bit_rank(sum(c << i for i, c in enumerate(row)) for row in rows)
    return rank(rows, p)


def choose3(n):
    return comb(n, 3) if n >= 3 else 0


def family_controls():
    basis = tuple(tuple(int(i == j) for i in range(4)) for j in range(4))
    records = []
    tetra_states = Counter()
    hilbert_records = []
    affine_caps = tuple((1,) + xyz for xyz in product((0, 1), repeat=3))
    for p in (2, 3, 5, 7):
        tetra = pair_arrangement(basis, p)
        for size in range(1, 7):
            for subset in combinations(tetra, size):
                a = initial_degree(subset, 1, p, 4)
                b = initial_degree(subset, 2, p, 2 * a)
                category = classify(subset, p)
                check((b == a + 1) == (category != "neither"), "all_tetrahedron_subsets_gap_iff_classified")
                tetra_states[(p, size, a, b, category)] += 1
        # An affine Boolean cube has no three collinear points over these fields.
        check(all(rank(t, p) == 3 for t in combinations(affine_caps, 3)), "eight_plane_no_triple_line_cap")
        families = [
            ("four_plane_point_cone", basis[:3] + ((1, 1, 1, 0),), "positive"),
            ("four_planes_with_triple_line", (basis[0], basis[1], (1, 1, 0, 0), basis[2]), "negative"),
            ("five_planes_with_triple_line", (basis[0], basis[1], (1, 1, 0, 0), basis[2], basis[3]), "negative"),
            ("eight_plane_boolean_cap", affine_caps, "positive"),
        ]
        for name, planes, expectation in families:
            lines = pair_arrangement(planes, p)
            if expectation == "positive":
                d = len(planes)
                check(ideal_dimension(lines, d - 2, 1, p) == 0, "large_pseudostar_no_lower_form")
                check(ideal_dimension(lines, d - 1, 1, p) > 0, "large_pseudostar_initial_form_exists")
                check(ideal_dimension(lines, d - 1, 2, p) == 0, "large_pseudostar_no_lower_double_form")
                check(ideal_dimension(lines, d, 2, p) > 0, "large_pseudostar_double_form_exists")
                a, b = d - 1, d
            else:
                a = initial_degree(lines, 1, p, len(planes))
                b = initial_degree(lines, 2, p, 2 * a)
                check(b != a + 1, "triple_line_arrangements_are_negative_controls")
            records.append({"p": p, "name": name, "lines": len(lines),
                            "alpha": a, "alpha_square": b, "expected": expectation,
                            "planes": planes, "point_bases": lines})
        # The minor ideal really becomes nonradical at a triple line.
        # Here F=x0*x1*(x0+x1)*x2, J has generators of degree 3,
        # x0*x2 belongs to the radical and (x0*x2)^2=x2*(g1-g2) in J.
        bad_planes = (basis[0], basis[1], (1, 1, 0, 0), basis[2])
        bad_lines = pair_arrangement(bad_planes, p)
        radical_witness = polynomial_product((basis[0], basis[2]), p)
        check(evaluate_constraints(radical_witness, bad_lines, 1, p), "triple_line_radical_witness_in_I")
        check(generator_span_dimension(bad_planes, 2, p) == 0,
              "triple_line_radical_witness_not_in_J_by_degree")
        g1 = polynomial_product((basis[0], (1, 1, 0, 0), basis[2]), p)
        g2 = polynomial_product((basis[0], basis[1], basis[2]), p)
        difference = {e: (g1.get(e, 0) - g2.get(e, 0)) % p for e in set(g1) | set(g2)}
        difference = {e: c for e, c in difference.items() if c}
        lhs = polynomial_multiply(radical_witness, radical_witness, p)
        rhs = polynomial_multiply(polynomial_product((basis[2],), p), difference, p)
        check(lhs == rhs, "triple_line_radical_witness_square_in_J_exact_identity")
        for d in range(3, 9):
            planes = affine_caps[:d]
            lines = pair_arrangement(planes, p)
            check(len(lines) == comb(d, 2), "cap_pair_lines_distinct")
            # Degree d+1 tests both generators and their linear syzygies.
            degrees = tuple(sorted({0, d - 2, d - 1, d, d + 1}))
            for degree in degrees:
                dim_i = ideal_dimension(lines, degree, 1, p)
                predicted_i = d * choose3(degree - d + 4) - (d - 1) * choose3(degree - d + 3)
                span_j = generator_span_dimension(planes, degree, p)
                check(dim_i == predicted_i == span_j, "hilbert_burch_and_actual_radical_ideal_components_agree")
                hilbert_records.append({"p": p, "planes": d, "lines": len(lines),
                                        "degree": degree, "ideal_dimension": dim_i,
                                        "generator_span_dimension": span_j,
                                        "hilbert_burch_prediction": predicted_i})
        # All maximal F_p rational lines in one ruling of a smooth quadric.
        ruling = tuple([line_basis(((1, 0, t, 0), (0, 1, 0, t)), p)
                        for t in range(p)] + [line_basis((basis[2], basis[3]), p)])
        a, b = (initial_degree(ruling, m, p, 4) for m in (1, 2))
        check((a, b) == (2, 4), "smooth_quadric_ruling_negative_control")
        records.append({"p": p, "name": "maximal_smooth_quadric_ruling", "lines": len(ruling),
                        "alpha": a, "alpha_square": b, "point_bases": ruling,
                        "geometry": "distinct lines in the same ruling are pairwise skew"})
        # Repeated factor x0^2*x1*x2 with noncoplanar target support.
        inside = tuple(plane_line(basis[0], v, p) for v in
                       (basis[1], basis[2], basis[3]))
        repeated_lines = tuple(sorted(set(inside + (plane_line(basis[1], basis[2], p),))))
        repeated_f = polynomial_product((basis[0], basis[0], basis[1], basis[2]), p)
        reduction = polynomial_product((basis[0], basis[2]), p)
        check(evaluate_constraints(repeated_f, repeated_lines, 2, p), "repeated_factor_form_double_membership")
        check(evaluate_constraints(reduction, repeated_lines, 1, p), "repeated_factor_degree_drop_witness")
        a, b = (initial_degree(repeated_lines, m, p, 4) for m in (1, 2))
        check((a, b) == (2, 4), "noncoplanar_repeated_factor_configuration_negative")
        records.append({"p": p, "name": "repeated_x0_squared_x1_x2", "lines": len(repeated_lines),
                        "alpha": a, "alpha_square": b,
                        "double_form": "x0^2*x1*x2", "degree_drop_witness": "x0*x2",
                        "point_bases": repeated_lines})
    # Every subcap, not just the largest state, in characteristic two.
    cap_states = Counter()
    for d in range(3, 9):
        for planes in combinations(affine_caps, d):
            lines = pair_arrangement(planes, 2)
            check(ideal_dimension(lines, d - 2, 1, 2) == 0, "all_F2_subcaps_alpha_lower_bound")
            check(ideal_dimension(lines, d - 1, 1, 2) > 0, "all_F2_subcaps_alpha_upper_bound")
            check(ideal_dimension(lines, d - 1, 2, 2) == 0, "all_F2_subcaps_square_lower_bound")
            check(ideal_dimension(lines, d, 2, 2) > 0, "all_F2_subcaps_square_upper_bound")
            cap_states[d] += 1
    return {"explicit_families": records,
            "tetrahedron_subsets_count": sum(tetra_states.values()),
            "tetrahedron_subset_states": [{"p": p, "lines": n, "alpha": a, "alpha_square": b,
                                           "class": category, "count": c}
                                          for (p, n, a, b, category), c in sorted(tetra_states.items())],
            "hilbert_function_components": hilbert_records,
            "F2_subcap_count": sum(cap_states.values()),
            "F2_subcap_sizes": dict(sorted(cap_states.items()))}


def engine_negative_controls():
    # An identically vanishing rational-point sample must not fool this engine.
    basis = tuple(tuple(int(i == j) for i in range(4)) for j in range(4))
    line = line_basis((basis[0], basis[1]), 2)
    polynomial = {(2, 1, 0, 0): 1, (1, 2, 0, 0): 1}
    samples = tuple(v for v in product((0, 1), repeat=2) if any(v))
    check(all(s * s * t + s * t * t == 0 or (s * s * t + s * t * t) % 2 == 0
              for s, t in samples), "finite_rational_point_sampling_trap_setup")
    check(not evaluate_constraints(polynomial, (line,), 1, 2), "jet_engine_rejects_point_sampling_false_positive")
    # The degree-two square has zero derivative in characteristic two but is
    # not in (x2,x3)^2 on this line, so the restriction condition is essential.
    square = {(2, 0, 0, 0): 1}
    check(not evaluate_constraints(square, (line,), 2, 2), "jet_engine_rejects_derivatives_only_false_positive")
    transverse_square = {(0, 0, 2, 0): 1}
    check(evaluate_constraints(transverse_square, (line,), 2, 2), "jet_engine_accepts_actual_transverse_square")
    return {"point_sampling_trap": "x0^2*x1+x0*x1^2 on the line x2=x3=0 over F2",
            "derivatives_only_trap": "x0^2 on the same line in characteristic two",
            "actual_square": "x2^2 on the same line"}


def crosscheck_original_examples():
    basis = tuple(tuple(int(i == j) for i in range(4)) for j in range(4))
    archived = json.loads((ROOT / "ORIGINAL_CONTROLS_REPRODUCED.json").read_text())
    expected = {(r["characteristic"], r["configuration"]):
                (r["alpha"], r["alpha_symbolic_square"]) for r in archived["line_examples"]}
    records = []
    for p in (2, 3, 5):
        tetra = pair_arrangement(basis, p)
        missing = plane_line(basis[0], basis[1], p)
        cases = {
            "single_line": (missing,),
            "three_coplanar": tuple(plane_line(basis[0], b, p) for b in
                                     (basis[1], basis[2], (0, 1, 1, 0))),
            "two_skew": (missing, plane_line(basis[2], basis[3], p)),
            "three_plane_pseudostar": pair_arrangement(basis[:3], p),
            "tetrahedron": tetra,
            "four_plane_cone": pair_arrangement(basis[:3] + ((1, 1, 1, 0),), p),
            "five_plane_star": pair_arrangement(basis + ((1, 1, 1, 1),), p),
            "tetrahedron_missing_edge": tuple(line for line in tetra if line != missing),
        }
        for name, lines in cases.items():
            actual = tuple(initial_degree(lines, m, p, 6) for m in (1, 2))
            check(actual == expected[(p, name)], "independent_engine_crosschecks_original_24_examples")
            records.append({"p": p, "configuration": name, "alpha": actual[0], "alpha_square": actual[1]})
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-exhaustive", action="store_true")
    parser.add_argument("--maximum-size", type=int, default=4)
    args = parser.parse_args()
    start = time.monotonic()
    result = {"status": "PASS_EXACT_FINITE_CONTROLS", "method": __doc__.strip(),
              "qualifications": ["Finite-field coefficient ranks persist over algebraic closure.",
                                 "The tested states do not prove the universal surface lemma.",
                                 "No numerical floating-point or rational-point membership tests are used."]}
    result["engine_negative_controls"] = engine_negative_controls()
    if not args.skip_exhaustive:
        result["exhaustive_F2"] = exhaustive_f2(args.maximum_size)
    result["families"] = family_controls()
    result["original_24_examples_crosschecked"] = crosscheck_original_examples()
    result["checks"] = dict(sorted(CHECKS.items()))
    result["assertion_count"] = sum(CHECKS.values())
    result["elapsed_seconds"] = round(time.monotonic() - start, 3)
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out = ROOT / ("INDEPENDENT_CONTROLS_FAMILIES_ONLY.json" if args.skip_exhaustive else "INDEPENDENT_CONTROLS.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "output": str(out),
                      "assertions": result["assertion_count"], "seconds": result["elapsed_seconds"]}), flush=True)


if __name__ == "__main__":
    main()
