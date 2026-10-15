"""Independent exact controls: solve the actual lines, not author incidence tests."""
import sympy as s
from collections import Counter
from fractions import Fraction
from math import gcd
import json
C=Counter()
def ck(v,key):
 assert v,key
 C[key]+=1
k,h,S,c,d,Y,D,kp=s.symbols('k h S c d Y D kp')
L=1-k*k*h*h*S*S
P=[]
for sign in (-1,1):
 sn=(S*c*d+sign*h*Y*D)/L;cn=(Y*c-sign*S*h*D*d)/L
 P.append(s.Matrix([-d*sn/c,kp*cn/c]))
# Independent midpoint/half-edge solve. Subtracting the two source equations
# gives E dot R=(2M-F) dot E; adding gives (M-F) dot R=M²+E²-F dot M.
mid=(P[0]+P[1])/2;half=(P[1]-P[0])/2;focus=s.Matrix([k,0])
rows=s.Matrix([list(mid-focus),list(half)])
rhs=s.Matrix([mid.dot(mid)+half.dot(half)-focus.dot(mid),(2*mid-focus).dot(half)])
det=rows.det();rx=(rhs[0]*rows[1,1]-rows[0,1]*rhs[1])/det;ry=(rows[0,0]*rhs[1]-rhs[0]*rows[1,0])/det
G=s.groebner([kp**2+k**2-1,c**2+h**2-1,d**2+k**2*h**2-1,Y**2+S**2-1,D**2+k**2*S**2-1],D,Y,d,c,kp,S,h,k,order='lex')
def zero(expr,key):
 num=s.fraction(s.together(expr))[0]
 ck(G.reduce(s.expand(num))[1]==0,key)
H=1-2*k*k*h*h+k*k*h**4
expected=s.Matrix([-(H*S+k*(c*c-d*d*S*S))/(c*c*L),Y*(2*kp*kp-H*(1+k*S))/(kp*c*c*L)])
zero(rx-expected[0],'midpoint_solve_recovers_antipedal_x')
zero(ry-expected[1],'midpoint_solve_recovers_antipedal_y')
# Direct chord projection, distinct from starting with the known caustic line.
edge=P[1]-P[0];foot=P[0]+(focus-P[0]).dot(edge)/edge.dot(edge)*edge
zero(foot[0]-(k-S)/(1-k*S),'actual_chord_projection_recovers_pedal_x')
zero(foot[1]-kp*Y/(1-k*S),'actual_chord_projection_recovers_pedal_y')
normal_det=(P[0][0]-k)*P[1][1]-P[0][1]*(P[1][0]-k)
zero(normal_det-2*kp*h*d*D*(1+k*S)/(c*L),'normal_determinant_finiteness_formula')
# The possible roots are simple in the strict parameter domain: the square
# of the sn derivative there has neither factor zero.
ck(s.factor((1-S*S).subs(S,1/(k*h))-(h*h*k*k-1)/(h*h*k*k))==0,'first_pole_derivative_factor')
ck(s.factor((1-k*k*S*S).subs(S,1/(k*h))-(h*h-1)/(h*h))==0,'second_pole_derivative_factor')
ck(s.factor(L.subs(S,-1/k)-(1-h*h))==0,'cancelled_extra_focus_root_regular')
# Parity forces the even Laurent coefficient to vanish, independently of N4 incidence.
a2,a1,a0,z=s.symbols('a2 a1 a0 z');f=a2/z**2+a1/z+a0
ck(s.expand((f+f.subs(z,-z))*z*z)==2*a2+2*a0*z*z,'odd_germ_excludes_double_pole')
# The incident pedal terms: even double-pole germ times odd holomorphic difference.
A,B,U,V=s.symbols('A B U V')
ck(s.expand((A/z**2+B)*(U*z+V*z**3)).coeff(z,-2)==0,'even_pedal_germ_odd_neighbor_difference')
# Generic aspect-ratio N4 controls from actual line systems.
a,b,f,r=s.symbols('a b f r',nonzero=True)
G4=s.groebner([f*f-a*a+b*b,r*r-a*a-b*b],f,r,a,b,order='lex')
def clean4(expr):return G4.reduce(s.expand(s.fraction(s.together(expr))[0]))[1]
def det2(x,y):return x[0]*y[1]-x[1]*y[0]
def polyarea(Q):return sum(det2(Q[i],Q[(i+1)%len(Q)]) for i in range(len(Q)))/2
orbits=[[(0,b),(-a,0),(0,-b),(a,0)],[(a*a/r,b*b/r),(-a*a/r,b*b/r),(-a*a/r,-b*b/r),(a*a/r,-b*b/r)]]
for idx,raw in enumerate(orbits):
 for sign in (1,-1):
  P=[s.Matrix(x) for x in raw];F=s.Matrix([sign*f,0]);Q=[];R=[]
  for i,p in enumerate(P):
   q=P[(i+1)%4];edge=q-p;foot=p+(F-p).dot(edge)/edge.dot(edge)*edge;Q.append(foot)
   n=p-F;v=q-F;hh=n.dot(p);gg=v.dot(q);den=det2(n,v)
   R.append(s.Matrix([(hh*v[1]-gg*n[1])/den,(n[0]*gg-v[0]*hh)/den]))
   cn=s.Matrix([-edge[1],edge[0]]);cc=cn.dot(p)
   ck(clean4(a**4*cn[0]**2/r**2+b**4*cn[1]**2/r**2-cc**2)==0,'generic_N4_same_caustic_tangency')
   ck(clean4(p[0]**2/a**2+p[1]**2/b**2-1)==0,'generic_N4_original_ellipse')
  AP=s.factor(polyarea(Q));AB=s.factor(polyarea(R))
  expectedP=4*a**3*b**3/(a*a+b*b)**2 if idx==0 else 2*a*a*b*b/(a*a+b*b)
  expectedB=4*a*b if idx==0 else 8*a*a*b*b/(a*a+b*b)
  ck(clean4(AP-expectedP)==0,'generic_N4_direct_pedal_area')
  ck(clean4(AB-expectedB)==0,'generic_N4_direct_antipedal_area')
  ck(clean4(AP*AB-16*a**4*b**4/(a*a+b*b)**2)==0,'generic_N4_focal_product_all_aspects')
# Exact reduced pole and zero locations, with all cyclic indices present.
periods=0
for N in range(4,205,4):
 m=N//2
 for tau in range(1,m):
  if gcd(N,tau)!=1:continue
  periods+=1;step=Fraction(tau,m);hp=Fraction(1,m)
  ck({j*step%1 for j in range(N)}=={Fraction(j,m) for j in range(m)},'full_real_reduced_period')
  ck(sum(j*step%1==0 for j in range(N))==2,'two_equal_trace_residues')
  ck(((Fraction(1,2)+step/2)/hp)%1==Fraction(1,2),'correct_contact_to_vertex_half_shift')
  allowed={(-j*step)%1 for j in range(N)}
  poles={((Fraction(sign,2)*step-step/2)-j*step)%1 for sign in (-1,1) for j in range(N)}
  ck(poles==allowed,'complete_antipedal_area_pole_classes')
  # Zero translates by half hp are disjoint from poles; translating twice returns.
  zeros={(u+hp/2)%1 for u in allowed}
  ck(not zeros&allowed,'trace_zero_classes_not_poles')
  ck({(u+hp/2)%1 for u in zeros}==allowed,'product_divisors_exactly_cancel')
  if N==4:ck(len({0,m-1,m,N-1})==N,'N4_all_singular_vertices_included')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(sorted(C.items())),'primitive_period_controls':periods,'limits':'Symbolic direct line geometry, generic N4 checks and exact lattice controls. The independent written review audits the full meromorphic proof, real domain and source scope.'},indent=2,sort_keys=True))
