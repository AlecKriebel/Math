#!/usr/bin/env python3
"""Exact finite checks for a partial Yamabe heat-trace result. No floats."""
from fractions import Fraction as F
import json
from pathlib import Path
import sys

SCALE=10**40

def require(condition,message):
    if not condition:
        raise ValueError(message)

def floor_scaled(x):
    return x.numerator*SCALE//x.denominator

def ceil_scaled(x):
    return -((-x.numerator*SCALE)//x.denominator)

def exp_neg_bounds(x):
    """Enclose exp(-x) in integer multiples of 10^-40.
    Alternating Taylor bounds at z<=1, then outward-rounded squaring.
    """
    require(x>=0,'negative exponential argument')
    k=0
    z=x
    while z>1:
        z/=2
        k+=1
    s=F(1); term=F(1)
    for j in range(1,34):
        term*=-z/j
        s+=term
        if j==32:
            even=s
    lo=floor_scaled(s)
    hi=ceil_scaled(even)
    require(0<=lo<=hi<=SCALE,'Taylor enclosure failure')
    for unused in range(k):
        lo=lo*lo//SCALE
        hi=(hi*hi+SCALE-1)//SCALE
    return lo,hi

def q_upper(x):
    lo,hi=exp_neg_bounds(x)
    a=2-x
    # For negative a the lower exponential gives the upper product.
    return a*F(hi if a>=0 else lo,SCALE)

def run(config):
    require(config['problem_id']==30001169,'wrong problem')
    require(config['status']=='partial_unresolved','resolution overclaim')
    require(config['n']==4,'dimension mismatch')
    require(config['weight_lower']==[999,1000] and config['weight_upper']==[1001,1000], 'weight scope mismatch')
    require(config['time_start']==[1,4] and config['time_stop']==[1,1], 'time scope mismatch')
    require(config['intervals']==750 and config['last_degree']==8,'finite cover mismatch')
    require(config['a2_n4']==[-1,90], 'heat coefficient mismatch')
    require(F(1,6)-F(4-2,4*(4-1))==0,'n4 a1')
    for n in range(5,41):
        require(F(1,6)-F(n-2,4*(n-1))==F(4-n,12*(n-1))<0,'a1 sign')
    require(-F(2,180)==F(-1,90),'Gauss Bonnet coefficient')
    require(F(3,2)<F(2*9,3),'theta interval overlap using pi>3')
    model_margin=F(1,3)-84*F(3,8)**6/(1-4*F(3,8)**4)-F(240,2**50)
    require(model_margin>F(1,20),'abstract spectral model margin')
    m=F(*config['weight_lower']);M=F(*config['weight_upper'])
    a=F(*config['time_start']);b=F(*config['time_stop'])
    N=config['intervals'];L=config['last_degree']
    # Every omitted eigenvalue has t*lambda>2, hence negative q.
    require(a*F((L+2)*(L+3),1)/M>2,'omitted tail not negative')
    worst=None; worst_index=None
    for i in range(N):
        left=a+(b-a)*i/N;right=a+(b-a)*(i+1)/N
        total=F(0)
        for ell in range(L+1):
            eigen=(ell+1)*(ell+2)
            mult=(2*ell+3)*(ell+1)*(ell+2)//6
            # q(x)=(2-x)e^-x has its unique critical point at x=3,
            # which is a minimum. Its maximum on any interval is at an end.
            total+=mult*max(q_upper(left*eigen/M),q_upper(right*eigen/m))
        require(total<F(-6,1000),f'failed interval {i}')
        if worst is None or total>worst:
            worst=total;worst_index=i
    return {'status':'partial_unresolved','intervals_checked':N,'degree_blocks':L+1,
            'exp_enclosures':2*N*(L+1),'upper_bound_strictly_below':'-3/500',
            'worst_interval_index':worst_index,'a2_n4':'-1/90',
            'abstract_model_margin_above':'1/20 (not a geometric counterexample)',
            'scope':'n=4; normalized smooth positive W with 999/1000<=W<=1001/1000; f prime<0 for t>=1/4',
            'certification':'exact rational arithmetic; asymptotic and spectral theorems checked in proof, not by code'}

if __name__=='__main__':
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('claim.json')
    print(json.dumps(run(json.loads(path.read_text())),sort_keys=True,indent=2))
