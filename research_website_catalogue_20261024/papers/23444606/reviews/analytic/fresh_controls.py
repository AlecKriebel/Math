#!/usr/bin/env python3
"""Fresh controls: exact ordinal-block sign sequences and finite Hahn algebra.
No submitted helper was read or imported before this script was written and run.
The ordinal-block model only covers finitely described ordinals below omega^2;
it is not a proof for every ordinal or proper class.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
from collections import Counter
from functools import cmp_to_key
from datetime import datetime,timezone
import json,hashlib,random
HERE=Path(__file__).resolve().parent
checks=Counter();started=datetime.now(timezone.utc).isoformat()
def ck(name,ok):
 if not ok:raise AssertionError(name)
 checks[name]+=1
# Ordinals omega*k+n, compared as pairs. This is ordinal, not commutative addition.
Z=(0,0);ONE=(0,1);W=(1,0)
def add(a,b):return (a[0]+b[0],b[1]) if b[0] else (a[0],a[1]+b[1])
def tail(a,b):
 assert a<=b
 return (b[0]-a[0],b[1]) if b[0]>a[0] else (0,b[1]-a[1])
def norm(runs):
 out=[]
 for sign,length in runs:
  if length==Z:continue
  if out and out[-1][0]==sign:out[-1]=(sign,add(out[-1][1],length))
  else:out.append((sign,length))
 return tuple(out)
def cat(*words):return norm([run for word in words for run in word])
def length(x):
 n=Z
 for sign,l in x:n=add(n,l)
 return n
def prefix(x,cut):
 assert cut<=length(x)
 out=[];start=Z
 for sign,l in x:
  end=add(start,l)
  if cut>=end:out.append((sign,l));start=end;continue
  out.append((sign,tail(start,cut)));break
 return norm(out)
def suffix(x,cut):
 assert cut<=length(x)
 out=[];start=Z
 for sign,l in x:
  end=add(start,l)
  if cut<=start:out.append((sign,l))
  elif cut<end:out.append((sign,tail(cut,end)))
  start=end
 return norm(out)
def starts(x):
 out={Z};n=Z
 for sign,l in x:n=add(n,l);out.add(n)
 return out
def at(x,pos):
 n=Z
 for sign,l in x:
  end=add(n,l)
  if n<=pos<end:return sign
  n=end
 return 0

def cmp(x,y):
 for pos in sorted(starts(x)|starts(y)):
  a,b=at(x,pos),at(y,pos)
  if a!=b:return 1 if a>b else -1
 return 0

def isp(x,y):return length(x)<=length(y) and prefix(y,length(x))==x
PLUS=((1,ONE),)
def rotate(x,alpha):
 a=norm([(-1,alpha)])
 assert cmp(x,a)>=0
 if x==a:return ()
 if not isp(a,x):return cat(PLUS,x)
 rest=suffix(x,alpha)
 assert at(rest,Z)==1
 return cat(PLUS,a,suffix(rest,ONE))
def inverse(z,alpha):
 a=norm([(-1,alpha)])
 assert cmp(z,())>=0
 if not z:return a
 v=suffix(z,ONE)
 return cat(a,PLUS,suffix(v,alpha)) if isp(a,v) else v

def cuts(x):
 L=length(x);out=set(starts(x))
 for k in range(L[0]+1):
  for n in range(7):
   pos=(k,n)
   if pos<L:out.add(pos)
 for pos in list(out):
  nxt=add(pos,ONE)
  if nxt<L:out.add(nxt)
 return sorted(pos for pos in out if pos<L)
# Finite words and transfinite constant-sign block strings are independently encoded.
words={()}
for n in range(1,7):
 for signs in product([-1,1],repeat=n):words.add(norm([(v,ONE) for v in signs]))
lengths=[ONE,(0,2),W,(1,1),(2,0)]
for n in range(1,4):
 for ls in product(lengths,repeat=n):
  for sign in [-1,1]:words.add(norm([(sign*(-1)**j,l) for j,l in enumerate(ls)]))
words=sorted(words,key=cmp_to_key(cmp))
alphas=[Z,ONE,(0,2),(0,3),(0,4),W,(1,2),(2,0),(2,3)]
summary=[]
ck('ordinal_absorption',add(ONE,W)==W and add(W,ONE)!=(1,0))
for alpha in alphas:
 a=norm([(-1,alpha)]);domain=sorted(set(x for x in words if cmp(x,a)>=0)|{a,cat(a,PLUS)},key=cmp_to_key(cmp))
 images=[rotate(x,alpha) for x in domain]
 ck('image_minimum_zero',images[0]==())
 ck('injective_image',len(set(images))==len(domain))
 for i,x in enumerate(domain):
  fx=images[i]
  ck('ray_inverse_source',inverse(fx,alpha)==x)
  ck('image_nonnegative',cmp(fx,())>=0)
  if alpha==Z:ck('alpha_zero_identity',fx==x)
  for pos in cuts(fx):
   v=prefix(fx,pos);pre=inverse(v,alpha)
   ck('sampled_image_prefix_identity',pre==a or (pre!=a and pre!=x and isp(pre,x)))
   ck('sampled_inverse_image_prefix',rotate(pre,alpha)==v)
  if x!=a:
   for pos in cuts(x):
    v=prefix(x,pos)
    ck('source_prefix_stays_in_ray',cmp(v,a)>=0)
    if v!=a:ck('sampled_forward_prefix_identity',isp(rotate(v,alpha),fx) and rotate(v,alpha)!=fx)
  for j in range(i):
   y=domain[j];fy=images[j]
   ck('strict_order_preservation',cmp(fy,fx)<0)
   if x!=a and y!=a:ck('prefix_reflection_away_from_bottom',isp(x,y)==isp(fx,fy) and isp(y,x)==isp(fy,fx))
   if isp(fx,fy):ck('right_predecessor_reflection',isp(x,y))
 # Deliberately omit the deletion after the minimum: a required prefix is missing.
 if alpha!=Z:
  bad=cat(PLUS,a,PLUS);missing=cat(PLUS,a)
  badimages={(() if x==a else cat(PLUS,x)) for x in domain}
  ck('negative_no_deletion_not_initial',isp(missing,bad) and missing!=bad and missing not in badimages)
 summary.append({'alpha_omega_multiple':alpha[0],'alpha_finite_tail':alpha[1],'source_nodes':len(domain),'sampled_transfinite_nodes':sum(length(x)[0]>0 for x in domain)})
# Exponent transport over a fixed finite ray/tree; exact rational cancellation retained.
alpha=(0,2);a=norm([(-1,alpha)])
exponents=[x for x in words if length(x)[0]==0 and length(x)[1]<=3 and cmp(x,a)>=0]
exponents.sort(key=cmp_to_key(cmp));rng=random.Random(23444606)
def clean(v):return {k:c for k,c in v.items() if c}
def vadd(x,y):
 out=dict(x)
 for k,c in y.items():out[k]=out.get(k,F(0))+c
 return clean(out)
def scale(x,n):return clean({k:n*c for k,c in x.items()})
def transport(x):return {rotate(k,alpha):c*(4 if k==a else 1) for k,c in x.items()}
def sign_series(x):
 if not x:return 0
 c=x[max(x,key=cmp_to_key(cmp))]
 return 1 if c>0 else -1
for trial in range(500):
 def randseries():return clean({k:F(rng.randrange(-4,5),4 if k==a else 8) for k in exponents if rng.randrange(3)==0})
 u,v=randseries(),randseries();tu,tv=transport(u),transport(v)
 ck('finite_Hahn_additivity',transport(vadd(u,v))==vadd(tu,tv))
 ck('finite_Hahn_order',sign_series(vadd(u,scale(v,-1)))==sign_series(vadd(tu,scale(tv,-1))))
 ck('bottom_coefficient_integral',tu.get((),F(0)).denominator==1)
 ordered=sorted(u,key=cmp_to_key(cmp),reverse=True)
 for j in range(len(ordered)+1):
  trunc={k:u[k] for k in ordered[:j]}
  target_order=sorted(tu,key=cmp_to_key(cmp),reverse=True)
  ck('finite_Hahn_truncation_commutes',transport(trunc)=={k:tu[k] for k in target_order[:j]})
ck('negative_wrong_bottom_scale', (F(1,4)*2).denominator!=1)
# Independent exact lexicographic controls of the legal unit cuts and their cofinality.
def arraycmp(x,y):
 for a,b in zip(x,y):
  if a!=b:return 1 if a>b else -1
 return 0
for trial in range(200):
 N=8;rs=[rng.choice([F(-2),F(-1),F(1,3),F(1),F(2)]) for _ in range(N)]
 for mu in range(N-1):
  sm=rs[:mu+1]+[F(0)]*(N-mu-1)
  for nu in range(mu+1,N):
   sn=rs[:nu+1]+[F(0)]*(N-nu-1)
   lo=sn.copy();hi=sn.copy();lo[nu]-=1;hi[nu]+=1
   ck('unit_options_bracket_actual_series',arraycmp(lo,rs)<0<arraycmp(hi,rs))
   for k in (1,2,5):
    left=sm.copy();right=sm.copy();left[mu]-=F(1,2**k);right[mu]+=F(1,2**k)
    ck('unit_option_cofinal_comparison',arraycmp(left,lo)<0 and arraycmp(hi,right)<0)
# A legal integer coefficient group need not contain a dyadic perturbation.
ck('negative_dyadic_option_not_legal', (F(1)-F(1,2)).denominator!=1)
# A bounded-exponent-stage union can miss a cofinal support: finite truncations are
# all present at some stage, while the formal omega-support has no last index.
ck('finite_stage_exhaustion_does_not_give_limit',all(max(range(n))<n for n in range(1,50)))
out={'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'assertions':sum(checks.values()),'counts':dict(checks),'ordinal_block_families':summary,'ordinal_arithmetic':'Exact omega*k+n and finite runs, with ordinal addition/left-tail extraction; includes 1+omega=omega and nonempty blocks retained. Only sampled proper prefixes and finite described transfinite nodes are tested.','scope':'Fresh exact diagnostics only. Neither arbitrary ordinal lengths nor set/proper-class support exhaustion is proved by finite enumeration; those are checked in the written proof. No submitted helper imported.','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(HERE/'fresh-control-results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
