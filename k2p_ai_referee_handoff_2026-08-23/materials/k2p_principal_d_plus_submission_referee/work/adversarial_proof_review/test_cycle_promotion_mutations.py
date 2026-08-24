#!/usr/bin/env python3
"""Mutation locks for corrected cycle truth and promotion artifacts."""

from __future__ import annotations

import copy
import gzip
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
OFFICIAL_PROMOTION = PROJECT / "work/cycle_three_port_closure/promotion"
OFFICIAL_TRUTH = HERE / "cycle_tree_sunlet_full_map_certificate.json"
PROMOTION_VERIFIER = HERE / "verify_corrected_cycle_promotion.py"
TRUTH_VERIFIER = HERE / "verify_cycle_whole_map_independent.py"
OUTPUT = HERE / "cycle_promotion_mutation_certificate.json"


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def rehash_document(document):
    document.pop("payload_sha256", None)
    document["payload_sha256"] = sha(document)


class GzipWriter:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.raw = self.path.open("wb")
        self.compressed = gzip.GzipFile(
            filename="", mode="wb", fileobj=self.raw, compresslevel=9, mtime=0
        )
        self.text = io.TextIOWrapper(self.compressed, encoding="utf-8", newline="\n")
        return self

    def write(self, row):
        self.text.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")

    def __exit__(self, exc_type, exc, traceback):
        self.text.close()
        self.raw.close()
        return False


def rewrite_ledger(source, target, mutator):
    changed = False
    with gzip.open(source, "rt") as handle, GzipWriter(target) as output:
        for row in map(json.loads, handle):
            if not changed:
                candidate = mutator(copy.deepcopy(row))
                if candidate is not False:
                    changed = True
                    if candidate is None:
                        continue
                    candidate.pop("authoritative_row_sha256", None)
                    candidate["authoritative_row_sha256"] = sha(candidate)
                    row = candidate
            output.write(row)
    if not changed:
        raise RuntimeError("mutation target not found")


def prepare_root(temporary, mutate_base=None, mutate_full=None):
    root = temporary / "promotion"
    root.mkdir()
    base_name = "cycle_base_authoritative.jsonl.gz"
    full_name = "cycle_full_authoritative.jsonl.gz"
    if mutate_base is None:
        os.symlink(OFFICIAL_PROMOTION / base_name, root / base_name)
    else:
        rewrite_ledger(OFFICIAL_PROMOTION / base_name, root / base_name, mutate_base)
    if mutate_full is None:
        os.symlink(OFFICIAL_PROMOTION / full_name, root / full_name)
    else:
        rewrite_ledger(OFFICIAL_PROMOTION / full_name, root / full_name, mutate_full)
    shutil.copy2(OFFICIAL_PROMOTION / "cycle_promotion_certificate.json", root)
    refresh_summary(root)
    return root


def refresh_summary(root):
    summary_path = root / "cycle_promotion_certificate.json"
    summary = json.loads(summary_path.read_text())
    base_hashes, base_counts = [], {}
    with gzip.open(root / "cycle_base_authoritative.jsonl.gz", "rt") as handle:
        for row in map(json.loads, handle):
            base_hashes.append(row["authoritative_row_sha256"])
            kind = row["terminal_kind"]
            base_counts[kind] = base_counts.get(kind, 0) + 1
    full_hashes, full_counts, transports, child_counts = [], {}, [], {}
    with gzip.open(root / "cycle_full_authoritative.jsonl.gz", "rt") as handle:
        for row in map(json.loads, handle):
            full_hashes.append(row["authoritative_row_sha256"])
            kind = row["terminal_kind"]
            full_counts[kind] = full_counts.get(kind, 0) + 1
            transports.append(row["fixed_full_transport_sha256"])
            root_id = row["root_id"]
            child_counts[root_id] = child_counts.get(root_id, 0) + 1
    roots = set()
    with gzip.open(PROJECT / "work/cycle_three_port_closure/artifacts/restoration_roots.jsonl.gz", "rt") as handle:
        roots = {json.loads(line)["root_id"] for line in handle}
    summary["base"].update({
        "rows": len(base_hashes), "terminal_census": base_counts,
        "ordered_authoritative_row_hash_root": sha(base_hashes),
    })
    summary["full"].update({
        "rows": len(full_hashes), "terminal_census": full_counts,
        "ordered_authoritative_row_hash_root": sha(full_hashes),
    })
    summary["fixed_full_restoration"].update({
        "children": len(full_hashes),
        "roots_with_zero_children": len(roots - set(child_counts)),
        "ordered_child_transport_hash_root": sha(transports),
    })
    for name, row_count in (
        ("cycle_base_authoritative.jsonl.gz", len(base_hashes)),
        ("cycle_full_authoritative.jsonl.gz", len(full_hashes)),
    ):
        summary["outputs"][name] = {"sha256": sha_file(root / name), "rows": row_count}
    rehash_document(summary)
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")


def run_promotion(root, report, optimized=False):
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend([
        str(PROMOTION_VERIFIER), "--promotion-root", str(root),
        "--truth-certificate", str(OFFICIAL_TRUTH), "--report", str(report),
    ])
    return subprocess.run(command, capture_output=True, text=True, env={**os.environ, "PYTHONHASHSEED": "41"})


def run_truth(certificate, report, optimized=False):
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend([
        str(TRUTH_VERIFIER), "--certificate", str(certificate),
        "--report", str(report), "--structure-only",
    ])
    return subprocess.run(command, capture_output=True, text=True, env={**os.environ, "PYTHONHASHSEED": "43"})


def diagnostic(completed, prefix, name):
    lines = (completed.stderr + completed.stdout).strip().splitlines()
    if completed.returncode == 0:
        raise RuntimeError(f"mutation survived:{name}")
    if not lines or prefix not in lines[-1]:
        raise RuntimeError(f"bad diagnostic:{name}:{lines[-3:]}")
    return lines[-1]


def first_kind(kind, change):
    def mutate(row):
        if row.get("terminal_kind") != kind:
            return False
        change(row)
        return row
    return mutate


def main():
    results = []
    with tempfile.TemporaryDirectory(prefix="cycle_promotion_mutations_") as name:
        temporary = Path(name)
        promotion_mutations = []

        promotion_mutations.append((
            "omitted_base_raw_record",
            lambda row: None if row["raw_id"] == 0 else False,
            None,
        ))
        promotion_mutations.append((
            "omitted_dummy_role",
            None,
            lambda row: (
                {**row, "dummy_roles_in_label_order": row["dummy_roles_in_label_order"][1:]}
                if row["dummy_roles_in_label_order"] else False
            ),
        ))
        promotion_mutations.append((
            "wrong_source_placement",
            None,
            lambda row: (
                {**row, "source_placement_path": [99, *row["source_placement_path"][1:]]}
                if row["source_placement_path"] else False
            ),
        ))
        quadratic_ids = sorted(
            json.loads((PROJECT / "work/cycle_three_port_closure/artifacts/quadratic_certificates.json").read_text())["certificates"]
        )
        promotion_mutations.append((
            "quadratic_certificate_reassigned",
            None,
            first_kind("exact_directional_quadratic", lambda row: row.update(
                proof_certificate_id=next(identifier for identifier in quadratic_ids if identifier != row["proof_certificate_id"])
            )),
        ))
        promotion_mutations.append((
            "broken_fixed_full_transport",
            None,
            lambda row: {**row, "fixed_full_transport_sha256": "0" * 64},
        ))
        promotion_mutations.append((
            "reassigned_full_map_truth_row",
            None,
            first_kind("full_map_Ti_strict_sign", lambda row: row.update(
                whole_map_truth_row_sha256="f" * 64
            )),
        ))
        promotion_mutations.append((
            "legacy_rooted_reason_reintroduction",
            first_kind("full_map_Ti_strict_sign", lambda row: row.update(
                topology_exclusion_reason="tree_sunlet"
            )),
            None,
        ))

        for index, (mutation_name, base_mutator, full_mutator) in enumerate(promotion_mutations):
            case = temporary / f"promotion_{index}"
            case.mkdir()
            root = prepare_root(case, base_mutator, full_mutator)
            completed = run_promotion(root, case / "report.json")
            results.append({
                "mutation": mutation_name, "rejected": True,
                "diagnostic": diagnostic(completed, "CYCLE_PROMOTION_VERIFY_FAIL:", mutation_name),
            })

        truth_original = json.loads(OFFICIAL_TRUTH.read_text())

        def truth_case(mutation_name, mutate):
            document = copy.deepcopy(truth_original)
            mutate(document)
            rehash_document(document)
            path = temporary / f"{mutation_name}.json"
            path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")
            completed = run_truth(path, temporary / f"{mutation_name}.report.json")
            results.append({
                "mutation": mutation_name, "rejected": True,
                "diagnostic": diagnostic(completed, "CYCLE_WHOLE_MAP_REPLAY_FAIL:", mutation_name),
            })

        truth_case("legacy_single_triple_reintroduction", lambda document: document[
            "revoked_legacy_witness_repairs"
        ][0].update(replacement_full_map_triple=[0, 1, 3]))
        truth_case("omitted_truth_row_hash", lambda document: document[
            "families"
        ]["cycle_full_equal_topology"]["ordered_truth_row_hashes"].pop())
        truth_case("sign_polynomial_reassigned", lambda document: document[
            "sign_certificates"
        ][sorted(document["sign_certificates"])[0]].update(pullback_sha256="0" * 64))

        def break_multihomogeneity(document):
            key = sorted(document["coordinate_invariant_certificates"])[0]
            record = document["coordinate_invariant_certificates"][key]
            record["common_boundary_incidence_multidegree"][0] += 1
            record.pop("certificate_sha256", None)
            record["certificate_sha256"] = sha(record)

        truth_case("broken_bridge_multihomogeneity", break_multihomogeneity)

        optimized = run_promotion(
            OFFICIAL_PROMOTION, temporary / "optimized_promotion.json", optimized=True
        )
        results.append({
            "mutation": "python_optimized_mode", "rejected": True,
            "diagnostic": diagnostic(
                optimized, "CYCLE_PROMOTION_OPTIMIZED_MODE_FORBIDDEN", "python_optimized_mode"
            ),
        })

    report = {
        "schema": "k2p-cycle-authoritative-promotion-mutations-v1",
        "status": "PASS",
        "source_promotion_certificate_sha256": sha_file(
            OFFICIAL_PROMOTION / "cycle_promotion_certificate.json"
        ),
        "source_truth_certificate_sha256": sha_file(OFFICIAL_TRUTH),
        "mutation_count": len(results), "survived": 0, "results": results,
    }
    report["payload_sha256"] = sha(report)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": report["status"], "mutations": report["mutation_count"],
        "survived": report["survived"], "payload_sha256": report["payload_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, KeyError, OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"CYCLE_PROMOTION_MUTATION_FAIL:{exc}") from exc
