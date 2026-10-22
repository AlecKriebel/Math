#!/usr/bin/env python3
"""Exact constructive controls for SP boundary coloring and small cubic cores."""
from itertools import combinations,product,permutations
from collections import Counter
import json
CHECK=Counter()
def ck(v,k):
 assert v,k;CHECK[k]+=1

# An expression is E, or (S,left,right), or (P,left,right).
def flags(T):
 if T=='E':return True,False,True
 op,L,R=T;a,x,f=flags(L);b,y,g=flags(R)
 return (False,a and b,f and g) if op=='S' else (a or b,x or y,f and g and not(a and y) and not(b and x))

def construct(T,mode):
 # mode0: adjacent/disjoint; mode1: nonadjacent overlap1; mode2: nonadjacent overlap2.
 adj,two,tf=flags(T);assert tf and (adj if mode==0 else not adj)
 five={};three={};edges=[];nextv=2;sets=[frozenset(c) for c in combinations(range(1,6),2)]
 def put(d,v,x):
  if v in d:assert d[v]==x
  d[v]=x
 def rec5(T,s,t,A,C):
  nonlocal nextv
  put(five,s,A);put(five,t,C)
  adj,two,tf=flags(T);z=len(A&C)
  assert tf and ((z==0 and not two) or (z==1 and not adj))
  if T=='E':assert not(A&C);edges.append((s,t));return
  op,L,R=T
  if op=='P':rec5(L,s,t,A,C);rec5(R,s,t,A,C);return
  u=nextv;nextv+=1
  a=0 if flags(L)[0] else 1;b=0 if flags(R)[0] else 1
  B=next(B for B in sets if len(A&B)==a and len(B&C)==b)
  rec5(L,s,u,A,B);rec5(R,u,t,B,C)
 rec5(T,0,1,frozenset([1,2]),frozenset([3,4] if mode==0 else [1,3]));size=nextv;nextv=2
 def rec3(T,s,t,a,b):
  nonlocal nextv
  put(three,s,a);put(three,t,b)
  if a==b:assert not flags(T)[0]
  if T=='E':assert a!=b;return
  op,L,R=T
  if op=='P':rec3(L,s,t,a,b);rec3(R,s,t,a,b);return
  u=nextv;nextv+=1;c=next(c for c in [6,7,8] if c not in [a,b])
  rec3(L,s,u,a,c);rec3(R,u,t,c,b)
 rec3(T,0,1,6,6 if mode==2 else 7);assert size==nextv
 out={i:five[i]|{three[i]} for i in range(size)}
 return edges,out

def cubic_multigraphs(n):
 A=[[0]*n for _ in range(n)];rem=[3]*n
 def rec(i):
  if i==n:
   if all(x==0 for x in rem):yield tuple(tuple(r) for r in A)
   return
  if rem[i]<0:return
  js=list(range(i+1,n))
  for values in product(*(range(min(rem[j],rem[i])+1) for j in js)):
   if sum(values)!=rem[i]:continue
   old=rem[i];rem[i]=0
   for j,v in zip(js,values):A[i][j]=A[j][i]=v;rem[j]-=v
   yield from rec(i+1)
   for j,v in zip(js,values):A[i][j]=A[j][i]=0;rem[j]+=v
   rem[i]=old
 yield from rec(0)

def connected(A,omit=None):
 V=[i for i in range(len(A)) if i!=omit]
 if not V:return True
 seen={V[0]};todo=list(seen)
 while todo:
  u=todo.pop()
  for v in V:
   if A[u][v] and v not in seen:seen.add(v);todo.append(v)
 return len(seen)==len(V)
def block(A):return connected(A) and all(connected(A,i) for i in range(len(A)))
def reduction(A):
 n=len(A);a,b=next((i,j) for i in range(n) for j in range(i+1,n) if A[i][j]==2)
 x=next(j for j in range(n) if j!=b and A[a][j]);y=next(j for j in range(n) if j!=a and A[b][j]);assert x!=y
 V=[i for i in range(n) if i not in [a,b]];B=[[A[i][j] for j in V] for i in V];i=V.index(x);j=V.index(y);B[i][j]+=1;B[j][i]+=1
 return B

# Verify all seven local middle-set choices against arbitrary prescribed pairs.
sets=list(map(frozenset,combinations(range(1,6),2)))
for A,C in product(sets,repeat=2):
 z=len(A&C)
 if z not in [0,1]:continue
 for a,b in product([0,1],repeat=2):
  if z==0 and a==b==0:continue
  ck(any(len(A&B)==a and len(B&C)==b for B in sets),'five_palette_middle_choices')
# Exhaust all ordered binary SP expressions through five edge leaves.
EXP={1:['E']};expressions=0;valid=0;colorings=0
for m in range(2,6):EXP[m]=[(op,L,R) for i in range(1,m) for L in EXP[i] for R in EXP[m-i] for op in ['S','P']]
for m in range(1,6):
 for T in EXP[m]:
  expressions+=1;a,two,tf=flags(T)
  if not tf:continue
  valid+=1
  for mode in ([0] if a else [1,2]):
   E,C=construct(T,mode);colorings+=1
   ck(all(len(S)==3 and S<=set(range(1,9)) for S in C.values()),'network_vertex_palette')
   ck(all(C[u].isdisjoint(C[v]) for u,v in E),'network_edge_disjointness')
   ck(len(C[0]&C[1])==mode,'network_boundary_overlap')
   ck(not any(all(tuple(sorted(e)) in {tuple(sorted(f)) for f in E} for e in combinations(K,2)) for K in combinations(C,3)),'network_trianglefree')
# Enumerate all loopless cubic multigraphs at the claimed small core sizes.
core_counts={};types=Counter();prism={(0,1),(0,2),(1,2),(3,4),(3,5),(4,5),(0,3),(1,4),(2,5)}
prism={tuple(sorted(e)) for e in prism}
for n in [2,4,6]:
 total=blocks=0
 for A in cubic_multigraphs(n):
  total+=1
  if not block(A):continue
  blocks+=1;simple=max(map(max,A))==1
  if n==2:ck(A[0][1]==3,'two_vertex_core');types['triple_edge']+=1
  elif n==4:
   if simple:ck(all(A[i][j]==1 for i in range(n) for j in range(n) if i!=j),'four_vertex_simple');types['K4']+=1
   else:
    B=reduction(A);ck(len(B)==2 and B[0][1]==3,'four_vertex_parallel_reduction');types['series_parallel_four']+=1
  elif simple:
   comp=[{j for j in range(n) if j!=i and not A[i][j]} for i in range(n)]
   seen={0};todo=[0]
   while todo:
    for v in comp[todo.pop()]:
     if v not in seen:seen.add(v);todo.append(v)
   if len(seen)==6:
    E={(i,j) for i in range(n) for j in range(i+1,n) if A[i][j]};ck(any({tuple(sorted((p[a],p[b]))) for a,b in E}==prism for p in permutations(range(6))),'prism_simple_core');types['prism']+=1
   else:
    ck(len(seen)==3 and all(A[i][j]==int((i in seen)!=(j in seen)) for i in range(n) for j in range(n)),'K33_nonplanar_core');types['K33_excluded']+=1
  else:
   B=reduction(A);ck(len(B)==4 and block(B) and all(sum(r)==3 for r in B) and not any(B[i][i] for i in range(4)),'six_vertex_parallel_reduction')
   types['K4_edge_network' if max(map(max,B))==1 else 'series_parallel_six']+=1
 core_counts[str(n)]={'all_loopless_cubic_multigraphs':total,'connected_no_cutvertex':blocks}
print(json.dumps({'status':'pass','assertions':sum(CHECK.values()),'breakdown':dict(CHECK),'SP_expressions':expressions,'trianglefree_SP_expressions':valid,'constructed_network_colorings':colorings,'small_core_counts':core_counts,'small_core_types':dict(types),'scope':'Exact controls for the written all-network induction and analytic small-core classification, not an all-graph source proof.'},indent=2,sort_keys=True))
