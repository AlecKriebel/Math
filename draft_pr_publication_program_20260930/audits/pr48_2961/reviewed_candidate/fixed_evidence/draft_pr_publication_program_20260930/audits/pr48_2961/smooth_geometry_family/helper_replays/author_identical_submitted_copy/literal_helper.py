"""Exact finite diagnostics for the compression and cutoff formulas.

These checks do not prove Mather--Thurston perfectness, the smooth support
constructions, or unbounded commutator length for a four-manifold.
"""
from itertools import permutations, product
from pathlib import Path
import hashlib
import json
import random

assertions = 0


def check(condition):
    global assertions
    assertions += 1
    assert condition


def compose(p, q):
    """p after q."""
    return tuple(p[q[i]] for i in range(len(p)))


def inverse(p):
    q = [0] * len(p)
    for i, j in enumerate(p):
        q[j] = i
    return tuple(q)


def multiply(values, degree):
    r = tuple(range(degree))
    for value in values:
        r = compose(r, value)
    return r


def commutator(p, q):
    return multiply([p, q, inverse(p), inverse(q)], len(p))


def power(p, n):
    return multiply([p] * n, len(p))


def conjugate(p, q):
    return multiply([p, q, inverse(p)], len(p))


def block_permutation(p, block, number):
    width = len(p)
    q = list(range(width * number))
    for i in range(width):
        q[block * width + i] = block * width + p[i]
    return tuple(q)


def verify_compression(pairs):
    m, width = len(pairs), len(pairs[0][0])
    degree = width * (m + 1)
    one = tuple(range(degree))
    shift = tuple(((i // width + 1) % (m + 1)) * width + i % width
                  for i in range(degree))
    factors = [(block_permutation(a, 0, m + 1), block_permutation(b, 0, m + 1))
               for a, b in pairs]
    cs = [commutator(a, b) for a, b in factors]
    h = multiply(cs, degree)
    T = lambda value, exponent: conjugate(power(shift, exponent), value)
    A = multiply([T(a, i + 1) for i, (a, b) in enumerate(factors)], degree)
    B = multiply([T(b, i + 1) for i, (a, b) in enumerate(factors)], degree)
    suffixes = [multiply(cs[i:], degree) for i in range(m)]
    C = multiply([T(suffix, i) for i, suffix in enumerate(suffixes)], degree)
    K = multiply([T(c, i + 1) for i, c in enumerate(cs)], degree)
    check(commutator(A, B) == K)
    check(commutator(C, shift) == compose(h, inverse(K)))
    check(compose(commutator(C, shift), commutator(A, B)) == h)
    # The product can be nontrivial, and within-block factors are not assumed to commute.
    return any(commutator(a, b) != one for a, b in factors)


S3 = list(permutations(range(3)))
exhaustive_cases = 0
for a, b in product(S3, repeat=2):
    verify_compression([(a, b)])
    exhaustive_cases += 1
for a, b, c, d in product(S3, repeat=4):
    verify_compression([(a, b), (c, d)])
    exhaustive_cases += 1

# Random S5 factors permit genuinely noncommuting commutators, testing word order.
rng = random.Random(485)
S5 = list(permutations(range(5)))
sampled_cases = 0
noncommuting_commutator_controls = 0
for m in range(1, 8):
    for _ in range(70):
        pairs = [(rng.choice(S5), rng.choice(S5)) for _ in range(m)]
        verify_compression(pairs)
        if m >= 2:
            c1, c2 = (commutator(*pairs[i]) for i in [0, 1])
            if compose(c1, c2) != compose(c2, c1):
                noncommuting_commutator_controls += 1
        sampled_cases += 1
check(noncommuting_commutator_controls > 0)

# Pointwise endpoint factorization does not require f_t to be a one-parameter group.
cutoff_cases = 0
one5 = tuple(range(5))
for _ in range(100):
    family = [one5] + [rng.choice(S5) for _ in range(8)]
    final = family[-1]
    for middle in family:
        a = middle
        b = compose(final, inverse(middle))
        check(compose(b, a) == final)
        cutoff_cases += 1
    check(family[0] == one5)
    check(compose(final, inverse(final)) == one5)

# Exact differential calculation for the point-dependent-time counterexample.
w = (0, 1, 0)
v = (-1, 0, 0)
rotation_field = (-w[1], w[0], 0)
gradient_tau = (w[1], w[0], 0)
directional = sum(a * b for a, b in zip(gradient_tau, v))
check(directional == -1)
check(v != (0, 0, 0))
check(tuple(v[i] + directional * rotation_field[i] for i in range(3)) == (0, 0, 0))

root = Path(__file__).resolve().parent
result = {
    "all_passed": True,
    "assertions": assertions,
    "exhaustive_S3_wreath_cases": exhaustive_cases,
    "sampled_S5_wreath_cases": sampled_cases,
    "maximum_number_of_input_commutators": 7,
    "noncommuting_commutator_controls": noncommuting_commutator_controls,
    "pointwise_cutoff_factorizations": cutoff_cases,
    "singular_time_cutoff_differential_checked": True,
    "arithmetic": "exact permutations and integer tangent vectors",
    "partial_sha256": hashlib.sha256((root / "PARTIAL.md").read_bytes()).hexdigest(),
    "scope": "Finite algebra and derivative diagnostics only; KP-4.85 remains unresolved.",
}
(root / "check_results.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
