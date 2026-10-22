#!/usr/bin/env python3
"""Exact finite controls and separately labeled numerical area diagnostics."""
from fractions import Fraction as F
from math import gcd
from collections import Counter
from pathlib import Path
import json,hashlib
import sympy as sy
counts=Counter()
def ck(name,test):
 assert test,name
 counts[name]+=1
# Symbolic addition and contact/area identities after clearing denominators.
s,c,d,h,C,D,k=sy.symbols('s c d h C D k')
den=1-k*k*s*s*h*h
snplus=(s*C*D+h*c*d)/den;snminus=(s*C*D-h*c*d)/den
cnplus=(c*C-s*h*d*D)/den;cnminus=(c*C+s*h*d*D)/den
def reduce_poly(expr):
 x=sy.factor(expr)
 for var,replacement in [(c*c,1-s*s),(C*C,1-h*h),(d*d,1-k*k*s*s),(D*D,1-k*k*h*h)]:x=sy.expand(x).subs(var,replacement)
 return sy.factor(x)
ck('universal_chord_contact_plus',reduce_poly((D*s*snplus+c*cnplus-C)*den)==0)
ck('universal_chord_contact_minus',reduce_poly((D*s*snminus+c*cnminus-C)*den)==0)
ck('universal_cross_area',reduce_poly((snplus*cnminus-snminus*cnplus-2*h*C*d/den)*den**2)==0)
# Foot formula from n/(n.n), normalized alpha=1, beta²=1-k².
x=sy.symbols('x')
norm=x+(1-x)/(1-k*k)
ck('origin_projection_denominator',sy.factor(norm-(1-k*k*x)/(1-k*k))==0)
# Reflection-even local Laurent series: the exact incident-term cancellation.
e=sy.symbols('e');ax,ay,bx,by,xx,xy,yx,yy,zx,zy=sy.symbols('ax ay bx by xx xy yx yy zx zy')
Q=sy.Matrix([ax/e**2+bx,ay/e**2+by])
Rplus=sy.Matrix([xx+yx*e+zx*e**2,xy+yy*e+zy*e**2])
Rminus=Rplus.subs(e,-e)
local=sy.expand(sy.det(sy.Matrix.hstack(Q,Rplus-Rminus))/2)
ck('no_pole_above_order_one',sy.limit(e*local,e,0)==ax*yy-ay*yx)
ck('no_double_pole',sy.limit(e**2*local,e,0)==0)
# Exact reduced-lattice controls for both target and excluded parity.
rotations=0;target_cases=0;excluded_cases=0
for N in range(3,203):
 for tau in range(1,(N+1)//2):
  if 2*tau>=N or gcd(N,tau)!=1:continue
  rotations+=1
  m=N if N%2 else N//2
  delta=F(2*tau,N) # units 2K
  ell=F(1,m)
  residues=[(j*delta)%1 for j in range(N)]
  multiplicity=Counter(residues)
  ck('distinct_pole_classes_before_quotient',len(multiplicity)==m)
  ck('repeated_poles_have_equal_positive_multiplicity',set(multiplicity.values())=={N//m})
  ck('generated_reduced_real_period',set(residues)=={j*ell for j in range(m)})
  ck('nonadjacent_poles',delta%1!=0)
  shift=(F(1,2)+delta/2)/ell
  if N%4!=2:
   target_cases+=1;ck('target_shift_is_half_period',shift%1==F(1,2))
  else:
   excluded_cases+=1;ck('excluded_shift_is_full_period',shift.denominator==1)
  # Evenness: -j reorders every finite cyclic orbit.
  ck('evenness_reindex',Counter((-r)%1 for r in residues)==multiplicity)
# Reduced torus coordinates normalized to real period1, imaginary period1.
poles=Counter({(F(0),F(1,4)):1,(F(0),F(3,4)):1})
zeros=Counter({(F(1,2),F(1,4)):1,(F(1,2),F(3,4)):1})
translated=lambda q:((q[0]-F(1,2))%1,q[1])
ck('half_shift_product_zero_divisor',zeros+Counter({translated(x):m for x,m in zeros.items()})==poles+Counter({translated(x):m for x,m in poles.items()}))
# Separately numeric diagnostics use actual Euclidean chord projections.
import mpmath as mp
mp.mp.dps=75
numeric=Counter();maxerr=mp.mpf(0)
def num(name,err):
 global maxerr
 assert err<mp.mpf('1e-55'),(name,mp.nstr(err,10))
 numeric[name]+=1;maxerr=max(maxerr,err)
def area(P):return sum(P[i][0]*P[(i+1)%len(P)][1]-P[i][1]*P[(i+1)%len(P)][0] for i in range(len(P)))/2
for mod in [mp.mpf('.2'),mp.mpf('.5'),mp.mpf('.8')]:
 par=mod*mod;K=mp.ellipk(par);Kp=mp.ellipk(1-par);beta=mp.sqrt(1-par)
 sn=lambda u:mp.ellipfun('sn',u,par)
 cn=lambda u:mp.ellipfun('cn',u,par)
 dn=lambda u:mp.ellipfun('dn',u,par)
 for N in [3,4,5,6,7,8,9,10,11,12,16]:
  for tau in range(1,N//2+1):
   if 2*tau>=N or gcd(N,tau)!=1:continue
   v=2*K*tau/N;delta=2*v;a=dn(v)/cn(v);b=beta/cn(v)
   S=lambda w:sum(dn(w+j*delta) for j in range(N))
   pedal=lambda u:(-(1-par)*sn(u)/dn(u)**2,beta*cn(u)/dn(u)**2)
   def values(w):
    P=[(-a*sn(w+j*delta),b*cn(w+j*delta)) for j in range(N)]
    Q=[]
    for j in range(N):
     R=P[j];Z=P[(j+1)%N];dx,dy=Z[0]-R[0],Z[1]-R[1]
     t=-(R[0]*dx+R[1]*dy)/(dx*dx+dy*dy)
     foot=(R[0]+t*dx,R[1]+t*dy);direct=pedal(w+v+j*delta)
     num('direct_chord_projection',max(abs(foot[r]-direct[r]) for r in [0,1])/max(1,abs(foot[0]),abs(foot[1])))
     Q.append(foot)
    A,A0=area(P),area(Q)
    num('orbit_dn_area_identity',abs(A-abcoef*S(w))/max(1,abs(A)))
    return A,A0
   abcoef=a*b*sn(v)*cn(v)/dn(v)
   Aref,Qref=values(K/17);prop=Qref/S(K/17+K+v);prod=Aref*Qref
   m=N if N%2 else N//2;ell=2*K/m
   Csum=S(K/17)*S(K/17+ell/2)
   for w in [K/9,K/3,8*K/7]:
    A,Q=values(w)
    num('pedal_two_pole_proportionality',abs(Q-prop*S(w+K+v))/max(1,abs(Q)))
    num('cyclic_dn_halfperiod_product',abs(S(w)*S(w+ell/2)/Csum-1))
    if N%4!=2:num('required_area_product',abs(A*Q-prod)/max(1,abs(prod)))
    else:num('excluded_parity_proportional_areas',abs(Q/A-Qref/Aref))
   # Reflection symmetry at a complex double pole, evaluated away from pole.
   r=K+1j*Kp;z=r+mp.mpf('.13')+mp.mpf('.07')*1j
   p1,p2=pedal(z),pedal(2*r-z)
   num('pedal_complex_even_reflection',max(abs(p1[j]-p2[j]) for j in [0,1])/max(1,abs(p1[0]),abs(p1[1])))
root=Path(__file__).resolve().parent
out={'status':'PASS','proof_sha256':hashlib.sha256((root/'PROOF.md').read_bytes()).hexdigest(),'exact_assertions':sum(counts.values()),'exact_categories':dict(counts),'primitive_rotation_cases':rotations,'target_parity_cases':target_cases,'excluded_parity_cases':excluded_cases,'numerical_diagnostics':sum(numeric.values()),'numerical_categories':dict(numeric),'numerical_precision_digits':75,'maximum_scaled_error':mp.nstr(maxerr,10),'limits':'Finite controls and non-certified numerical diagnostics support the written universal meromorphic proof, not replace it','software':'Locally authored code; preinstalled SymPy/mpmath; no downloaded source code executed'}
(root/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
