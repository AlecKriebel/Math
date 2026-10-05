"""Independent, standard-library, exact audit of the frozen power-sum packet.

Usage: python3 -B check_certificate_independent.py [safe_output_directory]
No frozen module is imported. No floating arithmetic enters a pass/fail test.
The polynomial is built by multiplying truncated exponential factors rather
than using the author's Newton recurrence. This file never writes to its input.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys

ZERO = (F(0), F(0))
ONE = (F(1), F(0))
EXPECTED_MANIFEST = 'cd89e252a6d2e0ad4eeaa9696e361c99f68c4fb89419f94c6f78e66402a16dac'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def add(a, b):
    return a[0] + b[0], a[1] + b[1]

def neg(a):
    return -a[0], -a[1]

def sub(a, b):
    return add(a, neg(b))

def mul(a, b):
    return a[0]*b[0] - a[1]*b[1], a[0]*b[1] + a[1]*b[0]

def scale(a, q):
    return a[0]*q, a[1]*q

def zsum(values):
    result = ZERO
    for v in values:
        result = add(result, v)
    return result

def norm2(a):
    return a[0]**2 + a[1]**2

def power(a, k):
    result = ONE
    for _ in range(k):
        result = mul(result, a)
    return result

def convolution(a, b, n):
    out = [ZERO] * (n+1)
    for i, x in enumerate(a):
        if x == ZERO:
            continue
        for j, y in enumerate(b[:n+1-i]):
            if y != ZERO:
                out[i+j] = add(out[i+j], mul(x, y))
    return out

def exponential_product(s):
    """Product over k of exp(-s_k t^k/k), modulo t^(n+1)."""
    n = len(s)
    result = [ONE] + [ZERO] * n
    for k, moment in enumerate(s, 1):
        factor = [ZERO] * (n+1)
        factor[0] = ONE
        term = ONE
        for j in range(1, n//k + 1):
            term = scale(mul(term, moment), -F(1, k*j))
            factor[k*j] = term
        result = convolution(result, factor, n)
    return result

def logarithmic_moments(p):
    """Compute -t P'(t)/P(t) by series inversion and convolution."""
    n = len(p)-1
    inv = [ONE]
    for j in range(1, n+1):
        inv.append(neg(zsum(mul(p[k], inv[j-k]) for k in range(1, j+1))))
    derivative = [ZERO] + [scale(p[j], -j) for j in range(1, n+1)]
    return convolution(derivative, inv, n)[1:]

def polynomial_from_roots(roots):
    p = [ONE]
    for r in roots:
        p = convolution(p, [ONE, neg(r)], len(p))
    return p

def exact_polynomial_identity():
    # Real polynomial dictionaries in x=Re(w), y=Im(w).
    def plus(a, b):
        d = dict(a)
        for k, v in b.items():
            d[k] = d.get(k, F(0)) + v
        return {k:v for k,v in d.items() if v}
    def times(a, b):
        d = {}
        for (i,j),v in a.items():
            for (k,l),w in b.items():
                d[i+k,j+l] = d.get((i+k,j+l),F(0)) + v*w
        return {k:v for k,v in d.items() if v}
    def by(a, q):
        return {k:v*q for k,v in a.items() if v*q}
    x = {(1,0):F(1)}
    y = {(0,1):F(1)}
    x2, y2 = times(x,x), times(y,y)
    real = plus(plus(plus(x2, by(y2,-1)),by(x,-2)),{(0,0):F(2)})
    imag = plus(by(times(x,y),2),by(y,-2))
    lhs = plus(times(real,real),times(imag,imag))
    t = plus(x2,y2)
    tminus2 = plus(t,{(0,0):F(-2)})
    linear = plus(plus(x,by(t,-F(1,4))),{(0,0):-F(1,2)})
    rhs = plus(by(times(tminus2,tminus2),F(1,2)),by(times(linear,linear),8))
    require(lhs == rhs, 'n=2 completed-square polynomial identity failed')
    # t0=3-sqrt(5) is the unique root of t^2-6t+4 in [3/4,4/5].
    f = lambda t:t*t-6*t+4
    require(f(F(3,4))>0 and f(F(4,5))<0, 'n=2 root isolation failed')
    require(F(3,4)-F(7,10)**2>0, 'n=2 nonreal witness radicand failed')

def verify_certificate(s, radius):
    require(all(norm2(v)<radius*radius for v in s), 'strict radius failure')
    p = exponential_product(s)
    require(p[0] == ONE, 'polynomial constant coefficient failure')
    require(zsum(p) == ZERO, 'exact polynomial root at one failure')
    require(logarithmic_moments(p) == s, 'independent logarithmic moment roundtrip failure')
    # Divisibility by 1-t, including the final coefficient condition.
    q = []
    partial = ZERO
    for v in p:
        partial = add(partial, v)
        q.append(partial)
    require(q[-1] == ZERO, 'degree-n coefficient of P/(1-t) did not vanish')
    require(convolution(q[:-1], [ONE, neg(ONE)], len(s)) == p, 'fixed-root factorization failure')
    return p

def main():
    root = Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent/'safe_output'
    raw = (root/'FREEZE_MANIFEST.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest()==EXPECTED_MANIFEST, 'wrong frozen manifest')
    manifest = json.loads(raw)
    require(manifest['file_count']==15 and len(manifest['files'])==15, 'wrong manifest entry count')
    listed = {r['path'] for r in manifest['files']}
    require(set(x.name for x in root.iterdir()) == listed|{'FREEZE_MANIFEST.json'}, 'unexpected or missing frozen entry')
    for record in manifest['files']:
        data = (root/record['path']).read_bytes()
        require(len(data)==record['bytes'], 'byte count: '+record['path'])
        require(hashlib.sha256(data).hexdigest()==record['sha256'], 'hash: '+record['path'])
    d = json.loads((root/'CERTIFICATE.json').read_bytes())
    require(d['n']==32 and d['radius']=='29/40' and len(d['sums'])==32, 'wrong certificate dimensions')
    s = [(F(a),F(b)) for a,b in d['sums']]
    radius = F(d['radius'])
    p = verify_certificate(s, radius)
    # Recompute the two-block exact linear constraint directly from rising factors.
    u = (F(869,2000),-F(5777,10000))
    require(s[:16] == [u]*16, 'first-block mismatch')
    alpha = sub(ONE,u)
    beta = [ONE]
    for j in range(1,33):
        beta.append(scale(mul(beta[-1],add(alpha,(F(j-1),F(0)))),F(1,j)))
    v = [scale(beta[32-k],F(1,k)) for k in range(17,33)]
    target = add(beta[32],mul(u,zsum(v)))
    actual = zsum(mul(a,b) for a,b in zip(s[16:],v))
    require(actual == target, 'two-block affine constraint failure')
    # Reject certificate errors separately: root constraint and radius constraint.
    wrong_root = list(s)
    wrong_root[-1] = add(wrong_root[-1],(F(1,10**6),F(0)))
    require(zsum(exponential_product(wrong_root)) != ZERO, 'root negative control not rejected')
    wrong_radius = list(s)
    wrong_radius[0] = add(wrong_radius[0],ONE)
    require(not all(norm2(v)<radius*radius for v in wrong_radius), 'norm negative control not rejected')
    # Realize and recover known tuples; include zeros, repeated roots and exterior roots.
    fixtures = [[ONE], [ONE,ZERO,ZERO], [ONE]*4,
                [ONE,(F(2),F(0)),(F(-3),F(0)),(F(0),F(2))],
                [ONE,(F(-3,10),F(1,2))]]
    for roots in fixtures:
        moments = [zsum(power(z,k) for z in roots) for k in range(1,len(roots)+1)]
        require(exponential_product(moments)==polynomial_from_roots(roots), 'root fixture polynomial mismatch')
        require(logarithmic_moments(polynomial_from_roots(roots))==moments, 'root fixture moments mismatch')
    exact_polynomial_identity()
    margins = [radius*radius-norm2(v) for v in s]
    smallest = min(margins)
    require(smallest > F(3,1000), 'uniform exact squared-margin control failure')
    output = {
        'status':'PASS',
        'input_manifest_sha256':EXPECTED_MANIFEST,
        'frozen_files_verified':16,
        'no_frozen_modules_imported':True,
        'exact_arithmetic':'Python standard-library Fraction pairs',
        'independent_method':'Product of truncated exponential factors; inverse-series logarithmic derivative',
        'moment_count':32,
        'strict_radius':'29/40',
        'all_squared_norm_margins_exceed':'3/1000',
        'min_margin_index_1_based':margins.index(smallest)+1,
        'exact_root_at_one':True,
        'monic_reciprocal_degree':32,
        'inverse_series_moment_roundtrip':True,
        'two_block_affine_identity':True,
        'fixed_root_factorization':True,
        'n2_identity_in_real_and_imaginary_coordinates':True,
        'root_fixture_count':len(fixtures),
        'negative_controls':2,
        'uses_floating_arithmetic':False,
        'formal_proof_assistant':False,
        'sharp_constant_solved':False,
    }
    print(json.dumps(output,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
