#!/usr/bin/env python3
"""Coherent, hash-resealed adversarial mutations for the independent replay."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE = HERE / "artifacts"
VERIFIER = HERE / "verify_full_four_port_replay.py"
REPORT = HERE / "FULL_FOUR_PORT_MUTATION_REPORT.json"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_gzip_json(root, name):
    with gzip.open(root / name, "rb") as handle:
        return json.loads(handle.read())


def write_gzip_json(root, name, value):
    with (root / name).open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as encoded:
            encoded.write(canonical(value) + b"\n")


def read_ledger(root):
    with gzip.open(root / "full_directional_ledger.jsonl.gz", "rt") as handle:
        return [json.loads(line) for line in handle]


def write_ledger(root, rows):
    with (root / "full_directional_ledger.jsonl.gz").open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as encoded:
            for row in rows:
                encoded.write(canonical(row) + b"\n")


def gzip_binding(path):
    compressed = file_hash(path)
    with gzip.open(path, "rb") as handle:
        payload = handle.read()
    return {"sha256": compressed,
            "uncompressed_sha256": hashlib.sha256(payload).hexdigest(),
            "uncompressed_bytes": len(payload)}


def reseal(root):
    summary_path = root / "FULL_FOUR_PORT_REPLAY.json"
    summary = json.loads(summary_path.read_text())
    for name in summary["artifacts"]:
        path = root / name
        summary["artifacts"][name] = (gzip_binding(path) if name.endswith(".gz") else
                                      {"sha256": file_hash(path), "bytes": path.stat().st_size})
    summary.pop("payload_sha256_without_hash", None)
    summary["payload_sha256_without_hash"] = hashlib.sha256(canonical(summary)).hexdigest()
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")


def invoke(root, extra, optimized=False):
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command += [str(VERIFIER), "--artifact-root", str(root), *extra]
    result = subprocess.run(command, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, timeout=180)
    return result.returncode, result.stdout


def update_class_category(record, old, new):
    require(record["member_categories"] == {old: record["raw_member_count"]},
            "class category precondition")
    record["member_categories"] = {new: record["raw_member_count"]}
    for member in record["members"]:
        require(member["category"] == old, "member category precondition")
        member["category"] = new


def raw_id(member, source_index):
    return (source_index * 2_814 + member["target_index"]) * 24 + member["permutation_index"]


def mutate_omit_and_reseal(root):
    rows = read_ledger(root)
    removed = rows.pop()
    summary = json.loads((root / "FULL_FOUR_PORT_REPLAY.json").read_text())
    summary["primitive_counts"]["raw_total"] -= 1
    summary["raw_category_counts"][removed["category"]] -= 1
    (root / "FULL_FOUR_PORT_REPLAY.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_ledger(root, rows)
    reseal(root)
    return ["--structure-only"], "LEDGER_CENSUS"


def mutate_iso_triangle_swap(root):
    classes = read_gzip_json(root, "eligible_class_registry.json.gz")
    iso = next(row for row in classes["records"]
               if row["raw_member_count"] == 1 and row["member_categories"] == {"isomorphic": 1})
    triangle = next(row for row in classes["records"]
                    if row["raw_member_count"] == 1 and row["member_categories"] == {"ordinary_triangle": 1})
    update_class_category(iso, "isomorphic", "ordinary_triangle")
    update_class_category(triangle, "ordinary_triangle", "isomorphic")
    iso["members"][0]["graph_relation"] = "triangle"
    triangle["members"][0]["graph_relation"] = "isomorphic"
    iso_id = raw_id(iso["members"][0], iso["source_index"])
    triangle_id = raw_id(triangle["members"][0], triangle["source_index"])
    rows = read_ledger(root)
    rows[iso_id]["category"] = "ordinary_triangle"
    rows[iso_id]["graph_relation"] = "triangle"
    rows[triangle_id]["category"] = "isomorphic"
    rows[triangle_id]["graph_relation"] = "isomorphic"
    write_gzip_json(root, "eligible_class_registry.json.gz", classes)
    write_ledger(root, rows)
    reseal(root)
    return ["--focus-raw-id", str(iso_id)], "FOCUS_RAW_CATEGORY"


def mutate_restoration_quadratic_swap(root):
    classes = read_gzip_json(root, "eligible_class_registry.json.gz")
    restoration = next(row for row in classes["records"]
                       if row["raw_member_count"] == 1 and
                       row["member_categories"] == {"restoration_obligation": 1})
    quadratic = next(row for row in classes["records"]
                     if row["raw_member_count"] == 1 and
                     row["member_categories"] == {"quadratic_separated": 1})
    update_class_category(restoration, "restoration_obligation", "quadratic_separated")
    update_class_category(quadratic, "quadratic_separated", "restoration_obligation")
    restoration["quadratic_certificate"] = quadratic["quadratic_certificate"]
    quadratic["quadratic_certificate"] = None
    restoration_id = raw_id(restoration["members"][0], restoration["source_index"])
    quadratic_id = raw_id(quadratic["members"][0], quadratic["source_index"])
    restoration["members"][0]["restoration_raw_id"] = None
    quadratic["members"][0]["restoration_raw_id"] = quadratic_id
    rows = read_ledger(root)
    rows[restoration_id]["category"] = "quadratic_separated"
    rows[restoration_id]["restoration_raw_id"] = None
    rows[quadratic_id]["category"] = "restoration_obligation"
    rows[quadratic_id]["restoration_raw_id"] = quadratic_id
    write_gzip_json(root, "eligible_class_registry.json.gz", classes)
    write_ledger(root, rows)
    reseal(root)
    return ["--focus-restoration"], "FOREST_RESTORATION_PRESENTATION_BIJECTION"


def mutate_upper_system_rank(root):
    upper = read_gzip_json(root, "exact_rank_upper_registry.json.gz")
    record = upper["records"][0]
    record["coefficient_system_rank"] += 1
    record["stacked_system_rank"] += 1
    digest = record["descriptor_sha256"]
    write_gzip_json(root, "exact_rank_upper_registry.json.gz", upper)
    reseal(root)
    return ["--focus-upper-hash", digest], "FOCUSED_UPPER_SEMANTICS"


def mutate_quotient_omit_orbit(root):
    path = root / "DERIVED_RESIDUE_QUOTIENT.json"
    quotient = json.loads(path.read_text())
    removed = quotient["orbits"].pop()
    quotient["canonical_orbits"] -= 1
    quotient["raw_records_in_fourteen_orbits"] -= len(removed["raw_members"])
    path.write_text(json.dumps(quotient, indent=2, sort_keys=True) + "\n")
    summary = json.loads((root / "FULL_FOUR_PORT_REPLAY.json").read_text())
    summary["residue_quotient"]["canonical_orbits"] = quotient["canonical_orbits"]
    summary["residue_quotient"]["raw_records_in_fourteen_orbits"] = quotient["raw_records_in_fourteen_orbits"]
    (root / "FULL_FOUR_PORT_REPLAY.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n")
    reseal(root)
    return ["--structure-only"], "QUOTIENT_FIXED_CENSUS"


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError("mutation suite refuses optimized mode")
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, default=REPORT)
    args = parser.parse_args()
    started = time.monotonic()
    baseline_code, baseline_output = invoke(BASE, ["--structure-only"])
    require(baseline_code == 0 and "K3P_FULL_FOUR_PORT_INDEPENDENT_STRUCTURE_PASS" in baseline_output,
            "baseline structure verification failed")
    mutations = [
        ("coherent_raw_omission", mutate_omit_and_reseal),
        ("coherent_isomorphic_triangle_reclassification", mutate_iso_triangle_swap),
        ("coherent_restoration_quadratic_reclassification", mutate_restoration_quadratic_swap),
        ("coefficientwise_upper_rank_forgery", mutate_upper_system_rank),
        ("coherent_quotient_orbit_omission", mutate_quotient_omit_orbit),
    ]
    results = []
    with tempfile.TemporaryDirectory(prefix="k3p-four-port-mutations-") as temporary:
        temporary = Path(temporary)
        for name, mutate in mutations:
            root = temporary / name
            shutil.copytree(BASE, root)
            arguments, expected = mutate(root)
            code, output = invoke(root, arguments)
            require(code != 0, f"mutation survived: {name}")
            require(expected in output, f"mutation rejected for wrong reason: {name}: {output[-1000:]}")
            results.append({"name": name, "rejected": True,
                            "expected_failure": expected,
                            "output_sha256": hashlib.sha256(output.encode()).hexdigest()})
    optimized_code, optimized_output = invoke(BASE, ["--structure-only"], optimized=True)
    require(optimized_code != 0 and "OPTIMIZED_MODE_FORBIDDEN" in optimized_output,
            "optimized verifier execution survived")
    results.append({"name": "optimized_mode", "rejected": True,
                    "expected_failure": "OPTIMIZED_MODE_FORBIDDEN",
                    "output_sha256": hashlib.sha256(optimized_output.encode()).hexdigest()})
    report = {
        "schema": "k3p-full-four-port-coherent-mutations-v1",
        "status": "PASS", "rejected": len(results), "survived": 0,
        "mutations": results,
        "verifier_sha256": file_hash(VERIFIER),
        "core_sha256": file_hash(HERE / "independent_replay_core.py"),
        "operational": {"runtime_seconds": time.monotonic() - started},
    }
    logical = {key: value for key, value in report.items() if key != "operational"}
    report["payload_sha256"] = hashlib.sha256(canonical(logical)).hexdigest()
    output = args.report.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + f".tmp.{os.getpid()}")
    temporary.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print("K3P_FULL_FOUR_PORT_COHERENT_MUTATIONS_PASS")
    print(json.dumps({"rejected": len(results), "report": str(output),
                      "runtime_seconds": time.monotonic() - started}, sort_keys=True))


if __name__ == "__main__":
    main()
