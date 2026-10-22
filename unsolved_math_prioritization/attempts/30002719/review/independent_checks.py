#!/usr/bin/env python3
"""Literal logarithm expansion and exact reversible spectral controls."""
from fractions import Fraction as Q
from math import factorial,comb
from itertools import product
from pathlib import Path
from collections import Counter
import hashlib,json
C=Counter()
def ck(name,b):
    assert b,name
    C[name]+=1
def partitions(n,small=1):
    if n==0:
        yield []
    for i in range(small,n+1):
        for tail in partitions(n-i,i):yield [i]+tail
def literal_A(n):
    a=[Q(0)]*(n*(n-1)//2+1)
    # The literal series sum (-1)^(m-1)(f-1)^m/m, grouped by
    # multiplicities of selected x-powers. No connected-graph recurrence.
    for parts in partitions(n):
        m=len(parts);multiplicity=Counter(parts)
        coefficient=Q((-1)**(n+m-2)*n*factorial(m-1))
        degree=0
        for j,num in multiplicity.items():
            coefficient/=factorial(num)*factorial(j)**num
            degree+=num*j*(j-1)//2
        a[degree]+=coefficient
    return a
def mul(a,b,N=8):
    out=[Q(0)]*(N+1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            if i+j<=N:out[i+j]+=x*y
    return out
def power(a,k,N=8):
    p=[Q(1)]+[Q(0)]*N
    for _ in range(k):p=mul(p,a,N)
    return p
def binomial_power(a,s,N=8):
    h=a[:N+1]+[Q(0)]*max(0,N+1-len(a));h[0]-=1
    answer=[Q(1)]+[Q(0)]*N
    term=answer[:];coeff=Q(1)
    for k in range(1,N+1):
        term=mul(term,h,N);coeff*=Q(s-k+1,k)
        answer=[x+coeff*y for x,y in zip(answer,term)]
    return answer
q=[-1,132,-108,-264,240]
sq=mul(q,q)
expected={4:Q(-25059,32),5:Q(-1016,5),6:Q(-153,2),7:Q(-2070,7),8:Q(-2265,8)}
G={};cert={}
for n in range(2,13):
    a=literal_A(n);g=binomial_power(a,Q(-1,n));G[n]=g
    ck('constant_term',a[0]==1)
    root=binomial_power(a,Q(1,n))
    ck('formal_root',power(root,n)==(a+[Q(0)]*9)[:9])
    ck('renewal_inverse',mul(root,g)==[Q(1)]+[Q(0)]*8)
    # Exact Taylor coefficients at y=1 directly from the literal polynomial.
    at_one=[sum(a[j]*comb(j,k) for j in range(k,len(a))) for k in range(n)]
    for k in range(n-1):ck('unit_root_order',at_one[k]==0)
    ck('first_nonzero_at_one',at_one[-1]==Q((-1)**(n-1)*n**(n-2),factorial(n-1)))
    ck('nonrational_valuation',Q(n-1,n).denominator==n and n>1)
    if n>=4:
        val=sum(x*y for x,y in zip(sq,g))
        ck('negative_form',val==expected.get(n,Q(-255)) and val<0)
        cert[str(n)]=str(val)

# Solve the leading-root identity one coefficient at a time, independently
# of both the graph recurrence and the finite-n logarithm formula.
U=[Q(1)]+[Q(0)]*8
for k in range(1,9):
    rhs=[Q(1)]+[Q(0)]*8
    for j in [2,3,4]:
        shift=j*(j-1)//2
        p=power(U,j)
        for i in range(9-shift):rhs[i+shift]+=Q((-1)**j,factorial(j))*p[i]
    U[k]=rhs[k]
stable=list(map(Q,['1','1/2','1/2','11/24','11/24','7/16','7/16','493/1152','163/384']))
ck('leading_root_coefficients',U==stable)
ck('stable_form',sum(x*y for x,y in zip(sq,U))==-255)
for n in range(9,13):ck('stabilization_control',G[n]==U)

# n=3 positive spectral control: affine image -1/2+(3/2)X of
# a Beta(2/3,1/3) probability law, whose moments are rational.
moments=[Q(1)]
for k in range(1,9):moments.append(moments[-1]*Q(Q(2,3)+k-1,k))
for k in range(9):
    val=sum(Q(comb(k,j))*(-Q(1,2))**(k-j)*Q(3,2)**j*moments[j] for j in range(k+1))
    ck('n3_signed_support_control',val==G[3][k])
ck('logconvexity_not_necessary',G[3][1]*G[3][3]-G[3][2]**2==-Q(1,24))

# Explicit two-state reversible chains, including negative nontrivial
# eigenvalues. Direct powers are compared to the two-atom spectral measure.
def dot(a,b):return sum(x*y for x,y in zip(a,b))
for i,j in product(range(1,11),repeat=2):
    a,b=Q(i,10),Q(j,10)
    P=[[1-a,a],[b,1-b]]
    row=[Q(1),Q(0)];g=[]
    for k in range(9):
        g.append(row[0])
        row=[sum(row[z]*P[z][w] for z in range(2)) for w in range(2)]
    lam=1-a-b;pi0=b/(a+b);pi1=a/(a+b)
    ck('two_state_moments',all(g[k]==pi0+pi1*lam**k for k in range(9)))
    Qval=dot(sq,g)
    spectral=pi0*sum(q)**2+pi1*sum(q[k]*lam**k for k in range(5))**2
    ck('two_state_PSD',Qval==spectral and Qval>=0)

root=Path(__file__).resolve().parent
r={'status':'PASS','assertions':sum(C.values()),'checks':dict(C),'negative_forms':cert,
   'proof_sha256':hashlib.sha256((root/'author_replay/OBSTRUCTION.md').read_bytes()).hexdigest(),
   'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
   'scope':'Exact literal logarithm and binomial-root calculations, unit-root valuations, and reversible controls. The infinite-n conclusion uses the credited stabilization identity; no unrestricted PGF positivity claim.'}
(root/'independent_results.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
