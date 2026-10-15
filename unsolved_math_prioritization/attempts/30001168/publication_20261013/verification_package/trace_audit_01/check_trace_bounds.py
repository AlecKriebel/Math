#!/usr/bin/env python3
"""Independent exact trace-family witness; stdlib, no source imports.

Analytic obligations are in REPORT.md. This checks their finite rational
inequalities and deliberate false alternatives under normal or -O execution.
"""
from fractions import Fraction as R
from math import factorial
import json
import sys


def demand(condition, reason):
    if not condition:
        raise ValueError(reason)


def atan_bracket(x):
    # 24 terms, last negative, and next positive term: integration of the
    # finite geometric expansion of 1/(1+x^2) proves the same brackets.
    low = sum(((-1)**k*x**(2*k+1)/(2*k+1) for k in range(24)), R(0))
    return low, low+x**49/49


def positive_exponential_bracket(x, degree):
    demand(0 <= x < degree+2, 'Taylor upper-tail ratio range')
    low = sum((x**k/factorial(k) for k in range(degree+1)), R(0))
    first = x**(degree+1)/factorial(degree+1)
    return low, low+first/(1-x/(degree+2))


def sqrt_bracket(x):
    # Search on an integer lattice; all branching comparisons are integers.
    scale = 10**8
    left, right = 0, 2*scale
    while right-left > 1:
        middle = (left+right)//2
        if middle*middle*x.denominator <= x.numerator*scale*scale:
            left = middle
        else:
            right = middle
    low, high = R(left,scale), R(right,scale)
    demand(low*low <= x < high*high, 'root enclosure')
    return low, high


def exp_negative_upper(x):
    demand(x > 0, 'positive reciprocal exponential argument')
    return 1/positive_exponential_bracket(x,50)[0]


def first_upper(t):
    return t*sqrt_bracket(t)[1]*exp_negative_upper(3*t/4)


def remaining_upper(t):
    demand(t >= R(7,5), 'modal-tail time range')
    demand(R(16,9)/(1+7*t) < R(1,2), 'j>=3 geometric ratio')
    return t*sqrt_bracket(t)[1]*(4*exp_negative_upper(15*t/4)
                              +18*exp_negative_upper(35*t/4))


def frac(x):
    return f'{x.numerator}/{x.denominator}'


def decimal_upper(x):
    scale = 10**15
    k = x.numerator*scale//x.denominator+1
    return f'{k//scale}.{k%scale:015d}'


def calculate(round_limit=R(321,500), length=10000):
    # 2 atan(1/3)+atan(1/7)=pi/4: tan(2 atan(1/3))=3/4;
    # tan addition then gives 1, with all angles in the first quadrant.
    p, q = atan_bracket(R(1,3)), atan_bracket(R(1,7))
    pi_low, pi_high = 8*p[0]+4*q[0], 8*p[1]+4*q[1]
    demand(R(157,50)<pi_low<pi_high<R(22,7), 'pi enclosure')
    sqrt_low, sqrt_high = R(1772,1000), R(1773,1000)
    demand(sqrt_low**2<pi_low and pi_high<sqrt_high**2, 'sqrt pi enclosure')
    e_upper = positive_exponential_bracket(R(1),14)[1]
    demand(e_upper<R(2719,1000), 'e enclosure')
    demand(2*pi_low**2>R(7,5), 'negative Poisson correction through 7/5')
    small_upper = sqrt_high*positive_exponential_bracket(R(7,20),14)[1]/4
    demand(small_upper<round_limit, 'small-time bound')
    endpoints = [R(k,10) for k in range(14,21)]
    rows = []
    for a,b in zip(endpoints,endpoints[1:]):
        value = first_upper(b)+remaining_upper(a)
        demand(value<round_limit, f'round middle interval {a}..{b}')
        rows.append({'a':str(a),'b':str(b),'bound_exact':frac(value),
                     'bound_decimal_upper':decimal_upper(value)})
    # At t>=2 all modes decrease; the last closed interval covers 2.
    demand(endpoints[0]==R(7,5) and endpoints[-1]==2 and len(rows)==6,
           'complete interval coverage')
    lower = sqrt_low/R(2719,1000)*(length-4*sqrt_high)/(length+4)
    demand(length>4*sqrt_high, 'positive cylinder lower numerator')
    demand(lower>R(13,20), 'cylinder strict threshold')
    demand(R(13,20)>R(129,200)>round_limit, 'target threshold separation')
    first_two_low = 2*sqrt_bracket(R(2))[0]/positive_exponential_bracket(R(3,2),14)[1]
    demand(first_two_low>sqrt_high/4, 'round maximum exceeds Weyl limit')
    demand(lower>sqrt_high/4, 'weighted maximum exceeds Weyl limit')
    return {'accepted':True,'problem_id':30001168,'dimension':3,
            'round_stronger_uniform_threshold':frac(round_limit),
            'small_time_bound_exact':frac(small_upper),
            'small_time_upper_decimal':decimal_upper(small_upper),
            'middle_intervals':rows,
            'all_region_upper_decimal':decimal_upper(max([small_upper]+[
                first_upper(b)+remaining_upper(a)
                for a,b in zip(endpoints,endpoints[1:])])),
            'cylinder_length':length,'cylinder_lower_exact':frac(lower),
            'cylinder_lower_minus_13_over_20':frac(lower-R(13,20)),
            'round_first_at_two_lower_exact':frac(first_two_low),
            'arithmetic':'Integers and Fraction only; mathematical obligations separately documented'}


if __name__=='__main__':
    demand(len(sys.argv)==1, 'No arguments accepted')
    print(json.dumps(calculate(),indent=2,sort_keys=True))
