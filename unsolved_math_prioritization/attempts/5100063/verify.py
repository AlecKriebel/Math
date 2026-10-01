#!/usr/bin/env python3
from fractions import Fraction as F
from collections import Counter
from math import gcd
from pathlib import Path
import json,hashlib
import sympy as sy
count=Counter()
def ck(n,x):
 assert x,n
 count[n]+=1
k,t,s=sy.symbols('k t s');q=1-t;d2=1-k*k*t;U=1-2*k*k*t+k*k*t*t;V=1-2*t+k*k*t*t;W=1-k*k*t*t;D=1-k*k*t*s*s
ck('outer_distance_factorization',sy.expand((d2*d2-(1-k*k))*s*s+2*k*d2*q*s+(1-k*k)+k*k*q*q-(1+k*s)*(U+k*V*s))==0)
ck('first_edge_product',sy.expand(D+k*k*(s*s-t)-d2-k*k*q*s*s)==0)
ck('second_edge_product_middle_coefficient',sy.expand(d2*(V*V-U*U*t)+q*(U*U-k*k*V*V*t)-2*U*V*q*d2)==0)
Z=W*W-4*k*k*t*t*q*d2;D3=U*W-2*k*k*t*q*V;C3=V*W-2*t*d2*U
ck('triple_dn_numerator',sy.expand(U*U-k*k*V*V*t-d2*D3)==0)
ck('triple_cn_numerator',sy.expand(V*V-U*U*t-q*C3)==0)
ck('triple_factor_positivity',sy.expand(d2*D3**2-k*k*q*C3**2-(1-k*k)*Z**2)==0)
# Odd reflected Laurent series has cancelling double principal coefficients.
e,a2,a1,a0=sy.symbols('e a2 a1 a0');p=a2/e**2+a1/e+a0
ck('double_laurent_cancellation',sy.limit(e*e*(p-p.subs(e,-e)),e,0)==0)
ck('remaining_simple_laurent',sy.limit(e*(p-p.subs(e,-e)),e,0)==2*a1)
rot=0
for N in range(3,304,2):
 for tau in range(1,N//2+1):
  if gcd(N,tau)!=1:continue
  rot+=1
  # Real period4K normalized to1, delta=tau/N, v=delta/2.
  delta=F(tau,N);v=delta/2;L=F(1,N)
  orbit=[(j*delta)%1 for j in range(N)]
  ck('primitive_order',len(set(orbit))==N)
  ck('reduced_lattice',set(orbit)=={j*L for j in range(N)})
  ck('opposite_focus_halfperiod',(F(1,2)/L)%1==F(1,2))
  ck('L1_nonzero_for_odd_period',3*v!=F(1,4))
  ck('N3_critical_equivalence',(3*v==F(1,2))==(N==3 and tau==1))
  first={(v)%1,(-v)%1};second={(3*v)%1,(-3*v)%1}
  ck('double_locations_distinct',len(first)==2)
  ck('double_and_simple_locations_disjoint',not(first&second))
  ck('simple_locations_count',len(second)==(1 if N==3 else 2))
  principal=Counter()
  for j in range(N):
   principal[(v-j*delta)%1]+=1;principal[(-v-j*delta)%1]-=1
  ck('double_coefficients_cancel',all(z==0 for z in principal.values()))
  R=v
  ck('all_poles_one_real_orbit',all(((x-R)/L).denominator==1 for x in first|second))
  ck('reflection_center_moves_by_period',((2*R)/L).denominator==1)
# Numerical diagnostics are independent direct geometry and not certificates.
import mpmath as mp
mp.mp.dps=85
nums=Counter();errmax=mp.mpf(0)
def num(n,e):
 global errmax
 assert e<mp.mpf('1e-62'),(n,mp.nstr(e,10))
 nums[n]+=1;errmax=max(errmax,e)
def area(P):return sum(P[i][0]*P[(i+1)%len(P)][1]-P[i][1]*P[(i+1)%len(P)][0] for i in range(len(P)))/2
for mod in [mp.mpf('.2'),mp.mpf('.5'),mp.mpf('.8')]:
 par=mod*mod;K=mp.ellipk(par);Kp=mp.ellipk(1-par);beta=mp.sqrt(1-par)
 sn=lambda u:mp.ellipfun('sn',u,par)
 cn=lambda u:mp.ellipfun('cn',u,par)
 dn=lambda u:mp.ellipfun('dn',u,par)
 for N in [3,5,7,9,11,13]:
  for tau in range(1,N//2+1):
   if gcd(N,tau)!=1:continue
   v=2*K*tau/N;delta=2*v;h=sn(v);C=cn(v);d=dn(v);t=h*h;q=C*C
   a=d/C;b=beta/C;Ao=a*d/C;Bo=b/C
   U=1-2*par*t+par*t*t;V=1-2*t+par*t*t;W=1-par*t*t
   L0=(U*U-par*V*V*t)/d;L1=(V*V-U*U*t)/C;CC=Bo*h*d*q**4/C
   Z=W*W-4*par*t*t*q*d*d
   num('triple_dn_identity',abs(L0-Z*dn(3*v)))
   num('triple_cn_identity',abs(L1-Z*cn(3*v)))
   E=lambda u:CC*dn(u)*(1-par*t*sn(u)**2)/((d+mod*C*sn(u))**2*(L0+mod*L1*sn(u)))
   cyc=lambda u:sum(E(u+j*delta) for j in range(N))
   def get(w):
    P=[]
    for j in range(N):
     u=w+j*delta
     # Direct intersection of original billiard tangents at phasesu-v,u+v.
     xm,ym=-a*sn(u-v),b*cn(u-v);xp,yp=-a*sn(u+v),b*cn(u+v)
     det=xm*yp-xp*ym
     X=a*a*(yp-ym)/det;Y=b*b*(xm-xp)/det
     num('outer_locus_direct_tangents',max(abs(X+Ao*sn(u)),abs(Y-Bo*cn(u)))/max(1,abs(X),abs(Y)))
     P.append((X,Y))
    vals=[]
    for f in [mod,-mod]:
     inv=[((x-f)/((x-f)**2+y*y),y/((x-f)**2+y*y)) for x,y in P]
     vals.append(area(inv))
    num('edge_sum_area_identity',abs(vals[0]-cyc(w+v))/max(1,abs(vals[0])))
    num('opposite_focus_phase',abs(vals[1]-cyc(w+v+2*K))/max(1,abs(vals[1])))
    return vals
   ref=get(K/17);product=ref[0]*ref[1]
   for w in [K/9,K/3,8*K/7]:
    vals=get(w)
    num('required_area_product',abs(vals[0]*vals[1]/product-1))
   r0=3*K+1j*Kp;z=r0+mp.mpf('.11')+mp.mpf('.07')*1j
   num('edge_odd_reflection',abs(E(2*r0-z)+E(z))/max(1,abs(E(z))))
   R=r0+v;L=4*K/N
   z=mp.mpf('.23')+mp.mpf('.17')*1j
   num('sum_odd_about_pole_class',abs(cyc(2*R-z)+cyc(z))/max(1,abs(cyc(z))))
   num('complex_halfshift_product',abs(cyc(z)*cyc(z+L/2)/product-1))
root=Path(__file__).resolve().parent
out={'status':'PASS','proof_sha256':hashlib.sha256((root/'PROOF.md').read_bytes()).hexdigest(),'exact_assertions':sum(count.values()),'exact_categories':dict(count),'primitive_rotations':rot,'numerical_diagnostics':sum(nums.values()),'numerical_categories':dict(nums),'numerical_precision_digits':85,'max_scaled_error':mp.nstr(errmax,10),'limits':'Finite exact controls and separate uncertified numerics support, not replace, the all-period meromorphic proof','software':'Locally authored; preinstalled SymPy/mpmath, no downloaded code'}
(root/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
