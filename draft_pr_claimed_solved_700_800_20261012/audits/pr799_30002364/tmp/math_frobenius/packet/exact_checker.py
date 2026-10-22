"""Independent arithmetic certificate: actual root substitutions and F_25 residues.

No candidate modules, matrices, cached results, or external packages are imported.
The output is a finite certificate; the geometry is reviewed in REPORT.md.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations
import json


def need(p, message):
    if not p:
        raise RuntimeError(message)


# A signed symbol 1 denotes a, 2 denotes b; the third coordinate is the i sign.
# Substitutions act on the concrete generators, not a supplied group table.
one = (1, 2, 1)
r = (2, -1, 1)
s = (1, -2, 1)
c = (1, 2, -1)


def image(g, symbol):
    return (1 if symbol > 0 else -1) * g[abs(symbol) - 1]


def compose(g, h):
    return (image(g, h[0]), image(g, h[1]), g[2] * h[2])


rot = [one]
for j in range(3):
    rot.append(compose(r, rot[-1]))
H = rot + [compose(g, s) for g in rot]
G = H + [compose(c, g) for g in H]
need(len(set(G)) == 16, '16 actual substitutions')
need(all(compose(g, h) in G for g in G for h in G), 'closure')
inverse = {g: next(h for h in G if compose(g, h) == one) for g in G}
need(compose(s, compose(r, s)) == inverse[r], 'root relation')
sign = [-1, -1, -1, 1, -1, 1, 1, -1]
Phi = {g if z == 1 else compose(c, g) for g, z in zip(H, sign)}
need(len(Phi) == 8 and all((g in Phi) != (compose(c, g) in Phi) for g in G),
     'CM type')


def rank(rows):
    a = [[Fraction(x) for x in row] for row in rows]
    j = 0
    for k in range(len(a[0])):
        t = next((t for t in range(j, len(a)) if a[t][k]), None)
        if t is None:
            continue
        a[j], a[t] = a[t], a[j]
        a[j] = [x / a[j][k] for x in a[j]]
        for i in range(len(a)):
            if i != j:
                q = a[i][k]
                a[i] = [x-q*y for x, y in zip(a[i], a[j])]
        j += 1
        if j == len(a):
            break
    return j


def det_expansion(rows):
    total = 0
    for p in permutations(range(len(rows))):
        inv = sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1, len(p)))
        t = (-1)**inv
        for i, j in enumerate(p):
            t *= rows[i][j]
        total += t
    return total


# Discriminant via the Sylvester resultant with the derivative, not a formula
# copied from the supplied checker. Degree four gives positive resultant sign.
F = [1, 0, -6, 0, 3]
dF = [4, 0, -12, 0]
sylvester = [[0]*j+F+[0]*(2-j) for j in range(3)]
sylvester += [[0]*j+dF+[0]*(3-j) for j in range(4)]
need(det_expansion(sylvester) == 27648, 'quartic discriminant')
need(all(z % 3 == 0 for z in F[1:]) and F[-1] % 9 != 0, 'Eisenstein at three')
product = [1, 0, -6, 0, 8]
need(all((x-y) % 5 == 0 for x, y in zip(F, product)), 'mod five factors')


# Centered type cocharacters, constructed by left-translating the actual type.
hodge = [[1 if g in {compose(t, ph) for ph in Phi} else -1 for g in G]
         for t in G]
M = [row[:8] for row in hodge[:8]]
need(det_expansion(M) == 256 and rank(hodge) == 8, 'full Hodge rank')


# F_25 = F_5[u]/(u^2-2); elements are pairs, with exact modular arithmetic.
def mul(x, y):
    return ((x[0]*y[0]+2*x[1]*y[1]) % 5,
            (x[0]*y[1]+x[1]*y[0]) % 5)


def power(x, n):
    ans = (1, 0)
    for j in range(n):
        ans = mul(ans, x)
    return ans


def negative(x):
    return ((-x[0]) % 5, (-x[1]) % 5)


def evaluate(g, values):
    def ev(sym):
        x = values[abs(sym)-1]
        return x if sym > 0 else negative(x)
    return (ev(g[0]), ev(g[1]), values[2] if g[2] > 0 else negative(values[2]))


def prime(values):
    # A prime is a residue homomorphism modulo the Frobenius of F_25/F_5.
    return min(values, tuple(power(x, 5) for x in values))


P = ((2, 0), (0, 1), (2, 0))
need(power(P[1], 5) == negative(P[1]), 'local Frobenius')
need(mul(P[0], P[0]) == (4, 0) and mul(P[1], P[1]) == (2, 0), 'local roots')
need(mul(P[2], P[2]) == (4, 0), 'split i')
fibers = {g: prime(evaluate(g, P)) for g in G}
primes = sorted(set(fibers.values()))
need(len(primes) == 8 and set(Counter(fibers.values()).values()) == {2}, 'local degree two')
need({g for g in G if fibers[g] == prime(P)} == {one, s}, 'actual decomposition group')
local = {v: Fraction(sum(fibers[g] == v for g in Phi), 2) for v in primes}
# v(h(pi)) equals (h^-1 v)(pi); rho_v composed with h has that kernel.
slopes = [[local[prime(evaluate(h, v))] for h in G] for v in primes]
center = [[2*x-1 for x in row] for row in slopes]
need(rank(center) == 4 and rank(slopes) == 5, 'Frobenius ranks')
minor = [[2*center[primes.index(fibers[inverse[t]])][G.index(h)] for h in rot] for t in rot]
need(det_expansion(minor) == 80, 'ordered slope minor')
cols = [tuple(row[j] for row in center) for j in range(16)]
need(len(set(cols)) == 16 and all(any(x) for x in cols), 'all extension separation')
need(all(cols[i+8] == tuple(-x for x in cols[i]) for i in range(8)), 'CM complements')
need(all((2*x).denominator == 1 for row in slopes for x in row), 'Honda-Tate local invariants')
e = [0, 1, 0, 1, 0, -1, 0, -1]
need(all(sum(z*row[j] for j, z in enumerate(e)) == 0 for row in center), 'claimed Weil relation')
need(any(sum(z*row[j] for j, z in enumerate(e)) != 0 for row in hodge), 'not Hodge relation')
quartic = (1, 3, 13, 15)
need(all(sum(row[j] for j in quartic) == 0 for row in center), 'actual exterior Tate line')


def dimensions(rows):
    dims = []
    witnesses = []
    for k in range(0, 17, 2):
        basis = [q for q in combinations(range(16), k)
                 if all(sum(row[j] for j in q) == 0 for row in rows)]
        dims.append(len(basis))
        if k == 4:
            witnesses = [list(q) for q in basis
                         if not all((j in q) == (j+8 in q) for j in range(8))]
    return dims, witnesses


tate, exotic = dimensions(center)
hodge_dims, _ = dimensions(hodge)
lefschetz = [len(list(combinations(range(8), k))) for k in range(9)]
need(hodge_dims == lefschetz, 'Hodge monomials on A')
need(tate == [1, 8, 32, 80, 114, 80, 32, 8, 1], 'all exterior degrees')
need(len(exotic) == 4 and list(quartic) in exotic, 'codimension two obstruction')
divisors = [q for q in combinations(range(16), 2)
            if all(sum(row[j] for j in q) == 0 for row in center)]
need(divisors == [(j, j+8) for j in range(8)], 'full divisor list')

result = {
    'mechanism': 'root substitutions and F25 residue homomorphisms',
    'hodge_centered_rank': rank(hodge), 'hodge_determinant': det_expansion(M),
    'quartic_discriminant': det_expansion(sylvester), 'slope_minor_determinant': int(det_expansion(minor)),
    'slope_centered_rank': rank(center), 'slope_full_rank': rank(slopes),
    'geometric_prime_count': len(primes), 'local_degree': 2,
    'distinct_valuation_columns': len(set(cols)), 'divisor_pairs': [list(x) for x in divisors],
    'newton_slopes': {str(x): n for x, n in sorted(Counter(slopes[primes.index(prime(P))]).items())},
    'tate_dimensions_by_codimension': tate, 'lefschetz_dimensions_by_codimension': lefschetz,
    'nonlefschetz_quartic_labels': exotic,
    'honda_tate_local_invariants_integral': True,
    'formal_geometric_proof': False,
}
print(json.dumps(result, sort_keys=True, indent=2))
