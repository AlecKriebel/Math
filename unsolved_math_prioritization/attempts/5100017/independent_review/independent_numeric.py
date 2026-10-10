#!/usr/bin/env python3
"""Independent mpmath diagnostics. These are not exact certificates or the all-period proof."""
import mpmath as mp, math,json
mp.mp.dps=85
counts={};worst={}
def check(x,key):
 x=abs(x);counts[key]=counts.get(key,0)+1;worst[key]=max(worst.get(key,mp.mpf(0)),x)
 assert x<mp.mpf('1e-65'),(key,mp.nstr(x,10))
def am(P):
 cs=[mp.im(mp.conj(p)*P[(i+1)%len(P)]) for i,p in enumerate(P)]
 return sum(cs)/2,sum(cs[i]*(p+P[(i+1)%len(P)]) for i,p in enumerate(P))
families=0
for N in (4,6,8,10,14,18,22):
 for r in range(1,N//2):
  if math.gcd(N,r)>1:continue
  for k in (mp.mpf(2)/7,mp.mpf(9)/10):
   m=k*k;K=mp.ellipk(m);v=2*K*r/N;delta=2*v
   sn=lambda u:mp.ellipfun('sn',u,m);cn=lambda u:mp.ellipfun('cn',u,m);dn=lambda u:mp.ellipfun('dn',u,m)
   a=dn(v)/cn(v);b=mp.sqrt(1-m)/cn(v);lam=a*a-1
   H=(a*a+b*b)/2;e=(a*a-b*b)/2;d=1-lam*(1/a**2+1/b**2);F=H*d+2*lam;vv=-4*e*lam*d/(F*F-e*e*d*d)
   Ms=[mp.mpc(0),mp.mpc(mp.mpf(7)/11,mp.mpf(-5)/13),mp.mpc(-8,3)]
   if d<-mp.mpf('1e-70'):Ms.append(mp.sqrt(-2*F/d))
   old={}
   for ph in (mp.mpf(1)/31,mp.mpf(7)/17,mp.mpf(19)/23):
    P=[mp.mpc(-a*sn(ph*K+j*delta),b*cn(ph*K+j*delta)) for j in range(N)]
    normals=[mp.mpc(p.real/a**2,p.imag/b**2) for p in P]
    Q0=[n/abs(n)**2 for n in normals];S0,_=am(Q0)
    for z in Ms:
     Q=[z+(1-mp.re(mp.conj(n)*z))*n/abs(n)**2 for n in normals]
     S,T=am(Q);G=2*F+d*abs(z)**2
     check((S-S0*G/(2*F))/(1+abs(S0)+abs(S)),'direct_area_identity')
     for q,n in zip(Q,normals):check((mp.re(mp.conj(n)*q)-1)/(1+abs(n)*abs(q)),'actual_outer_tangent_foot')
     if abs(G)<mp.mpf('1e-65'):
      check(S/(1+S0),'zero_circle_area');continue
     C=z/2-(z*(F+2*H*d+e*vv*d)+mp.conj(z)*(2*F*vv+3*e*d+vv*d*abs(z)**2/2))/(3*G)
     actual=T/(6*S);check((actual-C)/(1+abs(C)),'centroid_closed_formula')
     key=str(z)
     if key in old:check((actual-old[key])/(1+abs(C)),'phase_invariance')
     old[key]=actual
   families+=1
print(json.dumps({'status':'PASS','precision_digits':mp.mp.dps,'families':families,'diagnostic_assertions':sum(counts.values()),'counts':counts,'maximum_normalized_residuals':{k:mp.nstr(v,8) for k,v in worst.items()},'limitations':'High-precision diagnostics only; the written argument supplies the exact all-period theorem.'},indent=2))
