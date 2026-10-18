#!/usr/bin/env python3
"""Replay diagnostic durability checks without overwriting saved artifacts.

Default: print the execution record to stdout. Optional output paths use
exclusive creation. The CHECKS.py subprocesses have deterministic stdout;
actual start/end UTC observations belong only to this separate execution record.
"""
import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
CHECKER = HERE / "CHECKS.py"
INITIAL = HERE.parent / "corner_cohomology_adversary"
SENTINEL = "RuntimeError: intentional false sentinel: explicit validation must fail in every optimization mode"

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def utc():
    return datetime.now(timezone.utc).isoformat()

def digest(data):
    return hashlib.sha256(data).hexdigest()

def verify_initial_seal():
    binding = json.loads((HERE / "INPUT_BINDING.json").read_text())
    for item in binding["inputs"]:
        path = HERE / item["relative_path"]
        data = path.read_bytes()
        require(len(data) == item["bytes"], "initial binding byte-size mismatch: " + item["relative_path"])
        require(digest(data) == item["sha256"], "initial binding SHA256 mismatch: " + item["relative_path"])
    manifest = json.loads((INITIAL / "OUTPUT_MANIFEST.json").read_text())
    for item in manifest["files"]:
        data = (INITIAL / item["relative_path"]).read_bytes()
        require(len(data) == item["bytes"], "initial manifest byte-size mismatch: " + item["relative_path"])
        require(digest(data) == item["sha256"], "initial manifest SHA256 mismatch: " + item["relative_path"])
    return True

def run(mode, extra=()):
    command = [sys.executable, *mode, str(CHECKER), *map(str, extra)]
    started = utc()
    completed = subprocess.run(command, capture_output=True)
    ended = utc()
    record = dict(mode="normal" if not mode else mode[0],
                  arguments=list(map(str, extra)),
                  started_at_utc=started, ended_at_utc=ended,
                  returncode=completed.returncode,
                  stdout_bytes=len(completed.stdout),
                  stdout_sha256=digest(completed.stdout),
                  stderr_bytes=len(completed.stderr),
                  stderr_sha256=digest(completed.stderr))
    return completed, record

def save_new(path, payload):
    with path.open("x", encoding="utf-8") as output:
        output.write(payload)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", type=Path,
                        help="optional explicitly selected NEW execution-record path")
    parser.add_argument("--deterministic-output", type=Path,
                        help="optional explicitly selected NEW deterministic-result path")
    args = parser.parse_args()
    started = utc()
    require(verify_initial_seal(), "initial seal verification failed")
    checker_bytes = CHECKER.read_bytes()
    syntax = ast.parse(checker_bytes)
    require(not any(isinstance(node, ast.Assert) for node in ast.walk(syntax)),
            "revised checker still contains an optimization-sensitive validation statement")
    records = []
    outputs = []
    modes = ((), ("-O",), ("-OO",))
    for mode in modes:
        completed, record = run(mode)
        require(completed.returncode == 0, "positive checker run failed in " + record["mode"])
        require(completed.stderr == b"", "positive checker run produced stderr in " + record["mode"])
        parsed = json.loads(completed.stdout)
        require(parsed.get("all_passed") is True, "checker result did not report successful finite checks")
        outputs.append(completed.stdout)
        record["purpose"] = "positive finite checks"
        records.append(record)
    require(outputs[0] == outputs[1] == outputs[2],
            "normal, -O and -OO checker outputs are not byte-identical")
    deterministic = json.loads(outputs[0])
    require("checked_at_utc" not in deterministic,
            "nondeterministic execution timestamp leaked into the deterministic result")
    historical = json.loads((INITIAL / "CHECK_RESULTS.json").read_text())
    historical.pop("checked_at_utc", None)
    require(deterministic == historical,
            "revised finite mathematical results differ from the historical normal-mode results")
    for mode in modes:
        completed, record = run(mode, ("--false-sentinel",))
        require(completed.returncode != 0, "false sentinel was skipped in " + record["mode"])
        require(SENTINEL.encode() in completed.stderr,
                "false sentinel failed for an unexpected reason in " + record["mode"])
        require(completed.stdout == b"", "false sentinel emitted a positive result")
        record["purpose"] = "intentional false validation sentinel"
        record["expected_error_last_line"] = SENTINEL
        record["expected_failure_observed"] = True
        records.append(record)
    # All temporary mutation stays in this detached folder and is removed.
    with tempfile.TemporaryDirectory(prefix=".validation-temporary-", dir=HERE) as td:
        path = Path(td) / "explicit-new-result.json"
        completed, record = run((), ("--output", path))
        require(completed.returncode == 0, "explicit new output path failed")
        require(path.read_bytes() == outputs[0], "explicit output file differs from deterministic stdout")
        require(completed.stdout == outputs[0], "explicit output run changed deterministic stdout")
        record["arguments"] = ["--output", "<temporary explicit new path>"]
        record["purpose"] = "explicit new output path"
        records.append(record)
        before = path.read_bytes()
        completed, record = run((), ("--output", path))
        require(completed.returncode != 0, "existing output file was not refused")
        require(b"FileExistsError" in completed.stderr,
                "existing output refusal failed for an unexpected reason")
        require(path.read_bytes() == before, "existing output file was modified")
        record["arguments"] = ["--output", "<same existing temporary path>"]
        record["purpose"] = "existing output file refusal"
        record["expected_failure_observed"] = True
        record["existing_file_preserved"] = True
        records.append(record)
    require(verify_initial_seal(), "initial seal verification failed after replay")
    result = dict(started_at_utc=started, ended_at_utc=utc(),
                  checker_relative_path="CHECKS.py", checker_bytes=len(checker_bytes),
                  checker_sha256=digest(checker_bytes),
                  python_executable=sys.executable, python_version=sys.version,
                  deterministic_stdout_bytes=len(outputs[0]),
                  deterministic_stdout_sha256=digest(outputs[0]),
                  positive_outputs_byte_identical=True,
                  false_sentinel_rejected_in_all_modes=True,
                  no_optimization_sensitive_validation_statements=True,
                  initial_seal_verified_before_and_after=True,
                  historical_normal_result_matches=True,
                  scope="detached tooling revision; initial run remains historical normal-mode evidence only",
                  runs=records)
    if args.deterministic_output is not None:
        save_new(args.deterministic_output, outputs[0].decode())
    record_payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.record is not None:
        save_new(args.record, record_payload)
    print(record_payload, end="")

if __name__ == "__main__":
    main()
