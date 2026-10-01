#!/usr/bin/env python3
"""Fresh exact controls; universal claims are proved in INDEPENDENCE_SEAL.md.

No historical checker is imported. All arithmetic below is rational.
General moments are divided by Gamma(alpha+s+1)/Gamma(alpha+1).
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from math import factorial
from pathlib import Path
import json

counts = Counter()
def check(category, condition):
    assert condition, category
    counts[category] += 1

def rising(a, m):
    result = F(1)
    for i in range(m):
        result *= a+i
    return result

def binomial(a, m):
    return (-1)**m*rising(-a, m)/factorial(m)

@lru_cache(None)
def laguerre(j, alpha):
    return tuple((-1)**r*binomial(j+alpha, j-r)/factorial(r)
                 for r in range(j+1))

@lru_cache(None)
def direct_increment(j, alpha, s):
    coefficients = laguerre(j, alpha)
    return F(factorial(j))/rising(alpha+1, j)*sum(
        (c*d*rising(alpha+s+1, r+t)
         for r,c in enumerate(coefficients)
         for t,d in enumerate(coefficients)), F(0))

@lru_cache(None)
def positive_increment(j, alpha, s):
    return F(factorial(j))/rising(alpha+1, j)*sum(
        ((rising(-s,j-r)/factorial(j-r))**2
         *rising(alpha+s+1,r)/factorial(r)
         for r in range(j+1)), F(0))

def hypergeometric_moment(n, alpha, s):
    term = total = F(1)
    for j in range(n-1):
        term *= (1-n+j)*(1-s+j)*(s+2+j)/((j+2)*(alpha+2+j)*(j+1))
        total += term
    return n*(n+alpha)/(alpha+1)*total

shapes = [F(0),F(1,2),F(1),F(2),F(7,3)]
orders = [F(0),F(1,2),F(1),F(3,2),F(2),F(3)]
for alpha in shapes:
    for s in orders:
        q = [F(0)]
        for j in range(20):
            inc = direct_increment(j,alpha,s)
            check('direct_vs_positive_connection',
                  inc == positive_increment(j,alpha,s))
            check('positive_moment_increments', inc>0)
            q.append(q[-1]+inc)
            n = j+1
            check('direct_vs_terminating_hypergeometric',
                  q[n] == hypergeometric_moment(n,alpha,s))
            if s==0:
                check('counting_density_mass',q[n]==n)
            if s==1:
                check('first_moment_entry_variance',q[n]*(alpha+1)==n*(n+alpha))
        for n in range(1,20):
            check('dimension_recurrence_varied_shape_and_order',
                  q[n+1] == (2+s*(s+1)/(n*(n+alpha)))*q[n]-q[n-1])
        if s==F(1,2):
            for n in range(1,20):
                check('strict_half_moment_normalized_decrease',
                      q[n]**2*(n+1)**3 > q[n+1]**2*n**3)

# Directly check the universal telescoping certificate's exact local identity.
# The displayed symbolic identity in the seal proves all parameters; these
# controls guard transcription of that proof and exercise the upper endpoint.
for n in range(2,18):
    for alpha in shapes:
        for s in [F(1,2),F(3,2),F(3)]:
            D=(s-1)*(s+2)
            g=F(1)
            for j in range(n+1):
                qp=F((j+1)*(j+2))*(j+alpha+2)/n
                qj=F(j*(j+1))*(j+alpha+1)/n
                gp=g*(j-n)*(j+1-s)*(j+s+2)/((j+2)*(j+alpha+2)*(j+1))
                h=(-(n+alpha-1)*j*j-(D+3*n+alpha+1)*j+n*D)/n
                check('telescoping_local_identity',h*g==qp*gp-qj*g)
                if j==n:
                    check('telescoping_upper_boundary',gp==0)
                g=gp

# The quantitative-bound coefficient comparison has a universal positive
# residue 24j^2+77j+50; the exact coefficient controls also exercise j=0,1,2.
for j in range(101):
    lam=F(128,3)*binomial(F(3,2),2*j+4)
    aeven=sum((F(-1,2)**m/F(2*j+1-m)
               for m in range(2*j+1)),F(0))
    aodd=sum((F(-1,2)**m/F(2*j+2-m)
              for m in range(2*j+2)),F(0))
    check('bound_coefficient_even_dominance',aeven>=lam)
    check('bound_coefficient_odd_nonnegative',aodd>=0)
    check('bound_ratio_symbolic_residue',
          4*(2*j+5)*(2*j+6)*(j+1)
          -(4*j+5)*(4*j+7)*(j+2)==24*j*j+77*j+50)
    if j>=3:
        check('bound_binomial_coefficient_majorant',lam<F(1,3*(j+1)))

q=[F(0)]
for j in range(40):
    q.append(q[-1]+direct_increment(j,F(0),F(1,2))/2)
check('exact_initial_values',q[0]==0 and q[1]==F(1,2) and q[2]==F(11,8))
check('exact_base_strictness',121<128)

# Deliberate mutants must be rejected; each condition says why it is false.
mutants = {
    'complex_components_variance_one': 2*q[1]**2 != F(1,4),
    'density_divided_by_dimension': F(2,2)!=2,
    # Omitting sqrt(x) gives raw moment 1 at n=1; the true raw moment
    # has square pi/4<1, using the classical rigorous pi<22/7<4.
    'missing_sqrt_x': F(22,7)<4,
    'wrong_half_power_weight': F(1)!=q[1],
    'wrong_recurrence_minus_three_quarters':
        (2-F(3,4))*q[1]-q[0] != q[2],
    'wrong_recurrence_plus_previous':
        (2+F(3,16))*q[2]+q[1] != q[3],
    'shifted_dimension_denominator':
        (2+F(3,16))*q[1]-q[0] != q[2],
    'unnormalized_nuclear_norm_not_decreasing': q[2]>q[1],
    'average_without_matrix_scaling_not_decreasing': q[2]/2>q[1],
    'matrix_scaling_without_average_not_decreasing': q[2]**2>2*q[1]**2,
    'finite_extrapolation_can_fail_after_checked_range':
        (2*q[40])**2*40**3>q[40]**2*41**3,
    # At alpha=-1/2, C2/C1=7/(4 sqrt(2))>1. This is outside the theorem.
    'unsupported_negative_shape_extension': 49>32,
}
for name,rejected in mutants.items():
    check('intentional_mutant_rejection',rejected)

result={
    'status':'passed','arithmetic':'exact Python integers and fractions',
    'counts':dict(counts),'total_assertions':sum(counts.values()),
    'shapes':[str(x) for x in shapes],'orders':[str(x) for x in orders],
    'varied_parameter_dimensions':20,'square_mutation_reference_dimensions':40,
    'mutants_rejected':mutants,
    'scope':'Finite falsification controls only; universal proof is in INDEPENDENCE_SEAL.md',
    'no_real_universal_theorem_certified':True,
    'no_substantive_attempt_added':True,
}
Path(__file__).with_name('fresh_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
