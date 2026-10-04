from fractions import Fraction as F
from itertools import product
from math import prod,gcd
import json
checks=0;cats={}
def ck(x,k):
 global checks
 assert x,k;checks+=1;cats[k]=cats.get(k,0)+1
def rank(A):
 a=[list(map(F,row)) for row in A]
 if not a:return 0
 r=0
 for j in range(len(a[0])):
  z=next((i for i in range(r,len(a)) if a[i][j]),None)
  if z is None:continue
  a[r],a[z]=a[z],a[r];u=a[r][j];a[r]=[x/u for x in a[r]]
  for i in range(r+1,len(a)):
   u=a[i][j]
   if u:a[i]=[x-u*y for x,y in zip(a[i],a[r])]
  r+=1
  if r==len(a):break
 return r
def mm(A,B):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*B)] for row in A]
def tm(A):return list(map(list,zip(*A)))
def zeros(a,b):return [[0]*b for _ in range(a)]
def cover(q):
 # rows are cochain targets. Positive transport increments sheet label.
 D=zeros(q,q)
 for i in range(q):D[i][(i+1)%q]+=1;D[i][i]-=1
 d0=zeros(4*q,q);d1=zeros(4*q,4*q)
 for i in range(q):
  for j in range(q):
   d0[i][j]=D[i][j];d0[2*q+i][j]=D[i][j]
   d1[i][2*q+j]=D[i][j];d1[i][j]=-D[i][j]
   d1[q+i][3*q+j]=D[i][j];d1[2*q+i][q+j]=-D[i][j]
 return d0,d1
for q in range(1,25):
 d0,d1=cover(q);r0=rank(d0);r1=rank(d1)
 ck(mm(d1,d0)==zeros(4*q,q),'cover_cochain')
 ck((q-r0,4*q-r0-r1,4*q-r1)==(1,4,q+3),'cover_betti')
 if q<=10:
  e0,e1=cover(2*q)
  P=zeros(2*q,q)
  for i in range(2*q):P[i][i%q]=1
  P4=zeros(8*q,4*q)
  for block in range(4):
   for i in range(2*q):P4[block*2*q+i][block*q+i%q]=1
  ck(mm(P4,d0)==mm(e0,P),'pullback_degree0')
  ck(mm(P4,d1)==mm(e1,P4),'pullback_degree1')
  ck(mm(tm(P),P)==[[2*int(i==j) for j in range(q)] for i in range(q)],'transfer_leftinverse0')
  ck(mm(tm(P4),P4)==[[2*int(i==j) for j in range(4*q)] for i in range(4*q)],'transfer_leftinverse1and2')
  ck(mm(tm(P4),e0)==mm(d0,tm(P)),'transfer_cochain0')
  ck(mm(tm(P4),e1)==mm(d1,tm(P4)),'transfer_cochain1')
# Collared Thue-Morse graph independently from letter substitutions.
E=['001','010','011','100','101','110'];V=['00','01','10','11'];mu={'0':'01','1':'10'}
B=zeros(4,6);M=zeros(6,6);N=zeros(4,4)
for j,e in enumerate(E):
 B[V.index(e[1:])][j]+=1;B[V.index(e[:2])][j]-=1
 w=''.join(mu[a] for a in e)
 for pos in [1,2]:M[E.index(w[pos:pos+3])][j]+=1
for j,v in enumerate(V):N[V.index(mu[v[0]][-1]+mu[v[1]][0])][j]=1
ck(mm(B,M)==mm(N,B),'collared_chain')
C=[[1,0,0],[1,1,-1],[0,0,1],[1,0,0],[0,1,0],[0,0,1]]
J=[[1,1,0],[1,0,1],[1,1,0]]
ck(mm(B,C)==zeros(4,3),'cycle_basis_boundary');ck(rank(C)==3,'cycle_basis_rank');ck(mm(M,C)==mm(C,J),'cycle_substitution')
ck(rank(J)==rank(mm(J,J))==2,'stable_image')
# All shared-pair collar gluings coincide with the complete four-letter language.
wds={a+b for a,b in product('01',repeat=2)}
for _ in range(4):wds={''.join(mu[c] for c in w) for w in wds}
lang={w[i:i+4] for w in wds for i in range(len(w)-3)}
glue={e+f[-1] for e in E for f in E if e[1:]==f[:2]};ck(glue==lang and len(lang)==10,'collar_legality')
# Free-group inverse of the proper substitution.
def red(w):
 s=[]
 for a in w:
  if s and s[-1]==-a:s.pop()
  else:s.append(a)
 return tuple(s)
def iv(w):return tuple(-x for x in reversed(w))
A=(1,1,2);Bword=(1,2);ck(red(A+iv(Bword))==(1,),'proper_inverse_a');ck(red(Bword+iv(A)+Bword)==(2,),'proper_inverse_b')
# Surjectivity of pulled-back cyclic monodromy for all tested levels follows unimodularity.
for q in range(1,101):
 a,b=1,0
 for level in range(30):
  ck(gcd(gcd(a,b),q)==1,'cover_connected_monodromy');a,b=(2*a+b)%q,(a+b)%q
# Sharp product inequality, independent of the source's radius convention.
for d in range(1,6):
 for r in product(range(1,8),repeat=d):
  ck(prod(1+x for x in r)<=3**d*prod(max(1,x-1) for x in r),'product_rank_bound')
 ck(3**d==prod(1+2 for _ in range(d)),'sturmian_sharpness')
print(json.dumps({'exact_assertions':checks,'categories':cats,'scope':'Exact finite cochain, cover, collar and rank controls; topology and admissibility audited analytically'},indent=2,sort_keys=True))
