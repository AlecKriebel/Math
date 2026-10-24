#!/usr/bin/env python3
"""Independent certificate verifier: no HNF or saturation routine is imported.
All lattice decisions use rational ranks and determinantal divisors.
"""
import itertools,json,math,sys,time
from functools import lru_cache
from fractions import Fraction
from pathlib import Path

def determinant(A):
 A=[list(r) for r in A];n=len(A);previous=1;sign=1
 if n==0:return 1
 for k in range(n-1):
  if A[k][k]==0:
   q=next((j for j in range(k+1,n) if A[j][k]),None)
   if q is None:return 0
   A[k],A[q]=A[q],A[k];sign=-sign
  pivot=A[k][k]
  for i in range(k+1,n):
   for j in range(k+1,n):A[i][j]=(pivot*A[i][j]-A[i][k]*A[k][j])//previous
  previous=pivot
  for i in range(k+1,n):A[i][k]=0
 return sign*A[n-1][n-1]

@lru_cache(None)
def rank(A,d):
 a=[[Fraction(x) for x in r] for r in A];k=0
 for c in range(d):
  q=next((i for i in range(k,len(a)) if a[i][c]),None)
  if q is None:continue
  a[k],a[q]=a[q],a[k];z=a[k][c];a[k]=[x/z for x in a[k]]
  for i in range(k+1,len(a)):
   z=a[i][c];a[i]=[x-z*y for x,y in zip(a[i],a[k])]
  k+=1
  if k==len(a):break
 return k

@lru_cache(None)
def divisor(A,r,d):
 if r==0:return 1
 g=0
 for I in itertools.combinations(range(len(A)),r):
  for J in itertools.combinations(range(d),r):
   g=math.gcd(g,abs(determinant([[A[i][j] for j in J] for i in I])))
   if g==1:return 1
 return g

@lru_cache(None)
def member_after_2_saturation(A,v,d):
 r=rank(A,d);B=A+(v,)
 if rank(B,d)!=r:return False
 order=divisor(A,r,d)//divisor(B,r,d)
 return order>0 and order&(order-1)==0

def verify(n):
 data=json.loads(Path(f'universal_{n}_certificate.json').read_text());nodes=data['nodes'];d=n-1;started=time.time()
 cycles=[(0,)+p for p in itertools.permutations(range(1,n)) if p[0]<p[-1]]
 relations=[];pairs=[]
 for Q in itertools.combinations(range(n),4):
  a,b,c,z=Q
  for L,R in [((a,b),(c,z)),((a,c),(b,z)),((a,z),(b,c))]:
   relations.append(tuple(int(x in L)-int(x in R) for x in range(1,n)));pairs.append((L,R))
 cycle_events=[]
 for a in cycles:
  E={tuple(sorted((a[i],a[(i+1)%n]))) for i in range(n)}
  cycle_events.append(tuple(j for j,(L,R) in enumerate(pairs) if L in E and R in E))
 Hs=[tuple(tuple(row) for row in x['lattice']) for x in nodes]
 diffs=[tuple(int(k==i)-int(k==j) for k in range(1,n)) for i,j in itertools.combinations(range(n),2)]
 assert Hs[data['root']]==()
 edges=[];leafcount=0
 for ni,node in enumerate(nodes):
  H=Hs[ni];r=rank(H,d);assert r==len(H)
  assert divisor(H,r,d)%2==1 # Basis lattice is saturated at2.
  assert all(not member_after_2_saturation(H,v,d) for v in diffs)
  ci=node['cycle'];CE=cycle_events[ci]
  assert tuple(b['event'] for b in node['branches'])==CE
  assert all(not member_after_2_saturation(H,relations[j],d) for j in CE)
  for branch in node['branches']:
   row=relations[branch['event']];L=H+(row,)
   if 'child' in branch:
    target=branch['child'];K=Hs[target]
    assert H!=K
    assert all(member_after_2_saturation(K,x,d) for x in L)
    assert all(member_after_2_saturation(L,x,d) for x in K)
    edges.append((ni,target))
   else:
    i,j=branch['forced_equal_vertices'];v=tuple(int(k==i)-int(k==j) for k in range(1,n))
    assert member_after_2_saturation(L,v,d);leafcount+=1
  if (ni+1)%500==0:print('checked',ni+1,'nodes',time.time()-started,flush=True)
 # Check directed acyclicity explicitly, independent of lattice-inclusion reasoning.
 incoming=[0]*len(nodes);children=[[] for _ in nodes]
 for i,j in edges:incoming[j]+=1;children[i].append(j)
 stack=[i for i,x in enumerate(incoming) if not x];removed=0
 while stack:
  i=stack.pop();removed+=1
  for j in children[i]:
   incoming[j]-=1
   if incoming[j]==0:stack.append(j)
 assert removed==len(nodes)
 result={'n':n,'nodes':len(nodes),'child_edges':len(edges),'collision_leaves':leafcount,'seconds':time.time()-started,'passed':True,'method':'Independent rational rank, Bareiss determinant, and determinantal-divisor index; no HNF or saturation helper imported.'}
 Path(f'universal_{n}_independent_verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':verify(int(sys.argv[1]) if len(sys.argv)>1 else 7)
