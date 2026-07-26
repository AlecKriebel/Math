#!/usr/bin/env python3
"""Final hostile acceptance of the dedicated order-13, k=3 constructor.

The audit treats ``src/search/order13_k3`` as constructor A and
``reviews/order13_k3_constructor_independent/reconstruct.py`` as constructor
B.  It runs no SAT solver.  All subprocesses are an explicit allowlist of
constructor generation/audit/census/plan commands, the focused unit tests,
and constructor B's formula emitter.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import itertools
import json
import math
import os
import platform
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
PYTHON = Path(sys.executable).resolve()
TEMPLATES = ("hole5", "hole7", "hole9", "hole11")

FROZEN_FILES: Mapping[str, tuple[str, int]] = {
    "src/search/order13_k3/README.md": (
        "e11d26d2349139ae7481937a123e893840ae0692efc7a828619b73c1faa4f3a9",
        2370,
    ),
    "src/search/order13_k3/__init__.py": (
        "90809fbba9e0fb06998ac910db44ff232849bd5b4ab8f9dfbc4c4e931ca96892",
        584,
    ),
    "src/search/order13_k3/__main__.py": (
        "6a1a7df4c3919e17d29bbe27ac10c6ba66e18a37bdefac0e0f05af845572b524",
        125,
    ),
    "src/search/order13_k3/encoding.py": (
        "da06a797a29fcefff1eadbea4aa1535fb2ef14c0c64d84236bb3bf9241e1d47d",
        22581,
    ),
    "src/search/order13_k3/generate.py": (
        "35c78ecc4802667514c6294ac00558b83c9cfc83a37f9854533aedb9ca1bf1d0",
        24045,
    ),
    "tests/test_order13_k3_constructor.py": (
        "39e585b69972f8f47566c34cf66fb027bcc9797a9f0fe6238ba51cf5d4d904d5",
        10573,
    ),
    "results/order13_k3_constructor_gate/README.md": (
        "df20da429091c7fecf767a5b84bfb8fff41544fa12e0ce21caf30b83627d2939",
        950,
    ),
    "results/order13_k3_constructor_gate/census.json": (
        "abab7510db39506dd44d9f009f212c26d98ea83c73bde08bb2842e8f46cbcd1d",
        2133,
    ),
    "reviews/order13_k3_constructor_independent/reconstruct.py": (
        "fbdce8d2bf2e605a1520da1bacda3fc49ca8f4926d91457c3d4d256335902cfc",
        33886,
    ),
    "reviews/order13_k3_constructor_independent/evidence.json": (
        "784839ee925675b49a3636ab1625ef35389da2a6d418e629164c2ca5bb053e09",
        5559,
    ),
}

EXPECTED: Mapping[str, Mapping[str, int | str]] = {
    "hole5": {
        "variables": 9802,
        "base_clauses": 29791,
        "base_literals": 227006,
        "coloring_rows": 10935,
        "clauses": 40726,
        "literals": 493820,
        "size_bytes": 1805539,
        "sha256": "8df56270f1abf3a9a8e5d088a78680dcde0198292eaa51da78a7fce9179d2fb5",
        "bank_sha256": "b9a92c646b9622ec6a7296c3717f381d08600cd8cdaf967e340df2aebef2f89e",
    },
    "hole7": {
        "variables": 9802,
        "base_clauses": 29800,
        "base_literals": 227019,
        "coloring_rows": 5103,
        "clauses": 34903,
        "literals": 349248,
        "size_bytes": 1372338,
        "sha256": "3e1c86ccbcfc1e04b3ec4de29ec5b7d342cf909553655f959b1c35de0a36c340",
        "bank_sha256": "efafa89d6096d81bc0ae5a1860be4d0ce69b56f4e4957c8bd307316c121e692d",
    },
    "hole9": {
        "variables": 9802,
        "base_clauses": 29813,
        "base_literals": 227028,
        "coloring_rows": 2295,
        "clauses": 32108,
        "literals": 281028,
        "size_bytes": 1168197,
        "sha256": "3fff100cbfe66b422f9148fda66b6d1ccf6060a4ffbcdb37a54bde415e95e9ea",
        "bank_sha256": "a0f47a0aaa3be4659ce483f27a963d351f3a13424cac6a6a99ef6ac9e0c872f1",
    },
    "hole11": {
        "variables": 9802,
        "base_clauses": 29830,
        "base_literals": 227033,
        "coloring_rows": 1023,
        "clauses": 30853,
        "literals": 250664,
        "size_bytes": 1076723,
        "sha256": "1ab880e6d2cf9014e70362437b530c8d534fe57db7620029d06bc3ed9afee901",
        "bank_sha256": "b28be0de4af2c6635d1238d75c8ec23c2eea5dc0d8fc89c119e5ce921d982146",
    },
}

TAG_MAP = {
    "no_k4": "no_h_k4",
    "pair_has_witness": "pair_common_neighbor_choice",
    "pair_witness_edge": "pair_common_neighbor_implication",
    "template_rim_positive": "induced_hole",
    "template_rim_negative": "induced_hole",
    "template_hub_free": "hole_hub_free",
    "template_named_common_neighbor": "named_rim_edge_common_neighbor",
    "g_connected_cut": "g_connected_cut",
    "selected_state_dominates": "selected_state_dominates",
    "family_nonempty": "eternal_family_nonempty",
    "move_traverses_g_edge": "move_guard_adjacent_in_g",
    "move_successor_selected": "move_successor_in_family",
    "attack_has_response": "selected_attack_has_response",
    "triangle_selected": "h_triangle_forced_into_family",
    "complete_coloring_obstruction": "complete_coloring_obstruction",
}


class AuditError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def file_record(relative: str) -> dict[str, object]:
    path = ROOT / relative
    information = os.lstat(path)
    require(stat.S_ISREG(information.st_mode), f"{relative} is not regular")
    require(information.st_nlink == 1, f"{relative} has multiple hard links")
    payload = path.read_bytes()
    return {
        "path": relative,
        "sha256": sha256_bytes(payload),
        "size_bytes": len(payload),
    }


def bind_frozen_files() -> list[dict[str, object]]:
    records = []
    for relative, (digest, size) in FROZEN_FILES.items():
        record = file_record(relative)
        require(
            record["sha256"] == digest and record["size_bytes"] == size,
            f"frozen binding differs for {relative}",
        )
        records.append(record)
    return records


def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, allow_nan=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def strict_json_bytes(payload: bytes) -> object:
    def pairs_hook(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise AuditError(f"duplicate JSON key {key!r}")
            result[key] = value
        return result

    def reject_constant(value: str) -> object:
        raise AuditError(f"nonfinite JSON constant {value!r}")

    try:
        text = payload.decode("utf-8")
        return json.loads(
            text,
            object_pairs_hook=pairs_hook,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AuditError("malformed strict JSON") from error


def exact_dict(value: object, role: str) -> dict[str, object]:
    require(type(value) is dict, f"{role} is not an exact object")
    return value


def run_child(arguments: Sequence[str], *, timeout: int = 180) -> subprocess.CompletedProcess[bytes]:
    environment = os.environ.copy()
    environment.update(
        {
            "PYTHONPATH": "src",
            "PYTHONWARNINGS": "error",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    return subprocess.run(
        list(arguments),
        cwd=ROOT,
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )


def run_a_command(
    command: str,
    *arguments: str,
    timeout: int = 180,
    expect_success: bool = True,
) -> subprocess.CompletedProcess[bytes]:
    allowed = {"generate", "audit", "census", "plan"}
    require(command in allowed, "attempted a nonallowlisted constructor A command")
    child = run_child(
        (
            str(PYTHON),
            "-W",
            "error",
            "-m",
            "search.order13_k3",
            command,
            *arguments,
        ),
        timeout=timeout,
    )
    if expect_success:
        require(
            child.returncode == 0,
            f"constructor A {command} failed: {child.stderr.decode('utf-8', 'replace')}",
        )
    else:
        require(child.returncode != 0, f"mutated {command} was accepted")
    return child


def load_b_module() -> object:
    path = ROOT / "reviews/order13_k3_constructor_independent/reconstruct.py"
    specification = importlib.util.spec_from_file_location(
        "order13_constructor_b_frozen",
        path,
    )
    require(
        specification is not None and specification.loader is not None,
        "cannot load constructor B",
    )
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def parse_dimacs(payload: bytes) -> tuple[int, tuple[tuple[int, ...], ...]]:
    try:
        text = payload.decode("ascii")
    except UnicodeDecodeError as error:
        raise AuditError("DIMACS is not ASCII") from error
    require(text.endswith("\n"), "DIMACS lacks terminal LF")
    lines = text.splitlines()
    require(bool(lines), "DIMACS is empty")
    header = lines[0].split()
    require(len(header) == 4 and header[:2] == ["p", "cnf"], "bad DIMACS header")
    try:
        variables = int(header[2])
        promised = int(header[3])
    except ValueError as error:
        raise AuditError("noninteger DIMACS header") from error
    clauses = []
    for index, line in enumerate(lines[1:], 2):
        fields = line.split()
        require(fields and fields[-1] == "0", f"unterminated clause {index}")
        require("0" not in fields[:-1], f"embedded zero on clause {index}")
        try:
            clause = tuple(int(value) for value in fields[:-1])
        except ValueError as error:
            raise AuditError(f"noninteger clause {index}") from error
        require(bool(clause), f"empty clause {index}")
        require(
            all(0 < abs(literal) <= variables for literal in clause),
            f"out-of-range literal on clause {index}",
        )
        clauses.append(clause)
    require(len(clauses) == promised, "DIMACS clause count differs")
    return variables, tuple(clauses)


def edge_variable(first: int, second: int) -> int:
    pair = tuple(sorted((first, second)))
    return list(itertools.combinations(range(13), 2)).index(pair) + 1


def independent_coloring_rows(length: int) -> tuple[tuple[int, ...], ...]:
    positive = {
        tuple(sorted((v, (v + 1) % length)))
        for v in range(length)
    }
    positive.update({(0, length), (1, length)})
    previous = [[] for _ in range(13)]
    for first, second in positive:
        previous[second].append(first)
    for neighbors in previous:
        neighbors.sort()
    row = [-1] * 13
    result = []

    def visit(vertex: int, maximum: int) -> None:
        if vertex == 13:
            result.append(tuple(row))
            return
        for color in range(min(2, maximum + 1) + 1):
            if any(row[neighbor] == color for neighbor in previous[vertex]):
                continue
            row[vertex] = color
            visit(vertex + 1, max(maximum, color))
            row[vertex] = -1

    visit(0, -1)
    return tuple(result)


def b_family_census(module: object, length: int) -> tuple[bytes, dict[str, object]]:
    vm, base, rows, payload = module.reconstruct(length)
    tagged = base + module.derive_coloring_clauses(rows, vm)
    streams: dict[str, bytearray] = {}
    counts: dict[str, list[int]] = {}
    for item in tagged:
        require(item.family in TAG_MAP, f"unmapped B family {item.family}")
        family = TAG_MAP[item.family]
        counts.setdefault(family, [0, 0])
        counts[family][0] += 1
        counts[family][1] += len(item.literals)
        streams.setdefault(family, bytearray()).extend(
            (" ".join(map(str, item.literals)) + " 0\n").encode("ascii")
        )
    census = {
        family: {
            "clauses": counts[family][0],
            "literals": counts[family][1],
            "clause_stream_sha256": sha256_bytes(bytes(streams[family])),
        }
        for family in counts
    }
    return payload, census


def validate_retained_census(value: object, live: Mapping[str, object]) -> None:
    census = exact_dict(value, "retained census")
    require(
        census.get("schema") == "gamma-theta-order13-k3-constructor-gate-census-v1"
        and census.get("schema_version") == 1
        and census.get("classification") == "CONSTRUCTOR_GATE_ONLY"
        and census.get("solver_launched") is False
        and census.get("order") == 13
        and census.get("parameter") == 3,
        "retained census boundary differs",
    )
    claim = census.get("claim_boundary")
    require(
        type(claim) is str
        and "no solver was launched" in claim.lower()
        and "no sat or unsat result is claimed" in claim.lower(),
        "retained census claim boundary differs",
    )
    live_records = {
        record["template"]: record
        for record in live["templates"]
    }
    retained = census.get("templates")
    require(type(retained) is list and len(retained) == 4, "retained template set differs")
    require(
        [record.get("template") for record in retained] == list(TEMPLATES),
        "retained template order differs",
    )
    for record in retained:
        template = record["template"]
        expected = EXPECTED[template]
        live_record = live_records[template]
        required = {
            "template": template,
            "variables": expected["variables"],
            "base_clauses": expected["base_clauses"],
            "base_literals": expected["base_literals"],
            "coloring_rows": expected["coloring_rows"],
            "clauses": expected["clauses"],
            "literals": expected["literals"],
            "size_bytes": expected["size_bytes"],
            "sha256": expected["sha256"],
            "coloring_bank_sha256": expected["bank_sha256"],
        }
        require(
            all(record.get(key) == item for key, item in required.items()),
            f"retained census differs for {template}",
        )
        for key in (
            "variables",
            "coloring_rows",
            "clauses",
            "literals",
            "size_bytes",
            "sha256",
            "coloring_bank_sha256",
        ):
            require(
                live_record.get(key) == required[key],
                f"live census differs for {template}:{key}",
            )


def mutate_package(
    original: Path,
    destination: Path,
    role: str,
) -> None:
    shutil.copytree(original, destination)
    manifest_path = destination / "constructor-manifest.json"
    if role == "source_binding":
        manifest = exact_dict(strict_json_bytes(manifest_path.read_bytes()), "manifest")
        sources = manifest["runtime_sources"]
        sources[0]["sha256"] = "0" * 64
        manifest_path.write_bytes(canonical_json_bytes(manifest))
    elif role == "formula":
        path = destination / "instance.cnf"
        payload = path.read_bytes()
        path.write_bytes(payload[:-1] + b" ")
    elif role == "census":
        manifest = exact_dict(strict_json_bytes(manifest_path.read_bytes()), "manifest")
        manifest["clause_count"] += 1
        manifest_path.write_bytes(canonical_json_bytes(manifest))
    elif role == "bank":
        path = destination / "coloring-bank.json"
        rows = strict_json_bytes(path.read_bytes())
        path.write_bytes(canonical_json_bytes(rows[:-1]))
    elif role == "package_exclusivity":
        (destination / "unexpected.txt").write_text("reject me\n", encoding="utf-8")
    else:
        raise AuditError(f"unknown package mutation {role}")


def physical_memory_bytes() -> int:
    return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")


def validate_plan(
    plan_value: object,
    checkpoint_value: object,
    *,
    package: Path,
    run_directory: Path,
    tool: Path,
) -> None:
    plan = exact_dict(plan_value, "run plan")
    checkpoint = exact_dict(checkpoint_value, "run checkpoint")
    require(
        set(plan)
        == {
            "schema",
            "schema_version",
            "status",
            "claim_boundary",
            "template",
            "source_package",
            "instance",
            "tool",
            "hardware_at_plan_creation",
            "limits",
            "solver_command",
            "resume_protocol",
        },
        "run-plan fields differ",
    )
    require(
        plan["schema"] == "gamma-theta-order13-k3-run-plan-v1"
        and plan["schema_version"] == 1
        and plan["status"] == "READY_NOT_RUN"
        and plan["template"] == "hole11",
        "run-plan identity/status differs",
    )
    require(
        type(plan["claim_boundary"]) is str
        and "has not run" in plan["claim_boundary"]
        and "proof conversion and replay" in plan["claim_boundary"],
        "run-plan claim boundary differs",
    )
    require(plan["source_package"] == str(package.resolve()), "source package differs")
    instance = package / "instance.cnf"
    instance_binding = {
        "name": "instance.cnf",
        "sha256": sha256_bytes(instance.read_bytes()),
        "size_bytes": instance.stat().st_size,
    }
    require(plan["instance"] == instance_binding, "plan instance binding differs")
    tool_binding = {
        "path": str(tool.resolve()),
        "sha256": sha256_bytes(tool.read_bytes()),
        "size_bytes": tool.stat().st_size,
    }
    require(plan["tool"] == tool_binding, "plan tool binding differs")

    hardware = exact_dict(plan["hardware_at_plan_creation"], "hardware metadata")
    require(
        set(hardware)
        == {
            "machine",
            "logical_cpus",
            "physical_memory_bytes",
            "free_disk_bytes",
            "load_average",
        },
        "hardware fields differ",
    )
    require(hardware["machine"] == platform.machine(), "machine metadata differs")
    require(hardware["logical_cpus"] == os.cpu_count(), "CPU metadata differs")
    require(
        hardware["physical_memory_bytes"] == physical_memory_bytes(),
        "memory metadata differs",
    )
    require(
        type(hardware["free_disk_bytes"]) is int and hardware["free_disk_bytes"] > 0,
        "free-disk metadata differs",
    )
    loads = hardware["load_average"]
    require(
        type(loads) is list
        and len(loads) == 3
        and all(type(value) is float and math.isfinite(value) and value >= 0 for value in loads),
        "load-average metadata differs",
    )

    limits = {
        "solver_wall_seconds": 1800,
        "solver_memory_mib": 2048,
        "proof_file_limit_mib": 2048,
        "disk_reserve_mib": 8192,
        "memory_reserve_mib": 2048,
        "load_average_maximum": 7.5,
        "parallel_processes": 1,
    }
    require(plan["limits"] == limits, "resource limits differ")
    require(
        limits["solver_memory_mib"] * (1 << 20)
        < physical_memory_bytes() * 3 // 4,
        "planned solver memory exceeds 75 percent",
    )
    attempt = run_directory.resolve() / "attempt-000001"
    expected_command = [
        str(tool.resolve()),
        "--seed=0",
        "--binary",
        "--no-colors",
        "-q",
        "-t",
        "1800",
        "-w",
        str(attempt / "solver.result"),
        str(attempt / "instance.cnf"),
        str(attempt / "proof.raw.bdrat"),
    ]
    require(plan["solver_command"] == expected_command, "future solver command differs")
    require(
        plan["resume_protocol"]
        == {
            "next_attempt": 1,
            "refuse_if_attempt_directory_exists": True,
            "copy_frozen_instance_into_attempt": True,
            "rehash_instance_and_tool_before_launch": True,
            "write_resource_report_before_and_after_child": True,
            "checkpoint_after_every_attempt": True,
        },
        "resume protocol differs",
    )
    require(
        checkpoint
        == {
            "schema": "gamma-theta-order13-k3-run-checkpoint-v1",
            "schema_version": 1,
            "sequence": 0,
            "status": "READY_NOT_RUN",
            "attempts": [],
            "next_attempt": 1,
            "plan_sha256": sha256_bytes(canonical_json_bytes(plan)),
        },
        "initial checkpoint differs",
    )


def expect_plan_rejection(
    plan: object,
    checkpoint: object,
    *,
    package: Path,
    run_directory: Path,
    tool: Path,
) -> bool:
    try:
        validate_plan(
            plan,
            checkpoint,
            package=package,
            run_directory=run_directory,
            tool=tool,
        )
    except (AuditError, KeyError, TypeError):
        return True
    return False


def run() -> dict[str, object]:
    bindings_before = bind_frozen_files()
    b_module = load_b_module()
    independent_evidence = exact_dict(
        strict_json_bytes(
            (ROOT / "reviews/order13_k3_constructor_independent/evidence.json").read_bytes()
        ),
        "constructor B evidence",
    )
    require(
        independent_evidence.get("verdict")
        == "ACCEPT_EXACT_CLEAN_ROOM_RECONSTRUCTION"
        and independent_evidence.get("all_mutations_detected") is True,
        "constructor B evidence is not accepted",
    )

    tests = run_child(
        (
            str(PYTHON),
            "-W",
            "error",
            "-m",
            "unittest",
            "-v",
            "tests.test_order13_k3_constructor",
        ),
        timeout=300,
    )
    require(
        tests.returncode == 0,
        f"warnings-fatal focused tests failed: {tests.stderr.decode('utf-8', 'replace')}",
    )
    test_transcript = tests.stdout + tests.stderr
    match = re.search(rb"Ran ([0-9]+) tests?", test_transcript)
    require(match is not None and int(match.group(1)) == 7, "focused test census differs")
    require(b"OK" in test_transcript, "focused tests lack OK verdict")

    live_census_child = run_a_command("census")
    live_census = exact_dict(
        strict_json_bytes(live_census_child.stdout),
        "live census",
    )
    require(
        live_census.get("schema")
        == "gamma-theta-order13-k3-constructor-census-v1"
        and live_census.get("classification") == "CONSTRUCTOR_GATE_ONLY"
        and live_census.get("solver_launched") is False,
        "live census boundary differs",
    )
    retained_census_payload = (
        ROOT / "results/order13_k3_constructor_gate/census.json"
    ).read_bytes()
    retained_census = strict_json_bytes(retained_census_payload)
    validate_retained_census(retained_census, live_census)
    census_mutant = copy.deepcopy(retained_census)
    census_mutant["templates"][0]["clauses"] += 1
    census_mutation_rejected = False
    try:
        validate_retained_census(census_mutant, live_census)
    except AuditError:
        census_mutation_rejected = True
    require(census_mutation_rejected, "retained census mutation was accepted")

    template_evidence = []
    package_mutations: dict[str, bool] = {}
    planner_evidence: dict[str, object]
    with tempfile.TemporaryDirectory(
        prefix=".order13-k3-acceptance-",
        dir=ROOT / "results",
    ) as temporary:
        temporary_root = Path(temporary)
        packages: dict[str, Path] = {}
        for template in TEMPLATES:
            package = temporary_root / f"package-{template}"
            generate = run_a_command(
                "generate",
                "--template",
                template,
                "--output-directory",
                str(package),
                "--validation-gate",
            )
            generated_manifest = exact_dict(
                strict_json_bytes(generate.stdout),
                f"{template} generation output",
            )
            package_manifest_payload = (package / "constructor-manifest.json").read_bytes()
            require(
                canonical_json_bytes(generated_manifest) == package_manifest_payload,
                f"{template} CLI/installed manifest differs",
            )
            require(
                {entry.name for entry in package.iterdir()}
                == {
                    "instance.cnf",
                    "coloring-bank.json",
                    "constructor-manifest.json",
                },
                f"{template} package is not exclusive",
            )
            audit = run_a_command(
                "audit",
                "--package-directory",
                str(package),
                "--exhaustive",
            )
            audit_report = exact_dict(
                strict_json_bytes(audit.stdout),
                f"{template} audit output",
            )
            require(
                audit_report.get("accepted") is True
                and audit_report.get("solver_launched") is False
                and audit_report.get("exhaustive_reconstruction") is True,
                f"{template} exhaustive audit not accepted",
            )

            instance = (package / "instance.cnf").read_bytes()
            variables, clauses = parse_dimacs(instance)
            length = int(template[4:])
            b_output = temporary_root / f"b-{template}.cnf"
            b_child = run_child(
                (
                    str(PYTHON),
                    "-W",
                    "error",
                    "reviews/order13_k3_constructor_independent/reconstruct.py",
                    "emit",
                    "--hole",
                    str(length),
                    "--output",
                    str(b_output),
                )
            )
            require(
                b_child.returncode == 0,
                f"constructor B emit failed: {b_child.stderr.decode('utf-8', 'replace')}",
            )
            b_bytes = b_output.read_bytes()
            require(instance == b_bytes, f"{template} A/B DIMACS bytes differ")
            expected_b, b_families = b_family_census(b_module, length)
            require(instance == expected_b, f"{template} imported B bytes differ")
            require(
                generated_manifest.get("clause_families") == b_families,
                f"{template} clause-family streams differ from B",
            )

            bank_payload = (package / "coloring-bank.json").read_bytes()
            bank_raw = strict_json_bytes(bank_payload)
            require(type(bank_raw) is list, f"{template} bank is not a list")
            bank = tuple(tuple(row) for row in bank_raw)
            independent_bank = independent_coloring_rows(length)
            require(bank == independent_bank, f"{template} coloring bank is incomplete")
            labeled_count = ((1 << length) - 2) * (3 ** (12 - length))
            require(
                labeled_count == len(bank) * 6,
                f"{template} color-orbit identity differs",
            )

            fixed = (0, 1, length)
            unit_clauses = {clause for clause in clauses if len(clause) == 1}
            fixed_units = {
                (edge_variable(first, second),)
                for first, second in itertools.combinations(fixed, 2)
            }
            require(
                fixed_units <= unit_clauses,
                f"{template} fixed independent triple is absent",
            )
            require(
                generated_manifest.get("fixed_independent_triple_in_g")
                == list(fixed)
                and generated_manifest.get("heuristic_symmetry_breakers") == [],
                f"{template} anchor/symmetry metadata differs",
            )
            require(
                variables == EXPECTED[template]["variables"]
                and len(clauses) == EXPECTED[template]["clauses"]
                and sha256_bytes(instance) == EXPECTED[template]["sha256"]
                and sha256_bytes(bank_payload) == EXPECTED[template]["bank_sha256"],
                f"{template} formula/bank expected binding differs",
            )

            runtime_paths = [
                record["path"]
                for record in generated_manifest["runtime_sources"]
            ]
            require(
                runtime_paths
                == [
                    "src/search/order13_k3/__init__.py",
                    "src/search/order13_k3/__main__.py",
                    "src/search/order13_k3/encoding.py",
                    "src/search/order13_k3/generate.py",
                ],
                f"{template} runtime source list differs",
            )
            require(
                generated_manifest.get("generation_environment")
                == {
                    "python_implementation": platform.python_implementation(),
                    "python_version": platform.python_version(),
                },
                f"{template} Python metadata differs",
            )
            require(
                generated_manifest.get("production_defaults")
                == {
                    "seed": 0,
                    "solver_wall_seconds": 1800,
                    "solver_memory_mib": 2048,
                    "proof_file_limit_mib": 2048,
                    "disk_reserve_mib": 8192,
                    "memory_reserve_mib": 2048,
                    "maximum_parallel_solver_processes": 1,
                },
                f"{template} production defaults differ",
            )
            template_evidence.append(
                {
                    "template": template,
                    "variables": variables,
                    "clauses": len(clauses),
                    "literals": sum(map(len, clauses)),
                    "size_bytes": len(instance),
                    "sha256": sha256_bytes(instance),
                    "bank_rows": len(bank),
                    "bank_sha256": sha256_bytes(bank_payload),
                    "manifest_sha256": sha256_bytes(package_manifest_payload),
                    "constructor_a_exhaustive_audit": True,
                    "constructor_b_byte_identical": True,
                    "clause_family_names_counts_stream_hashes_match_b": True,
                    "fixed_independent_triple": list(fixed),
                    "complete_coloring_coverage": True,
                    "package_entries_exclusive": True,
                }
            )
            packages[template] = package

        mutation_source = packages["hole11"]
        for role in (
            "source_binding",
            "formula",
            "census",
            "bank",
            "package_exclusivity",
        ):
            mutant = temporary_root / f"mutant-{role}"
            mutate_package(mutation_source, mutant, role)
            run_a_command(
                "audit",
                "--package-directory",
                str(mutant),
                expect_success=False,
            )
            package_mutations[role] = True

        fake_tool = temporary_root / "cadical-never-run"
        fake_tool.write_text(
            '#!/bin/sh\ntouch "$(dirname "$0")/EXECUTED"\nexit 99\n',
            encoding="utf-8",
        )
        fake_tool.chmod(0o700)
        run_directory = temporary_root / "run-hole11"
        plan_child = run_a_command(
            "plan",
            "--package-directory",
            str(packages["hole11"]),
            "--output-directory",
            str(run_directory),
            "--cadical",
            str(fake_tool),
            "--validation-gate",
        )
        require(
            not (temporary_root / "EXECUTED").exists(),
            "run-plan creation executed the fake solver",
        )
        require(
            {entry.name for entry in run_directory.iterdir()}
            == {"instance.cnf", "run-plan.json", "checkpoint-000000.json"},
            "READY_NOT_RUN package entries differ",
        )
        require(
            not (run_directory / "attempt-000001").exists(),
            "run-plan creation made an attempt directory",
        )
        plan = strict_json_bytes((run_directory / "run-plan.json").read_bytes())
        checkpoint = strict_json_bytes(
            (run_directory / "checkpoint-000000.json").read_bytes()
        )
        require(
            strict_json_bytes(plan_child.stdout) == plan,
            "CLI and installed run plan differ",
        )
        validate_plan(
            plan,
            checkpoint,
            package=packages["hole11"],
            run_directory=run_directory,
            tool=fake_tool,
        )
        planner_mutations: dict[str, bool] = {}
        for role in (
            "status",
            "resource_limit",
            "solver_command",
            "hardware",
            "checkpoint_hash",
        ):
            mutated_plan = copy.deepcopy(plan)
            mutated_checkpoint = copy.deepcopy(checkpoint)
            if role == "status":
                mutated_plan["status"] = "RUNNING"
            elif role == "resource_limit":
                mutated_plan["limits"]["solver_memory_mib"] = 8192
            elif role == "solver_command":
                mutated_plan["solver_command"].insert(1, "--unexpected")
            elif role == "hardware":
                mutated_plan["hardware_at_plan_creation"][
                    "physical_memory_bytes"
                ] += 1
            elif role == "checkpoint_hash":
                mutated_checkpoint["plan_sha256"] = "0" * 64
            planner_mutations[role] = expect_plan_rejection(
                mutated_plan,
                mutated_checkpoint,
                package=packages["hole11"],
                run_directory=run_directory,
                tool=fake_tool,
            )
        require(all(planner_mutations.values()), "planner mutation was accepted")
        planner_evidence = {
            "status": "READY_NOT_RUN",
            "solver_executed": False,
            "attempt_directory_created": False,
            "package_entries_exclusive": True,
            "instance_and_tool_hash_bound": True,
            "hardware_metadata_validated": True,
            "resource_limits_validated": True,
            "memory_ceiling_below_75_percent": True,
            "checkpoint_zero_validated": True,
            "mutations_rejected": planner_mutations,
            "claim_boundary": (
                "Plan metadata only; no execution runner or proof acceptance "
                "is certified by this audit."
            ),
        }

    bindings_after = bind_frozen_files()
    require(bindings_after == bindings_before, "frozen files changed during audit")
    return {
        "schema": "gamma-theta-order13-k3-constructor-acceptance-v1",
        "schema_version": 1,
        "acceptance_audit": file_record(
            "reviews/order13_k3_constructor_acceptance/audit.py"
        ),
        "bindings": bindings_after,
        "environment": {
            "machine": platform.machine(),
            "logical_cpus": os.cpu_count(),
            "physical_memory_bytes": physical_memory_bytes(),
            "python_implementation": platform.python_implementation(),
            "python_version": platform.python_version(),
        },
        "warnings_fatal_test_suite": {
            "command": (
                "python3 -W error -m unittest -v "
                "tests.test_order13_k3_constructor"
            ),
            "tests_run": 7,
            "passed": True,
        },
        "live_census": {
            "sha256": sha256_bytes(live_census_child.stdout),
            "classification": live_census["classification"],
            "solver_launched": live_census["solver_launched"],
        },
        "retained_census": {
            "sha256": sha256_bytes(retained_census_payload),
            "exact_against_live_and_b": True,
            "mutation_rejected": census_mutation_rejected,
        },
        "templates": template_evidence,
        "package_mutations_rejected": package_mutations,
        "planner": planner_evidence,
        "source_bindings_stable_pre_post": True,
        "subprocess_allowlist": [
            "constructor A generate",
            "constructor A audit",
            "constructor A census",
            "constructor A plan",
            "constructor A focused unit tests",
            "constructor B emit",
        ],
        "solver_launched": False,
        "verdict": "ACCEPT_CONSTRUCTOR_A_FOR_PROOF_PRODUCTION_INPUTS",
        "claim_boundary": (
            "Accepts deterministic order-13 k=3 formula construction, package "
            "generation, and READY_NOT_RUN planning only. It proves no formula "
            "UNSAT and certifies no solver runner, proof conversion, proof "
            "checker, or four-branch finite exclusion."
        ),
    }


def main() -> int:
    print(json.dumps(run(), allow_nan=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
