#!/usr/bin/env python3
"""Exact certificates for abstract laws and Kempe signature constraints.
No LP output or floating-point calculation is trusted by this verifier.
"""
from itertools import product,combinations
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
checks=0

def ck(x):
 global checks
 assert x;checks+=1
P=[(1,2,12),(1,4,10),(1,6,8),(1,14),(2,4,9),(2,5,8),(2,13),(3,4,8),(3,12),(4,11),(5,10),(6,9),(7,8),(15,)]
h=[44,35,35,44,35,26,44,44,44,44,44,35,44,44]
signature=dict(zip(P,h))
def partition(c):return tuple(sorted(sum(1<<i for i in range(4) if c[i]==v) for v in set(c)))
def up(n):
 if not n:return[0,1]
 a=up(n-1);return[x|(y<<(1<<(n-1))) for x in a for y in a if x&y==x]
U=up(4);ck(len(U)==168)
w0=[0]*16;w1=[0]*16
for c in product(range(3),repeat=4):
 p=partition(c);z=sum((c[i]==0)<<i for i in range(4));a=signature[p];b=198*a+135*(3-len(p));ck(a>0 and b>0)
 w0[z]+=a;w1[z]+=b
ck(sum(w0)==3240);ck(sum(w1)==648000)
records=[]
for label,w,Z,expected in [('base',w0,3240,F(-11,8100)),('strict',w1,648000,F(-593,500000))]:
 for i in range(4):ck(sum(w[s] for s in range(16) if s>>i&1)*3==Z)
 reg=[]
 for i in range(4):
  for e in U:
   a=sum(w[s] for s in range(16) if e>>s&1);b=sum(w[s] for s in range(16) if e>>s&1 and s>>i&1)
   gap=3*b-a;ck(gap>=0);reg.append(gap)
 mF=sum(w[s] for s in range(16) if s&3==3);mG=sum(w[s] for s in range(16) if s&12==12);mFG=w[15]
 covariance=F(mFG,Z)-F(mF,Z)*F(mG,Z);ck(covariance==expected)
 records.append({'law':label,'zero_mask_weights':w,'total':Z,'mass_F':mF,'mass_G':mG,'mass_FG':mFG,'P_F':str(F(mF,Z)),'P_G':str(F(mG,Z)),'P_FG':str(F(mFG,Z)),'covariance':str(covariance),'all_singleton_regression_numerators':reg})
coarsen=0
for fine in P:
 for coarse in P:
  if fine==coarse:continue
  if all(any(b&c==b for c in coarse) for b in fine):
   ck(signature[coarse]>=signature[fine])
   Hc=198*signature[coarse]+135*(3-len(coarse));Hf=198*signature[fine]+135*(3-len(fine));ck(Hc>Hf);coarsen+=1
ck(signature[(15,)]==signature[(1,14)])
ck(F(records[0]['mass_F'],3240)!=F(1,9))
# Verify the injection itself on complete coloring spaces, not just its count consequence.
nb=[25,14,22,6];edges=[(i,5+j) for j,N in enumerate(nb) for i in range(5) if N>>i&1];adj=[[] for _ in range(9)]
for a,b in edges:adj[a].append(b);adj[b].append(a)
col=[c for c in product(range(3),repeat=9) if all(c[a]!=c[b] for a,b in edges)]
def swap_components(f,T,c,d,phi):
 seen=set();out=list(f)
 for v in range(9):
  if v in seen or f[v] not in (c,d):continue
  comp={v};todo=[v];seen.add(v)
  while todo:
   x=todo.pop()
   for y in adj[x]:
    if y not in seen and f[y] in (c,d):seen.add(y);comp.add(y);todo.append(y)
  if any(phi[i]==d and t in comp for i,t in enumerate(T)):
   for x in comp:out[x]=d if f[x]==c else c
 return tuple(out)
for T in combinations(range(5),4):
 groups={}
 for f in col:groups.setdefault(tuple(f[t] for t in T),[]).append(f)
 mono=len(groups[(0,0,0,0)])
 for phi in product(range(3),repeat=4):
  count=len(groups.get(phi,[]));ck((count==mono)==(len(set(phi))==1));ck(count<=mono)
 for c,d in ((0,1),(0,2),(1,2)):
  for phi,inputs in groups.items():
   outputs=[];psi=tuple(c if x==d else x for x in phi)
   for f in inputs:
    g=swap_components(f,T,c,d,phi);outputs.append(g);ck(tuple(g[t] for t in T)==psi);ck(all(g[a]!=g[b] for a,b in edges))
    # Reverse using the original color-d terminal locations.
    back=swap_components(g,T,c,d,phi);ck(back==f)
   ck(len(set(outputs))==len(inputs))
# Equality characterization in a disconnected two-component example.
for phi in product(range(3),repeat=4):
 count=(3-len({phi[0],phi[1]}))*(3-len({phi[2],phi[3]}))
 ck((count==4)==(phi[0]==phi[1] and phi[2]==phi[3]))
certificate={'partition_masks':P,'base_per_color_word_weights':h,'base_total_color_word_weight':3240,'strict_per_color_word_weight_formula':'198*h(partition)+135*(3-number_of_blocks)','strict_total':648000,'laws':records,'strict_coarsening_comparisons':coarsen,'interpretation':'Abstract color-symmetric laws, not graph-coloring counterexamples. Base law is ruled out by the proved equality characterization; strict perturbation is not realized by this packet.'}
blob=(json.dumps(certificate,indent=2)+'\n').encode();(Path(__file__).parent/'TURN_5_ABSTRACT_CERTIFICATE.json').write_bytes(blob)
print(json.dumps({'status':'PASS','exact_assertions':checks,'all_81_color_words_positive_in_both_laws':True,'regression_constraints_per_law':672,'strict_coarsening_comparisons':coarsen,'base_covariance':'-11/8100','strict_covariance':'-593/500000','dreidel_colorings_for_injection_controls':len(col),'abstract_certificate_sha256':hashlib.sha256(blob).hexdigest(),'scope':'Exact auxiliary-law and Kempe-injection controls. Neither abstract law is claimed to be the target coloring marginal; no source counterexample is certified.'},indent=2))
