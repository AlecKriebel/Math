#!/usr/bin/env python3
"""Independent exact algebra for the Honda datum and k-qss flag, no external imports."""
from fractions import Fraction
import json

def need(condition, message):
    if not condition:
        raise ValueError(message)

def unit(d, j):
    return tuple(int(i == j) for i in range(d))

def plus(*vectors):
    return tuple(sum(row) for row in zip(*vectors))

def scale(a, vector):
    return tuple(a * x for x in vector)

def act(arrows, vector):
    result = [0] * len(vector)
    for source, target in arrows.items():
        result[target] += vector[source]
    return tuple(result)

def coordinates(basis, vector):
    d = len(vector)
    rows = [[Fraction(basis[j][i]) for j in range(d)] + [Fraction(vector[i])] for i in range(d)]
    determinant = Fraction(1)
    for j in range(d):
        pivot = next((i for i in range(j, d) if rows[i][j]), None)
        need(pivot is not None, 'singular basis')
        if pivot != j:
            rows[j], rows[pivot] = rows[pivot], rows[j]
            determinant = -determinant
        q = rows[j][j]
        determinant *= q
        rows[j] = [value / q for value in rows[j]]
        for i in range(d):
            if i != j:
                q = rows[i][j]
                rows[i] = [a - q*b for a, b in zip(rows[i], rows[j])]
    return tuple(row[-1] for row in rows), determinant

F = {0: 1, 1: 2, 3: 4}
V = {0: 5, 3: 2, 5: 4}
e = [unit(6, j) for j in range(6)]
basis = [plus(e[1], e[3], e[5]), plus(e[2], e[4]), plus(scale(2,e[1]),e[3]), e[2], e[0], e[1]]
images = {}
for label, arrows in [('F', F), ('V', V)]:
    columns = []
    for vector in basis:
        column, determinant = coordinates(basis, act(arrows, vector))
        need(abs(determinant) == 1, 'basis not unimodular')
        need(all(x.denominator == 1 for x in column), 'nonintegral conjugation')
        columns.append(tuple(int(x) for x in column))
    images[label] = columns
    for size in (2, 4):
        need(all(not any(column[size:]) for column in columns[:size]), 'qss flag unstable')
    for start in (0, 2, 4):
        factor = tuple(tuple(column[start:start+2]) for column in columns[start:start+2])
        need(factor == ((0,1),(0,0)), 'wrong rank-two elliptic factor')
for vector in e:
    need(act(F, act(V, vector)) == (0,)*6, 'FV nonzero')
    need(act(V, act(F, vector)) == (0,)*6, 'VF nonzero')

def honda_certificate(arrows_f, arrows_v, d, ell_indices):
    im_f = set(arrows_f.values())
    im_v = set(arrows_v.values())
    ker_f = set(range(d)) - set(arrows_f)
    ker_v = set(range(d)) - set(arrows_v)
    exact = (len(im_f) == len(arrows_f) and len(im_v) == len(arrows_v)
             and im_f == ker_v and im_v == ker_f)
    complement = set(ell_indices).isdisjoint(im_f) and set(ell_indices) | im_f == set(range(d))
    restricted_images = [arrows_v.get(j) for j in ell_indices]
    injective_v = None not in restricted_images and len(set(restricted_images)) == len(ell_indices)
    return {'exact': exact, 'L_complement': complement, 'V_on_L_injective': injective_v,
            'passed': exact and complement and injective_v}

all_n = {}
for n in (3,4,7,12):
    f, v = dict(F), dict(V)
    ell = [0,3,5]
    for j in range(6, 2*n, 2):
        f[j] = v[j] = j+1
        ell.append(j)
    cert = honda_certificate(f,v,2*n,ell)
    need(cert['passed'], 'direct-sum Honda conditions failed')
    all_n[str(n)] = cert
small_controls = {}
for n in (0,1,2):
    f = {j:j+1 for j in range(0,2*n,2)}
    cert = honda_certificate(f,f,2*n,list(range(0,2*n,2)))
    need(cert['passed'], 'small split elliptic Honda control failed')
    small_controls[str(n)] = cert
negative = {'bad_L': honda_certificate(F,V,6,[0,1,3])['passed'],
            'zero_operator_nonliftable': honda_certificate({}, {},6,list(range(6)))['passed'],
            'unstable_flag': all(act(arrows,vector)[2:] == (0,)*4
                                 for arrows in (F,V) for vector in e[:2])}
need(not any(negative.values()), 'negative control accepted')

# F_125 = F_5[t]/(t^3+t+1); a cubic without F_5 roots is irreducible.
q = 5
zero, one = (0,0,0), (1,0,0)
def add(a,b):
    return tuple((x+y) % q for x,y in zip(a,b))
def times(a,b):
    coefficients = [0]*5
    for i in range(3):
        for j in range(3):
            coefficients[i+j] += a[i]*b[j]
    for j in (4,3):
        coefficients[j-3] -= coefficients[j]
        coefficients[j-2] -= coefficients[j]
    return tuple(x % q for x in coefficients[:3])
def power(a,n):
    result = one
    while n:
        if n & 1:
            result = times(result,a)
        a = times(a,a)
        n //= 2
    return result
need(all((x*x*x+x+1) % q for x in range(q)), 'modulus reducible')
field = [(a,b,c) for a in range(5) for b in range(5) for c in range(5)]
need(all(power(a,125) == a for a in field), 'field Frobenius check failed')
need(any(power(a,5) != power(a,25) for a in field), 'sigma inverse control degenerate')
def semi(arrows,vector,pow_frob):
    result = [zero]*len(vector)
    for source,target in arrows.items():
        result[target] = add(result[target],power(vector[source],pow_frob))
    return tuple(result)
def field_coordinates_vector(coefficients):
    result = [zero]*6
    for coefficient,vector in zip(coefficients,basis):
        for i,x in enumerate(vector):
            result[i] = add(result[i],times(coefficient,(x % 5,0,0)))
    return tuple(result)
vectors_tested = 0
for a in field:
    coeffs = [a,power(a,5),add(a,one),power(a,25),one,times(a,a)]
    vector = field_coordinates_vector(coeffs)
    for label,arrows,exponent in [('F',F,5),('V',V,25)]:
        actual = semi(arrows,vector,exponent)
        expected = [zero]*6
        for coefficient,column in zip(coeffs,images[label]):
            for i,x in enumerate(column):
                expected[i] = add(expected[i],times(power(coefficient,exponent),(x % 5,0,0)))
        need(actual == field_coordinates_vector(expected), 'nontrivial Frobenius basis transport failed')
    need(semi(F,semi(V,vector,25),5) == (zero,)*6, 'semilinear FV failed')
    need(semi(V,semi(F,vector,5),25) == (zero,)*6, 'semilinear VF failed')
    vectors_tested += 1
print(json.dumps({'exact_integer_basis_determinant': int(determinant),
                  'operator_columns_in_qss_basis': images,
                  'three_elliptic_module_factors': True,
                  'honda_direct_sum_controls': all_n,
                  'split_small_rank_controls': small_controls,
                  'negative_controls_accepted': negative,
                  'semilinear_field': 'F_5[t]/(t^3+t+1)',
                  'Frobenius_orders': {'sigma':5,'sigma_inverse':25,'field_cardinality':125},
                  'semilinear_vectors_tested': vectors_tested,
                  'scope': 'linear algebra controls; scheme existence uses cited primary classification'}, indent=2))
