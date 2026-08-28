#!/usr/bin/env python3
"""Targeted mutations for inheritance and paired-edge transport semantics."""

from __future__ import annotations

import argparse
import copy
import collections
import gzip
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
STRICT_JSON_DIR = PROJECT / "work/final_theorem_release"
if str(STRICT_JSON_DIR) not in sys.path:
    sys.path.insert(0, str(STRICT_JSON_DIR))

from strict_json import (  # noqa: E402
    StrictJSONError,
    decode_json_document,
    iter_canonical_gzip_jsonl,
)

VERIFY_PATH = HERE / "verify_parameter_transport_certificate.py"
AUTHORITATIVE_OUTPUT = HERE / "parameter_transport_mutation_report.json"
ANSI_ESCAPE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
USER_PATH = re.compile(r"/Users/[^/\s\"']+")
DARWIN_TEMP_PATH = re.compile(r"/(?:private/)?var/folders/[^\s\"']+")
CHILD_OUTPUT_TAIL_LIMIT = 2048


class Failure(RuntimeError):
    pass


def load_plain_json(path: Path) -> dict[str, Any]:
    try:
        return decode_json_document(
            path.read_bytes(), label=path.name, require_object=True
        )
    except (OSError, StrictJSONError) as error:
        raise Failure(f"strict JSON:{path}:{error}") from error


def iter_jsonl(path: Path):
    try:
        yield from iter_canonical_gzip_jsonl(path, label=path.name)
    except (OSError, StrictJSONError) as error:
        raise Failure(f"strict JSON:{path}:{error}") from error


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


def validate_output_path(output: Path, allow_authoritative_output: bool) -> Path:
    lexical = Path(os.path.abspath(os.fspath(output)))
    normalized = lexical.parent.resolve() / lexical.name
    resolved = lexical.resolve()
    authoritative = AUTHORITATIVE_OUTPUT.parent.resolve() / AUTHORITATIVE_OUTPUT.name
    source_inputs = {
        Path(__file__).resolve(),
        VERIFY_PATH.resolve(),
        (HERE / "build_parameter_transport_certificate.py").resolve(),
        (HERE / "parameter_transport_certificate.json").resolve(),
        *(
            (HERE / filename).resolve()
            for filename in (
                "probe_relation_parameter_transports.jsonl.gz",
                "probe_restriction_parameter_transports.jsonl.gz",
                "restoration_restriction_parameter_transports.jsonl.gz",
            )
        ),
    }
    if lexical.is_symlink():
        raise SystemExit(
            "PARAMETER_TRANSPORT_MUTATION_OUTPUT_POLICY_FAIL: output must not be a symlink"
        )
    if lexical.exists() and any(os.path.samefile(lexical, path) for path in source_inputs):
        raise SystemExit(
            "PARAMETER_TRANSPORT_MUTATION_OUTPUT_POLICY_FAIL: output hardlinks a source input"
        )
    if allow_authoritative_output:
        if normalized != authoritative or lexical.is_symlink():
            raise SystemExit(
                "PARAMETER_TRANSPORT_MUTATION_OUTPUT_POLICY_FAIL: authoritative "
                "override licenses only the nonsymbolic canonical mutation report"
            )
        return normalized
    try:
        resolved.relative_to(PROJECT.resolve())
    except ValueError:
        return normalized
    raise SystemExit(
        "PARAMETER_TRANSPORT_MUTATION_OUTPUT_POLICY_FAIL: routine output must be "
        "outside the project source tree"
    )


def atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o644)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        if temporary.exists():
            temporary.unlink()


def clear_stale_output(path: Path) -> None:
    path.unlink(missing_ok=True)
    require(not path.exists(), f"stale output remains:{path.name}")


def import_path(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"import:{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def rows(path: Path):
    for wrapped in iter_jsonl(path):
        yield wrapped["row"]


def find(path: Path, predicate: Callable[[dict[str, Any]], bool]) -> dict[str, Any]:
    for row in rows(path):
        if predicate(row):
            return row
    raise Failure(f"no mutation exemplar:{path.name}")


def diagnostic_line(output: str, expected: str) -> str | None:
    matches = [line.strip() for line in output.splitlines() if line.strip() == expected]
    require(len(matches) <= 1, f"duplicate diagnostic:{expected}")
    return matches[0] if matches else None


def sanitized_child_output_tail(
    output: str | bytes | None, limit: int = CHILD_OUTPUT_TAIL_LIMIT
) -> str:
    """Return bounded diagnostics without terminal controls or local user paths."""

    require(limit > 0, "invalid child-output tail limit")
    if isinstance(output, bytes):
        text = output.decode("utf-8", errors="replace")
    else:
        text = output or ""
    text = ANSI_ESCAPE.sub("", text)
    text = text.replace(str(PROJECT), "<PROJECT>")
    text = USER_PATH.sub("/Users/<USER>", text)
    text = DARWIN_TEMP_PATH.sub("<TEMP_PATH>", text)
    text = "".join(
        character
        if character in "\n\r\t" or 0x20 <= ord(character) <= 0x7E
        else "?"
        for character in text
    )
    if len(text) > limit:
        text = "<truncated>" + text[-limit:]
    return text or "<empty>"


def classify_unqualified_failure(
    completed: subprocess.CompletedProcess[str], expected: str, observed: str | None
) -> str:
    combined = completed.stdout or ""
    if completed.returncode < 0:
        return f"signal_exit_{-completed.returncode}"
    if completed.returncode == 0:
        return "unexpected_zero_exit"
    if completed.returncode != 1:
        return "unexpected_exit_code"
    if "PARAMETER_TRANSPORT_REPLAY_PASS " in combined:
        return "forbidden_pass_token"
    if "ModuleNotFoundError" in combined or "ImportError:" in combined:
        return "dependency_error"
    if "Traceback (most recent call last):" in combined:
        return "child_exception"
    if "TimeoutExpired" in combined:
        return "reported_timeout"
    if observed != expected:
        return "missing_or_wrong_semantic_diagnostic"
    return "other_unqualified_failure"


def qualifies_production_failure(
    completed: subprocess.CompletedProcess[str], expected: str
) -> tuple[bool, str | None]:
    combined = completed.stdout or ""
    observed = diagnostic_line(combined, expected)
    forbidden = (
        "Traceback (most recent call last):",
        "ModuleNotFoundError",
        "ImportError:",
        "TimeoutExpired",
    )
    qualified = (
        completed.returncode == 1
        and observed == expected
        and not any(marker in combined for marker in forbidden)
        and "PARAMETER_TRANSPORT_REPLAY_PASS " not in combined
    )
    return qualified, observed


def source_fingerprints() -> dict[str, str]:
    paths = {
        Path(__file__).resolve(),
        VERIFY_PATH.resolve(),
        (HERE / "build_parameter_transport_certificate.py").resolve(),
        (HERE / "parameter_transport_certificate.json").resolve(),
        *(HERE / filename for filename in (
            "probe_relation_parameter_transports.jsonl.gz",
            "probe_restriction_parameter_transports.jsonl.gz",
            "restoration_restriction_parameter_transports.jsonl.gz",
        )),
    }
    certificate = load_plain_json(HERE / "parameter_transport_certificate.json")
    paths.update((PROJECT / relative).resolve() for relative in certificate["inputs"])
    return {
        path.relative_to(PROJECT).as_posix(): sha_file(path)
        for path in sorted(paths)
    }


def reseal_certificate(certificate_path: Path, ledger_key: str | None = None) -> dict[str, Any]:
    certificate = load_plain_json(certificate_path)
    for relative in certificate["inputs"]:
        source = PROJECT / relative
        certificate["inputs"][relative] = {
            "bytes": source.stat().st_size,
            "sha256": sha_file(source),
        }
    if ledger_key is not None:
        record = certificate["ledgers"][ledger_key]
        ledger_path = certificate_path.parent / record["path"]
        record["bytes"] = ledger_path.stat().st_size
        record["sha256"] = sha_file(ledger_path)
    certificate.pop("payload_sha256", None)
    certificate["payload_sha256"] = sha(certificate)
    certificate_path.write_bytes(canonical_bytes(certificate) + b"\n")
    return certificate


def copy_clean_certificate_tree(destination: Path) -> dict[str, Any]:
    """Copy the already-qualified authoritative tree without repairing it."""

    destination.mkdir(parents=True, exist_ok=False)
    for filename in (
        "parameter_transport_certificate.json",
        "probe_relation_parameter_transports.jsonl.gz",
        "probe_restriction_parameter_transports.jsonl.gz",
        "restoration_restriction_parameter_transports.jsonl.gz",
    ):
        shutil.copyfile(HERE / filename, destination / filename)
        require(
            sha_file(destination / filename) == sha_file(HERE / filename),
            f"nonidentical authoritative copy:{filename}",
        )
    certificate = load_plain_json(destination / "parameter_transport_certificate.json")
    return certificate


def rewrite_complete_ledger(
    source: Path,
    destination: Path,
    occurrence_id: str,
    mutate: Callable[[dict[str, Any]], None],
    verifier,
) -> dict[str, Any]:
    row_count = 0
    changed = 0
    ordered_root = sha([])
    counts: collections.Counter[str] = collections.Counter()
    raw = destination.open("wb")
    stream = gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0)
    try:
        for wrapped in iter_jsonl(source):
            row = wrapped["row"]
            if row["occurrence_id"] == occurrence_id:
                require(changed == 0, f"duplicate mutation occurrence:{occurrence_id}")
                mutate(row)
                changed += 1
            row_sha256 = sha(row)
            stream.write(canonical_bytes({"row": row, "row_sha256": row_sha256}) + b"\n")
            ordered_root = sha({"previous": ordered_root, "row_sha256": row_sha256})
            counts.update(verifier.action_keys(row))
            row_count += 1
    finally:
        stream.close()
        raw.close()
    require(changed == 1, f"mutation occurrence absent:{occurrence_id}")
    return {
        "rows": row_count,
        "ordered_hash_root": ordered_root,
        "counts": dict(sorted(counts.items())),
        "bytes": destination.stat().st_size,
        "sha256": sha_file(destination),
    }


def invoke_production_verifier(certificate_dir: Path, timeout: float) -> tuple[subprocess.CompletedProcess[str], float]:
    started = time.monotonic()
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                str(VERIFY_PATH),
                "--certificate-dir",
                str(certificate_dir),
            ],
            cwd=PROJECT,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as error:
        tail = sanitized_child_output_tail(error.stdout)
        raise Failure(
            "production verifier child failure:failure_class=timeout:"
            f"child_output_tail={json.dumps(tail)}"
        ) from None
    return completed, time.monotonic() - started


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-authoritative-output", action="store_true")
    parser.add_argument("--timeout-seconds", type=float, default=1200.0)
    args = parser.parse_args()
    require(args.timeout_seconds > 0, "invalid timeout")
    output = validate_output_path(args.output, args.allow_authoritative_output)
    clear_stale_output(output)
    if not __debug__:
        raise SystemExit("PARAMETER_TRANSPORT_MUTATION_OPTIMIZED_MODE_FORBIDDEN")
    before = source_fingerprints()
    verifier = import_path("parameter_transport_mutation_verifier", VERIFY_PATH)
    relation_path = HERE / "probe_relation_parameter_transports.jsonl.gz"
    restriction_path = HERE / "probe_restriction_parameter_transports.jsonl.gz"
    restoration_path = HERE / "restoration_restriction_parameter_transports.jsonl.gz"

    relation_flip = find(
        relation_path,
        lambda row: any(
            action.get("parent_order_reversed") is True
            for action in row["inheritance_actions"]
        ),
    )
    relation_identity = find(
        relation_path,
        lambda row: any(
            action.get("mode") == "affine_parent_transport"
            and action.get("parent_order_reversed") is False
            for action in row["inheritance_actions"]
        ),
    )
    relation_triangle = find(relation_path, lambda row: row["relation"] == "triangle")
    restriction_flip = find(
        restriction_path,
        lambda row: any(action["parent_order_reversed"] for action in row["inheritance_actions"]),
    )
    serial = find(
        restriction_path,
        lambda row: any(len(action["child_rooted_factors"]) > 1 for action in row["edge_actions"]),
    )
    root_suppressed = find(
        restoration_path,
        lambda row: any(
            action.get("root_suppressed_incoming_incidence")
            for action in row["inheritance_actions"]
        ),
    )

    cases: list[dict[str, Any]] = []
    full_verifier_names = {
        "triangle_edge_false_product_map",
        "serial_product_factor_omitted",
        "root_suppressed_incoming_incidence_hidden",
        "source_target_reversal_without_inverse_transport",
    }
    local_expected = {
        "required_complement_removed": "required_complement_removed:flip flag",
        "illicit_complement_injected": "illicit_complement_injected:flip flag",
        "parent_order_reversal_unpaired": "parent_order_reversal_unpaired:flip flag",
        "triangle_reticulation_false_affine_map": (
            "triangle_reticulation_false_affine_map:triangle-local census"
        ),
        "restriction_complement_removed": "restriction_complement_removed:flip flag",
        "paired_s_g_action_broken": "paired_s_g_action_broken:paired products",
    }

    with tempfile.TemporaryDirectory(prefix="k2p-parameter-transport-mutations-") as temporary:
        scratch = Path(temporary)
        # The baseline is deliberately the stored authoritative certificate,
        # not a scratch copy whose input bindings have been silently resealed.
        # Only after this in-place full replay passes do we create disposable
        # mutant copies and coherently reseal those attacks.
        clean_certificate = load_plain_json(
            HERE / "parameter_transport_certificate.json"
        )
        clean_result, clean_runtime = invoke_production_verifier(
            HERE, args.timeout_seconds
        )
        clean_lines = [
            line.strip()
            for line in clean_result.stdout.splitlines()
            if line.startswith("PARAMETER_TRANSPORT_REPLAY_PASS ")
        ]
        require(
            clean_result.returncode == 0
            and len(clean_lines) == 1
            and "Traceback (most recent call last):" not in clean_result.stdout,
            "clean production verifier baseline:\n" + clean_result.stdout[-4000:],
        )

        def rejected(
            name: str,
            clean: dict[str, Any],
            mutate: Callable[[dict[str, Any]], None],
            relation: bool,
            ledger_key: str,
        ) -> None:
            mutant = copy.deepcopy(clean)
            mutate(mutant)
            require(mutant != clean, f"mutation did not change row:{name}")
            clean_row_sha256 = sha(clean)
            mutated_row_sha256 = sha(mutant)
            if name not in full_verifier_names:
                expected = local_expected[name]
                observed = None
                try:
                    if relation:
                        verifier.validate_relation(mutant, name)
                    else:
                        verifier.validate_restriction(mutant, name)
                except verifier.Failure as error:
                    observed = str(error)
                require(observed == expected, f"wrong local diagnostic:{name}:{observed}")
                cases.append({
                    "name": name,
                    "occurrence_id": clean["occurrence_id"],
                    "clean_row_sha256": clean_row_sha256,
                    "mutated_row_sha256": mutated_row_sha256,
                    "test_type": "exact_local_semantic_validator_attack",
                    "complete_mutant_ledger_created": False,
                    "production_verifier_invoked": False,
                    "expected_semantic_diagnostic": expected,
                    "observed_semantic_diagnostic": observed,
                    "semantic_diagnostic_matched": True,
                    "rejected": True,
                    "status": "REJECTED",
                })
                return

            mutant_root = scratch / f"mutant-{len(cases):02d}"
            copy_clean_certificate_tree(mutant_root)
            ledger_filename = verifier.LEDGER_KEYS[ledger_key]
            ledger_path = mutant_root / ledger_filename
            rewritten = mutant_root / f".{ledger_filename}.mutant"
            metadata = rewrite_complete_ledger(
                ledger_path,
                rewritten,
                clean["occurrence_id"],
                mutate,
                verifier,
            )
            os.replace(rewritten, ledger_path)
            certificate_path = mutant_root / "parameter_transport_certificate.json"
            certificate = load_plain_json(certificate_path)
            certificate["ledgers"][ledger_key].update(metadata)
            certificate_path.write_bytes(canonical_bytes(certificate) + b"\n")
            mutant_certificate = reseal_certificate(certificate_path, ledger_key)
            # This proves that all local rows, counts, ordered roots, file
            # hashes, and certificate hashes were coherently resealed.  Only
            # the independent primitive regeneration remains able to reject.
            verifier.validate_directory(mutant_root)
            expected = (
                "PARAMETER_TRANSPORT_REPLAY_FAIL:rederived bytes:"
                "parameter_transport_certificate.json"
            )
            result, runtime = invoke_production_verifier(
                mutant_root, args.timeout_seconds
            )
            qualified, observed = qualifies_production_failure(result, expected)
            failure_class = classify_unqualified_failure(
                result, expected, observed
            )
            tail = sanitized_child_output_tail(result.stdout)
            require(
                qualified,
                "unqualified production rejection:"
                f"{name}:returncode={result.returncode}:observed={observed}:"
                f"failure_class={failure_class}:"
                f"child_output_tail={json.dumps(tail)}",
            )
            cases.append({
                "name": name,
                "occurrence_id": clean["occurrence_id"],
                "clean_row_sha256": clean_row_sha256,
                "mutated_row_sha256": mutated_row_sha256,
                "test_type": "complete_disposable_ledger_and_certificate_attack",
                "complete_mutant_ledger_created": True,
                "complete_mutant_certificate_created": True,
                "complete_mutant_ledger_coherently_resealed": True,
                "mutant_structural_validation_passed": True,
                "full_primitive_regeneration_invoked": True,
                "mutated_ledger_key": ledger_key,
                "mutated_ledger_bytes": metadata["bytes"],
                "mutated_ledger_sha256": metadata["sha256"],
                "mutated_certificate_payload_sha256": mutant_certificate["payload_sha256"],
                "production_verifier_invoked": True,
                "production_verifier_sha256": sha_file(VERIFY_PATH),
                "verifier_exit_code": result.returncode,
                "expected_semantic_diagnostic": expected,
                "observed_semantic_diagnostic": observed,
                "semantic_diagnostic_matched": True,
                "success_token_observed": False,
                "traceback_observed": False,
                "rejected": True,
                "status": "REJECTED",
            })
            print(f"PARAMETER_TRANSPORT_MUTATION_CASE_PASS:{name}:seconds={runtime:.3f}", flush=True)

        def remove_required_complement(row):
            action = next(item for item in row["inheritance_actions"] if item.get("parent_order_reversed"))
            action["parent_order_reversed"] = False
            action["target_lambda_from_source"] = "lambda"

        rejected("required_complement_removed", relation_flip, remove_required_complement, True, "probe_relations")

        def inject_illicit_complement(row):
            action = next(
                item for item in row["inheritance_actions"]
                if item.get("mode") == "affine_parent_transport" and not item["parent_order_reversed"]
            )
            action["parent_order_reversed"] = True
            action["target_lambda_from_source"] = "one_minus_lambda"

        rejected("illicit_complement_injected", relation_identity, inject_illicit_complement, True, "probe_relations")

        def reverse_parent_order_without_complement(row):
            action = next(item for item in row["inheritance_actions"] if item.get("parent_order_reversed"))
            action["source_parent_index_to_target_parent_index"] = [0, 1]

        rejected("parent_order_reversal_unpaired", relation_flip, reverse_parent_order_without_complement, True, "probe_relations")

        def triangle_given_affine_map(row):
            action = next(item for item in row["inheritance_actions"] if item["mode"] == "ordinary_triangle_local_section")
            action.update({
                "mode": "affine_parent_transport",
                "source_parent_index_to_target_parent_index": [0, 1],
                "parent_order_reversed": False,
                "target_lambda_from_source": "lambda",
                "source_lambda_parent_index": 1,
                "target_lambda_parent_index": 1,
                "source_ordered_parents": ["mutant_parent_0", "mutant_parent_1"],
                "target_ordered_parents": ["mutant_parent_0", "mutant_parent_1"],
            })

        rejected("triangle_reticulation_false_affine_map", relation_triangle, triangle_given_affine_map, True, "probe_relations")

        def triangle_edge_promoted_to_product(row):
            action = next(item for item in row["edge_actions"] if item["mode"] == "ordinary_triangle_local_section")
            action["mode"] = "paired_K2P_product"
            action["s_action"] = action["g_action"] = "match_products"

        rejected("triangle_edge_false_product_map", relation_triangle, triangle_edge_promoted_to_product, True, "probe_relations")

        def restriction_flip_removed(row):
            action = next(item for item in row["inheritance_actions"] if item["parent_order_reversed"])
            action["parent_order_reversed"] = False
            action["parent_lambda_from_child"] = "lambda"

        rejected("restriction_complement_removed", restriction_flip, restriction_flip_removed, False, "probe_restrictions")

        def omit_serial_factor(row):
            action = next(item for item in row["edge_actions"] if len(item["child_rooted_factors"]) > 1)
            action["child_rooted_factors"].pop()

        rejected("serial_product_factor_omitted", serial, omit_serial_factor, False, "probe_restrictions")

        def break_paired_sector_action(row):
            row["edge_actions"][0]["parent_g_from_child"] = "identity"

        rejected("paired_s_g_action_broken", serial, break_paired_sector_action, False, "probe_restrictions")

        def hide_root_suppressed_incidence(row):
            action = next(item for item in row["inheritance_actions"] if item["root_suppressed_incoming_incidence"])
            action["root_suppressed_incoming_incidence"] = False

        rejected("root_suppressed_incoming_incidence_hidden", root_suppressed, hide_root_suppressed_incidence, False, "restoration_restrictions")

        def swap_directed_relation_without_inverse(row):
            row["source_graph_sha256"], row["target_graph_sha256"] = (
                row["target_graph_sha256"], row["source_graph_sha256"]
            )

        rejected("source_target_reversal_without_inverse_transport", relation_flip, swap_directed_relation_without_inverse, True, "probe_relations")

        wrong = subprocess.CompletedProcess(
            args=[], returncode=1, stdout="PARAMETER_TRANSPORT_REPLAY_FAIL:wrong semantic gate\n"
        )
        crash = subprocess.run(
            [sys.executable, "-B", "-c", "raise RuntimeError('unrelated crash control')"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        expected_control = "PARAMETER_TRANSPORT_REPLAY_FAIL:rederived bytes:control.jsonl.gz"
        signal = subprocess.CompletedProcess(
            args=[], returncode=-9, stdout=expected_control + "\n"
        )
        non_one = subprocess.CompletedProcess(
            args=[], returncode=2, stdout=expected_control + "\n"
        )
        pass_token = subprocess.CompletedProcess(
            args=[],
            returncode=1,
            stdout=(
                expected_control
                + "\nPARAMETER_TRANSPORT_REPLAY_PASS {\"mutant\":true}\n"
            ),
        )
        stale_control = scratch / "stale-pass-report.json"
        stale_control.write_text('{"status":"PASS"}\n')
        clear_stale_output(stale_control)
        timeout_rejected = False
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
            timeout_rejected = True
        require(timeout_rejected, "timeout control did not time out")
        optimized_output = scratch / "optimized-stale-pass-report.json"
        optimized_output.write_text('{"status":"PASS"}\n')
        optimized = subprocess.run(
            [
                sys.executable,
                "-O",
                "-B",
                str(Path(__file__).resolve()),
                "--output",
                str(optimized_output),
            ],
            cwd=PROJECT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        require(
            optimized.returncode == 1
            and optimized.stdout.strip()
            == "PARAMETER_TRANSPORT_MUTATION_OPTIMIZED_MODE_FORBIDDEN"
            and not optimized_output.exists(),
            "optimized stale-output control",
        )
        require(not qualifies_production_failure(wrong, expected_control)[0], "wrong diagnostic qualified")
        require(not qualifies_production_failure(crash, expected_control)[0], "unrelated crash qualified")
        require(not qualifies_production_failure(signal, expected_control)[0], "signal exit qualified")
        require(not qualifies_production_failure(non_one, expected_control)[0], "non-one exit qualified")
        require(not qualifies_production_failure(pass_token, expected_control)[0], "PASS token output qualified")
        require(not stale_control.exists(), "stale PASS output survived")
        require(len(cases) == 10 and all(row["status"] == "REJECTED" for row in cases), "mutation census")
        after = source_fingerprints()
        require(before == after, "source fingerprint drift")
    report = {
        "schema": "k2p_parameter_transport_mutations_v2",
        "status": "PASS",
        "certificate_payload_sha256": clean_certificate["payload_sha256"],
        "production_verifier_sha256": sha_file(VERIFY_PATH),
        "mutation_runner_sha256": sha_file(Path(__file__)),
        "clean_baseline": {
            "authoritative_certificate_verified_in_place": True,
            "authoritative_certificate_unmodified": True,
            "authoritative_certificate_file_sha256": sha_file(
                HERE / "parameter_transport_certificate.json"
            ),
            "authoritative_certificate_payload_sha256": clean_certificate[
                "payload_sha256"
            ],
            "authoritative_input_binding_count": len(clean_certificate["inputs"]),
            "authoritative_input_bindings_current": True,
            "authoritative_ledger_count": len(clean_certificate["ledgers"]),
            "production_verifier_invoked": True,
            "verifier_exit_code": clean_result.returncode,
            "full_primitive_regeneration": True,
            "pass_token_count": len(clean_lines),
            "status": "PASS",
        },
        "cases": cases,
        "rejected": len(cases),
        "survived": 0,
        "complete_production_verifier_attacks": len(full_verifier_names),
        "exact_local_semantic_attacks": len(cases) - len(full_verifier_names),
        "qualification_negative_controls": {
            "wrong_diagnostic_not_qualified": True,
            "unrelated_traceback_not_qualified": True,
            "signal_or_non_one_exit_not_qualified": True,
            "timeout_not_qualified": True,
            "failure_output_with_pass_token_not_qualified": True,
            "stale_pass_output_removed_before_work": True,
            "optimized_mode_stale_pass_removed_before_rejection": True,
        },
        "source_fingerprints_unchanged": True,
    }
    report["payload_sha256"] = sha(report)
    atomic_write_bytes(output, canonical_bytes(report) + b"\n")
    print(
        "PARAMETER_TRANSPORT_MUTATIONS_PASS "
        + json.dumps({"rejected": len(cases), "survived": 0, "payload_sha256": report["payload_sha256"]}, sort_keys=True)
    )


if __name__ == "__main__":
    try:
        main()
    except Failure as error:
        print(f"PARAMETER_TRANSPORT_MUTATIONS_FAIL:{error}", file=sys.stderr)
        raise SystemExit(1)
