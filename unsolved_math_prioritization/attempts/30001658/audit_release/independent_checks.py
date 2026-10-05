#!/usr/bin/env python3
"""Independent exact audit. No imports from the author packet; no network calls."""
from fractions import Fraction as Q
from itertools import product
from math import comb, lcm
from collections import Counter
import hashlib
import json

COUNTS = Counter()

def check(truth, label):
    if not truth:
        raise ValueError(label)
    COUNTS[label] += 1

def inverse(matrix):
    """Dense rational Gauss-Jordan, unrelated to the author's distance formula."""
    n = len(matrix)
    rows = [[Q(x) for x in row] + [Q(i == j) for j in range(n)]
            for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if rows[i][col])
        rows[col], rows[pivot] = rows[pivot], rows[col]
        d = rows[col][col]
        rows[col] = [x / d for x in rows[col]]
        for i in range(n):
            if i != col:
                d = rows[i][col]
                if d:
                    rows[i] = [x - d*y for x, y in zip(rows[i], rows[col])]
    return [row[n:] for row in rows]

def cube_matrix(n, shift=2):
    N = 1 << n
    return [[n + shift if x == y else -int((x ^ y).bit_count() == 1)
             for y in range(N)] for x in range(N)]

def multiply(A, B):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*B)] for row in A]

def bilinear(A, v):
    return sum(v[i]*v[j]*A[i][j] for i in range(len(v)) for j in range(len(v)))

def walsh(v):
    """Unnormalized fast Walsh transform, used as a separate cross-check."""
    w = list(v)
    stride = 1
    while stride < len(w):
        for start in range(0, len(w), 2*stride):
            for j in range(start, start + stride):
                a, b = w[j], w[j + stride]
                w[j], w[j + stride] = a + b, a - b
        stride *= 2
    return w

def logarithm_upper(n, m, divisor=256):
    """Return ceil(256 log2(2**n/m))/256 via integer comparisons alone.

    The comparison 2**j * m**256 >= (2**n)**256 is equivalent to
    j/256 >= log2(2**n/m). Binary search finds the least such integer j.
    This avoids the author's atanh series, rational ln2, and tail bound.
    """
    check(1 <= m <= (1 << n), 'log_domain')
    low, high = 0, n * divisor
    m_power = m ** divisor
    target = 1 << (n * divisor)
    while low < high:
        mid = (low + high) // 2
        if (m_power << mid) >= target:
            high = mid
        else:
            low = mid + 1
    check((m_power << low) >= target, 'log_upper_integer_certificate')
    check(low == 0 or (m_power << (low - 1)) < target, 'log_upper_minimality')
    return Q(low, divisor)

def antichain_ideals(n):
    """Enumerate antichains using comparability exclusion; return their ideals.

    A downset is uniquely the lower closure of its maximal-element antichain.
    This does not use the author's D1 subset D0 recursion.
    """
    N = 1 << n
    lower = [sum(1 << y for y in range(N) if y & x == y) for x in range(N)]
    incomparable = [sum(1 << y for y in range(N)
                        if x & y != x and x & y != y) for x in range(N)]
    out = []
    def visit(candidates, ideal):
        out.append(ideal)
        while candidates:
            bit = candidates & -candidates
            x = bit.bit_length() - 1
            candidates ^= bit
            visit(candidates & incomparable[x], ideal | lower[x])
    visit((1 << N) - 1, 0)
    check(len(out) == len(set(out)), 'antichain_to_ideal_injective')
    return sorted(out)

def compress(mask, n, i):
    """Reconstruct the two fiber layers by union/intersection."""
    result = 0
    for x in range(1 << n):
        if (x >> i) & 1:
            continue
        low, high = bool(mask & (1 << x)), bool(mask & (1 << (x | (1 << i))))
        if low or high:
            result |= 1 << x
        if low and high:
            result |= 1 << (x | (1 << i))
    return result

def points(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit

def rational_text(x):
    return str(x.numerator) + '/' + str(x.denominator)

def main():
    inverses = {}
    scaled = {}
    exhaustive = {}
    for n in range(6):
        N = 1 << n
        M = cube_matrix(n)
        R = inverse(M)
        inverses[n] = R
        check(multiply(M, R) == [[Q(i == j) for j in range(N)] for i in range(N)],
              'dense_inverse_identity')
        check(all(x > 0 for row in R for x in row), 'dense_inverse_strict_positivity')
        check(all(sum(row) == Q(1, 2) for row in R), 'dense_inverse_row_sum')
        for x in range(N):
            for y in range(N):
                d = (x ^ y).bit_count()
                formula = Q(sum(comb(n+1, j) for j in range(d+1, n+2)),
                            (n+1)*comb(n, d)*(1 << (n+1)))
                check(R[x][y] == formula, 'independent_inverse_matches_kernel')
        den = lcm(*(x.denominator for row in R for x in row))
        K = [[int(x*den) for x in row] for row in R]
        scaled[n] = K, den
        # Matrix and edge-sum conventions, including signed test functions.
        v = [Q(((7*x + 3) % 11) - 5, 3) for x in range(N)]
        edge = sum((v[x]-v[x ^ (1 << i)])**2 for x in range(N) for i in range(n))
        mass = sum(x*x for x in v)
        check(edge + 4*mass == 2*bilinear(M, v), 'ordered_energy_matrix_identity')
        check(sum((abs(v[x])-abs(v[x ^ (1 << i)]))**2
                  for x in range(N) for i in range(n)) <= edge,
              'absolute_value_contraction')
        w = walsh(v)
        check(bilinear(R, v) == sum(Q(w[s]**2, 2*N*(s.bit_count()+1))
                                   for s in range(N)), 'walsh_normalization_test')
        if n == 5:
            continue
        # Gray traversal updates K*1_A on insertions AND deletions.
        # Unlike the author, this does not recur on mask with its lowest bit removed.
        bounds = [None] + [logarithm_upper(n, m) for m in range(1, N+1)]
        energies = [0]*(1 << N)
        row_sums = [0]*N
        previous, mass_count, energy = 0, 0, 0
        max_q, max_mask = Q(-1), None
        for t in range(1, 1 << N):
            mask = t ^ (t >> 1)
            changed = mask ^ previous
            x = changed.bit_length() - 1
            sign = 1 if mask & changed else -1
            energy += 2*sign*row_sums[x] + K[x][x]
            for y in range(N):
                row_sums[y] += sign*K[y][x]
            mass_count += sign
            check(mass_count == mask.bit_count(), 'gray_cardinality')
            energies[mask] = energy
            q_bound = Q(energy, den*mass_count)*bounds[mass_count]
            check(q_bound <= 1, 'all_sets_n_zero_through_four')
            if q_bound > max_q:
                max_q, max_mask = q_bound, mask
            previous = mask
        for mask in range(1 << N):
            for i in range(n):
                cm = compress(mask, n, i)
                check(cm.bit_count() == mask.bit_count(), 'compression_size')
                check(energies[cm] >= energies[mask], 'compression_pair_sum')
        # Exact Walsh certificate for every ideal in dimensions <=4.
        for mask in antichain_ideals(n):
            w = walsh([int(mask >> x & 1) for x in range(N)])
            check(Q(energies[mask], den) == sum(Q(w[s]*w[s], 2*N*(s.bit_count()+1))
                                                   for s in range(N)), 'ideal_walsh_energy')
        exhaustive[str(n)] = {'nonempty_sets':(1 << N)-1,
                              'maximum_certified_q_upper':rational_text(max_q),
                              'one_maximizing_mask':max_mask}
    n, N = 5, 32
    K, den = scaled[n]
    bounds = [None] + [logarithm_upper(n, m) for m in range(1, N+1)]
    ideals = antichain_ideals(n)
    check(len(ideals) == 7581, 'n5_downset_count')
    hist = Counter()
    max_q, max_mask = Q(-1), None
    for mask in ideals:
        pts = list(points(mask))
        hist[len(pts)] += 1
        for x in pts:
            for i in range(n):
                check(mask & (1 << (x & ~(1 << i))), 'n5_ideal_definition')
        if not pts:
            continue
        # Unordered distinct pairs + the exact diagonal. The author sums all ordered pairs.
        energy = sum(K[x][x] for x in pts) + 2*sum(K[x][y] for j, x in enumerate(pts)
                                                 for y in pts[:j])
        w = walsh([int(mask >> x & 1) for x in range(N)])
        spectral = sum(Q(w[s]*w[s], 2*N*(s.bit_count()+1)) for s in range(N))
        check(Q(energy, den) == spectral, 'n5_walsh_pair_energy_agreement')
        q_bound = Q(energy, den*len(pts))*bounds[len(pts)]
        check(q_bound <= 1, 'n5_downset_inequality')
        if q_bound > max_q:
            max_q, max_mask = q_bound, mask
    # Every subspace through n=4 is detected by XOR closure, not generated by extending bases.
    affine_counts = {}
    for n in range(5):
        N = 1 << n
        R = inverses[n]
        cosets = set()
        for mask in range(1, 1 << N, 2):
            pts = list(points(mask))
            if all(mask & (1 << (x ^ y)) for x in pts for y in pts):
                for z in range(N):
                    cosets.add(sum(1 << (x ^ z) for x in pts))
        affine_counts[str(n)] = len(cosets)
        for mask in cosets:
            pts = list(points(mask)); m = len(pts)
            k = n - (m.bit_length()-1)
            value = sum(R[x][y] for x in pts for y in pts)/m
            cap = Q((1 << (k+1))-1, (k+1)*(1 << (k+1)))
            check(value <= cap, 'affine_resolvent_bound')
            check(k*value < 1, 'affine_strict_target_including_full')
            # Auxiliary-bound equality iff coordinate subcube, by direct geometry.
            variable = 0
            base = pts[0]
            for x in pts:
                variable |= x ^ base
            coordinate = (1 << variable.bit_count()) == m
            check((value == cap) == coordinate, 'affine_auxiliary_equality_class')
    negative = {}
    def reject(label, wrong):
        check(not wrong, 'reject_'+label)
        negative[label] = 'rejected'
    R1, R2 = inverses[1], inverses[2]
    reject('single_counted_energy_is_source_energy', 1 == 2)
    reject('uniform_energy_equals_counting_energy', Q(2,2) == 2)
    reject('wrong_resolvent_shift', multiply(cube_matrix(1, 1), R1) == [[1,0],[0,1]])
    reject('missing_kernel_half', multiply(cube_matrix(1), [[2*x for x in row] for row in R1]) == [[1,0],[0,1]])
    reject('unordered_pairs_without_factor_two', 2*R1[0][0]+R1[0][1] == sum(sum(row) for row in R1))
    diagonal = R2[0][0]+R2[3][3]+2*R2[0][3]
    edge = R2[0][0]+R2[1][1]+2*R2[0][1]
    reject('reverse_compression', diagonal >= edge)
    reject('erase_exterior_schur_correction', R1[0][0] == Q(1,3))
    reject('parity_correction_absorbed_by_two', Q(16,6) <= 2)
    reject('degree_one_relaxation_implies_target', Q(5*33,128) <= 1)
    reject('full_set_has_positive_log', logarithm_upper(5,32) > 0)
    reject('coefficient_three_universal', 2*5+4 >= 3*5)
    check(5+4 < 2*5 and 2*5+4 >= 2*5, 'wrong_normalization_singleton_is_not_target_counterexample')
    # A fixed-size dense comparison; empty A is deliberately excluded from logarithm calls.
    check(inverses[0] == [[Q(1,2)]] and exhaustive['0']['maximum_certified_q_upper']=='0/1',
          'dimension_zero_full_set')
    result = {
        'status':'PASS_INDEPENDENT_SCOPED_AUDIT',
        'arithmetic':'exact integer and Fraction arithmetic; no floating-point acceptance',
        'source_problem_id':'30001658',
        'all_sets':exhaustive,
        'n5_downsets_including_empty':len(ideals),
        'n5_downset_cardinality_histogram':dict(sorted(hist.items())),
        'n5_sorted_ideal_masks_sha256':hashlib.sha256(('\n'.join(map(str, ideals))+'\n').encode()).hexdigest(),
        'n5_maximum_certified_q_upper':rational_text(max_q),
        'n5_one_maximizing_mask':max_mask,
        'affine_cosets_checked':affine_counts,
        'mathematical_negative_controls':negative,
        'counts':dict(sorted(COUNTS.items())),
        'total_checks':sum(COUNTS.values()),
        'scope':'Independent exact verification through n=5 plus controls for written proofs. No all-dimension resolution, novelty, or global-openness claim.'
    }
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__ == '__main__':
    main()
