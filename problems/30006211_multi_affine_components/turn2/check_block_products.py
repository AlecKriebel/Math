#!/usr/bin/env python3
from fractions import Fraction as Q
from itertools import product
import random,json

def solve(A,c,m):
 R=[[Q(x) for x in row]+[Q(y)] for row,y in zip(A,c)];piv=[];r=0
 for j in range(m):
  k=next((i for i in range(r,len(R)) if R[i][j]),None)
  if k is None:continue
  R[r],R[k]=R[k],R[r];a=R[r][j];R[r]=[x/a for x in R[r]]
  for i in range(len(R)):
   if i!=r and R[i][j]:a=R[i][j];R[i]=[x-a*y for x,y in zip(R[i],R[r])]
  piv.append(j);r+=1
 if any(all(not x for x in row[:m]) and row[m] for row in R):return None
 h=[Q(0)]*m
 for i,j in enumerate(piv):h[j]=R[i][m]
 kernel=[]
 for j in range(m):
  if j in piv:continue
  v=[Q(0)]*m;v[j]=1
  for i,k in enumerate(piv):v[k]=-R[i][j]
  kernel.append(v)
 return h,kernel,len(piv)
checks=0
def ck(x):
 global checks
 assert x;checks+=1
rng=random.Random(34502);consistent=empty=0;counts={}
for case in range(300):
 m=rng.randrange(1,6);r=rng.randrange(1,4);sizes=[rng.randrange(1,4) for _ in range(m)]
 while sum(k-1 for k in sizes)>7:sizes[rng.randrange(m)]=1
 A=[[rng.randrange(-2,3) for _ in range(m)] for _ in range(r)];h0=[rng.randrange(-2,3) for _ in range(m)]
 c=[sum(a*x for a,x in zip(row,h0)) for row in A]
 if case%5==0:c=[rng.randrange(-2,3) for _ in range(r)]
 s=solve(A,c,m)
 if s is None:empty+=1;continue
 consistent+=1;h,K,rank=s;ck(all(sum(a*x for a,x in zip(row,h))==b for row,b in zip(A,c)));ck(all(all(sum(a*x for a,x in zip(row,v))==0 for row in A) for v in K))
 fixed=[i for i in range(m) if h[i] and all(v[i]==0 for v in K)];ck(len(fixed)<=rank)
 canzero=[]
 for i in range(m):
  e=[0]*m;e[i]=1;ok=solve(A+[e],c+[0],m) is not None;ck(ok==(i not in fixed));canzero.append(ok)
 bits=[]
 for i,k in enumerate(sizes):bits.extend([i]*(k-1))
 N=1<<len(bits);left=set(range(N));components=0
 while left:
  components+=1;todo=[left.pop()]
  while todo:
   u=todo.pop()
   for j,i in enumerate(bits):
    v=u^(1<<j)
    if canzero[i] and v in left:left.remove(v);todo.append(v)
 exponent=sum(sizes[i]-1 for i in fixed);ck(components==2**exponent);ck(exponent<=rank*(max(sizes)-1));counts[str(components)]=counts.get(str(components),0)+1
# Exact balanced sign sections, using perfect powers to avoid floating roots.
for k in range(1,8):
 for scale in (1,2,3):
  for sign in (-1,1):
   for sig in product((-1,1),repeat=k-1):
    last=sign
    for s in sig:last*=s
    xs=[s*scale for s in sig]+[last*scale];p=1
    for x in xs:p*=x
    ck(p==sign*scale**k)
print(json.dumps({'assertions':checks,'consistent_linear_systems':consistent,'inconsistent_linear_systems':empty,'branch_graph_component_counts':counts,'scope':'Finite exact linear algebra, branch graphs, and sign sections; the continuum path argument is supplied in the proof.'},indent=2))
