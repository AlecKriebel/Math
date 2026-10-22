#!/usr/bin/env python3
"""Exact, source-free checks supporting the partial report for K3 Problem 1.22.

These checks verify algebraic lemmas/models, not the unsolved knot conjecture.
Python 3 standard library only. No network, external files, or implicit assertions.
"""
from fractions import Fraction as F
from math import gcd
import json


def require(condition, name):
    if not condition:
        raise ValueError(name)


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def zero(n, m):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def transpose(a):
    return [list(r) for r in zip(*a)]


def add(a, b, factor=1):
    return [[x + factor*y for x, y in zip(r, s)] for r, s in zip(a, b)]


def mul(a, b):
    return [[sum(x*y for x, y in zip(r, c)) for c in zip(*b)] for r in a]


def power(a, n):
    result = eye(len(a))
    while n:
        if n & 1:
            result = mul(result, a)
        a = mul(a, a)
        n //= 2
    return result


def inverse(a):
    n = len(a)
    aug = [list(map(F, r)) + s for r, s in zip(a, eye(n))]
    for j in range(n):
        k = next((k for k in range(j, n) if aug[k][j]), None)
        require(k is not None, "singular matrix")
        aug[j], aug[k] = aug[k], aug[j]
        p = aug[j][j]
        aug[j] = [x/p for x in aug[j]]
        for i in range(n):
            if i != j:
                p = aug[i][j]
                aug[i] = [x-p*y for x, y in zip(aug[i], aug[j])]
    return [r[n:] for r in aug]


def determinant(a):
    a = [list(map(F, r)) for r in a]
    n, d = len(a), F(1)
    for j in range(n):
        k = next((k for k in range(j, n) if a[k][j]), None)
        if k is None:
            return F(0)
        if k != j:
            a[j], a[k] = a[k], a[j]
            d = -d
        p = a[j][j]
        d *= p
        for i in range(j+1, n):
            c = a[i][j]/p
            for k in range(j+1, n):
                a[i][k] -= c*a[j][k]
    return d


def positive(a):
    return all(determinant([r[:k] for r in a[:k]]) > 0
               for k in range(1, len(a)+1))


def tree_matrix(n, edges):
    q = [[F(2*(i == j)) for j in range(n)] for i in range(n)]
    for i, j in edges:
        q[i][j] = q[j][i] = F(-1)
    return q


def star(arms):
    edges, current = [], 1
    for length in arms:
        previous = 0
        for _ in range(length):
            edges.append((previous, current))
            previous, current = current, current+1
    return current, edges


def trim(p):
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def pmul(p, q):
    out = [0]*(len(p)+len(q)-1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i+j] += x*y
    return trim(out)


def pdiv(p, q):
    p = list(map(F, p))
    q = list(map(F, q))
    out = [F(0)]*max(1, len(p)-len(q)+1)
    while len(p) >= len(q) and p != [0]:
        k, c = len(p)-len(q), p[-1]/q[-1]
        out[k] += c
        for j, x in enumerate(q):
            p[k+j] -= c*x
        trim(p)
    return trim(out), trim(p)


def pgcd(p, q):
    while q != [0]:
        _, r = pdiv(p, q)
        p, q = q, r
    return [x/p[-1] for x in p]


def peval(p, t):
    out = 0
    for a in reversed(p):
        out = out*t+a
    return out


def companion(p):
    require(p[-1] == 1, "monic companion input")
    n = len(p)-1
    c = zero(n, n)
    for j in range(n-1):
        c[j+1][j] = F(1)
    for i in range(n):
        c[i][n-1] = -F(p[i])
    return c


def rank2(a):
    a = [[int(x) % 2 for x in r] for r in a]
    if not a:
        return 0
    row = 0
    for col in range(len(a[0])):
        k = next((i for i in range(row, len(a)) if a[i][col]), None)
        if k is None:
            continue
        a[row], a[k] = a[k], a[row]
        for i in range(len(a)):
            if i != row and a[i][col]:
                a[i] = [x ^ y for x, y in zip(a[i], a[row])]
        row += 1
        if row == len(a):
            break
    return row


def main():
    report = {"scope": "Exact algebraic support only; K3 1.22 remains unsolved."}
    controls = 0
    examples = [("A2", 2, [(0, 1)], 3, 6),
                ("A4", 4, [(i, i+1) for i in range(3)], 5, 10)]
    for label, arms, d, order in [("E6", [1, 2, 2], 3, 12),
                                 ("E8", [1, 2, 4], 1, 15)]:
        n, edges = star(arms)
        examples.append((label, n, edges, d, order))
    monodromy = []
    for label, n, edges, d, order in examples:
        q = tree_matrix(n, edges)
        v = eye(n)
        for i, j in edges:
            v[min(i, j)][max(i, j)] = -1
        m = mul(inverse(v), transpose(v))
        require(add(v, transpose(v)) == q, label+" Seifert form")
        require(positive(q), label+" positivity")
        require(determinant(q) == d, label+" determinant")
        require(mul(mul(transpose(m), q), m) == q, label+" invariant form")
        require(power(m, order) == eye(n), label+" finite order")
        require(all(power(m, k) != eye(n) for k in range(1, order)), label+" exact order")
        controls += 6
        monodromy.append({"type": label, "determinant": d, "exact_order": order})
    report["definite_monodromy_examples"] = monodromy

    # A formal L-space-shaped polynomial; no knot realization is asserted.
    phi6, phi30 = [1, -1, 1], [1, 1, 0, -1, -1, -1, 0, 1, 1]
    p = pmul(pmul(phi6, phi6), phi30)
    c = companion(p)
    u = add(power(c, 30), eye(12), -1)
    require(u != zero(12, 12), "nonzero unipotent part")
    require(mul(u, u) == zero(12, 12), "square-zero unipotent part")
    require(p == list(reversed(p)) and peval(p, 1) == 1, "formal Alexander normalization")
    nonzero = [x for x in reversed(p) if x]
    require(nonzero == [(-1)**i for i in range(len(nonzero))], "formal staircase shape")
    controls += 4
    report["cyclotomic_does_not_imply_finite_order"] = {
        "coefficients_ascending": p,
        "companion_C30_minus_I_nonzero": True,
        "companion_C30_minus_I_squared_zero": True,
        "knot_realization": "NOT_ASSERTED"}

    # Exact polynomial witnesses from the published Baker--Kegel family.
    bk = []
    for n in range(1, 9):
        a, b = 4*n+5, 4*n+2
        numerator = pmul([1]+[0]*(a-1)+[1], [1]+[0]*(b-1)+[1])
        q, rem = pdiv(numerator, pmul([1, 1], [1, 0, 1]))
        require(rem == [0], "Baker-Kegel polynomial division")
        require(all(x.denominator == 1 for x in q), "integral BK polynomial")
        q = [int(x) for x in q]
        derivative = [i*q[i] for i in range(1, len(q))]
        require(pgcd(q, derivative) == [1], "squarefree BK polynomial")
        require(len(q)-1 == 8*n+4 and peval(q, 1) == 1, "BK degree and normalization")
        require(abs(peval(q, -1)) == 4*n+5, "BK determinant")
        order = 2*a*b//gcd(a, b)
        # Avoid a huge dense polynomial: modular multiplication proves t^order=1 mod q.
        def modmul(x, y):
            return pdiv(pmul(x, y), q)[1]
        x, y, exponent = [0, 1], [1], order
        while exponent:
            if exponent & 1:
                y = modmul(y, x)
            x = modmul(x, x)
            exponent //= 2
        require(y == [1], "BK cyclotomic exponent")
        controls += 6
        bk.append({"n": n, "genus": 4*n+2, "determinant": 4*n+5,
                   "homological_order_divides": order,
                   "signature_defect_from_published_formula": 4*n})
    report["baker_kegel_family"] = bk

    # Star-shaped tree forms: exact Schur complement and determinant checks.
    tree_count = 0
    for a in range(1, 6):
        for b in range(a, 7):
            for c in range(b, 9):
                n, edges = star([a, b, c])
                q = tree_matrix(n, edges)
                s = F(1, a+1)+F(1, b+1)+F(1, c+1)-1
                require(determinant(q) == (a+1)*(b+1)*(c+1)*s, "tree Schur determinant")
                require(positive(q) == (s > 0), "tree Schur positivity")
                classified = (a == b == 1 or (a == 1 and b == 2 and c <= 4))
                require((s > 0) == classified, "bounded check of proved ADE classification")
                tree_count += 1
    controls += 3*tree_count
    n, edges = star([1, 1, 1, 1])
    require(mul(tree_matrix(n, edges), [[2], [1], [1], [1], [1]]) == zero(5, 1), "affine D4 null vector")
    controls += 1
    for length in range(1, 9):
        edges = [(i, i+1) for i in range(length)]
        for endpoint in [0, length]:
            for _ in range(2):
                index = max(max(e) for e in edges)+1
                edges.append((endpoint, index))
        n = length+5
        weights = [[2] for _ in range(length+1)]+[[1] for _ in range(4)]
        require(mul(tree_matrix(n, edges), weights) == zero(n, 1), "two branch vertices null vector")
        controls += 1
    report["ADE_tree_checks"] = {"star_cases": tree_count, "two_branch_null_models": 8,
                                 "degree_four_null_model": 1}

    slope_count = 0
    for b in range(3, 41):
        for a in range(1, (b+1)//2):
            c = F(a, b)
            if not 0 < c < F(1, 2):
                continue
            exceptions = [q for q in range(-5, 6) if abs(2*c-q) < 1]
            require(exceptions == [0, 1], "two exceptional filling slopes")
            slope_count += 1
    controls += slope_count
    report["FDTC_slope_arithmetic"] = {"rational_examples": slope_count,
                                      "residual_exceptional_q": [0, 1]}

    triangle_count = 0
    for d in [1, 3, 5, 9]:
        for r in [2, 4, 6, 10]:
            # A=F^d, B=F^(d+r), C=F^r; inclusion, projection, zero.
            f, g, h = zero(d+r, d), zero(r, d+r), zero(d, r)
            for i in range(d):
                f[i][i] = 1
            for i in range(r):
                g[i][d+i] = 1
            require(rank2(f)+rank2(g) == d+r, "triangle exact at B")
            require(rank2(g)+rank2(h) == r, "triangle exact at C")
            require(rank2(h)+rank2(f) == d, "triangle exact at A")
            require(mul(g, f) == zero(r, d) and mul(h, g) == zero(d, d+r)
                    and mul(f, h) == zero(d+r, r), "triangle zero composites")
            controls += 4
            triangle_count += 1
    report["abstract_exact_triangles"] = {"models": triangle_count, "manifold_realization": "NOT_ASSERTED"}

    spectral_count = 0
    for d in [1, 3, 5, 9]:
        for r in [1, 2, 3, 4]:
            n = d+2*r
            boundary = zero(n, n)
            for i in range(r):
                boundary[d+r+i][d+i] = 1
            require(mul(boundary, boundary) == zero(n, n), "spectral model differential")
            require(n-2*rank2(boundary) == d, "spectral model minimal terminal rank")
            require(all(boundary[i][0] == 0 for i in range(n)), "protected cycle")
            require(all(boundary[0][i] == 0 for i in range(n)), "protected cycle not boundary")
            controls += 4
            spectral_count += 1
    report["abstract_filtered_complexes"] = {"models": spectral_count,
        "E2_rank": "D+2r", "E3_rank": "D", "link_realization": "NOT_ASSERTED"}

    failures = 0
    for predicate, label in [(False, "false predicate"), (determinant([[2, -1], [-1, 2]]) == 4, "wrong determinant"),
                             (abs(2*F(1, 3)) >= 1, "invalid double-cover foliation threshold")]:
        try:
            require(predicate, label)
        except ValueError:
            failures += 1
    require(failures == 3, "negative controls trigger")
    report["positive_controls"] = controls
    report["negative_controls"] = failures
    report["result"] = "PASS"
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
