#!/usr/bin/env python3
"""Independent exact checks for the two flat retractions; no author imports.

Permutations are pullbacks: (p v)[i] = v[p[i]].  This is distinct from
the author's basis-image convention.  Finite tests supplement the proof.
"""
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from random import Random
import json


def compose(x, y):
    vx, px = x
    vy, py = y
    return (tuple(a + vy[i] for a, i in zip(vx, px)),
            tuple(py[i] for i in px))


def inverse(x):
    v, p = x
    q = [0] * len(p)
    for i, j in enumerate(p):
        q[j] = i
    return tuple(-v[q[i]] for i in range(len(p))), tuple(q)


def unit(n):
    return (0,) * n, tuple(range(n))


def power(x, m):
    if m < 0:
        return power(inverse(x), -m)
    out = unit(len(x[0]))
    while m:
        if m % 2:
            out = compose(out, x)
        x = compose(x, x)
        m //= 2
    return out


def comm(x, y):
    return compose(compose(compose(x, y), inverse(x)), inverse(y))


def conjugate(x, y):
    return compose(compose(x, y), inverse(x))


def model(k):
    if k == 1:
        # Independent boundary model, not the undefined 3k-coordinate rule.
        one = tuple(range(4))
        z = (0,) * 4
        return {
            'a': ((1, 0, -1, 0), one),
            'b': (z, (1, 2, 3, 0)),
            'c': (z, (2, 3, 0, 1)),
            't': ((0, 0, 1, 1), one),
        }
    n = 3 * k
    where = lambda j, i: (j % 3) * k + i % k
    pa = tuple(where(j, i - 1) for j in range(3) for i in range(k))
    pb = tuple(where(j - 1, i) for j in range(3) for i in range(k))
    pc = list(range(n))
    for x, y in ((where(0, 0), where(1, 0)),
                 (where(1, 1), where(2, 0)),
                 (where(2, 1), where(0, 1))):
        pc[x], pc[y] = pc[y], pc[x]
    # Independently derived closed coordinate formulas.
    a = tuple((-1, 0, 1)[j] for j in range(3) for i in range(k))
    b = tuple(0 if i == 0 else (k - 2 * i, i, i - k)[j]
              for j in range(3) for i in range(k))
    t = (k,) * k + (0,) * (2 * k)
    return {'a': (a, pa), 'b': (b, pb), 'c': ((0,) * n, tuple(pc)),
            't': (t, tuple(range(n)))}


def flat_functionals(k, flat, v):
    if k == 1:
        return Fraction(v[0]), Fraction(v[0] + v[2])
    if flat == 'at':
        return Fraction(sum(v[2*k:]), k), Fraction(sum(v[:k]) + sum(v[2*k:]), k*k)
    assert flat == 'wt'
    return Fraction(v[k], k), Fraction(sum(v), k*k)


def evaluate_word(images, word):
    out = unit(len(images['a'][0]))
    for letter in word:
        x = images[letter.lower()]
        out = compose(out, inverse(x) if letter.isupper() else x)
    return out


def free_inverse(word):
    return tuple(-x for x in reversed(word))


def free_reduce(word):
    out = []
    for x in word:
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return tuple(out)


def check_parameter(k, rng):
    images = model(k)
    a, b, c, t = (images[x] for x in 'abct')
    one = unit(len(a[0]))
    w = comm(a, b)
    y = conjugate(b, a)
    assert conjugate(t, a) == a
    assert conjugate(t, b) == compose(b, power(a, k))
    assert conjugate(t, c) == compose(c, w)
    assert conjugate(t, w) == w
    assert y[1] == a[1]
    assert comm(a, y)[1] == one[1]
    if k >= 2:
        assert any(comm(a, y)[0])  # Affine isometries need not commute.
        assert sum(w[0]) == 0 and sum(t[0]) == k*k
        assert any(w[0])
    for flat, first in (('at', a), ('wt', w)):
        assert flat_functionals(k, flat, first[0]) == (1, 0)
        assert flat_functionals(k, flat, t[0]) == (0, 1)
        # Verify actual lattice denominators on every coordinate basis vector.
        for i in range(len(a[0])):
            v = tuple(int(i == j) for j in range(len(a[0])))
            assert all((k*k*z).denominator == 1
                       for z in flat_functionals(k, flat, v))
    if k >= 2:
        # The at forms must be invariant under a's finite linear part P.
        for i in range(len(a[0])):
            e = tuple(int(i == j) for j in range(len(a[0])))
            pe = tuple(e[j] for j in a[1])
            assert flat_functionals(k, 'at', pe) == flat_functionals(k, 'at', e)
    # Produce genuine kernel words by conjugating known translation images.
    # For at, additionally allow a powers; wt uses only the full linear kernel.
    additivity = 0
    for flat in ('at', 'wt'):
        for _ in range(12):
            h = evaluate_word(images, ''.join(rng.choice('aAbBcCtT') for _ in range(10)))
            j = evaluate_word(images, ''.join(rng.choice('aAbBcCtT') for _ in range(10)))
            x = conjugate(h, compose(power(w, rng.randrange(-3, 4)), power(t, rng.randrange(-3, 4))))
            z = conjugate(j, power(a, k * rng.randrange(-3, 4)))
            assert x[1] == z[1] == one[1]
            if flat == 'at':
                x = compose(power(a, rng.randrange(-3, 4)), x)
                z = compose(power(a, rng.randrange(-3, 4)), z)
            fx, fz = (flat_functionals(k, flat, v[0]) for v in (x, z))
            assert flat_functionals(k, flat, compose(x, z)[0]) == tuple(p+q for p, q in zip(fx, fz))
            # Multiplying by k² always enters the integral-character subgroup.
            assert all(q.denominator == 1 for q in flat_functionals(k, flat, power(x, k*k)[0]))
            additivity += 1
        # On the entire distinguished Z², the retraction coordinates are exact.
        first = a if flat == 'at' else w
        for r in range(-5, 6):
            for s in range(-5, 6):
                assert flat_functionals(k, flat, compose(power(first, r), power(t, s))[0]) == (r, s)
    # A fixed explicit second-derived word maps trivially: [u, a u a^-1],
    # with u=[a,y].  This is a limitation of this representation only.
    u = comm(a, y)
    assert comm(u, conjugate(a, u)) == one
    return {'k': k, 'dimension': len(a[0]), 'relations': 'pass',
            'both_flat_dual_pairs': 'pass', 'additivity_samples': additivity,
            'exact_flat_element_samples': 242,
            'fixed_generator_commutator_detected': bool(any(u[0])),
            'second_derived_word_killed': True}


def check_distortion():
    checked = 0
    for k in range(1, 16):
        for n in range(1, 41):
            # Direct normal-form execution of (bt)^n t^-n in F(a,b) rtimes Z.
            word, height = [], 0
            for _ in range(n):
                word.extend([2] + [1] * (k * height))
                height += 1
            height -= n
            assert height == 0
            assert free_reduce(word) == tuple(word)
            assert len(word) == n + k * n * (n-1) // 2
            checked += 1
    # A genuinely nontrivial word in the second derived subgroup of F(x,y).
    z = (1, 2, -1, -2)
    conjugate_z = (1,) + z + (-1,)
    double = free_reduce(z + conjugate_z + free_inverse(z) + free_inverse(conjugate_z))
    assert double
    return {'positive_word_expansions': checked,
            'fixed_nontrivial_second_derived_word': list(double),
            'word_length': len(double),
            'finite_index_rank_boundary': 'index 2 in F2 has rank 3 by Schreier'}


def main():
    rng = Random(211242024)
    parameters = list(range(1, 65)) + [127, 128, 257, 509, 1000, 1001]
    results = [check_parameter(k, rng) for k in parameters]
    out = {'utc': datetime.now(timezone.utc).isoformat(), 'arithmetic': 'exact integers and Fraction',
           'author_code_imported': False, 'parameters': results,
           'distortion_and_limitation': check_distortion(),
           'scope': 'two explicit flat virtual retractions only; proof is unbounded, tests bounded; no full problem or originality claim'}
    destination = Path(__file__).with_name('RESULTS.json')
    destination.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({'parameters': len(results),
                      'additivity_samples': sum(x['additivity_samples'] for x in results),
                      'flat_element_samples': sum(x['exact_flat_element_samples'] for x in results),
                      'distortion_expansions': out['distortion_and_limitation']['positive_word_expansions'],
                      'all_passed': True}, indent=2))


if __name__ == '__main__':
    main()
