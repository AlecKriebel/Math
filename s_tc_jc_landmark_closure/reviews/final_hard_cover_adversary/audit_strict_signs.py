#!/usr/bin/env python3
"""Independently replay every stored n=3 strict-sign claim.

The historical n=3 streams are not accepted as fixed-root relation
certificates, but their sign claims are useful regression fixtures.  This
program reconstructs each raw rooted graph from provenance, regenerates the
displayed-tree JC pullback selected by the recorded quartet/invariant indices,
and independently factors and Bernstein-certifies it.  The producer's
``certificate['certified']`` flag is never consulted as evidence.
"""

from __future__ import annotations

from collections import Counter
import gzip
import hashlib
from itertools import combinations
import json
from pathlib import Path
import time

from audit_hard_cover import (
    CORE_PATH,
    INVARIANT_PATH,
    PROJECT,
    build_inventory,
    file_sha,
    source_graph_for,
    target_graph_for,
)
from cleanroom_core import (
    canonical_json,
    exact_poly_hash,
    independent_sign_certificate,
    invariant_orbit,
    pullback,
    quartet_descriptor,
)


HERE = Path(__file__).resolve().parent
STREAMS = tuple(
    PROJECT / "primary/certificates" / name
    for name in (
        "hard_cover_n3_sig0_all.jsonl.gz",
        "hard_cover_n3_sig1_all.jsonl.gz",
        "hard_cover_n3_sig2_all.jsonl.gz",
        "hard_cover_n3_sig3_5_all.jsonl.gz",
        "hard_cover_n3_sig6_7_all.jsonl.gz",
    )
)


def main() -> int:
    started = time.monotonic()
    inventory = build_inventory(
        selected_outgoing=3,
        recompute_all_descriptor_bits=False,
    )
    invariants = invariant_orbit(json.loads(INVARIANT_PATH.read_text()))
    core_payload = json.loads(CORE_PATH.read_text())
    failures = []
    counts = Counter()
    unique_polynomials: dict[str, dict] = {}
    first_replay = None

    for path in STREAMS:
        with gzip.open(path, "rt", encoding="utf-8") as handle:
            for line in handle:
                state = json.loads(line)
                if state.get("probe_classification") != "strict_open_cube_separation":
                    continue
                counts["strict_states"] += 1
                witness = state["probe_witness"]
                chunk = int(witness["quartet_chunk"])
                invariant_index = int(witness["invariant_index"])
                for coverage in state["raw_coverage"]:
                    counts["strict_raw_paths"] += 1
                    try:
                        source_variant = inventory.sources[coverage["source_primitive_id"]]
                        target_variant = inventory.targets[coverage["target_primitive_id"]]
                        source = source_graph_for(source_variant, coverage, core_payload)
                        target = target_graph_for(target_variant, coverage)
                        p = int(state["selected_port_count"])
                        quartet = tuple(combinations(range(p), 4))[chunk]
                        labels = tuple(f"L_{index}" for index in range(p))
                        source_poly = pullback(
                            quartet_descriptor(source, labels, quartet),
                            invariants[invariant_index],
                        )
                        target_poly = pullback(
                            quartet_descriptor(target, labels, quartet),
                            invariants[invariant_index],
                        )
                    except Exception as exc:  # fail closed with a bounded record
                        failures.append({
                            "type": "graph_to_polynomial_reconstruction_error",
                            "state_id": state["state_id"],
                            "path_binding_id": coverage.get("path_binding_id"),
                            "error": repr(exc),
                        })
                        continue
                    if source_poly or not target_poly:
                        failures.append({
                            "type": "strict_separator_orientation_failure",
                            "state_id": state["state_id"],
                            "path_binding_id": coverage.get("path_binding_id"),
                        })
                        continue
                    poly_hash = exact_poly_hash(target_poly)
                    if poly_hash != witness.get("target_pullback_exact_sha256"):
                        failures.append({
                            "type": "graph_derived_polynomial_hash_mismatch",
                            "state_id": state["state_id"],
                            "path_binding_id": coverage.get("path_binding_id"),
                            "derived": poly_hash,
                            "recorded": witness.get("target_pullback_exact_sha256"),
                        })
                        continue
                    if poly_hash not in unique_polynomials:
                        unique_polynomials[poly_hash] = independent_sign_certificate(target_poly)
                    independent = unique_polynomials[poly_hash]
                    recorded = witness.get("target_sign_certificate", {})
                    valid = (
                        independent.get("certified") is True
                        and independent.get("strict_sign")
                        == witness.get("target_strict_sign")
                        and independent.get("strict_sign")
                        == recorded.get("strict_sign")
                        and independent.get("polynomial_sha256")
                        == recorded.get("polynomial_sha256")
                        and independent.get("term_count") == recorded.get("term_count")
                        and canonical_json(independent.get("factors", []))
                        == canonical_json(recorded.get("factors", []))
                    )
                    if not valid:
                        failures.append({
                            "type": "independent_factor_bernstein_disagreement",
                            "state_id": state["state_id"],
                            "path_binding_id": coverage.get("path_binding_id"),
                            "polynomial_sha256": poly_hash,
                            "independent": independent,
                            "recorded": recorded,
                        })
                    else:
                        counts["strict_paths_verified"] += 1
                        if first_replay is None:
                            first_replay = (target_poly, independent)

    # Mutation: preserving the Boolean while corrupting one exact factor must
    # be rejected by comparison with a fresh factor/Bernstein replay.
    mutation = {"mutation": "forge_certified_flag_and_factor_hash", "rejected": False}
    if first_replay is not None:
        target_poly, independent = first_replay
        forged = json.loads(json.dumps(independent))
        forged["certified"] = True
        if forged.get("factors"):
            forged["factors"][0]["expanded_sha256"] = "0" * 64
        else:
            forged["strict_sign"] = -int(forged["strict_sign"])
        fresh = independent_sign_certificate(target_poly)
        mutation["rejected"] = canonical_json(forged) != canonical_json(fresh)
    if not mutation["rejected"]:
        failures.append({"type": "forged_strict_sign_mutation_not_rejected"})

    payload = {
        "schema": "historical-n3-strict-sign-clean-room-v1",
        "status": "FALSE" if failures else "VERIFIED",
        "scope": (
            "strict-sign pullbacks in the five historical n=3 streams only; "
            "this does not validate their withdrawn schema-2 state identity"
        ),
        "independence": (
            "every raw graph and pullback regenerated from primitive provenance; "
            "every unique polynomial independently factored and Bernstein checked"
        ),
        "inputs": {
            str(path.relative_to(PROJECT)): file_sha(path)
            for path in (*STREAMS, CORE_PATH, INVARIANT_PATH)
        },
        "counts": {
            **dict(sorted(counts.items())),
            "unique_strict_polynomials": len(unique_polynomials),
        },
        "mutation": mutation,
        "failure_count": len(failures),
        "failures": failures[:100],
        "elapsed_seconds": time.monotonic() - started,
    }
    output = HERE / "historical_n3_strict_sign_audit.json"
    output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": payload["status"],
        "counts": payload["counts"],
        "failure_count": payload["failure_count"],
        "output": str(output),
        "sha256": file_sha(output),
        "elapsed_seconds": payload["elapsed_seconds"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
