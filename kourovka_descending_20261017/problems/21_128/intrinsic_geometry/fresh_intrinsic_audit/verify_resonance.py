#!/usr/bin/env python3
"""Independent exterior-basis rewrite audit, no producer imports.
Every pair belongs to one verified rank-two flat. Reduce e_i^e_j to
(e_anchor^e_j)-(e_anchor^e_i) in that flat, retaining integer coefficients.
"""
from pathlib import Path
from itertools import combinations, product
from collections import defaultdict
import json,hashlib
p=Path(__file__).resolve().parent.parent
cert=json.loads((p/'resonance_certificate.json').read_text())
arr=json.loads((p/'restriction_certificate.json').read_text())
repro=json.loads(Path(__file__).with_name('resonance_reproduction.json').read_text())
assert cert==repro
results=[]
for d,c in zip(arr,cert):
 N=len(d['hyperplanes']);fs=[tuple(f['members']) for f in d['rank2_flats']]
 owner={pair:s for s in fs for pair in combinations(s,2)}
 assert len(owner)==N*(N-1)//2
 def cup(a,b):
  assert len(a)==len(b)==N
  out=defaultdict(int)
  for i,j in combinations(range(N),2):
   k=a[i]*b[j]-a[j]*b[i]
   if not k:continue
   s=owner[i,j];anchor=s[0]
   out[s,j]+=k
   if i!=anchor:out[s,i]-=k
  return {k:v for k,v in out.items() if v}
 ss=c['local_subspaces'];assert c['dimensions']==[len(s)-1 for s in ss]
 assert len(ss)==3 and len({tuple(s) for s in ss})==3
 def difference(i,j):
  a=[0]*N;a[i]=1;a[j]=-1;return a
 for s in ss:
  assert tuple(s) in fs and len(s)>=3
  basis=[difference(s[0],i) for i in s[1:]]
  assert all(sum(a)==0 for a in basis)
  assert all(not cup(a,b) for a,b in product(basis,repeat=2))
 seen=set();nonzero=[]
 for w in c['cross_cup_witnesses']:
  i,j=w['subspace_pair'];assert 0<=i<j<3
  seen.add((i,j));a=w['left_vector'];b=w['right_vector']
  assert sum(a)==sum(b)==0
  assert all(v==0 or k in ss[i] for k,v in enumerate(a))
  assert all(v==0 or k in ss[j] for k,v in enumerate(b))
  u=cup(a,b);assert u
  v=w['nonzero_cup_coordinate'];s=tuple(v['flat']);assert s[0]==v['anchor']
  assert u[s,v['basis_mirror']]==v['coefficient']!=0
  nonzero.append(v['coefficient'])
 assert seen==set(combinations(range(3),2))
 results.append({'ambient_type':d['ambient_type'],'planes':N,'subspaces':ss,'dimensions':c['dimensions'],'all_local_basis_cups_zero':True,'cross_cup_witness_values':nonzero})
r={'status':'PASS','method':'independent exterior pair reduction with Orlik-Solomon circuit relations','results':results,'input_sha256':{n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in ['restriction_certificate.json','resonance_certificate.json']}}
Path(__file__).with_name('resonance_verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
