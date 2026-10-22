"""Independent k906 controls: direct exact tangent solves and physical billiards.

The exact star polygons are built from the original ellipse's tangent equations,
not copied from the candidate's lists of outer vertices. High-precision controls
use geometric reflections instead of repeated Jacobi evaluation of vertices.
"""
import sympy as s
from collections import Counter
from math import gcd
import json
import mpmath as mp
C=Counter()
def clean(x):return s.simplify(s.radsimp(x))
def eq(x,y,key):
 assert clean(x-y)==0,(key,clean(x-y))
 C[key]+=1
# Positive Jacobi half-quarter data from two algebraic doublings.
m=s.Rational(20111,20736);kp=s.Rational(25,144)
x=s.sqrt(s.Rational(96,221));y=s.sqrt(s.Rational(125,221));d=s.sqrt(s.Rational(125,216))
def dbl(z):
 a,b,c=z;D=1-m*a**4
 return tuple(clean(q/D) for q in (2*a*b*c,b*b-a*a*c*c,c*c-m*a*a*b*b))
h2=dbl((x,y,d));h4=dbl(h2)
for a,b in zip(h2,(s.Rational(12,13),s.Rational(5,13),s.Rational(5,12))):eq(a,b,'double_to_half_period')
for a,b in zip(h4,(1,0,kp)):eq(a,b,'double_to_K')
z=clean(y/d);r=clean(kp*x/d);dv=clean(kp/d)
pairs=[(0,1),(x,y),(h2[0],h2[1]),(z,r),(1,0),(z,-r),(h2[0],-h2[1]),(x,-y)]
pairs += [(-u,-v) for u,v in pairs]
a=clean(dv/r);b=clean(kp/r)
A0=s.Rational(221,96);B0=s.Rational(1105,144)
eq(a*a-b*b,m,'original_confocality')

def det(p,q):return p[0]*q[1]-p[1]*q[0]
def outer(phase):
 ans=[]
 for j in range(8):
  mid=(phase+6*j)%16
  sm,cm=pairs[(mid-3)%16];sp,cp=pairs[(mid+3)%16]
  n1=(-sm/a,cm/b);n2=(-sp/a,cp/b);D=clean(det(n1,n2))
  assert D!=0;C['exact_tangents_nonsingular']+=1
  Q=(clean((n2[1]-n1[1])/D),clean((n1[0]-n2[0])/D))
  eq(n1[0]*Q[0]+n1[1]*Q[1],1,'tangent_incidence')
  eq(n2[0]*Q[0]+n2[1]*Q[1],1,'tangent_incidence')
  sn,cn=pairs[mid]
  eq(Q[0],-A0*sn,'actual_outer_x')
  eq(Q[1],B0*cn,'actual_outer_y')
  ans.append(Q)
 return ans
Q0=outer(0);Qh=outer(1)
A=Q0[2][0];B=Q0[0][1]
eq(A,A0,'fitted_outer_axis_A');eq(B,B0,'fitted_outer_axis_B')
fo=clean(s.sqrt(B*B-A*A));eq(fo,221*s.sqrt(91)/288,'fitted_own_focus')

def inverse_area(Q,f):
 # Pair opposite edge terms before simplification; translation by f is omitted.
 U=[]
 for X,Y in Q:
  D=clean(X*X+(Y-f)**2)
  assert D!=0;C['finite_exact_inversion']+=1
  U.append((X/D,(Y-f)/D))
 total=0
 for i in range(4):
  total+=clean(det(U[i],U[(i+1)%8])+det(U[i+4],U[(i+5)%8]))
 return clean(total/2)
areas=[]
for Q in (Q0,Qh):
 positive=inverse_area(Q,fo);negative=inverse_area(Q,-fo)
 eq(positive,negative,'direct_own_focus_equality');areas.append(positive)
eq(areas[0],s.Rational(1473536,30525625),'positive_exact_phase_area')
eq(areas[1],-s.Rational(51985629184,12455533443925)*s.sqrt(30),'negative_exact_phase_area')
assert areas[0]>0>areas[1];C['IVT_opposite_signs']+=1
M,T=s.symbols('M T');V=1-2*T+M*T*T;Q=1-T;D2=1-M*T
for v in [D2*D2-(1-M)-M*V,Q*D2-M*V-(1-M)*(Q+M*T*T)]:eq(v,0,'axis_and_inside_identity')
# Numerical physical ray reflection controls, with ordinary-angle initial points.
mp.mp.dps=80
checks=0;cases=0;maxres=mp.mpf(0);positive_cases=0

def dot(x,y):return x[0]*y[0]+x[1]*y[1]
def add(x,y):return [x[i]+y[i] for i in range(2)]
def scale(c,x):return [c*z for z in x]
def sub(x,y):return [x[i]-y[i] for i in range(2)]
def norm(x):return mp.sqrt(dot(x,x))
def near(r):
 global checks,maxres
 r=abs(r);maxres=max(maxres,r);assert r<mp.mpf('1e-60'),mp.nstr(r);checks+=1

def tangent_intersection(P,Q,a,b):
 n1=[P[0]/a**2,P[1]/b**2];n2=[Q[0]/a**2,Q[1]/b**2];D=det(n1,n2)
 return [(n2[1]-n1[1])/D,(n1[0]-n2[0])/D]
def area_about(Q,f):
 U=[]
 for p in Q:
  d=sub(p,f);D=dot(d,d);assert D>0
  U.append(scale(1/D,d))
 return mp.fsum(det(U[i],U[(i+1)%len(U)]) for i in range(len(U)))/2
for N in (4,6,8,10,12,14):
 for tau in range(1,N//2):
  if gcd(tau,N)!=1:continue
  for beta in (mp.mpf(1)/5,mp.mpf(1)/2,mp.mpf(4)/5):
   m0=1-beta**2;K=mp.ellipk(m0);v=2*K*tau/N
   cv=mp.ellipfun('cn',v,m0);dv=mp.ellipfun('dn',v,m0)
   aa=dv/cv;bb=beta/cv;AA=aa*dv/cv;BB=bb/cv
   if abs(AA-BB)<mp.mpf('1e-65'):f=[mp.mpf(0),mp.mpf(0)]
   elif AA>BB:f=[mp.sqrt(AA**2-BB**2),mp.mpf(0)]
   else:f=[mp.mpf(0),mp.sqrt(BB**2-AA**2)]
   for theta in (mp.mpf(0),mp.mpf(2)/7,mp.mpf(9)/11):
    P=[aa*mp.cos(theta),bb*mp.sin(theta)];start=P[:]
    # Tangency to the caustic is solved on its affine unit-circle image.
    w=[P[0],P[1]/beta];R=dot(w,w);Jw=[-w[1],w[0]]
    qs=[add(scale(1/R,w),scale(sign*mp.sqrt(R-1)/R,Jw)) for sign in (1,-1)]
    targets=[[q[0],beta*q[1]] for q in qs]
    direction=next(sub(q,P) for q in targets if det(P,sub(q,P))>0)
    verts=[]
    for j in range(N):
     verts.append(P[:]);d=direction
     t=-2*(P[0]*d[0]/aa**2+P[1]*d[1]/bb**2)/(d[0]**2/aa**2+d[1]**2/bb**2)
     Q=add(P,scale(t,d));near(Q[0]**2/aa**2+Q[1]**2/bb**2-1)
     normal=[Q[0]/aa**2,Q[1]/bb**2]
     direction=sub(d,scale(2*dot(d,normal)/dot(normal,normal),normal));P=Q
    near(norm(sub(P,start))/(1+aa+bb))
    outerQ=[tangent_intersection(verts[j],verts[(j+1)%N],aa,bb) for j in range(N)]
    for j,q in enumerate(outerQ):
     near(q[0]**2/AA**2+q[1]**2/BB**2-1)
     near(norm(add(q,outerQ[(j+N//2)%N]))/(1+AA+BB))
    plus=area_about(outerQ,f);minus=area_about(outerQ,scale(-1,f))
    near((plus-minus)/(1+abs(plus)+abs(minus)))
    if tau==1:assert plus>0 and minus>0;positive_cases+=1
    cases+=1
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'exact_families':dict(C),'independent_star_areas':[str(x) for x in areas],'numerical_diagnostics':{'precision_decimal_digits':80,'physical_billiard_cases':cases,'checks':checks,'winding_one_positive_cases':positive_cases,'maximum_normalized_residual':mp.nstr(maxres,10)},'limits':'Exact controls corroborate the source/domain proof. High-precision numerical physical-billiard tests are diagnostics, not exact certificates of all periods.'},indent=2))
