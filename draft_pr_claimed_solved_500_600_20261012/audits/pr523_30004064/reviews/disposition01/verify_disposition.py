#!/usr/bin/env python3
"""Fresh exact sign-separation, prior-example, and source-binding checks.

All checks remain active under python -O. No candidate/root/prior verifier import.
"""
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import hashlib
import json


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def dot(a, b):
    require(len(a) == len(b), "dot dimensions")
    return sum(x*y for x, y in zip(a, b))


def measurements(n):
    pixels = tuple(product(range(n), repeat=2))
    lines = [(1, 0, k) for k in range(n)]
    lines += [(0, 1, k) for k in range(n)]
    lines += [(-1, 1, k) for k in range(1-n, n)]
    return tuple(tuple(int(a*i+b*j == k) for i, j in pixels)
                 for a, b, k in lines)


def mv(a, v):
    return tuple(dot(row, v) for row in a)


def rowrank(a):
    work = [list(map(Fraction, row)) for row in a]
    pivot_row = 0
    for column in range(len(work[0])):
        pivots = [k for k in range(pivot_row, len(work)) if work[k][column]]
        if not pivots:
            continue
        k = pivots[0]
        work[pivot_row], work[k] = work[k], work[pivot_row]
        divisor = work[pivot_row][column]
        work[pivot_row] = [x/divisor for x in work[pivot_row]]
        for k in range(pivot_row+1, len(work)):
            multiplier = work[k][column]
            work[k] = [x-multiplier*y for x, y in zip(work[k], work[pivot_row])]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def row_conditioned_fiber(n, target):
    a = measurements(n)
    rows = [tuple(tuple(int(j in selected) for j in range(n))
                  for selected in combinations(range(n), k)) for k in target[:n]]
    solutions = []
    checked = 0
    for choice in product(*rows):
        checked += 1
        image = sum(choice, ())
        if mv(a, image) == target:
            solutions.append(image)
    return solutions, checked


def common(solutions):
    require(bool(solutions), "nonempty binary fiber")
    return tuple(col[0] if all(v == col[0] for v in col) else None
                 for col in zip(*solutions))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    a = measurements(5)
    # Read anew from Ferudun Theorem 4.2, 0/1 picture and signed kernel image.
    b = tuple(int(v) for v in "0001001000100011000000100")
    c = (1,0,0,-1,0, 0,-2,0,1,1, 0,0,1,0,-1,
         -1,1,0,0,0, 0,1,-1,0,0)
    s = tuple(2*v-1 for v in b)
    target = mv(a, b)
    require(target == (1,1,2,1,1,2,1,1,1,1,0,1,2,0,1,0,1,1,0), "primary line sums")
    solutions, checked = row_conditioned_fiber(5, target)
    require(solutions == [b] and checked == 6250, "unique 5x5 binary solution")
    require(mv(a, c) == (0,)*19, "integer kernel certificate")
    support = tuple(k for k, v in enumerate(c) if v)
    require(len(support) == 11, "movable support count")
    require(all(s[k]*c[k] < 0 for k in support), "nonzero cube-tangent kernel vector")
    require(all(-1 <= x+v <= 1 for x, v in zip(s, c)), "fractional competitor")

    # The prior table f is in row(A), independently checked by augmented rank;
    # no supplied line-potential coefficients are used here.
    f = (0,3,2,0,2, 1,0,3,0,0, -3,1,0,1,0,
         0,0,4,1,4, 1,0,0,2,1)
    arank = rowrank(a)
    require(arank == 16 and rowrank(a+(f,)) == arank, "f is in measurement rowspace")
    require(tuple(k for k,v in enumerate(f) if v == 0) == support, "exposing zero set")
    require(all(x*v <= 0 for x,v in zip(s,f)), "exposing signs")
    restricted = tuple(tuple(row[k] for k in support) for row in a)
    require(rowrank(restricted) == 10, "restricted kernel dimension one")
    lower, upper = None, None
    for x,v in zip(s,c):
        if v:
            lo, hi = sorted((Fraction(-1-x,v), Fraction(1-x,v)))
            lower = lo if lower is None else max(lower,lo)
            upper = hi if upper is None else min(upper,hi)
    require((lower,upper) == (Fraction(0),Fraction(1)), "exact box segment endpoints")

    # f.e = 0 and nonnegative summands imply e=0 outside support; restricted
    # rank gives e=lambda*c and the independently computed bounds give [0,1].
    # Also c^T(A^T mu) = 0. A full correct sign s would make all 11 nonzero
    # summands strictly negative. This rules out every exact multiplier sign,
    # independent of objective, solver, rank reduction, or central-path theory.

    # Independently check prior Theorem 4.6's four-solution/common-pixel example.
    a4 = measurements(4)
    b4 = tuple(int(v) for v in "1100100100100100")
    fiber4, checked4 = row_conditioned_fiber(4, mv(a4,b4))
    require(len(fiber4) == 4 and checked4 == 576, "4x4 binary classification")
    fixed_binary = tuple(k for k,v in enumerate(common(fiber4)) if v is not None)
    require(fixed_binary == (3,6,9,12), "four common binary pixels")
    h = Fraction(1,2)
    fractional4 = (1,h,h,0, h,h,h,h, h,h,0,0, 0,h,0,h)
    require(mv(a4,fractional4) == mv(a4,b4), "rational 4x4 feasible witness")
    require(fractional4[6] == fractional4[9] == h, "two common pixels move")
    common_sign4 = tuple(2*v-1 if v is not None else 0 for v in common(fiber4))
    tangent4 = tuple(2*(v-w) for v,w in zip(fractional4,b4))
    require(mv(a4,tangent4) == (0,)*len(a4), "4x4 kernel witness")
    require(all(tangent4[k]*common_sign4[k] <= 0 for k in fixed_binary), "4x4 tangent/common signs")
    require(any(tangent4[k]*common_sign4[k] < 0 for k in fixed_binary), "4x4 strict common obstruction")
    # For sign(A^T mu)=common_sign4, q vanishes at all variable coordinates;
    # on the common coordinates, tangent4.q has a strictly negative sum.
    # This again contradicts tangent4 in ker(A).

    # Independent approximate-direction control for the frozen two-direction
    # example: exact signs can be correct at every positive epsilon.
    a3 = measurements(3)[:5]  # three rows and first two columns
    direction = (1,0,0,1,0)
    q = mv(tuple(zip(*a3)),direction)
    expected = (1,1,1,1,0,0,1,0,0)
    require(tuple((v>0)-(v<0) for v in q) == expected, "finite correct common signs")
    y = (3,1,1,3,1)
    gaps = []
    for epsilon in (Fraction(1,2),Fraction(1,17),Fraction(1,10**8)):
        mu = tuple(epsilon*v for v in direction)
        backprojection = mv(tuple(zip(*a3)),mu)
        gap = Fraction(1,2)*sum((v-w)**2 for v,w in zip(mu,y))
        gap += sum(map(abs,backprojection))-Fraction(1,2)*dot(y,y)
        require(gap == epsilon**2, "objective-gap direction control")
        gaps.append({"epsilon":str(epsilon),"gap":str(gap)})

    # Do not certify all assertions in the overlapping note. Its Corollary 3.3
    # says that nonfixed pixels also survive a positive threshold for tau>=tau2.
    # Here Q={(1,t,-t): -1<=t<=1}; the unique central point always has z2=z3=0.
    # Strict convexity and symmetry prove the latter for every tau>0. An exact
    # stationary point at tau=3/8 independently checks this mechanism.
    counter_a = ((1,0,0),(0,1,1))
    counter_y = (1,0)
    tau = Fraction(3,8)
    central_z = (Fraction(1,2),Fraction(0),Fraction(0))
    residual = tuple(v-w for v,w in zip(mv(counter_a,central_z),counter_y))
    gradient = tuple(v+2*tau*z/(1-z*z)
                     for v,z in zip(mv(tuple(zip(*counter_a)),residual),central_z))
    require(gradient == (0,0,0), "exact central-point stationarity")
    central_mu = tuple(-v for v in residual)
    central_nu = mv(tuple(zip(*counter_a)),central_mu)
    require(central_nu == (Fraction(1,2),0,0), "nonfixed backprojections remain zero")

    attributes = json.loads(Path('sources/ferudun_datacite.json').read_text())['data']['attributes']
    metadata = json.loads(Path('sources/ferudun_metadata.json').read_text())
    require(metadata['files']['paper.pdf']['sha256'] == sha('sources/ferudun.pdf'), "public PDF binding")
    require(attributes['created'] == attributes['registered'] == attributes['updated'] == '2026-10-02T20:09:16.000Z', "DOI chronology")
    require(attributes['version'] == metadata['version'] == '1.0', "public version agreement")
    return {
        "status":"all_exact_checks_passed",
        "all_checks_active_under_optimized_python":True,
        "prior_5x5":{"row_conditioned_candidates":checked,"binary_solutions":len(solutions),
                     "measurement_rank":arank,"kernel_support":support,"restricted_rank":10,
                     "exact_box_segment":[str(lower),str(upper)],"fixed_pixels":14,
                     "no_exact_multiplier_has_full_correct_sign":True},
        "prior_4x4":{"row_conditioned_candidates":checked4,"binary_solutions":len(fiber4),
                     "common_binary_pixels":fixed_binary,"common_pixels_moved_by_fractional_witness":[6,9],
                     "no_exact_multiplier_has_correct_common_pattern":True},
        "frozen_example_correct_finite_sign_control":gaps,
        "prior_corollary_3_3_overbreadth_control":{
            "matrix":counter_a,"datum":counter_y,"box_fiber":"(1,t,-t), -1<=t<=1",
            "nonfixed_pixels":[1,2],"central_values_of_nonfixed_pixels":"zero for every tau>0 by symmetry and uniqueness",
            "rational_stationarity_tau":str(tau),"central_z":[str(v) for v in central_z],
            "central_backprojection":[str(v) for v in central_nu],
            "effect_on_lemma_2_1_or_prior_5x5_certificate":"none"
        },
        "prior_pdf_sha256":sha('sources/ferudun.pdf'),
        "datacite_created_registered_updated":attributes['created'],
        "no_solver_or_central_path_assertion_used":True,
        "root_checker_sha256":sha('../../root_reproduction/verify_repair_overlap.py'),
        "verifier_sha256":sha(__file__)
    }


if __name__ == '__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
