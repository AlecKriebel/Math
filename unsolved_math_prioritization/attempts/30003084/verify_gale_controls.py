"""Exact finite controls for TURN_2 and TURN_3; not a proof by enumeration."""
from itertools import combinations,product
from collections import Counter
import sympy as S
import json
C=Counter()
def ck(b,k):
 assert b,k
 C[k]+=1
def mat(cols):return S.Matrix.hstack(*cols)
def circuit5(cols,label):
 M=mat(cols);ck(M.rank()==4,label+'_rank4')
 for j in range(5):ck(M[:,[i for i in range(5) if i!=j]].det()!=0,label+'_four_minor')
e=[S.eye(4)[:,i] for i in range(4)];a=e[0]+e[1]+e[2]
for t in [-3,-1,1,2,4]:
 for u in [-3,-1,1,2,4]:
  q=e[0]+e[1]+t*e[3];qp=e[0]+e[2]+u*e[3]
  if u!=t:
   M=mat([q,qp,e[0],e[1],e[2]])
   ck(M*S.Matrix([u,-t,t-u,-u,t])==S.zeros(4,1),'mixed_pair_relation')
   circuit5([q,qp,e[0],e[1],e[2]],'mixed_pair_circuit')
  else:
   M=mat([a,q,qp,e[0],e[3]])
   ck(M*S.Matrix([1,-1,-1,1,2*t])==S.zeros(4,1),'equal_pair_relation')
   circuit5([a,q,qp,e[0],e[3]],'equal_pair_circuit')
# Weighted three-edge path: every four of the five columns are independent.
for weights in product([-2,1,3],repeat=3):
 cols=[e[0]+weights[0]*e[1],e[1]+weights[1]*e[2],e[2]+weights[2]*e[3],e[0],e[3]]
 circuit5(cols,'weighted_path_circuit')
# All graphs on four vertices validate connected/no-three-path => star.
edges=list(combinations(range(4),2))
from itertools import permutations
for bits in product([0,1],repeat=6):
 E={edges[j] for j,b in enumerate(bits) if b};reach={0}
 while True:
  nxt=reach|{v for u,v in E if u in reach}|{u for u,v in E if v in reach}
  if nxt==reach:break
  reach=nxt
 if len(reach)<4:continue
 path=any(all(tuple(sorted((p[i],p[i+1]))) in E for i in range(3)) for p in permutations(range(4)))
 if not path:ck(len(E)==3 and any(sum(v in edge for edge in E)==3 for v in range(4)),'graph_star_classification')
# Three concurrent line groups, with a central column and a zero column retained.
u=e[0]+e[1];vs=[e[0],e[2],e[3]];groups=[[v,u+v,u+2*v,u+3*v] for v in vs]
cols=sum(groups,[])+[u,S.zeros(4,1)]
for i in range(3):
 others=[u]+[vs[j] for j in range(3) if j!=i]
 ell=mat(others).T.nullspace()[0]
 vals=[(ell.T*c)[0] for c in cols]
 ck({j for j,v in enumerate(vals) if v!=0}==set(range(4*i,4*i+4)),'branch_relation_exact_support')
# Exact quadratic evaluations and Gale rank formula on several rational sets.
points=[(0,0,1),(1,0,1),(0,1,1),(1,1,1),(2,0,1),(0,2,1),(2,3,1),(3,2,1),(4,5,1),(5,3,1)]
def ev(p):
 x,y,z=p;return S.Matrix([x*x,y*y,z*z,x*y,x*z,y*z])
for n in [6,7,8,9,10]:
 V=mat([ev(p) for p in points[:n]]);ck(V.rank()==6,'full_quadratic_rank')
 if n==6:continue
 G=S.Matrix.vstack(*[v.T for v in V.nullspace()])
 for k in range(1,4):
  for subset in combinations(range(n),k):
   rest=[j for j in range(n) if j not in subset]
   ck(G[:,list(subset)].rank()==k-6+V[:,rest].rank(),'Gale_rank_identity')
# All four-point rank3 tests in this fixed sample really are collinear.
for ids in combinations(range(len(points)),4):
 M=mat([ev(points[j]) for j in ids]);P=mat([S.Matrix(points[j]) for j in ids])
 ck((M.rank()==3)==(P.rank()==2),'four_point_quadratic_dependence')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),'sympy_version':S.__version__,'scope':'Finite circuit, graph, branch-support, interpolation and Gale-rank controls. Universal small-cardinality theorems are proved analytically in TURN_2.md and TURN_3.md.'},indent=2,sort_keys=True))
