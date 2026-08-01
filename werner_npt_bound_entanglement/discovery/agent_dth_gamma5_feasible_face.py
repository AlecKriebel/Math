#!/usr/bin/env python3
"""Export the numerical Gamma5 face exposed by an interior DTH feasibility point.

The objective-free two-PPT ADMM produces a point which is full rank on the
holomorphic support and on the exact Gamma1 product face, but lies on a
proper Gamma5 face.  This utility records the blockwise range/kernel bases
of that face for exact representation-theoretic reconstruction.

The export is discovery data only.  Exact rank claims require reconstructing
the kernels through the exact Gamma5 diagram bridge.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np


NAMES = ("00", "03", "11", "22", "30", "41")
MULTS = (3, 2, 8, 3, 4, 1)
CARRIERS = (1, 10, 8, 27, 10, 35)


def coordinate_ranges():
    output = []
    offset = 0
    for multiplicity in MULTS:
        output.append(
            np.arange(offset, offset + multiplicity**2)
            .reshape(multiplicity, multiplicity)
        )
        offset += multiplicity**2
    assert offset == 103
    return output


def block_indices(ranges, shapes):
    grids = [ranges[s] for s in shapes]
    return (grids[0][:, None, None, :, None, None],
            grids[1][None, :, None, None, :, None],
            grids[2][None, None, :, None, None, :])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--checkpoint", default="/tmp/dth_double_feas_root500.npz")
    parser.add_argument(
        "--output", default="/tmp/dth_gamma5_feasible_face.npz")
    parser.add_argument("--tolerance", type=float, default=1e-9)
    args = parser.parse_args()

    checkpoint = np.load(args.checkpoint)
    z5 = checkpoint["z5"]
    ranges = coordinate_ranges()
    export = {
        "source_checkpoint": np.array(args.checkpoint),
        "names": np.asarray(NAMES),
        "mults": np.asarray(MULTS, dtype=int),
        "carriers": np.asarray(CARRIERS, dtype=int),
        "tolerance": np.array(args.tolerance),
        "iteration": checkpoint["iteration"],
        "residual1": checkpoint["residual1"],
        "residual5": checkpoint["residual5"],
        "support_leakage": checkpoint["support_leakage"],
    }
    rows = []
    all_values = []
    total_rank = 0
    for shapes in itertools.product(range(6), repeat=3):
        dimensions = tuple(MULTS[s] for s in shapes)
        size = int(np.prod(dimensions))
        matrix = z5[block_indices(ranges, shapes)].reshape(size, size)
        matrix = (matrix + matrix.T) / 2
        values, vectors = np.linalg.eigh(matrix)
        scale = max(1.0, float(np.max(np.abs(values))))
        rank = int(np.sum(values > args.tolerance * scale))
        key = "".join(map(str, shapes))
        export[f"eval_{key}"] = values
        export[f"range_{key}"] = vectors[:, size - rank:]
        export[f"kernel_{key}"] = vectors[:, :size - rank]
        export[f"matrix_{key}"] = matrix
        total_rank += rank
        all_values.extend(values)
        rows.append((key, shapes, dimensions, size, rank,
                     float(values[size - rank]) if rank else np.inf,
                     float(values[size - rank - 1]) if rank < size else -np.inf,
                     float(values[-1])))

    positives = [row for row in rows if row[4]]
    values = np.sort(np.asarray(all_values))
    threshold_index = int(np.searchsorted(values, args.tolerance))
    largest_kernel = float(values[threshold_index - 1])
    smallest_positive = float(values[threshold_index])
    export["total_rank"] = np.array(total_rank)
    export["active_blocks"] = np.array(len(positives))
    export["largest_kernel_eigenvalue"] = np.array(largest_kernel)
    export["smallest_positive_eigenvalue"] = np.array(smallest_positive)
    np.savez(args.output, **export)

    print("source:", args.checkpoint)
    print("iteration/residuals/support:", int(checkpoint["iteration"]),
          float(checkpoint["residual1"]), float(checkpoint["residual5"]),
          float(checkpoint["support_leakage"]))
    print("Gamma5 rank/active blocks:", total_rank, len(positives))
    print("largest kernel / smallest positive eigenvalue:",
          largest_kernel, smallest_positive)
    print("zero blocks:", [row[0] for row in rows if not row[4]])
    print("rank census")
    for row in rows:
        key, shapes, dimensions, size, rank, gap, below, maximum = row
        print(key, "/".join(NAMES[s] for s in shapes), dimensions,
              f"rank {rank}/{size}", f"first {gap:.12g}",
              f"below {below:.3g}", f"max {maximum:.12g}")
    print("saved:", args.output)


if __name__ == "__main__":
    main()
