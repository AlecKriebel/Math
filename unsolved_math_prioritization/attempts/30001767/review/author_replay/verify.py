#!/usr/bin/env python3
"""Exact finite controls for the p-subgroup fixed-algebra theorem."""
from pathlib import Path
from hashlib import sha256
from itertools import permutations,product
import json
count=0;sections={}
def ck(ok,tag):
 global count
 assert bool(ok),tag
 count+=1;sections[tag]=sections.get(tag,0)+1

def compose(a,b):return tuple(a[b[i]] for i in range(len(a)))
def inverse(a):return tuple(a.index(i) for i in range(len(a)))
def closure(gens,n):
 e=tuple(range(n));G={e};todo=[e]
 while todo:
  a=todo.pop()
  for b in gens:
   c=compose(a,b)
   if c not in G:G.add(c);todo.append(c)
 return G

def gf2_kernel(rows,n):
 piv={}
 for row in rows:
  while row:
   p=row.bit_length()-1
   if p in piv:row^=piv[p]
   else:piv[p]=row;break
 free=[i for i in range(n) if i not in piv];out=[]
 for f in free:
  v=1<<f
  for p,row in sorted(piv.items()):
   if (row&v).bit_count()%2:v|=1<<p
  ck(all((row&v).bit_count()%2==0 for row in rows),'kernel certificate')
  out.append(v)
 return out

def group_case(n,gens):
 G=list(permutations(range(n)));N=len(G);ix={g:i for i,g in enumerate(G)};P=closure(gens,n)
 table=[[ix[compose(g,h)] for h in G] for g in G]
 def mul(a,b):
  c=0
  while a:
   lo=a&-a;i=lo.bit_length()-1;a^=lo;bb=b
   while bb:
    lo=bb&-bb;j=lo.bit_length()-1;bb^=lo;c^=1<<table[i][j]
  return c
 unseen=set(G);basis=[]
 while unseen:
  g=min(unseen);O={compose(compose(p,g),inverse(p)) for p in P};unseen-=O;basis.append(sum(1<<ix[h] for h in O))
 def center_basis(B):
  rows=[]
  for b in B:
   comm=[mul(a,b)^mul(b,a) for a in B]
   rows.extend(sum(((v>>g)&1)<<i for i,v in enumerate(comm)) for g in range(N))
  ker=gf2_kernel(rows,len(B));Z=[]
  for v in ker:
   z=0
   for i,a in enumerate(B):
    if (v>>i)&1:z^=a
   ck(all(mul(z,b)==mul(b,z) for b in B),'center certificate');Z.append(z)
  return Z
 def idempotents(Z):
  vals=[]
  for choice in range(1<<len(Z)):
   a=0
   for i,z in enumerate(Z):
    if (choice>>i)&1:a^=z
   if mul(a,a)==a:vals.append(a)
  return sorted(vals)
 ZC=center_basis(basis);ZA=center_basis([1<<i for i in range(N)])
 IC=idempotents(ZC);IA=idempotents(ZA)
 ck(IC==IA,'p-subgroup central idempotents')
 nonnormal=any(compose(compose(g,p),inverse(g)) not in P for p in P for g in G)
 ck(nonnormal,'nonnormal subgroup test')
 ck(len(P)&(len(P)-1)==0,'p-group order')
 for a in IC:
  ck(all(mul(a,1<<i)==mul(1<<i,a) for i in range(N)),'ambient centrality')
 return {'n':n,'subgroup_order':len(P),'centralizer_dimension':len(basis),'center_dimension':len(ZC),'central_idempotents':len(IC),'nonnormal':nonnormal}

cases=[]
cases.append(group_case(3,[(1,0,2)]))
cases.append(group_case(4,[(1,0,2,3)]))
cases.append(group_case(4,[(1,0,2,3),(0,1,3,2)]))
cases.append(group_case(4,[(1,0,2,3),(2,3,0,1)]))

# Matrix algebra controls, using complete finite enumeration.
def mm(a,b,n,p):return tuple(sum(a[n*i+k]*b[n*k+j] for k in range(n))%p for i in range(n) for j in range(n))
def matrix_case(n,p,u):
 A=list(product(range(p),repeat=n*n));C=[a for a in A if mm(a,u,n,p)==mm(u,a,n,p)]
 Z=[a for a in C if all(mm(a,b,n,p)==mm(b,a,n,p) for b in C)]
 ids=[a for a in Z if mm(a,a,n,p)==a];I=tuple(int(i==j) for i in range(n) for j in range(n));O=(0,)*(n*n)
 ck(set(ids)=={O,I},'matrix central idempotents')
 for a in ids:ck(all(mm(a,b,n,p)==mm(b,a,n,p) for b in A),'matrix ambient centrality')
 return A,C,Z,I
A,C,Z,I=matrix_case(3,2,(1,1,0,0,1,0,0,0,1))
e=(1,0,0,0,1,0,0,0,0);cross=(0,0,1,0,0,0,0,0,0)
ck(e in C and mm(e,e,3,2)==e,'noncentral idempotent distinction')
ck(cross in C and mm(e,cross,3,2)!=mm(cross,e,3,2),'noncentral idempotent distinction')
matrix_case(2,3,(1,1,0,1))
# An external P=C2 action swaps two blocks of F2 x F2; only the orbit sum
# is a primitive central idempotent of the fixed algebra.
A=list(product(range(2),repeat=2));fixed=[a for a in A if a==a[::-1]]
ck(fixed==[(0,0),(1,1)],'external orbit-sum control')
ck((1,0) not in fixed and (0,1) not in fixed,'external orbit-sum control')

# Characteristic-three non-p-group control: diag(1,-1) on M2.
A=list(product(range(3),repeat=4));t=(1,0,0,2)
C=[a for a in A if mm(a,t,2,3)==mm(t,a,2,3)]
ck(set(C)==set((a,0,0,b) for a,b in product(range(3),repeat=2)),'non-p-group countermodel')
ids=[a for a in C if mm(a,a,2,3)==a];ck(len(ids)==4,'non-p-group countermodel')
e=(1,0,0,0);v=(0,1,0,0)
ck(mm(e,v,2,3)!=mm(v,e,2,3),'non-p-group countermodel')
ck(mm(mm(t,v,2,3),t,2,3)==tuple(-a%3 for a in v),'fixed-vector failure')
ck(all((2*a)%3!=a for a in (1,2)),'fixed-vector failure')
# The class algebra of S3 in F3: nilpotent radical in its center.
G=list(permutations(range(3)));ix={g:i for i,g in enumerate(G)};N=len(G)
def gm(a,b):
 c=[0]*N
 for i,u in enumerate(a):
  for j,v in enumerate(b):c[ix[compose(G[i],G[j])]]=(c[ix[compose(G[i],G[j])]]+u*v)%3
 return tuple(c)
elem=tuple(int(g==tuple(range(3))) for g in G)
T=tuple(int(sum(g[i]!=i for i in range(3))==2) for g in G)
C3=tuple(int(sum(g[i]!=i for i in range(3))==3) for g in G)
J=tuple((a+b)%3 for a,b in zip(elem,C3));O=(0,)*N
ck(gm(T,T)==O and gm(J,J)==O and gm(T,J)==O,'S3 characteristic-three center')
for A in (T,J):
 for j in range(N):
  b=tuple(int(i==j) for i in range(N));ck(gm(A,b)==gm(b,A),'S3 characteristic-three center')
ids=[]
for a,b,c in product(range(3),repeat=3):
 v=tuple((a*elem[i]+b*T[i]+c*J[i])%3 for i in range(N))
 if gm(v,v)==v:ids.append(v)
ck(set(ids)=={O,elem},'S3 characteristic-three center')
receipt={'problem_id':30001767,'result':'PASS','assertions':count,'sections':sections,'group_controls':cases,'arithmetic':'exact finite-field operations, no floating point','artifact_sha256':sha256(Path('PARTIAL_RESULT.md').read_bytes()).hexdigest(),'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Small controls support the written all-p-group theorem; they do not settle the unrestricted symmetric-subgroup conjecture.'}
Path('verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
