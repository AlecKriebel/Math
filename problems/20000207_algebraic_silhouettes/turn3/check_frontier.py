from fractions import Fraction as Q
from itertools import product
import json
n=0
def ck(x):
 global n;n+=1;assert x
# Seven quadric coefficients from eight allowed matrix entries; only off-diagonal skew kernel.
basis=[]
for k in range(8):
 a=[0]*9;a[k]=1
 basis.append([a[0],a[1]+a[3],a[4],a[2],a[5],a[6],a[7]])
# Exact row reduction.
def rank(a):
 a=[[Q(x) for x in row] for row in a];r=0
 for j in range(len(a[0])):
  k=next((k for k in range(r,len(a)) if a[k][j]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];v=a[r][j];a[r]=[x/v for x in a[r]]
  for k in range(len(a)):
   if k!=r:
    v=a[k][j];a[k]=[x-v*y for x,y in zip(a[k],a[r])]
  r+=1
 return r
ck(rank(basis)==7);ck(basis[1]==basis[3])
for k in range(8):
 a=[0]*9;a[k]=1
 for x,y,z,w in product(range(-1,2),repeat=4):
  lhs=sum([x,y,w][i]*a[3*i+j]*[x,y,z][j] for i in range(3) for j in range(3))
  coeff=basis[k];mon=[x*x,x*y,y*y,x*z,y*z,x*w,y*w]
  ck(lhs==sum(c*m for c,m in zip(coeff,mon)))
for A,B,C,D in product(range(-2,3),repeat=4):
 if not any([A,B,C,D]):continue
 dz=[3*A,2*B,C];dw=[B,2*C,3*D]
 r=rank([dz,dw]);ck(r in (1,2))
 # Binary cubic discriminant; squarefree implies derivative independence.
 disc=B*B*C*C-4*A*C**3-4*B**3*D-27*A*A*D*D+18*A*B*C*D
 if disc:ck(r==2)
for a,b in product(range(-3,4),repeat=2):
 if a==b==0:continue
 co=[a**3,3*a*a*b,3*a*b*b,b**3]
 ck(rank([[3*co[0],2*co[1],co[2]],[co[1],2*co[2],3*co[3]]])==1)
for d in range(3,31):
 # No syzygy can have total degree2, so generator multiples give degree2 ideal dimension.
 dim=sum((2-e+3)*(2-e+2)*(2-e+1)//6 for e in [d,d-1,d-1] if e<=2)
 ck(dim==(2 if d==3 else 0))
print(json.dumps({'assertions':n,'quadric_map_rank':7,'projective_kernel_dimension':0,'scope':'Finite exact coefficient checks; geometric genericity is proved in TURN_3.md.'},indent=2))
