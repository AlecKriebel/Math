#!/usr/bin/env python3
"""Independent exact checks of primary-source probability tables; no candidate input."""
from itertools import product, combinations
from collections import Counter
from fractions import Fraction
from pathlib import Path
from datetime import datetime, timezone
import json

STATES = tuple(product((0, 1), repeat=4))
EDGES = ((0, 1), (1, 2), (2, 3), (0, 3))

def projection(x, A):
    return tuple(x[i] for i in A)

def separated(A, B, C):
    allowed = set(range(4)) - set(C)
    seen = set(A)
    stack = list(A)
    while stack:
        i = stack.pop()
        for u, v in EDGES:
            j = v if u == i else u if v == i else None
            if j is not None and j in allowed and j not in seen:
                seen.add(j)
                stack.append(j)
    return not seen.intersection(B)

def all_global_checks(weights):
    tested, failed = [], []
    for assignment in product(range(4), repeat=4):
        A = tuple(i for i, a in enumerate(assignment) if a == 0)
        B = tuple(i for i, a in enumerate(assignment) if a == 1)
        C = tuple(i for i, a in enumerate(assignment) if a == 2)
        if not A or not B or not separated(A, B, C):
            continue
        row = {'A': [i+1 for i in A], 'B': [i+1 for i in B], 'C': [i+1 for i in C]}
        tables = {}
        for x in STATES:
            c, a, b = projection(x, C), projection(x, A), projection(x, B)
            table = tables.setdefault(c, {})
            table[a, b] = table.get((a, b), 0) + weights[x]
        bad = []
        for c, table in tables.items():
            rows = tuple(product((0, 1), repeat=len(A)))
            cols = tuple(product((0, 1), repeat=len(B)))
            for a1, a2 in combinations(rows, 2):
                for b1, b2 in combinations(cols, 2):
                    determinant = table[a1, b1]*table[a2, b2]-table[a1, b2]*table[a2, b1]
                    if determinant:
                        bad.append({'c': c, 'a1': a1, 'a2': a2, 'b1': b1, 'b2': b2, 'determinant': determinant})
        row['failures'] = bad
        tested.append(row)
        if bad:
            failed.append(row)
    return {'ordered_nontrivial_separation_checks': len(tested), 'checks': tested, 'failures': failed}

def mtp2_checks(weights):
    failures = []
    for x in STATES:
        for y in STATES:
            meet = tuple(min(a, b) for a, b in zip(x, y))
            join = tuple(max(a, b) for a, b in zip(x, y))
            left = weights[meet]*weights[join]
            right = weights[x]*weights[y]
            if left < right:
                failures.append({'x': x, 'y': y, 'meet': meet, 'join': join, 'left': left, 'right': right})
    return {'ordered_pairs_checked': len(STATES)**2, 'failure_count': len(failures), 'first_failures': failures[:8]}

def distribution_table(support, special=None):
    return {x: (special or {}).get(x, 1) if x in support else 0 for x in STATES}

def run_example(name, source, weights):
    support = {x for x in STATES if weights[x]}
    closure_failure = next(({'x': x, 'y': y} for x in support for y in support
        if tuple(min(a,b) for a,b in zip(x,y)) not in support or tuple(max(a,b) for a,b in zip(x,y)) not in support), None)
    join_support = {x for x in STATES if all(projection(x,e) in {projection(s,e) for s in support} for e in EDGES)}
    return {'name': name, 'source': source, 'integer_weights': {''.join(map(str,x)):weights[x] for x in STATES},
            'normalizer':sum(weights.values()), 'support_sublattice':closure_failure is None,
            'support_closure_failure':closure_failure, 'clique_projection_join_equals_support':join_support==support,
            'support_join_extra_states':[''.join(map(str,x)) for x in sorted(join_support-support)],
            'global_markov':all_global_checks(weights), 'mtp2':mtp2_checks(weights)}

def main():
    ks_support = {x for x in STATES if x[0] == x[1]}
    ks_weights = distribution_table(ks_support, {(0,0,0,0): 7})
    ex7_support = {tuple(map(int,s)) for s in ('0000','0001','1000','0011','1100','0111','1110','1111')}
    ex8_support = {tuple(map(int,s)) for s in ('0100','0111','1001','1010')}
    results = [run_example('Kahle–Sullivant Example 6.5 normalized reading',
        'arXiv:2411.03139v1, p.13, Example6.5; p_empty=1/2, others=1/14', ks_weights),
        run_example('Geiger–Meek–Sturmfels Example7', '2006 publisher pagination p.1480, (4.12)',distribution_table(ex7_support)),
        run_example('Geiger–Meek–Sturmfels Example8', '2006 publisher pagination p.1480',distribution_table(ex8_support))]
    U = tuple(tuple(map(int,s)) for s in ('0000','0011','1101','1110'))
    W = tuple(tuple(map(int,s)) for s in ('0001','0010','1100','1111'))
    balanced = {str(tuple(i+1 for i in e)): {'left':dict(Counter(''.join(map(str,projection(x,e))) for x in U)),
        'right':dict(Counter(''.join(map(str,projection(x,e))) for x in W))} for e in EDGES}
    assert all(v['left']==v['right'] for v in balanced.values())
    prod_left = prod_right = 1
    for x in U: prod_left *= ks_weights[x]
    for x in W: prod_right *= ks_weights[x]
    invariant={'left_states':[''.join(map(str,x)) for x in U], 'right_states':[''.join(map(str,x)) for x in W],
        'edge_multiplicity_balance': balanced, 'integer_product_left':prod_left,'integer_product_right':prod_right,
        'normalized_difference':str(Fraction(prod_left-prod_right,sum(ks_weights.values())**4))}
    ks=results[0]
    assert ks['normalizer']==14
    assert ks['support_sublattice']
    assert ks['mtp2']['failure_count']==0
    assert not ks['global_markov']['failures']
    assert invariant['integer_product_left']!=invariant['integer_product_right']
    assert results[1]['mtp2']['failure_count'] and results[2]['mtp2']['failure_count']
    output={'executed_actual_utc':datetime.now(timezone.utc).isoformat(timespec='microseconds'),
        'arithmetic':'integer weights and exact Fraction only; no floating point', 'candidate_material_read':False,
        'examples':results, 'ks_nonfactorization_invariant':invariant}
    Path('primary_examples_checks.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'ks_normalizer':ks['normalizer'],'ks_mtp2_pairs':ks['mtp2']['ordered_pairs_checked'],
        'ks_mtp2_failures':ks['mtp2']['failure_count'],'ks_global_separation_checks':ks['global_markov']['ordered_nontrivial_separation_checks'],
        'ks_global_failures':len(ks['global_markov']['failures']),'ks_invariant_left':prod_left,'ks_invariant_right':prod_right,
        'ks_invariant_normalized_difference':invariant['normalized_difference'],
        'gms_example7_mtp2_failures':results[1]['mtp2']['failure_count'],'gms_example8_mtp2_failures':results[2]['mtp2']['failure_count']},indent=2))

if __name__ == '__main__': main()
