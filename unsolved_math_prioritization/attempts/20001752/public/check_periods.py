#!/usr/bin/env python3
"""Non-interval diagnostic integration of exact q-expansions; not a proof.
Requires mpmath. No network access or source corpus is used.
"""
import mpmath as m, json
from pathlib import Path
N=180

def add(*terms): return [sum(t[n] for t in terms) for n in range(N+1)]
def scale(c,x): return [c*v for v in x]
def mul(a,b): return [sum(a[j]*b[n-j] for j in range(n+1)) for n in range(N+1)]
def pw(a,k):
 out=[1]+[0]*N
 for _ in range(k): out=mul(out,a)
 return out

def eis(k):
 coeff={2:-24,4:240,6:-504}[k]; sig=[0]*(N+1)
 for j in range(1,N+1):
  for n in range(j,N+1,j): sig[n]+=j**(k-1)
 return [1]+[coeff*v for v in sig[1:]]
def div(num,den,start):
 out=[0]*(N-start+1)
 for n in range(len(out)):
  v=num[n+start]-sum(den[start+j]*out[n-j] for j in range(1,n+1))
  assert v%den[start]==0
  out[n]=v//den[start]
 return out
E2,E4,E6=map(eis,[2,4,6])
Delta=[v//1728 for v in add(pw(E4,3),scale(-1,pw(E6,2)))]
phi8=div(pw(add(mul(E2,E4),scale(-1,E6)),2),Delta,1)
num24=add(scale(25,pw(E4,4)),scale(-49,mul(pw(E6,2),E4)),scale(48,mul(mul(E6,pw(E4,2)),E2)),mul(add(scale(-49,pw(E4,3)),scale(25,pw(E6,2))),pw(E2,2)))
phi24=div(num24,pw(Delta,2),2)
print(phi8[:4],phi24[:4],flush=True)
m.mp.dps=65
rows=[]
for d,co in [(8,phi8),(24,phi24)]:
 p=d//4
 def phi(t,sign=1): return m.polyval(co[::-1],sign*m.exp(-2*m.pi*t))
 I=m.quad(lambda t: phi(t,-1)/(t*t+m.mpf('.25'))**p,[m.mpf('.5'),1,2,4,8,16,32])
 J=m.quad(lambda t: phi(t)/t**p,[1,2,4,8,16,32])
 Pimag=-2*I-4*J
 value=Pimag/(17280*m.pi) if d==8 else -60*Pimag/(113218560*m.pi**5)
 rows.append({'dimension':d,'midpoint':str(value),'period_imag':str(Pimag),'e8_error_from_one_fifteenth':str(value-m.mpf(1)/15) if d==8 else None})
 print(rows[-1],flush=True)
Path(__file__).with_name('period_numerics.json').write_text(json.dumps(rows,indent=2))
