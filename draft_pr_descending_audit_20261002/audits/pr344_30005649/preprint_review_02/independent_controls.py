#!/usr/bin/env python3
"""Reviewer-written substantive algebra controls. No author-code imports, writes, or network."""
from fractions import Fraction as Q
import json,itertools,random
count=0;rejected=[]
def require(c,n):
 global count
 count+=1
 if not c:raise RuntimeError(n)
def trans(a):return list(map(list,zip(*a)))
def mul(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def inv(a):
 n=len(a);r=[list(map(Q,row))+list(map(Q,e)) for row,e in zip(a,eye(n))]
 for j in range(n):
  i=next((i for i in range(j,n) if r[i][j]),None)
  if i is None:raise ValueError('singular')
  r[i],r[j]=r[j],r[i];c=r[j][j];r[j]=[x/c for x in r[j]]
  for i in range(n):
   if i!=j:
    c=r[i][j];r[i]=[x-c*y for x,y in zip(r[i],r[j])]
 return [row[n:] for row in r]
def arrows(n,ar):
 a=[[0]*n for _ in range(n)]
 for s,t,c in ar:a[t][s]=c
 return a
F=arrows(6,[(0,1,1),(1,2,1),(3,4,1)])
V=arrows(6,[(0,5,1),(3,2,1),(5,4,1)])
B=trans([[0,1,0,1,0,1],[0,0,1,0,1,0],[0,2,0,1,0,0],[0,0,1,0,0,0],[1,0,0,0,0,0],[0,1,0,0,0,0]])
Binv=inv(B)
require(mul(B,Binv)==eye(6),'basis inverse')
for op in (F,V):
 C=mul(mul(Binv,op),B)
 for d in (2,4):require(all(C[i][j]==0 for i in range(d,6) for j in range(d)),'stable flag')
 for d in (0,2,4):require([row[d:d+2] for row in C[d:d+2]]==[[0,0],[1,0]],'exact elliptic factor')
wrong=eye(6)
C=mul(mul(inv(wrong),V),wrong);require(any(C[i][j] for i in range(2,6) for j in range(2)),'wrong flag rejected');rejected.append('rank-two factor with unstable V')
# Integral controls use exact rationals and cyclic coefficient evaluations, not the shipped Laurent engine.
def shift(a,s):return [a[(i+s)%6] for i in range(6)]
def integral_basis(a,p):
 a=list(map(Q,a));e=eye(6)
 m1=[e[1][i]+e[3][i]+e[5][i] for i in range(6)]
 m0=[p*e[0][i]+e[2][i]+e[4][i] for i in range(6)]
 x=[a[1]*e[3][i]-a[3]*e[1][i] for i in range(6)]
 y=[a[0]*e[2][i]-p*a[2]*e[0][i] for i in range(6)]
 return trans([m1,m0,x,y,[Q(z)/a[0] for z in e[0]],[Q(z)/a[1] for z in e[1]]])
for p,a in itertools.product((5,7,11),([1,5,2,7,-3,-12],[2,-1,4,3,-6,-2],[3,2,-1,5,-2,-7])):
 A=arrows(6,[(i,(i+1)%6,p if i in (2,4,5) else 1) for i in range(6)])
 C=arrows(6,[(i,(i-1)%6,p if i in (1,2,4) else 1) for i in range(6)])
 require(mul(A,C)==[[p*x for x in row] for row in eye(6)],'integral FV')
 basis=integral_basis(a,p);bi=inv(basis)
 for op,s in ((A,1),(C,-1)):
  action=mul(mul(bi,op),integral_basis(shift(a,s),p))
  for d in (2,4):require(all(action[i][j]==0 for i in range(d,6) for j in range(d)),'saturated integral flag')
  for d in (0,2,4):require([row[d:d+2] for row in action[d:d+2]]==[[0,p],[1,0]],'integral standard factor')
 bad=mul(mul(bi,A),basis)
 require(bad!=mul(mul(bi,A),integral_basis(shift(a,1),p)),'missing sigma rejected')
 require([row[2:4] for row in bad[2:4]]!=[[0,p],[1,0]],'wrong untwisted middle factor rejected')
rejected.extend(['integral basis change without sigma','middle elliptic factor without coefficient twists'])
# F_125 as a field of polynomial triples; dense Frobenius basis changes, independent Gaussian elimination.
p=5;q=125
Z=(0,0,0);O=(1,0,0)
def ad(x,y):return tuple((a+b)%p for a,b in zip(x,y))
def neg(x):return tuple(-a%p for a in x)
def mt(x,y):
 r=[0]*5
 for i,a in enumerate(x):
  for j,b in enumerate(y):r[i+j]+=a*b
 for i in (4,3):r[i-3]-=r[i];r[i-2]-=r[i]
 return tuple(a%p for a in r[:3])
def pw(x,n):
 r=O
 while n:
  if n%2:r=mt(r,x)
  x=mt(x,x);n//=2
 return r
def mm(a,b):
 return [[sumf([mt(x,y) for x,y in zip(row,col)]) for col in zip(*b)] for row in a]
def sumf(xs):
 r=Z
 for x in xs:r=ad(r,x)
 return r
def ei(n):return [[O if i==j else Z for j in range(n)] for i in range(n)]
def fieldmatrix(a):return [[(int(x)%p,0,0) for x in row] for row in a]
def tw(a,n):return [[pw(x,n) for x in row] for row in a]
def rr(a):
 a=[row[:] for row in a];n=len(a);d=0
 for j in range(len(a[0])):
  i=next((i for i in range(d,n) if a[i][j]!=Z),None)
  if i is None:continue
  a[d],a[i]=a[i],a[d];c=pw(a[d][j],q-2);a[d]=[mt(c,x) for x in a[d]]
  for i in range(n):
   if i!=d:
    c=a[i][j];a[i]=[ad(x,neg(mt(c,y))) for x,y in zip(a[i],a[d])]
  d+=1
  if d==n:break
 return d,a
def fi(a):return [r[len(a):] for r in rr([x+y for x,y in zip(a,ei(len(a)))])[1]]
def join(a,b):return [x+y for x,y in zip(a,b)]
def delta(f,v):
 f2=mm(f,tw(f,5));v2=mm(v,tw(v,25))
 return rr(f2)[0]+rr(v2)[0]-rr(join(f2,v2))[0]
require(all((x**3+x+1)%5 for x in range(5)),'irreducible cubic')
f,v=fieldmatrix(F),fieldmatrix(V)
rng=random.Random(34002);P=ei(6)
for i in range(6):
 for j in range(i+1,6):P[i][j]=(rng.randrange(5),rng.randrange(1,5),rng.randrange(5))
Pi=fi(P);require(mm(Pi,P)==ei(6),'dense basis inverse')
ff=mm(mm(Pi,f),tw(P,5));vv=mm(mm(Pi,v),tw(P,25))
fd=trans(tw(vv,5));vd=trans(tw(ff,25))
require(delta(ff,vv)==0 and delta(fd,vd)==1,'basis-invariant obstruction')
# The dual difference also equals codimension of ker F^2 + ker V^2 via annihilators.
f2=mm(ff,tw(ff,5));v2=mm(vv,tw(vv,25))
untwisted=rr(f2)[0]+rr(v2)[0]-rr(join(trans(f2),trans(v2)))[0]
corrected=rr(f2)[0]+rr(v2)[0]-rr(join(trans(tw(v2,25)),trans(tw(f2,5))))[0]
require(corrected==1 and untwisted==0,'opposite square twists are essential')
rejected.append('untwisted row-space dual kernel formula')
require(fd!=trans(vv) and vd!=trans(ff),'plain transpose rejected on dense nonprime basis');rejected.append('general dual as bare transposes')
require(tw(P,5)!=tw(P,25),'sigma inverse directions distinct')
L=[[O if i in (0,3,5) and (0,3,5)[j]==i else Z for j in range(3)] for i in range(6)]
require(rr(join(f,L))[0]==6 and rr(mm(v,L))[0]==3,'Honda conditions')
badL=[[O if i==(0,1,3)[j] else Z for j in range(3)] for i in range(6)]
require(rr(join(f,badL))[0]!=6 or rr(mm(v,badL))[0]!=3,'bad Honda L rejected');rejected.append('Honda L meeting im F')
mut=[r[:] for r in v];mut[5][0]=Z
require(rr(f)[0]+rr(mut)[0]!=6,'missing edge exactness rejected');rejected.append('lost V edge')
# Surjectivity of p kernels can fail in finite exact sequences.
require(all((p*x)%25==0 for x in (0,5,10,15,20)) and all(x%5==0 for x in (0,5,10,15,20)),'finite p-kernel map zero counterexample');rejected.append('p-kernel exactness without p-divisibility')
print(json.dumps(dict(status='PASS',assertions=count,rejected_mutants=rejected,integral_sample_pairs=9,dense_extension_field=125,delta_original=0,delta_dual=1,untwisted_row_formula=untwisted,corrected_twisted_row_formula=corrected,dense_basis=P,scope='Independent exact and finite corroboration. The universal symbolic proof and source theorem premises are reviewed separately.'),indent=2))
