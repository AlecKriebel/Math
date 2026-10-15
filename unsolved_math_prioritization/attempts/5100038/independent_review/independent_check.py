"""Independent exact checks for the frozen k610 proof.

Uses homogeneous line cross-products, rational centrally symmetric controls,
and direct dual-conic tangency. No imported author code or numerical roots.
"""
from fractions import Fraction as Q
from collections import Counter
import sympy as S
import json
C=Counter()
def check(x,key):
    assert x,key
    C[key]+=1
def eq(x,y,key):check(S.cancel(S.simplify(x-y))==0,key)
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def line(p,f):
    n=(p[0]-f[0],p[1]-f[1]);return (n[0],n[1],-n[0]*p[0]-n[1]*p[1])
def vertices(P,f):
    L=[line(p,f) for p in P];H=[cross(L[i],L[(i+1)%len(L)]) for i in range(len(L))]
    if any(h[2]==0 for h in H):return L,H,None
    V=[(h[0]/h[2],h[1]/h[2]) for h in H]
    return L,H,V
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def twicearea(V):return sum(det(V[i],V[(i+1)%len(V)]) for i in range(len(V)))
# Rational controls with arbitrary linear changes, translations of the focus,
# and primitive star traversal permutations. These are NOT billiard samples.
from math import gcd
for h in range(2,9):
 for seed in range(1,8):
  half=[]
  for j in range(h):
   t=Q(j+1,h+seed+1);u=(1-t*t)/(1+t*t);v=2*t/(1+t*t)
   half.append(((seed+1)*u+v,Q(2)*u+(seed+3)*v))
  P=half+[(-p[0],-p[1]) for p in half];n=len(P)
  for winding in range(1,n):
   if gcd(winding,n)!=1:continue
   poly=[P[(i*winding)%n] for i in range(n)]
   f=(Q(seed,41),Q(1,37));fm=(-f[0],-f[1])
   L,H,V=vertices(poly,f);Lm,Hm,Vm=vertices(poly,fm)
   check(V is not None and Vm is not None,'rational_finite_locus')
   for i,p in enumerate(poly):
    j=(i+h)%n
    check(poly[j]==(-p[0],-p[1]),'star_half_turn_order')
    check(Hm[j][2]==H[i][2],'determinant_locus_equivariance')
    check(Vm[j]==(-V[i][0],-V[i][1]),'homogeneous_intersection_equivariance')
    for k in (i,(i+1)%n):
     check(sum(L[k][d]*(*V[i],Q(1))[d] for d in range(3))==0,'intersection_line_incidence')
   check(twicearea(V)==twicearea(Vm),'signed_area_equivariance')
# Genuine axis-diamond billiards with rational a and c satisfying a^2-c^2=1.
for num in range(2,20):
 t=Q(num,1);a=(t*t+1)/(2*t);c=(t*t-1)/(2*t);R=a*a
 lam=R/(R+1);A=R-lam;B=1-lam
 P=[(a,Q(0)),(Q(0),Q(1)),(-a,Q(0)),(Q(0),-Q(1))]
 contacts=[]
 check(A>0 and B>0 and 0<lam<1,'strict_elliptic_caustic')
 check(A-B==c*c,'confocality')
 for i,p in enumerate(P):
  q=P[(i+1)%4];l=cross((*p,Q(1)),(*q,Q(1)))
  check(A*l[0]**2+B*l[1]**2==l[2]**2,'dual_conic_side_tangency')
  r=(-A*l[0]/l[2],-B*l[1]/l[2]);contacts.append(r)
  check(r[0]**2/A+r[1]**2/B==1,'contact_on_caustic')
  check(sum(l[d]*(*r,Q(1))[d] for d in range(3))==0,'contact_on_orbit_side')
  prev=P[(i-1)%4];incoming=(p[0]-prev[0],p[1]-prev[1]);outgoing=(q[0]-p[0],q[1]-p[1])
  normal=(p[0]/R,p[1]);nn=normal[0]**2+normal[1]**2;dn=sum(incoming[d]*normal[d] for d in range(2))
  # All diamond side lengths coincide, so unnormalised vectors suffice.
  check(tuple(incoming[d]-2*dn*normal[d]/nn for d in range(2))==outgoing,'exact_specular_reflection')
 L,H,V=vertices(contacts,(c,Q(0)));Lm,Hm,Vm=vertices(contacts,(-c,Q(0)))
 check(V is not None and Vm is not None,'diamond_finite_intersections')
 check(twicearea(V)==twicearea(Vm),'genuine_four_billiard_area_equality')
 x=a**3/(R+1);y=1/(R+1)
 check(contacts==[(x,y),(-x,y),(-x,-y),(x,-y)],'actual_contact_rectangle')
 check(twicearea(V)==4*x*(x*x+y*y-c*c)**2/(y*(x*x-c*c)),'direct_rectangle_area_formula')
# Derive the normal chord parameter, eliminating cos^2+sin^2=1.
u,v,A,B=S.symbols('u v A B',real=True)
# line normal (-a sin,b cos), h=-(A-B)sin cos, after multiplying by ab.
normal_norm=A*u+B*v
numerator=A*A*u+B*B*v-(A-B)**2*u*v
eq((numerator-normal_norm**2).subs(v,1-u),0,'normal_chord_parameter_identity')
# At R=2 solve every line with exact radicals, including the opposite focus.
a=S.sqrt(2);c=S.Integer(1);x=2*a/3;y=S.Rational(1,3)
P=[(x,y),(-x,y),(-x,-y),(x,-y)]
for f in [(c,0),(-c,0)]:
 L,H,V=vertices(P,f)
 check(V is not None,'collapse_unique_intersections')
 for h,z in zip(H,V):
  check(S.simplify(h[2])!=0,'collapse_nonzero_determinant')
  eq(z[0],-f[0],'collapse_opposite_focus_x');eq(z[1],0,'collapse_opposite_focus_y')
 eq(twicearea(V),0,'collapse_area_zero')
# Golden ratio: use exact R algebra and explicit two horizontal lines.
R=(1+S.sqrt(5))/2;a=S.sqrt(R);c=S.sqrt(R-1);x=a**3/(R+1);y=1/(R+1)
eq(x*x,c*c,'golden_contact_focus_abscissa_squared')
check(x>0 and c>0,'golden_positive_abscissae')
eq((R/(R+1))*(R+1),R,'golden_caustic_parameter')
check(0<R/(R+1)<1,'golden_strict_caustic')
L1=line((c,y),(c,0));L2=line((c,-y),(c,0));H=cross(L1,L2)
eq(H[2],0,'parallel_lines_no_finite_meet')
check(S.simplify(H[0])!=0,'parallel_lines_are_distinct')
eq(-L1[2]/L1[1],y,'upper_parallel_height');eq(-L2[2]/L2[1],-y,'lower_parallel_height')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),'sympy_version':S.__version__,'scope':'Independent finite algebra and exact genuine four-billiard domain certificates; source and universal geometry reviewed separately.'},indent=2,sort_keys=True))
