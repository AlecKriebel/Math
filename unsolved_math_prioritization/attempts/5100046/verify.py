"""k805 ratio checks. Shared algebra is credited to campaign5100044/PR207.
This is an author replay/adaptation, not an independent review.
"""
import json,math
from fractions import Fraction
from collections import Counter
import sympy as s
import mpmath as mp
C=Counter()
def ck(value,key):
 assert value,key
 C[key]+=1
u,t,k=s.symbols('u t k');q=1-t;dv2=1-k*k*t;D=1-k*k*t*u*u
U=1-2*k*k*t+k*k*t*t;V=1-2*t+k*k*t*t;W=1-k*k*t*t
for expr,key in [(U+V-2*q*dv2,'UV_sum'),(U-V-2*t*(1-k*k),'UV_difference'),(U*U-k*k*V*V-(1-k*k)*W*W,'strict_denominator_identity')]:ck(s.expand(expr)==0,key)
raw=dv2*D+2*k*dv2*q*u+k*k*q*(u*u-t)
ck(s.expand(raw-(1+k*u)*(U+k*V*u))==0,'distance_product_factorization')
lhs=1/((1+k*u)*(U+k*V*u)**2)+1/((1-k*u)*(U-k*V*u)**2)
rhs=2*(U*U+k*k*V*(V+2*U)*u*u)/((1-k*k*u*u)*(U*U-k*k*V*V*u*u)**2)
ck(s.factor(lhs-rhs)==0,'antipodal_edge_pair')
eps,a2,a1,a0=s.symbols('eps a2 a1 a0');f=a2/eps**2+a1/eps+a0;mir=-f.subs(eps,-eps)
ck(s.expand(f+mir)==2*a1/eps,'reflection_cancels_double_principal_part')
rotations=0
for N in range(6,207,4):
 m=N//2
 for tau in range(1,m):
  if math.gcd(tau,N)!=1:continue
  rotations+=1;delta=Fraction(tau,m);ell=Fraction(1,m)
  orbit={(j*delta)%1 for j in range(m)}
  ck(len(orbit)==m and orbit=={j*ell for j in range(m)},'odd_half_period_full_cyclic_orbit')
  ck(m%2==tau%2==1,'required_primitive_parities')
  ck(((Fraction(1,2)+delta/2)/ell).denominator==1,'ratio_shift_integral_period')
  ck(delta!=Fraction(1,2),'no_N4_exception_in_target')
  ck((2*delta)%1!=0,'two_double_poles_distinct_before_reduction')
  principal=Counter()
  for j in range(m):
   principal[(Fraction(1,2)+delta-j*delta)%1]+=1
   principal[(Fraction(1,2)-delta-j*delta)%1]-=1
  ck(all(v==0 for v in principal.values()),'opposite_double_coefficients_cancel_in_odd_sum')
# Explicit affine scaling of determinants under real inversion.
x1,y1,x2,y2,c=s.symbols('x1 y1 x2 y2 c',real=True)
r1=(x1-c)**2+y1*y1;r2=(x2-c)**2+y2*y2
ck(s.factor((x1-c)*y2/(r1*r2)-y1*(x2-c)/(r1*r2)-((x1-c)*y2-y1*(x2-c))/(r1*r2))==0,'inverse_edge_positive_scaling_identity')
mp.mp.dps=80
NC=Counter();maxerr=mp.mpf(0);samples=[]
def near(x,key):
 global maxerr
 x=abs(x);maxerr=max(maxerr,x);assert x<mp.mpf('1e-55'),(key,mp.nstr(x,12));NC[key]+=1

def area(P):return mp.fsum(P[i][0]*P[(i+1)%len(P)][1]-P[i][1]*P[(i+1)%len(P)][0] for i in range(len(P)))/2
for kk in map(mp.mpf,['.1','.5','.9']):
 par=kk*kk;K=mp.ellipk(par);Kp=mp.ellipk(1-par);beta=mp.sqrt(1-par)
 sn=lambda z:mp.ellipfun('sn',z,par)
 cn=lambda z:mp.ellipfun('cn',z,par)
 dn=lambda z:mp.ellipfun('dn',z,par)
 for N in [6,10,14,18,22,26]:
  m=N//2
  for tau in range(1,m):
   if math.gcd(tau,N)!=1:continue
   v=2*K*tau/N;delta=2*v;a=dn(v)/cn(v);b=beta/cn(v);h=sn(v);tt=h*h;qq=1-tt
   UU=1-2*par*tt+par*tt*tt;VV=1-2*tt+par*tt*tt;CC=b*h*dn(v)*qq*qq
   E=lambda z:CC*dn(z)*(1-par*tt*sn(z)**2)/((1+kk*sn(z))*(UU+kk*VV*sn(z))**2)
   B=lambda z:E(z)+E(z+2*K)
   S=lambda z:mp.fsum(dn(z+j*delta) for j in range(m))
   R=lambda z:mp.fsum(B(z+j*delta) for j in range(m))
   CA=a*b*sn(v)*cn(v)/dn(v);ratio=None;CR=R(mp.mpf('.21')*K)/S(mp.mpf('.21')*K+K)
   assert CR>0;NC['positive_proportionality_constant']+=1
   for phase in [mp.mpf(0),K/17,K/3,8*K/7]:
    P=[(-a*sn(phase+j*delta),b*cn(phase+j*delta)) for j in range(N)];AA=area(P);assert AA>0;NC['positive_original_area']+=1
    near((AA-2*CA*S(phase))/(1+abs(AA)),'direct_original_area_trace')
    inverse_areas=[]
    for focus in [kk,-kk]:
     II=[]
     for X,Y in P:
      dd=(X-focus)**2+Y*Y;assert dd>0;II.append(((X-focus)/dd,Y/dd))
     for j in range(N):
      cross=II[j][0]*II[(j+1)%N][1]-II[j][1]*II[(j+1)%N][0]
      assert cross>0;NC['positive_focal_inverse_edge']+=1
     inverse_areas.append(area(II))
    near((inverse_areas[0]-inverse_areas[1])/(1+abs(inverse_areas[0])),'both_foci_equal')
    Ai=inverse_areas[0];near((Ai-R(phase+v))/(1+abs(Ai)),'direct_inverse_area_trace')
    near((Ai-CR*S(phase))/(1+abs(Ai)),'odd_half_period_proportionality')
    if ratio is None:ratio=AA/Ai
    near((AA/Ai-ratio)/(1+abs(ratio)),'target_ratio_phase_invariance')
    if N==6:
     published=4*a**3*b**4/((2*a-b)*(a+b)**2)
     near((AA/Ai-published)/(1+abs(published)),'credited_published_N6_formula')
   for phase in [K/5+mp.j*Kp/11,2*K/7+mp.j*Kp/7]:
    near((R(phase)-CR*S(phase+K))/(1+abs(R(phase))),'nonreal_cyclic_trace_proportionality')
   if kk==mp.mpf('.5') and N<=14:samples.append({'N':N,'turning':tau,'ratio':mp.nstr(ratio,22)})
# Wrong parity controls: same generic trace, different shift and nonconstant ratio.
wrong=[]
par=mp.mpf('.64');kk=mp.sqrt(par);K=mp.ellipk(par);beta=mp.sqrt(1-par)
for N in [4,8,12]:
 v=2*K/N;a=mp.ellipfun('dn',v,par)/mp.ellipfun('cn',v,par);b=beta/mp.ellipfun('cn',v,par);vals=[]
 for phase in [0,K/11]:
  P=[(-a*mp.ellipfun('sn',phase+4*K*j/N,par),b*mp.ellipfun('cn',phase+4*K*j/N,par)) for j in range(N)]
  II=[((X-kk)/((X-kk)**2+Y**2),Y/((X-kk)**2+Y**2)) for X,Y in P];vals.append(area(P)/area(II))
 assert abs(vals[0]-vals[1])>mp.mpf('1e-30');NC['excluded_parity_ratio_varies']+=1;wrong.append({'N':N,'difference':mp.nstr(vals[1]-vals[0],12)})
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'exact_families':dict(sorted(C.items())),'primitive_rotation_controls':rotations,'numerical_diagnostics':sum(NC.values()),'numerical_families':dict(sorted(NC.items())),'precision_decimal_digits':80,'maximum_scaled_error':mp.nstr(maxerr,12),'sample_ratios':samples,'excluded_parity_controls':wrong,'credit':'Shared algebra and pole mechanism are adapted from campaign5100044/PR207; this is not independent verification or a separate-discovery claim.','limits':'Finite exact lattice/algebra controls and high-precision diagnostics support, not replace, the complete meromorphic proof.'},indent=2,sort_keys=True))
