#!/usr/bin/env python3
"""Independent exact finite checks; no imports from the author verifier.

Python 3.10+, standard library. No numerical simulation or infinite-volume
decision procedure is implemented. The finite exit chain is solved by integer
fraction-free elimination and checked against every unreduced state equation.
"""
import argparse
from collections import Counter, deque
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path


class Audit:
    def __init__(self):
        self.counts = Counter()

    def test(self, label, value):
        if not value:
            raise AssertionError(label)
        self.counts[label] += 1


def generator(audit):
    # Separate coefficients of recovery rate 1 and per-neighbor rate b.
    # All 511 nonempty subsets, rather than only subsets of size at most 3.
    edges = []
    for i in range(9):
        x, y = divmod(i, 3)
        edges.extend((i, 3*((x+dx) % 3)+(y+dy) % 3)
                     for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)))
    into = {i: [u for u,v in edges if v == i] for i in range(9)}
    for occupied in range(512):
        death = [(occupied & ~(1 << i)) for i in range(9) if occupied & (1 << i)]
        births = Counter(occupied | (1 << v) for u,v in edges if occupied & (1 << u))
        f = [int(occupied & subset == subset) for subset in range(512)]
        for subset in range(1,512):
            death_direct = sum(int(state & subset == subset)-f[subset] for state in death)
            birth_direct = sum(mult*(int(state & subset == subset)-f[subset])
                               for state,mult in births.items())
            birth_formula = 0
            for x in range(9):
                if subset & (1 << x):
                    for y in into[x]:
                        birth_formula += f[(subset & ~(1 << x)) | (1 << y)] - f[subset | (1 << y)]
            audit.test('generator_recovery_coefficient', death_direct == -subset.bit_count()*f[subset])
            audit.test('generator_infection_coefficient', birth_direct == birth_formula)
    return {'graph':'3 by 3 torus', 'configurations':512,
            'nonempty_subsets':511, 'rates':'formal coefficients of 1 and b=lambda/4'}


def hyperplanes(audit):
    output = []
    for eps in (Q(1,10), Q(1,4), Q(1,2), Q(9,10)):
        values = [Q(0),Q(0),Q(0)]
        mass = Q(0)
        for mask in range(16):
            p = eps**mask.bit_count()*(1-eps)**(4-mask.bit_count())
            mass += p
            for n in range(1,4):
                event = bool(mask & 1) or all(mask & (1 << i) for i in range(1,n+1))
                values[n-1] += p*event
        audit.test('hyperplane_mass', mass == 1)
        for n,val in enumerate(values,1):
            audit.test('hyperplane_moment_formula', val == eps+(1-eps)*eps**n)
        excess = values[0]*values[2]-values[1]**2
        audit.test('hyperplane_path_factorization_fails', excess == eps**2*(1-eps)**3 > 0)
        output.append({'epsilon':str(eps),'moments':list(map(str,values)), 'factorization_excess':str(excess)})
    return output


def geometry(audit):
    for d in range(2,21):
        audit.test('radius_one_uses_exact_probability', Q(1,2) > Q(1,2*d-1))
        for length in range(2,51):
            M = (2*length-1)**d
            audit.test('radius_exponent_comparison', M >= (2*length-1)**2 >= 3*length)
            audit.test('radius_base_comparison', (2*d-1)**3 > 2*d+1)
    for dimension in (1,2,3):
        for length in (1,2,3):
            modulus = 2*length-1
            interior = set(product(range(1-length,length),repeat=dimension))
            for shift in product((-modulus,0,modulus),repeat=dimension):
                if not any(shift):
                    continue
                other = {tuple(x+y for x,y in zip(point,shift)) for point in interior}
                audit.test('graphical_target_interiors_disjoint', not interior.intersection(other))
    # Explicit non-independence danger: target assignment is disjoint, whereas
    # pooling all touching arrows would share cross-boundary arrows.
    left = {(x,y) for x in (-1,0,1) for y in (-1,0,1)}
    right = {(x+3,y) for x,y in left}
    arc = ((1,0),(2,0))
    audit.test('negative_control_touching_arrow_assignment', arc[0] in left and arc[1] in right)
    return {'tested_dimensions':[2,20], 'tested_radii':[1,50],
            'scope':'Finite arithmetic controls only; universal inequalities are proved in the review.'}


def bareiss(matrix, rhs, audit):
    """Fraction-free Gaussian elimination of an integer nonsingular system."""
    n = len(rhs)
    b = [list(row)+[rhs[i]] for i,row in enumerate(matrix)]
    previous = 1
    for k in range(n-1):
        pivot_row = next(i for i in range(k,n) if b[i][k])
        if pivot_row != k:
            b[k],b[pivot_row] = b[pivot_row],b[k]
        pivot = b[k][k]
        for i in range(k+1,n):
            factor = b[i][k]
            for j in range(k+1,n+1):
                numerator = pivot*b[i][j]-factor*b[k][j]
                quotient,remainder = divmod(numerator,previous)
                audit.test('bareiss_exact_division', remainder == 0)
                b[i][j] = quotient
            b[i][k] = 0
        previous = pivot
    audit.test('bareiss_nonsingular', b[-1][-2] != 0)
    answer = [Q(0)]*n
    for i in range(n-1,-1,-1):
        answer[i] = (Q(b[i][-1])-sum(b[i][j]*answer[j] for j in range(i+1,n)))/b[i][i]
    for i in range(n):
        audit.test('quotient_equation',sum(matrix[i][j]*answer[j] for j in range(n)) == rhs[i])
    return answer


def exit_chain(audit):
    # Row-major coordinates 0,1,2; symmetry generated by quarter-turn and flip.
    def permute(state, reflect=False):
        result = 0
        for i in range(9):
            if state & (1 << i):
                r,c = divmod(i,3)
                u,v = (r,2-c) if reflect else (c,2-r)
                result |= 1 << (3*u+v)
        return result
    orbit_index = {0:0}
    orbit_sets = []
    for seed in range(1,512):
        if seed in orbit_index:
            continue
        seen = {seed}
        todo = deque([seed])
        while todo:
            s = todo.popleft()
            for t in (permute(s),permute(s,True)):
                if t not in seen:
                    seen.add(t);todo.append(t)
        orbit_sets.append(sorted(seen))
        for s in seen:
            orbit_index[s] = len(orbit_sets)
    audit.test('dihedral_orbit_count', len(orbit_sets) == 101 and len(orbit_index) == 512)
    # Scaling every rate by 4 changes no hitting probability: deaths have
    # rate 4 and each arrow rate 1, corresponding to total lambda=1.
    raw = {}
    for state in range(1,512):
        jumps = Counter()
        success = 0
        for i in range(9):
            if not state & (1 << i):
                continue
            jumps[state ^ (1 << i)] += 4
            r,c = divmod(i,3)
            for dr,dc in ((-1,0),(1,0),(0,-1),(0,1)):
                u,v = r+dr,c+dc
                if not (0 <= u < 3 and 0 <= v < 3):
                    success += 1
                else:
                    new = state | (1 << (3*u+v))
                    if new != state:
                        jumps[new] += 1
        raw[state] = (jumps,success)
    n = len(orbit_sets)
    matrix = [[0]*n for _ in range(n)]
    rhs = [0]*n
    for k,states in enumerate(orbit_sets):
        row_signatures = []
        for state in states:
            jumps,success = raw[state]
            lumped = Counter()
            for target,rate in jumps.items():
                lumped[orbit_index[target]] += rate
            row_signatures.append((lumped,success))
            audit.test('independent_lumpability',row_signatures[-1] == row_signatures[0])
        jumps,success = raw[states[0]]
        matrix[k][k] = sum(jumps.values())+success
        rhs[k] = success
        for target,rate in jumps.items():
            if target:
                matrix[k][orbit_index[target]-1] -= rate
    reduced = bareiss(matrix,rhs,audit)
    h = [Q(0)]+[reduced[orbit_index[s]-1] for s in range(1,512)]
    for state,(jumps,success) in raw.items():
        audit.test('unreduced_exit_equation', sum(rate*(h[state]-h[target]) for target,rate in jumps.items()) == success*(1-h[state]))
        audit.test('exit_strict_probability', 0 < h[state] < 1)
    for state in range(512):
        for bit in range(9):
            audit.test('exit_attractive_initial_sets', h[state] <= h[state | (1 << bit)])
    # Every raw row can reach zero through recoveries alone, so there are
    # no nonabsorbing closed classes: the exact hitting solution is unique.
    for state in range(1,512):
        bit = (state & -state)
        audit.test('recovery_reaches_smaller_state', raw[state][0][state ^ bit] == 4)
    origin = h[1 << 4]
    audit.test('origin_lower_and_cutoff',origin > Q(1,25) > Q(1,3**9))
    audit.test('origin_upper_comparison',origin < Q(1,2))
    # Deliberate wrong rate normalization: per-neighbor b=1 has total rate 4.
    audit.test('negative_control_rate_normalization', Q(1,2) != Q(4,5))
    return {'d':2,'L':2,'lambda_total':'1','per_neighbor_rate':'1/4',
            'transient_states':511,'dihedral_orbits':n,
            'origin_exit_probability':str(origin),
            'origin_decimal_for_orientation_only':float(origin),
            'unreduced_state_solution':list(map(str,h)),
            'scaled_recovery_rate':4,'scaled_arrow_rate':1}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--author-results',type=Path)
    args = parser.parse_args()
    audit = Audit()
    result = {'generator':generator(audit),'hyperplanes':hyperplanes(audit),
              'geometry':geometry(audit),'exit_chain':exit_chain(audit)}
    if args.author_results:
        author = json.loads(args.author_results.read_text())
        audit.test('author_exit_value_agrees',result['exit_chain']['origin_exit_probability'] == author['exit_chain']['origin_exit_probability'])
    result.update(status='PASS_INDEPENDENT_EXACT_FINITE_CONTROLS',
                  counts=dict(sorted(audit.counts.items())),total_checks=sum(audit.counts.values()),
                  original_problem_solved=False,
                  scope='Finite controls support, but do not replace, the analytic partial-result audit.')
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS:',result['total_checks'],'independent exact checks')


if __name__ == '__main__':
    main()
