#!/usr/bin/env python3
"""Independent exact-coordinate spot checks of Chen--Zhang (2026).

This is a diagnostic, not a proof over all points or parameters. It builds
the Levi--Civita tensor directly from metric derivatives, without using
the paper's submersion curvature formulas in that computation.
Requires SymPy; run: python3 check_metric.py
Source: https://arxiv.org/abs/2609.08119v1, equations (2), (18)--(22).
"""
import itertools
import json
import sympy as s

u, v = s.symbols('u v', real=True)
epsilon = s.Rational(1, 4)
coordinates = (u, v)
den = 1 + u*u + v*v
X1 = s.Matrix([-u*v, (u*u-v*v-1)/2])
X2 = s.Matrix([(1+u*u-v*v)/2, u*v])
P = s.eye(4)
P[:2, 2] = -epsilon*X1
P[:2, 3] = -epsilon*X2
metric = P.T*s.diag(4/den**2, 4/den**2, 1, 1)*P
first = [metric.diff(q) for q in coordinates] + [s.zeros(4), s.zeros(4)]
second = [[first[i].diff(coordinates[j]) if j < 2 else s.zeros(4)
           for j in range(4)] for i in range(4)]
pairs = list(itertools.combinations(range(4), 2))


def check_point(a, b):
    subs = {u: s.Rational(a), v: s.Rational(b)}
    g = metric.subs(subs)
    gi = g.inv()
    dg = [x.subs(subs) for x in first]
    ddg = [[x.subs(subs) for x in row] for row in second]
    dgi = [-gi*x*gi for x in dg]
    Gamma = [[[sum(gi[k,l]*(dg[i][l,j]+dg[j][l,i]-dg[l][i,j])
                    for l in range(4))/2 for j in range(4)]
               for i in range(4)] for k in range(4)]
    dGamma = [[[[sum(dgi[a][k,l]*(dg[i][l,j]+dg[j][l,i]-dg[l][i,j])
                         +gi[k,l]*(ddg[i][a][l,j]+ddg[j][a][l,i]-ddg[l][a][i,j])
                         for l in range(4))/2 for j in range(4)]
                    for i in range(4)] for k in range(4)] for a in range(4)]
    # R^l_{kij} = (R(partial_i, partial_j) partial_k)^l.
    R = [[[[dGamma[i][l][j][k]-dGamma[j][l][i][k]
             +sum(Gamma[l][i][m]*Gamma[m][j][k]
                  -Gamma[l][j][m]*Gamma[m][i][k] for m in range(4))
             for j in range(4)] for i in range(4)]
           for k in range(4)] for l in range(4)]
    RC = s.Matrix(6, 6, lambda A, B: sum(g[l,pairs[B][0]]
                  *R[l][pairs[B][1]][pairs[A][0]][pairs[A][1]]
                  for l in range(4)))
    h = den.subs(subs)/2
    E = s.eye(4)
    E[0,0] = E[1,1] = h
    E[:2,2] = epsilon*X1.subs(subs)
    E[:2,3] = epsilon*X2.subs(subs)
    assert E.T*g*E == s.eye(4)
    exterior = s.Matrix(6, 6, lambda A,B:
         E[pairs[A][0],pairs[B][0]]*E[pairs[A][1],pairs[B][1]]
        -E[pairs[A][1],pairs[B][0]]*E[pairs[A][0],pairs[B][1]])
    RF = exterior.T*RC*exterior
    assert RF == RF.T
    X3 = s.Matrix([-subs[v],subs[u]])
    f = -epsilon**2*X3/h
    d1 = -epsilon**3*X2.subs(subs)/h
    d2 = epsilon**3*X1.subs(subs)/h
    z = ((1-u*u-v*v)/den).subs(subs)
    q = -epsilon**2*z
    expected = s.zeros(6)
    def entry(A,B,value):
        expected[A,B] = expected[B,A] = value
    entry(0,0,1)
    entry(5,5,-s.Rational(3,4)*f.dot(f))
    entry(0,5,q)
    for A in (1,2): entry(A,A,f[0]**2/4)
    for A in (3,4): entry(A,A,f[1]**2/4)
    entry(1,3,f[0]*f[1]/4)
    entry(2,4,f[0]*f[1]/4)
    entry(1,4,q/2)
    entry(2,3,-q/2)
    entry(5,1,-d1[0]/2)
    entry(5,2,-d2[0]/2)
    entry(5,3,-d1[1]/2)
    entry(5,4,-d2[1]/2)
    assert RF == expected
    # Hodge matrices without sqrt(2); final block is T^t R T / 2.
    blocks = []
    for sign in (1,-1):
        T = s.zeros(6,3)
        T[0,0],T[5,0] = 1,sign
        T[1,1],T[4,1] = 1,-sign
        T[2,2],T[3,2] = 1,sign
        blocks.append(T.T*RF*T/2)
    rho = f.dot(f)
    for sign,A in zip((1,-1),blocks):
        assert A[0,0] == s.Rational(1,2)-3*rho/8+sign*q
        assert A[1,1] == A[2,2] == rho/8-sign*q/2
        assert A[1,2] == 0
    return {'stereographic_point':[str(a),str(b)],
            'epsilon':str(epsilon),'all_36_curvature_entries_match':True,
            'both_hodge_blocks_match':True}


if __name__ == '__main__':
    points = [(0,0),(1,0),(0,1),(1,1),(s.Rational(1,2),s.Rational(1,3)),(2,-1)]
    report = [check_point(a,b) for a,b in points]
    assert s.Rational(1,2)-epsilon**4/2-3*epsilon**2/2 == s.Rational(207,512)
    assert s.Rational(1,24)-s.Rational(1,32) == s.Rational(1,96)
    assert epsilon**4/s.Integer(384) == s.Rational(1,98304)
    assert epsilon**4/(24*(1+epsilon**2)) == s.Rational(1,6528)
    print(json.dumps({'source':'Chen--Zhang arXiv:2609.08119v1',
        'classification':'exact spot-check diagnostic, not a global proof',
        'points':report,'rational_constants_match':True},indent=2))
