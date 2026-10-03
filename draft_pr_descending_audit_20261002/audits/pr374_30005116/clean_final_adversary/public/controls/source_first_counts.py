#!/usr/bin/env python3
"""Original exact-count controls written without candidate access."""
from fractions import Fraction as Q
from itertools import combinations, product
import json

def matrix(n,mask):
    w=[[0]*n for _ in range(n)]
    for bit,(i,j) in enumerate(combinations(range(n),2)):
        w[i][j]=w[j][i]=(mask>>bit)&1
    return w

def subset_c4(w):
    n=len(w)
    return sum(all(sum(w[i][j] for j in s)==2 for i in s) for s in combinations(range(n),4))

def direct(w,a):
    p=sum(a[i]*a[j]*w[i][j] for i,j in product(range(len(a)),repeat=2))
    j=Q(0)
    for i,k,l,m in product(range(len(a)),repeat=4):
        j+=a[i]*a[k]*a[l]*a[m]*w[i][k]*w[k][l]*w[l][m]*w[m][i]*(1-w[i][l])*(1-w[k][m])
    return p,3*j

def compositions(n):
    if n==0:
        yield ()
    else:
        for first in range(1,n+1):
            for rest in compositions(n-first): yield (first,)+rest

def main():
    graphs=0
    for n in range(1,6):
        for mask in range(1<<(n*(n-1)//2)):
            w=matrix(n,mask); e=mask.bit_count(); count=subset_c4(w)
            assert 4*count<=e*(e-1)
            if n>=4:
                pg=Q(2*e,n*(n-1)); qg=Q(24*count,n*(n-1)*(n-2)*(n-3))
                pw,qw=direct(w,[Q(1,n)]*n)
                assert pw==pg*(1-Q(1,n))
                assert abs(qw-qg)<=Q(18,n)
            graphs+=1
    partitions=0
    for masses in compositions(8):
        a=[Q(x,8) for x in masses]
        w=[[int(i!=j) for j in range(len(a))] for i in range(len(a))]
        p,q=direct(w,a); s2=sum(x*x for x in a); s4=sum(x**4 for x in a)
        assert p==1-s2 and q==3*(s2*s2-s4)
        partitions+=1
    rankone=0
    for values in product((Q(0),Q(1,3),Q(2,3),Q(1)),repeat=3):
        a=[Q(1,3)]*3
        w=[[x*y for y in values] for x in values]
        m=sum(x/3 for x in values); s=sum(x*x/3 for x in values); t=sum(x**3/3 for x in values)
        p,q=direct(w,a)
        assert p==m*m and q==3*(s*s-t*t)**2
        if 0<m<1:
            assert m*m<=s<=m
            assert s*s/m<=t<=s-(m-s)**2/(1-m)
        rankone+=1
    print(json.dumps({'status':'PASS','exact_graphs':graphs,'multipartite_compositions':partitions,'rankone_distributions':rankone,'scope':'finite falsification controls only; proofs are separate'},sort_keys=True))

if __name__=='__main__': main()
