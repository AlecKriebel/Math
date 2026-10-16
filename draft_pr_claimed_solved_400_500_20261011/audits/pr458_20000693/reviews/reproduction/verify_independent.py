#!/usr/bin/env python3
"""Explicit-guard exact rational/local/CUE audit; no L-function moment test.

Tail and analytic trapezoid bounds below are exact rational bounds. Numerical
summations use mpmath and are corroborative, not interval enclosures.
"""
import json, math
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
mp.mp.dps=70
ZERO=(F(0),F(0));ONE=(F(1),F(0));NEG=(-F(1),F(0));II=(F(0),F(1));NI=(F(0),-F(1))
def require(condition,label):
 if not condition:raise RuntimeError('independent audit rejected: '+label)
def add(x,y):return (x[0]+y[0],x[1]+y[1])
def mul(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def scale(x,a):return (x[0]*a,x[1]*a)
def conj(x):return (x[0],-x[1])
def power(x,n):
 y=ONE
 for _ in range(n):y=mul(y,x)
 return y
def norm(x):return x[0]*x[0]+x[1]*x[1]
def mpf(x):return mp.mpf(x.numerator)/x.denominator
def mpc(x):return mp.mpc(mpf(x[0]),mpf(x[1]))
def coeff(terms,N):
 d=[ZERO]+[tuple(sum((a*power(c,k)[j] for c,a in terms),F(0)) for j in (0,1)) for k in range(1,N+1)]
 b=[ONE]
 for n in range(1,N+1):
  v=ZERO
  for k in range(1,n+1):v=add(v,mul(d[k],b[n-k]))
  b.append(scale(v,F(1,n)))
 return b
def conv(x,y,N):
 out=[]
 for n in range(N+1):
  z=ZERO
  for k in range(n+1):z=add(z,mul(x[k],y[n-k]))
  out.append(z)
 return out
def binomial_coeff(terms,N):
 out=[ONE]+[ZERO]*N
 for c,a in terms:
  v=[ONE]
  for n in range(1,N+1):v.append(scale(mul(v[-1],c),(a+n-1)/n))
  out=conv(out,v,N)
 return out
P={'one':(1,[ONE]),'quad3':(3,[ZERO,ONE,NEG]),'quad4':(4,[ZERO,ONE,ZERO,NEG]),
'quart5':(5,[ZERO,ONE,II,NI,NEG]),'quart5bar':(5,[ZERO,ONE,NI,II,NEG])}
def primitive(n,p):return P[n][1][p%P[n][0]]
def actual(n,q,p):
 require(q>0 and q%P[n][0]==0,'valid induction modulus')
 return primitive(n,p) if math.gcd(q,p)==1 else ZERO
def group(rows):
 g={}
 for n,q,a in rows:
  require(a>=0,'nonnegative weight')
  g[n]=g.get(n,F(0))+a
 return {n:a for n,a in g.items() if a>0}
def exponent(rows):return sum((a*a for a in group(rows).values()),F(0))
CASES=[[],[('one',30,F(0))],
 [('one',1,F(1)),('one',2,F(1))],
 [('quad3',3,F(1,2)),('quad3',12,F(3,2)),('quad4',20,F(1,3))],
 [('quart5',5,F(3,4)),('quart5bar',10,F(5,4))],
 [('quart5',5,F(1,4)),('quart5',10,F(3,4)),('quart5',20,F(2))],
 [('one',1,F(1,3)),('quart5',35,F(2,3)),('quad3',6,F(0))],
 [('quad4',4,F(0)),('quad4',12,F(0))],
 [('one',1,F(5,4)),('quad3',15,F(1,4)),('quart5',10,F(1,2))],
 [('quad3',6,F(0)),('quad4',4,F(7,4)),('quart5bar',20,F(1,8))]]
PRIMES=[2,3,5,7,11,13,17,19,23,29]
ASYMPTOTIC_PROVED=False
COUNTS={k:0 for k in ['input_prime_exact_recurrence','input_prime_lift','input_prime_aggregation','input_prime_zero_omission','good_prime_regularization','character_multiplicativity','distinct_primitive_witness','exact_boundary_normalization','rational_tail_phase_trapezoid','cue_exact_toeplitz','cue_fractional_fourier','cue_fractional_determinant','barnes_finite_quotient']}
# Early explicit negative-control targets: wrong formulas must abort even under -O.
require(exponent(CASES[2])==F(4),'same primitive collision exponent')
require(exponent(CASES[4])==F(34,16),'conjugate primitives remain distinct')
require(F(1,1)/(F(1)+F(1,2))*F(1,2)**2==F(1,6),'deletion ratio')
require(F(1)/(1-F(1,3)**2)==F(9,8),'correlated local expectation')
require(abs(mp.barnesg(3)**2/mp.barnesg(5)-mp.mpf(1)/12)<mp.mpf('1e-60'),'Barnes fourth moment')
require(all(a>=0 for rows in CASES for _,_,a in rows),'nonnegative domain')
require(ASYMPTOTIC_PROVED is False,'no actual L-function asymptotic claimed')
COUNTS['exact_boundary_normalization']+=7
for name,(f,values) in P.items():
 for a in range(f):
  for b in range(f):
   require(values[(a*b)%f]==mul(values[a],values[b]),'primitive multiplicativity')
   COUNTS['character_multiplicativity']+=1
for i,n in enumerate(P):
 for m in list(P)[i+1:]:
  Q=math.lcm(P[n][0],P[m][0]);require(any(mul(primitive(n,p),conj(primitive(m,p)))!=ONE for p in PRIMES if Q%p),'nonprincipal finite witness')
  COUNTS['distinct_primitive_witness']+=1
for rows in CASES:
 Q=math.lcm(*(q for _,q,_ in rows)) if rows else 1;g=group(rows)
 for p in PRIMES:
  terms=[(actual(n,q,p),a) for n,q,a in rows];b=coeff(terms,12)
  require(b==binomial_coeff(terms,12),'log recurrence versus binomial');COUNTS['input_prime_exact_recurrence']+=1
  restored=[(actual(n,Q,p),a) for n,q,a in rows]+[(primitive(n,p),a) for n,q,a in rows if Q%p==0 and q%p!=0]
  require(b==coeff(restored,12),'modulus lift and inverse restoration');COUNTS['input_prime_lift']+=1
  require(coeff([(primitive(n,p),a) for n,q,a in rows],12)==coeff([(primitive(n,p),a) for n,a in g.items()],12),'primitive aggregation');COUNTS['input_prime_aggregation']+=1
  require(b==coeff([(actual(n,q,p),a) for n,q,a in rows if a],12),'zero omission');COUNTS['input_prime_zero_omission']+=1
  if Q%p:
   J=[(norm(v),F(0)) for v in b[:3]]
   pair=[(mul(primitive(n,p),conj(primitive(m,p))),-a*c) for n,a in g.items() for m,c in g.items()]
   H=conv(J,coeff(pair,2),2)
   require(H[0]==ONE and H[1]==ZERO and all(v[1]==0 for v in H),'regularization cancellation');COUNTS['good_prime_regularization']+=1
# Exact rational geometric tail bound for coefficient majorants.
def tail_bound(A,p,N):
 if A==0:return F(0),F(0)
 d=F(1)
 for n in range(1,N+2):d*= (A+n-1)/n
 first=d*d/F(p**(N+1))
 ratio=max(F(1,p),((A+N+1)/(N+2))**2/F(p))
 require(ratio<1,'majorant tail geometric ratio')
 return first/(1-ratio),ratio
PHASE=[]
N=224;K=1024
for ci in [2,3,4,5,6,8]:
 rows=CASES[ci];A=sum((a for _,_,a in rows),F(0))
 for p in [2,3,5]:
  terms=[(actual(n,q,p),a) for n,q,a in rows];b=coeff(terms,N)
  finite=sum((norm(v)/F(p**n) for n,v in enumerate(b)),F(0))
  tail,ratio=tail_bound(A,p,N)
  # Since p>=2, 1/sqrt(p)<3/4; use annular radius R=5/4.
  # On both boundary circles, |F(w)| <= 40^ceil(A).
  # Cauchy bounds each nonconstant Fourier coefficient by M R^-|n|.
  # The K-point trapezoid error is <=2M/(R^K-1), exactly rational.
  trap_bound=2*F(40**math.ceil(A))/(F(5,4)**K-1)
  require(tail>=0 and trap_bound>0,'positive explicit analytic error bounds')
  def integrand(t):return mp.fprod(abs(1-mpc(c)*mp.e**(1j*t)/mp.sqrt(p))**(-2*mpf(a)) for c,a in terms)
  phase=mp.quad(integrand,[0,mp.pi,2*mp.pi])/(2*mp.pi)
  trapezoid=sum(integrand(2*mp.pi*j/K) for j in range(K))/K
  err=max(abs(phase-mpf(finite)),abs(trapezoid-mpf(finite)))
  require(err<mpf(tail)+mpf(trap_bound)+mp.mpf('1e-60'),'fractional local phase agreement')
  PHASE.append({'case':ci,'prime':p,'degree':N,'trapezoid_nodes':K,'observed_max_error':mp.nstr(err,12),
   'exact_series_tail_bound':str(tail),'exact_successive_majorant_ratio_bound':str(ratio),
   'exact_trapezoid_error_bound':str(trap_bound),'numerical_rounding_interval_certified':False})
  COUNTS['rational_tail_phase_trapezoid']+=1
# Fraction-only determinant for integer CUE weights 0 through 4.
def det(matrix):
 a=[row[:] for row in matrix];value=F(1);N=len(a)
 for j in range(N):
  pivot=next((k for k in range(j,N) if a[k][j]),None)
  if pivot is None:return F(0)
  if pivot!=j:a[pivot],a[j]=a[j],a[pivot];value=-value
  pivotval=a[j][j];value*=pivotval
  for k in range(j+1,N):
   ratio=a[k][j]/pivotval
   for l in range(j+1,N):a[k][l]-=ratio*a[j][l]
   a[k][j]=F(0)
 return value
CUE=[]
for m in range(5):
 for n in range(1,9):
  def fourier(k):return F((-1)**abs(k)*math.comb(2*m,m+k)) if -m<=k<=m else F(0)
  toeplitz=det([[fourier(j-k) for k in range(n)] for j in range(n)])
  gamma=F(1)
  for j in range(1,n+1):gamma*=F(math.factorial(j-1)*math.factorial(j+2*m-1),math.factorial(j+m-1)**2)
  require(toeplitz==gamma,'integer Toeplitz exact CUE');COUNTS['cue_exact_toeplitz']+=1
  CUE.append({'integer_m':m,'N':n,'exact_value':str(toeplitz)})
FRACTIONAL=[]
for m in [mp.mpf('0.25'),mp.mpf('0.5'),mp.mpf('1.75')]:
 fourier=[]
 for k in range(6):
  measured=mp.quad(lambda t:(2*abs(mp.sin(t/2)))**(2*m)*mp.cos(k*t),[0,mp.pi,2*mp.pi])/(2*mp.pi)
  closed=(-1)**k*mp.gamma(2*m+1)*mp.rgamma(m+k+1)*mp.rgamma(m-k+1)
  require(abs(measured-closed)<mp.mpf('1e-60'),'fractional Fourier integral');COUNTS['cue_fractional_fourier']+=1
  fourier.append(measured)
 for n in range(1,7):
  toeplitz=mp.det(mp.matrix([[fourier[abs(j-k)] for k in range(n)] for j in range(n)]))
  gamma=mp.fprod(mp.gamma(j)*mp.gamma(j+2*m)/mp.gamma(j+m)**2 for j in range(1,n+1))
  require(abs(toeplitz/gamma-1)<mp.mpf('1e-60'),'fractional Toeplitz CUE');COUNTS['cue_fractional_determinant']+=1
  FRACTIONAL.append({'m':str(m),'N':n,'relative_error':mp.nstr(abs(toeplitz/gamma-1),12)})
 for n in [1,5,30]:
  gamma=mp.fprod(mp.gamma(j)*mp.gamma(j+2*m)/mp.gamma(j+m)**2 for j in range(1,n+1))
  barnes=mp.barnesg(1+m)**2/mp.barnesg(1+2*m)*mp.barnesg(n+1)*mp.barnesg(n+1+2*m)/mp.barnesg(n+1+m)**2
  require(abs(barnes/gamma-1)<mp.mpf('1e-60'),'finite Barnes quotient');COUNTS['barnes_finite_quotient']+=1
report={'status':'PASS','reviewer':'/root/pr458_reproduction','pr':458,'problem_id':'20000693','frozen_head':'87a39f7b4e5ef81aacf98464f86586cc95684d7f',
 'asymptotic_proved':ASYMPTOTIC_PROVED,'actual_L_function_moments_tested':False,'scope':'Exact rational/local identities and model normalization checks; rigorous truncation and analytic trapezoid bounds, unvalidated numerical rounding.',
 'counts_by_family':COUNTS,'total_cases':sum(COUNTS.values()),'case_count_convention':'One per prime/input or matrix/Fourier size; not coefficientwise assertion counts.',
 'phase_cases':PHASE,'integer_CUE_cases':CUE,'fractional_CUE_cases':FRACTIONAL,'mpmath_version':mp.__version__}
print(json.dumps(report,indent=2))
