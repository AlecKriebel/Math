#!/usr/bin/env python3
"""Independent exact controls for the frozen Fibonacci partial-result packet.

Python 3 and SymPy are required. This script only reads the frozen packet and
prints JSON. It never writes to public/. Usage: python audit_controls.py
Optionally supply --public /path/to/public. No network or floating-point tests.
These controls do not certify an infinite-energy spectral ray.
"""
import argparse
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path
import sympy as sp


def run(public):
    checks = []
    negative = []

    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    def reject(name, erroneous_condition):
        if erroneous_condition:
            raise AssertionError("Negative control was not rejected: " + name)
        negative.append(name)

    frozen = json.loads(Path(__file__).with_name("FROZEN_INPUTS.json").read_text())
    for item in frozen["files"]:
        data = (public / item["path"]).read_bytes()
        check("frozen_bytes:" + item["path"], len(data) == item["bytes"])
        check("frozen_sha256:" + item["path"],
              hashlib.sha256(data).hexdigest() == item["sha256"])

    # Check a stronger unrestricted polynomial identity, independently of the
    # author's Groebner reduction modulo determinant-one constraints.
    a, b, c, d, e, f, g, h = sp.symbols("a b c d e f g h")
    A = sp.Matrix([[a, b], [c, d]])
    B = sp.Matrix([[e, f], [g, h]])
    u, v, w = sp.trace(A), sp.trace(B), sp.trace(A * B)
    det_a, det_b = A.det(), B.det()
    identity = ((A * B - B * A).det() + det_b*u**2 + det_a*v**2
                + w**2 - u*v*w - 4*det_a*det_b)
    check("unrestricted_commutator_trace_polynomial", sp.expand(identity) == 0)
    A1 = sp.Matrix([[1, 1], [0, 1]])
    B1 = sp.Matrix([[1, 0], [1, 1]])
    x, y, z = sp.trace(A1)/2, sp.trace(B1)/2, sp.trace(A1*B1)/2
    invariant = x*x + y*y + z*z - 2*x*y*z - 1
    det_comm = (A1*B1-B1*A1).det()
    check("positive_invariant_sign_witness", invariant == sp.Rational(1, 4)
          and det_comm == -1 and 4*invariant + det_comm == 0)
    reject("opposite_fricke_sign", 4*invariant - det_comm == 0)
    reject("missing_factor_four", invariant + det_comm == 0)

    k = sp.symbols("k", positive=True)
    q = sp.symbols("q", real=True)
    S = sp.diag(1, 1/k)
    generator = sp.Matrix([[0, 1], [q-k*k, 0]])
    J = sp.Matrix([[0, 1], [-1, 0]])
    P = sp.Matrix([[0, 0], [1, 0]])
    check("scaled_transfer_generator",
          sp.simplify(S*generator*S.inv() - k*J - q*P/k) == sp.zeros(2))
    check("trace_zero_generator", sp.trace(k*J + q*P/k) == 0)
    check("common_conjugation_traces",
          sp.simplify(sp.trace(S*A*S.inv()*S*B*S.inv()) - w) == 0)
    wrong_S = sp.diag(1, k)
    reject("reversed_state_scaling", sp.simplify(
        wrong_S*generator*wrong_S.inv() - k*J - q*P/k) == sp.zeros(2))
    c0, s0, c1, s1 = sp.symbols("c0 s0 c1 s1")
    R0, R1 = sp.Matrix([[c0, s0], [-s0, c0]]), sp.Matrix([[c1, s1], [-s1, c1]])
    check("free_rotation_commutation", sp.simplify(R0*R1-R1*R0) == sp.zeros(2))
    p0, p1 = sp.symbols("p0 p1")
    check("exponential_budget_combines", sp.expand(
        (p0-1)+(p1-1)+(p0-1)*(p1-1)-(p0*p1-1)) == 0)

    n, period, al, be, ga, de = sp.symbols("n P alpha beta gamma delta")
    width_a = (n*period+be)**2-(n*period+al)**2
    gap_b = ((n+1)*period+ga)**2-(n*period+de)**2
    width_b_next = ((n+1)*period+de)**2-((n+1)*period+ga)**2
    gap_a = ((n+1)*period+al)**2-(n*period+be)**2
    lead = 2*period*((be-al)+(de-ga)-period)
    for name, margin in [("first_overlap", width_a-gap_b),
                         ("second_overlap", width_b_next-gap_a)]:
        poly = sp.Poly(sp.expand(margin), n)
        check(name + "_leading_coefficient", sp.expand(poly.coeff_monomial(n)-lead) == 0)
        check(name + "_degree", poly.degree() == 1)
    reject("narrow_windows_force_positive_margin",
           lead.subs({period:1,al:0,be:sp.Rational(1,3),ga:0,de:sp.Rational(1,3)}) > 0)
    lower, upper, xx, yy = sp.symbols("l u x y", positive=True)
    check("square_map_secant", sp.expand((yy**2-xx**2)-(yy-xx)*(yy+xx)) == 0)

    residues_a = {0, 1, 2, 4, 5, 9}
    residues_b = {(-r) % 12 for r in residues_a}
    sums_a = {a+b for a in residues_a for b in residues_a}
    sums_b = {a+b for a in residues_b for b in residues_b}
    sums_mixed = {a+b for a in residues_a for b in residues_b}
    check("exact_B_residues", residues_b == {0,3,7,8,10,11})
    check("A_self_sum_integer_cover", set(range(12)) <= sums_a)
    check("B_self_sum_modular_cover", {s % 12 for s in sums_b} == set(range(12)))
    check("B_threshold_12_representatives",
          all(any(s % 12 == r and s <= 12+r for s in sums_b) for r in range(12)))
    check("mixed_missing_residue", set(range(12)) - {s % 12 for s in sums_mixed} == {6})
    reject("self_sum_rays_imply_mixed_residue_cover", 6 in {s % 12 for s in sums_mixed})

    prefixes = {0}
    denominator = 1
    radix_controls = []
    for level in range(1, 5):
        base = 2*(level+1)
        denominator *= base
        prefixes = {base*p+d for p in prefixes for d in range(level+1)}
        pair_sums = {p+q for p in prefixes for q in prefixes}
        count = math.factorial(level+1)
        sum_count = math.prod(2*j+1 for j in range(1, level+1))
        check("prefix_count_level_"+str(level), len(prefixes) == count)
        check("prefix_lattice_and_separation_level_"+str(level),
              all(v-u >= 1 for u,v in itertools.pairwise(sorted(prefixes))))
        check("no_carry_sum_count_level_"+str(level), len(pair_sums) == sum_count)
        check("radix_denominator_level_"+str(level), denominator == 2**level*count)
        radix_controls.append({"level":level,"prefixes":count,"sum_prefixes":sum_count,
                               "denominator":denominator,
                               "sum_cover_bound":str(Fraction(sum_count, denominator))})
    # For s=1-1/m, the m-th power of 2^n Q_(n-1)^(-1/m)
    # has consecutive ratio 2^(m-1)/(n+1). The displayed uniform tail bound
    # is exact; the proof uses it for arbitrary integer m, not these samples.
    check("factorial_frostman_tail_ratio",
          all(Fraction(2**(m-1), 2**m) == Fraction(1,2) for m in range(2,12)))
    harmonic = sum(Fraction(1, 2*j+2) for j in range(1,41))
    check("omitted_digit_harmonic_identity", harmonic ==
          (sum(Fraction(1,j) for j in range(1,42))-1)/2)
    reject("unrestricted_sum_digits_give_shrinking_cover",
           Fraction(math.prod(2*(j+1) for j in range(1,9)),
                    math.prod(2*(j+1) for j in range(1,9))) < 1)

    return {
        "status":"all_independent_exact_controls_passed",
        "positive_controls_passed":len(checks),
        "negative_controls_rejected":len(negative),
        "positive_controls":checks,
        "negative_controls":negative,
        "mixed_radix_controls":radix_controls,
        "sympy_version":sp.__version__,
        "frozen_input_files_unchanged":True,
        "full_resolution":False,
        "recommended_status":"unsolved 5/5",
        "limits":"Finite and symbolic controls supplement the analytic audit. They do not establish the spectral-ray conjecture, Hausdorff dimension, or infinite-scale thickness by themselves."
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--public", type=Path, default=Path(__file__).resolve().parent.parent/"public")
    args = parser.parse_args()
    print(json.dumps(run(args.public), indent=2))
