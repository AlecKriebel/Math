#!/usr/bin/env python3
"""Pinned Glucose3 certification with a streaming, compressed LRAT trace.

The ordinary certification pipeline materializes the generated LRAT file
before replaying it.  Large local-radius instances can make that temporary
file several gigabytes.  This variant sends drat-trim's LRAT output through a
FIFO into zstd, then streams the archive through lrat-check.  The checker
therefore sees the exact uncompressed LRAT byte stream while only the
compressed representation is retained.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
import tempfile
import threading
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from residual_completion import (  # noqa: E402
    DEFAULT_DRAT_TRIM,
    DEFAULT_LRAT_CHECK,
    DEFAULT_PYSAT_PATH,
    DEFAULT_PYTHON,
    PINNED_HASHES,
    PINNED_PYSAT_VERSION,
    Toolchain,
    WorkflowError,
    parse_single_json_line,
    run_bounded,
    sha256_file,
    verify_toolchain,
    write_json,
)


PIPELINE_ID = "ramsey55_pinned_glucose_streaming_zstd_lrat_pipeline_v1"
CHUNK_BYTES = 1 << 20
PINNED_ZSTD_SHA256 = (
    "aff8169fb421bb925fb16c44a7e0143fa2c7a941dc45cce76b15062a2ce54917"
)
WORKER_ID = "ramsey55_pysat_glucose3_proof_worker_v1"


def checker_says_verified(output: str) -> bool:
    return any(
        line.strip() in {"s VERIFIED", "c VERIFIED"} for line in output.splitlines()
    )


def paths_alias(left: Path, right: Path) -> bool:
    if left.resolve() == right.resolve():
        return True
    try:
        return left.exists() and right.exists() and os.path.samefile(left, right)
    except OSError:
        return False


def validate_output_paths(outputs: tuple[Path, ...], protected: tuple[Path, ...]) -> None:
    for index, left in enumerate(outputs):
        if any(paths_alias(left, right) for right in outputs[index + 1 :]):
            raise WorkflowError("proof, compressed LRAT, and result paths must differ")
        if any(paths_alias(left, source) for source in protected):
            raise WorkflowError(f"output path aliases a protected input: {left}")


def dimacs_model_satisfies(
    path: Path, true_variables: Any
) -> tuple[bool, int, int]:
    if (
        not isinstance(true_variables, list)
        or any(type(variable) is not int for variable in true_variables)
        or true_variables != sorted(set(true_variables))
    ):
        raise WorkflowError("SAT worker true_variables is not a sorted unique list")
    true_set = set(true_variables)
    variable_count: int | None = None
    declared_clauses: int | None = None
    observed_clauses = 0
    clause_satisfied = False
    pending_literals = False
    try:
        with path.open("r", encoding="ascii") as stream:
            for line_number, raw in enumerate(stream, start=1):
                fields = raw.split()
                if not fields or fields[0] == "c":
                    continue
                if fields[0] == "p":
                    if (
                        variable_count is not None
                        or pending_literals
                        or len(fields) != 4
                        or fields[1] != "cnf"
                    ):
                        raise WorkflowError(
                            f"invalid DIMACS header at line {line_number}"
                        )
                    variable_count = int(fields[2])
                    declared_clauses = int(fields[3])
                    if variable_count < 0 or declared_clauses < 0:
                        raise WorkflowError("negative DIMACS header count")
                    continue
                if variable_count is None:
                    raise WorkflowError(
                        f"DIMACS clause precedes header at line {line_number}"
                    )
                for field in fields:
                    literal = int(field)
                    if literal == 0:
                        observed_clauses += 1
                        if not clause_satisfied:
                            return False, variable_count, observed_clauses
                        clause_satisfied = False
                        pending_literals = False
                        continue
                    if not 1 <= abs(literal) <= variable_count:
                        raise WorkflowError(
                            f"DIMACS literal is out of range at line {line_number}"
                        )
                    pending_literals = True
                    clause_satisfied = clause_satisfied or (
                        (literal > 0) == (abs(literal) in true_set)
                    )
    except (OSError, UnicodeError, ValueError) as error:
        if isinstance(error, WorkflowError):
            raise
        raise WorkflowError(f"failed to check SAT model: {error}") from error
    if (
        variable_count is None
        or declared_clauses is None
        or pending_literals
        or observed_clauses != declared_clauses
        or any(not 1 <= variable <= variable_count for variable in true_set)
    ):
        raise WorkflowError("SAT model check found malformed DIMACS or variable list")
    return True, variable_count, observed_clauses


def _compress_fifo(
    fifo: Path,
    archive: Path,
    zstd: Path,
    timeout: float,
    opened: threading.Event,
    result: dict[str, Any],
) -> None:
    try:
        with fifo.open("rb", buffering=0) as source:
            opened.set()
            with archive.open("wb") as target:
                completed = subprocess.run(
                    [str(zstd), "-T1", "-3", "-q"],
                    stdin=source,
                    stdout=target,
                    stderr=subprocess.PIPE,
                    check=False,
                    timeout=timeout,
                )
        result.update(
            {
                "returncode": completed.returncode,
                "stderr": completed.stderr.decode("utf-8", errors="replace"),
            }
        )
    except BaseException as error:  # propagated to the main thread below
        result["exception"] = repr(error)
        opened.set()


def _decompress_fifo_and_hash(
    archive: Path,
    fifo: Path,
    zstd: Path,
    opened: threading.Event,
    result: dict[str, Any],
) -> None:
    digest = hashlib.sha256()
    byte_count = 0
    process: subprocess.Popen[bytes] | None = None
    try:
        process = subprocess.Popen(
            [str(zstd), "-d", "-c", "-q", str(archive)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        result["_process"] = process
        assert process.stdout is not None
        with fifo.open("wb", buffering=0) as target:
            opened.set()
            while True:
                block = process.stdout.read(CHUNK_BYTES)
                if not block:
                    break
                digest.update(block)
                byte_count += len(block)
                target.write(block)
        stderr = process.stderr.read() if process.stderr is not None else b""
        returncode = process.wait()
        result.update(
            {
                "returncode": returncode,
                "stderr": stderr.decode("utf-8", errors="replace"),
                "sha256": digest.hexdigest(),
                "bytes": byte_count,
            }
        )
    except BaseException as error:  # propagated to the main thread below
        result["exception"] = repr(error)
        opened.set()
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
    finally:
        result.pop("_process", None)


def _fifo_guard(fifo: Path) -> int:
    return os.open(fifo, os.O_RDWR | os.O_NONBLOCK)


def _stop_worker_process(result: dict[str, Any]) -> None:
    process = result.get("_process")
    if isinstance(process, subprocess.Popen) and process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def _join_worker(
    worker: threading.Thread,
    result: dict[str, Any],
    *,
    timeout: float,
    label: str,
    require_success: bool = True,
) -> bool:
    worker.join(timeout)
    if worker.is_alive():
        _stop_worker_process(result)
        worker.join(5)
        raise WorkflowError(f"{label} worker exceeded its time limit")
    succeeded = "exception" not in result and result.get("returncode") == 0
    if require_success and "exception" in result:
        raise WorkflowError(f"{label} worker failed: {result['exception']}")
    if require_success and result.get("returncode") != 0:
        raise WorkflowError(
            f"{label} worker returned {result.get('returncode')}: "
            f"{result.get('stderr', '')}"
        )
    return succeeded


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--proof", type=Path, required=True)
    parser.add_argument("--lrat-zst", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=600.0)
    parser.add_argument("--proof-check-time-limit", type=float, default=1200.0)
    parser.add_argument("--python", type=Path, default=DEFAULT_PYTHON)
    parser.add_argument("--pysat-path", type=Path, default=DEFAULT_PYSAT_PATH)
    parser.add_argument("--drat-trim", type=Path, default=DEFAULT_DRAT_TRIM)
    parser.add_argument("--lrat-check", type=Path, default=DEFAULT_LRAT_CHECK)
    parser.add_argument("--zstd", type=Path, default=Path("/opt/homebrew/bin/zstd"))
    args = parser.parse_args()
    if (
        args.time_limit <= 0
        or args.proof_check_time_limit <= 0
        or not math.isfinite(args.time_limit)
        or not math.isfinite(args.proof_check_time_limit)
    ):
        raise WorkflowError("time limits must be finite and positive")
    if not args.cnf.is_file():
        raise WorkflowError(f"CNF is missing: {args.cnf}")
    if not args.zstd.is_file():
        raise WorkflowError(f"zstd is missing: {args.zstd}")
    worker_path = ROOT / "src" / "residual_completion_glucose.py"
    helper_path = ROOT / "src" / "residual_completion.py"
    validate_output_paths(
        (args.proof, args.lrat_zst, args.result),
        (
            args.cnf,
            args.zstd,
            args.python,
            args.drat_trim,
            args.lrat_check,
            worker_path,
            helper_path,
            Path(__file__),
        ),
    )

    toolchain = Toolchain(
        args.python,
        args.pysat_path,
        args.drat_trim,
        args.lrat_check,
        PINNED_HASHES,
    )
    tool_metadata = verify_toolchain(toolchain)
    tool_metadata["zstd_path"] = str(args.zstd)
    zstd_sha256 = sha256_file(args.zstd)
    if zstd_sha256 != PINNED_ZSTD_SHA256:
        raise WorkflowError(
            f"pinned zstd hash mismatch: {zstd_sha256} != {PINNED_ZSTD_SHA256}"
        )
    tool_metadata["sha256"]["zstd"] = zstd_sha256
    tool_metadata["pipeline_sources"] = {
        "streaming_pipeline": sha256_file(Path(__file__)),
        "solver_worker": sha256_file(worker_path),
        "workflow_helpers": sha256_file(helper_path),
    }

    cnf_sha256 = sha256_file(args.cnf)
    args.proof.parent.mkdir(parents=True, exist_ok=True)
    args.lrat_zst.parent.mkdir(parents=True, exist_ok=True)
    args.proof.unlink(missing_ok=True)
    args.lrat_zst.unlink(missing_ok=True)
    environment = os.environ.copy()
    environment.update(
        {
            "PYTHONPATH": str(toolchain.pysat_path),
            "PYTHONHASHSEED": "0",
            "LC_ALL": "C",
        }
    )
    state, solved, solve_wall = run_bounded(
        (
            str(toolchain.python),
            str(worker_path),
            str(args.cnf),
            "--proof",
            str(args.proof),
        ),
        timeout=args.time_limit,
        environment=environment,
    )
    base = {
        "pipeline": PIPELINE_ID,
        "cnf_path": str(args.cnf.resolve()),
        "cnf_sha256": cnf_sha256,
        "time_limit_seconds": args.time_limit,
        "proof_check_time_limit_seconds": args.proof_check_time_limit,
        "toolchain": tool_metadata,
        "solver_wall_seconds": solve_wall,
    }
    if state == "TIMEOUT":
        args.proof.unlink(missing_ok=True)
        args.lrat_zst.unlink(missing_ok=True)
        result = {
            **base,
            "status": "TIMEOUT",
            "proof_written": False,
            "lrat_zst_written": False,
        }
        write_json(args.result, result)
        print(json.dumps(result, sort_keys=True))
        return 2

    assert solved is not None
    if solved.returncode not in {10, 20}:
        raise WorkflowError(
            f"Glucose worker failed ({solved.returncode}): {solved.stderr}"
        )
    solver_result = parse_single_json_line(solved.stdout)
    if (
        solver_result.get("cnf_sha256") != cnf_sha256
        or solver_result.get("pysat_version") != PINNED_PYSAT_VERSION
        or solver_result.get("worker") != WORKER_ID
        or solver_result.get("solver") != "Glucose3"
    ):
        raise WorkflowError("worker runtime or CNF fingerprint mismatch")
    if solved.returncode == 10:
        if (
            solver_result.get("status") != "SAT"
            or solver_result.get("proof_written") is not False
        ):
            raise WorkflowError("SAT worker status fields are inconsistent")
        model_valid, variable_count, clause_count = dimacs_model_satisfies(
            args.cnf, solver_result.get("true_variables")
        )
        if (
            not model_valid
            or solver_result.get("variable_count") != variable_count
            or solver_result.get("clause_count") != clause_count
            or sha256_file(args.cnf) != cnf_sha256
        ):
            raise WorkflowError("SAT model or CNF stability check failed")
        result = {
            **base,
            "status": "SAT",
            "solver_result": solver_result,
            "true_variables": solver_result["true_variables"],
            "model_valid": True,
            "model_check": "streaming_dimacs_clause_replay_v1",
            "proof_written": False,
            "lrat_zst_written": False,
        }
        write_json(args.result, result)
        print(json.dumps(result, sort_keys=True))
        return 10

    if (
        solver_result.get("status") != "UNSAT"
        or solver_result.get("proof_written") is not True
    ):
        raise WorkflowError("UNSAT worker status fields are inconsistent")
    if not args.proof.is_file():
        raise WorkflowError("UNSAT worker produced no proof file")
    proof_sha256 = sha256_file(args.proof)
    if (
        solver_result.get("proof_sha256") != proof_sha256
        or solver_result.get("proof_bytes") != args.proof.stat().st_size
        or Path(str(solver_result.get("proof_path"))).resolve() != args.proof.resolve()
    ):
        raise WorkflowError("worker proof hash mismatch")

    with tempfile.TemporaryDirectory(prefix="ramsey55-stream-lrat.") as directory:
        temporary = Path(directory)
        lrat_write_fifo = temporary / "lrat-write.fifo"
        os.mkfifo(lrat_write_fifo)
        compression: dict[str, Any] = {}
        lrat_write_guard = _fifo_guard(lrat_write_fifo)
        compression_opened = threading.Event()
        compressor = threading.Thread(
            target=_compress_fifo,
            args=(
                lrat_write_fifo,
                args.lrat_zst,
                args.zstd,
                args.proof_check_time_limit,
                compression_opened,
                compression,
            ),
            daemon=True,
        )
        compressor.start()
        if not compression_opened.wait(min(10.0, args.proof_check_time_limit)):
            os.close(lrat_write_guard)
            compressor.join(5)
            raise WorkflowError("LRAT compression worker did not open its FIFO")
        if "exception" in compression:
            os.close(lrat_write_guard)
            _join_worker(
                compressor,
                compression,
                timeout=min(10.0, args.proof_check_time_limit),
                label="LRAT compression",
            )
        drat_launch_error: OSError | None = None
        try:
            drat_state, drat, drat_wall = run_bounded(
                (
                    str(toolchain.drat_trim),
                    str(args.cnf),
                    str(args.proof),
                    "-I",
                    "-L",
                    str(lrat_write_fifo),
                ),
                timeout=args.proof_check_time_limit,
            )
        except OSError as error:
            drat_launch_error = error
            drat_state, drat, drat_wall = "ERROR", None, None
        finally:
            os.close(lrat_write_guard)
        compression_ok = _join_worker(
            compressor,
            compression,
            timeout=args.proof_check_time_limit,
            label="LRAT compression",
            require_success=False,
        )
        if drat_launch_error is not None:
            raise WorkflowError(
                f"failed to launch drat-trim: {drat_launch_error}"
            ) from drat_launch_error
        drat_valid = (
            drat_state == "COMPLETED"
            and drat is not None
            and drat.returncode == 0
            and checker_says_verified(drat.stdout + drat.stderr)
            and compression_ok
            and args.lrat_zst.is_file()
        )

        lrat = None
        lrat_state = None
        lrat_wall = None
        lrat_valid = False
        replay: dict[str, Any] = {}
        archive_sha256_before_replay = None
        if drat_valid and args.lrat_zst.is_file():
            archive_sha256_before_replay = sha256_file(args.lrat_zst)
            lrat_read_fifo = temporary / "lrat-read.fifo"
            os.mkfifo(lrat_read_fifo)
            lrat_read_guard = _fifo_guard(lrat_read_fifo)
            replay_opened = threading.Event()
            decompressor = threading.Thread(
                target=_decompress_fifo_and_hash,
                args=(
                    args.lrat_zst,
                    lrat_read_fifo,
                    args.zstd,
                    replay_opened,
                    replay,
                ),
                daemon=True,
            )
            decompressor.start()
            if not replay_opened.wait(min(10.0, args.proof_check_time_limit)):
                os.close(lrat_read_guard)
                _stop_worker_process(replay)
                decompressor.join(5)
                raise WorkflowError("LRAT replay worker did not open its FIFO")
            replay_reader_guard = os.open(
                lrat_read_fifo, os.O_RDONLY | os.O_NONBLOCK
            )
            os.close(lrat_read_guard)
            if "exception" in replay:
                os.close(replay_reader_guard)
                _join_worker(
                    decompressor,
                    replay,
                    timeout=min(10.0, args.proof_check_time_limit),
                    label="LRAT replay decompression",
                )
            lrat_launch_error: OSError | None = None
            try:
                lrat_state, lrat, lrat_wall = run_bounded(
                    (
                        str(toolchain.lrat_check),
                        str(args.cnf),
                        str(lrat_read_fifo),
                    ),
                    timeout=args.proof_check_time_limit,
                )
            except OSError as error:
                lrat_launch_error = error
                lrat_state, lrat, lrat_wall = "ERROR", None, None
            finally:
                os.close(replay_reader_guard)
            if lrat_state in {"TIMEOUT", "ERROR"}:
                _stop_worker_process(replay)
            replay_transport_ok = _join_worker(
                decompressor,
                replay,
                timeout=args.proof_check_time_limit,
                label="LRAT replay decompression",
                require_success=False,
            )
            if lrat_launch_error is not None:
                raise WorkflowError(
                    f"failed to launch lrat-check: {lrat_launch_error}"
                ) from lrat_launch_error
            lrat_valid = (
                lrat_state == "COMPLETED"
                and lrat is not None
                and lrat.returncode == 0
                and checker_says_verified(lrat.stdout + lrat.stderr)
                and replay_transport_ok
            )

    current_cnf_sha256 = sha256_file(args.cnf)
    current_proof_sha256 = sha256_file(args.proof) if args.proof.is_file() else None
    current_archive_sha256 = (
        sha256_file(args.lrat_zst) if args.lrat_zst.is_file() else None
    )
    artifact_inputs_stable = (
        current_cnf_sha256 == cnf_sha256
        and current_proof_sha256 == proof_sha256
        and (
            archive_sha256_before_replay is None
            or current_archive_sha256 == archive_sha256_before_replay
        )
    )
    status = (
        "CERTIFIED_UNSAT"
        if drat_valid and lrat_valid and artifact_inputs_stable
        else "UNSAT_UNCERTIFIED"
    )
    result = {
        **base,
        "status": status,
        "solver_result": solver_result,
        "proof_written": args.proof.is_file(),
        "proof_path": str(args.proof.resolve()),
        "proof_sha256": current_proof_sha256,
        "solver_proof_sha256": proof_sha256,
        "proof_bytes": args.proof.stat().st_size if args.proof.is_file() else None,
        "artifact_inputs_stable": artifact_inputs_stable,
        "cnf_sha256_after_checks": current_cnf_sha256,
        "drat_trim_valid": drat_valid,
        "drat_trim_state": drat_state,
        "lrat_compression": compression,
        "drat_trim_wall_seconds": drat_wall,
        "drat_trim_returncode": drat.returncode if drat is not None else None,
        "drat_trim_stdout": drat.stdout if drat is not None else None,
        "drat_trim_stderr": drat.stderr if drat is not None else None,
        "lrat_zst_written": args.lrat_zst.is_file(),
        "lrat_zst_path": str(args.lrat_zst.resolve()),
        "lrat_zst_sha256": current_archive_sha256,
        "lrat_zst_sha256_before_replay": archive_sha256_before_replay,
        "lrat_zst_bytes": (
            args.lrat_zst.stat().st_size if args.lrat_zst.is_file() else None
        ),
        "lrat_uncompressed_sha256": replay.get("sha256"),
        "lrat_uncompressed_bytes": replay.get("bytes"),
        "lrat_check_valid": lrat_valid,
        "lrat_check_state": lrat_state,
        "lrat_replay_transport": replay,
        "lrat_check_wall_seconds": lrat_wall,
        "lrat_check_returncode": lrat.returncode if lrat is not None else None,
        "lrat_check_stdout": lrat.stdout if lrat is not None else None,
        "lrat_check_stderr": lrat.stderr if lrat is not None else None,
    }
    write_json(args.result, result)
    print(json.dumps(result, sort_keys=True))
    return 20 if status == "CERTIFIED_UNSAT" else 3


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except WorkflowError as error:
        print(
            json.dumps(
                {"pipeline": PIPELINE_ID, "status": "ERROR", "error": str(error)},
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        raise SystemExit(1)
