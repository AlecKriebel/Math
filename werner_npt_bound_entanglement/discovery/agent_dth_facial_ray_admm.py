#!/usr/bin/env python3
"""Matrix-free search for a homogeneous facial-reduction ray.

Find a nonzero holomorphic invariant operator y such that

  P_K y P_K >= 0,
  P_L (-U^tensor3 y) P_L >= 0.

Its pairing with every feasible corrected DTH moment vanishes, so its two
compressed kernels expose a smaller common face.  The hol compressed trace is
fixed to one to exclude the zero solution.  Numerical output is discovery
only and must be reconstructed in the exact diagram bridge.
"""

from __future__ import annotations

import argparse
import time

import numpy as np
import scipy.linalg as la

import agent_dth_invariant_crossing as cross
import agent_dth_primal_admm as primal


def project_hol_dual_trace_one(tensor, blocks):
    out = tensor.copy()
    spectral = []
    upper = -np.inf
    for block in blocks:
        basis = block["basis"]
        if not basis.shape[1]:
            spectral.append(None)
            continue
        matrix = primal.get_block(tensor, block["indices"], block["dimensions"])
        matrix = (matrix + matrix.T) / 2
        compressed = basis.T @ matrix @ basis
        values, vectors = la.eigh(compressed)
        weight = block["weight"]
        upper = max(upper, float(np.max(values / weight)))
        spectral.append((values, vectors, weight, compressed, matrix))

    def trace_at(threshold):
        return sum(weight * np.sum(np.maximum(values - threshold * weight, 0))
                   for item in spectral if item is not None
                   for values, _, weight, _, _ in (item,))

    lower = min(-1.0, upper - 1.0)
    while trace_at(lower) < 1:
        lower = 2 * lower - upper
    for _ in range(80):
        middle = (lower + upper) / 2
        if trace_at(middle) > 1:
            lower = middle
        else:
            upper = middle
    threshold = (lower + upper) / 2

    for block, item in zip(blocks, spectral):
        if item is None:
            continue
        values, vectors, weight, compressed, matrix = item
        replacement = ((vectors * np.maximum(values - threshold * weight, 0))
                       @ vectors.T)
        basis = block["basis"]
        matrix += basis @ (replacement - compressed) @ basis.T
        primal.put_block(out, block["indices"], matrix, block["dimensions"])
    return out


def project_mixed_dual(tensor, blocks):
    out = tensor.copy()
    for block in blocks:
        kernel = block["kernel"]
        if not kernel.shape[1]:
            continue
        matrix = primal.get_block(tensor, block["indices"], block["dimensions"])
        matrix = (matrix + matrix.T) / 2
        compressed = kernel.T @ matrix @ kernel
        replacement = primal.positive_part(compressed)
        matrix += kernel @ (replacement - compressed) @ kernel.T
        primal.put_block(out, block["indices"], matrix, block["dimensions"])
    return out


def compressed_minima(y, mixed_y, hol_blocks, mixed_blocks):
    hol_min = np.inf
    mixed_min = np.inf
    hol_ranks = []
    mixed_ranks = []
    for block in hol_blocks:
        basis = block["basis"]
        if not basis.shape[1]:
            continue
        matrix = primal.get_block(y, block["indices"], block["dimensions"])
        values = la.eigvalsh(basis.T @ ((matrix + matrix.T) / 2) @ basis)
        hol_min = min(hol_min, float(values[0]))
        hol_ranks.append((int(np.sum(values > 1e-8)), block["shapes"], values))
    for block in mixed_blocks:
        kernel = block["kernel"]
        if not kernel.shape[1]:
            continue
        matrix = primal.get_block(mixed_y, block["indices"], block["dimensions"])
        values = la.eigvalsh(kernel.T @ ((matrix + matrix.T) / 2) @ kernel)
        mixed_min = min(mixed_min, float(values[0]))
        mixed_ranks.append((int(np.sum(values > 1e-8)), block["shapes"], values))
    return hol_min, mixed_min, hol_ranks, mixed_ranks


def solve(args):
    crossing, hol, mixed = cross.local_crossing(verbose=True)
    local, hol_ranges, mixed_ranges = primal.normalized_local_crossing(crossing)
    target = cross.target_highest_weight_bases()
    support = cross.local_support_highest_blocks(mixed, target, verbose=True)
    hol_blocks, _, _ = primal.prepare_hol_blocks(hol_ranges)
    mixed_blocks = primal.prepare_mixed_blocks(mixed_ranges, support)

    rng = np.random.default_rng(20260731)
    y = project_hol_dual_trace_one(
        rng.normal(size=(103, 103, 103)) * 1e-3, hol_blocks)
    ay = -primal.crossing_apply(local, y)
    z = project_mixed_dual(ay, mixed_blocks)
    dual = np.zeros_like(y)
    previous_z = z.copy()
    start = time.time()

    for iteration in range(1, args.iterations + 1):
        # A=-U^tensor3, hence A^T=-U^T.
        v = -primal.crossing_apply(local, z - dual, transpose=True)
        y = project_hol_dual_trace_one(v, hol_blocks)
        ay = -primal.crossing_apply(local, y)
        relaxed = args.alpha * ay + (1 - args.alpha) * z
        z = project_mixed_dual(relaxed + dual, mixed_blocks)
        dual += relaxed - z

        if iteration == 1 or iteration % args.report == 0:
            residual = la.norm(ay - z)
            dual_residual = la.norm(z - previous_z)
            hol_min, mixed_min, hr, mr = compressed_minima(
                y, z, hol_blocks, mixed_blocks)
            print(f"iter {iteration:5d} residual {residual:.5g} "
                  f"dual {dual_residual:.5g} norm {la.norm(y):.8g} "
                  f"holmin {hol_min:.3g} mixedmin {mixed_min:.3g} "
                  f"sec {time.time()-start:.1f}")
            print("  positive ranks hol/mixed",
                  sum(r > 0 for r, _, _ in hr),
                  sum(r > 0 for r, _, _ in mr),
                  "total ranks", sum(r for r, _, _ in hr),
                  sum(r for r, _, _ in mr))
            if args.save:
                np.savez(args.save, y=y, z=z, dual=dual,
                         iteration=np.array(iteration),
                         residual=np.array(residual),
                         dual_residual=np.array(dual_residual))
        previous_z = z.copy()
    return y, z


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--alpha", type=float, default=1.8)
    parser.add_argument("--report", type=int, default=100)
    parser.add_argument("--save")
    args = parser.parse_args()
    solve(args)


if __name__ == "__main__":
    main()
