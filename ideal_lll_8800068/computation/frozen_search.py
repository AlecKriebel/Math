from pathlib import Path
#!/usr/bin/env python3
"""Search LLL feasibility with a deliberately long first row held fixed.
Floating point only chooses unimodular operations. Reported candidates receive
an independent exact rational audit. No floating-point result is a proof.
"""
import json,random
import numpy as np
import sympy as S
from fractions import Fraction
from cyclic_search import basis,audit

def gs(B):
 A=np.array(B,dtype=float);n=len(A);G=A.copy();D=np.zeros(n);mu=np.zeros((n,n))
 for i in range(n):
  for j in range(i):
   mu[i,j]=np.dot(A[i],G[j])/D[j];G[i]-=mu[i,j]*G[j]
  D[i]=np.dot(G[i],G[i])
 return mu,D

def frozen_lll(B,steps=10000):
 B=[[int(x) for x in B.row(i)] for i in range(B.rows)];n=len(B);k=1
 for step in range(steps):
  if k>=n:return S.Matrix(B),step
  for j in range(k-1,-1,-1):
   mu,D=gs(B);q=int(np.rint(mu[k,j]))
   if q:B[k]=[x-q*y for x,y in zip(B[k],B[j])]
  mu,D=gs(B)
  if k==1 or D[k]+mu[k,k-1]**2*D[k-1]>=.75*D[k-1]-1e-8:k+=1
  else:B[k],B[k-1]=B[k-1],B[k];k=max(1,k-1)
 return None,steps

def boundary(B):
 b=list(map(Fraction,B.row(0)));c=list(map(Fraction,B.row(1)));a=sum(x*x for x in b);u=sum(x*y for x,y in zip(b,c))/a
 # (D2+mu21^2 D1)/D1 = ||b2||^2/||b1||^2.
 return sum(x*x for x in c)/a

out=[]
for n,m in [(6,4),(8,5),(10,6),(12,8),(16,12)]:
 best=None;trials=0
 for c in [0,1,2,m//2,m]:
  for t in [-m,-m//2,-1,0,1,m//2,m]:
   B=basis(n,m);B[0,:]+=c*B[1,:]+t*B[n-1,:]
   for seed in [0,1,2]:
    R=B.copy();rng=random.Random(8800068+1000*n+100*c+10*t+seed)
    ids=list(range(1,n));rng.shuffle(ids);R=R[[0]+ids,:]
    for _ in range(n):
     i,j=rng.sample(range(1,n),2);R[i,:]+=rng.choice([-1,1])*R[j,:]
    F,steps=frozen_lll(R);trials+=1
    if F is None:continue
    score=boundary(F)
    if best is None or score>Fraction(best['boundary_score']):
     best={'n':n,'m':m,'c':c,'t':t,'seed':seed,'steps':steps,'boundary_score':str(score),'first_squared':str(sum(x*x for x in F.row(0))),'basis':[[int(x) for x in F.row(i)] for i in range(n)],'audit':audit(F,m)}
 best['trials']=trials;out.append(best)
 print(n,m,best['boundary_score'],best['audit']['reduced'],flush=True)
 with open(Path(__file__).with_name('frozen_results.json'),'w') as f:json.dump(out,f,indent=2)
