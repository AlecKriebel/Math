"""Non-interval high-precision diagnostics, explicitly not proof certificates."""
import mpmath as mp,json
from math import gcd
from collections import Counter
mp.mp.dps=75
C=Counter();worst=mp.mpf(0)
def ck(err,kind):
 global worst
 err=abs(err);worst=max(worst,err);assert err<mp.mpf('1e-48'),(kind,err);C[kind]+=1
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def dot(p,q):return sum(x*y for x,y in zip(p,q))
def area(P):return sum(det(P[i],P[(i+1)%len(P)])for i in range(len(P)))/2
families=[];star=None
for N in [6,10,14,18]:
 for tau in range(1,N//2):
  if gcd(N,tau)>1:continue
  for ks in ['0.25','0.65','0.9']:
   k=mp.mpf(ks);par=k*k;kp=mp.sqrt(1-par);K=mp.ellipk(par);Ki=mp.ellipk(1-par);v=2*K*tau/N;delta=2*v
   sn=lambda u:mp.ellipfun('sn',u,par)
   cn=lambda u:mp.ellipfun('cn',u,par)
   dn=lambda u:mp.ellipfun('dn',u,par)
   a=dn(v)/cn(v);b=kp/cn(v)
   P=lambda u:(-a*sn(u),b*cn(u))
   normal=lambda u:(-sn(u),cn(u)/kp)
   def foot(u,M):
    n=normal(u);lam=(1-dot(n,M))/dot(n,n)
    return tuple(M[i]+lam*n[i]for i in range(2))
   S=lambda u:sum(dn(u+j*delta)for j in range(N))
   def data(w,M):
    Ps=[P(w+j*delta)for j in range(N)];ns=[normal(w+v+j*delta)for j in range(N)]
    Qs=[foot(w+v+j*delta,M)for j in range(N)]
    coeff=sum(2*det(ns[i],ns[(i+1)%N])*dot(ns[i],ns[(i+1)%N])/(dot(ns[i],ns[i])*dot(ns[(i+1)%N],ns[(i+1)%N]))for i in range(N))/8
    return area(Ps),area(Qs),coeff
   AA,B0,D0=data(0,(0,0));c0=B0/AA;c2=D0/AA
   assert c0>0
   if tau==1:assert c2>0
   for phase in ['0','0.137','0.731','1.41']:
    w=mp.mpf(phase)*K
    for M in [(0,0),(1,0),(0,1),(2,-3),(mp.mpf('0.3'),mp.mpf('1.7'))]:
     A,B,D=data(w,M);target=(c0+c2*dot(M,M))*A
     ck((B-target)/(1+abs(B)+abs(target)),'all_M_phase_proportionality')
     ck((D-c2*A)/(1+abs(D)+abs(c2*A)),'radial_coefficient_phase_proportionality')
     ca=a*b*sn(v)*cn(v)/dn(v)
     ck((A-ca*S(w))/(1+abs(A)),'direct_orbit_area_trace')
   # Two generic complex phases and a near-pole point for a real arbitrary M.
   M=(mp.mpf('0.7'),mp.mpf('-1.2'));c=(c0+c2*dot(M,M))*a*b*sn(v)*cn(v)/dn(v)
   for u in [K*mp.mpf('.2')+Ki*mp.mpc(0,'.31'),K*mp.mpf('.69')+Ki*mp.mpc(0,'.73'),K+1j*Ki+mp.mpf('1e-8')]:
    T=area([foot(u+j*delta,M)for j in range(N)])
    target=c*S(u+K)
    ck((T-target)/(1+abs(T)+abs(target)),'complex_pedal_trace')
   families.append({'N':N,'tau':tau,'modulus':ks,'c0':mp.nstr(c0,18),'c2':mp.nstr(c2,18)})
   if N==10 and tau==3 and ks=='0.25':
    assert D0<0;rho=mp.sqrt(-B0/D0)
    for phase in ['0','.19','.63','1.13']:
     w=mp.mpf(phase)*K
     for ang in [mp.mpf(0),mp.pi/5,mp.pi/2]:
      M=(rho*mp.cos(ang),rho*mp.sin(ang));A,B,D=data(w,M)
      ck(B/(1+abs(A)),'explicit_exceptional_circle_all_phases')
    star={'radius_squared':mp.nstr(rho*rho,30),'c0':mp.nstr(c0,30),'c2':mp.nstr(c2,30)}
print(json.dumps({'status':'PASS','diagnostic_assertions':sum(C.values()),'counts':dict(sorted(C.items())),'max_scaled_error':mp.nstr(worst,12),'families':families,'explicit_star_diagnostic':star,'scope':'75-digit non-interval diagnostics only. Exact sign and zero-family claims follow from the written proof, not numerical tolerance.'},indent=2,sort_keys=True))
