#!/usr/bin/env python3
"""Direct CG normalization test using Kashaev1994 finite-sum rho formulas.
This is separate from the h-shift checker and the full old unknot contraction.
"""
import mpmath as mp,itertools,json,hashlib
from pathlib import Path
mp.mp.dps=90;count=0;worst=mp.mpf(0)
def close(a,b):
 global count,worst
 e=abs(a-b)/max(1,abs(a),abs(b));worst=max(worst,e);count+=1
 assert e<mp.mpf('1e-70'),mp.nstr(e,15)
for N in [3,5,7,9,11]:
 zeta=mp.exp(2j*mp.pi/N);m=(N-1)//2
 def rt(x):return mp.power(x,mp.mpf(1)/N)
 def g(x):return mp.exp(sum(mp.mpf(j)/N*mp.log(1-x*zeta**j) for j in range(1,N)))
 g1=g(1)
 def h(x):return x**(-m)*g(x)/g1
 def bracket(x,y):return (x**N-y**N)/(N*(x-y))
 def finite_f(x,y,z):
  term=mp.mpc(1);total=term
  for j in range(1,N):term*=z*(1-y*zeta**j)/(1-x*zeta**j);total+=term
  return total
 def face(a,b):return h(rt(a+b)/rt(b))/mp.sqrt(bracket(rt(a+b),rt(b)))
 def faceg(a,b):return face(a,b)*rt(a+b)**m
 for p,q,r in [(mp.mpf(a),mp.mpf(b),mp.mpf(c)) for a,b,c in [(1,2,3),(2,3,7),(1,1,1),(5,1,3)]]+[(mp.mpc('1','.2'),mp.mpc('2','.3'),mp.mpc('4','-.1'))]:
  xp,xq,xr,xpq,xqr,xpqr=map(rt,[p,q,r,p+q,q+r,p+q+r])
  pref=mp.sqrt(bracket(xpq,xq))*mp.sqrt(bracket(xpqr,xr))*mp.sqrt(bracket(xqr,xr))/mp.sqrt(bracket(xpqr,xqr))
  rho=pref*finite_f(xr/xpqr,xr/(zeta*xqr),xpq*xqr/(xpqr*xq))
  rhobar=pref*finite_f(xr/xqr,xr/(zeta*xpqr),xpqr*xq/(xpq*xqr))
  Df=face(p,q)*face(p+q,r)/(face(q,r)*face(p,q+r))
  Dg=faceg(p,q)*faceg(p+q,r)/(faceg(q,r)*faceg(p,q+r))
  u=xpqr*xq/(xpq*xqr)
  old=h(1/u);oldbar=(1-u**N)/(N*(1-u))/old
  close((old/(Df*rho/xqr**(2*m)))**N,1)
  close((oldbar/(rhobar/(Df*xpq**(2*m))))**N,1)
  close(Dg,Df*(xpq/xqr)**m)
  for a,c in itertools.product(range(N),repeat=2):
   half=(N+1)//2
   pos=(xpq*xqr)**m*old*zeta**(-half*a*c)/(rho*zeta**(half*a*c))
   neg=(xpq*xqr)**m*oldbar*zeta**(half*a*c)/(rhobar*zeta**(-half*a*c))
   close((pos/(Dg*zeta**(-a*c)))**N,1)
   close((neg*Dg/zeta**(a*c))**N,1)
print(json.dumps({'problem_id':10400139,'numerical_controls':count,'mpmath_dps':mp.mp.dps,'worst_relative_error':mp.nstr(worst,12),'tolerance':'1e-70','scope':'Non-interval finite diagnostics of both Kashaev finite-rho formulas, CG face normalization, added edge-root face coboundary and every reduced-charge pair for N3,5,7,9,11. The proof of arbitrary triangulation cancellation is cellular.','checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2,sort_keys=True))
