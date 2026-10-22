#!/usr/bin/env python3
"""Independent rational Q(a), a^2=a+1, incidence and map controls.
No author imports, SymPy, group quotient, or E-infinity computation.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations,permutations
from collections import Counter
from pathlib import Path
import json,hashlib
@dataclass(frozen=True)
class Q:
 r:F=F(0)
 s:F=F(0)
 def __add__(x,y):
  y=cv(y);return Q(x.r+y.r,x.s+y.s)
 __radd__=__add__
 def __neg__(x):return Q(-x.r,-x.s)
 def __sub__(x,y):return x+-cv(y)
 def __rsub__(x,y):return cv(y)+-x
 def __mul__(x,y):
  y=cv(y);return Q(x.r*y.r+x.s*y.s,x.r*y.s+x.s*y.r+x.s*y.s)
 __rmul__=__mul__
 def inv(x):
  n=x.r*x.r+x.r*x.s-x.s*x.s;assert n
  return Q((x.r+x.s)/n,-x.s/n)
 def __truediv__(x,y):return x*cv(y).inv()
 def conj(x):return Q(x.r+x.s,-x.s)
def cv(x):return x if isinstance(x,Q) else Q(F(x),F(0))
def vec(*v):return tuple(cv(x) for x in v)
Z=cv(0);O=cv(1);a=Q(F(0),F(1));ap=1-a
checks=Counter()
def req(v,k):assert v,k;checks[k]+=1
def dot(u,v):return sum((x*y for x,y in zip(u,v)),Z)
def cross(u,v):return (u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
def norm(v):
 q=next(x for x in v if x!=Z);return tuple(x/q for x in v)
def mul(M,v):return tuple(dot(row,v) for row in M)
def transpose(M):return tuple(zip(*M))
V=[vec(0,0,1),vec(1,0,1),vec(a,1,1),vec(1,a,1),vec(0,1,1)]
endpoints=[(0,1),(2,4),(0,2),(3,4),(0,3),(1,2),(0,4),(1,3)]
L=[norm(cross(V[i],V[j])) for i,j in endpoints]+[vec(0,0,1)]
req(a*a==a+1 and a*ap==cv(-1),'field_identity')
for q in (a,ap,1+a,2-a,3+2*a):req(cv(q)*cv(q).inv()==O,'field_inverse')
for i,j in combinations(range(5),2):
 d=tuple(V[i][k]-V[j][k] for k in (0,1))
 length=d[0]*d[0]+d[1]*d[1]+(1-a)*d[0]*d[1]
 req(length==(O if abs(i-j) in (1,4) else a*a),'regular_pentagon_metric')
req(1-((1-a)/2)*((1-a)/2)==(2+a)/4,'positive_metric_determinant_formula')
flats={}
for i,j in combinations(range(9),2):
 P=norm(cross(L[i],L[j]));S=tuple(k for k in range(9) if dot(L[k],P)==Z)
 flats[P]=S
 req(i in S and j in S,'pair_incidence')
sets={frozenset(S) for S in flats.values()}
req(Counter(map(len,sets))=={2:6,3:8,4:1},'intersection_multiplicities')
req(sum(len(S)*(len(S)-1)//2 for S in sets)==36,'projective_pair_partition')
req(sum(len(S)*(len(S)-1)//2 for S in sets if 8 not in S)+4==28,'affine_pair_partition')
sigma=(2,3,6,7,0,1,4,5,8);square=tuple(sigma[sigma[i]] for i in range(9))
for S in sets:req(frozenset(sigma[i] for i in S) in sets,'sigma_incidence')
req(tuple(square[square[i]] for i in range(9))==tuple(range(9)),'square_order_two')
req(square!=tuple(range(9)),'sigma_exact_order_four')
# All permutations compatible with the unique quadruple and line infinity;
# unlike the submitted checker, do not presuppose images of parallel partners.
quad=(0,2,4,6);other=(1,3,5,7);auts=[]
for p in permutations(quad):
 for q in permutations(other):
  h=dict(zip(quad,p));h.update(zip(other,q));h[8]=8
  good={frozenset(h[i] for i in S) for S in sets}==sets
  checks['complete_incidence_candidate_test']+=1
  if good:auts.append(tuple(h[i] for i in range(9)))
powers=[];p=tuple(range(9))
for k in range(4):powers.append(p);p=tuple(sigma[i] for i in p)
req(set(auts)==set(powers),'full_combinatorial_group_C4')
# Infinity is intrinsically distinguished by its four triple points.
triples=[sum(len(S)==3 and i in S for S in sets) for i in range(9)]
req([i for i,n in enumerate(triples) if n==4]==[8],'infinity_intrinsic')
R=(vec(0,1,0),vec(1,0,0),vec(0,0,1))
T=(vec(a,1,0),vec(1,a,0),vec(0,0,1))
Tp=tuple(tuple(x.conj() for x in row) for row in T)
for i in range(9):req(norm(mul(transpose(R),L[square[i]]))==L[i],'swap_line_pullback')
base=vec(2,2,1)
req(mul(R,base)==base,'based_involution')
for l in L[:8]:req(dot(l,base)!=Z,'basepoint_avoids_line')
sv=(0,2,4,1,3)
for i in (0,1,4):req(mul(T,V[i])==V[sv[i]],'forced_affine_images')
req(mul(T,V[2])!=V[sv[2]],'forced_affine_contradiction')
for i in range(5):req(mul(T,tuple(x.conj() for x in V[i]))==V[sv[i]],'cross_realization_map')
for v in V:req(mul(T,mul(Tp,v))==mul(R,v),'two_cross_maps_give_square')
# Parallel intersections are distinct and force infinity under sigma.
P=norm(cross(L[0],L[1]));Qp=norm(cross(L[2],L[3]));
req(P!=Qp and norm(cross(P,Qp))==L[8],'source_infinity_forcing')
P2=norm(cross(L[sigma[0]],L[sigma[1]]));Q2=norm(cross(L[sigma[2]],L[sigma[3]]))
req(P2!=Q2 and norm(cross(P2,Q2))==L[8],'target_infinity_forcing')
# Published Example 5.2 forms, independently matched after point substitution.
U=(vec(0,1,0),vec(-1,a-1,1),vec(0,0,1))
N=[vec(1,0,0),vec(1,-a,a),vec(0,1,-1),vec(1,1,-1),vec(1,0,-1),vec(1,-a,0),vec(0,1,0),vec(1,1,-a-1),vec(0,0,1)]
match=[]
for i,l in enumerate(L):
 hits=[j for j,f in enumerate(N) if norm(mul(transpose(U),f))==l]
 req(len(hits)==1,'unique_FS_line_identification');match.append(hits[0])
req(match==[0,4,3,7,2,6,1,5,8],'FS_ordering')
for i,j in combinations(range(5),2):
 for k,f in enumerate(N):
  on1=dot(f,mul(U,V[i]))==Z;on2=dot(f,mul(U,V[j]))==Z
  if on1 and on2:req(norm(cross(V[i],V[j]))==norm(mul(transpose(U),f)),'FS_vertex_substitution')

root=Path(__file__).resolve().parent
result=dict(status='PASS',exact_assertions=sum(checks.values()),checks=dict(sorted(checks.items())),
 affine_lines=8,projective_lines=9,combinatorial_automorphisms=len(auts),FS_line_ordering=match,
 scope='Exact Q(a) geometry and algebra only; no full sigma group lift or integral E-infinity obstruction computed.')
print(json.dumps(result,indent=2,sort_keys=True))
