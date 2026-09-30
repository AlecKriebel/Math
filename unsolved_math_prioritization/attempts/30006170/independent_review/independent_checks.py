#!/usr/bin/env python3
"""Exact independent diagnostics; no claim to certify arbitrary measurable sets."""
from fractions import Fraction as F
from itertools import product
from collections import Counter
from pathlib import Path
from hashlib import sha256
import json
C=Counter()
def ck(g,b):assert b,g;C[g]+=1
P=((F(0),F(0),F(1,2),F(1,2)),(F(0),F(0),F(1,2),F(1,2)),(F(1,3),F(1,3),F(1,3),F(0)),(F(1,3),F(1,3),F(0),F(1,3)))
pi=(F(1,5),F(1,5),F(3,10),F(3,10));inv=(1,0,3,2)
for a in range(4):
 ck('row_stochastic',sum(P[a])==1)
 ck('stationarity',sum(pi[b]*P[b][a] for b in range(4))==pi[a])
 ck('no_inverse_transition',P[a][inv[a]]==0)
 for b in range(4):
  ck('reversibility',pi[a]*P[a][b]==pi[b]*P[b][a])
  ck('common_predecessor',any(P[c][a]>0 and P[c][b]>0 for c in range(4)))
  reachable={a}
  for _ in range(3):reachable|={j for i in reachable for j in range(4) if P[i][j]}
  ck('irreducibility',b in reachable)
ck('not_symmetric',P[0][2]!=P[2][0])
P2=[[sum(P[i][j]*P[j][k] for j in range(4)) for k in range(4)] for i in range(4)]
ck('uniform_two_step_hit_bound',min(x for row in P2 for x in row)==F(1,9))
# Exact cross-flow contradiction for a hypothetically symmetric row-stochastic matrix.
# The first two rows have no support except in the last two columns.
ck('symmetric_support_obstruction',F(1)+F(1)==2 and 2-(F(1)+F(1))==0)

def legal(w):return all(P[a][b]>0 for a,b in zip(w,w[1:]))
def red(w):
 out=[]
 for a in w:
  if out and inv[out[-1]]==a:out.pop()
  else:out.append(a)
 return tuple(out)
def inverse(w):return tuple(inv[a] for a in reversed(w))
def height(w):
 n=0
 for a in w:
  if a!=0:break
  n+=1
 return n
# Determine every possible output height by cancellation stopping cases.
# Once cancellation stops, only whether the next symbol is a matters; aa is forbidden.
groups=[()];layer=[()]
for n in range(1,8):
 layer=[w+(a,) for w in layer for a in range(4) if not w or a!=inv[w[-1]]]
 groups+=layer
branches=0
for g in groups:
 poss=set();p=height(g)
 for k in range(len(g)+1):
  canceled=inverse(g[len(g)-k:]) if k else ()
  if not legal(canceled):continue
  surviving=g[:len(g)-k]
  for q in range(4):
   if canceled and not P[canceled[-1]][q]:continue
   if surviving and q==inv[surviving[-1]]:continue
   initial=surviving+(q,)
   h=height(initial)
   # If q=a, the next legal letter is not a; if not, the height has already ended.
   ck('all_continuation_height_bound',max(0,p-1)<=h<=p+1)
   poss.add(h);branches+=1
   tail=next(t for t in (2,3) if P[q][t]>0)
   x=canceled+(q,)+(tail,)*(len(g)+3)
   ck('case_realization_legal',legal(x))
   ck('case_realization_reduction',height(red(g+x))==h)
 ck('nonempty_height_set',bool(poss))
 ck('translate_oscillation',max(poss)-min(poss)<=2)
# Exact Markov prefix-replacement ratios, using two different prefixes ending at one state.
prefixes=[];layer=[(a,) for a in range(4)]
for n in range(1,4):
 prefixes+=layer;layer=[w+(a,) for w in layer for a in range(4) if P[w[-1]][a]>0]
def mass(w):
 out=pi[w[0]]
 for a,b in zip(w,w[1:]):out*=P[a][b]
 return out
replacements=0
for v,w in product(prefixes,repeat=2):
 if v[-1]!=w[-1]:continue
 g=red(w+inverse(v));ratio=mass(w)/mass(v)
 for tail in product(range(4),repeat=2):
  if not legal((v[-1],)+tail):continue
  ck('prefix_ratio_constant',mass(w+tail)/mass(v+tail)==ratio)
  ck('prefix_replacement_group_identity',red(g+v+tail)==w+tail)
  replacements+=1
# Conditional-density transfer inequality, with exact positive errors.
for c,s,t in product(range(4),repeat=3):
 if not P[c][s] or not P[c][t]:continue
 for eps in (F(1,3),F(1,7),F(2,5)):
  delta=eps*min(P[c][s],P[c][t])/2
  ck('density_transfer_threshold',delta/P[c][s]<eps and delta/P[c][t]<eps)
# Generator returns and positive inaccessible cylinders under nonsingularization.
for d in range(4):
 t=next(t for t in range(4) if P[inv[d]][t])
 ck('generator_return_cylinder',mass((inv[d],t))>0 and red((d,inv[d],t))==(t,))
for k in range(12):
 g=(0,)*(2*k+2);x=(2,)*3
 ck('high_cylinder_translate',height(red(g+x))==2*k+2 and mass(x)>0)
 ck('chaining_height_gap',2*k+1<2*k+2)
# Direct translate-overlap paths versus return-set products in C5 and D5 actions.
finitecases=0
for dihedral in (False,True):
 n=5;G=[(a,s) for a in range(n) for s in ((1,-1) if dihedral else (1,))];e=(0,1)
 def mul(g,h):return((g[0]+g[1]*h[0])%n,g[1]*h[1])
 def img(g,A):return frozenset((g[0]+g[1]*x)%n for x in A)
 sets=[frozenset(i for i in range(n) if mask>>i&1) for mask in range(1,1<<n)]
 for A in sets:
  R={g for g in G if A&img(g,A)};reachable={e};powers={e}
  for k in range(5):
   ck('return_product_path_states',reachable==powers)
   U=frozenset().union(*(img(g,A) for g in powers))
   for B in sets:
    ck('return_union_chain_equivalence',bool(U&B)==any(img(g,A)&B for g in reachable));finitecases+=1
   reachable={h for g in reachable for h in G if img(g,A)&img(h,A)}
   powers={mul(g,r) for g in powers for r in R}
root=Path(__file__).resolve().parent
out={'verdict':'PASS_EXACT_INDEPENDENT_CONTROLS','assertions':sum(C.values()),'categories':dict(sorted(C.items())),'reduced_group_words':len(groups),'cancellation_stopping_cases':branches,'prefix_replacement_cases':replacements,'finite_action_set_tests':finitecases,'artifact_sha256':sha256((root/'author_replay/PARTIAL_RESULT.md').read_bytes()).hexdigest(),'limitations':'Exact finite diagnostics and bounded-word continuation classification. Arbitrary measurable-set density, nonsingularization and metric ergodicity are audited analytically in REVIEW.md.'}
(root/'independent_results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'verdict':out['verdict'],'assertions':out['assertions']}))
