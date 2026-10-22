"""Authored exact-rational controls for the PR1156 closure/congruence audit.

These finite controls check algebraic identities and edge instances. They do not
compute general CP-rank or prove the universal theorem by enumeration.
"""
from fractions import Fraction as Q
import json


def demand(condition, label):
    if not condition:
        raise RuntimeError(label)


def transpose(a):
    return list(map(list, zip(*a)))


def matmul(a, b):
    bt = transpose(b)
    return [[sum((x*y for x, y in zip(row, col)), Q(0)) for col in bt] for row in a]


def gram(b):
    return matmul(b, transpose(b))


def identity(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def transform(n, t, sign):
    return [[Q(i == j) + sign*t for j in range(n)] for i in range(n)]


def rank(a):
    a = [row[:] for row in a]
    if not a:
        return 0
    rows, cols = len(a), len(a[0])
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        v = a[r][c]
        a[r] = [x/v for x in a[r]]
        for i in range(rows):
            if i != r and a[i][c]:
                v = a[i][c]
                a[i] = [x-v*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == rows:
            break
    return r


def nullvector(a):
    a = [row[:] for row in a]
    rows, cols = len(a), len(a[0])
    pivots = []
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        v = a[r][c]
        a[r] = [x/v for x in a[r]]
        for i in range(rows):
            if i != r and a[i][c]:
                v = a[i][c]
                a[i] = [x-v*y for x, y in zip(a[i], a[r])]
        pivots.append(c)
        r += 1
        if r == rows:
            break
    free = next((c for c in range(cols) if c not in pivots), None)
    demand(free is not None, 'dependence exists')
    v = [Q(0)]*cols
    v[free] = Q(1)
    for i, c in enumerate(pivots):
        v[c] = -a[i][free]
    return v


def strict(a):
    return all(x > 0 for row in a for x in row)


def flat_outer(v):
    return [v[i]*v[j] for i in range(len(v)) for j in range(i, len(v))]


def weighted_sum(vectors, weights):
    return [sum((w*x for w, x in zip(weights, xs)), Q(0))
            for xs in zip(*(flat_outer(v) for v in vectors))]


def reduce_conic(vectors):
    n = len(vectors[0])
    N = n*(n+1)//2
    vectors = [v[:] for v in vectors]
    weights = [Q(1)]*len(vectors)
    original = weighted_sum(vectors, weights)
    steps = 0
    while len(vectors) > N:
        c = nullvector(transpose([flat_outer(v) for v in vectors]))
        if not any(x > 0 for x in c):
            c = [-x for x in c]
        t = min(w/x for w, x in zip(weights, c) if x > 0)
        new_weights = [w-t*x for w, x in zip(weights, c)]
        demand(all(w >= 0 for w in new_weights), 'weights remain nonnegative')
        kept = [(v, w) for v, w in zip(vectors, new_weights) if w]
        demand(len(kept) < len(vectors), 'at least one column removed')
        vectors = [v for v, w in kept]
        weights = [w for v, w in kept]
        demand(weighted_sum(vectors, weights) == original, 'conic identity preserved')
        demand(strict(vectors), 'retained vectors strictly positive')
        steps += 1
    return len(vectors), steps


def main():
    records = []
    for n in range(1, 7):
        t = Q(1, 2*n)
        T = transform(n, t, -1)
        Tinv = transform(n, t/(1-n*t), 1)
        demand(matmul(T, Tinv) == identity(n), 'inverse formula')
        demand(strict(Tinv), 'inverse entrywise positive')
        for j in range(n):
            d = [[Q(i == j)] for i in range(n)]
            demand(strict(matmul(Tinv, d)), 'inverse positive on nonzero nonnegative vectors')
        records.append({'check':'inverse_formula_and_basis_vectors', 'n':n, 'status':'pass'})

    # Includes n=1, rank one with zero rows, full rank, and singular rank two.
    factors = [
        [[Q(3)]],
        [[Q(1)], [Q(0)], [Q(0)]],
        [[Q(1), Q(0)], [Q(0), Q(1)]],
        [[Q(1), Q(0)], [Q(0), Q(1)], [Q(1), Q(1)], [Q(2), Q(1)]],
    ]
    for b in factors:
        n, p = len(b), len(b[0])
        demand(rank(b) == p, 'rank-certified minimal factor')
        t = Q(1, 100)
        S = transform(n, t, 1)
        sb = matmul(S, b)
        demand(strict(sb), 'positive congruence makes every nonzero column positive')
        demand(rank(gram(sb)) == p, 'positive congruence preserves rank')
        demand(gram(sb) == matmul(matmul(S, gram(b)), transpose(S)), 'positive congruence Gram identity')
        records.append({'check':'positive_congruence_rank_certified_cp_and_cp_plus', 'n':n, 'rank':p, 'status':'pass'})

    b = [[Q(1), Q(2)], [Q(2), Q(1)], [Q(3), Q(4)], [Q(5), Q(2)]]
    n = len(b)
    sums = [sum(col, Q(0)) for col in transpose(b)]
    alpha = min(b[i][j]/sums[j] for i in range(n) for j in range(len(sums)))
    t = alpha/2
    demand(t < Q(1,n), 'explicit safe parameter below invertibility threshold')
    T, Tinv = transform(n,t,-1), transform(n,t/(1-n*t),1)
    tb = matmul(T,b)
    demand(strict(tb), 'negative congruence strictly positive factor')
    demand(all(tb[i][j] >= b[i][j]/2 for i in range(n) for j in range(len(sums))), 'half-entry margin')
    demand(matmul(Tinv,tb) == b, 'negative congruence exact pullback')
    demand(rank(gram(tb)) == rank(gram(b)) == 2, 'singular rank preservation')
    demand(gram(tb) == matmul(matmul(T,gram(b)),transpose(T)), 'negative congruence Gram identity')
    records.append({'check':'negative_congruence_singular_rank_two', 'alpha':str(alpha), 't':str(t), 'status':'pass'})

    for vectors in [
        [[Q(1),Q(2)]]*7,
        [[Q(1),Q(1)],[Q(1),Q(2)],[Q(2),Q(1)],[Q(2),Q(3)],[Q(3),Q(2)],[Q(3),Q(4)],[Q(4),Q(3)]],
        [[Q(i+j+1) for i in range(3)] for j in range(10)],
    ]:
        final, steps = reduce_conic(vectors)
        records.append({'check':'strict_conic_reduction', 'n':len(vectors[0]), 'input_columns':len(vectors), 'retained_columns':final, 'steps':steps, 'status':'pass'})

    # Duplicate a row: the left inverse obtained by restricting original rows
    # proves equality of both factor ranks in the general argument.
    b = [[Q(1),Q(2)], [Q(2),Q(1)]]
    ext = b+[b[0][:]]
    demand(gram(ext)[:2] != gram(b), 'dimensions differ as intended')
    demand([row[:2] for row in gram(ext)[:2]] == gram(b), 'principal restriction recovers original Gram matrix')
    demand(rank(gram(ext)) == rank(gram(b)), 'duplication preserves ordinary rank')
    records.append({'check':'row_duplication_gram_restriction', 'status':'pass'})

    # A single t independent of B is invalid; the candidate does not claim it.
    t, eps = Q(1,10), Q(1,100)
    bad = matmul(transform(2,t,-1), [[eps],[Q(1)]])
    demand(bad[0][0] < 0, 'universal negative parameter would fail')
    records.append({'check':'unsafe_uniform_parameter_countercontrol', 't':str(t), 'epsilon':str(eps), 'negative_entry':str(bad[0][0]), 'status':'pass'})

    # Rank can decrease in a limit and CP-plus-finiteness need not be closed.
    # For every eps>0 this is a strictly positive rank-one factor; its limit
    # has a zero diagonal entry and hence cannot have a positive factor.
    for k in [1,2,10,100]:
        eps = Q(1,k)
        f = [[Q(1)],[eps]]
        demand(strict(f) and rank(gram(f)) == 1, 'positive rank one before limit')
    limit = [[Q(1),Q(0)],[Q(0),Q(0)]]
    demand(limit[1][1] == 0 and rank(limit) == 1, 'rank-one finite-domain nonclosed limit')
    for k in [1,2,10,100]:
        d = [[Q(1),Q(0)],[Q(0),Q(1,k)]]
        demand(rank(d) == 2, 'exact rank stratum before rank-dropping limit')
    records.append({'check':'nonclosed_strata_and_positive_factor_domain_controls', 'status':'pass'})
    print(json.dumps({'arithmetic':'fractions.Fraction exact rationals','records':records,'count':len(records),'status':'pass'},sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
