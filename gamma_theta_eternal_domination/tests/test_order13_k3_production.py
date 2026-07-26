from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from synthesis_k3.cegar import ChildResult, _command_sha256  # noqa: E402
from search.order13_k3.generate import (  # noqa: E402
    canonical_json_bytes,
    generate_package,
)
from search.order13_k3.normalize_bdrat import (  # noqa: E402
    NormalizationError,
    normalize_binary_drat,
)
from search.order13_k3.production import (  # noqa: E402
    ACCEPTED_TOOL_SHA256,
    FINAL_SUCCESS,
    FROZEN_TOOL_IDENTITY,
    INSTANCE_NAME,
    RECOVERED_OUTCOME_STATUS,
    RECOVERY_REASON,
    SAT_CANDIDATE,
    _append_checkpoint,
    _audit_resource_gate,
    _binding,
    _commands,
    _load_run,
    _strict_verified,
    _tool_identity,
    _validate_limits,
    _validate_normalization,
    audit,
    initialize,
    run,
)


def _limits() -> dict[str, object]:
    return {
        "solver_wall_seconds": 2,
        "postprocess_wall_seconds": 2,
        "solver_memory_mib": 64,
        "postprocess_memory_mib": 64,
        "file_limit_mib": 64,
        "disk_reserve_mib": 8192,
        "memory_reserve_mib": 512,
        "load_max": 1000.0,
        "parallel_children": 1,
    }


class Order13K3ProductionTests(unittest.TestCase):
    def setUp(self) -> None:
        fake_hashes = {
            role: hashlib.sha256((name + "\n").encode("ascii")).hexdigest()
            for role, name in (
                ("cadical", "cadical"),
                ("drat_trim", "drat-trim"),
                ("lrat_check", "lrat-check"),
            )
        }
        self.tool_policy_patch = patch.dict(
            ACCEPTED_TOOL_SHA256, fake_hashes, clear=True
        )
        self.tool_policy_patch.start()

    def tearDown(self) -> None:
        self.tool_policy_patch.stop()

    def _foundation(self, root: Path) -> tuple[Path, dict[str, Path]]:
        package = root / "package"
        generate_package(
            template="hole11",
            output_directory=package,
            validation_gate=True,
        )
        tools: dict[str, Path] = {}
        for name in ("cadical", "drat-trim", "lrat-check"):
            path = root / name
            path.write_bytes((name + "\n").encode("ascii"))
            path.chmod(0o700)
            tools[name] = path
        tools["python"] = Path(sys.executable).resolve()
        return package, tools

    def test_repository_production_tool_hashes_are_the_frozen_policy(self) -> None:
        # setUp replaces the mutable test-policy mapping, so compare against
        # the immutable production values explicitly.
        expected = {
            "cadical": "51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6",
            "drat_trim": "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb",
            "lrat_check": "5d7d77a57457db82e57f2505ea9d0267ff0bceff197235b6edfc8fda1f26c7a2",
        }
        paths = {
            "cadical": CAMPAIGN / "tools/cadical_3_0_1/build/cadical",
            "drat_trim": CAMPAIGN / "tools/drat_trim_2023_05_22/drat-trim",
            "lrat_check": CAMPAIGN / "tools/drat_trim_2023_05_22/lrat-check",
        }
        self.assertEqual(
            {
                role: hashlib.sha256(path.read_bytes()).hexdigest()
                for role, path in paths.items()
            },
            expected,
        )

    def test_repository_hole9_raw_proof_passes_plain_rup_gate(self) -> None:
        certificate = (
            CAMPAIGN
            / "certificates/order13_k3_hole9_attempt000001_lrat"
        )
        command = [
            str(CAMPAIGN / "tools/drat_trim_2023_05_22/drat-trim"),
            str(certificate / "instance.cnf"),
            str(certificate / "proof.raw.bdrat"),
            "-i",
            "-f",
            "-p",
            "-W",
            "-U",
            "-t",
            "30",
        ]
        completed = subprocess.run(
            command,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=40,
        )
        self.assertEqual(completed.returncode, 0)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            stdout = root / "stdout"
            stderr = root / "stderr"
            stdout.write_bytes(completed.stdout)
            stderr.write_bytes(completed.stderr)
            _strict_verified(stdout, stderr, "s VERIFIED")
        self.assertIn(b"0 RAT lemmas in core", completed.stdout)

    def test_initialize_is_generic_over_all_four_templates(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            _, tools = self._foundation(root)
            for template in ("hole5", "hole7", "hole9", "hole11"):
                package = root / f"package-{template}"
                generate_package(
                    template=template,
                    output_directory=package,
                    validation_gate=True,
                )
                run_directory = root / f"run-{template}"
                initialize(
                    package_directory=package,
                    run_directory=run_directory,
                    cadical_path=tools["cadical"],
                    drat_trim_path=tools["drat-trim"],
                    lrat_check_path=tools["lrat-check"],
                    normalizer_python_path=tools["python"],
                    seed=0,
                    limits=_limits(),
                    validation_gate=True,
                )
                report = audit(run_directory)
                self.assertEqual(report["template"], template)
                self.assertEqual(report["status"], "PENDING")

    def test_raw_forward_command_is_plain_warning_fatal_rup_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run_directory, _ = self._initialize(root)
            manifest, _, _, _ = _load_run(run_directory)
            command = _commands(manifest, root / "fresh-attempt")[
                "raw_forward"
            ]
            self.assertEqual(
                command[-7:],
                ["-i", "-f", "-p", "-W", "-U", "-t", "2"],
            )
            self.assertEqual(command.count("-p"), 1)
            self.assertEqual(command.count("-W"), 1)
            self.assertEqual(command.count("-U"), 1)

    def _initialize(
        self, root: Path
    ) -> tuple[Path, dict[str, Path]]:
        package, tools = self._foundation(root)
        run_directory = root / "run"
        initialize(
            package_directory=package,
            run_directory=run_directory,
            cadical_path=tools["cadical"],
            drat_trim_path=tools["drat-trim"],
            lrat_check_path=tools["lrat-check"],
            normalizer_python_path=tools["python"],
            seed=0,
            limits=_limits(),
            validation_gate=True,
        )
        return run_directory, tools

    def _rewrite_manifest(
        self,
        run_directory: Path,
        mutation: object,
    ) -> tuple[bytes, bytes]:
        manifest_path = run_directory / "run-manifest.json"
        checkpoint_path = (
            run_directory / "checkpoints" / "checkpoint-000000.json"
        )
        original_manifest = manifest_path.read_bytes()
        original_checkpoint = checkpoint_path.read_bytes()
        manifest = json.loads(original_manifest)
        mutation(manifest)
        payload = canonical_json_bytes(manifest)
        manifest_path.write_bytes(payload)
        checkpoint = json.loads(original_checkpoint)
        checkpoint["run_manifest_sha256"] = hashlib.sha256(payload).hexdigest()
        checkpoint_path.write_bytes(canonical_json_bytes(checkpoint))
        return original_manifest, original_checkpoint

    def _restore_manifest(
        self,
        run_directory: Path,
        originals: tuple[bytes, bytes],
    ) -> None:
        (run_directory / "run-manifest.json").write_bytes(originals[0])
        (
            run_directory / "checkpoints" / "checkpoint-000000.json"
        ).write_bytes(originals[1])

    def _create_running_attempt(
        self,
        run_directory: Path,
    ) -> tuple[
        dict[str, object],
        str,
        Path,
        dict[str, object],
        str,
        dict[str, object],
    ]:
        manifest, manifest_hash, latest, latest_hash = _load_run(run_directory)
        attempt = run_directory / "attempts" / "attempt-000001"
        attempt.mkdir()
        (attempt / INSTANCE_NAME).write_bytes(
            (run_directory / INSTANCE_NAME).read_bytes()
        )
        config = {
            "schema": "gamma-theta-order13-k3-attempt-config-v1",
            "schema_version": 1,
            "claim_status": "NO_SAT_OR_UNSAT_CLAIM_BEFORE_EXECUTION",
            "proof_pipeline": manifest["proof_pipeline"],
            "attempt_number": 1,
            "template": manifest["template"],
            "seed": manifest["seed"],
            "run_manifest_sha256": manifest_hash,
            "instance": _binding(attempt / INSTANCE_NAME, "attempt instance"),
            "runtime_source_set_sha256": manifest[
                "runtime_source_set_sha256"
            ],
            "tools": manifest["tools"],
            "limits": manifest["limits"],
            "commands": _commands(manifest, attempt),
            "created_unix_ns": 1,
        }
        config_path = attempt / "attempt-config.json"
        config_path.write_bytes(canonical_json_bytes(config))
        running, running_hash = _append_checkpoint(
            run_directory,
            manifest_hash=manifest_hash,
            previous_hash=latest_hash,
            previous=latest,
            status="RUNNING_UNFINISHED_NONCLAIM",
            event="RUN_STARTED",
            attempt_binding=_binding(config_path, "attempt config"),
            outcome_binding=None,
        )
        return (
            manifest,
            manifest_hash,
            attempt,
            running,
            running_hash,
            config,
        )

    def _refresh_success_metadata(self, run_directory: Path) -> None:
        attempt = run_directory / "attempts" / "attempt-000001"
        config_path = attempt / "attempt-config.json"
        certificate_path = attempt / "certificate.json"
        outcome_path = attempt / "outcome.json"
        certificate = json.loads(certificate_path.read_bytes())
        outcome = json.loads(outcome_path.read_bytes())
        outcome["details"] = {"certificate": certificate}
        outcome["artifacts"] = {
            path.name: _binding(path, f"refreshed {path.name}")
            for path in attempt.iterdir()
            if path.name != "outcome.json"
        }
        outcome_path.write_bytes(canonical_json_bytes(outcome))

        checkpoint_one_path = (
            run_directory / "checkpoints" / "checkpoint-000001.json"
        )
        checkpoint_one = json.loads(checkpoint_one_path.read_bytes())
        checkpoint_one["attempt"] = _binding(
            config_path, "refreshed attempt config"
        )
        checkpoint_one_path.write_bytes(
            canonical_json_bytes(checkpoint_one)
        )

        checkpoint_two_path = (
            run_directory / "checkpoints" / "checkpoint-000002.json"
        )
        checkpoint_two = json.loads(checkpoint_two_path.read_bytes())
        checkpoint_two["previous_checkpoint_sha256"] = hashlib.sha256(
            checkpoint_one_path.read_bytes()
        ).hexdigest()
        checkpoint_two["attempt"] = _binding(
            config_path, "refreshed attempt config"
        )
        checkpoint_two["outcome"] = _binding(
            outcome_path, "refreshed attempt outcome"
        )
        checkpoint_two_path.write_bytes(
            canonical_json_bytes(checkpoint_two)
        )

    def _fake_complete_child(self, **keywords: object) -> ChildResult:
        command = tuple(keywords["command"])
        stdout = Path(keywords["stdout_path"])
        stderr = Path(keywords["stderr_path"])
        phase = stdout.name.removesuffix(".stdout")
        stderr.write_bytes(b"")
        exit_code = 0
        if phase == "solver":
            exit_code = 20
            Path(command[command.index("-w") + 1]).write_bytes(
                b"s UNSATISFIABLE\n"
            )
            Path(command[-1]).write_bytes(b"a\x00")
            stdout.write_bytes(b"")
        elif phase == "normalizer":
            from search.order13_k3.normalize_bdrat import (
                normalize_binary_drat,
            )

            normalize_binary_drat(
                Path(command[command.index("--input") + 1]),
                Path(command[command.index("--output") + 1]),
                Path(command[command.index("--report") + 1]),
                max_variable=int(
                    command[command.index("--max-variable") + 1]
                ),
            )
            stdout.write_bytes(b"s NORMALIZED\n")
        elif phase == "lrat_conversion":
            Path(command[command.index("-L") + 1]).write_bytes(
                b"1 0 0\n"
            )
            stdout.write_bytes(b"s VERIFIED\n")
        elif phase == "lrat_check":
            stdout.write_bytes(b"c VERIFIED\n")
        else:
            stdout.write_bytes(b"s VERIFIED\n")
        executable_hash = hashlib.sha256(
            Path(command[0]).read_bytes()
        ).hexdigest()
        return ChildResult(
            command=command,
            command_sha256=_command_sha256(command),
            executable_sha256_before=executable_hash,
            executable_sha256_after=executable_hash,
            exit_code=exit_code,
            termination_signal=None,
            timed_out=False,
            memory_limit_exceeded=False,
            started_unix_ns=1,
            finished_unix_ns=2,
            wall_seconds=0.001,
            user_cpu_seconds=0.0,
            system_cpu_seconds=0.0,
            maximum_resident_set_size_mib=1.0,
            maximum_resident_set_size_raw=1,
            maximum_resident_set_size_raw_unit="bytes",
            peak_polled_resident_set_size_mib=1.0,
            available_memory_before_bytes=16 << 30,
            wall_limit_seconds=int(keywords["wall_limit_seconds"]),
            memory_limit_mib=int(keywords["memory_limit_mib"]),
            file_limit_mib=int(keywords["file_limit_mib"]),
            stdout_path=str(stdout.resolve()),
            stdout_sha256=hashlib.sha256(stdout.read_bytes()).hexdigest(),
            stderr_path=str(stderr.resolve()),
            stderr_sha256=hashlib.sha256(stderr.read_bytes()).hexdigest(),
        )

    def _run_fake_complete_success(
        self, run_directory: Path
    ) -> dict[str, object]:
        with patch(
            "search.order13_k3.production._available_memory_bytes",
            return_value=16 << 30,
        ), patch(
            "search.order13_k3.production.run_bounded_child",
            side_effect=self._fake_complete_child,
        ):
            return run(
                run_directory,
                production_gate=True,
                recover_interrupted=False,
            )

    def test_normalizer_exact_stream_and_mutations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            source = root / "raw.bdrat"
            output = root / "normalized.bdrat"
            report = root / "report.json"
            # add {+2}, delete {+2}, then the unique empty addition
            source.write_bytes(b"a\x04\x00d\x04\x00a\x00")
            result = normalize_binary_drat(
                source, output, report, max_variable=9802
            )
            self.assertEqual(output.read_bytes(), b"a\x04\x00a\x00")
            self.assertEqual(result["empty_addition_record_index"], 3)
            self.assertEqual(result["record_counts"]["deletions"], 1)
            _validate_normalization(report, source, output)
            injected = json.loads(report.read_bytes())
            injected["asserted_proof_verified"] = True
            report.write_bytes(canonical_json_bytes(injected))
            with self.assertRaises(ValueError):
                _validate_normalization(report, source, output)
            report.write_bytes(canonical_json_bytes(result))

            for index, payload in enumerate(
                (
                    b"a\x00a\x00",
                    b"a\x00a\x04\x00",
                    b"d\x00a\x00",
                    b"a\x04",
                    b"x\x00",
                    b"a\x80\x00",
                )
            ):
                bad = root / f"bad-{index}.bdrat"
                bad_output = root / f"bad-{index}.normalized"
                bad_report = root / f"bad-{index}.json"
                bad.write_bytes(payload)
                with self.assertRaises(NormalizationError):
                    normalize_binary_drat(
                        bad, bad_output, bad_report, max_variable=20
                    )
                self.assertFalse(bad_output.exists())
                self.assertFalse(bad_report.exists())

    def test_warning_fatal_output_and_limit_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            stdout = root / "stdout"
            stderr = root / "stderr"
            stderr.write_bytes(b"")
            stdout.write_bytes(b"c warning: ignored\ns VERIFIED\n")
            with self.assertRaises(ValueError):
                _strict_verified(stdout, stderr, "s VERIFIED")
            stdout.write_bytes(b"s VERIFIED\n")
            stderr.write_bytes(b"warning\n")
            with self.assertRaises(ValueError):
                _strict_verified(stdout, stderr, "s VERIFIED")
            stderr.write_bytes(b"")
            _strict_verified(stdout, stderr, "s VERIFIED")

        too_much_memory = _limits()
        too_much_memory["solver_memory_mib"] = 2049
        with self.assertRaises(ValueError):
            _validate_limits(too_much_memory)
        too_much_file = _limits()
        too_much_file["file_limit_mib"] = 2049
        with self.assertRaises(ValueError):
            _validate_limits(too_much_file)
        too_little_reserve = _limits()
        too_little_reserve["disk_reserve_mib"] = 8191
        with self.assertRaises(ValueError):
            _validate_limits(too_little_reserve)

    def test_initialize_audit_tool_and_formula_mutations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            package, tools = self._foundation(root)
            run_directory = root / "run"
            with self.assertRaises(PermissionError):
                initialize(
                    package_directory=package,
                    run_directory=run_directory,
                    cadical_path=tools["cadical"],
                    drat_trim_path=tools["drat-trim"],
                    lrat_check_path=tools["lrat-check"],
                    normalizer_python_path=tools["python"],
                    seed=0,
                    limits=_limits(),
                    validation_gate=False,
                )
            self.assertFalse(run_directory.exists())
            result = initialize(
                package_directory=package,
                run_directory=run_directory,
                cadical_path=tools["cadical"],
                drat_trim_path=tools["drat-trim"],
                lrat_check_path=tools["lrat-check"],
                normalizer_python_path=tools["python"],
                seed=0,
                limits=_limits(),
                validation_gate=True,
            )
            self.assertFalse(result["child_launched"])
            self.assertEqual(audit(run_directory)["status"], "PENDING")
            with self.assertRaises(PermissionError):
                run(
                    run_directory,
                    production_gate=False,
                    recover_interrupted=False,
                )
            self.assertEqual(audit(run_directory)["attempt_count"], 0)

            instance = run_directory / INSTANCE_NAME
            original_instance = instance.read_bytes()
            instance.write_bytes(original_instance[:-1] + b" ")
            with self.assertRaises(ValueError):
                audit(run_directory)
            instance.write_bytes(original_instance)

            tool = tools["lrat-check"]
            original_tool = tool.read_bytes()
            tool.write_bytes(b"mutated\n")
            with self.assertRaises(ValueError):
                audit(run_directory)
            tool.write_bytes(original_tool)
            self.assertTrue(audit(run_directory)["accepted"])

    def test_transitive_helper_source_mutations_refuse_before_child(self) -> None:
        newly_bound = (
            CAMPAIGN / "src/synthesis_k3/__init__.py",
            CAMPAIGN / "src/synthesis_k3/encoding.py",
            CAMPAIGN / "src/synthesis_k3/coloring.py",
            CAMPAIGN / "src/synthesis_k3/generate.py",
        )
        originals = {path: path.read_bytes() for path in newly_bound}
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run_directory, _ = self._initialize(root)
            try:
                for path in newly_bound:
                    with self.subTest(source=path.name):
                        path.write_bytes(originals[path] + b"\n")
                        with self.assertRaises(ValueError):
                            audit(run_directory)
                        with patch(
                            "search.order13_k3.production.run_bounded_child"
                        ) as child:
                            with self.assertRaises(ValueError):
                                run(
                                    run_directory,
                                    production_gate=True,
                                    recover_interrupted=False,
                                )
                        child.assert_not_called()
                        path.write_bytes(originals[path])
                        self.assertTrue(audit(run_directory)["accepted"])
            finally:
                for path, payload in originals.items():
                    path.write_bytes(payload)

    def test_tool_identity_mutations_refuse_before_child(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run_directory, _ = self._initialize(root)
            cases = (
                patch(
                    "search.order13_k3.production.platform.python_version",
                    return_value="0.invalid-test-version",
                ),
                patch.dict(
                    FROZEN_TOOL_IDENTITY["cadical"],
                    {"version": "invalid-test-version"},
                ),
            )
            for mutation in cases:
                with self.subTest(mutation=repr(mutation)), mutation:
                    with self.assertRaises(ValueError):
                        audit(run_directory)
                    with patch(
                        "search.order13_k3.production.run_bounded_child"
                    ) as child:
                        with self.assertRaises(ValueError):
                            run(
                                run_directory,
                                production_gate=True,
                                recover_interrupted=False,
                            )
                    child.assert_not_called()
            self.assertTrue(audit(run_directory)["accepted"])

    def test_coordinated_tool_rebinding_refuses_before_child(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run_directory, _ = self._initialize(root)
            for role in (
                "cadical",
                "drat_trim",
                "lrat_check",
                "normalizer_python",
            ):
                with self.subTest(role=role):
                    rebound = root / f"rebound-{role}"
                    rebound.write_bytes(f"rebound-{role}\n".encode("ascii"))
                    rebound.chmod(0o700)

                    def mutate(manifest: dict[str, object]) -> None:
                        tools = manifest["tools"]
                        self.assertIsInstance(tools, dict)
                        tools[role] = _binding(rebound, f"rebound {role}")
                        manifest["tool_identity"] = _tool_identity(tools)

                    originals = self._rewrite_manifest(
                        run_directory, mutate
                    )
                    try:
                        with self.assertRaises(ValueError):
                            audit(run_directory)
                        with patch(
                            "search.order13_k3.production.run_bounded_child"
                        ) as child:
                            with self.assertRaises(ValueError):
                                run(
                                    run_directory,
                                    production_gate=True,
                                    recover_interrupted=False,
                                )
                        child.assert_not_called()
                    finally:
                        self._restore_manifest(run_directory, originals)
                    self.assertTrue(audit(run_directory)["accepted"])

    def test_run_manifest_semantic_mutations_reject_after_rehash(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run_directory, _ = self._initialize(root)

            def extra_claim(manifest: dict[str, object]) -> None:
                manifest["asserted_resolution"] = True

            def wrong_claim_status(manifest: dict[str, object]) -> None:
                manifest["claim_status"] = "FORMULA_UNSAT"

            def zero_timestamp(manifest: dict[str, object]) -> None:
                manifest["created_unix_ns"] = 0

            def invalid_hardware(manifest: dict[str, object]) -> None:
                manifest["hardware"]["logical_cpus"] = 0

            def forged_invocation(manifest: dict[str, object]) -> None:
                manifest["normalized_resume_invocation"].append("--forged")

            for name, mutation in (
                ("extra_claim", extra_claim),
                ("claim_status", wrong_claim_status),
                ("timestamp", zero_timestamp),
                ("hardware", invalid_hardware),
                ("invocation", forged_invocation),
            ):
                with self.subTest(name=name):
                    originals = self._rewrite_manifest(
                        run_directory, mutation
                    )
                    try:
                        with self.assertRaises(ValueError):
                            audit(run_directory)
                        with patch(
                            "search.order13_k3.production.run_bounded_child"
                        ) as child:
                            with self.assertRaises(ValueError):
                                run(
                                    run_directory,
                                    production_gate=True,
                                    recover_interrupted=False,
                                )
                        child.assert_not_called()
                    finally:
                        self._restore_manifest(run_directory, originals)
                    self.assertTrue(audit(run_directory)["accepted"])

    def test_external_checkpoint_success_forgery_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run_directory, _ = self._initialize(root)
            _, manifest_hash, latest, latest_hash = _load_run(run_directory)
            external = root / "external"
            external.mkdir()
            config_path = external / "attempt-config.json"
            outcome_path = external / "outcome.json"
            config_path.write_bytes(
                canonical_json_bytes({"external": "not an attempt config"})
            )
            outcome_path.write_bytes(
                canonical_json_bytes({"status": FINAL_SUCCESS})
            )
            running, running_hash = _append_checkpoint(
                run_directory,
                manifest_hash=manifest_hash,
                previous_hash=latest_hash,
                previous=latest,
                status="RUNNING_UNFINISHED_NONCLAIM",
                event="RUN_STARTED",
                attempt_binding=_binding(config_path, "external config"),
                outcome_binding=None,
            )
            _append_checkpoint(
                run_directory,
                manifest_hash=manifest_hash,
                previous_hash=running_hash,
                previous=running,
                status=FINAL_SUCCESS,
                event="RUN_FINISHED",
                attempt_binding=_binding(config_path, "external config"),
                outcome_binding=_binding(outcome_path, "external outcome"),
            )
            self.assertEqual(
                list((run_directory / "attempts").iterdir()), []
            )
            with self.assertRaises(ValueError):
                audit(run_directory)

    def test_checkpoint_attempt_path_and_count_forgeries_are_rejected(self) -> None:
        for case in ("traversal", "wrong_number", "orphan", "missing_outcome"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                run_directory, _ = self._initialize(root)
                if case == "orphan":
                    (run_directory / "attempts" / "attempt-000001").mkdir()
                    with self.assertRaises(ValueError):
                        audit(run_directory)
                    continue

                (
                    _,
                    manifest_hash,
                    attempt,
                    running,
                    running_hash,
                    _,
                ) = self._create_running_attempt(run_directory)
                if case == "traversal":
                    checkpoint = (
                        run_directory
                        / "checkpoints"
                        / "checkpoint-000001.json"
                    )
                    payload = json.loads(checkpoint.read_bytes())
                    payload["attempt"]["path"] = str(
                        attempt
                        / ".."
                        / "attempt-000001"
                        / "attempt-config.json"
                    )
                    checkpoint.write_bytes(canonical_json_bytes(payload))
                    with self.assertRaises(ValueError):
                        audit(run_directory)
                    continue
                if case == "wrong_number":
                    wrong = (
                        run_directory / "attempts" / "attempt-000002"
                    )
                    wrong.mkdir()
                    wrong_config = wrong / "attempt-config.json"
                    wrong_config.write_bytes(
                        (attempt / "attempt-config.json").read_bytes()
                    )
                    checkpoint = (
                        run_directory
                        / "checkpoints"
                        / "checkpoint-000001.json"
                    )
                    payload = json.loads(checkpoint.read_bytes())
                    payload["attempt"] = _binding(
                        wrong_config, "wrong-number config"
                    )
                    checkpoint.write_bytes(canonical_json_bytes(payload))
                    with self.assertRaises(ValueError):
                        audit(run_directory)
                    continue

                outcome_path = attempt / "outcome.json"
                outcome = {
                    "schema": "gamma-theta-order13-k3-attempt-outcome-v1",
                    "schema_version": 1,
                    "status": "RETRYABLE_NONCLAIM",
                    "claim_status": "NO_SAT_OR_UNSAT_CLAIM",
                    "details": {
                        "phase_status": "TEST_RETRY_NONCLAIM",
                        "phase_details": {},
                    },
                    "artifacts": {
                        path.name: _binding(path, path.name)
                        for path in attempt.iterdir()
                    },
                    "finished_unix_ns": 2,
                }
                outcome_path.write_bytes(canonical_json_bytes(outcome))
                _append_checkpoint(
                    run_directory,
                    manifest_hash=manifest_hash,
                    previous_hash=running_hash,
                    previous=running,
                    status="RETRYABLE_NONCLAIM",
                    event="RUN_FINISHED",
                    attempt_binding=_binding(
                        attempt / "attempt-config.json", "attempt config"
                    ),
                    outcome_binding=_binding(outcome_path, "attempt outcome"),
                )
                outcome_path.unlink()
                with self.assertRaises(ValueError):
                    audit(run_directory)

    def test_attempt_instance_must_match_frozen_formula_contents(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run_directory, _ = self._initialize(root)
            (
                _,
                _,
                attempt,
                _,
                _,
                config,
            ) = self._create_running_attempt(run_directory)
            instance = attempt / INSTANCE_NAME
            instance.write_bytes(b"p cnf 1 2\n1 0\n-1 0\n")
            config["instance"] = _binding(
                instance, "coherently substituted attempt instance"
            )
            config_path = attempt / "attempt-config.json"
            config_path.write_bytes(canonical_json_bytes(config))
            checkpoint = (
                run_directory
                / "checkpoints"
                / "checkpoint-000001.json"
            )
            checkpoint_payload = json.loads(checkpoint.read_bytes())
            checkpoint_payload["attempt"] = _binding(
                config_path, "refreshed substituted config"
            )
            checkpoint.write_bytes(
                canonical_json_bytes(checkpoint_payload)
            )
            with self.assertRaisesRegex(
                ValueError, "attempt configuration differs from frozen inputs"
            ):
                audit(run_directory)

    def test_recovery_event_cannot_promote_success_or_candidate(self) -> None:
        for forged_status in (FINAL_SUCCESS, SAT_CANDIDATE):
            with self.subTest(status=forged_status), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                run_directory, _ = self._initialize(root)
                (
                    _,
                    manifest_hash,
                    attempt,
                    running,
                    running_hash,
                    _,
                ) = self._create_running_attempt(run_directory)
                outcome_path = attempt / "outcome.json"
                outcome = {
                    "schema": "gamma-theta-order13-k3-attempt-outcome-v1",
                    "schema_version": 1,
                    "status": RECOVERED_OUTCOME_STATUS,
                    "claim_status": "NO_SAT_OR_UNSAT_CLAIM",
                    "reason": RECOVERY_REASON,
                    "artifacts": {
                        path.name: _binding(path, path.name)
                        for path in attempt.iterdir()
                    },
                    "finished_unix_ns": 2,
                }
                outcome_path.write_bytes(canonical_json_bytes(outcome))
                _append_checkpoint(
                    run_directory,
                    manifest_hash=manifest_hash,
                    previous_hash=running_hash,
                    previous=running,
                    status=forged_status,
                    event="INTERRUPTED_RECOVERED",
                    attempt_binding=_binding(
                        attempt / "attempt-config.json", "attempt config"
                    ),
                    outcome_binding=_binding(outcome_path, "attempt outcome"),
                )
                with self.assertRaises(ValueError):
                    audit(run_directory)

    def test_sat_resource_gate_mutations_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            attempt = Path(temporary).resolve()
            limits = _limits()
            required_memory = (
                int(limits["solver_memory_mib"])
                + int(limits["memory_reserve_mib"])
            ) << 20
            required_disk = (
                int(limits["disk_reserve_mib"])
                + 5 * int(limits["file_limit_mib"])
                + 64
            ) << 20
            clean = {
                "schema": "gamma-theta-order13-k3-resource-gate-v1",
                "phase": "solver",
                "checked_unix_ns": 1,
                "load_average_one_minute": 0.0,
                "load_ceiling": limits["load_max"],
                "available_memory_bytes": required_memory,
                "required_memory_bytes": required_memory,
                "free_disk_bytes": required_disk,
                "required_free_disk_bytes": required_disk,
                "live_file_slots": 5,
                "probe_errors": [],
                "checks": {"load": True, "memory": True, "disk": True},
                "passed": True,
            }
            resource = attempt / "resource-solver.json"
            resource.write_bytes(canonical_json_bytes(clean))
            _audit_resource_gate(attempt, "solver", limits)
            for name, mutation in (
                ("passed", lambda value: value.update(passed=False)),
                (
                    "checks",
                    lambda value: value["checks"].update(memory=False),
                ),
                ("timestamp", lambda value: value.update(checked_unix_ns=0)),
                ("extra", lambda value: value.update(false_claim=True)),
            ):
                with self.subTest(name=name):
                    mutated = json.loads(canonical_json_bytes(clean))
                    mutation(mutated)
                    resource.write_bytes(canonical_json_bytes(mutated))
                    with self.assertRaises(ValueError):
                        _audit_resource_gate(attempt, "solver", limits)

    def test_interrupted_attempt_requires_explicit_recovery(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run_directory, _ = self._initialize(root)
            manifest, manifest_hash, latest, latest_hash = _load_run(run_directory)
            attempt = run_directory / "attempts" / "attempt-000001"
            attempt.mkdir()
            (attempt / INSTANCE_NAME).write_bytes(
                (run_directory / INSTANCE_NAME).read_bytes()
            )
            commands = _commands(manifest, attempt)
            config = {
                "schema": "gamma-theta-order13-k3-attempt-config-v1",
                "schema_version": 1,
                "claim_status": "NO_SAT_OR_UNSAT_CLAIM_BEFORE_EXECUTION",
                "proof_pipeline": manifest["proof_pipeline"],
                "attempt_number": 1,
                "template": manifest["template"],
                "seed": manifest["seed"],
                "run_manifest_sha256": manifest_hash,
                "instance": _binding(attempt / INSTANCE_NAME, "attempt instance"),
                "runtime_source_set_sha256": manifest[
                    "runtime_source_set_sha256"
                ],
                "tools": manifest["tools"],
                "limits": manifest["limits"],
                "commands": commands,
                "created_unix_ns": 1,
            }
            config_path = attempt / "attempt-config.json"
            config_path.write_bytes(
                (
                    json.dumps(config, allow_nan=False, indent=2, sort_keys=True)
                    + "\n"
                ).encode("utf-8")
            )
            running, _ = _append_checkpoint(
                run_directory,
                manifest_hash=manifest_hash,
                previous_hash=latest_hash,
                previous=latest,
                status="RUNNING_UNFINISHED_NONCLAIM",
                event="RUN_STARTED",
                attempt_binding=_binding(config_path, "attempt config"),
                outcome_binding=None,
            )
            self.assertEqual(running["status"], "RUNNING_UNFINISHED_NONCLAIM")
            with self.assertRaises(RuntimeError):
                run(
                    run_directory,
                    production_gate=True,
                    recover_interrupted=False,
                )
            recovered = run(
                run_directory,
                production_gate=True,
                recover_interrupted=True,
            )
            self.assertFalse(recovered["child_launched"])
            self.assertEqual(recovered["status"], "RETRYABLE_NONCLAIM")
            self.assertEqual(audit(run_directory)["attempt_count"], 1)

    def test_uncheckpointed_durable_outcome_is_quarantined(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run_directory, _ = self._initialize(root)
            (
                _,
                _,
                attempt,
                _,
                _,
                _,
            ) = self._create_running_attempt(run_directory)
            outcome = {
                "schema": "gamma-theta-order13-k3-attempt-outcome-v1",
                "schema_version": 1,
                "status": "RETRYABLE_NONCLAIM",
                "claim_status": "NO_SAT_OR_UNSAT_CLAIM",
                "details": {
                    "phase_status": "TEST_CRASH_WINDOW_NONCLAIM",
                    "phase_details": {},
                },
                "artifacts": {
                    path.name: _binding(path, path.name)
                    for path in attempt.iterdir()
                },
                "finished_unix_ns": 2,
            }
            (attempt / "outcome.json").write_bytes(
                canonical_json_bytes(outcome)
            )
            with self.assertRaisesRegex(
                ValueError, "running attempt unexpectedly has an outcome"
            ):
                audit(run_directory)
            recovered = run(
                run_directory,
                production_gate=True,
                recover_interrupted=True,
            )
            self.assertEqual(recovered["status"], "RETRYABLE_NONCLAIM")
            self.assertTrue(recovered["durable_outcome_quarantined"])
            self.assertTrue(
                recovered["uncheckpointed_outcome_quarantined"]
            )
            self.assertFalse(recovered["child_launched"])
            self.assertTrue(
                Path(recovered["quarantine"]["quarantined_path"]).is_file()
            )
            report = audit(run_directory)
            self.assertEqual(report["status"], "RETRYABLE_NONCLAIM")
            self.assertEqual(report["attempt_count"], 1)

    def test_partial_uncheckpointed_outcome_is_quarantined(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run_directory, _ = self._initialize(root)
            _, _, attempt, _, _, _ = self._create_running_attempt(
                run_directory
            )
            partial = b'{"schema":"partial"'
            (attempt / "outcome.json").write_bytes(partial)
            with self.assertRaisesRegex(
                ValueError, "running attempt unexpectedly has an outcome"
            ):
                audit(run_directory)
            recovered = run(
                run_directory,
                production_gate=True,
                recover_interrupted=True,
            )
            self.assertEqual(recovered["status"], "RETRYABLE_NONCLAIM")
            self.assertTrue(
                recovered["uncheckpointed_outcome_quarantined"]
            )
            quarantined = Path(
                recovered["quarantine"]["quarantined_path"]
            )
            self.assertEqual(quarantined.read_bytes(), partial)
            canonical_recovery = json.loads(
                (attempt / "outcome.json").read_bytes()
            )
            self.assertEqual(
                canonical_recovery["status"], RECOVERED_OUTCOME_STATUS
            )
            self.assertEqual(canonical_recovery["reason"], RECOVERY_REASON)
            self.assertEqual(
                audit(run_directory)["status"], "RETRYABLE_NONCLAIM"
            )

    def test_precheckpoint_orphan_recovery_all_creation_windows(self) -> None:
        stages = (
            "after_mkdir",
            "after_instance_copy",
            "after_config_write",
            "immediately_before_checkpoint",
        )
        for stage in stages:
            with self.subTest(stage=stage), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                run_directory, _ = self._initialize(root)
                manifest, manifest_hash, latest, _ = _load_run(run_directory)
                self.assertEqual(latest["status"], "PENDING")
                attempt = (
                    run_directory / "attempts" / "attempt-000001"
                )
                attempt.mkdir()
                if stage != "after_mkdir":
                    (attempt / INSTANCE_NAME).write_bytes(
                        (run_directory / INSTANCE_NAME).read_bytes()
                    )
                if stage in {
                    "after_config_write",
                    "immediately_before_checkpoint",
                }:
                    config = {
                        "schema": "gamma-theta-order13-k3-attempt-config-v1",
                        "schema_version": 1,
                        "claim_status": (
                            "NO_SAT_OR_UNSAT_CLAIM_BEFORE_EXECUTION"
                        ),
                        "proof_pipeline": manifest["proof_pipeline"],
                        "attempt_number": 1,
                        "template": manifest["template"],
                        "seed": manifest["seed"],
                        "run_manifest_sha256": manifest_hash,
                        "instance": _binding(
                            attempt / INSTANCE_NAME, "attempt instance"
                        ),
                        "runtime_source_set_sha256": manifest[
                            "runtime_source_set_sha256"
                        ],
                        "tools": manifest["tools"],
                        "limits": manifest["limits"],
                        "commands": _commands(manifest, attempt),
                        "created_unix_ns": 1,
                    }
                    (attempt / "attempt-config.json").write_bytes(
                        canonical_json_bytes(config)
                    )
                with self.assertRaisesRegex(
                    ValueError,
                    "attempt directory count differs from checkpoint",
                ):
                    audit(run_directory)
                with self.assertRaisesRegex(
                    ValueError,
                    "attempt directory count differs from checkpoint",
                ):
                    run(
                        run_directory,
                        production_gate=True,
                        recover_interrupted=False,
                    )
                recovered = run(
                    run_directory,
                    production_gate=True,
                    recover_interrupted=True,
                )
                self.assertEqual(recovered["status"], "RETRYABLE_NONCLAIM")
                self.assertTrue(
                    recovered["precheckpoint_orphan_quarantined"]
                )
                self.assertFalse(recovered["child_launched"])
                self.assertFalse(attempt.exists())
                quarantined = Path(
                    recovered["quarantine"]["quarantined_path"]
                )
                self.assertTrue(quarantined.is_dir())
                report = audit(run_directory)
                self.assertEqual(report["status"], "PENDING")
                self.assertEqual(report["attempt_count"], 0)

                with patch(
                    "search.order13_k3.production._execute",
                    return_value=(
                        "RETRYABLE_NONCLAIM",
                        {
                            "phase_status": "SYNTHETIC_RETRY_NONCLAIM",
                            "phase_details": {},
                        },
                    ),
                ):
                    fresh = run(
                        run_directory,
                        production_gate=True,
                        recover_interrupted=False,
                    )
                self.assertEqual(fresh["attempt_number"], 1)
                self.assertEqual(fresh["status"], "RETRYABLE_NONCLAIM")
                self.assertEqual(audit(run_directory)["attempt_count"], 1)

    def test_fake_complete_proof_chain_and_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run_directory, _ = self._initialize(root)
            outcome = self._run_fake_complete_success(run_directory)
            self.assertEqual(outcome["status"], FINAL_SUCCESS)
            report = audit(run_directory)
            self.assertEqual(report["status"], FINAL_SUCCESS)
            self.assertFalse(report["proof_freshly_replayed"])

            lrat = (
                run_directory
                / "attempts"
                / "attempt-000001"
                / "proof.converted.lrat"
            )
            lrat.write_bytes(lrat.read_bytes() + b"c mutation\n")
            with self.assertRaises(ValueError):
                audit(run_directory)

    def test_phase_record_rejects_coherent_postcheck_lrat_substitution(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run_directory, _ = self._initialize(root)
            self.assertEqual(
                self._run_fake_complete_success(run_directory)["status"],
                FINAL_SUCCESS,
            )
            attempt = (
                run_directory / "attempts" / "attempt-000001"
            )
            lrat = attempt / "proof.converted.lrat"
            phase_record = json.loads(
                (attempt / "child-lrat_check.json").read_bytes()
            )
            self.assertEqual(
                phase_record["readonly_inputs_before"]["LRAT"],
                _binding(lrat, "recorded LRAT"),
            )
            self.assertEqual(
                phase_record["readonly_inputs_after"]["LRAT"],
                _binding(lrat, "recorded LRAT"),
            )
            lrat.write_bytes(b"not an LRAT proof\n")
            certificate_path = attempt / "certificate.json"
            certificate = json.loads(certificate_path.read_bytes())
            certificate["converted_lrat"] = _binding(
                lrat, "substituted LRAT"
            )
            certificate_path.write_bytes(
                canonical_json_bytes(certificate)
            )
            self._refresh_success_metadata(run_directory)
            with self.assertRaisesRegex(
                ValueError, "phase input/output bindings differ"
            ):
                audit(run_directory)

    def test_success_certificate_exact_shape_and_boundary(self) -> None:
        for case in ("extra_key", "claim_boundary"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                run_directory, _ = self._initialize(root)
                self._run_fake_complete_success(run_directory)
                certificate_path = (
                    run_directory
                    / "attempts"
                    / "attempt-000001"
                    / "certificate.json"
                )
                certificate = json.loads(certificate_path.read_bytes())
                if case == "extra_key":
                    certificate["asserted_global_order13_exclusion"] = True
                else:
                    certificate["claim_boundary"] = (
                        "Fresh replay and complete coverage falsely asserted."
                    )
                certificate_path.write_bytes(
                    canonical_json_bytes(certificate)
                )
                self._refresh_success_metadata(run_directory)
                with self.assertRaisesRegex(
                    ValueError, "template certificate bindings differ"
                ):
                    audit(run_directory)

    def test_fake_timeout_is_retryable_nonclaim(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run_directory, _ = self._initialize(root)

            def timeout_child(**keywords: object) -> ChildResult:
                command = tuple(keywords["command"])
                stdout = Path(keywords["stdout_path"])
                stderr = Path(keywords["stderr_path"])
                stdout.write_bytes(b"")
                stderr.write_bytes(b"")
                digest = hashlib.sha256(Path(command[0]).read_bytes()).hexdigest()
                return ChildResult(
                    command=command,
                    command_sha256=_command_sha256(command),
                    executable_sha256_before=digest,
                    executable_sha256_after=digest,
                    exit_code=-15,
                    termination_signal=15,
                    timed_out=True,
                    memory_limit_exceeded=False,
                    started_unix_ns=1,
                    finished_unix_ns=2,
                    wall_seconds=2.0,
                    user_cpu_seconds=0.0,
                    system_cpu_seconds=0.0,
                    maximum_resident_set_size_mib=1.0,
                    maximum_resident_set_size_raw=1,
                    maximum_resident_set_size_raw_unit="bytes",
                    peak_polled_resident_set_size_mib=1.0,
                    available_memory_before_bytes=16 << 30,
                    wall_limit_seconds=int(keywords["wall_limit_seconds"]),
                    memory_limit_mib=int(keywords["memory_limit_mib"]),
                    file_limit_mib=int(keywords["file_limit_mib"]),
                    stdout_path=str(stdout.resolve()),
                    stdout_sha256=hashlib.sha256(b"").hexdigest(),
                    stderr_path=str(stderr.resolve()),
                    stderr_sha256=hashlib.sha256(b"").hexdigest(),
                )

            with patch(
                "search.order13_k3.production._available_memory_bytes",
                return_value=16 << 30,
            ), patch(
                "search.order13_k3.production.run_bounded_child",
                side_effect=timeout_child,
            ):
                outcome = run(
                    run_directory,
                    production_gate=True,
                    recover_interrupted=False,
                )
            self.assertEqual(outcome["status"], "RETRYABLE_NONCLAIM")
            attempt_outcome = json.loads(
                (
                    run_directory
                    / "attempts"
                    / "attempt-000001"
                    / "outcome.json"
                ).read_text()
            )
            self.assertEqual(
                attempt_outcome["details"]["phase_status"],
                "SOLVER_TIMEOUT_NONCLAIM",
            )

    def test_low_memory_and_high_load_reject_before_child(self) -> None:
        for case in ("memory", "load"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                run_directory, _ = self._initialize(root)
                with patch(
                    "search.order13_k3.production._available_memory_bytes",
                    return_value=(1 if case == "memory" else 16 << 30),
                ), patch(
                    "search.order13_k3.production.os.getloadavg",
                    return_value=(
                        (2000.0, 2000.0, 2000.0)
                        if case == "load"
                        else (0.0, 0.0, 0.0)
                    ),
                ), patch(
                    "search.order13_k3.production.run_bounded_child"
                ) as child:
                    outcome = run(
                        run_directory,
                        production_gate=True,
                        recover_interrupted=False,
                    )
                child.assert_not_called()
                self.assertEqual(outcome["status"], "RETRYABLE_NONCLAIM")
                self.assertFalse(outcome["child_launched"])


if __name__ == "__main__":
    unittest.main()
