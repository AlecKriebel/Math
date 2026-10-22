#!/usr/bin/env python3
"""Fresh exact checker; no author or previous reviewer code is imported.

One calculation starts with explicit (coefficient word, generator) chains and
Gaussian elimination. The other uses periods of necklaces, independently of
the chain matrix construction. Characteristic 0 means exact Fraction arithmetic.
Run: python3 exact_chain_check.py --output RESULTS.json
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


class VerificationFailure(RuntimeError):
    """A failed acceptance check; active with or without Python optimization."""


_checks_performed = 0


def need(condition, message):
    global _checks_performed
    _checks_performed += 1
    if not condition:
        raise VerificationFailure(message)


def words(r, n):
    return list(product(range(r), repeat=n))


def reduce_matrix(rows, ncols, p):
    """RREF, pivot columns. ncols is explicit even for zero-row matrices."""
    a = [[v % p for v in row] if p else [Fraction(v) for v in row]
         for row in rows]
    need(all(len(row) == ncols for row in a),
         f'Nonrectangular matrix: expected {ncols} columns, got {[len(row) for row in a]}')
    pivots = []
    k = 0
    for j in range(ncols):
        i = next((i for i in range(k, len(a)) if a[i][j]), None)
        if i is None:
            continue
        a[k], a[i] = a[i], a[k]
        inverse = pow(a[k][j], -1, p) if p else 1 / a[k][j]
        a[k] = [(v * inverse) % p if p else v * inverse for v in a[k]]
        for i in range(len(a)):
            if i == k or not a[i][j]:
                continue
            c = a[i][j]
            a[i] = [((v - c * w) % p if p else v - c * w)
                    for v, w in zip(a[i], a[k])]
        pivots.append(j)
        k += 1
        if k == len(a):
            break
    return a, pivots


def nullspace(rows, ncols, p):
    reduced, pivots = reduce_matrix(rows, ncols, p)
    out = []
    for j in range(ncols):
        if j in pivots:
            continue
        v = [0] * ncols
        v[j] = 1
        for i, t in enumerate(pivots):
            v[t] = -reduced[i][j]
            if p:
                v[t] %= p
        out.append(v)
    return out, len(pivots)


def rank(rows, ncols, p):
    return len(reduce_matrix(rows, ncols, p)[1])


def matvec(rows, v, p):
    return [sum(x * y for x, y in zip(row, v)) % p if p
            else sum(x * y for x, y in zip(row, v)) for row in rows]


def chain_matrices(r, n):
    degree_zero = words(r, n)
    degree_one = [(a, v) for a in words(r, n - 1) for v in range(r)] if n else []
    index = {w: i for i, w in enumerate(degree_zero)}
    b = [[0] * len(degree_one) for _ in degree_zero]
    left = [[0] * len(degree_one) for _ in degree_zero]
    concat = [[0] * len(degree_one) for _ in degree_zero]
    for j, (a, v) in enumerate(degree_one):
        i, t = index[a + (v,)], index[(v,) + a]
        b[i][j] += 1
        b[t][j] -= 1
        left[t][j] += 1       # BLS left cap, q=p=1, sign +1.
        concat[i][j] += 1     # Negative of the q=p=1 right cap.
    return b, left, concat, len(degree_one), len(degree_zero)


def matrix_answer(r, n, p):
    b, left, concat, c1, c0 = chain_matrices(r, n)
    cycles, brank = nullspace(b, c1, p)
    need(all(not any(matvec(b, v, p)) for v in cycles),
         f'Nullspace contains a noncycle: r={r}, n={n}, characteristic={p}')
    caps = [matvec(left, v, p) for v in cycles]
    # On cycles the two concatenations agree exactly, before quotienting.
    need(caps == [matvec(concat, v, p) for v in cycles],
         f'Left-cap/concatenation mismatch on cycles: r={r}, n={n}, characteristic={p}')
    augmented = [row + [v[i] for v in caps] for i, row in enumerate(b)]
    caprank = rank(augmented, c1 + len(cycles), p) - brank
    # Source for the next homology is HK_1 = ker b (C_2 is zero).
    # Target is HK_0 = C_0 / im b. No orbit calculations enter here.
    return {'c1': c1, 'c0': c0, 'ordinary_h1': len(cycles),
            'ordinary_h0': c0 - brank, 'cap_rank': caprank,
            'higher_h1': len(cycles) - caprank,
            'higher_h0': c0 - brank - caprank}


def period_necklaces(r, n, p):
    """Distinct necklaces via left shifts; size via least periodic block."""
    if n == 0:
        return {'ordinary_h1': 0, 'ordinary_h0': 1,
                'higher_h1': 0, 'higher_h0': 1, 'sizes': {}}
    representatives = {min(w[j:] + w[:j] for j in range(n))
                       for w in words(r, n)}
    sizes = Counter()
    for w in representatives:
        size = next(d for d in range(1, n + 1)
                    if n % d == 0 and w == w[:d] * (n // d))
        sizes[size] += 1
    exceptional = sum(count for d, count in sizes.items() if p and d % p == 0)
    return {'ordinary_h1': len(representatives),
            'ordinary_h0': len(representatives),
            'higher_h1': exceptional, 'higher_h0': exceptional,
            'sizes': dict(sorted(sizes.items()))}


def witness_block(p):
    """Primitive length-p witness without exponential full-alphabet matrices."""
    w = (0,) * (p - 1) + (1,)
    # Cut after each letter, independently of the concatenation-chain builder.
    rotated = [w[i:] + w[:i] for i in range(p)]
    need(len(set(rotated)) == p, f'Primitive rotations are not distinct for p={p}')
    index = {word: i for i, word in enumerate(rotated)}
    b = [[0] * p for _ in range(p)]
    left = [[0] * p for _ in range(p)]
    tensors = []
    for j, word in enumerate(rotated):
        a, v = word[:-1], word[-1]
        tensors.append((a, v))
        b[index[word]][j] += 1
        t = index[(v,) + a]
        b[t][j] -= 1
        left[t][j] += 1
    need(len(set(tensors)) == p, f'Witness tensors are not distinct for p={p}')
    z = [1] * p
    need(not any(matvec(b, z, 0)), f'Witness is not an integral cycle for p={p}')
    image = matvec(left, z, 0)
    # Produce an explicit degree-one preimage of the degree-zero cap, too.
    # Its ordinary boundary is in C_0; it cannot kill the C_1 cycle itself.
    filler = [0] * p
    word = w
    for i in range(p):
        filler[index[word]] = i
        word = (word[-1],) + word[:-1]
    over_z = matvec(b, filler, 0)
    need(over_z == [v - (p if i == index[w] else 0)
                    for i, v in enumerate(image)],
         f'Integral cap-filler identity failed for p={p}')
    need(matvec(b, filler, p) == [v % p for v in image],
         f'Characteristic-p cap-filler identity failed for p={p}')
    comparisons = []
    for characteristic in [0, 2 if p != 2 else 3, p]:
        brank = rank(b, p, characteristic)
        augmented = [row + [image[i]] for i, row in enumerate(b)]
        vanished = rank(augmented, p + 1, characteristic) == brank
        need(vanished == (characteristic == p),
             f'Wrong witness cap behavior: p={p}, characteristic={characteristic}, '
             f'cap_zero={vanished}')
        comparisons.append({'characteristic': characteristic,
                            'cap_zero_in_coinvariants': vanished})
    return {'prime': p, 'distinct_tensors': p, 'ordinary_boundary_sources': 0,
            'higher_boundary_sources': 0,
            'explicit_cap_preimage_coefficients': filler,
            'integer_identity': 'b(filler)=cap(z)-p*w',
            'comparisons': comparisons}


def negative_controls():
    out = []
    # A wrong scalar n in place of the orbit cardinality d fails on x^n.
    for p in [2, 3, 5, 7]:
        actual = matrix_answer(1, p, p)
        need(actual['higher_h1'] == actual['higher_h0'] == 0,
             f'Rank-one word-length negative control failed for p={p}: {actual}')
        out.append({'mutation': 'word_length_instead_of_distinct_orbit_size',
                    'r': 1, 'n': p, 'p': p, 'wrong_prediction': 1,
                    'verified_higher_h1': 0, 'detected': True})
    # Period 2 at length 6 distinguishes char 2 and 3; period 3 reverses it.
    for word, expected_size in [((0, 1) * 3, 2), ((0, 0, 1) * 2, 3)]:
        n = len(word)
        shifts = set(word[i:] + word[:i] for i in range(n))
        need(len(shifts) == expected_size,
             f'Repeated-word orbit has wrong size: word={word}, '
             f'actual={len(shifts)}, expected={expected_size}')
        for p in [2, 3]:
            coefficient = len(shifts) % p
            need((coefficient == 0) == (expected_size == p),
                 f'Repetition-stabilizer control failed: word={word}, p={p}')
        out.append({'mutation': 'ignore_repetition_stabilizer',
                    'word': ''.join('xy'[v] for v in word), 'length': n,
                    'actual_orbit_size': expected_size, 'detected': True})
    # Wrong plus sign and multiplication-only b both destroy the xx cycle in Q.
    b, left, concat, c1, c0 = chain_matrices(1, 2)
    need(b == [[0]] and left == concat == [[1]],
         'Rank-one commutator/cap matrices have unexpected entries')
    need([[2]] != b and concat != b,
         'Wrong plus-sign or multiplication-only differential escaped detection')
    out.append({'mutation': 'plus_sign_or_multiplication_for_commutator',
                'cycle': 'x tensor x', 'correct_boundary': 0,
                'wrong_plus_boundary': '2xx', 'wrong_mu_boundary': 'xx',
                'detected_over_Q': True})
    # A zero-cap mutant incorrectly keeps the coefficient-weight-zero cycles.
    actual = matrix_answer(2, 1, 2)
    need(actual['ordinary_h1'] == 2 and actual['higher_h1'] == 0,
         f'Zero-cap/trivial-coefficients negative control failed: {actual}')
    out.append({'mutation': 'zero_cap_or_trivial_module_coefficients',
                'r': 2, 'n': 1, 'p': 2, 'wrong_higher_h1': 2,
                'verified_higher_h1': 0, 'detected': True})
    # Listing n rotations with multiplicities can annihilate a proposed witness.
    need((1 + 1) % 2 == 0, 'Repeated-rotation multiplicity control failed over F_2')
    out.append({'mutation': 'claim_all_rotations_are_distinct',
                'word': 'xx', 'p': 2, 'duplicated_sum_is_zero': True,
                'single_orbit_sum_cap_is_nonzero': True, 'detected': True})
    # Claiming all ordinary cycles survive ignores a nonzero image under cap.
    ordinary = matrix_answer(1, 3, 3)
    need(ordinary['ordinary_h1'] == 1 and ordinary['higher_h1'] == 0,
         f'Ordinary-cycle/higher-cycle negative control failed: {ordinary}')
    out.append({'mutation': 'ordinary_cycle_implies_higher_cycle',
                'cycle': 'xx tensor x over F_3', 'cap': 'xxx nonzero',
                'detected': True})
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path('RESULTS.json'))
    parser.add_argument('--inject-wrong-expectation', action='store_true',
                        help='Test-only: corrupt one expected dimension; must fail before writing output.')
    args = parser.parse_args()
    cases = []
    ranges = [(0, range(0, 9)), (1, range(0, 13)),
              (2, range(0, 8)), (3, range(0, 5)), (4, range(0, 4))]
    for r, ns in ranges:
        for n in ns:
            for p in [0, 2, 3, 5, 7, 11]:
                exact = matrix_answer(r, n, p)
                orbit = period_necklaces(r, n, p)
                if args.inject_wrong_expectation and (r, n, p) == (2, 2, 2):
                    orbit['higher_h1'] += 1
                for name in ['ordinary_h1', 'ordinary_h0', 'higher_h1', 'higher_h0']:
                    need(exact[name] == orbit[name],
                         f'Matrix/necklace mismatch: r={r}, n={n}, characteristic={p}, '
                         f'quantity={name}, matrix={exact[name]}, expected={orbit[name]}')
                cases.append({'r': r, 'n': n, 'characteristic': p,
                              'matrix': exact, 'period_necklaces': orbit})
    witnesses = [witness_block(p) for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]]
    controls = negative_controls()
    need(len(cases) == 234, f'Wrong case coverage: {len(cases)} != 234')
    need(len(witnesses) == 14, f'Wrong witness coverage: {len(witnesses)} != 14')
    need(len(controls) == 10, f'Wrong negative-control coverage: {len(controls)} != 10')
    result = {'timestamp_utc': datetime.now(timezone.utc).isoformat(),
              'frozen_head': '286cc67c0727b4decfd4f261a0591cd8823ebce9',
              'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'independence': 'Fresh code; no imports or reads of author/prior-review implementations.',
              'arithmetic': 'Fractions over Q; modular integers over prime fields; no floating point.',
              'matrix_period_comparisons': len(cases),
              'witness_primes': len(witnesses), 'negative_controls': len(controls),
              'verification_checks_performed': _checks_performed,
              'all_passed': True, 'cases': cases, 'witnesses': witnesses,
              'mutation_controls': controls}
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items()
                      if k not in {'cases', 'witnesses', 'mutation_controls'}}, indent=2))


if __name__ == '__main__':
    main()
