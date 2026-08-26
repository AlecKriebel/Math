#!/usr/bin/env python3
"""Adversarial mutations for the physical probe-input contract."""

from __future__ import annotations

import argparse
import collections
import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
CONTRACT = HERE / "probe_input_contract.json"
STRUCTURE = HERE / "verify_probe_input_structure.py"
FULL = HERE / "verify_probe_input_contract.py"
OUTPUT = HERE / "probe_input_mutation_certificate.json"
AUTHORITATIVE_OUTPUT = OUTPUT
REPLAY = HERE / "probe_input_independent_verification.json"
PROJECT = HERE.parents[1]
FORBIDDEN_FAILURE_MARKERS = (
    "Traceback (most recent call last)",
    "ModuleNotFoundError",
    "ImportError",
    "No module named",
)
MUTATION_DIAGNOSTICS = {
    "omitted_anchor_record": "PROBE_INPUT_STRUCTURE_FAIL:anchor count",
    "old_172_anchor_count_reintroduction": "PROBE_INPUT_STRUCTURE_FAIL:anchor count",
    "duplicate_replacing_new_triangle_anchor": "PROBE_INPUT_STRUCTURE_FAIL:anchor ids",
    "raw67161_locator_reassignment": (
        "PROBE_INPUT_STRUCTURE_FAIL:regression rows:{67167: "
        "('four_port_restored_physical_k5', 'triangle'), 67401: "
        "('four_port_restored_physical_k5', 'triangle'), 67407: "
        "('four_port_restored_physical_k5', 'triangle')}"
    ),
    "collapse_two_k7_path_ids_sharing_topology_id": "PROBE_INPUT_STRUCTURE_FAIL:anchor ids",
    "omitted_pendant_arm": "PROBE_INPUT_STRUCTURE_FAIL:site formula:four:raw2040:source",
    "omitted_reticulation_incoming": "PROBE_INPUT_STRUCTURE_FAIL:site formula:four:raw2040:source",
    "dropped_root_suppressed_segment": "PROBE_INPUT_STRUCTURE_FAIL:site formula:four:raw2040:source",
    "split_artificial_root_halves": "PROBE_INPUT_STRUCTURE_FAIL:site formula:four:raw2040:source",
    "wrong_root_half_equivalence": "PROBE_INPUT_STRUCTURE_FAIL:half relation:four:raw2040:source",
    "wrong_site_transport": "PROBE_INPUT_STRUCTURE_FAIL:site transport mapping:four:raw2040",
    "corrupt_anchor_parent_transport": "PROBE_INPUT_STRUCTURE_FAIL:site transport mapping:four:raw2040",
    "wrong_site_formula": "PROBE_INPUT_STRUCTURE_FAIL:reported formula",
    "topology_first_classifier_reintroduction": "PROBE_INPUT_STRUCTURE_FAIL:classifier order",
    "triple_type_gate_reintroduction": "PROBE_INPUT_STRUCTURE_FAIL:classifier order",
    "forbidden_rooted_restriction_removed": "PROBE_INPUT_STRUCTURE_FAIL:forbidden shortcuts",
    "raw4424_false_tree_sunlet_reintroduction": "PROBE_INPUT_STRUCTURE_FAIL:top-level fields",
    "generic_rooted_restriction_reintroduction": "PROBE_INPUT_STRUCTURE_FAIL:top-level fields",
    "ordered_row_hash_omission": "PROBE_INPUT_STRUCTURE_FAIL:row hash order",
    "upstream_input_binding_corruption": "PROBE_INPUT_VERIFY_FAIL:input bindings",
    "optimized_mode": "PROBE_INPUT_STRUCTURE_OPTIMIZED_MODE_FORBIDDEN",
}


class MutationFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise MutationFailure(message)


def sha(value):
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


def sha_file(path):
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
    if allow_authoritative_output:
        if normalized != authoritative or lexical.is_symlink():
            raise SystemExit(
                "PROBE_INPUT_MUTATION_OUTPUT_POLICY_FAIL: authoritative override "
                "licenses only the canonical probe-input mutation certificate"
            )
        return normalized
    try:
        resolved.relative_to(PROJECT.resolve())
    except ValueError:
        return normalized
    raise SystemExit(
        "PROBE_INPUT_MUTATION_OUTPUT_POLICY_FAIL: routine output must be outside "
        "the project source tree"
    )


def atomic_write_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o644)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
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


def encoded_json(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def decoded_timeout_output(value):
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def reseal_profile(profile):
    sites = profile["sites"]
    profile["site_count"] = len(sites)
    profile["site_type_census"] = dict(sorted(collections.Counter(
        row["site_type"] for row in sites
    ).items()))
    profile["ordered_site_hash_root"] = sha([sha(row) for row in sites])
    half = profile["root_half_equivalence"]
    half["certificate_sha256"] = sha({
        key: value for key, value in half.items() if key != "certificate_sha256"
    })


def reseal_anchor(anchor):
    reseal_profile(anchor["source_candidate_profile"])
    reseal_profile(anchor["target_candidate_profile"])
    parent = anchor["parent_transport"]
    parent["transport_sha256"] = sha({
        key: value for key, value in parent.items() if key != "transport_sha256"
    })
    anchor["site_transport_sha256"] = sha(anchor["site_transport"])
    anchor["anchor_row_sha256"] = sha({
        key: value for key, value in anchor.items() if key != "anchor_row_sha256"
    })


def reseal(contract):
    for anchor in contract["anchors"]:
        reseal_anchor(anchor)
    hashes = [row["anchor_row_sha256"] for row in contract["anchors"]]
    contract["ordered_anchor_row_hashes"] = hashes
    contract["ordered_anchor_hash_root"] = sha(hashes)
    contract["payload_sha256"] = sha({
        key: value for key, value in contract.items() if key != "payload_sha256"
    })


def anchor_with_site(contract, site_type):
    return next(row for row in contract["anchors"] if any(
        site["site_type"] == site_type for site in row["source_candidate_profile"]["sites"]
    ))


def mutate_omit_anchor(contract):
    contract["anchors"].pop()


def mutate_old_172(contract):
    bad = {67161, 67167, 67401, 67407}
    contract["anchors"] = [
        row for row in contract["anchors"] if row.get("locator", {}).get("raw_id") not in bad
    ]


def mutate_duplicate_new_triangle(contract):
    index = next(i for i, row in enumerate(contract["anchors"])
                 if row.get("locator", {}).get("raw_id") == 67161)
    contract["anchors"][index] = copy.deepcopy(contract["anchors"][index + 1])


def mutate_reassign_67161(contract):
    row = next(row for row in contract["anchors"] if row.get("locator", {}).get("raw_id") == 67161)
    row["locator"]["raw_id"] = 67162


def mutate_collapse_k7_path_ids(contract):
    groups = collections.defaultdict(list)
    for row in contract["anchors"]:
        if row["origin"] == "theta2_physical_k7":
            groups[row["locator"]["upstream_anchor_id"]].append(row)
    pair = next(rows for rows in groups.values() if len(rows) == 2)
    pair[1]["anchor_id"] = pair[0]["anchor_id"]


def drop_site(contract, site_type):
    anchor = anchor_with_site(contract, site_type)
    profile = anchor["source_candidate_profile"]
    removed = next(site for site in profile["sites"] if site["site_type"] == site_type)
    profile["sites"].remove(removed)
    anchor["site_transport"] = [
        row for row in anchor["site_transport"] if row["source_site_id"] != removed["site_id"]
    ]


def mutate_drop_pendant(contract):
    drop_site(contract, "pendant_arm")


def mutate_drop_retic(contract):
    drop_site(contract, "reticulation_incoming")


def mutate_drop_root(contract):
    drop_site(contract, "root_suppressed_segment")


def mutate_split_root(contract):
    anchor = anchor_with_site(contract, "root_suppressed_segment")
    profile = anchor["source_candidate_profile"]
    site = copy.deepcopy(next(row for row in profile["sites"]
                              if row["site_type"] == "root_suppressed_segment"))
    site["mixed_endpoints"] = [site["mixed_endpoints"][0], "('artificial_split_half',)"]
    site["site_id"] = f"E:{sha(site['mixed_endpoints'])}"
    site["rooted_representatives"] = [site["rooted_representatives"][0]]
    site["site_type"] = "core_unheaded"
    profile["sites"].append(site)


def mutate_wrong_half(contract):
    anchor = contract["anchors"][0]
    anchor["source_candidate_profile"]["root_half_equivalence"][
        "semi_directed_relation_after_insertion"
    ] = "none"


def mutate_wrong_site_transport(contract):
    anchor = next(row for row in contract["anchors"] if len(row["site_transport"]) >= 2)
    anchor["site_transport"][0]["target_site_id"], anchor["site_transport"][1]["target_site_id"] = (
        anchor["site_transport"][1]["target_site_id"],
        anchor["site_transport"][0]["target_site_id"],
    )


def mutate_corrupt_parent_transport(contract):
    anchor = next(row for row in contract["anchors"]
                  if len(row["parent_transport"]["mixed_edge_map"]) >= 2)
    edge_map = anchor["parent_transport"]["mixed_edge_map"]
    edge_map[0][1], edge_map[1][1] = edge_map[1][1], edge_map[0][1]


def mutate_formula(contract):
    contract["candidate_census"]["per_graph_formula"] = "site_count = 2*k + 3*r - 4"


def mutate_topology_first(contract):
    order = contract["required_probe_classifier_order"]
    order.insert(0, "rooted_restriction_type_as_terminal_separator")


def mutate_triple_gate(contract):
    order = contract["required_probe_classifier_order"]
    order[2] = "triple_type_gate_then_selected_Ti_search"


def mutate_remove_forbidden(contract):
    contract["forbidden_probe_shortcuts"].remove("rooted_restriction_type_as_proof")


def mutate_raw4424_reintroduced(contract):
    contract["revoked_raw4424_tree_sunlet_terminal"] = True


def mutate_generic_rooted_reintroduced(contract):
    contract["rooted_restriction_classifier_enabled"] = True


def mutate_row_hash_omission(contract):
    contract["ordered_anchor_row_hashes"].pop()
    contract["ordered_anchor_hash_root"] = sha(contract["ordered_anchor_row_hashes"])


def mutate_input_binding(contract):
    contract["inputs"]["atlas_sha256"] = "0" * 64


MUTATIONS = [
    ("omitted_anchor_record", mutate_omit_anchor, "structure"),
    ("old_172_anchor_count_reintroduction", mutate_old_172, "structure"),
    ("duplicate_replacing_new_triangle_anchor", mutate_duplicate_new_triangle, "structure"),
    ("raw67161_locator_reassignment", mutate_reassign_67161, "structure"),
    ("collapse_two_k7_path_ids_sharing_topology_id", mutate_collapse_k7_path_ids, "structure"),
    ("omitted_pendant_arm", mutate_drop_pendant, "structure"),
    ("omitted_reticulation_incoming", mutate_drop_retic, "structure"),
    ("dropped_root_suppressed_segment", mutate_drop_root, "structure"),
    ("split_artificial_root_halves", mutate_split_root, "structure"),
    ("wrong_root_half_equivalence", mutate_wrong_half, "structure"),
    ("wrong_site_transport", mutate_wrong_site_transport, "structure"),
    ("corrupt_anchor_parent_transport", mutate_corrupt_parent_transport, "structure"),
    ("wrong_site_formula", mutate_formula, "structure"),
    ("topology_first_classifier_reintroduction", mutate_topology_first, "structure"),
    ("triple_type_gate_reintroduction", mutate_triple_gate, "structure"),
    ("forbidden_rooted_restriction_removed", mutate_remove_forbidden, "structure"),
    ("raw4424_false_tree_sunlet_reintroduction", mutate_raw4424_reintroduced, "structure"),
    ("generic_rooted_restriction_reintroduction", mutate_generic_rooted_reintroduced, "structure"),
    ("ordered_row_hash_omission", mutate_row_hash_omission, "structure-no-reseal"),
    ("upstream_input_binding_corruption", mutate_input_binding, "full"),
]


def run_verifier(path, kind, *, report=None, optimized=False, timeout=900.0):
    script = FULL if kind == "full" else STRUCTURE
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend([str(script), "--contract", str(path)])
    if kind == "full":
        require(report is not None, "full verifier report path required")
        report.unlink(missing_ok=True)
        command.extend(["--report", str(report)])
    else:
        command.append("--quiet")
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        return {
            "returncode": None,
            "diagnostic": (
                decoded_timeout_output(error.stdout)
                + decoded_timeout_output(error.stderr)
            ).strip(),
            "success_artifact_present": report is not None and report.exists(),
            "timeout": True,
            "signal": False,
        }
    return {
        "returncode": result.returncode,
        "diagnostic": (result.stdout + result.stderr).strip(),
        "success_artifact_present": report is not None and report.exists(),
        "timeout": False,
        "signal": result.returncode < 0,
    }


def qualify_mutation_failure(name, result):
    expected = MUTATION_DIAGNOSTICS[name]
    require(result.get("timeout") is False, f"mutation timeout:{name}")
    require(result.get("signal") is False, f"mutation signal:{name}")
    require(result.get("returncode") == 1, f"mutation exit:{name}:{result}")
    diagnostic = result.get("diagnostic")
    require(isinstance(diagnostic, str), f"mutation diagnostic type:{name}")
    require(
        not any(marker in diagnostic for marker in FORBIDDEN_FAILURE_MARKERS),
        f"mutation unrelated crash:{name}:{diagnostic[-1000:]}",
    )
    require(
        result.get("success_artifact_present") is False,
        f"mutation success artifact:{name}",
    )
    require(diagnostic == expected, f"mutation diagnostic:{name}:{diagnostic[-1000:]}")
    return {
        "mutation": name,
        "rejected": True,
        "returncode": 1,
        "expected_diagnostic": expected,
        "observed_diagnostic": expected,
        "success_artifact_absent": True,
        "timeout": False,
        "signal": False,
    }


def verify_payload(value):
    claimed = value.get("payload_sha256")
    unsigned = {key: item for key, item in value.items() if key != "payload_sha256"}
    require(claimed == sha(unsigned), "report payload")


def qualify_clean_baseline(root, timeout):
    structure = run_verifier(CONTRACT, "structure", timeout=timeout)
    require(
        structure
        == {
            "returncode": 0,
            "diagnostic": "",
            "success_artifact_present": False,
            "timeout": False,
            "signal": False,
        },
        f"structure baseline:{structure}",
    )
    report_path = root / "clean-full-replay.json"
    full = run_verifier(CONTRACT, "full", report=report_path, timeout=timeout)
    require(full.get("timeout") is False, "full baseline timeout")
    require(full.get("signal") is False, "full baseline signal")
    require(full.get("returncode") == 0, f"full baseline exit:{full}")
    require(
        not any(
            marker in str(full.get("diagnostic", ""))
            for marker in FORBIDDEN_FAILURE_MARKERS
        ),
        f"full baseline crash:{full}",
    )
    require(full.get("success_artifact_present") is True, "full baseline report absent")
    observed = json.loads(report_path.read_text())
    expected = json.loads(REPLAY.read_text())
    verify_payload(observed)
    verify_payload(expected)
    require(observed == expected, "full baseline report drift")
    require(
        observed.get("schema") == "k2p-probe-input-independent-replay-v1"
        and observed.get("status") == "PASS"
        and observed.get("anchors_reconstructed") == 176
        and observed.get("source_sites_reenumerated") == 2_206
        and observed.get("target_sites_reenumerated") == 2_206
        and observed.get("first_probe_source_target_pairs") == 29_964
        and observed.get("missing_anchors") == 0
        and observed.get("extra_anchors") == 0
        and observed.get("unresolved") == 0,
        "full baseline semantics",
    )
    return {
        "structure_returncode": 0,
        "structure_status": "PASS",
        "structure_success_artifact_absent": True,
        "full_returncode": 0,
        "full_status": "PASS",
        "full_report_schema": observed["schema"],
        "full_report_payload_sha256": observed["payload_sha256"],
        "full_success_artifact_present": True,
        "anchors": 176,
        "source_sites": 2_206,
        "target_sites": 2_206,
        "first_probe_pairs": 29_964,
        "timeout": False,
        "signal": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-authoritative-output", action="store_true")
    parser.add_argument("--timeout-seconds", type=float, default=900.0)
    args = parser.parse_args()
    output_path = validate_output_path(args.output, args.allow_authoritative_output)
    output_path.unlink(missing_ok=True)
    if not __debug__:
        raise SystemExit("PROBE_INPUT_MUTATIONS_OPTIMIZED_MODE_FORBIDDEN")
    require(args.timeout_seconds > 0, "positive timeout required")
    original = json.loads(CONTRACT.read_text())
    rows = []
    with tempfile.TemporaryDirectory(prefix="k2p_probe_mutations_") as temporary:
        temporary = Path(temporary)
        baseline = qualify_clean_baseline(temporary, args.timeout_seconds)
        for index, (name, function, kind) in enumerate(MUTATIONS):
            value = copy.deepcopy(original)
            function(value)
            if kind != "structure-no-reseal":
                reseal(value)
            else:
                value["payload_sha256"] = sha({
                    key: item for key, item in value.items() if key != "payload_sha256"
                })
            path = temporary / f"mutation_{index}.json"
            path.write_text(json.dumps(value, sort_keys=True))
            report_path = (
                temporary / f"mutation_{index}-success.json"
                if kind == "full"
                else None
            )
            rows.append(
                qualify_mutation_failure(
                    name,
                    run_verifier(
                        path,
                        "full" if kind == "full" else "structure",
                        report=report_path,
                        timeout=args.timeout_seconds,
                    ),
                )
            )
        rows.append(
            qualify_mutation_failure(
                "optimized_mode",
                run_verifier(
                    CONTRACT,
                    "structure",
                    optimized=True,
                    timeout=args.timeout_seconds,
                ),
            )
        )
    semantic_rejected = sum(row.get("rejected") is True for row in rows[:-1])
    optimized_rejected = rows[-1].get("rejected") is True
    passed = semantic_rejected == len(MUTATIONS) and optimized_rejected
    report = {
        "schema": "k2p-probe-input-mutation-certificate-v2",
        "status": "PASS" if passed else "FAIL",
        "clean_baseline": baseline,
        "diagnostic_contract": MUTATION_DIAGNOSTICS,
        "contract_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
        "contract_payload_sha256": original["payload_sha256"],
        "structure_verifier_sha256": sha_file(STRUCTURE),
        "full_verifier_sha256": sha_file(FULL),
        "mutation_runner_sha256": sha_file(Path(__file__).resolve()),
        "adversarial_mutations": len(MUTATIONS),
        "mutations_rejected": semantic_rejected,
        "mutation_survivors": len(MUTATIONS) - semantic_rejected,
        "case_count": len(rows),
        "optimized_mode_rejected": optimized_rejected,
        "execution_contract": {
            "clean_structure_and_full_baselines_required": True,
            "mutations_require_exit_code_one": True,
            "mutations_require_exact_diagnostics": True,
            "traceback_import_timeout_signal_rejected": True,
            "success_artifact_must_be_absent": True,
            "caller_owned_output_required": True,
        },
        "results": rows,
    }
    report["payload_sha256"] = sha(report)
    atomic_write_bytes(output_path, encoded_json(report))
    print(json.dumps({
        "status": report["status"], "rejected": semantic_rejected,
        "survivors": report["mutation_survivors"],
        "optimized_rejected": report["optimized_mode_rejected"],
        "payload_sha256": report["payload_sha256"],
    }, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
