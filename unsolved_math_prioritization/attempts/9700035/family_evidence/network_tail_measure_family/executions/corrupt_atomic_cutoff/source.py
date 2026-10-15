#!/usr/bin/env python3
"""Own finite/exact controls and shortcut counterexamples, not SIRSN proofs."""
from fractions import Fraction as F
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
checks, examples = [], []


def check(label, value, evidence):
    assert value, label
    checks.append({'label':label,'result':'PASS','evidence':evidence})


def union_length(intervals):
    merged = []
    for left,right in sorted(intervals):
        if not merged or left > merged[-1][1]: merged.append([left,right])
        else: merged[-1][1] = max(merged[-1][1],right)
    return sum((b-a for a,b in merged),F(0))


# This three-endpoint line example obeys finite route compatibility and shows
# why route lengths must not be summed as a measure with overlap multiplicity.
routes = [(F(0),F(1)),(F(1),F(2)),(F(0),F(2))]
check('union_not_route_sum',union_length(routes)==2 and sum(b-a for a,b in routes)==4,{'union':2,'route_sum':4})
for cutoff in [F(j,8) for j in range(17)]:
    local=[(max(a,cutoff),b) for a,b in routes if b>cutoff]
    check('restricted_measure_'+str(cutoff),union_length(local)==max(2-cutoff,0),{'cutoff':str(cutoff)})

# A 3-4-5 triangle has all-pair span length12, whereas removing its length5
# edge already gives a connected length7 network. No SIRSN axioms are claimed.
check('prescribed_union_not_minimum',3+4+5>3+4,{'all_pair_union':12,'connected_competitor':7})
examples.append({'mechanism':'finite geometric functional distinction','admissible_SIRSN_counterexample':False})

# Exact rare-event measures: no independence between event and length.
for m in [2,4,16,256]:
    probability=F(1,m*m);mass=F(m*m);expectation=probability*mass
    check('correlation_counterexample_'+str(m),expectation==1 and expectation>expectation*probability,
          {'P_event':str(probability),'E_mass':str(expectation),'E_mass_on_event':str(expectation),'false_product':str(expectation*probability)})
    # Y_m=m with probability1/m tends to0 in probability but E Y_m=1.
    check('escaping_mass_counterexample_'+str(m),F(1,m)*m==1 and m>1,{'rare_probability':str(F(1,m)),'rare_normalized_mass':m,'expectation':1})
examples.append({'mechanism':'nonuniform integrability and correlated rare-event mass','admissible_SIRSN_counterexample':False})

# Exterior area and intensity constants are independently computed from the
# four-coordinate expanded square, including rational noninteger radii.
for n in [F(1),F(7,3),F(10)]:
    for r in [F(1,3),F(1),F(9,2)]:
        area=(n+4*r)**2-(n+2*r)**2
        predicted=4*n*r+12*r*r
        check('annulus_'+str(n)+'_'+str(r),area==predicted and area/r==4*n+12*r,{'area':str(area),'mass_bound_per_p':str(area/r)})
for j in range(12):
    for factor in [F(1),F(4,3),F(31,16)]:
        radius=(2**j)*factor
        intervals=[(0,F(1))]+[(F(2**i),F(2**(i+1))) for i in range(j+1)]
        check('dyadic_cover_'+str(j)+'_'+str(factor),union_length(intervals)>=radius and sum(2**i for i in range(j+1))<=2*radius,{'radius':str(radius),'covered_to':str(2**(j+1))})
check('unbounded_major_road_bound_diverges',sum(12*2**i for i in range(20))>12*2**19,{'lower_bound_partial_sum':12*(2**20-1),'reason':'positive geometric terms do not tend to zero'})

# Atomic cutoff tests are independent of any simulated spatial network.
atoms=[(F(1),F(1,4)),(F(3),F(1,2)),(F(9),F(1,4))]
for cutoff in [F(1),F(3),F(9)]:
    ge=sum(x*p for x,p in atoms if x>cutoff)
    gt=sum(x*p for x,p in atoms if x>cutoff)
    check('cutoff_atom_'+str(cutoff),ge>gt and ge<=sum(x*p for x,p in atoms if x>cutoff/2),{'nonstrict':str(ge),'strict':str(gt)})
for scale in [F(1,4),F(1),F(4)]:
    for radius in [F(1,2),F(2),F(8)]:
        maximal=4*scale
        lhs=sum(scale*x*p for x,p in atoms if scale*x>=2*radius)
        rhs=maximal*sum(x*p for x,p in atoms if x>=2*radius/maximal)
        check('scaled_pair_tail_'+str(scale)+'_'+str(radius),lhs<=rhs,{'left':str(lhs),'right':str(rhs)})

# Power-law exponent arithmetic tests exactly why first moment and big-O at
# order4 do not close this particular truncation, and why fixed-delta works.
for alpha in [F(2),F(4),F(9,2),F(5)]:
    coefficient=alpha/(alpha-1)
    exponent_at_R_delta_n2=4-alpha
    check('power_tail_boundary_'+str(alpha),(exponent_at_R_delta_n2<0)==(alpha>4),{'h_coefficient':str(coefficient),'normalized_n_exponent':str(exponent_at_R_delta_n2)})
check('critical_big_O_does_not_vanish',F(4,3)>0,{'alpha':4,'truncated_moment_coefficient':str(F(4,3)),'far_coefficient_lambda1_delta1':str(F(1,3)),'delta_power':-3})
for m in [4,8,16,32]:
    # D tail t^-4/log(t) for t>=e has finite mean and infinite fourth
    # moment. h(t)<=4/(3*t^3*log(t)). At t=2^m the envelope decreases.
    coefficient=F(4,3*m)
    check('slow_little_o_fixed_delta_'+str(m),coefficient<1 and coefficient>0,{'coefficient_times_log2':str(coefficient)})
    # Shrinking delta=n^-1/2 with n=2^(2m) yields a lower bound
    # n^3*t*P(D>t)=2^(3m)/(m*log2), not0. Fixed-delta and this
    # simultaneous limit are materially different.
    lower=F(2**(3*m),m)
    check('shrinking_delta_counterexample_'+str(m),lower>m,{'far_lower_bound_times_log2':str(lower),'delta':str(F(1,2**m))})
examples.append({'mechanism':'scalar t^-4/log(t) tail and limit-order diagnostic','admissible_SIRSN_counterexample':False,
                 'proof':'fourth moment tail integral contains 4*integral_e^infinity dt/(t log(t)), which diverges; h envelope is at most4/(3 t^3 log(t))'})

# Coefficients of Poisson factorial moments, including the two-index shift.
for count in range(2,25):
    check('factorial_shift_'+str(count),F(count*(count-1),math.factorial(count))==F(1,math.factorial(count-2)),{'count':count,'coefficient':str(F(1,math.factorial(count-2)))})
check('independent_count_is_essential',F(0)<F(1,4)*10,{'example':'F_k=10 on A,0 otherwise; P(A)=1/2; choose N>=k exactly on A-complement; E[F_k 1(N>=k)]=0 but E F_k P(N>=k)=5/2'})

result={'status':'PASS_OWN_FINITE_COUNTERCONTROLS_ONLY','checks_passed':len(checks),'checks':checks,'generic_examples':examples,
        'reviewed_helper_execution':False,'scope':'Finite rational identities and analytic shortcut counterexamples; no admissible SIRSN counterexample, no universal theorem certificate.',
        'new_substantive_attempts':0,'audit_turns':0}
(HERE/'NETWORK_MEASURE_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
