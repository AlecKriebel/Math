"""CM/Hodge audit: exact finite checks, standard library only.

Independent construction uses 2x2 signed matrices on (a,b), then actual
embedding-to-prime fibers. It never imports any submitted checker.
"""
from fractions import Fraction as Q
from itertools import combinations
import json


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def mm(x, y):
    return tuple(sum(x[2*i+k]*y[2*k+j] for k in range(2))
                 for i in range(2) for j in range(2))


I = (1, 0, 0, 1)
# The columns are the coordinates of the images of a and b.
R = (0, -1, 1, 0)
S = (1, 0, 0, -1)
powers = [I]
for _ in range(3):
    powers.append(mm(powers[-1], R))
H = powers + [mm(x, S) for x in powers]
need(len(set(H)) == 8 and mm(R, R) == (-1, 0, 0, -1), 'root action')
G = [(x, z) for z in (0, 1) for x in H]


def prod(x, y):
    return (mm(x[0], y[0]), x[1] ^ y[1])


one = (I, 0)
inv = {x: next(y for y in G if prod(x, y) == one) for x in G}
f = (-1, -1, -1, 1, -1, 1, 1, -1)
Phi = {(h, int(f[j] < 0)) for j, h in enumerate(H)}
CM = [[Q(2*int(prod(inv[t], h) in Phi)-1) for h in G] for t in G]
MT = [[(x+1)/2 for x in row] for row in CM]


def rank(a):
    a = [list(map(Q, row)) for row in a]
    k = 0
    for j in range(len(a[0])):
        i = next((i for i in range(k, len(a)) if a[i][j]), None)
        if i is None:
            continue
        a[k], a[i] = a[i], a[k]
        pivot = a[k][j]
        a[k] = [x/pivot for x in a[k]]
        for i in range(k+1, len(a)):
            c = a[i][j]
            a[i] = [x-c*y for x, y in zip(a[i], a[k])]
        k += 1
        if k == len(a):
            break
    return k


def determinant(a):
    # Fraction-free Bareiss elimination, rather than the submitted rational routine.
    a = [list(map(int, row)) for row in a]
    sign, old = 1, 1
    for j in range(len(a)-1):
        i = next((i for i in range(j, len(a)) if a[i][j]), None)
        if i is None:
            return 0
        if i != j:
            a[i], a[j] = a[j], a[i]
            sign = -sign
        pivot = a[j][j]
        for i in range(j+1, len(a)):
            for k in range(j+1, len(a)):
                numerator = a[i][k]*pivot-a[i][j]*a[j][k]
                need(numerator % old == 0, 'Bareiss exact division')
                a[i][k] = numerator//old
        for i in range(j+1, len(a)):
            a[i][j] = 0
        old = pivot
    return sign*a[-1][-1]


def local_data(D):
    def place(g):
        return frozenset(prod(g, d) for d in D)
    places = list(dict.fromkeys(place(g) for g in G))
    reps = [next(g for g in G if place(g) == v) for v in places]
    fibers = {v: [sigma for sigma in G if place(inv[sigma]) == v] for v in places}
    need(all(len(fiber) == len(D) for fiber in fibers.values()), 'local fiber size')
    base = {v: Q(sum(sigma in Phi for sigma in fiber), len(fiber))
            for v, fiber in fibers.items()}
    slopes = [[base[place(prod(inv[h], t))] for h in G] for t in reps]
    return slopes


slopes = local_data({one, (S, 0)})
center = [[2*x-1 for x in row] for row in slopes]
columns = list(zip(*center))
need(rank(CM) == 8 and rank(MT) == 9, 'CM/Hodge orbit ranks')
need(determinant([row[:8] for row in CM[:8]]) == 256, 'Hodge determinant')
need(rank(center) == 4 and rank(slopes) == 5, 'Frobenius orbit ranks')
need(len(set(columns)) == 16 and all(any(v) for v in columns), 'embedding separation')
need(len(slopes) == 8, 'prime count')
need(all((2*x).denominator == 1 for row in slopes for x in row), 'local invariant integrality')


def is_tate(indices):
    return all(sum(row[j] for j in indices) == 0 for row in center)


pairs = [x for x in combinations(range(16), 2) if is_tate(x)]
need(pairs == [(j, j+8) for j in range(8)], 'only conjugate-pair divisors')
quartics = {x for x in combinations(range(16), 4) if is_tate(x)}
divisor_products = {tuple(sorted(x+y)) for x, y in combinations(pairs, 2)}
extra = sorted(quartics-divisor_products)
need(len(quartics) == 32 and len(divisor_products) == 28, 'quartic dimensions')
witness = (1, 3, 13, 15)
need(witness in quartics and witness not in divisor_products, 'explicit Tate obstruction')
need(any(sum(row[j] for j in witness) for row in CM), 'obstruction is not Hodge')
need(all(tuple(sorted(G.index(prod(t, G[j])) for j in x)) in extra
         for t in G for x in extra), 'exceptional span Galois stability')
# Boundary controls: trivial decomposition preserves the CM rank; a decomposition
# group containing central conjugation kills every centered slope and separation.
split = local_data({one})
all_c = local_data({one, (I, 1)})
need(rank([[2*x-1 for x in row] for row in split]) == 8, 'split-prime control')
need(rank([[2*x-1 for x in row] for row in all_c]) == 0, 'supersingular control')
need(len(set(zip(*all_c))) == 1, 'endomorphism-enlargement control')
print(json.dumps({
    'result': 'PASS', 'scope': 'finite arithmetic, not formalized geometry',
    'Hodge_centered_rank': 8, 'Mumford_Tate_dimension': 9,
    'Hodge_determinant': 256, 'Frobenius_centered_rank': 4,
    'Frobenius_torus_dimension': 5, 'distinct_embedding_columns': 16,
    'Tate_H2_dimension': len(pairs), 'Tate_H4_dimension': len(quartics),
    'Lefschetz_H4_dimension': len(divisor_products),
    'exceptional_quartics': extra,
    'slopes': {str(x): slopes[0].count(x) for x in sorted(set(slopes[0]))},
    'controls': {'complete_splitting_rank': 8, 'conjugation_decomposition_rank': 0}
}, sort_keys=True))
