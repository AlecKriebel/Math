#!/usr/bin/env python3
"""Locally authored exact controls plus separately identified numerical diagnostics."""
from fractions import Fraction as F
from collections import Counter
from math import gcd
from pathlib import Path
import hashlib,json
counts=Counter()
def ck(label,test):
    assert test,label
    counts[label]+=1
# General polynomial identities are also expanded symbolically, not sampled.
import sympy as sy
t,z,S=sy.symbols('t kappa S')
q=1-t; U=1-2*z*t+z*t*t; V=1-2*t+z*t*t
ck('universal_U_plus_V',sy.expand(U+V-2*q*(1-z*t))==0)
ck('universal_distance_factorization',sy.expand((U+z*V*S)**2-4*z*(1-z*t)**2*q*q*S-(1-z*S)*(U*U-z*V*V*S))==0)
ck('universal_outer_axis_difference',sy.expand((1-z*t)**2-(1-z)-z*V)==0)
ck('universal_outer_norm_constant',sy.expand(1-z+z*q*q-U)==0)
# Exact rational sanity checks independently instantiate the raw geometry.
for kk in [F(1,25),F(1,4),F(9,16),F(81,100)]:
 for tt in [F(1,17),F(1,4),F(1,2),F(4,5),F(99,100)]:
  qq=1-tt; UU=1-2*kk*tt+kk*tt*tt; VV=1-2*tt+kk*tt*tt; WW=1-kk*tt*tt
  ck('factor_constants_positive',qq>0 and UU>0 and WW>0)
  Ao2=(1-kk*tt)**2/qq**2; Bo2=(1-kk)/qq**2
  for ss in [F(0),F(1,9),F(1,2),F(8,9),F(1)]:
   raw=((Ao2-Bo2)*ss+Bo2+kk)**2-4*kk*Ao2*ss
   fact=(1-kk*ss)*(UU*UU-kk*VV*VV*ss)/qq**4
   ck('raw_distance_factorization',raw==fact)
   ck('paired_distance_positive',raw>0)
   ck('outer_strictly_exterior',(1-kk*tt*ss)/qq>1)
   # Second factor at real u has lower bound k'^2 after normalizing by WW^2.
   cnD=VV/WW;dnD=UU/WW
   ck('real_second_factor_positive',dnD*dnD-kk*cnD*cnD*ss>=1-kk)
# Normalize the torus real period 2K to 1. delta=tau/m and K=1/2.
rotations=0
for N in range(4,405,4):
 n=N//4;m=N//2
 for tau in range(1,N//2):
  if gcd(tau,N)!=1:continue
  rotations+=1;delta=F(tau,m)
  orbit=[(-j*delta)%1 for j in range(m)]
  ck('primitive_translation_order',len(set(orbit))==m)
  ck('half_period_belongs_to_orbit',(n*delta-F(1,2))%1==0)
  ck('antipodal_real_half_orbit',(m*delta)%2==1)
  if N==4:
   ck('N4_only_exception',delta==F(1,2))
   poles=Counter({x:2 for x in orbit})
   zeros=Counter()
   for j in range(m):zeros[(F(1,2)-j*delta)%1]+=2
  else:
   ck('generic_not_quarter_period',delta!=F(1,2))
   basic=[F(1,2)%1,(F(1,2)+delta)%1,(F(1,2)-delta)%1]
   ck('distinct_zero_locations',len(set(basic))==3 and 0 not in basic)
   poles=Counter({x:4 for x in orbit});zeros=Counter()
   for j in range(m):
    zeros[(F(1,2)-j*delta)%1]+=2
    zeros[(F(1,2)+delta-j*delta)%1]+=1
    zeros[(F(1,2)-delta-j*delta)%1]+=1
  ck('cyclic_norm_divisor_cancels',zeros==poles)
# Wrong-parity controls ensure the proof does not silently extend to k114.
for N in [6,10,14,18,22,26]:
 m=N//2;delta=F(1,m)
 poles=Counter({(-j*delta)%1:4 for j in range(m)});zeros=Counter()
 for j in range(m):
  for shift,mult in [(F(1,2),2),(F(1,2)+delta,1),(F(1,2)-delta,1)]:zeros[(shift-j*delta)%1]+=mult
 ck('wrong_parity_divisor_rejected',poles!=zeros)
# Numerical checks are deliberately separate and do not certify the theorem.
import mpmath as mp
mp.mp.dps=85
numeric=0;maxerr=mp.mpf(0)
def num(label,error):
 global numeric,maxerr
 assert error<mp.mpf('1e-65'),(label,mp.nstr(error,8))
 numeric+=1;maxerr=max(maxerr,error)
for k in [mp.mpf('0.2'),mp.mpf('0.5'),mp.mpf('0.8')]:
 par=k*k;K=mp.ellipk(par);Kp=mp.ellipk(1-par)
 sn=lambda u:mp.ellipfun('sn',u,par)
 cn=lambda u:mp.ellipfun('cn',u,par)
 dn=lambda u:mp.ellipfun('dn',u,par)
 for N in [4,8,12,16,20]:
  for tau in range(1,N//2):
   if gcd(tau,N)!=1:continue
   v=2*K*tau/N;delta=2*v
   a=dn(v)/cn(v);b=mp.sqrt(1-par)/cn(v)
   Ao=a*dn(v)/cn(v);Bo=b/cn(v)
   point=lambda u:(-a*sn(u),b*cn(u))
   outer=lambda u:(-Ao*sn(u),Bo*cn(u))
   def product(u,focus=1):
    return mp.fprod(mp.sqrt((outer(u+j*delta)[0]-focus*k)**2+outer(u+j*delta)[1]**2) for j in range(N))
   ref=product(0)
   for u in [K/11,K/3,7*K/5]:
    val=product(u)
    num('full_ordinary_product',abs(val/ref-1))
    num('other_focus_equal',abs(product(u,-1)/ref-1))
    X,Y=outer(u)
    for w in [u-v,u+v]:num('both_tangent_equations',abs(-X*sn(w)/a+Y*cn(w)/b-1))
    p0=point(u-v);p1=point(u+v)
    det=p0[0]*p1[1]-p1[0]*p0[1]
    # Solve x*x_i/a^2+y*y_i/b^2=1 directly from actual vertex coordinates.
    xx=a*a*(p1[1]-p0[1])/det;yy=b*b*(p0[0]-p1[0])/det
    num('direct_intersection_x',abs(xx-X)/max(1,abs(X)))
    num('direct_intersection_y',abs(yy-Y)/max(1,abs(Y)))
root=Path(__file__).resolve().parent
res={'status':'PASS','proof_sha256':hashlib.sha256((root/'PROOF.md').read_bytes()).hexdigest(),'exact_assertions':sum(counts.values()),'exact_categories':dict(counts),'primitive_rotation_cases':rotations,'numerical_diagnostics':numeric,'numerical_precision_digits':85,'maximum_relative_or_scaled_error':mp.nstr(maxerr,10),'scope':'Exact algebra/lattice controls and separate numerical tangent/focal checks; written proof supplies the all-period conclusion','external_software_executed':'Only preinstalled SymPy/mpmath; no downloaded source code'}
(root/'verification.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
