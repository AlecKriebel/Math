"""Bounded independent mechanism controls; no deposited program is executed.

This is not an all-algebra or all-degree computational proof. The universal
arguments are written separately in DERIVATIONS.md. Writes only its own JSON.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction
from datetime import datetime, timezone
import json
import sympy as s

rows = []
E = []
for i, j in product(range(2), repeat=2):
    a = s.zeros(2); a[i, j] = 1; E.append(a)
vec = lambda x: s.Matrix(list(x))
mat = lambda x: s.Matrix(2, 2, list(x))
H = s.Matrix([[s.Rational(((i+2)*(j+3)) % 11 - 5, 100)
               for j in range(4)] for i in range(4)])
h = lambda a: mat(H * vec(a))
G = s.eye(4) + H
g = lambda a: mat(G * vec(a))
b = lambda a: mat(G.inv() * vec(a))

# An arbitrary bilinear defect tests the exact formula independently of
# associativity; all 16 basis pairs suffice for this finite bilinear identity.
table = [[s.Matrix(2, 2, [s.Rational((i*7+j*3+k*5) % 13-6, 31)
                         for k in range(4)]) for j in range(4)] for i in range(4)]
def delta(a, c):
    out = s.zeros(2)
    for i in range(4):
        for j in range(4):
            out += vec(a)[i] * vec(c)[j] * table[i][j]
    return out
dh = lambda a, c: a*h(c)-h(a*c)+h(a)*c
correct, omitted_right = 0, 0
for x, y in product(E, repeat=2):
    a, c = b(x), b(y)
    actual = g(a*c+delta(a,c))-x*y
    expected = delta(a,c)-dh(a,c)+h(delta(a,c))-h(a)*h(c)
    if actual != expected: raise RuntimeError('transport identity')
    correct += 4
    bad = delta(a,c)-(a*h(c)-h(a*c))+h(delta(a,c))-h(a)*h(c)
    omitted_right += int(actual != bad)
if omitted_right == 0: raise RuntimeError('negative transport control ineffective')
rows.append(dict(name='exact transported-product identity', scalar_equalities=correct,
                 bad_omitted_right_term_rejected_pairs=omitted_right))

# Pull back an actual associative product. Check the associator/differential
# sign on all 64 triples, including noncommuting matrix units.
mu = lambda a,c: b(g(a)*g(c))
D = lambda a,c: mu(a,c)-a*c
assoc_checks = 0; wrong_sign_rejections = 0
for a,c,e in product(E,repeat=3):
    lhs=a*D(c,e)-D(a*c,e)+D(a,c*e)-D(a,c)*e
    rhs=D(D(a,c),e)-D(a,D(c,e))
    if lhs != rhs: raise RuntimeError('associator sign')
    assoc_checks += 4
    wrong_sign_rejections += int(lhs != -rhs)
rows.append(dict(name='associativity defect differential', scalar_equalities=assoc_checks,
                 wrong_sign_rejected_triples=wrong_sign_rejections))

# Deterministic generic complex multilinear cochains, independent of the
# cohomology equation. Thus the degree-three reversal sign cannot hide behind
# a zero cocycle or real-only input.
def f(n):
    def call(xs):
        out=s.zeros(2)
        for inds in product(range(4),repeat=n):
            c=s.prod(vec(x)[i] for x,i in zip(xs,inds))
            for j in range(4):
                out[j] += c*(sum((k+1)*(i+2) for k,i in enumerate(inds))+j+1
                             +s.I*(j+1)*(1+sum(inds)))
        return out
    return call
def deriv(F,n):
    def call(xs):
        z=xs[0]*F(xs[1:])
        for j in range(n):
            z+=(-1)**(j+1)*F(xs[:j]+(xs[j]*xs[j+1],)+xs[j+2:])
        return z+(-1)**(n+1)*F(xs[:-1])*xs[-1]
    return call
def reversal(F,n,sign=None):
    q=(-1)**((n-1)*(n-2)//2) if sign is None else sign
    return lambda xs:q*F(tuple(x.conjugate().T for x in reversed(xs))).conjugate().T
for n in (1,2,3):
    F=f(n); lhs=deriv(reversal(F,n),n); rhs=reversal(deriv(F,n),n+1)
    checked=0; bad=0
    bad_rhs=reversal(deriv(F,n),n+1,sign=-(-1)**(n*(n-1)//2))
    for xs in product(E,repeat=n+1):
        if lhs(xs)!=rhs(xs): raise RuntimeError(('signed reversal',n))
        checked+=4;bad+=int(lhs(xs)!=bad_rhs(xs))
    if not bad: raise RuntimeError('negative reversal control ineffective')
    rows.append(dict(name='signed involution chain map',degree=n,
                     scalar_equalities=checked,opposite_sign_rejected_tuples=bad))

# Exact separation diagnostic for ordinary versus completely bounded norms.
# Flip has norm one; its partial transpose is rank-one Omega Omega*, norm n.
for n in (2,3,4,5):
    flip=s.zeros(n*n);omega=s.zeros(n*n,1)
    for i,j in product(range(n),repeat=2):flip[i*n+j,j*n+i]=1
    for i in range(n):omega[i*n+i]=1
    partial=s.zeros(n*n)
    for a,c,i,j in product(range(n),repeat=4):
        partial[a*n+j,c*n+i]=flip[a*n+i,c*n+j]
    if flip.T*flip!=s.eye(n*n) or partial!=omega*omega.T:
        raise RuntimeError('partial transpose witness')
    if partial*omega!=n*omega:raise RuntimeError('norm eigenvalue')
    rows.append(dict(name='ordinary/cb transpose distinction',n=n,
                     flip_norm=1,partial_transpose_norm=n,
                     universal_statement='ordinary transpose is isometric; this witness gives cb norm >=n'))

# Rational upper controls only. These do not estimate the unknown K,L for an
# arbitrary infinite algebra. e^{-x}<=x^{-2} for x>=2 replaces the exponential
# term by ell*p_ell, making the displayed bound wholly rational.
walk=[]
for ell in range(1,10):
    p=Fraction(1,2**(2**ell));root=Fraction(1,2**(2**(ell-1)))
    n=2**(3*2**(ell-1));K=ell*n
    bound=Fraction(16,15)*ell*root+Fraction(1,K)+Fraction(1,2*K*K)+ell*p
    walk.append(dict(ell=ell,upper_bound_float=float(bound),p0_lower_bound='2/3'))
if not all(walk[i+1]['upper_bound_float']<walk[i]['upper_bound_float'] for i in range(8)):
    raise RuntimeError('walk bound diagnostic')
rows.append(dict(name='walk bad-event rational bounds',cases=walk))
carrier=[]
for m in (10,20,40):
    root=Fraction(1,10**m);t=root*root;upper=284*(1+t)*root
    if not upper<1:raise RuntimeError('carrier bound')
    carrier.append(dict(t='10^-'+str(2*m),carrier_upper_float=float(upper)))
rows.append(dict(name='carrier sufficient smallness diagnostic',cases=carrier,
                 universal_reason='sqrt(2t+t^2)<=2sqrt(t) for 0<=t<=1'))
result=dict(utc=datetime.now(timezone.utc).isoformat(),status='COMPLETE',
            limitation='Finite exact diagnostics only; universal proofs and exact external input remain necessary.',
            no_deposited_program_executed=True,rows=rows)
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(status=result['status'],families=len(rows),
                     scalar_equalities=sum(x.get('scalar_equalities',0) for x in rows))))
