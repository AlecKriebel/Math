"""Exact independent degree/sign controls; does not reprove ruling theory."""
from pathlib import Path
from itertools import combinations,product
from collections import defaultdict,Counter
import hashlib,json
C=Counter()
def ck(k,b):assert b,k;C[k]+=1
def add(P,Q):
 R=defaultdict(int,P)
 for e,c in Q.items():R[e]+=c
 return {e:c for e,c in R.items() if c}
def shift(P,a,z,c=1):return {(i+a,j+z):c*v for (i,j),v in P.items()}
def mul(P,Q):
 R={}
 for (a,z),c in P.items():R=add(R,shift(Q,a,z,c))
 return R
def degrees(P):return min(a for a,z in P),max(a for a,z in P)
# Actual two-strand HOMFLY skein recurrence in the source convention.
H=[{(-1,-1):1,(1,-1):-1},{(0,0):1}]
for n in range(2,11):H.append(add(shift(H[n-2],2,0),shift(H[n-1],1,1)))
ck('positive_trefoil_normalization',H[3]=={(2,0):2,(4,0):-1,(2,2):1})
ck('unknot_degrees',degrees(H[1])==(0,0))
ck('two_component_unlink',degrees(H[0])==(-1,1))
for n in range(1,11):
 ck('positive_two_braid_signature',degrees(H[n])[0]<=n-1)
 mirror={(-a,z):c*(-1 if z%2 else 1) for (a,z),c in H[n].items()}
 ck('mirror_degree_inversion',degrees(mirror)[0]==-degrees(H[n])[1])
 ck('negative_two_braid_signature',degrees(mirror)[0]<=-(n-1))
# Arbitrary independent split factors, including crossing-free unknots.
dH=H[0];dF={(-1,-1):1,(1,-1):1,(0,0):-1}
for ns in product(range(1,5),repeat=3):
 P={(0,0):1}
 for n in ns:P=mul(P,H[n])
 for q in range(1,5):
  L=P;Fpoly=P
  for _ in range(q-1):L=mul(L,dH);Fpoly=mul(Fpoly,dF)
  ck('split_minimum_additivity',degrees(L)[0]==sum(degrees(H[n])[0] for n in ns)-(q-1))
  ck('split_maximum_additivity',degrees(Fpoly)[1]==degrees(P)[1]+q-1)
# Three genuinely joined graph blocks: two triangles and a parallel-edge block.
blocks=[[(0,1),(1,2),(2,0)],[(2,3),(3,4),(4,2)],[(4,5),(4,5)]]
edges=[(u,v,b) for b,block in enumerate(blocks) for u,v in block]
for signs in product((-1,1),repeat=3):
 A=sum(signs[b]*(len(block)-len(set(v for e in block for v in e))+1) for b,block in enumerate(blocks))
 w=sum(signs[b] for u,v,b in edges)
 ntree=0
 for inds in combinations(range(len(edges)),5):
  par=list(range(6))
  def root(x):
   while par[x]!=x:x=par[x]
   return x
  cycle=False
  for i in inds:
   u,v,b=edges[i];u,v=root(u),root(v)
   if u==v:cycle=True;break
   par[u]=v
  if cycle or len({root(x) for x in range(6)})!=1:continue
  ntree+=1
  ck('actual_spanning_tree_signed_rank',w-sum(signs[edges[i][2]] for i in inds)==A)
 ck('spanning_tree_count',ntree==18)
# A sharp Kauffman bound on one representative, not two unrelated bounds.
for maxF,maxP,tb in product(range(-4,5),repeat=3):
 if tb==-maxF-1 and tb<-maxP:
  ck('sharp_bound_implication',maxP<=maxF and -maxF<=-maxP)
# Contrast control: arbitrary common upper bounds cannot order themselves.
ck('common_upper_bound_not_enough',0<=2 and 0<=1 and not 2<=1)
root=Path(__file__).resolve().parent
r={'status':'PASS','exact_assertions':sum(C.values()),'checks':dict(C),'artifact_sha256':hashlib.sha256((root/'author_replay/KNOWN_RESULT.md').read_bytes()).hexdigest(),'scope':'Independent Laurent/split calculations, exact two-strand skein normalization controls, signed spanning-tree identities, and the sharp-bound logic. No reproof of the imported contact-geometric theorems.'}
(root/'independent_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
