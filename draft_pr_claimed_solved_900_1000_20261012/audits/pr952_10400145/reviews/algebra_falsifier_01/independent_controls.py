#!/usr/bin/env python3
"""Exact finite guards for the accompanying proofs; not a proof of a completion theorem."""
from itertools import product
from math import comb, factorial
from random import Random
import json


def add(a,b,d):
    return tuple((a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(d+1))


def mul(a,b,d):
    return tuple(sum(a[j]*b[i-j] for j in range(max(0,i-len(b)+1),min(i,len(a)-1)+1)) for i in range(d+1))


def qpow(n,d):
    return tuple(comb(n,i) if i<=n else 0 for i in range(d+1))


def eval_poly(coeff,n,d):
    out=(0,)*(d+1)
    for j,c in enumerate(coeff):
        out=add(out,mul(c,qpow(n*j,d),d),d)
    return out


def diff(seq):
    return [b-a for a,b in zip(seq,seq[1:])]


def finite_difference(seq,k):
    for _ in range(k):seq=diff(seq)
    return seq


def matadd(a,b):
    return tuple(tuple(x+y for x,y in zip(ar,br)) for ar,br in zip(a,b))


def scale(k,a):return tuple(tuple(k*x for x in row) for row in a)


def matmul(a,b):
    n=len(a)
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(n)) for j in range(n)) for i in range(n))


def comm(a,b):return matadd(matmul(a,b),scale(-1,matmul(b,a)))


def matrix_unit(n,i,j):return tuple(tuple(int(r==i and c==j) for c in range(n)) for r in range(n))


def casimir(n,x):
    z=scale(0,x)
    for i in range(n):
        for j in range(n):z=matadd(z,comm(matrix_unit(n,i,j),comm(matrix_unit(n,j,i),x)))
    return z


def trim(p):
    while len(p)>1 and p[-1]==0:p.pop()
    return p


def poly_mul_mod(a,b,mod):
    c=[0]*(len(a)+len(b)-1)
    for i,u in enumerate(a):
        for j,v in enumerate(b):c[i+j]=(c[i+j]+u*v)%mod
    return trim(c)


def poly_eval_mod(p,x,mod):
    ans=0
    for c in reversed(p):ans=(ans*x+c)%mod
    return ans


def monic_remainder_mod(p,e,mod):
    p=[x%mod for x in p];trim(p)
    assert e[-1]==1
    while len(p)>=len(e):
        k=len(p)-len(e);v=p[-1]
        for i,c in enumerate(e):p[i+k]=(p[i+k]-v*c)%mod
        trim(p)
    return p


def main():
    # Exhaustive first jets of every quadratic polynomial with six small integer coefficients.
    first_count=0
    for six in product(range(-2,3),repeat=6):
        coeff=[six[2*j:2*j+2] for j in range(3)]
        vals=[eval_poly(coeff,n,1) for n in (1,2,3)]
        assert vals[0][0]==vals[1][0]==vals[2][0]
        assert vals[2][1]-2*vals[1][1]+vals[0][1]==0
        first_count+=1
    # Arbitrarily high t degree: order-d coefficient has zero (d+1)-st difference.
    rng=Random(10400145);higher_count=0
    for d in range(7):
        for _ in range(80):
            coeff=[tuple(rng.randrange(-7,8) for _ in range(d+1)) for j in range(rng.randrange(1,10))]
            values=[eval_poly(coeff,n,d)[d] for n in range(1,13)]
            assert all(x==0 for x in finite_difference(values,d+1))
            higher_count+=1
    # After canceling 1-q, the kth Poincare summand is a polynomial with exact order k.
    poincare={};d=8;total=(0,)*(d+1)
    for k in range(9):
        geom=(0,)*(d+1)
        for j in range(k+1):geom=add(geom,qpow(j,d),d)
        term=mul(qpow(k,d),geom,d)
        for j in range(k+2,2*k+2):term=mul(term,add((1,),tuple(-x for x in qpow(j,d)),d),d)
        assert all(x==0 for x in term[:k])
        assert term[k]==(-1)**k*factorial(2*k+1)//factorial(k)
        total=add(total,term,d);poincare[str(k)]={'order':k,'leading':term[k]}
    assert total[:2]==(1,-6)
    # Lie-theoretic ratio: C_ad(X)=2nX for a full spanning basis of sl_n.
    weights={};casimir_count=0
    for n in range(2,6):
        basis=[matrix_unit(n,i,j) for i in range(n) for j in range(n) if i!=j]
        basis += [matadd(matrix_unit(n,i,i),scale(-1,matrix_unit(n,i+1,i+1))) for i in range(n-1)]
        assert len(basis)==n*n-1
        for x in basis:
            assert casimir(n,x)==scale(2*n,x);casimir_count+=1
        weights[str(n)]=2*n*(n*n-1)
    assert weights['3']==4*weights['2']
    # Monic division is valid even with zero divisors in Z/6; q=5 is a unit of order two.
    mod=6;q=5;e=[1]
    for n in (1,2,3):e=poly_mul_mod(e,[-pow(q,n,mod)%mod,1],mod)
    monic_count=0
    for _ in range(200):
        p=[rng.randrange(mod) for _ in range(rng.randrange(1,12))];r=monic_remainder_mod(p,e,mod)
        assert len(r)<len(e)
        for n in (1,2,3):assert poly_eval_mod(p,pow(q,n,mod),mod)==poly_eval_mod(r,pow(q,n,mod),mod)
        monic_count+=1
    # Correct first-jet interpolant for ranks 1,2 predicts rank3=-12, not -24.
    test_coeff=[(7,6),(-6,0)] # 1-6(t-q), q=1+h
    model=[eval_poly(test_coeff,n,1) for n in (1,2,3)]
    assert model==[(1,0),(1,-6),(1,-12)]
    source_slopes=[0,-6,-24];residual=source_slopes[2]-2*source_slopes[1]+source_slopes[0]
    assert residual==-12
    assert residual%6==0 and residual%5!=0 # Torsion can conceal the obstruction.
    # The cubic family's consecutive second difference is 6(n+1)*lambda.
    for n in range(1,21):
        vals=[k*(k*k-1) for k in (n,n+1,n+2)]
        assert vals[2]-2*vals[1]+vals[0]==6*(n+1)
    out={'status':'PASS','interpretation':'Finite exact guards only; infinite-limit claims require the written proofs.',
         'first_jet_exhaustive_cases':first_count,'higher_jet_cases':higher_count,
         'poincare_terms':poincare,'poincare_constant_and_linear':list(total[:2]),
         'casimir_basis_cases':casimir_count,'theta_trace_weights':weights,
         'monic_zero_divisor_cases':monic_count,'interpolating_control_first_jets':model,
         'actual_first_slopes':source_slopes,'obstruction':residual,
         'hidden_in_characteristics':[2,3,6],'detected_in_characteristic':5}
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
