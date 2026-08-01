#!/usr/bin/env python3
"""Numerically search for the homogeneous normal exposing the Gamma5 face.

An objective-free two-PPT feasibility point is full rank on the holomorphic
support and on the exact Gamma1 product face, but has Gamma5 rank 751.  If it
is a relative-interior point, a homogeneous facial certificate has the form

    F1^T Y1 F1 = 0,
    Y5 >= 0 with ran(Y5) in ker(Z5),
    P_K(U1^T Y1 + U5^T Y5)P_K = 0,
    Tr(Y5) = 1.

This program applies exact metric projections to those two convex sets.  Its
output is numerical discovery data; an exposing normal becomes a theorem
only after exact reconstruction in the diagram basis.
"""

from __future__ import annotations

import argparse
import itertools
import sys
import time
import types

sys.modules.setdefault("cvxpy", types.ModuleType("cvxpy"))

import numpy as np
import scipy.linalg as la


_SCIPY_SVD = la.svd


def _empty_safe_svd(matrix, full_matrices=True, **kwargs):
    if 0 in matrix.shape:
        m, n = matrix.shape
        return np.eye(m), np.empty(0), np.eye(n)
    return _SCIPY_SVD(matrix, full_matrices=full_matrices, **kwargs)


la.svd = _empty_safe_svd

import agent_dth_invariant_crossing as cross
import agent_dth_primal_admm as primal


def coordinate_ranges(multiplicities):
    output = []
    offset = 0
    for multiplicity in multiplicities:
        output.append(
            np.arange(offset, offset + multiplicity**2)
            .reshape(multiplicity, multiplicity)
        )
        offset += multiplicity**2
    assert offset == 103
    return output


def prepare_gamma1_blocks(ranges, product):
    blocks = []
    for shapes in itertools.product(range(6), repeat=3):
        dimensions = tuple(cross.MIXED_MULTS[s] for s in shapes)
        key = "".join(map(str, shapes))
        blocks.append({
            "shapes": shapes,
            "dimensions": dimensions,
            "indices": primal.block_indices(ranges, shapes),
            "basis": product[f"L_{key}"] @ product[f"q_{key}"],
        })
    return blocks


def prepare_gamma5_blocks(ranges, multiplicities, carriers, face):
    blocks = []
    for shapes in itertools.product(range(6), repeat=3):
        dimensions = tuple(multiplicities[s] for s in shapes)
        key = "".join(map(str, shapes))
        blocks.append({
            "shapes": shapes,
            "dimensions": dimensions,
            "indices": primal.block_indices(ranges, shapes),
            "kernel": face[f"kernel_{key}"],
            "weight": float(np.sqrt(np.prod([carriers[s]
                                               for s in shapes]))),
        })
    return blocks


def symmetrize(matrix):
    return (matrix + matrix.T) / 2


def project_gamma1_zero_compression(tensor, blocks):
    out = tensor.copy()
    for block in blocks:
        basis = block["basis"]
        if not basis.shape[1]:
            continue
        matrix = primal.get_block(tensor, block["indices"],
                                  block["dimensions"])
        matrix = symmetrize(matrix)
        compressed = basis.T @ matrix @ basis
        matrix -= basis @ compressed @ basis.T
        primal.put_block(out, block["indices"], matrix,
                         block["dimensions"])
    return out


def project_gamma5_face_trace_one(tensor, blocks):
    spectral = []
    upper = -np.inf
    for block in blocks:
        kernel = block["kernel"]
        if not kernel.shape[1]:
            spectral.append(None)
            continue
        matrix = primal.get_block(tensor, block["indices"],
                                  block["dimensions"])
        compressed = kernel.T @ symmetrize(matrix) @ kernel
        values, vectors = la.eigh(compressed)
        weight = block["weight"]
        upper = max(upper, float(np.max(values / weight)))
        spectral.append((values, vectors, weight))

    def weighted_trace(threshold):
        return sum(
            weight * np.sum(np.maximum(values - threshold * weight, 0))
            for item in spectral if item is not None
            for values, _, weight in (item,)
        )

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
        replacement = ((vectors * np.maximum(
            values - threshold * weight, 0)) @ vectors.T)
        kernel = block["kernel"]
        matrix = kernel @ replacement @ kernel.T
        primal.put_block(out, block["indices"], matrix,
                         block["dimensions"])
    return out


def project_zero_hol_pair(y1, y5, local1, local5, hol_blocks):
    combined = (primal.crossing_apply(local1, y1, transpose=True)
                + primal.crossing_apply(local5, y5, transpose=True))
    delta = np.zeros_like(combined)
    for block in hol_blocks:
        basis = block["basis"]
        if not basis.shape[1]:
            continue
        matrix = primal.get_block(combined, block["indices"],
                                  block["dimensions"])
        compressed = basis.T @ symmetrize(matrix) @ basis
        correction = -basis @ compressed @ basis.T
        primal.put_block(delta, block["indices"], correction,
                         block["dimensions"])
    return (y1 + primal.crossing_apply(local1, delta) / 2,
            y5 + primal.crossing_apply(local5, delta) / 2)


def gamma1_compression_norm(tensor, blocks):
    square = 0.0
    maximum = 0.0
    worst = None
    for block in blocks:
        basis = block["basis"]
        if not basis.shape[1]:
            continue
        matrix = primal.get_block(tensor, block["indices"],
                                  block["dimensions"])
        compressed = basis.T @ symmetrize(matrix) @ basis
        norm = float(la.norm(compressed))
        square += norm * norm
        if norm > maximum:
            maximum, worst = norm, block["shapes"]
    return np.sqrt(square), maximum, worst


def gamma5_audit(tensor, blocks, tolerance=1e-9):
    trace = 0.0
    outside_square = 0.0
    minimum = np.inf
    positive_rank = 0
    active_blocks = 0
    rows = []
    for block in blocks:
        kernel = block["kernel"]
        matrix = primal.get_block(tensor, block["indices"],
                                  block["dimensions"])
        matrix = symmetrize(matrix)
        compressed = kernel.T @ matrix @ kernel
        projected = kernel @ compressed @ kernel.T
        outside_square += la.norm(matrix - projected)**2
        if not kernel.shape[1]:
            continue
        values = la.eigvalsh(compressed)
        current = float(values[0])
        minimum = min(minimum, current)
        rank = int(np.sum(values > tolerance))
        positive_rank += rank
        active_blocks += int(rank > 0)
        trace += block["weight"] * float(np.trace(compressed))
        rows.append((float(values[-1]), block["shapes"], rank, len(values),
                     current))
    return {
        "trace": trace, "outside": np.sqrt(outside_square),
        "minimum": minimum, "positive_rank": positive_rank,
        "active_blocks": active_blocks, "largest": sorted(rows, reverse=True)[:12],
    }


def hol_compression_norm(y1, y5, local1, local5, hol_blocks):
    combined = (primal.crossing_apply(local1, y1, transpose=True)
                + primal.crossing_apply(local5, y5, transpose=True))
    square = 0.0
    maximum = 0.0
    worst = None
    for block in hol_blocks:
        basis = block["basis"]
        if not basis.shape[1]:
            continue
        matrix = primal.get_block(combined, block["indices"],
                                  block["dimensions"])
        compressed = basis.T @ symmetrize(matrix) @ basis
        norm = float(la.norm(compressed))
        square += norm * norm
        if norm > maximum:
            maximum, worst = norm, block["shapes"]
    return np.sqrt(square), maximum, worst


def solve(args):
    product = np.load(args.product_face)
    gamma5 = np.load(args.gamma5_cache)
    face = np.load(args.gamma5_face)
    local1 = product["local_crossing"]
    local5 = gamma5["local"]
    mults5 = tuple(map(int, gamma5["mults"]))
    carriers5 = tuple(map(int, gamma5["carriers"]))
    hol_ranges = coordinate_ranges(cross.HOL_MULTS)
    mixed_ranges = coordinate_ranges(cross.MIXED_MULTS)
    final_ranges = coordinate_ranges(mults5)
    hol_blocks, _, _ = primal.prepare_hol_blocks(hol_ranges)
    blocks1 = prepare_gamma1_blocks(mixed_ranges, product)
    blocks5 = prepare_gamma5_blocks(
        final_ranges, mults5, carriers5, face)
    print("dimensions hol/Gamma1/Gamma5 kernel:",
          sum(b["basis"].shape[1] for b in hol_blocks),
          sum(b["basis"].shape[1] for b in blocks1),
          sum(b["kernel"].shape[1] for b in blocks5))

    if args.resume:
        checkpoint = np.load(args.resume)
        a1, a5 = checkpoint["a1"], checkpoint["a5"]
        b1, b5 = checkpoint["b1"], checkpoint["b5"]
        dual1, dual5 = checkpoint["dual1"], checkpoint["dual5"]
        start_iteration = int(checkpoint["iteration"])
        print("resumed", args.resume, "iteration", start_iteration)
    else:
        zero = np.zeros((103, 103, 103), dtype=float)
        a1 = project_gamma1_zero_compression(zero, blocks1)
        a5 = project_gamma5_face_trace_one(zero, blocks5)
        b1, b5 = project_zero_hol_pair(
            a1, a5, local1, local5, hol_blocks)
        dual1 = np.zeros_like(zero)
        dual5 = np.zeros_like(zero)
        start_iteration = 0

    previous_b1 = b1.copy()
    previous_b5 = b5.copy()
    start = time.time()
    for step in range(1, args.iterations + 1):
        iteration = start_iteration + step
        a1 = project_gamma1_zero_compression(b1 - dual1, blocks1)
        a5 = project_gamma5_face_trace_one(b5 - dual5, blocks5)
        relaxed1 = args.alpha * a1 + (1 - args.alpha) * b1
        relaxed5 = args.alpha * a5 + (1 - args.alpha) * b5
        b1, b5 = project_zero_hol_pair(
            relaxed1 + dual1, relaxed5 + dual5,
            local1, local5, hol_blocks)
        dual1 += relaxed1 - b1
        dual5 += relaxed5 - b5

        if step == 1 or iteration % args.report == 0:
            residual = np.hypot(la.norm(a1 - b1), la.norm(a5 - b5))
            change = np.hypot(la.norm(b1 - previous_b1),
                              la.norm(b5 - previous_b5))
            y1 = (a1 + b1) / 2
            y5 = (a5 + b5) / 2
            c1 = gamma1_compression_norm(y1, blocks1)
            c5 = gamma5_audit(y5, blocks5, args.rank_tol)
            hk = hol_compression_norm(
                y1, y5, local1, local5, hol_blocks)
            print(f"iter {iteration:6d} residual {residual:.4g} "
                  f"change {change:.4g} norms ({la.norm(y1):.5g},"
                  f"{la.norm(y5):.5g}) sec {time.time()-start:.1f}")
            print("  Gamma1 compression norm/max/worst:", c1)
            print("  hol identity norm/max/worst:", hk)
            print("  Gamma5 trace/outside/min/rank/active:",
                  c5["trace"], c5["outside"], c5["minimum"],
                  c5["positive_rank"], c5["active_blocks"])
            print("  largest Gamma5 face blocks:", c5["largest"][:6])
            if args.save:
                np.savez(
                    args.save, a1=a1, a5=a5, b1=b1, b5=b5,
                    dual1=dual1, dual5=dual5, y1=y1, y5=y5,
                    iteration=np.array(iteration),
                    residual=np.array(residual), change=np.array(change),
                    gamma1_compression=np.array(c1[0]),
                    hol_identity=np.array(hk[0]),
                    gamma5_trace=np.array(c5["trace"]),
                    gamma5_outside=np.array(c5["outside"]),
                    gamma5_minimum=np.array(c5["minimum"]),
                )
        previous_b1 = b1.copy()
        previous_b5 = b5.copy()
    return a1, a5, b1, b5


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=500)
    parser.add_argument("--alpha", type=float, default=1.6)
    parser.add_argument("--report", type=int, default=25)
    parser.add_argument("--rank-tol", type=float, default=1e-9)
    parser.add_argument("--save")
    parser.add_argument("--resume")
    parser.add_argument(
        "--product-face", default="/tmp/dth_product_face_bases.npz")
    parser.add_argument(
        "--gamma5-cache", default="/tmp/dth_gamma5_local_crossing_root.npz")
    parser.add_argument(
        "--gamma5-face", default="/tmp/dth_gamma5_feasible_face.npz")
    args = parser.parse_args()
    solve(args)


if __name__ == "__main__":
    main()
