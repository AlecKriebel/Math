"""Independent exact finite controls for the frozen 30001321 candidate.
Written for this review, with no import of any author's checker.
The analytic proof, not finite controls, establishes the asymptotic conclusion.
"""
from fractions import Fraction as Q
from collections import defaultdict, Counter
from itertools import product
from math import comb, factorial
import json
C=Counter()
def check(x,label):
    assert x,label
    C[label]+=1
def convolve(p,q,n):
    return [sum((p[i]*q[k-i] for i in range(k+1) if i<len(p) and k-i<len(q)),Q()) for k in range(n+1)]
def advance_pair(mu,q,delta,coalesce=False):
    out=defaultdict(Q); a=q*(1-q)
    for (x,y),w in mu.items():
        if x==y:
            choices=[(1,1,q),(-1,-1,1-q)] if coalesce else [(1,1,q-delta),(-1,-1,1-q-delta),(1,-1,delta),(-1,1,delta)]
        else:
            choices=[(i,j,pi*pj) for i,pi in [(1,q),(-1,1-q)] for j,pj in [(1,q),(-1,1-q)]]
        for dx,dy,p in choices:out[x+dx,y+dy]+=w*p
    return dict(out)
def sticky_step(mu,a,delta):
    out=defaultdict(Q)
    for x,w in mu.items():
        d=delta if x==0 else a
        for y,p in [(x-1,d),(x,1-2*d),(x+1,d)]:out[y]+=w*p
    return dict(out)
def l1(p,q):return sum((abs(p.get(x,Q())-q.get(x,Q())) for x in p.keys()|q.keys()),Q())
# A polynomial identity for the return resolvent, rather than a symbolic sqrt expansion.
for q in [Q(1,100),Q(2,7),Q(1,2),Q(8,9)]:
 a=q*(1-q)
 for ratio in [Q(1,100),Q(1,3),Q(1)]:
  delta=ratio*a; mu={0:Q(1)}; g=[]
  for n in range(25):
   g.append(mu.get(0,Q()));check(sum(mu.values())==1,'sticky_mass')
   if n:check(g[-1]<=g[-2],'return_decreases')
   mu=sticky_step(mu,a,delta)
  # delta^2/a^2 * (1-z)(1-(1-4a)z)G^2 = [1-(1-delta/a)(1-z)G]^2.
  left=convolve([ratio*ratio,-ratio*ratio*(2-4*a),ratio*ratio*(1-4*a)],convolve(g,g,24),24)
  temp=convolve([1,-1],g,24);right_poly=[- (1-ratio)*x for x in temp];right_poly[0]+=1
  right=convolve(right_poly,right_poly,24)
  for x,y in zip(left,right):check(x==y,'return_resolvent_squared_identity')
  u={0:Q(1)}
  for n in range(18):
   check(u[0]==g[n],'forward_backward_return')
   for d in range(n+1):check(u.get(d,Q())>=u.get(d+1,Q())>=0,'backward_radial_order')
   u={d:(1-2*(delta if d==0 else a))*u.get(d,Q())+(delta if d==0 else a)*(u.get(d-1,Q())+u.get(d+1,Q())) for d in range(-n-1,n+2)}
  # Direct two-particle propagation from a genuinely nontrivial old law.
  old={-2:Q(1,7),0:Q(2,7),4:Q(4,7)}
  pair={(x,y):px*py for x,px in old.items() for y,py in old.items()}
  difference=defaultdict(Q)
  for (x,y),w in pair.items():difference[(x-y)//2]+=w
  for n in range(10):
   got=defaultdict(Q)
   for (x,y),w in pair.items():got[(x-y)//2]+=w
   check(l1(dict(got),dict(difference))==0,'arbitrary_old_law_replica_transition')
   check(got[0]<=g[n],'arbitrary_old_law_overlap_bound')
   pair=advance_pair(pair,q,delta);difference=sticky_step(difference,a,delta)
# Coalescing pair checked directly against absorbing lazy recurrence.
for q in [Q(1,11),Q(3,8),Q(1,2),Q(7,9)]:
 a=q*(1-q)
 for d in range(1,7):
  pair={(0,2*d):Q(1)};killed={d:Q(1)};free={0:Q(1)}
  for n in range(13):
   check(all(x<=y for x,y in pair),'coalescence_order')
   survival=sum((w for (x,y),w in pair.items() if x!=y),Q())
   check(survival==sum(killed.values()),'coalescence_absorbing_walk')
   check(survival==sum((free.get(j,Q()) for j in range(1-d,d+1)),Q()),'reflection_survival_direct')
   px=defaultdict(Q);py=defaultdict(Q)
   for (x,y),w in pair.items():px[x]+=w;py[y]+=w
   check(l1(dict(px),dict(py))<=2*survival,'annealed_pair_coupling_bound')
   pair=advance_pair(pair,q,a,True)
   killed={x:w for x,w in sticky_step(killed,a,a).items() if x>0}
   free=sticky_step(free,a,a)
# Independent complete enumeration of a three-valued environment through time three.
values=[Q(1,10),Q(1,2),Q(4,5)];probs=[Q(1,4),Q(1,3),Q(5,12)]
q=sum((p*w for p,w in zip(values,probs)),Q());delta=sum((w*p*(1-p) for p,w in zip(values,probs)),Q());a=q*(1-q)
mu={0:Q(1)};g=[]
for n in range(4):g.append(mu.get(0,Q()));mu=sticky_step(mu,a,delta)
sites=[(t,x) for t in range(3) for x in range(-t,t+1,2)]
prefix_groups=[defaultdict(list) for _ in range(4)]
for indices in product(range(3),repeat=len(sites)):
 env={s:values[j] for s,j in zip(sites,indices)};w=Q(1)
 for j in indices:w*=probs[j]
 mu={0:Q(1)};overlaps=[Q(1)]
 for t in range(3):
  out=defaultdict(Q)
  for x,p in mu.items():out[x+1]+=p*env[t,x];out[x-1]+=p*(1-env[t,x])
  mu=dict(out);overlaps.append(sum((p*p for p in mu.values()),Q()))
 for s in range(4):prefix_groups[s][indices[:s*(s+1)//2]].append((w,overlaps))
for s in range(4):
 for records in prefix_groups[s].values():
  mass=sum((w for w,_ in records),Q())
  for L in range(1,5-s):
   A=sum(g[:L],Q())
   for k in range(1,7):
    moment=sum((w*sum(Is[s:s+L],Q())**k for w,Is in records),Q())/mass
    check(moment<=factorial(k)*A**k,'conditional_repeated_index_occupation_moment')
# Path-sum implementation, not a forward kernel recursion, verifies moving-strip dependence.
def path_kernel(env,steps,start,drift,radius=None):
 out=defaultdict(Q);used=set()
 for increments in product([-1,1],repeat=steps):
  x=start;weight=Q(1);alive=True
  for t,dx in enumerate(increments):
   used.add((t,x));p=env[t,x];weight*=p if dx==1 else 1-p;x+=dx
   if radius is not None and abs(x-start-drift*(t+1))>radius:alive=False;break
  if alive:out[x]+=weight
 return dict(out),used
old={-4:Q(2,11),0:Q(3,11),2:Q(6,11)};steps=5
sites=sorted({(t,x) for t in range(steps) for start in old for x in range(start-t,start+t+1,2)})
def coarse(mu,width,shift):
 out=defaultdict(Q)
 for x,p in mu.items():out[(Q(x)-shift)//width]+=p
 return dict(out)
for drift in [Q(-3,5),Q(0),Q(2,7),Q(9,10)]:
 for radius in [1,2,4]:
  strips={site:(Q(site[1])-drift*site[0])//radius for site in sites};keys=sorted(set(strips.values()))
  weights={k:sum((p for x,p in old.items() if k*radius-radius-1<=x<=(k+1)*radius+radius+1),Q()) for k in keys}
  check(sum(weights.values())<=6,'influence_total_mass')
  check(sum((w*w for w in weights.values()),Q())<=6*max(weights.values()),'influence_squared_mass')
  for pattern in range(3):
   env={site:Q(1+((j*j+3*j+pattern)%12),14) for j,site in enumerate(sites)}
   killed={};full={};mix=defaultdict(Q);allmix=defaultdict(Q)
   for x,px in old.items():
    killed[x],used=path_kernel(env,steps,x,drift,radius);full[x],_=path_kernel(env,steps,x,drift)
    check(all(abs(Q(y)-drift*t-x)<=radius for t,y in used),'used_variables_inside_alive_tube')
    for y,p in killed[x].items():mix[y]+=px*p
    for y,p in full[x].items():allmix[y]+=px*p
   mix=dict(mix);allmix=dict(allmix);loss=1-sum(mix.values())
   check(l1(mix,allmix)==loss,'path_sum_killing_loss')
   for k in keys:
    changed={site:(Q(13,14) if p<Q(1,2) else Q(1,14)) if strips[site]==k else p for site,p in env.items()};other=defaultdict(Q)
    for x,px in old.items():
     row,_=path_kernel(changed,steps,x,drift,radius)
     if not k*radius-radius-1<=x<=(k+1)*radius+radius+1:check(row==killed[x],'out_of_strip_influence_unchanged')
     for y,p in row.items():other[y]+=px*p
    other=dict(other);check(l1(mix,other)<=2*weights[k],'strip_subprobability_output_bound')
    for width in [Q(1),Q(5,2),Q(7,3),Q(9)]:
     for shift in [Q(0),Q(1,3),Q(-4,7)]:
      target=coarse({-1:Q(1,3),7:Q(2,3)},width,shift)
      c1,c2=coarse(mix,width,shift),coarse(other,width,shift)
      check(abs(l1(c1,target)-l1(c2,target))<=2*weights[k],'strip_nonlinear_norm_bound_real_cells')
      check(abs(l1(c1,target)-l1(coarse(allmix,width,shift),target))<=loss,'killed_full_norm_difference')
# Uniform point-mass gradients and periodic residues: exact finite inequalities.
for n in range(1,61):
 for q in [Q(1,5),Q(2,3),Q(1,2)]:
  b={2*j-n:Q(comb(n,j))*q**j*(1-q)**(n-j) for j in range(n+1)};peak=max(b.values())
  diff={x:b.get(x+2,Q())-b.get(x,Q()) for x in range(-n-2,n+1,2)}
  check(sum(abs(x) for x in diff.values())==2*peak,'parity_kernel_variation')
  for M in range(1,13):
   for shift in range(M):
    total=sum((p for x,p in b.items() if (x-shift)%M==0),Q())
    check(total<=Q(2,M)+2*peak,'residue_bound_with_parity')
# All exponent comparisons as exact identities, including gamma very close to 1/4.
for d in [Q(1,10**j) for j in range(1,10)]+[Q(1,7),Q(2,9)]:
 gamma=Q(1,4)+d;beta=(gamma+Q(1,4))/2;eta=d/4
 check(beta-eta-(Q(1,2)-gamma)==5*d/4>0,'sign_entropy_margin')
 check(2*beta-Q(1,2)-eta==3*d/4>0,'boundary_variance_margin')
 check(gamma-beta==d/2>0,'boundary_vs_cell_margin')
eta=Q(1,32);kappa=Q(1,32);b=Q(3,8)
check(-(eta+Q(1,2)-2*b)-2*kappa==Q(5,32),'old_mass_freedman_variance_exponent')
check(b-kappa>Q(5,32),'old_mass_increment_exponent')
check(Q(5,16)-Q(3,8)==-Q(1,16),'coalescence_scale_margin')
check(Q(1,2)-Q(3,8)>kappa,'old_mean_vs_threshold_margin')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(sorted(C.items())),'scope':'Independent exact finite controls. No asymptotic theorem, novelty, or source disposition follows from finite checks alone.'},indent=2,sort_keys=True))
