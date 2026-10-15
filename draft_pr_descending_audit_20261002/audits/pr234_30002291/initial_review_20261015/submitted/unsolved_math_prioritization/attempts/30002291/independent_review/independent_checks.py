"""Independent exact analytic-identity controls; not a stochastic proof."""
from collections import Counter
from fractions import Fraction as F
import json
import sympy as s
C=Counter()
def ck(v,k):
    assert v,k
    C[k]+=1

# An independently selected non-Poisson count: rates 1, 2, 0 after 0,1,2 jumps.
# Ordered two-jump density on 0<a<b<T is 2 exp(a-2b).
a,b,T=s.symbols('a b T',positive=True)
p2=s.integrate(s.integrate(2*s.exp(a-2*b),(a,0,b)),(b,0,T))
p1=s.integrate(s.exp(-a)*s.exp(-2*(T-a)),(a,0,T))
p0=s.exp(-T)
ck(s.simplify(p2-(1-s.exp(-T))**2)==0,'non_Poisson_two_time_density_mass')
ck(s.simplify(p0+p1+p2-1)==0,'non_Poisson_count_mass')
ck(s.simplify(p1-(s.exp(-T)-s.exp(-2*T)))==0,'non_Poisson_one_time_mass')

# Exact Fourier transforms of this simplex density. Integer frequencies make
# endpoint exponentials one, giving a rational expression in the frequency n.
n=s.symbols('n',positive=True)
for qa,qb in [(0,1),(1,0),(1,1),(1,-1),(2,-3),(-2,3)]:
    A=2*s.pi*qa*n;B=2*s.pi*qb*n
    I=2/(1+s.I*A)*((s.exp(-1)-1)/(-1+s.I*(A+B))-
                         (s.exp(-2)-1)/(-2+s.I*B))
    ck(s.limit(I,n,s.oo)==0,'non_Poisson_phase_Fourier_decay')

# Coarea/Fubini triangle identity for test densities exp(-r*x), derived both ways.
r=s.symbols('r',positive=True)
u,x=s.symbols('u x',nonnegative=True)
# Use explicit antiderivatives to avoid a SymPy Piecewise-recursion issue at u=0.
F0=-s.exp(-r*x)/r
F1=-s.exp(-r*x)*(r*x+1)/r**2
ck(s.simplify(s.diff(F0,x)-s.exp(-r*x))==0,'exponential_antiderivative')
ck(s.simplify(s.diff(F1,x)-x*s.exp(-r*x))==0,'weighted_exponential_antiderivative')
left=(1-s.exp(-r*T))/r**2
right=(1-s.exp(-r*T)*(1+r*T))/r**2+T*s.exp(-r*T)/r
ck(s.simplify(left-right)==0,'prehistory_min_weight_identity')

# Independent rational witnesses of the three endpoint exponents.
for aa in [F(j,102) for j in range(1,51)]:
    ck(2*aa-1>-1,'prehistory_local_integrability')
    ck(aa-1>-1,'drift_derivative_integrability')
    ck(2*aa-2<-1,'single_impulse_tail_summability')
    ck(1-2*aa>0,'AC_variation_decay')

# General Lévy index-two rate and the remaining small-jump variance exactly.
L=s.symbols('L',positive=True)
q=s.symbols('q',positive=True)
ck(s.integrate(2/q**2,(q,L,s.oo))==2/L,'index_two_small_jump_rate')
ck(s.limit(2/L,L,s.oo)==0,'index_two_small_jump_vanishes')

# Uniform phases at opposite indexing conventions, with arbitrary symbolic data.
A=s.symbols('a0:14')
for m in range(2,13):
    old=sum((A[j+1]-A[j])**2 for j in range(m))
    renamed=sum((A[j]-A[j-1])**2 for j in range(1,m+1))
    ck(s.expand(old-renamed)==0,'prior_theorem_phase_reindexing')

# Tail bound at alpha=1/4 used to separate deterministic and uniform phases.
bound=s.sqrt(s.Rational(1,2))+s.sqrt(2)/8
ck(s.simplify(bound**2-s.Rational(25,32))==0,'deterministic_phase_separation_square')
ck(F(25,32)<1,'deterministic_phase_separation_strict')

print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),
 'counts':dict(sorted(C.items())),
 'scope':'Independent finite integral, Fourier, exponent, phase and truncation identities. Analytic all-process arguments are assessed in INDEPENDENT_REVIEW.md; these controls do not establish stable convergence by sampling.'},sort_keys=True,indent=2))
