#!/usr/bin/env python3
"""Exact examples and a negative control, not a search over all subsurfaces."""
from collections import deque
from itertools import permutations
from pathlib import Path
import hashlib
import json

assertions = 0

def check(condition):
    global assertions
    assertions += 1
    assert condition


def compose(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def inverse(p):
    q = [0]*len(p)
    for i, x in enumerate(p):
        q[x] = i
    return tuple(q)


def commutator(p, q):
    return compose(compose(p, q), compose(inverse(p), inverse(q)))


def generated(generators, degree):
    identity = tuple(range(degree))
    seen = {identity}
    todo = deque([identity])
    while todo:
        h = todo.popleft()
        for g in generators:
            x = compose(g, h)
            if x not in seen:
                seen.add(x)
                todo.append(x)
    return sorted(seen)


def orbits(generators, points, action):
    remaining = set(points)
    parts = []
    while remaining:
        start = min(remaining)
        orbit = {start}
        todo = deque([start])
        while todo:
            point = todo.popleft()
            for g in generators:
                new = action(g, point)
                if new not in orbit:
                    orbit.add(new)
                    todo.append(new)
        remaining -= orbit
        parts.append(sorted(orbit))
    return parts

identity = (0, 1, 2)
r = (1, 2, 0)
t = (1, 0, 2)
a, b, c, e = r, t, inverse(r), t
check(compose(commutator(a, b), commutator(c, e)) == identity)
check(commutator(r, t) == compose(r, r))
check(commutator(inverse(r), t) == r)
whole = generated([a, b, c, e], 3)
check(whole == list(permutations(range(3))))
pants_generators = [a, compose(compose(b, inverse(a)), inverse(b))]
image = generated(pants_generators, 3)
check(len(image) == 3)
check(image == generated([r], 3))
regular = orbits(pants_generators, whole, compose)
natural = orbits(pants_generators, range(3), lambda g, i: g[i])
check(sorted(map(len, regular)) == [3, 3])
check(list(map(len, natural)) == [3])
check(len(regular) == len(whole)//len(image))
check(1+6*(2-1) == 7)
check(1+3*(2-1) == 4)

cyclic = []
for p in (2, 3, 5, 7):
    # Genus-two cyclic cover: a maps to the p-cycle, b,c,e to identity.
    ident = tuple(range(p))
    cycle = tuple((i+1) % p for i in range(p))
    check(len(generated([cycle], p)) == p)
    check(compose(commutator(cycle, ident), commutator(ident, ident)) == ident)
    # The four boundary loops after cutting along b,e are conjugates of b,e.
    boundary = [ident, compose(compose(cycle, inverse(ident)), inverse(cycle)), ident, ident]
    check(all(x == ident for x in boundary))
    lifted_components = orbits(boundary, range(p), lambda g, i: g[i])
    check(len(lifted_components) == p)
    check(all(len(x) == 1 for x in lifted_components))
    cyclic.append({'degree':p,'domain_genus':p+1,'four_holed_preimage_components':len(lifted_components)})

result = {'description':'Exact monodromy examples only; neither original universal claim is established',
          'all_assertions_passed':True,'assertions':assertions,
          's3_negative_control':{'base_genus':2,'regular_cover_degree':6,'regular_domain_genus':7,
                'irregular_cover_degree':3,'irregular_domain_genus':4,'pants_image_order':len(image),
                'regular_component_degrees':list(map(len,regular)),
                'irregular_component_degrees':list(map(len,natural)),
                'meaning':'Disconnectedness for this pants subsurface does not descend from a regular refinement'},
          'cyclic_examples':cyclic,
          'partial_note_sha256':hashlib.sha256(Path(__file__).with_name('PARTIAL.md').read_bytes()).hexdigest()}
Path(__file__).with_name('check_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
