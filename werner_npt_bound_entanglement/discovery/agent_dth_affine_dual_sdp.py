#!/usr/bin/env python3
"""Site-symmetric general affine-support dual search for first-level DTH.

The restricted ansatz C_s^* T C_s is replaced by the general affine ideal

    Y = C_s^* R + R^* C_s.

After local U(3)^3 twirling, one local equivariant Hom space has dimension
23.  Physical-site symmetrization reduces the global R coefficients to
Sym^3(R^23), of dimension 2300.  All input data in the chosen highest-weight
bases are real, so conjugation averaging permits a real coefficient vector.

This remains discovery code.  A nonnegative numerical margin must be
rationally/algebraically reconstructed and independently checked exactly.
"""

from __future__ import annotations

import argparse
import itertools

import cvxpy as cp
import numpy as np
import scipy.linalg as la

import agent_dth_dual_sdp as base
import agent_dth_invariant_crossing as cross


COMMON_MIXED = (1, 2, 4)  # 21, 10, 02


def local_hom_images(crossing, support_blocks):
    """A[lambda][alpha] = Theta(C_s^* r_alpha) on hol multiplicities."""
    images = [[] for _ in cross.HOL_SHAPES]
    labels = []
    for nu, mu in enumerate(COMMON_MIXED):
        c = support_blocks[nu]
        target_dim, input_dim = c.shape
        for a in range(target_dim):
            for b in range(input_dim):
                r = np.zeros((target_dim, input_dim))
                r[a, b] = 1.0
                y = c.T @ r
                labels.append((nu, a, b))
                for lam in range(len(cross.HOL_SHAPES)):
                    adjoint = cross.local_crossing_adjoint(crossing, lam, mu)
                    image = np.einsum("ijab,ab->ij", adjoint, y)
                    images[lam].append(np.real_if_close(image, tol=1000))
    assert len(labels) == 23
    assert all(len(row) == 23 for row in images)
    worst_imaginary = max(np.max(np.abs(np.imag(a)))
                          for row in images for a in row)
    print("local Hom dimension:", len(labels))
    print("local Hom image imaginary residual:", worst_imaginary)
    assert worst_imaginary < 1e-9
    return [[np.asarray(a, dtype=float) for a in row] for row in images], labels


def distinct_permutations(triple):
    return sorted(set(itertools.permutations(triple)))


def affine_coefficient(images, hol_shapes, hol_basis, alpha_triples):
    k = hol_basis.shape[1]
    out = np.zeros((k * k, len(alpha_triples)), dtype=float)
    for column, triple in enumerate(alpha_triples):
        full = np.zeros((hol_basis.shape[0],) * 2, dtype=float)
        for permuted in distinct_permutations(triple):
            term = np.kron(np.kron(images[hol_shapes[0]][permuted[0]],
                                   images[hol_shapes[1]][permuted[1]]),
                                   images[hol_shapes[2]][permuted[2]])
            full += term
        full += full.T
        restricted = hol_basis.T @ full @ hol_basis
        restricted = (restricted + restricted.T) / 2
        out[:, column] = restricted.reshape(-1)
    return out


def unordered_hol_triples():
    return list(itertools.combinations_with_replacement(
        range(len(cross.HOL_SHAPES)), 3))


def solve(args):
    crossing, hol, mixed = cross.local_crossing(verbose=True)
    target = cross.target_highest_weight_bases()
    support = cross.local_support_highest_blocks(mixed, target, verbose=True)
    images, labels = local_hom_images(crossing, support)
    alpha_triples = list(itertools.combinations_with_replacement(range(23), 3))
    assert len(alpha_triples) == 2300

    coefficient = cp.Variable(2300, name="R_sym3")
    gamma = cp.Variable(name="gamma")
    constraints = []
    blocks = []
    total_coefficients = 0

    print("building 35 site-symmetric hol LMIs")
    for number, shapes in enumerate(unordered_hol_triples(), 1):
        basis, objective, _ = base.hol_block(shapes)
        k = basis.shape[1]
        if not k:
            continue
        matrix = affine_coefficient(images, shapes, basis, alpha_triples)
        correction = cp.reshape(matrix @ coefficient, (k, k), order="C")
        constraints.append(objective - gamma * np.eye(k) - correction >> 0)
        blocks.append((shapes, basis, objective, matrix))
        total_coefficients += matrix.size
        print(f" {number:2d}/35",
              "/".join(cross.HOL_NAMES[i] for i in shapes),
              "K", k,
              "O inertia",
              (int(np.sum(la.eigvalsh(objective) > 1e-8)),
               int(np.sum(la.eigvalsh(objective) < -1e-8)),
               int(np.sum(np.abs(la.eigvalsh(objective)) <= 1e-8))))
    print("real variables: 2301")
    print("stored coefficient scalars:", total_coefficients)

    problem = cp.Problem(cp.Maximize(gamma), constraints)
    options = {"verbose": args.solver_verbose}
    if args.solver == "SCS":
        options.update(eps=args.eps, max_iters=args.max_iters,
                       acceleration_lookback=20)
    value = problem.solve(solver=args.solver, **options)
    print("status:", problem.status)
    print("gamma:", value)

    minimum = float("inf")
    worst = None
    residuals = []
    for (shapes, _, objective, matrix), constraint in zip(blocks, constraints):
        lhs = objective - value * np.eye(objective.shape[0]) \
            - (matrix @ coefficient.value).reshape(objective.shape)
        eig = float(np.min(la.eigvalsh((lhs + lhs.T) / 2)))
        residuals.append((eig, shapes))
        if eig < minimum:
            minimum, worst = eig, shapes
    print("minimum reconstructed LMI eigenvalue:", minimum)
    print("worst block:", "/".join(cross.HOL_NAMES[i] for i in worst))
    print("ten smallest block margins:")
    for eig, shapes in sorted(residuals)[:10]:
        print(" ", f"{eig:.10g}",
              "/".join(cross.HOL_NAMES[i] for i in shapes))
    print("coefficient norm/max:", la.norm(coefficient.value),
          np.max(np.abs(coefficient.value)))
    if args.save:
        np.savez(args.save,
                 gamma=np.array(value),
                 coefficient=coefficient.value,
                 alpha_triples=np.array(alpha_triples, dtype=int),
                 hom_labels=np.array(labels, dtype=int))
        print("saved", args.save)
    return problem, coefficient, blocks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", choices=("SCS", "CLARABEL"), default="CLARABEL")
    parser.add_argument("--eps", type=float, default=2e-7)
    parser.add_argument("--max-iters", type=int, default=100000)
    parser.add_argument("--solver-verbose", action="store_true")
    parser.add_argument("--save")
    args = parser.parse_args()
    solve(args)


if __name__ == "__main__":
    main()
