#!/usr/bin/env python3
"""Independent exact generation-family controls; not a large-rank theorem test."""
from itertools import combinations,product
from fractions import Fraction as F
from collections import Counter
import json

def mm(A,B,p):
 return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(len(B)))%p for j in range(len(B[0]))) for i in range(len(A)))
def tr(A):return tuple(zip(*A))
def eye(n):return tuple(tuple(int(i==j) for j in range(n)) for i in range(n))
def add(A,B,p,c=1):return tuple(tuple((x+c*y)%p for x,y in zip(a,b)) for a,b in zip(A,B))
def neg(A,p):return tuple(tuple(-x%p for x in a) for a in A)
def rref(A,p):
 A=[list(x) for x in A]
 if not A:return ()
 n=len(A[0]);r=0
 for c in range(n):
  z=next((z for z in range(r,len(A)) if A[z][c]%p),None)
  if z is None:continue
  A[r],A[z]=A[z],A[r];inv=pow(A[r][c],-1,p);A[r]=[x*inv%p for x in A[r]]
  for j in range(len(A)):
   if j!=r:
    a=A[j][c];A[j]=[(x-a*y)%p for x,y in zip(A[j],A[r])]
  r+=1
  if r==len(A):break
 return tuple(tuple(x) for x in A[:r])
def rank(A,p):return len(rref(A,p))
def subspaces(n,k,p):
 if k==0:yield ();return
 for piv in combinations(range(n),k):
  free=[(i,j) for i,c in enumerate(piv) for j in range(c+1,n) if j not in piv]
  for v in product(range(p),repeat=len(free)):
   A=[[int(j==c) for j in range(n)] for c in piv]
   for (i,j),x in zip(free,v):A[i][j]=x
   yield tuple(map(tuple,A))
def gram(U,B,p):return mm(mm(U,B,p),tr(U),p) if U else ()
def counts(n,B,p):
 r=[]
 for k in range(n+1):
  vals=list(subspaces(n,k,p));gs=[gram(U,B,p) for U in vals]
  r.append({'all':len(vals),'singular':sum(all(not x for row in G for x in row) for G in gs),'nondegenerate':sum(rank(G,p)==k for G in gs)})
 return r
def invariant(U,T,p):return rank(U+mm(U,T,p),p)==len(U) if U else True
# Exhaustive actual RREF spaces, exact invariant decomposition convolutions.
p=3;forms={'Sp4':((0,1,0,0),(2,0,0,0),(0,0,0,1),(0,0,2,0)),
'O4plus':tuple(tuple(int(i==j) for j in range(4)) for i in range(4)),
'O4minus':((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,2))}
T=((2,0,0,0),(0,2,0,0),(0,0,1,0),(0,0,0,1));small=[]
for name,B in forms.items():
 allc=counts(4,B,p);A=tuple(tuple(B[i][j] for j in range(2)) for i in range(2));D=tuple(tuple(B[i+2][j+2] for j in range(2)) for i in range(2));ac=counts(2,A,p);bc=counts(2,D,p)
 for k in range(5):
  actual=Counter()
  for U in subspaces(4,k,p):
   if invariant(U,T,p):
    G=gram(U,B,p)
    if all(not x for row in G for x in row):actual['singular']+=1
    if rank(G,p)==k:actual['nondegenerate']+=1
  for key in ['singular','nondegenerate']:
   expected=sum(ac[i][key]*bc[k-i][key] for i in range(3) if 0<=k-i<=2)
   if actual[key]!=expected:raise RuntimeError((name,k,key,actual,expected))
  small.append({'form':name,'k':k,'total':allc[k],'invariant_singular':actual['singular'],'invariant_nondegenerate':actual['nondegenerate']})
# Symplectic strong class in dimension4: every nondegenerate plane gives x=I-2projection.
B=forms['Sp4'];classes=[]
for U in subspaces(4,2,3):
 G=gram(U,B,3)
 if rank(G,3)!=2:continue
 a,b=G[0];c,d=G[1];det=(a*d-b*c)%3;di=pow(det,-1,3);Gi=((d*di%3,-b*di%3),(-c*di%3,a*di%3))
 # row-vector projection x -> x B U^t (U B U^t)^-1 U
 P=mm(mm(mm(B,tr(U),3),Gi,3),U,3)
 X=add(eye(4),P,3,-2)
 if mm(X,X,3)!=eye(4) or mm(mm(X,B,3),tr(X),3)!=B:raise RuntimeError('bad Sp involution')
 classes.append(X)
cs=set(classes)
if len(cs)!=90 or any(neg(x,3) not in cs for x in cs):raise RuntimeError('Sp class/lift check')
x=classes[0];two_lifts=len({x,neg(x,3)}&cs)
if two_lifts!=2:raise RuntimeError('lost central lift')
# Equal-negative lemma: complete conjugacy class of rank-one negative GL3(3) involutions.
lines=list(subspaces(3,1,3));invol=[]
for (u,) in lines:
 for f in product(range(3),repeat=3):
  if sum(x*y for x,y in zip(u,f))%3==1:
   P=tuple(tuple(u[i]*f[j]%3 for j in range(3)) for i in range(3));invol.append(add(eye(3),P,3,-2))
if len(set(invol))!=117:raise RuntimeError('GL3 class count')
t=tuple(tuple((2 if i==0 else 1) if i==j else 0 for j in range(3)) for i in range(3));hist=Counter()
for s in invol:
 y=mm(t,s,3);v=eye(3);o=0
 while True:
  o+=1;v=mm(v,y,3)
  if v==eye(3):break
  if o>11232:raise RuntimeError('order bound')
 hist[o]+=1;z=eye(3)
 if o%2==0:
  for _ in range(o//2):z=mm(z,y,3)
 zm=add(z,eye(3),3);tp=add(t,eye(3),3,-1);tn=add(t,eye(3),3)
 pos=3-rank(zm+tp,3);negative=3-rank(zm+tn,3)
 if pos!=negative:raise RuntimeError('equal-negative failure')
# Exact endpoint/exponent inequalities, with no floating-point traces.
nd=ts=0
for e in range(3,121):
 for a in range((e+2)//3,(2*e)//3+1):
  b=e-a
  for k in range(1,e//2+1):
   for i in range(k+1):
    j=k-i
    if i<=a and j<=b:
     D=i*b+j*a-2*i*j
     if 12*D<e*k:raise RuntimeError('nondegenerate exponent')
     nd+=1
    if 2*i<=a and 2*j<=b:
     D=i*b+j*a-3*i*j
     if 12*D<e*k:raise RuntimeError('singular exponent')
     ts+=1
for e in [384,385,500,1000]:
 for k in range(1,e//2+1):
  if 128*(k+1)>3**(e*k//48):raise RuntimeError('constant absorption')
for e in range(16,401):
 if F(1,e)+F(1,e-2)>F(1,6):raise RuntimeError('Burness exponent')
 # (21/256)*3^(e^2/45)>=1, equivalent after raising45th power.
 if 21**45*3**(e*e)<256**45:raise RuntimeError('projective class lower bound')
# Exact first-success law for a weighted mixture of product-class supports.
support=[(0,0),(0,1),(1,0),(1,1),(2,2),(2,3)];w=[F(1,8)]*4+[F(1,4)]*2;law=Counter();success=F(0)
for idx in product(range(6),repeat=3):
 prob=w[idx[0]]*w[idx[1]]*w[idx[2]];sel=next((i for i in idx if i<4),None)
 if sel is not None:success+=prob;law[support[sel]]+=prob
if success!=F(7,8) or any(v/success!=F(1,4) for v in law.values()):raise RuntimeError('first success bias')
print(json.dumps({'scope':'finite structural/arithmetic guards; not a proof by tested large-rank instances','RREF_subspace_controls':small,'Sp4_F3_strong_class_size':len(cs),'same_projective_element_lifts_in_class':two_lifts,'exact_extra_graph_bound':str(F(two_lifts,len(cs))),'GL3_F3_complete_involution_class':len(invol),'product_order_histogram':dict(sorted(hist.items())),'equal_negative_all_class_elements':True,'closed_endpoint_integer_cases':{'nondegenerate':nd,'totally_singular':ts,'max_dimension':120},'Burness_and_absorption_exact_guards':True,'first_success_target_probability':str(success),'first_success_each_target_atom':str(F(1,4)),'passed':True},indent=2))
