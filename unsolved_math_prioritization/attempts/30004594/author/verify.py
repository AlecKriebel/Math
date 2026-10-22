#!/usr/bin/env python3
"""Exact finite controls for PROOF.md; not an infinite-lattice proof certificate."""
import argparse
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations, product
import json
from pathlib import Path


class Checks:
    def __init__(self):
        self.counts = defaultdict(int)

    def check(self, category, condition):
        self.counts[category] += 1
        if not condition:
            raise AssertionError(category)


def generator_controls(c):
    """Pointwise identity, prior to taking any stationary expectation."""
    points = list(product(range(3), repeat=2))
    index = {x: i for i, x in enumerate(points)}
    neighbors = []
    for x in points:
        row = []
        for j in range(2):
            for s in [-1, 1]:
                y = list(x)
                y[j] = (y[j] + s) % 3
                row.append(index[tuple(y)])
        neighbors.append(row)
    subsets = [sum(1 << i for i in a) for k in [1, 2, 3]
               for a in combinations(range(9), k)]
    # A single rational lambda is enough for this exact pointwise control;
    # the proof establishes the formal identity for all lambda.
    lam = F(7, 5)
    for state in range(1 << 9):
        for a in subsets:
            f = int((state & a) == a)
            direct = F(0)
            for x in range(9):
                if state >> x & 1:
                    new = state & ~(1 << x)
                    direct += int((new & a) == a) - f
                    for y in neighbors[x]:
                        new = state | (1 << y)
                        direct += lam / 4 * (int((new & a) == a) - f)
            rhs = -a.bit_count() * f
            for x in range(9):
                if a >> x & 1:
                    for y in neighbors[x]:
                        a1 = (a & ~(1 << x)) | (1 << y)
                        a2 = a | (1 << y)
                        rhs += lam / 4 * (int((state & a1) == a1)
                                          - int((state & a2) == a2))
            c.check('generator_pointwise', direct == rhs)
    return {'torus': '3 by 3', 'configurations': 512,
            'subsets': len(subsets), 'lambda': str(lam)}


def hyperplane_controls(c):
    eps = F(1, 4)
    moments = [F(0) for _ in range(3)]
    total = F(0)
    # Common horizontal line and three distinct vertical lines.
    for bits in product([0, 1], repeat=4):
        prob = eps ** sum(bits) * (1 - eps) ** (4 - sum(bits))
        total += prob
        occupied = [bits[0] or bits[i] for i in range(1, 4)]
        for k in range(1, 4):
            if all(occupied[:k]):
                moments[k-1] += prob
    c.check('hyperplane_cylinder', total == 1)
    c.check('hyperplane_cylinder', moments == [F(7,16), F(19,64), F(67,256)])
    excess = moments[2] * moments[0] - moments[1] ** 2
    c.check('hyperplane_cylinder', excess == F(27,1024))
    c.check('hyperplane_cylinder', excess > 0)
    return {'epsilon': str(eps), 'moments': list(map(str, moments)),
            'triple_times_density_minus_pair_squared': str(excess)}


def geometric_controls(c):
    comparisons = []
    for d in range(2, 13):
        for L in range(1, 21):
            M = (2*L - 1) ** d
            if L == 1:
                c.check('radius_obstruction', F(1,2) > F(1,2*d-1))
            else:
                c.check('radius_obstruction', M >= 3*L)
                c.check('radius_obstruction', (2*d-1)**3 > 2*d+1)
                # Comparing bases and exponents avoids gigantic integers.
                c.check('radius_obstruction', (2*L-1)**2 >= 3*L)
            if d <= 3 and L <= 3:
                comparisons.append({'d': d, 'L': L, 'classes': M,
                    'straight_path_lower_at_lambda_1': str(F(1,2*d+1)**L),
                    'coloring_cutoff': str(F(1,2*d-1)**M)})
    # The exact geometric primitive used in the coloring proof.
    for d in [1, 2, 3]:
        for L in [1, 2, 3]:
            m = 2*L - 1
            points = list(product(range(-L+1, L), repeat=d))
            for shift in product([-m, 0, m], repeat=d):
                if any(shift):
                    translated = {tuple(x[j]+shift[j] for j in range(d))
                                  for x in points}
                    c.check('disjoint_interiors', set(points).isdisjoint(translated))
    return comparisons


def gauss_solve(matrix, vector):
    n = len(vector)
    a = [[F(v) for v in row] + [F(vector[i])]
         for i, row in enumerate(matrix)]
    for k in range(n):
        pivot = next(i for i in range(k,n) if a[i][k])
        a[k], a[pivot] = a[pivot], a[k]
        p = a[k][k]
        for j in range(k,n+1):
            a[k][j] /= p
        for i in range(k+1,n):
            p = a[i][k]
            if p:
                for j in range(k,n+1):
                    a[i][j] -= p*a[k][j]
    x = [F(0)] * n
    for i in range(n-1,-1,-1):
        x[i] = a[i][n] - sum(a[i][j]*x[j] for j in range(i+1,n))
    return x


def exit_chain_control(c, lam=F(1)):
    """Exact d=2,L=2 dual exit probability via dihedral lumping."""
    vertices = list(product([-1,0,1], repeat=2))
    index = {v:i for i,v in enumerate(vertices)}
    transforms = []
    for swap in [False,True]:
        for sx,sy in product([-1,1],repeat=2):
            transforms.append([index[(sx*(y if swap else x),
                                      sy*(x if swap else y))]
                               for x,y in vertices])
    def transform(state, mapping):
        return sum(1<<mapping[i] for i in range(9) if state>>i&1)
    orbit = {s:min(transform(s,t) for t in transforms) for s in range(512)}
    reps = sorted(set(orbit.values())-{0})
    ri = {s:i for i,s in enumerate(reps)}
    def transitions(state):
        rates = defaultdict(F)
        success = F(0)
        for i,(x,y) in enumerate(vertices):
            if not state>>i&1:
                continue
            rates[orbit[state & ~(1<<i)]] += 1
            for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                v = (x+dx,y+dy)
                if v not in index:
                    success += lam/4
                elif not state>>index[v]&1:
                    rates[orbit[state | (1<<index[v])]] += lam/4
        return dict(rates),success
    cached = {s:transitions(s) for s in range(1,512)}
    for s in range(1,512):
        c.check('exit_chain_lumpability', cached[s] == cached[orbit[s]])
    matrix = [[F(0) for _ in reps] for _ in reps]
    vector = []
    for s in reps:
        i = ri[s]
        rates,success = cached[s]
        matrix[i][i] = sum(rates.values()) + success
        for t,r in rates.items():
            if t:
                matrix[i][ri[t]] -= r
        vector.append(success)
    solution = gauss_solve(matrix,vector)
    h = {0:F(0)}
    h.update({s:solution[ri[orbit[s]]] for s in range(1,512)})
    for s in range(1,512):
        rates,success = cached[s]
        c.check('exit_chain_full_residual',
                (sum(rates.values())+success)*h[s]
                == success+sum(r*h[t] for t,r in rates.items()))
        c.check('exit_chain_probability', 0 < h[s] < 1)
    start = 1 << index[(0,0)]
    val = h[start]
    lower = (lam/(4+lam))**2
    cutoff = F(1,3)**9
    c.check('exit_chain_bounds', val >= lower > cutoff)
    for s in range(512):
        for i in range(9):
            c.check('exit_chain_monotone', h[s] <= h[s | (1<<i)])
    return {'d':2,'L':2,'lambda':str(lam),'transient_states':511,
            'dihedral_orbits':len(reps),'origin_exit_probability':str(val),
            'straight_path_lower':str(lower),'coloring_cutoff':str(cutoff),
            'scope':'Finite dual-exit computation; does not certify infinite-volume percolation.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    c = Checks()
    result = {'status':'PASS_EXACT_FINITE_CONTROLS',
              'original_problem_solved':False,
              'generator':generator_controls(c),
              'hyperplane':hyperplane_controls(c),
              'geometric_samples':geometric_controls(c),
              'exit_chain':exit_chain_control(c)}
    result['checks_by_category'] = dict(sorted(c.counts.items()))
    result['total_checks'] = sum(c.counts.values())
    result['limits'] = ('Finite controls corroborate algebra and constructions. '
        'They do not prove critical extinction, the source threshold gap, '
        'or all imported literature results. Analytic proofs are in PROOF.md.')
    text = json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text,end='')


if __name__ == '__main__':
    main()
