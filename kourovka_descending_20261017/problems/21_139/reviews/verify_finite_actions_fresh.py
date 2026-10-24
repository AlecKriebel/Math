#!/usr/bin/env python3
"""Independent 2026-10-24 audit: actual right-action relator walks only.

No imports from the construction authors or their saved results. Rational
elimination uses Fraction; all permutation actions and words are rebuilt here.
"""
from fractions import Fraction
from math import gcd
from datetime import datetime, timezone
from pathlib import Path
import json


def inv(p):
    out = [0] * len(p)
    for i, j in enumerate(p):
        out[j] = i
    assert sorted(p) == list(range(len(p)))
    return out


def negative(w):
    return [(g, -s) for g, s in reversed(w)]


def cellular(actions, word):
    """Rows: a-,b-,t-edges; columns: relator cells; actual right action."""
    size = len(actions[0])
    backwards = [inv(p) for p in actions]
    matrix = [[0] * size for _ in range(3 * size)]
    for face in range(size):
        cursor = face
        for g, sign in word:
            if sign == 1:
                matrix[g * size + cursor][face] += 1
                cursor = actions[g][cursor]
            else:
                cursor = backwards[g][cursor]
                matrix[g * size + cursor][face] -= 1
        assert cursor == face, ("relation does not close", face)
    # Check d1 d2, separately from closed relator paths.
    for col in range(size):
        vertices = [0] * size
        for g, p in enumerate(actions):
            for v in range(size):
                coeff = matrix[g * size + v][col]
                vertices[p[v]] += coeff
                vertices[v] -= coeff
        assert not any(vertices)
    reached = {0}
    stack = [0]
    while stack:
        v = stack.pop()
        for p in actions + backwards:
            if p[v] not in reached:
                reached.add(p[v])
                stack.append(p[v])
    assert len(reached) == size, "cover is disconnected"
    return matrix


def rank(matrix):
    m = [[Fraction(x) for x in row] for row in matrix]
    pivot = 0
    cols = len(m[0])
    for c in range(cols):
        candidates = [r for r in range(pivot, len(m)) if m[r][c]]
        if not candidates:
            continue
        r = candidates[0]
        m[pivot], m[r] = m[r], m[pivot]
        scale = m[pivot][c]
        for j in range(c, cols):
            m[pivot][j] /= scale
        for i in range(pivot + 1, len(m)):
            scale = m[i][c]
            if scale:
                for j in range(c, cols):
                    m[i][j] -= scale * m[pivot][j]
        pivot += 1
        if pivot == cols:
            break
    return pivot


def apply(matrix, vector):
    return [sum(x * y for x, y in zip(row, vector)) for row in matrix]


def word_for(p, k, eps):
    w = ([(0, 1)] + [(1, 1)] * k) * p + [(1, eps)]
    return [(2, -1), (0, 1), (2, 1)] + negative(w)


def slot_case(q, n):
    size = 2 * n * q
    index = lambda side, v, j: (side * n + v) * q + j
    P = [0] * size
    R = [0] * size
    for side in range(2):
        for v in range(n):
            for j in range(q):
                P[index(side, v, j)] = index(side, v, (j + 1) % q)
    for v in range(n):
        for j in range(q):
            u = (v + 1) % n if j == 1 else v
            left, right = index(0, v, j), index(1, u, j)
            R[left], R[right] = right, left
    T = [R[P[v]] for v in range(size)]
    m = cellular([list(range(size)), P, T], word_for(q - 1, 1, 1))
    b2 = size - rank(m)
    assert b2 == n * (q - 2) + 1
    # Check the claimed boundary formula against every direct-walk column.
    Pi, Ti = inv(P), inv(T)
    for j in range(size):
        orbit = []
        cur = j
        for _ in range(q):
            orbit.append(cur)
            cur = P[cur]
        a = [0] * size
        a[Ti[j]] += 1
        a[Pi[j]] += 1
        for u in orbit:
            a[u] -= 1
        assert [m[i][j] for i in range(size)] == a
        b = [-1 if i in orbit else 0 for i in range(size)]
        assert [m[size+i][j] for i in range(size)] == b
        assert not any(m[2*size+i][j] for i in range(size))
    return {"q": q, "n": n, "degree": size, "b2": b2}


def telescoping_case(p, k, eps, n):
    q = p * k + eps
    size = q * n
    P = [0] * size
    T = [0] * size
    for j in range(n):
        for i in range(q):
            P[j * q + i] = j * q + (i + 1) % q
            T[j * q + i] = j * q + p * i % q
    unused = [i for i in range(q) if i not in (0, -k % q)]
    if n > 1:
        assert unused
        s = unused[0]
        for j in range(n):
            T[j * q + s] = (j + 1) % n * q + p * s % q
    m = cellular([list(range(size)), inv(P), inv(T)], word_for(p, k, eps))
    for j in range(n):
        v = [0] * size
        v[j * q] = 1
        v[j * q + (-k % q)] = -1
        assert not any(apply(m, v))
    b2 = size - rank(m)
    assert b2 >= n
    return {"p": p, "k": k, "epsilon": eps, "n": n,
            "degree": size, "b2": b2,
            "all_abelian_blind": gcd(q, k - 1) == gcd(q, k + 1) == 1}


def exact_e(n, affine=False):
    size = 5 * n
    P = [0] * size
    T = [0] * size
    for j in range(n):
        for i in range(5):
            P[5*j+i] = 5*j+(i+1) % 5
        if affine:
            assert n == 1
            for i in range(5):
                T[i] = (2*i) % 5
        else:
            for i, target in [(0, 0), (1, 1), (2, 3), (3, 4), (4, 2)]:
                T[5*j+i] = 5*((j+1) % n if i == 2 else j)+target
    m = cellular([list(range(size)), inv(P), inv(T)], word_for(2, 2, 1))
    b2 = size - rank(m)
    assert b2 == n
    if not affine:
        for j in range(n):
            v = [0] * size
            v[5*j+1], v[5*j+4] = 1, -1
            assert not any(apply(m, v))
    group_order = None
    if affine:
        identity = tuple(range(5))
        group = {identity}
        stack = [identity]
        while stack:
            g = stack.pop()
            for h in [P, T]:
                product = tuple(h[g[i]] for i in range(5))
                if product not in group:
                    group.add(product)
                    stack.append(product)
        group_order = len(group)
        assert group_order == 20
        # Every element really is affine, proving solvability independently.
        affine_set = {tuple((u*i+v) % 5 for i in range(5))
                      for u in range(1, 5) for v in range(5)}
        assert group == affine_set
    return {"degree": size, "b2": b2, "b1": size+1+b2,
            "affine": affine, "monodromy_order": group_order}


def higher_rank_boundary(n):
    """Two relators, rebuilt separately rather than importing the Fox matrix."""
    ident = list(range(n))
    actions = [ident, ident, ident, [(i+1) % n for i in range(n)]]
    backwards = [inv(p) for p in actions]
    words = [[(3, -1), (0, 1), (3, 1), (2, -1), (1, -1)],
             [(3, -1), (1, 1), (3, 1), (0, -1), (2, -1)]]
    m = [[0] * (2*n) for _ in range(4*n)]
    for r, word in enumerate(words):
        for v in range(n):
            col, cursor = r*n+v, v
            for g, sign in word:
                if sign == 1:
                    m[g*n+cursor][col] += 1
                    cursor = actions[g][cursor]
                else:
                    cursor = backwards[g][cursor]
                    m[g*n+cursor][col] -= 1
            assert cursor == v
    b2 = 2*n-rank(m)
    assert b2 == (1 if n % 2 == 0 else 0)
    return {"degree": n, "b2": b2}


def main():
    results = {"timestamp": datetime.now(timezone.utc).isoformat(),
               "method": "Independent actual right-action relator walks and Fraction rank",
               "slot_flow": [], "telescoping": [], "exact_e": []}
    for q in range(2, 8):
        for n in range(1, 5):
            results["slot_flow"].append(slot_case(q, n))
    parameters = [(1, 1, 1), (1, 2, 1), (1, 3, -1), (2, 1, 1),
                  (2, 2, 1), (2, 2, -1), (2, 3, -1), (3, 1, 1),
                  (3, 2, -1), (4, 2, 1)]
    for p, k, eps in parameters:
        for n in range(1, 4 if p*k+eps > 2 else 2):
            results["telescoping"].append(telescoping_case(p, k, eps, n))
    for n in range(1, 9):
        results["exact_e"].append(exact_e(n))
    results["solvable_witness"] = exact_e(1, affine=True)
    results["higher_rank_boundary"] = [higher_rank_boundary(n) for n in range(1, 9)]
    target = Path(__file__).with_name("finite_action_fresh_checks_20261024.json")
    target.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({"output": str(target), "cases": sum(len(results[k]) for k in
                     ("slot_flow", "telescoping", "exact_e", "higher_rank_boundary")) + 1}, indent=2))


if __name__ == "__main__":
    main()
