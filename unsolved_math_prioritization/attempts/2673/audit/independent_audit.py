#!/usr/bin/env python3
"""Independent exact arithmetic cross-checks of an externally pinned SU(2) bundle.

Finite checks are regression evidence, not certification of Floer theorems.
Only Python's standard library is used. This program writes nothing.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from math import gcd, isqrt
from pathlib import Path
import runpy
import sys

sys.dont_write_bytecode = True
NAMES = {'REPORT.md', 'README.md', 'SOURCE_PINS.json', 'VALIDATION.json',
         'audit.py', 'controls.py', 'verify.py', 'MANIFEST.json'}


def check(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def independent_prime(n):
    return n > 1 and all(n % d for d in range(2, isqrt(n) + 1))


def prime_power(n):
    if n < 2:
        return False
    for p in range(2, isqrt(n) + 1):
        if n % p == 0:
            while n % p == 0:
                n //= p
            return n == 1 and independent_prime(p)
    return True


def guaranteed_nondegenerate(p):
    n = abs(p)
    if n % 2 == 0:
        n //= 2
    return n == 1 or prime_power(n)


def four_class(p):
    n = abs(p)
    return n % 4 == 0 and (n // 4) % 2 == 1 and prime_power(n // 4)


def published(p, q):
    n = abs(p)
    return (n <= 2*q or (n < 5*q and guaranteed_nondegenerate(p))
            or (n < 7*q and (n & (n-1) == 0 or four_class(p))))


def independent_torus(p, q):
    n = abs(p)
    # If |n-abq| <= 1, then ab <= (n+1)/q. Generate products directly.
    products = []
    for a in range(2, isqrt((n+1)//q) + 1):
        for b in range(a+1, (n+1)//(a*q) + 1):
            if gcd(a,b) == 1 and (abs(n-a*b*q) == 1 or (n == a*b*q and a == 2)):
                products.append([a,b])
    return products[0] if products else None


def analytic_trefoil(p, q):
    d = abs(p-6*q)
    if d == 0:
        return None
    lo = d//6+1
    hi = (5*d-1)//6
    if (lo-q) % 2:
        lo += 1
    return Fraction(lo,d) if lo <= hi else None


def multiply(a,b):
    out = [0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i+j] += x*y
    return out


def mobius(n):
    count = 0
    d = 2
    while d*d <= n:
        if n % d == 0:
            n //= d
            if n % d == 0:
                return 0
            count += 1
        d += 1
    return (-1)**(count+(n>1))


def exact_quotient(a,b):
    # Independent division from the constant term; these divisors have unit constant.
    out = [0]*(len(a)-len(b)+1)
    check(b[0] in (-1,1), 'nonunit constant')
    for i in range(len(out)):
        out[i] = a[i]//b[0]
        for j,v in enumerate(b):
            a[i+j] -= out[i]*v
    check(not any(a), 'Mobius polynomial quotient not exact')
    return out


def independent_cyclotomic(n):
    top, bottom = [1], [1]
    for d in range(1,n+1):
        if n % d:
            continue
        m = mobius(n//d)
        term = [-1]+[0]*(d-1)+[1]
        if m == 1:
            top = multiply(top,term)
        elif m == -1:
            bottom = multiply(bottom,term)
    return exact_quotient(top,bottom)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('bundle',type=Path)
    ap.add_argument('--manifest-sha256',required=True)
    ap.add_argument('--verifier-sha256',required=True)
    args = ap.parse_args()
    root = args.bundle
    check(root.is_dir() and not root.is_symlink(), 'non-directory or linked bundle')
    check({p.name for p in root.iterdir()} == NAMES, 'unexpected original file set')
    check(sha(root/'MANIFEST.json') == args.manifest_sha256, 'external manifest pin mismatch')
    check(sha(root/'verify.py') == args.verifier_sha256, 'external verifier pin mismatch')
    before = {n:sha(root/n) for n in NAMES}
    verifier = runpy.run_path(str(root/'verify.py'))
    verifier['verify'](root,args.manifest_sha256)
    author = runpy.run_path(str(root/'audit.py'))
    count = 0
    trefoil = 0
    for p in range(-240,241):
        if p == 0:
            continue
        for q in range(1,81):
            if gcd(p,q) != 1:
                continue
            got = author['classify']({'p':p,'q':q})
            obs = independent_torus(p,q)
            check(got['published_input_corollary'] == published(p,q), 'independent positive mismatch')
            check(got['torus_obstruction'] == obs, 'independent torus mismatch')
            cond = abs(p) <= 8*q and (guaranteed_nondegenerate(p) or four_class(p)) and obs is None
            check(got['conditional_preprint_corollary'] == cond, 'conditional class mismatch')
            check(got['unresolved_by_this_audit'] == (not published(p,q) and obs is None), 'scope flag mismatch')
            count += 1
            # Full independent congruence witness comparison on a separate narrower strip.
            if abs(p) <= 100 and q <= 30:
                witness = analytic_trefoil(p,q)
                check(author['trefoil_witness'](p,q) == witness, 'analytic witness mismatch')
                check((witness is not None) == (abs(p-6*q) >= 2), 'analytic existence mismatch')
                trefoil += 1
    polys = author['cyclotomics'](160)
    for n in range(1,161):
        check(polys[n] == independent_cyclotomic(n), 'Mobius cyclotomic mismatch')
    divisor_cases = 0
    for p in range(1,5001):
        check(author['four_odd_prime_power'](p) == four_class(p), 'four class mismatch')
        check(author['prime_power_or_one'](p//gcd(p,2)) == guaranteed_nondegenerate(p), 'nondegenerate class mismatch')
        if four_class(p):
            for d in range(1,p//2+1):
                if (p//2)%d == 0 and d != 1 and not prime_power(d):
                    check(d % 2 == 0 and d//2 % 2 == 1 and prime_power(d//2), 'residual divisor escaped')
                    divisor_cases += 1
    for g in range(1,1001):
        smallest = 4*((2*g-1+3)//4)
        check(smallest == 4*((g+1)//2), 'rounding identity failed')
        check(smallest == (2*g if g%2 == 0 else 2*g+2), 'rounding parity failed')
        if smallest < 8:
            check(g <= 2, 'conditional genus bound failed')
    # Published-only sequence lies in U and converges to the excluded coefficient 6.
    for k in range(4,101):
        p=2**k
        q=(2**(k-1)+(-1)**k)//3
        check(3*q == 2**(k-1)+(-1)**k and q>0 and q%2 == 1, 'sequence denominator failed')
        check(gcd(p,q) == 1 and 5*q < p < 7*q, 'sequence slope hypotheses failed')
        check(p-6*q == -2*(-1)**k, 'sequence distance failed')
        check(analytic_trefoil(p,q) == Fraction(1,2), 'sequence witness failed')
    check(analytic_trefoil(6,1) is None, 'limit coefficient failed')
    # Values exactly at and adjacent to the documented CLI bound.
    for p,q in [(100000,1),(-100000,1),(1,100000),(-1,100000),(99999,100000),(100000,99999)]:
        got=author['classify']({'p':p,'q':q})
        check(got['published_input_corollary'] == published(p,q), 'CLI boundary arithmetic failed')
    check(before == {n:sha(root/n) for n in NAMES}, 'original bundle changed')
    print(json.dumps({'status':'passed','independent_slope_cases':count,
        'independent_trefoil_witness_cases':trefoil,'mobius_cyclotomic_cases':160,
        'numerator_class_cases':5000,'four_class_divisor_cases':divisor_cases,
        'rounding_cases':1000,'published_nonclosure_sequence_cases':97,
        'cli_exact_boundary_cases':6,'frozen_original_unchanged':True,
        'scope':'finite exact arithmetic and byte integrity; imported mathematical theorems are not machine-certified'},sort_keys=True))

if __name__ == '__main__':
    main()
