#!/usr/bin/env python3
"""Byte-level audit of fixed-IN assumptions in the two producer branches."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError((label, needle))


def main() -> None:
    primary = (PROJECT / "primary" / "atlas_compiler.py").read_bytes()
    completion = (PROJECT / "primary" / "completion_universe.py").read_bytes()
    independent_rel = (PROJECT / "independent" / "decorated_atlas" / "relations.py").read_bytes()
    independent_primitive = (PROJECT / "independent" / "decorated_atlas" / "primitive.py").read_bytes()
    frozen = (HERE / "cleanroom_engine.py").read_bytes()
    head_primary = subprocess.check_output([
        "git", "show", "HEAD:s_tc_jc_landmark_closure/primary/atlas_compiler.py"
    ], cwd=PROJECT.parent)

    p = primary.decode()
    c = completion.decode()
    ir = independent_rel.decode()
    ip = independent_primitive.decode()
    h = head_primary.decode()
    f = frozen.decode()
    require(h, "permutations(range(n))", "committed primary fixed-IN action")
    require(p, "permutations(range(n + 1))", "working primary full boundary action")
    require(c, "def marginal_incoming_completions", "working primary omitted incoming mode")
    require(ir, "if port_map[0] != 0:", "independent fixed-IN relation guard")
    require(ip, "permutations(range(1, port_count))", "independent fixed-IN labelling")
    require(f, "permutations(range(p))", "frozen clean-room full boundary action")
    require(f, '"incoming_dummy"', "frozen clean-room omitted incoming mode")

    result = {
        "schema": "incoming-boundary-code-assumption-audit-v1",
        "status": "EXACTLY_COMPUTED",
        "committed_primary": {
            "sha256": digest(head_primary),
            "fixed_IN": True,
            "verdict": "FALSE_UNIVERSE_QUOTIENT",
        },
        "working_tree_primary": {
            "atlas_sha256": digest(primary),
            "completion_sha256": digest(completion),
            "full_boundary_action_present": True,
            "marginalized_incoming_completion_present": True,
            "verdict": "CORRECTED_DISCOVERY_CODE_NOT_USED_AS_INDEPENDENT_EVIDENCE",
        },
        "independent_decorated_atlas": {
            "relations_sha256": digest(independent_rel),
            "primitive_sha256": digest(independent_primitive),
            "requires_port_map_0_to_0": True,
            "permutes_only_labels_1_through_p_minus_1": True,
            "verdict": "FALSE_UNIVERSE_QUOTIENT",
        },
        "frozen_cleanroom_replay": {
            "sha256": digest(frozen),
            "full_boundary_action_present": True,
            "marginalized_incoming_mode_present": True,
        },
    }
    result["body_sha256"] = digest(json.dumps(result, sort_keys=True, separators=(",", ":")).encode())
    output = HERE / "certificates" / "code_assumption_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
