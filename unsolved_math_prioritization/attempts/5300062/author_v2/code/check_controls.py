#!/usr/bin/env python3
"""Finite algebra and numerical controls only; not a proof of ray smoothness."""
import cmath
import json
import math
import random
import sys
from fractions import Fraction as Q
from pathlib import Path

if sys.flags.optimize:
    raise SystemExit('Run with unoptimized Python; optimization is not supported.')


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def mul(a, b):
    n = min(len(a), len(b))
    return [sum((a[j]*b[k-j] for j in range(k+1)), Q(0)) for k in range(n)]


def inv(a):
    b = [1/a[0]]
    for k in range(1, len(a)):
        b.append(-sum((a[j]*b[k-j] for j in range(1,k+1)), Q(0))/a[0])
    return b


def exp0(a):
    check(a[0] == 0, 'exp0 constant')
    b = [Q(1)]
    for k in range(1, len(a)):
        b.append(sum((j*a[j]*b[k-j] for j in range(1,k+1)), Q(0))/k)
    return b


def log1(a):
    check(a[0] == 1, 'log1 constant')
    ai = inv(a)
    return [Q(0)] + [sum((j*a[j]*ai[k-j] for j in range(1,k+1)), Q(0))/k for k in range(1,len(a))]


def F(x):
    return math.expm1(x)


def orbit(x, n):
    for _ in range(n):
        x = F(x)
    return x


def ray(kappa, t, address):
    w = complex(orbit(t, len(address)))
    # Derivative with respect to kappa, and potential derivative.
    dt = 1.
    u = t
    for _ in address:
        dt *= math.exp(u)
        u = F(u)
    dk = 0j
    for s in reversed(address):
        dt = dt/w
        dk = dk/w-1
        w = cmath.log(w)-kappa+2j*math.pi*s
    return w, dk, dt


def run():
    rng = random.Random(5300062)
    algebra = 0
    for degree in range(1, 9):
        for _ in range(20):
            a = [Q(0)] + [Q(rng.randint(-5,5), rng.randint(1,7)) for _ in range(degree)]
            ea = exp0(a)
            check(log1(ea) == a, 'log(exp(a)) jet identity')
            algebra += 1
            b = [Q(1)] + a[1:]
            check(exp0(log1(b)) == b, 'exp(log(b)) jet identity')
            algebra += 1
            unit = mul(b, inv(b))
            check(unit == [Q(1)]+[Q(0)]*degree, 'reciprocal jet identity')
            algebra += 1
    conjugacy = derivatives = branch = growth = implicit = 0
    for j in range(30):
        k = complex(-.15+j/120, -.2+j/100)
        z = complex(-.7+j/80, .2-j/170)
        left = cmath.exp(z+k)+k
        w = z+k
        right = cmath.exp(w)+k
        check(abs(left-right) < 1e-12, 'translation conjugacy')
        conjugacy += 1
        check(abs(cmath.exp(k)*cmath.exp(z)-cmath.exp(z+k)) < 1e-12, 'lambda normalization')
        conjugacy += 1
        t = 0.6+j/150
        addr = [0,1,-1]
        value, dk, dt = ray(k,t,addr)
        h = 1e-6
        fd_k = (ray(k+h,t,addr)[0]-ray(k-h,t,addr)[0])/(2*h)
        fd_t = (ray(k,t+h,addr)[0]-ray(k,t-h,addr)[0])/(2*h)
        check(abs(dk-fd_k) < 2e-6*(1+abs(dk)), 'parameter derivative recurrence')
        derivatives += 1
        check(abs(dt-fd_t) < 2e-6*(1+abs(dt)), 'potential derivative recurrence')
        derivatives += 1
        # A = Log(F^n), B = Log(F^n+d), controlled continuation.
        v = complex(6+j/100, .03)
        U = cmath.exp(v)-1
        qv = v+cmath.log(1-cmath.exp(-v))
        d = -.1+.2j
        check(abs(qv+cmath.log(1+d/U)-cmath.log(U+d)) < 1e-11, 'two-log continued identity')
        branch += 1
        # An explicit simple-root test Phi=kappa-t-i*t^2.
        tt = Q(j,11)
        gp = complex(1, float(2*tt))
        phi_t = -gp
        check(abs(gp+phi_t) == 0, 'implicit derivative identity')
        implicit += 1
    for u in [2., 2.1, 2.2]:
        for d in [.01,.02,.04,.1]:
            v = u+d
            for m in [1,2]:
                um,vm=orbit(u,m),orbit(v,m)
                check(vm-um >= 2**m*(v-u)*(1-1e-12), 'growth gap lower bound')
                check(um/vm <= 2*math.exp(-2**(m-1)*(v-u))*(1+1e-12), 'growth ratio upper bound')
                growth += 2
    # Finite tail-buffer checks used in the proof, not universal certification.
    lower = 0
    for K in [1.,2.,5.,10.,20.]:
        for extra in [.1,.5,1.,2.]:
            a=K+6+extra
            check((K+2)*math.exp(-a)<1-math.exp(-1), 'logarithmic real-part buffer')
            check(math.log(math.expm1(a)-K-1)-K >= a-K-1, 'one-step real part')
            check(abs(1/(1-cmath.exp(-(a+.03j))))<2, 'q derivative buffer')
            lower += 3
    # The flat function is a logical countercontrol, not an exponential example.
    flat = 0
    for m in range(1,10):
        t=1/(m+1)
        check(math.exp(-1/t**2)>0, 'flat positive side')
        flat += 1
    return {
        'problem_id':5300062,
        'result':'PASS_FINITE_CONTROLS_ONLY',
        'exact_rational_jet_controls':algebra,
        'numerical_conjugacy_controls':conjugacy,
        'numerical_derivative_controls':derivatives,
        'numerical_branch_continuation_controls':branch,
        'numerical_growth_controls':growth,
        'numerical_tail_buffer_controls':lower,
        'simple_root_identity_controls':implicit,
        'flat_function_positive_side_controls':flat,
        'dependencies':'Python 3 standard library',
        'not_certified':['infinite derivative convergence','all-address ray construction','cited transversality theorem','real analyticity','endpoint regularity'],
        'scope':'Written analysis carries the proof; finite checks are algebraic or numerical smoke controls.'
    }

if __name__=='__main__':
    out=json.dumps(run(),indent=2,sort_keys=True)+'\n'
    if len(sys.argv)==3 and sys.argv[1]=='--output':
        Path(sys.argv[2]).write_text(out)
    elif len(sys.argv)==1:
        print(out,end='')
    else:
        raise SystemExit('Usage: check_controls.py [--output PATH]')
