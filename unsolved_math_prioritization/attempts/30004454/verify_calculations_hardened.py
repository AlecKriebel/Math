# Original-preserving correction: executable checks survive -O/-OO.
"""Exact arithmetic checks accompanying the authored Coxeter quotient audit.

These finite checks do not replace the universal proofs in the Markdown files.
Run with Python 3; no third-party packages and no network access are required.
"""

def require(condition, message):
    if not condition:
        raise RuntimeError(message)
from fractions import Fraction
from math import gcd

def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b)))) for j in range(len(b[0]))] for i in range(len(a))]

def transpose(a):
    return [list(r) for r in zip(*a)]

def mv(a, v):
    return [sum((x * y for x, y in zip(row, v))) for row in a]

def bilinear(a, v, w):
    return sum((x * y for x, y in zip(v, mv(a, w))))

def test_reflection_obstruction():
    b = [[1, -1, -1], [-1, 1, -1], [-1, -1, 1]]
    s = [[-1, 2, 2], [0, 1, 0], [0, 0, 1]]
    t = [[1, 0, 0], [2, -1, 2], [0, 0, 1]]
    ident = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    require(mm(s, s) == ident and mm(t, t) == ident, 'Failed original check at line 32')
    require(mm(mm(transpose(s), b), s) == b, 'Failed original check at line 33')
    require(mm(mm(transpose(t), b), t) == b, 'Failed original check at line 34')
    a = mm(s, t)
    require(a == [[3, -2, 6], [2, -1, 2], [0, 0, 1]], 'Failed original check at line 36')
    v = [0, 0, 1]
    for n in range(101):
        require(v == [2 * n * (2 * n + 1), 2 * n * (2 * n - 1), 1], 'Failed original check at line 39')
        require(bilinear(b, v, v) == 1, 'Failed original check at line 40')
        require(bilinear(b, [0, 1, 0], v) == -4 * n - 1, 'Failed original check at line 41')
        if n:
            require(abs(bilinear(b, [0, 1, 0], v)) != 1, 'Failed original check at line 43')
        v = mv(a, v)

def test_triangle_quotient_example():
    edges = {(0, 1): 3, (1, 2): 6, (2, 3): 9, (3, 4): 12, (0, 4): 15}
    parts = [0, 0, 0, 1, 2]
    d = 3
    require(all((m % d == 0 for m in edges.values())), 'Failed original check at line 52')
    quot = {}
    for (i, j), m in edges.items():
        a, b = sorted((parts[i], parts[j]))
        if a != b:
            quot[a, b] = gcd(quot.get((a, b), 0), d)
    require(quot == {(0, 1): 3, (1, 2): 3, (0, 2): 3}, 'Failed original check at line 58')
    require(sum((Fraction(1, m) for m in quot.values())) == 1, 'Failed original check at line 59')
if __name__ == '__main__':
    test_reflection_obstruction()
    test_triangle_quotient_example()
    print('PASS: exact reflection identities for n=0..100; triangle quotient presentation check.')
