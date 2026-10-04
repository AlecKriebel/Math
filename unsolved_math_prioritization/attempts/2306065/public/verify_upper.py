#!/usr/bin/env python3
"""Verify a rational Fejer/linear-programming outer bound for B(3).
No optimizer is used. No floating-point step enters the certificate check.
"""
from fractions import Fraction as F
import json
from pathlib import Path

def verify():
    o=json.loads((Path(__file__).parent/'UPPER_CERTIFICATE.json').read_text());N=o['N'];J=o['grid_denominator'];K=o['intervals'];den=o['dual_denominator'];U=F(o['L_upper_numerator'],o['L_upper_denominator'])
    assert N==40 and J==100 and K==64 and den==10**12
    # Taylor lower bound e^U>3 certifies log(3)<U.
    term=F(1);s=term
    for k in range(1,31):term*=U/k;s+=term
    assert s>3
    cs=[]
    for j in range(-J,J+1):
        x=F(j,J);row=[F(1),x]
        for n in range(2,N+1):row.append(2*x*row[-1]-row[-2])
        cs.append(row[1:])
    weights=[F(N+1-n,N+1) for n in range(1,N+1)]
    A=[[-n*weights[n-1]*r[n-1] for n in range(1,N+1)] for r in cs]+[[weights[n]*r[n] for n in range(N)] for r in cs]
    B=[F(1)]*len(cs)+[U]*len(cs)
    assert sorted(r['k'] for r in o['rows'])==list(range(K))
    upper_bounds=[]
    for record in o['rows']:
        k=record['k'];lo=F(4*k,3*K);hi=F(4*(k+1),3*K)
        target=[(lo+hi)/2,F(1)]+[F(0)]*(N-2);combo=[F(0)]*N;bound=F(0)
        for i,integer in record['inequality_dual']:
            assert 0<=i<len(A) and isinstance(integer,int) and integer>=0
            y=F(integer,den);bound+=y*B[i]
            for n in range(N):combo[n]+=y*A[i][n]
        for name,sgn in [('upper_dual',1),('lower_dual',-1)]:
            for n,integer in record[name]:
                assert 0<=n<N and isinstance(integer,int) and integer>=0
                y=F(integer,den)
                endpoint=(hi if sgn==1 else lo) if n==0 else F(2*sgn,n+1)
                combo[n]+=sgn*y;bound+=sgn*y*endpoint
        # Exact correction for every rounded-dual residual, using |c_n|<=2/n.
        residual=sum(F(2,n+1)*abs(target[n]-combo[n]) for n in range(N))
        upper=bound+residual-lo*hi/2
        assert upper<F(957,1000)
        upper_bounds.append(upper)
    return {'arithmetic':'exact Python Fraction','number_of_slabs':K,'Fejer_degree':N,'rational_grid_points':2*J+1,'all_slabs_below_957_over_1000':True,'largest_certificate_bound':str(max(upper_bounds)),'limits':'Certifies B(3)<0.957 using a finite necessary relaxation. It does not assert that the relaxation is exact or determine B(M) for all e<M<5.'}

if __name__=='__main__':print(json.dumps(verify(),indent=2))
