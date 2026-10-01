#!/usr/bin/env python3
"""Separately authored sparse-arithmetic controls; no author functions imported."""
from fractions import Fraction as F
from collections import Counter
from itertools import combinations_with_replacement
from math import gcd
from pathlib import Path
import random,heapq,json
C=Counter()
def ck(k,x):assert x,k;C[k]+=1
def sg(x):return (x>0)-(x<0)
def collect(terms):
 d={}
 for e,a in terms:d[e]=d.get(e,0)+a
 return sorted((e,a) for e,a in d.items() if a)
def exact(p,q,terms):return sum((a*F(p,q)**e for e,a in terms),F(0))
def zero(p,q,terms):
 ts=collect(terms)
 if not ts:return True
 carry=ts[0][1];height=sum(abs(a) for e,a in ts);prev=ts[0][0]
 for e,a in ts[1:]:
  d=e-prev
  if carry:
   if d>abs(carry).bit_length():return False
   div=p**d
   if carry%div:return False
   carry=carry//div*q**d
  carry+=a;prev=e
  ck('zero_carry_height',abs(carry)<=height)
 return carry==0
def constants(p,q):
 c=1
 while p**c<2*q**c:c+=1
 return c,(q-1).bit_length()
def cluster(p,q,terms):
 ts=list(reversed(collect(terms)))
 if not ts:return 0
 A=sum(abs(a) for e,a in ts);B=A.bit_length();c,Q=constants(p,q)
 v,a=ts[0];value=F(a);W=0
 for e,a in ts[1:]:
  if not value:value=F(a);W=0;v=e;continue
  gap=v-e
  if gap>=c*(B+Q*W+1):return sg(value)
  value=value*F(p,q)**gap+a;W+=gap;v=e
  ck('cluster_height_control',abs(value)<=A*F(p,q)**W)
 return sg(value)
def strip(p,q,terms):
 ts=collect(terms)
 if not ts:return []
 B=sum(abs(a) for e,a in ts).bit_length();blocks=[];cur=[]
 for e,a in ts:
  if cur and e-cur[-1][0]>B:blocks.append(cur);cur=[]
  cur.append((e,a))
 blocks.append(cur);out=[]
 for b in blocks:
  if not zero(p,q,b):out.extend(b)
 return out
def adaptive(p,q,terms):
 ts=strip(p,q,terms)
 if not ts:return 0,0
 E=ts[-1][0];A=sum(abs(a) for e,a in ts);B=A.bit_length();c,_=constants(p,q);P=1
 while True:
  D=c*(P+B+2);S=sum((a*F(q,p)**(E-e) for e,a in ts if E-e<D),F(0));err=A*F(q,p)**D
  ck('truncation_error_bound',err<F(1,2**(P+2)))
  if S>err:return 1,P
  if S<-err:return -1,P
  P*=2
  assert P<4096

def norm(p,q,terms):
 data={}
 for e,a in terms:
  assert a>=0
  if a:data[e]=data.get(e,0)+a
 A=sum(data.values());m=len(data);B=A.bit_length();heap=[-e for e in data];heapq.heapify(heap);queued=set(data);out={};steps=0
 while heap:
  e=-heapq.heappop(heap);queued.remove(e);a=data.pop(e);steps+=1
  ck('canonical_coefficient_height',a<=A)
  carry,digit=divmod(a,q)
  if digit:out[e]=digit
  if carry:
   j=e-1;data[j]=data.get(j,0)+p*carry
   if j not in queued:queued.add(j);heapq.heappush(heap,-j)
 c=1
 while 2*p**c>q**c:c+=1
 ck('sparse_canonical_step_bound',steps<=m*(c*(B+1)+1))
 ck('bounded_digits',all(0<a<q for a in out.values()))
 return sorted(out.items()),steps
rng=random.Random(3999)
bases=[(2,1),(3,1),(3,2),(4,3),(5,2),(5,3),(7,4),(8,5)]
for p,q in bases:
 for j in range(800):
  terms=[(rng.randrange(-4,13),rng.randrange(-10,11)) for _ in range(rng.randrange(0,7))]
  val=exact(p,q,terms)
  ck('zero_matches_rational_ground_truth',zero(p,q,terms)==(val==0))
  ck('FPT_sign_matches_ground_truth',cluster(p,q,terms)==sg(val))
  out,precision=adaptive(p,q,terms)
  ck('adaptive_sign_matches_ground_truth',out==sg(val))
  kept=strip(p,q,terms);ck('zero_deletion_value_identity',exact(p,q,kept)==val)
# Exact huge-binary-gap tests require no power with that gap.
H=1<<4096
for p,q in bases:
 for shift in [0,-H,H]:
  terms=[(shift,-p),(shift+1,q),(shift+H,-p),(shift+H+1,q)]
  ck('huge_gap_zero',zero(p,q,terms))
  ck('huge_gap_FPT_zero',cluster(p,q,terms)==0)
  ck('huge_gap_adaptive_zero',adaptive(p,q,terms)[0]==0)
  ck('huge_gap_nonzero',not zero(p,q,[(shift,1),(shift+H,1)]))
# Nonnegative canonical forms: direct values, idempotence, and equal-word consistency.
for q in range(2,10):
 for p in range(1,q):
  if gcd(p,q)!=1:continue
  seen={}
  for j in range(160):
   terms=[(rng.randrange(-5,10),rng.randrange(0,30)) for _ in range(rng.randrange(0,7))]
   out,steps=norm(p,q,terms);val=exact(p,q,terms)
   ck('canonical_preserves_exact_value',exact(p,q,out)==val)
   ck('canonical_idempotent',norm(p,q,out)[0]==out)
   if val in seen:ck('finite_word_uniqueness_controls',seen[val]==out)
   seen[val]=out
  if p>1:
   d=(q+p-1)//p;t=d*p-q
   ck('lexical_counterexample',1<=d<q and F(d*p,q)>1)
   ck('certificate_remainder_range',1<=t<p)
   for R in range(1,31):ck('integer_certificate_modular_obstruction',(t*pow(q,R-1,p))%p!=0)
# Huge binary coefficients and gaps: verify normalization by an independent zero test.
big_rows=[]
for p,q in [(1,2),(2,3),(4,5),(5,7)]:
 terms=[(H,1<<2048),(-H,1<<1024)]
 out,steps=norm(p,q,terms)
 diff=[(-e,a) for e,a in terms]+[(-e,-a) for e,a in out]
 ck('huge_canonical_value_by_zero_test',zero(q,p,diff))
 big_rows.append({'base':[p,q],'exponent_input_bitlength':H.bit_length(),'coefficient_input_bitlength':2049,'processed_positions':steps,'output_positions':len(out)})
# Rouché and positive-root constants, using independent rational identities.
for n in range(2,101):
 rad=F(1,1024*n)
 ck('rouche_disk_contained',F(3,4)+rad<F(7,8))
 ck('rouche_strict_linear_dominance',512*n*rad*rad==rad/2 and rad/2<F(4,3)*rad)
for r in range(1,1001):ck('uniform_derivative_bound',r*F(3,4)**(r-1)<=F(27,16))
for n in range(2,6):
 k=(n-1).bit_length();M=3*k*(3**n-1)//2;bound=F(11,27)*F(1,3)**M
 for rs in combinations_with_replacement(range(1,9),n):
  val=sum((F(2,3)**r for r in rs),F(0))-1
  ck('positive_parity_gap_control',val!=0 and abs(val)>=bound)
# Conservative implementation family: its recurrence, margin and adaptive precision.
for m in [3,4,6,10,30,80,200]:
 B=m.bit_length();W=[0]
 for j in range(1,m):W.append(3*W[-1]+2*B+1)
 E=W[-1];terms=[(E,1)]+[(E-W[j],-1) for j in range(1,m)]
 ck('conservative_exponential_width',2*E==(2*B+1)*(3**(m-1)-1))
 ck('positive_family_margin',m*F(2,3)**(2*B+1)<F(2,3))
 answer,P=adaptive(3,2,terms);ck('adaptive_family_precision_one',answer==1 and P==1)
result={'status':'PASS_EXACT','assertions':sum(C.values()),'categories':dict(C),'large_binary_cases':big_rows,'scope':'Independent rational tests of partial algorithms and estimates; no general polynomial sign theorem or hardness claim','author_functions_imported':False,'floating_point':False}
Path(__file__).with_name('INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
