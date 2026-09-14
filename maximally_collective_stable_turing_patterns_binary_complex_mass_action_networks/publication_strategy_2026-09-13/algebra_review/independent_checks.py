"""Bounded independent checks reconstructed from manuscript reactions.

No project verifier imports. Exact computations use SymPy; numerical stress
checks are explicitly separate. This is regression evidence, not an all-m proof.
Run: /usr/local/bin/python independent_checks.py
"""
import itertools as it
import json
from datetime import datetime, timezone
from pathlib import Path
import sympy as s
import numpy as np


def reaction_data(m, a, b):
    n = m + 1
    e = [s.eye(n)[:, i] for i in range(n)]
    zero = s.zeros(n, 1)
    reactions = [(zero, e[0])]
    reactions += [(e[0] + e[i], e[0] + e[i+1]) for i in range(1, m-2)]
    reactions += [(e[0]+e[m-2], 2*e[m-1]), (2*e[m-1], e[1]),
                  (2*e[m], e[0]+e[m-1]), (e[0]+e[m-1], 2*e[m])]
    Y = s.Matrix.hstack(*(u for u, v in reactions))
    Gamma = s.Matrix.hstack(*(v-u for u, v in reactions))
    flux = [a]*m + [b,b]
    return Gamma, Y, Gamma*s.diag(*flux)*Y.T


def scc_closure(M, I):
    # Transitive closure, independently of repository Tarjan implementation.
    reach = {(i,j): i == j or M[j,i] != 0 for i in I for j in I}
    for k in I:
        for i in I:
            for j in I:
                reach[i,j] = reach[i,j] or (reach[i,k] and reach[k,j])
    return set(tuple(j for j in I if reach[i,j] and reach[j,i]) for i in I)


def is_hurwitz(M):
    coeff = M.charpoly().all_coeffs()
    n = M.rows
    hurwitz = s.Matrix(n,n,lambda i,j: coeff[2*j-i+1] if 0 <= 2*j-i+1 <= n else 0)
    return all(hurwitz[:k,:k].det() > 0 for k in range(1,n+1))


report = {'timestamp_utc':datetime.now(timezone.utc).isoformat(), 'checks':[]}
def record(msg):
    print(msg, flush=True)
    report['checks'].append(msg)

a,b = s.symbols('a b', positive=True)
h1,hm,hz=s.symbols('h1 hm hz',positive=True)
_,_,test_A=reaction_data(4,a,b)
triad=test_A.extract([0,3,4],[0,3,4])*s.diag(h1,hm,hz)
coeff=triad.charpoly().all_coeffs()
gap=s.Poly(s.expand(coeff[1]*coeff[2]-coeff[3]),a,b,h1,hm,hz)
assert len(gap.terms())==14 and all(c>0 for _,c in gap.terms())
for k in [1,2]:
    for I in it.combinations(range(3),k):
        for coefficient in triad.extract(I,I).charpoly().all_coeffs():
            assert all(c>0 for _,c in s.Poly(coefficient,a,b,h1,hm,hz).terms())
record('EXACT arbitrary-positive-H boundary triad: 14 positive Routh-gap monomials; every proper block Hurwitz')
for m in range(3,8):
    Gamma,Y,A = reaction_data(m,a,b)
    c = s.Matrix([0]+[4]*(m-2)+[2,1])
    assert c.T*Gamma == s.zeros(1,m+2)
    assert Gamma.rank() == m
    assert Gamma*s.Matrix([a]*m+[b,b]) == s.zeros(m+1,1)
    assert all(sum(Y[:,j]) <= 2 and sum(Y[:,j]+Gamma[:,j]) <= 2 for j in range(m+2))
    expected = [0]+[16*a**(m-1)*b]*(m-2)+[0,-2*a**(m-1)*b]
    for j in range(m+1):
        I = [i for i in range(m+1) if i != j]
        assert s.factor((-1)**m*A.extract(I,I).det(method='domain-ge')-expected[j]) == 0
    record(f'EXACT reaction conservation/rank/binary/omission identities: m={m}')

    for av,bv in [(s.Rational(3,2),s.Rational(5,3)), (s.Integer(1),s.Integer(2))]:
        H = s.diag(*[s.Rational(i+2,i+1) for i in range(m+1)])
        J = A.subs({a:av,b:bv})*H
        seen = set()
        count = 0
        for k in range(1,m):
            for I in it.combinations(range(m+1),k):
                count += 1
                for C in scc_closure(J,I):
                    assert len(C) == 1 or set(C) <= {0,m-1,m} or C in [tuple(range(m-1)),tuple(range(1,m))]
                    if C not in seen:
                        assert is_hurwitz(J.extract(C,C)), (m,av,bv,C)
                        seen.add(C)
        record(f'EXACT SCC classification and Hurwitz blocks: m={m}, a={av}, b={bv}, {count} principal subsets')

    # Independent exact selected-profile and contrast reconstruction.
    nu = m-2
    K = lambda i: 91*m-181-i
    D = s.diag(s.Rational(23,63),*[1/s.Integer(K(i)) for i in range(2,m)],s.Rational(1,7),s.Rational(16,45))
    r = s.Matrix([1]+[-s.Rational(K(i),63*nu) for i in range(2,m)]+[-s.Rational(2,9),s.Rational(5,14)])
    A1 = A.subs({a:1,b:1})
    assert (A1-D)*r == s.zeros(m+1,1)
    assert is_hurwitz(A1.extract(range(m),range(m))) is False  # core is unstable
    lam = s.Symbol('lam')
    fullpoly = A1.charpoly(lam).as_expr()
    q = s.Poly(s.cancel(fullpoly/lam),lam)
    coeff=q.all_coeffs(); N=q.degree()
    HM=s.Matrix(N,N,lambda i,j:coeff[2*j-i+1] if 0<=2*j-i+1<=N else 0)
    assert all(HM[:k,:k].det()>0 for k in range(1,N+1))
    for L in [s.sqrt(s.Rational(1,3)) if nu==1 else s.sqrt(s.Rational(5,4*nu)),s.Rational(90*nu,90*nu+1)]:
        h=[s.Integer(1)]+[s.Rational(K(i),K(i-1))/L for i in range(2,m)]+[s.Integer(1),s.Integer(1)]
        ds=[h[i]*D[i,i] for i in range(m+1)]
        chih=max(h)/min(h); chid=max(ds)/min(ds)
        assert s.simplify(chih-s.Rational(91*nu-1,91*nu)/L)==0
        assert s.simplify(chid-s.Rational(23*91*nu,63)*L)==0
        assert s.simplify(chih*chid-s.Rational(23*(91*nu-1),63))==0
    record(f'EXACT homogeneous stability, critical vector, scaled endpoint contrasts: m={m}')

# Exact ray-polynomial boundary tests, including the theorem endpoint n=2.
z,t=s.symbols('z t')
examples=[(s.Matrix([[1,2],[-2,-4]]),s.diag(1,10),'n=2')]
for m in [3,4,5]:
    _,_,A=reaction_data(m,s.Integer(1),s.Integer(1))
    for offset in [-1,0,1]:
        examples.append((A,s.diag(*([1]*m+[8*(m-2)+offset])),f'm={m}, threshold offset={offset}'))
for J,D,label in examples:
    n=J.rows
    expression=s.Poly((z*s.eye(n)+t*D-J).det(method='domain-ge'),z,t)
    independently_expanded=0
    for k in range(n+1):
        for I in it.combinations(range(n),k):
            minor=(-1)**k*J.extract(I,I).det() if k else s.Integer(1)
            independently_expanded += minor*s.prod(z+t*D[j,j] for j in range(n) if j not in I)
    assert s.expand(expression.as_expr()-independently_expanded)==0
    derivative=s.Poly(s.diff(expression.as_expr(),z),z,t)
    assert all(coef>0 for monomial,coef in derivative.terms())
    quotient=s.Poly(s.cancel(expression.as_expr().subs(z,0)/t),t)
    assert all(coef>0 for coef in quotient.all_coeffs()[:-1])
    record(f'EXACT principal-minor expansion / positive derivative coefficients / monotone ray bracket: {label}, beta1={quotient.eval(0)}')

# Non-proof stress test across substantial diagonal scaling and edge cancellation.
rng=np.random.default_rng(20260913)
worst=-float('inf'); trials=0
for m in [3,4,5,8,12]:
    for j in range(12):
        av,bv = np.exp(rng.uniform(-3,3,2))
        if j==0: bv=2*av
        _,_,A=reaction_data(m,float(av),float(bv))
        h=np.exp(rng.uniform(-5,5,m+1)); J=np.array(A,dtype=float)*h
        for k in range(1,m):
            I=sorted(rng.choice(m+1,k,replace=False))
            top=np.linalg.eigvals(J[np.ix_(I,I)]).real.max()
            assert top<0,(m,I,top)
            worst=max(worst,float(top)); trials+=1
record(f'NUMERICAL ONLY random smaller-subsystem eigenvalue tests: {trials}, largest observed spectral abscissa={worst}')
report['status']='PASS'
Path(__file__).with_name('independent_checks_results.json').write_text(json.dumps(report,indent=2)+'\n')
