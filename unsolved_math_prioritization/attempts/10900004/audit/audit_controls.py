#!/usr/bin/env python3
"""Independent exact controls for AMR-108-0004. Standard library only.

No imported author code, source files, network, or global convexity oracle.
Run from any directory: python audit_controls.py [--output results.json].
Finite controls supplement, and never replace, the proofs in AUDIT_REPORT.md.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import permutations, product
from math import gcd, prod
import argparse
import json
from pathlib import Path

counts = Counter()
negative_controls = []


def test(name, truth):
    if not truth:
        raise AssertionError(name)
    counts[name] += 1


def negative(name, invalid_conclusion_rejected):
    test('negative_controls', invalid_conclusion_rejected)
    negative_controls.append(name)


def M(rows):
    return tuple(tuple(F(x) for x in row) for row in rows)


def mul(a, b):
    return tuple(tuple(sum(x*y for x, y in zip(row, col))
                       for col in zip(*b)) for row in a)


def transpose(a):
    return tuple(zip(*a))


def det(a):
    return a[0][0]*a[1][1]-a[0][1]*a[1][0]


def inverse(a):
    z = det(a)
    return M(((a[1][1]/z, -a[0][1]/z), (-a[1][0]/z, a[0][0]/z)))


def scalar(s, a):
    return tuple(tuple(s*x for x in row) for row in a)


def power(a, n):
    x = M(((1, 0), (0, 1)))
    for _ in range(n):
        x = mul(x, a)
    return x


def rows(a):
    return Counter(tuple(r) for r in a)


def projectively_similar_diagonal(a, b):
    # Every possible scalar is forced by the image of the first eigenvalue.
    return any(Counter(s*x for x in a) == Counter(b)
               for s in {y/a[0] for y in b})


def max_intertwiner_rank(a, b):
    # Joint eigenvalue tuples index the exact intertwining blocks.
    # Blocks are complete bipartite graphs, so maximum rank is this sum.
    ca, cb = Counter(a), Counter(b)
    return sum(min(n, cb[k]) for k, n in ca.items())


def rank(a):
    a = [list(row) for row in a]
    pivots = 0
    for j in range(len(a[0])):
        k = next((k for k in range(pivots, len(a)) if a[k][j]), None)
        if k is None:
            continue
        a[pivots], a[k] = a[k], a[pivots]
        pivot = a[pivots][j]
        a[pivots] = [x/pivot for x in a[pivots]]
        for k in range(len(a)):
            if k != pivots:
                ratio = a[k][j]
                a[k] = [x-ratio*y for x, y in zip(a[k], a[pivots])]
        pivots += 1
        if pivots == len(a):
            break
    return pivots


I = M(((1, 0), (0, 1)))
W0 = M(((1, 0), (0, 1), (-1, -1), (0, 0)))
W = M(((3, 0), (1, 2), (-4, -2), (0, 0)))
Wp = M(((3, 2), (1, 0), (-4, -2), (0, 0)))
perms = list(permutations(range(4)))
gl = [M(((a, b), (c, d))) for a, b, c, d in product(range(-4, 5), repeat=4)
      if abs(a*d-b*c) == 1]

# Independent homology controls: count homomorphisms into Z/n, rather than
# repeating the author's row/column operations on the relation matrix.
for A in gl:
    a, b = (int(x) for x in A[0])
    for n in range(2, 14):
        found = sum((x-a*y) % n == 0 and (b*y) % n == 0
                    for x, y in product(range(n), repeat=2))
        test('homology_modular_character_count', found == gcd(abs(b), n))
    test('inverse_swap_keeps_homology_torsion', abs(inverse(A)[0][1]) == abs(b))
    for E1 in (M(((1, 0), (3, 1))), M(((-1, 0), (2, 1)))):
        for E2 in (M(((1, 0), (-2, -1))), M(((-1, 0), (4, -1)))):
            B = mul(mul(E2, A), inverse(E1))
            test('extendable_kernel_group_preserves_abs_b', abs(B[0][1]) == abs(b))
# The explicit shear with b=3,c=0 distinguishes cyclic homology from Z.
negative('transposed homology entry c', gcd(3, 2) != gcd(0, 2))

# Exact rational eigenvalues, independent joint-eigenspace block rank.
U = (F(8), F(2), F(1, 16), F(1))
V = (F(1), F(4), F(1, 4), F(1))
Vp = (F(4), F(1), F(1, 4), F(1))
test('normalized_positive_spectra', all(prod(z) == 1 and min(z) > 0 for z in (U, V, Vp)))
test('same_individual_spectra', Counter(V) == Counter(Vp))
test('joint_intertwiner_maximum_rank_two', max_intertwiner_rank(zip(U, V), zip(U, Vp)) == 2)
negative('separate generator conjugators imply one common conjugator', rows(W) != rows(Wp))
for Z, expected in ((W, 18), (Wp, -6), (W0, 3), (scalar(-1, W0), 3)):
    L = tuple(tuple(Z[i][j]-Z[2][j] for j in range(2)) for i in range(2))
    test('triangle_lattice_area', det(L) == expected)
    test('strict_middle_centroid_certificate',
         rank(Z[:3]) == 2 and Z[3] == (0, 0)
         and all(sum(Z[i][j] for i in range(3)) == 0 for j in range(2)))
Q = mul(transpose(W0), W0)
test('gram_matrix', Q == M(((2, 1), (1, 2))))
negative('Gram equality implies joint conjugacy',
         mul(transpose(scalar(-1, W0)), scalar(-1, W0)) == Q
         and rows(W0) != rows(scalar(-1, W0)))

# Surface projective holonomy agrees while the full transverse holonomy differs.
X = scalar(10, W0)
Y = M(((11, 1), (1, 11), (-9, -9), (-3, -3)))
test('same_triangle_projective_action',
     all(Y[i][j]-Y[2][j] == X[i][j]-X[2][j] for i in range(2) for j in range(2)))
test('transverse_character_inside_triangle',
     all(F(1, 5)*Y[0][j] + F(1, 5)*Y[1][j] + F(3, 5)*Y[2][j] == Y[3][j]
         for j in range(2)))
negative('triangle surface holonomy determines neighborhood holonomy', rows(X) != rows(Y))

# Repeated eigenvalues of individual generators do not destroy joint simplicity.
R1 = (F(2), F(2), F(1, 2), F(1, 2))
R2 = (F(3), F(1, 3), F(3), F(1, 3))
p = (1, 0, 2, 3)
test('repeated_generator_distinct_joint_characters', len(set(zip(R1, R2))) == 4)
negative('centralizing one peripheral generator is sufficient',
         tuple(R1[i] for i in p) == R1 and tuple(R2[i] for i in p) != R2)

# Derive all W0 stabilizers through the metric equation, independent of the
# author's method of reading the first two rows of each permuted W0.
# If A^T Q A=Q, Q(x,y)=2(x^2+xy+y^2) forces each column to be among six vectors.
# Completeness: x^2+xy+y^2 >= 3*x^2/4 and >= 3*y^2/4, so |x|,|y| <= 1.
unit_vectors = [v for v in product(range(-2, 3), repeat=2)
                if v[0]*v[0]+v[0]*v[1]+v[1]*v[1] == 1]
metric_group = []
character_group = []
for v, w in product(unit_vectors, repeat=2):
    A = M(((v[0], w[0]), (v[1], w[1])))
    if mul(mul(transpose(A), Q), A) != Q:
        continue
    metric_group.append(A)
    if rows(mul(W0, A)) == rows(W0):
        character_group.append(A)
test('metric_group_size_twelve', len(metric_group) == 12)
test('character_group_size_six', len(character_group) == 6)
test('opposite_ray_adds_exactly_six', set(metric_group) == set(character_group + [scalar(-1, A) for A in character_group]))
for A in character_group:
    test('character_group_order', any(power(A, n) == I for n in (1, 2, 3)))
for A in metric_group:
    test('signed_ray_group_order', power(A, 6) == I)
for A in gl:
    for r in (F(-3), F(-1), F(-1, 3), F(1, 3), F(1), F(3)):
        match = rows(mul(W0, A)) == rows(scalar(r, W0))
        gram_match = mul(mul(transpose(A), Q), A) == scalar(r*r, Q)
        test('independent_ray_gram_necessary', not match or gram_match)
        test('independent_unimodular_ray_scale', not gram_match or abs(r) == 1)
        test('ray_stabilizer_membership', not match or A in metric_group)

shear = M(((1, 5), (0, 1)))
rank_one = M(((0, -2), (0, -1), (0, 1), (0, 2)))
negative('omit the full-rank hypothesis', mul(rank_one, shear) == rank_one and power(shear, 12) != I)
negative('omit unimodularity in the ray claim', mul(W0, scalar(2, I)) == scalar(2, W0) and det(scalar(2, I)) != 1)

# Test finite cover cancellation with nontrivial changes D of the upstairs basis,
# genuinely different W1,W2, and positive as well as negative determinant covers.
cover_matrices = [M(((a, b), (c, d))) for a, b, c, d in product(range(-2, 3), repeat=4)
                  if a*d-b*c != 0]
Ds = (I, M(((0, 1), (1, 0))), M(((1, 2), (0, 1))), M(((0, -1), (1, 0))))
As = (I, M(((1, 3), (0, 1))), M(((2, 1), (1, 1))), M(((1, 0), (0, -1))))
for A, B1, D in product(As, cover_matrices, Ds):
    B2 = mul(mul(A, B1), inverse(D))
    test('cover_diagram_with_nontrivial_D', mul(A, B1) == mul(B2, D))
    for W1, W2 in ((W, Wp), (W0, W0), (mul(W, A), W)):
        downstairs = rows(W1) == rows(mul(W2, A))
        upstairs = rows(mul(W1, B1)) == rows(mul(mul(W2, B2), D))
        test('cover_simultaneous_conjugacy_equivalence', downstairs == upstairs)
negative('omit cover-diagram compatibility',
         rows(W0) == rows(W0) and rows(W0) != rows(mul(W0, shear)))
signed_U = (-U[0], -U[1], U[2], U[3])
negative('drop positivity and cancel finite-index holonomy',
         not projectively_similar_diagonal(U, signed_U)
         and tuple(x*x for x in U) == tuple(x*x for x in signed_U))

# Explicit semidirect-product group law checks and scalar-aware nonextension.
def group_mul(x, y):
    a, e = x
    b, f = y
    b = b if e == 0 else tuple(reversed(b))
    return ((a[0]+b[0], a[1]+b[1]), (e+f) % 2)


one = ((0, 0), 0)
tau = ((0, 0), 1)
e1 = ((1, 0), 0)
e2 = ((0, 1), 0)
test('semidirect_involution_square', group_mul(tau, tau) == one)
test('semidirect_conjugates_generators', group_mul(group_mul(tau, e1), tau) == e2)
S1 = (F(2), F(1, 2), F(1), F(1))
S2 = (F(1), F(1), F(3), F(1, 3))
test('descent_scalar_aware_nonconjugacy', not projectively_similar_diagonal(S1, S2))
negative('normalizing a subgroup alone supplies group extension',
         tuple(x*x for x in S1) != (F(1),)*4)

# Nilpotent Jordan data survive when the logarithmic spectrum is zero.
N = M(((0, 1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)))
test('nonzero_square_zero_jordan_part', rank(N) == 1 and rank(mul(N, N)) == 0)
negative('zero eigenvalue logs certify identity holonomy', rank(N) != 0)

out = {
    'result': 'PASS',
    'scope': 'Independent exact matrix and algebraic group controls; no global convex holonomy or full resolution.',
    'assertions': sum(counts.values()),
    'counts': dict(counts),
    'negative_controls_rejected': len(negative_controls),
    'negative_controls': negative_controls,
    'gl2_matrices': len(gl),
    'nonsingular_cover_matrices': len(cover_matrices),
    'complete_metric_group_size': len(metric_group),
    'complete_character_group_size': len(character_group),
}
parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path)
args = parser.parse_args()
text = json.dumps(out, indent=2) + '\n'
if args.output:
    args.output.write_text(text)
print(text, end='')
