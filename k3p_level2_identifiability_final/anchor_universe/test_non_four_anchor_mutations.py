#!/usr/bin/env python3
"""Coherent, resealed attacks on the non-four anchor-universe artifact."""

from __future__ import annotations

import argparse
import collections
import copy
import gzip
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
DEFAULT_ARTIFACT = HERE / "artifacts/NON_FOUR_ANCHOR_UNIVERSE.json"
DEFAULT_OUTPUT = HERE / "NON_FOUR_ANCHOR_MUTATION_REPORT.json"
VERIFIER = HERE / "verify_non_four_anchor_universe.py"
CROSSWALK = HERE / "verify_complete_anchor_crosswalk.py"
FOUR_SUMMARY = (
    HERE.parent
    / "four_port_atlas/full_universe_replay/artifacts/FULL_FOUR_PORT_REPLAY.json"
)
FOUR_VERIFICATION = (
    HERE.parent
    / "four_port_atlas/full_universe_replay/INDEPENDENT_FULL_FOUR_PORT_VERIFICATION.json"
)
FOUR_RAW_LEDGER = (
    HERE.parent
    / "four_port_atlas/full_universe_replay/artifacts/full_directional_ledger.jsonl.gz"
)
ONE_PORT_MANIFEST = HERE.parent / "probes/ONE_PORT_PROBE_MANIFEST.json"
ONE_PORT_LEDGER = HERE.parent / "probes/one_port_ledger.jsonl.gz"
TWO_PORT_MANIFEST = HERE.parent / "probes/TWO_PORT_PROBE_MANIFEST.json"
TWO_PORT_PARENT_INVENTORY = (
    HERE.parent / "probes/two_port_parent_inventory.jsonl.gz"
)
TWO_PORT_LEDGER = HERE.parent / "probes/two_port_ledger.jsonl.gz"


class MutationFailure(RuntimeError):
    pass


def require(condition: bool, code: str) -> None:
    if not condition:
        raise MutationFailure(code)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def reseal(value: dict[str, Any]) -> None:
    for row in value["anchors"]:
        body = {
            key: row[key]
            for key in (
                "origin",
                "port_count",
                "relation",
                "source_graph_sha256",
                "target_graph_sha256",
                "structural_locator",
            )
        }
        row["anchor_key"] = digest(body)
    by_origin = collections.Counter(row["origin"] for row in value["anchors"])
    by_relation = collections.Counter(row["relation"] for row in value["anchors"])
    by_port = collections.Counter(row["port_count"] for row in value["anchors"])
    value["census"] = {
        "total": len(value["anchors"]),
        "by_origin": dict(sorted(by_origin.items())),
        "by_relation": dict(sorted(by_relation.items())),
        "by_port_count": {str(key): count for key, count in sorted(by_port.items())},
    }
    value["ordered_anchor_key_sha256"] = digest(
        sorted(row["anchor_key"] for row in value["anchors"])
    )
    value["payload_sha256"] = digest(
        {
            key: item
            for key, item in value.items()
            if key not in {"payload_sha256", "operational"}
        }
    )


def remove_origin(origin: str) -> Callable[[dict[str, Any]], None]:
    def mutate(value: dict[str, Any]) -> None:
        index = next(
            number
            for number, row in enumerate(value["anchors"])
            if row["origin"] == origin
        )
        del value["anchors"][index]

    return mutate


def mutate_cycle_triangle_relation(value: dict[str, Any]) -> None:
    row = next(
        row
        for row in value["anchors"]
        if row["origin"] == "cycle_physical_k3" and row["relation"] == "triangle"
    )
    row["relation"] = "isomorphic"


def mutate_theta_graph_hash(value: dict[str, Any]) -> None:
    row = next(row for row in value["anchors"] if row["origin"] == "theta2_physical_k6")
    row["source_graph_sha256"] = "0" * 64


def mutate_fold_k7_path(value: dict[str, Any]) -> None:
    rows = [row for row in value["anchors"] if row["origin"] == "theta2_physical_k7"]
    first = rows[0]["structural_locator"]
    second = rows[1]["structural_locator"]
    for key in (
        "first_restored_role",
        "first_source_insertion_index",
        "first_source_insertion",
    ):
        first[key] = copy.deepcopy(second[key])


def mutate_restored_role(value: dict[str, Any]) -> None:
    row = next(row for row in value["anchors"] if row["origin"] == "theta2_physical_k6")
    row["structural_locator"]["restored_role"] = "D_REPAIR_FORGED"


def mutate_add_bogus_anchor(value: dict[str, Any]) -> None:
    row = copy.deepcopy(value["anchors"][0])
    row["structural_locator"] = {"bogus": True}
    value["anchors"].append(row)


def mutate_incoming_boundary_partition(value: dict[str, Any]) -> None:
    theta = value["primitive_counts"]["theta2"]
    theta["base_counts"]["incoming_boundary_mismatch"] -= 1
    theta["base_counts"]["none"] += 1
    theta["per_source_counts"]["0"]["incoming_boundary_mismatch"] -= 1
    theta["per_source_counts"]["0"]["none"] += 1


def mutate_stage_cardinality(value: dict[str, Any]) -> None:
    value["stage_counts"]["theta2_base_presentations"] -= 1
    theta = value["primitive_counts"]["theta2"]
    theta["base_raw"] -= 1
    theta["base_enumeration"]["rows"] -= 1
    theta["base_counts"]["displayed_quartet_mismatch"] -= 1


MUTATIONS: tuple[tuple[str, Callable[[dict[str, Any]], None]], ...] = (
    ("omit_tree_seed", remove_origin("tree_physical_k3")),
    ("omit_cycle_restored_seed", remove_origin("cycle_restored_physical_k4")),
    ("omit_theta2_k5_seed", remove_origin("theta2_physical_k5")),
    ("omit_theta2_k6_seed", remove_origin("theta2_physical_k6")),
    ("cycle_triangle_relabelled_isomorphic", mutate_cycle_triangle_relation),
    ("theta2_source_graph_hash_replaced", mutate_theta_graph_hash),
    ("theta2_k7_restoration_path_folded", mutate_fold_k7_path),
    ("theta2_restored_role_forged", mutate_restored_role),
    ("bogus_anchor_appended", mutate_add_bogus_anchor),
    ("incoming_boundary_partition_reclassified", mutate_incoming_boundary_partition),
    ("theta2_base_stage_omitted", mutate_stage_cardinality),
)


def run_verifier(artifact: Path, report: Path, *, optimized: bool = False):
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(
        [
            "-B",
            str(VERIFIER),
            "--artifact",
            str(artifact),
            "--report",
            str(report),
        ]
    )
    result = subprocess.run(
        command,
        cwd=HERE.parent,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        text=True,
        timeout=300,
    )
    return command, result


def run_crosswalk(raw_ledger: Path, report: Path):
    command = [
        sys.executable,
        "-B",
        str(CROSSWALK),
        "--four-raw-ledger",
        str(raw_ledger),
        "--output",
        str(report),
    ]
    result = subprocess.run(
        command,
        cwd=HERE.parent,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        text=True,
        timeout=300,
    )
    return command, result


def run_crosswalk_with_rebound_bindings(
    raw_ledger: Path,
    report: Path,
    *,
    four_summary: Path = FOUR_SUMMARY,
    four_verification: Path = FOUR_VERIFICATION,
    one_port_manifest: Path = ONE_PORT_MANIFEST,
    one_port_ledger: Path = ONE_PORT_LEDGER,
    two_port_manifest: Path = TWO_PORT_MANIFEST,
    two_port_ledger: Path = TWO_PORT_LEDGER,
):
    """Run the real crosswalk after rebinding deliberately mutated inputs.

    The small runner mode below changes only the verifier's input constants.
    It does not bypass or replace any semantic check in the verifier.
    """
    command = [
        sys.executable,
        "-B",
        str(Path(__file__).resolve()),
        "--crosswalk-binding-runner",
        "--four-summary",
        str(four_summary),
        "--four-verification",
        str(four_verification),
        "--one-port-manifest",
        str(one_port_manifest),
        "--two-port-manifest",
        str(two_port_manifest),
        "--four-raw-ledger",
        str(raw_ledger),
        "--one-port-ledger",
        str(one_port_ledger),
        "--two-port-ledger",
        str(two_port_ledger),
        "--output",
        str(report),
    ]
    result = subprocess.run(
        command,
        cwd=HERE.parent,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        text=True,
        timeout=300,
    )
    return command, result


def omitted_four_port_raw_ledger(source: Path, target: Path) -> None:
    """Delete one equality row while preserving a valid gzip/JSONL stream."""
    omitted = 0
    with gzip.open(source, "rt") as reader, gzip.open(target, "wt") as writer:
        for line in reader:
            row = json.loads(line)
            if row.get("raw_id") == 137124:
                omitted += 1
                continue
            writer.write(line)
    require(omitted == 1, "FOUR_PORT_OMISSION_TARGET_COUNT")


def transform_gzip_jsonl(
    source: Path,
    target: Path,
    transform: Callable[[dict[str, Any]], dict[str, Any] | None],
) -> dict[str, Any]:
    """Rewrite a ledger deterministically and return its exact public census."""
    matched = 0
    status_counts: collections.Counter[str] = collections.Counter()
    ordered_root = digest([])
    rows = 0
    with gzip.open(source, "rt") as reader, target.open("wb") as raw_output:
        compressed = gzip.GzipFile(
            filename="", mode="wb", fileobj=raw_output, mtime=0
        )
        writer = io.TextIOWrapper(compressed, encoding="utf-8", newline="\n")
        try:
            for line in reader:
                original = json.loads(line)
                row = transform(copy.deepcopy(original))
                if row != original:
                    matched += 1
                if row is None:
                    continue
                writer.write(
                    json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n"
                )
                rows += 1
                if "status" in row:
                    status_counts[row["status"]] += 1
                ordered_root = digest(
                    {"previous": ordered_root, "row_sha256": digest(row)}
                )
        finally:
            writer.close()
    return {
        "matched": matched,
        "rows": rows,
        "status_counts": dict(sorted(status_counts.items())),
        "ordered_hash_root": ordered_root,
    }


def gzip_metadata(path: Path) -> dict[str, Any]:
    uncompressed = hashlib.sha256()
    uncompressed_bytes = 0
    with gzip.open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            uncompressed.update(block)
            uncompressed_bytes += len(block)
    return {
        "sha256": sha_file(path),
        "uncompressed_bytes": uncompressed_bytes,
        "uncompressed_sha256": uncompressed.hexdigest(),
    }


def write_resealed_json(
    path: Path,
    value: dict[str, Any],
    field: str,
    *,
    excluded: tuple[str, ...] = (),
) -> None:
    logical = copy.deepcopy(value)
    logical.pop(field, None)
    for key in excluded:
        logical.pop(key, None)
    value[field] = digest(logical)
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n")


def rebound_four_port_bindings(
    raw_ledger: Path, summary_path: Path, verification_path: Path
) -> None:
    """Rebind both four-port metadata layers to a mutated raw ledger."""
    metadata = gzip_metadata(raw_ledger)
    summary = json.loads(FOUR_SUMMARY.read_text())
    summary["artifacts"]["full_directional_ledger.jsonl.gz"] = metadata
    write_resealed_json(summary_path, summary, "payload_sha256_without_hash")

    verification = json.loads(FOUR_VERIFICATION.read_text())
    verification["bindings"]["artifacts"][
        "full_directional_ledger.jsonl.gz"
    ] = metadata
    verification["bindings"]["summary_sha256"] = sha_file(summary_path)
    verification["verified_summary_payload_sha256"] = summary[
        "payload_sha256_without_hash"
    ]
    write_resealed_json(
        verification_path,
        verification,
        "payload_sha256",
        excluded=("operational",),
    )


def rebound_probe_manifest(
    source_manifest: Path,
    target_manifest: Path,
    ledger: Path,
    census: dict[str, Any],
) -> None:
    """Recompute the manifest fields affected by a ledger-status mutation."""
    manifest = json.loads(source_manifest.read_text())
    manifest["ledger_sha256"] = sha_file(ledger)
    manifest["raw_pairs"] = census["rows"]
    manifest["counts"] = census["status_counts"]
    manifest["equality_survivors"] = sum(
        census["status_counts"].get(status, 0)
        for status in ("isomorphic", "triangle")
    )
    manifest["ordered_ledger"]["rows"] = census["rows"]
    manifest["ordered_ledger"]["ordered_hash_root"] = census[
        "ordered_hash_root"
    ]
    write_resealed_json(target_manifest, manifest, "payload_sha256")


def mutate_used_one_port_equality(row: dict[str, Any]) -> dict[str, Any]:
    if (
        row.get("parent_anchor_id") == "four:raw154873"
        and row.get("source_site_index") == 0
        and row.get("target_site_index") == 0
        and row.get("status") == "triangle"
    ):
        row["status"] = "isomorphic"
    return row


def mutate_used_two_port_separator(row: dict[str, Any]) -> dict[str, Any]:
    if (
        row.get("one_port_parent_id") == "P1:four:raw154873:0:0"
        and row.get("second_source_site_index") == 0
        and row.get("second_target_site_index") == 6
        and row.get("status") == "displayed_quartet_mismatch"
    ):
        row["status"] = "isomorphic"
    return row


def mutate_extra_terminal_raw_id(row: dict[str, Any]) -> dict[str, Any]:
    if row.get("raw_id") == 202225:
        row["raw_id"] = 999_999_999
    return row


def command_record(*, optimized: bool, artifact: str) -> list[str]:
    """Location-independent replay description stored in the certificate."""
    command = ["{python}"]
    if optimized:
        command.append("-O")
    command.extend([
        "-B",
        "anchor_universe/verify_non_four_anchor_universe.py",
        "--artifact",
        artifact,
        "--report",
        "{temporary_report}",
    ])
    return command


def crosswalk_command_record(raw_ledger: str) -> list[str]:
    return [
        "{python}",
        "-B",
        "anchor_universe/verify_complete_anchor_crosswalk.py",
        "--four-raw-ledger",
        raw_ledger,
        "--output",
        "{temporary_crosswalk_report}",
    ]


def rebound_crosswalk_command_record(
    *, raw_ledger: str, one_port_ledger: str, two_port_ledger: str
) -> list[str]:
    return [
        "{python}",
        "-B",
        "anchor_universe/test_non_four_anchor_mutations.py",
        "--crosswalk-binding-runner",
        "--four-summary",
        "{coherently_rebound_four_summary}",
        "--four-verification",
        "{coherently_rebound_four_verification}",
        "--one-port-manifest",
        "{coherently_rebound_one_port_manifest}",
        "--two-port-manifest",
        "{coherently_rebound_two_port_manifest}",
        "--four-raw-ledger",
        raw_ledger,
        "--one-port-ledger",
        one_port_ledger,
        "--two-port-ledger",
        two_port_ledger,
        "--output",
        "{temporary_crosswalk_report}",
    ]


def crosswalk_binding_main(argv: list[str]) -> int:
    """Private subprocess entry point for coherently rebound attacks."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--four-summary", type=Path, required=True)
    parser.add_argument("--four-verification", type=Path, required=True)
    parser.add_argument("--one-port-manifest", type=Path, required=True)
    parser.add_argument("--two-port-manifest", type=Path, required=True)
    parser.add_argument("--four-raw-ledger", type=Path, required=True)
    parser.add_argument("--one-port-ledger", type=Path, required=True)
    parser.add_argument("--two-port-ledger", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    spec = importlib.util.spec_from_file_location(
        "k3p_mutation_crosswalk", CROSSWALK
    )
    require(spec is not None and spec.loader is not None, "CROSSWALK_IMPORT_SPEC")
    module = importlib.util.module_from_spec(spec)
    sys.modules["k3p_mutation_crosswalk"] = module
    spec.loader.exec_module(module)
    module.FOUR_SUMMARY = args.four_summary.resolve()
    module.FOUR_VERIFICATION = args.four_verification.resolve()
    module.ONE_PORT_MANIFEST = args.one_port_manifest.resolve()
    module.TWO_PORT_MANIFEST = args.two_port_manifest.resolve()
    return module.main(
        [
            "--four-raw-ledger",
            str(args.four_raw_ledger),
            "--one-port-ledger",
            str(args.one_port_ledger),
            "--two-port-ledger",
            str(args.two_port_ledger),
            "--output",
            str(args.output),
        ]
    )


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    with temporary.open("w") as handle:
        handle.write(json.dumps(value, sort_keys=True, indent=2) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def main(argv: list[str] | None = None) -> int:
    if not __debug__:
        raise MutationFailure("OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path, default=DEFAULT_ARTIFACT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    started = time.monotonic()
    artifact_path = args.artifact.resolve()
    pristine = json.loads(artifact_path.read_text())
    cases = []
    with tempfile.TemporaryDirectory(prefix="k3p_non_four_mutations_") as raw:
        temporary = Path(raw)
        clean_command, clean = run_verifier(
            artifact_path, temporary / "clean_report.json"
        )
        require(clean.returncode == 0, "CLEAN_CONTROL_FAILED")
        require(
            "K3P_INDEPENDENT_NON_FOUR_ANCHOR_UNIVERSE_PASS" in clean.stdout,
            "CLEAN_CONTROL_SENTINEL",
        )
        clean_crosswalk_command, clean_crosswalk = run_crosswalk(
            FOUR_RAW_LEDGER, temporary / "clean_crosswalk_report.json"
        )
        require(clean_crosswalk.returncode == 0, "CLEAN_CROSSWALK_FAILED")
        require(
            "K3P_COMPLETE_ANCHOR_UNIVERSE_CROSSWALK_PASS"
            in clean_crosswalk.stdout,
            "CLEAN_CROSSWALK_SENTINEL",
        )
        cases.append(
            {
                "name": "clean_control",
                "expected": "accept",
                "observed": "accept",
                "returncode": clean.returncode,
                "stdout_sha256": hashlib.sha256(clean.stdout.encode()).hexdigest(),
                "command": command_record(
                    optimized=False,
                    artifact="anchor_universe/artifacts/NON_FOUR_ANCHOR_UNIVERSE.json",
                ),
                "four_port_crosswalk_control": {
                    "returncode": clean_crosswalk.returncode,
                    "stdout_sha256": hashlib.sha256(
                        clean_crosswalk.stdout.encode()
                    ).hexdigest(),
                    "command": crosswalk_command_record(
                        "four_port_atlas/full_universe_replay/artifacts/"
                        "full_directional_ledger.jsonl.gz"
                    ),
                },
            }
        )
        for number, (name, mutation) in enumerate(MUTATIONS):
            value = copy.deepcopy(pristine)
            mutation(value)
            reseal(value)
            mutated_path = temporary / f"mutation_{number:02d}.json"
            mutated_path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n")
            command, result = run_verifier(
                mutated_path, temporary / f"mutation_{number:02d}_report.json"
            )
            rejected = (
                result.returncode != 0
                and "K3P_INDEPENDENT_NON_FOUR_ANCHOR_UNIVERSE_FAIL" in result.stdout
            )
            require(rejected, f"MUTATION_ACCEPTED:{name}:{result.returncode}")
            case = {
                "name": name,
                "expected": "reject",
                "observed": "reject",
                "returncode": result.returncode,
                "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
                "stdout_tail": result.stdout[-800:],
                "command": command_record(
                    optimized=False, artifact=f"{{mutation_{number:02d}}}"
                ),
            }
            if name == "omit_tree_seed":
                omitted_ledger = temporary / "four_raw_equality_omitted.jsonl.gz"
                omitted_four_port_raw_ledger(FOUR_RAW_LEDGER, omitted_ledger)
                omission_command, omission = run_crosswalk(
                    omitted_ledger,
                    temporary / "four_raw_omission_crosswalk_report.json",
                )
                omission_rejected = (
                    omission.returncode != 0
                    and "FOUR_RAW_LEDGER_BINDING" in omission.stdout
                )
                require(
                    omission_rejected,
                    "FOUR_PORT_RAW_EQUALITY_OMISSION_ACCEPTED",
                )
                case["folded_four_port_raw_equality_omission"] = {
                    "omitted_raw_id": 137124,
                    "expected": "reject",
                    "observed": "reject",
                    "returncode": omission.returncode,
                    "stdout_sha256": hashlib.sha256(
                        omission.stdout.encode()
                    ).hexdigest(),
                    "stdout_tail": omission.stdout[-800:],
                    "command": crosswalk_command_record(
                        "{four_raw_equality_omitted}"
                    ),
                }
            cases.append(case)

        semantic_cases = []

        omitted_ledger = temporary / "four_raw_equality_omitted.jsonl.gz"
        require(omitted_ledger.exists(), "FOUR_PORT_OMISSION_FIXTURE_MISSING")
        omission_summary = temporary / "four_raw_omission_summary.json"
        omission_verification = temporary / "four_raw_omission_verification.json"
        rebound_four_port_bindings(
            omitted_ledger, omission_summary, omission_verification
        )
        command, result = run_crosswalk_with_rebound_bindings(
            omitted_ledger,
            temporary / "four_raw_semantic_omission_report.json",
            four_summary=omission_summary,
            four_verification=omission_verification,
        )
        require(
            result.returncode != 0 and "FOUR_RAW_EQUALITY_COUNT" in result.stdout,
            "REBOUND_FOUR_RAW_EQUALITY_OMISSION_ACCEPTED",
        )
        semantic_cases.append(
            {
                "name": "four_raw_equality_parent_omitted_after_rebinding",
                "expected": "reject",
                "expected_failure_code": "FOUR_RAW_EQUALITY_COUNT",
                "observed": "reject",
                "returncode": result.returncode,
                "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
                "stdout_tail": result.stdout[-800:],
                "coherent_rebinding": {
                    "four_summary_raw_ledger_sha256": sha_file(omitted_ledger),
                    "four_verification_summary_sha256": sha_file(omission_summary),
                },
                "command": rebound_crosswalk_command_record(
                    raw_ledger="{four_raw_equality_omitted}",
                    one_port_ledger="probes/one_port_ledger.jsonl.gz",
                    two_port_ledger="probes/two_port_ledger.jsonl.gz",
                ),
            }
        )

        mutated_one_ledger = temporary / "one_port_equality_status_mutated.jsonl.gz"
        one_census = transform_gzip_jsonl(
            ONE_PORT_LEDGER, mutated_one_ledger, mutate_used_one_port_equality
        )
        require(one_census["matched"] == 1, "ONE_PORT_MUTATION_TARGET_COUNT")
        mutated_one_manifest = temporary / "one_port_manifest_rebound.json"
        rebound_probe_manifest(
            ONE_PORT_MANIFEST,
            mutated_one_manifest,
            mutated_one_ledger,
            one_census,
        )
        command, result = run_crosswalk_with_rebound_bindings(
            FOUR_RAW_LEDGER,
            temporary / "one_port_semantic_mutation_report.json",
            one_port_manifest=mutated_one_manifest,
            one_port_ledger=mutated_one_ledger,
        )
        require(
            result.returncode != 0
            and "FOUR_ONE_PORT_EQUALITY_STATUS" in result.stdout,
            "REBOUND_ONE_PORT_EQUALITY_CORRUPTION_ACCEPTED",
        )
        semantic_cases.append(
            {
                "name": "used_one_port_equality_status_corrupted_after_rebinding",
                "expected": "reject",
                "expected_failure_code": "FOUR_ONE_PORT_EQUALITY_STATUS",
                "observed": "reject",
                "returncode": result.returncode,
                "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
                "stdout_tail": result.stdout[-800:],
                "mutated_key": ["four:raw154873", 0, 0],
                "coherent_rebinding": {
                    "manifest_ledger_sha256": sha_file(mutated_one_ledger),
                    "manifest_payload_sha256": json.loads(
                        mutated_one_manifest.read_text()
                    )["payload_sha256"],
                    "ordered_hash_root": one_census["ordered_hash_root"],
                },
                "command": rebound_crosswalk_command_record(
                    raw_ledger="four_port_atlas/full_universe_replay/artifacts/"
                    "full_directional_ledger.jsonl.gz",
                    one_port_ledger="{one_port_equality_status_mutated}",
                    two_port_ledger="probes/two_port_ledger.jsonl.gz",
                ),
            }
        )

        mutated_two_ledger = temporary / "two_port_separator_status_mutated.jsonl.gz"
        two_census = transform_gzip_jsonl(
            TWO_PORT_LEDGER, mutated_two_ledger, mutate_used_two_port_separator
        )
        require(two_census["matched"] == 1, "TWO_PORT_MUTATION_TARGET_COUNT")
        mutated_two_manifest = temporary / "two_port_manifest_rebound.json"
        rebound_probe_manifest(
            TWO_PORT_MANIFEST,
            mutated_two_manifest,
            mutated_two_ledger,
            two_census,
        )
        command, result = run_crosswalk_with_rebound_bindings(
            FOUR_RAW_LEDGER,
            temporary / "two_port_semantic_mutation_report.json",
            two_port_manifest=mutated_two_manifest,
            two_port_ledger=mutated_two_ledger,
        )
        require(
            result.returncode != 0 and "FOUR_TWO_PORT_NONE_STATUS" in result.stdout,
            "REBOUND_TWO_PORT_SEPARATOR_CORRUPTION_ACCEPTED",
        )
        semantic_cases.append(
            {
                "name": "used_two_port_status_corrupted_after_rebinding",
                "expected": "reject",
                "expected_failure_code": "FOUR_TWO_PORT_NONE_STATUS",
                "observed": "reject",
                "returncode": result.returncode,
                "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
                "stdout_tail": result.stdout[-800:],
                "mutated_key": ["P1:four:raw154873:0:0", 0, 6],
                "coherent_rebinding": {
                    "manifest_ledger_sha256": sha_file(mutated_two_ledger),
                    "manifest_payload_sha256": json.loads(
                        mutated_two_manifest.read_text()
                    )["payload_sha256"],
                    "ordered_hash_root": two_census["ordered_hash_root"],
                },
                "command": rebound_crosswalk_command_record(
                    raw_ledger="four_port_atlas/full_universe_replay/artifacts/"
                    "full_directional_ledger.jsonl.gz",
                    one_port_ledger="probes/one_port_ledger.jsonl.gz",
                    two_port_ledger="{two_port_separator_status_mutated}",
                ),
            }
        )

        extra_terminal_ledger = temporary / "four_extra_terminal_id_mutated.jsonl.gz"
        extra_census = transform_gzip_jsonl(
            FOUR_RAW_LEDGER, extra_terminal_ledger, mutate_extra_terminal_raw_id
        )
        require(extra_census["matched"] == 1, "EXTRA_TERMINAL_MUTATION_TARGET_COUNT")
        extra_summary = temporary / "four_extra_terminal_summary.json"
        extra_verification = temporary / "four_extra_terminal_verification.json"
        rebound_four_port_bindings(
            extra_terminal_ledger, extra_summary, extra_verification
        )
        command, result = run_crosswalk_with_rebound_bindings(
            extra_terminal_ledger,
            temporary / "four_extra_terminal_semantic_report.json",
            four_summary=extra_summary,
            four_verification=extra_verification,
        )
        require(
            result.returncode != 0 and "FOUR_EXTRA_TERMINAL_IDS" in result.stdout,
            "REBOUND_EXTRA_TERMINAL_CORRUPTION_ACCEPTED",
        )
        semantic_cases.append(
            {
                "name": "extra_terminal_descendant_identity_corrupted_after_rebinding",
                "expected": "reject",
                "expected_failure_code": "FOUR_EXTRA_TERMINAL_IDS",
                "observed": "reject",
                "returncode": result.returncode,
                "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
                "stdout_tail": result.stdout[-800:],
                "mutated_raw_id": [202225, 999999999],
                "coherent_rebinding": {
                    "four_summary_raw_ledger_sha256": sha_file(extra_terminal_ledger),
                    "four_verification_summary_sha256": sha_file(extra_summary),
                },
                "command": rebound_crosswalk_command_record(
                    raw_ledger="{four_extra_terminal_id_mutated}",
                    one_port_ledger="probes/one_port_ledger.jsonl.gz",
                    two_port_ledger="probes/two_port_ledger.jsonl.gz",
                ),
            }
        )
        cases.extend(semantic_cases)

        optimized_command, optimized = run_verifier(
            artifact_path, temporary / "optimized_report.json", optimized=True
        )
        optimized_rejected = (
            optimized.returncode != 0
            and "K3P_INDEPENDENT_NON_FOUR_ANCHOR_UNIVERSE_FAIL" in optimized.stdout
        )
        require(optimized_rejected, "OPTIMIZED_MODE_ACCEPTED")
        cases.append(
            {
                "name": "optimized_mode",
                "expected": "reject",
                "observed": "reject",
                "returncode": optimized.returncode,
                "stdout_sha256": hashlib.sha256(optimized.stdout.encode()).hexdigest(),
                "stdout_tail": optimized.stdout[-800:],
                "command": command_record(
                    optimized=True,
                    artifact="anchor_universe/artifacts/NON_FOUR_ANCHOR_UNIVERSE.json",
                ),
            }
        )
    mutation_count = len(MUTATIONS) + 1 + len(semantic_cases)
    report = {
        "schema": "k3p-non-four-anchor-universe-mutations-v2",
        "status": "PASS",
        "bindings": {
            "artifact_sha256": sha_file(artifact_path),
            "verifier_sha256": sha_file(VERIFIER),
            "crosswalk_sha256": sha_file(CROSSWALK),
            "four_summary_sha256": sha_file(FOUR_SUMMARY),
            "four_verification_sha256": sha_file(FOUR_VERIFICATION),
            "four_raw_ledger_sha256": sha_file(FOUR_RAW_LEDGER),
            "one_port_manifest_sha256": sha_file(ONE_PORT_MANIFEST),
            "one_port_ledger_sha256": sha_file(ONE_PORT_LEDGER),
            "two_port_manifest_sha256": sha_file(TWO_PORT_MANIFEST),
            "two_port_parent_inventory_sha256": sha_file(
                TWO_PORT_PARENT_INVENTORY
            ),
            "two_port_ledger_sha256": sha_file(TWO_PORT_LEDGER),
        },
        "counts": {
            "clean_controls": 1,
            "preserved_non_four_and_runtime_mutations": len(MUTATIONS) + 1,
            "coherently_rebound_four_port_semantic_mutations": len(
                semantic_cases
            ),
            "mutations": mutation_count,
            "rejected": mutation_count,
            "accepted": 0,
        },
        "cases": cases,
    }
    report["payload_sha256"] = digest(
        {
            key: value
            for key, value in report.items()
            if key not in {"payload_sha256", "operational"}
        }
    )
    atomic_json(args.output.resolve(), report)
    elapsed = time.monotonic() - started
    print(
        "K3P_NON_FOUR_ANCHOR_MUTATIONS_PASS "
        f"rejected={mutation_count} runtime_seconds={elapsed:.3f}"
    )
    return 0


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--crosswalk-binding-runner":
            raise SystemExit(crosswalk_binding_main(sys.argv[2:]))
        raise SystemExit(main())
    except MutationFailure as exc:
        print(f"K3P_NON_FOUR_ANCHOR_MUTATIONS_FAIL {exc}")
        raise SystemExit(1) from exc
