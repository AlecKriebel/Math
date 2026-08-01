#!/usr/bin/env python3
"""Unrestricted invariant primal search with both DTH PPT constraints.

This is discovery code for the strengthened first five-replica relaxation

  minimize   <O0~, rho>
  subject to rho >= 0 on the holomorphic Pluecker/Omega support,
             Tr(rho) = 1,
             rho^Gamma_1 >= 0 on the mixed support kernel,
             rho^Gamma_5 >= 0.

Here Gamma_1 transposes the first bivector pair and Gamma_5 transposes the
final ``z`` replica.  Local-unitary invariance reduces every local commutant
to 103 Hilbert--Schmidt normalized coordinates.  Both partial transposes are
real orthogonal 103 by 103 maps, and the global maps are their tensor cubes.

The program uses a three-cone consensus ADMM.  Its output is numerical
discovery evidence only.  In particular, a negative iterate is not a theorem
until it is reconstructed and replayed by a separate exact verifier.
"""

from __future__ import annotations

import argparse
import itertools
from pathlib import Path
import time

import numpy as np
import scipy.linalg as la

import agent_dth_invariant_crossing as cross
import agent_dth_primal_admm as primal


# V^tensor4 tensor conjugate(V), ordered as in the cached numerical bridge.
FINAL_WEIGHTS = ((0, 0), (0, 3), (1, 1), (2, 2), (3, 0), (4, 1))
FINAL_NAMES = ("00", "03", "11", "22", "30", "41")
FINAL_CARRIER_DIMS = (1, 10, 8, 27, 10, 35)
FINAL_MULTS = (3, 2, 8, 3, 4, 1)

assert sum(d * m for d, m in zip(FINAL_CARRIER_DIMS, FINAL_MULTS)) == 3**5
assert sum(m * m for m in FINAL_MULTS) == 103


def final_weight(word):
    counts = [0, 0, 0]
    for position, value in enumerate(word):
        counts[value] += -1 if position == 4 else 1
    return tuple(counts)


def final_gl_weight(pq):
    """Compatible GL(3) highest weight of net tensor degree three."""
    p, q = pq
    bottom = (3 - p - 2 * q) // 3
    assert 3 * bottom == 3 - p - 2 * q
    return (bottom + q + p, bottom + q, bottom)


def final_raised_words(word, simple_root):
    high = simple_root
    low = simple_root + 1
    for position, value in enumerate(word):
        if position == 4:
            if value == high:
                out = list(word)
                out[position] = low
                yield tuple(out), -1.0
        elif value == low:
            out = list(word)
            out[position] = high
            yield tuple(out), 1.0


def final_raising_matrix(source_indices, simple_root):
    rows = {}
    terms = []
    for column, source in enumerate(source_indices):
        for word, coefficient in final_raised_words(
                cross.WORDS[source], simple_root):
            row = rows.setdefault(word, len(rows))
            terms.append((row, column, coefficient))
    matrix = np.zeros((len(rows), len(source_indices)), dtype=float)
    for row, column, coefficient in terms:
        matrix[row, column] += coefficient
    return matrix


def final_highest_weight_bases(tol=1e-10):
    bases = []
    for pq, expected in zip(FINAL_WEIGHTS, FINAL_MULTS):
        weight = final_gl_weight(pq)
        indices = [index for index, word in enumerate(cross.WORDS)
                   if final_weight(word) == weight]
        raising = np.vstack((final_raising_matrix(indices, 0),
                             final_raising_matrix(indices, 1)))
        kernel = la.null_space(raising, rcond=tol)
        if kernel.shape[1] != expected:
            raise RuntimeError(
                f"final type {pq}: kernel {kernel.shape[1]}, expected "
                f"{expected}")
        full = np.zeros((cross.LOCAL_DIM, expected), dtype=float)
        full[indices, :] = kernel
        bases.append(full)
    return bases


def partial_transpose_last(operator):
    tensor = operator.reshape((cross.D,) * (2 * cross.NREP))
    axes = list(range(2 * cross.NREP))
    axes[4], axes[9] = axes[9], axes[4]
    return tensor.transpose(axes).reshape(operator.shape)


def coordinate_ranges(multiplicities):
    ranges = []
    offset = 0
    for multiplicity in multiplicities:
        ranges.append(np.arange(offset, offset + multiplicity**2).reshape(
            multiplicity, multiplicity))
        offset += multiplicity**2
    assert offset == 103
    return ranges


def build_final_local_crossing(verbose=True):
    """Construct the normalized Gamma_5 crossing from permutation diagrams."""
    hol = cross.hol_highest_weight_bases()
    final = final_highest_weight_bases()
    hol_columns = []
    final_columns = []
    for permutation in itertools.permutations(range(cross.NREP)):
        operator = cross.permutation_matrix(permutation)
        hol_columns.append(cross.flatten_blocks(
            [basis.T @ operator @ basis for basis in hol]))
        crossed = partial_transpose_last(operator)
        final_columns.append(cross.flatten_blocks(
            [basis.T @ crossed @ basis for basis in final]))
    hol_restriction = np.column_stack(hol_columns)
    final_restriction = np.column_stack(final_columns)
    _, triangular, pivots = la.qr(
        hol_restriction, mode="economic", pivoting=True)
    rank = int(np.sum(np.abs(np.diag(triangular)) > 1e-9))
    if rank != 103:
        raise RuntimeError(f"holomorphic commutant rank {rank}, expected 103")
    selected = pivots[:rank]
    square = hol_restriction[:, selected]
    # If h is the vector of highest-weight restrictions, then raw @ h is
    # the final-slot highest-weight restriction after partial transpose.
    raw = la.solve(square.T, final_restriction[:, selected].T).T
    input_carriers = np.concatenate([
        np.full(f * f, d, dtype=float)
        for f, d in zip(cross.HOL_MULTS, cross.HOL_CARRIER_DIMS)
    ])
    output_carriers = np.concatenate([
        np.full(m * m, d, dtype=float)
        for m, d in zip(FINAL_MULTS, FINAL_CARRIER_DIMS)
    ])
    local = (np.sqrt(output_carriers)[:, None] * raw
             / np.sqrt(input_carriers)[None, :])
    orthogonality = la.norm(local.T @ local - np.eye(103), ord=2)

    trace_in = np.zeros(103)
    trace_out = np.zeros(103)
    offset = 0
    for f, d in zip(cross.HOL_MULTS, cross.HOL_CARRIER_DIMS):
        for index in range(f):
            trace_in[offset + index * f + index] = np.sqrt(d)
        offset += f * f
    offset = 0
    for m, d in zip(FINAL_MULTS, FINAL_CARRIER_DIMS):
        for index in range(m):
            trace_out[offset + index * m + index] = np.sqrt(d)
        offset += m * m
    trace_error = la.norm(trace_out @ local - trace_in)
    if verbose:
        print("Gamma5 local crossing diagnostics")
        print("  final weights:", FINAL_WEIGHTS)
        print("  final multiplicities:", FINAL_MULTS)
        print("  commutant rank:", rank)
        print("  orthogonality error:", orthogonality)
        print("  trace error:", trace_error)
    assert orthogonality < 3e-8
    assert trace_error < 2e-7
    return local


def load_or_build_final_crossing(cache, rebuild=False):
    path = Path(cache) if cache else None
    if path is not None and path.exists() and not rebuild:
        data = np.load(path)
        local = data["local"]
        assert tuple(map(tuple, data["weights"])) == FINAL_WEIGHTS
        assert tuple(map(int, data["mults"])) == FINAL_MULTS
        assert tuple(map(int, data["carriers"])) == FINAL_CARRIER_DIMS
        error = la.norm(local.T @ local - np.eye(103), ord=2)
        print("loaded Gamma5 crossing", path,
              "orthogonality error", error)
        assert error < 3e-8
    else:
        local = build_final_local_crossing(verbose=True)
        if path is not None:
            np.savez(path, local=local,
                     weights=np.asarray(FINAL_WEIGHTS, dtype=int),
                     mults=np.asarray(FINAL_MULTS, dtype=int),
                     carriers=np.asarray(FINAL_CARRIER_DIMS, dtype=int))
            print("saved Gamma5 crossing", path)
    return local, coordinate_ranges(FINAL_MULTS)


def prepare_full_psd_blocks(local_ranges):
    blocks = []
    for shapes in itertools.product(range(len(FINAL_MULTS)), repeat=3):
        dimensions = tuple(FINAL_MULTS[shape] for shape in shapes)
        size = int(np.prod(dimensions))
        blocks.append({
            "shapes": shapes,
            "dimensions": dimensions,
            "indices": primal.block_indices(local_ranges, shapes),
            "kernel": np.eye(size),
        })
    return blocks


def restrict_blocks_to_snapshot_range(blocks, tensor, tolerance=1e-10):
    """Restrict PSD blocks to the positive range of a facial snapshot.

    This is a numerical acceleration/diagnostic only unless a separate exact
    argument proves that the displayed face contains the full feasible cone.
    """
    before = sum(block["kernel"].shape[1] for block in blocks)
    after = 0
    smallest_retained = np.inf
    largest_discarded = -np.inf
    retained_blocks = 0
    for block in blocks:
        kernel = block["kernel"]
        matrix = primal.get_block(
            tensor, block["indices"], block["dimensions"])
        compressed = kernel.T @ ((matrix + matrix.T) / 2) @ kernel
        values, vectors = la.eigh(compressed)
        keep = values > tolerance
        if np.any(keep):
            smallest_retained = min(smallest_retained,
                                    float(np.min(values[keep])))
            retained_blocks += 1
        if np.any(~keep):
            largest_discarded = max(largest_discarded,
                                    float(np.max(values[~keep])))
        block["kernel"] = kernel @ vectors[:, keep]
        after += int(np.sum(keep))
    print("snapshot range-face restriction:", before, "->", after,
          "in", retained_blocks, "blocks; smallest retained",
          smallest_retained, "largest discarded", largest_discarded,
          "tolerance", tolerance)
    return blocks


def linear_range_projection(tensor, blocks):
    out = np.zeros_like(tensor)
    for block in blocks:
        matrix = primal.get_block(
            tensor, block["indices"], block["dimensions"])
        kernel = block["kernel"]
        compressed = kernel.T @ matrix @ kernel
        primal.put_block(out, block["indices"],
                         kernel @ compressed @ kernel.T,
                         block["dimensions"])
    return out


def spectral_summary(tensor, blocks, supported, tolerance=1e-9):
    minimum = np.inf
    worst = None
    negative = zero = positive = 0
    active_blocks = 0
    positive_blocks = 0
    for block in blocks:
        matrix = primal.get_block(
            tensor, block["indices"], block["dimensions"])
        basis = block["kernel"] if supported else block["basis"]
        if not basis.shape[1]:
            continue
        compressed = basis.T @ ((matrix + matrix.T) / 2) @ basis
        values = la.eigvalsh(compressed)
        current = float(values[0])
        if current < minimum:
            minimum = current
            worst = block["shapes"]
        nnegative = int(np.sum(values < -tolerance))
        npositive = int(np.sum(values > tolerance))
        negative += nnegative
        positive += npositive
        zero += len(values) - nnegative - npositive
        if np.max(np.abs(values)) > tolerance:
            active_blocks += 1
        if npositive:
            positive_blocks += 1
    return {
        "minimum": minimum,
        "worst": worst,
        "negative": negative,
        "zero": zero,
        "positive": positive,
        "active_blocks": active_blocks,
        "positive_blocks": positive_blocks,
    }


def print_summary(label, summary):
    print(f"  {label}: min {summary['minimum']:+.4g} at "
          f"{summary['worst']}; inertia "
          f"({summary['positive']},{summary['negative']},"
          f"{summary['zero']}); positive/active blocks "
          f"{summary['positive_blocks']}/{summary['active_blocks']}")


def audit_known_obstruction(local5, final_ranges, path):
    checkpoint = np.load(path)
    x = checkpoint["x"]
    gamma5 = primal.crossing_apply(local5, x)
    blocks5 = prepare_full_psd_blocks(final_ranges)
    summary = spectral_summary(gamma5, blocks5, supported=True,
                               tolerance=1e-11)
    print("known Gamma1-only obstruction under Gamma5:")
    print_summary("Gamma5", summary)
    type30 = FINAL_WEIGHTS.index((3, 0))
    shapes = (type30,) * 3
    dimensions = (FINAL_MULTS[type30],) * 3
    matrix = primal.get_block(
        gamma5, primal.block_indices(final_ranges, shapes), dimensions)
    values = la.eigvalsh((matrix + matrix.T) / 2)
    print("  (30)^3 leading eigenvalues:", values[:6])
    if values[0] >= -1e-10:
        raise RuntimeError("Gamma5 crossing failed the known NPT audit")


def setup(args):
    crossing1, hol, mixed = cross.local_crossing(verbose=True)
    local1, hol_ranges, mixed_ranges = primal.normalized_local_crossing(
        crossing1)
    local5, final_ranges = load_or_build_final_crossing(
        args.final_crossing_cache, args.rebuild_final_crossing)
    target = cross.target_highest_weight_bases()
    support = cross.local_support_highest_blocks(mixed, target, verbose=True)

    print("preparing 125 holomorphic Pluecker/Omega blocks")
    hol_blocks, objective, trace = primal.prepare_hol_blocks(hol_ranges)
    print("preparing 216 Gamma1 mixed-support blocks")
    blocks1 = primal.prepare_mixed_blocks(mixed_ranges, support)
    print("preparing 216 unrestricted Gamma5 blocks")
    blocks5 = prepare_full_psd_blocks(final_ranges)
    if args.gamma1_product_face:
        primal.restrict_mixed_blocks_to_product_face(
            blocks1, np.load(args.gamma1_product_face))
    if args.gamma5_range_face:
        snapshot = np.load(args.gamma5_range_face)
        restrict_blocks_to_snapshot_range(
            blocks5, snapshot[args.gamma5_range_face_field],
            args.range_face_tol)
    print("supported dimensions hol/Gamma1/Gamma5:",
          sum(block["basis"].shape[1] for block in hol_blocks),
          sum(block["kernel"].shape[1] for block in blocks1),
          sum(block["kernel"].shape[1] for block in blocks5))
    return (local1, local5, hol_blocks, blocks1, blocks5,
            objective, trace, final_ranges)


def solve(args):
    (local1, local5, hol_blocks, blocks1, blocks5,
     objective, trace, final_ranges) = setup(args)
    if args.audit_known:
        audit_known_obstruction(local5, final_ranges, args.audit_known)
    if args.setup_only:
        return None

    rho = args.rho
    if args.load:
        checkpoint = np.load(args.load)
        x = checkpoint["x"]
        z1 = checkpoint["z1"]
        z5 = checkpoint["z5"]
        load_rho = float(checkpoint["rho"]) if "rho" in checkpoint else args.load_rho
        dual1 = checkpoint["dual1"] * (load_rho / rho)
        dual5 = checkpoint["dual5"] * (load_rho / rho)
        start_iteration = int(checkpoint["iteration"])
        print("loaded full checkpoint", args.load, "at iteration",
              start_iteration, "and rescaled duals from", load_rho, "to", rho)
    else:
        start_iteration = 0
        if args.load_x:
            source = np.load(args.load_x)
            x = source[args.load_x_field]
            x = primal.project_hol_trace_one(x, hol_blocks)
            print("initialized x from", args.load_x,
                  "field", args.load_x_field)
        else:
            x = primal.project_hol_trace_one(
                -args.objective_scale * objective / max(2 * rho, 1e-12),
                hol_blocks)
        z1 = primal.project_mixed(
            primal.crossing_apply(local1, x), blocks1)
        z5 = primal.project_mixed(
            primal.crossing_apply(local5, x), blocks5)
        dual1 = np.zeros_like(x)
        dual5 = np.zeros_like(x)

    previous_z1 = z1.copy()
    previous_z5 = z5.copy()
    start = time.time()
    for step in range(1, args.iterations + 1):
        iteration = start_iteration + step
        back1 = primal.crossing_apply(local1, z1 - dual1, transpose=True)
        back5 = primal.crossing_apply(local5, z5 - dual5, transpose=True)
        center = ((back1 + back5) / 2
                  - args.objective_scale * objective / (2 * rho))
        x = primal.project_hol_trace_one(center, hol_blocks)

        ux1 = primal.crossing_apply(local1, x)
        ux5 = primal.crossing_apply(local5, x)
        relaxed1 = args.alpha * ux1 + (1 - args.alpha) * z1
        relaxed5 = args.alpha * ux5 + (1 - args.alpha) * z5
        z1 = primal.project_mixed(relaxed1 + dual1, blocks1)
        z5 = primal.project_mixed(relaxed5 + dual5, blocks5)
        dual1 += relaxed1 - z1
        dual5 += relaxed5 - z5

        if step == 1 or iteration % args.report == 0:
            residual1 = la.norm(ux1 - z1)
            residual5 = la.norm(ux5 - z5)
            primal_residual = np.hypot(residual1, residual5)
            dual_separate = rho * np.hypot(
                la.norm(z1 - previous_z1), la.norm(z5 - previous_z5))
            dual_combined = rho * la.norm(
                primal.crossing_apply(local1, z1 - previous_z1,
                                      transpose=True)
                + primal.crossing_apply(local5, z5 - previous_z5,
                                        transpose=True))
            value = float(np.vdot(objective, x).real)
            trace_value = float(np.vdot(trace, x).real)
            support_leakage = la.norm(
                ux1 - linear_range_projection(ux1, blocks1))
            print(f"iter {iteration:6d} obj {value:+.12g} "
                  f"trace {trace_value:.12g} r1 {residual1:.3g} "
                  f"r5 {residual5:.3g} dual {dual_separate:.3g} "
                  f"dualA {dual_combined:.3g} rho {rho:.3g} "
                  f"suppleak {support_leakage:.3g} "
                  f"sec {time.time()-start:.1f}")
            print_summary("hol", spectral_summary(
                x, hol_blocks, supported=False, tolerance=args.rank_tol))
            print_summary("Gamma1 z", spectral_summary(
                z1, blocks1, supported=True, tolerance=args.rank_tol))
            print_summary("Gamma5 z", spectral_summary(
                z5, blocks5, supported=True, tolerance=args.rank_tol))
            print_summary("Gamma1(x)", spectral_summary(
                ux1, blocks1, supported=True, tolerance=args.rank_tol))
            print_summary("Gamma5(x)", spectral_summary(
                ux5, blocks5, supported=True, tolerance=args.rank_tol))
            print("  dual norms:", la.norm(dual1), la.norm(dual5))
            if args.save:
                np.savez(args.save, x=x, z1=z1, z5=z5,
                         dual1=dual1, dual5=dual5,
                         iteration=np.array(iteration), rho=np.array(rho),
                         objective=np.array(value), trace=np.array(trace_value),
                         residual1=np.array(residual1),
                         residual5=np.array(residual5),
                         dual_residual=np.array(dual_separate),
                         support_leakage=np.array(support_leakage))

            if args.adapt_rho:
                old_rho = rho
                if primal_residual > args.balance * max(dual_separate, 1e-16):
                    rho *= 2
                elif dual_separate > args.balance * max(primal_residual, 1e-16):
                    rho /= 2
                if rho != old_rho:
                    dual1 *= old_rho / rho
                    dual5 *= old_rho / rho
                    print("  adapted rho", old_rho, "->", rho)
        previous_z1 = z1.copy()
        previous_z5 = z5.copy()
    return x, z1, z5, dual1, dual5


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=500)
    parser.add_argument("--rho", type=float, default=10.0)
    parser.add_argument("--alpha", type=float, default=1.0)
    parser.add_argument("--objective-scale", type=float, default=1.0)
    parser.add_argument("--report", type=int, default=25)
    parser.add_argument("--rank-tol", type=float, default=1e-9)
    parser.add_argument("--save")
    parser.add_argument("--load")
    parser.add_argument("--load-rho", type=float, default=10.0)
    parser.add_argument("--load-x")
    parser.add_argument("--load-x-field", default="x")
    parser.add_argument("--adapt-rho", action="store_true")
    parser.add_argument("--balance", type=float, default=10.0)
    parser.add_argument(
        "--final-crossing-cache",
        default="/tmp/dth_gamma5_local_crossing_root.npz")
    parser.add_argument("--rebuild-final-crossing", action="store_true")
    parser.add_argument("--audit-known")
    parser.add_argument("--setup-only", action="store_true")
    parser.add_argument("--gamma1-product-face")
    parser.add_argument("--gamma5-range-face")
    parser.add_argument("--gamma5-range-face-field", default="z5")
    parser.add_argument("--range-face-tol", type=float, default=1e-10)
    args = parser.parse_args()
    solve(args)


if __name__ == "__main__":
    main()
