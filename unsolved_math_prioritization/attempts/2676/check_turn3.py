"""Exact graph/ADE controls for the source-qualified Turn-3 reduction.
No claim to implement link recognition, geometrization or Floer homology.
"""
from itertools import combinations,product,permutations
from math import gcd
from functools import reduce
from collections import Counter
import sympy as s
import json
C=Counter()
def ck(x,label):
 assert x,label
 C[label]+=1
def connected(n,edges):
 seen={0}
 while True:
  new=seen|{v for u,v in edges if u in seen}|{u for u,v in edges if v in seen}
  if new==seen:return len(seen)==n
  seen=new
def lap(n,edges):
 A=s.zeros(n)
 for a,b in edges:A[a,a]+=1;A[b,b]+=1;A[a,b]-=1;A[b,a]-=1
 return A[:-1,:-1]
def canonical(n,edges):
 def encoding(p):
  ct=Counter(tuple(sorted((p[u],p[v]))) for u,v in edges)
  return tuple(ct[i,j] for i,j in combinations(range(n),2))
 return n,min(encoding(p) for p in permutations(range(n)))
classes={}
for n in range(2,5):
 pairs=list(combinations(range(n),2))
 for mult in product(range(5),repeat=len(pairs)):
  m=sum(mult)
  if not 2<=m<=4:continue
  edges=[e for e,k in zip(pairs,mult) for _ in range(k)]
  if not connected(n,edges) or any(not connected(n,edges[:j]+edges[j+1:]) for j in range(m)):continue
  tau=int(lap(n,edges).det())
  enum=sum(connected(n,[edges[i] for i in inds]) for inds in combinations(range(m),n-1))
  ck(tau==enum,'small_graph_matrix_tree_count')
  ck(tau>=m,'small_graph_edge_bound')
  if tau<=4:classes[canonical(n,edges)]=(n,m,tau,tuple(sorted(sum(v in e for e in edges) for v in range(n))))
ck(len(classes)==6,'six_small_tait_graphs')
expected={(2,2,2,(2,2)),(2,3,3,(3,3)),(2,4,4,(4,4)),(3,3,3,(2,2,2)),(4,4,4,(2,2,2,2)),(3,4,4,(2,2,4))}
ck(set(classes.values())==expected,'small_tait_graph_list_complete')
# Ear-tree lower-bound algebra and block-product bound.
for trees,ell in product(range(2,61),range(1,31)):
 ck(ell*trees+1>=trees+ell,'ear_count_increment_bound')
for k in range(2,6):
 for edges in product(range(2,8),repeat=k):
  prod=1
  for e in edges:prod*=e
  ck(prod>=sum(edges),'block_product_bounds_edge_sum')
# Cartan matrices as stars with specified arm lengths.
def star(arms):
 n=1+sum(arms);A=2*s.eye(n);nextv=1
 for length in arms:
  previous=0
  for _ in range(length):
   A[previous,nextv]=A[nextv,previous]=-1;previous=nextv;nextv+=1
 return A
for n in range(4,31):
 A=star([n-3,1,1]);ck(A.det()==4,'D_cartan_determinant_all_parities')
 # Direct pretzel reduced Goeritz matrix [[a+b,-b],[-b,b+c]].
 G=s.Matrix([[0,-2],[-2,n]])
 ck(abs(G.det())==4,'D_pretzel_goeritz_determinant')
for n,arms,want in [(6,[2,2,1],3),(7,[3,2,1],2),(8,[4,2,1],1)]:
 ck(star(arms).det()==want,'E_cartan_determinant')
# Binary dihedral abelianization, calculated from relation minors.
for r in range(2,101):
 relations=[(2*r,0),(-r,2),(2,0)]
 minors=[abs(a*d-b*c) for (a,b),(c,d) in combinations(relations,2)]
 order=reduce(gcd,minors)
 first=reduce(gcd,[abs(x) for row in relations for x in row])
 ck(order==4,'binary_dihedral_abelian_order_four')
 ck((first,order//first)==((1,4) if r%2 else (2,2)),'binary_dihedral_abelian_structure')
 mul=lambda x,y:((x[0]+(-1 if x[1] else 1)*y[0]+r*x[1]*y[1])%(2*r),x[1]^y[1])
 ck(mul((1,0),(0,1))!=mul((0,1),(1,0)),'binary_dihedral_noncommutative')
# Lens plumbing chain determinants.
for n in range(2,31):
 A=2*s.eye(n-1)
 for i in range(n-2):A[i,i+1]=A[i+1,i]=-1
 ck(A.det()==n,'cycle_lens_chain_determinant')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(sorted(C.items())),'small_tait_graphs':[{'vertices':n,'edges':m,'tree_count':t,'degree_sequence':list(d)} for n,m,t,d in sorted(set(classes.values()))],'scope':'Exact finite graph, Cartan and group-presentation controls only. The source-qualified topological reduction uses the written argument and cited theorems; original problem unresolved.'},indent=2,sort_keys=True))
