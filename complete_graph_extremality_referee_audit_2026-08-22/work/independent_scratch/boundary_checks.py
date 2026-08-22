"""Exact-rational endpoint and zero-support checks, independent of package code."""

from fractions import Fraction
from itertools import combinations
import sympy as sp


def fixation(weights, fitness):
    n = len(weights)
    transient = [frozenset(S) for k in range(1, n) for S in combinations(range(n), k)]
    index = {S: z for z, S in enumerate(transient)}
    Q = sp.zeros(len(transient))
    b = sp.zeros(len(transient), 1)
    r = sp.Rational(fitness.numerator, fitness.denominator)
    for S in transient:
        row = index[S]
        for target in range(n):
            mutant = sum(weights[u][target] for u in S if u != target)
            resident = sum(weights[u][target] for u in range(n) if u not in S and u != target)
            pm = r * mutant / (r * mutant + resident)
            for becomes_mutant, probability in ((True, pm), (False, 1-pm)):
                new = set(S)
                if becomes_mutant:
                    new.add(target)
                else:
                    new.discard(target)
                new = frozenset(new)
                probability /= n
                if len(new) == n:
                    b[row] += probability
                elif len(new) != 0:
                    Q[row, index[new]] += probability
    h = (sp.eye(len(transient))-Q).inv() * b
    return sp.cancel(sum(h[index[frozenset((i,))]] for i in range(n))/n)


def baseline(n, r):
    r = sp.Rational(r.numerator, r.denominator)
    if r == 1:
        return sp.Rational(1, n)
    return sp.Rational(n-1, n) * (1-1/r)/(1-r**(-(n-1)))


def undirected_matrix(n, edge_weights):
    W = [[sp.Rational(0) for _ in range(n)] for _ in range(n)]
    for (i, j), value in edge_weights.items():
        W[i][j] = W[j][i] = sp.Rational(value)
    return W


# n=2: every admissible weighting is dynamically identical to J_2.
W2 = [[sp.Rational(0), sp.Rational(7)], [sp.Rational(5), sp.Rational(0)]]
for rv in (Fraction(1), Fraction(2), Fraction(10)):
    assert fixation(W2, rv) == sp.Rational(1, 2) == baseline(2, rv)

# One missing triangle edge (connected path) remains strictly below J_3 for r>1.
W_path = undirected_matrix(3, {(0, 1): 2, (0, 2): 3, (1, 2): 0})
assert fixation(W_path, Fraction(1)) == sp.Rational(1, 3)
assert fixation(W_path, Fraction(2)) < baseline(3, Fraction(2))

# G_13(0), G_22(0,3), and G_22(0,0) are connected zero-support boundaries.
W13_0 = undirected_matrix(4, {
    (0, 1): 1, (0, 2): 1, (0, 3): 1,
    (1, 2): 0, (1, 3): 0, (2, 3): 0,
})
W22_03 = undirected_matrix(4, {
    (0, 1): 0, (2, 3): 3,
    (0, 2): 1, (0, 3): 1, (1, 2): 1, (1, 3): 1,
})
W22_00 = undirected_matrix(4, {
    (0, 1): 0, (2, 3): 0,
    (0, 2): 1, (0, 3): 1, (1, 2): 1, (1, 3): 1,
})
for W in (W13_0, W22_03, W22_00):
    assert fixation(W, Fraction(1)) == sp.Rational(1, 4)
    assert fixation(W, Fraction(2)) < baseline(4, Fraction(2))

# A directed 3-cycle has one incoming parent at every target; fitness is
# dynamically irrelevant and the cited noncomplete-support conclusion holds.
W_cycle = [
    [sp.Rational(0), sp.Rational(1), sp.Rational(0)],
    [sp.Rational(0), sp.Rational(0), sp.Rational(1)],
    [sp.Rational(1), sp.Rational(0), sp.Rational(0)],
]
for rv in (Fraction(1), Fraction(2), Fraction(100)):
    assert fixation(W_cycle, rv) == sp.Rational(1, 3)
assert fixation(W_cycle, Fraction(2)) < baseline(3, Fraction(2))

# A nonsymmetric complete directed kernel is nondecreasing in fitness.
W_directed = [
    [sp.Rational(0), sp.Rational(2), sp.Rational(7)],
    [sp.Rational(5), sp.Rational(0), sp.Rational(3)],
    [sp.Rational(1), sp.Rational(11), sp.Rational(0)],
]
values = [fixation(W_directed, rv) for rv in
          (Fraction(1), Fraction(3, 2), Fraction(2), Fraction(10))]
assert values == sorted(values)

print("n2_all_positive_weightings_tie=PASS")
print("r1_uniform_average_endpoints=PASS")
print("zero_support_connected_boundaries=PASS")
print("directed_cycle_noncomplete_support=PASS")
print("directed_complete_monotonicity_spotcheck=PASS")

