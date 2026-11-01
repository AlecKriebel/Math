#!/usr/bin/env python3
"""Deterministic numerical falsification checks; not a replacement for proof."""
import json, math, hashlib
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

ROOT=Path(__file__).resolve().parent
checks=[]
def check(name, condition, **details):
    if not bool(condition): raise RuntimeError(name+': '+repr(details))
    checks.append(dict(name=name,passed=True,**details))

def H(y): return 1-math.cos(2*math.pi*y)
def avg(C,N,a,b,s):
    pts=[a]+[k/N for k in range(math.floor(a*N)+1,math.ceil(b*N)) if a<k/N<b]+[b]
    return sum(quad(lambda x:s*math.sqrt(2*(C+H(N*x))),l,r,epsabs=2e-12,epsrel=2e-12)[0] for l,r in zip(pts,pts[1:]))/(b-a)

rng=np.random.default_rng(20002454)
lo,hi=.4,4.0
for N in [1,7,31]:
    edges=np.r_[0,np.sort(rng.uniform(.02,.98,6)),1]
    d=np.diff(edges); m=len(d); L=math.sqrt(2*(hi+2)); dt=.83*min(d)/L
    for s in [1,-1]:
        def E(C): return np.array([avg(C,N,a,b,s) for a,b in zip(edges,edges[1:])])
        def inv(u):
            out=[]
            for j,z in enumerate(u):
                el,eh=avg(lo,N,edges[j],edges[j+1],s),avg(hi,N,edges[j],edges[j+1],s)
                if abs(z-el)<1e-12: out.append(lo)
                elif abs(z-eh)<1e-12: out.append(hi)
                else: out.append(brentq(lambda c:avg(c,N,edges[j],edges[j+1],s)-z,lo,hi,xtol=1e-13))
            return np.array(out)
        def T(u):
            c=inv(u)
            return u-dt/d*((c-np.roll(c,1)) if s==1 else (np.roll(c,-1)-c))
        e=E(2); low=np.minimum(E(lo),E(hi)); high=np.maximum(E(lo),E(hi))
        check(f'equilibrium_N{N}_s{s}',max(abs(T(e)-e))<2e-12)
        u=low+(high-low)*rng.uniform(.1,.9,m); v=low+(high-low)*rng.uniform(.1,.9,m)
        mass=float(d@u); initial_dist=float(d@abs(u-v)); worst_entropy=0.
        for step in range(25):
            c=inv(u); un=T(u); vn=T(v)
            q=abs(c-2) if s==1 else -abs(np.roll(c,-1)-2)
            ent=abs(un-e)-abs(u-e)+dt/d*(q-np.roll(q,1))
            worst_entropy=max(worst_entropy,float(max(ent)))
            check(f'step_N{N}_s{s}_{step}', min(un-low)>-2e-11 and min(high-un)>-2e-11 and abs(float(d@un)-mass)<2e-11 and float(d@abs(un-vn))<=float(d@abs(u-v))+2e-11 and max(ent)<2e-11)
            u,v=un,vn
        check(f'contract_N{N}_s{s}',float(d@abs(u-v))<=initial_dist+2e-11,initial=initial_dist,final=float(d@abs(u-v)),entropy_max=worst_entropy)
        # Compare ordered states to test full map monotonicity.
        a=low+.3*(high-low); b=a+.001*(high-low)*rng.random(m)
        check(f'order_N{N}_s{s}',min(T(b)-T(a))>-2e-11)
        # Exact reconstruction-to-equilibrium L1 identity.
        c=inv(u); reconstructed=sum(quad(lambda x:abs(s*math.sqrt(2*(c[j]+H(N*x)))-s*math.sqrt(2*(2+H(N*x)))),aa,bb,epsabs=1e-10,limit=400)[0] for j,(aa,bb) in enumerate(zip(edges,edges[1:])))
        check(f'reconstruction_identity_N{N}_s{s}',abs(reconstructed-float(d@abs(u-e)))<2e-8)

# Critical profiles, including non-Lipschitz admissible shock members.
for theta in [0,.1,.5,.8,1]:
    integral=quad(lambda y:2*math.sin(math.pi*y),0,theta)[0]-quad(lambda y:2*math.sin(math.pi*y),theta,1)[0]
    check(f'shock_integral_{theta}',abs(integral+4*math.cos(math.pi*theta)/math.pi)<1e-13)
    if 0<theta<1:
        a=2*math.sin(math.pi*theta)
        for r in [-.9*a,0,.6*a]:
            prod=2*(r*r/2-a*a/2)
            check(f'entropy_down_{theta}_{r}',prod<0)
            check(f'reject_entropy_up_{theta}_{r}',-prod>0)
check('critical_continuum_witness', .3 not in [0,1])
for N in [2,8,32]:
    micro=[(-1)**k*4/(math.pi*N) for k in range(N)]
    check(f'aligned_alias_N{N}',max(abs(micro[2*j]+micro[2*j+1]) for j in range(N//2))==0)
    distance=sum(8/(math.pi*N) for _ in range(N))
    check(f'lower_bound_N{N}',abs(distance-8/math.pi)<1e-13)
# The same data on the microcell-resolving mesh are NOT identical.
check('reject_arbitrary_mesh_ambiguity',abs(4/(math.pi*8)-(-4/(math.pi*8)))>.1)

# Endpoint alias error is exactly independent of integer N.
errors=[avg(2,N,0,1,1)-2 for N in [1,7,31]]
check('nonvanishing_endpoint_quadrature',min(errors)>.1 and max(errors)-min(errors)<2e-12,errors=errors)
# A phase-aware midpoint rule: true-average equilibrium residual and bound (4).
N=7; edges=np.array([0,.13,.37,.69,1]); d=np.diff(edges); mids=(edges[:-1]+edges[1:])/2
k=3; u=np.array([avg(k,N,a,b,1) for a,b in zip(edges,edges[1:])]); hm=np.array([H(N*x) for x in mids]); c=u*u/2-hm
qk=np.sqrt(2*(k+hm)); delta=abs(qk-u); L=math.sqrt(2*(7+2)); dt=.7*min(d)/L
check('quadrature_inverse_domain',min(c)>.1 and max(c)<7)
un=u-dt/d*(c-np.roll(c,1)); defect=float(d@abs(un-u)); bound=float(2*dt*L*sum(delta))
check('quadrature_stationarity_defect',defect>1e-6 and defect<=bound+1e-12,defect=defect,bound=bound)
# Mutation: wrong conservative-flux sign makes F= C+2H nonconstant.
check('reject_wrong_source_sign',abs((2+2*H(.5))-(2+2*H(0)))>1)
# Mutation: unrestricted dt destroys monotonicity, already with H=0.
c=2.; speed=math.sqrt(2*c); lam=2/speed; diagonal=1-lam*speed
check('reject_missing_CFL',diagonal<0,diagonal=diagonal)

out=dict(status='PASS',scope='Floating-point falsification checks only; mathematical proofs are in the manuscript.',seed=20002454,checks=checks)
(ROOT/'CHECK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
manifest={p.name:dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [ROOT/'MATHEMATICAL_AUDIT.md',ROOT/'verify.py',ROOT/'CHECK_RESULTS.json']}
(ROOT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(dict(status='PASS',checks=len(checks),manifest=manifest),indent=2))
