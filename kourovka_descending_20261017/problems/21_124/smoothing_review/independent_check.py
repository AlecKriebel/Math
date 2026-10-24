#!/usr/bin/env python3
"""Independent exact checks of the self-contained height smoothing tool.

Run with Python 3, standard library only. Author inputs are never modified.
"""
from datetime import datetime, timezone
from fractions import Fraction as Q
from math import comb, factorial, gcd, lcm
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
AUTHOR = BASE/'nonabelian_holonomy'
FILES = ('HEIGHT_SMOOTHING.md','HEIGHT_SMOOTHING_MANIFEST.json',
         'check_height_smoothing.py','height_smoothing_results.json')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def trim(p):
    p = list(map(Q,p))
    while len(p)>1 and p[-1] == 0:
        p.pop()
    return p


def mul(p,q):
    out = [Q(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):
            out[i+j] += a*b
    return trim(out)


def power(p,n):
    out = [Q(1)]
    for _ in range(n):
        out = mul(out,p)
    return out


def coef(p,n,k):
    # Closed coefficient, separate from recurrence smoothing below.
    return sum(c*comb(n,k-j) for j,c in enumerate(p) if 0 <= k-j <= n)


def falling(n,k):
    out = 1
    for j in range(k):
        out *= n-j
    return out


def smooth(p,limit=2048):
    out = trim(p)
    for n in range(limit+1):
        if min(out) >= 0:
            return n,out
        out = [out[0]]+[out[i-1]+out[i] for i in range(1,len(out))]+[out[-1]]
    raise AssertionError('No exponent found in the test budget')


def make_integer_multiset(slices, common_shift=0):
    scale = lcm(*(x.denominator for p in slices.values() for x in p))
    out = {}
    for (a,b),p in slices.items():
        for t,c in enumerate(p):
            if c:
                assert c > 0
                value = int(c*scale)
                assert value == c*scale and value > 0
                out[a,b,t+common_shift] = value
    assert {(a,b) for a,b,t in out} == set(slices)
    return out


def projection(multiset,p,q):
    left,right = {},{}
    for (a,b,t),m in multiset.items():
        left[p*a+t] = left.get(p*a+t,0)+m
        right[q*b+t] = right.get(q*b+t,0)+m
    assert left == right


def main():
    before = {n:sha(AUTHOR/n) for n in FILES}
    manifest = json.loads((AUTHOR/'HEIGHT_SMOOTHING_MANIFEST.json').read_text())
    for name,digest in manifest['files'].items():
        assert sha(AUTHOR/name) == digest
    ratio_checks = bound_checks = 0
    for d in range(9):
        for M in range(max(1,d),41):
            n = M-d
            for k in range(M+1):
                for j in range(d+1):
                    exact = Q(falling(k,j)*falling(M-k,d-j), falling(M,d))
                    combinatorial = Q(comb(n,k-j),comb(M,k)) if 0 <= k-j <= n else Q(0)
                    assert exact == combinatorial
                    ratio_checks += 1
                    repeated = Q(k,M)**j * Q(M-k,M)**(d-j)
                    assert abs(exact-repeated) <= Q(comb(d,2),M)
                    bound_checks += 1
    # Test the sharp family with only the last failing and first passing
    # exponents. Monotonicity under multiplication by (1+Z) proves minimality.
    family = []
    family_coefficients = 0
    for m in range(1,101):
        f = [Q(1),Q(1,m)-2,Q(1)]
        n = 4*m-3
        positive = [coef(f,n,k) for k in range(n+3)]
        assert min(positive) == 0
        assert sum(c == 0 for c in positive) == 2
        M = n+1  # degree at exponent n-1
        middle = M//2
        assert coef(f,n-1,middle) < 0
        for k,c in enumerate(positive):
            degree = n+2
            normalized = Q(degree*(degree-1),degree*(degree-1))
            normalized -= (4-Q(1,m))*Q(k*(degree-k),degree*(degree-1))
            assert c/Q(comb(degree,k)) == normalized
            family_coefficients += 1
        family.append({'integer_m':m,'first_exponent':n})
    # Degree0/1, vanishing endpoint after monomial factoring, and strictly
    # positive products of quadratic factors whose middle coefficients vary.
    basic = [[Q(3,7)], [Q(2,5),Q(3,2)]]
    quadratics = []
    for r in (Q(1,2),Q(1),Q(2),Q(3)):
        for epsilon in (Q(1,3),Q(1),Q(2)):
            # (z-r)^2 + epsilon*z > 0 for every z>0.
            quadratics.append([r*r,epsilon-2*r,Q(1)])
    cases = basic + quadratics
    cases += [mul(quadratics[i],quadratics[-i-1]) for i in range(6)]
    cases += [mul(mul(quadratics[0],quadratics[5]),quadratics[9])]
    smoothing = []
    for index,p in enumerate(cases):
        n,positive = smooth(p)
        assert positive == [coef(p,n,k) for k in range(len(p)+n)]
        assert positive[0] > 0 and positive[-1] > 0
        # Arbitrary negative height shift is undone by a common Z shift;
        # horizontal Laurent exponents, deliberately negative, are unchanged.
        shifted = make_integer_multiset({(-3,2):positive},common_shift=-7)
        assert {a for a,b,t in shifted} == {-3}
        unshifted = {(a,b,t+7):m for (a,b,t),m in shifted.items()}
        assert min(t for a,b,t in unshifted) == 0
        smoothing.append({'case':index,'degree':len(p)-1,'exponent':n})
    # A nonzero nonnegative-but-not-strict slice cannot ever smooth: evaluation
    # at z=1 is zero, whereas a nonzero nonnegative-coefficient polynomial
    # would have positive coefficient sum.
    boundary = [Q(1),Q(-2),Q(1)]
    for n in range(101):
        values = [coef(boundary,n,k) for k in range(n+3)]
        assert sum(values) == 0 and min(values) < 0 and max(values) > 0
    # Clear distinct strictly-positive denominators by their squared product.
    q1,q2 = [Q(1),Q(1),Q(1)], [Q(1),Q(-1),Q(1)]
    f,h = [Q(1),Q(-5,3),Q(1)], [Q(4),Q(-11,3),Q(1)]
    D = mul(power(q1,4),power(q2,2))
    first = mul(mul(f,power(q1,3)),power(q2,2))
    zero = mul(mul(h,power(q1,4)),q2)
    assert mul(first,q1) == mul(f,D)
    assert mul(zero,q2) == mul(h,D)
    n1,_ = smooth(first)
    n2,_ = smooth(zero)
    common = max(n1,n2)
    factor = [Q(comb(common,k)) for k in range(common+1)]
    slices = {(-2,0):mul(first,factor), (0,-2):mul(first,factor),
              (0,0):mul(zero,factor)}
    witness = make_integer_multiset(slices)
    projections = 0
    for p in (-3,-1,0,2,5):
        projection(witness,p,p)
        projections += 1
    # A heterogeneous slope control: w10=(1+z)*r(z), w01=r(z), pi=1,qi=2.
    # Thus w10*(z-1)+w01*(1-z^2)=0 identically.
    base = mul(f,power(q1,3))
    n,_ = smooth(base)
    base_positive = mul(base,[Q(comb(n,k)) for k in range(n+1)])
    heterogeneous = make_integer_multiset({(1,0):mul(base_positive,[Q(1),Q(1)]),
                                          (0,1):base_positive})
    projection(heterogeneous,1,2)
    projections += 1
    # Common signed convolution can work if the final coefficients are positive.
    assert mul([Q(1),Q(1)],[Q(1),Q(-1),Q(1)]) == [1,0,0,1]
    # Endpoint zeros in cleared polynomials are harmless after factoring.
    # w=1/z, D=z^2 gives D*w=z, with lowest-height exponent1 and positive
    # factored constant. No denominator zero occurs on the open positive axis.
    assert mul([0,1],[0,1]) == [0,0,1]
    # Reproduce the author arithmetic independently, with a temporary copy.
    with tempfile.TemporaryDirectory(prefix='smoothing_author_') as tmp:
        target = Path(tmp)
        shutil.copyfile(AUTHOR/'check_height_smoothing.py',target/'check_height_smoothing.py')
        subprocess.run([sys.executable,str(target/'check_height_smoothing.py')],
                       check=True,capture_output=True,text=True)
        author = json.loads((target/'height_smoothing_results.json').read_text())
        frozen = json.loads((AUTHOR/'height_smoothing_results.json').read_text())
        for key in frozen:
            if key != 'utc':
                assert author[key] == frozen[key]
    assert before == {n:sha(AUTHOR/n) for n in FILES}
    result = {'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),
              'input_sha256':{'nonabelian_holonomy/'+n:h for n,h in before.items()},
              'script_sha256':sha(Path(__file__)),
              'falling_factorial_binomial_identities':ratio_checks,
              'uniform_probability_bounds_checked':bound_checks,
              'sharp_family_integer_cases':len(family),
              'sharp_family_coefficients':family_coefficients,
              'other_smoothing_cases':smoothing,
              'positive_root_boundary_failures':101,
              'denominator_clearing_identities':2,
              'projection_identities_checked':projections,
              'common_height_smoothing_exponent':common,
              'finite_multiset_types':len(witness),
              'heterogeneous_slope_types':len(heterogeneous),
              'author_checker_reproduced_in_temporary_copy':True,
              'frozen_author_inputs_unchanged':True,
              'scope':'Supporting finite projection-coupling criterion only; no Gram implication, full solution, or novelty certification'}
    (HERE/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
