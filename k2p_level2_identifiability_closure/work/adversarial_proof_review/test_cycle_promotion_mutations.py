#!/usr/bin/env python3
"""Mutation locks for corrected cycle truth and promotion artifacts."""

from __future__ import annotations

import argparse
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
import time
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
OFFICIAL_PROMOTION = PROJECT / "work/cycle_three_port_closure/promotion"
OFFICIAL_TRUTH = HERE / "cycle_tree_sunlet_full_map_certificate.json"
PROMOTION_VERIFIER = HERE / "verify_corrected_cycle_promotion.py"
TRUTH_VERIFIER = HERE / "verify_cycle_whole_map_independent.py"
AUTHORITATIVE_OUTPUT = HERE / "cycle_promotion_mutation_certificate.json"
STORED_PROMOTION_REPLAY = HERE / "cycle_promotion_independent_verification.json"
EXPECTED_DIAGNOSTICS = {
    "omitted_base_raw_record": "CYCLE_PROMOTION_VERIFY_FAIL:base order:0",
    "omitted_dummy_role": (
        "CYCLE_PROMOTION_VERIFY_FAIL:full field:0:dummy_roles_in_label_order"
    ),
    "wrong_source_placement": (
        "CYCLE_PROMOTION_VERIFY_FAIL:full field:0:source_placement_path"
    ),
    "quadratic_certificate_reassigned": "CYCLE_PROMOTION_VERIFY_FAIL:quadratic proof:92",
    "broken_fixed_full_transport": "CYCLE_PROMOTION_VERIFY_FAIL:full transport:0",
    "reassigned_full_map_truth_row": "CYCLE_PROMOTION_VERIFY_FAIL:full truth:558",
    "legacy_rooted_reason_reintroduction": (
        "CYCLE_PROMOTION_VERIFY_FAIL:forbidden fields:base:0:"
        "['topology_exclusion_reason']"
    ),
    "legacy_single_triple_reintroduction": (
        "CYCLE_WHOLE_MAP_REPLAY_FAIL:repair triple:23652"
    ),
    "omitted_truth_row_hash": (
        "CYCLE_WHOLE_MAP_REPLAY_FAIL:truth coverage:cycle_full_equal_topology"
    ),
    "sign_polynomial_reassigned": (
        "CYCLE_WHOLE_MAP_REPLAY_FAIL:sign digest key:"
        "00f81925ab1902e06d3e1bc4125a21b14bac557b25b49314a5742430141b6a0a"
    ),
    "broken_bridge_multihomogeneity": (
        "CYCLE_WHOLE_MAP_REPLAY_FAIL:invariant multidegree:k3:t012:i2"
    ),
    "python_optimized_mode": (
        "CYCLE_PROMOTION_VERIFY_FAIL:CYCLE_PROMOTION_OPTIMIZED_MODE_FORBIDDEN"
    ),
}


class MutationFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise MutationFailure(message)


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


def validate_output_path(output: Path, allow_authoritative_output: bool) -> Path:
    lexical = Path(os.path.abspath(os.fspath(output)))
    normalized = lexical.parent.resolve() / lexical.name
    authoritative = (
        AUTHORITATIVE_OUTPUT.parent.resolve() / AUTHORITATIVE_OUTPUT.name
    )
    source_inputs = {
        Path(__file__).resolve(),
        PROMOTION_VERIFIER.resolve(),
        TRUTH_VERIFIER.resolve(),
        OFFICIAL_TRUTH.resolve(),
        STORED_PROMOTION_REPLAY.resolve(),
        *((path.resolve()) for path in OFFICIAL_PROMOTION.rglob("*") if path.is_file()),
    }
    if lexical.is_symlink():
        raise SystemExit("CYCLE_PROMOTION_MUTATION_OUTPUT_POLICY_FAIL:output symlink")
    if lexical.exists() and any(
        source.exists() and os.path.samefile(lexical, source)
        for source in source_inputs
    ):
        raise SystemExit(
            "CYCLE_PROMOTION_MUTATION_OUTPUT_POLICY_FAIL:output hardlinks source"
        )
    if allow_authoritative_output:
        if normalized != authoritative:
            raise SystemExit(
                "CYCLE_PROMOTION_MUTATION_OUTPUT_POLICY_FAIL:wrong authoritative path"
            )
        return normalized
    try:
        normalized.relative_to(PROJECT.resolve())
    except ValueError:
        return normalized
    raise SystemExit(
        "CYCLE_PROMOTION_MUTATION_OUTPUT_POLICY_FAIL:routine output must be external"
    )


def clear_stale_output(path: Path) -> None:
    path.unlink(missing_ok=True)
    require(not path.exists(), f"stale output remains:{path.name}")


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o644)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        temporary.unlink(missing_ok=True)


def source_fingerprints() -> dict[str, str]:
    summary = json.loads(
        (OFFICIAL_PROMOTION / "cycle_promotion_certificate.json").read_text()
    )
    fixed_inputs = {
        PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py",
        PROJECT / "work/cycle_three_port_closure/cycle_common.py",
        PROJECT / "work/cycle_three_port_closure/generate_cycle_closure.py",
        PROJECT / "work/cycle_three_port_closure/artifacts/base_raw_ledger.jsonl.gz",
        PROJECT / "work/cycle_three_port_closure/artifacts/full_completion_ledger.jsonl.gz",
        PROJECT / "work/cycle_three_port_closure/artifacts/restoration_roots.jsonl.gz",
        PROJECT / "work/cycle_three_port_closure/artifacts/topology_witnesses.json",
        PROJECT / "work/cycle_three_port_closure/artifacts/transport_certificates.json",
        PROJECT / "work/cycle_three_port_closure/artifacts/quadratic_certificates.json",
        PROJECT / "work/cycle_three_port_closure/artifacts/physical_anchors.json",
    }
    paths = {
        Path(__file__).resolve(),
        PROMOTION_VERIFIER.resolve(),
        TRUTH_VERIFIER.resolve(),
        OFFICIAL_TRUTH.resolve(),
        STORED_PROMOTION_REPLAY.resolve(),
        *fixed_inputs,
        *(path.resolve() for path in OFFICIAL_PROMOTION.rglob("*") if path.is_file()),
    }
    require(
        summary["inputs"]["whole_map_truth_file_sha256"] == sha_file(OFFICIAL_TRUTH),
        "authoritative promotion truth binding stale",
    )
    return {
        path.relative_to(PROJECT).as_posix(): sha_file(path)
        for path in sorted(paths)
    }


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


def run_promotion(root, report, timeout, optimized=False):
    report.unlink(missing_ok=True)
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend([
        str(PROMOTION_VERIFIER), "--promotion-root", str(root),
        "--truth-certificate", str(OFFICIAL_TRUTH), "--report", str(report),
    ])
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        env={
            **os.environ,
            "PYTHONHASHSEED": "41",
            "PYTHONDONTWRITEBYTECODE": "1",
        },
        timeout=timeout,
        check=False,
    )


def run_truth(certificate, report, timeout, optimized=False):
    report.unlink(missing_ok=True)
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend([
        str(TRUTH_VERIFIER), "--certificate", str(certificate),
        "--report", str(report), "--structure-only",
    ])
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        env={
            **os.environ,
            "PYTHONHASHSEED": "43",
            "PYTHONDONTWRITEBYTECODE": "1",
        },
        timeout=timeout,
        check=False,
    )


def qualify_failure(completed, expected, report):
    combined = (completed.stderr or "") + (completed.stdout or "")
    exact_lines = [line.strip() for line in combined.splitlines() if line.strip() == expected]
    forbidden = (
        "Traceback (most recent call last):",
        "ModuleNotFoundError",
        "ImportError:",
        "TimeoutExpired",
    )
    qualified = (
        completed.returncode == 1
        and len(exact_lines) == 1
        and not report.exists()
        and not any(marker in combined for marker in forbidden)
        and '"status": "PASS"' not in combined
        and '"status":"PASS"' not in combined
    )
    return qualified, exact_lines[0] if exact_lines else None


def record_failure(results, name, completed, report, verifier, test_type):
    expected = EXPECTED_DIAGNOSTICS[name]
    qualified, observed = qualify_failure(completed, expected, report)
    require(
        qualified,
        f"unqualified rejection:{name}:{completed.returncode}:{observed}",
    )
    results.append({
        "mutation": name,
        "test_type": test_type,
        "production_verifier_invoked": True,
        "production_verifier_sha256": sha_file(verifier),
        "verifier_exit_code": completed.returncode,
        "expected_semantic_diagnostic": expected,
        "observed_semantic_diagnostic": observed,
        "semantic_diagnostic_matched": True,
        "success_artifact_created": False,
        "success_token_observed": False,
        "traceback_observed": False,
        "rejected": True,
        "status": "REJECTED",
    })


def first_kind(kind, change):
    def mutate(row):
        if row.get("terminal_kind") != kind:
            return False
        change(row)
        return row
    return mutate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-authoritative-output", action="store_true")
    parser.add_argument("--timeout-seconds", type=float, default=1200.0)
    arguments = parser.parse_args()
    require(arguments.timeout_seconds > 0, "invalid timeout")
    output = validate_output_path(arguments.output, arguments.allow_authoritative_output)
    clear_stale_output(output)
    if not __debug__:
        raise SystemExit("CYCLE_PROMOTION_MUTATION_OPTIMIZED_MODE_FORBIDDEN")

    before = source_fingerprints()
    results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="cycle_promotion_mutations_") as name:
        temporary = Path(name)

        clean_promotion_report = temporary / "clean-promotion.json"
        clean_promotion_started = time.monotonic()
        clean_promotion = run_promotion(
            OFFICIAL_PROMOTION,
            clean_promotion_report,
            arguments.timeout_seconds,
        )
        clean_promotion_seconds = time.monotonic() - clean_promotion_started
        require(
            clean_promotion.returncode == 0
            and clean_promotion_report.is_file()
            and clean_promotion_report.read_bytes()
            == STORED_PROMOTION_REPLAY.read_bytes()
            and "Traceback (most recent call last):" not in (
                clean_promotion.stderr + clean_promotion.stdout
            ),
            "clean promotion baseline",
        )
        clean_promotion_payload = json.loads(clean_promotion_report.read_text())
        clean_promotion_report_sha256 = sha_file(clean_promotion_report)
        require(
            clean_promotion_payload
            == {
                "base_rows": 13_440,
                "full_children": 536_364,
                "incoherent": 0,
                "legacy_rooted_fields_or_reasons": 0,
                "payload_sha256": clean_promotion_payload["payload_sha256"],
                "promotion_certificate_sha256": sha_file(
                    OFFICIAL_PROMOTION / "cycle_promotion_certificate.json"
                ),
                "promotion_payload_sha256": json.loads(
                    (OFFICIAL_PROMOTION / "cycle_promotion_certificate.json").read_text()
                )["payload_sha256"],
                "restoration_roots": 5_964,
                "schema": "k2p-cycle-authoritative-promotion-independent-verification-v1",
                "status": "PASS",
                "unresolved": 0,
            },
            "clean promotion payload",
        )
        promotion_unsigned = dict(clean_promotion_payload)
        promotion_claimed = promotion_unsigned.pop("payload_sha256")
        require(promotion_claimed == sha(promotion_unsigned), "clean promotion payload hash")

        clean_truth_report = temporary / "clean-truth-structure.json"
        clean_truth_started = time.monotonic()
        clean_truth = run_truth(
            OFFICIAL_TRUTH,
            clean_truth_report,
            arguments.timeout_seconds,
        )
        clean_truth_seconds = time.monotonic() - clean_truth_started
        require(
            clean_truth.returncode == 0
            and clean_truth_report.is_file()
            and "Traceback (most recent call last):" not in (
                clean_truth.stderr + clean_truth.stdout
            ),
            "clean truth-structure baseline",
        )
        clean_truth_payload = json.loads(clean_truth_report.read_text())
        truth_unsigned = dict(clean_truth_payload)
        truth_claimed = truth_unsigned.pop("payload_sha256", None)
        require(
            truth_claimed == sha(truth_unsigned)
            and clean_truth_payload
            == {
                "base_rows": 7_452,
                "full_rows": 300,
                "payload_sha256": truth_claimed,
                "repairs": 24,
                "schema": "k2p-cycle-whole-map-structure-preflight-v1",
                "source_certificate_payload_sha256": json.loads(
                    OFFICIAL_TRUTH.read_text()
                )["payload_sha256"],
                "source_certificate_sha256": sha_file(OFFICIAL_TRUTH),
                "status": "PASS",
                "unresolved": 0,
            },
            "clean truth-structure payload",
        )

        promotion_mutations = [
            (
                "omitted_base_raw_record",
                lambda row: None if row["raw_id"] == 0 else False,
                None,
            ),
            (
                "omitted_dummy_role",
                None,
                lambda row: (
                    {
                        **row,
                        "dummy_roles_in_label_order": row[
                            "dummy_roles_in_label_order"
                        ][1:],
                    }
                    if row["dummy_roles_in_label_order"]
                    else False
                ),
            ),
            (
                "wrong_source_placement",
                None,
                lambda row: (
                    {
                        **row,
                        "source_placement_path": [
                            99,
                            *row["source_placement_path"][1:],
                        ],
                    }
                    if row["source_placement_path"]
                    else False
                ),
            ),
        ]
        quadratic_ids = sorted(
            json.loads(
                (
                    PROJECT
                    / "work/cycle_three_port_closure/artifacts/quadratic_certificates.json"
                ).read_text()
            )["certificates"]
        )
        promotion_mutations.extend([
            (
                "quadratic_certificate_reassigned",
                None,
                first_kind(
                    "exact_directional_quadratic",
                    lambda row: row.update(
                        proof_certificate_id=next(
                            identifier
                            for identifier in quadratic_ids
                            if identifier != row["proof_certificate_id"]
                        )
                    ),
                ),
            ),
            (
                "broken_fixed_full_transport",
                None,
                lambda row: {**row, "fixed_full_transport_sha256": "0" * 64},
            ),
            (
                "reassigned_full_map_truth_row",
                None,
                first_kind(
                    "full_map_Ti_strict_sign",
                    lambda row: row.update(whole_map_truth_row_sha256="f" * 64),
                ),
            ),
            (
                "legacy_rooted_reason_reintroduction",
                first_kind(
                    "full_map_Ti_strict_sign",
                    lambda row: row.update(topology_exclusion_reason="tree_sunlet"),
                ),
                None,
            ),
        ])

        for index, (mutation_name, base_mutator, full_mutator) in enumerate(
            promotion_mutations
        ):
            case = temporary / f"promotion_{index}"
            case.mkdir()
            root = prepare_root(case, base_mutator, full_mutator)
            case_report = case / "report.json"
            completed = run_promotion(
                root, case_report, arguments.timeout_seconds
            )
            record_failure(
                results,
                mutation_name,
                completed,
                case_report,
                PROMOTION_VERIFIER,
                "complete_disposable_cycle_promotion_attack",
            )

        truth_original = json.loads(OFFICIAL_TRUTH.read_text())

        def truth_case(mutation_name, mutate):
            document = copy.deepcopy(truth_original)
            mutate(document)
            rehash_document(document)
            path = temporary / f"{mutation_name}.json"
            path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")
            case_report = temporary / f"{mutation_name}.report.json"
            completed = run_truth(
                path, case_report, arguments.timeout_seconds
            )
            record_failure(
                results,
                mutation_name,
                completed,
                case_report,
                TRUTH_VERIFIER,
                "complete_disposable_cycle_truth_certificate_attack",
            )

        truth_case(
            "legacy_single_triple_reintroduction",
            lambda document: document["revoked_legacy_witness_repairs"][0].update(
                replacement_full_map_triple=[0, 1, 3]
            ),
        )
        truth_case(
            "omitted_truth_row_hash",
            lambda document: document["families"]["cycle_full_equal_topology"][
                "ordered_truth_row_hashes"
            ].pop(),
        )
        truth_case(
            "sign_polynomial_reassigned",
            lambda document: document["sign_certificates"][
                sorted(document["sign_certificates"])[0]
            ].update(pullback_sha256="0" * 64),
        )

        def break_multihomogeneity(document):
            key = sorted(document["coordinate_invariant_certificates"])[0]
            record = document["coordinate_invariant_certificates"][key]
            record["common_boundary_incidence_multidegree"][0] += 1
            record.pop("certificate_sha256", None)
            record["certificate_sha256"] = sha(record)

        truth_case("broken_bridge_multihomogeneity", break_multihomogeneity)

        optimized_report = temporary / "optimized_promotion.json"
        optimized = run_promotion(
            OFFICIAL_PROMOTION,
            optimized_report,
            arguments.timeout_seconds,
            optimized=True,
        )
        record_failure(
            results,
            "python_optimized_mode",
            optimized,
            optimized_report,
            PROMOTION_VERIFIER,
            "optimized_production_verifier_attack",
        )

        expected_control = EXPECTED_DIAGNOSTICS["omitted_base_raw_record"]
        wrong = subprocess.CompletedProcess(
            args=[], returncode=1, stdout="", stderr="CYCLE_PROMOTION_VERIFY_FAIL:wrong gate\n"
        )
        crash = subprocess.CompletedProcess(
            args=[],
            returncode=1,
            stdout="",
            stderr=(
                "Traceback (most recent call last):\n"
                + expected_control
                + "\n"
            ),
        )
        signal = subprocess.CompletedProcess(
            args=[], returncode=-9, stdout="", stderr=expected_control + "\n"
        )
        non_one = subprocess.CompletedProcess(
            args=[], returncode=2, stdout="", stderr=expected_control + "\n"
        )
        pass_token = subprocess.CompletedProcess(
            args=[],
            returncode=1,
            stdout='{"status": "PASS"}\n',
            stderr=expected_control + "\n",
        )
        control_report = temporary / "control-report.json"
        require(
            not qualify_failure(wrong, expected_control, control_report)[0],
            "wrong diagnostic qualified",
        )
        require(
            not qualify_failure(crash, expected_control, control_report)[0],
            "traceback qualified",
        )
        require(
            not qualify_failure(signal, expected_control, control_report)[0],
            "signal qualified",
        )
        require(
            not qualify_failure(non_one, expected_control, control_report)[0],
            "non-one exit qualified",
        )
        require(
            not qualify_failure(pass_token, expected_control, control_report)[0],
            "PASS token qualified",
        )
        control_report.write_text('{"status":"PASS"}\n')
        require(
            not qualify_failure(
                subprocess.CompletedProcess(
                    args=[],
                    returncode=1,
                    stdout="",
                    stderr=expected_control + "\n",
                ),
                expected_control,
                control_report,
            )[0],
            "PASS artifact qualified",
        )
        control_report.unlink()
        timed_out = False
        try:
            subprocess.run(
                [sys.executable, "-B", "-c", "import time; time.sleep(1)"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
                timeout=0.01,
            )
        except subprocess.TimeoutExpired:
            timed_out = True
        require(timed_out, "timeout control did not time out")

        optimized_runner_output = temporary / "optimized-runner-stale.json"
        optimized_runner_output.write_text('{"status":"PASS"}\n')
        optimized_runner = subprocess.run(
            [
                sys.executable,
                "-O",
                "-B",
                str(Path(__file__).resolve()),
                "--output",
                str(optimized_runner_output),
            ],
            cwd=PROJECT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        require(
            optimized_runner.returncode == 1
            and optimized_runner.stdout.strip()
            == "CYCLE_PROMOTION_MUTATION_OPTIMIZED_MODE_FORBIDDEN"
            and not optimized_runner_output.exists(),
            "optimized runner stale-output control",
        )

        policy_target = temporary / "policy-target.json"
        policy_target.write_text("source\n")
        policy_symlink = temporary / "policy-symlink.json"
        policy_symlink.symlink_to(policy_target)
        symlink_rejected = False
        try:
            validate_output_path(policy_symlink, False)
        except SystemExit as error:
            symlink_rejected = str(error).startswith(
                "CYCLE_PROMOTION_MUTATION_OUTPUT_POLICY_FAIL:output symlink"
            )
        require(symlink_rejected, "symlink output policy control")
        policy_symlink.unlink()
        policy_hardlink = temporary / "policy-hardlink.json"
        os.link(OFFICIAL_TRUTH, policy_hardlink)
        hardlink_rejected = False
        try:
            validate_output_path(policy_hardlink, False)
        except SystemExit as error:
            hardlink_rejected = str(error).startswith(
                "CYCLE_PROMOTION_MUTATION_OUTPUT_POLICY_FAIL:output hardlinks source"
            )
        require(hardlink_rejected, "hardlink output policy control")
        policy_hardlink.unlink()

    after = source_fingerprints()
    require(before == after, "authoritative cycle source fingerprint drift")
    require(
        [row["mutation"] for row in results] == list(EXPECTED_DIAGNOSTICS)
        and len(results) == 12
        and all(row["status"] == "REJECTED" for row in results),
        "mutation census/order",
    )
    report = {
        "schema": "k2p-cycle-authoritative-promotion-mutations-v2",
        "status": "PASS",
        "source_promotion_certificate_sha256": sha_file(
            OFFICIAL_PROMOTION / "cycle_promotion_certificate.json"
        ),
        "source_truth_certificate_sha256": sha_file(OFFICIAL_TRUTH),
        "mutation_runner_sha256": sha_file(Path(__file__).resolve()),
        "promotion_verifier_sha256": sha_file(PROMOTION_VERIFIER),
        "truth_verifier_sha256": sha_file(TRUTH_VERIFIER),
        "expected_diagnostics": EXPECTED_DIAGNOSTICS,
        "clean_baseline": {
            "authoritative_promotion_verified_in_place": True,
            "promotion_production_verifier_invoked": True,
            "promotion_verifier_exit_code": clean_promotion.returncode,
            "promotion_success_artifact_created": True,
            "promotion_success_artifact_byte_identical_to_stored": True,
            "promotion_success_artifact_sha256": clean_promotion_report_sha256,
            "promotion_base_rows": clean_promotion_payload["base_rows"],
            "promotion_full_children": clean_promotion_payload["full_children"],
            "promotion_unresolved": clean_promotion_payload["unresolved"],
            "promotion_incoherent": clean_promotion_payload["incoherent"],
            "truth_structure_production_verifier_invoked": True,
            "truth_structure_verifier_exit_code": clean_truth.returncode,
            "truth_structure_success_artifact_created": True,
            "truth_structure_payload_sha256": clean_truth_payload["payload_sha256"],
            "truth_structure_base_rows": clean_truth_payload["base_rows"],
            "truth_structure_full_rows": clean_truth_payload["full_rows"],
            "truth_structure_repairs": clean_truth_payload["repairs"],
            "truth_structure_unresolved": clean_truth_payload["unresolved"],
            "status": "PASS",
        },
        "qualification_negative_controls": {
            "wrong_diagnostic_not_qualified": True,
            "unrelated_traceback_not_qualified": True,
            "signal_exit_not_qualified": True,
            "positive_non_one_exit_not_qualified": True,
            "timeout_not_qualified": True,
            "failure_output_with_pass_token_not_qualified": True,
            "preexisting_pass_artifact_not_qualified": True,
            "optimized_mode_stale_pass_removed_before_rejection": True,
        },
        "output_policy_negative_controls": {
            "symlink_output_rejected": True,
            "hardlink_source_output_rejected": True,
        },
        "source_fingerprints_unchanged": True,
        "mutation_count": len(results),
        "survived": 0,
        "results": results,
    }
    report["payload_sha256"] = sha(report)
    atomic_write(output, json.dumps(report, indent=2, sort_keys=True).encode() + b"\n")
    print(json.dumps({
        "status": report["status"],
        "mutations": report["mutation_count"],
        "survived": report["survived"],
        "payload_sha256": report["payload_sha256"],
        "clean_baseline_seconds": round(
            clean_promotion_seconds + clean_truth_seconds, 3
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (
        MutationFailure,
        RuntimeError,
        KeyError,
        OSError,
        ValueError,
        json.JSONDecodeError,
        subprocess.TimeoutExpired,
    ) as exc:
        print(f"CYCLE_PROMOTION_MUTATION_FAIL:{exc}", file=sys.stderr)
        raise SystemExit(1)
