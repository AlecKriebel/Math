#!/usr/bin/env python3
"""Exact controls: Gaussian quadratic variance, cyclic area, homogeneity and Gamma factors."""
from fractions import Fraction as Q
from math import factorial
import json
count=0
def check(x):
 global count
 assert x
 count+=1

def mul(a,b):
 return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def area(gs):
 z=(Q(0),Q(0));out=Q(0)
 for g in gs:
  zz=(z[0]+g[0],z[1]+g[1]);out+=det(z,zz)/2;z=zz
 check(z==(0,0));return out
# Independent rational covariance-matrix calculation of Var(x^T H y).
for n in range(3,25):
 C=[[Q(int(i==j),n)-Q(1,n*n) for j in range(n)] for i in range(n)]
 H=[[Q(1,2) if i<j else Q(-1,2) if i>j else Q(0) for j in range(n)] for i in range(n)]
 HC=mul(H,C)
 variance=-sum(HC[i][j]*HC[j][i] for i in range(n) for j in range(n))
 check(variance==Q((n-1)*(n-2),12*n*n))
 check(sum(C[i][i] for i in range(n))*2==Q(2*(n-1),n))
 for row in C:check(sum(row)==0)
# For n=3 there is exactly one positive orientation among the two cyclic orders.
for ax in range(-4,5):
 for ay in range(-4,5):
  for bx in range(-3,4):
   for by in range(-3,4):
    a=(Q(ax),Q(ay));b=(Q(bx),Q(by))
    if det(a,b)==0:continue
    c=(-a[0]-b[0],-a[1]-b[1]);s=area([a,b,c]);t=area([a,c,b])
    check(s==-t and s!=0)
    check(int(s>0)+int(t>0)==1)
    check(s==det(a,b)/2)
    for scale in (Q(1,3),Q(5,2)):
     scaled=[(scale*x,scale*y) for x,y in (a,b,c)]
     check(area(scaled)==scale*scale*s)
# Integer moments of the exact radial Gamma law and its variance.
for n in range(3,151):
 moments=[Q(2,n)**p*Q(factorial(n-2+p),factorial(n-2)) for p in range(7)]
 check(moments[1]==Q(2*(n-1),n))
 check(moments[2]-moments[1]**2==Q(4*(n-1),n*n))
 for p in range(6):check(moments[p+1]==moments[p]*Q(2*(n-1+p),n))
print(json.dumps({'status':'PASS','assertions':count,'coverage':['independent rational Gaussian signed-area variance','triangle filling count and cyclic area','positive-dilation area homogeneity','radial Gamma moment recursion'],'scope':'Finite exact controls; the n-sided filling count and mean asymptotic remain explicitly credited source inputs.'},indent=2,sort_keys=True))
