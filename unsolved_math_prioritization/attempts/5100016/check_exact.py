"""Exact k304 controls; topology and complex analysis remain in the proof."""
from fractions import Fraction as Q
from collections import Counter
from math import gcd
import sympy as s,json
C=Counter()
def ck(x,k):
 assert x,k
 C[k]+=1
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def det(x,y):return x[0]*y[1]-x[1]*y[0]
def area(P):return sum(det(P[i],P[(i+1)%len(P)])for i in range(len(P)))/2
def foot(n,h,M):return tuple(M[j]+(h-dot(n,M))*n[j]/dot(n,n)for j in range(2))
x,y,z,w,a,b=s.symbols('x y z w a b',real=True);t=(x,y);r=(z,w);M=(a,b)
proj=lambda t:tuple(v*dot(t,M)/dot(t,t)for v in t)
rhs=dot(M,M)*det(t,r)*dot(t,r)/(2*dot(t,t)*dot(r,r))+(det(t,M)*dot(t,M)/dot(t,t)-det(r,M)*dot(r,M)/dot(r,r))/2
ck(s.cancel(det(proj(t),proj(r))-rhs)==0,'radial_symbolic_identity')
alpha,k,kp,sv,cv,dv=s.symbols('alpha k kp sv cv dv',nonzero=True)
aa=alpha*dv/cv;bb=alpha*kp/cv
np=(-dv/(k*cv*aa),-s.I*kp/(k*cv*bb))
ck(all(s.cancel(np[i]+[1,s.I][i]/(alpha*k))==0 for i in range(2)),'common_isotropic_normal_exact')
ck(s.simplify(dot(np,np))==0,'normal_isotropic')
z1,z2=s.symbols('z1 z2');ck(s.simplify(det(tuple(z1*x for x in np),tuple(z2*x for x in np)))==0,'adjacent_double_pole_coefficient_zero')
X,Y,K2=s.symbols('X Y K2');CV2=1-Y;DV2=1-K2*Y;KP2=1-K2
norm2=X/(DV2/CV2)+(1-X)/(KP2/CV2)
D=DV2-K2*CV2*X
ck(s.factor(norm2-D/((KP2/CV2)*DV2))==0,'normal_denominator_identity')
for N in range(4,201,4):
 m=N//2
 for tau in range(1,m):
  if gcd(tau,N)>1:continue
  ck(m%2==0 and tau%2==1,'target_parity')
  ck(Q(m,2).denominator==1,'K_is_trace_period')
  ck(gcd(tau,m)==1,'reduced_period_Bezout')
  left=Q(1,2)-Q(tau,2*m);right=Q(1,2)+Q(tau,2*m)
  pole_indices=[j for j in range(N)if (left+Q(j*tau,m)-left).denominator==1 or(left+Q(j*tau,m)-right).denominator==1]
  ck(pole_indices==sorted({0,1,m,m+1}),'complete_four_singular_index_list')
  hits=Counter(j*tau%m for j in range(N))
  ck(set(hits)==set(range(m))and set(hits.values())=={2},'trace_residue_multiplicity')
  ck(((Q(1,2)+Q(tau,2*m))-left-Q(tau,m))==0,'pole_pair_separated_by_step')
  for j in range(N):
   jj=(j+1)%N
   if j in pole_indices and jj in pole_indices:
    ck(N==4 or(j,jj)in[(0,1),(m,m+1)],'adjacent_pole_pattern_including_N4')
# Arbitrary centrally symmetric line pedals with rational direction data.
for m in range(2,10):
 H=[(Q(1),Q(j,m))for j in range(m)];ns=H+[tuple(-x for x in n)for n in H]
 coeff=sum(2*det(ns[i],ns[(i+1)%(2*m)])*dot(ns[i],ns[(i+1)%(2*m)])/(dot(ns[i],ns[i])*dot(ns[(i+1)%(2*m)],ns[(i+1)%(2*m)]))for i in range(2*m))/8
 ck((coeff==0 if m==2 else coeff>0),'convex_coefficient_m2_and_larger')
 for shift in range(3):
  hs=[Q(j+shift+2,j+1)for j in range(m)]*2
  base=area([foot(n,h,(0,0))for n,h in zip(ns,hs)])
  ck(base>0,'origin_pedal_positive')
  for X in range(-3,4):
   for Y in range(-3,4):
    M=(Q(X,2),Q(Y,3));B=area([foot(n,h,M)for n,h in zip(ns,hs)])
    ck(B==base+coeff*dot(M,M),'rational_radial_foot_area')
    ck(B>0,'convex_all_M_positive')
for A in [Q(1),Q(3,2),Q(2),Q(7,3)]:
 for B in [Q(1,2),Q(1),Q(4,3)]:
  ns=[(1,0),(0,1),(-1,0),(0,-1)];hs=[A,B,A,B]
  for X in range(-3,4):
   for Y in range(-3,4):
    f=area([foot(n,h,(Q(X),Q(Y)))for n,h in zip(ns,hs)])
    ck(f==2*A*B,'four_period_rectangle_half_area_all_M')
kp2=Q(15,16);lo=Q(3,4)*kp2;hi=Q(3,4)/kp2
ck(lo==Q(45,64)and hi==Q(4,5),'exact_star_angle_endpoints')
ck(Q(1,2)<lo<hi<1,'negative_double_angle_sine_interval')
ck(gcd(8,3)==1,'star_primitive')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(sorted(C.items())),'scope':'Exact identities, parity/pole indexing, rational projection geometry and star angle arithmetic; not a finite substitute for the meromorphic proof.'},indent=2,sort_keys=True))
