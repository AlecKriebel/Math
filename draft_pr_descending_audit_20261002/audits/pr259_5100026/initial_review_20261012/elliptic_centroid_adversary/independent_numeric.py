"""Independent diagnostics. Direct tangent + normal construction; not a proof."""
import json,sys,platform,math
from pathlib import Path
from datetime import datetime,timezone
sys.path.insert(0,str(Path(__file__).resolve().parent/'vendor'))
import mpmath as mp
mp.mp.dps=70
fmt=lambda x:mp.nstr(x,28)
rows=[]
for ktext in ['0.01','0.6','0.95','0.999']:
 k=mp.mpf(ktext);m=k*k;q=mp.sqrt(1-m);K=mp.ellipk(m)
 sn=lambda t:mp.ellipfun('sn',t,m);cn=lambda t:mp.ellipfun('cn',t,m);dn=lambda t:mp.ellipfun('dn',t,m)
 for N,p in [(4,1),(6,1),(8,1),(8,3),(10,3),(12,5),(14,3),(18,7)]:
  assert math.gcd(N,p)==1
  v=2*K*p/N;S=sn(v);C=cn(v);D=dn(v);a=D/q;f=k*C/q
  A=a*D/C;B=1/C
  def P(t):return mp.matrix([a*sn(t),cn(t)])
  def R(t):
   # Recompute from original tangent equations rather than asserted locus.
   r=P(t-v);s=P(t+v)
   return mp.lu_solve(mp.matrix([[r[0]/a**2,r[1]],[s[0]/a**2,s[1]]]),mp.matrix([1,1]))
  def U(t):
   r=R(t-v);s=R(t+v)
   mat=mp.matrix([[r[0]-f,r[1]],[s[0]-f,s[1]]])
   return mp.lu_solve(mat,mp.matrix([mp.fdot(r,r)-f*r[0],mp.fdot(s,s)-f*s[0]])),mp.det(mat)
  means=[];detmins=[];pairerrors=[];locuserrors=[]
  for ph in [mp.mpf('.173'),mp.mpf('.617'),K*mp.mpf('.811')]:
   vals=[];dets=[]
   for j in range(N):
    t=ph+2*v*j;u,det=U(t);vals.append(u);dets.append(abs(det))
    locuserrors.append(mp.norm(R(t)-mp.matrix([A*sn(t),B*cn(t)])))
    un,_=U(t+2*K)
    expected=2*f*(D**2*sn(t)**2-C**2)/(C**2*(1-m*S**2*sn(t)**2))
    pairerrors.append(abs(u[0]+un[0]-expected))
   means.append(mp.matrix([sum(u[i] for u in vals)/N for i in range(2)]));detmins.append(min(dets))
  rows.append({'k':ktext,'N':N,'winding':p,'a':fmt(a),'lambda':fmt(S*S),'focus':fmt(f),'x':fmt(means[0][0]),'x_over_f':fmt(means[0][0]/f),'max_phase_spread':fmt(max(mp.norm(u-means[0]) for u in means)),'max_abs_y':fmt(max(abs(u[1]) for u in means)),'min_abs_normal_det':fmt(min(detmins)),'max_outer_locus_error':fmt(max(locuserrors)),'max_pair_identity_error':fmt(max(pairerrors))})
print(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),'mpmath':mp.__version__,'precision_dps':mp.mp.dps,'proof':False,'rows':rows},indent=2))
