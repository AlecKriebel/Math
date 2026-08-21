#!/usr/bin/env python3
"""Matrix-free invariant ADMM for the corrected first-degree DTH cone.

The local covariant and mixed commutants both have dimension 103.  In
Hilbert--Schmidt normalized Schur coordinates, partial transpose is a real
orthogonal 103 by 103 crossing matrix locally and its three-site action is
the tensor cube.  This permits the full invariant primal relaxation to be
explored without constructing the 3,326,427-dimensional ambient matrices or
any dense million-by-million superoperator.

The program solves, at discovery precision,

  min <O0tilde,rho>
  s.t. rho >= 0, ran(rho) in K_hol, Tr rho=1,
       rho^Gamma >= 0, ran(rho^Gamma) in ker(C_s).

ADMM output is numerical evidence only.  A negative point must be compressed,
reconstructed exactly, and checked by a separate exact verifier.
"""

from __future__ import annotations

import argparse
import itertools
import time

import numpy as np
import scipy.linalg as la

import agent_dth_dual_sdp as hol_data
import agent_dth_invariant_crossing as cross


def normalized_local_crossing(data):
    matrix = np.zeros((103, 103), dtype=float)
    in_offset = 0
    input_ranges = []
    for lam, (f, dlam) in enumerate(zip(cross.HOL_MULTS,
                                        cross.HOL_CARRIER_DIMS)):
        input_ranges.append(np.arange(in_offset, in_offset + f * f)
                            .reshape(f, f))
        out_offset = 0
        for mu, (m, dmu) in enumerate(zip(cross.MIXED_MULTS,
                                          cross.MIXED_CARRIER_DIMS)):
            block = np.sqrt(dlam * dmu) * data[mu][lam]
            matrix[out_offset:out_offset + m * m,
                   in_offset:in_offset + f * f] = block.reshape(m * m, f * f)
            out_offset += m * m
        assert out_offset == 103
        in_offset += f * f
    assert in_offset == 103
    output_ranges = []
    offset = 0
    for m in cross.MIXED_MULTS:
        output_ranges.append(np.arange(offset, offset + m * m).reshape(m, m))
        offset += m * m
    error = la.norm(matrix.T @ matrix - np.eye(103), ord=2)
    print("normalized local crossing orthogonality error:", error)
    assert error < 2e-8
    return matrix, input_ranges, output_ranges


def block_indices(local_ranges, shapes):
    grids = [local_ranges[s] for s in shapes]
    return (grids[0][:, None, None, :, None, None],
            grids[1][None, :, None, None, :, None],
            grids[2][None, None, :, None, None, :])


def put_block(tensor, indices, matrix, dimensions):
    tensor[indices] = matrix.reshape((*dimensions, *dimensions))


def get_block(tensor, indices, dimensions):
    n = int(np.prod(dimensions))
    return tensor[indices].reshape(n, n)


def crossing_apply(local, tensor, transpose=False):
    u = local.T if transpose else local
    # Three BLAS-friendly mode products.  Keeping the transformed mode in
    # place avoids forming the dense tensor-cube superoperator.
    out = np.tensordot(u, tensor, axes=(1, 0))
    out = np.tensordot(u, out, axes=(1, 1)).transpose(1, 0, 2)
    out = np.tensordot(u, out, axes=(1, 2)).transpose(1, 2, 0)
    return out


def prepare_hol_blocks(local_ranges):
    blocks = []
    objective_tensor = np.zeros((103, 103, 103), dtype=float)
    trace_tensor = np.zeros_like(objective_tensor)
    for shapes in itertools.product(range(5), repeat=3):
        basis, objective, _ = hol_data.hol_block(shapes)
        dimensions = tuple(cross.HOL_MULTS[s] for s in shapes)
        indices = block_indices(local_ranges, shapes)
        carrier = int(np.prod([cross.HOL_CARRIER_DIMS[s] for s in shapes]))
        weight = np.sqrt(carrier)
        full_objective = basis @ objective @ basis.T
        full_trace = basis @ basis.T
        put_block(objective_tensor, indices, weight * full_objective, dimensions)
        put_block(trace_tensor, indices, weight * full_trace, dimensions)
        blocks.append({"shapes": shapes, "dimensions": dimensions,
                       "indices": indices, "basis": basis,
                       "objective": objective, "weight": weight})
    return blocks, objective_tensor, trace_tensor


def absolute_null_space(matrix, tol=2e-9):
    _, singular, vh = la.svd(matrix, full_matrices=True)
    rank = int(np.sum(singular > tol))
    return vh[rank:, :].conj().T


def prepare_mixed_blocks(local_ranges, support_blocks):
    blocks = []
    common = {1: 0, 2: 1, 4: 2}
    for shapes in itertools.product(range(6), repeat=3):
        dimensions = tuple(cross.MIXED_MULTS[s] for s in shapes)
        n = int(np.prod(dimensions))
        indices = block_indices(local_ranges, shapes)
        if all(s in common for s in shapes):
            c = np.kron(np.kron(support_blocks[common[shapes[0]]],
                                support_blocks[common[shapes[1]]]),
                                support_blocks[common[shapes[2]]])
            kernel = absolute_null_space(c)
        else:
            kernel = np.eye(n)
        blocks.append({"shapes": shapes, "dimensions": dimensions,
                       "indices": indices, "kernel": kernel})
    return blocks


def restrict_mixed_blocks_to_exposed_face(blocks, face_tensor, tolerance=1e-9):
    """Replace each L block by ker(P_L face_tensor P_L)."""
    total_before = sum(block["kernel"].shape[1] for block in blocks)
    total_after = 0
    positive_rank = 0
    for block in blocks:
        kernel = block["kernel"]
        if not kernel.shape[1]:
            continue
        matrix = get_block(face_tensor, block["indices"], block["dimensions"])
        compressed = kernel.T @ ((matrix + matrix.T) / 2) @ kernel
        values, vectors = la.eigh(compressed)
        keep = values < tolerance
        positive_rank += int(np.sum(~keep))
        block["kernel"] = kernel @ vectors[:, keep]
        total_after += block["kernel"].shape[1]
    print("mixed exposed-face restriction:", total_before, "->", total_after,
          "exposed rank", positive_rank, "tolerance", tolerance)
    return blocks


def restrict_mixed_blocks_to_product_face(blocks, checkpoint):
    """Use block range bases reconstructed from exact physical product twirls.

    The checkpoint convention is ``L_ijk @ q_ijk`` in the full mixed
    multiplicity block, where ``L`` is the original support kernel and ``q``
    is an orthonormal face basis in its coordinates.
    """
    total_before = sum(block["kernel"].shape[1] for block in blocks)
    total_after = 0
    maximum_orthogonality_error = 0.0
    for block in blocks:
        key = "".join(str(s) for s in block["shapes"])
        basis = checkpoint[f"L_{key}"] @ checkpoint[f"q_{key}"]
        expected_rows = int(np.prod(block["dimensions"]))
        assert basis.shape[0] == expected_rows
        if basis.shape[1]:
            error = la.norm(basis.T @ basis - np.eye(basis.shape[1]), ord=2)
            maximum_orthogonality_error = max(maximum_orthogonality_error,
                                               float(error))
        block["kernel"] = basis
        total_after += basis.shape[1]
    print("mixed exact-product-face restriction:", total_before, "->",
          total_after, "max basis orthogonality error",
          maximum_orthogonality_error)
    assert maximum_orthogonality_error < 1e-8
    return blocks


def positive_part(matrix):
    matrix = (matrix + matrix.T) / 2
    values, vectors = la.eigh(matrix)
    positive = np.maximum(values, 0)
    return (vectors * positive) @ vectors.T


def project_mixed(tensor, blocks):
    out = np.zeros_like(tensor)
    for block in blocks:
        matrix = get_block(tensor, block["indices"], block["dimensions"])
        kernel = block["kernel"]
        compressed = kernel.T @ ((matrix + matrix.T) / 2) @ kernel
        projected = kernel @ positive_part(compressed) @ kernel.T
        put_block(out, block["indices"], projected, block["dimensions"])
    return out


def project_hol_trace_one(tensor, blocks):
    spectral = []
    upper = -np.inf
    for block in blocks:
        basis = block["basis"]
        if not basis.shape[1]:
            spectral.append(None)
            continue
        matrix = get_block(tensor, block["indices"], block["dimensions"])
        compressed = basis.T @ ((matrix + matrix.T) / 2) @ basis
        values, vectors = la.eigh(compressed)
        weight = block["weight"]
        upper = max(upper, float(np.max(values / weight)))
        spectral.append((values, vectors, weight))

    def weighted_trace(threshold):
        return sum(weight * np.sum(np.maximum(values - threshold * weight, 0))
                   for item in spectral if item is not None
                   for values, _, weight in (item,))

    lower = min(-1.0, upper - 1.0)
    while weighted_trace(lower) < 1:
        lower = 2 * lower - upper
    for _ in range(80):
        middle = (lower + upper) / 2
        if weighted_trace(middle) > 1:
            lower = middle
        else:
            upper = middle
    threshold = (lower + upper) / 2

    out = np.zeros_like(tensor)
    for block, item in zip(blocks, spectral):
        if item is None:
            continue
        values, vectors, weight = item
        positive = np.maximum(values - threshold * weight, 0)
        compressed = (vectors * positive) @ vectors.T
        basis = block["basis"]
        projected = basis @ compressed @ basis.T
        put_block(out, block["indices"], projected, block["dimensions"])
    return out


def cone_minimum_eigenvalue(tensor, blocks, mixed=False):
    minimum = np.inf
    worst = None
    for block in blocks:
        matrix = get_block(tensor, block["indices"], block["dimensions"])
        if mixed:
            basis = block["kernel"]
        else:
            basis = block["basis"]
        if not basis.shape[1]:
            continue
        compressed = basis.T @ ((matrix + matrix.T) / 2) @ basis
        value = float(np.min(la.eigvalsh(compressed)))
        if value < minimum:
            minimum, worst = value, block["shapes"]
    return minimum, worst


def solve(args):
    crossing, hol, mixed = cross.local_crossing(verbose=True)
    local, hol_ranges, mixed_ranges = normalized_local_crossing(crossing)
    target = cross.target_highest_weight_bases()
    support = cross.local_support_highest_blocks(mixed, target, verbose=True)

    print("preparing 125 hol blocks")
    hol_blocks, objective, trace = prepare_hol_blocks(hol_ranges)
    print("preparing 216 mixed blocks")
    mixed_blocks = prepare_mixed_blocks(mixed_ranges, support)
    if args.mixed_face and args.product_face:
        raise ValueError("choose only one of --mixed-face and --product-face")
    if args.product_face:
        restrict_mixed_blocks_to_product_face(
            mixed_blocks, np.load(args.product_face))
    elif args.mixed_face:
        face_checkpoint = np.load(args.mixed_face)
        face_tensor = face_checkpoint[args.mixed_face_field]
        restrict_mixed_blocks_to_exposed_face(
            mixed_blocks, face_tensor, args.face_tol)
    print("hol supported dimensions:", sum(b["basis"].shape[1] for b in hol_blocks))
    print("mixed supported dimensions:", sum(b["kernel"].shape[1] for b in mixed_blocks))

    if args.load:
        checkpoint = np.load(args.load)
        x = checkpoint["x"]
        z = checkpoint["z"]
        dual = checkpoint["dual"] * (args.load_rho / args.rho)
        print("loaded", args.load, "and rescaled dual from rho",
              args.load_rho, "to", args.rho)
    else:
        # A deterministic trace-one hol start, followed by a mixed projection.
        x = project_hol_trace_one(
            -args.objective_scale * objective / max(args.rho, 1e-12),
            hol_blocks)
        ux = crossing_apply(local, x)
        z = project_mixed(ux, mixed_blocks)
        dual = np.zeros_like(x)
    previous_z = z.copy()
    start = time.time()

    for iteration in range(1, args.iterations + 1):
        v = (crossing_apply(local, z - dual, transpose=True)
             - args.objective_scale * objective / args.rho)
        x = project_hol_trace_one(v, hol_blocks)
        ux = crossing_apply(local, x)
        relaxed = args.alpha * ux + (1 - args.alpha) * z
        z = project_mixed(relaxed + dual, mixed_blocks)
        dual += relaxed - z

        if iteration == 1 or iteration % args.report == 0:
            primal = la.norm(ux - z)
            dual_residual = args.rho * la.norm(z - previous_z)
            value = float(np.vdot(objective, x).real)
            trace_value = float(np.vdot(trace, x).real)
            hol_min, hol_worst = cone_minimum_eigenvalue(x, hol_blocks)
            mix_min, mix_worst = cone_minimum_eigenvalue(z, mixed_blocks, mixed=True)
            print(f"iter {iteration:5d} obj {value:+.12g} trace {trace_value:.12g} "
                  f"primal {primal:.4g} dual {dual_residual:.4g} "
                  f"holmin {hol_min:.3g} mixmin {mix_min:.3g} "
                  f"sec {time.time()-start:.1f}")
            print("  hol worst", hol_worst, "mixed worst", mix_worst,
                  "dual norm", la.norm(dual))
            if args.save:
                np.savez(args.save, x=x, z=z, dual=dual,
                         iteration=np.array(iteration),
                         objective=np.array(value),
                         primal=np.array(primal),
                         dual_residual=np.array(dual_residual))
        previous_z = z.copy()
    return x, z, dual


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=500)
    parser.add_argument("--rho", type=float, default=1.0)
    parser.add_argument("--alpha", type=float, default=1.0)
    parser.add_argument("--objective-scale", type=float, default=1.0)
    parser.add_argument("--report", type=int, default=10)
    parser.add_argument("--save")
    parser.add_argument("--load")
    parser.add_argument("--load-rho", type=float, default=1.0)
    parser.add_argument("--mixed-face")
    parser.add_argument("--product-face")
    parser.add_argument("--mixed-face-field", default="a")
    parser.add_argument("--face-tol", type=float, default=1e-9)
    args = parser.parse_args()
    solve(args)


if __name__ == "__main__":
    main()
