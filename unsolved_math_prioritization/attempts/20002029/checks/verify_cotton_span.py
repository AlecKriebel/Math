#!/usr/bin/env python3
"""Exact finite checks of identities used in Attempt 2; not a proof by sampling."""
from fractions import Fraction as Q
from itertools import product
import json

def check(n):
    ids=range(n)
    A={(k,i,j):Q(((k+1)*17+(i+j+2)*7+(i+1)*(j+1)*3)%13-6) for k,i,j in product(ids, repeat=3)}
    T={(k,i,j):A[k,i,j]-(A[k,i,j]+A[i,k,j]+A[j,i,k])/3 for k,i,j in product(ids,repeat=3)}
    t={k:sum(T[k,i,i] for i in ids) for k in ids}
    for k,i,j in T:
        T[k,i,j]-=(t[k]*(i==j)-(t[i]*(k==j)+t[j]*(k==i))/2)/(n-1)
    C={(i,j,k):T[k,i,j]-T[j,i,k] for i,j,k in product(ids,repeat=3)}
    assert any(C.values())
    assert all(C[i,j,k]==-C[i,k,j] and C[i,j,k]+C[j,k,i]+C[k,i,j]==0 for i,j,k in C)
    assert all(sum(C[i,i,k] for i in ids)==0 for k in ids)
    assert all(T[k,i,j]==(C[i,j,k]+C[j,i,k])/3 for k,i,j in T)
    out={q:Q(0) for q in C}
    for a in ids:
        R={(i,j,k,l): (i==a)*C[j,k,l]-(j==a)*C[i,k,l]+(k==a)*C[l,i,j]-(l==a)*C[k,i,j] for i,j,k,l in product(ids,repeat=4)}
        ric={(j,l):sum(R[i,j,i,l] for i in ids) for j,l in product(ids,repeat=2)}
        W={(i,j,k,l):R[i,j,k,l]-(ric[i,k]*(j==l)+ric[j,l]*(i==k)-ric[i,l]*(j==k)-ric[j,k]*(i==l))/(n-2) for i,j,k,l in R}
        assert all(W[i,j,k,l]==-W[j,i,k,l] and W[i,j,k,l]==W[k,l,i,j] and W[i,j,k,l]+W[i,k,l,j]+W[i,l,j,k]==0 for i,j,k,l in W)
        assert all(sum(W[i,j,i,l] for i in ids)==0 for j,l in ric)
        for j,k,l in out:out[j,k,l]+=W[a,j,k,l]
    b=Q(n-2,n+1)
    def h3(i,j,a,b_,c):
        return -2*b*(T[a,i,j]*(b_==c)+T[b_,i,j]*(a==c)+T[c,i,j]*(a==b_))
    Ric1={(k,i,j):sum(h3(j,a,a,i,k)+h3(i,a,a,j,k)-h3(i,j,a,a,k)-h3(a,a,i,j,k) for a in ids)/2 for k,i,j in T}
    assert all(Ric1[k,i,j]==(n-2)*T[k,i,j] for k,i,j in T)
    coefficient=Q((n-3)*(n+1),n-2)
    assert all(out[q]==coefficient*C[q] for q in C)
    return {'dimension':n,'coefficient':str(coefficient),'cotton_norm_squared':str(sum(v*v for v in C.values())),'passed':True}
if __name__=='__main__':
    print(json.dumps({'checks':[check(n) for n in range(4,9)],'scope':'exact tests of displayed tensor identities, not an exhaustive invariant classification'},indent=2))
