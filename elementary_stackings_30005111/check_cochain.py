"""Exact standard-library corroboration of the finite cochain proof."""
from fractions import Fraction
from itertools import product
import json

def primitive(w):
    return not any((len(w) % d == 0 and w == w[:d] * (len(w) // d) for d in range(1, len(w))))

def solve(vs, es):
    n = len(vs)
    origvs = vs[:]
    origes = es[:]
    levels = []
    trace = []
    while True:
        verts = set(vs)
        edges = {e for e, d in es}
        ends = {}
        for i, (e, d) in enumerate(es):
            p, q = (vs[i], vs[(i + 1) % n])
            if d < 0:
                p, q = (q, p)
            if not (e not in ends or ends[e] == (p, q)):
                raise AssertionError()
            ends[e] = (p, q)
        rank = len(edges) - len(verts) + 1
        trace.append((len(verts), len(edges), rank))
        if rank == 1:
            break
        if not rank >= 2:
            raise AssertionError()
        parent = {v: v for v in verts}

        def find(v):
            while parent[v] != v:
                v = parent[v]
            return v
        chords = []
        for e in sorted(edges):
            p, q = map(find, ends[e])
            if p == q:
                chords.append(e)
            else:
                parent[p] = q
        if not len(chords) == rank:
            raise AssertionError()
        hom = {e: sum((d for f, d in es if f == e)) for e in chords}
        c = {e: 0 for e in edges}
        nz = next((e for e in chords if hom[e]), None)
        if nz is None:
            c[chords[0]] = 1
        else:
            other = next((e for e in chords if e != nz))
            c[nz] = hom[other]
            c[other] = -hom[nz]
        s = [0]
        for e, d in es:
            s.append(s[-1] + d * c[e])
        if not s[-1] == 0:
            raise AssertionError()
        vp = [(v, s[i]) for i, v in enumerate(vs)]
        ep = [(e, s[i] if d > 0 else s[i + 1]) for i, (e, d) in enumerate(es)]
        vm = {p: j for j, p in enumerate(sorted(set(vp)))}
        em = {p: j for j, p in enumerate(sorted(set(ep)))}
        if not len(vm) > len(verts):
            raise AssertionError()
        levels.append(s[:-1])
        vs = [vm[p] for p in vp]
        es = [(em[p], d) for p, (_, d) in zip(ep, es)]
    degree = n // len(set(vs))
    if degree != 1:
        return (None, trace, degree)
    h = [Fraction(0) for _ in vs]
    for a in reversed(levels):
        eps = 1 / (2 * max(map(abs, h)) + 1)
        h = [Fraction(x) + eps * y for x, y in zip(a, h)]
    for i in range(n):
        for j in range(i):
            if origvs[i] == origvs[j]:
                if not h[i] != h[j]:
                    raise AssertionError()
    strands = {}
    for i, (e, d) in enumerate(origes):
        pair = (h[i], h[(i + 1) % n])
        if d < 0:
            pair = pair[::-1]
        for p, q in strands.get(e, []):
            if not (pair[0] - p) * (pair[1] - q) > 0:
                raise AssertionError()
        strands.setdefault(e, []).append(pair)
    return (h, trace, degree)

def run(w, subdivide=False):
    if not subdivide:
        return solve([0] * len(w), [(abs(x), 1 if x > 0 else -1) for x in w])
    vs = []
    es = []
    for x in w:
        a = abs(x)
        vs.extend([0, a])
        es.extend([(2 * a, 1), (2 * a + 1, -1)] if x > 0 else [(2 * a + 1, 1), (2 * a, -1)])
    return solve(vs, es)
if __name__ == '__main__':
    counts = {'primitive': 0, 'proper_power': 0, 'subdivided': 0}
    sample = None
    for n in range(1, 8):
        for t in product((1, -1, 2, -2), repeat=n):
            w = list(t)
            if any((w[i] == -w[(i + 1) % n] for i in range(n))):
                continue
            h, tr, deg = run(w)
            if primitive(w):
                if not (h is not None and deg == 1):
                    raise AssertionError()
                counts['primitive'] += 1
            else:
                if not (h is None and deg > 1):
                    raise AssertionError()
                counts['proper_power'] += 1
            if n <= 5:
                hh, tt, dd = run(w, True)
                if not (hh is not None) == primitive(w):
                    raise AssertionError()
                counts['subdivided'] += 1
            if w == [1, 2, -1, -2]:
                sample = {'word': w, 'trace': tr, 'heights': [str(x) for x in h]}
    print(json.dumps({'PASS': True, 'counts': counts, 'commutator_certificate': sample}, indent=2))
