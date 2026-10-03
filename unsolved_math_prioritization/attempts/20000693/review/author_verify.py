#!/usr/bin/env python3
"""Local/model consistency checks only. Does not test/prove L-function moments."""
import json
import math
from fractions import Fraction
from pathlib import Path
import sympy as s
import mpmath as mp

ROOT = Path(__file__).resolve().parent
I=s.I
PRIM={
 'one':(1,{0:s.Integer(1)}),
 'quad3':(3,{0:0,1:1,2:-1}),
 'quad4':(4,{0:0,1:1,2:0,3:-1}),
 'quart5':(5,{0:0,1:1,2:I,3:-I,4:-1}),
 'quart5bar':(5,{0:0,1:1,2:-I,3:I,4:-1}),
}
def primitive(name,p):
 f,vals=PRIM[name]
 return s.sympify(vals[p%f])
def char(name,q,p):
 assert q%PRIM[name][0]==0
 return primitive(name,p) if math.gcd(q,p)==1 else s.Integer(0)
def conv(a,b,N):
 return [s.expand(sum(a[j]*b[n-j] for j in range(n+1))) for n in range(N+1)]
def coefficients(terms,N):
 c=[s.Integer(1)]+[s.Integer(0)]*N
 for z,a in terms:
  c=conv(c,[s.rf(a,n)*z**n/s.factorial(n) for n in range(N+1)],N)
 return c
def groups(rows):
 d={}
 for name,q,a in rows:d[name]=d.get(name,s.Integer(0))+a
 return {k:v for k,v in d.items() if v!=0}
def equal(a,b):return all(s.simplify(x-y)==0 for x,y in zip(a,b))
CASES=[
 [('one',1,s.Integer(1)),('one',2,s.Integer(1))],
 [('quad3',3,s.Rational(1,2)),('quad3',12,s.Rational(3,2)),('quad4',20,s.Rational(1,3))],
 [('quart5',5,s.Integer(1)),('quart5bar',10,s.Integer(1))],
 [('quart5',5,s.Rational(1,4)),('quart5',10,s.Rational(3,4)),('quart5',20,s.Integer(1))],
 [('one',6,s.Integer(0)),('quad4',4,s.Rational(1,2))],
 [('one',2,s.Integer(0))],
]
checks=0
for rows in CASES:
 Q=math.lcm(*(q for _,q,_ in rows));g=groups(rows)
 for p in [2,3,5,7,11,13,17,19]:
  orig=coefficients([(char(n,q,p),a) for n,q,a in rows],8)
  lifted=[(char(n,Q,p),a) for n,q,a in rows]
  lifted += [(primitive(n,p),a) for n,q,a in rows if Q%p==0 and q%p!=0]
  assert equal(orig,coefficients(lifted,8));checks+=9
  core=coefficients([(primitive(n,p),a) for n,q,a in rows],8)
  grouped=coefficients([(primitive(n,p),a) for n,a in g.items()],8)
  assert equal(core,grouped);checks+=9
  if Q%p:
   J=[s.expand(b*s.conjugate(b)) for b in orig[:3]]
   # Ordered-pair factors: (1-rho*x)^(M_psi*M_phi).
   pair=[(primitive(n,p)*s.conjugate(primitive(m,p)),-a*b)
         for n,a in g.items() for m,b in g.items()]
   H=conv(J,coefficients(pair,2),2)
   assert s.simplify(H[0]-1)==0 and s.simplify(H[1])==0
   checks+=2

# Exact local normalizations and a differing-modulus deletion at p=2.
x=s.symbols('x',real=True)
one=1/(1-x)
two=(1+x)/(1-x)**3
assert s.simplify((1-x)**4*two-(1-x*x))==0;checks+=1
assert s.simplify(one/two-(1-x)**2/(1+x))==0;checks+=1
assert s.simplify((one/two).subs(x,s.Rational(1,2)))==s.Rational(1,6);checks+=1
assert sum(v*v for v in groups(CASES[0]).values())==4;checks+=1
assert sum(v*v for v in groups(CASES[2]).values())==2;checks+=1

# Real-weight Parseval checks at small primes, separately using quadrature.
mp.mp.dps=55
def mpc(z):return mp.mpc(str(s.re(z)),str(s.im(z)))
def mpf(a):return mp.mpf(int(s.numer(a)))/int(s.denom(a))
numerical=[]
for ci,rows in enumerate(CASES[:5]):
 for p in [2,3,5]:
  terms=[(mpc(char(n,q,p)),mpf(a)) for n,q,a in rows]
  c=[mp.mpc(1)]+[mp.mpc(0)]*160
  for z,a in terms:
   d=[mp.mpc(1)]
   for r in range(1,161):d.append(d[-1]*z*(a+r-1)/r)
   c=[sum(c[j]*d[r-j] for j in range(r+1)) for r in range(161)]
  series=sum(abs(v)**2/mp.mpf(p)**r for r,v in enumerate(c))
  quad=mp.quad(lambda theta:mp.fprod(abs(1-z*mp.e**(1j*theta)/mp.sqrt(p))**(-2*a) for z,a in terms),[0,mp.pi,2*mp.pi])/(2*mp.pi)
  err=abs(series-quad)
  assert err<mp.mpf('1e-35');checks+=1
  numerical.append({'case':ci,'prime':p,'absolute_error':mp.nstr(err,8)})

# Known unitary-matrix moments, not actual Dirichlet L-values.
matrix=[]
for m in [mp.mpf('0.25'),mp.mpf('0.5'),mp.mpf(1),mp.mpf('1.5'),mp.mpf(2),mp.mpf(3)]:
 target=mp.barnesg(1+m)**2/mp.barnesg(1+2*m)
 errors=[]
 for N in [10,100,1000]:
  logv=sum(mp.loggamma(j)+mp.loggamma(j+2*m)-2*mp.loggamma(j+m) for j in range(1,N+1))-m*m*mp.log(N)
  errors.append(abs(mp.exp(logv)/target-1))
 assert errors[2]<errors[1]<errors[0];checks+=1
 matrix.append({'weight':str(m),'relative_errors_N10_N100_N1000':[mp.nstr(e,9) for e in errors]})
assert abs(mp.barnesg(2)**2/mp.barnesg(3)-1)<mp.mpf('1e-50');checks+=1
assert abs(mp.barnesg(3)**2/mp.barnesg(5)-mp.mpf(1)/12)<mp.mpf('1e-50');checks+=1

report={'status':'PASS','check_count':checks,'scope':'exact local coefficient/lift/aggregation identities and independent numerical phase/matrix normalizations; no L-function moment verification','exact_series_degree':8,'cases':len(CASES),'phase_checks':numerical,'matrix_checks':matrix,'asymptotic_proved':False,'versions':{'sympy':s.__version__,'mpmath':mp.__version__}}
(ROOT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
