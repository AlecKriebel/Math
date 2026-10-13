"""Finite exact controls for KP-1.17 Turn 1; no geometric certificate or solution.
The group operations and graph Laplacian checks are independently explicit.
"""
from itertools import product,combinations,permutations
from collections import Counter
import json
C=Counter()
def ck(x,s):
 assert x,s
 C[s]+=1
def group_checks(elements,mul,e,label):
 inv={x:next(y for y in elements if mul(x,y)==e and mul(y,x)==e) for x in elements}
 invol=[x for x in elements if x!=e and mul(x,x)==e]
 conjugate={x:{mul(mul(g,x),inv[g]) for g in elements} for x in invol}
 for t in invol:
  commuting=[z for z in invol if mul(t,z)==mul(z,t)]
  if len(commuting)==1:ck(conjugate[t]==set(invol),'centralizer_unique_involution_implies_one_class')
  if conjugate[t]!=set(invol):
   ck(len(commuting)>1,'multiple_classes_force_commuting_partner')
   z=next(x for x in commuting if x!=t);v4={e,t,z,mul(t,z)}
   ck(len(v4)==4 and all(mul(x,x)==e for x in v4),'commuting_partner_klein_four')
  ck(t in conjugate[t] and conjugate[t]<=set(invol),'conjugation_preserves_involutions')
 return invol,conjugate
# Dihedral 2-groups D_(2m), represented by (rotation exponent, reflection bit).
for m in [2,4,8,16,32,64]:
 el=list(product(range(m),range(2)));mul=lambda x,y,m=m:((x[0]+(-1 if x[1] else 1)*y[0])%m,x[1]^y[1])
 invol,classes=group_checks(el,mul,(0,0),'dihedral')
 for a,b in product(range(m),repeat=2):
  x,y=(a,1),(b,1)
  ck((mul(x,y)==mul(y,x))==((2*(a-b))%m==0),'dihedral_reflection_commutation_formula')
  ck((y in classes[x])==((a-b)%2==0),'dihedral_reflection_conjugacy_parity')
  if m>=4 and (a-b)%2:ck(mul(x,y)!=mul(y,x),'distinct_reflection_classes_need_not_commute')
# Cyclic and generalized quaternion Sylow examples.
for m in [2,4,8,16,32]:
 el=list(range(m));iv,_=group_checks(el,lambda x,y,m=m:(x+y)%m,0,'cyclic');ck(iv==[m//2],'cyclic_unique_involution')
for n in [2,4,8,16,32]:
 el=list(product(range(2*n),range(2)))
 mul=lambda x,y,n=n:((x[0]+(-1 if x[1] else 1)*y[0]+n*x[1]*y[1])%(2*n),x[1]^y[1])
 iv,_=group_checks(el,mul,(0,0),'quaternion');ck(iv==[(n,0)],'quaternion_unique_involution')
 for a in range(2*n):ck(mul((a,1),(a,1))==(n,0),'quaternion_outside_squares')
# Non-2-groups: symmetric and alternating groups through degree five.
for n in range(2,6):
 allp=list(permutations(range(n)));e=tuple(range(n));mul=lambda x,y:tuple(x[y[j]] for j in range(len(x)))
 for even_only in [False,True]:
  el=[x for x in allp if not even_only or sum(x[i]>x[j] for i in range(n) for j in range(i+1,n))%2==0]
  group_checks(el,mul,e,'permutation')
# Exact matrix-tree controls on small loopless multigraphs.
def connected(n,edges):
 seen={0}
 while True:
  nxt=seen|{v for u,v in edges if u in seen}|{u for u,v in edges if v in seen}
  if nxt==seen:return len(seen)==n
  seen=nxt
def determinant(A):
 A=[r[:] for r in A];n=len(A);sign=1;previous=1
 for k in range(n-1):
  if not A[k][k]:
   j=next((j for j in range(k+1,n) if A[j][k]),None)
   if j is None:return 0
   A[k],A[j]=A[j],A[k];sign=-sign
  pivot=A[k][k]
  for i in range(k+1,n):
   for j in range(k+1,n):
    numerator=A[i][j]*pivot-A[i][k]*A[k][j];ck(numerator%previous==0,'bareiss_exact_division');A[i][j]=numerator//previous
  for i in range(k+1,n):A[i][k]=0
  previous=pivot
 return sign*A[-1][-1] if n else 1
for n in range(2,6):
 pairs=list(combinations(range(n),2));values=range(3) if n<=4 else range(2)
 for mults in product(values,repeat=len(pairs)):
  edges=[e for e,m in zip(pairs,mults) for _ in range(m)]
  if not connected(n,edges):continue
  lap=[[0]*n for _ in range(n)]
  for u,v in edges:lap[u][u]+=1;lap[v][v]+=1;lap[u][v]-=1;lap[v][u]-=1
  tau=determinant([r[:-1] for r in lap[:-1]])
  enumerated=sum(connected(n,[edges[i] for i in ids]) for ids in combinations(range(len(edges)),n-1))
  ck(tau==enumerated,'matrix_tree_exact_count')
  no_bridges=all(connected(n,edges[:j]+edges[j+1:]) for j in range(len(edges)))
  if no_bridges:ck(tau>=2,'nonempty_reduced_tait_graph_not_unimodular')
  if tau==1:ck(len(edges)==n-1,'unique_tree_graph_is_tree')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(sorted(C.items())),'scope':'Finite group and graph controls only. Hyperbolic realization and actual quotient alternation require the analytic proof and cited classical inputs; original KP-1.17 remains unresolved.'},indent=2,sort_keys=True))
