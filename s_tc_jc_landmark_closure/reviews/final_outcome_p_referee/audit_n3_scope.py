#!/usr/bin/env python3
"""Bounded scope audit for the claimed independent n3 relation gate.

This script deliberately does not import project code.  It checks only what
the active clean-room verifier actually consumes and what the arbitrary-word
probe stream actually anchors.  It is not a topology generator.
"""

from __future__ import annotations

import ast
import gzip
import json
from pathlib import Path
import subprocess


PROJECT = Path(__file__).resolve().parents[2]


def jsonl(path: Path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            if line.strip():
                yield json.loads(line)


def main() -> None:
    verifier_path = PROJECT / "reviews/bounded_directed_relation_cleanroom/cleanroom_verify.py"
    source = verifier_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    loaded_relation_stream = False
    generated_target_grammar_calls = []
    grammar_names = {
        "completions",
        "marginal_incoming_completions",
        "target_bases",
        "weak_compositions",
        "compile_relation_records",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            text = ast.get_source_segment(source, node) or ""
            if "relations = list(iter_jsonl(relation_path))" in text:
                loaded_relation_stream = True
        if isinstance(node, ast.Call):
            name = None
            if isinstance(node.func, ast.Name):
                name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                name = node.func.attr
            if name in grammar_names:
                generated_target_grammar_calls.append(name)

    bounded_summary = json.loads(
        (PROJECT / "primary/certificates/bounded_relation_n3_all_filtered_summary.json").read_text()
    )
    relation_path = PROJECT / bounded_summary["runs"][0]["bounded_relation_certificate"]["relation_path"]
    relation_counts = {}
    direct_ids = []
    for record in jsonl(relation_path):
        kind = record["classification"]
        relation_counts[kind] = relation_counts.get(kind, 0) + 1
        if kind == "isomorphism_or_T":
            direct_ids.append(record["relation_id"])

    promotion = json.loads(
        (
            PROJECT
            / "reviews/arbitrary_subdivision_promotion_referee/certificates/promotion_audit_certificate.json"
        ).read_text()
    )
    n3_promotion = next(row for row in promotion["families"] if row["family"] == "n3")
    probe_summary_path = PROJECT / "primary/certificates/probe_extension_schema3_n3_final_summary.json"
    bindings_path = PROJECT / "primary/certificates/probe_extension_bindings_schema3_n3_final.jsonl.gz"

    git_root = Path(
        subprocess.check_output(
            ["git", "-C", str(PROJECT), "rev-parse", "--show-toplevel"], text=True
        ).strip()
    )

    def tracked(path: Path) -> bool:
        relative = path.relative_to(git_root)
        completed = subprocess.run(
            ["git", "-C", str(git_root), "ls-files", "--error-unmatch", str(relative)],
            text=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return completed.returncode == 0

    promotion_text = json.dumps(promotion, sort_keys=True)
    direct_crosswalk_declared = any(
        token in promotion_text
        for token in ("direct_residual_relation", "direct_relation_id", "direct_anchor_crosswalk")
    )

    result = {
        "status": "PRESERVED_SCOPE_FAILURE",
        "cleanroom_relation_universe": {
            "loads_primary_relation_stream": loaded_relation_stream,
            "target_completion_generation_calls_found": sorted(set(generated_target_grammar_calls)),
            "canonical_relation_count_loaded": sum(relation_counts.values()),
            "classification_counts": dict(sorted(relation_counts.items())),
            "direct_residual_relation_count": len(direct_ids),
            "conclusion": (
                "The clean-room implementation independently validates loaded relation records, "
                "but does not independently generate the target-completion/presentation universe."
            ),
        },
        "arbitrary_word_probe_scope": {
            "base_terminal_paths": n3_promotion["path_inventory_count"],
            "base_terminal_states": n3_promotion["path_inventory_count"],
            "base_inventory": "frozen path-bound hard-cover terminal inventory",
            "direct_anchor_crosswalk_declared_in_tracked_promotion_certificate": direct_crosswalk_declared,
            "probe_summary_tracked_at_head": tracked(probe_summary_path),
            "probe_bindings_tracked_at_head": tracked(bindings_path),
            "conclusion": (
                "The n3 probe stream is rooted only at the 144 hard-cover terminal paths.  "
                "It contains no explicit binding or crosswalk for the 62 direct residual relations."
            ),
        },
        "required_closure": [
            "Independently generate the complete n3 target-completion grammar and all relative port presentations, then compare the normalized directed-relation multiset.",
            "Prove and certify that every direct residual anchor with one/two extra ports is covered by the existing 144 terminal families, or add its missing graph-to-algebra probe families.",
        ],
    }
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
