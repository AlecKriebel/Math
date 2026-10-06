#!/usr/bin/env python3
"""Exact finite algebra controls only; not a topology or general proof checker."""
import itertools, json, math, sys

def require(ok, msg):
    if not ok:
        raise ValueError(msg)

def determinant(m):
    n = len(m)
    require(n > 0 and all(len(row) == n for row in m), 'nonsquare matrix')
    if n == 1:
        return m[0][0]
    return sum(((-1) ** j) * m[0][j] * determinant(
        [[m[r][c] for c in range(n) if c != j] for r in range(1, n)])
        for j in range(n))

def determinantal_divisor(m, k):
    g = 0
    for rows in itertools.combinations(range(len(m)), k):
        for cols in itertools.combinations(range(len(m[0])), k):
            g = math.gcd(g, determinant([[m[r][c] for c in cols] for r in rows]))
    return abs(g)

def inspect(phi, expected_p):
    require(len(phi) == 3 and all(len(row) == 3 for row in phi), 'shape')
    require(all(type(x) is int for row in phi for x in row), 'noninteger entry')
    require(abs(determinant(phi)) == 1, 'gluing matrix not unimodular')
    u, v, p = phi[2]
    require(type(expected_p) is int and p == expected_p, 'wrong multiplicity')
    a, b = phi[0][2], phi[1][2]
    require(math.gcd(math.gcd(a, b), p) == 1, 'meridian image is not primitive')
    presentation = [[-u, 1, 0], [-v, 0, 1], [p, 0, 0]]
    ds = [determinantal_divisor(presentation, k) for k in (1, 2, 3)]
    require(ds == [1, 1, abs(p)], 'incorrect H1 invariant factors')
    return (1 if p == 0 else 0, abs(p))

def run():
    count = 0
    observed = {'infinite_cyclic': 0, 'trivial': 0, 'nontrivial_finite_cyclic': 0}
    for a, b, u, v in itertools.product(range(-3, 4), repeat=4):
        p = 1 + a*u + b*v
        phi = [[1, 0, a], [0, 1, b], [u, v, p]]
        rank, order = inspect(phi, p)
        kind = 'infinite_cyclic' if rank else ('trivial' if order == 1 else 'nontrivial_finite_cyclic')
        observed[kind] += 1
        count += 1
    require(count == 2401, 'case count')
    hopf = [[0, 1], [1, 0]]
    require(determinantal_divisor(hopf, 1) == 1 and abs(determinant(hopf)) == 1, 'Hopf final homology')
    require(determinant([[0]]) == 0, 'Hopf first filling homology')
    rejected = 0
    for phi, p in [([[1,0,0],[0,1,0],[0,0,2]],2),
                   ([[1,0,0],[0,1,0],[0,0,1]],0),
                   ([[1,0,0],[0,1,0],[0,0,True]],1)]:
        try:
            inspect(phi, p)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('negative control accepted')
    require(rejected == 3, 'negative control count')
    return {'result':'pass','matrix_cases':count,'h1_outcomes':observed,
            'hopf_homology_controls':2,'negative_controls_rejected':rejected,
            'certifies_topology':False,'certifies_general_solution':False}

if __name__ == '__main__':
    try:
        print(json.dumps(run(), sort_keys=True))
    except Exception as exc:
        print(json.dumps({'result':'fail','error':str(exc)}, sort_keys=True), file=sys.stderr)
        sys.exit(1)
