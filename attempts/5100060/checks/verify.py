"""Exact N=4 normalization and separately labeled direct-geometry diagnostics.
No finite check replaces the two full mathematical inputs or their scope audit.
"""
import sympy as S
import mpmath as mp
import math,json
from collections import Counter
E=Counter();C=Counter();worst=mp.mpf(0)
def ck(v,n):assert bool(v),n;E[n]+=1
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def dot(p,q):return sum(x*y for x,y in zip(p,q))
def area(P):return sum(det(p,q) for p,q in zip(P,P[1:]+P[:1]))/2
def minus(p,q):return tuple(x-y for x,y in zip(p,q))
def ant(P,F):
 U=[]
 for p,q in zip(P,P[1:]+P[:1]):
  n=minus(p,F);m=minus(q,F);hp=dot(n,p);hq=dot(m,q);D=det(n,m)
  U.append(((hp*m[1]-n[1]*hq)/D,(n[0]*hq-hp*m[0])/D))
 return U
def inv(P,F,rho=1):
 return [tuple(F[i]+rho*rho*(p[i]-F[i])/dot(minus(p,F),minus(p,F)) for i in range(2)) for p in P]
a,b,c=S.symbols('a b c',positive=True)
P=[(0,b),(-a,0),(0,-b),(a,0)];F=(c,0);U=ant(P,F);I=inv(P,F)
def reduced(x):
 p=S.together(x).as_numer_denom()[0]
 return S.factor(S.rem(S.Poly(p,c),S.Poly(c*c-a*a+b*b,c)).as_expr())
ck(S.factor(area(P)-2*a*b)==0,'N4_original_area')
ck(S.factor(area(U)-4*a*b)==0,'N4_actual_antipedal_area')
ck(reduced(area(I)-2/(a*b))==0,'N4_actual_unit_inverse_area')
ck(reduced(area(U)*area(I)-8)==0,'N4_target_product_eight')
for j,u in enumerate(U):
 for p in [P[j],P[(j+1)%4]]:
  ck(S.factor(dot(minus(p,F),minus(u,p)))==0,'N4_actual_antipedal_lines')
rho=S.symbols('rho',positive=True)
ck(reduced(area(inv(P,F,rho))-rho**4*area(I))==0,'radius_fourth_power_normalization')
# Integer arithmetic behind the source period class and the inverse input's half shift.
rot=0
for N in range(4,161,4):
 for tau in range(1,N//2):
  if math.gcd(N,tau)!=1:continue
  rot+=1;m=N//2
  ck(tau%2==1 and m%2==0,'primitive_source_parity')
  ck((m+tau)%2==1,'inverse_product_half_shift')
  ck((m*tau)%N==m,'primitive_antipodal_pairing')
# Corollary and zero behavior without any division.
A,V,Kappa,Const=S.symbols('A V Kappa Const')
ck(S.expand(V*(Kappa*A)-Kappa*(A*V))==0,'product_corollary_identity')
ck(S.expand((V*(Kappa*A)).subs(Kappa,0))==0,'zero_antipedal_coefficient_allowed')
mp.mp.dps=85
def close(x,y,n,tol=mp.mpf('1e-60')):
 global worst
 z=abs(x-y)/(1+abs(x)+abs(y))
 assert z<tol,(n,mp.nstr(z,8))
 worst=max(worst,z);C[n]+=1
def compute(k,N,tau,w,rho=mp.mpf(1),scale=mp.mpf(1)):
 K=mp.ellipk(k*k);v=2*K*tau/N
 sn=lambda u:mp.ellipfun('sn',u,k*k)
 cn=lambda u:mp.ellipfun('cn',u,k*k)
 dn=lambda u:mp.ellipfun('dn',u,k*k)
 aa=scale*dn(v)/cn(v);bb=scale*mp.sqrt(1-k*k)/cn(v)
 pp=[(-aa*sn(w+2*j*v),bb*cn(w+2*j*v)) for j in range(N)]
 out=[]
 for sign in [1,-1]:
  ff=(sign*scale*k,mp.mpf(0));ii=inv(pp,ff,rho);uu=ant(pp,ff)
  for j,(p,q) in enumerate(zip(pp,pp[1:]+pp[:1])):
   assert dot(minus(p,ff),minus(p,ff))>0;C['finite_focal_inversion']+=1
   assert det(minus(p,ff),minus(q,ff))>0;C['nonzero_focal_antipedal_determinant']+=1
   for z in [p,q]:close(dot(minus(z,ff),minus(uu[j],z)),0,'actual_antipedal_line')
  out.append((area(pp),area(ii),area(uu)))
 close(out[0][1],out[1][1],'opposite_focus_inverse_equality')
 close(out[0][2],out[1][2],'opposite_focus_antipedal_equality')
 return out[0]
families=phases=0
for N in [4,8,12,16,20,24,28]:
 for tau in range(1,N//2):
  if math.gcd(N,tau)!=1:continue
  for kk in ['.1','.5','.9','.99']:
   kval=mp.mpf(kk);K=mp.ellipk(kval*kval);families+=1
   vals=[compute(kval,N,tau,K*x) for x in map(mp.mpf,['.073','.329','.761'])]
   ref=vals[0]
   for aa,vv,bb in vals:
    close(aa*vv,ref[0]*ref[1],'credited_inverse_product_input')
    close(bb/aa,ref[2]/ref[0],'general_even_antipedal_input')
    close(vv*bb,ref[1]*ref[2],'exact_source_product')
    phases+=1
   if N==4:
    for aa,vv,bb in vals:close(vv*bb,8,'N4_value_eight')
# The unit-radius product is scale invariant because the two areas scale oppositely.
base=compute(mp.mpf('.6'),12,5,mp.mpf('.2'))
scaled=compute(mp.mpf('.6'),12,5,mp.mpf('.2'),scale=mp.mpf('2.3'))
close(scaled[1]*scaled[2],base[1]*base[2],'unit_product_uniform_scale')
rr=compute(mp.mpf('.6'),12,5,mp.mpf('.2'),rho=mp.mpf('1.5'))
close(rr[1]*rr[2],mp.mpf('1.5')**4*base[1]*base[2],'nonunit_radius_control')
wrong=[]
for N,tau in [(6,1),(10,3),(14,5)]:
 k0=mp.mpf('.7');K=mp.ellipk(k0*k0)
 vals=[compute(k0,N,tau,K*x) for x in map(mp.mpf,['.073','.329','.761'])]
 products=[v*b for a,v,b in vals];spread=max(products)-min(products)
 assert abs(spread)>mp.mpf('1e-12');C['excluded_parity_control']+=1
 wrong.append({'N':N,'tau':tau,'product_spread':mp.nstr(spread,15)})
print(json.dumps({'status':'PASS','exact_assertions':sum(E.values()),'exact_counts':dict(E),'primitive_rotations':rot,'numerical_diagnostics':{'precision_decimal_digits':85,'comparisons':sum(C.values()),'counts':dict(C),'families':families,'phases':phases,'maximum_scaled_error':mp.nstr(worst,15),'excluded_parity_controls':wrong},'scope':'Finite exact normalization and arithmetic checks; direct floating diagnostics are separate. The full theorem is a credited corollary of the two pinned proofs, not inferred from tests.'},indent=2,sort_keys=True))
