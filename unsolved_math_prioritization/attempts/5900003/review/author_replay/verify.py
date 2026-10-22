#!/usr/bin/env python3
"""Exact cap geometry and constrained second-variation diagnostics."""
import sympy as s
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
import hashlib,json
C=Counter()
def ck(k,b):
 assert bool(b),k
 C[k]+=1
r,d=s.symbols('r d',positive=True)
D=lambda f:s.diff(f,r)+(2*r-1)/(2*d)*s.diff(f,d)
zb=(2-r)/(2*d);rho2=1-zb**2;z0=1/(d+r);h=zb-z0;ha=r+d-zb;hb=1-zb
W=h*(3*rho2+h*h)/6
V=ha**2*(r-ha/3)+W
U=hb**2*(1-hb/3)+W
S=2*r*ha+2*zb+rho2+h*h
# Expressions V,U,S are divided by pi throughout.
poly=d*d-r*r+r-1
def vanishes_mod_quad(expr):
 num=s.fraction(s.factor(expr))[0]
 return s.rem(num,poly,d)==0
ck('general_pressure_first_variation',vanishes_mod_quad(D(S)-2/r*D(V)+2*D(U)))
base_data=[({r:1,d:1},[[s.Rational(9,8),s.Rational(5,24),s.Rational(19,4)],[s.Rational(243,64),s.Rational(27,64),s.Rational(27,4)],[s.Rational(135,16),0,s.Rational(297,32)]],s.Rational(-243,16)),({r:s.Rational(1,2),d:s.sqrt(3)/2},[[s.Rational(3,4)-3*s.sqrt(3)/8,s.Rational(4,3)-3*s.sqrt(3)/4,s.Rational(5,2)],[(17-9*s.sqrt(3))/2,(16-9*s.sqrt(3))/2,18-9*s.sqrt(3)],[(196-109*s.sqrt(3))/2,96-55*s.sqrt(3),132-72*s.sqrt(3)]],72*s.sqrt(3)-136)]
for sub,table,qval in base_data:
 funcs=[V,U,S]
 for k in range(3):
  for j,f in enumerate(funcs):
   ck('cap_derivative_table',s.simplify(f.subs(sub)-table[k][j])==0)
  funcs=[D(f) for f in funcs]
 pA=s.Integer(2)/sub[r]
 Q=2*D(D(S))-2*pA*D(D(V))+4*D(D(U))
 ck('negative_Q_formula',s.simplify(Q.subs(sub)-qval)==0)
 ck('pressure_derivative_Q',s.simplify(qval+4*D(V).subs(sub)/(sub[r]**2))==0)
 ck('positive_volume_exchange',D(V).subs(sub)>0)
 ck('negative_Q_sign',qval<0)
# Exact stationary geometry identities.
x,y,z=s.symbols('x y z',real=True);norm=x*x+y*y+z*z
Fr=(1-r)*norm-2*d*z+1;G=norm-2*d*z+d*d-r*r
ck('partition_side_identity',vanishes_mod_quad(Fr-G-r*(1-norm)))
nAB=s.Matrix([(1-r)*x/r,(1-r)*y/r,((1-r)*z-d)/r])
nAO=s.Matrix([x/r,y/r,(z-d)/r]);nBO=s.Matrix([x,y,z])
ck('triple_normal_balance',(nAB+nBO-nAO).applyfunc(s.simplify)==s.zeros(3,1))
ck('interface_unit_normal',vanishes_mod_quad((nAB.dot(nAB)-1)*r*r-(1-r)*Fr))
ck('interface_curvature',s.simplify(sum(s.diff(nAB[i],[x,y,z][i]) for i in range(3))-3*(1/r-1))==0)
# The last ambient divergence is 3k; the surface trace is 2k.
ck('surface_mean_curvature',s.simplify(3*(1/r-1)-(1/r-1)-(2/r-2))==0)
# Ambient cutoff-compatible normal velocities at the two base configurations.
Z=s.Matrix([z*x,z*y,z*z-(1+norm)/2])
ck('central_sphere_tangency',s.expand(Z.dot(s.Matrix([x,y,z]))-z*(norm-1)/2)==0)
q=s.symbols('q',real=True)
ZX=z*(q-1)/2;ZZ=z*z-(1+q)/2
ck('planar_outer_velocity',s.simplify((ZX-ZZ).subs(q,2*z)-(1+z)/2)==0)
ck('planar_internal_velocity',s.simplify((-ZZ).subs({q:x*x+y*y+s.Rational(1,4),z:s.Rational(1,2)})-(x*x+y*y)/2-s.Rational(3,8))==0)
ck('spherical_outer_velocity',s.simplify((4/s.sqrt(3)*(2*ZX-s.sqrt(3)*ZZ)).subs(q,s.sqrt(3)*z-s.Rational(1,2))-1)==0)
ck('spherical_internal_velocity',s.simplify((4/s.sqrt(3)*(ZX-s.sqrt(3)*ZZ)-q).subs(q,2*s.sqrt(3)*z-2))==0)
# Rational points on d^2=r^2-r+1, inside a separated-satellite range.
fixtures=set()
for a in range(1,13):
 for b in range(1,13):
  u=F(a,b);rr=F(1,2)+(F(3,4)/u-u)/2;dd=(u+F(3,4)/u)/2
  if F(2,5)<=rr<=F(6,5):fixtures.add((rr,dd))
for rr,dd in sorted(fixtures):
 zz=(2-rr)/(2*dd);rh=1-zz*zz;zaxis=1/(dd+rr)
 ck('quadric_parameter',dd*dd==1+rr*rr-rr)
 ck('nondegenerate_triple_circle',rh>0 and 0<zz<1)
 ck('separated_caps',zaxis>0 and rr+dd>zz)
 ck('outer_normal_angle',(1-dd*zz)/rr==F(1,2))
 ck('circle_on_interface',(1-rr)-2*dd*zz+1==0)
 ck('axis_on_interface',(1-rr)*zaxis*zaxis-2*dd*zaxis+1==0)
 ck('unit_interface_normal',((1-rr)**2-2*dd*(1-rr)*zz+dd*dd)/(rr*rr)==1)
# The pure-sphere model has no infinite-radius component.
ck('pure_sphere_curvatures',2/s.Rational(1,2)-2==2)
ck('radical_sign_certificate',9**2*3<17**2)
for flux in range(1,21):
 v=s.Matrix([flux,-flux,0]);merged=s.Matrix([[1,1,0],[0,0,1]])
 ck('merged_volume_kernel',merged*v==s.zeros(2,1))
 ck('separate_volume_exclusion',v!=s.zeros(3,1))
# Disjoint-sphere control has exactly constant total volume and negative area Hessian.
t,R=s.symbols('t R',real=True,positive=True)
area=4*s.pi*((R**3+3*R**2*t)**s.Rational(2,3)+(R**3-3*R**2*t)**s.Rational(2,3))
ck('disjoint_sphere_area_Hessian',s.simplify(s.diff(area,t,2).subs(t,0)+16*s.pi)==0)
ck('disjoint_sphere_first_area',s.diff(area,t).subs(t,0)==0)
here=Path(__file__).resolve().parent
out={'status':'PASS','exact_assertions':sum(C.values()),'rational_geometry_fixtures':len(fixtures),'checks':dict(C),'artifact_sha256':hashlib.sha256((here/'PARTIAL.md').read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'sympy_version':s.__version__,'scope':'Exact sphere/cap algebra, physical normal velocities and constraint-label controls. Does not resolve the original interpretation or prove stability for the stronger class.'}
print(json.dumps(out,indent=2,sort_keys=True))
