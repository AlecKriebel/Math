#!/usr/bin/env python3
"""Independent exact controls; no author code imported."""
from fractions import Fraction as F
from collections import Counter
from math import gcd
import random,json,sympy as s
C=Counter()
def ck(b,k):assert b,k;C[k]+=1
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def cross3(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def ar(ps):return sum(det(ps[j],ps[(j+1)%len(ps)]) for j in range(len(ps)))/2
def ant_line(p):return (p[0],p[1],-dot(p,p))
def intersection(l,m):
 q=cross3(l,m);return (q[0]/q[2],q[1]/q[2])
def edge(p,q):
 A=dot(p,p);B=dot(q,q);D=dot(p,q)
 return (2*A*B-(A+B)*D)/(2*det(p,q))
def side(p,q):return cross3((p[0],p[1],1),(q[0],q[1],1))
def foot(l):return (-l[2]*l[0]/(l[0]**2+l[1]**2),-l[2]*l[1]/(l[0]**2+l[1]**2))
rng=random.Random(4032026);done=0
while done<240:
 n=rng.randrange(3,11);ps=[(F(rng.randrange(-12,13),rng.randrange(1,6)),F(rng.randrange(-12,13),rng.randrange(1,6))) for _ in range(n)]
 if any(det(ps[j],ps[(j+1)%n])==0 for j in range(n)):continue
 rs=[]
 for j,p in enumerate(ps):
  q=ps[(j+1)%n];l,m=ant_line(p),ant_line(q);r=intersection(l,m);rs.append(r)
  ck(l[0]*r[0]+l[1]*r[1]+l[2]==0,'specific_first_antipedal_line')
  ck(m[0]*r[0]+m[1]*r[1]+m[2]==0,'specific_second_antipedal_line')
  L=side(p,q);Q=foot(L)
  ck(L[0]*Q[0]+L[1]*Q[1]+L[2]==0,'specific_original_side_foot_incidence')
  ck(dot(Q,(q[0]-p[0],q[1]-p[1]))==0,'foot_perpendicular_to_side')
 ck(ar(rs)==sum(edge(ps[j],ps[(j+1)%n]) for j in range(n)),'signed_area_vs_homogeneous_intersections')
 ck(ar(rs)==-ar(rs[::-1]),'orientation_reversal')
 done+=1
x,y,u,v=s.symbols('x y u v');A=x*x+y*y;B=u*u+v*v;D=x*u+y*v
ck(s.expand(A*B-(A+B)*D/2-((A+B)*((x-u)**2+(y-v)**2)-(A-B)**2)/4)==0,'removable_numerator_identity')
# Leading local divisor coefficients obtained from the p-shift formulas.
a,b,k,sp,cp,dp,kp=s.symbols('a b k sp cp dp kp',nonzero=True)
Dprime=s.simplify(-2*k*k*sp*sp*(1/(k*sp))*(-s.I*dp/(k*sp))*(-s.I*cp/sp))
ck(Dprime==2*cp*dp/sp,'simple_D_root_derivative')
ck(s.simplify(2*a*b*sp*cp*(-s.I*cp/sp)/Dprime)==-s.I*a*b*sp*cp/dp,'B_residue_at_shifted_pole')
# Exact direct four-orbit geometry, reconstructed independently from source objects.
aa=s.sqrt(5);bb=s.sqrt(3);al=5/s.sqrt(8);be=3/s.sqrt(8)
products=[]
for ps in [[(aa,0),(0,bb),(-aa,0),(0,-bb)],[(al,be),(-al,be),(-al,-be),(al,-be)]]:
 Qs=[];Rs=[]
 for j,p in enumerate(ps):
  q=ps[(j+1)%4];L=side(p,q)
  ck(s.simplify(p[0]**2/5+p[1]**2/3-1)==0,'four_orbit_outer_ellipse')
  ck(s.simplify(L[0]**2*al**2+L[1]**2*be**2-L[2]**2)==0,'four_orbit_exact_same_caustic')
  Qs.append(foot(L));Rs.append(intersection(ant_line(p),ant_line(q)))
  for R,pt in [(Rs[-1],p),(Rs[-1],q)]:ck(s.simplify(dot(pt,R)-dot(pt,pt))==0,'four_orbit_named_antipedal_line')
 products.append(s.simplify(ar(Qs)*ar(Rs)))
ck(products==[s.Rational(225,4),s.Rational(289,4)],'even_products_from_direct_geometry')
ck(products[0]!=products[1],'all_parity_extension_false')
# Primitive odd quotient arithmetic, including every star winding tested.
for N in range(3,122,2):
 ell=F(2,N)
 for t in range(1,N//2+1):
  if gcd(t,N)!=1:continue
  vv=F(2*t,N);dd=2*vv;orbit=[j*dd%2 for j in range(N)]
  ck(len(set(orbit))==N,'unique_vertex_pole_index')
  ck(set(orbit)=={j*ell for j in range(N)},'minimal_quotient_lattice')
  ck(all((-vv-j*dd)%ell==0 for j in range(N)),'opposite_midpoint_poles_join_vertex_classes')
  ck((1+vv)%ell==ell/2,'pedal_shift_exact_half_period')
  ck(sum((vv+j*dd)%2==0 for j in range(N))==1,'exactly_one_opposite_edge_at_vertex_class')
  ck(sum((1-vv-j*dd)%ell==ell/2 for j in range(N))==N,'coincident_endpoint_class_is_other_real_half')
ck(F(1,2)%1==F(1,2),'even_four_midpoint_class_distinct')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'categories':dict(C),'rational_polygons':done,'even_products':[str(p) for p in products],'scope':'Finite exact controls; the full analytic argument is audited in INDEPENDENT_REVIEW.md.'},indent=2))
