#!/usr/bin/env python3
"""Exact finite proof checks; no network; Python -O has identical behavior."""
from itertools import permutations,combinations
from collections import Counter
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent
B=((1,3,2,4),(1,5,3,4,2),(2,5,3,4,1),(3,6,5,2,4,1),(4,6,5,2,3,1))
def need(b,msg):
 if not b:raise RuntimeError(msg)
def std(p):return tuple(sorted(p).index(x)+1 for x in p)
def positions(p,b):
 for ix in combinations(range(len(p)),len(b)):
  if std(tuple(p[i] for i in ix))==b:return tuple(i+1 for i in ix)
 return None
def avoid(p,b):return positions(p,b) is None
def literal(p):return avoid(p,B[0]) and any(avoid(p[:c],(1,3,2)) and avoid(p[c:],(2,3,1)) for c in range(len(p)+1))
def inv(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))
def boundary(p):return [i for i in range(1,len(p)) if max(p[:i])==i]
def T(p):
 i=boundary(p)[0];return p[:i]+(i+1,)+tuple(x+1 for x in p[i:])
cert=[]
for n in (5,6):
 for p in permutations(range(1,n+1)):
  if not(p[0]<p[2]<p[1] and p[-1]<p[-3]<p[-2]):continue
  matches=[(b,positions(p,b)) for b in B if not avoid(p,b)]
  need(bool(matches),('uncovered witness',p))
  b,ix=matches[0];cert.append({'witness':p,'forbidden_pattern':b,'positions':ix})
need(sum(len(c['witness'])==5 for c in cert)==4,'five witnesses')
need(sum(len(c['witness'])==6 for c in cert)==20,'six witnesses')
for b in B:
 need(not literal(b),('basis is member',b))
 for i in range(len(b)):need(literal(std(b[:i]+b[i+1:])),('not minimal',b,i))
archived=json.loads((ROOT/'counts_extended.json').read_text())
comparisons=0;exhaustive=[];Tchecks=0
for n in range(8):
 counts=Counter()
 for p in permutations(range(1,n+1)):
  x=literal(p);y=all(avoid(p,b) for b in B)
  need(x==y,('basis mismatch',p))
  if x:
   counts[inv(p)]+=1
   if boundary(p):
    q=T(p);need(literal(q) and inv(q)==inv(p),('T failure',p,q));Tchecks+=1
  comparisons+=1
 expected=[counts[k] for k in range(n*(n-1)//2+1)]
 need(expected==archived[n]['counts'],('count mismatch',n))
 exhaustive.append({'n':n,'total':sum(counts.values())})
for n,row in enumerate(archived):
 need(row['n']==n and sum(row['counts'])==row['total'],('row malformed',n))
 if n:
  old=archived[n-1]['counts'];new=row['counts']
  need(all(new[k]>=v for k,v in enumerate(old)),('monotonicity fails',n))
  for k,v in enumerate(old):
   if n-1>=k+2:need(new[k]==v,('stabilization fails',n,k))
p=(2,4,1,3);need(literal(p) and not boundary(p),'insertion witness input')
need(not literal(p+(5,)) and not literal((1,)+tuple(x+1 for x in p)),'endpoint witness')
p=(4,7,2,3,5,1,6);q=(4,2,8,3,5,1,6,7)
need(literal(p) and not literal(q) and inv(p)==inv(q)==11 and avoid(q,B[0]),'f witness')
need(positions(q,(2,5,3,4,1))==(2,3,4,5,6),'f witness positions')
family_checks=[]
for n in range(7,21):
 p=(4,n,2,3,5,1)+tuple(range(6,n))
 q=(4,2,n+1,3,5,1)+tuple(range(6,n+1))
 need(literal(p) and not literal(q) and avoid(q,B[0]),('family membership',n))
 need(inv(p)==inv(q)==n+4,('family inversions',n))
 for v in (p[0],1,p[-1]):need(not boundary(std(tuple(x for x in p if x!=v))),('family priority',n,v))
 r=std(tuple(x for x in p if x!=n));need(bool(boundary(r)),('family F4 decomposability',n))
 r=T(r);i=p.index(n)+1;got=r[:i]+(n+1,)+r[i:]
 need(got==q,('family F4 map',n))
 family_checks.append({'n':n,'k':n+4,'within_half_range':n+4<=2*n-7})
(ROOT/'basis_certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
result={'status':'PASS_PARTIAL_ONLY','basis_witnesses':len(cert),'basis_comparisons':comparisons,'direct_exhaustive_counts':exhaustive,'decomposable_injection_checks':Tchecks,'max_enumerated_length':archived[-1]['n'],'last_total':archived[-1]['total'],'checked_adjacent_transitions':len(archived)-1,'count_file_sha256':hashlib.sha256((ROOT/'counts_extended.json').read_bytes()).hexdigest(),'map_obstruction_family_checks':family_checks,'full_conjecture':'UNRESOLVED'}
(ROOT/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,sort_keys=True))
