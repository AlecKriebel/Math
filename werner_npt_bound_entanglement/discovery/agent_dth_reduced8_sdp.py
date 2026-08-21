#!/usr/bin/env python3
"""Solve the exact-product-face DTH relaxation on its 8D intersection.

The input basis is the eight unit-principal-angle vectors found by
``agent_dth_linear_angles.py``.  On the physical-product mixed face the
ninth principal eigenvalue is about 0.4872, so these eight vectors isolate
the complete common Hermitian linear intersection at discovery precision.

This script compresses every holomorphic and mixed PSD block to an affine
matrix pencil in eight real variables and solves the resulting spectrahedron.
It is a numerical discovery tool; an exact theorem requires a rational basis
and an exact certificate for the reduced pencils.
"""

from __future__ import annotations

import argparse

import cvxpy as cp
import numpy as np
import scipy.linalg as la

import agent_dth_invariant_crossing as cross
import agent_dth_linear_angles as angles
import agent_dth_primal_admm as primal


def block_pencils(tensors, blocks, field):
    pencils = []
    for block in blocks:
        basis = block[field]
        if not basis.shape[1]:
            continue
        matrices = []
        for tensor in tensors:
            matrix = primal.get_block(
                tensor, block["indices"], block["dimensions"])
            matrix = basis.T @ ((matrix + matrix.T) / 2) @ basis
            matrices.append(matrix)
        pencils.append((block["shapes"], np.asarray(matrices)))
    return pencils


def evaluate_pencils(coefficients, pencils):
    data = []
    for shapes, matrices in pencils:
        matrix = np.tensordot(coefficients, matrices, axes=1)
        values = la.eigvalsh((matrix + matrix.T) / 2)
        data.append((float(values[0]), shapes, values))
    return sorted(data)


def solve_with(solver, variable, constraints, objective, args):
    problem = cp.Problem(cp.Minimize(objective), constraints)
    options = {"verbose": args.verbose}
    if solver == "CLARABEL":
        options.update(tol_gap_abs=args.tolerance,
                       tol_feas=args.tolerance,
                       tol_gap_rel=args.tolerance,
                       max_iter=args.max_iterations)
    elif solver == "SCS":
        options.update(eps=args.tolerance,
                       max_iters=args.max_iterations)
    value = problem.solve(solver=solver, **options)
    return problem.status, value, np.array(variable.value).reshape(-1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--product-face", required=True)
    parser.add_argument("--angles", required=True)
    parser.add_argument("--solver", choices=("CLARABEL", "SCS"),
                        default="CLARABEL")
    parser.add_argument("--tolerance", type=float, default=1e-9)
    parser.add_argument("--max-iterations", type=int, default=200000)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--save")
    args = parser.parse_args()

    crossing_data, hol, mixed = cross.local_crossing(verbose=False)
    local, hol_ranges, mixed_ranges = primal.normalized_local_crossing(
        crossing_data)
    target = cross.target_highest_weight_bases()
    support = cross.local_support_highest_blocks(mixed, target, verbose=False)
    hol_blocks, objective_tensor, trace_tensor = primal.prepare_hol_blocks(
        hol_ranges)
    mixed_blocks = primal.prepare_mixed_blocks(mixed_ranges, support)
    primal.restrict_mixed_blocks_to_product_face(
        mixed_blocks, np.load(args.product_face))

    codec = angles.HolSymmetricCodec(hol_blocks)
    angle_data = np.load(args.angles)
    values = angle_data["values"]
    select = np.flatnonzero(values > 1 - 1e-8)
    if len(select) != 8:
        raise RuntimeError(f"expected eight intersection directions, got {len(select)}")
    vectors = angle_data["vectors"][:, select]
    hol_tensors = [codec.decode(vectors[:, index])
                   for index in range(vectors.shape[1])]
    mixed_tensors = [primal.crossing_apply(local, tensor)
                     for tensor in hol_tensors]

    support_residuals = []
    for tensor in mixed_tensors:
        supported = np.zeros_like(tensor)
        for block in mixed_blocks:
            basis = block["kernel"]
            if not basis.shape[1]:
                continue
            matrix = primal.get_block(
                tensor, block["indices"], block["dimensions"])
            projected = basis @ (basis.T @ matrix @ basis) @ basis.T
            primal.put_block(supported, block["indices"], projected,
                             block["dimensions"])
        support_residuals.append(float(la.norm(tensor - supported)))
    print("intersection support residuals:", support_residuals)

    trace_coefficients = np.array([
        np.vdot(trace_tensor, tensor).real for tensor in hol_tensors])
    objective_coefficients = np.array([
        np.vdot(objective_tensor, tensor).real for tensor in hol_tensors])
    print("trace coefficients:", trace_coefficients)
    print("objective coefficients:", objective_coefficients)

    hol_pencils = block_pencils(hol_tensors, hol_blocks, "basis")
    mixed_pencils = block_pencils(mixed_tensors, mixed_blocks, "kernel")
    print("PSD pencils hol/mixed:", len(hol_pencils), len(mixed_pencils))

    coefficient = cp.Variable(8)
    constraints = [trace_coefficients @ coefficient == 1]
    for _, matrices in hol_pencils + mixed_pencils:
        expression = sum(coefficient[index] * matrices[index]
                         for index in range(8))
        constraints.append(expression >> 0)
    objective = objective_coefficients @ coefficient
    status, value, solution = solve_with(
        args.solver, coefficient, constraints, objective, args)
    print("solver/status/value:", args.solver, status, value)
    print("solution coefficients:", solution)
    print("trace/objective audit:",
          float(trace_coefficients @ solution),
          float(objective_coefficients @ solution))

    hol_spectrum = evaluate_pencils(solution, hol_pencils)
    mixed_spectrum = evaluate_pencils(solution, mixed_pencils)
    print("hol minimum and ten active:", hol_spectrum[0][0],
          [(x[0], x[1], int(np.sum(x[2] > 1e-7)))
           for x in hol_spectrum[:10]])
    print("mixed minimum and ten active:", mixed_spectrum[0][0],
          [(x[0], x[1], int(np.sum(x[2] > 1e-7)))
           for x in mixed_spectrum[:10]])

    if args.save:
        np.savez(args.save, coefficients=solution,
                 trace_coefficients=trace_coefficients,
                 objective_coefficients=objective_coefficients,
                 intersection_vectors=vectors,
                 intersection_values=values[select],
                 hol_tensors=np.asarray(hol_tensors),
                 mixed_tensors=np.asarray(mixed_tensors),
                 support_residuals=np.asarray(support_residuals),
                 solver=np.array(args.solver), status=np.array(status),
                 value=np.array(value))


if __name__ == "__main__":
    main()
