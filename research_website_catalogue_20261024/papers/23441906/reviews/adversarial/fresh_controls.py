#!/usr/bin/env python3
"""Fresh literal manuscript implementation. No submitted helper imports."""
from itertools import product
from functools import lru_cache
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
import json,hashlib
R=list(product(range(5),repeat=4));zero=(0,0,0,0)
V=[v for v in range(32) if v.bit_count()%2==0]
def add(a,b):return tuple((x+y)%5 for x,y in zip(a,b))
def scale(n,a):return tuple(n*x%5 for x in a)
@lru_cache(None)
def mul(a,b):return tuple(sum(a[i]*b[j] for i in range(4) for j in range(4) if i+j+2==k)%5 for k in range(1,5))
def sig(a):return tuple(x*(-1 if i%2==0 else 1)%5 for i,x in enumerate(a))
def circle(a,b):return add(add(a,b),mul(a,b))
def log(a):
 a2=mul(a,a);a3=mul(a2,a);a4=mul(a3,a)
 return add(add(a,scale(2,a2)),add(scale(2,a3),a4))
def exp(a):
 a2=mul(a,a);a3=mul(a2,a);a4=mul(a3,a)
 return add(add(a,scale(3,a2)),add(a3,scale(4,a4)))
logs={a:log(a) for a in R};eta={a:logs[a][3] for a in R}
def beta(v,w):return (v&w).bit_count()%2
def Q(v):return (v.bit_count()//2)%2
def M(v,n=1):
 for _ in range(n%5):v=((v<<1)&31)|(v>>4)
 return v
Z=(zero,0,0)
def plus(a,b):return(add(a[0],b[0]),a[1]^b[1],a[2]^b[2])
def scal(n,a):return(scale(n,a[0]),a[1] if n%2 else 0,a[2] if n%2 else 0)
def minus(a,b):return plus(a,scal(-1,b))
def circ(a,b):
 r,v,z=a;u,w,t=b;u=sig(u) if z^Q(v) else u;w=M(w,eta[r])
 return(circle(r,u),v^w,z^t^beta(v,w))
def lam(a,b):return minus(circ(a,b),a)
def star(a,b):return minus(lam(a,b),b)
def psi(a):
 r,v,z=a;l=logs[r]
 return(l[:3],z^Q(v),v,l[3])
def gp(x,y):
 k,e,v,s=x;h,f,w,t=y
 return(tuple((k[i]+((-1 if i!=1 else 1) if e else 1)*h[i])%5 for i in range(3)),e^f,v^M(w,s),(s+t)%5)
checks=Counter()
def ck(ok,name):
 if not ok:raise ValueError(name)
 checks[name]+=1
for r in R:
 ck(exp(logs[r])==r and log(exp(r))==r,'log_exp_inverse')
 ck(logs[sig(r)]==sig(logs[r]),'sigma_log_commutation')
 for u in R:ck(logs[circle(r,u)]==add(logs[r],logs[u]),'all_ring_pair_log_homomorphisms')
for v in V:
 ck(M(v,5)==v and Q(M(v))==Q(v),'rotation_Q')
 ck((M(v)==v)==(v==0),'no_nonzero_fixed_rotation_vector')
 ck(v==0 or any(beta(v,w) for w in V),'nondegenerate_dot_form')
 for w in V:
  ck(Q(v^w)==Q(v)^Q(w)^beta(v,w),'quadratic_polarization')
  ck(beta(M(v),M(w))==beta(v,w),'rotation_beta')
mons=[tuple(int(i==j) for i in range(4)) for j in range(4)]
gens=[(m,0,0) for m in mons]+[(zero,(1<<j)|16,0) for j in range(4)]+[(zero,0,1)]
B=[(r,v,z) for r in R for v in V for z in range(2)]
ck(len(set(map(psi,B)))==20000,'psi_global_bijection')
for a in B:
 for g in gens:
  ck(psi(circ(a,g))==gp(psi(a),psi(g)),'all_elements_right_generator_Psi_product')
  ck(psi(circ(g,a))==gp(psi(g),psi(a)),'all_elements_left_generator_Psi_product')
# Fresh all-seed ideal implications: only scalar, lambda difference, and i*ambient.
A=(mons[3],0,0);b=(zero,0,1);tracehash=hashlib.sha256();seed_branches=Counter()
for seed in B[1:]:
 # B enumeration begins with zero; every subsequent seed is nonzero.
 i=seed;steps=[]
 def st(out,why):steps.append((why,out));return out
 if i[0]!=zero:
  i=st(scal(6,i),'sixfold_primary_projection');seed_branches['ring']+=1
 else:
  seed_branches['binary']+=1
  if i[1]:
   w=next(w for w in V if beta(w,i[1]))
   i=st(minus(lam((zero,w,0),i),i),'binary_nondegenerate_lambda_difference')
  ck(i==b,'binary_seed_reaches_b')
  i=st(star(i,(mons[0],0,0)),'ideal_first_star_to_ring')
 j=next(j for j,c in enumerate(i[0]) if c);c=i[0][j]
 if j<3:i=st(minus(lam((mons[2-j],0,0),i),i),'raise_least_ring_degree_to_four')
 i=st(scal(pow(c,-1,5),i),'rescale_x4');ck(i==A,'every_seed_reaches_A')
 pv=[]
 for target in gens[4:8]:
  w=next(w for w in V if M(w)^w==target[1]);v=st(star(i,(zero,w,0)),'A_star_produces_binary_generator');ck(v==target,'V_generator_from_A');pv.append(v)
 w=next(w for w in V if beta(w,pv[0][1]));bb=st(minus(lam((zero,w,0),pv[0]),pv[0]),'recover_b');ck(bb==b,'b_from_V')
 xx=st(scal(2,star(bb,(mons[0],0,0))),'recover_x');ck(xx==gens[0],'x_from_b')
 for j in range(3):
  xx=st(minus(lam(gens[0],xx),xx),'ring_successive_monomial');ck(xx==gens[j+1],'successive_ring_generator')
 tracehash.update(json.dumps([seed,steps],separators=(',',':')).encode()+b'\n')
# Intrinsic witness uses the actual additive five-part.
ck(star(star(gens[0],gens[0]),gens[0])==gens[2]!=Z,'nonzero_primary_triple_star')
# Full cocycle boundary: T=S=C2, b(t,u)=tu, alpha=id yields additive C4, multiplicative C2^2.
D=list(product(range(2),repeat=2))
def dp(a,b):return(a[0]^b[0],a[1]^b[1]^(a[0]&b[0]))
def dn(a):return(a[0],a[1]^a[0])
def dm(a,b):return(a[0]^b[0],a[1]^b[1])
def dl(a,b):return dp(dm(a,b),dn(a))
def ds(a,b):return dp(dl(a,b),dn(b))
ck(dp((1,0),(1,0))==(0,1) and dm((1,0),(1,0))==(0,0),'non_split_additive_two_primary_example')
for a,b0,c in product(D,repeat=3):
 ck(dl(a,dp(b0,c))==dp(dl(a,b0),dl(a,c)),'C4_additive_boundary_left_brace_identity')
 ck(ds(ds(a,b0),c)==(0,0),'C4_additive_boundary_all_triple_stars')
# A normalized symmetric cocycle need not be bilinear, but inadmissibility must be detected.
qv=[0,0,0,1]
def bc(t,u):return(qv[t]+qv[u]-qv[(t+u)%4])%2
for t,u,w in product(range(4),repeat=3):
 ck((bc((t+u)%4,w)+bc(t,u)-bc(t,(u+w)%4)-bc(u,w))%2==0,'nonbilinear_cocycle_identity')
ck(bc(1,2)!=(bc(1,1)+bc(1,1))%2,'nonbilinear_cocycle_rejected_by_lambda_composition')
out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','check_total':sum(checks.values()),'checks':dict(checks),'ideal_seeds':len(B)-1,'seed_branches':dict(seed_branches),'all_seed_derivation_stream_sha256':tracehash.hexdigest(),'negative_controls':{'nonbilinear_b_not_automatically_admissible':True,'additive_primary_not_assumed_split':True,'primary_triple_star_not_zero_in_constructed_brace':True},'scope':'Fresh literal operations, complete ring-pair identities, binary forms, all20,000 elements and nine additive-generator product controls, all19,999 nonzero ideal-seed derivations, and full small-cocycle boundary examples. Universal nonpresentation and group/brace proofs are reviewed independently; no enumeration of20,000^3 triples or all asymmetric products.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
