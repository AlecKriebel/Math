"""Source-convention controls, not a replacement for Stachel's published proof."""
from fractions import Fraction
from math import gcd
import json
import mpmath as mp
exact=0
for N in range(3,100,2):
    n=(N-1)//2
    ell=[Fraction(i*i+3,2*i+1) for i in range(N)]
    # Stachel rho_i=ell_(i+n), imported r_i=rho_(i+1).
    rho=[ell[(i+n)%N] for i in range(N)]
    r=[rho[(i+1)%N] for i in range(N)]
    assert sum(ell)==sum(rho)==sum(r); exact+=1
    for i in range(N):
        assert rho[(i+n)%N]==ell[(i-1)%N]; exact+=1
        assert ell[i]==r[(i+n)%N]; exact+=1
    assert sum(ell)==sum(ell+r)/2; exact+=1
mp.mp.dps=70
worst=mp.mpf(0); checks=0; families=0
sn=lambda u,m:mp.ellipfun('sn',u,m)
cn=lambda u,m:mp.ellipfun('cn',u,m)
dn=lambda u,m:mp.ellipfun('dn',u,m)
def check(x,scale=1):
    global checks,worst
    err=abs(x)/max(1,abs(scale)); worst=max(worst,err)
    assert err<mp.mpf('1e-58'), str(err)
    checks+=1
def dist(x,y):return mp.sqrt(sum((a-b)**2 for a,b in zip(x,y)))
for N in (3,5,7,9,11,15):
 for tau in range(1,N//2+1):
  if gcd(tau,N)>1:continue
  for ms in ('0.1','0.5','0.9'):
   m=mp.mpf(ms);K=mp.ellipk(m);v=2*K*tau/N
   beta=mp.sqrt(1-m);a=dn(v,m)/cn(v,m);b=beta/cn(v,m)
   check(a*a-b*b-m)
   ref=None;families+=1
   for phase in (mp.mpf('0.013'),mp.mpf('0.217'),mp.mpf('0.683')):
    us=[4*K*phase+2*v*j for j in range(N)]
    P=[(-a*sn(u,m),b*cn(u,m)) for u in us]
    Q=[(-sn(u+v,m),beta*cn(u+v,m)) for u in us]
    ell=[dist(P[i],Q[i]) for i in range(N)]
    r=[dist(Q[i],P[(i+1)%N]) for i in range(N)]
    L=sum(dist(P[i],P[(i+1)%N]) for i in range(N))
    for i in range(N):
     j=(i+1)%N
     normal=(Q[i][0],Q[i][1]/beta**2)
     check(sum(normal[t]*(P[j][t]-P[i][t]) for t in (0,1)))
     check(ell[i]+r[i]-dist(P[i],P[j]))
     check(ell[i]-r[(i+(N-1)//2)%N])
     assert ell[i]>0 and r[i]>0;checks+=1
    check(sum(ell)-L/2,L);check(sum(r)-L/2,L)
    if ref is not None:check(L-ref,L)
    ref=L
print(json.dumps({'status':'PASS','exact_index_assertions':exact,'numerical_assertions':checks,'primitive_families':families,'precision_decimal_digits':mp.mp.dps,'max_scaled_error':mp.nstr(worst,14),'limitations':'Finite high-precision diagnostics, not interval certificates or a proof; the resolution is the cited published theorem.'},indent=2))
