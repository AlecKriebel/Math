#!/usr/bin/env python3
"""Independent exact controls for the conditional 9700035 proof."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json, math
import sympy as s
checks={}
def ck(name,value):
    assert bool(value),name
    checks[name]="PASS"

n,r,R,lam,d,t,eta=s.symbols("n r R lam d t eta",positive=True)
ck("annular_area",s.expand((n+4*r)**2-(n+2*r)**2)==4*n*r+12*r*r)
ck("unit_strip",s.expand((n+2)**2-n*n)==4*n+4)
ck("poisson_pair_coefficient",s.simplify(s.sqrt(2)*n*(lam*n*n)**2/2-lam**2*n**5/s.sqrt(2))==0)
tail=s.simplify(lam**2*n**5/s.sqrt(2)*eta/(s.sqrt(2)*d*n)**3/n**2)
ck("normalized_far_constant",tail==lam**2*eta/(4*d**3))
ck("normalized_near_limit",s.limit((4*n*(1+s.log(d*n*n,2))+24*d*n*n)/n**2,n,s.oo)==24*d)
ck("fixed_delta_far_little_o_model",s.limit(n**3/(d*n)**4,n,s.oo)==0)
ck("little_o_is_essential",s.simplify(n**3/(d*n)**3)==d**-3)

# Tile counting has an O_r(n) boundary loss and does not require integer n.
tile_cases=0
for a in (F(1),F(3,2),F(2),F(13,4)):
    for N in (F(4),F(11,2),F(10),F(41,2),F(100)):
        if N<a:continue
        count=(2*math.floor((N-a)/2)+1)**2
        # |sqrt(count)-N| <= a+1; |count-N²| <= (a+1)(2N+a+1).
        ck(f"tile_count_{tile_cases}",abs(count-N*N)<=(a+1)*(2*N+a+1))
        tile_cases+=1

annuli_cases=0
for j in range(14):
    for f in (F(1),F(5,4),F(3,2),F(15,8)):
        radius=(2**j)*f
        ck(f"annulus_cover_{annuli_cases}",2**j<=radius<2**(j+1))
        ck(f"annulus_sum_{annuli_cases}",sum(2**i for i in range(j+1))<=2*radius)
        annuli_cases+=1

# Check the exact index shift, including k=0,1, with finite polynomial sums.
mu=s.symbols("mu")
for k in range(10):
    left=sum(m*(m-1)*mu**m/s.factorial(m) for m in range(13) if m>k)
    right=mu**2*sum(mu**j/s.factorial(j) for j in range(11) if j>k-2)
    ck(f"factorial_tail_index_{k}",s.expand(left-right)==0)

# Arbitrary monotone sequences satisfying F_m <= binom(m,2), with independent
# finitely supported counts. This checks the sandwich logic, not a Poisson model.
sandwich_cases=0
M=5
laws=[
 [F(1,6)]*6,
 [F(i+1,21) for i in range(6)],
 [F(6-i,21) for i in range(6)]
]
for increments in product(*[range(m) for m in range(2,M+1)]):
    values=[0,0]
    for inc in increments:values.append(values[-1]+inc)
    assert all(values[m]<=m*(m-1)/2 for m in range(6))
    for probs in laws:
        expectation=sum(probs[m]*values[m] for m in range(6))
        for k in range(1,6):
            p_upper=sum(probs[m] for m in range(k,6))
            ck(f"upper_sandwich_{sandwich_cases}",p_upper*values[k]<=expectation)
            excess=sum(probs[m]*F(m*(m-1),2) for m in range(k+1,6))
            ck(f"lower_sandwich_{sandwich_cases}",expectation<=values[k]+excess)
            sandwich_cases+=1

# Atomic distributions test >= cutoff and the uniform endpoint-distance bound.
atoms=[(F(1),F(1,2)),(F(2),F(1,3)),(F(4),F(1,6))]
pair_cases=0
for A in (F(1),F(2),F(5)):
    for c in (A/4,A/2,A):
        for radius in (F(1,4),F(1,2),F(1),F(2),F(4)):
            lhs=sum(prob*c*v for v,prob in atoms if c*v>=2*radius)
            rhs=A*sum(prob*v for v,prob in atoms if v>=2*radius/A)
            ck(f"pair_tail_{pair_cases}",lhs<=rhs);pair_cases+=1
for cutoff in (F(1),F(2),F(4)):
    h_ge=sum(v*p for v,p in atoms if v>=cutoff)
    h_gt=sum(v*p for v,p in atoms if v>cutoff)
    jump=sum(p for v,p in atoms if v==cutoff)
    ck(f"atomic_jump_{cutoff}",h_ge-h_gt==cutoff*jump)
    ck(f"half_cutoff_{cutoff}",h_ge<=sum(v*p for v,p in atoms if v>cutoff/2))

# Scalar tails do not by themselves certify realizability by a SIRSN.
for alpha in (s.Rational(2),s.Rational(4),s.Rational(9,2),s.Rational(5)):
    h=alpha*t**(1-alpha)/(alpha-1)
    ck(f"pareto_differentiated_layercake_{alpha}",s.simplify(s.diff(h,t)+alpha*t**(-alpha))==0)
    ck(f"pareto_threshold_{alpha}",(s.limit(t**3*h,t,s.oo)==0)==(alpha>4))
ck("finite_mean_tail_countercontrol",s.integrate(2*t**(-2),(t,1,s.oo))==2)

result={
 "passed":len(checks),"failed":0,"sympy_version":s.__version__,
 "tile_cases":tile_cases,"dyadic_cases":annuli_cases,
 "monotone_sandwich_cases":sandwich_cases,"atomic_pair_tail_cases":pair_cases,
 "scope":"Exact algebra and finite-law controls. No SIRSN simulation, no proof of the unconditional target, and no numerical substitute for exhaustion or limiting arguments.",
 "checks":checks
}
Path(__file__).with_name("independent_results.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k!="checks"},indent=2))
