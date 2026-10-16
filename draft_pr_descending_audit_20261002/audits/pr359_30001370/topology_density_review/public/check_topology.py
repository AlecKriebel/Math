#!/usr/bin/env python3
"""Independent exact rough-law constructions, not a finite proof of the theorem.

Only Python's standard library is used. The script writes no files.
Use t=x+1/2 on [0,1], so centered doubling is D(t)=2t mod 1.
"""
from fractions import Fraction as Q
from math import comb
import json

checks = {}


def ck(category, value):
    if not value:
        raise AssertionError(category)
    checks[category] = checks.get(category, 0) + 1


flat_cases = []
for delta in (Q(1, 16), Q(1, 64), Q(1, 1000)):
    edges = [Q(0), Q(1, 2)-delta, Q(1, 2)+delta, Q(1)]
    heights = [1/(1-2*delta), Q(0), 1/(1-2*delta)]
    cumulative = [Q(0)]
    for a, b, h in zip(edges, edges[1:], heights):
        cumulative.append(cumulative[-1]+(b-a)*h)
    ck('cdf_mass', cumulative[-1] == 1)
    ck('cdf_symmetry', cumulative[1]+cumulative[2] == 1)
    for depth in (1, 2, 4, 8):
        cylinders = 2**depth
        mass = Q(0)
        field = Q(0)
        variation = Q(0)
        displacement = Q(0)
        last_image = Q(0)
        flat_mass = Q(0)
        for k in range(cylinders):
            for i, h in enumerate(heights):
                a, b = (k+edges[i])/cylinders, (k+edges[i+1])/cylinders
                ha, hb = (k+cumulative[i])/cylinders, (k+cumulative[i+1])/cylinders
                ck('gluing', ha == last_image)
                ck('monotonicity', hb >= ha)
                ck('derivative', hb-ha == (b-a)*h)
                if h:
                    ck('push_density', h*(b-a)/(hb-ha) == 1)
                else:
                    flat_mass += h*(b-a)
                    ck('flat_no_atom', ha == hb and h*(b-a) == 0)
                last_image = hb
                mass += h*(b-a)
                field += h*((b*b-a*a)/2-(b-a)/2)
                variation += abs(h-1)*(b-a)
                displacement = max(displacement, abs(ha-a), abs(hb-b))
        ck('full_law', mass == 1 and last_image == 1)
        ck('feedback_zero', field == 0)
        ck('variation', variation == 4*delta)
        ck('displacement', displacement == delta/cylinders)
        ck('flat_no_atom', flat_mass == 0)
        flat_cases.append({'delta':str(delta), 'depth':depth,
                           'epsilon':str(variation),
                           'sup_displacement':str(displacement),
                           'initial_corrected_density':'1',
                           'all_feedback_parameters':'0'})

# A nonuniform conditional branch allocation, with a genuinely zero output
# region and a target putting all of its mass on that old zero region.
edges = [Q(0),Q(1,5),Q(2,5),Q(1)]
out = [Q(0),Q(5,4),Q(5,4)]
target = [Q(5),Q(0),Q(0)]
allocation = [Q(1),Q(1,3),Q(7,4)]
mass = lift_mass = section_difference = target_difference = Q(0)
for a,b,v,z,qa in zip(edges,edges[1:],out,target,allocation):
    qb=2-qa
    wa,wb=qa*v,qb*v
    ck('positive_section', 0<=qa<=2 and 0<=qb<=2)
    ck('positive_section', (wa+wb)/2 == v)
    ck('positive_section', (qa*z+qb*z)/2 == z)
    ck('zero_fiber', v != 0 or (wa == wb == 0 and qa == qb == 1))
    mass += (b-a)*(wa+wb)/2
    lift_mass += (b-a)*(qa*z+qb*z)/2
    section_difference += (b-a)*(abs(qa*z-wa)+abs(qb*z-wb))/2
    target_difference += (b-a)*abs(z-v)
ck('positive_section', mass == lift_mass == 1)
ck('positive_section', section_difference == target_difference == 2)

# Integrable unbounded symmetric density w(x)=1/(2 sqrt(2|x|)).
# Put x=s^2/2 on the positive half. For w_theta=(1-theta)+theta*w,
# J_theta(x)=((1-theta)*s^2+theta*s)/2. Moments use only rational
# polynomial integrals, and verify exact pushforward on this half.
unbounded_cases = []
for theta in (Q(1), Q(1,10), Q(1,1000)):
    aa,bb=(1-theta)/2,theta/2
    for degree in range(7):
        # J^degree * dJ/ds, integrated from 0 to 1.
        integral=Q(0)
        for i in range(degree+1):
            coeff=Q(comb(degree,i))*aa**i*bb**(degree-i)
            power=degree+i
            integral += coeff*(2*aa/Q(power+2)+bb/Q(power+1))
        ck('unbounded_transport_moment', integral == Q(1,2)**(degree+1)/Q(degree+1))
    # Full variation = four times the positive-half excess on s in [0,1/2].
    epsilon=4*theta*(Q(1,2)*Q(1,2)-Q(1,2)**2/2)
    ck('unbounded_variation', epsilon == theta/2)
    ck('unbounded_endpoint', aa+bb == Q(1,2))
    unbounded_cases.append({'theta':str(theta),'epsilon':str(epsilon),
                            'density':'(1-theta)+theta/(2 sqrt(2|x|))',
                            'finite_preimage_construction':'u=w_theta composed with T0^n; Hprime=u; corrected law=1'})

# D0 cannot approximate the rough symmetric neutral endpoint density.
support_length=Q(1,4)
maximum_core_mass=2*support_length
ck('core_non_density', 2*(1-maximum_core_mass) == 1)

print(json.dumps({'status':'PASS','exact_assertions':sum(checks.values()),
                  'categories':checks,'flat_cumulative_cases':flat_cases,
                  'unbounded_analytic_cases':unbounded_cases,
                  'core_neutral_distance_lower_bound':'1',
                  'scope':'Exact finite piecewise constructions and polynomial integrals support the independent analytic rough-density audit; they do not establish the infinite-dimensional theorem by sampling.'},sort_keys=True,indent=2))
