#!/usr/bin/env python3
"""Nonauthor reconstruction of the one-twist cubulations; standard library only.

Builds the vertex cover and its annuli directly (not by deleting cylinders from
an ambient cover). Does not import or execute the author's construction.
"""
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from itertools import product
from math import gcd
from pathlib import Path
import hashlib
import json
import random


HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / "positive_hierarchy"


def red(w):
    stack = []
    for a in w:
        if stack and stack[-1] == -a:
            stack.pop()
        else:
            stack.append(a)
    return tuple(stack)


def inv(w):
    return tuple(-a for a in w[::-1])


def apply(w, images):
    return red(a for x in w for a in (images[x] if x > 0 else inv(images[-x])))


def character(w, r):
    ex = [sum((a == i) - (a == -i) for a in w) for i in range(1, r + 1)]
    k = gcd(*ex)
    if not k:
        return None
    # Incremental Bezout calculation, independently implemented iteratively.
    value, coeffs = 0, []
    for e in ex:
        aa, bb = value, e
        s0, s1, t0, t1 = 1, 0, 0, 1
        while bb:
            q = aa // bb
            aa, bb = bb, aa - q * bb
            s0, s1, t0, t1 = s1, s0 - q * s1, t1, t0 - q * t1
        if aa < 0:
            aa, s0, t0 = -aa, -s0, -t0
        coeffs = [s0 * x for x in coeffs] + [t0]
        value = aa
    assert value == k == sum(e * x for e, x in zip(ex, coeffs))
    return k, coeffs


class Complex:
    def __init__(self):
        self.e = {}  # positive id -> tail, head, projected edge key, parity/color
        self.s = []
        self.v = set()
        self.lookup = {}

    def edge(self, name, tail, head, image, color):
        assert name not in self.lookup
        i = len(self.e) + 1
        self.lookup[name] = i
        self.e[i] = (tail, head, image, color)
        self.v.update((tail, head))
        return i

    def ends(self, a):
        t, h = self.e[abs(a)][:2]
        return (t, h) if a > 0 else (h, t)

    def square(self, boundary):
        b = tuple(boundary)
        assert len(b) == 4
        assert all(self.ends(b[j])[1] == self.ends(b[(j + 1) % 4])[0] for j in range(4))
        self.s.append(b)

    def links(self):
        dirs, links = defaultdict(set), defaultdict(Counter)
        for a, (t, h, *_rest) in self.e.items():
            dirs[t].add(a)
            dirs[h].add(-a)
        for b in self.s:
            for j in range(4):
                v = self.ends(b[j])[0]
                x, y = -b[(j - 1) % 4], b[j]
                assert x != y, (v, "loop")
                links[v][frozenset((x, y))] += 1
        for v in self.v:
            assert all(n == 1 for n in links[v].values()), (v, "double edge")
            adj = {a: set() for a in dirs[v]}
            for edge in links[v]:
                x, y = tuple(edge)
                adj[x].add(y)
                adj[y].add(x)
            assert all(not (adj[x] & adj[y]) for x in adj for y in adj[x]), (v, "triangle")
        neighbours = defaultdict(set)
        for t, h, *_ in self.e.values():
            neighbours[t].add(h)
            neighbours[h].add(t)
        todo, reached = deque([next(iter(self.v))]), set()
        while todo:
            x = todo.popleft()
            if x not in reached:
                reached.add(x)
                todo.extend(neighbours[x] - reached)
        assert reached == self.v
        assert len(self.v) - len(self.e) + len(self.s) == 0
        return dirs, links


def model(w, r, k, chi, degree, copies=1):
    """Direct voltage product-cover plus `copies` copies of ONE annulus."""
    L = len(w)
    out = Complex()
    root = (0, 0)
    rose = [root] + [(a, j) for a in range(1, r + 1) for j in range(1, k)]
    rv = lambda a, j: root if j in (0, k) else (a, j)
    for q in range(copies):
        for h in range(degree):
            for v in rose:
                for n in range(L):
                    endh = (h + (n == L - 1)) % degree
                    out.edge(("z", v, n, h, q), (v, n, h, q),
                             (v, (n + 1) % L, endh, q), ("z", v, n), 1 ^ q)
            for a in range(1, r + 1):
                for j in range(k):
                    for n in range(L):
                        endh = (h + (chi[a - 1] if j == k - 1 else 0)) % degree
                        out.edge(("f", a, j, n, h, q), (rv(a, j), n, h, q),
                                 (rv(a, j + 1), n, endh, q), ("f", a, j, n), q)
        for h in range(degree):
            for a in range(1, r + 1):
                for j in range(k):
                    for n in range(L):
                        ah = (h + (chi[a - 1] if j == k - 1 else 0)) % degree
                        zh = (h + (n == L - 1)) % degree
                        out.square((out.lookup["f", a, j, n, h, q],
                                    out.lookup["z", rv(a, j + 1), n, ah, q],
                                    -out.lookup["f", a, j, (n + 1) % L, zh, q],
                                    -out.lookup["z", rv(a, j), n, h, q]))
    for q in range(copies):
        target = (q + 1) % copies
        left, right = [], []
        h = 0
        for j in range(k * L):
            edge = out.lookup["z", root, j % L, h, q]
            left.append(edge)
            h = out.ends(edge)[1][2]
        assert h == 0
        h = 0
        for a in w:
            if a > 0:
                for j in range(k):
                    edge = out.lookup["f", a, j, 0, h, target]
                    right.append(edge)
                    h = out.ends(edge)[1][2]
            else:
                for j in range(k - 1, -1, -1):
                    preh = (h - (chi[-a - 1] if j == k - 1 else 0)) % degree
                    edge = -out.lookup["f", -a, j, 0, preh, target]
                    right.append(edge)
                    h = out.ends(edge)[1][2]
        assert h == 0 and len(right) == k * L
        transverse = [out.edge(("c", j, q), out.ends(left[j])[0],
                              out.ends(right[j])[0], ("c", j), q)
                      for j in range(k * L)]
        for j in range(k * L):
            out.square((left[j], transverse[(j + 1) % (k * L)], -right[j], -transverse[j]))
    return out


def local_isometry(small, large):
    sd, sl = small.links()
    ld, ll = large.links()
    keys = {data[2]: i for i, data in large.e.items()}
    for v in small.v:
        basev = v[:2] + (0, 0)
        project = {a: (1 if a > 0 else -1) * keys[small.e[abs(a)][2]] for a in sd[v]}
        assert len(set(project.values())) == len(project), (v, "noninjective link")
        image_edges = {frozenset(project[a] for a in e) for e in sl[v]}
        assert image_edges == {e for e in ll[basev] if e <= set(project.values())}, (v, "nonfull link")


def monodromy_and_retraction(w, r, k):
    images = {i: (i,) for i in range(1, r + 1)}
    for j in range(k):
        images[r + 1 + j] = (r + 2 + j,) if j + 1 < k else (r + 1,) + w
    backward = {i: (i,) for i in range(1, r + 1)}
    backward[r + 1] = (r + k,) + inv(w)
    for j in range(1, k):
        backward[r + j + 1] = (r + j,)
    theta_k = {}
    for i in images:
        assert apply(images[i], backward) == apply(backward[i], images) == (i,)
        powered = (i,)
        for _ in range(k):
            powered = apply(powered, images)
        theta_k[i] = powered
        assert powered == ((i,) if i <= r else (i,) + w)
    retract = {i: ((i,) if i <= r else (r + 1,)) for i in images}
    for i in images:
        assert apply(theta_k[i], retract) == apply(retract[i], theta_k)
    for j in range(1, k):
        assert apply((r + 1 + j, -(r + 1)), theta_k) == (r + 1 + j, -(r + 1))


def case(w, r, supplied_chi=None):
    ch = character(w, r)
    if ch is None:
        return None
    assert w and red(w) == w and w[0] != -w[-1]
    k, chi = ch
    if supplied_chi is not None:
        chi = list(supplied_chi)
        assert len(chi) == r
        assert sum((1 if a > 0 else -1) * chi[abs(a) - 1] for a in w) == k
    ambient = model(w, r, k, chi, 1)
    original = model(w, r, k, chi, k)
    double = model(w, r, k, chi, k, 2)
    ambient.links(); original.links(); double.links()
    local_isometry(original, ambient)
    for b in double.s:
        colors = [double.e[abs(e)][3] for e in b]
        assert colors[0] == colors[2] != colors[1] == colors[3]
    monodromy_and_retraction(w, r, k)
    counts = lambda c: [len(c.v), len(c.e), len(c.s)]
    return {"rank": r, "word": list(w), "gcd": k, "character": chi,
            "ambient_cells": counts(ambient), "original_cells": counts(original),
            "double_cells": counts(double)}


def main():
    authored = json.loads((AUTHOR / "one_twist_certificate.json").read_text())
    completed = []
    for cert in authored["cases"]:
        got = case(tuple(cert["word"]), cert["rank"])
        for key in ("rank", "word", "gcd", "ambient_cells", "original_cells", "double_cells"):
            assert got[key] == cert[key], (key, got, cert)
        completed.append(got)
    # Extra ranks, negative exponents, proper powers, mixed signs and larger gcd.
    extras = [(r, (s * a,) * n) for r in range(1, 6) for a in (1, r)
              for s in (-1, 1) for n in (1, 2, 3, 6)]
    extras += [(1, (1,) * 12), (1, (-1,) * 12), (2, (1, 2) * 8),
               (2, (1, 2) * 6), (3, (1, -2, 3) * 4),
               (4, (1, 2, -1, 3, 4, -3) * 3)]
    rng = random.Random(21124001)
    for _ in range(200):
        r = rng.randint(1, 6)
        w = red(rng.choice((-1, 1)) * rng.randint(1, r) for _ in range(rng.randint(1, 12)))
        while len(w) > 1 and w[0] == -w[-1]:
            w = w[1:-1]
        if w and character(w, r):
            extras.append((r, w))
    for r, w in extras:
        completed.append(case(w, r))
    alternate_characters = [
        (2, (1, 1, 2, 2, 2, 2), (-1, 1)),
        (2, (1, 1, 2, 2, 2, 2), (7, -3)),
        (3, (1, 2, -1, 3, 2, -3), (7, 1, -11)),
        (3, (1, 2, -1, 3, 2, -3), (-12, 1, 20)),
    ]
    for r, w, chi in alternate_characters:
        completed.append(case(w, r, chi))
    payload = {"utc": datetime.now(timezone.utc).isoformat(), "status": "PASS",
               "author_cases_reconstructed": len(authored["cases"]),
               "additional_cases": len(extras) + len(alternate_characters),
               "alternate_character_cases": len(alternate_characters),
               "total_cases": len(completed),
               "max_gcd": max(c["gcd"] for c in completed),
               "rank_range": [min(c["rank"] for c in completed), max(c["rank"] for c in completed)],
               "scope": "direct product covers and annuli; all links; connectedness; Euler characteristic; full-link local isometry; VH colors; monodromy inverse/power/retraction",
               "completed_cases_sha256": hashlib.sha256(json.dumps(completed, sort_keys=True).encode()).hexdigest(),
               "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "proof_sha256": hashlib.sha256((AUTHOR / "ONE_TWIST_CUBULATION.md").read_bytes()).hexdigest()}
    (HERE / "independent_results.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
