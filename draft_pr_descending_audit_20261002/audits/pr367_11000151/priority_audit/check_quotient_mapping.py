#!/usr/bin/env python3
"""Independent faithful-Artin checks of identities used in priority mapping.

Only Python standard library; no candidate code imports. Words have positive
standard braid-generator indices. Automorphisms are represented by reduced
signed-generator words in F6. Apply generators on the left consistently.
"""
import json
from pathlib import Path

N = 6

def inv(w):
    return tuple(-x for x in reversed(w))

def reduce_word(w):
    out = []
    for x in w:
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return tuple(out)

def subst(w, images):
    out = []
    for x in w:
        out.extend(images[x-1] if x > 0 else inv(images[-x-1]))
    return reduce_word(out)

def action(word):
    current = tuple((i,) for i in range(1,N+1))
    for k in word:
        images = [(i,) for i in range(1,N+1)]
        images[k-1] = (k,k+1,-k)
        images[k] = (k,)
        current = tuple(subst(w, images) for w in current)
    return current

c = (1,2,3,4)*5
h = (5,4,3,2,1,1,2,3,4,5)
z = (1,2,3,4,5)*6
checks = {
    "recursive_full_twist_c_h_equals_z": action(c+h) == action(z),
    "recursive_full_twist_h_c_equals_z": action(h+c) == action(z),
    "Matsumoto_A4_relabelled_equals_c": action((1,4,3,2)*5) == action(c),
    "Matsumoto_A5_relabelled_equals_z": action((1,5,4,3,2)*6) == action(z),
}
assert all(checks.values()), checks
print(json.dumps({"checks": checks, "status":"PASS", "method":"faithful Artin action on F6, exact integer free reduction"}, indent=2))
