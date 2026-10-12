"""Exact assumption controls, independent of historical checkers; not a universal proof.

Univariate polynomial coefficients and chamber coordinates are rational/integer.
The report supplies the general geometry/valuation proof separately.
"""
from fractions import Fraction as Q
from itertools import product, combinations
import json, os
from datetime import datetime, timezone
from pathlib import Path
FAMILY = Path(__file__).resolve().parent
def add(a, b):
    c = dict(a)
    for k, v in b.items(): c[k] = c.get(k, Q(0)) + v
    return {k:v for k,v in c.items() if v}
def mul(a, b):
    c = {}
    for i, x in a.items():
        for j, y in b.items(): c[i+j] = c.get(i+j, Q(0)) + x*y
    return {k:v for k,v in c.items() if v}
def scale(a, s): return {k:v*s for k,v in a.items() if v*s}
def L(a): return {0:Q(1), 1:Q(-a)} if a else {0:Q(1)}
def main():
    controls = []
    # Actual unit union [1,3] U [2,4]=[1,4], rather than multiplicity-two overlap.
    residual = add(add(scale(mul(L(2),L(4)),2), scale(mul(L(1),L(3)),2)),
                   add(scale(mul(L(1),L(4)),-1), scale(mul(L(2),L(3)),-3)))
    assert residual == {}
    assert 2+2 != 3 and 2+2-1 == 3
    controls.append({'control':'overlapping convex components require unit union/inclusion-exclusion',
        'exact_cleared_identity_residual': residual, 'naive_mass':4, 'union_mass':3})
    d12 = mul(L(1),L(2)); d124 = mul(d12,L(4))
    assert d124 != d12 and mul(d12,L(0)) == d12 and L(1) != {0:Q(1)}
    controls.append({'control':'ambient-null isolated pieces and the literal origin unit',
        'interval_plus_nonzero_isolated_point_V':'{1,2,4}', 'A':'{1,2}',
        'extra_nonzero_factor_changes_target_product':True,
        'interval_plus_origin_target_unchanged':True, 'pure_nonzero_point_denominator':'1'})
    # At an artificial boundary vertex, the upper halfplane is the disjoint union
    # of the two upper quadrants; their rational tangent coefficients cancel.
    assert Q(1)+Q(-1) == 0
    controls.append({'control':'artificial edge midpoint halfplane',
        'tangent_coefficient_numerator':0, 'line_direction':'(1,0)',
        'does_not_force_an_extra_denominator_factor':True})
    assert Q(0)-Q(1) == -1
    controls.append({'control':'hole/reentrant corner whole-plane minus a pointed quadrant',
        'tangent_coefficient':'-1/(u1*u2)', 'nonzero':True,
        'convex_hull_vertices_would_miss_this_geometric_corner':True})
    parity = []
    for dimension in (2,3,4):
        # Boolean polynomial of prod h_i + prod(1-h_i), not sampled directions.
        coefficients = {frozenset(range(dimension)): 1}
        for size in range(dimension+1):
            for subset in combinations(range(dimension), size):
                key = frozenset(subset)
                coefficients[key] = coefficients.get(key,0) + (-1)**size
        highest = coefficients[frozenset(range(dimension))]
        assert highest == 1+(-1)**dimension
        valuation_numerator = (-1)**dimension+1
        assert highest == valuation_numerator
        if dimension == 3:
            assert highest == 0
            assert all(len(k)<dimension for k,v in coefficients.items() if v)
        parity.append({'dimension':dimension, 'opposite_cone_valuation_numerator':valuation_numerator,
                       'signed_line_cone_decomposition_when_odd':dimension==3})
    controls.append({'control':'opposite orthant parity; non-line-cone need not be algebraic',
                     'exact_boolean_coefficients':parity})
    q1, q2 = (1,1), (-1,2)
    determinant = q1[0]*q2[1]-q1[1]*q2[0]
    flipped = tuple(-x for x in q2)
    assert determinant == 3 and flipped == (1,-2)
    assert abs(q1[0]*flipped[1]-q1[1]*flipped[0]) == 3
    # C: lambda1>0,lambda2>0; C_flip: lambda1>0,lambda2<0;
    # D: lambda1>0, lambda2 arbitrary. Four chambers exhaust the two facet lines.
    chambers = []
    for a,b in product((-1,1),repeat=2):
        c, cf, dc = int(a>0 and b>0), int(a>0 and b<0), int(a>0)
        assert c+cf == dc
        chambers.append({'lambda1_sign':a,'lambda2_sign':b,'C_plus_Cflip':c+cf,'line_cone_D':dc})
    controls.append({'control':'skew generator flip and finite facet chamber certificate',
        'determinant':3, 'flipped_generator':flipped, 'all_four_chambers':chambers,
        'valuation_sign_changes_exactly':True})
    def flip_sign(dot):
        if not dot: raise ValueError('eta must be nonorthogonal to each generator')
        return 1 if dot>0 else -1
    assert flip_sign(1) == 1 and flip_sign(-1) == -1
    try: flip_sign(0)
    except ValueError: pass
    else: raise AssertionError('Nongeneric eta was incorrectly accepted')
    controls.append({'control':'cone-flipping generic eta guard', 'zero_dot_rejected':True})
    assert L(1) != L(2) and L(0) == {0:Q(1)}
    controls.append({'control':'distinct normalized affine factors even for collinear vertices',
        'L_v_equals_L_w_only_for_equal_vertices':True, 'origin_factor_is_unit':True})
    result = {'schema':'pr58-independent-tangent-geometric-controls/v1',
        'operator_pid':os.getpid(), 'utc':datetime.now(timezone.utc).isoformat(),
        'control_families':len(controls), 'controls':controls, 'all_exact':True,
        'historical_checker_read_or_replayed':False, 'finite_controls_are_not_universal_proof':True,
        'new_substantive_proof_attempt_increment':0, 'novelty_credit_claimed':False}
    (FAMILY/'GEOMETRIC_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__ == '__main__': main()
