"""Exact elementary controls for the source specialization, not a homology proof."""
from itertools import product
import json

counts = {}
def check(category, condition):
    assert condition, category
    counts[category] = counts.get(category, 0) + 1

def reduce_word(w):
    s = []
    for x in w:
        if s and s[-1] == -x:
            s.pop()
        else:
            s.append(x)
    return tuple(s)

def inverse(w):
    return tuple(-x for x in reversed(w))

def apply(images, w):
    out = []
    for x in w:
        v = images[abs(x)-1]
        out.extend(v if x > 0 else inverse(v))
    return reduce_word(out)

identity = tuple((i,) for i in range(1, 7))
automorphisms, inverses = [], []
for i in range(1, 5):
    for side, fixed in [('left', 5), ('right', 6)]:
        A, B = list(identity), list(identity)
        A[i-1] = (fixed, i) if side == 'left' else (i, fixed)
        B[i-1] = (-fixed, i) if side == 'left' else (i, -fixed)
        automorphisms.append(tuple(A))
        inverses.append(tuple(B))
for A, B in zip(automorphisms, inverses):
    for w in identity:
        check('inverse_on_free_basis', apply(A, apply(B, w)) == w)
        check('inverse_on_free_basis', apply(B, apply(A, w)) == w)
for A in automorphisms:
    for B in automorphisms:
        for w in identity:
            check('commutation_on_free_basis', apply(A, apply(B, w)) == apply(B, apply(A, w)))

# A column is the exponent-sum vector of the image of its basis element.
order = (5, 6, 1, 2, 3, 4)
def matrix(A):
    return [[sum((1 if v > 0 else -1) for v in A[col-1] if abs(v)==row)
             for col in order] for row in order]
I = [[int(i==j) for j in range(6)] for i in range(6)]
for index, A in enumerate(automorphisms):
    M = matrix(A)
    i, side = divmod(index, 2)
    expected = [r[:] for r in I]
    expected[side][i+2] = 1
    check('explicit_column_matrix', M == expected)
    check('fixed_rank_two_and_quotient', all(M[r][c] == I[r][c]
          for r in range(6) for c in range(6) if not(r < 2 and c >= 2)))

# An independently recovered upper block reads all eight coordinates back.
seen = set()
for exponents in product((-1,0,1), repeat=8):
    A = list(identity)
    def power(g, n):
        return (g if n >= 0 else -g,) * abs(n)
    for i in range(4):
        A[i] = power(5, exponents[2*i]) + (i+1,) + power(6, exponents[2*i+1])
    M = matrix(A)
    block = tuple(M[side][i+2] for i in range(4) for side in range(2))
    check('coordinate_recovery', block == exponents)
    check('sampled_injectivity', block not in seen)
    seen.add(block)

nu = lambda n: n*(n-1)//2
for a in range(1,33):
    for b in range(1,33):
        check('dimension_identity', nu(a+b)-nu(a)-nu(b) == a*b)
        check('primitive_degree_gap', nu(a)+nu(b) < nu(a+b))
        if a == b:
            check('equal_block_sign', ((nu(a)+a) % 2 == 0) == (a % 4 in (0,3)))
for det_a, det_b in product((-1,1), repeat=2):
    check('unipotent_orientation_character', det_a**4 * det_b**2 == 1)
check('exact_target_parameters', (2+4,2*4,nu(6)-nu(2)-nu(4)) == (6,8,8))
check('steinberg_product_degree', (nu(2),nu(4),nu(6),nu(2)+nu(4)) == (1,6,15,7))
check('different_coproduct_summands', (2,4) != (4,2))
check('graded_swap_sign', (-1)**((nu(2)+2)*(nu(4)+4)) == 1)
check('first_class_cancellation', 1 + (-1)**((nu(2)+2)**2) == 0)
print(json.dumps({
    'status': 'PASS', 'exact_assertions': sum(counts.values()),
    'categories': counts,
    'scope': 'Finite free-group, matrix, dimension and parity controls only; the primary duality and homology theorems require mathematical review.',
    'sampled_coordinate_tuples': len(seen),
    'target': {'k':2,'rank':6,'homological_degree':8,'a':2,'b':4,'coefficients':'Q, trivial'},
}, indent=2, sort_keys=True))
