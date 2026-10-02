#!/usr/bin/env python3
from pathlib import Path
from itertools import product
from random import Random
import json
from anchor_solver import optimize_anchors,direct_cost,label_from_certificate

checks=0

def check(v,label):
 global checks
 checks+=1
 if not v:raise AssertionError(label)

def valid(L,d,f):
 return f is not None and len(f)==len(L) and all(f[i] in L[i] for i in range(len(L))) and all(abs(f[i]-f[j])>=d for i in range(len(L)) for j in range(i+1,min(i+3,len(L))))

# Independent direct cost, without unary/edge decomposition.
def raw_cost(L,d,I,values):
 out=0
 for j,A in enumerate(L):
  if j in I:continue
  kept=0
  for x in A:
   if all(abs(i-j)>2 or abs(x-c)>=d for i,c in zip(I,values)):kept+=1
  out+=max(0,2*d-kept)
 return out

rng=Random(300004174);small=0;certified=0
for n in range(3,9):
 for d in range(1,4):
  for k in range(1,5):
   for trial in range(12):
    L=[sorted(rng.sample(range(1,13),k)) for _ in range(n)]
    for r in range(3):
     I=list(range(r,n,3));result=optimize_anchors(L,d,r)
     exact=min(raw_cost(L,d,I,values) for values in product(*(L[i] for i in I)))
     check(result['cost']==exact,'exhaustive anchor optimum')
     check(direct_cost(L,d,result['anchors'])==exact,'backtracked optimizer')
     if exact<2*d:
      check(valid(L,d,label_from_certificate(L,d,result)),'sufficient witness')
      certified+=1
     small+=1
# Arbitrary large palettes, nonconsecutive lists, distinct locally minimal anchors.
local=0
for n in range(3,31):
 for d in range(1,8):
  k=3*d*(n-1)//n+1
  sizes=[len(range(r,n,3)) for r in range(3)];r=sizes.index(max(sizes));I=list(range(r,n,3))
  L=[None]*n
  for t,i in enumerate(I):L[i]=[1000*(t+1)+2*j for j in range(k)]
  for j in range(n):
   if j not in I:
    high=max(min(L[i]) for i in I if abs(i-j)<=2)
    L[j]=[high+50*d+3*x for x in range(k)]
  check(all(min(L[i])<=min(L[j]) for i in I for j in range(n) if j not in I and abs(i-j)<=2),'local minimum hypothesis')
  result=optimize_anchors(L,d,r)
  check(result['cost']<2*d,'local minimum budget')
  check(valid(L,d,label_from_certificate(L,d,result)),'local minimum labeling')
  top=max(max(A) for A in L)+100
  reflected=[[top-x for x in A] for A in L];res=optimize_anchors(reflected,d,r)
  check(res['cost']<2*d and valid(reflected,d,label_from_certificate(reflected,d,res)),'local maximum reflection')
  local+=2
# Frozen method-failure certificate, audited by independent stage-cost accounting.
cert=json.loads((Path(__file__).resolve().parent/'TURN_4_CERTIFICATE.json').read_text());L=cert['lists'];d=cert['d'];n=len(L)
check(n==42 and all(len(set(A))==6 for A in L),'certificate list shape')
check(valid(L,d,cert['explicit_valid_labeling']),'explicit feasible original instance')
check(3*d*(n-1)//n+1==6,'source cardinality')
for record in cert['optimum_by_residue']:
 r=record['residue'];I=list(range(r,n,3));tables=record['layers'];previous=None
 for h,i in enumerate(I):
  # These vertices have their rightmost anchor neighbor exactly i_h.
  finished=[]
  for j in range(n):
   if j in I:continue
   neigh=[t for t,a in enumerate(I) if abs(a-j)<=2]
   if max(neigh)==h:finished.append((j,neigh))
  current={}
  for b in L[i]:
   candidates=[(0,None)] if h==0 else [(score,a) for a,score in previous.items()]
   values=[]
   for score,a in candidates:
    extra=0
    for j,neigh in finished:
     chosen=[b] if len(neigh)==1 else [a,b]
     kept=sum(all(abs(x-y)>=d for y in chosen) for x in L[j])
     extra+=max(0,2*d-kept)
    values.append((score+extra,a))
   current[b]=min(values)[0]
  given={a:score for a,score,prev in tables[h]}
  check(given==current,'independent Bellman layer')
  previous=current
 check(min(previous.values())==record['cost']==4,'all anchor choices fail strict threshold')
 check(raw_cost(L,d,I,[c for _,c in record['anchors']])==4,'optimizer realizes reported cost')
 check(label_from_certificate(L,d,record) is None,'method correctly declines certification')
print(json.dumps(dict(problem_id=30000417,turn=4,status='all controls passed',assertions=checks,small_exhaustive_anchor_instances=small,certified_small_witnesses=certified,local_extremum_instances=local,method_failure_n=42,method_failure_optima=[4,4,4],scope='Variable-anchor sufficient theorem and exact method-incompleteness certificate; original conjecture unresolved.',dependencies='Python 3 standard library'),indent=2))
