#!/usr/bin/env python3
"""Matrix-free gamma=0 dual-feasibility search for corrected DTH.

On the full mixed invariant operator Y, intersect

  A = {Y : P_L Y P_L >= 0},
  B = {Y : P_K (O - U^T Y) P_K >= 0}.

Membership proves the first-degree corrected cone has objective at least zero.
The two metric projections are blockwise, so ADMM/Douglas--Rachford can search
the complete 103^3-dimensional invariant dual without a dense SDP.  Output is
numerical discovery only until reconstructed in the exact diagram basis.
"""

from __future__ import annotations

import argparse
import time

import numpy as np
import scipy.linalg as la

import agent_dth_facial_ray_admm as face
import agent_dth_invariant_crossing as cross
import agent_dth_primal_admm as primal


def project_dual_B(mixed_y, local, objective, hol_blocks):
    hol_y = primal.crossing_apply(local, mixed_y, transpose=True)
    out = hol_y.copy()
    for block in hol_blocks:
        basis = block["basis"]
        if not basis.shape[1]:
            continue
        matrix = primal.get_block(hol_y, block["indices"], block["dimensions"])
        matrix = (matrix + matrix.T) / 2
        objective_block = primal.get_block(
            objective, block["indices"], block["dimensions"])
        compressed = basis.T @ matrix @ basis
        target = basis.T @ objective_block @ basis
        slack = target - compressed
        replacement = target - primal.positive_part(slack)
        matrix += basis @ (replacement - compressed) @ basis.T
        primal.put_block(out, block["indices"], matrix, block["dimensions"])
    return primal.crossing_apply(local, out)


def audit(y, local, objective, hol_blocks, mixed_blocks):
    mixed_min = np.inf
    for block in mixed_blocks:
        kernel = block["kernel"]
        if not kernel.shape[1]:
            continue
        matrix = primal.get_block(y, block["indices"], block["dimensions"])
        values = la.eigvalsh(kernel.T @ ((matrix + matrix.T) / 2) @ kernel)
        mixed_min = min(mixed_min, float(values[0]))
    hol_y = primal.crossing_apply(local, y, transpose=True)
    hol_min = np.inf
    active = []
    for block in hol_blocks:
        basis = block["basis"]
        if not basis.shape[1]:
            continue
        matrix = primal.get_block(hol_y, block["indices"], block["dimensions"])
        ob = primal.get_block(objective, block["indices"], block["dimensions"])
        slack = basis.T @ ((ob - matrix + (ob - matrix).T) / 2) @ basis
        values = la.eigvalsh(slack)
        hol_min = min(hol_min, float(values[0]))
        active.append((float(values[0]), block["shapes"],
                       int(np.sum(values > 1e-8))))
    return hol_min, mixed_min, sorted(active)


def solve(args):
    crossing, hol, mixed = cross.local_crossing(verbose=True)
    local, hol_ranges, mixed_ranges = primal.normalized_local_crossing(crossing)
    target = cross.target_highest_weight_bases()
    support = cross.local_support_highest_blocks(mixed, target, verbose=True)
    hol_blocks, objective, _ = primal.prepare_hol_blocks(hol_ranges)
    mixed_blocks = primal.prepare_mixed_blocks(mixed_ranges, support)
    if args.mixed_face and args.product_face:
        raise ValueError("choose only one of --mixed-face and --product-face")
    if args.product_face:
        primal.restrict_mixed_blocks_to_product_face(
            mixed_blocks, np.load(args.product_face))
    elif args.mixed_face:
        face_checkpoint = np.load(args.mixed_face)
        face_tensor = face_checkpoint[args.mixed_face_field]
        primal.restrict_mixed_blocks_to_exposed_face(
            mixed_blocks, face_tensor, args.face_tol)
    print("mixed dual face dimension:",
          sum(block["kernel"].shape[1] for block in mixed_blocks))

    if args.resume:
        checkpoint = np.load(args.resume)
        a = checkpoint["a"]
        b = checkpoint["b"]
        dual = checkpoint["dual"]
        print("resumed ADMM state from", args.resume)
    elif args.load:
        checkpoint = np.load(args.load)
        y = checkpoint[args.load_field]
        if args.load_field == "dual":
            y = -args.load_rho * y
        print("loaded initial Y from", args.load, args.load_field)
        a = face.project_mixed_dual(y, mixed_blocks)
        b = project_dual_B(a, local, objective, hol_blocks)
        dual = np.zeros_like(y)
    else:
        y = np.zeros((103, 103, 103), dtype=float)
        a = face.project_mixed_dual(y, mixed_blocks)
        b = project_dual_B(a, local, objective, hol_blocks)
        dual = np.zeros_like(y)
    previous_b = b.copy()
    start = time.time()

    for iteration in range(1, args.iterations + 1):
        a = face.project_mixed_dual(b - dual, mixed_blocks)
        relaxed = args.alpha * a + (1 - args.alpha) * b
        b = project_dual_B(relaxed + dual, local, objective, hol_blocks)
        dual += relaxed - b
        if iteration == 1 or iteration % args.report == 0:
            residual = la.norm(a - b)
            step = la.norm(b - previous_b)
            midpoint = (a + b) / 2
            hol_min, mixed_min, active = audit(
                midpoint, local, objective, hol_blocks, mixed_blocks)
            print(f"iter {iteration:5d} residual {residual:.6g} "
                  f"step {step:.6g} norm {la.norm(midpoint):.8g} "
                  f"holmin {hol_min:.3g} mixedmin {mixed_min:.3g} "
                  f"sec {time.time()-start:.1f}")
            print("  ten least hol slacks", active[:10])
            if args.save:
                np.savez(args.save, a=a, b=b, dual=dual, y=midpoint,
                         iteration=np.array(iteration),
                         residual=np.array(residual), step=np.array(step),
                         hol_min=np.array(hol_min), mixed_min=np.array(mixed_min))
        previous_b = b.copy()
    return a, b


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--alpha", type=float, default=1.8)
    parser.add_argument("--report", type=int, default=100)
    parser.add_argument("--save")
    parser.add_argument("--load")
    parser.add_argument("--resume")
    parser.add_argument("--load-field", default="dual")
    parser.add_argument("--load-rho", type=float, default=1.0)
    parser.add_argument("--mixed-face")
    parser.add_argument("--product-face")
    parser.add_argument("--mixed-face-field", default="a")
    parser.add_argument("--face-tol", type=float, default=1e-9)
    args = parser.parse_args()
    solve(args)


if __name__ == "__main__":
    main()
