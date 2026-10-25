#!/usr/bin/env python3
"""Content-wise differential check of independent and proof graph catalogs."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

import networkx as nx

from anchor_verifier import lowest_reticulations
from independent_graph_enumerator import (
    build_port_repair,
    canonical_code,
    enumerate_minimal_repairs,
    graph_from_payload,
)
from record_schema import (
    load_records,
    make_record,
    validate_record,
    write_json_record,
)


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reference_graph(row: dict) -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()
    for index, (tail, head) in enumerate(row["arcs"]):
        edge_id = f"e{index}"
        graph.add_edge(tail, head, key=edge_id, edge_id=edge_id)
    sources = [node for node in graph if graph.in_degree(node) == 0]
    if len(sources) != 1:
        raise ValueError(f"reference core has {len(sources)} sources")
    for node in graph:
        if node == sources[0]:
            role = "source"
        elif node in row["retics"]:
            role = "retic"
        else:
            role = "tree"
        graph.nodes[node]["role"] = role
    return graph


def selected_case_code(graph: nx.MultiDiGraph, reticulation: str) -> str:
    selected = graph.copy()
    parents = sorted(set(selected.predecessors(reticulation)), key=str)
    children = sorted(set(selected.successors(reticulation)), key=str)
    if len(parents) != 2 or len(children) != 1:
        raise ValueError("selected case requires two parents and one sampled child")
    selected.nodes[reticulation]["role"] = "retic|selected"
    for parent in parents:
        selected.nodes[parent]["role"] = (
            f"{selected.nodes[parent].get('role')}|selected_parent"
        )
    selected.nodes[children[0]]["role"] = "sink_leaf|selected_child"
    return canonical_code(selected)


def reference_cases(
    topology_reference: dict,
) -> tuple[dict[str, dict], list[str]]:
    failures = []
    cases: dict[str, dict] = {}
    for name, row in sorted(topology_reference["cores"].items()):
        graph = reference_graph(row)
        code = canonical_code(graph)
        listed = tuple(
            tuple(f"e{index}" for index in repair)
            for repair in row["repairs"]
        )
        independently_derived = enumerate_minimal_repairs(graph)
        if set(listed) != set(independently_derived):
            failures.append(
                f"{name}: proof repairs {listed!r} != predicate repairs {independently_derived!r}"
            )
        expansion_codes = []
        selected_codes = []
        lowest_by_repair = {}
        expansions_by_repair = {}
        for repair in listed:
            expansion = build_port_repair(graph, repair)
            expansions_by_repair[repair] = expansion
            expansion_codes.append(canonical_code(expansion))
            lowest = lowest_reticulations(expansion)
            lowest_by_repair[repair] = lowest
            for reticulation in lowest:
                selected_codes.append(selected_case_code(expansion, reticulation))
        cases[name] = {
            "core_code": code,
            "listed_repairs": listed,
            "predicate_repairs": independently_derived,
            "expansion_codes": expansion_codes,
            "selected_codes": selected_codes,
            "lowest_by_repair": lowest_by_repair,
            "expansions_by_repair": expansions_by_repair,
        }
    if len({case["core_code"] for case in cases.values()}) != len(cases):
        failures.append("proof catalog contains role-isomorphic duplicate core entries")
    return cases, failures


def _validate_reference_reattachment(
    reference: dict,
    reference_cases_by_name: dict[str, dict],
) -> list[str]:
    failures = []
    rows = reference.get("rows", [])
    if not rows:
        return ["proof reattachment reference has no rows"]
    seen = set()

    def side_base(graph: nx.MultiDiGraph, node: str) -> str:
        if str(node).startswith("port:"):
            predecessors = sorted(set(graph.predecessors(node)), key=str)
            if len(predecessors) != 1:
                raise ValueError("a repair port must have one primitive upstream tail")
            return predecessors[0]
        return node

    def structural_relation(
        graph: nx.MultiDiGraph,
        reticulation: str,
    ) -> str:
        parents = sorted(set(graph.predecessors(reticulation)), key=str)
        if len(parents) != 2:
            return "invalid"
        bases = [side_base(graph, parent) for parent in parents]
        if bases[0] == bases[1]:
            return "parallel-sides"
        residual = graph.copy()
        residual.remove_node(reticulation)
        if nx.has_path(residual, bases[0], bases[1]) or nx.has_path(
            residual, bases[1], bases[0]
        ):
            return "comparable"
        return "incomparable"

    for row in rows:
        name = row.get("core")
        repair = tuple(f"e{index}" for index in row.get("repair", []))
        key = (name, repair)
        if key in seen:
            failures.append(f"duplicate proof reattachment row {key!r}")
        seen.add(key)
        if name not in reference_cases_by_name:
            failures.append(f"unknown reattachment core {name!r}")
            continue
        case = reference_cases_by_name[name]
        if repair not in case["listed_repairs"]:
            failures.append(f"{name}: reattachment row uses unlisted repair {repair!r}")
            continue
        expected_lowest = set(case["lowest_by_repair"][repair])
        observed_lowest = set(row.get("lowest_roles", []))
        if observed_lowest != expected_lowest:
            failures.append(
                f"{name} {repair!r}: lowest roles {observed_lowest!r} != {expected_lowest!r}"
            )
        expansion = case["expansions_by_repair"][repair]
        relations = {
            structural_relation(expansion, reticulation)
            for reticulation in expected_lowest
        }
        declared_relation = str(row.get("parent_relation", "")).lower()
        if "incomparable" in declared_relation:
            declared_category = "incomparable"
        elif "distinct-cycle-sides" in declared_relation:
            declared_category = "parallel-sides"
        elif "ancestor" in declared_relation:
            declared_category = "comparable"
        else:
            declared_category = "unparsed"
        if relations != {declared_category}:
            failures.append(
                f"{name} {repair!r}: declared parent relation {declared_category!r} "
                f"!= graph-derived {sorted(relations)!r}"
            )
        for reticulation in expected_lowest:
            children = sorted(set(expansion.successors(reticulation)), key=str)
            if len(children) != 1 or expansion.nodes[children[0]].get("role") != "sink_leaf":
                failures.append(
                    f"{name} {repair!r} {reticulation}: no unique sampled child"
                )
        for field in ("child", "parent_relation", "residual", "reinsertion"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                failures.append(f"{name} {repair!r}: empty {field}")
        certificates = row.get("parent_certificates", [])
        if len(certificates) != 2 or not all(
            isinstance(value, str) and value.strip() for value in certificates
        ):
            failures.append(f"{name} {repair!r}: invalid parent certificates")
    expected_keys = {
        (name, repair)
        for name, case in reference_cases_by_name.items()
        for repair in case["listed_repairs"]
    }
    if seen != expected_keys:
        failures.append("proof reattachment rows do not cover exactly every catalog repair")
    return failures


def _primitive_from_exposure_payload(payload: dict) -> tuple[nx.MultiDiGraph, tuple[int, ...]]:
    """Recover the primitive core from an independently emitted ported graph."""
    graph = nx.MultiDiGraph()
    for row in payload.get("nodes", []):
        attributes = row.get("attributes", {})
        graph.add_node(row["id"], role=attributes.get("role"))
    for row in payload.get("edges", []):
        graph.add_edge(row["tail"], row["head"], key=row["key"])
    repair = tuple(sorted(
        int(node[1:])
        for node, data in graph.nodes(data=True)
        if data.get("role") == "sample"
        and node.startswith("L")
        and node[1:].isdigit()
    ))
    graph.remove_nodes_from([
        node for node, data in graph.nodes(data=True)
        if data.get("role") == "sample"
    ])
    for segment in repair:
        port = f"p{segment}"
        if port not in graph or graph.in_degree(port) != 1 or graph.out_degree(port) != 1:
            raise ValueError("exposure payload has a malformed repair port")
        tail = next(iter(graph.predecessors(port)))
        head = next(iter(graph.successors(port)))
        graph.remove_node(port)
        graph.add_edge(tail, head)
    return graph, repair


def compare_catalogs(
    topology_reference: dict,
    reattachment_reference: dict,
    core_records: list[dict],
    anchor_records: list[dict],
    reattachment_records: list[dict],
    exposure_records: list[dict],
) -> tuple[dict, list[str]]:
    reference, failures = reference_cases(topology_reference)
    if topology_reference.get("schema") != "nmsc-model-independent-trilogy-topology-lock-v1":
        failures.append("unexpected proof topology reference schema")
    if set(topology_reference.get("cores", {})) != {
        "cycle",
        "theta0",
        "theta1",
        "theta2",
        "theta3",
    }:
        failures.append("proof topology reference does not contain the named five-core catalog")
    if reattachment_reference.get("schema") != "nmsc-level2-decorated-reattachment-v2":
        failures.append("unexpected proof reattachment reference schema")
    failures.extend(
        _validate_reference_reattachment(
            reattachment_reference,
            reference,
        )
    )
    reference_name_by_code = {
        case["core_code"]: name for name, case in reference.items()
    }

    derived_by_name = {}
    for record in core_records:
        validate_record(record, "independent_graph_enumerator")
        core_code = canonical_code(graph_from_payload(record["graph"]))
        if core_code != record["exact_witness"]["core_code"]:
            failures.append("enumerator record core code does not match its graph payload")
        name = reference_name_by_code.get(core_code)
        if name is None:
            failures.append(f"independent core absent from proof catalog: {core_code}")
            continue
        if name in derived_by_name:
            failures.append(f"multiple independent records map to {name}")
        derived_by_name[name] = record
    if set(derived_by_name) != set(reference):
        failures.append(
            f"core name coverage differs: derived={sorted(derived_by_name)} "
            f"reference={sorted(reference)}"
        )

    raw_repair_counts = {}
    repair_orbit_counts = {}
    for name in sorted(set(derived_by_name).intersection(reference)):
        record = derived_by_name[name]
        derived_codes = [
            repair["expansion_code"]
            for repair in record["exact_witness"]["repairs"]
        ]
        expected_codes = reference[name]["expansion_codes"]
        if Counter(derived_codes) != Counter(expected_codes):
            failures.append(f"{name}: repaired expansion multiset differs content-wise")
        for repair in record["exact_witness"]["repairs"]:
            payload_code = canonical_code(graph_from_payload(repair["graph"]))
            if payload_code != repair["expansion_code"]:
                failures.append(f"{name}: repair payload has a false expansion code")
        raw_repair_counts[name] = len(derived_codes)
        repair_orbit_counts[name] = len(set(derived_codes))

    expected_raw = sum(len(case["listed_repairs"]) for case in reference.values())
    observed_raw = sum(raw_repair_counts.values())
    if len(reference) != 5 or len(derived_by_name) != 5:
        failures.append("expected exactly five core orbits")
    if expected_raw != 12 or observed_raw != 12:
        failures.append(
            f"expected exactly twelve raw repairs (reference={expected_raw}, derived={observed_raw})"
        )

    exposure_by_core: dict[str, list[tuple[int, ...]]] = defaultdict(list)
    swapped_physical_q_count = 0
    equal_parent_branch_count = 0
    q_half_count = 0
    for record in exposure_records:
        validate_record(record, "independent_exposure_loss")
        try:
            primitive, repair = _primitive_from_exposure_payload(record["graph"])
            core_code = canonical_code(primitive)
        except (KeyError, TypeError, ValueError, nx.NetworkXError) as error:
            failures.append(f"malformed independent exposure graph: {error}")
            continue
        if core_code != record["exact_witness"].get("core_code"):
            failures.append("exposure witness core code does not replay from its graph")
        name = reference_name_by_code.get(core_code)
        if name is None:
            failures.append("independent exposure core is absent from the proof catalog")
            continue
        exposure_by_core[name].append(repair)
        expected_repairs = {
            tuple(int(edge_id[1:]) for edge_id in listed)
            for listed in reference[name]["listed_repairs"]
        }
        if repair not in expected_repairs:
            failures.append(f"{name}: exposure repair {repair!r} is absent from proof catalog")
        witness = record["exact_witness"]
        if witness.get("failures"):
            failures.append(f"{name} {repair!r}: exposure verifier retained failures")
        if not witness.get("joint_reattachment_exact"):
            failures.append(f"{name} {repair!r}: joint V/X reattachment is not exact")
        if not witness.get("independent_expected_record_match"):
            failures.append(f"{name} {repair!r}: inverse differs from manifest-derived expectation")
        if not all(witness.get("field_consumption_mutants_killed", {}).values()):
            failures.append(f"{name} {repair!r}: an exposure record field is unused")
        formula_checks = witness.get("prony_formula_checks", {})
        if not all(
            value for key, value in formula_checks.items()
            if key != "determinant_formula"
        ):
            failures.append(f"{name} {repair!r}: independent Prony identity failed")
        equal_rows = witness.get("equal_parent_rate_checks", [])
        if len(equal_rows) != 2 or any(
            not row.get("exact") or not row.get("joint_reattachment_exact")
            for row in equal_rows
        ):
            failures.append(f"{name} {repair!r}: a full equal-first-rate lift failed")
        equal_child = witness.get("equal_child_epoch_check", {})
        if not (
            equal_child.get("exact")
            and equal_child.get("one_compressed_epoch")
            and equal_child.get("joint_reattachment_exact")
        ):
            failures.append(f"{name} {repair!r}: full equal-child-epoch lift failed")
        if witness.get("repair_subset_count_checked") != 32:
            failures.append(f"{name} {repair!r}: repair-subset search is not exhaustive")
        equal_parent_branch_count += len(equal_rows)
        q_half_count += sum(row.get("q") == "1/2" and row.get("exact") for row in equal_rows)
        swapped_physical_q_count += bool(witness.get("swapped_physical_q_fixture"))

    expected_exposure_coverage = {
        "theta0": {(2, 3), (3, 4)},
        "theta1": {(2, 3), (2, 4)},
    }
    observed_exposure_coverage = {
        name: set(repairs) for name, repairs in exposure_by_core.items()
    }
    if observed_exposure_coverage != expected_exposure_coverage:
        failures.append(
            "independent exposure repair coverage differs: "
            f"observed={observed_exposure_coverage!r} "
            f"expected={expected_exposure_coverage!r}"
        )
    if len(exposure_records) != 4 or equal_parent_branch_count != 8 or q_half_count != 4:
        failures.append("exposure branch coverage is not 4 unequal / 8 equal / 4 q-half")
    if swapped_physical_q_count != 1:
        failures.append("exposure suite must contain one swapped physical-q assignment")

    actual_selected: dict[str, dict[str, list[str]]] = defaultdict(
        lambda: {"anchor": [], "reattachment": []}
    )
    for record in anchor_records:
        validate_record(record, "anchor_verifier")
        witness = record["exact_witness"]
        name = reference_name_by_code.get(witness["core_code"])
        if name is None:
            failures.append("anchor record points to an unknown core")
            continue
        graph = graph_from_payload(record["graph"])
        actual_selected[name]["anchor"].append(
            selected_case_code(graph, witness["lowest_reticulation"])
        )
        anchors = witness.get("parent_anchors", [])
        if len(anchors) != 2 or any(
            anchor.get("incidence_witness_count", 0) < 2 for anchor in anchors
        ):
            failures.append(f"{name}: anchor record has empty/weak parent coverage")

    for record in reattachment_records:
        validate_record(record, "peeling_reattachment")
        witness = record["exact_witness"]
        name = reference_name_by_code.get(witness["core_code"])
        if name is None:
            failures.append("reattachment record points to an unknown core")
            continue
        graph = graph_from_payload(record["graph"])
        actual_selected[name]["reattachment"].append(
            selected_case_code(graph, witness["lowest_reticulation"])
        )
        if not witness.get("tagged_residual_code"):
            failures.append(f"{name}: empty tagged residual")
        if witness.get("reconstructed_expansion_code") != witness.get("expansion_code"):
            failures.append(f"{name}: reattachment reconstruction changed expansion orbit")
        if len(witness.get("signature_target_codes", [])) != 1:
            failures.append(f"{name}: tagged residual has nonunique target")

    role_record_counts = {}
    for name, case in reference.items():
        expected = Counter(case["selected_codes"])
        anchor = Counter(actual_selected[name]["anchor"])
        reattachment = Counter(actual_selected[name]["reattachment"])
        if anchor != expected:
            failures.append(f"{name}: anchor selected-case multiset differs content-wise")
        if reattachment != expected:
            failures.append(f"{name}: reattachment selected-case multiset differs content-wise")
        if anchor != reattachment:
            failures.append(f"{name}: anchor/reattachment coverage disagrees")
        role_record_counts[name] = len(case["selected_codes"])

    expected_role_records = sum(role_record_counts.values())
    if expected_role_records != 18:
        failures.append(
            f"expected eighteen lowest-role records, found {expected_role_records}"
        )

    witness = {
        "core_code_to_proof_name": dict(sorted(reference_name_by_code.items())),
        "core_orbit_count": len(derived_by_name),
        "raw_minimal_repair_count": observed_raw,
        "raw_repair_counts_by_core": raw_repair_counts,
        "repair_orbit_counts_by_core": repair_orbit_counts,
        "lowest_role_record_count": expected_role_records,
        "lowest_role_counts_by_core": role_record_counts,
        "independent_exposure_loss": {
            "record_count": len(exposure_records),
            "coverage_by_core": {
                name: [list(repair) for repair in sorted(repairs)]
                for name, repairs in sorted(observed_exposure_coverage.items())
            },
            "equal_parent_branch_count": equal_parent_branch_count,
            "q_half_count": q_half_count,
            "swapped_physical_q_count": swapped_physical_q_count,
        },
        "content_checks": {
            "core_graph_codes": not any("core" in failure for failure in failures),
            "repair_expansion_multisets": not any(
                "repair" in failure or "expansion" in failure for failure in failures
            ),
            "anchor_selected_case_multisets": not any(
                "anchor" in failure for failure in failures
            ),
            "reattachment_selected_case_multisets": not any(
                "reattachment" in failure or "residual" in failure
                for failure in failures
            ),
        },
        "failures": failures,
    }
    return witness, failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topology-reference", required=True)
    parser.add_argument("--reattachment-reference", required=True)
    parser.add_argument("--cores", required=True)
    parser.add_argument("--anchors", required=True)
    parser.add_argument("--reattach", required=True)
    parser.add_argument("--exposure", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    topology_path = Path(args.topology_reference)
    reattachment_reference_path = Path(args.reattachment_reference)
    cores_path = Path(args.cores)
    anchors_path = Path(args.anchors)
    reattach_path = Path(args.reattach)
    exposure_path = Path(args.exposure)
    witness, failures = compare_catalogs(
        json.loads(topology_path.read_text()),
        json.loads(reattachment_reference_path.read_text()),
        load_records(cores_path),
        load_records(anchors_path),
        load_records(reattach_path),
        load_records(exposure_path),
    )
    input_files = {
        "proof_topology_reference": file_hash(topology_path),
        "proof_reattachment_reference": file_hash(reattachment_reference_path),
        "independent_cores": file_hash(cores_path),
        "anchor_certificates": file_hash(anchors_path),
        "peeling_reattachment": file_hash(reattach_path),
        "independent_exposure_loss": file_hash(exposure_path),
    }
    record = make_record(
        job="differential_harness",
        case_input=input_files,
        status="BLOCKING" if failures else "PASS",
        system={"input_file_sha256": input_files},
        exact_witness=witness,
        declared_quotient_orbit={
            "proof_core_names": sorted(json.loads(topology_path.read_text())["cores"])
        },
        notes=(
            "Comparison uses exact role-preserving graph codes and multisets of "
            "repaired and selected-reticulation expansions, not count-only checks."
        ),
    )
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    write_json_record(output, record)
    if failures:
        print(f"DIFFERENTIAL_HARNESS_BLOCKING count={len(failures)}")
        raise SystemExit(1)
    print(
        "DIFFERENTIAL_HARNESS_OK "
        f"core_orbits={witness['core_orbit_count']} "
        f"raw_repairs={witness['raw_minimal_repair_count']} "
        f"role_records={witness['lowest_role_record_count']}"
    )


if __name__ == "__main__":
    main()
