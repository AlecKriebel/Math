#!/usr/bin/env python3
"""Negative controls for nested semantic-mutation qualification contracts."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load(name: str, relative: str):
    path = PROJECT / relative
    specification = importlib.util.spec_from_file_location(name, path)
    require(
        specification is not None and specification.loader is not None,
        f"cannot import:{path}",
    )
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def expect_failure(function, marker: str) -> None:
    try:
        function()
    except (RuntimeError, SystemExit) as error:
        require(
            marker.lower() in str(error).lower(),
            f"wrong failure:{marker}:{error}",
        )
        return
    raise RuntimeError(f"negative control accepted:{marker}")


def synthetic_result(diagnostic: str) -> dict[str, object]:
    return {
        "returncode": 1,
        "diagnostic": diagnostic,
        "output": diagnostic,
        "success_artifact_present": False,
        "timeout": False,
        "signal": False,
    }


def exercise_dictionary_qualifier(module, name: str) -> int:
    expected = module.MUTATION_DIAGNOSTICS[name]
    accepted = module.qualify_mutation_failure(name, synthetic_result(expected))
    require(accepted["observed_diagnostic"] == expected, f"qualified drift:{name}")
    attacks = {
        "wrong diagnostic": {
            **synthetic_result(expected),
            "diagnostic": expected + ":wrong",
            "output": expected + ":wrong",
        },
        "unrelated crash": {
            **synthetic_result(expected),
            "diagnostic": "Traceback (most recent call last):\nModuleNotFoundError: dependency",
            "output": "Traceback (most recent call last):\nModuleNotFoundError: dependency",
        },
        "timeout": {**synthetic_result(expected), "returncode": None, "timeout": True},
        "signal": {**synthetic_result(expected), "returncode": -9, "signal": True},
        "success artifact": {**synthetic_result(expected), "success_artifact_present": True},
    }
    for label, attack in attacks.items():
        expect_failure(
            lambda attack=attack: module.qualify_mutation_failure(name, attack),
            "mutation",
        )
    return len(attacks)


def main() -> None:
    if not __debug__:
        raise SystemExit("SEMANTIC_MUTATION_DIAGNOSTIC_TEST_OPTIMIZED_MODE_FORBIDDEN")
    canonicalizer = load(
        "k2p_test_canonicalizer_mutations",
        "work/canonicalizer_completeness/test_canonicalizer_mutations.py",
    )
    restoration = load(
        "k2p_test_restoration_mutations",
        "work/restoration_sign_reclassification/mutate_corrected_restoration_forest.py",
    )
    probe = load(
        "k2p_test_probe_mutations",
        "work/probe_coherence_corrected/run_probe_coherence_mutations.py",
    )
    unified = load(
        "k2p_test_unified_mutations",
        "work/final_theorem_release/run_corrected_universe_mutations.py",
    )
    probe_input = load(
        "k2p_test_probe_input_mutations",
        "work/adversarial_proof_review/test_probe_input_mutations.py",
    )
    raw4_full_map = load(
        "k2p_test_raw4_full_map_mutations",
        "work/raw4_sign_reclassification/mutation_tests.py",
    )
    theta2_full_map = load(
        "k2p_test_theta2_full_map_mutations",
        "work/theta2_sign_reclassification/mutation_tests.py",
    )
    independent_probe = load(
        "k2p_test_independent_probe_mutations",
        "work/global_proof_adversary/probe_full_audit/independent_probe_graph_audit.py",
    )
    direct_closure = load(
        "k2p_test_direct_closure_mutations",
        "package/referee/k2p_offline_sweep_portable/"
        "test_direct_closure_release_mutations.py",
    )

    negative_controls = 0
    with tempfile.TemporaryDirectory(prefix="k2p-canonicalizer-contract-") as directory:
        root = Path(directory)
        artifact = Path(directory) / "success.json"
        stale_output = Path(directory) / "stale-pass.json"
        stale_output.write_text('{"status":"PASS"}\n')
        missing_dependency = root / "missing-dependency"
        missing_dependency.mkdir()
        (missing_dependency / "networkx.py").write_text(
            'raise ModuleNotFoundError("No module named \'networkx\'")\n'
        )
        environment = dict(os.environ)
        environment["PYTHONPATH"] = os.pathsep.join(
            filter(
                None,
                (
                    str(missing_dependency),
                    environment.get("PYTHONPATH", ""),
                ),
            )
        )
        dependency_attack = subprocess.run(
            [
                sys.executable,
                "-B",
                str(Path(canonicalizer.__file__).resolve()),
                "--output",
                str(stale_output),
            ],
            cwd=PROJECT,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        require(
            dependency_attack.returncode != 0
            and "CANONICALIZER_MUTATION_BASELINE_EXIT" in dependency_attack.stdout
            and "ModuleNotFoundError" in dependency_attack.stdout
            and not stale_output.exists(),
            "missing-dependency attack did not fail closed or retained stale PASS",
        )
        negative_controls += 1
        name = "accept_nonordinary_split_heads"
        expected = canonicalizer.MUTATION_DIAGNOSTICS[name]
        completed = SimpleNamespace(returncode=1, stdout=expected)
        accepted = canonicalizer.qualify_mutation_failure(name, completed, artifact)
        require(accepted["observed_diagnostic"] == expected, "canonical qualified drift")
        canonical_attacks = {
            "wrong diagnostic": SimpleNamespace(returncode=1, stdout=expected + ":wrong"),
            "missing dependency": SimpleNamespace(
                returncode=1,
                stdout="Traceback (most recent call last):\nModuleNotFoundError: No module named 'networkx'",
            ),
            "signal": SimpleNamespace(returncode=-9, stdout=""),
        }
        for label, attack in canonical_attacks.items():
            expect_failure(
                lambda attack=attack: canonicalizer.qualify_mutation_failure(
                    name, attack, artifact
                ),
                "CANONICALIZER_MUTATION_",
            )
        artifact.write_text("false success\n")
        expect_failure(
            lambda: canonicalizer.qualify_mutation_failure(name, completed, artifact),
            "CANONICALIZER_MUTATION_SUCCESS_ARTIFACT",
        )
        negative_controls += len(canonical_attacks) + 1

    with mock.patch.object(
        canonicalizer.subprocess,
        "run",
        side_effect=subprocess.TimeoutExpired(["python"], 60),
    ):
        expect_failure(
            lambda: canonicalizer.run_semantic_audit(
                canonicalizer.ATLAS, Path("/tmp/never-created-k2p-success.json")
            ),
            "CANONICALIZER_MUTATION_TIMEOUT",
        )
    negative_controls += 1

    negative_controls += exercise_dictionary_qualifier(
        restoration, "omitted_clean_first_edge"
    )
    negative_controls += exercise_dictionary_qualifier(probe, "omitted_anchor")
    negative_controls += exercise_dictionary_qualifier(unified, "omitted_raw_row")
    negative_controls += exercise_dictionary_qualifier(
        probe_input, "omitted_anchor_record"
    )
    negative_controls += exercise_dictionary_qualifier(
        raw4_full_map, "omitted_raw_record"
    )
    negative_controls += exercise_dictionary_qualifier(
        theta2_full_map, "omitted_truth_row"
    )
    negative_controls += exercise_dictionary_qualifier(direct_closure, "merged_root")
    accepted = independent_probe.qualify_in_process_mutation_failure(
        "qualified_control",
        "expected diagnostic",
        lambda _value: (_ for _ in ()).throw(
            independent_probe.AuditFailure("expected diagnostic")
        ),
        None,
    )
    require(
        accepted.get("observed_diagnostic") == "expected diagnostic",
        "independent-probe qualified diagnostic drift",
    )
    independent_controls = (
        independent_probe.run_mutation_qualification_negative_controls()
    )
    require(
        len(independent_controls) == 4 and all(independent_controls.values()),
        f"independent-probe negative controls:{independent_controls}",
    )
    negative_controls += len(independent_controls)
    timeout_error = subprocess.TimeoutExpired(
        ["python"], 1, output=b"partial-stdout", stderr=b"partial-stderr"
    )
    with tempfile.TemporaryDirectory(prefix="k2p-timeout-decoding-") as directory:
        root = Path(directory)
        with mock.patch.object(
            restoration.subprocess, "run", side_effect=timeout_error
        ):
            decoded = restoration.invoke_verifier(
                ["python"], root / "restoration-report.json", 1
            )
        require(
            decoded["timeout"] is True
            and decoded["diagnostic"] == "partial-stdoutpartial-stderr",
            f"restoration timeout decoding drift:{decoded}",
        )
        negative_controls += 1

        with mock.patch.object(probe.subprocess, "run", side_effect=timeout_error):
            decoded = probe.run_verifier(root)
        require(
            decoded["timeout"] is True
            and decoded["diagnostic"] == "partial-stdoutpartial-stderr",
            f"probe timeout decoding drift:{decoded}",
        )
        negative_controls += 1
    with tempfile.TemporaryDirectory(prefix="k2p-restoration-stale-report-") as directory:
        stale_report = Path(directory) / "stale-pass.json"
        stale_report.write_text('{"status":"PASS"}\n')
        with mock.patch.dict(
            os.environ,
            {restoration.LEGACY_WORKER_ENV: "omitted_clean_first_edge"},
            clear=False,
        ):
            expect_failure(
                lambda: restoration.prepare_public_run(stale_report),
                "legacy ambient worker selector forbidden",
            )
        require(not stale_report.exists(), "stale restoration report survived")
    negative_controls += 1
    authoritative_before = restoration.sha_file(restoration.AUTHORITATIVE_OUTPUT)
    environment = dict(os.environ)
    environment.pop(restoration.LEGACY_WORKER_ENV, None)
    environment.pop(restoration.INTERNAL_NONCE_ENV, None)
    unauthorized = subprocess.run(
        [
            sys.executable,
            "-B",
            str(Path(restoration.__file__).resolve()),
            "--internal-worker",
            "omitted_clean_first_edge",
            "--parent-nonce",
            "0" * 64,
        ],
        cwd=PROJECT,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    require(
        unauthorized.returncode != 0
        and "internal worker parent nonce" in unauthorized.stdout
        and restoration.sha_file(restoration.AUTHORITATIVE_OUTPUT)
        == authoritative_before,
        f"unauthorized internal worker accepted:{unauthorized.stdout[-1000:]}",
    )
    negative_controls += 1
    require(negative_controls == 49, f"negative control census:{negative_controls}")
    print(
        "K2P_SEMANTIC_MUTATION_DIAGNOSTIC_CONTRACTS_PASS "
        "qualified=9 negative_controls=49"
    )


if __name__ == "__main__":
    main()
