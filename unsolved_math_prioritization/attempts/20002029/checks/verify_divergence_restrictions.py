#!/usr/bin/env python3
"""Exact Ricci-flat witnesses for Case et al. (2026), v4 equation (3.4)."""
from fractions import Fraction as Q
from itertools import product
import json

def evaluate(p):
    n=len(p)+1; ids=range(n)
    assert sum(p)==sum(x*x for x in p)==1
    K=[[Q(0) for b in ids] for a in ids]
    for i in range(1,n): K[0][i]=K[i][0]=p[i-1]*(1-p[i-1])
    for i in range(1,n):
        for j in range(i+1,n): K[i][j]=K[j][i]=-p[i-1]*p[j-1]
    assert all(sum(row)==0 for row in K)
    R={(a,b,c,d):K[a][b]*((a==c)*(b==d)-(a==d)*(b==c)) for a,b,c,d in product(ids,repeat=4)}
    t1=[2*sum(K[a][c]*sum(x*x for x in K[c]) for c in ids) for a in ids]
    t2=[4*sum(x**3 for x in K[a]) for a in ids]
    # Independent direct component contractions, including off-diagonal zero tests.
    M={(c,d):sum(R[c,e,f,g]*R[d,e,f,g] for e,f,g in product(ids,repeat=3)) for c,d in product(ids,repeat=2)}
    for a,b in product(ids,repeat=2):
        raw1=sum(R[a,c,b,d]*M[c,d] for c,d in product(ids,repeat=2))
        raw2=Q(0)
        for c,d,e in product(ids,repeat=3):
            x=R[a,c,d,e]
            if x:
                raw2+=x*sum(R[b,c,f,g]*R[d,e,f,g] for f,g in product(ids,repeat=2))
        assert raw1==(t1[a] if a==b else 0)
        assert raw2==(t2[a] if a==b else 0)
    A=sum(t2)
    U1=30*t1[0]+6*sum(pi*ti for pi,ti in zip(p,t1[1:]))
    U2=30*t2[0]+6*sum(pi*ti for pi,ti in zip(p,t2[1:]))-6*A
    return U1,U2

if __name__=='__main__':
    ps=[(Q(-1,3),Q(2,3),Q(2,3),0,0,0,0),(Q(-1,2),Q(1,2),Q(1,2),Q(1,2),0,0,0)]
    rows=[evaluate(p) for p in ps]
    assert rows==[(Q(0),Q(-256,81)),(Q(-63,4),Q(-45,2))]
    det=rows[0][0]*rows[1][1]-rows[0][1]*rows[1][0]
    assert det==Q(-448,9)
    print(json.dumps({'dimension':8,'exponents':[[str(x) for x in p] for p in ps],'rows':[[str(x)for x in row] for row in rows],'determinant':str(det),'passed':True},indent=2))
