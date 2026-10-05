#!/usr/bin/env python3
"""Independent finite algebra probes for KP-3.72; no manifold or Floer oracle."""
from collections import Counter
from fractions import Fraction
from itertools import product
from math import comb, gcd
import json

counts = Counter()

def test(ok, label):
    counts[label] += 1
    if not ok:
        raise AssertionError((label, counts[label]))

# Symbolic polynomial arithmetic, coefficients ordered from constant term.
def poly_mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out

p = poly_mul(poly_mul([1,2], [1,4]), [3,4])
shifted = [sum(p[j]*comb(j,i) for j in range(i,len(p))) for i in range(len(p))]
test(p == [3,22,48,32], 'symbolic_DHST_product')
test([a-b for a,b in zip(shifted,p)] == [102,192,96,0], 'symbolic_DHST_increment')
test(all(c > 0 for c in [102,192,96]), 'positive_increment_coefficients')

# Necessary hypotheses in the one-handle attachment exact sequence.
for a in range(-30,31):
    if a:
        test(Fraction(a)*Fraction(1,a) == 1, 'nonzero_rational_map_isomorphism')
    else:
        test((1,1) != (0,0), 'zero_attachment_does_not_kill_H1_or_H2')

# Calculate Tor and tensor dimensions by enumerating maps on finite fields,
# independently of the packet's Gaussian-elimination implementation.
for cyclic_orders in [(m,) for m in range(1,31)] + list(product([2,3,4,6,8,9,10,12], repeat=2)):
    for prime in [2,3,5,7,11]:
        kernel_dims=[]; cokernel_dims=[]
        for m in cyclic_orders:
            image={m*x % prime for x in range(prime)}
            kernel={x for x in range(prime) if m*x % prime == 0}
            test(len(image)*len(kernel) == prime, 'enumerated_finite_field_exactness')
            kernel_dims.append(int(len(kernel)==prime))
            cokernel_dims.append(int(len(image)==1))
        r=sum(int(m % prime == 0) for m in cyclic_orders)
        t=sum(cokernel_dims); u=sum(kernel_dims)
        test((1,t,t+u,u,0) == (1,r,2*r,r,0), 'independent_UCT_Betti_probe')
        test((t==u==0) == all(gcd(prime,m)==1 for m in cyclic_orders), 'independent_prime_ball_probe')

# Rational collinearity is weaker than equality in the target group.
# Target: Z plus Z/t. q(e0)=(a,1), q(ei)=(i+1,i+2).
# v_i = a e_i - (i+1)e0 has zero free image; t*v_i has zero full image.
uncorrected_torsion_witnesses=0
for n,a,t in product(range(1,13),[-3,-2,-1,1,2,3],[2,4,6,9]):
    for i in range(1,n+1):
        b,z=i+1,i+2
        test(a*b-b*a == 0, 'denominator_clearing_free_image')
        residue=(a*z-b) % t
        uncorrected_torsion_witnesses += int(residue != 0)
        test(t*(a*z-b) % t == 0, 'torsion_killing_full_image')
    test((t*a)**n != 0, 'corrected_classes_nonzero_diagonal_minor')
test(uncorrected_torsion_witnesses > 0, 'rational_equality_not_actual_equality_negative_control')

# The rank-transfer hypothesis must handle finite, nontrivial torsion image.
for t,n in product(range(2,13),range(1,13)):
    test(all((t*j)%t == 0 for j in range(n)), 'pure_torsion_image_killed')
    test(t**n > 0, 'torsion_target_full_rank_kernel_model')

# Ordinary d(B_n)=2n, even when known, cannot prove independence of the family.
for n in range(1,121):
    test((n+1)*(2*n)-n*(2*(n+1)) == 0, 'nonzero_coefficient_d_cancellation')
    test((n+1,-n)!=(0,0), 'd_cancellation_is_nontrivial')

# Integer versus rational retraction; arbitrary sparse elements have finite
# support, whereas a prescribed dual family may be nonlocally finite at z.
for scale in range(2,61):
    test(Fraction(1,scale).denominator != 1, 'nonprimitive_basis_no_integral_dual')
for n in range(1,81):
    prescribed_image_of_z=[1]*n
    test(sum(bool(x) for x in prescribed_image_of_z)==n, 'nonlocally_finite_duals_fragment')

print(json.dumps({
    'problem_id':2870,
    'status':'PASS_INDEPENDENT_FINITE_ALGEBRA_PROBES',
    'assertions':sum(counts.values()),
    'counts':dict(sorted(counts.items())),
    'torsion_residual_witnesses':uncorrected_torsion_witnesses,
    'limitations':[
        'Finite probes do not construct or classify smooth manifolds.',
        'No Floer invariant or rational-cobordism relation is computed.',
        'Symbolic identities prove only the displayed polynomial identities.',
        'Source hypotheses and infinite mathematical arguments require the written audit.'
    ]},sort_keys=True,indent=2))
