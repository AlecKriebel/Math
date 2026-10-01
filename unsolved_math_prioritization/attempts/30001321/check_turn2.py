"""Independent exact finite controls for the turn-2 scoped RWRE argument.
No simulation and no assertion that finite controls prove asymptotics.
"""
from fractions import Fraction as F
from itertools import product
from collections import defaultdict, Counter
from math import factorial, comb
import json
counts=Counter()
def ck(condition,label):
    assert condition,label
    counts[label]+=1
laws=[((F(1,4),F(3,4)),(F(1,2),F(1,2))),((F(1,5),F(2,5)),(F(1,3),F(2,3)))]
for values,probs in laws:
    q=sum(p*w for p,w in zip(values,probs));a=q*(1-q)
    delta=sum(w*p*(1-p) for p,w in zip(values,probs))
    # Backward transition rather than forward return-mass propagation.
    u={0:F(1)};us=[u];g=[F(1)]
    for n in range(40):
        nxt={}
        for d in range(-n-1,n+2):
            step=delta if d==0 else a
            nxt[d]=(1-2*step)*u.get(d,F(0))+step*(u.get(d-1,F(0))+u.get(d+1,F(0)))
        for d in range(n+2):
            ck(nxt.get(d,F(0))>=nxt.get(d+1,F(0)),'hitting_profile_radial_monotonicity')
            ck(nxt.get(d,F(0))==nxt.get(-d,F(0)),'hitting_profile_symmetry')
            ck(nxt.get(d,F(0))<=nxt[0],'hitting_profile_origin_maximum')
        u=nxt;us.append(u);g.append(u[0])
    for N in range(1,5):
        sites=[(s,x) for s in range(N) for x in range(-s,s+1,2)]
        # Group full-environment enumeration by each exposed prefix.
        groups=[defaultdict(list) for _ in range(N+1)]
        for bits in product((0,1),repeat=len(sites)):
            env=dict(zip(sites,(values[b] for b in bits)))
            weight=F(1)
            for b in bits:weight*=probs[b]
            mu={0:F(1)};mus=[mu];I=[F(1)]
            for s in range(N):
                nxt=defaultdict(F)
                for x,w in mu.items():
                    p=env[s,x];nxt[x+1]+=w*p;nxt[x-1]+=w*(1-p)
                mu=dict(nxt);mus.append(mu);I.append(sum(w*w for w in mu.values()))
            for s in range(N+1):
                prefix=bits[:s*(s+1)//2]
                groups[s][prefix].append((weight,mus,I))
        for s in range(N+1):
            for data in groups[s].values():
                mass=sum(w for w,_,_ in data);mu=data[0][1][s]
                for t in range(N-s+1):
                    observed=sum(w*I[s+t] for w,_,I in data)/mass
                    predicted=sum(px*py*us[t].get((x-y)//2,F(0)) for x,px in mu.items() for y,py in mu.items())
                    ck(observed==predicted,'conditional_replica_identity')
                    ck(observed<=g[t],'conditional_overlap_maximum')
                for L in range(1,N-s+2):
                    A=sum(g[:L])
                    for k in range(1,6):
                        moment=sum(w*sum(I[s:s+L])**k for w,_,I in data)/mass
                        ck(moment<=factorial(k)*A**k,'conditional_occupation_moments')
# Deterministic block geometry and parameter margins.
for N in range(2,65):
    for ell in range(1,N//2+1):
        m=N-ell;blocks=defaultdict(list)
        for s in range(m):
            t=N-s-1;j=0
            while 2**(j+1)*ell<=t:j+=1
            blocks[j].append(s)
        ck(sorted(sum(blocks.values(),[]))==list(range(m)),'dyadic_exact_cover')
        for j,B in blocks.items():
            h=2**j*ell
            ck(len(B)<=h,'dyadic_length_bound')
            ck(B==list(range(min(B),max(B)+1)),'dyadic_time_interval')
            ck(all(F(1,N-s)<=F(1,h) for s in B),'dyadic_variance_weight_bound')
for gamma in [F(1,4)+F(k,200) for k in range(1,50)]:
    beta=(gamma+F(1,4))/2;eta=(gamma-F(1,4))/4;gap=gamma-F(1,4)
    ck(beta-eta-(F(1,2)-gamma)==5*gap/4>0,'entropy_exponent_margin')
    ck(2*beta-F(1,2)-eta==3*gap/4>0,'boundary_variance_margin')
    ck(gamma-beta==gap/2>0,'boundary_strip_smaller_than_cell')
    ck(beta<F(1,2),'boundary_strip_subdiffusive')
for u,w,b in product([F(1,100),F(1,3),F(1),F(7)],repeat=3):
    lam=u/(2*(w+b*u))
    ck(lam*b<=F(1,2),'exponential_increment_domain')
    ck(lam*u-lam*lam*w>=u*u/(4*(w+b*u)),'exponential_tail_constant')
# A conservative residue-class bound derived directly from unimodality.
for n in range(1,31):
    for q in [F(1,3),F(1,2),F(4,5)]:
        mass={2*j-n:F(comb(n,j))*q**j*(1-q)**(n-j) for j in range(n+1)}
        peak=max(mass.values())
        for M in range(1,20):
            for shift in range(M):
                residue=sum(p for x,p in mass.items() if (x-shift)%M==0)
                ck(residue<=F(2,M)+2*peak,'parity_residue_bound')
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'families':dict(sorted(counts.items())),'scope':'Finite conditional-moment, transition, partition, parameter and concentration-algebra controls; analytic proof remains necessary; arbitrary diverging-scale source target unresolved.'},indent=2,sort_keys=True))
