#!/usr/bin/env python3
"""Independent exact cellular row ranks; no author imports or dependencies."""
from pathlib import Path
from datetime import datetime, timezone
from math import gcd
import json
from independent_check import data


def primitive(row):
    g = 0
    for z in row:
        g = gcd(g, z)
    if g:
        row = [z // g for z in row]
    return row


def row_basis(rows):
    out = {}
    for original in rows:
        row = list(original)
        for p in sorted(out):
            if row[p]:
                old = row[p]
                pivot = out[p][p]
                row = primitive([pivot * x - old * y for x, y in zip(row, out[p])])
        if any(row):
            p = next(j for j, z in enumerate(row) if z)
            out[p] = primitive(row)
    return out


def check(k):
    g = data(k)
    n = 3 * k
    names = 'abct'
    forwards = {name: g[name][0] for name in names}
    backwards = {}
    for name, p in forwards.items():
        inv = [0] * n
        for j, z in enumerate(p):
            inv[z] = j
        backwards[name] = inv
    # Generator-major edge order, unlike the author's vertex-major order.
    def chain(word, start):
        row = [0] * (4 * n)
        v = start
        for letter in word:
            name = letter.lower()
            col = n * names.index(name)
            if letter.islower():
                row[col + v] += 1
                v = forwards[name][v]
            else:
                v = backwards[name][v]
                row[col + v] -= 1
        assert v == start
        return row
    relators = ['taTA', 'tbT' + 'A' * k + 'B', 'tcTbaBAC']
    rows = [chain(word, v) for word in relators for v in range(n)]
    basis = row_basis(rows)
    assert len(basis) == 2 * n - 3
    # The translation offset is an integral cocycle in this edge ordering.
    cochain = [z for name in names for z in g[name][1]]
    assert all(sum(x * y for x, y in zip(row, cochain)) == 0 for row in rows)
    # Test every a-cycle by exact rational row independence; no mod-p shortcut.
    visible = []
    for v in range(n):
        a_chain = chain('a' * k, v)
        assert len(row_basis(list(basis.values()) + [a_chain])) == len(basis) + 1
        visible.append(v)
    assert sum(x * y for x, y in zip(chain('a' * k, 0), cochain)) == -k
    return {'k': k, 'degree': n, 'C2_boundary_rank_Q': len(basis),
            'lifted_relators_checked': len(rows), 'cocycle': 'PASS',
            'a_power': k, 'a_visible_at_every_vertex': visible,
            'a_power_cocycle_at_vertex0': -k,
            'method': 'primitive integer row elimination computes Q-rank exactly'}


def main():
    out = {'utc': datetime.now(timezone.utc).isoformat(),
           'independent_cases': [check(k) for k in [2, 3, 5, 7]],
           'scope': 'Independently reproduces author lifted certificates for k=3,5,7 and adds k=2.'}
    Path(__file__).with_name('independent_cellular_results.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({'result': 'PASS', 'cases': 4, 'source': 'no author imports'}))


if __name__ == '__main__':
    main()
