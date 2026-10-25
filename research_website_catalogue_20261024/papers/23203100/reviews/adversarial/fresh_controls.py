"""Independent exact controls for the capacity/secrecy reduction.

Only standard-library imports. Does not import or execute any submitted code.
The universal reasoning is in FRESH_PROOFS.md; finite tests are regression and
mutation checks, not a substitute for that reasoning or a proof of EPnI.
"""
from fractions import Fraction as Q
from itertools import product
import json
import random


def entropy_symbol(mask):
    return {mask: Q(1)} if mask else {}


def linear(*parts):
    answer = {}
    for coefficient, part in parts:
        for mask, value in part.items():
            answer[mask] = answer.get(mask, Q(0)) + coefficient * value
    return {mask: value for mask, value in answer.items() if value}


def mutual(a, b, given=0):
    return linear((1, entropy_symbol(a | given)),
                  (1, entropy_symbol(b | given)),
                  (-1, entropy_symbol(given)),
                  (-1, entropy_symbol(a | b | given)))


W, V, B, E, X, K, L = (1 << j for j in range(7))


second_residual = linear(
    (1, mutual(W, B | V, X)), (-1, mutual(W, E, X)),
    (-1, mutual(W | V, B, X)), (1, mutual(W | V, E, X)),
    (-1, mutual(W, V, X)), (1, mutual(V, B, X)),
    (-1, mutual(V, E, W | X)))
third_residual = linear(
    (1, mutual(K | W, B | L | V)), (-1, mutual(W, E, K | L)),
    (-1, mutual(K | L | W | V, B)),
    (1, mutual(W | V, E, K | L)), (1, mutual(L | V, B)),
    (-1, mutual(K | W, L | V)), (-1, mutual(V, E, K | W | L)))
assert second_residual == third_residual == {}


def gf2_rank(rows):
    basis = {}
    for row in rows:
        while row:
            pivot = row.bit_length() - 1
            if pivot in basis:
                row ^= basis[pivot]
            else:
                basis[pivot] = row
                break
    return len(basis)


def evaluate(expression, variables):
    total = Q(0)
    for mask, coefficient in expression.items():
        rows = [row for bit, data in variables.items() if mask & bit for row in data]
        total += coefficient * gf2_rank(rows)
    return total


rng = random.Random(23203100)
classical_trials = 10000
for _ in range(classical_trials):
    variables = {bit: [rng.randrange(16) for __ in range(rng.randrange(4))]
                 for bit in (W, V, B, E, X, K, L)}
    second_remainder = linear((1, mutual(W, V, X)),
                              (-1, mutual(V, B, X)),
                              (1, mutual(V, E, W | X)),
                              (-1, entropy_symbol(V | X)),
                              (1, entropy_symbol(X)))
    assert evaluate(second_remainder, variables) <= 0
    third_remainder = linear((1, mutual(K | W, L | V)),
                             (1, mutual(V, E, K | W | L)),
                             (-1, entropy_symbol(L)),
                             (-1, entropy_symbol(V)))
    assert evaluate(third_remainder, variables) <= 0


def simplex_grid(d, denominator):
    for numerators in product(range(denominator + 1), repeat=d - 1):
        if sum(numerators) <= denominator:
            yield tuple(Q(x, denominator) for x in numerators) + (
                Q(denominator - sum(numerators), denominator),)


otp_comparisons = 0
for d in (1, 2, 3, 4, 5):
    for public_q in simplex_grid(d, 5):
        distance = Q(0)
        generated_distance = Q(0)
        for m, s, ciphertext in product(range(d), repeat=3):
            actual = Q(1, d * d) if ciphertext == (m + s) % d else Q(0)
            comparison = public_q[ciphertext] / (d * d)
            distance += abs(actual - comparison)
        for m, ciphertext in product(range(d), repeat=2):
            marginal = sum(Q(1, d * d) for s in range(d)
                           if ciphertext == (m + s) % d)
            generated_distance += abs(marginal - Q(1, d * d))
        assert distance == 2 * (1 - Q(1, d))
        assert generated_distance == 0
        otp_comparisons += 1


quantum_vectors = ((-2, 1, -1), (2, -1, -1), (0, -1, 1))
private_vectors = ((-1, 1, -1), (1, -1, 0), (0, -1, 1))
cone_points = 0
for point in product((Q(x, 2) for x in range(-6, 7)), repeat=3):
    c, q, e = point
    quantum_coefficients = (-(c + q + e) / 2, -(q + e) / 2, -(c + 2*q) / 2)
    private_coefficients = (-(c + q + e), -(q + e), -(c + q))
    for vectors, coefficients in ((quantum_vectors, quantum_coefficients),
                                  (private_vectors, private_coefficients)):
        recovered = tuple(sum(a * v[j] for a, v in zip(coefficients, vectors))
                          for j in range(3))
        assert recovered == point
    cone_points += 1


# Controls that must reject deliberately weakened or sign-mutated statements.
mutations = {}
omit_consumed_environment_term = mutual(V, E, W | X)
witness = {W: [1], V: [2], E: [2], B: [], X: [], K: [], L: []}
mutations['omit_second_I_V_E_given_WX'] = evaluate(omit_consumed_environment_term, witness) == 1

# OTP: W=m, V=s, X=m+s, B=E=constant. The uncharged bound would say 1<=0.
otp_variables = {W: [1], V: [2], X: [3], B: [], E: [], K: [], L: []}
left = linear((1, mutual(W, B | V, X)), (-1, mutual(W, E, X)))
uncharged = linear((1, mutual(W | V, B, X)), (-1, mutual(W | V, E, X)))
mutations['omit_consumed_private_key_cost'] = (
    evaluate(left, otp_variables) == 1 and evaluate(uncharged, otp_variables) == 0)
mutations['flip_OTP_key_sign'] = not (1 + 1 <= 0)  # P+S for (-1,1,+1)
mutations['replace_literal_joint_secrecy_by_generated_only'] = Q(1) == 2*(1-Q(1,2))

# Cost selection cannot in general work with equality of expected cost to N.
for n in range(2, 65):
    bad_probability = Q(1, n)
    good_probability = 1 - bad_probability
    low_error_cost = 1 / good_probability
    assert good_probability * low_error_cost == 1
    assert low_error_cost > 1
    # Every admissible-cost realization has error one, while mean error=1/n.
mutations['remove_strict_cost_margin'] = True

# Superlinear secret registers invalidate normalized continuity from trace error.
for n in range(2, 65):
    epsilon = Q(1, n)
    log_dimension = n*n
    mutual_information = epsilon * log_dimension
    assert mutual_information / n == 1
    assert 2*epsilon <= 1
mutations['allow_superlinear_gross_secret_registers'] = True
assert all(mutations.values())

print(json.dumps({
    'scope': 'exact algebra, rational controls, and exact GF(2)-linear classical witnesses; no EPnI validation',
    'formal_entropy_identity_residuals': [len(second_residual), len(third_residual)],
    'classical_GF2_remainder_trials': classical_trials,
    'OTP_public_marginal_comparisons': otp_comparisons,
    'cone_inverse_points_per_cone': cone_points,
    'mutation_controls_rejected': mutations,
    'passed': True,
}, indent=2))
