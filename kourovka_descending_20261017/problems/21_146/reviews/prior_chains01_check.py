"""Finite consistency checks for manuscript Lemma 6.1; not a substitute for proof.

Run with Python 3, no third-party dependencies. Normalized integral chains,
including nonadjacent repeated vertices, are used throughout.
"""
from collections import defaultdict
from functools import lru_cache
from itertools import product


def clean(a):
    return {s: c for s, c in a.items() if c}


def plus(*terms):
    out = defaultdict(int)
    for scalar, chain in terms:
        for s, c in chain.items():
            out[s] += scalar * c
    return clean(out)


def simplex(s):
    s = tuple(s)
    return {} if any(a == b for a, b in zip(s, s[1:])) else {s: 1}


def linear(chain, op):
    return plus(*((c, op(s)) for s, c in chain.items()))


def bd_basis(s):
    if len(s) == 1:
        return {}
    return plus(*((-1 if i % 2 else 1, simplex(s[:i] + s[i + 1:]))
                  for i in range(len(s))))


def bd(chain):
    return linear(chain, bd_basis)


def tensor(a, b):
    return clean({(x, y): cx * cy for x, cx in a.items() for y, cy in b.items()})


def tensor_bd(chain):
    return linear(chain, lambda p: plus(
        (1, tensor(bd_basis(p[0]), simplex(p[1]))),
        ((-1) ** (len(p[0]) - 1), tensor(simplex(p[0]), bd_basis(p[1])))))


def aw(chain):
    return linear(chain, lambda s: plus(*(
        (1, tensor(simplex(s[:i + 1]), simplex(s[i:])))
        for i in range(len(s)))))


@lru_cache(None)
def paths(p, q):
    if p == q == 0:
        return (((), 1),)
    out = []
    if p:
        out.extend((w + ("h",), sign * (-1) ** q) for w, sign in paths(p - 1, q))
    if q:
        out.extend((w + ("v",), sign) for w, sign in paths(p, q - 1))
    return tuple(out)


def shuffle_basis(pair):
    a, b = pair
    terms = []
    for steps, sign in paths(len(a) - 1, len(b) - 1):
        i = j = 0
        out = [(a[0], b[0])]
        for step in steps:
            i += step == "h"
            j += step == "v"
            out.append((a[i], b[j]))
        terms.append((sign, simplex(out)))
    return plus(*terms)


def shuffle(chain):
    return linear(chain, shuffle_basis)


def diagonal(chain):
    return linear(chain, lambda s: simplex(tuple((u, u) for u in s)))


@lru_cache(None)
def r_basis(s):
    if len(s) == 1:
        return {}
    residual = plus((1, diagonal(simplex(s))), (-1, shuffle(aw(simplex(s)))),
                    (-1, linear(bd_basis(s), r_basis)))
    return linear(residual, lambda a: simplex(((s[0], s[0]),) + a))


def h_basis(s, n):
    return simplex((0,) + s) if len(s) - 1 < n else {}


def fprime_basis(s, n):
    return plus((1, simplex(s)), (-1, bd(h_basis(s, n))),
                (-1, linear(bd_basis(s), lambda a: h_basis(a, n))))


def k_basis(pair, n):
    a, b = pair
    return plus((1, tensor(h_basis(a, n), simplex(b))),
                ((-1) ** (len(a) - 1), tensor(fprime_basis(a, n), h_basis(b, n))))


def l_basis(s, n):
    return plus((1, r_basis(s)),
                (1, shuffle(linear(aw(simplex(s)), lambda p: k_basis(p, n)))))


def main():
    verts = range(3)
    samples = {q: [s for s in product(verts, repeat=q + 1) if simplex(s)]
               for q in range(5)}
    checks = 0
    for q in range(5):
        for a in samples[q]:
            ac = simplex(a)
            assert tensor_bd(aw(ac)) == aw(bd(ac))
            assert plus((1, bd(r_basis(a))), (1, linear(bd(ac), r_basis))) == plus(
                (1, diagonal(ac)), (-1, shuffle(aw(ac))))
            checks += 2
    for p in range(5):
        for q in range(5 - p):
            for a in samples[p]:
                for b in samples[q]:
                    tc = tensor(simplex(a), simplex(b))
                    assert bd(shuffle(tc)) == shuffle(tensor_bd(tc))
                    checks += 1
                    for n in (1, 2, 3):
                        lhs = plus((1, tensor_bd(k_basis((a, b), n))),
                                   (1, linear(tensor_bd(tc), lambda t: k_basis(t, n))))
                        rhs = plus((1, tc), (-1, tensor(fprime_basis(a, n), fprime_basis(b, n))))
                        assert lhs == rhs
                        checks += 1
    for n in (1, 2, 3):
        for q in range(4):
            for a in samples[q]:
                ac = simplex(a)
                lhs = plus((1, bd(l_basis(a, n))),
                           (1, linear(bd(ac), lambda s: l_basis(s, n))))
                transformed = linear(aw(ac), lambda p: tensor(
                    fprime_basis(p[0], n), fprime_basis(p[1], n)))
                assert lhs == plus((1, diagonal(ac)), (-1, shuffle(transformed)))
                checks += 1
                if q < n:
                    expected = {(0,): 1} if q == 0 else {}
                    assert fprime_basis(a, n) == expected
                    checks += 1
    print(f"PASS: {checks} exact integral chain identities on 3 vertices; degrees through 4.")


if __name__ == "__main__":
    main()
