#!/usr/bin/env python3
"""Independent exact audit controls, Python standard library only.

The cyclic-character engine evaluates every group element in Z[X]/Phi_n(X).
It does not import the release verifier or infer fields from its spectra.
No check is a proof/search for arbitrary irreducible finite-group characters.
Run: python3 independent_checks.py [--output result.json]
"""
import argparse
import hashlib
import itertools
import json
import math
from collections import Counter
from functools import lru_cache
from pathlib import Path


def divisors(n):
    return tuple(d for d in range(1, n + 1) if n % d == 0)


def trim(f):
    while len(f) > 1 and f[-1] == 0:
        f.pop()
    return f


def divide_monic(f, g):
    f = list(f)
    q = [0] * (len(f) - len(g) + 1)
    for j in range(len(q) - 1, -1, -1):
        q[j] = f[j + len(g) - 1]
        for k, c in enumerate(g):
            f[j + k] -= q[j] * c
    assert not any(f)
    return trim(q)


@lru_cache(None)
def cyclotomic(n):
    f = [-1] + [0] * (n - 1) + [1]
    for d in divisors(n)[:-1]:
        f = divide_monic(f, cyclotomic(d))
    return tuple(f)


@lru_cache(None)
def powers(n):
    f = cyclotomic(n)
    degree = len(f) - 1
    one = (1,) + (0,) * (degree - 1)
    ans = [one]
    for k in range(1, n):
        v = [0] + list(ans[-1])
        top = v.pop()
        ans.append(tuple(x - top * c for x, c in zip(v, f[:-1])))
    return tuple(ans)


@lru_cache(None)
def units(n):
    return tuple(a for a in range(n) if math.gcd(a, n) == 1)


def sum_roots(n, exponents):
    rows = [powers(n)[j % n] for j in exponents]
    return tuple(sum(c) for c in zip(*rows))


def evaluated_stabilizer(n, spectrum):
    # sigma_a(chi(x^k)) = chi(x^(ak)); compare exact algebraic integers.
    values = tuple(sum_roots(n, (j * k for j in spectrum)) for k in range(n))
    return tuple(a for a in units(n)
                 if all(values[k] == values[a * k % n] for k in range(n)))


def least_conductor(n, stabilizer):
    for d in divisors(n):
        if all(a in stabilizer for a in units(n) if a % d == 1 % d):
            return d
    raise AssertionError("No candidate conductor")


def ppart(n, p):
    out = 1
    while n % p == 0:
        out *= p
        n //= p
    return out


def small_degree():
    plans = [(2, 8, 1), (2, 24, 1), (3, 9, 2), (3, 18, 2),
             (3, 45, 2), (5, 25, 3), (5, 50, 2), (7, 49, 2)]
    results = []
    for p, n, maxdegree in plans:
        pn = ppart(n, p)
        count = 0
        for d in range(1, maxdegree + 1):
            for w in itertools.combinations_with_replacement(range(n), d):
                h = evaluated_stabilizer(n, w)
                conductor = least_conductor(n, h)
                hp = evaluated_stabilizer(pn, w)
                restriction_degree = len(units(pn)) // len(hp)
                top_degree = len(units(ppart(conductor, p)))
                assert top_degree % restriction_degree == 0
                assert (top_degree // restriction_degree) % p != 0
                count += 1
        results.append(dict(p=p, n=n, max_degree=maxdegree, cases=count))
    assert sum(r['cases'] for r in results) == 7229
    return results


def cyclic_induction():
    # Count solutions to p^(b-j) | z and z == t (mod p^h), by CRT compatibility.
    def at_most(p, b, h, t, j):
        if t % (p ** min(h, b - j)):
            return 0
        return p ** (b - max(h, b - j))
    count = 0
    for p in (2, 3, 5):
        for b in range(1, 5):
            for h in range(b):
                for t in range(p ** h):
                    for i in range(2, b + 1):
                        value = at_most(p, b, h, t, i) - at_most(p, b, h, t, i - 1)
                        assert value % p == 0
                        count += 1
    assert count == 748
    # The stated exclusion i=1 is real, rather than merely technical.
    return dict(congruences=count, excluded_i1_counts={str(p): p - 1 for p in (2, 3, 5)})


def obstruction_examples():
    result = []
    for p, q in ((2, 3), (3, 5), (5, 7), (7, 11), (11, 13)):
        # Work in C_(p^2) x C_q directly, avoiding the release CRT encoding.
        pairs = {(0, 0)} | {(1 + p * j, j) for j in range(p)}
        fixed = []
        for u in units(p * p):
            for v in units(q):
                moved = {(u * a % (p * p), v * b % q) for a, b in pairs}
                if moved == pairs:
                    fixed.append((u, v))
        assert fixed == [(1, 1)]
        local = tuple([0] + [1 + p * j for j in range(p)])
        h = evaluated_stabilizer(p * p, local)
        conductor = least_conductor(p * p, h)
        assert conductor == (1 if p == 2 else p)
        assert len(h) == p
        assert len(pairs) == p + 1
        # Explicit exact cancellation at every x^k, in Q(zeta_(p^2)).
        for k in range(p * p):
            actual = sum_roots(p * p, (k * e for e in local))
            expected = sum_roots(p * p, [0] if k % p else [0] + [k] * p)
            assert actual == expected
        # Every nontrivial decomposition coordinate is a primitive p^2 root.
        assert all(math.gcd(1 + p * j, p * p) == 1 for j in range(1, p))
        result.append(dict(p=p, q=q, degree=p+1, norm=p+1,
                           global_conductor=p*p*q, local_conductor=conductor,
                           tested_index=len(h), global_stabilizer=fixed))
    h = evaluated_stabilizer(8, (0, 1, 7))
    assert h == (1, 7) and least_conductor(8, h) == 8
    return result, dict(spectrum=[0, 1, 7], conductor=8,
                        stabilizer=list(h), tested_index=2, norm=3)


def compose(x, y):
    return tuple(x[y[i]] for i in range(len(x)))


def inverse(x):
    ans = [0] * len(x)
    for i, j in enumerate(x):
        ans[j] = i
    return tuple(ans)


def closure(generators, n=5):
    identity = tuple(range(n))
    found, todo = {identity}, [identity]
    while todo:
        x = todo.pop()
        for g in generators:
            y = compose(x, g)
            if y not in found:
                found.add(y)
                todo.append(y)
    return found


def power(x, i):
    y = tuple(range(len(x)))
    for _ in range(i):
        y = compose(y, x)
    return y


def normalizer(group, subgroup):
    return {g for g in group if {compose(compose(g, h), inverse(g))
                                for h in subgroup} == subgroup}


def permutation_restriction(group, subgroup, sylow):
    unseen = set(group)
    cosets = []
    while unseen:
        g = min(unseen)
        c = frozenset(compose(g, h) for h in subgroup)
        cosets.append(c)
        unseen -= c
    # Count fixed cosets directly, independently of the normalizer formula.
    values = {x: sum(frozenset(compose(x, g) for g in c) == c for c in cosets)
              for x in sylow}
    return len(cosets), values


def composite_index_mackey():
    group = set(itertools.permutations(range(5)))
    c3 = (1, 2, 0, 3, 4)
    p3 = closure([c3])
    n3 = normalizer(group, p3)
    s3 = closure([c3, (1, 0, 2, 3, 4)])
    result = []
    # G=S5 x C9, P=C3 x C9, K=K0 x C9, psi=1 x faithful lambda.
    # P is abelian and every constituent has faithful central C9 component.
    for k in (n3, s3):
        index, vals = permutation_restriction(group, k, p3)
        ratio = len(n3) // len(normalizer(k, p3))
        # Their s_2 equals their degree, because all constituents have order 9.
        assert index % 3 == ratio % 3
        result.append(dict(group='S5 x C9', p=3, index=index,
                           normalizer_index=ratio, s_2=index,
                           fixed_cosets_nonidentity=vals[c3]))
    # G=S5 x C4, P=D8 x C4, K=P. The high-order linear sum is not total degree.
    r = (1, 2, 3, 0, 4)
    s = (0, 3, 2, 1, 4)
    p2 = closure([r, s])
    assert len(p2) == 8
    index, vals = permutation_restriction(group, p2, p2)
    multiplicities = []
    for epsilon, delta in itertools.product((1, -1), repeat=2):
        inner = sum(vals[compose(power(r, i), power(s, j))] * epsilon**i * delta**j
                    for i in range(4) for j in range(2))
        assert inner % 8 == 0
        multiplicities.append(inner // 8)
    ratio = len(normalizer(group, p2)) // 8
    assert sum(multiplicities) % 2 == ratio % 2
    result.append(dict(group='S5 x C4', p=2, index=index,
                       normalizer_index=ratio, s_2=sum(multiplicities),
                       linear_multiplicities=multiplicities))
    return result


def cyclotomic_lifting():
    count = 0
    noncyclic_binary = 0
    for p in (2, 3, 5):
        for a in range(2, 5):
            n = p ** a
            pp_elements = set()
            subgroups = set()
            for u in units(n):
                generated = set()
                x = 1
                while x not in generated:
                    generated.add(x)
                    x = x * u % n
                size = len(generated)
                if ppart(size, p) == size:
                    pp_elements.add(u)
                    subgroups.add(frozenset(generated))
            subgroups.add(frozenset(pp_elements))
            for s in subgroups:
                for e in range(a, a + 3):
                    lifted = [u for u in units(p ** e) if u % n in s]
                    assert {u % n for u in lifted} == set(s)
                    assert ppart(len(lifted), p) == len(lifted)
                    fixed = [j for j in units(n) if all(u * j % n == j for u in s)]
                    assert bool(fixed) == (s == frozenset({1}))
                    if p == 2 and a >= 3 and s == frozenset(pp_elements):
                        noncyclic_binary += 1
                    count += 1
    return dict(preimage_and_fixed_point_controls=count,
                noncyclic_binary_controls=noncyclic_binary)


def freeze_integrity():
    root = Path(__file__).resolve().parent.parent
    path = root / 'RELEASE_MANIFEST.json'
    if not path.exists():
        return {'status': 'SKIP', 'reason': 'Portable copy has no adjacent frozen packet'}
    manifest = json.loads(path.read_text())
    files = []
    for record in manifest['files']:
        data = (root / record['path']).read_bytes()
        assert len(data) == record['bytes']
        assert hashlib.sha256(data).hexdigest() == record['sha256']
        files.append(record['path'])
    return dict(status='PASS', files=files, public_release_manifest_verified=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    integrity = freeze_integrity()
    small = small_degree()
    induction = cyclic_induction()
    reducible, binary = obstruction_examples()
    result = dict(status='PASS', scope='Independent finite controls; not a general resolution',
                  freeze_integrity=integrity, small_degree_plans=small,
                  small_degree_cases=sum(x['cases'] for x in small),
                  cyclic_induction=induction, reducible_obstructions=reducible,
                  binary_conductor_warning=binary,
                  composite_index_mackey_controls=composite_index_mackey(),
                  cyclotomic_lifting_controls=cyclotomic_lifting())
    encoded = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(encoded)
    print(encoded, end='')


if __name__ == '__main__':
    main()
