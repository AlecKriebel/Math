#!/usr/bin/env python3
"""Check scalar zero/pole orders and parity constraints, not invariant-functional spaces."""
import json, itertools
from pathlib import Path
S = {'A': (0, 2), 'B': (1, 4), 'C': (3, 3), 'D': (2, 5), 'E': (4, 6)}

def lexps(d, e):
    a, b = d
    c, f = e
    return list(range(b - c, b - c - min(b - a + 1, f - c + 1), -1))

def gamma_ord(d, e, eta):
    if eta:
        return 0
    return lexps(d, e).count(0) - lexps(e, d).count(-1)

def main():
    rows = []
    for kind, pairs in [('linked', [('E', 'D'), ('D', 'B'), ('B', 'A'), ('E', 'C'), ('C', 'A')]), ('nested', [('D', 'C'), ('C', 'B')])]:
        for u, v in pairs:
            for equal in (False, True):
                eta = equal
                fw = gamma_ord(S[u], S[v], eta)
                rv = gamma_ord(S[v], S[u], eta)
                ratio = rv - fw
                if not (ratio == 0 if equal or kind == 'nested' else ratio > 0):
                    raise RuntimeError('Diagnostic invariant failed')
                rows.append({'kind': kind, 'pair': [u, v], 'equal_lift_labels': equal, 'forward_L_exponents': lexps(S[u], S[v]), 'reverse_L_exponents': lexps(S[v], S[u]), 'forward_gamma_order': fw, 'reverse_gamma_order': rv, 'coefficient_order': ratio})
    orders = [['E', 'D', 'C', 'B', 'A'], ['E', 'C', 'D', 'B', 'A'], ['E', 'D', 'B', 'C', 'A']]
    for o in orders:
        for i, j in itertools.combinations(o, 2):
            a, b = S[i]
            c, d = S[j]
            if not not a <= c <= b <= d:
                raise RuntimeError('Diagnostic invariant failed')
    edges = [('E', 'D'), ('D', 'B'), ('B', 'A'), ('A', 'C'), ('C', 'E')]
    good = []
    for bits in itertools.product((0, 1), repeat=4):
        labels = {'E': 0, **dict(zip(['D', 'C', 'B', 'A'], bits))}
        if all((labels[a] != labels[b] for a, b in edges)):
            good.append(labels)
    if not not good:
        raise RuntimeError('Diagnostic invariant failed')
    out = {'kind': 'Scalar and finite-label diagnostic, conditional on the cited analytic interfaces', 'all_three_FLO_order_hypotheses_checked': True, 'all_zero_pole_checks_passed': True, 'tested_labels_mod_global_twist': 16, 'surviving_labels': good, 'computed_Hom_space': False, 'gamma_checks': rows}
    print(json.dumps(out, indent=2, sort_keys=True))
if __name__ == '__main__':
    main()
