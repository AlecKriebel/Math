#!/usr/bin/env python3
"""Fail-closed mutation suite for the independent weak-sharpness audit."""

from __future__ import annotations

import argparse
import copy
import json
import os
import subprocess
import sys
import tempfile
from fractions import Fraction as F
from pathlib import Path

import audit_weak_sharpness as audit


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
AUTHORITATIVE_OUTPUT = HERE / "mutation_report.json"
SCHEMA = "k2p-weak-sharpness-audit-mutations-v2"
SUCCESS_TERMINAL = "K2P_WEAK_SHARPNESS_INDEPENDENT_AUDIT_PASS"
EXPECTED_DIAGNOSTICS = {
    "omitted_graph_arc": "X: retic has degree (2, 0), expected (2, 1)",
    "reversed_reticulation_arc": "Z: tree has degree (2, 1), expected (1, 2)",
    "reticulation_role_changed": "V: tree has degree (2, 1), expected (1, 2)",
    "reticulation_arrowhead_removed": "mutated arrowhead census",
    "first_rooting_count": "primary first census drift",
    "second_tree_child_count": "primary second census drift",
    "stored_inheritance": "primary inheritance drift",
    "stored_internal_pair": "primary internal parameter drift",
    "stored_arm_pair": "primary pendant parameter drift",
    "actual_inheritance_reevaluation": (
        "independent normalized tensor differs from stated tensor"
    ),
    "common_tensor_entry": "primary common tensor reassigned",
    "normalized_tensor_entry": "primary normalized tensor drift",
    "minor_determinant": "primary minor determinant is reassigned",
    "minor_column_repeated": (
        "primary stored minor vanishes under independent expansion"
    ),
    "rank_claim_lowered": "primary rank claim drift",
    "actual_cherry_CT_pair": "mutant: outside D_plus",
    "cherry_jacobian_entry": "mutated determinant",
    "stored_cherry_determinant": "primary cherry determinant drift",
    "broken_cherry_pruning": "new leaf is not in a cherry",
    "cherry_edge_ceases_to_be_bridge": "mutated edge not bridge",
    "optimized_mode": "WEAK_SHARPNESS_AUDIT_OPTIMIZED_MODE_FORBIDDEN",
}
RESULTS: list[dict[str, object]] = []


def fail(code: str, detail: object | None = None) -> "None":
    raise RuntimeError(code if detail is None else f"{code}:{detail}")


def sha_file(path: Path) -> str:
    return audit.hashlib.sha256(path.read_bytes()).hexdigest()


def validate_output_path(output: Path, allow_authoritative: bool = False) -> Path:
    lexical = Path(os.path.abspath(os.fspath(output)))
    normalized = lexical.parent.resolve() / lexical.name
    resolved = lexical.resolve()
    canonical = AUTHORITATIVE_OUTPUT.parent.resolve() / AUTHORITATIVE_OUTPUT.name
    if allow_authoritative:
        if normalized != canonical or resolved != canonical:
            fail(
                "WEAK_SHARPNESS_MUTATION_OUTPUT_POLICY_FAIL",
                "authoritative override requires the exact nonsymbolic canonical report",
            )
        return canonical
    project_root = PROJECT.resolve()
    for candidate in (normalized, resolved):
        try:
            candidate.relative_to(project_root)
        except ValueError:
            continue
        break
    else:
        return normalized
    fail(
        "WEAK_SHARPNESS_MUTATION_OUTPUT_POLICY_FAIL",
        "routine report output must be outside the project source tree",
    )


def prepare_output(output: Path) -> None:
    output.unlink(missing_ok=True)


def atomic_write_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o644)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
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


def qualify_exception(name: str, error: Exception) -> dict[str, object]:
    expected = EXPECTED_DIAGNOSTICS[name]
    if type(error) is not RuntimeError or str(error) != expected:
        fail(
            "WEAK_SHARPNESS_MUTATION_DIAGNOSTIC_FAIL",
            {
                "mutation": name,
                "expected_type": "RuntimeError",
                "observed_type": type(error).__name__,
                "expected": expected,
                "observed": str(error),
            },
        )
    return {
        "mutation": name,
        "status": "rejected",
        "expected_exception_type": "RuntimeError",
        "observed_exception_type": "RuntimeError",
        "expected_diagnostic": expected,
        "observed_diagnostic": expected,
    }


def must_reject(label: str, action) -> None:
    try:
        action()
    except Exception as error:
        RESULTS.append(qualify_exception(label, error))
        return
    fail("WEAK_SHARPNESS_MUTATION_SURVIVED", label)


def mutated(primary: dict[str, object], action) -> dict[str, object]:
    result = copy.deepcopy(primary)
    action(result)
    return result


def demand_first_census(mixed) -> None:
    census = audit.rooting_census(mixed)
    audit.require(
        (census["admissible_rootings"], census["tree_child_rootings"], census["non_tree_child_rootings"])
        == (5, 2, 3),
        "mutated census",
    )
    audit.require(census["reticulation_edges_explicitly_tried"] == 4, "mutated arrowhead census")


def qualify_optimized_failure(observation: dict[str, object]) -> dict[str, object]:
    expected = EXPECTED_DIAGNOSTICS["optimized_mode"]
    output = str(observation.get("output", ""))
    returncode = observation.get("returncode")
    if observation.get("timeout") is not False:
        fail("WEAK_SHARPNESS_MUTATION_TIMEOUT", "optimized_mode")
    if observation.get("signal") is not False or (
        isinstance(returncode, int) and returncode < 0
    ):
        fail("WEAK_SHARPNESS_MUTATION_SIGNAL_EXIT", "optimized_mode")
    if returncode != 1:
        fail(
            "WEAK_SHARPNESS_MUTATION_EXIT_CODE_FAIL",
            {"mutation": "optimized_mode", "returncode": returncode},
        )
    forbidden = [
        token
        for token in (
            "Traceback (most recent call last)",
            "AssertionError",
            "ModuleNotFoundError",
            "ImportError",
        )
        if token in output
    ]
    if forbidden:
        fail("WEAK_SHARPNESS_MUTATION_UNRELATED_CRASH", forbidden)
    if observation.get("success_artifact_present") is not False:
        fail("WEAK_SHARPNESS_MUTATION_SUCCESS_ARTIFACT", "optimized_mode")
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    if lines != [expected]:
        fail(
            "WEAK_SHARPNESS_MUTATION_DIAGNOSTIC_FAIL",
            {"mutation": "optimized_mode", "expected": expected, "observed": lines},
        )
    return {
        "mutation": "optimized_mode",
        "status": "rejected",
        "returncode": 1,
        "expected_diagnostic": expected,
        "observed_diagnostic": expected,
        "timeout": False,
        "signal": False,
        "success_artifact_present": False,
        "forbidden_crash_text_present": False,
    }


def qualification_negative_controls() -> dict[str, bool]:
    exception_name = "omitted_graph_arc"
    controls: dict[str, bool] = {}
    for label, error in (
        ("wrong_exception_type_rejected", ValueError(EXPECTED_DIAGNOSTICS[exception_name])),
        ("wrong_diagnostic_rejected", RuntimeError("unrelated diagnostic")),
    ):
        try:
            qualify_exception(exception_name, error)
        except RuntimeError:
            controls[label] = True
        else:
            fail("WEAK_SHARPNESS_MUTATION_NEGATIVE_CONTROL_SURVIVED", label)
    expected = EXPECTED_DIAGNOSTICS["optimized_mode"]
    valid = {
        "returncode": 1,
        "output": expected,
        "timeout": False,
        "signal": False,
        "success_artifact_present": False,
    }
    optimized_controls = {
        "optimized_wrong_diagnostic_rejected": {**valid, "output": expected + ":wrong"},
        "optimized_traceback_rejected": {
            **valid,
            "output": f"Traceback (most recent call last):\nRuntimeError: {expected}",
        },
        "optimized_import_error_rejected": {
            **valid,
            "output": f"ModuleNotFoundError: dependency\n{expected}",
        },
        "optimized_timeout_rejected": {**valid, "returncode": None, "timeout": True},
        "optimized_signal_rejected": {**valid, "returncode": -9, "signal": True},
        "optimized_non_one_exit_rejected": {**valid, "returncode": 2},
        "optimized_success_artifact_rejected": {
            **valid,
            "output": f"{expected}\n{SUCCESS_TERMINAL}",
            "success_artifact_present": True,
        },
    }
    for label, observation in optimized_controls.items():
        try:
            qualify_optimized_failure(observation)
        except RuntimeError:
            controls[label] = True
        else:
            fail("WEAK_SHARPNESS_MUTATION_NEGATIVE_CONTROL_SURVIVED", label)
    return controls


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-authoritative-output", action="store_true")
    parser.add_argument("--timeout-seconds", type=float, default=60.0)
    args = parser.parse_args()
    output_path = validate_output_path(args.output, args.allow_authoritative_output)
    prepare_output(output_path)
    if not __debug__:
        raise SystemExit("WEAK_SHARPNESS_MUTATIONS_OPTIMIZED_MODE_FORBIDDEN")
    if args.timeout_seconds <= 0:
        fail("WEAK_SHARPNESS_MUTATION_TIMEOUT_INVALID")
    RESULTS.clear()
    source_fingerprints = {
        "primary_certificate_sha256": sha_file(audit.PRIMARY),
        "independent_audit_certificate_sha256": sha_file(
            audit.HERE / "audit_certificate.json"
        ),
        "independent_audit_verifier_sha256": sha_file(
            audit.HERE / "audit_weak_sharpness.py"
        ),
        "mutation_runner_sha256": sha_file(Path(__file__).resolve()),
    }
    primary = json.loads(audit.PRIMARY.read_text())
    baseline_payload = audit.build_audit(primary)
    baseline = dict(baseline_payload)
    baseline["payload_sha256"] = audit.digest(baseline_payload)
    frozen_baseline = json.loads((audit.HERE / "audit_certificate.json").read_text())
    if baseline != frozen_baseline:
        fail("WEAK_SHARPNESS_MUTATION_BASELINE_BYTE_LOGIC_FAIL")
    clean_baseline = {
        "status": "PASS",
        "payload_sha256": baseline["payload_sha256"],
        "certificate_sha256": source_fingerprints[
            "independent_audit_certificate_sha256"
        ],
        "exact_object_equal": True,
        "rooting_censuses": [[5, 2, 3], [7, 2, 5]],
        "ranks": [9, 9],
        "relation": "none",
    }
    negative_controls = qualification_negative_controls()
    first_spec, second_spec = audit.independent_specs()
    first = audit.rooted_graph(first_spec)
    second = audit.rooted_graph(second_spec)

    # Graph arc and role mutations.
    must_reject(
        "omitted_graph_arc",
        lambda: audit.rooted_graph(
            audit.NetworkSpec(first_spec.name, first_spec.nodes, first_spec.arcs[:-1])
        ),
    )
    reversed_arcs = tuple(("X", "Z") if edge == ("Z", "X") else edge for edge in first_spec.arcs)
    must_reject(
        "reversed_reticulation_arc",
        lambda: audit.rooted_graph(audit.NetworkSpec(first_spec.name, first_spec.nodes, reversed_arcs)),
    )
    wrong_roles = tuple(
        (node, "tree" if node == "V" else role, label) for node, role, label in first_spec.nodes
    )
    must_reject(
        "reticulation_role_changed",
        lambda: audit.rooted_graph(audit.NetworkSpec(first_spec.name, wrong_roles, first_spec.arcs)),
    )
    mixed = audit.semi_directed(first)
    mixed.edges["U", "V"]["heads"] = frozenset()
    must_reject("reticulation_arrowhead_removed", lambda: demand_first_census(mixed))

    # Stored rooting-count mutations.
    bad = mutated(
        primary,
        lambda value: value["first"]["rooting_census"].__setitem__("admissible_rootings", 4),
    )
    must_reject("first_rooting_count", lambda: audit.build_audit(bad))
    bad = mutated(
        primary,
        lambda value: value["second"]["rooting_census"].__setitem__("tree_child_rootings", 3),
    )
    must_reject("second_tree_child_count", lambda: audit.build_audit(bad))

    # Parameter mutations, both stored and actually re-evaluated.
    bad = mutated(
        primary,
        lambda value: value["first"]["parameter_certificate"].__setitem__("lambdas", ["1/2", "1/8"]),
    )
    must_reject("stored_inheritance", lambda: audit.build_audit(bad))
    bad = mutated(
        primary,
        lambda value: value["first"]["parameter_certificate"].__setitem__("internal_edge_pair", ["1/6", "1/7"]),
    )
    must_reject("stored_internal_pair", lambda: audit.build_audit(bad))
    bad = mutated(
        primary,
        lambda value: value["second"]["parameter_certificate"]["arm_pairs"][0].__setitem__(0, "1/2"),
    )
    must_reject("stored_arm_pair", lambda: audit.build_audit(bad))

    def reevaluate_wrong_lambda() -> None:
        local = copy.deepcopy(primary["first"]["parameter_certificate"])
        local["lambdas"] = ["1/2", "1/8"]
        audit.case_certificate(
            first,
            F(1, 7),
            (F(1, 2), F(1, 8)),
            (F(86779, 80), F(320, 253), F(114373, 20240)),
            F(1, 2**30),
            (
                F(1), F(64009, 457492), F(64009, 457492), F(6400, 39229939),
                F(1, 1372), F(4048, 39229939), F(4048, 39229939),
                F(6400, 39229939), F(4048, 39229939), F(1, 1372),
            ),
            local,
        )

    must_reject("actual_inheritance_reevaluation", reevaluate_wrong_lambda)

    # Tensor-entry and minor mutations.
    bad = mutated(primary, lambda value: value["common_tensor"].__setitem__(1, "2"))
    must_reject("common_tensor_entry", lambda: audit.build_audit(bad))
    bad = mutated(
        primary,
        lambda value: value["first"]["parameter_certificate"]["normalized_tensor"].__setitem__(2, "0"),
    )
    must_reject("normalized_tensor_entry", lambda: audit.build_audit(bad))
    bad = mutated(
        primary,
        lambda value: value["first"]["parameter_certificate"].__setitem__("minor_determinant", "1"),
    )
    must_reject("minor_determinant", lambda: audit.build_audit(bad))
    bad = mutated(
        primary,
        lambda value: value["second"]["parameter_certificate"]["minor_columns"].__setitem__(8, 0),
    )
    must_reject("minor_column_repeated", lambda: audit.build_audit(bad))
    bad = mutated(
        primary,
        lambda value: value["second"]["parameter_certificate"].__setitem__("rank", 8),
    )
    must_reject("rank_claim_lowered", lambda: audit.build_audit(bad))

    # Cherry-domain, determinant, and pruning mutations.
    must_reject("actual_cherry_CT_pair", lambda: audit.check_domain((F(4, 5), F(1, 2)), "mutant"))

    def wrong_cherry_determinant() -> None:
        block = [
            [*audit.cherry_block(F(2, 5), F(3, 7))[0], F(0), F(0)],
            [*audit.cherry_block(F(2, 5), F(3, 7))[1], F(0), F(0)],
            [F(0), F(0), *audit.cherry_block(F(4, 9), F(5, 11))[0]],
            [F(0), F(0), *audit.cherry_block(F(4, 9), F(5, 11))[1]],
        ]
        block[0][0] += 1
        audit.require(
            audit.determinant(block) == F(4) * F(2, 5) * F(4, 9) / (F(3, 7) * F(5, 11)),
            "mutated determinant",
        )

    must_reject("cherry_jacobian_entry", wrong_cherry_determinant)
    bad = mutated(
        primary,
        lambda value: value["cherry_extension"].__setitem__("four_by_four_determinant", "1"),
    )
    must_reject("stored_cherry_determinant", lambda: audit.build_audit(bad))

    def broken_pruning() -> None:
        candidate = next(
            graph
            for index, edge in enumerate(sorted(tuple(sorted(e)) for e in audit.semi_directed(first).edges()))
            for graph in audit.orientations_on_edge(audit.semi_directed(first), edge, index)
        )
        extended = audit.attach_directed_cherry(candidate, 0, 3)
        extended.add_node("extra_leaf", role="leaf", label=4)
        extended.add_edge("cherry_parent_3", "extra_leaf")
        audit.prune_directed_cherry(extended, 3)

    must_reject("broken_cherry_pruning", broken_pruning)

    def nonbridge_attachment() -> None:
        extended = audit.attach_mixed_cherry(audit.semi_directed(first), 0, 3)
        extended.add_edge("new_leaf_3", "S", heads=frozenset())
        bridge_set = {frozenset(edge) for edge in audit.nx.bridges(extended)}
        audit.require(frozenset(("new_leaf_3", "cherry_parent_3")) in bridge_set, "mutated edge not bridge")

    must_reject("cherry_edge_ceases_to_be_bridge", nonbridge_attachment)

    # Python optimized mode must never erase the verifier's guards.
    try:
        process = subprocess.run(
            [sys.executable, "-O", "-B", str(audit.HERE / "audit_weak_sharpness.py")],
            text=True,
            capture_output=True,
            check=False,
            timeout=args.timeout_seconds,
        )
        optimized_observation = {
            "returncode": process.returncode,
            "output": process.stdout + process.stderr,
            "timeout": False,
            "signal": process.returncode < 0,
            "success_artifact_present": SUCCESS_TERMINAL
            in (process.stdout + process.stderr).splitlines(),
        }
    except subprocess.TimeoutExpired as error:
        optimized_observation = {
            "returncode": None,
            "output": "".join(
                value.decode("utf-8", "replace")
                if isinstance(value, bytes)
                else (value or "")
                for value in (error.stdout, error.stderr)
            ),
            "timeout": True,
            "signal": False,
            "success_artifact_present": False,
        }
    RESULTS.append(qualify_optimized_failure(optimized_observation))

    expected_order = list(EXPECTED_DIAGNOSTICS)
    if [row["mutation"] for row in RESULTS] != expected_order:
        fail("WEAK_SHARPNESS_MUTATION_ORDER_FAIL")
    after_fingerprints = {
        "primary_certificate_sha256": sha_file(audit.PRIMARY),
        "independent_audit_certificate_sha256": sha_file(
            audit.HERE / "audit_certificate.json"
        ),
        "independent_audit_verifier_sha256": sha_file(
            audit.HERE / "audit_weak_sharpness.py"
        ),
        "mutation_runner_sha256": sha_file(Path(__file__).resolve()),
    }
    if after_fingerprints != source_fingerprints:
        fail("WEAK_SHARPNESS_MUTATION_SOURCE_TREE_DRIFT")
    payload = {
        "schema": SCHEMA,
        "status": "PASS",
        **source_fingerprints,
        "clean_baseline": clean_baseline,
        "diagnostic_contract": EXPECTED_DIAGNOSTICS,
        "execution_contract": {
            "exact_exception_type_and_diagnostic_required": True,
            "optimized_mode_requires_exit_code_one": True,
            "traceback_import_timeout_signal_non_one_forbidden": True,
            "success_terminal_forbidden": True,
            "source_tree_unchanged": True,
        },
        "qualification_negative_controls": negative_controls,
        "mutation_count": len(RESULTS),
        "mutations_rejected": len(RESULTS),
        "mutations_survived": 0,
        "cases": RESULTS,
        "conclusion": "PASS",
    }
    report = dict(payload)
    report["payload_sha256"] = audit.digest(payload)
    atomic_write_bytes(
        output_path, (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()
    )
    print("K2P_WEAK_SHARPNESS_AUDIT_MUTATIONS_PASS")
    print(
        json.dumps(
            {
                "mutations_rejected": len(RESULTS),
                "optimized_mode_rejected": True,
                "payload_sha256": report["payload_sha256"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
