#!/usr/bin/env python3
"""Finite encoding/witness controls, NOT an implementation of Razborov's algorithm."""
from itertools import product
from math import gcd
from collections import Counter
import json

checks = Counter()


def check(value, name):
    checks[name] += 1
    if not value:
        raise AssertionError(name)


def reduce_word(word):
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
    out = []
    for x in word:
        image = images[abs(x)]
        out.extend(image if x > 0 else inverse(image))
    return reduce_word(out)


def surface_relator(g):
    return tuple(x for i in range(g) for x in (2*i+1, 2*i+2, -2*i-1, -2*i-2))


def presentation(g, word):
    if g < 0 or any(x == 0 or abs(x) > 2*g for x in word):
        raise ValueError('Bad genus or generator index')
    return {'unknowns': list(range(1, 2*g+1)),
            'coefficient_free_relators': [surface_relator(g), tuple(word)]}


def audit():
    check(presentation(0, ()) == {'unknowns': [], 'coefficient_free_relators': [(), ()]}, 'sphere_input')
    for g in range(1, 13):
        standard = {i: (() if i % 2 else (i//2,)) for i in range(1, 2*g+1)}
        diagonal = dict(standard)
        diagonal[1], diagonal[2] = (1,), (-1,)
        alternative = dict(standard)
        alternative[1], alternative[2] = (1,), ()
        examples = [(standard, (1,)),
                    (standard, (1, 2, -1, -2)),
                    (standard, surface_relator(g)),
                    (alternative, (2,)),
                    (diagonal, (1, 2)),
                    (diagonal, (1, 2)*7)]
        for images, word in examples:
            data = presentation(g, word)
            check(len(data['unknowns']) == 2*g, 'all_unknowns_retained')
            for relator in data['coefficient_free_relators']:
                check(substitute(relator, images) == (), 'positive_relator_witness')
            # Sufficient explicit generation certificate for these toy examples.
            present = {abs(w[0]) for w in images.values() if len(w) == 1}
            check(present == set(range(1, g+1)), 'positive_surjectivity_witness')
            for conjugator in [(1,), (2,), (1,2,-1)]:
                conjugate = conjugator + word + inverse(conjugator)
                check(substitute(conjugate, images) == (), 'conjugacy_invariance')
                check(substitute(inverse(word), images) == (), 'orientation_invariance')
    torus_words = 0
    for length in range(6):
        for word in product((1,-1,2,-2), repeat=length):
            p = sum((1 if x > 0 else -1) for x in word if abs(x) == 1)
            q = sum((1 if x > 0 else -1) for x in word if abs(x) == 2)
            d = gcd(p,q)
            u,v = (q//d,-p//d) if d else (1,0)
            images = {1: ((1,) if u>=0 else (-1,))*abs(u),
                      2: ((1,) if v>=0 else (-1,))*abs(v)}
            check(gcd(u,v) == 1, 'torus_epimorphism')
            check(p*u+q*v == 0, 'torus_kernel_vector')
            check(substitute(word,images) == (), 'torus_word_killed')
            check(substitute(surface_relator(1),images) == (), 'torus_surface_relation')
            torus_words += 1
    for g,word in [(0,(1,)),(1,(3,)),(1,(0,)),(-1,())]:
        try:
            presentation(g,word)
        except ValueError:
            check(True,'invalid_encoding_rejected')
        else:
            raise AssertionError('Invalid presentation accepted')
    return {'status':'PASS','assertions':sum(checks.values()),
            'assertions_by_family':dict(checks),'torus_words':torus_words,
            'scope':'Finite coefficient-free input and positive-witness controls only',
            'not_implemented':'Razborov rank algorithm, compression bodies, stable map construction',
            'negative_control':'The separately verified Carter example; no corank solver was executed on it'}


if __name__ == '__main__':
    print(json.dumps(audit(),indent=2))
