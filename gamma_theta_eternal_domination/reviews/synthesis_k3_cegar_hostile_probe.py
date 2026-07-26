#!/usr/bin/env python3
"""Independent hostile probes for the proof-producing k=3 CEGAR runner.

This is an audit aid, not a search driver.  It creates only temporary,
one-cut smoke runs, mutates copied checkpoint metadata in place, restores the
original bytes after every mutation, and removes all temporary artifacts.
"""

from __future__ import annotations

import copy
from dataclasses import asdict
from itertools import combinations
import gzip
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
from unittest import mock

from synthesis_k3.cegar import (
    AuditInstrumentation,
    CampaignHeavyChildLock,
    CANDIDATE_MARKER_NAME,
    CHECKPOINT_NAME,
    DRAT_TRIM_BINARY_SHA256,
    RunLock,
    UNSAT_MARKER_NAME,
    _history_chain_step,
    atomic_write,
    audit_run,
    build_configuration,
    canonical_json_bytes,
    parse_dimacs_file,
    parse_solver_result_bytes,
    run_bounded_child,
    run_cegar,
    run_unsat_proof_replay,
    runtime_source_manifest,
    sha256_bytes,
    sha256_file,
    source_set_sha256,
    strict_json_file,
    verify_stored_drat_certificate,
)
from synthesis_k3.encoding import build_k3_encoding


ROOT = Path(__file__).resolve().parents[1]
CADICAL = ROOT / "tools/cadical_3_0_1/build/cadical"
DRAT_TRIM = ROOT / "tools/drat_trim_2023_05_22/drat-trim"
N = 12
FROZEN_ARTIFACT_SHA256 = {
    "src/synthesis_k3/cegar.py": (
        "411fffff34c0122d679ee710aff0e3856a7ff166bff30c69edb1f0044defce8c"
    ),
    "tests/test_synthesis_k3_cegar.py": (
        "56101dee36685e476ace516fc30b31f7f0d3dc2a5efd11b3e25387038b0146fb"
    ),
    "math/synthesis_k3_cegar_protocol.md": (
        "c51db6d865557f4dcc3147772dbaa1c86d3c6c6d3544ab0090f0f89267a9de31"
    ),
}
FROZEN_RUNTIME_SOURCE_SET_SHA256 = (
    "8c4e811bc4250c3e2b0b7edeb8afd07f7509ebda3cbae3db1b3ca82c07b35299"
)


def kwargs(run_directory: Path) -> dict[str, object]:
    return {
        "template": "hole5",
        "run_directory": run_directory,
        "cadical_path": CADICAL,
        "drat_trim_path": DRAT_TRIM,
        "solver_seed": 0,
        "solver_wall_seconds": 10,
        "solver_memory_mib": 1024,
        "checker_wall_seconds": 10,
        "checker_memory_mib": 1024,
        "disk_reserve_mib": 256,
        "child_file_limit_mib": 64,
        "retained_attempt_limit_mib": 2,
    }


def load_object(path: Path) -> dict[str, object]:
    value = strict_json_file(path)
    if not isinstance(value, dict):
        raise AssertionError(f"{path} is not a JSON object")
    return value


def install(path: Path, value: object) -> None:
    path.write_bytes(canonical_json_bytes(value))


def verify_frozen_bindings() -> dict[str, object]:
    observed = {
        relative: sha256_file(ROOT / relative)
        for relative in FROZEN_ARTIFACT_SHA256
    }
    if observed != FROZEN_ARTIFACT_SHA256:
        raise AssertionError(
            f"frozen artifact hash mismatch: {observed!r}"
        )
    runtime_digest = source_set_sha256(runtime_source_manifest())
    if runtime_digest != FROZEN_RUNTIME_SOURCE_SET_SHA256:
        raise AssertionError(
            "frozen runtime source-set hash mismatch: "
            f"{runtime_digest}"
        )
    return {
        "artifact_sha256": observed,
        "runtime_source_set_sha256": runtime_digest,
        "all_match": True,
    }


def tree_snapshot(root: Path) -> tuple[tuple[str, str, str | None], ...]:
    records: list[tuple[str, str, str | None]] = []
    for path in sorted(root.rglob("*")):
        relative = str(path.relative_to(root))
        if path.is_file():
            records.append((relative, "file", sha256_file(path)))
        elif path.is_dir():
            records.append((relative, "directory", None))
        elif path.is_symlink():
            records.append((relative, "symlink", os.readlink(path)))
        else:
            records.append((relative, "other", None))
    return tuple(records)


def rebind_first_attempt(
    run_directory: Path,
    mutate,
) -> None:
    checkpoint_path = run_directory / CHECKPOINT_NAME
    checkpoint = load_object(checkpoint_path)
    reference = checkpoint["attempts"][0]  # type: ignore[index]
    attempt_path = Path(reference["manifest_path"])
    attempt = load_object(attempt_path)
    mutate(attempt)
    install(attempt_path, attempt)
    digest = sha256_file(attempt_path)
    reference["manifest_sha256"] = digest
    reference["checkpoint_before_sha256"] = attempt[
        "checkpoint_before_sha256"
    ]
    reference["history_chain_before_sha256"] = attempt[
        "history_chain_before_sha256"
    ]
    cut = checkpoint["cuts"][0]  # type: ignore[index]
    cut["source_attempt_manifest_sha256"] = digest
    checkpoint["history_chain_sha256"] = _history_chain_step(
        reference["history_chain_before_sha256"],
        attempt_reference=reference,
        cut_record=cut,
        status_value="running",
        terminal=None,
    )
    install(checkpoint_path, checkpoint)


def mutation_is_accepted(
    run_directory: Path,
    mutate,
) -> bool:
    checkpoint_path = run_directory / CHECKPOINT_NAME
    checkpoint_before = checkpoint_path.read_bytes()
    checkpoint = load_object(checkpoint_path)
    attempt_path = Path(checkpoint["attempts"][0]["manifest_path"])  # type: ignore[index]
    attempt_before = attempt_path.read_bytes()
    try:
        rebind_first_attempt(run_directory, mutate)
        try:
            audit_run(**kwargs(run_directory), deep_reconstruct=True)
        except (RuntimeError, ValueError):
            return False
        return True
    finally:
        attempt_path.write_bytes(attempt_before)
        checkpoint_path.write_bytes(checkpoint_before)


def independent_first_cut_check(run_directory: Path) -> dict[str, int | bool]:
    checkpoint = load_object(run_directory / CHECKPOINT_NAME)
    attempt = load_object(
        Path(checkpoint["attempts"][0]["manifest_path"])  # type: ignore[index]
    )
    decoded = load_object(
        Path(attempt["artifacts"]["decoded_candidate"]["path"])  # type: ignore[index]
    )
    coloring = json.loads(
        Path(attempt["artifacts"]["coloring"]["path"]).read_text(  # type: ignore[index]
            encoding="utf-8"
        )
    )
    h_edges = {tuple(edge) for edge in decoded["h_edges"]}  # type: ignore[index]
    g_edges = {tuple(edge) for edge in decoded["g_edges"]}  # type: ignore[index]
    all_pairs = set(combinations(range(N), 2))
    if h_edges & g_edges or h_edges | g_edges != all_pairs:
        raise AssertionError("decoded H and G are not exact complements")
    if any(coloring[u] == coloring[v] for u, v in h_edges):
        raise AssertionError("recorded coloring is not proper in H")
    if any(
        all(tuple(sorted(pair)) in h_edges for pair in combinations(four, 2))
        for four in combinations(range(N), 4)
    ):
        raise AssertionError("decoded H contains a four-clique")
    if not any(
        all(tuple(sorted(pair)) in h_edges for pair in combinations(triple, 2))
        for triple in combinations(range(N), 3)
    ):
        raise AssertionError("decoded H has no triangle")
    for first, second in combinations(range(N), 2):
        if not any(
            tuple(sorted((first, witness))) in h_edges
            and tuple(sorted((second, witness))) in h_edges
            for witness in range(N)
            if witness not in (first, second)
        ):
            raise AssertionError("a pair of H has no external common neighbor")

    reached = {0}
    frontier = [0]
    while frontier:
        first = frontier.pop()
        for second in range(N):
            pair = tuple(sorted((first, second)))
            if (
                second != first
                and second not in reached
                and pair in g_edges
            ):
                reached.add(second)
                frontier.append(second)
    if len(reached) != N:
        raise AssertionError("decoded G is disconnected")

    rim = range(5)
    rim_edges = {
        tuple(sorted((vertex, (vertex + 1) % 5))) for vertex in rim
    }
    for pair in combinations(rim, 2):
        if (pair in h_edges) != (pair in rim_edges):
            raise AssertionError("decoded H lacks the forced induced C5")
    if any(
        all(tuple(sorted((outside, vertex))) in h_edges for vertex in rim)
        for outside in range(5, N)
    ):
        raise AssertionError("decoded C5 has an external H-hub")
    if (0, 5) not in h_edges or (1, 5) not in h_edges:
        raise AssertionError("decoded C5 edge lacks its labeled common neighbor")

    family = {tuple(state) for state in decoded["eternal_family"]}  # type: ignore[index]
    if not family:
        raise AssertionError("decoded eternal family is empty")
    for state in family:
        for attacked in set(range(N)) - set(state):
            if not any(
                tuple(sorted((set(state) - {guard}) | {attacked})) in family
                and tuple(sorted((guard, attacked))) in g_edges
                for guard in state
            ):
                raise AssertionError("decoded family has an undefended attack")
        for outside in set(range(N)) - set(state):
            if not any(
                tuple(sorted((outside, guard))) in g_edges
                for guard in state
            ):
                raise AssertionError("decoded family contains a nondominating state")

    edge_variable = {
        pair: index
        for index, pair in enumerate(combinations(range(N), 2), start=1)
    }
    expected_clause = [
        edge_variable[pair]
        for pair in combinations(range(N), 2)
        if coloring[pair[0]] == coloring[pair[1]]
    ]
    actual_clause = checkpoint["cuts"][0]["clause"]  # type: ignore[index]
    if actual_clause != expected_clause:
        raise AssertionError("checkpoint cut is not the same-color H-edge clause")

    model_record = attempt["compressed_artifacts"]["solver_result"]  # type: ignore[index]
    model_bytes = gzip.decompress(
        Path(model_record["gzip_path"]).read_bytes()  # type: ignore[index]
    )
    positive = {
        int(token)
        for line in model_bytes.decode("ascii").splitlines()
        if line.startswith("v ")
        for token in line[2:].split()
        if int(token) > 0
    }
    if any(variable in positive for variable in expected_clause):
        raise AssertionError("new cut is not false in its source H model")
    return {
        "h_edge_count": len(h_edges),
        "g_edge_count": len(g_edges),
        "family_size": len(family),
        "cut_length": len(expected_clause),
        "complement_and_one_guard_semantics_passed": True,
        "static_and_template_semantics_passed": True,
    }


def orphan_marker_is_fail_closed(run_directory: Path) -> bool:
    with mock.patch("synthesis_k3.cegar.find_coloring", return_value=None):
        outcome = run_cegar(**kwargs(run_directory), max_iterations=1)
    if outcome.status != "candidate_review_pending":
        raise AssertionError("candidate smoke did not freeze")
    marker = run_directory / CANDIDATE_MARKER_NAME
    checkpoint_path = run_directory / CHECKPOINT_NAME
    checkpoint = load_object(checkpoint_path)
    checkpoint["status"] = "running"
    checkpoint["attempts"] = []
    checkpoint["cuts"] = []
    checkpoint["cuts_payload_sha256"] = sha256_bytes(b"[]\n")
    checkpoint["history_chain_sha256"] = load_object(marker)[
        "history_chain_before_sha256"
    ]
    checkpoint["terminal"] = None
    install(checkpoint_path, checkpoint)
    with mock.patch("synthesis_k3.cegar.find_coloring", return_value=None):
        audited = audit_run(**kwargs(run_directory))
    return marker.is_file() and audited.status == "candidate_review_pending"


def fabricated_unsat_terminal_is_accepted(run_directory: Path) -> bool:
    """Try to turn a real SAT attempt into a fake terminal by rebinding hashes."""

    checkpoint_path = run_directory / CHECKPOINT_NAME
    checkpoint = load_object(checkpoint_path)
    attempt_path = Path(checkpoint["attempts"][0]["manifest_path"])  # type: ignore[index]
    attempt = load_object(attempt_path)
    attempt["outcome"] = "unsat_verified"
    attempt.pop("committed_cut", None)
    attempt["validation"] = {
        "initial_unsat": True,
        "identical_cnf_rerun": True,
        "proof_rerun_unsat": True,
        "drat_trim_flags": ["-I", "-f", "-W"],
        "drat_trim_exact_verified_line": True,
        "drat_trim_warning_free": True,
        "cnf_unchanged": True,
        "proof_unchanged_during_check": True,
    }
    artifacts = attempt["artifacts"]  # type: ignore[assignment]
    compressed = attempt["compressed_artifacts"]  # type: ignore[assignment]
    reconstructible = attempt["reconstructible_artifacts"]  # type: ignore[assignment]

    # No proof is introduced.  Existing unrelated bytes are merely assigned
    # proof/result/log roles to test whether the audit enforces role semantics.
    artifacts["drat_proof"] = dict(artifacts["coloring"])
    artifacts["proof_result"] = dict(artifacts["coloring"])
    for new_role, old_role in (
        ("proof_solver_stdout", "solver_stdout"),
        ("checker_stdout", "solver_stdout"),
        ("proof_solver_stderr", "solver_stderr"),
        ("checker_stderr", "solver_stderr"),
    ):
        compressed[new_role] = dict(compressed[old_role])

    cnf_path = reconstructible["cnf"]["raw_path"]
    proof_path = artifacts["drat_proof"]["path"]
    proof_solver = copy.deepcopy(attempt["initial_solver"])
    proof_solver["exit_code"] = 20
    proof_solver["command"] = [
        str(CADICAL.resolve()),
        "--seed=0",
        "-t",
        "10",
        cnf_path,
        proof_path,
    ]
    proof_solver["command_sha256"] = sha256_bytes(
        canonical_json_bytes(proof_solver["command"], pretty=False)
    )
    proof_solver["stdout_path"] = compressed["proof_solver_stdout"]["raw_path"]
    proof_solver["stdout_sha256"] = compressed["proof_solver_stdout"]["raw_sha256"]
    proof_solver["stderr_path"] = compressed["proof_solver_stderr"]["raw_path"]
    proof_solver["stderr_sha256"] = compressed["proof_solver_stderr"]["raw_sha256"]

    proof_checker = copy.deepcopy(attempt["initial_solver"])
    proof_checker["exit_code"] = 0
    proof_checker["command"] = [
        str(DRAT_TRIM.resolve()),
        cnf_path,
        proof_path,
        "-I",
        "-f",
        "-W",
    ]
    proof_checker["command_sha256"] = sha256_bytes(
        canonical_json_bytes(proof_checker["command"], pretty=False)
    )
    proof_checker["executable_sha256_before"] = DRAT_TRIM_BINARY_SHA256
    proof_checker["executable_sha256_after"] = DRAT_TRIM_BINARY_SHA256
    proof_checker["stdout_path"] = compressed["checker_stdout"]["raw_path"]
    proof_checker["stdout_sha256"] = compressed["checker_stdout"]["raw_sha256"]
    proof_checker["stderr_path"] = compressed["checker_stderr"]["raw_path"]
    proof_checker["stderr_sha256"] = compressed["checker_stderr"]["raw_sha256"]
    attempt["proof_solver"] = proof_solver
    attempt["proof_checker"] = proof_checker

    install(attempt_path, attempt)
    attempt_hash = sha256_file(attempt_path)
    reference = checkpoint["attempts"][0]  # type: ignore[index]
    reference["outcome"] = "unsat_verified"
    reference["manifest_sha256"] = attempt_hash
    checkpoint["cuts"] = []
    checkpoint["cuts_payload_sha256"] = sha256_bytes(b"[]\n")
    checkpoint["status"] = "unsat_verified"
    marker = {
        "schema": "gamma-theta-k3-cegar-terminal-v2",
        "schema_version": 2,
        "kind": "unsat",
        "status": "unsat_verified",
        "configuration_sha256": checkpoint["configuration_sha256"],
        "run_manifest_sha256": checkpoint["run_manifest_sha256"],
        "checkpoint_before_sha256": attempt["checkpoint_before_sha256"],
        "history_chain_before_sha256": attempt[
            "history_chain_before_sha256"
        ],
        "attempt_manifest_path": str(attempt_path.resolve()),
        "attempt_manifest_sha256": attempt_hash,
    }
    marker_path = run_directory / UNSAT_MARKER_NAME
    install(marker_path, marker)
    checkpoint["terminal"] = {
        "kind": "unsat",
        "path": str(marker_path.resolve()),
        "sha256": sha256_file(marker_path),
    }
    checkpoint["history_chain_sha256"] = _history_chain_step(
        reference["history_chain_before_sha256"],
        attempt_reference=reference,
        cut_record=None,
        status_value="unsat_verified",
        terminal=checkpoint["terminal"],
    )
    install(checkpoint_path, checkpoint)
    try:
        outcome = audit_run(**kwargs(run_directory), deep_reconstruct=True)
    except (RuntimeError, ValueError):
        return False
    return outcome.status == "unsat_verified"


def falsify_auxiliary_model_clause(attempt: dict[str, object]) -> None:
    record = attempt["compressed_artifacts"]["solver_result"]  # type: ignore[index]
    gzip_path = Path(record["gzip_path"])  # type: ignore[index]
    raw = gzip.decompress(gzip_path.read_bytes())
    encoding = build_k3_encoding("hole5")
    parsed = parse_solver_result_bytes(raw, encoding.cnf.variable_count)
    if parsed.model is None:
        raise AssertionError("SAT smoke has no model")
    model = dict(parsed.model)
    protected = set(encoding.edge_variables.values()) | set(
        encoding.family_variables.values()
    )
    for clause in encoding.cnf.clauses:
        true_literals = [
            literal
            for literal in clause
            if model[abs(literal)] == (literal > 0)
        ]
        if len(true_literals) == 1 and abs(true_literals[0]) not in protected:
            literal = true_literals[0]
            model[abs(literal)] = literal < 0
            break
    else:
        raise AssertionError("no singly supported auxiliary clause found")
    rewritten = (
        "s SATISFIABLE\nv "
        + " ".join(
            str(variable if model[variable] else -variable)
            for variable in range(1, encoding.cnf.variable_count + 1)
        )
        + " 0\n"
    ).encode("ascii")
    packed = gzip.compress(rewritten, compresslevel=9, mtime=0)
    gzip_path.write_bytes(packed)
    record["raw_sha256"] = sha256_bytes(rewritten)  # type: ignore[index]
    record["raw_size_bytes"] = len(rewritten)  # type: ignore[index]
    record["gzip_sha256"] = sha256_bytes(packed)  # type: ignore[index]
    record["gzip_size_bytes"] = len(packed)  # type: ignore[index]


def later_checkpoint_digest_mutation_is_accepted(run_directory: Path) -> bool:
    run_cegar(**kwargs(run_directory), max_iterations=2)
    checkpoint_path = run_directory / CHECKPOINT_NAME
    checkpoint = load_object(checkpoint_path)
    reference = checkpoint["attempts"][1]  # type: ignore[index]
    attempt_path = Path(reference["manifest_path"])
    attempt = load_object(attempt_path)
    attempt["checkpoint_before_sha256"] = "0" * 64
    install(attempt_path, attempt)
    digest = sha256_file(attempt_path)
    reference["manifest_sha256"] = digest
    reference["checkpoint_before_sha256"] = "0" * 64
    cut = checkpoint["cuts"][1]  # type: ignore[index]
    cut["source_attempt_manifest_sha256"] = digest
    first_reference = checkpoint["attempts"][0]  # type: ignore[index]
    first_cut = checkpoint["cuts"][0]  # type: ignore[index]
    history = _history_chain_step(
        first_reference["history_chain_before_sha256"],
        attempt_reference=first_reference,
        cut_record=first_cut,
        status_value="running",
        terminal=None,
    )
    if reference["history_chain_before_sha256"] != history:
        raise AssertionError("two-cut history predecessor is inconsistent")
    checkpoint["history_chain_sha256"] = _history_chain_step(
        history,
        attempt_reference=reference,
        cut_record=cut,
        status_value="running",
        terminal=None,
    )
    install(checkpoint_path, checkpoint)
    try:
        audit_run(**kwargs(run_directory), deep_reconstruct=True)
    except (RuntimeError, ValueError):
        return False
    return True


def prefix_replay_cost(run_directory: Path, cut_count: int = 8) -> dict[str, object]:
    run_cegar(**kwargs(run_directory), max_iterations=cut_count)
    import synthesis_k3.cegar as cegar_module

    observed: list[int] = []
    original = cegar_module.validate_model_satisfies_encoding_prefix

    def counted(encoding, cuts, prefix_count, model):
        observed.append(prefix_count)
        return original(encoding, cuts, prefix_count, model)

    instrumentation = AuditInstrumentation()
    with mock.patch(
        "synthesis_k3.cegar.validate_model_satisfies_encoding_prefix",
        side_effect=counted,
    ):
        audit_run(
            **kwargs(run_directory),
            instrumentation=instrumentation,
        )
    counters = asdict(instrumentation)
    expected_counters = {
        "attempt_semantic_validations": cut_count,
        "historical_sat_base_cnf_validations": cut_count,
        "historical_own_cut_validations": cut_count,
        "cut_ledger_record_validations": cut_count,
        "decisive_cnf_reconstructions": 0,
    }
    return {
        "attempt_prefix_lengths": observed,
        "total_prior_cut_replays": sum(observed),
        "triangular_expected": cut_count * (cut_count - 1) // 2,
        "instrumentation": counters,
        "expected_linear_instrumentation": expected_counters,
        "linear_history_audit_passed": (
            counters == expected_counters and not observed
        ),
        "quadratic_prefix_replay_observed": (
            observed == list(range(cut_count))
            and sum(observed) == cut_count * (cut_count - 1) // 2
        ),
    }


def live_tiny_drat_recheck(temporary: Path) -> bool:
    configuration = build_configuration(
        template="hole5",
        run_directory=temporary,
        cadical_path=CADICAL,
        drat_trim_path=DRAT_TRIM,
        solver_seed=0,
        solver_wall_seconds=10,
        solver_memory_mib=1024,
        checker_wall_seconds=10,
        checker_memory_mib=1024,
        disk_reserve_mib=256,
        child_file_limit_mib=64,
        retained_attempt_limit_mib=2,
    )
    cnf = temporary / "tiny-unsat.cnf"
    atomic_write(cnf, b"p cnf 1 2\n1 0\n-1 0\n")
    parsed = parse_dimacs_file(cnf)
    _, _, artifacts = run_unsat_proof_replay(
        configuration=configuration,
        cnf_path=cnf,
        parsed_cnf=parsed,
        attempt_directory=temporary,
    )
    result = verify_stored_drat_certificate(
        configuration=configuration,
        cnf_path=cnf,
        proof_path=artifacts["drat_proof"],
    )
    return result.exit_code == 0


def sigterm_leaves_child_alive(temporary: Path) -> bool:
    pid_path = temporary / "grandchild.pid"
    helper = (
        "from pathlib import Path\n"
        "import sys\n"
        "from synthesis_k3.cegar import run_bounded_child\n"
        "root=Path(sys.argv[1])\n"
        "pidfile=root/'grandchild.pid'\n"
        "code='import os,sys,time; from pathlib import Path; "
        "Path(sys.argv[1]).write_text(str(os.getpid())); time.sleep(30)'\n"
        "run_bounded_child(command=(str(Path(sys.executable).resolve()),"
        "'-c',code,str(pidfile)),cwd=root,stdout_path=root/'child.out',"
        "stderr_path=root/'child.err',wall_limit_seconds=30,"
        "memory_limit_mib=128,readonly_paths={})\n"
    )
    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(ROOT / "src")
    parent = subprocess.Popen(
        [sys.executable, "-c", helper, str(temporary)],
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    child_pid: int | None = None
    try:
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline and not pid_path.exists():
            time.sleep(0.02)
        if not pid_path.exists():
            raise AssertionError("grandchild PID was not recorded")
        child_pid = int(pid_path.read_text(encoding="ascii"))
        parent.terminate()
        parent.wait(timeout=5)
        time.sleep(0.2)
        try:
            os.kill(child_pid, 0)
        except ProcessLookupError:
            return False
        return True
    finally:
        if parent.poll() is None:
            parent.kill()
            parent.wait(timeout=5)
        if child_pid is not None:
            try:
                os.killpg(child_pid, signal.SIGKILL)
            except ProcessLookupError:
                pass


def main() -> int:
    results: dict[str, object] = {
        "frozen_bindings": verify_frozen_bindings(),
    }
    with tempfile.TemporaryDirectory(prefix="cegar-hostile-") as raw:
        temporary = Path(raw).resolve()
        run_directory = temporary / "one-cut"
        outcome = run_cegar(**kwargs(run_directory), max_iterations=1)
        if outcome.status != "iteration_budget_exhausted" or outcome.cut_count != 1:
            raise AssertionError("one-cut smoke did not reach the expected state")
        results["baseline"] = independent_first_cut_check(run_directory)
        before_audit = tree_snapshot(run_directory)
        results["deep_audit_passed"] = (
            audit_run(**kwargs(run_directory), deep_reconstruct=True).status
            == "running_audit_passed"
        )
        results["audit_run_directory_byte_tree_unchanged"] = (
            tree_snapshot(run_directory) == before_audit
        )

        results["accepted_rebound_mutations"] = {
            "unvalidated_checkpoint_before_sha256": mutation_is_accepted(
                run_directory,
                lambda attempt: attempt.__setitem__(
                    "checkpoint_before_sha256", "not-a-sha256"
                ),
            ),
            "negative_child_limits": mutation_is_accepted(
                run_directory,
                lambda attempt: attempt["initial_solver"].update(  # type: ignore[union-attr,index]
                    {
                        "wall_limit_seconds": -1,
                        "memory_limit_mib": -1,
                        "file_limit_mib": -1,
                    }
                ),
            ),
            "contradictory_solver_exit_code": mutation_is_accepted(
                run_directory,
                lambda attempt: attempt["initial_solver"].update(  # type: ignore[union-attr,index]
                    {"exit_code": 20}
                ),
            ),
            "extra_unrecognized_solver_flag": mutation_is_accepted(
                run_directory,
                lambda attempt: (
                    attempt["initial_solver"]["command"].append(  # type: ignore[index,union-attr]
                        "--hostile-unrecognized-option"
                    ),
                    attempt["initial_solver"].__setitem__(  # type: ignore[index,union-attr]
                        "command_sha256",
                        sha256_bytes(
                            canonical_json_bytes(
                                attempt["initial_solver"]["command"],  # type: ignore[index]
                                pretty=False,
                            )
                        ),
                    ),
                ),
            ),
            "decoded_candidate_aliases_coloring": mutation_is_accepted(
                run_directory,
                lambda attempt: attempt["artifacts"].__setitem__(  # type: ignore[union-attr,index]
                    "decoded_candidate",
                    dict(attempt["artifacts"]["coloring"]),  # type: ignore[index]
                ),
            ),
            "auxiliary_model_clause_falsified": mutation_is_accepted(
                run_directory,
                falsify_auxiliary_model_clause,
            ),
        }
        results["fabricated_unsat_without_proof_accepted"] = (
            fabricated_unsat_terminal_is_accepted(run_directory)
        )

        candidate_directory = temporary / "orphan-candidate"
        results["orphan_candidate_marker_blocks_resume"] = (
            orphan_marker_is_fail_closed(candidate_directory)
        )

        lock_directory = temporary / "locked"
        run_cegar(**kwargs(lock_directory), max_iterations=1)
        with RunLock(lock_directory):
            try:
                audit_run(**kwargs(lock_directory))
            except RuntimeError as error:
                results["same_run_lock_rejected"] = (
                    "another orchestrator" in str(error)
                )
            else:
                results["same_run_lock_rejected"] = False

        try:
            with CampaignHeavyChildLock():
                run_bounded_child(
                    command=(
                        str(Path(sys.executable).resolve()),
                        "-c",
                        "raise SystemExit(0)",
                    ),
                    cwd=temporary,
                    stdout_path=temporary / "global-lock.out",
                    stderr_path=temporary / "global-lock.err",
                    wall_limit_seconds=2,
                    memory_limit_mib=128,
                    readonly_paths={},
                )
        except RuntimeError as error:
            results["campaign_global_lock_rejected"] = (
                "campaign solver/checker" in str(error)
            )
        else:
            results["campaign_global_lock_rejected"] = False

        process_directory = temporary / "sigterm"
        process_directory.mkdir()
        results["parent_sigterm_left_solver_child_alive"] = (
            sigterm_leaves_child_alive(process_directory)
        )

        results["later_checkpoint_digest_mutation_accepted"] = (
            later_checkpoint_digest_mutation_is_accepted(
                temporary / "two-cut-checkpoint"
            )
        )
        results["history_replay_complexity"] = prefix_replay_cost(
            temporary / "prefix-cost"
        )
        drat_directory = temporary / "tiny-drat"
        drat_directory.mkdir()
        results["live_tiny_drat_recheck_passed"] = live_tiny_drat_recheck(
            drat_directory
        )

    accepted_mutations = results["accepted_rebound_mutations"]
    assert isinstance(accepted_mutations, dict)
    complexity = results["history_replay_complexity"]
    assert isinstance(complexity, dict)
    acceptance_checks = {
        "frozen_bindings": results["frozen_bindings"]["all_match"],  # type: ignore[index]
        "independent_math_semantics": (
            results["baseline"][
                "complement_and_one_guard_semantics_passed"
            ]  # type: ignore[index]
            and results["baseline"][
                "static_and_template_semantics_passed"
            ]  # type: ignore[index]
        ),
        "deep_audit": results["deep_audit_passed"],
        "read_only_audit": results[
            "audit_run_directory_byte_tree_unchanged"
        ],
        "all_rebound_mutations_rejected": not any(
            accepted_mutations.values()
        ),
        "fabricated_unsat_rejected": not results[
            "fabricated_unsat_without_proof_accepted"
        ],
        "orphan_marker_fail_closed": results[
            "orphan_candidate_marker_blocks_resume"
        ],
        "same_run_lock": results["same_run_lock_rejected"],
        "campaign_global_lock": results["campaign_global_lock_rejected"],
        "signal_cleanup": not results[
            "parent_sigterm_left_solver_child_alive"
        ],
        "checkpoint_chronology": not results[
            "later_checkpoint_digest_mutation_accepted"
        ],
        "linear_history_work": complexity[
            "linear_history_audit_passed"
        ],
        "no_quadratic_prefix_replay": not complexity[
            "quadratic_prefix_replay_observed"
        ],
        "live_pinned_drat_check": results[
            "live_tiny_drat_recheck_passed"
        ],
    }
    results["acceptance_checks"] = acceptance_checks
    if not all(value is True for value in acceptance_checks.values()):
        results["verdict"] = "REJECT"
        print(json.dumps(results, indent=2, sort_keys=True))
        raise AssertionError("one or more hostile acceptance gates failed")
    results["verdict"] = "ACCEPT"
    results["hostile_probe_sha256"] = sha256_file(Path(__file__).resolve())
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
