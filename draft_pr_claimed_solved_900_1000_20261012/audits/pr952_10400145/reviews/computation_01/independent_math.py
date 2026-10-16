#!/usr/bin/env python3
"""Independently authored exact controls; no candidate modules or assertions.

The mathematical all-tail and inverse-limit proofs are in COMPUTATION_REVIEW.md.
This program checks finite instances and general identities in polynomial n.
It does not verify the topological source bridge.
"""
from fractions import Fraction
from math import comb, factorial
from functools import lru_cache
import json
import sys

class Failure(Exception):
    pass

def need(c, msg):
    if not c:
        raise Failure(msg)

def plus(a,b):
    n=max(len(a),len(b)); out=[0]*n
    for i in range(n):out[i]=(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0)
    while len(out)>1 and out[-1]==0:out.pop()
    return out

def times(a,b,cut=None):
    n=len(a)+len(b)-1
    if cut is not None:n=min(n,cut)
    out=[0]*n
    for i,u in enumerate(a):
        for j,v in enumerate(b):
            if i+j<n:out[i+j]+=u*v
    while len(out)>1 and out[-1]==0:out.pop()
    return out

def scalar(a,c):return [u*c for u in a]

def power(a,n,cut=None):
    need(type(n) is int and n>=0,'power input')
    out=[1]
    while n:
        if n&1:out=times(out,a,cut)
        a=times(a,a,cut);n//=2
    return out

def diff(p):
    # Polynomial p(n+1)-p(n), using binomial expansion over Q.
    out=[Fraction(0)]*len(p)
    for j,c in enumerate(p):
        for i in range(j+1):out[i]+=c*comb(j,i)
    return plus(out,scalar(p,-1))

def evaluate(a,x):
    out=0
    for c in reversed(a):out=out*x+c
    return out

def choose_polynomial(j,r):
    # [epsilon^r](1+epsilon)^(j*n) = binom(j*n,r) in Q[n].
    out=[Fraction(1)]
    for k in range(r):out=times(out,[-k,j])
    return scalar(out,Fraction(1,factorial(r)))

def summand(k,cut=None):
    # Every summand is a polynomial after exact cancellation of 1-q.
    q=[1,1]
    geom=[0]
    for a in range(k+1):geom=plus(geom,power(q,a,cut))
    out=times(power(q,k,cut),geom,cut)
    for a in range(k+2,2*k+2):out=times(out,plus([1],scalar(power(q,a,cut),-1)),cut)
    return out

@lru_cache(None)
def gaussian(N,k):
    # Gaussian-binomial recurrence, in x=q-1. This establishes a polynomial
    # quotient, supplementing the all-k product identity in the review.
    if k<0 or k>N:return [0]
    if k==0 or k==N:return [1]
    return plus(gaussian(N-1,k),times(power([1,1],N-k),gaussian(N-1,k-1)))

def main():
    q=[1,1]
    need(times(q,[1,-1],2)==[1],'q Laurent inverse')
    need(plus(q,[-1])==[0,1],'level one cannot kill epsilon')
    kernel=[]
    for jet in range(1,7):
        out=[1]
        for j in range(1,jet+1):out=times(out,plus(power(q,j),[-1]),jet)
        need(out==[0],'Habiro finite-level kernel');kernel.append(jet)
    universal=0
    for jet in range(1,7):
        for j in range(25):
            for coefficient_epsilon_degree in range(jet):
                for total_degree in range(coefficient_epsilon_degree,jet):
                    p=choose_polynomial(j,total_degree-coefficient_epsilon_degree)
                    for _ in range(total_degree+1):p=diff(p)
                    need(all(c==0 for c in p),'jet coefficient degree exceeded')
                    universal+=1
    # Evaluation of every degree<=24 basis monomial in finite characteristic.
    # This tests torsion/nonunits; characteristic-zero proof is not inferred.
    finite=[]
    for modulus in [2,3,4,5,6,7,12,25]:
        count=0
        for degree in range(25):
            rows=[power(q,degree*n,2) for n in range(1,13)]
            rows=[r+[0]*(2-len(r)) for r in rows]
            for n in range(10):
                need((rows[n+2][0]-rows[n][0])%modulus==0,'constant torsion failure')
                need((rows[n+2][1]-2*rows[n+1][1]+rows[n][1])%modulus==0,'affine torsion failure')
                count+=1
        finite.append({'modulus':modulus,'basis_second_differences':count})
    # Monic quotient: for E_N every node q^n, 1<=n<=N, kills E_N exactly.
    quotient_tests=0
    for jet in range(2,6):
        for N in range(1,9):
            nodes=[power(q,n,jet) for n in range(1,N+1)]
            for node in nodes:
                out=[1]
                for root in nodes:out=times(out,plus(node,scalar(root,-1)),jet)
                need(out==[0],'monic quotient evaluation');quotient_tests+=1
    tail=[]
    for k in range(19):
        s=summand(k)
        order=next((i for i,c in enumerate(s) if c),None)
        need(order==k,'tail order')
        leading=(-1)**k*factorial(2*k+1)//factorial(k)
        need(s[k]==leading,'tail leading coefficient')
        if k>=2:need(s[0]==s[1]==0,'low-order tail mutation')
        tail.append({'k':k,'valuation':order,'leading':leading})
    habiro_divisibility=[]
    for k in range(13):
        J=[1]
        for j in range(1,k+1):J=times(J,plus([1],scalar(power(q,j),-1)))
        G=[0]
        for j in range(k+1):G=plus(G,power(q,j))
        factored=times(times(times(power(q,k),G),gaussian(2*k+1,k)),J)
        need(factored==summand(k),'Habiro product divisibility factorization')
        habiro_divisibility.append(k)
    # Only k<=r can contribute through x^r, by the all-k factor proof.
    jet=[0]
    for k in range(7):jet=plus(jet,summand(k,7))
    need(jet[:5]==[1,-6,45,-464,6224],'independent Poincare jet')
    # Derive arbitrary consecutive-rank second difference in Z[n].
    cubic=[0,-1,0,1]
    twice=diff(diff(cubic))
    need(twice==[6,6],'rank cubic second difference is 6(n+1)')
    values=[-evaluate(cubic,n) for n in (1,2,3,4)]
    need(values==[0,-6,-24,-60],'rank specialization')
    need(values[2]-2*values[1]+values[0]==-12,'rank 1..3 residual')
    need(values[3]-2*values[2]+values[1]==-18,'rank 2..4 residual')
    # Construct P(t)=1+C(t-q) at stages >=2 for arbitrary affine slopes.
    # This proves two ranks alone allow arbitrary integer v2 with F(q)=1.
    affine=[]
    for C in [-24,-6,0,5]:
        coeff=[plus([1],scalar(q,-C)),[C]]
        rows=[]
        for n in range(1,6):
            v=plus(coeff[0],times(coeff[1],power(q,n,2),2));rows.append(v+[0]*(2-len(v)))
        need(rows==[[1,C*(n-1)] for n in range(1,6)],'affine interpolation control')
        affine.append(rows)
    # Rank-dependent 1/(n(n+1)) rescaling really can flatten n(n^2-1).
    rescaled=[Fraction(n*(n*n-1),n*(n+1)) for n in (1,2,3,4)]
    need(rescaled==[0,1,2,3],'rank-dependent scaling boundary')
    modular_obstruction=[{'modulus':m,'residual_mod_m':(-12)%m} for m in [2,3,4,5,6,7,12,13]]
    return {'schema':'pr952-independent-computation-v1','status':'PASS_FINITE_CONTROLS','habiro_kernel_levels':kernel,'universal_polynomial_in_n_checks':universal,'finite_quotient_checks':finite,'monic_node_kernel_checks':quotient_tests,'poincare_summand_controls':tail,'habiro_product_factorization_controls':habiro_divisibility,'poincare_jet_through_degree_6':jet,'cubic_second_difference_polynomial':[int(c) for c in twice],'rank_values':values,'residual_rank_1_2_3':-12,'residual_rank_2_3_4':-18,'affine_construction_controls':affine,'rank_dependent_rescale':[int(c) for c in rescaled],'torsion_boundary':modular_obstruction,'limits':['Finite summand controls supplement the all-tail proof; they do not replace it.','First-jet obstruction over Z, not over arbitrary characteristics where 12 may vanish.','Quantum-topological first-coefficient theorem remains a separate mathematical source input.','No assertion statements; all checks remain active under -O and -OO.']}

if __name__=='__main__':
    try:
        if len(sys.argv)!=1:raise Failure('no arguments')
        print(json.dumps(main(),sort_keys=True,separators=(',',':')))
    except Exception as e:
        print('REJECT: '+str(e),file=sys.stderr);raise SystemExit(1)
