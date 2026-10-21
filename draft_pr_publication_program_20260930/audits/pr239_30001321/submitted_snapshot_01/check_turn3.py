"""Exact controls for the final-segment closure, not an asymptotic proof.
Standard library only. Environment enumeration is exact, not Monte Carlo.
"""
from fractions import Fraction as F
from collections import defaultdict, Counter
from itertools import product
import json
counts=Counter()
def ck(value,label):
    assert value,label
    counts[label]+=1
def l1(p,q):return sum(abs(p.get(x,F(0))-q.get(x,F(0))) for x in p.keys()|q.keys())
def coarse(p,M,shift=0):
    out=defaultdict(F)
    for x,w in p.items():out[(x-shift)//M]+=w
    return dict(out)
def lazy(n,a,d=0,killed=False):
    mu={d:F(1)}
    for _ in range(n):
        nxt=defaultdict(F)
        for x,w in mu.items():
            for z,p in [(x-1,a),(x,1-2*a),(x+1,a)]:
                if not killed or z>0:nxt[z]+=w*p
        mu=dict(nxt)
    return mu
for a in [F(1,4),F(2,9),F(6,25)]:
    for n in range(21):
        base=lazy(n,a)
        for d in range(1,13):
            kill=lazy(n,a,d,True)
            reflected={z:base.get(z-d,F(0))-base.get(z+d,F(0)) for z in range(1,n+d+1)}
            ck(l1(kill,reflected)==0,'lazy_killed_reflection_kernel')
            survive=sum(kill.values())
            ck(survive==sum(base.get(j,F(0)) for j in range(1-d,d+1)),'lazy_reflection_survival_sum')
            ck(survive<=2*d*max(base.values()),'reflection_peak_bound')
def kernel(env,n,start,R=None,v=F(0)):
    mu={start:F(1)}
    for t in range(n):
        nxt=defaultdict(F)
        for x,w in mu.items():
            p=env[t,x]
            for z,a in [(x+1,p),(x-1,1-p)]:
                if R is None or abs(z-start-v*(t+1))<=R:nxt[z]+=w*a
        mu=dict(nxt)
    return mu
def couple(env,n,x0,y0):
    mu={(x0,y0):F(1)}
    for t in range(n):
        nxt=defaultdict(F)
        for (x,y),w in mu.items():
            if x==y:
                p=env[t,x];nxt[x+1,y+1]+=w*p;nxt[x-1,y-1]+=w*(1-p)
            else:
                p,q=env[t,x],env[t,y]
                for dx,px in [(1,p),(-1,1-p)]:
                    for dy,py in [(1,q),(-1,1-q)]:nxt[x+dx,y+dy]+=w*px*py
        mu=dict(nxt)
    return mu
laws=[((F(1,4),F(3,4)),(F(1,2),F(1,2))),((F(1,5),F(2,5)),(F(1,3),F(2,3)))]
for values,probs in laws:
    q=sum(v*w for v,w in zip(values,probs));a=q*(1-q)
    for n in range(1,4):
        sites=sorted({(t,x) for t in range(n) for st in [0,2] for x in range(st-t,st+t+1,2)})
        mean_survival=F(0);mean_l1=F(0)
        for bits in product((0,1),repeat=len(sites)):
            env=dict(zip(sites,(values[b] for b in bits)))
            weight=F(1)
            for b in bits:weight*=probs[b]
            joint=couple(env,n,0,2);first=defaultdict(F);second=defaultdict(F)
            for (x,y),w in joint.items():first[x]+=w;second[y]+=w
            px,py=kernel(env,n,0),kernel(env,n,2)
            ck(l1(dict(first),px)==0 and l1(dict(second),py)==0,'quenched_coupling_marginals')
            ck(all(x<=y for x,y in joint),'same_parity_order_preservation')
            survival=sum(w for (x,y),w in joint.items() if x!=y)
            distance=l1(px,py)
            ck(distance<=2*survival,'quenched_l1_coupling_bound')
            mean_survival+=weight*survival;mean_l1+=weight*distance
        ck(mean_survival==sum(lazy(n,a,1,True).values()),'annealed_coupling_lazy_survival')
        ck(mean_l1<=2*mean_survival,'averaged_kernel_coupling_bound')
# Direct strip-dependency tests, with biased and unbiased moving strips.
old={-2:F(1,6),0:F(1,3),2:F(1,2)};n=4
sites=sorted({(t,x) for t in range(n) for st in old for x in range(st-t,st+t+1,2)})
for v in [F(0),F(-1,3),F(3,5)]:
    for R in [1,2,3]:
        W=R
        strip={site:(F(site[1])-v*site[0])//W for site in sites}
        keys=sorted(set(strip.values()))
        weights={k:sum(w for x,w in old.items() if k*W-R-1<=x<=(k+1)*W+R+1) for k in keys}
        ck(sum(weights.values())<=6,'strip_influence_sum')
        ck(sum(w*w for w in weights.values())<=6*max(weights.values()),'strip_square_sum')
        for pattern in range(6):
            env={site:[F(1,7),F(2,5),F(4,5)][(j+pattern*(j%3+1))%3] for j,site in enumerate(sites)}
            original={x:kernel(env,n,x) for x in old}
            killed={x:kernel(env,n,x,R,v) for x in old}
            mixture=defaultdict(F);full=defaultdict(F)
            for x,w in old.items():
                for y,p in killed[x].items():mixture[y]+=w*p
                for y,p in original[x].items():full[y]+=w*p
            mixture,full=dict(mixture),dict(full)
            for y in mixture:ck(mixture[y]<=full.get(y,F(0)),'killed_kernel_is_subkernel')
            loss=1-sum(mixture.values())
            ck(l1(full,mixture)==loss,'unrestricted_killed_l1_is_loss')
            for k in keys:
                altered={site:(1-p if strip[site]==k else p) for site,p in env.items()}
                other={x:kernel(altered,n,x,R,v) for x in old}
                for x in old:
                    if not k*W-R-1<=x<=(k+1)*W+R+1:
                        ck(l1(killed[x],other[x])==0,'outside_influence_kernel_unchanged')
                changed=defaultdict(F)
                for x,w in old.items():
                    for y,p in other[x].items():changed[y]+=w*p
                changed=dict(changed)
                ck(l1(mixture,changed)<=2*weights[k],'single_strip_output_oscillation')
                for M in range(1,5):
                    for shift in range(M):
                        target=coarse(full,M,shift)
                        before=coarse(mixture,M,shift);after=coarse(changed,M,shift)
                        ck(abs(l1(before,target)-l1(after,target))<=2*weights[k],'single_strip_norm_oscillation')
                        ck(abs(l1(before,target)-l1(coarse(full,M,shift),target))<=loss,'coarse_killing_error_bound')
# Exact within-cell replacement identity with sparse reachable parity support.
from math import comb
for m in range(2,13):
    for q in [F(1,3),F(1,2),F(4,5)]:
        alpha={2*j-m:F(comb(m,j))*q**j*(1-q)**(m-j) for j in range(m+1)}
        Z=sum(F(j+1) for j in range(m+1));mu={2*j-m:F(j+1)/Z for j in range(m+1)}
        for H in range(1,8):
            for shift in range(H):
                ca,cm=coarse(alpha,H,shift),coarse(mu,H,shift)
                prime={x:cm[(x-shift)//H]*p/ca[(x-shift)//H] for x,p in alpha.items()}
                ck(sum(prime.values())==1,'replacement_probability_mass')
                ck(coarse(prime,H,shift)==cm,'replacement_cell_masses')
                ck(l1(prime,alpha)==l1(cm,ca),'replacement_l1_identity')
# Explicit exponent margins in the final mesoscopic choice.
ck(F(5,16)>F(1,4),'auxiliary_scale_in_turn2_range')
ck(F(5,16)-F(3,8)==-F(1,16),'coupling_error_exponent')
ck(F(1,32)+F(1,2)-2*F(3,8)==-F(7,32),'soft_interval_variance_exponent')
ck(-2*F(1,32)+F(7,32)==F(5,32),'soft_interval_tail_exponent')
ck(F(1,8)>F(1,32),'soft_interval_mean_margin')
# Opposite parity would invalidate the coalescence conclusion; this is excluded.
ck(all((x-y)%2 for x in [-3,-1,1,3] for y in [-2,0,2,4]),'opposite_parity_negative_control')
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'families':dict(sorted(counts.items())),'scope':'Exact finite coupling, reflection, moving-strip sensitivity, killed-mass and replacement controls. The all-scale asymptotic theorem requires the analytic proof and separate review.'},indent=2,sort_keys=True))
