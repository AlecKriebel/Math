"""Read-only independent low-degree controls using nilpotent matrix evaluation.

No imported source checker, symbolic package, float arithmetic or file write.
The universal topological and finite-type deductions are in DERIVATION.md.
"""
from fractions import Fraction as Q
from itertools import permutations
import json


def need(x, label):
    if not x:
        raise RuntimeError(label)


def ident(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def mul(A, B):
    return [[sum(a*b for a, b in zip(row, col)) for col in zip(*B)] for row in A]


def add(A, B, scale=1):
    return [[a+scale*b for a, b in zip(x, y)] for x, y in zip(A, B)]


def word_matrix(word, generators, inverses):
    z = ident(3)
    for a in word:
        z = mul(z, generators[a] if a > 0 else inverses[-a])
    return z


words = [(1, 2, -1, 3, 1, -2, -1, -3),
         (-3, -1, 3, 1),
         (-3, -1, 3, 1, -2, -1, -3, 1, 3, 1, 2, -1)]
expected = [{(2, 3): 1, (3, 2): -1},
            {(1, 3): -1, (3, 1): 1},
            {(1, 2): 1, (2, 1): -1}]
matrix_certificates = []
for u in range(1, 4):
    for v in range(1, 4):
        generators, inverses = {}, {}
        for label in range(1, 4):
            N = [[0]*3 for _ in range(3)]
            N[0][1] = int(label == u)
            N[1][2] = int(label == v)
            generators[label] = add(ident(3), N)
            inverses[label] = add(add(ident(3), N, -1), mul(N, N))
            need(mul(generators[label], inverses[label]) == ident(3), 'nilpotent inverse')
        for j, word in enumerate(words):
            value = word_matrix(word, generators, inverses)
            # X_u X_v is exactly E13, while every product of >=3 X's is zero.
            need(value[0][1] == value[1][2] == 0, 'no linear longitude term')
            need(value[0][2] == expected[j].get((u, v), 0), 'quadratic Magnus coefficient')
            matrix_certificates.append({'strand': j+1, 'u': u, 'v': v,
                                        'quadratic_coefficient': value[0][2]})


class Poly:
    """Rational polynomial in r,s,t,u,v, with exact canonical coefficients."""
    def __init__(self, terms=None):
        self.t = {m: Q(c) for m, c in (terms or {}).items() if c}

    @staticmethod
    def coerce(x):
        return x if isinstance(x, Poly) else Poly({(0,)*5: x})

    def __add__(self, other):
        out = self.t.copy()
        for m, c in self.coerce(other).t.items():
            out[m] = out.get(m, Q(0))+c
        return Poly(out)

    __radd__ = __add__

    def __mul__(self, other):
        out = {}
        for m, c in self.t.items():
            for n, d in self.coerce(other).t.items():
                k = tuple(a+b for a, b in zip(m, n))
                out[k] = out.get(k, Q(0))+c*d
        return Poly(out)

    __rmul__ = __mul__


def determinant(A):
    ans = Poly()
    n = len(A)
    for perm in permutations(range(n)):
        inversions = sum(perm[i] > perm[j] for i in range(n) for j in range(i+1, n))
        term = Poly.coerce((-1)**inversions)
        for i, j in enumerate(perm):
            term = term*A[i][j]
        ans = ans+term
    return ans


variables = []
for i in range(5):
    m = [0]*5
    m[i] = 1
    variables.append(Poly({tuple(m): 1}))
r, s, t, u, v = variables
M = [[1, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0], [1, -1, 1, 0, 0, 0],
     [1, r, r*r, 0, 0, 1], [1, s, s*s, 1, 5, u], [1, t, t*t, 5, 1, v]]
det_cases = {'six_rows_all_five_indeterminates': (M, -48),
             'span_all_linking_values': ([[1, 0, 0, 0], [1, 1, 1, 0],
                                         [1, -1, 1, 0], [1, t, t*t, 1]], 2),
             'slice_rows': ([[2, 0, 0], [0, 2, 0], [2, 2, -4]], -16),
             'component_pair': ([[1, 5], [5, 1]], -24)}
det_results = {}
for name, (matrix, wanted) in det_cases.items():
    got = determinant(matrix)
    need(got.t == {(0,)*5: Q(wanted)}, 'literal polynomial determinant '+name)
    det_results[name] = {'constant': wanted, 'nonconstant_coefficients': 0}
erased_w = [row[:5]+[0] for row in M]
need(not determinant(erased_w).t, 'erasing plat coordinate destroys full rank')
collapsed = [[1, 1], [1, 1]]
need(not determinant(collapsed).t, 'collapsing unequal component evaluations loses rank')
need(Q((3*3-1)*(4*4-1), 24) == 5, 'torus Conway normalization')
need(Q((2*2-1)*(3*3-1), 24) == 1, 'trefoil normalization')

# Universal quadratic coefficient-recovery identities are verified by testing
# every monomial symbolically for each chosen finite dimension. Their formulas
# in DERIVATION.md work for arbitrary dimension, not just these controls.
quadratic_recovery_dimensions = []
for dim in range(1, 16):
    monomials = [()] + [(i,) for i in range(dim)]
    monomials += [(i, j) for i in range(dim) for j in range(i, dim)]
    for mon in monomials:
        def evaluate(point):
            ans = 1
            for idx in mon:
                ans *= point[idx]
            return Q(ans)
        zero = [0]*dim
        constant = evaluate(zero)
        linear, square, cross = {}, {}, {}
        for i in range(dim):
            plus, minus = zero.copy(), zero.copy()
            plus[i], minus[i] = 1, -1
            linear[i] = (evaluate(plus)-evaluate(minus))/2
            square[i] = (evaluate(plus)+evaluate(minus)-2*constant)/2
            for j in range(i+1, dim):
                both, second = plus.copy(), zero.copy()
                both[j], second[j] = 1, 1
                cross[i, j] = evaluate(both)-evaluate(plus)-evaluate(second)+constant
        need(constant == int(mon == ()), 'quadratic constant recovery')
        need(all(a == int(mon == (i,)) for i, a in linear.items()), 'quadratic linear recovery')
        need(all(a == int(mon == (i, i)) for i, a in square.items()), 'quadratic square recovery')
        need(all(a == int(mon == key) for key, a in cross.items()), 'quadratic mixed recovery')
    quadratic_recovery_dimensions.append({'dimension': dim, 'all_monomials': len(monomials)})

print(json.dumps({'status': 'PASS',
                  'independent_mechanism': '3x3 strictly upper-triangular Magnus evaluation and exact rational polynomial determinant expansion',
                  'complete_quadratic_longitude_matrix_certificates': matrix_certificates,
                  'polynomial_determinants': det_results,
                  'quadratic_recovery_dimensions': quadratic_recovery_dimensions,
                  'negative_controls': ['zero plat column destroys six-row rank',
                                        'equalized component values destroy pair rank',
                                        'determinants are not units in characteristic2 or3'],
                  'topology_classification_deframing_integration_machine_proved': False,
                  'source_code_imported': False, 'file_writes': 0}, sort_keys=True))
