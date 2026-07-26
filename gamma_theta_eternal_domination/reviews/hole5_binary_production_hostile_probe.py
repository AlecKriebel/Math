#!/usr/bin/env python3
"""Hostile, solver-free audit of the hole5 binary production runner.

This probe never launches CaDiCaL.  It checks frozen file identities, command
construction, parser/checker acceptance boundaries, status taxonomy, resource
caps, and three end-to-end mocked mutation paths.  The mocked UNSAT path uses
the already-audited clean-room binary parser on an eleven-byte fixture.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import os
import shutil
import signal
import sys
import tempfile
from contextlib import ExitStack
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Callable, Mapping, Sequence
from unittest.mock import patch


CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from synthesis_k3 import hole5_binary_production as production  # noqa: E402


EXPECTED_FILES = {
    "src/synthesis_k3/__init__.py": (
        "fbc5ca4211eb97b498e0eecd692333596bba409c26629623f8d547a48a379e86"
    ),
    "src/synthesis_k3/encoding.py": (
        "fda94aeb7a2c48e64f1b9a975c27263b100542359c13264f4a625f115ff563c6"
    ),
    "src/synthesis_k3/coloring.py": (
        "9791599aaca6b9f7ec5e6fed8cfce41a5c5bec825a350e5e493a0d1aa06d3713"
    ),
    "src/synthesis_k3/generate.py": (
        "456029e08a199e3cc8d4aa6070e3209d6884901fc6c3db8486b80862614430e1"
    ),
    "src/synthesis_k3/cegar.py": (
        "411fffff34c0122d679ee710aff0e3856a7ff166bff30c69edb1f0044defce8c"
    ),
    "src/synthesis_k3/template_color_bank.py": (
        "dc69687f01e85bea643b73f713b1afca51b3911b3fee4a857da3fb07cc979838"
    ),
    "src/synthesis_k3/hole5_signature_breaker.py": (
        "cc1dc4249dc20f78e8eff4de14ffdca632da1e9455a381000786faa28c950c77"
    ),
    "src/synthesis_k3/hole5_binary_production.py": (
        "02e8a13d806593017071ca0ad89680ece8c947e0c24d7579e6a779bc25ba044f"
    ),
    "tests/test_hole5_binary_production.py": (
        "e622ef081da50fa7f6dc917f3b0af76f3cda34a67e5642128779b47e8c234072"
    ),
    "tests/test_hole5_signature_breaker.py": (
        "cd73ae2275d1d08363a1ed7db5990ad294952270e449d5cec8229312d738a892"
    ),
    "math/lemmas/hole5_signature_symmetry.md": (
        "8f8192774c3de65c2468115cc2d4aadd392fa7a1f73261c23fa49886d9c183e8"
    ),
    "reviews/hole5_signature_symmetry_hostile_probe.py": (
        "3515adc846e961738b86c572a90aa0f42945cfa6794e3700986c392999c4ab66"
    ),
    "reviews/hole5_signature_symmetry_hostile_probe_log.json": (
        "f1d8f6d8d6f85bdffadcf39e5d4c4504b9cf0d1b8a609d8e5fe540523091b9de"
    ),
    "reviews/hole5_signature_symmetry_hostile_review.md": (
        "169b99e083fe2079b3957de3095591142162aca76a10b42f9bb61266775ef223"
    ),
    "reviews/hole5_signature_package_hostile_probe.py": (
        "ddf75d62dda73779cca880d2c3ec60ee00b91d5f1110ffa84426678a8ef32cc9"
    ),
    "reviews/hole5_signature_package_hostile_probe_log.json": (
        "58edf995b84de703c466e956f47d50443de025fa8b5c5268d781f8962a39d694"
    ),
    "reviews/hole5_signature_package_hostile_review.md": (
        "b675ed1ba1e83a37069af4f3f526a98b3c627d1133300b1e5764fe933fa7b5ed"
    ),
    "reviews/hole5_binary_drat_hostile_probe.py": (
        "02c3c00faf7afb91a3217f5b738d0dacf7699875928162d01ce2df97e600007d"
    ),
    "reviews/hole5_binary_drat_hostile_probe_log.json": (
        "2674cf53eecd881535c6bc4bc2732d669562d7a86816e7bc9057222aadeb3ca8"
    ),
    "reviews/hole5_binary_drat_hostile_review.md": (
        "d2abc28ad804e8bb5a675ad0bb5a6f5f08f8fd51482d7be1953d0fb31aff41fe"
    ),
    "results/synthesis_k3_hole5_signature_package/instance.cnf": (
        "c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd55f0b0152703d104"
    ),
    "results/synthesis_k3_hole5_signature_package/signature_breaker.json": (
        "62ce8f60ecfe74f58bcd113166009637f854d7d663aea2e59395ae224682d18a"
    ),
    "results/synthesis_k3_hole5_signature_package/manifest.json": (
        "da33bc1708f7d21b92ceedc68710d5433a1aacbe6e32b8a7432bbab45d8cc788"
    ),
    "results/synthesis_k3_template_bank_packages/hole5/instance.cnf": (
        "76bf36ecb663cd37272acded2208206fdba6aa571dd5f2e757cc132bd533e0b7"
    ),
    "results/synthesis_k3_template_bank_packages/hole5/coloring_bank.json": (
        "b3c24db61e7a33c3d8803e2bbadcdda92b950fb04445e59e7930330e92b74a00"
    ),
    "results/synthesis_k3_template_bank_packages/hole5/manifest.json": (
        "99a56197074ad3373691578527e41baff4d76eb1e86141366c4edf8bc5871402"
    ),
    "tools/cadical_3_0_1/build/cadical": (
        "51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6"
    ),
    "tools/cadical_3_0_1.tar.gz": (
        "2dccd6ecc1878348dd70194d51df6b69006bf86439b5b3c395a5c5dd8863201e"
    ),
    "tools/drat_trim_2023_05_22/drat-trim": (
        "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb"
    ),
    "tools/drat_trim_2023_05_22.tar.gz": (
        "2ac28cd9e38e050b4f78fbff0efd4a1aa2349d157aef08c9b1fb6c7139949108"
    ),
}

SOURCE_PACKAGE = CAMPAIGN / "results/synthesis_k3_template_bank_packages/hole5"
RETAINED_PACKAGE = CAMPAIGN / "results/synthesis_k3_hole5_signature_package"
CADICAL = CAMPAIGN / "tools/cadical_3_0_1/build/cadical"
DRAT_TRIM = CAMPAIGN / "tools/drat_trim_2023_05_22/drat-trim"
PARSER = CAMPAIGN / "reviews/hole5_binary_drat_hostile_probe.py"
TEST_SUPPORT_PATH = CAMPAIGN / "tests/test_hole5_binary_production.py"
FAKE_HEAD = "a" * 40


def require(condition: object, message: str) -> None:
    if condition is not True:
        raise AssertionError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_json(value: object) -> bytes:
    return (
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=True,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("ascii")


def exact_file_audit() -> dict[str, object]:
    records: dict[str, object] = {}
    for relative, expected in sorted(EXPECTED_FILES.items()):
        path = CAMPAIGN / relative
        information = os.lstat(path)
        observed = sha256_file(path)
        require(path.is_file(), f"not a regular file: {relative}")
        require(not path.is_symlink(), f"symlink forbidden: {relative}")
        require(information.st_nlink == 1, f"hard link forbidden: {relative}")
        require(observed == expected, f"hash differs: {relative}")
        records[relative] = {
            "sha256": observed,
            "size_bytes": information.st_size,
        }
    return records


def command_audit() -> dict[str, object]:
    root = CAMPAIGN / "__hostile_probe_path_fixture__"
    result = root / "solver.result"
    raw = root / "proof.raw.bdrat"
    addition = root / "proof.additions.bdrat"
    cnf = RETAINED_PACKAGE / "instance.cnf"
    solver = production._solver_command(
        CADICAL,
        seed=2_000_000_000,
        internal_seconds=37,
        result_path=result,
        cnf_path=cnf,
        proof_path=raw,
    )
    parser = production._parser_command(
        Path(sys.executable).resolve(),
        PARSER,
        raw_proof=raw,
        addition_proof=addition,
    )
    checker = production._checker_command(
        DRAT_TRIM,
        cnf_path=cnf,
        proof_path=addition,
        internal_seconds=41,
    )
    require(solver[1] == "--seed=2000000000", "seed is not normalized")
    require(solver[2:5] == ("--binary", "--no-colors", "-q"), "solver flags")
    require(solver[5:7] == ("-t", "37"), "solver time flag")
    require(solver[7] == "-w" and solver[8] == str(result), "result path")
    require(solver[-2:] == (str(cnf.resolve()), str(raw)), "solver operands")
    require(parser[1:3] == ("-I", "-B"), "Python is not isolated")
    require(parser[4] == "strip", "parser subcommand differs")
    require(parser[-2:] == ("--max-var", "6886"), "parser max-var differs")
    require(
        checker[-6:] == ("-i", "-f", "-W", "-U", "-t", "41"),
        "checker is not strict binary forward RUP",
    )
    source = (CAMPAIGN / "src/synthesis_k3/hole5_binary_production.py").read_text(
        encoding="utf-8"
    )
    require(
        'seed, "solver seed", minimum=0, maximum=2_000_000_000' in source,
        "CaDiCaL seed bound is not exact",
    )
    runtime = set(production.RUNTIME_SOURCE_RELATIVE_PATHS)
    audit_paths = {
        "reviews/hole5_binary_production_hostile_probe.py",
        "reviews/hole5_binary_production_hostile_probe_log.json",
        "reviews/hole5_binary_production_hostile_review.md",
    }
    require(audit_paths <= runtime, "hostile audit artifacts are not source-bound")
    return {
        "audit_artifacts_in_runtime_manifest": sorted(audit_paths),
        "checker": list(checker),
        "parser": list(parser),
        "seed_boundary": [0, 2_000_000_000],
        "solver": list(solver),
    }


def import_closure_audit() -> dict[str, object]:
    source_prefix = Path("src/synthesis_k3")
    entry = source_prefix / "hole5_binary_production.py"
    package_init = source_prefix / "__init__.py"
    pending = [entry, package_init]
    closure: set[Path] = set()
    dynamic_import_calls: list[str] = []
    while pending:
        relative = pending.pop()
        if relative in closure:
            continue
        require((CAMPAIGN / relative).is_file(), f"missing import: {relative}")
        closure.add(relative)
        tree = ast.parse((CAMPAIGN / relative).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                called = node.func
                name = (
                    called.id
                    if isinstance(called, ast.Name)
                    else called.attr
                    if isinstance(called, ast.Attribute)
                    else ""
                )
                if name in {
                    "__import__",
                    "exec",
                    "eval",
                    "import_module",
                    "spec_from_file_location",
                }:
                    dynamic_import_calls.append(f"{relative}:{node.lineno}:{name}")
            modules: list[str] = []
            if isinstance(node, ast.ImportFrom):
                if node.level > 0:
                    if node.level != 1:
                        raise AssertionError(
                            f"unsupported upward relative import: {relative}"
                        )
                    if node.module is None:
                        modules.extend(alias.name for alias in node.names)
                    else:
                        modules.append(node.module)
                elif (
                    node.module == "synthesis_k3"
                    or (
                        node.module is not None
                        and node.module.startswith("synthesis_k3.")
                    )
                ):
                    suffix = node.module.removeprefix("synthesis_k3").lstrip(".")
                    if suffix:
                        modules.append(suffix)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith("synthesis_k3."):
                        modules.append(alias.name.removeprefix("synthesis_k3."))
            for module in modules:
                dependency = source_prefix / (
                    module.replace(".", "/") + ".py"
                )
                if (CAMPAIGN / dependency).is_file():
                    pending.append(dependency)
    expected = {
        source_prefix / "__init__.py",
        source_prefix / "cegar.py",
        source_prefix / "coloring.py",
        source_prefix / "encoding.py",
        source_prefix / "generate.py",
        source_prefix / "hole5_binary_production.py",
        source_prefix / "hole5_signature_breaker.py",
        source_prefix / "template_color_bank.py",
    }
    require(closure == expected, "recursive local import closure differs")
    declared = {Path(value) for value in production.RUNTIME_SOURCE_RELATIVE_PATHS}
    require(closure <= declared, "runtime manifest omits a local import")
    require(not dynamic_import_calls, "dynamic local import surface found")
    return {
        "declared_runtime_source_count": len(declared),
        "dynamic_import_calls": dynamic_import_calls,
        "local_import_closure": sorted(path.as_posix() for path in closure),
    }


def independent_tool_gate_audit() -> dict[str, object]:
    cadical_archive = CAMPAIGN / "tools/cadical_3_0_1.tar.gz"
    checker_archive = CAMPAIGN / "tools/drat_trim_2023_05_22.tar.gz"
    expected = {
        "cadical_binary": production.EXPECTED_CADICAL_BINARY_SHA256,
        "cadical_archive": production.EXPECTED_CADICAL_ARCHIVE_SHA256,
        "checker_binary": production.EXPECTED_DRAT_TRIM_BINARY_SHA256,
        "checker_archive": production.EXPECTED_DRAT_TRIM_ARCHIVE_SHA256,
    }
    paths = {
        "cadical_binary": CADICAL,
        "cadical_archive": cadical_archive,
        "checker_binary": DRAT_TRIM,
        "checker_archive": checker_archive,
    }
    observed = {role: sha256_file(path) for role, path in paths.items()}
    require(observed == expected, "independent tool/archive hashes differ")
    cadical_binding, checker_binding = production.verify_pinned_tools(
        CADICAL, DRAT_TRIM
    )
    production._independent_tool_hash_gate(
        cadical_binding, checker_binding
    )

    rejected: list[str] = []
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary).resolve()
        copies: dict[str, Path] = {}
        for role, source in paths.items():
            target = root / role
            shutil.copyfile(source, target)
            copies[role] = target

        def fresh_bindings() -> tuple[SimpleNamespace, SimpleNamespace]:
            return (
                SimpleNamespace(
                    path=str(copies["cadical_binary"]),
                    source_archive_path=str(copies["cadical_archive"]),
                    sha256=expected["cadical_binary"],
                    source_archive_sha256=expected["cadical_archive"],
                ),
                SimpleNamespace(
                    path=str(copies["checker_binary"]),
                    source_archive_path=str(copies["checker_archive"]),
                    sha256=expected["checker_binary"],
                    source_archive_sha256=expected["checker_archive"],
                ),
            )

        local_cadical, local_checker = fresh_bindings()
        production._independent_tool_hash_gate(
            local_cadical, local_checker
        )
        for role, source in paths.items():
            target = copies[role]
            with target.open("r+b") as handle:
                original = handle.read(1)
                require(len(original) == 1, f"empty tool artifact: {role}")
                handle.seek(0)
                handle.write(bytes((original[0] ^ 1,)))
                handle.flush()
                os.fsync(handle.fileno())
            local_cadical, local_checker = fresh_bindings()
            try:
                production._independent_tool_hash_gate(
                    local_cadical, local_checker
                )
            except ValueError:
                rejected.append(f"bytes:{role}")
            else:
                raise AssertionError(f"tool-byte mutation accepted: {role}")
            shutil.copyfile(source, target)

        for role in (
            "cadical_binary",
            "cadical_archive",
            "checker_binary",
            "checker_archive",
        ):
            local_cadical, local_checker = fresh_bindings()
            selected = (
                local_cadical
                if role.startswith("cadical")
                else local_checker
            )
            attribute = (
                "sha256" if role.endswith("binary") else "source_archive_sha256"
            )
            setattr(selected, attribute, "0" * 64)
            try:
                production._independent_tool_hash_gate(
                    local_cadical, local_checker
                )
            except ValueError:
                rejected.append(f"binding:{role}")
            else:
                raise AssertionError(f"tool-binding mutation accepted: {role}")
    require(len(rejected) == 8, "tool mutation coverage differs")
    return {
        "hard_coded_hashes": expected,
        "independent_hashes": observed,
        "rejected_mutations": sorted(rejected),
        "verify_pinned_tools_precedes_independent_gate": True,
    }


def checker_boundary_audit() -> dict[str, object]:
    accepted = (
        b"c forward verification\n"
        b"s VERIFIED\n"
        b"c 0 RAT lemmas in core; 0 redundant literals\n"
    )
    mutations = {
        "warning_stdout": accepted + b"c warning: injected\n",
        "warning_stderr": accepted,
        "non_ascii": accepted + b"\xff\n",
        "missing_verified": b"c 0 RAT lemmas in core\n",
        "duplicate_verified": accepted + b"s VERIFIED\n",
        "wrong_status": (
            b"s NOT VERIFIED\nc 0 RAT lemmas in core; 0 redundant literals\n"
        ),
        "one_rat": b"s VERIFIED\nc 1 RAT lemmas in core\n",
        "hundred_rat": b"s VERIFIED\nc 100 RAT lemmas in core\n",
        "duplicate_rat_line": accepted + b"c 0 RAT lemmas in core\n",
        "zero_prefix_ambiguity": b"s VERIFIED\nc 00 RAT lemmas in core\n",
    }
    rejected: list[str] = []
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary).resolve()
        stdout = root / "stdout"
        stderr = root / "stderr"
        stdout.write_bytes(accepted)
        stderr.write_bytes(b"")
        production._strict_checker_verified(stdout, stderr)
        for name, payload in mutations.items():
            stdout.write_bytes(payload)
            stderr.write_bytes(
                b"hostile stderr\n" if name == "warning_stderr" else b""
            )
            try:
                production._strict_checker_verified(stdout, stderr)
            except (ValueError, UnicodeDecodeError):
                rejected.append(name)
            else:
                raise AssertionError(f"checker mutation accepted: {name}")
    require(set(rejected) == set(mutations), "checker mutation coverage differs")
    return {
        "accepted_fixture_sha256": hashlib.sha256(accepted).hexdigest(),
        "accepted_fixture_size_bytes": len(accepted),
        "rejected_mutations": sorted(rejected),
    }


def parser_report_audit() -> dict[str, object]:
    raw_bytes = bytes.fromhex("61 02 00 64 04 00 61 03 00 61 00")
    rejected: list[str] = []
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary).resolve()
        raw = root / "raw.bdrat"
        addition = root / "addition.bdrat"
        stdout = root / "parser.stdout"
        stderr = root / "parser.stderr"
        raw.write_bytes(raw_bytes)
        completed = __import__("subprocess").run(
            (
                str(Path(sys.executable).resolve()),
                "-I",
                "-B",
                str(PARSER),
                "strip",
                "--proof",
                str(raw),
                "--output",
                str(addition),
                "--max-var",
                "6886",
            ),
            cwd=CAMPAIGN,
            env={},
            stdin=__import__("subprocess").DEVNULL,
            capture_output=True,
            timeout=10,
            check=False,
        )
        require(completed.returncode == 0, "clean-room fixture parse failed")
        stdout.write_bytes(completed.stdout)
        stderr.write_bytes(completed.stderr)
        report = production._validate_parser_report(
            stdout,
            stderr,
            raw_proof=raw,
            addition_proof=addition,
        )
        mutations: dict[str, Callable[[dict[str, object]], None]] = {
            "source_record_count": lambda value: value["source"].__setitem__(
                "record_count", value["source"]["record_count"] + 1
            ),
            "source_byte_count": lambda value: value["source"].__setitem__(
                "byte_count", value["source"]["byte_count"] + 1
            ),
            "source_addition_count": lambda value: value["source"].__setitem__(
                "addition_count", value["source"]["addition_count"] + 1
            ),
            "source_final_empty": lambda value: value["source"].__setitem__(
                "final_empty_record", 0
            ),
            "source_first_deletion": lambda value: value["source"].__setitem__(
                "first_deletion_record", value["source"]["record_count"] + 1
            ),
            "addition_deletion_count": lambda value: value[
                "addition_only"
            ].__setitem__("deletion_count", 1),
            "addition_max_var": lambda value: value["addition_only"].__setitem__(
                "maximum_variable", 6887
            ),
            "preservation_flag": lambda value: value.__setitem__(
                "all_addition_bytes_preserved_in_order", False
            ),
        }
        for name, mutate in mutations.items():
            candidate = json.loads(json.dumps(report))
            mutate(candidate)
            stdout.write_bytes(canonical_json(candidate))
            try:
                production._validate_parser_report(
                    stdout,
                    stderr,
                    raw_proof=raw,
                    addition_proof=addition,
                )
            except ValueError:
                rejected.append(name)
            else:
                raise AssertionError(f"parser-report mutation accepted: {name}")
    require(set(rejected) == set(mutations), "parser mutation coverage differs")
    return {
        "addition_only_sha256": hashlib.sha256(
            bytes.fromhex("61 02 00 61 03 00 61 00")
        ).hexdigest(),
        "raw_fixture_sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "rejected_mutations": sorted(rejected),
    }


def resource_and_status_audit() -> dict[str, object]:
    source_path = CAMPAIGN / "src/synthesis_k3/hole5_binary_production.py"
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    statuses = sorted(
        {
            node.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Constant)
            and isinstance(node.value, str)
            and (
                node.value.endswith("_NONCLAIM")
                or node.value.startswith("INCONCLUSIVE_")
                or node.value
                in {
                    "SAT_MODEL_VERIFIED_CANDIDATE_ONLY",
                    "UNSAT_VERIFIED_FINITE_CERTIFICATE",
                }
            )
        }
    )
    claiming = {
        "SAT_MODEL_VERIFIED_CANDIDATE_ONLY",
        "UNSAT_VERIFIED_FINITE_CERTIFICATE",
    }
    for status in statuses:
        if status not in claiming:
            require(
                status.endswith("_NONCLAIM")
                or status == "INCONCLUSIVE_SOLVER_UNKNOWN",
                f"terminal status is not fail-closed: {status}",
            )

    child_statuses: dict[str, str] = {}
    cases = {
        "timeout": SimpleNamespace(
            timed_out=True,
            memory_limit_exceeded=False,
            termination_signal=int(signal.SIGTERM),
        ),
        "memory": SimpleNamespace(
            timed_out=False,
            memory_limit_exceeded=True,
            termination_signal=int(signal.SIGKILL),
        ),
        "file": SimpleNamespace(
            timed_out=False,
            memory_limit_exceeded=False,
            termination_signal=int(signal.SIGXFSZ),
        ),
        "signal": SimpleNamespace(
            timed_out=False,
            memory_limit_exceeded=False,
            termination_signal=int(signal.SIGTERM),
        ),
    }
    for phase in ("solver", "parser", "checker"):
        for name, child in cases.items():
            status = production._child_failure_status(child, phase)
            require(
                isinstance(status, str) and status.endswith("_NONCLAIM"),
                f"{phase}/{name} does not classify as nonclaim",
            )
            child_statuses[f"{phase}_{name}"] = status

    with patch.object(production, "_physical_memory_bytes", return_value=16 << 30), patch.object(
        production,
        "_disk_gate",
        return_value={
            "free_bytes": 20 << 30,
            "required_bytes": 1,
            "remaining_file_slots": 9,
        },
    ):
        resources = production._resource_preflight(
            output_parent=CAMPAIGN,
            solver_seconds=3600,
            parser_seconds=1800,
            checker_seconds=1800,
            solver_memory_mib=4096,
            parser_memory_mib=512,
            checker_memory_mib=4096,
            file_limit_mib=600,
            disk_reserve_mib=4096,
        )
        require(
            resources["maximum_responsive_child_memory_mib"] == 4096,
            "25% memory ceiling differs",
        )
    rejected_limits: list[str] = []
    for role, kwargs in (
        ("solver_seconds", {"solver_seconds": 3601}),
        ("parser_seconds", {"parser_seconds": 1801}),
        ("checker_seconds", {"checker_seconds": 1801}),
        ("child_memory", {"solver_memory_mib": 4097}),
        ("file_limit", {"file_limit_mib": 601}),
        ("disk_reserve", {"disk_reserve_mib": 4095}),
    ):
        arguments = {
            "output_parent": CAMPAIGN,
            "solver_seconds": 1,
            "parser_seconds": 1,
            "checker_seconds": 1,
            "solver_memory_mib": 64,
            "parser_memory_mib": 64,
            "checker_memory_mib": 64,
            "file_limit_mib": 1,
            "disk_reserve_mib": 4096,
        }
        arguments.update(kwargs)
        with patch.object(
            production, "_physical_memory_bytes", return_value=16 << 30
        ), patch.object(
            production,
            "_disk_gate",
            return_value={
                "free_bytes": 20 << 30,
                "required_bytes": 1,
                "remaining_file_slots": 9,
            },
        ):
            try:
                production._resource_preflight(**arguments)
            except ValueError:
                rejected_limits.append(role)
            else:
                raise AssertionError(f"resource cap accepted: {role}")
    return {
        "child_failure_statuses": child_statuses,
        "resource_caps": {
            "child_memory_mib": 4096,
            "checker_seconds": 1800,
            "disk_reserve_minimum_mib": 4096,
            "file_limit_mib": 600,
            "parser_seconds": 1800,
            "physical_memory_fraction": "1/4",
            "solver_seconds": 3600,
        },
        "rejected_limit_mutations": sorted(rejected_limits),
        "terminal_statuses": statuses,
    }


def load_test_support() -> ModuleType:
    specification = importlib.util.spec_from_file_location(
        "_hole5_binary_production_test_support", TEST_SUPPORT_PATH
    )
    require(
        specification is not None and specification.loader is not None,
        "cannot load test support",
    )
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def mocked_run(
    support: ModuleType,
    *,
    output: Path,
    scenario: str,
    mutation: Callable[[Path], None] | None,
    mutation_call: int,
) -> tuple[Mapping[str, object], int]:
    pipeline = support.FakePipeline(scenario)
    original_verify = production._verify_all_bindings
    calls = 0

    def verify_with_mutation(
        bindings: Mapping[str, Mapping[str, object]],
    ) -> None:
        nonlocal calls
        original_verify(bindings)
        calls += 1
        if mutation is not None and calls == mutation_call:
            mutation(output)

    fake_binding = {
        "head_commit": FAKE_HEAD,
        "repository_relative_campaign_path": "gamma_theta_eternal_domination",
        "runtime_sources_match_head": True,
        "runtime_source_mismatches": [],
        "global_worktree_cleanliness_required": False,
    }
    with ExitStack() as stack:
        stack.enter_context(
            patch.object(production, "runtime_source_manifest", return_value=())
        )
        stack.enter_context(
            patch.object(production, "git_source_binding", return_value=fake_binding)
        )
        stack.enter_context(
            patch.object(
                production, "run_bounded_child", side_effect=pipeline
            )
        )
        stack.enter_context(
            patch.object(production, "_verify_all_bindings", verify_with_mutation)
        )
        stack.enter_context(
            patch.object(
                production,
                "_disk_gate",
                return_value={
                    "free_bytes": 20 << 30,
                    "required_bytes": 1,
                    "remaining_file_slots": 9,
                },
            )
        )
        if scenario == "sat":
            complete_model = {
                variable: False for variable in range(1, 6_887)
            }
            stack.enter_context(
                patch.object(
                    production,
                    "parse_solver_result_file",
                    return_value=support.ParsedSolverResult(
                        "SAT", complete_model
                    ),
                )
            )
            stack.enter_context(
                patch.object(production, "validate_model_satisfies_cnf")
            )
        outcome = production.run_production(
            package_directory=RETAINED_PACKAGE,
            source_package_directory=SOURCE_PACKAGE,
            output_directory=output,
            expected_package_manifest_sha256=(
                production.EXPECTED_PACKAGE_MANIFEST_SHA256
            ),
            expected_head_commit=FAKE_HEAD,
            cadical_path=CADICAL,
            drat_trim_path=DRAT_TRIM,
            seed=7,
            solver_seconds=5,
            parser_seconds=5,
            checker_seconds=5,
            solver_memory_mib=64,
            parser_memory_mib=64,
            checker_memory_mib=64,
            file_limit_mib=1,
            disk_reserve_mib=4096,
            validation_gate=True,
            hostile_audit_gate=True,
        )
    return outcome, len(pipeline.calls)


def mocked_mutation_audit() -> dict[str, object]:
    support = load_test_support()
    results: dict[str, object] = {}
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary).resolve()

        def mutate_certificate(output: Path) -> None:
            path = output / production.CERTIFICATE_NAME
            value = json.loads(path.read_text(encoding="utf-8"))
            value["claim_status"] = "VERIFIED_FINITE_CERTIFICATE"
            path.write_bytes(canonical_json(value))

        def mutate_candidate(output: Path) -> None:
            path = output / production.SAT_CANDIDATE_NAME
            value = json.loads(path.read_text(encoding="utf-8"))
            value["counterexample_claim"] = True
            value["claim_status"] = "COUNTEREXAMPLE"
            path.write_bytes(canonical_json(value))

        def mutate_config(output: Path) -> None:
            path = output / production.RUN_CONFIG_NAME
            value = json.loads(path.read_text(encoding="utf-8"))
            value["gates"]["hostile_audit_gate"] = False
            path.write_bytes(canonical_json(value))

        cases = (
            ("certificate", "unsat", mutate_certificate, 2, 3),
            ("sat_candidate", "sat", mutate_candidate, 2, 1),
            ("run_config", "unknown", mutate_config, 2, 1),
        )
        for name, scenario, mutation, call, expected_children in cases:
            outcome, children = mocked_run(
                support,
                output=root / name,
                scenario=scenario,
                mutation=mutation,
                mutation_call=call,
            )
            require(children == expected_children, f"{name} child count differs")
            require(
                outcome["claim_status"] == "NO_MATHEMATICAL_CLAIM",
                f"{name} mutation was not demoted",
            )
            require(
                str(outcome["status"]).endswith("_NONCLAIM"),
                f"{name} mutation status is not a nonclaim",
            )
            require(
                outcome["artifacts"] == {},
                f"{name} mutation retained an activation artifact map",
            )
            results[name] = {
                "child_count": children,
                "claim_status": outcome["claim_status"],
                "status": outcome["status"],
            }
    return results


def audit() -> dict[str, object]:
    return {
        "schema": "gamma-theta-hole5-binary-production-hostile-probe-v1",
        "production_solver_launched": False,
        "result": "ACCEPT_FOR_COMMIT_WITH_POSTCOMMIT_GATE",
        "checks": {
            "checker_boundary": checker_boundary_audit(),
            "commands": command_audit(),
            "exact_files": exact_file_audit(),
            "independent_tool_gate": independent_tool_gate_audit(),
            "local_import_closure": import_closure_audit(),
            "mocked_post_write_mutations": mocked_mutation_audit(),
            "parser_report_boundary": parser_report_audit(),
            "resources_and_statuses": resource_and_status_audit(),
        },
        "launch_gate": {
            "required": (
                "commit the exact audited runner, tests, probe, log, and review "
                "on main; use that exact current HEAD as --expected-head; "
                "confirm runtime_sources_match_head=true before any solve"
            ),
            "satisfied_during_probe": False,
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    payload = canonical_json(audit())
    if arguments.output is None:
        sys.stdout.buffer.write(payload)
    else:
        output = arguments.output
        if output.exists() or output.is_symlink():
            raise FileExistsError(output)
        with output.open("xb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
