#!/usr/bin/env python3
"""Independent rational reconstruction of the frozen packet's 1,682 controls.

Uses Gaussian-rational reflection, matrix tangent maps, Cayley-Hamilton
recurrence, and homogeneous affine flow matrices. Does not import or execute
the author's verifier. Finite controls are not a proof of analytic density.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import product
import json

counts = Counter()

def require(name, condition):
    if not condition:
        raise AssertionError(name)
    counts[name] += 1

def cmul(z, w):
    return z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0]

def conjugate(z):
    return z[0], -z[1]

def scaled(z, c):
    return c*z[0], c*z[1]

def inner(z, w):
    return cmul(conjugate(z), w)[0]

def oriented_area(z, w):
    return cmul(conjugate(z), w)[1]

def tangent_reflection(u, x, radius):
    # In complex notation reflection in the tangent at x is -x^2 conjugate(u)/R^2.
    return scaled(cmul(cmul(x, x), conjugate(u)), -1/(radius*radius))

parameters = tuple(map(Q, ('-3/4', '-1/2', '-1/3', '0', '1/3', '1/2', '3/4')))
for R, t, v in product(map(Q, ('1/2', '1', '7/3')), parameters, parameters):
    p, s = 2*R*t/(1+t*t), R*(1-t*t)/(1+t*t)
    u = ((1-v*v)/(1+v*v), 2*v/(1+v*v))
    collision = cmul(u, (s, p))
    reflected = tangent_reflection(u, collision, R)
    p_after = oriented_area(reflected, collision)
    require('transverse_last_endpoint', s > 0 and inner(u, collision) == s)
    require('on_circle', inner(collision, collision) == R*R)
    require('unit_reflected_direction', inner(reflected, reflected) == 1)
    require('angular_momentum_preserved', p_after == p)
    require('outgoing_points_inside', inner(reflected, collision) == -s)
    require('circle_direction_formula', reflected == cmul(u, (2*p*p/(R*R)-1, -2*p*s/(R*R))))
    first_after = cmul(reflected, (-s, p_after))
    recovered = tangent_reflection(reflected, first_after, R)
    require('inverse_recovers_line', recovered == u and oriented_area(recovered, first_after) == p)
    require('inverse_uses_same_collision', first_after == collision)
    reversed_u = scaled(u, -1)
    reversed_last = cmul(reversed_u, (s, -p))
    jtj = scaled(tangent_reflection(reversed_u, reversed_last, R), -1)
    first_before = cmul(u, (-s, p))
    require('reversibility_JTJ', jtj == tangent_reflection(u, first_before, R))

u = (Q(1), Q(0))
p, s, R = Q(3, 5), Q(4, 5), Q(1)
collision = cmul(u, (s, p))
once = tangent_reflection(u, collision, R)
twice = tangent_reflection(once, cmul(once, (s, p)), R)
require('noninvolution_witness', twice != u)
require('noninvolution_exact_coordinates', twice == (Q(-527, 625), Q(336, 625)))

vectors = ((Q(1), Q(0)), (Q(0), Q(1)), (Q(2), Q(-3)))
for z, w in product(vectors, repeat=2):
    require('orientation_reversal_antisymplectic',
            -oriented_area(conjugate(z), conjugate(w)) == oriented_area(z, w))

def matrix_product(a, b):
    return tuple(tuple(sum((a[i][k]*b[k][j] for k in range(len(b))), Q(0))
                       for j in range(len(b[0]))) for i in range(len(a)))

I = ((Q(1), Q(0)), (Q(0), Q(1)))
radii = tuple(map(Q, ('3/4', '1', '5/4')))
for length in range(5):
    for word in product(radii, repeat=length):
        tangent = I
        for radius in word:
            tangent = matrix_product(((Q(1), 2/radius), (Q(0), Q(1))), tangent)
        require('concentric_shear_gap', tangent[0][1] + 2 >= 2*length/max(radii) + 2)
        require('empty_or_positive_shear', tangent[0][1] >= 0)
for length in range(1, 21):
    tangent = I
    for _ in range(length):
        tangent = matrix_product(((Q(1), Q(2)), (Q(0), Q(1))), tangent)
    require('power_shear_identity_gap', tangent[0][1] > 0)
    require('power_shear_inverse_gap', tangent[0][1] + 2 >= 4)

def cayley_hamilton_powers(a, n):
    # Every determinant-one 2x2 matrix satisfies P_(k+1)=trace(A) P_k-P_(k-1).
    trace = a[0][0]+a[1][1]
    powers = [I, a]
    for k in range(1, n):
        powers.append(tuple(tuple(trace*powers[k][i][j]-powers[k-1][i][j]
                                  for j in range(2)) for i in range(2)))
    return powers

for a, pair in product(map(Q, ('1/3', '1', '5/2')), ((3, Q(-1, 2)), (4, Q(0)), (6, Q(1, 2)))):
    N, cosine = pair
    epsilon = (2-2*cosine)/a
    matrix = ((Q(1), a), (-epsilon, 1-a*epsilon))
    inverse = ((matrix[1][1], -matrix[0][1]), (-matrix[1][0], matrix[0][0]))
    powers = cayley_hamilton_powers(matrix, N)
    require('linear_model_determinant', matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0] == 1)
    require('linear_model_trace', matrix[0][0]+matrix[1][1] == 2*cosine)
    require('linear_model_exact_order_control', powers[N] == I)
    require('linear_model_positive_power_is_inverse', powers[N-1] == inverse)
    require('linear_model_inverse_multiplication', matrix_product(matrix, inverse) == I)
    require('linear_model_shear_sign_reverses', matrix[0][1] > 0 and powers[N-1][0][1] < 0)

def affine_x(h):
    return ((Q(1), Q(0), h), (Q(0), Q(1), Q(0)), (Q(0), Q(0), Q(1)))

def affine_y(h):
    return ((Q(1), Q(0), Q(0)), (h, Q(1), Q(0)), (Q(0), Q(0), Q(1)))

for x, y, h in product(map(Q, ('-2', '0', '3/2')), map(Q, ('-1', '1/3')), map(Q, ('1/10', '-2/7'))):
    commutator = matrix_product(affine_y(-h), matrix_product(affine_x(-h),
                                matrix_product(affine_y(h), affine_x(h))))
    point = matrix_product(commutator, ((x,), (y,), (Q(1),)))
    require('commutator_bracket_sign', point == ((x,), (y+h*h,), (Q(1),)))

if sum(counts.values()) != 1682:
    raise AssertionError('unexpected control count')
print(json.dumps({
    'problem_id': 5200008,
    'arithmetic': 'exact rational arithmetic using fractions.Fraction',
    'implementation': 'independent Gaussian-rational and matrix reconstruction; no author-code import',
    'checks': dict(sorted(counts.items())),
    'total_assertions': sum(counts.values()),
    'passed': True,
    'scope': 'Finite controls only; no analytic, optical-realizability, or density certification.'
}, indent=2, sort_keys=True))
