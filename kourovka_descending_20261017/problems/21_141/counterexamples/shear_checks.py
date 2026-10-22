"""Exact local checks for the nonproper shear example; no coherence inference.

Run with any Python 3. The proof for all primes is in approach_counterexamples.md.
"""
from collections import deque


def mul(a, b, p):
    return tuple(sum(a[2*i+k]*b[2*k+j] for k in range(2)) % p
                 for i in range(2) for j in range(2))


def power(a, n, p):
    out = (1, 0, 0, 1)
    for _ in range(n):
        out = mul(out, a, p)
    return out


def order(a, p):
    out = (1, 0, 0, 1)
    for n in range(1, p*(p*p-1)+1):
        out = mul(out, a, p)
        if out == (1, 0, 0, 1):
            return n
    raise AssertionError("order not found")


def act(a, v, p):
    return ((a[0]*v[0]+a[1]*v[1]) % p,
            (a[2]*v[0]+a[3]*v[1]) % p)


def line(v, p):
    if v[0]:
        scale = pow(v[0], -1, p)
        return (1, v[1]*scale % p)
    assert v[1]
    return (0, 1)


def subgroup(gens, p):
    identity = (1, 0, 0, 1)
    seen, queue = {identity}, deque([identity])
    while queue:
        a = queue.popleft()
        for g in gens:
            b = mul(a, g, p)
            if b not in seen:
                seen.add(b)
                queue.append(b)
    return seen


def run():
    for p in (2, 3, 5, 7, 11, 13, 17, 19):
        u, l = (1, 1, 0, 1), (1, 0, 1, 1)
        li = (1, 0, -1 % p, 1)
        assert mul(l, li, p) == (1, 0, 0, 1)
        lines = {(1, x) for x in range(p)} | {(0, 1)}
        common = {v for v in lines
                  if line(act(u, v, p), p) == v
                  and line(act(l, v, p), p) == v}
        assert not common
        witness = mul(u, li, p)
        if p != 2:
            witness = mul(witness, u, p)
        expected_order = 3 if p == 2 else 4
        assert order(witness, p) == expected_order
        generated = subgroup((u, l), p)
        assert len(generated) == p*(p*p-1)
        print(f"p={p}: no common invariant line; witness order "
              f"{expected_order}; generated subgroup order {len(generated)}")
    print("PASS: all exact finite matrix checks; infinite-group proof is separate.")


if __name__ == "__main__":
    run()
