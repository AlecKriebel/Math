#!/usr/bin/env python3
"""Search the forced mixed face exposed by a hol-zero dual ray.

The exact feasibility point obtained with zero objective is strictly positive
on all 768 holomorphic K directions but singular on the mixed support space.
Hence any common exposing ray must have zero holomorphic compressed slack.
This program searches for Y satisfying

  P_L Y P_L >= 0,  sum_mu sqrt(e_mu) Tr(P_L Y P_L)=1,
  P_K U^T Y P_K = 0.

Components outside L and K are retained.  Numerical output is discovery only.
"""

from __future__ import annotations

import argparse
import time

import numpy as np
import scipy.linalg as la

import agent_dth_invariant_crossing as cross
import agent_dth_primal_admm as primal


def mixed_weight(shapes):
    return np.sqrt(np.prod([cross.MIXED_CARRIER_DIMS[s] for s in shapes]))


def project_mixed_dual_trace_one(tensor, blocks):
    out = tensor.copy()
    data = []
    upper = -np.inf
    for block in blocks:
        kernel = block["kernel"]
        if not kernel.shape[1]:
            data.append(None)
            continue
        matrix = primal.get_block(tensor, block["indices"], block["dimensions"])
        matrix = (matrix + matrix.T) / 2
        compressed = kernel.T @ matrix @ kernel
        values, vectors = la.eigh(compressed)
        weight = mixed_weight(block["shapes"])
        upper = max(upper, float(np.max(values / weight)))
        data.append((values, vectors, weight, compressed, matrix))

    def trace_at(threshold):
        return sum(weight * np.sum(np.maximum(values - threshold * weight, 0))
                   for item in data if item is not None
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

    for block, item in zip(blocks, data):
        if item is None:
            continue
        values, vectors, weight, compressed, matrix = item
        replacement = ((vectors * np.maximum(values - threshold * weight, 0))
                       @ vectors.T)
        kernel = block["kernel"]
        matrix += kernel @ (replacement - compressed) @ kernel.T
        primal.put_block(out, block["indices"], matrix, block["dimensions"])
    return out


def project_hol_zero(mixed_y, local, hol_blocks):
    hol = primal.crossing_apply(local, mixed_y, transpose=True)
    out = hol.copy()
    for block in hol_blocks:
        basis = block["basis"]
        if not basis.shape[1]:
            continue
        matrix = primal.get_block(hol, block["indices"], block["dimensions"])
        matrix = (matrix + matrix.T) / 2
        compressed = basis.T @ matrix @ basis
        matrix -= basis @ compressed @ basis.T
        primal.put_block(out, block["indices"], matrix, block["dimensions"])
    return primal.crossing_apply(local, out)


def audit(y, local, hol_blocks, mixed_blocks):
    hol = primal.crossing_apply(local, y, transpose=True)
    hol_residual = 0.0
    for block in hol_blocks:
        basis = block["basis"]
        if basis.shape[1]:
            matrix = primal.get_block(hol, block["indices"], block["dimensions"])
            hol_residual += la.norm(basis.T @ matrix @ basis) ** 2
    mixed_min = np.inf
    trace = 0.0
    ranks = []
    for block in mixed_blocks:
        kernel = block["kernel"]
        if not kernel.shape[1]:
            continue
        matrix = primal.get_block(y, block["indices"], block["dimensions"])
        compressed = kernel.T @ ((matrix + matrix.T) / 2) @ kernel
        values = la.eigvalsh(compressed)
        mixed_min = min(mixed_min, float(values[0]))
        trace += mixed_weight(block["shapes"]) * float(np.sum(values))
        ranks.append((int(np.sum(values > 1e-9)), block["shapes"], values))
    return np.sqrt(hol_residual), mixed_min, trace, ranks


def solve(args):
    crossing, hol, mixed = cross.local_crossing(verbose=True)
    local, hol_ranges, mixed_ranges = primal.normalized_local_crossing(crossing)
    target = cross.target_highest_weight_bases()
    support = cross.local_support_highest_blocks(mixed, target, verbose=True)
    hol_blocks, _, _ = primal.prepare_hol_blocks(hol_ranges)
    mixed_blocks = primal.prepare_mixed_blocks(mixed_ranges, support)

    if args.load:
        checkpoint = np.load(args.load)
        a = checkpoint["a"]
        b = checkpoint["b"]
        dual = checkpoint["dual"]
        print("loaded continuation checkpoint", args.load)
    else:
        rng = np.random.default_rng(20260731)
        a = project_mixed_dual_trace_one(
            rng.normal(size=(103, 103, 103)) * 1e-3, mixed_blocks)
        b = project_hol_zero(a, local, hol_blocks)
        dual = np.zeros_like(a)
    previous = b.copy()
    start = time.time()
    for iteration in range(1, args.iterations + 1):
        a = project_mixed_dual_trace_one(b - dual, mixed_blocks)
        relaxed = args.alpha * a + (1 - args.alpha) * b
        b = project_hol_zero(relaxed + dual, local, hol_blocks)
        dual += relaxed - b
        if iteration == 1 or iteration % args.report == 0:
            residual = la.norm(a - b)
            step = la.norm(b - previous)
            midpoint = (a + b) / 2
            hol_res, mixed_min, trace, ranks = audit(
                midpoint, local, hol_blocks, mixed_blocks)
            print(f"iter {iteration:5d} residual {residual:.6g} "
                  f"step {step:.6g} hol {hol_res:.6g} trace {trace:.12g} "
                  f"mixedmin {mixed_min:.3g} norm {la.norm(midpoint):.8g} "
                  f"sec {time.time()-start:.1f}")
            print("  positive mixed blocks/rank",
                  sum(r > 0 for r, _, _ in ranks),
                  sum(r for r, _, _ in ranks))
            if args.save:
                np.savez(args.save, a=a, b=b, dual=dual, y=midpoint,
                         iteration=np.array(iteration),
                         residual=np.array(residual), step=np.array(step),
                         hol_residual=np.array(hol_res), trace=np.array(trace),
                         mixed_min=np.array(mixed_min))
        previous = b.copy()
    return a, b


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--alpha", type=float, default=1.8)
    parser.add_argument("--report", type=int, default=100)
    parser.add_argument("--save")
    parser.add_argument("--load")
    args = parser.parse_args()
    solve(args)


if __name__ == "__main__":
    main()
