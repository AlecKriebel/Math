#!/usr/bin/env python3
from itertools import product,combinations
from pathlib import Path
import json,subprocess,sys
from surface_gluing import surface
ar=[(0,1),(0,2),(1,2),(1,3),(2,3)];I={(0,2),(0,3),(1,4),(2,4)}
checks=0
def ck(v):
 global checks
 assert v;checks+=1
def gentle(rel):
 for a,(s,t) in enumerate(ar):
  out=[b for b,(v,w) in enumerate(ar) if v==t];inc=[b for b,(v,w) in enumerate(ar) if w==s]
  for status in (True,False):
   if sum(((a,b) in rel)==status for b in out)>1:return False
   if sum(((b,a) in rel)==status for b in inc)>1:return False
 return True
def paths(rel):
 P=[(i,) for i in range(5)];front=P[:]
 while front:
  new=[q+(b,) for q in front for b in range(5) if ar[q[-1]][1]==ar[b][0] and (q[-1],b) not in rel]
  P+=new;front=new
 return P
ck(all(s<t for s,t in ar));ck(len(paths(I))+4==9)
allJ=[];pairs=sorted(I)
for mask in range(16):
 J={pairs[i] for i in range(4) if mask>>i&1}
 if gentle(J):allJ.append(J)
ck(len(allJ)==4)
cert=json.loads(subprocess.check_output([sys.executable,str(Path(__file__).with_name('ribbon_certificate.py'))]));rows=[]
for index,J in enumerate([{(0,2),(1,4)},{(0,2),(2,4)}]):
 ck(gentle(J));ck(len(paths(J))+4==11);ck(not any(J<K for K in allJ));ck(J<I)
 expected=(0,3) if index==0 else (1,1)
 for u,v in product((0,1),repeat=2):
  z=surface(4,ar,J,{0:u,3:v});ck((z['genus'],z['boundaries'])==expected);ck(z['Euler_characteristic']==-1);ck(z['white_punctures']==z['black_punctures']==0)
  rows.append({'cover':index,'completion_at_source_sink':[u,v],**z})
  zd=surface(4,ar,I-J,{0:u,3:v});ck((zd['genus'],zd['boundaries'])==expected)
 r=cert['covers'][index];ck((r['genus'],r['boundary_components'])==expected);ck(r['Euler_characteristic']==-1)
 # Reconstruct boundary permutation from the stored independent ribbon arrays.
 phi=[r['sigma'][r['alpha'][i]] for i in range(8)];ck(phi==r['boundary_permutation']);ck(sorted(x for c in r['boundary_cycles'] for x in c)==list(range(8)))
 for cyc in r['boundary_cycles']:
  ck(all(phi[a]==b for a,b in zip(cyc,cyc[1:]+cyc[:1])))
print(json.dumps({'status':'PASS','exact_assertions':checks,'acyclic_quiver':ar,'all_saturated_gentle_ideals':[sorted(j) for j in allJ],'surface_gluings':rows,'independent_ribbon_certificate':'ribbon_certificate.json','scope':'Exact finite algebras and two surface reconstructions. This does not identify the undefined OWR tile-rotation equivalence.'},indent=2,sort_keys=True))
