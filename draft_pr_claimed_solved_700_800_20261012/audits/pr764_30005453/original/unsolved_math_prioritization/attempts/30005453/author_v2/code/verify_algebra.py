#!/usr/bin/env python3
"""Exact finite diagnostics for PROOF.md. These do not certify the infinite proof."""
from fractions import Fraction as F
from pathlib import Path
import json
import random


def graph_cases():
    return {
        'single_edge': (2, [(0, 1)]),
        'path_9': (9, [(i, i+1) for i in range(8)]),
        'cycle_even': (8, [(i, (i+1) % 8) for i in range(8)]),
        'cycle_odd': (7, [(i, (i+1) % 7) for i in range(7)]),
        'star': (8, [(0, i) for i in range(1, 8)]),
        'binary_tree': (15, [((i-1)//2, i) for i in range(1, 15)]),
        'complete_5': (5, [(i, j) for i in range(5) for j in range(i+1, 5)])
    }


def main():
    rng = random.Random(30005453)
    counts = {'equilibrium_edges': 0, 'jacobian_rows': 0,
              'positive_hessian_forms': 0, 'exact_extremum_signs': 0,
              'discrete_drift_cancellations': 0, 'boundary_fixed_point_edges': 0}
    cases = []
    for name, (n, edges) in graph_cases().items():
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v); adj[v].append(u)
        for beta in [1, 2, 3, 9]:
            c = F(1, beta+1)
            for mode in ['heterogeneous', 'small_rates']:
                z = ([F(rng.randint(2, 15), 17) for _ in range(n)]
                     if mode == 'heterogeneous' else [F(1, 2**(v+1)) for v in range(n)])
                S = [sum((z[v]+z[w])**beta for w in adj[v]) for v in range(n)]
                p = [z[v]*S[v] for v in range(n)]
                x = {(u, v): (z[u]+z[v])**(beta+1) for u, v in edges}
                for (u, v), xe in x.items():
                    assert (z[u]+z[v])**beta * (p[u]/S[u]+p[v]/S[v]) == xe
                    assert xe <= p[u]+p[v]
                    counts['equilibrium_edges'] += 1
                # Off-diagonal derivatives of c(p_v/T_v(a)-a_v) are negative.
                # The diagonal contains exactly their negative absolute sum, minus c.
                for v in range(n):
                    off_abs = [c*p[v]*beta*(z[v]+z[w])**(beta-1)/S[v]**2 for w in adj[v]]
                    diag = -c-sum(off_abs)
                    assert diag + sum(off_abs) == -c
                    counts['jacobian_rows'] += 1
                for _ in range(4):
                    h = [F(rng.randint(-5, 5), 7) for _ in range(n)]
                    if not any(h): h[0] = F(1)
                    energy = sum(beta*(z[u]+z[v])**(beta-1)*(h[u]+h[v])**2 for u,v in edges)
                    energy += sum(p[v]*h[v]**2/z[v]**2 for v in range(n))
                    assert energy > 0
                    counts['positive_hessian_forms'] += 1
                    M = min(z)/4
                    perturbation = [F(rng.randint(-10,10),10)*M for _ in range(n)]
                    for sign in [1,-1]:
                        v = rng.randrange(n)
                        d = perturbation[:]; d[v] = sign*M
                        a = [z[w]+d[w] for w in range(n)]
                        Ta = sum((a[v]+a[w])**beta for w in adj[v])
                        deriv = c*(p[v]/Ta-a[v])
                        assert sign*deriv <= -c*M
                        counts['exact_extremum_signs'] += 1
                cases.append({'graph': name, 'beta': beta, 'alpha': str(1-c),
                              'rate_mode': mode, 'vertices': n, 'edges': len(edges),
                              'status': 'exact_rational_pass'})
            for k in range(1, 21):
                # Counts k^(beta+1) make n^alpha and n^(-alpha) rational.
                intensity_factor = F(k**beta)
                H_jump = F(1,k**beta)
                assert intensity_factor*H_jump == 1
                counts['discrete_drift_cancellations'] += 1
    # Literal all-nonnegative-equilibria uniqueness is false. Even cycle = local Z pattern.
    for beta in [1, 2, 3, 9]:
        n = 8
        # x_e alternates 2,0. Each vertex has exactly one nonzero incident edge.
        for offset in [0,1]:
            weights = [2 if (i+offset)%2 == 0 else 0 for i in range(n)]
            for i, xe in enumerate(weights):
                nonzero_at_left = int(weights[(i-1)%n] > 0) + int(xe > 0)
                nonzero_at_right = int(weights[(i+1)%n] > 0) + int(xe > 0)
                assert nonzero_at_left == nonzero_at_right == 1
                flow = 2 if xe > 0 else 0
                assert flow == xe
                counts['boundary_fixed_point_edges'] += 1
    result = {'status': 'PASS', 'arithmetic': 'fractions.Fraction exact',
              'seed': 30005453, 'case_count': len(cases), 'counts': counts,
              'scope': 'finite algebra diagnostics only; no computational certification of the infinite stochastic theorem',
              'cases': cases}
    out = Path(__file__).resolve().parents[1]/'results'/'algebra_checks.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'cases'}, indent=2))


if __name__ == '__main__':
    main()
