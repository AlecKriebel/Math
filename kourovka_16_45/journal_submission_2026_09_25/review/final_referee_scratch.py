"""Independent exact checks reconstructed from the compressed manuscript.

This is arithmetic corroboration, not a proof of the universal bounds.
No project verification code or earlier audit code is imported.
"""

P = 29
I = (1, 0, 0, 1)
NEG = (28, 0, 0, 28)
A = (0, 28, 1, 0)
B = (2, 7, 12, 28)
R = [A, (12, 24, 0, 17), (25, 3, 4, 4)]


def mul(a, b):
    return (
        (a[0] * b[0] + a[1] * b[2]) % P,
        (a[0] * b[1] + a[1] * b[3]) % P,
        (a[2] * b[0] + a[3] * b[2]) % P,
        (a[2] * b[1] + a[3] * b[3]) % P,
    )


def power(a, n):
    out = I
    for _ in range(n):
        out = mul(out, a)
    return out


def order(a):
    out = I
    for n in range(1, 500):
        out = mul(out, a)
        if out == I:
            return n
    raise AssertionError("Order exceeds independent check bound")


def closure(generators):
    seen, queue = {I}, [I]
    for a in queue:
        for g in generators:
            b = mul(a, g)
            if b not in seen:
                seen.add(b)
                queue.append(b)
    return seen


def act(a, v):
    return ((a[0] * v[0] + a[1] * v[1]) % P,
            (a[2] * v[0] + a[3] * v[1]) % P)


def add(v, w):
    return ((v[0] + w[0]) % P, (v[1] + w[1]) % P)


H = closure([A, B])
assert power(A, 2) == power(B, 3) == power(mul(A, B), 5) == NEG
assert all((r[0] * r[3] - r[1] * r[2]) % P == 1 for r in H)
assert len(H) == 120
assert mul(mul(B, A), power(B, 2)) == R[1]
assert mul(mul(A, R[1]), power(mul(A, B), 2)) == R[2]
assert [power(r, 2) for r in R] == [NEG] * 3
assert [order(mul(R[i], R[j])) for i, j in [(1, 2), (0, 2), (0, 1)]] == [4, 3, 10]
pairs = [closure([R[j] for j in range(3) if j != i]) for i in range(3)]
assert list(map(len, pairs)) == [8, 12, 20]
assert len(closure(R)) == 120
assert set.intersection(*pairs) == {I, NEG}
assert pairs[0] & pairs[1] == closure([R[2]])
assert all(R[i] not in pairs[i] for i in range(3))

ZERO = (0, 0)
lines = [{((t*x) % P, (t*y) % P) for t in range(P)}
         for x, y in [(1, t) for t in range(P)] + [(0, 1)]]
stabilizers = [{h for h in H if {act(h, v) for v in W} == W}
              for W in lines]
assert len(lines) == 30
assert set(map(len, stabilizers)) == {4}
for W, S in zip(lines, stabilizers):
    v = next(v for v in W if v != ZERO)
    assert len({act(h, v) for h in S}) == len(S)

L = []
for v, c in [((1, 0), (0, 0)), ((0, 1), (0, 0)), ((1, 1), (2, 0))]:
    W = {((t*v[0]) % P, (t*v[1]) % P) for t in range(P)}
    L.append({(w, I) for w in W} | {(add(w, c), NEG) for w in W})
assert list(map(len, L)) == [58] * 3
assert L[0] & L[1] == {(ZERO, I), (ZERO, NEG)}
assert L[0] & L[2] == {(ZERO, I), ((2, 0), NEG)}
assert L[1] & L[2] == {(ZERO, I), ((0, 27), NEG)}
assert set.intersection(*L) == {(ZERO, I)}
assert len(H) * P * P == 100920
assert 3 * len(H) * P * P // 58 == 5220
print("PASS: every displayed matrix and affine intersection witness;")
print("120 matrices, pair orders 8/12/20, 30 faithful line stabilizers of order 4,")
print("affine group order 100920, faithful witness degree 5220.")
