#!/usr/bin/env python3
"""Exact calibration of credited generator-coupling formulas, not new research."""
from fractions import Fraction as F
from itertools import product
from collections import Counter
import json
C=Counter()
def ck(x,label):
    assert x,label
    C[label]+=1
def line_transport(m,n,points):
    a=m[:];b=n[:];pi=[[F(0) for _ in b] for _ in a]
    i=j=0
    while i<len(a) and j<len(b):
        t=min(a[i],b[j]);pi[i][j]+=t;a[i]-=t;b[j]-=t
        if a[i]==0:i+=1
        if b[j]==0:j+=1
    cost=sum(pi[i][j]*abs(points[i]-points[j]) for i in range(len(a)) for j in range(len(b)))
    f=[F(0)];pref=F(0)
    for k in range(len(points)-1):
        pref+=m[k]-n[k];sgn=(pref>0)-(pref<0)
        f.append(f[-1]-sgn*(points[k+1]-points[k]))
    ck(all(sum(pi[i])==m[i] for i in range(len(m))),'transport_first_marginal')
    ck(all(sum(pi[i][j] for i in range(len(m)))==n[j] for j in range(len(n))),'transport_second_marginal')
    ck(all(abs(f[i]-f[j])<=abs(points[i]-points[j]) for i in range(len(f)) for j in range(len(f))),'dual_one_Lipschitz')
    ck(sum(f[i]*(m[i]-n[i]) for i in range(len(m)))==cost,'primal_dual_exact_optimality')
    return pi,cost
for points in [[F(0),F(1),F(2)],[F(0),F(1,3),F(7,4)]]:
    for rates in product([F(0),F(1,3),F(2)],repeat=4):
        a,b,c,e=rates;J=[[F(0),a,b],[c,F(0),e],[b,c,F(0)]]
        for x,y in [(0,1),(1,2),(0,2)]:
            rx=sum(J[x]);ry=sum(J[y]);m=J[x][:];n=J[y][:];m[x]+=ry;n[y]+=rx
            ck(sum(m)==sum(n)==rx+ry,'augmented_equal_mass')
            pi,cost=line_transport(m,n,points)
            for k in range(3):
                g=[F(int(i==k)) for i in range(3)]
                first=sum(pi[i][j]*(g[i]-g[x]) for i in range(3) for j in range(3))
                second=sum(pi[i][j]*(g[j]-g[y]) for i in range(3) for j in range(3))
                ck(first==sum(J[x][i]*(g[i]-g[x]) for i in range(3)),'false_first_jumps_cancel')
                ck(second==sum(J[y][j]*(g[j]-g[y]) for j in range(3)),'false_second_jumps_cancel')
            drift=sum(pi[i][j]*(abs(points[i]-points[j])-abs(points[x]-points[y])) for i in range(3) for j in range(3))
            ck(drift==cost-(rx+ry)*abs(points[x]-points[y]),'coupling_distance_drift')
for a,b in product([F(0),F(1,7),F(1),F(5)],repeat=2):
    # At (0,1), augmented measures both equal b*delta0+a*delta1.
    m=[F(0)+b,a];n=[b,F(0)+a]
    pi,cost=line_transport(m,n,[F(0),F(1)])
    ck(cost==0,'two_state_augmented_transport_cost_zero')
    drift=sum(pi[i][j]*(abs(i-j)-1) for i in range(2) for j in range(2))
    ck(drift==-(a+b),'two_state_curvature_a_plus_b')
    if a+b:
        p=a/(a+b)
        for z in [F(0),F(1,3),F(1)]:
            # z=exp(-(a+b)t); transition probabilities of state1.
            p0=p*(1-z);p1=p+(1-p)*z
            ck(0<=p0<=1 and 0<=p1<=1,'two_state_transition_probability_range')
            ck(abs(p1-p0)==z,'two_state_exact_contraction_factor')
    else:ck(a==b==0,'zero_rates_have_no_positive_contraction')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'categories':dict(C),'scope':'Finite arithmetic calibration of credited optimal-transport and generator identities. No new theorem or general convergence without hypotheses is asserted.'},indent=2))
