"""Own exact finite controls for signs, gauge identity and central cuts.

No original or foreign code imported. Default verifies sealed results read-only;
--write creates only MECHANISM_RESULTS.json in this own directory.
"""
from fractions import Fraction as Q
import argparse
import itertools
import json
from pathlib import Path


def d_terms(n):
    # Opaque f applied to words in ordered variables, with outer multipliers.
    args = [(i,) for i in range(n + 1)]
    terms = [(1, (0,), tuple(args[1:]), ())]
    for j in range(n):
        a = args[:j] + [(j, j + 1)] + args[j + 2:]
        terms.append(((-1) ** (j + 1), (), tuple(a), ()))
    terms.append(((-1) ** (n + 1), (), tuple(args[:-1]), (n,)))
    return terms


def signs():
    count = 0
    bad = 0
    for n in range(1, 9):
        sn = (-1) ** ((n - 1) * (n - 2) // 2)
        sn1 = (-1) ** (n * (n - 1) // 2)
        # d(S_n f): f-arguments reverse/star; outer factors stay put.
        left = {(l, tuple(tuple(reversed(w)) for w in reversed(a)), r): c * sn
                for c, l, a, r in d_terms(n)}
        # S_(n+1)(d f): reverse/star variables, then star the whole output.
        right = {}
        transform = lambda w: tuple(n - i for i in reversed(w))
        for c, l, a, r in d_terms(n):
            # The final star reverses outer products. Opaque f arguments
            # remain inside f, so only their variable labels are reflected.
            key = (transform(r), tuple(tuple(n - i for i in w) for w in a), transform(l))
            right[key] = c * sn1
        assert left == right
        count += len(left)
        if n == 2:
            # Omitting the required S3 minus sign must fail.
            assert left != {key: -v for key, v in right.items()}
            bad += 1
    return count, bad


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def scale(c, x):
    return tuple(c * a for a in x)


def sub(x, y):
    return add(x, scale(-1, y))


def mul(x, y):
    a, b, c, d = x
    e, f, g, h = y
    return (a * e + b * g, a * f + b * h, c * e + d * g, c * f + d * h)


def matrix_controls():
    zero = (Q(0),) * 4
    basis = [tuple(Q(i == j) for i in range(4)) for j in range(4)]
    identity = (Q(1), Q(0), Q(0), Q(1))
    eps = Q(1, 100)
    trace = lambda x: x[0] + x[3]
    g = lambda x: add(x, scale(eps * trace(x), identity))
    inverse = lambda x: sub(x, scale(eps * trace(x) / (1 + 2 * eps), identity))
    h = lambda x: sub(g(x), x)
    mu = lambda x, y: inverse(mul(g(x), g(y)))
    delta = lambda x, y: sub(mu(x, y), mul(x, y))
    dh = lambda x, y: sub(add(mul(x, h(y)), mul(h(x), y)), h(mul(x, y)))
    pairs = triples = 0
    for x, y in itertools.product(basis, repeat=2):
        bx, by = inverse(x), inverse(y)
        exact = sub(g(mu(bx, by)), mul(x, y))
        rhs = sub(add(sub(delta(bx, by), dh(bx, by)), h(delta(bx, by))), mul(h(bx), h(by)))
        assert exact == rhs == zero
        pairs += 1
    for x, y, z in itertools.product(basis, repeat=3):
        ddelta = sub(add(mul(x, delta(y, z)), delta(x, mul(y, z))),
                     add(delta(mul(x, y), z), mul(delta(x, y), z)))
        square = sub(delta(delta(x, y), z), delta(x, delta(y, z)))
        assert ddelta == square
        assert mu(mu(x, y), z) == mu(x, mu(y, z))
        triples += 1
    # This associative product does not have original unit I: lemma must allow it.
    assert mu(identity, basis[0]) != basis[0]
    assert g(inverse(identity)) == identity
    return pairs, triples


def central_controls():
    e0, e1 = (1, 0), (0, 1)
    prod = lambda a, b: (a[0] * b[0], a[1] * b[1])
    zcut = lambda a: (a[0], 0)
    qcut = lambda a: (0, a[1])

    def differential(f, n):
        def result(*a):
            value = a[0][0] * f(*a[1:])
            for j in range(n):
                value += (-1) ** (j + 1) * f(*(a[:j] + (prod(a[j], a[j + 1]),) + a[j + 2:]))
            return value + (-1) ** (n + 1) * f(*a[:-1]) * a[-1][0]
        return result

    def homotopy(f, n):
        if n <= 1:
            return lambda *a: 0
        return lambda *a: sum((-1) ** (j + 1) * f(
            *(tuple(zcut(v) for v in a[:j]) + (e1, qcut(a[j])) + a[j + 1:]))
            for j in range(n - 1))

    count = negative = 0
    for n in range(1, 6):
        def f(*a):
            value = 0
            for bits in itertools.product(range(2), repeat=n):
                coefficient = 1 + sum((j + 2) * (bit + 1) for j, bit in enumerate(bits))
                term = coefficient
                for v, bit in zip(a, bits):
                    term *= v[bit]
                value += term
            return value
        dj = differential(homotopy(f, n), n - 1)
        jd = homotopy(differential(f, n), n + 1)
        for args in itertools.product((e0, e1), repeat=n):
            expected = f(*args) - f(*(zcut(a) for a in args))
            assert dj(*args) + jd(*args) == expected
            count += 1
            negative += expected != 0  # A cut alone fails on these mixed inputs.
    assert negative
    return count, negative


def run():
    term_count, bad_sign = signs()
    pairs, triples = matrix_controls()
    cuts, mixed = central_controls()
    return dict(scope='finite exact mechanism diagnostics; universal derivations separate',
                reflection_degrees=list(range(1, 9)), reflection_term_comparisons=term_count,
                omitted_S3_sign_negative_controls=bad_sign,
                noncommutative_M2_gauge_pairs=pairs, associative_defect_triples=triples,
                nonoriginal_unit_control=True, central_homotopy_degrees=list(range(1, 6)),
                central_basis_tuple_checks=cuts, cut_alone_negative_cases=mixed)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = run()
    path = Path(__file__).with_name('MECHANISM_RESULTS.json')
    if args.write:
        assert not path.exists()
        path.write_text(json.dumps(result, indent=2) + '\n')
    else:
        assert result == json.loads(path.read_text())
    print(json.dumps(result, sort_keys=True))
