#!/usr/bin/env python3
"""Own exact controls for the frozen PR946 global-Hessian audit; no original code imported.
Run: python3 independent_controls.py [output-json]
These finite controls supplement the proof and do not establish universal existence.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import datetime, hashlib, json, sys

def tr(a): return sum(a[i][i] for i in range(len(a)))
def T(a): return list(map(list,zip(*a)))
def mm(a,b): return [[sum(x*y for x,y in zip(r,c)) for c in T(b)] for r in a]
def add(a,b): return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def neg(a): return [[-x for x in r] for r in a]
def scale(a,s): return [[x*s for x in r] for r in a]
def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def inv(a):
 n=len(a); w=[list(map(F,r))+s for r,s in zip(a,eye(n))]
 for i in range(n):
  j=next(j for j in range(i,n) if w[j][i]); w[i],w[j]=w[j],w[i]
  s=w[i][i]; w[i]=[v/s for v in w[i]]
  for j in range(n):
   if j!=i:
    s=w[j][i]; w[j]=[x-s*y for x,y in zip(w[j],w[i])]
 return [r[n:] for r in w]
def det(a):
 if not a:return F(1)
 n=len(a); w=[list(map(F,r)) for r in a]; out=F(1)
 for i in range(n):
  js=[j for j in range(i,n) if w[j][i]]
  if not js:return F(0)
  j=js[0]
  if i!=j: w[i],w[j]=w[j],w[i]; out=-out
  pivot=w[i][i]; out*=pivot
  for j in range(i+1,n):
   s=w[j][i]/pivot
   for k in range(i+1,n):w[j][k]-=s*w[i][k]
 return out

def pd(a):return all(det([r[:k] for r in a[:k]])>0 for k in range(1,len(a)+1))
def psd(a):
 return all(det([[a[i][j] for j in I] for i in I])>=0 for k in range(1,len(a)+1) for I in combinations(range(len(a)),k))
def eq(a,b):return a==b

rows=[]
# Vanishing tangent eigenvalue, divergent cross block, all exact.
for k in [1,2,10,100,10000]:
 A=[[F(1,k**4),F(0)],[F(0),F(k*k)]]
 B=[[F(k),F(-k*k),F(2)],[F(1,k),F(3*k),F(-2*k)]]
 ai=inv(A); btab=mm(mm(T(B),ai),B)
 t=tr(ai)*sum(x*x for r in B for x in r); lam=1+t
 S=add(scale(eye(3),2*lam),neg(btab))
 bound=add(S,neg(scale(eye(3),2+t)))
 H=[A[i]+B[i] for i in range(2)]+[T(B)[j]+scale(eye(3),2*lam)[j] for j in range(3)]
 assert pd(H) and pd(S) and psd(bound)
 Q=[[F(3,5),F(-4,5)],[F(4,5),F(3,5)]]
 R=[[F(3,5),F(-4,5),F(0)],[F(4,5),F(3,5),F(0)],[F(0),F(0),F(-1)]]
 A2=mm(mm(T(Q),A),Q); B2=mm(mm(T(Q),B),R)
 t2=tr(inv(A2))*sum(x*x for r in B2 for x in r)
 assert t2==t
 rows.append({'k':k,'lambda':str(lam),'hessian_positive':True,'schur_bound_positive_semidefinite':True,'orthonormal_frame_change_exact':True})
# Mutants: no normal correction, or a fixed correction at a degeneration.
assert det([[F(1),F(1)],[F(1),F(0)]])<0
assert det([[F(1,1000000),F(100)],[F(100),F(2)]])<0
# Curved parabola: f(t)=(t,t^2), g=1+t, phi=(t+t^2,-(1+t)/2).
# F(t,v)=f(t)+v*(-2t,1)/sqrt(1+4t^2). Chain rule at t=v=0:
H0=[[F(1),F(-1,2)],[F(-1,2),F(0)]]
lam=1+F(1,4); H=add(H0,[[F(0),F(0)],[F(0),2*lam]])
assert H==[[F(1),F(-1,2)],[F(-1,2),F(5,2)]] and pd(H)
# tangent f'=e1 and f''=2e2: induced lowered coefficient is -1.
assert 2*H[1][0]==-1
assert 2*F(0)!=-1 # discarding mixed block breaks the prescribed connection.
# Circle: Psi=r^2-r gives radial Hessian eigenvalue2, tangential2-1/r.
for r in [F(3,5),F(1),F(100)]:assert 2-F(1)/r>0
# Noninjective gradient control, without floating point: pi<22/7.
# Psi=e^x+e^-x*cos(y)+y^2/(2*pi). At(log2,+/-pi/2), eta=(2,0).
# Horizontal rails at |y|=pi/2, e^x=s>=2 have det=s/pi-s^-2.
# Vertical connector e^x=4, |y|<=pi/2: Gxx>=4, Gyy>=1/pi-1/4,
# |Gxy|<=1/4, hence determinant>=4/pi-17/16.
pi_upper=F(22,7)
assert 2/pi_upper-F(1,4)>0
assert 4/pi_upper-F(17,16)>0

# Exact curvature and local eta-coordinate identities for a nonquadratic potential.
P={(2,0):F(1,2),(0,2):F(1,2),(3,0):F(1,6),(2,1):F(1,2),(0,4):F(1,24),(2,2):F(1,2)}
def derivative(alpha,pt):
 out=F(0)
 for powers,c in P.items():
  if any(a>p for a,p in zip(alpha,powers)):continue
  v=c
  for p,a,x in zip(powers,alpha,pt):
   for q in range(a):v*=p-q
   v*=x**(p-a)
  out+=v
 return out
def tensor_deriv(indices,pt):return derivative(tuple(indices.count(j) for j in range(2)),pt)
flat=[]
for pt in [(F(0),F(0)),(F(1,10),F(-1,10))]:
 G=[[tensor_deriv([a,b],pt) for b in range(2)] for a in range(2)]
 assert pd(G); Gi=inv(G)
 C=[[[tensor_deriv([i,a,b],pt) for b in range(2)] for a in range(2)] for i in range(2)]
 Gamma=[mm(Gi,c) for c in C]
 for k in range(2):
  for i in range(2):
   for j in range(2):assert Gamma[i][k][j]==Gamma[j][k][i]
 for i in range(2):
  for j in range(2):
   Hij=[[tensor_deriv([i,j,a,b],pt) for b in range(2)] for a in range(2)]
   d_i_Gamma_j=add(neg(mm(mm(Gi,C[i]),Gamma[j])),mm(Gi,Hij))
   d_j_Gamma_i=add(neg(mm(mm(Gi,C[j]),Gamma[i])),mm(Gi,Hij))
   Rcurv=add(add(d_i_Gamma_j,neg(d_j_Gamma_i)),add(mm(Gamma[i],Gamma[j]),neg(mm(Gamma[j],Gamma[i]))))
   assert Rcurv==[[0,0],[0,0]]
   # Covariant Hessian(eta_E)=Psi_Eij - Gamma^k_ij G_Ek.
   for E in range(2):assert C[i][E][j]==sum(G[E][k]*Gamma[i][k][j] for k in range(2))
 flat.append({'point':[str(x) for x in pt],'positive_hessian':True,'torsion_zero':True,'curvature_zero_exact':True,'eta_covariant_hessian_zero_exact':True})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pass':True,'arithmetic':'Python standard library fractions; exact rational arithmetic; analytic trigonometric control uses pi<22/7','universal_claim_limit':'Finite controls supplement the written argument; they are not a proof of universal existence.','schur_and_bundle_frame_checks':rows,'mutations_rejected':['normal correction removed','uniform constant correction under degeneration','mixed block discarded changes induced connection'],'curved_parabola_mixed_block':{'H0':[[str(x) for x in r] for r in H0],'H':[[str(x) for x in r] for r in H],'induced_lowered_connection':'-1'},'compact_circle_positive_annulus':'r>1/2','noninjective_gradient_connected_control':{'potential':'exp(x)+exp(-x)*cos(y)+y^2/(2*pi)','equal_gradient_points':['(log(2), pi/2)','(log(2), -pi/2)'],'equal_gradient':'(2,0)','positive_path':'horizontal rails to x=log(4), joined vertically; all inside same positive-Hessian component','rail_determinant_lower_bound':str(2/pi_upper-F(1,4)),'connector_determinant_lower_bound':str(4/pi_upper-F(17,16))},'dual_connection_checks':flat}
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
else:print(json.dumps(out,indent=2))
