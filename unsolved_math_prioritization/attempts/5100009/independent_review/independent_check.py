"""Independent source-convention diagnostics; no finite test proves the theorem."""
from fractions import Fraction
from math import gcd
import mpmath as mp
import json
mp.mp.dps=80
exact=0
for N in range(3,102,2):
 n=(N-1)//2
 ell=[Fraction(3*i*i+7,2*i+3) for i in range(N)]
 rho=[ell[(i+n)%N] for i in range(N)]
 right=[rho[(i+1)%N] for i in range(N)]
 assert sum(right)==sum(ell);exact+=1
 for i in range(N):
  assert right[(i+n)%N]==ell[i];exact+=1
  assert rho[(i+n)%N]==ell[(i-1)%N];exact+=1
 for q in (1,3,5):
  assert sum(ell*q)==q*sum(ell);exact+=1
checks=0;worst=mp.mpf(0);families=0;turning_parities=set()
def test(x,scale=1):
 global checks,worst
 e=abs(x)/max(1,abs(scale));worst=max(worst,e)
 assert e<mp.mpf('1e-63'),str(e)
 checks+=1
def positive(x):
 global checks
 assert x>0;checks+=1
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def norm(x):return mp.sqrt(dot(x,x))
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
for N in (3,5,7,9,11):
 for tau in range(1,(N+1)//2):
  if gcd(N,tau)!=1:continue
  turning_parities.add(tau%2)
  for m in map(mp.mpf,('0.15','0.55','0.92')):
   K=mp.ellipk(m);h=2*K*tau/N
   sn=lambda u:mp.ellipfun('sn',u,m)
   cn=lambda u:mp.ellipfun('cn',u,m)
   dn=lambda u:mp.ellipfun('dn',u,m)
   beta=mp.sqrt(1-m);a=dn(h)/cn(h);b=beta/cn(h)
   ref=None;families+=1
   for phase in map(mp.mpf,('0.073','0.319','0.701')):
    u=4*K*phase
    P=(-a*sn(u),b*cn(u));P0=P
    next_seed=(-a*sn(u+2*h),b*cn(u+2*h))
    d=sub(next_seed,P);d=tuple(x/norm(d) for x in d)
    left=[];right=[];length=[]
    for i in range(N):
     # Thereafter use only Euclidean ray/ellipse intersection and reflection.
     t=-2*(P[0]*d[0]/a**2+P[1]*d[1]/b**2)/(d[0]**2/a**2+d[1]**2/b**2)
     s=-(P[0]*d[0]+P[1]*d[1]/beta**2)/(d[0]**2+d[1]**2/beta**2)
     Q=tuple(P[j]+s*d[j] for j in range(2))
     R=tuple(P[j]+t*d[j] for j in range(2))
     positive(s);positive(t-s)
     test(Q[0]**2+Q[1]**2/beta**2-1)
     test(R[0]**2/a**2+R[1]**2/b**2-1)
     test(Q[0]*d[0]+Q[1]*d[1]/beta**2)
     test(norm(d)-1)
     left.append(s);right.append(t-s);length.append(t)
     normal=(R[0]/a**2,R[1]/b**2)
     factor=2*dot(d,normal)/dot(normal,normal)
     d=tuple(d[j]-factor*normal[j] for j in range(2));P=R
    test(norm(sub(P,P0)),norm(P0))
    L=sum(length);test(sum(left)-L/2,L);test(sum(right)-L/2,L)
    for i in range(N):test(left[i]-right[(i+(N-1)//2)%N],L)
    if ref is not None:test(L-ref,L)
    ref=L
print(json.dumps({'status':'PASS','exact_assertions':exact,'numerical_assertions':checks,'primitive_families':families,'turning_number_parities':sorted(turning_parities),'precision_digits':mp.mp.dps,'max_scaled_error':mp.nstr(worst,16),'method':'Exact cyclic indexing and independent Euclidean ray/reflection recurrence, initialized using standard Jacobi coordinates','limitations':'Finite non-interval diagnostics only; source theorem supplies the proof.'},indent=2))
