#!/usr/bin/env python3
"""Construct the computational product-DTH equality twirl in solver coordinates.

The physical triple is

    u0 = |111>,  u1 = |112>,  z = |000>.

Its five-replica monomial is expanded into 16 rank-one terms, locally twirled
through the selected 103 permutation diagrams, and converted to the
Hilbert--Schmidt-normalized Schur coordinates used by the invariant solver.
The resulting point should have trace one, lie in the exact 2266-dimensional
product face, and have lifted DTH objective zero.

This is a floating conversion/audit utility.  The input vectors and all raw
diagram moments are integers, but the Schur basis conversion is numerical.
"""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path
import sys

import numpy as np
import scipy.linalg as la

import agent_dth_invariant_crossing as cross
import agent_dth_primal_admm as primal


EXACT_BRIDGE = (Path(__file__).resolve().parent.parent / "verification"
                / "agent_dth_local_crossing_exact.py")
sys.path.insert(0, str(EXACT_BRIDGE.parent))
SPEC = importlib.util.spec_from_file_location("dth_exact_bridge", EXACT_BRIDGE)
BRIDGE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(BRIDGE)


def cycle_count(permutation):
    seen = set()
    cycles = 0
    for start in range(5):
        if start in seen:
            continue
        cycles += 1
        point = start
        while point not in seen:
            seen.add(point)
            point = permutation[point]
    return cycles


def compose_inverse(left, right):
    inverse = [0] * 5
    for index, value in enumerate(left):
        inverse[value] = index
    return tuple(inverse[right[index]] for index in range(5))


def local_moment(ket, bra, permutation):
    value = 1.0
    for position in range(5):
        value *= np.vdot(bra[permutation[position]], ket[position]).real
    return value


def local_twirl_transform(hol):
    selected = BRIDGE.SELECTED_PERMUTATIONS
    restriction = []
    for permutation in selected:
        matrix = cross.permutation_matrix(permutation)
        restriction.append(np.concatenate(
            [(basis.T @ matrix @ basis).reshape(-1) for basis in hol]))
    restriction = np.column_stack(restriction)
    gram = np.array([
        [3 ** cycle_count(compose_inverse(left, right))
         for right in selected]
        for left in selected], dtype=float)
    transform = restriction @ la.inv(gram)

    scale = np.empty(103)
    offset = 0
    for multiplicity, carrier in zip(cross.HOL_MULTS,
                                     cross.HOL_CARRIER_DIMS):
        scale[offset:offset + multiplicity * multiplicity] = np.sqrt(carrier)
        offset += multiplicity * multiplicity
    return scale[:, None] * transform, selected


def main():
    crossing_data, hol, mixed = cross.local_crossing(verbose=False)
    local, hol_ranges, mixed_ranges = primal.normalized_local_crossing(
        crossing_data)
    target = cross.target_highest_weight_bases()
    support = cross.local_support_highest_blocks(mixed, target, verbose=False)
    hol_blocks, objective, trace = primal.prepare_hol_blocks(hol_ranges)
    mixed_blocks = primal.prepare_mixed_blocks(mixed_ranges, support)
    product_face_path = Path("/tmp/dth_product_face_bases.npz")
    if not product_face_path.exists():
        raise FileNotFoundError(product_face_path)
    primal.restrict_mixed_blocks_to_product_face(
        mixed_blocks, np.load(product_face_path))

    transform, selected = local_twirl_transform(hol)
    e = [np.eye(3)[index] for index in range(3)]
    sites = ((e[1], e[1], e[0]),
             (e[1], e[1], e[0]),
             (e[1], e[2], e[0]))

    x = np.zeros((103, 103, 103), dtype=float)
    for alpha, beta, gamma, delta in itertools.product(range(2), repeat=4):
        vectors = []
        for a, b, z in sites:
            ket = ([b, a] if alpha else [a, b])
            ket += ([b, a] if beta else [a, b])
            ket += [z]
            bra = ([b, a] if gamma else [a, b])
            bra += ([b, a] if delta else [a, b])
            bra += [z]
            moments = np.array([
                local_moment(ket, bra, permutation)
                for permutation in selected])
            vectors.append(transform @ moments)
        sign = -1 if (alpha + beta + gamma + delta) % 2 else 1
        x += (sign / 4) * np.einsum(
            "i,j,k->ijk", vectors[0], vectors[1], vectors[2])

    z = primal.crossing_apply(local, x)
    trace_value = float(np.vdot(trace, x).real)
    objective_value = float(np.vdot(objective, x).real)
    hol_min = primal.cone_minimum_eigenvalue(x, hol_blocks)
    mixed_min = primal.cone_minimum_eigenvalue(z, mixed_blocks, mixed=True)
    supported = np.zeros_like(z)
    for block in mixed_blocks:
        basis = block["kernel"]
        if not basis.shape[1]:
            continue
        matrix = primal.get_block(z, block["indices"], block["dimensions"])
        projected = basis @ (basis.T @ matrix @ basis) @ basis.T
        primal.put_block(supported, block["indices"], projected,
                         block["dimensions"])
    support_residual = float(la.norm(z - supported))

    print("computational equality trace:", trace_value)
    print("computational equality objective:", objective_value)
    print("hol/mixed cone minima:", hol_min, mixed_min)
    print("exact-product-face support residual:", support_residual)
    print("crossing norm audit:", la.norm(x), la.norm(z))
    np.savez("/tmp/dth_computational_equality.npz", x=x, z=z,
             trace=np.array(trace_value), objective=np.array(objective_value),
             support_residual=np.array(support_residual))


if __name__ == "__main__":
    main()
