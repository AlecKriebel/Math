#!/usr/bin/env python3
"""Independent compatibility-graph clique enumeration, without canonical families."""
from itertools import combinations
from fractions import Fraction as Q
import json

n=9;T=frozenset(range(4));U=T;A=set(range(n))
triples=[frozenset(s) for s in combinations(A,3) if not frozenset(s)<=T]
adj={i:{j for j in range(len(triples)) if j!=i and len(triples[i]|triples[j])<=4} for i in range(len(triples))}
maximal=[]
def bron(R,P,X):
 if not P and not X:maximal.append(tuple(sorted(R)));return
 pivot=max(P|X,key=lambda i:len(adj[i]&P)) if P|X else None
 for v in list(P-(adj[pivot] if pivot is not None else set())):
  bron(R|{v},P&adj[v],X&adj[v]);P.remove(v);X.add(v)
bron(set(),set(range(len(triples))),set())
families={()}
for clique in maximal:
 for size in range(1,len(clique)+1):families.update(combinations(clique,size))
counts={'eligible_triples':len(triples),'maximal_compatibility_cliques':len(maximal),'all_compatible_subfamilies':len(families),'independent_classification_checks':0,'exact_charge_neighborhood_checks':0,'exceptional_disjoint_fourset_cases':0}
for fam in sorted(families,key=lambda x:(len(x),x)):
 F=[triples[i] for i in fam]
 I=set.intersection(*map(set,F)) if F else set()
 D=set.union(*map(set,F)) if F else set()
 assert not F or len(I)>=2 or len(D)==4
 counts['independent_classification_checks']+=1
 # Compute a dual certificate directly on all permitted neighborhoods.
 if not F:charge={v:Q(1,4) if v in U else Q(1,2) for v in A}
 elif len(I)>=2:
  P=set(sorted(I)[:2]);charge={v:Q(1,4) if v in U|P else Q(1,2) for v in A}
 else:
  charge={v:Q(1,4) if v in U else Q(1,3) if v in D else Q(1,2) for v in A}
  if sum(charge.values())<3:
   assert len(U)==4 and not U&D and len(A-U-D)==1
   counts['exceptional_disjoint_fourset_cases']+=1
   w=next(iter(A-U-D))
   if I:charge={v:Q(1,4) if v in U else Q(1) if v==w else Q(0) if v in I else Q(1,2) for v in A}
   else:charge={v:Q(1,4) if v in U else Q(1) if v==w else Q(1,3) for v in A}
 assert sum(charge.values())>=3
 permitted={frozenset()}
 for size in range(1,5):
  for v in combinations(A,size):
   S=frozenset(v)
   if S<=T or S in F or (len(S)<=2 and all(len(S|f)<=4 for f in F)):permitted.add(S)
 for S in permitted:
  assert sum(charge[v] for v in S)<=1,(fam,S,charge)
  counts['exact_charge_neighborhood_checks']+=1

# Explicit equal-vs-weighted cardinality obstruction to a forbidden reduction.
# A c reaches three positive types of weights 1/10 each in a five-type A part:
# mass 3/10<1/2, but three exceeds floor((5-1)/2)=2.
weighted_A=(Q(1,10),Q(1,10),Q(1,10),Q(7,20),Q(7,20))
assert sum(weighted_A)==1 and sum(weighted_A[:3])<Q(1,2)
assert 3>(len(weighted_A)-1)//2
print(json.dumps({'status':'PASS','counts':counts,'weighted_A_cardinality_obstruction':{'weights':list(map(str,weighted_A)),'reached_types':[0,1,2],'reached_mass':'3/10','uniform_rank_bound':2,'purpose':'Refutes weighted-mass-to-uniform-cardinality step, not the original conjecture.'},'scope':'All pairwise-compatible residual triple families on nine equally weighted first vertices with one specified four-type, via independent maximal-clique enumeration.'},indent=2))
