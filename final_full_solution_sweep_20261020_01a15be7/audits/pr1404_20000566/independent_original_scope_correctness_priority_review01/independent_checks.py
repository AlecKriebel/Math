"""Independent exact rational witnesses and boundary controls; no third-party imports."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def outer(u, v):
    return [[a*b for b in v] for a in u]


def identity(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def combine(a, b, x=F(1), y=F(1)):
    return [[x*av+y*bv for av, bv in zip(ar, br)] for ar, br in zip(a, b)]


def multiply(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def block(a, b, cross):
    return [x+y for x, y in zip(a, cross)] + [list(x)+y for x, y in zip(zip(*cross), b)]


def principal(a, indices):
    return [[a[i][j] for j in indices] for i in indices]


def rank(a):
    a = [list(row) for row in a]
    if not a:
        return 0
    r = 0
    for col in range(len(a[0])):
        candidates = [i for i in range(r, len(a)) if a[i][col]]
        if not candidates:
            continue
        k = candidates[0]
        a[r], a[k] = a[k], a[r]
        pivot = a[r][col]
        a[r] = [v/pivot for v in a[r]]
        for i in range(r+1, len(a)):
            pivot = a[i][col]
            a[i] = [x-pivot*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def subsets(n):
    for size in range(n+1):
        yield from combinations(range(n), size)


def ceil(a):
    return -((-a.numerator)//a.denominator)


def prefix(q, r, weak=False):
    q = sorted(q)
    return all((sum(q[:k*r+1]) >= k if weak else sum(q[:k*r+1]) > k)
               for k in range((len(q)-1)//r+1))


def all_subsets(q, r):
    return all(len(j) <= r*ceil(sum((q[i] for i in j), F(0)))
               for j in subsets(len(q)))


def certify_projection(q):
    n = len(q)
    require(q == [list(x) for x in zip(*q)], 'symmetry')
    require(multiply(q, q) == q, 'idempotence')
    diagonal = [q[i][i] for i in range(n)]
    require(all(0 <= x <= 1 for x in diagonal), 'diagonal admissibility')
    require(sum(diagonal) == rank(q), 'integer trace/rank')
    return diagonal


def fractional_witness(theta, cross_scalar, f):
    # A rational orthonormal pair: each coordinate is nonzero.
    u = [F(1, 3), F(2, 3), F(2, 3)]
    w = [F(2, 3), F(1, 3), F(-2, 3)]
    uu, ww, eye = outer(u, u), outer(w, w), identity(3)
    require(sum(v*v for v in u) == sum(v*v for v in w) == 1
            and sum(a*b for a, b in zip(u, w)) == 0, 'orthonormal pair')
    if f == 0:
        a, c = combine(uu, uu, theta, 0), combine(eye, uu, 1, -theta)
    elif f == 1:
        a, c = combine(ww, uu, 1, theta), combine(ww, uu, 1, 1-theta)
    else:
        a, c = combine(eye, uu, 1, -(1-theta)), combine(uu, uu, 1-theta, 0)
    require(cross_scalar*cross_scalar == theta*(1-theta), 'rank-one coupling')
    cross = combine(uu, uu, cross_scalar, 0)
    q = block(a, c, cross)
    diagonal = certify_projection(q)
    compression_rank = rank(principal(q, range(3)))
    require(compression_rank == ceil(sum(diagonal[:3])), 'minimum compression rank')
    return q, diagonal


def main():
    witnesses = []
    strict_bad = None
    equality_bad = None
    for theta, cross in [(F(0), F(0)), (F(9, 25), F(12, 25)),
                         (F(1, 2), F(1, 2)), (F(16, 25), F(12, 25)),
                         (F(1), F(0))]:
        for f in range(3):
            q, diagonal = fractional_witness(theta, cross, f)
            witnesses.append({'theta': str(theta), 'f': f,
                              'diagonal_q': list(map(str, diagonal)),
                              'rank': rank(q), 'compression_rank': rank(principal(q, range(3)))})
            if theta == F(9, 25) and f == 0:
                strict_bad = q, diagonal
            if theta == 1 and f == 0:
                equality_bad = q, diagonal
    require(strict_bad is not None and equality_bad is not None, 'selected witnesses')
    q, diagonal = strict_bad
    require(sum(diagonal[:3]) == F(9, 25) and rank(q) == 3
            and rank(principal(q, range(3))) == 1, 'strict-violation certificate')
    require(6 <= 2*rank(q) and all(0 < x < 1 for x in diagonal),
            'total-rank and max-diagonal elementary obstructions absent')
    failing_partitions = 0
    # Each unordered two-partition appears once, with coordinate0 in its first block.
    for j in subsets(6):
        if 0 not in j or len(j) == 6:
            continue
        other = tuple(i for i in range(6) if i not in j)
        require(rank(principal(q, j)) < len(j)
                or rank(principal(q, other)) < len(other), 'no strict two-paving')
        failing_partitions += 1
    require(failing_partitions == 31, 'all unordered nonempty two-partitions')
    # Equality must fail, while changing the strict prefix test to weak accepts it.
    eq = equality_bad[1]
    require(not prefix(eq, 2) and prefix(eq, 2, weak=True), 'strictness mutant')
    half = [F(1, 2)]*6
    require(prefix(half, 2), 'constant threshold equality is allowed')
    # Actual rational positive half-diagonal projection: three paired rank-one blocks.
    positive = [[F(i == j or (i+3) % 6 == j, 2) for j in range(6)] for i in range(6)]
    require(certify_projection(positive) == half, 'positive projection')
    require(rank(principal(positive, range(3))) == rank(principal(positive, range(3, 6))) == 3,
            'positive strict partition')
    test_diagonals = [half, diagonal, eq, [F(0)]*3, [F(1)]*3,
                      [F(1), F(0), F(1)], [F(1, 3)]*3,
                      [F(9, 10), F(1, 10)], [F(1, 3), F(2, 3)]]
    equivalences = 0
    majorizations = 0
    for target in test_diagonals:
        require(sum(target).denominator == 1, 'admissible total trace')
        n = len(target)
        for r in range(1, n+1):
            require(prefix(target, r) == all_subsets(target, r), 'subset/prefix equivalence')
            equivalences += 1
        for j in subsets(n):
            a = sum((target[i] for i in j), F(0))
            f = a.numerator//a.denominator
            theta = a-f
            spectrum = [F(1)]*f + ([theta] if theta else [])
            spectrum += [F(0)]*(len(j)-len(spectrum))
            desired = sorted((target[i] for i in j), reverse=True)
            require(len(spectrum) == len(j), 'spectrum dimension')
            require(sum(spectrum) == sum(desired), 'equal trace')
            require(all(sum(spectrum[:k]) >= sum(desired[:k]) for k in range(len(j)+1)),
                    'majorization at every partial sum')
            majorizations += 1
    require(not prefix([F(0)]*3, 3) and prefix([F(1)]*3, 1), 'zero/identity edge')
    result = {'status': 'PASS', 'exact_arithmetic': 'stdlib Fraction only',
              'rank_construction_witnesses': witnesses, 'subset_prefix_equivalences': equivalences,
              'majorization_subsets': majorizations, 'all_bad_two_partitions': failing_partitions,
              'strict_violation_bad_Q': [[str(x) for x in row] for row in q],
              'strict_violation_q': list(map(str, diagonal)),
              'strict_violation_trace_J': '9/25', 'strict_violation_rank_J': 1,
              'equality_mutant_rejected': True, 'half_threshold_positive': True,
              'scope': 'Selected constructive witnesses and exact boundary controls supplement the written general proof; no large numerical matrix, prescribed-gap, or complexity claim.'}
    Path(__file__).with_name('INDEPENDENT_CHECKS.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['status', 'subset_prefix_equivalences',
                                            'majorization_subsets', 'all_bad_two_partitions']}))


if __name__ == '__main__':
    main()
