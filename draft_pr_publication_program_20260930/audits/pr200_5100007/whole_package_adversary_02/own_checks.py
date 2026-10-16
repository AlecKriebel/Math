"""Fresh finite adversarial checks; not a universal proof."""
import json, math
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
import sympy as s
import mpmath as m
m.mp.dps=105

def require(c,label):
    if not c: raise RuntimeError(label)
A,B,l,X=s.symbols('A B l X'); d=A-B
U=A*A/(A-l); V=B*B/(B-l)
h=(V+d+(U-V)*X)**2-4*d*U*X
f=(1-d*X/(A-l))*((V+d)**2-(A-l)*(U-V)**2*X/d)
require(s.cancel(h-f)==0,'physical factorization')
require(s.factor((U-V).subs(l,A*B/(A+B)))==0,'four locus')
count=0
for n in range(3,257):
 for w in range(1,(n+1)//2):
  if math.gcd(n,w)>1: continue
  L=n//math.gcd(n,2); q=F(2*w,n); c=Counter()
  for j in range(L):
   x=-j*q
   if n==4:
    c[x%1]-=2; c[(x+F(1,2))%1]+=2
   else:
    c[x%1]-=4; c[(x+F(1,2))%1]+=2
    c[(x+F(1,2)+q)%1]+=1;c[(x+F(1,2)-q)%1]+=1
  c={x:v for x,v in c.items() if v}
  require((len(c)==0)==(n%4==0),'divisor parity')
  if c: require(len(c)==2*L and set(c.values())=={-4,4},'divisor complete')
  count+=1
samples=[]
for kt in ('0.12','0.61','0.985'):
 k=m.mpf(kt); p=k*k; K=m.ellipk(p)
 sn=lambda u:m.ellipfun('sn',u,p)
 cn=lambda u:m.ellipfun('cn',u,p)
 dn=lambda u:m.ellipfun('dn',u,p)
 for n in range(3,19):
  for w in range(1,(n+1)//2):
   if math.gcd(n,w)>1: continue
   v=2*K*w/n; delta=2*v; a=dn(v)/cn(v); b=m.sqrt(1-p)/cn(v)
   Ao=a*dn(v)/cn(v); Bo=b/cn(v)
   maxerr=m.mpf(0); logs=[]
   for phase in (m.mpf(0),K*m.sqrt(2)/11,K*m.sqrt(3)/7,K*m.sqrt(5)/3):
    plus=minus=m.mpf(0)
    for j in range(n):
     u=phase+j*delta
     left=(-sn(u-v)/a,cn(u-v)/b);right=(-sn(u+v)/a,cn(u+v)/b)
     det=left[0]*right[1]-left[1]*right[0]
     x=(right[1]-left[1])/det; y=(left[0]-right[0])/det
     expected=(-Ao*sn(u),Bo*cn(u))
     maxerr=max(maxerr,abs(x-expected[0])/max(1,abs(x)),abs(y-expected[1])/max(1,abs(y)))
     r1=(x-k)**2+y*y;r2=(x+k)**2+y*y
     require(r1>0 and r2>0,'positive distance')
     hdirect=r1*r2
     C=(1-p*sn(v)**4)**2/(cn(v)**8)
     hformula=C*dn(u)**2*(dn(delta)**2-p*cn(delta)**2*sn(u)**2)
     maxerr=max(maxerr,abs(hdirect-hformula)/max(1,abs(hdirect)))
     plus+=m.log(r1)/2;minus+=m.log(r2)/2
    logs.append((plus,minus))
   spread=max(x[0] for x in logs)-min(x[0] for x in logs)
   require(maxerr<m.mpf('1e-90'),'direct tangent/factor residual')
   if n%4==0: require(spread<m.mpf('1e-88'),'positive product constancy')
   else: require(spread>m.mpf('1e-85'),'negative parity counterphase')
   samples.append({'k':kt,'N':n,'w':w,'max_relative_error':m.nstr(maxerr,10),'log_phase_spread_plus':m.nstr(spread,15)})
report={'status':'PASS','sympy':s.__version__,'mpmath':m.__version__,'precision':m.mp.dps,'rational_full_divisor_cases':count,'numeric_cases':len(samples),'samples':samples}
Path('OWN_CHECKS_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='samples'}))
