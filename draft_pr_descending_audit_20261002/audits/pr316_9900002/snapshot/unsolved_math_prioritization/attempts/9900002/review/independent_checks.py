from fractions import Fraction as F
import json
count=0;cases=0
vals=(1,2,8,32)
for a in range(1,10):
 for b in range(1,10-a):
  for c in range(1,10-a-b):
   w=(a,b,c,10-a-b-c);p=[F(x,10) for x in w]
   for j in (2,3):
    v=vals[j];t=v//2;q=sum(p[j:]);M=sum(p[i]*vals[i] for i in range(j))
    U=[F(0)]*(t+1);U[0]=F(1)
    for s in range(1,t+1):U[s]=sum((p[i]*U[s-x] for i,x in enumerate(vals) if x<=s),F(0))
    exact=p[j]*sum(U)
    bound=1-(q-p[j])/q-M/(q*t)
    assert exact>=bound;count+=1
    total=sum(p[i]*sum(U[s] for s in range(t+1) if s+x>t) for i,x in enumerate(vals))
    assert total==1;count+=1;cases+=1
last=None
for n in range(2,101):
 exponent=1+4**(n-1)+2**n-4**n
 assert exponent==1+2**n-3*4**(n-1);count+=1
 assert exponent<0;count+=1
 if last is not None:assert exponent<last;count+=1
 last=exponent
for n in range(1,8):
 p=F(1,2**(2**n));q=sum((F(1,2**(2**k)) for k in range(n,n+5)),F(0))
 assert q<=p/(1-p);count+=1
 assert q-p<=p*p/(1-p);count+=1
print(json.dumps({'status':'PASS','assertions':count,'exact_renewal_laws_and_thresholds':cases},sort_keys=True))
