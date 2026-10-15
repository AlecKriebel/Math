#!/usr/bin/env python3
"""Locally authored exact algebra and finite index checks; not the all-period proof."""
import sympy as z,math,json
from collections import Counter
C=Counter()
def ck(v,key):assert bool(v),key;C[key]+=1
def eq(v,key):ck(z.cancel(z.together(v))==0,key)
S,Cn,D,s,c,d,k,kp=z.symbols('S C D s c d k kp',nonzero=True)
D0=1-k*k*s*s*S*S
# Reduce only square relations. This is exact polynomial ideal membership, not sampling.
basis=z.groebner([Cn*Cn+S*S-1,D*D+k*k*S*S-1,c*c+s*s-1,d*d+k*k*s*s-1,kp*kp+k*k-1],Cn,D,c,d,kp,S,s,k,order='lex')
def red(v,key):
 n=z.fraction(z.cancel(z.together(v)))[0]; ck(basis.reduce(z.expand(n))[1]==0,key)
a=d/c;b=kp/c;A=d*d/(c*c);B=kp/(c*c)
sp=(S*c*d+s*Cn*D)/D0;sm=(S*c*d-s*Cn*D)/D0
cp=(Cn*c-S*s*D*d)/D0;cm=(Cn*c+S*s*D*d)/D0
red(a*a-b*b-k*k,'original_focus_identity')
for sn,cn in [(sp,cp),(sm,cm)]:red(sn*S*d/c+cn*Cn/c-1,'actual_outer_tangent_incidence')
rminus=z.Matrix([-A*sm,B*cm]);rplus=z.Matrix([-A*sp,B*cp]);M=z.Matrix([k,0]);qm=rminus-M;qp=rplus-M
det=lambda a,b:a[0]*b[1]-a[1]*b[0]
red(det(rminus,rplus)-2*A*B*s*c*D/D0,'outer_cross_determinant')
red(det(qm,qp)-2*B*s*d*D*(a+k*S)/D0,'focal_antipedal_determinant')
# Isotropic roots and the unique real overlap equation.
aa,bb,kk=z.symbols('a b k',nonzero=True)
eq(1/(kk*kk)+(1-aa*aa/(kk*kk))/(bb*bb)-(bb*bb+kk*kk-aa*aa)/(kk*kk*bb*bb),'isotropic_focal_normal')
x,rr=z.symbols('x r')
eq((1-rr*rr)*x*x-2*x+1-((1-(1+rr)*x)*(1-(1-rr)*x)),'overlap_factorization')
eq((1-rr*rr)/(1+rr)**2-2/(1+rr)+1,'unique_in_unit_interval_root')
# Unrestricted residue vector and its four-way cancellation.
lx,ly,qx,qy,mx,my=z.symbols('lx ly qx qy mx my')
L=z.Matrix([lx,ly]);Q=z.Matrix([qx,qy]);MM=z.Matrix([mx,my]);J=lambda v:z.Matrix([-v[1],v[0]])
def V(M,Q):return -(L.dot(L))*J(Q-M)/det(L,Q-M)
v=V(MM,Q)
eq(L.dot(v)-L.dot(L),'residue_leading_pole_equation')
eq((Q-MM).dot(v),'residue_regular_neighbor_equation')
for i in range(2):
 eq(V(MM,-Q)[i]-V(-MM,Q)[i],'residue_pair_identity')
 eq((V(MM,Q)+V(MM,-Q)-V(-MM,Q)-V(-MM,-Q))[i],'four_residue_sum')
# Actual unrestricted rectangle antipedal intersections.
h,l,m,n=z.symbols('h l m n',nonzero=True);MM=z.Matrix([m,n]);P=[z.Matrix([h,l]),z.Matrix([-h,l]),z.Matrix([-h,-l]),z.Matrix([h,-l])]
def intersect(p,q):
 p=p-MM;q=q-MM;dd=det(p,q);x=(p.dot(p)*q[1]-q.dot(q)*p[1])/dd;y=(p[0]*q.dot(q)-q[0]*p.dot(p))/dd
 return MM+z.Matrix([x,y])
U=[intersect(P[i],P[(i+1)%4]) for i in range(4)];cent=sum(U,z.zeros(2,1))/4
pred=z.Matrix([m*((l*l-n*n)/(h*h-m*m)-1)/2,n*((h*h-m*m)/(l*l-n*n)-1)/2])
for i in range(2):eq(cent[i]-pred[i],'rectangle_arbitrary_focus_centroid')
eq(U[0][0]+m,'rectangle_top_x');eq(U[0][1]-l-(h*h-m*m)/(l-n),'rectangle_top_y')
# Every sampled primitive even orbit has precisely two real pole slots and four incident edges.
for N in range(4,402,2):
 for tau in range(1,N//2):
  if math.gcd(N,tau)>1:continue
  ck(tau%2==1,'even_primitive_odd_turning')
  ck((N//2*tau)%N==N//2,'antipodal_index')
  poles=[i for i in range(N) if (2*i*tau)%N==0]
  ck(poles==[0,N//2],'exact_two_real_pole_slots')
  ck((4*tau==N)==(N==4 and tau==1),'quarter_period_exception_only_four')
  if N>=6:ck(len({N-1,0,N//2-1,N//2})==4,'four_distinct_incident_vertices')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'sympy_version':z.__version__,'scope':'Exact rational identities and finite integer controls only; full analytic coverage is PROOF.md.'},indent=2))
