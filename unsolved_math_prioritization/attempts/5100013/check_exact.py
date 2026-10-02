"""Own exact controls for the credited k204 corollary; not the analytic proof."""
from fractions import Fraction as Q
from math import gcd
from collections import Counter
import sympy as s
import json
C=Counter()
def ck(v,k):
 assert v,k
 C[k]+=1
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def area(P):return sum(det(P[i],P[(i+1)%len(P)])for i in range(len(P)))/2
def foot(n,h,M):
 c=(h-dot(n,M))/dot(n,n)
 return tuple(M[j]+c*n[j]for j in range(2))
def proj(t,M):return tuple(v*dot(t,M)/dot(t,t)for v in t)
x,y,z,w,a,b=s.symbols('x y z w a b',real=True);t=(x,y);v=(z,w);M=(a,b)
L=det(proj(t,M),proj(v,M))
R=dot(M,M)*det(t,v)*dot(t,v)/(2*dot(t,t)*dot(v,v))+(det(t,M)*dot(t,M)/dot(t,t)-det(v,M)*dot(v,M)/dot(v,v))/2
ck(s.cancel(L-R)==0,'symbolic_radial_telescope_identity')
for N in range(6,203,4):
 m=N//2
 for tau in range(1,m):
  if gcd(tau,N)>1:continue
  ck(m%2==tau%2==1,'primitive_target_parity')
  ck(gcd(tau,m)==1,'reduced_real_period_Bezout')
  ck(Q(m+tau,2).denominator==1,'K_plus_v_trace_period')
  hits=Counter((j*tau)%m for j in range(N))
  ck(set(hits)==set(range(m))and set(hits.values())=={2},'noncancelling_residue_multiplicity')
  for j in range(N):
   ck((j+m)%N not in[(j-1)%N,(j+1)%N],'simultaneous_poles_not_adjacent')
for N in range(4,121,4):
 m=N//2
 for tau in range(1,m):
  if gcd(tau,N)==1:ck(Q(m+tau,2).denominator==2,'wrong_even_parity_negative_control')
# Rational increasing normal directions over one half-turn, then antipodes.
# Arbitrary positive support distances preserve central line pairing.
for m in range(3,10):
 H=[(Q(1),Q(j,m))for j in range(m)]
 # This increasing fan plus its antipode defines a strict convex cyclic set of normals.
 normals=H+[tuple(-x for x in n)for n in H]
 coeff=sum(2*det(normals[i],normals[(i+1)%(2*m)])*dot(normals[i],normals[(i+1)%(2*m)])/(dot(normals[i],normals[i])*dot(normals[(i+1)%(2*m)],normals[(i+1)%(2*m)]))for i in range(2*m))/8
 ck(coeff>0,'convex_half_turn_sine_sum_exact')
 for shift in range(4):
  supports=[Q(j+shift+2,j+1)for j in range(m)]*2
  base=area([foot(n,h,(Q(0),Q(0)))for n,h in zip(normals,supports)])
  ck(base>0,'central_pedal_area_positive')
  for X in range(-4,5):
   for Y in range(-3,4):
    M=(Q(X,3),Q(Y,2));P=[foot(n,h,M)for n,h in zip(normals,supports)]
    ck(area(P)==base+coeff*dot(M,M),'direct_rational_pedal_radial_identity')
    ck(area(P)>0,'arbitrary_M_convex_positive')
# Explicit star angle interval, with pi factored out.
kp2=Q(15,16);lo=Q(3,5)*kp2;hi=Q(3,5)/kp2
ck(lo==Q(9,16)and hi==Q(16,25),'exact_star_angle_interval')
ck(Q(1,2)<lo<=hi<Q(1),'every_star_double_angle_sine_negative')
ck(gcd(10,3)==1 and 0<Q(3,5)<1,'star_family_primitive_and_v_range')
# Source caustic parameter identities, algebraic Jacobi relations.
k2,X=s.symbols('k2 X');cn2=1-X;dn2=1-k2*X
A2=dn2/cn2;B2=(1-k2)/cn2
ck(s.factor(A2-B2-k2)==0,'explicit_confocality')
ck(s.factor(A2-1-(B2-(1-k2)))==0,'same_positive_caustic_offset')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(sorted(C.items())),'scope':'Exact algebra, period parity, residue multiplicities and rational geometry controls. The written meromorphic and angle-bound proofs give the universal claims.'},indent=2,sort_keys=True))
