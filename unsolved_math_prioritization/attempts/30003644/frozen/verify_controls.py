#!/usr/bin/env python3
"""Exact rational identities and outward interval tests; no global zero claim.

Requires mpmath 1.3.0. Run: python verify_controls.py > control_results.json
The finite-height cover uses interval elementary functions, not point samples.
"""
from fractions import Fraction as Q
import hashlib
import json
from collections import Counter
import mpmath as mp

mp.iv.dps = 35
iv = mp.iv
primes = (2, 3, 5)
logs = [iv.log(p) for p in primes]


def excludes_zero(x):
    return bool(x.a > 0 or x.b < 0)


def line_box(lo, hi, coefficients=(1, 1, 1)):
    t = iv.mpf([lo, hi])
    re, im = iv.mpf(1), iv.mpf(0)
    for p, logp, c in zip(primes, logs, coefficients):
        phase = t * logp
        re += (iv.mpf(c) / p) * iv.cos(phase)
        im -= (iv.mpf(c) / p) * iv.sin(phase)
    return re, im


def cover(height, coefficients=(1, 1, 1), max_depth=30):
    """Cover [0,height] by exact dyadic leaves; never treat unknown as pass."""
    counts = Counter()
    digest = hashlib.sha256()
    unresolved = []
    stack = [(0.0, height, 0)]
    while stack:
        lo, hi, depth = stack.pop()
        re, im = line_box(lo, hi, coefficients)
        if excludes_zero(re) or excludes_zero(im):
            counts[depth] += 1
            digest.update(f'{lo.hex()}:{hi.hex()}:{depth}\n'.encode())
        elif depth == max_depth:
            unresolved.append([lo, hi])
        else:
            mid = (lo + hi) / 2
            assert lo < mid < hi
            stack += [(mid, hi, depth + 1), (lo, mid, depth + 1)]
    return {
        'height': height,
        'certified_nonzero': not unresolved,
        'accepted_intervals': sum(counts.values()),
        'depth_histogram': dict(sorted(counts.items())),
        'leaf_endpoint_sha256': digest.hexdigest(),
        'unresolved_count': len(unresolved),
        'unresolved_first': unresolved[:5],
    }


def main():
    # The three phases are u=-1, v=(-289+i sqrt(6479))/300,
    # w=(-161-i sqrt(6479))/180. Pairs encode a+b*i*sqrt(6479).
    q = 6479
    u, v, w = (Q(-1), Q(0)), (Q(-289,300), Q(1,300)), (Q(-161,180), Q(-1,180))
    def norm(z): return z[0]**2 + q*z[1]**2
    assert norm(u) == norm(v) == norm(w) == 1
    assert 1 + u[0]/2 + v[0]/3 + w[0]/5 == 0
    assert u[1]/2 + v[1]/3 + w[1]/5 == 0
    assert sum((Q(1,p) for p in primes), Q()) == Q(31,30)
    assert 1 + sum((Q(1,p) for p in primes), Q()) == Q(61,30)
    assert 1 + sum((z[0]/p for z,p in zip((u,v,w),primes)),Q()) == 0
    assert sum(((1+z[0])/p for z,p in zip((u,v,w),primes)),Q()) == Q(1,30)
    # Independent exact evaluation of the elimination polynomial (4).
    def add(x,y): return (x[0]+y[0],x[1]+y[1])
    def mul(x,y): return (x[0]*y[0]-q*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
    def scale(a,x): return (a*x[0],a*x[1])
    a,b,c = Q(1,2),Q(1,3),Q(1,5)
    A = add((Q(1),Q(0)),scale(a,u))
    B = add((Q(1),Q(0)),scale(a,(u[0],-u[1])))
    polynomial = add(add(mul(scale(b,B),mul(v,v)),
                         mul(add(mul(A,B),(b*b-c*c,Q(0))),v)),scale(b,A))
    assert polynomial == (0,0)

    # Deliberate sign/denominator mutants must fail the exact zero identity.
    mutants = []
    for j in range(3):
        terms = [u,v,w]
        terms[j] = (-terms[j][0],-terms[j][1])
        residual = (1 + sum((z[0]/p for z,p in zip(terms,primes)),Q()),
                    sum((z[1]/p for z,p in zip(terms,primes)),Q()))
        assert residual != (0,0)
        mutants.append([str(x) for x in residual])

    L = sum((logp / p for logp,p in zip(logs,primes)), iv.mpf(0))
    assert L - logs[-1]/30 > iv.mpf('0.98')
    # Rigorous bracket, no floating root is used in a proof.
    def h(s): return sum((iv.exp(-s*logp) for logp in logs),iv.mpf(0))-1
    assert h(iv.mpf('1.032')) > 0
    assert h(iv.mpf('1.033')) < 0

    # Rouche certificate for a zero strictly to the right of Re(s)=1.
    # The center and radius are decimal rationals, not floating approximations.
    center_re = '1.006705654528482647538233912439'
    center_im = '185.725918497342080628141229326837'
    radius = '1e-20'
    sigma, t, r = iv.mpf(center_re), iv.mpf(center_im), iv.mpf(radius)
    re, im, derivative_re, second_derivative_bound = iv.mpf(1), iv.mpf(0), iv.mpf(0), iv.mpf(0)
    for logp in logs:
        amplitude = iv.exp(-sigma*logp)
        cosine, sine = iv.cos(t*logp), iv.sin(t*logp)
        re += amplitude*cosine
        im -= amplitude*sine
        derivative_re -= logp*amplitude*cosine
        second_derivative_bound += logp**2*iv.exp(-(sigma-r)*logp)
    assert abs(re)+abs(im) < iv.mpf('1e-27')
    assert derivative_re > iv.mpf('0.9')
    assert second_derivative_bound < 2
    assert iv.mpf('1e-27') + r*r < iv.mpf('0.9')*r
    assert sigma-r > 1

    target = cover(10000.0)
    assert target['certified_nonzero']
    # 1+2*2^(-s) vanishes at s=1+i*pi/log(2). The bounded
    # certificate MUST fail, rather than reporting every polynomial zero-free.
    negative = cover(8.0, (2,0,0), max_depth=22)
    assert not negative['certified_nonzero']
    root_interval = iv.pi/logs[0]
    assert any(iv.mpf(lo) < root_interval.a and root_interval.b < iv.mpf(hi)
               for lo,hi in negative['unresolved_first'])
    print(json.dumps({
        'mpmath_version':mp.__version__, 'interval_decimal_precision':iv.dps,
        'exact_torus_witness':'PASS', 'sign_mutants_rejected':mutants,
        'sigma_star_bracket':['1.032','1.033'],
        'simple_zero_derivative_lower_bound':'0.98',
        'right_halfplane_rouche':{
            'center':[center_re,center_im], 'radius':radius,
            'residual_upper':'1e-27', 'derivative_modulus_lower':'0.9',
            'second_derivative_upper':'2', 'unique_zero_in_disk':True,
            'scope':'Zero strictly to the right of the target line; not a counterexample to the target.'},
        'target_finite_height':target, 'negative_control':negative,
        'scope':'The target cover proves only |t|<=10000, using conjugation. It does not prove all-height nonvanishing.'
    },indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
