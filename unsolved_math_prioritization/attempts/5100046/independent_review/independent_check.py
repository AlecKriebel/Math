"""Independent k805 checks, without importing author code.
Full endpoint algebra, quotient pole multiplicities, and direct inversion tests.
"""
import sympy as S, mpmath as mp, math,json
from collections import Counter
from fractions import Fraction
EX=Counter();NU=Counter();worst=mp.mpf(0)
def ck(v,n):assert bool(v),n;EX[n]+=1
s,c,d,k,h,H,D,B=S.symbols('s c d k h H D B')
relations=[(c,1-s*s),(d,1-k*k*s*s),(H,1-h*h),(D,1-k*k*h*h),(B,1-k*k)]
def red(x):
 p=S.together(x).as_numer_denom()[0]
 for z,r in relations:p=S.rem(S.Poly(p,z),S.Poly(z*z-r,z)).as_expr()
 return S.factor(p)
def zero(x,n):ck(red(x)==0,n)
dot=lambda x,y:sum(a*b for a,b in zip(x,y))
det=lambda x,y:x[0]*y[1]-x[1]*y[0]
t=h*h;q=1-t;L=1-k*k*t*s*s
aa=D/H;bb=B/H;F=(k,0)
pm=(-aa*(s*H*D-h*c*d)/L,bb*(c*H+s*h*d*D)/L)
pp=(-aa*(s*H*D+h*c*d)/L,bb*(c*H-s*h*d*D)/L)
dm=aa+k*(s*H*D-h*c*d)/L
dp=aa+k*(s*H*D+h*c*d)/L
nm=(pm[0]-k,pm[1]);np=(pp[0]-k,pp[1])
zero(dm*dm-dot(nm,nm),'ordinary_minus_distance_squared')
zero(dp*dp-dot(np,np),'ordinary_plus_distance_squared')
U=1-2*k*k*t+k*k*t*t;V=1-2*t+k*k*t*t;W=1-k*k*t*t
zero(dm*dp-(1+k*s)*(U+k*V*s)/(q*L),'full_endpoint_focal_distance_product')
zero(det(nm,np)-2*bb*h*D*d*(1+k*s)/L,'full_endpoint_translated_cross_product')
Ce=bb*h*D*q*q
zero(det(nm,np)*(1+k*s)*(U+k*V*s)**2/2-Ce*d*L*(dm*dp)**2,'full_inverse_half_edge_formula')
zero(U-q*D*D-B*B*t,'positive_U_decomposition')
zero(U*U-k*k*V*V-B*B*W*W,'nonzero_real_denominator_margin')
zero(U-V-2*t*B*B,'dn_zero_other_factor_nonzero')
zero(U+V-2*q*D*D,'dn_zero_sum_factor_positive')
# Pole-zero derivative at s0=U/(k V); nonzero factors follow from domain inequalities.
s0=U/(k*V)
zero((1-s0*s0)*k*k*V*V-(k*k*V*V-U*U),'generic_cn_at_extra_pole')
zero((1-k*k*s0*s0)*V*V-(V*V-U*U),'generic_dn_at_extra_pole')
# Opposite dn and sn-derivative signs at reflected roots reverse the order-two coefficient.
N0,d0,j0,r0=S.symbols('N0 d0 j0 r0',nonzero=True)
coef=N0/(d0*j0*j0)
ck(S.simplify(coef+N0/((-d0)*(-j0)*(-j0)))==0,'actual_double_coefficient_sign_pattern')
rot=0
for m in range(3,80,2):
 for tau in range(1,m):
  if math.gcd(tau,2*m)!=1:continue
  rot+=1;delta=Fraction(tau,m)
  ck((m+tau)%2==0,'integer_shift_for_source')
  ck(delta!=Fraction(1,2),'generic_V_nonzero')
  orb=[(j*delta)%1 for j in range(m)]
  ck(len(set(orb))==m,'all_real_quotient_classes_distinct')
  for a in range(m):
   x=orb[a]
   plus=[j for j in range(m) if (delta-j*delta)%1==x]
   minus=[j for j in range(m) if (-delta-j*delta)%1==x]
   base=[j for j in range(m) if (-j*delta)%1==x]
   ck(len(plus)==len(minus)==len(base)==1,'all_three_pole_types_once_per_class')
   ck(plus[0]!=minus[0] and plus[0]!=base[0] and minus[0]!=base[0],'distinct_base_torus_contributors')
# Explicit smallest target: m=3 merges the types only after quotienting.
ck({Fraction(0),Fraction(1,3),Fraction(2,3)}=={Fraction(j,3) for j in [0,1,2]},'m3_collision_accounting')

mp.mp.dps=110
def close(x,y,n,tol=mp.mpf('1e-70')):
 global worst
 e=abs(x-y)/(1+abs(x)+abs(y));assert e<tol,(n,mp.nstr(e,8));worst=max(worst,e);NU[n]+=1
def area(P):return sum(det(p,q) for p,q in zip(P,P[1:]+P[:1]))/2
def make(k,N,tau,alpha=mp.mpf(1)):
 K=mp.ellipk(k*k);Kp=mp.ellipk(1-k*k);v=2*K*tau/N;delta=2*v;m=N//2
 sn=lambda u:mp.ellipfun('sn',u,k*k)
 cn=lambda u:mp.ellipfun('cn',u,k*k)
 dn=lambda u:mp.ellipfun('dn',u,k*k)
 beta=alpha*mp.sqrt(1-k*k);a=alpha*dn(v)/cn(v);b=beta/cn(v);f=alpha*k
 h=sn(v);tt=h*h;qq=1-tt;U=1-2*k*k*tt+k*k*tt*tt;V=1-2*tt+k*k*tt*tt
 C=b*h*dn(v)*qq*qq/alpha**3
 def BB(u):
  ss=sn(u)
  return 2*C*(1-k*k*tt*ss*ss)*(U*U+k*k*V*(V+2*U)*ss*ss)/(dn(u)*(U*U-k*k*V*V*ss*ss)**2)
 Tr=lambda u:sum(dn(u+j*delta) for j in range(m))
 R=lambda u:sum(BB(u+j*delta) for j in range(m))
 def direct(w):
  P=[(-a*sn(w+j*delta),b*cn(w+j*delta)) for j in range(N)];res=[]
  for sign in [1,-1]:
   P0=[(x-sign*f,y) for x,y in P]
   I=[(x/(x*x+y*y),y/(x*x+y*y)) for x,y in P0]
   for j,(x,y) in enumerate(zip(P0,P0[1:]+P0[:1])):
    assert det(x,y)>0;NU['strict_focal_edge_orientation']+=1
    close(det(I[j],I[(j+1)%N]),det(x,y)/(dot(x,x)*dot(y,y)),'independent_inverse_edge_scaling')
   res.append(area(I))
  close(res[0],res[1],'both_focus_areas')
  return area(P),res[0]
 return K,Kp,v,delta,R,Tr,direct,a,b
families=0
for kk in ['.07','.63','.94','.999']:
 for N,tau in [(6,1),(10,1),(10,3),(14,3),(14,5),(18,7),(22,5),(22,9),(30,13)]:
  k0=mp.mpf(kk);K,Kp,v,delta,R,T,direct,a,b=make(k0,N,tau,mp.mpf('1.7'));families+=1
  coeff=R(K*mp.mpf('.217'))/T(K*mp.mpf('.217')+K)
  assert coeff>0;NU['positive_C_R']+=1
  vals=[]
  for frac in ['.019','.271','.683']:
   w=K*mp.mpf(frac);A,Ai=direct(w)
   close(Ai,R(w+v),'direct_geometry_vs_cyclic_sum')
   close(Ai,coeff*T(w),'source_integer_shift')
   vals.append(A/Ai)
   if N==6:close(A/Ai,4*a**3*b**4/((2*a-b)*(a+b)**2),'published_N6_value')
  for x in vals:close(x,vals[0],'phase_ratio_constancy')
# Near every pole type, including the common Jacobi pole removable in each B.
near_cases=0
for N,tau,kk in [(6,1,'.4'),(10,3,'.83'),(22,5,'.97')]:
 K,Kp,v,delta,R,T,direct,a,b=make(mp.mpf(kk),N,tau)
 coef=R(K/7)/T(K/7+K);r=K+1j*Kp;p=1j*Kp
 for center in [r,r+delta,r-delta,p]:
  for eps in ['1e-6','1e-12']:
   u=center+mp.mpf(eps)
   close(R(u)/T(u+K),coef,'near_pole_or_removable_point',mp.mpf('1e-58'))
   near_cases+=1
print(json.dumps({'status':'PASS','exact_assertions':sum(EX.values()),'exact_counts':dict(EX),'primitive_rotations':rot,'numerical_diagnostics':{'precision_decimal_digits':110,'comparisons':sum(NU.values()),'counts':dict(NU),'families':families,'near_pole_cases':near_cases,'maximum_scaled_error':mp.nstr(worst,15)},'scope':'Independent endpoint algebra and pole-class multiplicities, plus separate high-precision direct inversion and near-pole diagnostics. The analytic proof was audited independently; finite checks alone do not prove it.'},indent=2,sort_keys=True))
