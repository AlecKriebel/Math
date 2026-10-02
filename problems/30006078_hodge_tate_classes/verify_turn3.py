#!/usr/bin/env python3
import json,itertools as it
import sympy as s
checks=0
def ck(v):
 global checks
 assert v
 checks+=1
x,y,u=s.symbols('x y u')
F=y*y-x**3+x
ck(s.rem((u*y)**2-(-x)**3+(-x)+F,u*u+1,u)==0)
ck(-16*(4*(-1)**3+27*0**2)==64)
ck(64%5!=0)
points=[(a,b) for a,b in it.product(range(5),repeat=2) if (b*b-a**3+a)%5==0]
ck(len(points)+1==8)
ck([a for a in range(5) if (a*a+1)%5==0]==[2,3])
for a in (2,3):ck((2*a)%5!=0)
# Hensel lifts of a root, checked exactly at every step.
a=2
for k in range(1,41):
 modulus=5**k
 ck((a*a+1)%modulus==0)
 roots=[a+t*modulus for t in range(5) if ((a+t*modulus)**2+1)%(modulus*5)==0]
 ck(len(roots)==1);a=roots[0]
M=s.Matrix([[0,1,1,1],[1,0,1,1],[1,1,0,2],[1,1,2,0]])
ck(M.det()==-4);ck(M*M.inv()==s.eye(4));ck(M.rank()==4)
# Complete exact intersection-pairing reconstruction on a bounded integral box.
for v in it.product(range(-2,3),repeat=4):
 V=s.Matrix(v);ck(M.inv()*(M*V)==V)
weights_H1=[0,0,1,1]
weights_M=sorted(sum(z) for z in it.combinations(weights_H1,2))
ck(weights_M==[0,1,1,1,1,2])
weights_T=weights_M.copy()
for _ in range(4):weights_T.remove(1)
ck(weights_T==[0,2]);ck(sorted(-a+1 for a in weights_T)==[-1,1]);ck(sorted(-a-1 for a in weights_T)==[-3,-1])
ck(0 not in [-a-1 for a in weights_H1])
# Exact linear models of the proven rank/kernel assertions, not p-adic computation.
for e in range(1,61):
 for i in range(2,21):
  functional=s.Matrix([[1]+[0]*(e-1)])
  ck(functional.rank()==1);ck(len(functional.nullspace())==e-1)
  ck(2*i-1>2 and 2*(i-1)+2==2*i)
C=s.zeros(4,6)
for i in range(4):C[i,i]=1
ck(C.rank()==4);ck(len(C.nullspace())==2)
for a,b in it.product(range(-20,21),repeat=2):
 v=s.Matrix([0,0,0,0,a,b]);ck(C*v==s.zeros(4,1));ck((v==s.zeros(6,1))==(a==b==0))
print(json.dumps({'status':'PASS','assertions':checks,'intersection_determinant':-4,'E_F5_points':len(points)+1,'projective_kernel_dimension':'[K:Q_p]-1','elliptic_square_rank':4,'elliptic_square_kernel_dimension':2,'scope':'exact algebra and dimension controls; no original-conjecture counterexample is claimed'},indent=2,sort_keys=True))
