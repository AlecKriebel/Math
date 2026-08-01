#!/usr/bin/env python3
"""Bounded invariant dual search for the corrected first DTH cone.

This discovery program searches the restricted dual ansatz

    Y = C_s^* T C_s

with invariant Hermitian T on (wedge^2 H) tensor conjugate(H).  It maximizes
the common lower margin gamma in

    O_K - gamma I_K - Theta_1(Y)|_K >= 0

over every local-unitary highest-weight block of the holomorphic constraint
space K.  A nonnegative result is only a numerical discovery candidate until
the blocks are reconstructed and verified exactly.  A negative optimum only
refutes this restricted dual ansatz, not the primal cone.
"""

from __future__ import annotations

import argparse
import itertools
from functools import lru_cache

import cvxpy as cp
import numpy as np
import scipy.linalg as la

import agent_dth_invariant_crossing as cross


def parity(permutation):
    return -1 if sum(permutation[i] > permutation[j]
                     for i in range(len(permutation))
                     for j in range(i + 1, len(permutation))) % 2 else 1


def transposition(a, b):
    p = list(range(5))
    p[a], p[b] = p[b], p[a]
    return tuple(p)


@lru_cache(None)
def all_local_representations():
    hol = cross.hol_highest_weight_bases()
    result = []
    for h in hol:
        reps = {}
        for p in itertools.permutations(range(5)):
            reps[p] = h.T @ cross.permutation_matrix(p) @ h
        result.append(reps)
    return result


def kron3(a, b, c):
    return np.kron(np.kron(a, b), c)


def global_representation(shape_indices, permutation):
    reps = all_local_representations()
    return kron3(*(reps[lam][permutation] for lam in shape_indices))


def omega_local(hol_basis, first):
    retained = (2, 3) if first == 0 else (0, 1)
    raw = np.zeros((9, cross.LOCAL_DIM), dtype=float)
    for col, word in enumerate(cross.WORDS):
        eps = cross.CENSUS.epsilon(word[4], word[first], word[first + 1])
        if eps:
            row = 3 * word[retained[0]] + word[retained[1]]
            raw[row, col] = eps
    return raw @ hol_basis


@lru_cache(None)
def local_omega_data():
    hol = cross.hol_highest_weight_bases()
    return tuple((omega_local(h, 0), omega_local(h, 2)) for h in hol)


def hol_block(shape_indices, tol=2e-9):
    dimensions = [cross.HOL_MULTS[i] for i in shape_indices]
    size = int(np.prod(dimensions))
    identity = np.eye(size)

    p12 = (identity - global_representation(shape_indices,
                                             transposition(0, 1))) / 2
    p34 = (identity - global_representation(shape_indices,
                                             transposition(2, 3))) / 2
    pair_swap = (2, 3, 0, 1, 4)
    ppair = (identity + global_representation(shape_indices, pair_swap)) / 2
    a4 = np.zeros((size, size))
    for q in itertools.permutations(range(4)):
        p = tuple(q) + (4,)
        a4 += parity(q) * global_representation(shape_indices, p) / 24
    source = p12 @ p34 @ ppair @ (identity - a4)
    source = (source + source.T) / 2
    values, vectors = la.eigh(source)
    src = vectors[:, values > 1 - tol]

    omega = local_omega_data()
    o0 = kron3(*(omega[i][0] for i in shape_indices))
    o2 = kron3(*(omega[i][1] for i in shape_indices))
    constrained = (o0 + o2) @ src
    # scipy.null_space uses a relative cutoff.  Some representation blocks
    # have an Omega map which is identically zero, leaving only roundoff of
    # size ~1e-13; a relative cutoff would incorrectly declare that noise to
    # have positive rank.  Use the fixed absolute symmetry tolerance here.
    _, singular, vh = la.svd(constrained, full_matrices=True)
    rank = int(np.sum(singular > tol))
    kernel = vh[rank:, :].conj().T
    basis = src @ kernel

    def global_pair_antisym(first):
        locals_ = []
        for lam in shape_indices:
            r = all_local_representations()[lam][transposition(first, 4)]
            locals_.append((np.eye(r.shape[0]) - r) / 2)
        return kron3(*locals_)

    witness = (np.eye(size) / 4
               - global_pair_antisym(0)
               - global_pair_antisym(2))
    objective = basis.T @ witness @ basis
    objective = (objective + objective.T) / 2

    jucys = sum(global_representation(shape_indices, transposition(r, 4))
                 for r in range(4))
    support_scalar = basis.T @ jucys @ basis
    support_scalar = (support_scalar + support_scalar.T) / 2
    return basis, objective, support_scalar


def dual_coefficient(local_maps, hol_shapes, target_shapes, hol_basis):
    """Linear map vec(T_target) -> vec(Theta(C*TC)|K), C ordering."""
    maps = [local_maps[hol_shapes[s]][target_shapes[s]] for s in range(3)]
    target_dims = [cross.TARGET_MULTS[i] for i in target_shapes]
    mtot = int(np.prod(target_dims))
    k = hol_basis.shape[1]
    columns = np.zeros((k * k, mtot * mtot), dtype=complex)
    for a in range(mtot):
        for b in range(mtot):
            x = np.zeros((mtot, mtot), dtype=complex)
            x[a, b] = 1
            tensor = x.reshape((*target_dims, *target_dims))
            full = np.einsum(
                "ijab,klcd,mnef,acebdf->ikmjln",
                maps[0], maps[1], maps[2], tensor,
                optimize=True).reshape((hol_basis.shape[0],) * 2)
            restricted = hol_basis.conj().T @ full @ hol_basis
            columns[:, a * mtot + b] = restricted.reshape(-1)
    return np.real_if_close(columns, tol=1000)


def ordered_triples(n):
    return list(itertools.product(range(n), repeat=3))


def solve(args):
    hol = cross.hol_highest_weight_bases()
    local_maps, _ = cross.local_dual_support_map(hol, verbose=True)
    hol_triples = ordered_triples(len(cross.HOL_SHAPES))
    target_triples = ordered_triples(len(cross.TARGET_WEIGHTS))

    blocks = {}
    print("building hol K blocks")
    for count, shapes in enumerate(hol_triples, 1):
        basis, objective, support = hol_block(shapes)
        blocks[shapes] = (basis, objective, support)
        if args.verbose or (basis.shape[1]
                            and np.min(la.eigvalsh(objective)) < -1e-8):
            print(" ", "/".join(cross.HOL_NAMES[i] for i in shapes),
                  "K", basis.shape[1],
                  "O eig", np.round(la.eigvalsh(objective), 8))
        if count % 25 == 0:
            print(f"  {count}/{len(hol_triples)}")

    variables = {}
    for shapes in target_triples:
        n = int(np.prod([cross.TARGET_MULTS[i] for i in shapes]))
        variables[shapes] = cp.Variable((n, n), hermitian=True,
                                        name="T_" + "_".join(map(str, shapes)))
    gamma = cp.Variable(name="gamma")
    constraints = []

    print("building dual LMIs")
    coefficient_count = 0
    for count, shapes in enumerate(hol_triples, 1):
        basis, objective, _ = blocks[shapes]
        k = basis.shape[1]
        if not k:
            continue
        correction = 0
        for target_shapes in target_triples:
            matrix = dual_coefficient(local_maps, shapes, target_shapes, basis)
            if la.norm(matrix) < 1e-10:
                continue
            variable = variables[target_shapes]
            vector = cp.reshape(variable, (variable.shape[0] ** 2,), order="C")
            term = cp.reshape(matrix @ vector, (k, k), order="C")
            correction = correction + term
            coefficient_count += matrix.size
        constraints.append(objective - gamma * np.eye(k) - correction >> 0)
        if count % 20 == 0:
            print(f"  {count}/{len(hol_triples)}")
    print("coefficient scalars:", coefficient_count)

    problem = cp.Problem(cp.Maximize(gamma), constraints)
    options = {"verbose": args.solver_verbose}
    if args.solver == "SCS":
        options.update(eps=args.eps, max_iters=args.max_iters,
                       acceleration_lookback=20)
    value = problem.solve(solver=args.solver, **options)
    print("status:", problem.status)
    print("gamma:", value)
    print("constraint residual audit")
    minimum = float("inf")
    worst = None
    for shapes, constraint in zip(
            [s for s in hol_triples if blocks[s][0].shape[1]], constraints):
        eig = np.min(la.eigvalsh(constraint.args[0].value))
        if eig < minimum:
            minimum = eig
            worst = shapes
    print("  minimum LMI eigenvalue:", minimum)
    print("  worst block:", worst)
    print("  target block norms")
    for shapes, variable in variables.items():
        norm = la.norm(variable.value) if variable.value is not None else np.nan
        if norm > 1e-6:
            print("   ", "/".join(cross.TARGET_NAMES[i] for i in shapes), norm)
    return problem, variables, blocks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", choices=("SCS", "CLARABEL"), default="CLARABEL")
    parser.add_argument("--eps", type=float, default=2e-7)
    parser.add_argument("--max-iters", type=int, default=100000)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--solver-verbose", action="store_true")
    args = parser.parse_args()
    solve(args)


if __name__ == "__main__":
    main()
