#!/usr/bin/env python3
"""Reduce the 864 base-ansatz exceptions by the exact S4 port action."""

from __future__ import annotations

import json
import pickle
from collections import defaultdict
from itertools import permutations
from pathlib import Path

import sympy as sp

from descriptor_actions import port_transform_canonical_retic
from k2p_atlas_core import descriptor_jacobian


ROOT = Path(__file__).resolve().parents[2]
ATLAS = ROOT / "package/referee/k2p_offline_sweep_portable/atlas"
WORK = Path(__file__).resolve().parent


def descriptor_key(d):
    return d.retic_count, d.edge_class_count, d.outputs, d.edge_signatures


def main():
    with (ATLAS / "descriptors_4.pkl").open("rb") as handle:
        sources, targets, compatible, source_descriptors, descriptor_map = pickle.load(handle)
    with (ATLAS / "rank_certs_4.pkl").open("rb") as handle:
        lower_certificates = pickle.load(handle)
    census = json.loads((WORK / "base_ansatz_census.json").read_text())
    unique = sorted(set(source_descriptors) | set(descriptor_map.values()), key=descriptor_key)
    index = {d: i for i, d in enumerate(unique)}
    exceptional_indices = {row["descriptor_index"] for row in census["exceptional"]}
    exceptional = {unique[i] for i in exceptional_indices}
    unassigned = set(exceptional)

    bindings = defaultdict(list)
    for (target_index, port_permutation), descriptor in descriptor_map.items():
        if descriptor in unassigned and len(bindings[descriptor]) < 4:
            record = targets[target_index]
            bindings[descriptor].append(
                {
                    "target_index": target_index,
                    "port_permutation": list(port_permutation),
                    "core_id": record.core_id,
                    "incoming_selected": record.incoming_selected,
                    "repair_index": record.repair_index,
                    "selected_sink_mask": record.selected_sink_mask,
                    "words": repr(record.words),
                    "dummy_labels": list(record.dummy_labels),
                }
            )

    orbit_rows = []
    representatives = []
    port_perms = tuple(permutations(range(4)))
    while unassigned:
        seed = min(unassigned, key=descriptor_key)
        full_orbit = {port_transform_canonical_retic(seed, p) for p in port_perms}
        orbit = full_orbit & exceptional
        nonexceptional = [d for d in full_orbit if d in index and index[d] not in exceptional_indices]
        if nonexceptional:
            raise AssertionError(("exception orbit mixes rank families", len(nonexceptional)))
        unassigned -= orbit
        representative = min(orbit, key=descriptor_key)
        representatives.append(representative)
        cert = lower_certificates[representative]
        evars = 2 * representative.edge_class_count
        matrix = sp.Matrix([row[:evars] for row in descriptor_jacobian(representative)])
        edge_kernel = matrix.nullspace()
        supports = [tuple(i for i, value in enumerate(vector) if value) for vector in edge_kernel]
        supports.sort(key=lambda support: (-len(support), support))
        lower = int(cert["rank"])
        base_upper = next(
            row["base_upper_rank"]
            for row in census["exceptional"]
            if row["descriptor_index"] == index[representative]
        )
        missing = base_upper - lower
        orbit_rows.append(
            {
                "orbit_index": len(orbit_rows),
                "representative_descriptor_index": index[representative],
                "compiled_orbit_size": len(orbit),
                "full_port_orbit_size": len(full_orbit),
                "retic_count": representative.retic_count,
                "edge_class_count": representative.edge_class_count,
                "parameter_count": evars + representative.retic_count,
                "lower_rank": lower,
                "base_upper_rank": base_upper,
                "missing_kernel_directions": missing,
                "numeric_edge_kernel_dimension": len(edge_kernel),
                "numeric_edge_kernel_supports_largest_first": [list(s) for s in supports],
                "bindings": bindings.get(representative, []),
            }
        )
        print(
            f"orbit {len(orbit_rows)-1}: compiled={len(orbit)}/full={len(full_orbit)} rank={lower}/{base_upper} "
            f"E={representative.edge_class_count} supports={supports}",
            flush=True,
        )

    if sum(row["compiled_orbit_size"] for row in orbit_rows) != len(exceptional_indices):
        raise AssertionError("orbits do not partition the exception set")
    with (WORK / "exception_orbit_representatives.pkl").open("wb") as handle:
        pickle.dump(tuple(representatives), handle, protocol=5)
    result = {
        "schema": "k2p-exceptional-rank-port-orbits-v1",
        "exceptional_descriptor_count": len(exceptional_indices),
        "orbit_count": len(orbit_rows),
        "compiled_orbit_size_histogram": {
            str(size): sum(row["compiled_orbit_size"] == size for row in orbit_rows)
            for size in sorted({row["compiled_orbit_size"] for row in orbit_rows})
        },
        "orbits": orbit_rows,
    }
    (WORK / "exception_orbits.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: result[k] for k in result if k != "orbits"}, indent=2))


if __name__ == "__main__":
    main()
