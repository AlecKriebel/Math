#!/usr/bin/env python3
"""Fail-closed mutation suite for the hardened K3P clean-room verifier."""
from __future__ import annotations

import ast
import copy
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
PROJECT = HERE.parent
sys.path.insert(0, str(HERE))

import verify_h21_transport_and_fourteen_orbits as verifier


RESULTS = []


def record(name, mechanism, expected_failure, kind="mutation"):
    RESULTS.append({
        "name": name,
        "kind": kind,
        "result": "REJECTED",
        "mechanism": mechanism,
        "expected_failure": expected_failure,
    })


def expect_rejected(name, function, expected_failure):
    try:
        function()
    except (verifier.CertificationError, RuntimeError) as error:
        verifier.require(expected_failure in str(error),
                         "mutation failed for the wrong reason",
                         name, str(error), expected_failure)
        record(name, "in-process explicit certification gate", expected_failure)
        return
    raise verifier.CertificationError(f"mutation was accepted: {name}")


def subprocess_rejection(name, command, environment, expected_failure):
    completed = subprocess.run(
        command,
        cwd=PROJECT,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    verifier.require(completed.returncode != 0,
                     "mutation subprocess unexpectedly exited zero", name)
    verifier.require(expected_failure in completed.stdout,
                     "mutation subprocess failed for the wrong reason",
                     name, completed.stdout, expected_failure)
    record(name, "fresh-process terminal gate", expected_failure)


def reconstruct_all():
    return {
        orbit_id: verifier.reconstruct_record(record)
        for orbit_id, record in verifier.RECORDS.items()
    }


def run():
    started = time.perf_counter()
    verifier_source = (HERE /
        "verify_h21_transport_and_fourteen_orbits.py").read_text()
    parsed = ast.parse(verifier_source)
    verifier.require(not any(isinstance(node, ast.Assert) for node in ast.walk(parsed)),
                     "hardened verifier still contains an assert statement")
    record("static_no_assert_gate", "AST scan", "zero Assert nodes", "control")

    historical = HERE / "HISTORICAL_cleanroom_verify_fourteen_orbits.py"
    historical_hash = hashlib.sha256(historical.read_bytes()).hexdigest()
    verifier.require(historical_hash ==
                     "ee5e29a2cd795d9389e8e1257ebdb9eeaa4256fb5d03e07f230bf82ba555ef91",
                     "historical verifier bytes changed", historical_hash)
    record("historical_verifier_preserved", "fixed SHA-256 binding",
           "historical SHA-256 exact match", "control")

    port_record = copy.deepcopy(verifier.RECORDS["H21-01"])
    port_record["port_permutation"] = [0, 1, 2, 3]
    expect_rejected(
        "mutated_port_permutation",
        lambda: verifier.reconstruct_record(port_record),
        "port_permutation is not bound",
    )

    incoming_record = copy.deepcopy(verifier.RECORDS["H21-01"])
    incoming_record["target_incoming_role"] = "selected-port-3"
    expect_rejected(
        "mutated_target_incoming_role",
        lambda: verifier.reconstruct_record(incoming_record),
        "target incoming-role metadata mismatch",
    )

    reconstructions = reconstruct_all()
    rank_records = verifier.load_bound_json(
        "k3p_directed_rank_obstructions.json"
    )["records"]
    h21 = next(item for item in rank_records if item["orbit_id"] == "H21-02")

    weakened_rank = copy.deepcopy(h21)
    weakened_rank["target_rank_certificate"]["rank"] -= 1
    expect_rejected(
        "weakened_target_rank_claim",
        lambda: verifier.verify_rank_obstruction_certificate(
            weakened_rank, reconstructions
        ),
        "rank claim is not bound to square minor size",
    )

    weakened_upper_bound = copy.deepcopy(h21)
    weakened_upper_bound["target_dimension_upper_bound"] -= 1
    expect_rejected(
        "weakened_target_upper_bound_claim",
        lambda: verifier.verify_rank_obstruction_certificate(
            weakened_upper_bound, reconstructions
        ),
        "claimed target upper bound differs from reconstructed generator count",
    )

    inflated_labels = copy.deepcopy(h21)
    inflated_labels["source_rank_certificate"]["rank"] = 101
    inflated_labels["target_dimension_upper_bound"] = 100
    inflated_labels["target_rank_certificate"]["rank"] = 100
    expect_rejected(
        "inflated_101_over_100_rank_labels",
        lambda: verifier.verify_rank_obstruction_certificate(
            inflated_labels, reconstructions
        ),
        "rank claim is not bound to square minor size",
    )

    nonsquare_minor = copy.deepcopy(h21)
    nonsquare_minor["target_rank_certificate"]["parameter_columns"].pop()
    expect_rejected(
        "mismatched_target_minor_size",
        lambda: verifier.verify_rank_obstruction_certificate(
            nonsquare_minor, reconstructions
        ),
        "rank claim is not bound to square minor size",
    )

    wrong_selected_set = copy.deepcopy(h21)
    wrong_selected_set["selected_output_rows"][-1] = 62
    wrong_selected_set["selected_output_labels"][-1] = "TTGT"
    expect_rejected(
        "mutated_selected_observable_set",
        lambda: verifier.verify_rank_obstruction_certificate(
            wrong_selected_set, reconstructions
        ),
        "rank minor row lies outside selected observable set",
    )

    expect_rejected(
        "skip_all_algebraic_certificates",
        lambda: verifier.verify_all(run_certificates=False),
        "full verifier cannot skip algebraic certificates",
    )

    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    subprocess_rejection(
        "optimized_python_mode",
        [sys.executable, "-O", str(HERE /
            "verify_h21_transport_and_fourteen_orbits.py")],
        environment,
        "certification verifier refuses optimized Python",
    )

    with tempfile.TemporaryDirectory(prefix="k3p-cleanroom-mutation-") as temp_name:
        temp = Path(temp_name)
        for filename in verifier.EXPECTED_INPUT_SHA256:
            shutil.copy2(verifier.ARTIFACTS / filename, temp / filename)
        rank_path = temp / "k3p_directed_rank_obstructions.json"
        rank_path.chmod(0o600)
        rank_path.write_bytes(rank_path.read_bytes() + b"\n")
        mutated_environment = dict(environment)
        mutated_environment["K3P_CLEANROOM_ARTIFACTS"] = str(temp)
        subprocess_rejection(
            "mutated_active_input_hash",
            [sys.executable, str(HERE /
                "verify_h21_transport_and_fourteen_orbits.py")],
            mutated_environment,
            "active input hash mismatch",
        )

    mutation_count = sum(item["kind"] == "mutation" for item in RESULTS)
    control_count = sum(item["kind"] == "control" for item in RESULTS)
    results = {
        "schema": "k3p-clean-room-mutation-results-v2",
        "status": "PASS",
        "mutation_count": mutation_count,
        "control_count": control_count,
        "accepted_mutations": 0,
        "rejected_mutations": mutation_count,
        "records": RESULTS,
    }
    output_path = HERE / "CLEAN_ROOM_MUTATION_RESULTS.json"
    output_path.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    elapsed = time.perf_counter() - started
    print("CLEAN_ROOM_MUTATIONS_PASS "
          f"rejected={mutation_count} controls={control_count} "
          f"elapsed={elapsed:.6f}s")


if __name__ == "__main__":
    run()
