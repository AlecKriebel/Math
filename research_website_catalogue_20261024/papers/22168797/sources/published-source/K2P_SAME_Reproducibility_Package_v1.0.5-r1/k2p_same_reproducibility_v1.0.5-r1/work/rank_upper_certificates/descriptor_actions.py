#!/usr/bin/env python3
"""Exact port and inheritance-coordinate actions on MapDescriptor objects."""

from __future__ import annotations

from collections import defaultdict
from itertools import permutations, product

from k2p_atlas_core import MapDescriptor, ct_orbit_rep, orbit_assignments


def _switch_index(bits):
    value = 0
    for bit in bits:
        value = (value << 1) | bit
    return value


def _output_old_indices(k, port_permutation):
    """For every new coordinate, return its old-coordinate index.

    ``port_permutation[i]`` is the new label attached to old label i, matching
    ``relabel_record`` in the atlas core.
    """
    assignments = orbit_assignments(k)
    index = {chars: i for i, chars in enumerate(assignments)}
    result = []
    for new_chars in assignments:
        old_chars = tuple(new_chars[port_permutation[i]] for i in range(k))
        result.append(index[ct_orbit_rep(old_chars)])
    return tuple(result)


def _substitute_lambda_polynomial(poly, retic_count, retic_permutation, flips):
    """Substitute old lambdas by permuted/complemented new lambdas."""
    inverse = [None] * retic_count
    for new_j, old_j in enumerate(retic_permutation):
        inverse[old_j] = new_j
    answer = defaultdict(int)
    for old_mask, coefficient in poly:
        partial = {0: coefficient}
        for old_j in range(retic_count):
            if not ((old_mask >> old_j) & 1):
                continue
            new_j = inverse[old_j]
            if not flips[new_j]:
                partial = {mask | (1 << new_j): value for mask, value in partial.items()}
            else:
                expanded = defaultdict(int)
                for mask, value in partial.items():
                    expanded[mask] += value
                    expanded[mask | (1 << new_j)] -= value
                partial = {mask: value for mask, value in expanded.items() if value}
        for mask, value in partial.items():
            answer[mask] += value
    return tuple(sorted((mask, value) for mask, value in answer.items() if value))


def transform_descriptor(desc, port_permutation, retic_permutation, flips):
    """Apply one port action and one retic hyperoctahedral action exactly."""
    r = desc.retic_count
    m = len(desc.outputs)
    old_output = _output_old_indices(desc.k, port_permutation)

    # Transform every edge signature.  New switch bits nb refer to old bits
    # ob[p[j]]=nb[j]^flip[j], exactly as in model_descriptor_fast2.
    transformed_signatures = []
    for signature in desc.edge_signatures:
        values = []
        for new_bits in product((0, 1), repeat=r):
            old_bits = [0] * r
            for j in range(r):
                old_bits[retic_permutation[j]] = new_bits[j] ^ flips[j]
            block = _switch_index(old_bits) * m
            values.extend(signature[block + old_output[new_i]] for new_i in range(m))
        transformed_signatures.append(tuple(values))
    active = tuple(sorted(set(transformed_signatures)))
    signature_class = {signature: i for i, signature in enumerate(active)}
    edge_class_map = tuple(signature_class[sig] for sig in transformed_signatures)

    outputs = []
    for new_i in range(m):
        grouped = defaultdict(lambda: defaultdict(int))
        for monomial, lambda_poly in desc.outputs[old_output[new_i]]:
            new_monomial = tuple(
                sorted((edge_class_map[ci], sector, exponent) for ci, sector, exponent in monomial)
            )
            new_poly = _substitute_lambda_polynomial(
                lambda_poly, r, retic_permutation, flips
            )
            for mask, coefficient in new_poly:
                grouped[new_monomial][mask] += coefficient
        expression = []
        for monomial, polynomial in grouped.items():
            clean = tuple(sorted((mask, c) for mask, c in polynomial.items() if c))
            if clean:
                expression.append((monomial, clean))
        outputs.append(tuple(sorted(expression)))
    return MapDescriptor(desc.k, r, len(active), tuple(outputs), active)


def port_transform_canonical_retic(desc, port_permutation):
    variants = []
    r = desc.retic_count
    actions = (
        [(p, f) for p in permutations(range(r)) for f in product((0, 1), repeat=r)]
        if r
        else [((), ())]
    )
    for p, f in actions:
        variants.append(transform_descriptor(desc, port_permutation, p, f))
    return min(
        variants,
        key=lambda d: (d.retic_count, d.edge_class_count, d.outputs, d.edge_signatures),
    )


def canonical_port_orbit(desc):
    variants = [
        port_transform_canonical_retic(desc, p) for p in permutations(range(desc.k))
    ]
    return min(
        variants,
        key=lambda d: (d.retic_count, d.edge_class_count, d.outputs, d.edge_signatures),
    )
