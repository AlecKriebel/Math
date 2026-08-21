#!/usr/bin/env python3
"""Search an exposing normal for the exact 2266-dimensional product face.

Discovery-layer ADMM.  On each mixed support block L, the first projection
forces the compression to be positive on the orthogonal complement N of the
exact product-face range R and zero on R and the R:N cross terms.  The second
projection forces the holomorphic pullback to vanish on K.  A converged point
is the numerical precursor of the rational face-exposing certificate.
"""

from __future__ import annotations

import argparse
import time

import numpy as np
import scipy.linalg as la

import agent_dth_invariant_crossing as cross
import agent_dth_mixed_face_admm as face
import agent_dth_primal_admm as primal


def product_complements(blocks, data):
    result = []
    for block in blocks:
        tag = "".join(map(str, block["shapes"]))
        local_support = data["L_" + tag]
        product_range = data["q_" + tag]
        complement_coordinates = la.null_space(product_range.T, rcond=1e-10)
        complement = local_support @ complement_coordinates
        result.append((local_support, complement))
    return result


def project_face_complement_trace_one(tensor, blocks, complements):
    data = []
    upper = -np.inf
    for block, (local_support, complement) in zip(blocks, complements):
        matrix = primal.get_block(
            tensor, block["indices"], block["dimensions"])
        matrix = (matrix + matrix.T) / 2
        compressed = complement.T @ matrix @ complement
        values, vectors = la.eigh(compressed)
        weight = face.mixed_weight(block["shapes"])
        if len(values):
            upper = max(upper, float(np.max(values / weight)))
        data.append((matrix, local_support, complement, values, vectors,
                     weight))

    def trace_at(threshold):
        return sum(weight * np.sum(np.maximum(values - threshold * weight, 0))
                   for _, _, _, values, _, weight in data)

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

    out = tensor.copy()
    for block, item in zip(blocks, data):
        matrix, local_support, complement, values, vectors, weight = item
        local_compression = local_support.T @ matrix @ local_support
        replacement = ((vectors * np.maximum(
            values - threshold * weight, 0)) @ vectors.T)
        matrix = (matrix
                  - local_support @ local_compression @ local_support.T
                  + complement @ replacement @ complement.T)
        primal.put_block(out, block["indices"], matrix, block["dimensions"])
    return out


def audit(y, local, hol_blocks, mixed_blocks, complements):
    hol = primal.crossing_apply(local, y, transpose=True)
    hol_residual = 0.0
    for block in hol_blocks:
        basis = block["basis"]
        if basis.shape[1]:
            matrix = primal.get_block(
                hol, block["indices"], block["dimensions"])
            hol_residual += la.norm(basis.T @ matrix @ basis) ** 2
    trace = 0.0
    minimum = np.inf
    rank = 0
    leakage = 0.0
    for block, (local_support, complement) in zip(mixed_blocks, complements):
        matrix = primal.get_block(y, block["indices"], block["dimensions"])
        matrix = (matrix + matrix.T) / 2
        local_matrix = local_support.T @ matrix @ local_support
        compressed = complement.T @ matrix @ complement
        if len(compressed):
            values = la.eigvalsh(compressed)
            minimum = min(minimum, float(values[0]))
            rank += int(np.sum(values > 1e-9))
            trace += face.mixed_weight(block["shapes"]) * float(np.sum(values))
        leakage = max(leakage, la.norm(
            local_support @ local_matrix @ local_support.T
            - complement @ compressed @ complement.T))
    return np.sqrt(hol_residual), minimum, rank, trace, leakage


def solve(args):
    crossing_data, hol, mixed = cross.local_crossing(verbose=True)
    local, hol_ranges, mixed_ranges = primal.normalized_local_crossing(
        crossing_data)
    target = cross.target_highest_weight_bases()
    support = cross.local_support_highest_blocks(mixed, target, verbose=True)
    hol_blocks, _, _ = primal.prepare_hol_blocks(hol_ranges)
    mixed_blocks = primal.prepare_mixed_blocks(mixed_ranges, support)
    product_data = np.load(args.product_face)
    complements = product_complements(mixed_blocks, product_data)
    print("product face/complement dimensions:",
          sum(product_data["q_" + "".join(map(str, b["shapes"]))].shape[1]
              for b in mixed_blocks),
          sum(n.shape[1] for _, n in complements))

    if args.load:
        checkpoint = np.load(args.load)
        a = checkpoint["a"]
        b = checkpoint["b"]
        dual = checkpoint["dual"]
    else:
        rng = np.random.default_rng(20260801)
        a = project_face_complement_trace_one(
            rng.normal(size=(103, 103, 103)) * 1e-3,
            mixed_blocks, complements)
        b = face.project_hol_zero(a, local, hol_blocks)
        dual = np.zeros_like(a)

    previous = b.copy()
    start = time.time()
    for iteration in range(1, args.iterations + 1):
        a = project_face_complement_trace_one(
            b - dual, mixed_blocks, complements)
        relaxed = args.alpha * a + (1 - args.alpha) * b
        b = face.project_hol_zero(relaxed + dual, local, hol_blocks)
        dual += relaxed - b
        if iteration == 1 or iteration % args.report == 0:
            midpoint = (a + b) / 2
            residual = la.norm(a - b)
            step = la.norm(b - previous)
            hol_res, minimum, rank, trace, leakage = audit(
                midpoint, local, hol_blocks, mixed_blocks, complements)
            print(f"iter {iteration:5d} residual {residual:.6g} "
                  f"step {step:.6g} hol {hol_res:.6g} "
                  f"trace {trace:.12g} min {minimum:.3g} "
                  f"rank {rank} leak {leakage:.3g} "
                  f"sec {time.time()-start:.1f}")
            if args.save:
                np.savez(args.save, a=a, b=b, dual=dual, y=midpoint,
                         iteration=np.array(iteration),
                         residual=np.array(residual), step=np.array(step),
                         hol_residual=np.array(hol_res),
                         trace=np.array(trace), minimum=np.array(minimum),
                         rank=np.array(rank), leakage=np.array(leakage))
        previous = b.copy()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--product-face", required=True)
    parser.add_argument("--iterations", type=int, default=2000)
    parser.add_argument("--alpha", type=float, default=1.8)
    parser.add_argument("--report", type=int, default=100)
    parser.add_argument("--load")
    parser.add_argument("--save")
    solve(parser.parse_args())


if __name__ == "__main__":
    main()
