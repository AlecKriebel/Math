#!/usr/bin/env python3
"""Detached exact reconstruction of every finite number in current_profile_exact.json.

This script does not import the table generator or any precomputed table row.
It builds Gamma,Y,A and the Hessian from the indexed reactions, solves the
zero- and second-harmonic systems directly, and compares exact rationals.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'data'/'current_profile_exact.json').read_text())


def reaction_matrices(m:int):
    n=m+1
    def v(items=None):
        z=[0]*n
        for i,a in (items or {}).items(): z[i]=a
        return sp.Matrix(z)
    rx=[(v(),v({0:1}))]
    for i in range(2,m-1): rx.append((v({0:1,i-1:1}),v({0:1,i:1})))
    rx += [(v({0:1,m-2:1}),v({m-1:2})),(v({m-1:2}),v({1:1})),
           (v({m:2}),v({0:1,m-1:1})),(v({0:1,m-1:1}),v({m:2}))]
    Y=sp.Matrix.hstack(*(a for a,b in rx)); Yp=sp.Matrix.hstack(*(b for a,b in rx))
    return Yp-Y,Y


def Bmap(G,Y,u,v):
    ans=sp.zeros(G.rows,1)
    for k in range(Y.cols):
        q=0
        for i in range(Y.rows):
            yi=int(Y[i,k]); q += yi*(yi-1)*u[i]*v[i]
            for j in range(i+1,Y.rows):
                yj=int(Y[j,k]); q += yi*yj*(u[i]*v[j]+u[j]*v[i])
        ans += q*G[:,k]
    return sp.simplify(ans)


def sx(x): return sp.sympify(x,locals={'sqrt':sp.sqrt})

for z in DATA['rows']:
    m=int(z['m']); G,Y=reaction_matrices(m)
    A=sp.Matrix(G*sp.eye(m+2)*Y.T)  # all m+2 unit fluxes
    K=lambda i:91*m-181-i
    r=sp.Matrix([1]+[-sp.Rational(K(i),63*(m-2)) for i in range(2,m)]+[-sp.Rational(2,9),sp.Rational(5,14)])
    d=[sp.Rational(23,63)]+[sp.Rational(1,K(i)) for i in range(2,m)]+[sp.Rational(1,7),sp.Rational(16,45)]
    D=sp.diag(*d)
    ell=sp.Matrix([-sp.Rational(266,815)]+[sp.Rational(78260*(m-2),163*(91*m-180-i)) for i in range(2,m)]+[sp.Rational(18368,7335),1])
    c=sp.Matrix([0]+[4]*(m-2)+[2,1])
    assert (A-D)*r==sp.zeros(m+1,1)
    assert (A-D).T*ell==sp.zeros(m+1,1)
    rhs=-sp.Rational(1,4)*Bmap(G,Y,r,r)
    M=A.copy(); q=sp.Matrix(rhs); M[m,:]=c.T; q[m]=0
    w0=M.inv()*q
    w2=(A-4*D).inv()*rhs
    numerator=sp.factor((ell.T*(Bmap(G,Y,r,w0)+sp.Rational(1,2)*Bmap(G,Y,r,w2)))[0])
    ellr=sp.factor((ell.T*r)[0]); ellDr=sp.factor((ell.T*D*r)[0])
    eta=sp.factor(ellDr/ellr); cubic=sp.factor(numerator/ellr)
    assert str(ellr)==z['ell_dot_r']
    assert str(ellDr)==z['ell_dot_Dr']
    assert str(eta)==z['eta']['exact']
    assert str(cubic)==z['cubic']['exact']
    assert [str(x) for x in r]==z['right_critical_vector']
    assert [str(x) for x in ell]==z['left_critical_vector']
    assert [str(x) for x in d]==z['diffusion_profile']

z3=DATA['rows'][0]
assert z3['eta']['exact']=='143636/7451873'
assert z3['eta']['decimal'].startswith('0.0192751540451642')
print('NUMERICAL_PROVENANCE_PASS')
