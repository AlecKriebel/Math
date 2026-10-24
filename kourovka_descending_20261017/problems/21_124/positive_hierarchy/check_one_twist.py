#!/usr/bin/env python3
"""Exact bounded checks for ONE_TWIST_CUBULATION.md; not a specialness test.

Only Python's standard library is used. The proof is the general argument in
the accompanying note. This constructs the actual square complexes, all vertex
links, the chosen cover and VH double cover, and checks the stated free-word
monodromy formulas. Run from any directory; output is written next to this file.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from itertools import product
from math import gcd
from pathlib import Path
import hashlib
import json


def reduced(word):
    out = []
    for x in word:
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return tuple(out)


def inverse(word):
    return tuple(-x for x in reversed(word))


def substitute(word, images):
    out = ()
    for x in word:
        image = images[abs(x)]
        out = reduced(out + (image if x > 0 else inverse(image)))
    return out


def egcd(a, b):
    if b == 0:
        return abs(a), (1 if a >= 0 else -1), 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


def character(exponents):
    value, coeff = 0, []
    for exponent in exponents:
        new_value, s, t = egcd(value, exponent)
        coeff = [s * x for x in coeff] + [t]
        value = new_value
    assert value > 0
    assert sum(x * y for x, y in zip(exponents, coeff)) == value
    return value, tuple(coeff)


class Squares:
    def __init__(self):
        self.vertices = set()
        self.edges = []  # tail, head, name, type, voltage
        self.squares = []  # cyclic oriented edge ids; ids start at 1

    def edge(self, tail, head, name, edge_type, voltage=0):
        self.vertices.update((tail, head))
        self.edges.append((tail, head, name, edge_type, voltage))
        return len(self.edges)

    def ends(self, signed_edge):
        tail, head, *_ = self.edges[abs(signed_edge) - 1]
        return (tail, head) if signed_edge > 0 else (head, tail)

    def square(self, boundary):
        boundary = tuple(boundary)
        assert len(boundary) == 4
        for x, y in zip(boundary, boundary[1:] + boundary[:1]):
            assert self.ends(x)[1] == self.ends(y)[0]
        self.squares.append(boundary)

    def check_npc(self):
        links = defaultdict(Counter)
        for square in self.squares:
            for prev, cur in zip(square[-1:] + square[:-1], square):
                v = self.ends(cur)[0]
                directions = tuple(sorted((-prev, cur)))
                assert directions[0] != directions[1], (v, 'link loop')
                links[v][directions] += 1
        link_edges = 0
        for v, incidences in links.items():
            assert max(incidences.values(), default=0) <= 1, (v, 'double link edge')
            adjacency = defaultdict(set)
            for x, y in incidences:
                adjacency[x].add(y)
                adjacency[y].add(x)
            for x, neighbours in adjacency.items():
                for y in neighbours:
                    assert not (neighbours & adjacency[y]), (v, 'link triangle')
            link_edges += len(incidences)
        return link_edges


def ambient_complex(word, rank, k):
    L = len(word)
    out = Squares()
    # R has k edges on each basis circle, all at common vertex (0,0).
    rv = lambda a, j: (0, 0) if j in (0, k) else (a, j)
    f_edges, z_edges = {}, {}
    rose_vertices = {(0, 0)} | {(a, j) for a in range(1, rank + 1) for j in range(1, k)}
    for v in sorted(rose_vertices):
        for n in range(L):
            z_edges[v, n] = out.edge((v, n), (v, (n + 1) % L), ('z', v, n), 'z')
    for a in range(1, rank + 1):
        for j in range(k):
            for n in range(L):
                f_edges[a, j, n] = out.edge((rv(a, j), n), (rv(a, j + 1), n), ('f', a, j, n), 'f')
    for a in range(1, rank + 1):
        for j in range(k):
            for n in range(L):
                out.square((f_edges[a, j, n], z_edges[rv(a, j + 1), n],
                            -f_edges[a, j, (n + 1) % L], -z_edges[rv(a, j), n]))
    right_path = []
    for letter in word:
        if letter > 0:
            right_path.extend(f_edges[letter, j, 0] for j in range(k))
        else:
            right_path.extend(-f_edges[-letter, j, 0] for j in reversed(range(k)))
    left_path = [z_edges[(0, 0), j % L] for j in range(k * L)]
    transverse = [out.edge(out.ends(left_path[j])[0], out.ends(right_path[j])[0],
                          ('c', j), 'c', 1) for j in range(k * L)]
    for j in range(k * L):
        out.square((left_path[j], transverse[(j + 1) % (k * L)],
                    -right_path[j], -transverse[j]))
    return out, f_edges, z_edges, left_path, right_path


def cover(base, modulus, edge_voltages):
    out = Squares()
    lifted_edges = {}
    for eid, (tail, head, name, kind, _) in enumerate(base.edges, 1):
        voltage = edge_voltages[eid] % modulus
        for sheet in range(modulus):
            lifted_edges[eid, sheet] = out.edge((tail, sheet), (head, (sheet + voltage) % modulus),
                                               (name, sheet), kind, voltage)
    for square in base.squares:
        for initial_sheet in range(modulus):
            sheet = initial_sheet
            boundary = []
            for signed in square:
                voltage = edge_voltages[abs(signed)]
                if signed > 0:
                    boundary.append(lifted_edges[signed, sheet])
                    sheet = (sheet + voltage) % modulus
                else:
                    sheet = (sheet - voltage) % modulus
                    boundary.append(-lifted_edges[-signed, sheet])
            assert sheet == initial_sheet
            out.square(boundary)
    return out, lifted_edges


def original_complex(word, rank, k, chi):
    ambient, fs, zs, left, right = ambient_complex(word, rank, k)
    # A vertex-product cover is specified on a maximal tree by zero voltages;
    # the last a_i edge has chi_i, and the last z edge has 1. Their generator
    # voltages are n+chi(g) mod k. Both attaching loops have voltage zero.
    voltage = {}
    for eid, (_, _, name, kind, _) in enumerate(ambient.edges, 1):
        if kind == 'f':
            _, a, j, _ = name
            voltage[eid] = chi[a - 1] if j == k - 1 else 0
        elif kind == 'z':
            _, _, n = name
            voltage[eid] = 1 if n == len(word) - 1 else 0
        else:
            voltage[eid] = 0
    # Voltage for transverse edge j is forced by the annulus-square relation.
    initial_left = initial_right = 0
    transverse_voltage = {}
    for j, (le, re) in enumerate(zip(left, right)):
        transverse_voltage[j] = (initial_right - initial_left) % k
        initial_left += voltage[abs(le)] * (1 if le > 0 else -1)
        initial_right += voltage[abs(re)] * (1 if re > 0 else -1)
    assert initial_left % k == initial_right % k == 0
    for eid, (_, _, name, kind, _) in enumerate(ambient.edges, 1):
        if kind == 'c':
            voltage[eid] = transverse_voltage[name[1]]
    full_cover, lifts = cover(ambient, k, voltage)
    # Keep all vertex-product lifts but only the annulus that begins on sheet0.
    kept = {lifts[eid, sheet] for eid, edge in enumerate(ambient.edges, 1)
            if edge[3] != 'c' for sheet in range(k)}
    left_sheet = 0
    for j, le in enumerate(left):
        ambient_c = next(eid for eid, edge in enumerate(ambient.edges, 1) if edge[2] == ('c', j))
        kept.add(lifts[ambient_c, left_sheet])
        left_sheet = (left_sheet + voltage[le]) % k
    out = Squares()
    renumber = {}
    for eid in sorted(kept):
        renumber[eid] = out.edge(*full_cover.edges[eid - 1])
    for square in full_cover.squares:
        if all(abs(eid) in kept for eid in square):
            out.square(tuple(renumber[abs(eid)] * (1 if eid > 0 else -1) for eid in square))
    assert len(out.vertices) == k * len({edge[0] for edge in ambient.edges if edge[3] != 'c'} |
                                       {edge[1] for edge in ambient.edges if edge[3] != 'c'})
    return ambient, out


def monodromy_check(word, rank, k):
    images = {i: (i,) for i in range(1, rank + 1)}
    images.update({rank + j + 1: ((rank + j + 2,) if j < k - 1 else (rank + 1,) + word)
                   for j in range(k)})
    inv = {i: (i,) for i in range(1, rank + 1)}
    inv[rank + 1] = (rank + k,) + inverse(word)
    inv.update({rank + j + 1: (rank + j,) for j in range(1, k)})
    for i in images:
        assert substitute(images[i], inv) == (i,)
        assert substitute(inv[i], images) == (i,)
        powered = (i,)
        for _ in range(k):
            powered = substitute(powered, images)
        assert powered == ((i,) if i <= rank else (i,) + word)
    return len(images)


def check_word(word, rank):
    assert reduced(word) == word and word[0] != -word[-1]
    exponents = tuple(sum((x == a) - (x == -a) for x in word) for a in range(1, rank + 1))
    if not any(exponents):
        return None
    k, chi = character(exponents)
    ambient, original = original_complex(word, rank, k, chi)
    ambient_links = ambient.check_npc()
    original_links = original.check_npc()
    # Double cover transverse c parity. Product-cover edges have parity0.
    parity = {eid: int(edge[3] == 'c') for eid, edge in enumerate(original.edges, 1)}
    double, _ = cover(original, 2, parity)
    double.check_npc()
    colors = {}
    for eid, (tail, _, _, kind, _) in enumerate(double.edges, 1):
        sheet = tail[1]
        colors[eid] = ((kind == 'z') ^ bool(sheet)) if kind != 'c' else bool(sheet)
    for square in double.squares:
        c = [colors[abs(eid)] for eid in square]
        assert c[0] == c[2] and c[1] == c[3] and c[0] != c[1]
    n = monodromy_check(word, rank, k)
    return {'word': list(word), 'rank': rank, 'gcd': k, 'character': list(chi),
            'fiber_rank': n, 'ambient_cells': [len(ambient.vertices), len(ambient.edges), len(ambient.squares)],
            'original_cells': [len(original.vertices), len(original.edges), len(original.squares)],
            'double_cells': [len(double.vertices), len(double.edges), len(double.squares)],
            'link_edges': [ambient_links, original_links]}


def main():
    cases = []
    omitted_zero_ab = 0
    # Every rank-two cyclically reduced word of length<=5, with nonzero H1.
    alphabet = (1, -1, 2, -2)
    for length in range(1, 6):
        for word in product(alphabet, repeat=length):
            if reduced(word) != word or word[0] == -word[-1]:
                continue
            result = check_word(word, 2)
            if result is None:
                omitted_zero_ab += 1
            else:
                cases.append(result)
    extra_words = [(2, (1, 1, 2, 2)), (2, (1, 2, -1, -2, 1)),
                   (2, (1,) * 6), (3, (1, 2, -1, 3, 2, -3)),
                   (3, (1, 1, 2, 2, 3, 3)), (4, (1, -2, 3, 4, -1, 2))]
    for rank, word in extra_words:
        result = check_word(word, rank)
        assert result is not None
        cases.append(result)
    here = Path(__file__).resolve().parent
    payload = {'utc': datetime.now(timezone.utc).isoformat(), 'status': 'PASS',
               'scope': 'NPC links, VH coloring, exact monodromy; no RAAG-embedding test',
               'case_count': len(cases), 'zero_abelianization_excluded': omitted_zero_ab,
               'max_gcd': max(c['gcd'] for c in cases), 'cases': cases,
               'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'proof_sha256': hashlib.sha256((here / 'ONE_TWIST_CUBULATION.md').read_bytes()).hexdigest()}
    (here / 'one_twist_certificate.json').write_text(json.dumps(payload, indent=2) + '\n')
    print(json.dumps({k: v for k, v in payload.items() if k != 'cases'}, indent=2))


if __name__ == '__main__':
    main()
