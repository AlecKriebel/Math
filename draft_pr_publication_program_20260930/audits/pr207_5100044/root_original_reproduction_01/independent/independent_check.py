#!/usr/bin/env python3
"""Independent geometric and pole diagnostics; no author code imported."""
from math import gcd
from collections import defaultdict
import json
import mpmath as mp
mp.mp.dps=110
exact=0;rots=0
for m in range(2,122,2):
 for t in range(1,m):
  if gcd(t,2*m)!=1:continue
  residues={(j*t)%m for j in range(m)}
  assert len(residues)==m;exact+=1
  coeff=defaultdict(int)
  for j in range(m):
   coeff[(t-j*t)%m]+=1;coeff[(-t-j*t)%m]-=1
  assert all(x==0 for x in coeff.values());exact+=1
  assert ((2*t)%m==0)==(m==2);exact+=1
  assert (m+t)%2==1;exact+=1
  rots+=1
checks=0;maxerror=mp.mpf(0);excluded=[];poles=[]
def close(a,b,name,tol='1e-88'):
 global checks,maxerror
 e=abs(a-b)/max(1,abs(a),abs(b))
 assert e<mp.mpf(tol),(name,str(e))
 checks+=1;maxerror=max(maxerror,e)
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def area(P):return sum(det(P[j],P[(j+1)%len(P)]) for j in range(len(P)))/2
for kval in ['.13','.57','.88']:
 k=mp.mpf(kval);par=k*k;kp=mp.sqrt(1-par);K=mp.ellipk(par);Kp=mp.ellipk(1-par)
 sn=lambda z:mp.ellipfun('sn',z,par)
 cn=lambda z:mp.ellipfun('cn',z,par)
 dn=lambda z:mp.ellipfun('dn',z,par)
 for N,t in [(4,1),(8,1),(8,3),(12,1),(12,5),(16,3),(16,7),(20,7),(20,9),(6,1),(10,3)]:
  v=2*K*t/N;delta=2*v;aa=dn(v)/cn(v);bb=kp/cn(v);m=N//2
  P=lambda w:(-aa*sn(w),bb*cn(w))
  def inv(w,focus=k):
   x,y=P(w);x-=focus;den=x*x+y*y
   return (x/den,y/den)
  def geometry(w):
   PP=[P(w+j*delta) for j in range(N)]
   JJ=[inv(w+j*delta) for j in range(N)]
   MM=[inv(w+j*delta,-k) for j in range(N)]
   A,B,C=area(PP),area(JJ),area(MM)
   close(B,C,'focal equality')
   return A*B
  vals=[geometry(K*p) for p in map(mp.mpf,['.041','.277','.831','1.73'])]
  if N%4==0:
   for x in vals[1:]:close(x,vals[0],f'product {N}/{t}')
  else:excluded.append(float(max(vals)-min(vals)))
  if N==4:
   for x in vals:close(x,4,'N4 credited value')
  E=lambda u:det(inv(u-v),inv(u+v))/2
  B=lambda u:E(u)+E(u+2*K)
  RR=lambda u:sum(B(u+j*delta) for j in range(m))
  SS=lambda u:sum(dn(u+j*delta) for j in range(m))
  const=RR(mp.mpf('.31')*K)/SS(mp.mpf('.31')*K+K)
  for zz in [K*mp.mpf('.23')+mp.j*Kp*mp.mpf('.37'),K*mp.mpf('1.29')+mp.j*Kp*mp.mpf('.51')]:
   close(RR(zz),const*SS(zz+K),'complex pole matching')
  if N%4==0 and N<=12:
   r=K+mp.j*Kp;e=mp.mpf('1e-18')
   if N>4:
    leadplus=e*e*B(r+delta+e);leadminus=e*e*B(r-delta+e)
    close(leadplus,-leadminus,'opposite double principal parts',tol='1e-14')
   res1=mp.mpf('1e-13')*RR(r+mp.mpf('1e-13'))
   res2=e*RR(r+e)
   close(res1,res2,'simple summed pole',tol='1e-22')
   poles.append({'modulus':kval,'N':N,'turning':t,'nonzero_residue':abs(res2)>mp.mpf('1e-20')})
assert any(abs(x)>1e-7 for x in excluded)
print(json.dumps({'status':'PASS','exact_integer_assertions':exact,'primitive_rotations':rots,
 'high_precision_diagnostics':checks,'precision_digits':110,'max_scaled_error':mp.nstr(maxerror,10),
 'wrong_parity_nonconstant_examples':len(excluded),'pole_diagnostics':poles,
 'limits':'Exact finite lattice controls and non-certified numerical diagnostics of direct inversions, both foci, and complex principal-part cancellation. Universal result rests on the separate written analytic review.'},indent=2))
