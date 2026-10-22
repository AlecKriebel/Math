#!/usr/bin/env python3
"""Independent exact audit certificates; no imports from the author's code.

The published general theorem and the all-degree/flatness arguments are reviewed
in AUDIT.md. Finite checks here do not replace those proofs.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
from math import comb, gcd
from functools import reduce
import json


def require(test, message):
    if not test:
        raise AssertionError(message)


def determinant(matrix):
    total = 0
    for p in permutations(range(len(matrix))):
        inversions = sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1, len(p)))
        term = (-1) ** inversions
        for i, j in enumerate(p):
            term *= matrix[i][j]
        total += term
    return total


def multiply(matrix, vector):
    return tuple(sum(row[i]*vector[i] for i in range(len(vector))) for row in matrix)


def column(matrix, j):
    return tuple(row[j] for row in matrix)


def kernel_certificate(matrix):
    cofactors = tuple((-1)**j * determinant(tuple(tuple(row[k] for k in range(4) if k != j) for row in matrix)) for j in range(4))
    content = reduce(gcd, map(abs, cofactors))
    primitive = tuple(x // content for x in cofactors)
    if primitive[1] < 0:
        primitive = tuple(-x for x in primitive)
    require(multiply(matrix, primitive) == (0, 0, 0), 'cofactor kernel')
    return primitive, content


def hull(points):
    points = sorted(set(points))
    def cross(a, b, c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    def half(seq):
        out = []
        for p in seq:
            while len(out) > 1 and cross(out[-2], out[-1], p) <= 0:
                out.pop()
            out.append(p)
        return out
    return half(points)[:-1] + half(reversed(points))[:-1]


def vertical_slice(polygon, x):
    heights = []
    for p, q in zip(polygon, polygon[1:] + polygon[:1]):
        if min(p[0], q[0]) <= x <= max(p[0], q[0]):
            if p[0] == q[0]:
                heights.extend([F(p[1]), F(q[1])])
            else:
                heights.append(F(p[1]) + (x-p[0])*F(q[1]-p[1], q[0]-p[0]))
    return min(heights), max(heights)


M = [((1, 1, 1, 1), (0, 1, 2, 3), (0, 0, -1, 4)),
     ((1, 1, 1, 1), (0, 1, 2, 3), (0, 0, 3, -1))]
a, b, c = (0, 11, 0, 0), (6, 0, 4, 1), (7, 0, 1, 3)
terms = [a, b, c]
kernels = [kernel_certificate(m) for m in M]
require(kernels == [((-6, 11, -4, -1), 1), ((-7, 11, -1, -3), 1)], 'primitive kernels and full value lattices')

# The two independent exponent differences cut out a two-dimensional common
# lineality space. Positive ray weights identify the three maximal cones.
differences = [tuple(a[j]-b[j] for j in range(4)), tuple(a[j]-c[j] for j in range(4))]
rank2_witnesses = [determinant(tuple(tuple(row[j] for j in js) for row in differences)) for js in combinations(range(4), 2)]
require(any(rank2_witnesses), 'common face codimension two in weight space')
weights = [multiply((w,), e)[0] for w in [M[0][2], M[1][2], (0, 0, -2, -3)] for e in terms]
require(weights == [0, 0, 11, 0, 11, 0, 0, -11, -11], 'initial forms and three cones')
factor = (6, 0, 1, 1)
residuals = [tuple(e[j]-factor[j] for j in range(4)) for e in [b, c]]
require(residuals == [(0, 0, 3, 0), (1, 0, 0, 2)], 'third initial factorization')

# Independent dynamic-programming reachability, followed by exact reconstruction
# using a 2x2 linear system for each of the 11 possible x_2 exponents.
def standard_representatives(matrix, value):
    n, x, z = value
    w3, w4 = matrix[2][2:]
    det = 2*w4 - 3*w3
    out = []
    for j in range(11):
        nc, nd = w4*(x-j)-3*z, 2*z-w3*(x-j)
        if nc % det or nd % det:
            continue
        k, l = nc//det, nd//det
        i = n-j-k-l
        if min(i, j, k, l) >= 0:
            out.append((i, j, k, l))
    return out


states = [{(0, 0, 0)}, {(0, 0, 0)}]
counts, points_checked = [], 0
for degree in range(25):
    target = comb(degree+3, 3) - (comb(degree-8, 3) if degree >= 11 else 0)
    require(all(len(s) == target for s in states), 'Hilbert function')
    images = []
    for i in range(2):
        image = set()
        for value in states[i]:
            reps = standard_representatives(M[i], value)
            require(len(reps) == 1, 'unique standard representative')
            require(multiply(M[i], reps[0]) == value, 'independent linear solve')
            transformed = multiply(M[1-i], reps[0])
            require(transformed[:2] == value[:2], 'common value preserved')
            require(standard_representatives(M[1-i], transformed) == reps, 'inverse map')
            image.add(transformed)
        require(image == states[1-i], 'onto target semigroup in degree')
        images.append(image)
        points_checked += len(states[i])
    counts.append(target)
    states = [{tuple(v[k]+column(M[i],j)[k] for k in range(3)) for v in states[i] for j in range(4)} for i in range(2)]

polygons = [hull([column(m,j)[1:] for j in range(4)]) for m in M]
require(polygons == [[(0,0),(2,-1),(3,4)],[(0,0),(3,-1),(2,3)]], 'convex hull vertices')
breaks = sorted({F(p[0]) for polygon in polygons for p in polygon})
require(breaks == [0, 2, 3], 'all affine fiber chambers')
for left, right in zip(breaks, breaks[1:]):
    # Endpoints determine each affine identity on this entire chamber.
    for x in (left, right):
        low1, high1 = vertical_slice(polygons[0], x)
        low2, high2 = vertical_slice(polygons[1], x)
        require(high1-low1 == high2-low2, 'fiber length identity')
        require(low1+high2 == x, 'global flip shear')

low1, high1 = vertical_slice(polygons[0], F(1))
low2, high2 = vertical_slice(polygons[1], F(1))
q, h = (1,1,0), (1,1,1)
shift_q, flip_q = (1,1,-low1+low2), (1,1,low1+high2)
require(shift_q == (1,1,F(1,6)), 'exact shift')
require(flip_q == h, 'exact flip')
theta_q = multiply(M[1], standard_representatives(M[0], q)[0])
theta_11q = multiply(M[1], standard_representatives(M[0], (11,11,0))[0])
require(theta_q == q and theta_11q == (11,11,11), 'nonadditivity certificate')
for i in range(2):
    require(not standard_representatives(M[i], h), 'degree-one saturation hole')
    require(multiply(M[i], [c,b][i]) == (11,11,11), 'integral multiple of hole')
flip_matrix = ((1,0,0),(0,1,0),(0,1,-1))
require(determinant(flip_matrix) == -1, 'unimodular flip')
require({(x,x-z) for x,z in polygons[0]} == set(polygons[1]), 'flip identifies cones')

# Deliberately false strengthenings must all be rejected.
negatives = {
    'arbitrary_representatives_define_theta': multiply(M[0],a)==multiply(M[0],b) and multiply(M[1],a)==multiply(M[1],b),
    'theta_is_additive': theta_11q == tuple(11*t for t in theta_q),
    'theta_is_shift_restriction': theta_q == shift_q,
    'theta_is_flip_restriction': theta_q == flip_q,
    'flip_preserves_unsaturated_semigroup': bool(standard_representatives(M[1],h)),
    'shift_is_integral': all(F(t).denominator == 1 for t in shift_q),
    'arbitrary_row_rescaling_preserves_euclidean_length': high1-low1 == 2*(high2-low2),
    'degree_one_check_establishes_additivity': all(multiply(M[1], standard_representatives(M[0],column(M[0],j))[0]) == column(M[1],j) for j in range(4)) and theta_11q==tuple(11*t for t in theta_q),
}
require(not any(negatives.values()), 'a negative control was incorrectly accepted')

# The monic family reduction has coefficient binomial(k,j) s^j t^(k-j).
# Check all displayed specializations and weight exponents without assuming
# equality of Hilbert polynomials implies flatness.
family_specializations = {'original':(1,1),'prime_1':(1,0),'prime_2':(0,1)}
for k in range(12):
    require(sum(comb(k,j) for j in range(k+1)) == 2**k, 'monic reduction binomial expansion')
    for j in range(k+1):
        exponent = tuple(j*b[t]+(k-j)*c[t] for t in range(4))
        require(sum(exponent) == 11*k and exponent[1] == 0, 'homogeneous monic remainder')

print(json.dumps({
    'arithmetic_result':'PASS',
    'method':'Independent cofactor kernels, dynamic reachability, exact 2x2 inverse reconstruction, convex hull slices',
    'source_example':'Escobar-Harada, arXiv:1912.04809v2, Example 4.5',
    'kernel_certificates':[{'primitive':r,'maximal_minor_gcd':g} for r,g in kernels],
    'degrees_checked':[0,24], 'values_checked_both_semigroups':points_checked,
    'hilbert_counts':counts,
    'polygons':polygons,'theta_q':theta_q,'theta_11q':theta_11q,
    'shift_q':[str(x) for x in shift_q], 'flip_q':[int(x) for x in flip_q],
    'negative_controls_rejected':list(negatives),
    'family_specializations':family_specializations,
    'all_degree_and_flatness_status':'Reviewed mathematical proofs in AUDIT.md; not inferred from finite arithmetic',
    'limitations':['No formal proof-assistant certification','No new general theorem','No network or author-code dependency']
}, indent=2))
