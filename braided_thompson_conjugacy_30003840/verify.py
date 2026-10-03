#!/usr/bin/env python3
"""Exact elementary checks for the partial results, not a conjugacy solver."""
import itertools
import json
import random


def linking(n, word):
    positions = list(range(n))
    twice = [[0] * n for _ in range(n)]
    for letter in word:
        i = abs(letter) - 1
        assert 0 <= i < n - 1
        a, b = positions[i:i + 2]
        twice[a][b] += 1 if letter > 0 else -1
        twice[b][a] = twice[a][b]
        positions[i], positions[i + 1] = b, a
    assert positions == list(range(n)), "Input must be a pure braid."
    assert all(x % 2 == 0 for row in twice for x in row)
    return tuple(tuple(x // 2 for x in row) for row in twice)


def submatrix(m, indices):
    return tuple(tuple(m[i][j] for j in indices) for i in indices)


def rotate(m, shift):
    n = len(m)
    return submatrix(m, [(i + shift) % n for i in range(n)])


def reduce_linear(m):
    assert m and all(len(row) == len(m) for row in m)
    keep = [0] + [i for i in range(1, len(m)) if m[i] != m[i - 1]]
    return submatrix(m, keep)


def reduce_cyclic(m):
    # Try every cylinder boundary as the cut. A cut through a twin run
    # leaves equal first/last rows; remove the last copy in that case.
    possibilities = []
    for shift in range(len(m)):
        r = reduce_linear(rotate(m, shift))
        if len(r) > 1 and r[0] == r[-1]:
            r = submatrix(r, list(range(len(r) - 1)))
        possibilities.extend(rotate(r, k) for k in range(len(r)))
    return min(possibilities)


def clone(m, index):
    indices = list(range(len(m)))
    indices.insert(index + 1, index)
    return submatrix(m, indices)


def product(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def inverse(a):
    assert a[0][0] * a[1][1] - a[0][1] * a[1][0] == 1
    return ((a[1][1], -a[0][1]), (-a[1][0], a[0][0]))


def run():
    p3 = linking(3, [1, 1])
    q3 = linking(3, [2, 1, 1, -2])
    assert p3[0][-1] == 0 and q3[0][-1] == 1
    p4 = linking(4, [1, 1, 3, 3])
    q4 = linking(4, [2, 1, 1, 3, 3, -2])
    assert reduce_cyclic(p4) != reduce_cyclic(q4)
    comm = [1, 1, 2, 2, -1, -1, -2, -2]
    assert linking(3, comm) == ((0, 0, 0),) * 3
    u, l = ((1, 1), (0, 1)), ((1, 0), (-1, 1))
    assert product(product(u, l), u) == product(product(l, u), l)
    u2, l2 = product(u, u), product(l, l)
    image = product(product(product(u2, l2), inverse(u2)), inverse(l2))
    assert image != ((1, 0), (0, 1))
    rng = random.Random(30003840)
    tested = 0
    for n in range(1, 8):
        for _ in range(40):
            m = [[0] * n for _ in range(n)]
            for i, j in itertools.combinations(range(n), 2):
                m[i][j] = m[j][i] = rng.randrange(-2, 3)
            m = tuple(map(tuple, m))
            linear, circular = reduce_linear(m), reduce_cyclic(m)
            for __ in range(8):
                m = clone(m, rng.randrange(len(m)))
                assert reduce_linear(m) == linear
                assert reduce_cyclic(m) == circular
                shift = rng.randrange(len(m))
                assert reduce_cyclic(rotate(m, shift)) == circular
                tested += 1
    # Repeated nonadjacent twin runs must remain distinct linear runs.
    repeated = ((0, 1, 0), (1, 0, 1), (0, 1, 0))
    assert len(reduce_linear(repeated)) == 3
    assert len(reduce_cyclic(repeated)) == 2
    return {"status": "PASS", "scope": "Exact elementary witnesses and finite linking-pattern checks only",
            "F_ambient_witness": {"p": p3, "q": q3},
            "T_ambient_witness": {"p": p4, "q": q4},
            "zero_linking_commutator_SL2Z_image": image,
            "cloning_and_rotation_test_cases": tested,
            "solves_target_conjugacy_problem": False}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
