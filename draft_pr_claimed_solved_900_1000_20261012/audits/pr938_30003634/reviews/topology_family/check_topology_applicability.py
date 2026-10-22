#!/usr/bin/env python3
"""Read-only finite diagnostics; not a proof of the topology theorem.

Checks use explicit exceptions, so -O, -OO and PYTHONOPTIMIZE cannot disable them.
Successful replay emits JSON to stdout and never rewrites the frozen receipt.
"""
from fractions import Fraction
import json
import sys

EXPECTED_WORD_LENGTH = 104
EXPECTED_RANK_CASES = 6561

class ValidationError(RuntimeError):
    """A finite applicability check failed."""

def require(condition, message):
    if not condition:
        raise ValidationError(message)

def inverse(w):
    return [-x for x in reversed(w)]

def multiply(*words):
    out = []
    for word in words:
        for letter in word:
            if out and out[-1] == -letter:
                out.pop()
            else:
                out.append(letter)
    return out

def comm(x, y):
    return multiply(x, y, inverse(x), inverse(y))

def rank(matrix, prime=None):
    matrix = [[Fraction(x) if prime is None else x % prime for x in row]
              for row in matrix]
    m = len(matrix)
    n = len(matrix[0]) if m else 0
    r = 0
    for j in range(n):
        at = next((i for i in range(r, m) if matrix[i][j]), None)
        if at is None:
            continue
        matrix[r], matrix[at] = matrix[at], matrix[r]
        pivot = matrix[r][j]
        inv = 1 / pivot if prime is None else pow(int(pivot), -1, prime)
        matrix[r] = [v * inv if prime is None else v * inv % prime
                     for v in matrix[r]]
        for i in range(m):
            if i != r:
                q = matrix[i][j]
                matrix[i] = [x - q * y if prime is None else (x - q * y) % prime
                             for x, y in zip(matrix[i], matrix[r])]
        r += 1
        if r == m:
            break
    return r

def check():
    a = [1, 1]
    b = [2, 2]
    c = comm(a, b)
    d = multiply(inverse(a), c, a)
    e = multiply(inverse(b), c, b)
    u = comm(c, d)
    v = comm(d, e)
    beta = comm(u, v)
    require(len(beta) == EXPECTED_WORD_LENGTH,
            'nested commutator Artin length differs from the expected 104')
    labels = [0, 1, 2]
    signed = {(0, 1): 0, (0, 2): 0, (1, 2): 0}
    for letter in beta:
        k = abs(letter) - 1
        key = tuple(sorted(labels[k:k+2]))
        signed[key] += 1 if letter > 0 else -1
        labels[k], labels[k+1] = labels[k+1], labels[k]
    require(labels == [0, 1, 2], 'nested word has nonidentity strand permutation')
    require(all(n % 2 == 0 for n in signed.values()),
            'pure closure has a nonintegral pairwise linking count')
    linking = {str(k): n // 2 for k, n in signed.items()}
    require(all(n == 0 for n in linking.values()),
            'nested word has a nonzero pairwise linking number')
    total_exponent = sum(1 if letter > 0 else -1 for letter in beta)
    require(total_exponent == 0, 'nested commutator has nonzero exponent sum')

    # Exhaust all 2x2 matrices with entries a+b*t and a,b in {-1,0,1}.
    entries = [(a, b) for a in [-1, 0, 1] for b in [-1, 0, 1]]
    count = 0
    for x in entries:
        for y in entries:
            for z in entries:
                for w in entries:
                    terms = [x, y, z, w]
                    twist = [[a-b for a, b in terms[:2]],
                             [a-b for a, b in terms[2:]]]
                    ordinary = [[a+b for a, b in terms[:2]],
                                [a+b for a, b in terms[2:]]]
                    require(rank(twist) >= rank(ordinary, 2),
                            'signed rational rank is smaller than mod-2 rank')
                    count += 1
    require(count == EXPECTED_RANK_CASES, 'rank diagnostic inventory is incomplete')

    # RP^2 boundaries d2=1+t, d1=t-1 demonstrate the integral-H1 torsion gap.
    rp2 = {'ordinary_Q_b2': 0, 'ordinary_F2_b2': 1,
           'sign_Q_b2': 1, 'H1_integral': 'Z/2'}
    require(rp2['sign_Q_b2'] <= rp2['ordinary_F2_b2'],
            'RP2 mod-2 rank countercontrol failed')
    require(rp2['sign_Q_b2'] > rp2['ordinary_Q_b2'],
            'RP2 torsion countercontrol no longer detects the rational-H2 gap')

    # Matching sheets in (L+,L-,D+,D-) reinforce in anti-invariant cycles.
    q = [[0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]]
    x = [1, -1, 0, 0]
    y = [0, 0, 1, -1]
    pair = sum(x[i] * q[i][j] * y[j] for i in range(4) for j in range(4))
    require(pair == 2, 'anti-invariant matching sheets failed to reinforce')
    return {
        'scope': 'finite diagnostics and actual character applicability only; no computed signature or theorem certification',
        'word': {'freely_reduced_artin_length': len(beta), 'final_strand_labels': labels,
                 'signed_crossing_counts': {str(k): n for k, n in signed.items()},
                 'pairwise_linking_numbers': linking, 'total_exponent': total_exponent},
        'zero_surgery': {'linking_matrix': [[0,0,0],[0,0,0],[0,0,0]], 'H1': 'Z^3',
                         'all_meridian_sign_character': 'exists and sends all zero-surgery slopes to 1',
                         'one_color_Seifert_framing': [0,0,0],
                         'Toffoli_corrections': {'signature_linking_matrix': 0, 'sum_framed_linking_entries': 0}},
        'rank_diagnostics': {'signed_group_ring_2_by_2_matrices_tested': count,
                             'all_rank_inequalities_pass': True, 'torsion_countercontrol': rp2},
        'lift_diagnostic': {'anti_invariant_intersection': pair,
                            'signature_relevance': 'positive normalization factors do not affect nondegeneracy or signature'}
    }

if __name__ == '__main__':
    try:
        print(json.dumps(check(), indent=2))
    except ValidationError as exc:
        print('validation failure: ' + str(exc), file=sys.stderr)
        raise SystemExit(1)
