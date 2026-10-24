#!/usr/bin/env python3
"""Exact, standard-library checks of the scoped coordinate-flow statements.

This is a certificate sanity check, not a verification of all RAAG scl values.
"""
from __future__ import annotations
from collections import deque
from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
import argparse
import json
import random


def components(n, edges):
    adj = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        adj[u].append((v, i))
        if u != v:
            adj[v].append((u, i))
    out, seen = [], set()
    for root in range(n):
        if root in seen:
            continue
        todo, vs, es = [root], set(), set()
        seen.add(root)
        while todo:
            u = todo.pop()
            vs.add(u)
            for v, i in adj[u]:
                es.add(i)
                if v not in seen:
                    seen.add(v)
                    todo.append(v)
        out.append((vs, es))
    return out


def flow(n, edges, charges, required):
    """Spanning-tree integral construction; returns None if impossible."""
    adj = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        if u != v:
            adj[u].append((v, i))
            adj[v].append((u, i))
    ts = [0] * len(edges)
    for vs, _ in components(n, edges):
        reservoirs = vs - required
        if not reservoirs and sum(charges[v] for v in vs):
            return None
        root = min(reservoirs or vs)
        order, parent = [root], {root: None}
        for u in order:
            for v, i in adj[u]:
                if v not in parent:
                    parent[v] = (u, i)
                    order.append(v)
        residual = charges.copy()
        for v in reversed(order[1:]):
            u, i = parent[v]
            # Edge flow contributes +t at its head, -t at its tail.
            head = edges[i][1]
            t = -residual[v] if head == v else residual[v]
            ts[i] = t
            residual[u] += residual[v]
            residual[v] = 0
        assert reservoirs or residual[root] == 0
    w = charges.copy()
    for t, (u, v) in zip(ts, edges):
        w[u] -= t
        w[v] += t
    assert all(w[v] == 0 for v in required)
    return ts


def gaussian_feasible(n, edges, charges, required):
    """Independent rational elimination of the full incidence system."""
    rows = []
    for v in sorted(required):
        rows.append([Fraction(int(b == v) - int(a == v)) for a, b in edges]
                    + [Fraction(-charges[v])])
    pivot = 0
    for col in range(len(edges)):
        r = next((r for r in range(pivot, len(rows)) if rows[r][col]), None)
        if r is None:
            continue
        rows[pivot], rows[r] = rows[r], rows[pivot]
        z = rows[pivot][col]
        rows[pivot] = [x / z for x in rows[pivot]]
        for k in range(len(rows)):
            if k != pivot and rows[k][col]:
                z = rows[k][col]
                rows[k] = [a - z * b for a, b in zip(rows[k], rows[pivot])]
        pivot += 1
    return not any(not any(row[:-1]) and row[-1] for row in rows)


def voltage_cover(n, edges, m, voltages):
    lifted = []
    for (u, v), z in zip(edges, voltages):
        for sheet in range(m):
            lifted.append((u * m + sheet, v * m + (sheet + z) % m))
    return n * m, lifted


def free_product_reduce(word, modulus):
    """Normal form in C_modulus * Z; each token is ('b'|'d', exponent)."""
    out = []
    for letter, exponent in word:
        if letter == 'b':
            exponent %= modulus
        if not exponent:
            continue
        if out and out[-1][0] == letter:
            exponent += out.pop()[1]
            if letter == 'b':
                exponent %= modulus
            if exponent:
                out.append((letter, exponent))
        else:
            out.append((letter, exponent))
    return out


def z2_free_z_reduce(word):
    out = []
    for letter, exponent in word:
        token = ('A', (exponent if letter == 'a' else 0, exponent if letter == 'b' else 0)) if letter != 'd' else ('D', exponent)
        if out and out[-1][0] == token[0]:
            previous = out.pop()[1]
            value = tuple(a+b for a,b in zip(previous, token[1])) if token[0] == 'A' else previous+token[1]
            if value != ((0,0) if token[0] == 'A' else 0):
                out.append((token[0], value))
        elif token[1] != ((0,0) if token[0] == 'A' else 0):
            out.append(token)
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('CHECKS.json'))
    args = parser.parse_args()
    rng = random.Random(21127)
    tested = 0
    for n in range(1, 9):
        for _ in range(400):
            edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randrange(12))]
            charges = [rng.randrange(-5, 6) for _ in range(n)]
            required = {v for v in range(n) if rng.randrange(3)}
            answer = flow(n, edges, charges, required)
            assert (answer is not None) == gaussian_feasible(n, edges, charges, required)
            tested += 1

    brute_checked = 0
    for n in range(1, 4):
        for _ in range(35):
            edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randrange(4))]
            charges = [rng.randrange(-1, 2) for _ in range(n)]
            required = {v for v in range(n) if rng.randrange(2)}
            expected = flow(n, edges, charges, required) is not None
            found = False
            # Tree-solution flow magnitudes are <= total absolute charge <= n.
            for ts in product(range(-n, n + 1), repeat=len(edges)):
                w = charges.copy()
                for t, (a, b) in zip(ts, edges):
                    w[a] -= t
                    w[b] += t
                if all(not w[v] for v in required):
                    found = True
                    break
            assert expected == found
            brute_checked += 1

    # P4 piece cycle: M0,L0,M1,R0,M2,L1,M3,R1.
    labels = [{'b','c'}, {'a','b'}, {'b','c'}, {'c','d'},
              {'b','c'}, {'a','b'}, {'b','c'}, {'c','d'}]
    edges = [(i, (i + 1) % 8) for i in range(8)]
    edge_labels = ['b','b','c','c','b','b','c','c']
    charges = [{'b': 1}, {}, {}, {}, {'b': -1}, {}, {}, {}]
    p4 = {}
    for x in 'abcd':
        vs = [v for v in range(8) if x in labels[v]]
        local = {v: i for i, v in enumerate(vs)}
        xe = [(local[a], local[b]) for (a,b), y in zip(edges, edge_labels) if y == x]
        q = [charges[v].get(x, 0) for v in vs]
        cs = components(len(vs), xe)
        p4[x] = [{'vertices':[vs[v] for v in sorted(c)],
                  'charge':sum(q[v] for v in c),
                  'tree': len(es) == len(c) - 1} for c, es in cs]
        feasible = flow(len(vs), xe, q, set(range(len(vs)))) is not None
        assert feasible == (x != 'b')
    assert sum(c['charge'] for c in p4['b']) == 0
    assert sorted(c['charge'] for c in p4['b']) == [-1, 1]

    covers = []
    for m in range(1, 41):
        # A connected cyclic M-cover of the entire 8-cycle.
        nn, ee = voltage_cover(8, edges, m, [0]*7 + [1])
        bvs = [v*m+s for v in range(8) if 'b' in labels[v] for s in range(m)]
        local = {v:i for i,v in enumerate(bvs)}
        be = []
        for i, ((a,b), x) in enumerate(zip(edges, edge_labels)):
            if x == 'b':
                for s in range(m):
                    be.append((local[a*m+s], local[b*m+s]))
        bq = [charges[v//m].get('b', 0) for v in bvs]
        cs = components(len(bvs), be)
        assert len(cs) == 2*m
        assert all(len(es) == len(c)-1 and abs(sum(bq[v] for v in c)) == 1 for c, es in cs)
        assert flow(len(bvs), be, bq, set(range(len(bvs)))) is None
        exceptions = {local[v*m+s] for v in [0,4] for s in range(m)}
        assert len(exceptions) == 2*m
        assert flow(len(bvs), be, bq, set(range(len(bvs)))-exceptions) is not None
        # A one-loop charged graph has an M-cycle cover and only one exception.
        nv, ev = voltage_cover(1, [(0,0)], m, [1])
        qv = [1]*nv
        assert flow(nv, ev, qv, set(range(nv))) is None
        assert flow(nv, ev, qv, set(range(nv))-{0}) is not None
        covers.append({'degree':m,'p4_minimum_exceptions':2*m,
                       'cyclic_example_exceptions':1,'cyclic_loss':str(Fraction(1,m))})

    torsion_checks = []
    g = [('b',1), ('d',1), ('b',-1), ('d',-1)]
    for n in range(2, 101):
        word = []
        for i in range(n-1, -1, -1):
            word += [('b',i)] + g + [('b',-i)]
        assert free_product_reduce(word, n) == []
        assert free_product_reduce(g, n) != []
        bound = Fraction(n-2, 2*n)
        assert bound < Fraction(1,2)
        torsion_checks.append({'N':n,'sphere_degree':n,'Euler_characteristic':2-n,
                               'scl_upper_bound':str(bound)})
    forward = [('b',1), ('a',1), ('d',1), ('b',-1), ('a',-1), ('d',-1)]
    reverse = [('d',1), ('a',1), ('d',-1), ('a',-1)]
    comparison = [('a',1), ('d',1), ('a',-1), ('d',-1)]
    f_normal = z2_free_z_reduce(forward)
    c_normal = z2_free_z_reduce(comparison)
    assert len(f_normal) == len(c_normal) == 4
    assert all(f_normal != c_normal[i:]+c_normal[:i] for i in range(4))
    assert z2_free_z_reduce(reverse) == [('D',1),('A',(1,0)),('D',-1),('A',(-1,0))]
    chain = {'forward_word':'b a d b^-1 a^-1 d^-1 = [ab,d]',
             'reverse_word':'d a d^-1 a^-1 = [d,a]',
             'forward_cyclically_reduced_syllables':f_normal,
             'inverse_reverse_cyclically_reduced_syllables':c_normal,
             'no_conjugacy_by_cyclic_syllable_rotation':True,
             'original_piece_vertices':8,'bands':8,'capped_zero_charge_pieces':6,
             'resulting_Euler_characteristic':-2,'resulting_boundary_components':4}
    result = {'scope':'fixed-graph flow and explicit relaxation obstruction only; not RAAG rationality',
              'random_incidence_vs_gaussian_cases':tested,'independent_bruteforce_cases':brute_checked,
              'p4_coordinate_components':p4,'p4_boundary_chain':chain,'cover_checks':covers,'torsion_sphere_checks':torsion_checks,
              'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(), 'all_checks_passed':True}
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['random_incidence_vs_gaussian_cases','independent_bruteforce_cases','all_checks_passed']}))


if __name__ == '__main__':
    main()
