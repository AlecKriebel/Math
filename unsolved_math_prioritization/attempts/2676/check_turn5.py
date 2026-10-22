"""Exact algebraic controls for the family-scoped branching-rigidity proof.
The topological classification inputs are stated and sourced in TURN_5.md;
this script does not claim to recognize manifolds, links, or involutions.
"""
from collections import Counter
from itertools import product
from math import gcd
import json
import sympy as s
from sympy.matrices.normalforms import smith_normal_form

C = Counter()


def ck(ok, label):
    assert ok, label
    C[label] += 1


r = s.symbols('r', integer=True)
p = r*(r+1)-1
A = s.Matrix([[r+1, -p], [1, -r]])
ck(s.expand(A.det()) == -1, 'symbolic_orientation_reversing_determinant')
ck(A.trace() == 1, 'symbolic_trace_one')
ck((A*A-A-s.eye(2)).applyfunc(s.expand) == s.zeros(2), 'symbolic_cayley_hamilton_identity')
ck(s.expand((A*A)[1, 0]) == 1, 'symbolic_no_piece_exchange_peripheral_matrix')
fiber = A*s.Matrix([6, 1])
ck(s.expand(fiber[0]-6*fiber[1]) == -r*r+11*r-29, 'symbolic_fiber_mismatch_polynomial')
ck(5 not in {i*i % 8 for i in range(8)}, 'discriminant_five_not_integer_square')
ck(s.expand(4*(-r*r+11*r-29)+(2*r-11)**2) == 5,
   'fiber_mismatch_nonzero_all_integers')
z = s.symbols('z')
ck(s.cancel(((r+1)*z-p)/(z-r)-(r+1+1/(z-r))) == 0, 'symbolic_slope_formula')

examples = []
for n in range(2, 502):
    order = n*(n+1)-1
    M = s.Matrix([[n+1, -order], [1, -n]])
    ck(order % 2 == 1 and order >= 5, 'odd_nontrivial_homology_order')
    ck(gcd(n+1, order) == 1, 'both_piece_meridians_generate_cover_homology')
    ck(1 < n+1 < order-1, 'homological_exchange_congruence_excluded')
    for sign in [-1, 1]:
        ck((sign*(n+1)+1) % order != 0, 'neither_exchange_sign_is_deck_minus_identity')
    presentation = s.Matrix([[1, -(n+1)], [0, order]])
    snf = smith_normal_form(presentation, domain=s.ZZ)
    ck(tuple(abs(int(snf[i, i])) for i in range(2)) == (1, order), 'family_full_smith_normal_form')
    ck(M*M != s.eye(2) and M*M != -s.eye(2), 'family_matrix_square_not_signed_identity')
    low = s.Rational(n+1)-s.Rational(1, n-1)
    ck(low > 1, 'lspace_image_endpoint_strictly_interior')
    for numerator in [-101, -19, -1, 0, 1, 3, 7, 31]:
        for denominator in [1, 2, 5, 17]:
            slope = s.Rational(numerator, denominator)
            if slope > 1:
                continue
            image = (n+1)+1/(slope-n)
            ck(low <= image < n+1, 'sample_exact_projective_complement_image')
    if n <= 8:
        examples.append({'r': n, 'homology_order': order,
                         'gluing_matrix': [[int(v) for v in row] for row in M.tolist()],
                         'image_interval': [str(low), str(n+1)]})

# The peripheral calculation tested directly, without assuming the answer.
for epsilon, delta, k in product([-1, 1], [-1, 1], range(-100, 101)):
    B = s.Matrix([[epsilon, 0], [k, delta]])
    if B.det() != 1:
        continue
    central = B*s.Matrix([6, 1])
    preserves_fiber = central in (s.Matrix([6, 1]), s.Matrix([-6, -1]))
    ck(preserves_fiber == (k == 0), 'peripheral_kernel_and_center_force_signed_identity')

# Explicit half-period translations on the four branch points of the torus.
points = tuple(product(range(2), repeat=2))
perms = []
for a, b in points:
    perm = tuple(points.index(((x+a) % 2, (y+b) % 2)) for x, y in points)
    perms.append(perm)
    ck(tuple(perm[perm[i]] for i in range(4)) == tuple(range(4)), 'pillowcase_translation_order_two')
    if a or b:
        ck(all(perm[i] != i for i in range(4)), 'three_nontrivial_double_transpositions')
ck(len(set(perms)) == 4, 'four_pillowcase_kernel_permutations')
for u, v in product(perms, repeat=2):
    ck(tuple(u[v[i]] for i in range(4)) in perms, 'pillowcase_klein_four_closure')

print(json.dumps({'status': 'PASS', 'exact_assertions': sum(C.values()),
                  'families': dict(sorted(C.items())), 'initial_family_examples': examples,
                  'pillowcase_kernel_permutations': perms,
                  'scope': 'Exact algebraic controls for the specified two-trefoil-splice family only. Equivariant JSJ, local strong-inversion conjugacy and the mapping-class kernel are justified in the written argument and primary sources. KP-1.17 remains unresolved after five author turns.'},
                 indent=2, sort_keys=True))
