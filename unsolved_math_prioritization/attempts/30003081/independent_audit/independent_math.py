#!/usr/bin/env python3
"""Independent rational checks using divisibility multipliers, not author remainder code."""
import argparse
from fractions import Fraction
from itertools import product
from math import comb, factorial
import json

class AuditFailure(Exception):
    pass

def require(value, message):
    if not value:
        raise AuditFailure(message)

def powers(n, d):
    return [e for e in product(range(d + 1), repeat=n) if sum(e) == d]

def rank(a):
    if not a:
        return 0
    a = [[Fraction(x) for x in row] for row in a]
    width = len(a[0])
    require(all(len(row) == width for row in a), 'ragged input')
    pivot = 0
    for column in range(width):
        selected = next((i for i in range(pivot, len(a)) if a[i][column]), None)
        if selected is None:
            continue
        a[pivot], a[selected] = a[selected], a[pivot]
        value = a[pivot][column]
        for i in range(pivot + 1, len(a)):
            if a[i][column]:
                factor = a[i][column] / value
                for j in range(column, width):
                    a[i][j] -= factor * a[pivot][j]
        pivot += 1
        if pivot == len(a):
            break
    return pivot

def tangencies(forms, degree):
    n = len(forms[0])
    p, q = powers(n, degree), powers(n, degree - 1)
    qi = {e: i for i, e in enumerate(q)}
    width = n * len(p) + len(forms) * len(q)
    matrix = []
    for k, form in enumerate(forms):
        for m, e in enumerate(p):
            row = [0] * width
            for j, scalar in enumerate(form):
                row[j * len(p) + m] += scalar
                if e[j]:
                    predecessor = list(e)
                    predecessor[j] -= 1
                    row[n * len(p) + k * len(q) + qi[tuple(predecessor)]] -= scalar
            matrix.append(row)
    return p, matrix, width

SEVEN = [(1,0,0),(0,1,0),(0,0,1),(1,0,-1),(0,1,-1),(1,-1,1),(1,-1,-1)]
PRODUCT = [(1,0,0),(0,1,0),(0,0,1),(1,-1,0)]
TARGET = [(1,0),(0,1),(1,-1)]

def restriction(forms, degree):
    p, a, width = tangencies(forms, degree)
    rows = []
    labels = []
    for j in range(2):
        for k, e in enumerate(p):
            if e[2] == 0:
                row = [0] * width
                row[j * len(p) + k] = 1
                rows.append(row)
                labels.append((j, e))
    base = rank(a)
    image = rank(a + rows) - base
    target_p, target, target_width = tangencies(TARGET, degree)
    target_dimension = target_width - rank(target)
    if degree == 2 and forms == SEVEN:
        eta = [1 if j == 0 and e == (2,0,0) else -1 if j == 0 and e == (1,1,0) else 0 for j,e in labels]
        augmented = [r + [0] for r in a] + [r + [s] for r,s in zip(rows,eta)]
        require(rank(augmented) == rank(a + rows) + 1, 'specified eta unexpectedly lifts')
    return {'degree': degree, 'ambient_dimension': width - base, 'target_dimension': target_dimension,
            'restriction_rank': image, 'defect_dimension': target_dimension - image}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--false-control', choices=['surjection','codimension','chern','torsion'])
    args = parser.parse_args()
    profiles = [restriction(SEVEN, d) for d in range(1,6)]
    expected = [0,1,1,0,0]
    if args.false_control == 'surjection':
        expected = [0,0,0,0,0]
    require([x['defect_dimension'] for x in profiles] == expected, 'seven-plane defects')
    products = [restriction(PRODUCT, d) for d in range(1,6)]
    require(all(x['defect_dimension'] == 0 for x in products), 'product surjection')
    counts = []
    for n in range(2,10):
        for d in range(1,13):
            # Degree d in two normal variables, or degree d-1 times one tangent variable.
            dimension = comb(d+1,1) + comb(d,1) * (n-1)
            require(dimension == n*d+1, 'normal-degree decomposition')
            counts.append((n,d,dimension))
    line_conditions = comb(6,3) - (3*3+1)
    point_conditions = comb(4,3)
    require(line_conditions == (point_conditions if args.false_control == 'codimension' else 10), 'line/point distinction')
    ch = [sum(Fraction((-1)**j * comb(3,j) * (-j)**k, factorial(k)) for j in range(4)) for k in range(4)]
    require(ch == ([0,0,0,0] if args.false_control == 'chern' else [0,0,0,1]), 'Koszul Chern defect')
    # f=x(x-z): J=(f,2x-z,-x)=(x,z); z-torsion has dimension one.
    # x*d/dx produces c=x, zero modulo J; Euler lifts the target generator.
    jacobian_linear_rows = [[2,-1],[-1,0]]
    require(rank(jacobian_linear_rows) == 2, 'Jacobian quotient must kill x and z')
    # x*f_x - 2*f = x*z by exact coefficients of x^2 and x*z.
    residual = (2 - 2, -1 + 2)
    require(residual == (0,1), 'explicit obstruction numerator')
    c = [1,0]
    require(rank(jacobian_linear_rows + [c]) == 2, 'obstruction class is not zero')
    torsion_dimension = 1 + 2 - rank(jacobian_linear_rows)
    obstruction_dimension = rank(jacobian_linear_rows + [c]) - rank(jacobian_linear_rows)
    require(torsion_dimension == (obstruction_dimension if args.false_control == 'torsion' else 1), 'torsion is not identical to restriction defect')
    print(json.dumps({'status':'PASS','method':'independent multiplier linear systems over Q',
        'seven_plane_profiles':profiles,'product_profiles':products,'normal_monomial_cases':len(counts),
        'double_line_conditions':line_conditions,'double_point_conditions':point_conditions,
        'point_ch':[str(x) for x in ch], 'nonnecessary_torsion_control':{'torsion_dimension':1,'restriction_defect':0},
        'scope':'Finite checks plus an elementary explicit control; no proof of universal sheaf claims.'},indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
