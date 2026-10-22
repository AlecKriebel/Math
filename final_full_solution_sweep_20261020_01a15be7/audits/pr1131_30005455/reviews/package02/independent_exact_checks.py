#!/usr/bin/env python3
"""Independent exact finite controls, authored by whole-package review02.
No candidate code is imported. These controls are not universal proof certificates.
"""
from fractions import Fraction as Q
from math import factorial
import json

def det(a):
 a=[list(row) for row in a];out=Q(1)
 for i in range(len(a)):
  j=next((j for j in range(i,len(a)) if a[j][i]),None)
  if j is None:return Q(0)
  if j!=i:a[i],a[j]=a[j],a[i];out=-out
  d=a[i][i];out*=d
  for j in range(i+1,len(a)):
   scale=a[j][i]/d
   for k in range(i,len(a)):a[j][k]-=scale*a[i][k]
 return out

def need(x,msg):
 if not x:raise ValueError(msg)

def main():
 edges=[(0,1),(1,2),(2,3),(3,4)]
 a=list(map(Q,['1/12','1/4','3/4','9/4']))
 lam=list(map(Q,['1/16','5/24','5/8','15/8','9/16']))
 inc=[[i for i,e in enumerate(edges) if v in e] for v in range(5)]
 S=[sum((a[i]**2 for i in Is),Q()) for Is in inc]
 for i,(u,v) in enumerate(edges):need(a[i]**2*(lam[u]/S[u]+lam[v]/S[v])==a[i],'path equilibrium')
 K=[[(-a[i]**(-3) if i==j else Q())+2*sum((lam[v]/S[v]**2 for v in range(5) if i in inc[v] and j in inc[v]),Q()) for j in range(4)] for i in range(4)]
 minors=[det([row[:k] for row in K[:k]]) for k in range(1,5)]
 need(minors==list(map(Q,['4752/5','421632/25','782336/125','4194304/18225'])),'path minors')
 rows=[]
 for A,B,T,expected in [('17/4','13/3','29/5','1/1734'),('13/3','9/2','25/4','163/65598'),('9/2','5','243/32','5399/1361250'),('5','6','729/64','74117/6288490'),('6','7','2187/128','527104/16077675')]:
  A,B,T=Q(A),Q(B),Q(T);S0=T/(1+T);f=(S0*S0+(Q(3,2)-S0)**2)/Q(3,2);margin=1-1/A-f
  need(T**B.denominator>=Q(3,2)**B.numerator and margin==Q(expected)>0,'interval')
  rows.append(str(margin))
 expnew=sum((Q(8,5)**k/factorial(k) for k in range(5)),Q())+Q(8,5)**5/factorial(5)/(1-Q(4,15))
 expold=sum((Q(9,4)**k/factorial(k) for k in range(13)),Q())+Q(9,4)**13/factorial(13)/(1-Q(9,56))
 need(expnew<6 and Q(9,4)*(expold+1)<24,'exponential')
 print(json.dumps({'verdict':'PASS_FINITE_ONLY','path_minus_scaled_hessian':[[str(x) for x in row] for row in K],'path_leading_minors':[str(x) for x in minors],'five_strict_margins':rows,'new_exponential_upper':str(expnew),'old_exponential_upper':str(expold),'universal_proof_certified_by_software':False},sort_keys=True))
if __name__=='__main__':main()
