#!/usr/bin/env python3
"""Recover every exact mixed product-face coordinate block by CRT.

The full-face verifier proves that the corrected holomorphic certificate
crosses into the exact product face.  This generator additionally retains
the 64,900 entries of the face pivot principal submatrices during the same
CRT replay.  Once the modulus exceeds twice the rigorous mixed-entry bound,
those integer entries are uniquely reconstructed and the exact coordinate
matrices

    B = E_J^{-1} M_JJ E_J^{-T}

are exported for an independent small-block PSD verifier.

This is certificate generation code.  The output must be checked by the
independent verifier; it is not itself a proof.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from pathlib import Path
import argparse
import importlib.util
import json

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parent.parent
VERIFY_PATH = ROOT / "verification" / "agent_dth_full_face_crt.py"
SPEC = importlib.util.spec_from_file_location("dth_full_face_export", VERIFY_PATH)
FULL = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(FULL)


def crt_update(current, new_residue, modulus, prime):
    if current.size == 0:
        return current
    current_mod = np.asarray(
        [int(value) % prime for value in current.flat], dtype=np.int64
    ).reshape(current.shape)
    inverse = pow(modulus % prime, -1, prime)
    delta = (new_residue - current_mod) % prime
    delta = delta * inverse % prime
    return current + modulus * delta.astype(object)


def signed_representatives(matrix, modulus, bound):
    half = modulus // 2
    output = np.empty(matrix.shape, dtype=object)
    maximum = 0
    for index, value in enumerate(matrix.flat):
        value = int(value)
        if value > half:
            value -= modulus
        maximum = max(maximum, abs(value))
        output.flat[index] = value
    assert maximum <= bound
    return output


def write_mixed_certificate(path, blocks, source_path, modulus_bits,
                            mixed_denominator):
    output = {
        "version": 1,
        "source": str(source_path),
        "crt_modulus_bits": modulus_bits,
        "mixed_denominator": str(mixed_denominator),
        "blocks": {},
    }
    for shapes in product(range(6), repeat=3):
        matrix = blocks[shapes]
        dimension = matrix.rows
        entries = []
        for i in range(dimension):
            value = Fraction(int(sp.numer(matrix[i, i])),
                             int(sp.denom(matrix[i, i])))
            entries.append([value.numerator, value.denominator])
        for i in range(dimension):
            for j in range(i + 1, dimension):
                value = Fraction(int(sp.numer(matrix[i, j])),
                                 int(sp.denom(matrix[i, j])))
                entries.append([value.numerator, value.denominator])
        output["blocks"]["".join(map(str, shapes))] = {
            "dimension": dimension,
            "upper": entries,
        }
    path.write_text(json.dumps(output, separators=(",", ":")))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate", default="/tmp/dth_exact_obstruction_v2.json.gz"
    )
    parser.add_argument("--output", default="/tmp/dth_exact_mixed_coordinates.json")
    parser.add_argument("--maximum-primes", type=int, default=1000)
    args = parser.parse_args()

    coordinates, coordinate_denominator = FULL.parse_certificate(args.certificate)
    crossing = FULL.exact_crossing_numerator()
    hol_charts, integer_coordinates, hol_bound = FULL.integer_hol_charts(
        coordinates, coordinate_denominator
    )
    (face_kernels, maximum_l1, face_charts,
     face_pivots) = FULL.integer_face_kernels(with_charts=True)
    crossing_row_l1 = max(
        sum(abs(int(value)) for value in row) for row in crossing
    )
    mixed_bound = hol_bound * crossing_row_l1 ** 3
    residual_bound = maximum_l1 * mixed_bound
    print("mixed entry bound bits:", mixed_bound.bit_length(), flush=True)
    print("residual bound bits:", residual_bound.bit_length(), flush=True)

    residues = {
        shapes: np.zeros((len(face_pivots[shapes]), len(face_pivots[shapes])),
                         dtype=object)
        for shapes in product(range(6), repeat=3)
    }
    modulus = 1
    hol_ranges = FULL.block_ranges(FULL.BRIDGE.HOL_MULTS)
    mixed_ranges = FULL.block_ranges(FULL.BRIDGE.MIXED_MULTS)
    primes = []
    for prime in FULL.deterministic_primes():
        pivot_blocks = FULL.replay_prime(
            prime, crossing, hol_charts, integer_coordinates, face_kernels,
            hol_ranges, mixed_ranges, face_pivots,
        )
        for shapes in product(range(6), repeat=3):
            residues[shapes] = crt_update(
                residues[shapes], pivot_blocks[shapes], modulus, prime
            )
        modulus *= prime
        primes.append(prime)
        print("mixed CRT prime", len(primes), prime,
              "modulus bits", modulus.bit_length(), flush=True)
        if modulus > 2 * residual_bound:
            break
        if len(primes) >= args.maximum_primes:
            raise RuntimeError("maximum prime count did not exceed bound")
    assert modulus > 2 * residual_bound

    mixed_denominator = (
        coordinate_denominator
        * FULL.HOL_SCALE ** 2
        * FULL.CROSS_SCALE ** 3
    )
    exact_blocks = {}
    for count, shapes in enumerate(product(range(6), repeat=3), 1):
        signed = signed_representatives(
            residues[shapes], modulus, mixed_bound
        )
        face = sp.Matrix(face_charts[shapes].tolist())
        pivots = face_pivots[shapes]
        rank = len(pivots)
        if rank:
            principal = face[list(pivots), :]
            mixed_principal = sp.Matrix(signed.tolist()) / mixed_denominator
            coordinate = principal.inv() * mixed_principal * principal.inv().T
            coordinate = coordinate.applyfunc(sp.factor)
            assert coordinate == coordinate.T
        else:
            coordinate = sp.zeros(0)
        exact_blocks[shapes] = coordinate
        if count % 24 == 0:
            print("recovered exact mixed blocks", count, "/216", flush=True)

    output = Path(args.output)
    write_mixed_certificate(
        output, exact_blocks, Path(args.certificate),
        modulus.bit_length(), mixed_denominator,
    )
    print("wrote", output, "bytes", output.stat().st_size, flush=True)


if __name__ == "__main__":
    main()
