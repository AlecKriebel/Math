#!/usr/bin/env python3
"""Numerical local crossing data for the corrected first DTH cone.

Discovery code only.  It constructs the covariant Schur multiplicity spaces
inside (C^3)^tensor5 and the highest-weight multiplicity spaces of the mixed
module conjugate(C^3)^tensor2 tensor (C^3)^tensor3.  Partial transpose of
local permutation-algebra matrix units then gives the 6 by 5 family of local
crossing superoperators used by the invariant SDP.

No numerical conclusion produced by this file is a theorem.  Every eventual
certificate must be reconstructed and checked independently over exact
arithmetic.
"""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path

import numpy as np
import scipy.linalg as la


HERE = Path(__file__).resolve().parent
VERIFY = HERE.parent / "verification" / "agent_dth_block_census.py"
SPEC = importlib.util.spec_from_file_location("dth_census", VERIFY)
CENSUS = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CENSUS)

D = 3
NREP = 5
LOCAL_DIM = D**NREP

HOL_SHAPES = CENSUS.PARTITIONS
HOL_NAMES = ("5", "41", "32", "311", "221")
HOL_CARRIER_DIMS = (21, 24, 15, 6, 3)
HOL_MULTS = (1, 4, 5, 6, 5)

MIXED_WEIGHTS = ((3, 2), (2, 1), (1, 0), (1, 3), (0, 2), (4, 0))
MIXED_NAMES = ("32", "21", "10", "13", "02", "40")
MIXED_CARRIER_DIMS = (42, 15, 3, 24, 6, 15)
MIXED_MULTS = (1, 6, 6, 2, 5, 1)

TARGET_WEIGHTS = ((2, 1), (1, 0), (0, 2))
TARGET_NAMES = ("21", "10", "02")
TARGET_CARRIER_DIMS = (15, 3, 6)
TARGET_MULTS = (1, 2, 1)


def words():
    return list(itertools.product(range(D), repeat=NREP))


WORDS = words()
WORD_INDEX = {w: i for i, w in enumerate(WORDS)}


def sparse_word_columns(vectors):
    out = np.zeros((LOCAL_DIM, len(vectors)), dtype=float)
    for j, vector in enumerate(vectors):
        for word, value in vector.items():
            out[WORD_INDEX[word], j] = float(value)
    return out


def orthonormal_columns(a, tol=1e-11):
    q, r = la.qr(a, mode="economic")
    rank = int(np.sum(np.abs(np.diag(r)) > tol))
    if rank != a.shape[1]:
        raise RuntimeError(f"column rank {rank}, expected {a.shape[1]}")
    return q[:, :rank]


def hol_highest_weight_bases():
    result = []
    for shape, expected in zip(HOL_SHAPES, HOL_MULTS):
        raw = sparse_word_columns(CENSUS.specht_basis(shape))
        assert raw.shape[1] == expected
        result.append(orthonormal_columns(raw))
    return result


def mixed_weight(word):
    counts = [0, 0, 0]
    for r in (2, 3, 4):
        counts[word[r]] += 1
    for r in (0, 1):
        counts[word[r]] -= 1
    return tuple(counts)


def highest_gl_weight(pq):
    p, q = pq
    w2 = (1 - p - 2 * q) // 3
    assert 3 * w2 == 1 - p - 2 * q
    return (w2 + q + p, w2 + q, w2)


def raised_word(word, simple_root):
    """Terms in E_01 or E_12 acting on the mixed local tensor module."""
    lo = simple_root + 1
    hi = simple_root
    for position in range(NREP):
        value = word[position]
        if position < 2:  # contravariant: -E_(lo,hi)
            if value == hi:
                new = list(word)
                new[position] = lo
                yield tuple(new), -1.0
        else:  # covariant: E_(hi,lo)
            if value == lo:
                new = list(word)
                new[position] = hi
                yield tuple(new), 1.0


def raising_matrix(source_indices, simple_root):
    rows = {}
    terms = []
    for j, index in enumerate(source_indices):
        for word, coeff in raised_word(WORDS[index], simple_root):
            if word not in rows:
                rows[word] = len(rows)
            terms.append((rows[word], j, coeff))
    out = np.zeros((len(rows), len(source_indices)), dtype=float)
    for i, j, coeff in terms:
        out[i, j] += coeff
    return out


def mixed_highest_weight_bases(tol=1e-10):
    result = []
    for pq, expected in zip(MIXED_WEIGHTS, MIXED_MULTS):
        weight = highest_gl_weight(pq)
        indices = [i for i, word in enumerate(WORDS)
                   if mixed_weight(word) == weight]
        stacked = np.vstack((raising_matrix(indices, 0),
                             raising_matrix(indices, 1)))
        kernel = la.null_space(stacked, rcond=tol)
        if kernel.shape[1] != expected:
            raise RuntimeError(
                f"mixed {pq}: kernel {kernel.shape[1]}, expected {expected}")
        full = np.zeros((LOCAL_DIM, expected), dtype=float)
        full[indices, :] = kernel
        result.append(full)
    return result


def permute_word(word, permutation):
    out = [None] * NREP
    for old in range(NREP):
        out[permutation[old]] = word[old]
    return tuple(out)


def permutation_matrix(permutation):
    out = np.zeros((LOCAL_DIM, LOCAL_DIM), dtype=float)
    for j, word in enumerate(WORDS):
        out[WORD_INDEX[permute_word(word, permutation)], j] = 1.0
    return out


def partial_transpose_first_pair(operator):
    tensor = operator.reshape((D, D, D, D, D) * 2)
    axes = list(range(10))
    axes[0], axes[5] = axes[5], axes[0]
    axes[1], axes[6] = axes[6], axes[1]
    return tensor.transpose(axes).reshape((LOCAL_DIM, LOCAL_DIM))


def flatten_blocks(blocks):
    return np.concatenate([x.reshape(-1) for x in blocks])


def local_crossing(verbose=True):
    """Return T[mu][lambda] with shape (m_mu,m_mu,f_lam,f_lam)."""
    hol = hol_highest_weight_bases()
    mixed = mixed_highest_weight_bases()
    permutations = list(itertools.permutations(range(NREP)))
    pmats = [permutation_matrix(p) for p in permutations]

    restriction_columns = []
    mixed_restrictions = []
    for pmat in pmats:
        restriction_columns.append(flatten_blocks(
            [h.T @ pmat @ h for h in hol]))
        crossed = partial_transpose_first_pair(pmat)
        mixed_restrictions.append(
            [m.T @ crossed @ m for m in mixed])
    restriction = np.column_stack(restriction_columns)
    q, r, pivots = la.qr(restriction, mode="economic", pivoting=True)
    rank = int(np.sum(np.abs(np.diag(r)) > 1e-9))
    assert rank == 103
    selected = list(pivots[:rank])
    square = restriction[:, selected]

    crossing = [[None for _ in HOL_SHAPES] for _ in MIXED_WEIGHTS]
    offset = 0
    residual_max = 0.0
    trace_errors = []
    for lam, (f, carrier_dim) in enumerate(zip(HOL_MULTS,
                                                HOL_CARRIER_DIMS)):
        for a in range(f):
            for b in range(f):
                target = np.zeros(103)
                target[offset + a * f + b] = 1.0 / carrier_dim
                coeff = la.solve(square, target)
                residual_max = max(residual_max,
                                   la.norm(square @ coeff - target))
                for mu, (m, mixed_dim) in enumerate(zip(MIXED_MULTS,
                                                        MIXED_CARRIER_DIMS)):
                    block = sum(coeff[j] * mixed_restrictions[s][mu]
                                for j, s in enumerate(selected))
                    if crossing[mu][lam] is None:
                        crossing[mu][lam] = np.zeros((m, m, f, f))
                    crossing[mu][lam][:, :, a, b] = block
                # Partial transpose is trace preserving.
                crossed_trace = sum(
                    mixed_dim * np.trace(crossing[mu][lam][:, :, a, b])
                    for mu, mixed_dim in enumerate(MIXED_CARRIER_DIMS))
                trace_errors.append(abs(crossed_trace - (1.0 if a == b else 0.0)))
        offset += f * f
    assert offset == 103

    adjoint_error = 0.0
    for row in crossing:
        for t in row:
            adjoint_error = max(adjoint_error,
                                np.max(np.abs(t.transpose(1, 0, 3, 2) - t)))
    if verbose:
        print("local crossing diagnostics")
        print("  covariant commutant rank:", rank)
        print("  inversion residual:", residual_max)
        print("  trace error:", max(trace_errors))
        print("  adjoint error:", adjoint_error)
        print("  local nonzero pattern (mixed rows, hol columns)")
        for mu, row in enumerate(crossing):
            print(" ", MIXED_NAMES[mu],
                  [HOL_NAMES[lam] for lam, t in enumerate(row)
                   if la.norm(t) > 1e-9])
    assert residual_max < 1e-8
    assert max(trace_errors) < 1e-7
    assert adjoint_error < 1e-7
    return crossing, hol, mixed


def target_words():
    return list(itertools.product(range(D), repeat=3))


TARGET_WORDS = target_words()
TARGET_INDEX = {w: i for i, w in enumerate(TARGET_WORDS)}


def target_weight(word):
    counts = [0, 0, 0]
    for r in (0, 1):
        counts[word[r]] += 1
    counts[word[2]] -= 1
    return tuple(counts)


def target_raised_word(word, simple_root):
    lo = simple_root + 1
    hi = simple_root
    for position in range(3):
        value = word[position]
        if position == 2:
            if value == hi:
                new = list(word)
                new[position] = lo
                yield tuple(new), -1.0
        elif value == lo:
            new = list(word)
            new[position] = hi
            yield tuple(new), 1.0


def target_raising_matrix(source_indices, simple_root):
    rows = {}
    terms = []
    for j, index in enumerate(source_indices):
        for word, coeff in target_raised_word(TARGET_WORDS[index], simple_root):
            if word not in rows:
                rows[word] = len(rows)
            terms.append((rows[word], j, coeff))
    out = np.zeros((len(rows), len(source_indices)), dtype=float)
    for i, j, coeff in terms:
        out[i, j] += coeff
    return out


def target_highest_weight_bases(tol=1e-10):
    result = []
    for pq, expected in zip(TARGET_WEIGHTS, TARGET_MULTS):
        weight = highest_gl_weight(pq)
        indices = [i for i, word in enumerate(TARGET_WORDS)
                   if target_weight(word) == weight]
        stacked = np.vstack((target_raising_matrix(indices, 0),
                             target_raising_matrix(indices, 1)))
        kernel = la.null_space(stacked, rcond=tol)
        if kernel.shape[1] != expected:
            raise RuntimeError(
                f"target {pq}: kernel {kernel.shape[1]}, expected {expected}")
        full = np.zeros((D**3, expected), dtype=float)
        full[indices, :] = kernel
        result.append(full)
    return result


def target_commutant_generators():
    """The six-dimensional commutant of 3 tensor 3 tensor bar(3)."""
    identity = np.eye(D**3)
    swap = np.zeros_like(identity)
    for j, word in enumerate(TARGET_WORDS):
        swap[TARGET_INDEX[(word[1], word[0], word[2])], j] = 1.0

    def contraction(covariant_position):
        out = np.zeros_like(identity)
        other = 1 - covariant_position
        for col, word in enumerate(TARGET_WORDS):
            # |a,bar(a)><b,bar(b)| on the selected covariant/bar pair.
            if word[covariant_position] != word[2]:
                continue
            for a in range(D):
                new = list(word)
                new[covariant_position] = a
                new[2] = a
                out[TARGET_INDEX[tuple(new)], col] += 1.0
        return out

    e13 = contraction(0)
    e23 = contraction(1)
    return (identity, swap, e13, e23,
            swap @ e23 + e23 @ swap,
            1j * (swap @ e23 - e23 @ swap))


def mixed_support_matrix():
    """Raw local C_s: (bar3)^2 3^3 -> 3^2 bar3."""
    out = np.zeros((D**3, LOCAL_DIM), dtype=float)
    for col, word in enumerate(WORDS):
        if word[0] == word[4]:
            target = (word[2], word[3], word[1])
            out[TARGET_INDEX[target], col] = 1.0
    return out


def local_dual_support_map(hol=None, verbose=True):
    """Return U[lambda][nu] with shape (f,f,m,m).

    If a target invariant operator has highest-weight block T_nu, then
    partial_transpose(C_s^* T C_s) has covariant highest-weight block
    sum_nu U[lambda][nu](T_nu).
    """
    if hol is None:
        hol = hol_highest_weight_bases()
    target = target_highest_weight_bases()
    generators = target_commutant_generators()
    restriction = np.column_stack([
        flatten_blocks([h.conj().T @ g @ h for h in target])
        for g in generators
    ])
    assert np.linalg.matrix_rank(restriction, tol=1e-9) == 6
    support = mixed_support_matrix()
    result = [[None for _ in TARGET_WEIGHTS] for _ in HOL_SHAPES]
    residual = 0.0
    offset = 0
    for nu, m in enumerate(TARGET_MULTS):
        for a in range(m):
            for b in range(m):
                rhs = np.zeros(6, dtype=complex)
                rhs[offset + a * m + b] = 1.0
                coeff = la.solve(restriction, rhs)
                residual = max(residual, la.norm(restriction @ coeff - rhs))
                target_operator = sum(c * g for c, g in zip(coeff, generators))
                mixed_operator = support.conj().T @ target_operator @ support
                hol_operator = partial_transpose_first_pair(mixed_operator)
                for lam, (h, f) in enumerate(zip(hol, HOL_MULTS)):
                    block = h.conj().T @ hol_operator @ h
                    if result[lam][nu] is None:
                        result[lam][nu] = np.zeros((f, f, m, m), complex)
                    result[lam][nu][:, :, a, b] = block
        offset += m * m
    assert offset == 6
    adjoint_error = max(
        np.max(np.abs(t.transpose(1, 0, 3, 2).conj() - t))
        for row in result for t in row)
    if verbose:
        print("local dual-support diagnostics")
        print("  target commutant rank: 6")
        print("  inversion residual:", residual)
        print("  adjoint error:", adjoint_error)
        print("  nonzero pattern (hol rows, target columns)")
        for lam, row in enumerate(result):
            print(" ", HOL_NAMES[lam],
                  [TARGET_NAMES[nu] for nu, t in enumerate(row)
                   if la.norm(t) > 1e-9])
    assert residual < 1e-9
    assert adjoint_error < 1e-8
    return result, target


def local_support_highest_blocks(mixed=None, target=None, verbose=True):
    """Highest-weight matrices of C_s on the three common mixed types."""
    if mixed is None:
        mixed = mixed_highest_weight_bases()
    if target is None:
        target = target_highest_weight_bases()
    support = mixed_support_matrix()
    # target 21,10,02 correspond to mixed 21,10,02.
    mixed_indices = (1, 2, 4)
    blocks = []
    for nu, mu in enumerate(mixed_indices):
        block = target[nu].conj().T @ support @ mixed[mu]
        blocks.append(block)
        if verbose:
            print("support highest block", TARGET_NAMES[nu],
                  block.shape, "rank", np.linalg.matrix_rank(block, 1e-9),
                  "singular", np.round(la.svdvals(block), 10))
    return blocks


def local_crossing_adjoint(crossing, lam, mu):
    """Map a mixed highest block Y to the covariant hol dual block.

    Returned tensor A[i,j,a,b] satisfies H_ij=A[i,j,a,b]Y_ab.  The mixed
    carrier dimension is included, so raw invariant Hilbert-space traces are
    paired correctly against the normalized covariant density convention.
    """
    t = crossing[mu][lam]
    return MIXED_CARRIER_DIMS[mu] * t.transpose(3, 2, 1, 0)


def audit_affine_support_adjoint(crossing, hol, mixed, tol=2e-8):
    """Check the crossing adjoint against direct C_s^* T C_s restriction."""
    direct, target = local_dual_support_map(hol, verbose=False)
    support_blocks = local_support_highest_blocks(mixed, target, verbose=False)
    mixed_indices = (1, 2, 4)
    rng = np.random.default_rng(20260731)
    worst = 0.0
    for nu, mu in enumerate(mixed_indices):
        m = TARGET_MULTS[nu]
        x = rng.normal(size=(m, m)) + 1j * rng.normal(size=(m, m))
        x = (x + x.conj().T) / 2
        y = support_blocks[nu].conj().T @ x @ support_blocks[nu]
        for lam in range(len(HOL_SHAPES)):
            via_crossing = np.einsum(
                "ijab,ab->ij", local_crossing_adjoint(crossing, lam, mu), y)
            via_direct = np.einsum("ijab,ab->ij", direct[lam][nu], x)
            worst = max(worst, la.norm(via_crossing - via_direct))
    print("affine-support/crossing adjoint audit:", worst)
    assert worst < tol
    return support_blocks


if __name__ == "__main__":
    crossing_data, hol_bases, mixed_bases = local_crossing()
    local_dual_support_map(hol_bases)
    audit_affine_support_adjoint(crossing_data, hol_bases, mixed_bases)
