#!/usr/bin/env python3
"""Exact, standard-library-only replay for problem 30006060.
All polynomial coefficient lists run from degree zero upward.
No downloaded source material or external services are needed.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb, lcm
import json
import sys

checks = 0

def check(b):
    global checks
    assert b
    checks += 1

def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0: p.pop()
    return p

def add(a,b):
    c = [0]*max(len(a),len(b))
    for i,x in enumerate(a): c[i] += x
    for i,x in enumerate(b): c[i] += x
    return trim(c)

def neg(a): return [-x for x in a]
def sub(a,b): return add(a,neg(b))

def mul(a,b):
    c = [0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j] += x*y
    return trim(c)

def exactdiv(a,b):
    a = a[:]; q=[0]*max(1,(len(a)-len(b)+1))
    while len(a)>=len(b) and a != [0]:
        k=len(a)-len(b); check(a[-1]%b[-1]==0)
        c=a[-1]//b[-1];q[k]=c;a=sub(a,[0]*k+[c*x for x in b])
    check(a==[0]);return trim(q)

def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def transpose(M): return [list(r) for r in zip(*M)]
def matmul(A,B): return [[sum(x*y for x,y in zip(r,c)) for c in zip(*B)] for r in A]

def determinant(A):
    A=[[F(x) for x in r] for r in A]; ans=F(1);n=len(A)
    for j in range(n):
        k=next((k for k in range(j,n) if A[k][j]),None)
        if k is None:return F(0)
        if k!=j:A[j],A[k]=A[k],A[j];ans=-ans
        p=A[j][j];ans*=p
        for i in range(j+1,n):
            c=A[i][j]/p
            for k in range(j+1,n):A[i][k]-=c*A[j][k]
    return ans

def inverse(A):
    n=len(A);A=[[F(x) for x in r]+eye(n)[i] for i,r in enumerate(A)]
    for j in range(n):
        k=next(k for k in range(j,n) if A[k][j]);A[j],A[k]=A[k],A[j]
        p=A[j][j];A[j]=[x/p for x in A[j]]
        for i in range(n):
            if i!=j:
                c=A[i][j];A[i]=[x-c*y for x,y in zip(A[i],A[j])]
    return [r[n:] for r in A]

def pairing(Q,a,b):return sum(a[i]*Q[i][j]*b[j] for i in range(len(a)) for j in range(len(b)))
def unit(n,i):return [int(j==i) for j in range(n)]
def image(Q,a):return [sum(x*y for x,y in zip(r,a)) for r in Q]
def order(Q,a):return lcm(*(x.denominator for x in image(Q,a)))
def modone(a):return tuple(x%1 for x in a)
def ldl(A):
    n=len(A);L=eye(n);D=[]
    for j in range(n):
        d=F(A[j][j])-sum(L[j][k]**2*D[k] for k in range(j));check(d!=0);D.append(d)
        for i in range(j+1,n):L[i][j]=(A[i][j]-sum(L[i][k]*L[j][k]*D[k] for k in range(j)))/d
    check(matmul(matmul(L,[[D[i] if i==j else 0 for j in range(n)] for i in range(n)]),transpose(L))==A)
    return D

def burau(word):
    I=[[[1],[0]],[[0],[1]]]
    A=[[[0,-1],[1]],[[0],[1]]];B=[[[1],[0]],[[0,1],[0,-1]]]
    M=I
    for c in word:
        N=A if c==1 else B
        M=[[add(mul(M[i][0],N[0][j]),mul(M[i][1],N[1][j])) for j in range(2)] for i in range(2)]
    d=sub(mul(sub([1],M[0][0]),sub([1],M[1][1])),mul(M[0][1],M[1][0]))
    return exactdiv(d,[1,1,1])

def word(v):
    p,q,r,s=v;return [1]*p+[2]*q+[1]*r+[2]*s

def components(w):
    perm=list(range(3))
    for a in w:perm[a-1],perm[a]=perm[a],perm[a-1]
    seen=set();cycles=[]
    for i in range(3):
        if i in seen:continue
        c=[];j=i
        while j not in seen:seen.add(j);c.append(j+1);j=perm[j]
        cycles.append(c)
    return cycles

def seifert(v):
    # Basis: consecutive occurrences of sigma1, then of sigma2.
    # Collins's positive-crossing convention (positive trefoil signature -2).
    p,q,r,s=v;n=p+r-1;m=q+s-1;V=[[-int(i==j) for j in range(n+m)] for i in range(n+m)]
    for i in range(n-1):V[i+1][i]=1
    for i in range(m-1):V[n+i+1][n+i]=1
    V[p-1][n+q-1]=1
    return V

def interval_seifert(w):
    intervals=[]
    for i,a in enumerate(w):
        j=next((j for j in range(i+1,len(w)) if w[j]==a),None)
        if j is not None:intervals.append((a,i,j))
    intervals.sort()
    n=len(intervals);V=[[-int(i==j) for j in range(n)] for i in range(n)]
    for u,(a,i,h) in enumerate(intervals):
        for v,(b,j,k) in enumerate(intervals):
            if i>=j:continue
            if h==j:V[v][u]=1
            elif i<j<h<k and abs(a-b)==1:
                if a<b:V[u][v]=1
                else:V[v][u]=-1
    return V

def matchings(A):
    n=len(A)
    @lru_cache(None)
    def f(mask):
        if not mask:return (1,)
        v=(mask&-mask).bit_length()-1;rest=mask^(1<<v);ans=list(f(rest))
        for w in range(n):
            if rest>>w&1 and A[v][w]:ans=add(ans,[0]+list(f(rest^(1<<w))))
        return tuple(ans)
    return list(f((1<<n)-1))

def lcs(a,b):
    d=[[0]*(len(b)+1) for _ in range(len(a)+1)]
    for i,x in enumerate(a,1):
        for j,y in enumerate(b,1):d[i][j]=d[i-1][j-1]+1 if x==y else max(d[i-1][j],d[i][j-1])
    return d[-1][-1]

def analyze(v,other_index,c,expected_orders,expected_pairings):
    w=word(v);check(len(w)==18);check(len(components(w))==1)
    V=seifert(v);check(V==interval_seifert(w));n=len(V);check(n==16)
    S=[[-V[i][j]-V[j][i] for j in range(n)] for i in range(n)]
    A=[[2*int(i==j)-S[i][j] for j in range(n)] for i in range(n)]
    check(sum(map(sum,A))==2*(n-1))
    reach={0}
    while True:
        r=reach|{j for i in reach for j in range(n) if A[i][j]}
        if r==reach:break
        reach=r
    check(len(reach)==n)
    ms=matchings(A);cp=[0]*(n+1)
    for k,m in enumerate(ms):cp[n-2*k]=(-1)**k*m
    delta=[0]
    for k,m in enumerate(ms):
        delta=add(delta,[0]*k+[m*comb(n-2*k,j)*(-1)**j for j in range(n-2*k+1)])
    check(delta==burau(w));check(delta==delta[::-1]);check(sum(delta)==1)
    for t in range(-8,9):
        check(determinant([[V[i][j]-t*V[j][i] for j in range(n)] for i in range(n)])==sum(c*t**i for i,c in enumerate(delta)))
    check(sum(c*(-1)**i for i,c in enumerate(delta))==-243)
    check(determinant(S)==-243)
    check(determinant([[V[i][j]-V[j][i] for j in range(n)] for i in range(n)])==1)
    Q=inverse(S);check(matmul(S,Q)==eye(n))
    x=unit(n,0);y=unit(n,other_index);y[0]-=c
    check([order(Q,z) for z in (x,y)]==expected_orders)
    gram=[[pairing(Q,a,b)%1 for b in (x,y)] for a in (x,y)]
    check(gram==[[F(expected_pairings[0]),F(0)],[F(0),F(expected_pairings[1])]])
    elements={modone(image(Q,[a*x[i]+b*y[i] for i in range(n)])) for a in range(expected_orders[0]) for b in range(expected_orders[1])}
    check(len(elements)==243)
    D=ldl(S);check(sum(d>0 for d in D)==15);check(sum(d<0 for d in D)==1)
    return {'exponents':v,'word':w,'closure_permutation_cycles':components(w),'seifert_matrix':V,'positive_symmetrized_matrix':S,'matching_counts':ms,'adjacency_characteristic_coefficients':cp,'alexander_coefficients':delta,'determinant':243,'standard_signature':-14,'genus':(len(w)-2)//2,'tau':(len(w)-2)//2,'rasmussen_s':len(w)-2,'upsilon_at_1':-sum(v)//2+2,'cyclic_generators':{'x':x,'y':y},'cyclic_orders':expected_orders,'pairing_mod_1':[[str(t) for t in r] for r in gram],'ldl_positive_matrix':[str(t) for t in D]}

K=analyze([3,3,6,6],8,20,[27,9],['16/27','5/9'])
J=analyze([3,5,3,7],3,29,[81,3],['50/81','1/3'])
check(K['alexander_coefficients']==J['alexander_coefficients'])
check(K['matching_counts']==J['matching_counts'])
check(K['adjacency_characteristic_coefficients']==J['adjacency_characteristic_coefficients'])
factorization=mul(mul([1,-2,1],[1,2,1]),mul([-1,-3,9,4,-6,-1,1],[-1,3,9,-4,-6,1,1]))
check(factorization==K['adjacency_characteristic_coefficients'])
# Linking form on K # -J, in cyclic coordinates (x,y,x',y').
orders=[27,9,81,3];diag=[F(16,27),F(5,9),F(-50,81),F(-1,3)]
gens=[(3,0,0,1),(0,3,0,0),(0,0,9,0)]
for a in gens:
    for b in gens:check(sum(diag[i]*a[i]*b[i] for i in range(4)).denominator==1)
M={tuple((a*gens[0][i]+b*gens[1][i]+c*gens[2][i])%orders[i] for i in range(4)) for a,b,c in product(range(9),range(3),range(9))}
check(len(M)==243);check(len(M)**2==27*9*81*3)
for a in M:check(all(sum(diag[i]*a[i]*b[i] for i in range(4)).denominator==1 for b in gens))
# Six explicit oriented saddle moves through a common positive braid closure.
stages=[[3,3,6,6],[3,3,5,6],[3,3,4,6],[3,3,3,6],[3,4,3,6],[3,5,3,6],[3,5,3,7]]
for a,b in zip(stages,stages[1:]):check(sum(abs(x-y) for x,y in zip(a,b))==1)
check(word(stages[0])==K['word']);check(word(stages[-1])==J['word'])
check(len(components(word(stages[3])))==2)
# Restricted optimization: only cyclic rotations and generator interchange, no stabilizations.
variants=lambda w:{tuple(w[i:]+w[:i]) for i in range(len(w))}|{tuple(3-x for x in w[i:]+w[:i]) for i in range(len(w))}
restricted_max=max(lcs(a,b) for a in variants(K['word']) for b in variants(J['word']))
check(restricted_max==15)
# Negative controls: trefoil, a changed exponent, and a nonmetabolic proposed generator.
check(burau([1,1,1,2])==[1,-1,1]);check(len(components([1,1,1,2]))==1)
check(burau(word([3,3,4,6]))!=K['alexander_coefficients'])
check(sum(diag[i]*[1,0,0,1][i]**2 for i in range(4)).denominator!=1)
output={'problem_id':'30006060','status':'unsolved','substantive_approaches':5,'K':K,'J':J,'whole_signature_functions_equal':True,'whole_upsilon_functions_computed':False,'algebraic_concordance_computed':False,'difference_linking_form':{'orders':orders,'diagonal':[str(x) for x in diag],'metabolizer_generators':gens,'metabolizer_order':len(M)},'cobordism':{'block_exponent_stages':stages,'saddles':6,'euler_characteristic':-6,'boundary_components':2,'connected':True,'genus':3,'intermediate_closure_components':[len(components(word(s))) for s in stages],'restricted_common_subword_maximum':restricted_max},'assertions':checks}
print(json.dumps(output,indent=2,sort_keys=True))
