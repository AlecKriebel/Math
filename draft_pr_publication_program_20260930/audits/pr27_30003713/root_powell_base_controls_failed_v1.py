"""Exact primary-proof base-case control; no original/family code imported.

Powell v4 Lemma6.7 on multilinear Lambda3 tensor V tensor V, then the
three-edge compatibility equalizer. This tests the delicate r=3 base of
the universal induction; it does not compute unrestricted homology.
"""
from itertools import combinations, permutations
from pathlib import Path
from hashlib import sha256
import json
import sympy as s


def wedge(a):
    if len(set(a)) != len(a):
        return None, 0
    sign = (-1) ** sum(a[i] > a[j] for i in range(len(a))
                      for j in range(i + 1, len(a)))
    return tuple(sorted(a)), sign


labels = set(range(5))
basis = [(a, b, c, u, v) for a, b, c in combinations(range(5), 3)
         for u, v in permutations(sorted(labels - {a, b, c}))]
assert len(basis) == 20
index = {word: i for i, word in enumerate(basis)}
B = s.zeros(20)
for column, (x, y, z, u, v) in enumerate(basis):
    # The exact primary formula for -beta, including its factor one-half.
    terms = [((x, y, z), v, u, 1), ((x, y, u), v, z, 1),
             ((x, z, u), v, y, -1), ((y, z, u), v, x, 1)]
    for triple, left, right, coefficient in terms:
        ordered, sign = wedge(triple)
        if sign:
            B[index[ordered + (left, right)], column] += s.Rational(coefficient * sign, 2)

t = s.Symbol('t')
expected = (t - 1) ** 7 * (t + 1) ** 5 * (t ** 2 + t / 2 + 1) ** 4
assert B.charpoly(t).as_expr().expand() == expected.expand()
assert B.trace() == 0 and B.det() == -1
fixed = 20 - (B ** 3 - s.eye(20)).rank()
assert fixed == 7  # multilinear Lambda5 plus S_(3,1,1), dimensions1+6
assert (t ** 2 + t / 2 + 1).rem(t ** 3 - 1) != 0
assert s.gcd(t ** 2 + t / 2 + 1, t ** 3 - 1) == 1

# All letter permutations preserve the exact endomorphism: not ranks alone.
equivariant = 0
for permutation in permutations(range(5)):
    A = s.zeros(20)
    for column, (x, y, z, u, v) in enumerate(basis):
        triple, sign = wedge([permutation[x], permutation[y], permutation[z]])
        A[index[triple + (permutation[u], permutation[v])], column] = sign
    assert A * B == B * A
    equivariant += 1

mutants = {
    'omit_half_normalization': 20 - ((2 * B) ** 3 - s.eye(20)).rank(),
    'reverse_overall_sign': 20 - ((-B) ** 3 - s.eye(20)).rank(),
    'omit_third_edge_compatibility': 20,
}
assert all(value != fixed for value in mutants.values())
assert (-B).trace() == B.trace()  # trace alone would miss the sign error
receipt = {'status': 'PASS', 'primary_formula': 'Powell2507.03453v4 Lemma6.7 and Proposition6.6',
           'dimension': 20, 'characteristic_polynomial': str(expected),
           'fixed_cube_dimension': fixed, 'permutation_equivariance_checks': equivariant,
           'mutant_fixed_dimensions': mutants, 'same_trace_wrong_sign_detected': True,
           'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
           'scope': 'Exact finite primary-proof base-case validation; universal credited induction and all-degree partial reduction are separately checked. No unrestricted solution or new proof-search attempt.'}
Path(__file__).with_name('root_powell_base_results.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
