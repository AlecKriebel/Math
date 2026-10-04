"""Fresh source-family rational controls. No candidate module is imported.
Written after candidate exposure; finite controls do not prove an LDP.
"""
from fractions import Fraction as F
from itertools import product
from math import isqrt
import json

counts = {}
def require(condition, label):
    if not condition:
        raise AssertionError(label)
    counts[label] = counts.get(label, 0) + 1

def integrate_second_fourth(coefficients, gaussian_variance):
    # Direct addition of independent centered variables, not a CF polynomial.
    second = gaussian_variance
    fourth = 3 * gaussian_variance**2
    for a in coefficients:
        u2, u4 = a*a / 3, a**4 / 5
        fourth = fourth + 6 * second * u2 + u4
        second = second + u2
    return second, fourth

values = [F(-1), F(-3,4), F(-1,2), F(-1,4), F(0), F(1,4), F(1,2), F(3,4), F(1)]
accepted = 0
for coeff in product(values, repeat=4):
    norm2 = sum((a*a for a in coeff), F(0))
    if norm2 > 1:
        continue
    accepted += 1
    a = sorted((abs(x) for x in coeff), reverse=True)
    second, fourth = integrate_second_fourth(coeff, (1-norm2)/3)
    require(second == F(1,3), 'mixed_law_variance')
    require(fourth == F(1,3)-F(2,15)*sum((x**4 for x in coeff), F(0)), 'direct_fourth_moment')
    require(integrate_second_fourth(a,(1-norm2)/3)==(second,fourth), 'sign_sorting_moments')
    require(integrate_second_fourth(tuple(reversed(coeff)),(1-norm2)/3)==(second,fourth), 'permutation_moments')
    require(F(1,5)<=fourth<=F(1,3), 'fourth_moment_range')
    for n in (5,11,27):
        m = isqrt(n)
        prefix = a[:m] + [F(0)]*max(0,m-len(a))
        mass = sum((x*x for x in prefix),F(0))
        r = n-m
        q = (1-mass)/r  # squared filler, roots unnecessary
        b2 = sorted([x*x for x in prefix]+[q]*r, reverse=True)
        require(sum(b2,F(0))==1, 'exact_unit_vectors')
        require(F(0)<=q<=F(1,r), 'filler_maximum_bound')
        require(r*q*q<=F(1,r), 'filler_fourth_error')
        for j in range(m):
            target = prefix[j]**2
            require(target<=b2[j]<=max(target,q), 'rank_interval_including_ties')
        if mass<1:
            wrong_q = (1-mass)/(r+1)
            require(mass+r*wrong_q!=1, 'wrong_filler_denominator_rejected')

# A genuinely infinite l2 sequence with explicit telescoping square masses.
for n in (2,6,17,65,257):
    m=isqrt(n);r=n-m
    for norm2 in (F(0),F(2,5),F(1)):
        squares=[norm2/F(j*(j+1)) for j in range(1,m+1)]
        require(sum(squares,F(0))==norm2*(1-F(1,m+1)), 'infinite_telescoping_prefix')
        q=(1-sum(squares,F(0)))/r
        require(sum(squares,F(0))+r*q==1,'infinite_unit_normalization')
        require(r*q-(1-norm2)==norm2/F(m+1),'exact_missing_mass_error')
        require(r*q*q<=F(1,r),'infinite_filler_fourth_bound')

# Explicit negative controls distinguish norm topology, Gaussian variance, boundary.
for n in (2,7,41):
    require(n*F(1,n)==1,'diffuse_norm_stays_one')
    require(F(1,n)<=F(1,2),'diffuse_coordinate_square_shrinks')
    require(n*F(1,n)**2==F(1,n),'diffuse_fourth_sum')
for s in (F(0),F(1,4),F(7,8)):
    require(s/3+(1-s)!=F(1,3),'missing_variance_without_divisor_rejected')
require(integrate_second_fourth([F(1)],F(0))==(F(1,3),F(1,5)), 'norm_one_uniform_not_deleted')
require(F(1,120)+F(1,69)==F(21,920)<F(1,40),'explicit_log_remainder_constant')
print(json.dumps({'status':'PASS','accepted_signed_vectors':accepted,'assertions':sum(counts.values()),'counts':counts,'arithmetic':'Exact Python standard-library fractions','scope':'Finite signed/permuted moment integration, exhaustive rank intervals, all-N filler normalization, infinite telescoping family, and negative controls. No LDP inference; published Theorem A establishes it.','written_after_candidate_exposure':True},indent=2))
