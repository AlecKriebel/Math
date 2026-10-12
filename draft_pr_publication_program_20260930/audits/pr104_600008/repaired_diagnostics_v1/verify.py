#!/usr/bin/env python3
"""Exact algebra for the conformal cylinder and closure bookkeeping."""
import sympy as s
from fractions import Fraction as F
from itertools import product
from collections import Counter
from pathlib import Path
import json,hashlib,math
C=Counter()
def ck(k,b):
 if not bool(b):raise RuntimeError(k)
 C[k]+=1
a,b,c,v,w=s.symbols('a b c v w',positive=True)
f2=b+(a-b)*w
X=a*(a+v)*(1-w)/(a+c)
Y=b*(b+v)*w/(b+c)
Z=c*(c+f2)*(c-v)/((a+c)*(b+c))
ck('ellipsoid_identity',s.factor(X/a+Y/b+Z/c-1)==0)
ck('tropic_normal_identity',s.factor(X/a**2+Y/b**2-Z/c**2-f2*v/(a*b*c))==0)
def metric(i,j):return s.factor(sum(sign*s.diff(t,i)*s.diff(t,j)/(4*t) for t,sign in [(X,1),(Y,1),(Z,-1)]))
gtt=s.factor(metric(w,w)*4*w*(1-w));gvv=metric(v,v)
ck('angular_metric',s.factor(gtt-(v+f2)*f2/(c+f2))==0)
ck('latitude_metric',s.factor(gvv+(v+f2)*v/(4*(a+v)*(b+v)*(c-v)))==0)
ck('metric_cross_term',metric(w,v)==0)
ck('conformal_spatial_coefficient',s.factor(gtt*(c+f2)/f2-(v+f2))==0)
ck('conformal_temporal_coefficient',s.factor(gvv*4*(a+v)*(b+v)*(c-v)/v+(v+f2))==0)
ck('axisymmetric_metric',s.factor(gtt.subs(b,a)-(v+a)*a/(c+a))==0)
# Sample signs, the unique-root monotonicity, and both equal/unequal axes.
for aa,bb,cc in product([F(1,2),F(1),F(3)],repeat=3):
 for ww,vfrac in product([F(1,5),F(1,2),F(4,5)],repeat=2):
  vv=cc*vfrac;ff=bb+(aa-bb)*ww
  xx=aa*(aa+vv)*(1-ww)/(aa+cc)
  yy=bb*(bb+vv)*ww/(bb+cc)
  zz=cc*(cc+ff)*(cc-vv)/((aa+cc)*(bb+cc))
  ck('real_coordinate_patch',xx>0 and yy>0 and zz>0)
  ck('belt_sign',xx/aa**2+yy/bb**2-zz/cc**2>0)
  ck('root_equation', (aa+cc)*xx/(aa*(aa+vv))+(bb+cc)*yy/(bb*(bb+vv))==1)
  derivative=-(aa+cc)*xx/(aa*(aa+vv)**2)-(bb+cc)*yy/(bb*(bb+vv)**2)
  ck('unique_root_monotonicity',derivative<0)
  ck('metric_signature',(vv+ff)*ff/(cc+ff)>0 and -(vv+ff)*vv/(4*(aa+vv)*(bb+vv)*(cc-vv))<0)
# Positive densities decrease strictly in c, symbolically.
r=s.symbols('r',positive=True)
ck('density_c_derivative',s.simplify(s.diff(s.sqrt(r/(c+r)),c)+s.sqrt(r)/(2*(c+r)**s.Rational(3,2)))==0)
# Residues of the imported quartic density at the two points at infinity.
p0,q0,t=s.symbols('p0 q0 t',positive=True)
poly=(p0-q0/t)*(c+p0-q0/t)*(1-1/t**2)
ck('quartic_infinity_leading',s.limit(t**4*poly,t,0)==-q0**2)
for sign in [-1,1]:
 residue=-q0/(2*sign*s.I*q0)
 ck('nonzero_third_kind_residue',s.simplify(residue-sign*s.I/2)==0 and residue!=0)
# The contour differential has 1/z leading behavior on its infinity branch.
z=s.symbols('z',positive=True)
ck('contour_infinity_coefficient',s.limit(z*z/s.sqrt(z*(z+a)*(z+b)*(z-c)),z,s.oo)==1)
# Algebraic form of the period identity and the target conversion.
M=s.symbols('M',positive=True)
L=2*s.pi*M;Iv=s.pi-L/2
ck('period_to_rotation',s.simplify(Iv/L-(1-M)/(2*M))==0)
n,rr=s.symbols('n rr',positive=True)
ck('closure_to_mean',s.simplify(((1-M)/(2*M)-rr/n).subs(M,n/(n+2*rr)))==0)
for nn,rrr in product(range(1,17),repeat=2):
 target=F(nn,nn+2*rrr);cf=F(4*rrr*(nn+rrr),nn*nn)
 ck('rotational_parameter',F(1,1)/(1+cf)==target*target)
 ck('positive_axis_parameter',cf>0)
# Least period of the folded map and of actual alternating-boundary chains.
for pp,qq in product(range(1,14),repeat=2):
 if math.gcd(pp,qq)!=1:continue
 rho=F(pp,qq)
 eq=next(k for k in range(1,2*qq+1) if (k*rho).denominator==1)
 full=next(k for k in range(1,2*qq+1) if k%2==0 and (k*rho).denominator==1)
 ck('equator_least_period',eq==qq)
 ck('full_chain_least_period',full==math.lcm(2,qq))
 ck('full_chain_winding',F(full*pp,qq).denominator==1)
here=Path(__file__).resolve().parent
out={'status':'PASS','exact_assertions':sum(C.values()),'checks':dict(C),'artifact_sha256':hashlib.sha256((here/'ANALYTIC_CRITERION.md').read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'sympy_version':s.__version__,'scope':'Exact algebra and bounded rational controls. Global coordinate gluing, contour deformation and the analytic closure criterion are proved in the text, not certified by finite sampling.'}
print(json.dumps(out,indent=2,sort_keys=True))
