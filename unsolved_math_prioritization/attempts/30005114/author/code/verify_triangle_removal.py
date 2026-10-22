#!/usr/bin/env python3
"""Exact finite checks accompanying the authored triangle-removal partial results.
Standard library only. These checks do not prove the asymptotic open problem.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations
from math import comb
import argparse, json
from pathlib import Path


def instance(n):
    edges = list(combinations(range(n), 2))
    edge_index = {e: i for i, e in enumerate(edges)}
    triangles = list(combinations(range(n), 3))
    masks = [sum(1 << edge_index[e] for e in combinations(t, 2)) for t in triangles]
    return edges, triangles, masks


def terminal_distribution(n):
    edges, triangles, masks = instance(n)
    active = {(0, 0): F(1)}
    terminal = defaultdict(F)
    levels = []
    for step in range(len(edges) // 3 + 1):
        levels.append(len(active))
        nxt = defaultdict(F)
        for (used, chosen), prob in active.items():
            available = [j for j, mask in enumerate(masks) if not used & mask]
            if not available:
                terminal[chosen] += prob
            else:
                for j in available:
                    nxt[(used | masks[j], chosen | (1 << j))] += prob / len(available)
        active = nxt
    assert not active
    assert sum(terminal.values()) == 1
    expected_size = sum(prob * chosen.bit_count() for chosen, prob in terminal.items())
    marginals = [sum(prob for chosen, prob in terminal.items() if chosen >> j & 1)
                 for j in range(len(triangles))]
    assert sum(marginals) == expected_size
    assert len(set(marginals)) == 1
    pair = None
    if n >= 5:
        a, b = triangles.index((0, 1, 2)), triangles.index((0, 3, 4))
        joint = sum(prob for chosen, prob in terminal.items()
                    if chosen >> a & 1 and chosen >> b & 1)
        pair = {'triangles': [[0, 1, 2], [0, 3, 4]], 'joint': str(joint),
                'marginal': str(marginals[a]),
                'joint_over_product': str(joint / (marginals[a] * marginals[b]))}
    return {'n': n, 'active_states_by_step': levels, 'terminal_outputs': len(terminal),
            'expected_output_size': str(expected_size), 'one_triangle_marginal': str(marginals[0]),
            'selected_pair': pair}


def hazard_checks(n=5):
    edges, triangles, masks = instance(n)
    checked = 0
    multiplicity_slack_min = None
    wedge_slack_min = None
    for graph in range(1 << len(edges)):
        available = [j for j, mask in enumerate(masks) if graph & mask == mask]
        # Enumerate every nonempty edge-disjoint prescribed family in this graph.
        def extend(start, chosen, used):
            nonlocal checked, multiplicity_slack_min, wedge_slack_min
            for pos in range(start, len(available)):
                j = available[pos]
                if masks[j] & used:
                    continue
                fam = chosen + [j]
                union = used | masks[j]
                r = len(fam)
                degrees = [0] * n
                protected_edges = [e for i, e in enumerate(edges) if union >> i & 1]
                for u, v in protected_edges:
                    degrees[u] += 1; degrees[v] += 1
                delta = max(degrees)
                d = min(sum(1 for t in available if masks[t] >> i & 1)
                        for i in range(len(edges)) if union >> i & 1)
                bad = sum(1 for t in available if t not in fam and masks[t] & union)
                slack1 = bad - r * (d - 1)
                slack2 = bad - 3 * r * (d - delta)
                assert slack1 >= 0
                assert slack2 >= 0
                multiplicity_slack_min = slack1 if multiplicity_slack_min is None else min(multiplicity_slack_min, slack1)
                wedge_slack_min = slack2 if wedge_slack_min is None else min(wedge_slack_min, slack2)
                checked += 1
                extend(pos + 1, fam, union)
        extend(0, [], 0)
    return {'n': n, 'graphs': 1 << len(edges), 'graph_family_pairs': checked,
            'bad_ge_r_d_minus_one': True, 'bad_ge_3r_d_minus_delta': True,
            'minimum_multiplicity_slack': multiplicity_slack_min,
            'minimum_wedge_slack': wedge_slack_min}


def scalar_barrier_checks():
    # The proof reduces to 3*(.99-.1)-.5 > 2*1.01.
    margin = 3 * (F(99, 100) - F(1, 10)) - F(1, 2) - 2 * F(101, 100)
    assert margin == F(3, 20)
    checks = 0
    for n in [100, 200, 1000, 10000]:
        h = F(6, n*n)
        for p in [F(1), F(3,4), F(1,2), F(1,4), F(1,10)]:
            if h >= p:
                continue
            pp = p-h
            q = F(2,n)/p**2
            qp = F(2,n)/pp**2
            beta = 3*(F(99,100)-F(1,10))*n*p*p
            upper_Q = F(101,600)*n**3*p**3
            assert beta + 1 - 1/qp >= upper_Q*(1-q/qp)
            checks += 1
    # Bernoulli's inequality is used for every r, not only these checks.
    for r in range(1,101):
        for a in [F(1,10), F(1,3), F(1,2), F(9,10), F(999,1000)]:
            assert a**r >= 1-r*(1-a)
    return {'rational_margin': str(margin), 'parameter_checks': checks,
            'bernoulli_spot_checks': 500, 'universal_argument_in_report': True}


def bose_system(q):
    assert q % 2 == 1
    inv2 = (q+1)//2
    vertex = lambda x, i: 3*x+i
    triples = [tuple(vertex(x,i) for i in range(3)) for x in range(q)]
    for x,y in combinations(range(q),2):
        z = ((x+y)*inv2) % q
        for i in range(3):
            triples.append(tuple(sorted((vertex(x,i),vertex(y,i),vertex(z,(i+1)%3)))))
    counts = defaultdict(int)
    for t in triples:
        assert len(set(t)) == 3
        for e in combinations(sorted(t),2):
            counts[e] += 1
    s = 3*q
    assert len(triples) == s*(s-1)//6
    assert len(counts) == comb(s,2)
    assert set(counts.values()) == {1}
    return triples


def dense_barrier_witness():
    s = 201
    triples = bose_system(s//3)
    n=2*s; r=len(triples); Q=comb(n,3)
    bad = comb(s,3)+comb(s,2)*(n-s)-r
    assert bad == r*(3*n-2*s-3)
    p_next = 1-F(6,n*n)
    q_next = F(2,n)/p_next**2
    bracket = 1-F(r+bad,Q)+F(r,Q)/q_next
    ratio = bracket/p_next**(2*r)
    assert ratio > 1
    # Every first-step outcome is isomorphic, and neither side is killed by the 1% bounds.
    assert n-2 >= F(99,100)*n
    assert F(99,600)*n**3 <= Q <= F(101,600)*n**3
    assert n-4 >= F(99,100)*n*p_next**2
    Q_next = Q-(3*n-8)
    assert F(99,600)*n**3*p_next**3 <= Q_next <= F(101,600)*n**3*p_next**3
    return {'n': n, 'subsystem_vertices': s, 'bose_parameter': s//3,
            'target_triangles': r, 'target_shadow_max_degree': s-1,
            'initial_bad_triangles': bad, 'initial_total_triangles': Q,
            'positive_drift_exact_rational_comparison': True,
            'first_step_not_killed_by_trajectory_bounds': True,
            'drift_ratio_decimal_diagnostic': float(ratio),
            'limiting_ratio': '(5/8)*exp(1/2) > 1',
            'limiting_lower_bound_by_exp_series': '65/64 > 1',
            'scope': 'A counterexample to an unrestricted proposed potential inequality, not to the open problem. The finite n stopping time is not the problem stopping time.'}


def run():
    distribution = [terminal_distribution(n) for n in range(3,8)]
    n5 = next(x for x in distribution if x['n']==5)
    assert n5['selected_pair']['joint'] == '1/15'
    assert n5['selected_pair']['marginal'] == '1/5'
    assert n5['selected_pair']['joint_over_product'] == '5/3'
    return {'status':'PASS', 'arithmetic':'exact fractions and integer comparisons, except labeled diagnostic float',
            'terminal_distributions':distribution, 'hazard_enumeration':hazard_checks(),
            'scalar_barrier':scalar_barrier_checks(), 'dense_barrier_witness':dense_barrier_witness(),
            'limits':['Not a full resolution of problem 30005114.',
                      'Finite checks do not establish the asymptotic quasirandomness theorem.',
                      'The complete analytic proofs and their hypotheses are in REPORT.md.']}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output');args=ap.parse_args()
    result=run();text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:Path(args.output).write_text(text)
    print(text,end='')
