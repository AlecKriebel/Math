"""Finite controls for the pure-jump variation proof. Not a stochastic proof."""
from fractions import Fraction as F
from collections import Counter
import json,math
import sympy as s
C=Counter()
def ck(v,k):
 assert v,k
 C[k]+=1
# Exact mesh phase indexing, including exact grid hits.
for numerator in range(1,18):
 for denominator in [7,11,19]:
  time=F(numerator,denominator)
  for mesh in [F(1,8),F(1,25),F(3,101)]:
   phase=time/mesh; j=phase.numerator//phase.denominator;u=phase-j
   ck(0<=u<1,'fractional_phase_range')
   for l in range(1,7):
    ck((j+l)*mesh-time==mesh*(l-u),'right_endpoint_kernel_argument')
    ck((j+l-1)*mesh-time==mesh*(l-1-u),'left_endpoint_kernel_argument')
# Exact moment/truncation inequalities used for compensators.
for e in [F(1,2),F(1,7),F(1,20)]:
 for z in [F(i,13) for i in range(-40,41) if i]:
  if abs(z)>e:
   ck(1<=z*z/(e*e),'counting_intensity_bound')
   ck(abs(z)<=z*z/e,'compensating_drift_bound')
# All three integrability exponents are distinct and have the required signs.
for a in [F(i,40) for i in range(1,20)]:
 ck(2*a-2 < -1,'uniform_series_tail_exponent')
 ck(2*a-1 > -1,'past_derivative_weighted_integrability')
 ck(1-2*a > 0,'smooth_variation_vanishing_exponent')
# Finite endpoint reindexing proves the infinite W function is periodic at 0/1.
for n in range(2,12):
 A=[s.Integer(0)]+list(s.symbols('a1:'+str(n+1)))
 W0=sum((A[i]-A[i-1])**2 for i in range(1,n+1))
 W1=sum((A[i]-A[i-1])**2 for i in range(1,n))
 ck(s.expand(W0-W1-(A[n]-A[n-1])**2)==0,'W_endpoint_partial_sum_identity')
# Cauchy–Schwarz integration bound for the deterministic-time counterexample.
a=s.Rational(1,4);bound=2**(-2*a)+a*a/(1-2*a)*s.Rational(1,2)**(2*a-1)
ck(s.simplify(bound-5/(4*s.sqrt(2)))==0,'nonconstant_phase_exact_upper_bound')
ck(F(25,32)<1,'nonconstant_phase_strict_comparison')
# Deterministic quadratic expansions and truncation comparison, exactly rational.
for n in range(1,21):
 x=[F((i+2)*(n+1)%17-8,7) for i in range(n)]
 y=[F((i+3)*(n+2)%13-6,5) for i in range(n)]
 xx=sum(z*z for z in x);yy=sum(z*z for z in y);xy=sum(z*w for z,w in zip(x,y))
 ck(xy*xy<=xx*yy,'finite_Cauchy_Schwarz')
 ck(sum((z+w)**2 for z,w in zip(x,y))==xx+2*xy+yy,'finite_jump_cross_term_expansion')
 # Reverse norm triangle follows from CS; verify its squared rearrangement.
 target=sum((z-w)**2 for z,w in zip(x,y))
 ck(target==xx+yy-2*xy,'reverse_norm_squared_identity')
# An index-2 Lévy measure can have finite quadratic rate: integrate after x=e^-u.
u=s.symbols('u',positive=True)
ck(s.integrate(2/u**2,(u,1,s.oo))==2,'index_two_finite_quadratic_rate')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),'sympy_version':s.__version__,'scope':'Finite phase-index, compensation, exponent, endpoint and quadratic-algebra controls only. No stable convergence, stochastic Fubini, or point-process theorem is established by sampling.'},indent=2,sort_keys=True))
