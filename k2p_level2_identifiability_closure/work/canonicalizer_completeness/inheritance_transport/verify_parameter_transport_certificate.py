#!/usr/bin/env python3
"""Fail-closed replay of the graph-derived K2P parameter transports."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
BUILDER = HERE / "build_parameter_transport_certificate.py"
CERTIFICATE = HERE / "parameter_transport_certificate.json"
STRICT_JSON_DIR = PROJECT / "work/final_theorem_release"
if str(STRICT_JSON_DIR) not in sys.path:
    sys.path.insert(0, str(STRICT_JSON_DIR))

from strict_json import (  # noqa: E402
    StrictJSONError,
    decode_json_document,
    iter_canonical_gzip_jsonl,
)

LEDGER_KEYS = {
    "probe_relations": "probe_relation_parameter_transports.jsonl.gz",
    "probe_restrictions": "probe_restriction_parameter_transports.jsonl.gz",
    "restoration_restrictions": "restoration_restriction_parameter_transports.jsonl.gz",
}


class Failure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Failure(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def action_keys(row: dict[str, Any]) -> list[str]:
    keys = [f"occurrence:{row['occurrence_kind']}"]
    for action in row["inheritance_actions"]:
        if action["mode"] == "ordinary_triangle_local_section":
            keys.append("inheritance:triangle_local_section")
        elif action["parent_order_reversed"]:
            keys.append("inheritance:complement")
        else:
            keys.append("inheritance:identity")
        if action.get("root_suppressed_incoming_incidence"):
            keys.append("inheritance:root_suppressed_incoming")
    return keys


def validate_relation(row: dict[str, Any], context: str) -> None:
    require(row["schema"] == "k2p_graph_derived_relation_parameter_transport_v1", f"{context}:schema")
    require(row["relation"] in {"isomorphic", "triangle"}, f"{context}:relation")
    require(row["triangle_local_parameters_are_not_affine_parent_flips"] is True, f"{context}:triangle guard")
    source_edges, target_edges = set(), set()
    for action in row["edge_actions"]:
        require(action["mode"] in {"paired_K2P_product", "ordinary_triangle_local_section"}, f"{context}:edge mode")
        source = tuple(action["source_physical_edge"])
        target = tuple(action["target_physical_edge"])
        require(source not in source_edges and target not in target_edges, f"{context}:edge bijection")
        source_edges.add(source)
        target_edges.add(target)
        require(bool(action["source_rooted_factors"]) and bool(action["target_rooted_factors"]), f"{context}:edge factors")
        if action["mode"] == "paired_K2P_product":
            require(action["s_action"] == action["g_action"] == "match_products", f"{context}:paired sectors")
        else:
            require(row["relation"] == "triangle", f"{context}:triangle edge outside relation")
            require(action["s_action"] == action["g_action"] == "local_section", f"{context}:triangle section")
    triangle_actions = 0
    affine_targets = set()
    for action in row["inheritance_actions"]:
        if action["mode"] == "ordinary_triangle_local_section":
            triangle_actions += 1
            require(row["relation"] == "triangle", f"{context}:triangle inheritance outside relation")
            require(action["section_certificate"] == "rank_nine_ordinary_triangle_common_germ", f"{context}:triangle certificate")
            continue
        require(action["mode"] == "affine_parent_transport", f"{context}:inheritance mode")
        permutation = tuple(action["source_parent_index_to_target_parent_index"])
        require(permutation in {(0, 1), (1, 0)}, f"{context}:parent permutation")
        flip = permutation == (1, 0)
        require(action["parent_order_reversed"] is flip, f"{context}:flip flag")
        require(
            action["target_lambda_from_source"] == ("one_minus_lambda" if flip else "lambda"),
            f"{context}:affine lambda action",
        )
        require(action["source_lambda_parent_index"] == action["target_lambda_parent_index"] == 1, f"{context}:lambda convention")
        require(len(action["source_ordered_parents"]) == len(action["target_ordered_parents"]) == 2, f"{context}:parent width")
        target = action["target_reticulation"]
        require(target not in affine_targets, f"{context}:target reticulation bijection")
        affine_targets.add(target)
    require(triangle_actions == (1 if row["relation"] == "triangle" else 0), f"{context}:triangle-local census")


def validate_restriction(row: dict[str, Any], context: str) -> None:
    require(row["schema"] == "k2p_graph_derived_restriction_parameter_transport_v1", f"{context}:schema")
    parent_edges = set()
    used_child_factors = set()
    for action in row["edge_actions"]:
        require(action["mode"] == "paired_serial_product", f"{context}:edge mode")
        parent_edge = tuple(action["parent_physical_edge"])
        require(parent_edge not in parent_edges, f"{context}:parent edge duplicate")
        parent_edges.add(parent_edge)
        require(bool(action["parent_rooted_factors"]) and bool(action["child_rooted_factors"]), f"{context}:empty serial product")
        require(action["parent_s_from_child"] == action["parent_g_from_child"] == "product", f"{context}:paired products")
        factors = {tuple(item) for item in action["child_rooted_factors"]}
        require(not (factors & used_child_factors), f"{context}:child factor reused")
        used_child_factors.update(factors)
        require(action["root_suppressed_parent_edge"] is (len(action["parent_rooted_factors"]) == 2), f"{context}:root edge flag")
    forgotten = {tuple(item) for item in row["forgotten_child_rooted_arcs"]}
    require(not (forgotten & used_child_factors), f"{context}:forgotten/used overlap")
    require(row["forgotten_reticulations"] == [], f"{context}:unexpected invisible/forgotten reticulation")
    targets = set()
    for action in row["inheritance_actions"]:
        require(action["mode"] == "affine_parent_transport", f"{context}:inheritance mode")
        permutation = tuple(action["child_parent_index_to_parent_parent_index"])
        require(permutation in {(0, 1), (1, 0)}, f"{context}:parent permutation")
        flip = permutation == (1, 0)
        require(action["parent_order_reversed"] is flip, f"{context}:flip flag")
        require(
            action["parent_lambda_from_child"] == ("one_minus_lambda" if flip else "lambda"),
            f"{context}:affine lambda action",
        )
        require(action["child_lambda_parent_index"] == action["parent_lambda_parent_index"] == 1, f"{context}:lambda convention")
        target = action["parent_reticulation"]
        require(target not in targets, f"{context}:reticulation duplicate")
        targets.add(target)


def validate_ledger(path: Path, expected: dict[str, Any], key: str) -> None:
    require(path.name == expected["path"], f"{key}:path")
    require(path.stat().st_size == expected["bytes"], f"{key}:bytes")
    require(sha_file(path) == expected["sha256"], f"{key}:file hash")
    rows = 0
    root = sha([])
    counts = Counter()
    occurrence_ids = set()
    try:
        strict_rows = iter_canonical_gzip_jsonl(path, label=str(path))
        for number, wrapped in enumerate(strict_rows):
            context = f"{key}:{number}"
            require(set(wrapped) == {"row", "row_sha256"}, f"{context}:wrapper schema")
            row = wrapped["row"]
            require(wrapped["row_sha256"] == sha(row), f"{context}:row hash")
            occurrence = row["occurrence_id"]
            require(occurrence not in occurrence_ids, f"{context}:duplicate occurrence")
            occurrence_ids.add(occurrence)
            if key == "probe_relations":
                validate_relation(row, context)
            else:
                validate_restriction(row, context)
            counts.update(action_keys(row))
            root = sha({"previous": root, "row_sha256": wrapped["row_sha256"]})
            rows += 1
    except (OSError, StrictJSONError) as error:
        raise Failure(f"{key}:strict JSON decode:{error}") from error
    require(rows == expected["rows"], f"{key}:row count")
    require(root == expected["ordered_hash_root"], f"{key}:ordered root")
    require(dict(sorted(counts.items())) == expected["counts"], f"{key}:counts")


def validate_directory(root: Path) -> dict[str, Any]:
    certificate_path = root / "parameter_transport_certificate.json"
    certificate = decode_json_document(
        certificate_path.read_bytes(),
        label=certificate_path.name,
        require_object=True,
    )
    require(certificate["schema"] == "k2p_graph_derived_parameter_transport_certificate_v1", "certificate schema")
    require(certificate["status"] == "PASS", "certificate status")
    payload = dict(certificate)
    claimed = payload.pop("payload_sha256")
    require(claimed == sha(payload), "certificate payload hash")
    for relative, record in certificate["inputs"].items():
        path = PROJECT / relative
        require(path.is_file(), f"missing bound input:{relative}")
        require(path.stat().st_size == record["bytes"], f"input bytes:{relative}")
        require(sha_file(path) == record["sha256"], f"input hash:{relative}")
    for key, filename in LEDGER_KEYS.items():
        validate_ledger(root / filename, certificate["ledgers"][key], key)
    closure = certificate["closure"]
    require(closure["all_exact_transport_records_used"] == 67_741, "exact transport closure")
    require(closure["all_frozen_parent_restriction_records_used"] == 4_379, "restriction record closure")
    require(closure["restoration_canonical_parents"] == 997, "restoration parent closure")
    require(closure["restoration_member_roots"] == 2_540, "restoration root closure")
    require(closure["restoration_first_source_classes"] == 42, "restoration source class closure")
    require(closure["restoration_first_target_classes"] == 4_986, "restoration target class closure")
    require(closure["restoration_second_edges"] == 256, "restoration second closure")
    require(closure["unresolved_parameter_transports"] == 0, "unresolved parameter transport")
    return certificate


def rederive_and_compare(root: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="k2p-parameter-transport-replay-") as temporary:
        regenerated = Path(temporary)
        environment = dict(os.environ)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        completed = subprocess.run(
            [sys.executable, "-B", str(BUILDER), "--output-dir", str(regenerated)],
            cwd=PROJECT,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        require(completed.returncode == 0, "producer replay failed:\n" + completed.stdout[-4000:])
        require("PARAMETER_TRANSPORT_BUILD_PASS" in completed.stdout, "producer PASS token")
        validate_directory(regenerated)
        for filename in ["parameter_transport_certificate.json", *LEDGER_KEYS.values()]:
            require((root / filename).read_bytes() == (regenerated / filename).read_bytes(), f"rederived bytes:{filename}")


def main() -> None:
    require(__debug__, "optimized Python is forbidden")
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate-dir", type=Path, default=HERE)
    parser.add_argument("--structural-only", action="store_true")
    args = parser.parse_args()
    root = args.certificate_dir.resolve()
    certificate = validate_directory(root)
    if not args.structural_only:
        rederive_and_compare(root)
    print(
        "PARAMETER_TRANSPORT_REPLAY_PASS "
        + json.dumps({
            "payload_sha256": certificate["payload_sha256"],
            "rederived": not args.structural_only,
            "unresolved": certificate["closure"]["unresolved_parameter_transports"],
        }, sort_keys=True)
    )


if __name__ == "__main__":
    try:
        main()
    except Failure as error:
        print(f"PARAMETER_TRANSPORT_REPLAY_FAIL:{error}", file=sys.stderr)
        raise SystemExit(1)
