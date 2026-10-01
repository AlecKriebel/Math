#!/usr/bin/env python3
"""Exact calibration of conditional angular determinant calculation."""
import sympy as S,json
r,R,t,b=S.symbols('r R t b',positive=True)
checks=[]
def ck(name,x):
 assert S.simplify(x)==0,(name,S.factor(x));checks.append(name)
for n in [3,4]:
 q=r**n+R**n;p=q**S.Rational(1,n)
 ck(f'radial determinant n={n}',S.diff(p,r)*(p/r)**(n-1)-1)
 # Normalized radial/tangential Hessian, t=r^(n/2).
 ds=S.symbols('d0:'+str(n-1),positive=True)
 gs=S.symbols('g0:'+str(n-1),real=True)
 M=S.zeros(n);M[0,0]=n*(n+1)*b
 for i in range(n-1):
  M[0,i+1]=M[i+1,0]=n*t*gs[i]
  M[i+1,i+1]=ds[i]+t*t*(i+1)
 det=S.expand(M.det())
 ck(f'angular determinant leading term n={n}',det.subs(t,0)-n*(n+1)*b*S.prod(ds))
 ck(f'angular determinant first correction order n={n}',S.diff(det,t).subs(t,0))
 # Ellipsoid calibration at a principal-axis direction, det B=1.
 ms=[S.Rational(4),S.Rational(1,4)] if n==3 else [S.Rational(4),S.Rational(9),S.Rational(1,36)]
 m0=S.Rational(1)
 qdet=R**(n-1)*S.prod(ms)/(m0**S.Rational(n-1,2))
 coeff=m0**S.Rational(n+1,2)/(n*(n+1)*R**(n-1))
 ck(f'ellipsoid coefficient calibration n={n}',n*(n+1)*coeff*qdet-1)
print(json.dumps({'status':'PASS','checks':len(checks),'verified':checks,
 'limitation':'Checks local algebra/calibration only; neither selects an angular support function nor proves the assumed expansion.'},indent=2))
