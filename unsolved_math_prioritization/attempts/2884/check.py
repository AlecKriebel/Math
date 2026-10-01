#!/usr/bin/env python3
"""Independent author arithmetic controls; not a formal topology proof."""
from itertools import permutations
from math import comb
import json
checks=0
def ck(p):
    global checks
    assert p
    checks+=1
def trim(p):
    p=list(p)
    while len(p)>1 and p[-1]==0:p.pop()
    return p
def add(a,b):
    c=[0]*max(len(a),len(b))
    for i,x in enumerate(a):c[i]+=x
    for i,x in enumerate(b):c[i]+=x
    return trim(c)
def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return trim(c)
def detpoly(A):
    out=[0]
    for p in permutations(range(len(A))):
        inv=sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))
        term=[(-1)**inv]
        for i,j in enumerate(p):term=mul(term,A[i][j])
        out=add(out,term)
    return out
def mm(A,B):return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def mp(A,n):
    R=[[1,0],[0,1]]
    for _ in range(n):R=mm(R,A)
    return R
A=[[1,1],[0,1]];B=[[1,0],[-1,1]];I=[[1,0],[0,1]]
ck(mm(mm(A,B),A)==mm(mm(B,A),B))
ck(mp(mm(A,B),6)==I)
ck(mp(mm(A,B),12)==I)
ck(mm(mm(mm(A,B),A),B)==mm(mm(mm(A,A),B),A))
polys=[]
for q in (3,5):
    n=q-1
    ck(q%2==1) # single component of positive 2-braid
    ck((q-1)//2==n//2)
    V=[[int(i==j)-int(j==i+1) for j in range(n)] for i in range(n)]
    P=detpoly([[[-V[j][i],V[i][j]] for j in range(n)] for i in range(n)])
    ck(P==[(-1)**i for i in range(q)])
    ck(mul(P,[1,1])==[1]+[0]*(q-1)+[1])
    ck(len(P)-1==2*((q-1)//2))
    ck(sum(P)==1)
    ck(P==P[::-1])
    ck(abs(sum(a*(-1)**i for i,a in enumerate(P)))==q)
    polys.append(P)
ck(polys[0]!=polys[1])
ck((-1)**2-4==-3)
# Phi_5(x+1), coefficient order increasing.
E=[sum(comb(j,i) for j in range(i,5)) for i in range(5)]
ck(E==[5,10,10,5,1])
ck(E[-1]%5!=0)
ck(all(a%5==0 for a in E[:-1]))
ck(E[0]%25!=0)
# Under standard E(2), chi=24, signature=-16; H adds chi 4 and signature 0.
ck(24+4-2==26)
ck((3+1,19+1)==(4,20))
ck(2+4+20==26)
ck(4-20==-16)
print(json.dumps({'status':'PASS','assertions':checks,'polynomials_in_increasing_order':polys,'eisenstein_shift':E,'scope':'Finite exact controls only; stabilization, complement and gluing require written source audit.'},sort_keys=True,indent=2))
