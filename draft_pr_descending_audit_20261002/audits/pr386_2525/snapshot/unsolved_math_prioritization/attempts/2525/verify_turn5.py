from finite_groups import *
from itertools import product
import json
checks=0;cats={};rows=[]
def ck(x,k):
 global checks
 assert x,k;checks+=1;cats[k]=cats.get(k,0)+1
for ns in [(2,3),(2,3,4),(3,3,3),(2,2,2,2)]:
 es=list(product(*(range(n) for n in ns)));ix={x:i for i,x in enumerate(es)};M=[[ix[tuple((a+b)%n for a,b,n in zip(x,y,ns))] for y in es] for x in es]
 choices=[]
 for n in ns:
  _,H=cyclic(n);choices.append([(tuple([0]+S),lengths(H,S)) for S in subsets(n) if len(lengths(H,S))==n])
 num=0
 for sets in product(*choices):
  S=[ix[x] for x in product(*(ss for ss,dd in sets))];l=lengths(M,S);num+=1
  ck(len(l)==len(es),'cartesian_generation')
  for j,g in enumerate(es):ck(l[j]==max(dd[a] for a,(ss,dd) in zip(g,sets)),'cartesian_max_formula')
 rows.append({'factor_orders':ns,'generating_rectangles':num})
for k in range(1,15):
 m=2**k
 # BFS on a cyclic successor without allocating a quadratic multiplication table.
 d={0:0};front=[0]
 for a in front:
  b=(a+1)%m
  if b not in d:d[b]=d[a]+1;front.append(b)
 for a in range(m):ck(d[a]==a,'cyclic_successor_exact_length')
 ck(d[m-1]==m-1,'two_adic_negative_one')
 if k>1:
  for a in range(m):ck(a%(m//2)<=d[a],'quotient_length_comparison')
for n in range(1,13):
 # Independent Cayley BFS for the coordinate basis of C2^n.
 d={0:0};front=[0]
 for a in front:
  for j in range(n):
   b=a^(1<<j)
   if b not in d:d[b]=d[a]+1;front.append(b)
 for mask in range(1<<n):ck(d[mask]==mask.bit_count(),'support_exact_word_length')
 ck(max(d.values())==n,'support_diameter')
print(json.dumps({'assertions':checks,'categories':cats,'products':rows,'scope':'Exact finite metric/projection controls; compact-category and analytic-set statements are proved or explicitly credited, not computationally inferred.'},indent=2,sort_keys=True))
