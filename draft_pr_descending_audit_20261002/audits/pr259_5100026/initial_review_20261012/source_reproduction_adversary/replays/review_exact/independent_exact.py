#!/usr/bin/env python3
"""Independent homogeneous-line and rational-geometry controls for k407."""
from fractions import Fraction as F
from itertools import product
from collections import Counter
from math import gcd
import sympy as s
import json
C=Counter()
def ck(p,k):
 C[k]+=1
 if not p:raise AssertionError(k)
def dot(x,y):return x[0]*y[0]+x[1]*y[1]
def sub(x,y):return (x[0]-y[0],x[1]-y[1])
def neg(x):return(-x[0],-x[1])
def det(x,y):return x[0]*y[1]-x[1]*y[0]
def cross(x,y):return(x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0])
def line(P,M):
 q=sub(P,M);return(q[0],q[1],-dot(P,q))
def inter(P,Q,M):
 z=cross(line(P,M),line(Q,M));assert z[2];return(z[0]/z[2],z[1]/z[2])
# Direct homogeneous construction, symmetry and similarity covariance.
for a,b,c,d in product(range(-2,3),repeat=4):
 P=(F(a),F(b));Q=(F(c),F(d));M=(F(2,7),F(-3,11))
 if not det(sub(P,M),sub(Q,M)):continue
 U=inter(P,Q,M)
 ck(dot(sub(P,M),sub(U,P))==0,'first_actual_line_incidence')
 ck(dot(sub(Q,M),sub(U,Q))==0,'second_actual_line_incidence')
 ck(U==inter(Q,P,M),'unordered_endpoint_symmetry')
 ck(inter(neg(P),neg(Q),neg(M))==neg(U),'central_reflection_equivariance')
 scale=F(7,3);shift=(F(4,5),F(2,9))
 tr=lambda Z:(scale*Z[0]+shift[0],scale*Z[1]+shift[1])
 ck(inter(tr(P),tr(Q),tr(M))==tr(U),'similarity_covariance')
# Universal symbolic residue from homogeneous lines, rather than the author's V function.
z=s.symbols('z');lx,ly,ax,ay,qx,qy,mx,my=s.symbols('lx ly ax ay qx qy mx my')
L=(lx,ly);A=(ax,ay);Q=(qx,qy);M=(mx,my)
# This is z^2 times the line through L/z+A, perpendicular to L/z+A-M.
pl=(z*lx+z*z*(ax-mx),z*ly+z*z*(ay-my),-dot(L,L)-z*dot(L,(2*ax-mx,2*ay-my))-z*z*dot(A,sub(A,M)))
reg=line(Q,M);hom=cross(pl,reg)
wx=s.expand(hom[2]).coeff(z,1)
res=tuple(s.cancel(hom[i].subs(z,0)/wx) for i in (0,1))
ck(s.factor(wx-det(L,sub(Q,M)))==0,'leading_projective_denominator')
ck(s.cancel(dot(L,res)-dot(L,L))==0,'symbolic_residue_pole_equation')
ck(s.cancel(dot(sub(Q,M),res))==0,'symbolic_residue_neighbor_equation')
# Build all four incident residues from independent homogeneous coefficient extraction.
def residue(l,q,m):
 den=det(l,sub(q,m));h=cross((0,0,-dot(l,l)),line(q,m))
 return(h[0]/den,h[1]/den)
res4=[residue(L,Q,M),residue(L,neg(Q),M),residue(neg(L),Q,M),residue(neg(L),neg(Q),M)]
for j in (0,1):ck(s.cancel(sum(x[j] for x in res4))==0,'symbolic_four_edge_cancellation')
# Include isotropic complex leading vectors explicitly.
for Q0 in [(s.Rational(2),s.Rational(3)),(s.Rational(-1,2),s.Rational(7,3))]:
 for M0 in [(s.Rational(1,3),0),(0,s.Rational(1,5))]:
  rr=residue((1,s.I),Q0,M0)
  for z0 in rr:ck(s.simplify(z0)==0,'isotropic_residue_zero_control')
# Rational rectangles that really circumscribe ellipses having the chosen focal point.
vals=[F(2,3),F(3,4),F(4,3),F(3,2),F(2),F(5,2)]
for r,t,beta in product(vals,vals,(F(1),F(2),F(3))):
 h=beta*(r+1/r)/2;m=beta*(r-1/r)/2
 l=beta*(t+1/t)/2;n=beta*(t-1/t)/2;M=(m,n)
 ck(h*h-m*m==l*l-n*n==beta*beta,'ellipse_support_identity')
 R=[(h,l),(-h,l),(-h,-l),(h,-l)]
 U=[inter(R[j],R[(j+1)%4],M) for j in range(4)]
 for j in (0,1):ck(sum(z[j] for z in U)==0,'actual_rectangle_centroid_origin')
 # Original tangent contacts on Q=beta^2 I+M M^T, in CCW order.
 P=[(h,m*n/h),(m*n/l,l),(-h,-m*n/h),(-m*n/l,-l)]
 Q11=beta*beta+m*m;Q22=beta*beta+n*n;Q12=m*n;Delta=Q11*Q22-Q12*Q12
 for j,(x,y) in enumerate(P):
  ck((Q22*x*x-2*Q12*x*y+Q11*y*y)/Delta==1,'original_ellipse_contact')
  normal=((Q22*x-Q12*y)/Delta,(-Q12*x+Q11*y)/Delta)
  incoming=sub(P[j],P[(j-1)%4]);outgoing=sub(P[(j+1)%4],P[j])
  dn=dot(incoming,normal)/dot(normal,normal)
  reflected=(incoming[0]-2*dn*normal[0],incoming[1]-2*dn*normal[1])
  ck(det(reflected,outgoing)==0 and dot(reflected,outgoing)>0,'genuine_four_orbit_reflection')
  ck(dot(normal,R[(j-1)%4])==dot(normal,R[j])==1,'two_named_outer_tangent_incidences')
# Generic point cannot be silently substituted for a focus.
R=[(F(2),F(3)),(F(-2),F(3)),(F(-2),F(-3)),(F(2),F(-3))];M=(F(1,2),F(1,3))
U=[inter(R[i],R[(i+1)%4],M) for i in range(4)]
ck(any(sum(x[j] for x in U)!=0 for j in (0,1)),'nonfocal_rectangle_negative_control')
# Exact cyclic pole multiplicities, translated to every vertex slot on selected primitive orbits.
for N in range(6,102,2):
 for tau in range(1,N//2):
  if gcd(N,tau)>1:continue
  positions=[F(4*tau*j,N)%4 for j in range(N)]
  for anchor in (0,1,N//2):
   pole=[j for j in range(N) if (positions[j]-positions[anchor])%2==0]
   ck(len(pole)==2,'two_antipodal_pole_slots')
   ck((pole[1]-pole[0])%N==N//2,'pole_slot_separation')
   edges=[e for j in pole for e in ((j-1)%N,j)]
   ck(len(set(edges))==4,'four_distinct_edges')
   for j in pole:ck((positions[(j+1)%N]+positions[(j-1)%N]-2*positions[j])%4==0,'neighbor_phase_reflection')
  ck(F(2*tau,N)!=F(1,2),'no_quarter_period_overlap')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(C),'scope':'Exact homogeneous-line identities, rational genuine N4 ellipses/contacts/reflection and bounded integer pole bookkeeping; not a substitute for the complete meromorphic proof.'},indent=2,sort_keys=True))
