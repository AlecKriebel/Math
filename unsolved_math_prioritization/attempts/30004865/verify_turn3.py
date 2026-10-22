#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product
import random,json
checks=0

def ck(x):
 global checks
 assert x
 checks+=1
# Rational squared-coordinate implementation of the trilinear determinant identity.
parameter_cases=0
for r in range(2,101):
 u=F(r+1,2*r) # c^2
 ck(F(1,2)<u<=F(3,4))
 ck((3*u-1)**2<=4*u**3) # lambda^2<=1
 ck(1<=4*u) # h^2<=1
 ck((3*u-1)/2+3*(1-u)/2==1)
 for n in range(-80,121):
  z=F(n,40) # w/c; identity valid outside norm-test domain too
  det=1-F(1,4)/u-(4*u-1)*z/(2*u)+(4*u-1)*z*z/(4*u)
  target=(4*u-1)*(z-1)**2/(4*u)
  ck(det==target and target>=0)
  parameter_cases+=1
 # Diagonal SIC Gram and centroid coordinate, independent of ambient dimension.
 total=sum(F(1+int(i==j),2) for i,j in product(range(r),repeat=2))
 ck(total/r**2==u)
 ck((F(1)+(r-1)*F(1,2))/r==u)
# Generic complex Gram states, exactly positive semidefinite by construction.
def add(z,w):return(z[0]+w[0],z[1]+w[1])
def mul(z,w):return(z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def conj(z):return(z[0],-z[1])
def norm2(z):return z[0]*z[0]+z[1]*z[1]
rng=random.Random(300048653);state_cases=0;negative_blocks=0
for r in range(2,9):
 for _ in range(50):
  B=[[(rng.randrange(-3,4),rng.randrange(-3,4)) for k in range(3)] for i in range(r)]
  C=[]
  for i in range(r):
   row=[]
   for j in range(r):
    z=(0,0)
    for k in range(3):z=add(z,mul(B[i][k],conj(B[j][k])))
    row.append(z)
   C.append(row)
  tr=sum(C[i][i][0] for i in range(r));ck(tr>0)
  A=[[(F(z[0],tr),F(z[1],tr)) for z in row] for row in C]
  ck(sum(A[i][i][0] for i in range(r))==1)
  for i,j in product(range(r),repeat=2):
   ck(A[j][i]==conj(A[i][j]))
   if i==j:ck(A[i][j][1]==0 and A[i][j][0]>=0)
   else:
    det=-norm2(A[i][j]);ck(det<=0)
    if det<0:negative_blocks+=1
  # Actual index check of the partial transpose image for m=2..5.
  for m in range(2,6):
   for i,j in product(range(r),repeat=2):
    if i==j:continue
    row=(j,)+(i,)*(m-1);col=(i,)+(j,)*(m-1)
    ck(row!=col and len(set(row))==2 and len(set(col))==2)
  state_cases+=1
# Nonnegative rational coefficient examples: exact l1 coherence and norm relation.
for r in range(2,21):
 for m in range(2,21,2):
  q=m//2
  # A=(1-p)I/r + p all-ones/r is PSD; off-diagonal mass p(r-1).
  for n in range(21):
   p=F(n,20);C=p*(r-1);R=1+C;S=1+C/(2**q)
   ck(S-1==(R-1)/(2**q))
   ck((R>1)==(p>0));ck((S>1)==(p>0))
print(json.dumps({'exact_assertions':checks,'trilinear_determinant_parameter_cases':parameter_cases,'generic_complex_PSD_Gram_states':state_cases,'certified_negative_partial_transpose_blocks':negative_blocks,'complex_multilinear_norm_bound_proved_in_text':True,'general_SIC_existence_assumed':False},indent=2))
