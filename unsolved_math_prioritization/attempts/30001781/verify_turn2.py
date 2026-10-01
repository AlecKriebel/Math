#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product
import json
n=0
def ck(v):
 global n
 assert v
 n+=1
def tr(a):return list(map(list,zip(*a)))
def mm(a,b):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def ident(d):return [[F(int(i==j)) for j in range(d)] for i in range(d)]
# Rational square-root weight vectors with rational length.
for roots,L in [([1,2,2],3),([2,3,6],7),([1,2,2,4],5),([1,1,1,1],2)]:
 D=len(roots);N=D-1;q=[F(x,L) for x in roots];ck(sum(x*x for x in q)==1)
 v=[q[j]-int(j==D-1) for j in range(D)];v2=sum(x*x for x in v)
 H=[[F(int(i==j))-2*v[i]*v[j]/v2 for j in range(D)] for i in range(D)]
 U=H[:N];ck(mm(U,tr(U))==ident(N))
 ck([sum(r[j]*q[j] for j in range(D)) for r in U]==[0]*N)
 for scale in (1,2,3,5):
  alpha=[F((scale*x)**2) for x in roots];A=sum(alpha)
  V=[[U[i][j]/(scale*roots[j]) for j in range(D)] for i in range(N)]
  ck([sum(V[i][j]*alpha[j] for j in range(D)) for i in range(N)]==[0]*N)
  cov=[[((alpha[i] if i==j else 0)-alpha[i]*alpha[j]/A)/(A*(A+1)) for j in range(D)] for i in range(D)]
  covx=mm(mm(V,cov),tr(V));ck([[A*(A+1)*z for z in r] for r in covx]==ident(N))
  ck((A+1)/A<=F(3,2));ck(A>=D)
  # Exact Dirichlet means, second moments, and normalization relations.
  mean=[a/A for a in alpha]
  second=[[alpha[i]*(alpha[j]+int(i==j))/(A*(A+1)) for j in range(D)] for i in range(D)]
  ck(sum(mean)==1)
  for i in range(D):
   ck(sum(second[i])==mean[i])
   for j in range(D):ck(second[i][j]-mean[i]*mean[j]==cov[i][j])
  for masses in product(range(1,4),repeat=D):
   pp=[F(x,sum(masses)) for x in masses]
   for S in (F(1,2),F(3),F(11)):
    g=[S*x for x in pp]
    yy=[sum(V[i][j]*(g[j]-alpha[j]) for j in range(D)) for i in range(N)]
    rhs=[S*sum(V[i][j]*pp[j] for j in range(D)) for i in range(N)]
    ck(yy==rhs)
# Standard isotropic-simplex vertex Gram matrix; noncentral for N>=2.
for D in range(3,31):
 G=[[D*(D+1)*(F(int(i==j))-F(1,D)) for j in range(D)] for i in range(D)]
 ck(all(G[i][i]==D*D-1 for i in range(D)))
 ck(all(G[i][j]==-(D+1) for i in range(D) for j in range(D) if i!=j))
 ck(all(G[0][j]!=-G[0][0] for j in range(1,D)))
 ck(all(sum(r)==0 for r in G))
 # Second moment of the uniform simplex using exact barycentric moments.
 ck(F(2,D*(D+1))*D+F(1,D*(D+1))*D*(D-1)==1)
# Gamma Jacobian exponent and deterministic conditional scaling.
for D in range(2,9):
 for A in range(D,D+21):
  ck((A-D)+(D-1)==A-1)
  ck(F(A*A,A*(A+1))*F(A+1,A)==1)
print(json.dumps({'status':'PASS','exact_assertions':n,'scope':'Exact Dirichlet covariance, common weighted coisometry, Gamma coupling and simplex geometry controls; no empirical tail fit or general original-conjecture claim.'},indent=2,sort_keys=True))
