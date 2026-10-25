"""Fresh exact adversarial controls. No imported archive checkers, no simulations.
Independent mechanisms: exact Q(sqrt(2)) strip geometry, complete conditional
strip exposure of the nonlinear norm, and general unimodal residue sequences.
Finite controls supplement the analytic review; they do not prove asymptotics.
"""
from fractions import Fraction as Q
from collections import Counter, defaultdict
from itertools import product
from math import comb
from datetime import datetime, timezone
import json, hashlib
from pathlib import Path
C=Counter()
def check(value,key):
    if not value: raise RuntimeError(key)
    C[key]+=1

def sgn(q): return (q>0)-(q<0)
# A surd is exactly a+b*sqrt(2), with rational a,b; no float comparisons.
def sign(z):
    a,b=z
    if not a: return sgn(b)
    if not b or sgn(a)==sgn(b): return sgn(a)
    return sgn(a)*sgn(a*a-2*b*b)
def add(z,w): return (z[0]+w[0],z[1]+w[1])
def scale(z,r): return (z[0]*r,z[1]*r)
def le(z,w): return sign(add(z,scale(w,-1)))<=0
def floor_surd(z):
    lo,hi=-1,1
    while le(z,(Q(lo),Q(0))): lo*=2
    while le((Q(hi),Q(0)),z): hi*=2
    while hi-lo>1:
        mid=(lo+hi)//2
        if le((Q(mid),Q(0)),z): lo=mid
        else: hi=mid
    return lo
for a,b in product(range(-6,7),repeat=2):
    z=(Q(a,3),Q(b,5)); k=floor_surd(z)
    check(le((Q(k),Q(0)),z) and not le((Q(k+1),Q(0)),z),'surd_floor_exact_bracket')
# Three irrational drifts, path-read geometry including all time-boundary cases.
geometry=0; exit_return=False
for v in [(Q(0),Q(1,2)),(Q(0),Q(-1,2)),(Q(-1,2),Q(1,2))]:
 for R in (1,2,4):
  for steps in range(1,8):
   for start in (-5,0,4):
    for increments in product((-1,1),repeat=steps):
     y=start; alive=True
     for t,dx in enumerate(increments):
      shifted=add((Q(y),Q(0)),scale(v,-t))
      if alive:
       check(le((Q(start-R),Q(0)),shifted) and le(shifted,(Q(start+R),Q(0))),'irrational_alive_read_tube')
       k=floor_surd(scale(shifted,Q(1,R)))
       check(k*R-R-1<=start<=(k+1)*R+R+1,'irrational_read_strip_influence')
      y+=dx
      deviation=add((Q(y-start),Q(0)),scale(v,-(t+1)))
      if not le((Q(-R),Q(0)),deviation) or not le(deviation,(Q(R),Q(0))): alive=False
     endpoint=add((Q(y-start),Q(0)),scale(v,-steps))
     exit_return |= (not alive and le((Q(-R),Q(0)),endpoint) and le(endpoint,(Q(R),Q(0))))
     geometry+=1
check(exit_return,'irrational_exit_return_requires_maximal_killing')

def norm(a,b): return sum((abs(a.get(k,Q())-b.get(k,Q())) for k in a.keys()|b.keys()),Q())
def coarse(mu,width,offset):
 out=defaultdict(Q)
 for x,p in mu.items(): out[(Q(x)-offset)//width]+=p
 return dict(out)
def binomial(n,q): return {2*j-n:Q(comb(n,j))*q**j*(1-q)**(n-j) for j in range(n+1)}
def row(env,start,n,R,v):
 out=defaultdict(Q)
 # Enumerate path words rather than evolve endpoint masses.
 for word in product((-1,1),repeat=n):
  x=start; p=Q(1)
  for t,dx in enumerate(word):
   p*=env[t,x] if dx==1 else 1-env[t,x]
   x+=dx
   if abs(x-start-v*(t+1))>R: break
  else: out[x]+=p
 return dict(out)
values=(Q(1,8),Q(5,6)); weights=(Q(2,7),Q(5,7))
q=sum(p*w for p,w in zip(values,weights)); v=2*q-1
starts=(-2,0,2); n=2
sites=sorted({(t,x+z) for x in starts for t in range(n) for z in range(-t,t+1,2)})
worlds_count=0
for R in (1,2):
 strip={s:(Q(s[1])-v*s[0])//R for s in sites}; keys=sorted(set(strip.values()))
 for old in ({-2:Q(5,11),0:Q(4,11),2:Q(2,11)},{0:Q(1)}):
  w={k:sum((p for x,p in old.items() if k*R-R-1<=x<=(k+1)*R+R+1),Q()) for k in keys}
  for width,offset in ((Q(3,2),Q(1,7)),(Q(7,3),Q(-2,5)),(Q(2),Q())):
   target=coarse(binomial(4,q),width,offset); worlds=[]
   for labels in product((0,1),repeat=len(sites)):
    env={s:values[j] for s,j in zip(sites,labels)}
    probability=Q(1)
    for j in labels: probability*=weights[j]
    mix=defaultdict(Q)
    for x,px in old.items():
     for y,py in row(env,x,n,R,v).items(): mix[y]+=px*py
    result=norm(coarse(mix,width,offset),target)
    worlds.append((labels,probability,result)); worlds_count+=1
   check(sum((p for _,p,_ in worlds),Q())==1,'complete_world_probability')
   mean=sum((p*f for _,p,f in worlds),Q())
   variance=sum((p*(f-mean)**2 for _,p,f in worlds),Q())
   increment_variance=Q()
   previous={():mean}
   exposed=[]
   # Exact Doob martingale of the actual nonlinear F-dagger, strip by strip.
   for k in keys:
    old_exposed=list(exposed)
    exposed += [j for j,s in enumerate(sites) if strip[s]==k]
    grouped=defaultdict(lambda:[Q(),Q()]); parent_children=defaultdict(list)
    for labels,p,f in worlds:
     prefix=tuple(labels[j] for j in exposed)
     grouped[prefix][0]+=p; grouped[prefix][1]+=p*f
    current={key:total/mass for key,(mass,total) in grouped.items()}
    for prefix,value in current.items():
     parent=prefix[:len(old_exposed)]
     parent_children[parent].append(value)
     increment_variance+=grouped[prefix][0]*(value-previous[parent])**2
    for parent,vals in parent_children.items():
     check(max(vals)-min(vals)<=2*w[k],'nonlinear_strip_conditional_range')
    previous=current
   check(increment_variance==variance,'exact_doob_variance_decomposition')
   check(variance<=sum((x*x for x in w.values()),Q()),'strip_bounded_range_variance')
   check(sum(w.values(),Q())<=6 and sum((x*x for x in w.values()),Q())<=6*max(w.values()),'actual_strip_weight_bounds')
# General unimodal sequences, beyond binomial profiles, test the residue lemma.
unimodal_sequences=0
for length in range(1,8):
 for raw in product(range(1,4),repeat=length):
  if not any(all(raw[j]<=raw[j+1] for j in range(mode)) and all(raw[j]>=raw[j+1] for j in range(mode,length-1)) for mode in range(length)): continue
  total=sum(raw); p=[Q(x,total) for x in raw]; unimodal_sequences+=1
  for D in range(1,10):
   for residue in range(D):
    mass=sum((x for i,x in enumerate(p) if i%D==residue),Q())
    check(mass<=Q(1,D)+2*max(p),'general_unimodal_residue')
# Omitted independence is essential even with probabilities strictly inside (0,1).
# Environment is one global random p=1/4 or3/4; this is deliberately outside iid scope.
a=coarse(binomial(32,Q(1,4)),Q(4),Q()); b=coarse(binomial(32,Q(3,4)),Q(4),Q())
mean={k:(a.get(k,Q())+b.get(k,Q()))/2 for k in a.keys()|b.keys()}
non_iid_gap=norm(a,mean)
check(non_iid_gap>Q(9,10),'strict_ellipticity_without_independence_fails_control')
# Exact exponent arithmetic, including gamma arbitrarily close to the endpoint.
for j in range(1,30):
 d=Q(1,10**j); beta=Q(1,4)+d/2; eta=d/4; gamma=Q(1,4)+d
 check(beta-eta-(Q(1,2)-gamma)==5*d/4 and 2*beta-Q(1,2)-eta==3*d/4,'auxiliary_strict_positive_margins')
check(Q(1,32)+Q(1,2)-2*Q(3,8)==-Q(7,32) and Q(7,32)-2*Q(1,32)==Q(5,32),'old_mass_tail_margin')
check(Q(5,16)-Q(3,8)==-Q(1,16),'conditional_mean_coupling_margin')
print(json.dumps({'status':'PASS','UTC':datetime.now(timezone.utc).isoformat(),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'checks':sum(C.values()),'families':dict(C),'irrational_path_cases':geometry,'strip_world_functional_cases':worlds_count,'unimodal_sequences':unimodal_sequences,'non_iid_negative_control_gap':str(non_iid_gap),'scope':'Exact finite rational and quadratic-surd checks; no asymptotic or novelty certification. No archive checker imported.'},indent=2))
