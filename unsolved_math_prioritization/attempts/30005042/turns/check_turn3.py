#!/usr/bin/env python3
"""Exact finite controls for Turn3; no network or imported source executable.
The infinite endpoint lemmas and logarithmic theorem are proved in TURN_3.md.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json
C=Counter()
def ck(p,k):
    assert p,k
    C[k]+=1

# Work with alpha^n directly, avoiding numerical nth roots in the moving grid.
for a,b in [(F(3,2),F(4)),(F(2),F(3)),(F(5,4),F(7,2))]:
    for n in range(1,21):
        t=a**n;end=b**n;pieces=[]
        while t<end:
            u=min(2*t,end)
            ck(t<u<=2*t,'moving_grid_growth_ratio')
            pieces.append((t,u));t=u
        ck(pieces[0][0]==a**n and pieces[-1][1]==end,'moving_grid_cover')
        ck(all(pieces[j][1]==pieces[j+1][0] for j in range(len(pieces)-1)),'moving_grid_adjacency')

for n,y in product(range(1,18),range(0,130)):
    a=F(2);t0=a**n
    # Infinite geometric j-tail can be evaluated exactly.
    j=0
    while y>2*t0*2**j:j+=1
    total=F(2*y*y,t0*2**j)
    ck(total<=4*min(F(y*y,t0),F(y)),'truncated_square_geometric_bound')
    terms=[t0*2**j for j in range(20) if t0*2**j<y]
    ck(sum(terms,F(0))<2*y or y==0,'large_family_geometric_count')

for y in range(1,1025):
    q=y.bit_length()-1
    exact=F(q*y)+F(y*y,2**q)
    ck(exact<=y*(q+2),'endpoint_Bn_sum_bound')
    weighted=F(y*q*(q+1)*(2*q+1),6)+F(y*y*(q*q+4*q+6),2**q)
    ck(weighted<=12*y*(q+1)**3,'log_cubed_weighted_square_bound')
    pairs=sum(1 for n in range(1,q+2) for j in range(q+2) if 2**(n+j)<y)
    ck(pairs<=(q+1)**2,'discarded_tail_pair_count')
    large=sum(2*2**(n+j) for n in range(1,q+2) for j in range(q+2) if 2**(n+j)<y)
    ck(large<=4*y*q,'endpoint_large_family_total')

# Conditional generation law with a heavy endpoint relative to the parameter.
# B is0 or8, E B=2; one uniform four-point jump gives EX_j=2+j/4.
curves=[]
for B,pB in [(0,F(3,4)),(8,F(1,4))]:
    for threshold in range(1,5):
        curves.append((tuple(B+int(threshold<=j) for j in (1,2,3)),pB/4))
lam=[F(9,4),F(5,2),F(11,4)];active=[1,2,3]
for j in range(3):ck(sum(p*x[j] for x,p in curves)==lam[j],'offspring_means')
for n in range(1,4):
    mu=[sum(p*x[j]*int(x[-1]<=lam[j]**n) for x,p in curves) for j in range(3)]
    remainder=[lam[j]-mu[j] for j in range(3)]
    for x,p in curves:
        u=[x[j]*int(x[-1]<=lam[j]**n) for j in range(3)]
        ck(u==sorted(u),'adaptive_truncation_monotonicity')
        ck(all(0<=u[j]<=x[j] for j in range(3)),'adaptive_truncation_bounds')
    ED=[F(0)]*3;EC=[F(0)]*3;Erawmax=F(0)
    for config in product(curves,repeat=3):
        prob=config[0][1]*config[1][1]*config[2][1]
        raw=[]
        for j in range(3):
            U=sum(config[i][0][j]*int(config[i][0][-1]<=lam[j]**n) for i in range(active[j]))
            T=sum(config[i][0][j]*int(config[i][0][-1]>lam[j]**n) for i in range(active[j]))
            D=(U-active[j]*mu[j])/lam[j]**(n+1)
            R=(T-active[j]*remainder[j])/lam[j]**(n+1)
            actual=(sum(config[i][0][j] for i in range(active[j]))-active[j]*lam[j])/lam[j]**(n+1)
            ck(D+R==actual,'exact_innovation_decomposition')
            ED[j]+=prob*D;EC[j]+=prob*R
            raw.append(U-active[j]*mu[j])
            if T==0:
                W=F(active[j])/lam[j]**n
                ck(actual==D-remainder[j]*W/lam[j],'eventual_negative_drift_identity')
        Erawmax+=prob*max(r*r for r in raw)
    for j in range(3):
        ck(ED[j]==0,'conditional_D_centering');ck(EC[j]==0,'conditional_tail_centering')
    end2=sum(p*x[-1]**2*int(x[-1]<=lam[-1]**n) for x,p in curves)
    ck(Erawmax<=16*active[-1]*end2,'monotone_L2_application')

# Summable deterministic tail bias implies the needed weighted square bound.
for support in [(1,2,3,16),(0,4,17,129),(1,100,1000)]:
    bn=[sum(F(y,len(support)) for y in support if y>2**n) for n in range(1,14)]
    ck(bn==sorted(bn,reverse=True),'tail_bias_monotonicity')
    ck(sum((n+1)*v*v for n,v in enumerate(bn))<=sum(bn)**2,'weighted_tail_bias_square_bound')

# Generic continuous-martingale countercontrol on its finite Cantor cylinders.
# Every sign pattern is realized. E over epsilon equals the same uniform sum.
H=F(1)
for n in range(2,13):
    Hprev=H;H+=F(1,n)
    ck(1+F(1,n)/Hprev==H/Hprev,'harmonic_product_telescope')
    vals=[];diffs=[]
    for bits in product((-1,1),repeat=n-1):
        v=F(1);hh=F(1);prev=F(1)
        for k,sign in enumerate(bits,start=2):
            prev=v;v*=1+F(sign,k)/hh;hh+=F(1,k)
        vals.append(v);diffs.append(abs(v-prev))
    ck(max(vals)==H,'generic_martingale_supremum')
    ck(max(diffs)==F(1,n),'generic_martingale_increment_norm')
    ck(sum(vals)/len(vals)==1,'generic_martingale_mean_one')
    hh=F(1);second=F(1)
    for k in range(2,n+1):second*=1+(F(1,k)/hh)**2;hh+=F(1,k)
    ck(sum(v*v for v in vals)/len(vals)==second,'generic_martingale_second_moment')

out={'problem_id':30005042,'author_turn':3,'exact_assertions':sum(C.values()),'by_kind':dict(sorted(C.items())),
     'scope':'Finite exact controls only. Actual X log X endpoint functional convergence remains unresolved; the generic martingale countercontrol is not a source-model counterexample.',
     'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(out,indent=2,sort_keys=True))
