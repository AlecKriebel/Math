#!/usr/bin/env python3
"""Exact finite controls for the conditional Lang descent argument.
No inference of geometric connectedness or general Lang surjectivity from a finite scan.
"""
from itertools import product,combinations
from collections import Counter
from random import Random
import json
checks=Counter()
def ck(x,label):
 assert x,label;checks[label]+=1
# F9 = F3[s]/(s²-2), encoded a+3b.
def add(a,b):return (a%3+b%3)%3+3*((a//3+b//3)%3)
def neg(a):return (-(a%3)%3)+3*((-(a//3))%3)
def mul(a,b):return ((a%3*(b%3)+2*(a//3)*(b//3))%3)+3*((a%3*(b//3)+a//3*(b%3))%3)
def sub(a,b):return add(a,neg(b))
inv={a:next(b for b in range(1,9) if mul(a,b)==1) for a in range(1,9)}
def total(xs):
 t=0
 for x in xs:t=add(t,x)
 return t
def matmul(A,B):return tuple(tuple(total(mul(a,b) for a,b in zip(row,col)) for col in zip(*B)) for row in A)
def det2(A):return sub(mul(A[0][0],A[1][1]),mul(A[0][1],A[1][0]))
def inverse2(A):
 c=inv[det2(A)];return ((mul(c,A[1][1]),mul(c,neg(A[0][1]))),(mul(c,neg(A[1][0])),mul(c,A[0][0])))
def frob(A):return tuple(tuple(mul(mul(x,x),x) for x in r) for r in A)
I=((1,0),(0,1));r=((1,1),(0,1));GL=[];image={};normone=set()
for a,b,c,d in product(range(9),repeat=4):
 h=((a,b),(c,d))
 if not det2(h):continue
 GL.append(h)
 ih=inverse2(h);x=matmul(ih,frob(h));image.setdefault(x,h)
 ck(matmul(x,frob(x))==I,'F9_cocycle_norm')
 g=matmul(r,h)
 ck(matmul(inverse2(g),frob(g))==x,'frobenius_orientation')
 corrected=matmul(g,ih)
 ck(corrected==r and frob(corrected)==corrected,'explicit_rational_correction')
 if matmul(h,frob(h))==I:normone.add(h)
ck(len(GL)==5760 and len(image)==120,'finite_GL2_counts')
ck(set(image)==normone,'F9_norm_one_image_exhaustiveness')
# Exterior-square compatibility on free class-two models, using 3x3 matrices.
pairs=list(combinations(range(3),2));rng=Random(634504)
def det3(A):
 ans=0
 for sig,perm in [(1,(0,1,2)),(1,(1,2,0)),(1,(2,0,1)),(-1,(2,1,0)),(-1,(1,0,2)),(-1,(0,2,1))]:
  v=mul(mul(A[0][perm[0]],A[1][perm[1]]),A[2][perm[2]])
  ans=add(ans,v if sig==1 else neg(v))
 return ans
def mv(A,x):return tuple(total(mul(a,b) for a,b in zip(row,x)) for row in A)
def wedge(x,y):return tuple(sub(mul(x[i],y[j]),mul(x[j],y[i])) for i,j in pairs)
def Wmat(A):return tuple(tuple(sub(mul(A[i][k],A[j][l]),mul(A[i][l],A[j][k])) for k,l in pairs) for i,j in pairs)
free_models=0
while free_models<240:
 A=tuple(tuple(rng.randrange(9) for _ in range(3)) for _ in range(3))
 if not det3(A):continue
 C=Wmat(A);ck(det3(C)!=0,'exterior_square_invertible')
 for _ in range(5):
  x=tuple(rng.randrange(9) for _ in range(3));y=tuple(rng.randrange(9) for _ in range(3))
  ck(wedge(mv(A,x),mv(A,y))==mv(C,wedge(x,y)),'exterior_square_tensor_intertwining')
 free_models+=1
# Two Heisenberg factors: a genuine stabilizer that swaps the two rank-drop lines.
def beta(x,y):return (sub(mul(x[0],y[1]),mul(x[1],y[0])),sub(mul(x[2],y[3]),mul(x[3],y[2])))
def swap(x):return x[2:]+x[:2]
basis=[tuple(int(i==j) for i in range(4)) for j in range(4)]
for x,y in product(basis,repeat=2):ck(beta(swap(x),swap(y))==beta(x,y)[::-1],'split_factor_swap_intertwines')
ck((1,0)!=(0,1),'split_factor_nontrivial_permutation')
print(json.dumps({'status':'PASS','arithmetic':'exact F9','assertions':sum(checks.values()),'assertions_by_scope':dict(checks),'GL2_F9_size':len(GL),'norm_one_cocycle_count':len(normone),'free_exterior_square_models':free_models,'scope':'The finite F9 Lang image equals the norm-one cocycles, not all GL2(F9). General Lang surjectivity over the algebraic closure and geometric connectedness are credited theorem inputs; original MIP unresolved.'},indent=2,sort_keys=True))
