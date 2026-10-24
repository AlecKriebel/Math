"""Second-review stress tests using concrete UT4 coefficient matrices.

Written for this review; does not import any packaged evaluator.
Finite checks supplement the independently reconstructed universal proof.
"""
from itertools import permutations
from pathlib import Path
import json
import random


def check(q):
    # q=4 is F2[t]/(t^2+t+1); other q are prime fields.
    def add(x, y):
        return x ^ y if q == 4 else (x + y) % q

    def neg(x):
        return x if q == 4 else -x % q

    def mul(x, y):
        if q != 4:
            return x * y % q
        z = 0
        while y:
            if y & 1:
                z ^= x
            x <<= 1
            if x & 4:
                x ^= 7
            y >>= 1
        return z

    def eye(n):
        return [[int(i == j) for j in range(n)] for i in range(n)]

    def mm(a, b):
        c = [[0] * len(b[0]) for _ in a]
        for i in range(len(a)):
            for k, x in enumerate(a[i]):
                if x:
                    for j, y in enumerate(b[k]):
                        if y:
                            c[i][j] = add(c[i][j], mul(x, y))
        return c

    def chain(*xs):
        ans = eye(len(xs[0]))
        for x in xs:
            ans = mm(ans, x)
        return ans

    def inverse_unit(u):
        a = [[add(u[i][j], neg(int(i == j))) for j in range(4)] for i in range(4)]
        ans, power = eye(4), eye(4)
        for k in range(1, 4):
            power = mm(power, a)
            ans = [[add(ans[i][j], neg(power[i][j]) if k % 2 else power[i][j])
                    for j in range(4)] for i in range(4)]
        assert chain(u, ans) == chain(ans, u) == eye(4)
        return ans

    def diagonal(*xs):
        out = [[0] * 12 for _ in range(12)]
        for block, x in enumerate(xs):
            for i in range(4):
                for j in range(4):
                    out[4 * block + i][4 * block + j] = x[i][j]
        return out

    def elementary(i, j, x):
        out = eye(12)
        for r in range(4):
            for s in range(4):
                out[4 * i + r][4 * j + s] = x[r][s]
        return out

    def negative(a):
        return [[neg(x) for x in row] for row in a]

    rng = random.Random(2113102 + q)
    one = eye(4)
    cases = 0
    for _ in range(24):
        u = [[rng.randrange(q) if i < j else int(i == j) for j in range(4)] for i in range(4)]
        v = [[rng.randrange(q) if i < j else int(i == j) for j in range(4)] for i in range(4)]
        ui, vi, uv = inverse_unit(u), inverse_unit(v), mm(u, v)
        d = lambda w: diagonal(w, inverse_unit(w), one)
        factor = chain(elementary(0, 1, u), elementary(1, 0, negative(ui)),
                       elementary(0, 1, u), elementary(0, 1, negative(one)),
                       elementary(1, 0, one), elementary(0, 1, negative(one)))
        assert factor == d(u)
        assert chain(d(u), d(v), diagonal(inverse_unit(uv), uv, one)) == diagonal(one, chain(ui, vi, u, v), one)
        assert chain(diagonal(one, u, one), diagonal(one, v, one)) == diagonal(one, uv, one)
        cases += 3
    x, y = [[0] * 4 for _ in range(4)], [[0] * 4 for _ in range(4)]
    x[0][1], y[1][2] = 1, 1
    assert mm(x, y) != mm(y, x)
    for i, j, k in permutations(range(3)):
        assert chain(elementary(i, k, x), elementary(k, j, y),
                     elementary(i, k, negative(x)), elementary(k, j, negative(y))) == elementary(i, j, mm(x, y))
        cases += 1
    u = [[add(one[i][j], x[i][j]) for j in range(4)] for i in range(4)]
    v = [[add(one[i][j], y[i][j]) for j in range(4)] for i in range(4)]
    assert chain(d(u), d(v)) != d(mm(u, v))
    return {"field_order": q, "named_comparisons": cases,
            "noncommutative_negative_control": True,
            "incorrect_D_homomorphism_rejected": True}


if __name__ == "__main__":
    data = {"method": "concrete 12x12 matrices with noncommutative UT4 coefficient blocks",
            "results": [check(q) for q in (2, 3, 4, 5, 7, 11)],
            "scope": "finite supplemental falsification only; no universal proof certification"}
    Path(__file__).with_suffix('.json').write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps(data, indent=2))
