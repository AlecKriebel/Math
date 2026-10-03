#!/usr/bin/env python3
"""Finite controls of quotient-relation formulas; not a formal proof."""
import itertools
import json


def partitions(n):
    if not n:
        yield ()
    else:
        for p in itertools.product(range(n), repeat=n):
            if p[0] == 0 and all(p[i] <= max(p[:i], default=-1) + 1
                                for i in range(n)):
                yield p


def size(p):
    return max(p, default=-1) + 1


def arrows(p, q):
    for f in itertools.product(range(size(q)), repeat=size(p)):
        yield frozenset((x, y) for x in range(len(p)) for y in range(len(q))
                        if f[p[x]] == q[y])


def identity(p):
    return frozenset((x, y) for x in range(len(p)) for y in range(len(p))
                     if p[x] == p[y])


def compose(r, s):
    return frozenset((x, z) for x, y in r for y2, z in s if y == y2)


def run():
    objects = tuple(p for n in range(3) for p in partitions(n))
    hom = {(p, q): tuple(arrows(p, q)) for p in objects for q in objects}
    counts = dict(identities=0, compositions=0, associativity=0,
                  equalizer_predicates=0, image_kernel_formulas=0)
    for p in objects:
        for q in objects:
            for r in hom[p, q]:
                assert compose(identity(p), r) == r
                assert compose(r, identity(q)) == r
                counts["identities"] += 1
                image = {y for x, y in r}
                kernel = {(x, z) for x, y in r for z, yy in r if y == yy}
                assert set(identity(p)) <= kernel
                assert all((z, x) in kernel for x, z in kernel)
                assert all((x, z) in kernel for x, y in kernel
                           for yy, z in kernel if y == yy)
                assert all((y in image) == (z in image)
                           for y in range(len(q)) for z in range(len(q))
                           if q[y] == q[z])
                counts["image_kernel_formulas"] += 1
                for s in hom[p, q]:
                    equalizer = {x for x, y in r if (x, y) in s}
                    assert all((x in equalizer) == (z in equalizer)
                               for x in range(len(p)) for z in range(len(p))
                               if p[x] == p[z])
                    expected = {x for x in range(len(p))
                                if {q[y] for xx, y in r if xx == x}
                                == {q[y] for xx, y in s if xx == x}}
                    assert equalizer == expected
                    counts["equalizer_predicates"] += 1
                for t in objects:
                    for s in hom[q, t]:
                        rs = compose(r, s)
                        assert rs in hom[p, t]
                        counts["compositions"] += 1
                        for u in objects:
                            for v in hom[t, u]:
                                assert compose(rs, v) == compose(r, compose(s, v))
                                counts["associativity"] += 1
    return dict(status="PASS", counts=counts, total=sum(counts.values()),
                object_count=len(objects), carrier_bound=2,
                empty_objects=True,
                limitation="Finite set controls only; no proof of constructive metatheory or semantic reconstruction")


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, indent=2))
