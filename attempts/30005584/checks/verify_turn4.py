"""Symbolic warped-product even block and finite rational Schur controls."""
import sympy as s
from itertools import product
from collections import Counter
import json
C=Counter()
def ck(x,n):
 assert x,n
 C[n]+=1
A,B,Cc,D,E,p,q,x,y,z,t,w=s.symbols('A B C D E p q x y z t w',real=True)
# Base indices (0,2,3); tensor entries p=S00,x=S02,y=S03,z=S22,t=S23,w=S33.
T=s.Matrix([[p,0,x,y],[0,q,0,0],[x,0,z,t],[y,0,t,w]])
Gamma=s.zeros(4);Gamma[0,1]=A;Gamma[1,0]=-A
circle=-Gamma*T-T*Gamma.T
norm=sum(v*v for v in circle)
ck(s.expand(norm-2*A*A*((p-q)**2+x*x+y*y))==0,'circle_connection_square')
K={(0,1):-Cc,(0,2):-D,(0,3):-D,(1,2):-A*B,(1,3):-A*B,(2,3):E}
R={}
for (i,j),v in K.items():
 R[i,j,j,i]=v;R[j,i,i,j]=v;R[i,j,i,j]=-v;R[j,i,j,i]=-v
rm=sum(T[i,j]*R.get((i,k,l,j),0)*T[k,l] for i,j,k,l in product(range(4),repeat=4))
base=[0,2,3]
rmb=sum(T[i,j]*R.get((i,k,l,j),0)*T[k,l] for i,j,k,l in product(base,repeat=4))
ck(s.expand(rm-rmb+2*q*(Cc*p+A*B*(z+w)))==0,'mixed_curvature_contraction')
extra=s.expand(norm-2*(rm-rmb))
expected=2*A*A*(p*p+x*x+y*y)+2*A*A*q*q+4*q*((Cc-A*A)*p+A*B*(z+w))
ck(s.expand(extra-expected)==0,'Hessian_log_a_coupling')
# General finite scalar-block square, including positive definite matrix blocks.
for h1,h2,b11,b12,b21,b22,u1,u2,v1,v2 in product(range(1,3),range(1,3),range(-1,2),range(-1,2),range(-1,2),range(-1,2),range(-1,2),range(-1,2),range(-1,2),range(-1,2)):
 H=s.diag(h1,h2);Rr=s.Matrix([[b11,b12],[b21,b22]]);u=s.Matrix([u1,u2]);v=s.Matrix([v1,v2]);bval=Rr*u;inv=s.diag(s.Rational(1,h1),s.Rational(1,h2))
 left=(v.T*H*v)[0]+4*(v.T*bval)[0]
 shifted=v+2*inv*bval
 right=(shifted.T*H*shifted)[0]-4*(bval.T*inv*bval)[0]
 ck(left==right,'rational_matrix_completion')
# Explicit finite warning against separate-block positivity.
Q=s.Matrix([[1,2],[2,1]])
ck(Q[0,0]>0 and Q[1,1]>0 and Q.det()<0,'positive_diagonal_blocks_can_be_indefinite')
for m0,m1,m2,m3 in product(range(8),repeat=4):
 ck((m0+3*m1+5*m2+7*m3)%2==(m0+m1+m2+m3)%2,'SO3_odd_dimension_parity')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'counts':dict(sorted(C.items())),'sympy_version':s.__version__,'scope':'Exact local contractions and finite Schur identities; compactness, closed-domain inertia and the original unresolved degree are separate analytic matters.'},indent=2,sort_keys=True))
