#!/usr/bin/env python3
"""Numerical zero-dual search for the Gamma1+Gamma5 DTH relaxation.

The strengthened first five-replica primal has two partial-transpose cones:

* Gamma1 is positive on the exact product-DTH face;
* Gamma5 is positive on the complete final-slot mixed commutant.

This program searches its zero-level dual

    Y1 in C1*,  Y5 in C5*,
    P_K (O - U1^T Y1 - U5^T Y5) P_K >= 0.

Both metric projections are exact in Hilbert--Schmidt-normalized invariant
coordinates.  The optional ``--equality-face`` flag also imposes the lossless
complementary faces exposed by the exact computational equality monomial.

All output is numerical discovery evidence.  A successful iterate must still
be reconstructed and verified in exact diagram coordinates.
"""

from __future__ import annotations

import argparse
import itertools
import sys
import time
import types

# ``agent_dth_primal_admm`` imports a CVXPY discovery module only for its
# representation-theoretic block constructor.  CVXPY is not needed here and
# is absent from the lightweight local Python environment.
sys.modules.setdefault("cvxpy", types.ModuleType("cvxpy"))

import numpy as np
import scipy.linalg as la


# scipy 1.10 on macOS rejects an empty 0-by-n SVD.  Some exact Omega maps are
# identically zero, so make that harmless case explicit before importing the
# shared block constructor.
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
    ranges = []
    offset = 0
    for multiplicity in multiplicities:
        ranges.append(
            np.arange(offset, offset + multiplicity * multiplicity)
            .reshape(multiplicity, multiplicity)
        )
        offset += multiplicity * multiplicity
    assert offset == 103
    return ranges


def prepare_product_blocks(local_ranges, checkpoint):
    blocks = []
    for shapes in itertools.product(range(6), repeat=3):
        dimensions = tuple(cross.MIXED_MULTS[s] for s in shapes)
        key = "".join(str(s) for s in shapes)
        basis = checkpoint[f"L_{key}"] @ checkpoint[f"q_{key}"]
        size = int(np.prod(dimensions))
        assert basis.shape[0] == size
        blocks.append({
            "shapes": shapes,
            "dimensions": dimensions,
            "indices": primal.block_indices(local_ranges, shapes),
            "basis": basis,
        })
    return blocks


def prepare_full_blocks(local_ranges, multiplicities):
    blocks = []
    for shapes in itertools.product(range(6), repeat=3):
        dimensions = tuple(multiplicities[s] for s in shapes)
        size = int(np.prod(dimensions))
        blocks.append({
            "shapes": shapes,
            "dimensions": dimensions,
            "indices": primal.block_indices(local_ranges, shapes),
            "basis": np.eye(size),
        })
    return blocks


def prepare_reduced_gamma5_blocks(local_ranges, multiplicities, face):
    blocks = []
    for shapes in itertools.product(range(6), repeat=3):
        dimensions = tuple(multiplicities[s] for s in shapes)
        key = "".join(map(str, shapes))
        basis = face[f"range_{key}"]
        blocks.append({
            "shapes": shapes,
            "dimensions": dimensions,
            "indices": primal.block_indices(local_ranges, shapes),
            "basis": basis,
        })
    return blocks


def symmetrize(matrix):
    return (matrix + matrix.T) / 2


def positive_part(matrix):
    if not matrix.shape[0]:
        return np.zeros_like(matrix)
    return primal.positive_part(matrix)


def null_face_basis(matrix, tolerance):
    """Return the numerical kernel of a positive semidefinite matrix."""
    matrix = symmetrize(matrix)
    if not matrix.shape[0]:
        return np.empty((0, 0)), np.empty(0)
    values, vectors = la.eigh(matrix)
    scale = max(1.0, float(np.max(np.abs(values))))
    keep = values < tolerance * scale
    if np.min(values) < -20 * tolerance * scale:
        raise RuntimeError(
            f"equality point is not PSD: minimum {np.min(values):.4g}")
    return vectors[:, keep], values


def install_equality_faces(hol_blocks, blocks1, blocks5, x0, local1, local5,
                           tolerance):
    """Attach lossless complementary kernel faces to all three block lists."""
    z1 = primal.crossing_apply(local1, x0)
    z5 = primal.crossing_apply(local5, x0)
    census = {"slack_rank": 0, "gamma1_rank": 0, "gamma5_rank": 0,
              "slack_active": 0, "gamma1_active": 0, "gamma5_active": 0}

    for block in hol_blocks:
        basis = block["basis"]
        matrix = primal.get_block(x0, block["indices"], block["dimensions"])
        compressed = basis.T @ symmetrize(matrix) @ basis
        face, values = null_face_basis(compressed, tolerance)
        rank = len(values) - face.shape[1]
        block["slack_face"] = face
        census["slack_rank"] += rank
        census["slack_active"] += int(rank > 0)

    for block in blocks1:
        basis = block["basis"]
        matrix = primal.get_block(z1, block["indices"], block["dimensions"])
        compressed = basis.T @ symmetrize(matrix) @ basis
        face, values = null_face_basis(compressed, tolerance)
        rank = len(values) - face.shape[1]
        block["dual_face"] = face
        census["gamma1_rank"] += rank
        census["gamma1_active"] += int(rank > 0)

    for block in blocks5:
        basis = block["basis"]
        matrix = primal.get_block(z5, block["indices"], block["dimensions"])
        compressed = basis.T @ symmetrize(matrix) @ basis
        face, values = null_face_basis(compressed, tolerance)
        rank = len(values) - face.shape[1]
        block["dual_face"] = face
        census["gamma5_rank"] += rank
        census["gamma5_active"] += int(rank > 0)

    return z1, z5, census


def project_cone(tensor, blocks, equality_face=False, full=False):
    """Project onto C* or its equality-exposed complementary face.

    For Gamma1 only the product-face compression is constrained; components
    transverse to that compression remain affine multipliers.  Gamma5 is a
    full PSD cone, so its equality-face projection removes all transverse
    components.
    """
    out = tensor.copy()
    for block in blocks:
        basis = block["basis"]
        if not basis.shape[1]:
            if full:
                primal.put_block(out, block["indices"],
                                 np.zeros((0, 0)), block["dimensions"])
            continue
        matrix = primal.get_block(tensor, block["indices"],
                                  block["dimensions"])
        matrix = symmetrize(matrix)
        compressed = basis.T @ matrix @ basis
        if equality_face:
            face = block["dual_face"]
            reduced = face.T @ compressed @ face
            replacement = face @ positive_part(reduced) @ face.T
        else:
            replacement = positive_part(compressed)
        if full:
            output = basis @ replacement @ basis.T
        else:
            output = matrix + basis @ (replacement - compressed) @ basis.T
        primal.put_block(out, block["indices"], output,
                         block["dimensions"])
    return out


def project_slack_pair(y1, y5, local1, local5, objective, hol_blocks,
                       equality_face=False):
    """Exact product-metric projection onto the common hol slack constraint."""
    hol1 = primal.crossing_apply(local1, y1, transpose=True)
    hol5 = primal.crossing_apply(local5, y5, transpose=True)
    combined = hol1 + hol5
    delta = np.zeros_like(combined)
    for block in hol_blocks:
        basis = block["basis"]
        if not basis.shape[1]:
            continue
        matrix = primal.get_block(combined, block["indices"],
                                  block["dimensions"])
        target_full = primal.get_block(objective, block["indices"],
                                       block["dimensions"])
        compressed = basis.T @ symmetrize(matrix) @ basis
        target = basis.T @ symmetrize(target_full) @ basis
        slack = target - compressed
        if equality_face:
            face = block["slack_face"]
            replacement_slack = (
                face @ positive_part(face.T @ slack @ face) @ face.T
            )
        else:
            replacement_slack = positive_part(slack)
        replacement = target - replacement_slack
        correction = basis @ (replacement - compressed) @ basis.T
        primal.put_block(delta, block["indices"], correction,
                         block["dimensions"])
    return (y1 + primal.crossing_apply(local1, delta) / 2,
            y5 + primal.crossing_apply(local5, delta) / 2)


def block_spectrum(tensor, blocks, face_key=None, full=False,
                   tolerance=1e-9):
    minimum = np.inf
    worst = None
    positive = negative = zero = active = 0
    smallest = []
    for block in blocks:
        basis = block["basis"]
        if face_key is not None:
            basis = basis @ block[face_key]
        if not basis.shape[1]:
            continue
        matrix = primal.get_block(tensor, block["indices"],
                                  block["dimensions"])
        compressed = basis.T @ symmetrize(matrix) @ basis
        values = la.eigvalsh(compressed)
        current = float(values[0])
        if current < minimum:
            minimum, worst = current, block["shapes"]
        np_ = int(np.sum(values > tolerance))
        nn = int(np.sum(values < -tolerance))
        positive += np_
        negative += nn
        zero += len(values) - np_ - nn
        active += int(np_ > 0 or nn > 0)
        smallest.append((current, block["shapes"], np_, nn, len(values)))
    return {
        "minimum": minimum, "worst": worst, "positive": positive,
        "negative": negative, "zero": zero, "active": active,
        "smallest": sorted(smallest)[:12],
    }


def slack_tensor(y1, y5, local1, local5, objective, hol_blocks):
    combined = (primal.crossing_apply(local1, y1, transpose=True)
                + primal.crossing_apply(local5, y5, transpose=True))
    output = np.zeros_like(combined)
    for block in hol_blocks:
        basis = block["basis"]
        if not basis.shape[1]:
            continue
        matrix = primal.get_block(combined, block["indices"],
                                  block["dimensions"])
        target = primal.get_block(objective, block["indices"],
                                  block["dimensions"])
        compressed = basis.T @ symmetrize(target - matrix) @ basis
        primal.put_block(output, block["indices"],
                         basis @ compressed @ basis.T,
                         block["dimensions"])
    return output


def pairing(left, right):
    return float(np.vdot(left, right).real)


def audit(y1, y5, local1, local5, objective, hol_blocks, blocks1, blocks5,
          equality_face=False, x0=None, z10=None, z50=None, tolerance=1e-9):
    slack = slack_tensor(y1, y5, local1, local5, objective, hol_blocks)
    slack_summary = block_spectrum(
        slack, hol_blocks,
        face_key="slack_face" if equality_face else None,
        tolerance=tolerance)
    gamma1_summary = block_spectrum(
        y1, blocks1,
        face_key="dual_face" if equality_face else None,
        tolerance=tolerance)
    gamma5_summary = block_spectrum(
        y5, blocks5,
        face_key="dual_face" if equality_face else None,
        tolerance=tolerance)
    result = {"slack": slack_summary, "gamma1": gamma1_summary,
              "gamma5": gamma5_summary, "slack_tensor": slack}
    if x0 is not None:
        result["pairings"] = (
            pairing(slack, x0), pairing(y1, z10), pairing(y5, z50))
    return result


def print_summary(label, summary):
    print(f"  {label}: min {summary['minimum']:+.4g} at "
          f"{summary['worst']}; inertia "
          f"({summary['positive']},{summary['negative']},"
          f"{summary['zero']}); active {summary['active']}")


def solve(args):
    product = np.load(args.product_face)
    local1 = product["local_crossing"]
    hol_ranges = coordinate_ranges(cross.HOL_MULTS)
    mixed_ranges = coordinate_ranges(cross.MIXED_MULTS)
    gamma5 = np.load(args.gamma5_cache)
    local5 = gamma5["local"]
    final_mults = tuple(map(int, gamma5["mults"]))
    final_ranges = coordinate_ranges(final_mults)
    print("loaded Gamma5 crossing", args.gamma5_cache,
          "target multiplicities", final_mults,
          "orthogonality error",
          la.norm(local5.T @ local5 - np.eye(103), ord=2))
    print("Gamma1 orthogonality error:",
          la.norm(local1.T @ local1 - np.eye(103), ord=2))

    print("preparing holomorphic, Gamma1-product, and Gamma5-full blocks")
    hol_blocks, objective, _ = primal.prepare_hol_blocks(hol_ranges)
    blocks1 = prepare_product_blocks(mixed_ranges, product)
    if args.gamma5_face:
        gamma5_face = np.load(args.gamma5_face)
        blocks5 = prepare_reduced_gamma5_blocks(
            final_ranges, final_mults, gamma5_face)
        gamma5_full = False
        print("using facially reduced Gamma5 cone", args.gamma5_face)
    else:
        blocks5 = prepare_full_blocks(final_ranges, final_mults)
        gamma5_full = True
    print("supported dimensions hol/Gamma1/Gamma5:",
          sum(b["basis"].shape[1] for b in hol_blocks),
          sum(b["basis"].shape[1] for b in blocks1),
          sum(b["basis"].shape[1] for b in blocks5))

    x0 = z10 = z50 = None
    if args.equality:
        equality = np.load(args.equality)
        x0 = equality["x"]
        z10, z50, census = install_equality_faces(
            hol_blocks, blocks1, blocks5, x0, local1, local5,
            args.face_tol)
        print("equality exposed ranks/active blocks:", census)
    if args.equality_face and x0 is None:
        raise ValueError("--equality-face requires --equality")

    if args.resume:
        checkpoint = np.load(args.resume)
        a1, a5 = checkpoint["a1"], checkpoint["a5"]
        b1, b5 = checkpoint["b1"], checkpoint["b5"]
        dual1, dual5 = checkpoint["dual1"], checkpoint["dual5"]
        start_iteration = int(checkpoint["iteration"])
        print("resumed", args.resume, "at iteration", start_iteration)
    elif args.load_primal:
        checkpoint = np.load(args.load_primal)
        rho = float(checkpoint["rho"]) if "rho" in checkpoint else 1.0
        # Scaled ADMM duals are normal-cone seeds.  Both signs are useful in
        # practice; choose with --primal-dual-sign after a one-step audit.
        seed1 = args.primal_dual_sign * rho * checkpoint["dual1"]
        seed5 = args.primal_dual_sign * rho * checkpoint["dual5"]
        a1 = project_cone(seed1, blocks1, args.equality_face, full=False)
        a5 = project_cone(seed5, blocks5, args.equality_face,
                          full=gamma5_full)
        b1, b5 = project_slack_pair(
            a1, a5, local1, local5, objective, hol_blocks,
            args.equality_face)
        dual1 = np.zeros_like(a1)
        dual5 = np.zeros_like(a5)
        start_iteration = 0
        print("initialized from primal ADMM duals", args.load_primal,
              "rho", rho, "sign", args.primal_dual_sign)
    else:
        zero = np.zeros((103, 103, 103), dtype=float)
        a1 = project_cone(zero, blocks1, args.equality_face, full=False)
        a5 = project_cone(zero, blocks5, args.equality_face,
                          full=gamma5_full)
        b1, b5 = project_slack_pair(
            a1, a5, local1, local5, objective, hol_blocks,
            args.equality_face)
        dual1 = np.zeros_like(a1)
        dual5 = np.zeros_like(a5)
        start_iteration = 0

    previous_b1 = b1.copy()
    previous_b5 = b5.copy()
    start = time.time()
    for step in range(1, args.iterations + 1):
        iteration = start_iteration + step
        a1 = project_cone(b1 - dual1, blocks1,
                          args.equality_face, full=False)
        a5 = project_cone(b5 - dual5, blocks5,
                          args.equality_face, full=gamma5_full)
        relaxed1 = args.alpha * a1 + (1 - args.alpha) * b1
        relaxed5 = args.alpha * a5 + (1 - args.alpha) * b5
        b1, b5 = project_slack_pair(
            relaxed1 + dual1, relaxed5 + dual5,
            local1, local5, objective, hol_blocks, args.equality_face)
        dual1 += relaxed1 - b1
        dual5 += relaxed5 - b5

        if step == 1 or iteration % args.report == 0:
            residual = np.hypot(la.norm(a1 - b1), la.norm(a5 - b5))
            change = np.hypot(la.norm(b1 - previous_b1),
                              la.norm(b5 - previous_b5))
            y1 = (a1 + b1) / 2
            y5 = (a5 + b5) / 2
            result = audit(
                y1, y5, local1, local5, objective, hol_blocks,
                blocks1, blocks5, args.equality_face, x0, z10, z50,
                args.rank_tol)
            print(f"iter {iteration:6d} residual {residual:.4g} "
                  f"change {change:.4g} norms ({la.norm(y1):.6g},"
                  f"{la.norm(y5):.6g}) sec {time.time()-start:.1f}")
            print_summary("slack", result["slack"])
            print_summary("Gamma1 dual", result["gamma1"])
            print_summary("Gamma5 dual", result["gamma5"])
            if "pairings" in result:
                print("  equality pairings slack/Gamma1/Gamma5:",
                      result["pairings"])
            print("  least slack blocks:", result["slack"]["smallest"][:5])
            if args.save:
                np.savez(
                    args.save, a1=a1, a5=a5, b1=b1, b5=b5,
                    dual1=dual1, dual5=dual5, y1=y1, y5=y5,
                    slack=result["slack_tensor"],
                    iteration=np.array(iteration),
                    residual=np.array(residual), change=np.array(change),
                    equality_face=np.array(args.equality_face),
                )
        previous_b1 = b1.copy()
        previous_b5 = b5.copy()
    return a1, a5, b1, b5


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=500)
    parser.add_argument("--alpha", type=float, default=1.7)
    parser.add_argument("--report", type=int, default=25)
    parser.add_argument("--save")
    parser.add_argument("--resume")
    parser.add_argument("--load-primal")
    parser.add_argument("--primal-dual-sign", type=float, default=1.0)
    parser.add_argument(
        "--product-face", default="/tmp/dth_product_face_bases.npz")
    parser.add_argument(
        "--gamma5-cache", default="/tmp/dth_gamma5_local_crossing_root.npz")
    parser.add_argument("--gamma5-face")
    parser.add_argument(
        "--equality", default="/tmp/dth_computational_equality.npz")
    parser.add_argument("--equality-face", action="store_true")
    parser.add_argument("--face-tol", type=float, default=1e-10)
    parser.add_argument("--rank-tol", type=float, default=1e-9)
    args = parser.parse_args()
    solve(args)


if __name__ == "__main__":
    main()
