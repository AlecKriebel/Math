#!/usr/bin/env python3
"""Exact free-group checks supplementary to the independent mathematical audit.

Uses only the Python standard library. No quotient word-problem heuristic is
used: derivatives are checked before passing to the presented group, where
the substitutions r=1 and t v t^-1=v are explicit defining relations.
"""
import hashlib
import json
from pathlib import Path


def reduce_word(word):
    out = []
    for letter in word:
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return tuple(out)


def inv(word):
    return tuple(-letter for letter in reversed(word))


def mul_word(left, right):
    return reduce_word(left + right)


def substitute(word, images):
    out = ()
    for letter in word:
        image = images[abs(letter)]
        out = mul_word(out, image if letter > 0 else inv(image))
    return out


def ring(terms):
    out = {}
    for word, coefficient in terms:
        word = reduce_word(word)
        out[word] = out.get(word, 0) + coefficient
    return {word: coefficient for word, coefficient in out.items() if coefficient}


def add(*terms):
    return ring((word, coefficient) for term in terms for word, coefficient in term.items())


def scale(term, coefficient):
    return ring((word, value * coefficient) for word, value in term.items())


def product(left, right):
    return ring((mul_word(u, v), a * b) for u, a in left.items() for v, b in right.items())


def singleton(word):
    return {word: 1}


def fox(word, generator):
    prefix = ()
    terms = []
    for letter in word:
        if letter == generator:
            terms.append((prefix, 1))
        prefix = mul_word(prefix, (letter,))
        if letter == -generator:
            terms.append((prefix, -1))
    return ring(terms)


def check(n):
    a, t = 1, n + 2
    u = [()]
    for i in range(1, n + 1):
        u.append(mul_word(u[-1], (a, i + 1)))
    w = mul_word(u[-1], (a,))
    old_from_new = {a: (a,), **{i + 1: u[i] for i in range(1, n + 1)}}
    new_from_old = {a: (a,)}
    for i in range(1, n + 1):
        previous = () if i == 1 else (i,)
        new_from_old[i + 1] = mul_word(mul_word((-a,), inv(previous)), (i + 1,))
    for generator in range(1, n + 2):
        assert substitute(old_from_new[generator], new_from_old) == (generator,)
        assert substitute(new_from_old[generator], old_from_new) == (generator,)

    S = ring((word, 1) for word in u)
    assert fox(w, a) == S
    for i in range(1, n + 1):
        assert fox(w, i + 1) == singleton(mul_word(u[i - 1], (a,)))

    one = singleton(())
    telescoping = {}
    for generator in range(1, n + 2):
        telescoping = add(telescoping, product(fox(w, generator), add(singleton((generator,)), scale(one, -1))))
    assert telescoping == add(singleton(w), scale(one, -1))

    # Verify all relator derivatives in the free group, before imposing r=1.
    words = [(i + 1,) for i in range(1, n + 1)] + [w]
    for v in words:
        r = reduce_word((t,) + v + (-t,) + inv(v))
        r_ring = singleton(r)
        for generator in range(1, n + 2):
            expected = product(add(singleton((t,)), scale(r_ring, -1)), fox(v, generator))
            assert fox(r, generator) == expected
        assert fox(r, t) == add(one, scale(singleton(reduce_word((t,) + v + (-t,))), -1))
        full_boundary = {}
        for generator in range(1, n + 3):
            full_boundary = add(full_boundary, product(fox(r, generator), add(singleton((generator,)), scale(one, -1))))
        assert full_boundary == add(r_ring, scale(one, -1))

    return {"n": n, "free_basis_substitutions": "pass", "Fox_word_derivatives": "pass", "relator_Fox_derivatives": "pass", "telescoping_boundaries": "pass"}


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    candidates = (root / "DIRECT_BETTI.md",
                  root / "proof-audits" / "direct" / "DIRECT_BETTI.md")
    reviewed = next((proof for proof in candidates if proof.is_file()), None)
    if reviewed is None:
        raise FileNotFoundError("DIRECT_BETTI.md is missing from the repository or archive proof layout")
    print(json.dumps({
        "reviewed_sha256": hashlib.sha256(reviewed.read_bytes()).hexdigest(),
        "checks": [check(n) for n in (0, 1, 2, 99)],
        "scope": "Exact finite-support algebra only; analytic injectivity is established by the written proof, not by computation."
    }, indent=2))
