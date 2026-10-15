#!/usr/bin/env python3
"""Reproduce utility portability, optimization, and mutation-control receipts.

Fixtures contain only the current public allowlist and unchanged original
packet. They are disposable copies under ignored private_tmp/. No source PDF
or mathematical candidate file is modified by this script.
"""
from pathlib import Path
import argparse
import ast
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

PREFIX = "unsolved_math_prioritization/attempts/30006419/"
CONTROL_PIN = "e022ef5834ae41f135a308818af975d612c59af0fc4e836ee397a4e451b02783"
MODES = {"normal": [], "-O": ["-O"], "-OO": ["-OO"]}


class ReceiptFailure(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ReceiptFailure(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def locate_inputs(root):
    for ancestor in (root, *root.parents):
        if (ancestor / "ORIGINAL_SNAPSHOT.json").is_file():
            snapshot = json.loads((ancestor / "ORIGINAL_SNAPSHOT.json").read_text())
            if (ancestor / "original").is_dir():
                return ancestor, snapshot, "original"
            if (ancestor / "original_packet").is_dir():
                return ancestor, snapshot, "original_packet"
    raise ReceiptFailure("No supported original input layout found")


def build_fixture(root, destination, layout):
    package, snapshot, source_layout = locate_inputs(root)
    review = destination / "reviews" / "reshetnyak_proof_family"
    review.mkdir(parents=True)
    manifest = json.loads((root / "MANIFEST.json").read_text())
    for name in [*manifest["intentional_public_files"], "MANIFEST.json"]:
        target = review / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / name, target)
    shutil.copy2(package / "ORIGINAL_SNAPSHOT.json", destination / "ORIGINAL_SNAPSHOT.json")
    for name in snapshot["files"]:
        suffix = name.removeprefix(PREFIX)
        source = package / source_layout / (name if source_layout == "original" else suffix)
        target = destination / ("original" if layout == "workspace" else "original_packet") / (
            name if layout == "workspace" else suffix)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return review


def command(script, mode, arguments=()):
    result = subprocess.run([sys.executable, *MODES[mode], str(script), *map(str, arguments)],
                            text=True, capture_output=True, timeout=4)
    return result


def rehash_review_entry(review, name):
    path = review / name
    manifest_path = review / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["intentional_public_files"][name] = {
        "bytes": path.stat().st_size, "sha256": sha(path)}
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")


def mutate(package, review, layout, case):
    proof = package / ("original" if layout == "workspace" else "original_packet") / (
        PREFIX + "author/PROOF.md" if layout == "workspace" else "author/PROOF.md")
    if case == "public_hash_tamper":
        with (review / "AUDIT.md").open("ab") as stream:
            stream.write(b"\nmutation\n")
    elif case == "missing_public_file":
        (review / "AUDIT.md").unlink()
    elif case == "unlisted_regular_file":
        (review / "rogue.txt").write_text("unlisted\n")
    elif case == "unlisted_empty_directory":
        (review / "rogue_directory").mkdir()
    elif case == "unlisted_file_added_to_manifest":
        (review / "rogue.txt").write_text("unlisted\n")
        rehash_review_entry(review, "rogue.txt")
    elif case == "broaden_manifest_exclusions":
        path = review / "MANIFEST.json"
        manifest = json.loads(path.read_text())
        manifest["excluded_globs"].append("*")
        path.write_text(json.dumps(manifest, indent=2) + "\n")
    elif case == "public_symlink":
        (review / "AUDIT.md").unlink()
        (review / "AUDIT.md").symlink_to("RESULT.json")
    elif case == "listed_fifo":
        (review / "CONTROL_RESULTS.json").unlink()
        os.mkfifo(review / "CONTROL_RESULTS.json")
    elif case == "unlisted_fifo":
        os.mkfifo(review / "rogue.pipe")
    elif case == "manifest_fifo":
        (review / "MANIFEST.json").unlink()
        os.mkfifo(review / "MANIFEST.json")
    elif case == "original_proof_tamper":
        with proof.open("ab") as stream:
            stream.write(b"\nmutation\n")
    elif case == "proof_and_snapshot_self_consistent_tamper":
        with proof.open("ab") as stream:
            stream.write(b"\nmutation\n")
        path = package / "ORIGINAL_SNAPSHOT.json"
        snapshot = json.loads(path.read_text())
        snapshot["files"][PREFIX + "author/PROOF.md"] = sha(proof)
        path.write_text(json.dumps(snapshot, indent=2) + "\n")
    elif case == "original_proof_fifo":
        proof.unlink()
        os.mkfifo(proof)
    elif case == "initial_history_tamper_with_rehashed_active_manifest":
        name = "history/initial_revision/AUDIT.md"
        with (review / name).open("ab") as stream:
            stream.write(b"\nmutation\n")
        rehash_review_entry(review, name)
    elif case == "history_manifest_self_consistent_tamper":
        prefix = "history/initial_revision/"
        history_audit = review / prefix / "AUDIT.md"
        with history_audit.open("ab") as stream:
            stream.write(b"\nmutation\n")
        history_manifest = review / prefix / "MANIFEST.json"
        document = json.loads(history_manifest.read_text())
        document["intentional_public_files"]["AUDIT.md"] = {
            "bytes": history_audit.stat().st_size, "sha256": sha(history_audit)}
        history_manifest.write_text(json.dumps(document, indent=2) + "\n")
        rehash_review_entry(review, prefix + "AUDIT.md")
        rehash_review_entry(review, prefix + "MANIFEST.json")
    elif case == "control_result_tamper_with_rehashed_manifest":
        (review / "CONTROL_RESULTS.json").write_text("{}\n")
        rehash_review_entry(review, "CONTROL_RESULTS.json")
    else:
        raise ReceiptFailure(f"Unknown mutation case: {case}")


VERIFIER_MUTATIONS = [
    "public_hash_tamper", "missing_public_file", "unlisted_regular_file",
    "unlisted_empty_directory", "unlisted_file_added_to_manifest",
    "broaden_manifest_exclusions", "public_symlink", "listed_fifo",
    "unlisted_fifo", "manifest_fifo", "original_proof_tamper",
    "proof_and_snapshot_self_consistent_tamper", "original_proof_fifo",
    "initial_history_tamper_with_rehashed_active_manifest",
    "history_manifest_self_consistent_tamper",
    "control_result_tamper_with_rehashed_manifest",
]


def run():
    root = Path(__file__).absolute().parent
    receipts = []
    ast_counts = {}
    for name in ("independent_controls.py", "verify_manifest.py", "utility_repair_checks.py"):
        count = sum(isinstance(node, ast.Assert) for node in ast.walk(ast.parse((root / name).read_text())))
        require(count == 0, f"Active utility still contains optimization-disabled assertions: {name}")
        ast_counts[name] = count
    require(sha(root / "CONTROL_RESULTS.json") == CONTROL_PIN,
            "Active analytic control result has changed")
    require((root / "CONTROL_RESULTS.json").read_bytes() ==
            (root / "history" / "initial_revision" / "CONTROL_RESULTS.json").read_bytes(),
            "Current control result is not byte-identical to initial revision")
    temporary = root / "private_tmp"
    temporary.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="utility_receipts_", dir=temporary) as task_tmp:
        task_root = Path(task_tmp)
        for layout in ("workspace", "standalone"):
            base = task_root / f"base_{layout}"
            review = build_fixture(root, base, layout)
            for mode in MODES:
                for explicit in (False, True):
                    args = ["--audit-root", base] if explicit else []
                    result = command(review / "verify_manifest.py", mode, args)
                    require(result.returncode == 0, f"Valid {layout}/{mode} verifier failed: {result.stderr}")
                    output = json.loads(result.stdout)
                    require(output["layout"] == layout and output["original_file_count"] == 30,
                            "Valid verifier reported wrong layout or original count")
                    receipts.append({"utility": "verify_manifest.py", "layout": layout,
                                     "mode": mode, "case": "valid_explicit_root" if explicit else "valid_auto_root",
                                     "expected": "accept", "passed": True})
                output_file = task_root / f"control_{layout}_{mode.replace('-', '')}.json"
                result = command(review / "independent_controls.py", mode, ["--output", output_file])
                require(result.returncode == 0, f"Valid control run failed: {result.stderr}")
                require(sha(output_file) == CONTROL_PIN, "Control result bytes changed under optimization")
                receipts.append({"utility": "independent_controls.py", "layout": layout,
                                 "mode": mode, "case": "fixed_analytic_controls",
                                 "expected": "accept_unchanged_result", "passed": True})

            for case in VERIFIER_MUTATIONS:
                package = task_root / f"case_{layout}_{case}"
                shutil.copytree(base, package)
                mutated_review = package / "reviews" / "reshetnyak_proof_family"
                mutate(package, mutated_review, layout, case)
                for mode in MODES:
                    result = command(mutated_review / "verify_manifest.py", mode)
                    require(result.returncode != 0 and "Verification failure:" in result.stderr,
                            f"Mutation was not explicitly rejected: {layout}/{mode}/{case}")
                    if "fifo" in case:
                        require("before open" in result.stderr,
                                f"FIFO rejection was not recorded before content open: {case}")
                    receipts.append({"utility": "verify_manifest.py", "layout": layout,
                                     "mode": mode, "case": case,
                                     "expected": "reject", "passed": True,
                                     "fifo_rejected_before_open": True if "fifo" in case else None})

            for case in ("false_scalar_control_guard", "wrong_fixed_result_pin"):
                package = task_root / f"case_{layout}_{case}"
                shutil.copytree(base, package)
                script = package / "reviews" / "reshetnyak_proof_family" / "independent_controls.py"
                source = script.read_text()
                if case == "false_scalar_control_guard":
                    require("cross == 0 and" in source, "Scalar mutation anchor disappeared")
                    source = source.replace("cross == 0 and", "cross == 1 and", 1)
                else:
                    require(CONTROL_PIN in source, "Fixed result pin mutation anchor disappeared")
                    source = source.replace(CONTROL_PIN, "0" * 64, 1)
                script.write_text(source)
                for mode in MODES:
                    output_file = task_root / f"bad_control_{layout}_{case}_{mode.replace('-', '')}.json"
                    result = command(script, mode, ["--output", output_file])
                    require(result.returncode != 0 and "Control failure:" in result.stderr,
                            f"Control mutation accepted under {mode}: {case}")
                    require(not output_file.exists(), "Failed control wrote a result file")
                    receipts.append({"utility": "independent_controls.py", "layout": layout,
                                     "mode": mode, "case": case,
                                     "expected": "reject_without_output", "passed": True})
    return {
        "purpose": "utility-only portability, optimization and mutation validation",
        "analytic_verdict_changed": False,
        "original_packet_modified": False,
        "initial_revision_preserved": True,
        "control_result_sha256_unchanged": CONTROL_PIN,
        "active_assert_node_counts": ast_counts,
        "supported_layouts": ["workspace", "standalone"],
        "python_modes": list(MODES),
        "receipt_count": len(receipts),
        "all_passed": True,
        "disposable_fixtures": "ignored private_tmp/; automatically removed",
        "receipts": receipts,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("UTILITY_REPAIR_RESULTS.json"))
    args = parser.parse_args()
    try:
        result = run()
        args.output.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps({"all_passed": result["all_passed"], "receipt_count": result["receipt_count"]}))
    except (ReceiptFailure, OSError, ValueError, subprocess.TimeoutExpired) as exc:
        parser.exit(1, f"Utility receipt failure: {exc}\n")
