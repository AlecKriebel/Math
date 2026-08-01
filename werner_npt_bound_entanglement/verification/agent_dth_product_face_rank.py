#!/usr/bin/env python3
"""Exact finite-field rank certificate for the product-DTH mixed face.

This verifier uses no floating-point arithmetic.  It constructs one product
DTH triple for each allocation (i,j,k) in {0,1,2}^3 of

  <z,u0> = 0 at site i,
  <z,u1> = 0 at site j,
  det(z,u0,u1) = 0 at site k.

The local U(3)^3 twirl is evaluated in the exact 103-diagram bridge.  The
rank of every one of the 216 mixed multiplicity blocks is then computed over
a prime field.  A rank-r result modulo a good prime is an exact certificate
that the rational face has rank at least r.  It is deliberately not called
an upper-rank certificate: an independent rational kernel/exposing identity
is required for that direction.
"""

from __future__ import annotations

from itertools import permutations, product
from pathlib import Path
import hashlib
import importlib.util
import random

import numpy as np


HERE = Path(__file__).resolve().parent
BRIDGE_PATH = HERE / "agent_dth_local_crossing_exact.py"
SPEC = importlib.util.spec_from_file_location("dth_exact_bridge", BRIDGE_PATH)
BRIDGE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(BRIDGE)


PRIMES = (1_000_003, 1_000_033)
EXPECTED_MIXED_RANK = 2266
EXPECTED_ACTIVE_BLOCKS = 198
EXPECTED_PIVOT_SHA256 = (
    "2297a5d32caba44ac2dd6a8d26983a9fe61b7bf11d73e7daba06af251a050955"
)
MIXED_MULTS = BRIDGE.MIXED_MULTS


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scale(c, a):
    return tuple(c * x for x in a)


def nonzero(a):
    return any(a)


def independent(a, b):
    return nonzero(cross(a, b))


class IntegerTriples:
    """Deterministic small-integer product DTH triples."""

    def __init__(self, seed=91377):
        self.rng = random.Random(seed)

    def vector(self):
        while True:
            out = tuple(self.rng.randrange(-1, 2) for _ in range(3))
            if nonzero(out):
                return out

    def pair(self):
        while True:
            a, b = self.vector(), self.vector()
            if independent(a, b):
                return a, b

    def local(self, orthogonal_a, orthogonal_b, determinant_zero):
        if orthogonal_a and orthogonal_b and determinant_zero:
            a = self.vector()
            b = a
            c = cross(a, self.vector())
            while not nonzero(c):
                c = cross(a, self.vector())
        elif orthogonal_a and orthogonal_b:
            a, b = self.pair()
            c = cross(a, b)
        elif orthogonal_a and determinant_zero:
            a, b = self.pair()
            c = sub(scale(dot(a, a), b), scale(dot(a, b), a))
        elif orthogonal_b and determinant_zero:
            a, b = self.pair()
            c = sub(scale(dot(b, b), a), scale(dot(a, b), b))
        elif orthogonal_a:
            a = self.vector()
            c = cross(a, self.vector())
            while not nonzero(c):
                c = cross(a, self.vector())
            b = self.vector()
        elif orthogonal_b:
            b = self.vector()
            c = cross(b, self.vector())
            while not nonzero(c):
                c = cross(b, self.vector())
            a = self.vector()
        elif determinant_zero:
            a, b = self.pair()
            c = add(a, b)
        else:
            a, b, c = self.vector(), self.vector(), self.vector()
        assert nonzero(a) and nonzero(b) and nonzero(c)
        if orthogonal_a:
            assert dot(c, a) == 0
        if orthogonal_b:
            assert dot(c, b) == 0
        if determinant_zero:
            assert dot(c, cross(a, b)) == 0
        return a, b, c

    def global_triples(self):
        out = []
        for i, j, k in product(range(3), repeat=3):
            sites = tuple(
                self.local(site == i, site == j, site == k)
                for site in range(3)
            )
            # These three product identities are the complete physical DTH
            # equations for this branch.
            assert product_dot(sites, 0, 2) == 0
            assert product_dot(sites, 1, 2) == 0
            assert product_det(sites) == 0
            # Product vectors are proportional only if every local pair is
            # proportional.  Exclude that degenerate bivector exactly.
            assert any(independent(a, b) for a, b, _ in sites)
            out.append((i, j, k, sites))
        return out


def product_dot(sites, first, second):
    value = 1
    for site in sites:
        value *= dot(site[first], site[second])
    return value


def product_det(sites):
    value = 1
    for a, b, c in sites:
        value *= dot(c, cross(a, b))
    return value


def cycle_count(permutation):
    seen = set()
    cycles = 0
    for start in range(5):
        if start in seen:
            continue
        cycles += 1
        point = start
        while point not in seen:
            seen.add(point)
            point = permutation[point]
    return cycles


def compose_inverse(left, right):
    inverse = [0] * 5
    for i, value in enumerate(left):
        inverse[value] = i
    return tuple(inverse[right[i]] for i in range(5))


def modular_inverse(matrix, prime):
    n = len(matrix)
    work = [
        [int(x) % prime for x in row]
        + [int(i == j) for j in range(n)]
        for i, row in enumerate(matrix)
    ]
    for column in range(n):
        pivot = next(row for row in range(column, n) if work[row][column])
        work[column], work[pivot] = work[pivot], work[column]
        inv = pow(work[column][column], -1, prime)
        work[column] = [(x * inv) % prime for x in work[column]]
        for row in range(n):
            if row == column:
                continue
            coefficient = work[row][column]
            if coefficient:
                work[row] = [
                    (x - coefficient * y) % prime
                    for x, y in zip(work[row], work[column])
                ]
    return [row[n:] for row in work]


def matmul_mod(left, right, prime):
    a = np.asarray(left, dtype=np.int64) % prime
    b = np.asarray(right, dtype=np.int64) % prime
    # 103 products of numbers below 10^6 may overflow int64 if accumulated
    # at once.  Chunking at eight keeps every accumulator below 8*10^12.
    out = np.zeros((a.shape[0], b.shape[1]), dtype=np.int64)
    for start in range(0, a.shape[1], 8):
        out += a[:, start:start + 8] @ b[start:start + 8, :]
        out %= prime
    return out


def matvec_mod(matrix, vector, prime):
    a = np.asarray(matrix, dtype=np.int64)
    v = np.asarray(vector, dtype=np.int64) % prime
    out = np.zeros(a.shape[0], dtype=np.int64)
    for start in range(0, a.shape[1], 8):
        out += a[:, start:start + 8] @ v[start:start + 8]
        out %= prime
    return out


def local_moment(ket, bra, permutations_, prime):
    out = []
    for permutation in permutations_:
        value = 1
        for position in range(5):
            # Reducing after every factor is essential: a raw five-factor
            # numpy product can overflow int64 before the final remainder.
            value = (
                value
                * (dot(ket[position], bra[permutation[position]]) % prime)
            ) % prime
        out.append(value)
    return np.asarray(out, dtype=np.int64)


def block_offsets(multiplicities):
    out = []
    offset = 0
    for multiplicity in multiplicities:
        size = multiplicity * multiplicity
        out.append((offset, offset + size, multiplicity))
        offset += size
    assert offset == 103
    return out


def rank_mod(matrix, prime, return_pivots=False):
    a = np.asarray(matrix, dtype=np.int64).copy() % prime
    rows, columns = a.shape
    pivot_row = 0
    pivot_columns = []
    for column in range(columns):
        candidates = np.flatnonzero(a[pivot_row:, column])
        if not len(candidates):
            continue
        row = pivot_row + int(candidates[0])
        a[[pivot_row, row]] = a[[row, pivot_row]]
        a[pivot_row] = a[pivot_row] * pow(int(a[pivot_row, column]), -1, prime) % prime
        active = np.flatnonzero(a[:, column])
        active = active[active != pivot_row]
        for start in range(0, len(active), 64):
            rr = active[start:start + 64]
            a[rr] = (a[rr] - a[rr, column, None] * a[pivot_row]) % prime
        pivot_row += 1
        pivot_columns.append(column)
        if pivot_row == rows:
            break
    if return_pivots:
        return pivot_row, tuple(pivot_columns)
    return pivot_row


def exact_local_transform(prime):
    _, mixed_restriction, _, _ = BRIDGE.exact_restriction_bridge()
    permutations_ = BRIDGE.SELECTED_PERMUTATIONS
    gram = [
        [3 ** cycle_count(compose_inverse(left, right))
         for right in permutations_]
        for left in permutations_
    ]
    gram_inverse = modular_inverse(gram, prime)
    return matmul_mod(mixed_restriction, gram_inverse, prime)


def product_terms(transform, prime):
    terms = []
    for _, _, _, sites in IntegerTriples().global_triples():
        for alpha, beta, gamma, delta in product(range(2), repeat=4):
            local_vectors = []
            for a, b, z in sites:
                ket = ([b, a] if alpha else [a, b])
                ket += ([b, a] if beta else [a, b])
                ket += [z]
                bra = ([b, a] if gamma else [a, b])
                bra += ([b, a] if delta else [a, b])
                bra += [z]
                moment = local_moment(
                    ket, bra, BRIDGE.SELECTED_PERMUTATIONS, prime
                )
                local_vectors.append(matvec_mod(transform, moment, prime))
            sign = -1 if (alpha + beta + gamma + delta) % 2 else 1
            terms.append((sign, tuple(local_vectors)))
    assert len(terms) == 27 * 16
    return terms


def mixed_block_ranks(prime, with_pivots=False):
    transform = exact_local_transform(prime)
    terms = product_terms(transform, prime)
    offsets = block_offsets(MIXED_MULTS)
    ranks = {}
    pivots = {}
    for shapes in product(range(6), repeat=3):
        dimensions = tuple(MIXED_MULTS[s] for s in shapes)
        size = dimensions[0] * dimensions[1] * dimensions[2]
        matrix = np.zeros((size, size), dtype=np.int64)
        slices = [offsets[s] for s in shapes]
        for sign, vectors in terms:
            local = []
            zero = False
            for vector, (start, stop, multiplicity) in zip(vectors, slices):
                block = vector[start:stop].reshape(multiplicity, multiplicity)
                if not np.any(block):
                    zero = True
                    break
                local.append(block)
            if zero:
                continue
            contribution = np.kron(np.kron(local[0], local[1]), local[2]) % prime
            if sign == 1:
                matrix += contribution
            else:
                matrix -= contribution
            matrix %= prime
        result = rank_mod(matrix, prime, return_pivots=with_pivots)
        if with_pivots:
            ranks[shapes], pivots[shapes] = result
        else:
            ranks[shapes] = result
    if with_pivots:
        return ranks, pivots
    return ranks


def main():
    reference = None
    for prime in PRIMES:
        ranks, pivots = mixed_block_ranks(prime, with_pivots=True)
        total = sum(ranks.values())
        active = sum(rank > 0 for rank in ranks.values())
        assert total == EXPECTED_MIXED_RANK, (prime, total)
        assert active == EXPECTED_ACTIVE_BLOCKS, (prime, active)
        if reference is None:
            reference = ranks
        else:
            assert ranks == reference
        serialized = repr(tuple(sorted(pivots.items()))).encode()
        digest = hashlib.sha256(serialized).hexdigest()
        if EXPECTED_PIVOT_SHA256 != "TO_BE_FILLED":
            assert digest == EXPECTED_PIVOT_SHA256
        print(f"prime {prime}: mixed rank {total}, active blocks {active}")
        print("  pivot-basis sha256:", digest)
    print("exact finite-field product-DTH face certificate passed")
    print("rational mixed-face rank is at least 2266")


if __name__ == "__main__":
    main()
