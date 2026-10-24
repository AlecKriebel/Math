#!/usr/bin/env python3
"""Fresh audit: affine maps by output-coordinate substitution, standard library only.

This does not import any author implementation. The b-offset is the independently
derived closed form, rather than a cumulative solution of the author's equation.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import random


def compose(f, g):
    """f(g(x)); row j is x[source[j]] + offset[j]."""
    fs, fv = f
    gs, gv = g
    return (tuple(gs[s] for s in fs), tuple(v + gv[s] for s, v in zip(fs, fv)))


def inverse(f):
    src, off = f
    back = [0] * len(src)
    for j, s in enumerate(src):
        back[s] = j
    return tuple(back), tuple(-off[j] for j in back)


def power(f, n):
    if n < 0:
        return power(inverse(f), -n)
    out = (tuple(range(len(f[0]))), (0,) * len(f[0]))
    while n:
        if n & 1:
            out = compose(out, f)
        f = compose(f, f)
        n >>= 1
    return out


def eval_word(word, generators):
    n = len(generators['a'][0])
    out = (tuple(range(n)), (0,) * n)
    for letter in word:
        gen = generators[letter.lower()]
        out = compose(out, gen if letter.islower() else inverse(gen))
    return out


def data(k):
    assert k >= 2
    coords = [(j, i) for j in range(3) for i in range(k)]
    position = {p: r for r, p in enumerate(coords)}
    c = {p: p for p in coords}
    for p, q in [((0, 0), (1, 0)), ((1, 1), (2, 0)), ((2, 1), (0, 1))]:
        assert len({p, q}) == 2
        c[p], c[q] = q, p
    one = tuple(range(3 * k))
    zero = (0,) * (3 * k)
    av = (-1, 0, 1)
    a = (tuple(position[j, (i - 1) % k] for j, i in coords),
         tuple(av[j] for j, i in coords))
    def u(j, i):
        if i == 0:
            return 0
        return (k - 2 * i, i, i - k)[j]
    b = (tuple(position[(j - 1) % 3, i] for j, i in coords),
         tuple(u(j, i) for j, i in coords))
    c_map = (tuple(position[c[p]] for p in coords), zero)
    t = (one, tuple(k if j == 0 else 0 for j, i in coords))
    return {'a': a, 'b': b, 'c': c_map, 't': t}


def block0_sum(v, k):
    return -sum(v[:k])


def check(k):
    g = data(k)
    n = 3 * k
    identity = (tuple(range(n)), (0,) * n)
    for x in g.values():
        assert compose(x, inverse(x)) == identity
    assert eval_word('taTA', g) == identity
    assert compose(compose(g['t'], g['b']), inverse(g['t'])) == compose(g['b'], power(g['a'], k))
    comm = eval_word('abAB', g)
    assert compose(compose(g['t'], g['c']), inverse(g['t'])) == compose(g['c'], comm)
    # Independent direct evaluation of the literal long relator.
    assert eval_word('tbT' + 'A' * k + 'B', g) == identity
    assert eval_word('tcTbaBAC', g) == identity
    a_power = power(g['a'], k)
    assert a_power[0] == identity[0]
    assert a_power[1] == tuple(k * z for z in g['a'][1])
    assert any(a_power[1])
    assert block0_sum(g['a'][1], k) == k
    # Every P-power preserves ell. This also checks both holonomy conventions.
    p = (g['a'][0], (0,) * n)
    probe = tuple(17 * i - i * i for i in range(n))
    shifts = {0, 1, k // 2, k - 1, k, k + 1}
    for s in shifts:
        pull = power(p, s)[0]
        assert block0_sum(tuple(probe[i] for i in pull), k) == block0_sum(probe, k)
    # P^k=1, B^3=1, C^2=1, PB=BP at the linear level.
    pl = (g['a'][0], (0,) * n)
    bl = (g['b'][0], (0,) * n)
    cl = (g['c'][0], (0,) * n)
    assert power(pl, k) == power(bl, 3) == power(cl, 2) == identity
    assert compose(pl, bl) == compose(bl, pl)
    return {'k': k, 'dimension': n, 'literal_affine_relators': 'PASS',
            'a_power_translation_nonzero': True, 'k_times_chi_a': k,
            'max_abs_b_offset': max(map(abs, g['b'][1]))}


def sampling_character(k):
    """Finite exact checks only; the unbounded character argument is in AUDIT.md."""
    g = data(k)
    n = 3 * k
    zero = (0,) * n
    p_powers = {power((g['a'][0], zero), e)[0] for e in range(k)}
    rng = random.Random(210124 + k)
    accepted = []
    for _ in range(3000):
        word = ''.join(rng.choice('abctABCT') for _ in range(rng.randrange(1, 20)))
        x = eval_word(word, g)
        if x[0] in p_powers:
            accepted.append(x)
    assert accepted
    for x in accepted:
        for y in accepted[:12]:
            z = compose(x, y)
            assert z[0] in p_powers
            assert block0_sum(z[1], k) == block0_sum(x[1], k) + block0_sum(y[1], k)
    integral = [x for x in accepted if block0_sum(x[1], k) % k == 0]
    for x in integral:
        for y in integral[:12]:
            z = compose(x, y)
            assert block0_sum(z[1], k) % k == 0
    return {'k': k, 'words_sampled': 3000, 'in_preimage_cyclic_holonomy': len(accepted),
            'integral_character_elements': len(integral), 'character_additivity': 'PASS'}


def main():
    ks = list(range(2, 129)) + [257, 509, 1000, 1001]
    results = [check(k) for k in ks]
    samples = [sampling_character(k) for k in [2, 3, 4, 5, 7, 8]]
    examples = {}
    for k in [2, 3]:
        g = data(k)
        examples[str(k)] = {name: {'source': list(f[0]), 'offset': list(f[1])}
                            for name, f in g.items()}
    out = {'utc': datetime.now(timezone.utc).isoformat(),
           'implementation': 'Independent output-coordinate substitution; closed-form b-offset; no author imports',
           'arithmetic': 'exact integers', 'unbounded_proof': 'AUDIT.md',
           'tested_parameters': results, 'character_samples': samples, 'boundary_examples': examples,
           'scope': 'All-k proof and finite tests for the virtual retract of exact <a> only; no virtual RAAG, specialness, VRC, or priority claim'}
    target = Path(__file__).with_name('independent_results.json')
    target.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({'parameter_cases': len(results), 'character_sample_cases': len(samples),
                      'parameters_range': '2..128,257,509,1000,1001', 'result': 'PASS',
                      'sha256': hashlib.sha256(target.read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
