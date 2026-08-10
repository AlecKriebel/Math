#!/usr/bin/env python3
"""Mutation-sensitive adversarial tests required by the gate directive."""

from copy import deepcopy
import json
from pathlib import Path

from cleanroom_probe import expected_base_relation_id, expected_relation_id
from verify_probe_extension import VerificationError, verify_payload


HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "certificates" / "fixture.json"
OUT = HERE / "certificates" / "mutation_results.json"


def rehash(record):
    record["relation_id"] = expected_relation_id(record)


def mutations(clean):
    # 1. Alter a physical port correspondence but recompute the shallow id.
    x = deepcopy(clean)
    child = x["p_relations"][0]
    old_id = child["relation_id"]
    child["port_matching"][0] = ["i", "b"]
    rehash(child)
    ids = x["base_relations"][0]["p_child_relation_ids"]
    x["base_relations"][0]["p_child_relation_ids"] = sorted(child["relation_id"] if z == old_id else z for z in ids)
    yield "altered_port_correspondence", x

    # 2. Bind a q child to a different allowed p parent and recompute its id.
    x = deepcopy(clean)
    allowed = [r for r in x["p_relations"] if r["classification"] in ("labelled_isomorphism", "ordinary_T")]
    q = x["q_relations"][0]
    q["parent_relation_id"] = next(r["relation_id"] for r in allowed if r["relation_id"] != q["parent_relation_id"])
    rehash(q)
    yield "wrong_parent", x

    # 3. Make a child transport disagree with the parent's fixed map.
    x = deepcopy(clean)
    q = next(r for r in x["q_relations"] if r["classification"] in ("labelled_isomorphism", "ordinary_T"))
    q["transport"][0][1], q["transport"][1][1] = q["transport"][1][1], q["transport"][0][1]
    yield "inconsistent_T_or_isomorphism_map", x

    # 4. Delete one admissible p arc-pair relation.
    x = deepcopy(clean)
    x["p_relations"].pop()
    yield "dropped_insertion_arc", x

    # 5. Duplicate a decorated relation byte-for-byte.
    x = deepcopy(clean)
    x["p_relations"].append(deepcopy(x["p_relations"][0]))
    yield "duplicate_relation", x

    # 6. Attach a valid invariant/tensor body to the wrong graph relation.
    x = deepcopy(clean)
    separated = [r for r in x["q_relations"] if r["classification"] == "generic_polynomial_separation"]
    a = separated[0]
    b = next(r for r in separated[1:] if r["witness"]["source_quartet_tensor_sha256"] != a["witness"]["source_quartet_tensor_sha256"])
    a["witness"] = deepcopy(b["witness"])
    yield "graph_polynomial_mismatch", x

    # 7. Reproduce the quarantined primary failure: retain the old state id
    # while changing the fixed-full root case.  A mixed-code-only identity
    # would merge this record; the strengthened rooted identity must not.
    x = deepcopy(clean)
    b = deepcopy(x["base_relations"][0])
    b["raw_terminal_id"] = "synthetic-raw-terminal-cross-root-mutation"
    b["fixed_full_root_case_id"] = "different-fixed-full-root-case"
    # Recompute the relation id but deliberately preserve the old weaker
    # state_identity_sha256, as the failed implementation did.
    b["relation_id"] = expected_base_relation_id(b)
    x["base_relations"].append(b)
    yield "cross_root_case_state_merge", x

    # 8. Keep all records but lie about one path's complete child set.
    x = deepcopy(clean)
    x["base_relations"][0]["p_child_relation_ids"] = x["base_relations"][0]["p_child_relation_ids"][:-1]
    yield "borrowed_or_truncated_per_path_child_set", x


def main():
    clean = json.loads(FIXTURE.read_text())
    clean_result = verify_payload(clean)
    results = []
    for name, payload in mutations(clean):
        try:
            verify_payload(payload)
        except VerificationError as exc:
            results.append({"mutation": name, "rejected": True, "reason": str(exc)})
        else:
            results.append({"mutation": name, "rejected": False, "reason": "verifier accepted mutation"})
    if not all(x["rejected"] for x in results):
        raise SystemExit(json.dumps(results, indent=2))
    report = {
        "schema": "stc-jc-probe-extension-mutations-v1",
        "clean_result": clean_result,
        "mutations": results,
        "all_rejected": True,
    }
    OUT.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
