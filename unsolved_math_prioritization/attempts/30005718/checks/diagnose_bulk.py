#!/usr/bin/env python3
"""80-digit, non-interval diagnostics only; no proof or effective threshold claim."""
import mpmath as mp,json
mp.mp.dps=80
samples=[40,80,160,320,640];fracs=[mp.mpf(1)/4,mp.mpf(1)/2,mp.mpf(3)/4,mp.mpf(1),mp.mpf(5)/4]
def add(*ps):
 a=[0]*max(map(len,ps))
 for p in ps:
  for i,v in enumerate(p):a[i]+=v
 while len(a)>1 and a[-1]==0:a.pop()
 return a
def mul(p,q):
 a=[0]*(len(p)+len(q)-1)
 for i,v in enumerate(p):
  for j,w in enumerate(q):a[i+j]+=v*w
 return a
def lam(z):return 1+3*z/2+z*mp.sqrt(5+4*z)/2
def H(z):return 2*(1+z)+(z*z+6*z+6)/mp.sqrt(5+4*z)
def alpha(z):return mp.diff(lambda x:mp.log(lam(mp.exp(x))),mp.log(z))
params={}
for target in fracs:
 lo=mp.mpf(-30);hi=mp.mpf(30)
 for _ in range(300):
  mid=(lo+hi)/2
  if alpha(mp.exp(mid))<target:lo=mid
  else:hi=mid
 x=(lo+hi)/2;z=mp.exp(x);s=mp.diff(lambda x:mp.log(lam(mp.exp(x))),x,2);k3=mp.diff(lambda x:mp.log(lam(mp.exp(x))),x,3);k4=mp.diff(lambda x:mp.log(lam(mp.exp(x))),x,4);h=H(z);h1=mp.diff(lambda x:H(mp.exp(x)),x);h2=mp.diff(lambda x:H(mp.exp(x)),x,2)
 A=-h2/(2*h*s)+h1*k3/(2*h*s*s)+k4/(8*s*s)-5*k3*k3/(24*s**3)
 params[target]=(z,s,h,A)
D=[2];Q=[0,1];rows=[]
for m in range(max(samples)+1):
 F=add(mul([2,1],D),mul([2],Q))
 if m in samples:
  n=m+4;degree=len(F)+2
  for target in fracs:
   j=int(target*m);k=j+3;z,s,h,A=params[target]
   c=mp.mpf(F[j]);cprev=mp.mpf(F[j-1]);cnext=mp.mpf(F[j+1]);leading=h*lam(z)**m*z**(-j)/mp.sqrt(2*mp.pi*m*s)
   observed=m*(mp.log(c*c/(cprev*cnext))-mp.log(mp.mpf((k+1)*(degree-k+1))/(k*(degree-k))))
   prediction=1/s-1/target-1/(mp.mpf(3)/2-target)
   row={'m':m,'alpha':str(target),'rho':mp.nstr(z,18),'m_scaled_ULC_log_margin':mp.nstr(observed,18),'limit_prediction':mp.nstr(prediction,18),'prediction_error':mp.nstr(observed-prediction,18),'relative_saddle_error_times_m_1_5':mp.nstr((c/leading-1-A/m)*m**mp.mpf('1.5'),18)}
   rows.append(row)
 D,Q=add(mul([1,2],D),mul([0,1],Q)),add(mul([0,1,1],D),mul([1,1],Q))
print(json.dumps({'status':'DIAGNOSTIC_ONLY','precision_decimal_digits':80,'interval_certification':False,'samples':rows},indent=2,sort_keys=True))
