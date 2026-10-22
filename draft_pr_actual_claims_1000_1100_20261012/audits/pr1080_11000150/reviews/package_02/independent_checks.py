#!/usr/bin/env python3
"""New exact finite controls for whole review 02; not a universal proof."""
from fractions import Fraction as F
from itertools import product, combinations
import json
import sys


def require(test, message):
    if not test:
        raise RuntimeError(message)


# Integral Heisenberg group: (x,y,z) is [[1,x,z],[0,1,y],[0,0,1]].
ONE = (0, 0, 0)


def mul(a, b):
    x, y, z = a
    X, Y, Z = b
    return x + X, y + Y, z + Z + x * Y


def inv(a):
    x, y, z = a
    return -x, -y, x * y - z


def ev(word):
    out = ONE
    for a in word:
        out = mul(out, a)
    return out


def positive(a):
    return a > ONE  # Lex order x,y,z is conjugation invariant here.


def le(a, b):
    q = mul(b, inv(a))
    return q == ONE or positive(q)


def subsequence(a, b):
    cursor = iter(b)
    return all(any(x == y for y in cursor) for x in a)


def insertion(retained, blocks, fault=False):
    full = []
    prefix = ONE
    right = ONE
    for j, block in enumerate(blocks):
        full.extend(block)
        right = mul(right, ev(block) if fault else mul(mul(prefix, ev(block)), inv(prefix)))
        if j < len(retained):
            full.append(retained[j])
            prefix = mul(prefix, retained[j])
    return mul(ev(full), inv(ev(retained))), right


def matchings(items):
    if not items:
        yield []
    else:
        a = items[0]
        for j in range(1, len(items)):
            b = items[j]
            for rest in matchings(items[1:j] + items[j + 1:]):
                yield [(a, b)] + rest


def cycles(p):
    left = set(p)
    count = 0
    while left:
        start = next(iter(left))
        cur = start
        while cur in left:
            left.remove(cur)
            cur = p[cur]
        require(cur == start, "permutation cycle did not close")
        count += 1
    return count


def ribbon_boundary(sigma, alpha):
    return cycles({d: sigma[alpha[d]] for d in sigma})


def main(fault=None):
    grid = list(product(range(-1, 2), repeat=3))
    A, B, C, D = (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, -2, -5)
    letters = (A, B, C, D)
    normal = ordered = insertion_cases = proper_insertions = 0
    for a, b in product(grid, repeat=2):
        require(mul(a, inv(a)) == ONE, "inverse")
        conjugate = mul(mul(b, a), inv(b))
        require(positive(conjugate) == positive(a), "normal cone")
        normal += 1
        for t in grid:
            require(le(a, b) == le(mul(t, a), mul(t, b)), "left invariant order")
            require(le(a, b) == le(mul(a, t), mul(b, t)), "right invariant order")
            ordered += 2
    block_options = ((), (A,), (B,), (D,), (A, B), (B, A))
    for size in range(4):
        for retained in product(letters, repeat=size):
            for blocks in product(block_options, repeat=size + 1):
                lhs, rhs = insertion(retained, blocks, fault == "conjugation")
                require(lhs == rhs, "insertion conjugation identity")
                insertion_cases += 1
                if any(blocks):
                    require(positive(lhs), "proper insertion must be positive")
                    require(ev(retained) != mul(lhs, ev(retained)), "comparable fiber")
                    proper_insertions += 1
    # An alphabet submonoid can fail normality even inside a normal cone.
    require(mul(mul(inv(B), A), B) == (1, 0, 1), "nonnormal H witness")
    require(ev((A,)) != (1, 0, 1), "x=1,y=0 allows only A in <A,B>")
    # Raw letters may be composite and the expansion need not be injective.
    expansion = {"a": (A,), "b": (B,), "c": (A, A), "d": (A,)}
    if fault == "erasing":
        expansion["c"] = ()
    expanded = 0
    for n in range(7):
        for word in product(expansion, repeat=n):
            atoms = tuple(v for k in word for v in expansion[k])
            require(len(atoms) >= len(word), "nonerasing raw-length bound")
            expanded += 1
    require(ev((A, B)) != ev((B, A)), "ordered words cannot be identified by matching")
    # Exhaustive finite fibers with a duplicate letter and a noncentral target.
    alphabet = {"a": A, "b": B, "c": mul(A, A), "d": A}
    target = ev((A, A, B))
    fiber = []
    for n in range(6):
        for w in product(alphabet, repeat=n):
            if ev(alphabet[x] for x in w) == target:
                fiber.append(w)
    require(fiber and max(map(len, fiber)) <= 3, "finite sample BF length")
    for u, v in product(fiber, repeat=2):
        require(u == v or not subsequence(u, v), "equal fiber antichain")
    # Full alternating forms over F2 through dimension 8, including zero.
    parity_cases = 0
    for g in range(1, 5):
        for v in product((0, 1), repeat=2 * g):
            pairing = sum(v[i] * v[g+i] + v[g+i] * v[i] for i in range(g)) % 2
            if fault == "parity":
                pairing = 1
            require(pairing == 0, "alternating self pairing")
            parity_cases += 1
    # Every pairing of darts at one ribbon vertex, up to five edges.
    ribbon_cases = 0
    for e in range(1, 6):
        sigma = {j: (j + 1) % (2 * e) for j in range(2 * e)}
        for matching in matchings(list(range(2 * e))):
            alpha = {a: b for x, y in matching for a, b in [(x, y), (y, x)]}
            b = ribbon_boundary(sigma, alpha)
            numerator = 1 + e - b
            require(numerator >= 0 and numerator % 2 == 0, "ribbon Euler genus")
            require(numerator // 2 <= e // 2, "ribbon genus bound")
            ribbon_cases += 1
    alpha = {0: 2, 2: 0, 1: 3, 3: 1}
    crossing = {0: 1, 1: 2, 2: 3, 3: 0}
    adjacent = {0: 2, 2: 1, 1: 3, 3: 0}
    require(ribbon_boundary(crossing, alpha) == 1, "crossing punctured torus")
    require(ribbon_boundary(adjacent, alpha) == 3, "different ribbon order gives pants")
    require(ribbon_boundary({0: 1, 1: 0}, {0: 1, 1: 0}) == 2, "isolated circle annulus")
    # Explicit rational perturbations of m concurrent straight branches.
    crossing_pairs = endpoint_orders = triple_checks = 0
    for m in range(2, 15):
        labels = list(range(-m, m + 1))
        eps = F(1, 100 * m ** 3)
        points = []
        for s, t in combinations(labels, 2):
            x, y = -eps * m * (s + t), -eps * s * t
            require(abs(x) < F(1, 10) and abs(y) < F(1, 10), "crossing stays local")
            for endpoint in (-1, 1):
                before = F(s-t, m) * endpoint
                after = before + eps * (s*s-t*t)
                require(before * after > 0, "endpoint ordering preserved")
                endpoint_orders += 1
            points.append((x, y))
            crossing_pairs += 1
        require(len(set(points)) == len(points), "no coinciding pair crossings")
        for s, t, u in combinations(labels, 3):
            x, y = -eps * m * (s+t), -eps * s*t
            require(y != F(u, m)*x + eps*u*u, "triple concurrence remained")
            triple_checks += 1
    result = {
        "status": "PASS", "normal_cone_checks": normal, "two_sided_order_checks": ordered,
        "noncommutative_insertion_cases": insertion_cases, "proper_positive_insertions": proper_insertions,
        "nonerasing_expansion_cases": expanded, "sample_noncentral_duplicate_alphabet_fiber": ["".join(w) for w in fiber],
        "mod2_alternation_cases": parity_cases, "ribbon_pairings": ribbon_cases,
        "local_crossing_pairs": crossing_pairs, "endpoint_order_checks": endpoint_orders,
        "no_triple_concurrence_checks": triple_checks, "assertions_used": False,
        "scope": "New exact finite mathematical fault controls; neither surface enumeration nor universal proof nor exhaustive priority evidence."
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
