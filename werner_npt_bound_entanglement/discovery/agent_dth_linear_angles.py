#!/usr/bin/env python3
"""Principal-angle audit for the facially reduced DTH linear supports.

The holomorphic Hermitian support has only 4,139 real coordinates after local
Schur reduction.  This program builds an orthonormal coordinate codec and
uses a matrix-free Lanczos calculation on

    P_hol U^T P_face U P_hol.

Eigenvalue one is the common linear intersection; near-one eigenvalues expose
the conditioning that can make small ADMM residuals misleading.  Results are
floating-point discovery diagnostics only.
"""

from __future__ import annotations

import argparse

import numpy as np
import scipy.sparse.linalg as sla

import agent_dth_invariant_crossing as cross
import agent_dth_primal_admm as primal
import agent_dth_primal_bracket as bracket


class HolSymmetricCodec:
    def __init__(self, blocks):
        self.blocks = []
        offset = 0
        for block in blocks:
            k = block["basis"].shape[1]
            diagonal = np.arange(k)
            upper = np.triu_indices(k, 1)
            count = k * (k + 1) // 2
            self.blocks.append((block, slice(offset, offset + count),
                                diagonal, upper))
            offset += count
        self.size = offset

    def decode(self, vector):
        tensor = np.zeros((103, 103, 103), dtype=float)
        for block, section, diagonal, upper in self.blocks:
            basis = block["basis"]
            k = basis.shape[1]
            if not k:
                continue
            data = vector[section]
            matrix = np.zeros((k, k), dtype=float)
            matrix[diagonal, diagonal] = data[:k]
            matrix[upper] = data[k:] / np.sqrt(2)
            matrix[(upper[1], upper[0])] = data[k:] / np.sqrt(2)
            full = basis @ matrix @ basis.T
            primal.put_block(tensor, block["indices"], full,
                             block["dimensions"])
        return tensor

    def encode(self, tensor):
        vector = np.zeros(self.size, dtype=float)
        for block, section, diagonal, upper in self.blocks:
            basis = block["basis"]
            k = basis.shape[1]
            if not k:
                continue
            full = primal.get_block(
                tensor, block["indices"], block["dimensions"])
            matrix = basis.T @ ((full + full.T) / 2) @ basis
            data = np.empty(section.stop - section.start, dtype=float)
            data[:k] = matrix[diagonal, diagonal]
            data[k:] = np.sqrt(2) * matrix[upper]
            vector[section] = data
        return vector


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mixed-face")
    parser.add_argument("--product-face")
    parser.add_argument("--mixed-face-field", default="a")
    parser.add_argument("--face-tol", type=float, default=1e-9)
    parser.add_argument("--eigenvalues", type=int, default=10)
    parser.add_argument("--ncv", type=int, default=30)
    parser.add_argument("--tol", type=float, default=1e-11)
    parser.add_argument("--maxiter", type=int, default=1000)
    parser.add_argument("--save")
    args = parser.parse_args()

    crossing_data, hol, mixed = cross.local_crossing(verbose=False)
    local, hol_ranges, mixed_ranges = primal.normalized_local_crossing(
        crossing_data)
    target = cross.target_highest_weight_bases()
    support = cross.local_support_highest_blocks(mixed, target, verbose=False)
    hol_blocks, _, trace = primal.prepare_hol_blocks(hol_ranges)
    mixed_blocks = primal.prepare_mixed_blocks(mixed_ranges, support)
    if bool(args.mixed_face) == bool(args.product_face):
        raise ValueError("choose exactly one of --mixed-face and --product-face")
    if args.product_face:
        primal.restrict_mixed_blocks_to_product_face(
            mixed_blocks, np.load(args.product_face))
    else:
        face = np.load(args.mixed_face)[args.mixed_face_field]
        primal.restrict_mixed_blocks_to_exposed_face(
            mixed_blocks, face, args.face_tol)
    codec = HolSymmetricCodec(hol_blocks)
    print("hol Hermitian coordinate dimension:", codec.size)

    rng = np.random.default_rng(20260801)
    test = rng.normal(size=codec.size)
    codec_error = np.linalg.norm(codec.encode(codec.decode(test)) - test)
    print("codec roundtrip error:", codec_error)

    def action(vector):
        tensor = codec.decode(vector)
        mixed_tensor = primal.crossing_apply(local, tensor)
        mixed_tensor = bracket.project_mixed_linear(
            mixed_tensor, mixed_blocks)
        pulled = primal.crossing_apply(local, mixed_tensor, transpose=True)
        return codec.encode(pulled)

    operator = sla.LinearOperator((codec.size, codec.size), matvec=action,
                                  dtype=float)
    values, vectors = sla.eigsh(
        operator, k=args.eigenvalues, which="LA", ncv=args.ncv,
        tol=args.tol, maxiter=args.maxiter)
    order = np.argsort(values)[::-1]
    values = values[order]
    vectors = vectors[:, order]
    print("largest eigenvalues:")
    for index, value in enumerate(values):
        residual = np.linalg.norm(action(vectors[:, index])
                                  - value * vectors[:, index])
        print(index, repr(float(value)), "gap", repr(float(1 - value)),
              "residual", residual)

    trace_vector = codec.encode(trace)
    overlaps = vectors.T @ (trace_vector / np.linalg.norm(trace_vector))
    print("normalized trace overlaps:", overlaps)
    if args.save:
        np.savez(args.save, values=values, vectors=vectors,
                 trace_vector=trace_vector)


if __name__ == "__main__":
    main()
