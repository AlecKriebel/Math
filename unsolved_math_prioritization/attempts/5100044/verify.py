#!/usr/bin/env python3
from fractions import Fraction as F
from collections import Counter
from math import gcd
from pathlib import Path
import json,hashlib
import sympy as sy
counts=Counter()
def ck(n,x):
 assert x,n
 counts[n]+=1
s,t,k=sy.symbols('s t k');q=1-t;Dv2=1-k*k*t;Dmid=1-k*k*t*s*s
U=1-2*k*k*t+k*k*t*t;V=1-2*t+k*k*t*t;W=1-k*k*t*t
ck('UV_sum',sy.expand(U+V-2*q*Dv2)==0)
ck('UV_difference',sy.expand(U-V-2*t*(1-k*k))==0)
ck('positive_focal_factor',sy.expand(U*U-k*k*V*V-(1-k*k)*W*W)==0)
raw=Dv2*Dmid+2*k*Dv2*q*s+k*k*q*(s*s-t)
ck('focal_distance_product_factorization',sy.expand(raw-(1+k*s)*(U+k*V*s))==0)
rawpair=1/((1+k*s)*(U+k*V*s)**2)+1/((1-k*s)*(U-k*V*s)**2)
paired=2*(U*U+k*k*V*(V+2*U)*s*s)/((1-k*k*s*s)*(U*U-k*k*V*V*s*s)**2)
ck('antipodal_edge_sum',sy.factor(rawpair-paired)==0)
# Reflection-odd Laurent expansions have opposite quadratic principal parts.
e,b2,b1,b0,bp=sy.symbols('e b2 b1 b0 bp')
f=b2/e**2+b1/e+b0+bp*e
mirror=-f.subs(e,-e)
ck('opposite_double_coefficients',sy.limit(e**2*(f+mirror),e,0)==0)
ck('simple_coefficients_add',sy.limit(e*(f+mirror),e,0)==2*b1)
# Exact N4 axial value, with b²=a²-c².
a,b,c=sy.symbols('a b c',positive=True)
area_inv=b/a**2*(1/(a-c)+1/(a+c))
ck('N4_area_product_four',sy.factor((2*a*b*area_inv-4).subs(b*b,a*a-c*c))==0)
rot=0
for N in range(4,405,4):
 m=N//2
 for tau in range(1,m):
  if gcd(N,tau)!=1:continue
  rot+=1;delta=F(tau,m);ell=F(1,m)
  orbit=[(-j*delta)%1 for j in range(m)]
  ck('full_cyclic_order',len(set(orbit))==m)
  ck('all_reduced_real_classes',set(orbit)=={j*ell for j in range(m)})
  ck('product_shift_halfperiod',((F(1,2)+delta/2)/ell)%1==F(1,2))
  ck('N4_exception_equivalence',(delta==F(1,2))==(N==4))
  if N>4:
   ck('two_generic_double_locations_distinct',(2*delta)%1!=0)
   double=Counter()
   for j in range(m):
    double[(F(1,2)+delta-j*delta)%1]+=1
    double[(F(1,2)-delta-j*delta)%1]-=1
   ck('double_principal_parts_cancel',all(v==0 for v in double.values()))
  else:ck('exception_p_and_r_same_reduced_class',(F(1,2)/ell).denominator==1)
for N in [6,10,14,18,22]:
 m=N//2;delta=F(1,m);ell=F(1,m)
 ck('wrong_parity_shift_fullperiod',((F(1,2)+delta/2)/ell).denominator==1)
# Numerical direct Euclidean inversions, separately identified.
import mpmath as mp
mp.mp.dps=80
numcounts=Counter();maxerr=mp.mpf(0)
def num(n,x):
 global maxerr
 assert x<mp.mpf('1e-58'),(n,mp.nstr(x,8))
 numcounts[n]+=1;maxerr=max(maxerr,x)
def area(P):return sum(P[i][0]*P[(i+1)%len(P)][1]-P[i][1]*P[(i+1)%len(P)][0] for i in range(len(P)))/2
for kk in [mp.mpf('.2'),mp.mpf('.5'),mp.mpf('.8')]:
 par=kk*kk;K=mp.ellipk(par);Kp=mp.ellipk(1-par);beta=mp.sqrt(1-par)
 sn=lambda u:mp.ellipfun('sn',u,par)
 cn=lambda u:mp.ellipfun('cn',u,par)
 dn=lambda u:mp.ellipfun('dn',u,par)
 for N in [4,6,8,10,12,16,20]:
  for tau in range(1,N//2):
   if gcd(N,tau)!=1:continue
   v=2*K*tau/N;delta=2*v;m=N//2;a=dn(v)/cn(v);b=beta/cn(v)
   h=sn(v);t=h*h;q=1-t;U=1-2*par*t+par*t*t;V=1-2*t+par*t*t;C=b*h*dn(v)*q*q
   E=lambda u:C*dn(u)*(1-par*t*sn(u)**2)/((1+kk*sn(u))*(U+kk*V*sn(u))**2)
   B=lambda u:E(u)+E(u+2*K)
   S=lambda w:sum(dn(w+j*delta) for j in range(m))
   def get(w):
    P=[(-a*sn(w+j*delta),b*cn(w+j*delta)) for j in range(N)]
    II=[]
    for focus in [kk,-kk]:
     I=[((x-focus)/((x-focus)**2+y*y),y/((x-focus)**2+y*y)) for x,y in P]
     II.append(area(I))
    num('both_focal_areas_equal',abs(II[0]-II[1])/max(1,abs(II[0])))
    formula=sum(E(w+v+j*delta) for j in range(N))
    num('direct_inverse_area_formula',abs(II[0]-formula)/max(1,abs(II[0])))
    for j in [0,N//3]:
     u=w+v+j*delta
     R=P[j];T=P[(j+1)%N]
     dm=a+kk*sn(u-v);dp=a+kk*sn(u+v)
     D=1-par*t*sn(u)**2
     rhs=(1+kk*sn(u))*(U+kk*V*sn(u))/(q*D)
     num('edge_distance_factorization',abs(dm*dp-rhs)/max(1,abs(rhs)))
     raw=((R[0]-kk)*T[1]-R[1]*(T[0]-kk))/(2*dm**2*dp**2)
     num('edge_area_identity',abs(raw-E(u))/max(1,abs(raw)))
    return area(P),II[0]
   a0,i0=get(K/17);product=a0*i0;ratio=i0/S(K/17+K+v)
   for w in [K/9,K/3,8*K/7]:
    aa,ii=get(w)
    num('two_pole_proportionality',abs(ii-ratio*S(w+K+v))/max(1,abs(ii)))
    if N%4==0:num('required_product',abs(aa*ii-product)/max(1,abs(product)))
    else:num('excluded_parity_ratio',abs(ii/aa-i0/a0))
    if N==4:num('credited_N4_constant',abs(aa*ii-4))
   if N>4:
    r=K+1j*Kp;z=r+mp.mpf('.12')+mp.mpf('.08')*1j
    num('odd_reflection_about_r',abs(B(2*r-z)+B(z))/max(1,abs(B(z))))
root=Path(__file__).resolve().parent
out={'status':'PASS','proof_sha256':hashlib.sha256((root/'PROOF.md').read_bytes()).hexdigest(),'exact_assertions':sum(counts.values()),'exact_categories':dict(counts),'primitive_rotation_cases':rot,'numerical_diagnostics':sum(numcounts.values()),'numerical_categories':dict(numcounts),'numerical_precision_digits':80,'maximum_scaled_error':mp.nstr(maxerr,10),'limits':'Finite exact controls and non-certified numerical diagnostics support, not replace, the universal meromorphic proof','software':'Locally authored code; preinstalled SymPy/mpmath only'}
(root/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
