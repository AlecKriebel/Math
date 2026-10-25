#!/usr/bin/env python3
"""Fast independent semantic verifier for the v3 finite-eight certificate."""

from __future__ import annotations

import argparse
from collections import Counter, deque
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
from typing import Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CERTIFICATE = ROOT / "certificates" / "finite_marginal_atlas_certificate.json"
DEFAULT_TOPOLOGY = ROOT / "data" / "NMSC_TOPOLOGY_IMPORT.json"
SCHEMA = "nmsc-finite-marginal-atlas-literal-cylinder-v3"
FORBIDDEN = (
    "route", "occupancy", "segment", "primitive", "source_order",
    "path_count", "route_count", "population_id",
)


class VerificationError(RuntimeError):
    pass


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: object) -> str:
    return sha256(canonical_json(value).encode()).hexdigest()


def powerset(values: Sequence[int]) -> Iterable[tuple[int, ...]]:
    for size in range(len(values) + 1):
        yield from combinations(values, size)


def domain_graph(
    core: Mapping[str, object], repair: Sequence[int]
) -> tuple[list[tuple[str, str]], dict[str, str]]:
    arcs = [tuple(arc) for arc in core["arcs"]]  # type: ignore[index]
    retics = set(core["retics"])  # type: ignore[index]
    edges: list[tuple[str, str]] = []
    roles = {
        node: ("retic" if node in retics else "tree")
        for arc in arcs for node in arc
    }
    for segment, (tail, head) in enumerate(arcs):
        if segment in repair:
            port, leaf = f"R{segment}", f"L{segment}"
            roles[port], roles[leaf] = "tree", "leaf"
            edges.extend(((tail, port), (port, head), (port, leaf)))
        else:
            edges.append((tail, head))
    for sink in core["sinks"]:  # type: ignore[index]
        leaf = f"C_{sink}"
        roles[leaf] = "leaf"
        edges.append((str(sink), leaf))
    return edges, roles


def valid_repair(core: Mapping[str, object], repair: Sequence[int]) -> bool:
    edges, roles = domain_graph(core, repair)
    nodes = {node for edge in edges for node in edge}
    for node in nodes:
        if roles[node] == "leaf":
            continue
        children = [head for tail, head in edges if tail == node]
        if not any(roles[child] in {"tree", "leaf"} for child in children):
            return False
        if roles[node] == "retic" and len(children) != 1:
            return False
    for retic in core["retics"]:  # type: ignore[index]
        for parent in {tail for tail, head in edges if head == retic}:
            ordinary = sum(head == parent for _, head in edges)
            ordinary += sum(
                roles[child] != "retic"
                for tail, child in edges if tail == parent
            )
            if parent == "S":
                ordinary += 1
            if ordinary < 2:
                return False
    return True


def derive_repairs(core: Mapping[str, object]) -> tuple[tuple[int, ...], ...]:
    result: list[tuple[int, ...]] = []
    segments = tuple(range(len(core["arcs"])))  # type: ignore[arg-type,index]
    for candidate in powerset(segments):
        if valid_repair(core, candidate) and not any(
            set(old).issubset(candidate) for old in result
        ):
            result.append(candidate)
    return tuple(result)


def full_graph(
    core: Mapping[str, object], repair: Sequence[int], transport: Mapping[str, str]
) -> list[tuple[str, str]]:
    edges = [("TOP", "ROOT"), ("ROOT", "S"), ("ROOT", "O")]
    for segment, (tail, head) in enumerate(core["arcs"]):  # type: ignore[index]
        if segment in repair:
            port = f"R{segment}"
            edges.extend(((str(tail), port), (port, str(head)), (port, f"L{segment}")))
        else:
            edges.append((str(tail), str(head)))
    for sink in core["sinks"]:  # type: ignore[index]
        edges.append((str(sink), f"C_{sink}"))
    return [(transport.get(tail, tail), transport.get(head, head)) for tail, head in edges]


def temporal_extensions(
    edges: Sequence[tuple[str, str]], samples: Sequence[str]
) -> tuple[dict[str, int], ...]:
    sample_set = set(samples)
    internal = sorted({node for edge in edges for node in edge} - sample_set)
    predecessors = {
        node: {tail for tail, head in edges if head == node and tail in internal}
        for node in internal
    }
    results: list[dict[str, int]] = []

    def extend(prefix: tuple[str, ...], remaining: frozenset[str]) -> None:
        if not remaining:
            total = len(prefix)
            ranks = {node: total - index for index, node in enumerate(prefix)}
            ranks.update({sample: 0 for sample in sample_set})
            results.append(ranks)
            return
        for node in sorted(
            candidate for candidate in remaining
            if predecessors[candidate].isdisjoint(remaining)
        ):
            extend(prefix + (node,), remaining - {node})

    extend((), frozenset(internal))
    return tuple(results)


def degrees(
    edges: Sequence[tuple[str, str]], node: str
) -> tuple[int, int]:
    return (
        sum(head == node for _, head in edges),
        sum(tail == node for tail, _ in edges),
    )


def descendants(
    edges: Sequence[tuple[str, str]], node: str, samples: Sequence[str]
) -> tuple[str, ...]:
    outgoing: dict[str, list[str]] = {}
    for tail, head in edges:
        outgoing.setdefault(tail, []).append(head)
    sample_set = set(samples)
    found: set[str] = set()
    seen = {node}
    stack = [node]
    while stack:
        current = stack.pop()
        if current in sample_set:
            found.add(current)
        for child in outgoing.get(current, ()):
            if child not in seen:
                seen.add(child)
                stack.append(child)
    return tuple(sorted(found))


def row_state(
    row: Mapping[str, object], topology: Mapping[str, object]
) -> tuple[list[tuple[str, str]], dict[str, int], tuple[str, ...]]:
    provenance = row["provenance"]  # type: ignore[index]
    core = topology["cores"][provenance["core"]]  # type: ignore[index]
    repair = tuple(int(v) for v in provenance["repair"])  # type: ignore[index]
    transport = {str(k): str(v) for k, v in provenance["transport"].items()}  # type: ignore[index]
    samples = tuple(sorted(transport.values()))
    edges = full_graph(core, repair, transport)
    extensions = temporal_extensions(edges, samples)
    extension_id = int(provenance["temporal_extension"])  # type: ignore[index]
    if extension_id >= len(extensions):
        raise VerificationError("base row has nonexistent temporal extension")
    return edges, extensions[extension_id], samples


def role_value(provenance: Mapping[str, object], role: str) -> str:
    return str(provenance["transport"][role])  # type: ignore[index]


def expected_role_generators(
    left: Mapping[str, object], right: Mapping[str, object]
) -> tuple[str, ...] | None:
    lp = left["provenance"]  # type: ignore[index]
    rp = right["provenance"]  # type: ignore[index]
    if lp["core"] != rp["core"] or lp["temporal_extension"] != rp["temporal_extension"]:  # type: ignore[index]
        return None
    core = str(lp["core"])  # type: ignore[index]
    lr = tuple(int(v) for v in lp["repair"])  # type: ignore[index]
    rr = tuple(int(v) for v in rp["repair"])  # type: ignore[index]

    def same(left_role: str, right_role: str | None = None) -> bool:
        return role_value(lp, left_role) == role_value(
            rp, left_role if right_role is None else right_role
        )

    def swap(la: str, lb: str, ra: str, rb: str) -> bool:
        return same(la, rb) and same(lb, ra)

    if core == "cycle":
        ll, rl = f"L{lr[0]}", f"L{rr[0]}"
        if lr == rr and swap("C_X", ll, "C_X", rl):
            return ("Q6",)
        if lr != rr and same("C_X") and same(ll, rl):
            return ("Q5",)
    if core == "theta0" and lr == rr == (3, 4):
        if same("L4") and swap("C_X", "L3", "C_X", "L3"):
            return ("Q5", "Q6")
    if core == "theta1":
        lo = next(segment for segment in lr if segment != 2)
        ro = next(segment for segment in rr if segment != 2)
        if lr == rr and same(f"L{lo}") and swap("C_X", "L2", "C_X", "L2"):
            return ("Q6",)
        if lr != rr and same("C_X") and same("L2") and same(f"L{lo}", f"L{ro}"):
            return ("Q5",)
    if core == "theta3":
        if lr == rr == (2,) and same("C_X1") and swap("C_X0", "L2", "C_X0", "L2"):
            return ("Q6",)
        if lr == rr == (4,) and same("C_X0") and swap("C_X1", "L4", "C_X1", "L4"):
            return ("Q6",)
        if lr == (2,) and rr == (4,) and same("C_X0", "C_X1") and same("C_X1", "C_X0") and same("L2", "L4"):
            return ("Q6", "Q5")
        if lr == (4,) and rr == (2,) and same("C_X0", "C_X1") and same("C_X1", "C_X0") and same("L4", "L2"):
            return ("Q5", "Q6")
    return None


def q(value: Sequence[int]) -> Fraction:
    if len(value) != 2 or value[1] == 0:
        raise VerificationError("invalid rational pair")
    return Fraction(int(value[0]), int(value[1]))


def walk_observables(
    value: object, inside: bool = False, path: str = ""
) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            now = inside or key.startswith("observable") or key in {
                "cylinder", "exclusive_cylinders", "observable_literal_witness"
            }
            if now and any(token in key.lower() for token in FORBIDDEN):
                raise VerificationError(
                    f"latent field in observable payload at {path}/{key}"
                )
            walk_observables(item, now, f"{path}/{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            walk_observables(item, inside, f"{path}/{index}")


def verify_cylinder(row: Mapping[str, object]) -> None:
    if row.get("no_unlisted_selected_merger") is not True:
        raise VerificationError("literal cylinder lacks exclusion condition")
    event = row.get("event")
    if event == "first_merger":
        pair = row.get("pair")
        if not isinstance(pair, list) or pair != sorted(pair):
            raise VerificationError("noncanonical first-merger pair")
        keys = ("open_chamber",)
    elif event == "first_then_second_merger":
        pair = row.get("first_pair")
        if not isinstance(pair, list) or pair != sorted(pair):
            raise VerificationError("noncanonical second-merger first pair")
        keys = ("first_open_chamber", "second_open_chamber")
    else:
        raise VerificationError(f"unknown literal cylinder {event!r}")
    for key in keys:
        chamber = row.get(key)
        if (
            not isinstance(chamber, list)
            or len(chamber) != 2
            or chamber[0] >= chamber[1]
        ):
            raise VerificationError("invalid open chamber")


def verify_generator_edge(
    edge: Mapping[str, object],
    rows: Mapping[str, Mapping[str, object]],
    topology: Mapping[str, object],
) -> None:
    left_id = str(edge["from_row_id"])
    right_id = str(edge["to_row_id"])
    if left_id not in rows or right_id not in rows or left_id == right_id:
        raise VerificationError("generator edge has invalid endpoint")
    left, right = rows[left_id], rows[right_id]
    generators = tuple(str(value) for value in edge["generators"])  # type: ignore[index]
    if not generators or not set(generators).issubset({"Q5", "Q6", "Q7", "Q8"}):
        raise VerificationError("unlisted generator in collision path")

    if "directed_label_preserving_node_map" not in edge:
        expected = expected_role_generators(left, right)
        if expected is None or generators != expected:
            raise VerificationError("unchecked Q5/Q6 role permutation")
        lp = left["provenance"]  # type: ignore[index]
        rp = right["provenance"]  # type: ignore[index]
        if edge.get("left_transport") != lp["transport"] or edge.get("right_transport") != rp["transport"]:  # type: ignore[index]
            raise VerificationError("role move transport audit mismatch")
        counts = edge.get("primitive_selected_block_count_by_role")
        if "Q6" in generators and (
            not isinstance(counts, dict)
            or len(counts) != 2
            or set(counts.values()) != {1}
        ):
            raise VerificationError("Q6 edge lacks primitive bi-unary audit")
        return

    left_edges, left_ranks, left_samples = row_state(left, topology)
    right_edges, right_ranks, right_samples = row_state(right, topology)
    if left_samples != right_samples:
        raise VerificationError("directed graph map changes sampled labels")
    mapping = {
        str(key): str(value)
        for key, value in edge["directed_label_preserving_node_map"].items()  # type: ignore[index]
    }
    left_nodes = {node for graph_edge in left_edges for node in graph_edge}
    right_nodes = {node for graph_edge in right_edges for node in graph_edge}
    if set(mapping) != left_nodes or set(mapping.values()) != right_nodes or len(set(mapping.values())) != len(mapping):
        raise VerificationError("directed node map is not a bijection")
    if any(mapping[label] != label for label in left_samples):
        raise VerificationError("directed node map changes a sampled-lineage label")
    if any(mapping[node] != node for node in ("TOP", "ROOT", "S")):
        raise VerificationError("directed node map changes a boundary role")
    if Counter((mapping[tail], mapping[head]) for tail, head in left_edges) != Counter(right_edges):
        raise VerificationError("directed node map does not preserve arc multiplicity")

    mismatches: list[dict[str, object]] = []
    for left_node, right_node in sorted(mapping.items()):
        if left_ranks[left_node] == right_ranks[right_node]:
            continue
        if degrees(left_edges, left_node)[0] != 2 or degrees(right_edges, right_node)[0] != 2:
            raise VerificationError("Q8 edge changes a nonreticulation rank")
        left_descendants = descendants(left_edges, left_node, left_samples)
        right_descendants = descendants(right_edges, right_node, right_samples)
        if len(left_descendants) != 1 or len(right_descendants) != 1:
            raise VerificationError("Q8 edge changes a pair-exposed reticulation clock")
        mismatches.append(
            {
                "left_node": left_node,
                "right_node": right_node,
                "left_rank": left_ranks[left_node],
                "right_rank": right_ranks[right_node],
                "left_selected_descendants": list(left_descendants),
                "right_selected_descendants": list(right_descendants),
            }
        )
    expected_generators = ("Q8", "Q7") if mismatches else ("Q7",)
    if generators != expected_generators or edge.get("q8_clock_changes") != mismatches:
        raise VerificationError("Q7/Q8 path annotation does not match the graph map")
    if edge.get("arc_multiset_preserved") is not True or edge.get("nonretic_ranks_preserved") is not True:
        raise VerificationError("Q7/Q8 path lacks preservation assertions")


def law_precode_orbit_key(precode: Mapping[str, object]) -> str:
    separator = precode["within_coordinate_triple_source_separator"]  # type: ignore[index]
    pattern = tuple(bool(value) for value in separator["zero_positive_pattern"])  # type: ignore[index]
    if len(pattern) != 3:
        raise VerificationError("triple source separator needs three truth values")
    reciprocal_pattern = (pattern[1], pattern[0], pattern[2])
    return digest(
        {
            "lower_shell_key": precode["lower_shell_key"],
            "unordered_source_pair": sorted(precode["oriented_source_pair"]),  # type: ignore[arg-type,index]
            "common_cut_component_measures": precode["common_cut_component_measures"],
            "normalized_continuation_columns": precode["normalized_continuation_columns"],
            "triple_source_pattern_mod_reciprocity": list(min(pattern, reciprocal_pattern)),
            "entire_piecewise_donor_word": precode["entire_piecewise_donor_word"],
            "gamma": precode["gamma"],
        }
    )


def verify_law_precode(precode: Mapping[str, object]) -> str:
    forbidden = ("graph", "route", "parent", "retic", "clock", "physical", "segment")

    def reject_latent(value: object, path: str = "precode") -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if any(token in str(key).lower() for token in forbidden):
                    raise VerificationError(f"latent field in law precode at {path}/{key}")
                reject_latent(child, f"{path}/{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                reject_latent(child, f"{path}/{index}")

    reject_latent(precode)
    if q(precode["gamma"]) != Fraction(1, 2):  # type: ignore[arg-type,index]
        raise VerificationError("balanced law precode lost gamma=1/2")
    atoms = precode["observable_first_contact_atoms"]  # type: ignore[index]
    if not isinstance(atoms, list) or len(atoms) != 2:
        raise VerificationError("first-contact precode must have two atoms")
    residuals: list[Fraction] = []
    for atom in atoms:
        residual = q(atom["observed_entry_mass"])
        for term in atom["predecessor_no_contact_terms"]:
            predecessor = int(term["predecessor_index"])
            if predecessor >= len(residuals):
                raise VerificationError("first-contact renewal uses a non-earlier atom")
            residual -= residuals[predecessor] * q(term["coefficient"])
        if residual <= 0:
            raise VerificationError("first-contact component measure is not positive")
        residuals.append(residual)
    stored_measures = [q(value) for value in precode["common_cut_component_measures"]]  # type: ignore[index]
    if residuals != stored_measures or residuals != [Fraction(1, 2), Fraction(1, 2)]:
        raise VerificationError("common-cut component measures were not renewed exactly")
    columns = [
        [q(value) for value in column]
        for column in precode["normalized_continuation_columns"]  # type: ignore[index]
    ]
    if (
        len(columns) != 2
        or any(sum(column) != 1 for column in columns)
        or all(
            columns[0][i] * columns[1][j] == columns[0][j] * columns[1][i]
            for i, j in combinations(range(len(columns[0])), 2)
        )
    ):
        raise VerificationError("common-cut continuation components are not scalar separated")
    separator = precode["within_coordinate_triple_source_separator"]  # type: ignore[index]
    if separator["sampled_lineage_labels"] != ["a", "b", "x"]:  # type: ignore[index]
        raise VerificationError("source separator is not an intrinsic three-label coordinate")
    cylinders = separator["literal_cylinders"]  # type: ignore[index]
    if len(cylinders) != 3:
        raise VerificationError("source separator must contain one zero/positive triple")
    for cylinder in cylinders:
        verify_cylinder(cylinder)
    pattern = separator["zero_positive_pattern"]  # type: ignore[index]
    if not isinstance(pattern, list) or len(pattern) != 3 or not all(isinstance(value, bool) for value in pattern):
        raise VerificationError("source separator pattern is not literal zero/positive data")
    word = precode["entire_piecewise_donor_word"]  # type: ignore[index]
    if not isinstance(word, list) or len(word) < 2:
        raise VerificationError("Q6 precode omitted the piecewise donor word")
    previous_end: Fraction | None = None
    for epoch in word:
        start, end = (q(value) for value in epoch["open_interval"])
        if start >= end or q(epoch["rate"]) <= 0 or (previous_end is not None and start != previous_end):
            raise VerificationError("piecewise donor word is not positive and contiguous")
        previous_end = end
    computed = law_precode_orbit_key(precode)
    if computed != precode["reciprocal_orbit_key"]:  # type: ignore[index]
        raise VerificationError("stored reciprocal precode key was not recomputed")
    return computed


def verify_law_q6_q8_interface(interface: Mapping[str, object]) -> None:
    if interface.get("schema") != "nmsc-law-only-q6-q8-interface-v1":
        raise VerificationError("wrong law-only Q6/Q8 interface schema")
    precodes = interface["first_contact_precodes"]
    if not isinstance(precodes, list) or len(precodes) != 2:
        raise VerificationError("hidden sister requires two oriented precodes")
    orbit_keys = [verify_law_precode(row) for row in precodes]
    if len(set(orbit_keys)) != 1:
        raise VerificationError("hidden sister precodes did not form one reciprocal orbit")
    first_pair = list(precodes[0]["oriented_source_pair"])
    second_pair = list(precodes[1]["oriented_source_pair"])
    first_pattern = list(
        precodes[0]["within_coordinate_triple_source_separator"]["zero_positive_pattern"]
    )
    second_pattern = list(
        precodes[1]["within_coordinate_triple_source_separator"]["zero_positive_pattern"]
    )
    if (
        second_pair != list(reversed(first_pair))
        or second_pattern != [first_pattern[1], first_pattern[0], first_pattern[2]]
    ):
        raise VerificationError("two hidden-sister precodes are not literal reciprocals")
    renewal = interface["common_cut_renewal"]
    entries = [q(value) for value in renewal["observed_entry_masses"]]  # type: ignore[index]
    coefficient = q(renewal["predecessor_no_contact_coefficient"])  # type: ignore[arg-type,index]
    recovered = [entries[0], entries[1] - entries[0] * coefficient]
    if (
        recovered != [Fraction(1, 2), Fraction(1, 2)]
        or [q(value) for value in renewal["recovered_component_measures"]] != recovered  # type: ignore[index]
        or q(renewal["component_measure_sum"]) != sum(recovered)  # type: ignore[arg-type,index]
    ):
        raise VerificationError("common-cut renewal record is inconsistent")
    orbit = interface["hidden_sister_reciprocal_orbit"]
    if (
        orbit["first_contact_precode_count"] != 2  # type: ignore[index]
        or orbit["reciprocal_orbit_count"] != len(set(orbit_keys))  # type: ignore[index]
        or orbit["reciprocal_orbit_count"] != 1  # type: ignore[index]
        or orbit["orbit_keys"] != sorted(set(orbit_keys))  # type: ignore[index]
        or orbit["counting_precodes_instead_of_orbits_rejected"] is not True  # type: ignore[index]
    ):
        raise VerificationError("precode count was substituted for reciprocal-orbit count")
    q8 = interface["q8_first_contact_projection"]
    common_projection = digest(
        {
            key: precodes[0][key]
            for key in (
                "lower_shell_key",
                "common_cut_component_measures",
                "normalized_continuation_columns",
            )
        }
    )
    if (
        q8["positive_hidden_presentations"] != 2  # type: ignore[index]
        or q8["distinct_law_first_contact_precodes"] != 1  # type: ignore[index]
        or q8["hidden_boundary_coordinate_in_precode"] is not False  # type: ignore[index]
        or q8["common_precode_digest"] != common_projection  # type: ignore[index]
    ):
        raise VerificationError("Q8 first-contact projection retained a hidden coordinate")
    false_focal = interface["anchored_false_focal_rejection"]
    false_key = verify_law_precode(false_focal["candidate_precode"])  # type: ignore[arg-type,index]
    if (
        false_focal["reference_orbit_key"] != orbit_keys[0]  # type: ignore[index]
        or false_focal["candidate_orbit_key"] != false_key  # type: ignore[index]
        or false_key == orbit_keys[0]
        or false_focal["zero_positive_triple_rejects"] is not True  # type: ignore[index]
    ):
        raise VerificationError("anchored false focal survived its zero/positive triple")
    different = interface["different_incidence_rejection"]
    different_key = verify_law_precode(different["candidate_precode"])  # type: ignore[arg-type,index]
    if (
        different["reference_orbit_key"] != orbit_keys[0]  # type: ignore[index]
        or different["candidate_orbit_key"] != different_key  # type: ignore[index]
        or different_key == orbit_keys[0]
        or different["nonsister_not_collapsed"] is not True  # type: ignore[index]
    ):
        raise VerificationError("different-incidence/nonsister precode was collapsed")
    exposure = interface["pair_exposure_balanced_case"]
    if (
        q(exposure["gamma"]) != Fraction(1, 2)  # type: ignore[arg-type,index]
        or q(exposure["rate"]) != 7  # type: ignore[arg-type,index]
        or q(exposure["one_child_lower_pair_density_at_zero"]) != 0  # type: ignore[arg-type,index]
        or q(exposure["two_child_lower_pair_density_at_zero"]) != q(exposure["rate"])  # type: ignore[arg-type,index]
        or exposure["pair_exposure_separates_at_gamma_half"] is not True  # type: ignore[index]
        or exposure["source_separator_sampled_lineage_count"] != 3  # type: ignore[index]
    ):
        raise VerificationError("pair exposure failed at balanced inheritance")
    germ = exposure["shared_upper_mixed_germ"]  # type: ignore[index]
    if (
        q(germ["constant_coefficient"]) != Fraction(1, 2)
        or q(germ["exponential_coefficient"]) != Fraction(1, 2)
        or q(germ["exponential_rate"]) != 7
    ):
        raise VerificationError("balanced upper mixed germ was altered")
    transfer = interface["whole_piecewise_donor_word_transfer"]
    if (
        transfer["forward_word"] != transfer["reciprocal_word"]  # type: ignore[index]
        or transfer["middle_epoch_mutant"] == transfer["forward_word"]  # type: ignore[index]
        or transfer["whole_word_equal_under_q6"] is not True  # type: ignore[index]
        or transfer["single_epoch_mutant_rejected"] is not True  # type: ignore[index]
    ):
        raise VerificationError("Q6 did not transfer the entire donor word")
    if interface["label_accounting"] != {  # type: ignore[index]
        "atlas_base": 5,
        "within_coordinate_source_separator": 3,
        "maximum_joint_coordinate": 8,
    }:
        raise VerificationError("law-only source separator changed the <=8 accounting")


def expansion_graph(
    core: Mapping[str, object], repair: Sequence[int]
) -> list[tuple[str, str, int | None, str]]:
    edges: list[tuple[str, str, int | None, str]] = [
        ("TOP", "ROOT", None, "top-boundary"),
        ("ROOT", "S", None, "incoming-boundary"),
        ("ROOT", "O", None, "outgroup"),
    ]
    for segment, (tail, head) in enumerate(core["arcs"]):  # type: ignore[index]
        tail, head = str(tail), str(head)
        if segment in repair:
            anchor = f"R{segment}"
            edges.extend(
                (
                    (tail, anchor, segment, "population"),
                    (anchor, head, segment, "population"),
                    (anchor, f"L{segment}", None, "repair-sample"),
                )
            )
        else:
            edges.append((tail, head, segment, "population"))
    for sink in core["sinks"]:  # type: ignore[index]
        edges.append((str(sink), f"C_{sink}", None, "sink-sample"))
    return edges


def expansion_paths(
    edges: Sequence[tuple[str, str, int | None, str]], source: str, target: str
) -> tuple[tuple[int, ...], ...]:
    outgoing: dict[str, list[int]] = {}
    for edge_id, (tail, _, _, _) in enumerate(edges):
        outgoing.setdefault(tail, []).append(edge_id)
    found: list[tuple[int, ...]] = []

    def visit(node: str, path: tuple[int, ...], seen: frozenset[str]) -> None:
        if node == target:
            found.append(path)
            return
        for edge_id in outgoing.get(node, ()):
            head = edges[edge_id][1]
            if head not in seen:
                visit(head, path + (edge_id,), seen | {head})

    visit(source, (), frozenset({source}))
    return tuple(found)


def expansion_ranks(
    edges: Sequence[tuple[str, str, int | None, str]], samples: Sequence[str]
) -> dict[str, int]:
    sample_set = set(samples)
    remaining = {
        node for edge in edges for node in edge[:2]
    } - sample_set
    order: list[str] = []
    while remaining:
        available = sorted(
            node
            for node in remaining
            if not any(head == node and tail in remaining for tail, head, _, _ in edges)
        )
        if not available:
            raise VerificationError("expansion base graph is cyclic")
        order.append(available[0])
        remaining.remove(available[0])
    total = len(order)
    ranks = {node: total - index for index, node in enumerate(order)}
    ranks.update({sample: 0 for sample in sample_set})
    return ranks


def expansion_base_labels(
    core: Mapping[str, object], repair: Sequence[int]
) -> tuple[str, ...]:
    return tuple(
        sorted(
            [
                "O",
                *(f"L{segment}" for segment in repair),
                *(f"C_{sink}" for sink in core["sinks"]),  # type: ignore[index]
            ]
        )
    )


def expansion_origin_language(
    edges: Sequence[tuple[str, str, int | None, str]], labels: Sequence[str]
) -> list[dict[str, object]]:
    paths = {label: expansion_paths(edges, "TOP", label) for label in labels}
    records: dict[str, dict[str, object]] = {}
    for left, right in combinations(sorted(labels), 2):
        for left_path in paths[left]:
            for right_path in paths[right]:
                for edge_id in set(left_path).intersection(right_path):
                    row = {
                        "event": "first_merger",
                        "pair": [left, right],
                        "origin_edge": edge_id,
                    }
                    records[canonical_json(row)] = row
    for triple in combinations(sorted(labels), 3):
        for first_pair in combinations(triple, 2):
            left, right = first_pair
            third = next(label for label in triple if label not in first_pair)
            for left_path in paths[left]:
                for right_path in paths[right]:
                    for first in set(left_path).intersection(right_path):
                        for continuation in (left_path, right_path):
                            first_position = continuation.index(first)
                            for third_path in paths[third]:
                                for second in continuation[: first_position + 1]:
                                    if second not in third_path:
                                        continue
                                    row = {
                                        "event": "first_then_second_merger",
                                        "first_pair": [left, right],
                                        "third": third,
                                        "first_origin_edge": first,
                                        "second_origin_edge": second,
                                    }
                                    records[canonical_json(row)] = row
    return [records[key] for key in sorted(records)]


def expansion_component_support(
    edges: Sequence[tuple[str, str, int | None, str]],
    routed: str,
    other: str,
    components: Sequence[int],
) -> tuple[set[int], set[int]]:
    routed_paths = expansion_paths(edges, "TOP", routed)
    other_paths = expansion_paths(edges, "TOP", other)
    supports = []
    for component in components:
        shared: set[int] = set()
        for routed_path in routed_paths:
            if component not in routed_path:
                continue
            for other_path in other_paths:
                shared.update(set(routed_path).intersection(other_path))
        supports.append(shared)
    if len(supports) != 2:
        raise VerificationError("expansion focal lacks two components")
    return supports[0], supports[1]


def expansion_reachable(core: Mapping[str, object], source: str, target: str) -> bool:
    outgoing: dict[str, set[str]] = {}
    for tail, head in core["arcs"]:  # type: ignore[index]
        outgoing.setdefault(str(tail), set()).add(str(head))
    seen = {source}
    queue = deque([source])
    while queue:
        node = queue.popleft()
        if node == target:
            return True
        for child in outgoing.get(node, set()) - seen:
            seen.add(child)
            queue.append(child)
    return False


def expansion_probe_graph(
    core: Mapping[str, object], repair: Sequence[int], segment_probe: int
) -> list[tuple[str, str, int | None, str]]:
    edges: list[tuple[str, str, int | None, str]] = [
        ("TOP", "ROOT", None, "top-boundary"),
        ("ROOT", "S", None, "incoming-boundary"),
        ("ROOT", "O", None, "outgroup"),
    ]
    for segment, (tail, head) in enumerate(core["arcs"]):  # type: ignore[index]
        chain = [str(tail)]
        if segment in repair:
            chain.append(f"R{segment}")
        if segment == segment_probe:
            chain.append("ZPORT")
        chain.append(str(head))
        edges.extend(
            (left, right, segment, "population")
            for left, right in zip(chain, chain[1:])
        )
        if segment in repair:
            edges.append((f"R{segment}", f"L{segment}", None, "repair-sample"))
        if segment == segment_probe:
            edges.append(("ZPORT", "Z", None, "probe-sample"))
    for sink in core["sinks"]:  # type: ignore[index]
        edges.append((str(sink), f"C_{sink}", None, "sink-sample"))
    return edges


def expansion_triage(
    core: Mapping[str, object], repair: Sequence[int], sink: str, segment: int
) -> tuple[str, tuple[str, ...], list[tuple[str, str, int | None, str]], tuple[int, ...]]:
    arcs = [tuple(map(str, arc)) for arc in core["arcs"]]  # type: ignore[index]
    tail = arcs[segment][0]
    pair_exposed = (
        tail in set(map(str, core["retics"]))  # type: ignore[index]
        and tail != sink
        and sum(arc[0] == tail for arc in arcs) == 1
        and expansion_reachable(core, tail, sink)
    )
    edges = expansion_probe_graph(core, repair, segment)
    routed = f"C_{sink}"
    components = tuple(
        edge_id
        for edge_id, (_, head, _, kind) in enumerate(edges)
        if head == sink and kind == "population"
    )
    roles: set[str] = set()
    for component in components:
        for routed_path in expansion_paths(edges, "TOP", routed):
            if component not in routed_path:
                continue
            for port_path in expansion_paths(edges, "TOP", "Z"):
                shared = [
                    edge_id
                    for edge_id in routed_path
                    if edge_id in port_path
                    and edges[edge_id][3]
                    in {"population", "incoming-boundary", "top-boundary"}
                ]
                if not shared:
                    raise VerificationError("centered port lacks a frontier")
                origin_segment = edges[shared[-1]][2]
                roles.add(
                    f"primitive-segment:{origin_segment}"
                    if origin_segment is not None
                    else "common-incoming-boundary"
                )
    if pair_exposed:
        classification = "intrinsic_pair_exposure"
    elif len(roles) == 2:
        classification = "two_frontier_no_pair_exposure"
    elif len(roles) == 1:
        classification = "one_pairwise_frontier"
    else:
        classification = "three_or_more_pairwise_frontiers"
    return classification, tuple(sorted(roles)), edges, components


def expansion_origin_language_mapped(
    edges: Sequence[tuple[str, str, int | None, str]],
    labels: Sequence[str],
    origins: Sequence[int | None],
) -> list[dict[str, object]]:
    paths = {label: expansion_paths(edges, "TOP", label) for label in labels}
    records: dict[str, dict[str, object]] = {}
    for left, right in combinations(sorted(labels), 2):
        for left_path in paths[left]:
            for right_path in paths[right]:
                for edge_id in set(left_path).intersection(right_path):
                    origin = origins[edge_id]
                    if origin is None:
                        continue
                    row = {"event": "first_merger", "pair": [left, right], "origin_edge": origin}
                    records[canonical_json(row)] = row
    for triple in combinations(sorted(labels), 3):
        for first_pair in combinations(triple, 2):
            left, right = first_pair
            third = next(label for label in triple if label not in first_pair)
            for left_path in paths[left]:
                for right_path in paths[right]:
                    for first in set(left_path).intersection(right_path):
                        first_origin = origins[first]
                        if first_origin is None:
                            continue
                        for continuation in (left_path, right_path):
                            first_position = continuation.index(first)
                            for third_path in paths[third]:
                                for second in continuation[: first_position + 1]:
                                    if second not in third_path or origins[second] is None:
                                        continue
                                    row = {
                                        "event": "first_then_second_merger",
                                        "first_pair": [left, right],
                                        "third": third,
                                        "first_origin_edge": first_origin,
                                        "second_origin_edge": origins[second],
                                    }
                                    records[canonical_json(row)] = row
    return [records[key] for key in sorted(records)]


def expansion_decorate(
    base: Sequence[tuple[str, str, int | None, str]],
    segment: int,
    side: str,
    word: Sequence[str],
) -> tuple[list[tuple[str, str, int | None, str]], list[int | None], tuple[str, ...]]:
    anchor = f"R{segment}"
    targets = [
        edge_id
        for edge_id, (tail, head, edge_segment, kind) in enumerate(base)
        if edge_segment == segment
        and kind == "population"
        and (
            (side == "above" and head == anchor)
            or (side == "below" and tail == anchor)
            or (side == "whole" and tail != anchor and head != anchor)
        )
    ]
    if len(targets) != 1:
        raise VerificationError("independent decoration target is not unique")
    target = targets[0]
    edges: list[tuple[str, str, int | None, str]] = []
    origins: list[int | None] = []
    ports: list[str] = []
    for old_id, edge in enumerate(base):
        if old_id != target:
            edges.append(edge)
            origins.append(old_id)
            continue
        tail, head, edge_segment, _ = edge
        nodes = [tail, *(f"W_{segment}_{side}_{i}_{s}" for i, s in enumerate(word)), head]
        for left, right in zip(nodes, nodes[1:]):
            edges.append((left, right, edge_segment, "population"))
            origins.append(old_id)
        for index, symbol in enumerate(word):
            if symbol == "P":
                label = f"E_{segment}_{side}_{index}"
                edges.append((nodes[index + 1], label, None, "decorated-port-sample"))
                origins.append(None)
                ports.append(label)
    return edges, origins, tuple(ports)


def expansion_support_mapped(
    edges: Sequence[tuple[str, str, int | None, str]],
    origins: Sequence[int | None],
    routed: str,
    other: str,
    components: Sequence[int],
) -> tuple[set[int], set[int]]:
    supports: list[set[int]] = []
    for component in components:
        shared: set[int] = set()
        for routed_path in expansion_paths(edges, "TOP", routed):
            if not any(origins[edge_id] == component for edge_id in routed_path):
                continue
            for other_path in expansion_paths(edges, "TOP", other):
                shared.update(set(routed_path).intersection(other_path))
        supports.append(shared)
    return supports[0], supports[1]


def expansion_separator_mapped(
    edges: Sequence[tuple[str, str, int | None, str]],
    origins: Sequence[int | None], routed: str, other: str,
    components: Sequence[int], required_origin: int | None = None,
) -> tuple[int, int] | None:
    left, right = expansion_support_mapped(edges, origins, routed, other, components)
    candidates = sorted(
        edge_id for edge_id in left.symmetric_difference(right)
        if required_origin is None or origins[edge_id] == required_origin
    )
    if not candidates:
        return None
    edge_id = candidates[0]
    return edge_id, 0 if edge_id in left else 1


def expansion_word_invariant(segment: int, side: str, word: Sequence[str], ports: Sequence[str]) -> dict[str, object]:
    port_index = 0
    tokens: list[dict[str, object]] = []
    demographic: list[dict[str, object]] = []
    port_positions: list[dict[str, object]] = []
    for position, symbol in enumerate(word):
        chamber_id = f"I_{segment}_{side}_{position}"
        if symbol == "D":
            token = {"kind": "demographic-boundary", "position": position, "chamber_id": chamber_id, "positive_rate_symbol": f"lambda_{segment}_{side}_{position}"}
            demographic.append(token)
        else:
            label = ports[port_index]
            port_index += 1
            token = {"kind": "sampled-port", "position": position, "chamber_id": chamber_id, "sample_label": label}
            port_positions.append({"position": position, "sample_label": label})
        tokens.append(token)
    return {
        "ordered_tokens": tokens,
        "sampling_restriction_demographic_word": demographic,
        "sampled_port_positions": port_positions,
        "ordinary_suppression_preserves_demographic_boundaries": True,
        "q3_distinct_rate_normal_form": [row["positive_rate_symbol"] for row in demographic],
    }


def expansion_contracted_paths(
    edges: Sequence[tuple[str, str, int | None, str]],
    labels: Sequence[str], origins: Sequence[int | None],
) -> dict[str, list[list[int]]]:
    result: dict[str, list[list[int]]] = {}
    for label in sorted(labels):
        paths: set[tuple[int, ...]] = set()
        for path in expansion_paths(edges, "TOP", label):
            contracted: list[int] = []
            for edge_id in path:
                origin = origins[edge_id]
                if origin is not None and (not contracted or contracted[-1] != origin):
                    contracted.append(origin)
            paths.add(tuple(contracted))
        result[label] = [list(path) for path in sorted(paths)]
    return result


def expansion_centered_context(
    base: Sequence[tuple[str, str, int | None, str]], segment: int,
    pointed_side: str, above_word: Sequence[str], below_word: Sequence[str],
) -> tuple[list[tuple[str, str, int | None, str]], list[int | None]]:
    anchor = f"R{segment}"
    targets = [
        edge_id for edge_id, (tail, head, edge_segment, kind) in enumerate(base)
        if edge_segment == segment and kind == "population"
        and (
            (pointed_side == "above" and head == anchor)
            or (pointed_side == "below" and tail == anchor)
            or (pointed_side == "whole" and tail != anchor and head != anchor)
        )
    ]
    if len(targets) != 1:
        raise VerificationError("independent centered context target differs")
    target = targets[0]
    edges: list[tuple[str, str, int | None, str]] = []
    origins: list[int | None] = []
    for old_id, edge in enumerate(base):
        if old_id != target:
            edges.append(edge)
            origins.append(old_id)
            continue
        tail, head, edge_segment, _ = edge
        nodes = [tail]
        nodes.extend(f"CTX_A_{i}_{s}" for i, s in enumerate(above_word))
        nodes.append("CTX_T")
        nodes.extend(f"CTX_B_{i}_{s}" for i, s in enumerate(below_word))
        nodes.append(head)
        for left, right in zip(nodes, nodes[1:]):
            edges.append((left, right, edge_segment, "population"))
            origins.append(old_id)
        edges.append(("CTX_T", "T", None, "pointed-false-focal-sample"))
        origins.append(None)
        for side, word in (("A", above_word), ("B", below_word)):
            for index, symbol in enumerate(word):
                if symbol == "P":
                    edges.append((f"CTX_{side}_{index}_{symbol}", f"CTX_{side}_{index}", None, "context-port-sample"))
                    origins.append(None)
    return edges, origins


def expected_expansion_base_cases(
    topology: Mapping[str, object],
    repairs: Mapping[str, Sequence[Sequence[int]]],
) -> tuple[
    list[dict[str, object]],
    dict[tuple[str, tuple[int, ...]], list[dict[str, object]]],
    dict[tuple[str, tuple[int, ...]], str],
]:
    rows: list[dict[str, object]] = []
    by_repair: dict[tuple[str, tuple[int, ...]], list[dict[str, object]]] = {}
    base_digests: dict[tuple[str, tuple[int, ...]], str] = {}
    for core_name in sorted(topology["cores"]):  # type: ignore[index]
        core = topology["cores"][core_name]  # type: ignore[index]
        for repair_value in repairs[core_name]:
            repair = tuple(repair_value)
            edges = expansion_graph(core, repair)
            labels = expansion_base_labels(core, repair)
            ranks = expansion_ranks(edges, labels)
            key = (str(core_name), repair)
            base_digests[key] = digest(expansion_origin_language(edges, labels))
            false_focals = sorted(
                head for _, head, _, kind in edges if kind == "repair-sample"
            )
            local: list[dict[str, object]] = []
            for sink in sorted(map(str, core["sinks"])):
                routed = f"C_{sink}"
                components = tuple(
                    edge_id
                    for edge_id, (_, head, _, kind) in enumerate(edges)
                    if head == sink and kind == "population"
                )
                for false_focal in false_focals:
                    triage, frontier_roles, _, _ = expansion_triage(
                        core, repair, sink, int(false_focal.removeprefix("L"))
                    )
                    case_id = digest(
                        {
                            "core": core_name,
                            "repair": repair,
                            "routed": routed,
                            "false_focal": false_focal,
                        }
                    )[:24]
                    found: tuple[str, int, int] | None = None
                    for other in sorted(
                        label
                        for label in labels
                        if label not in {"O", routed, false_focal}
                    ):
                        left, right = expansion_component_support(
                            edges, routed, other, components
                        )
                        difference = sorted(left.symmetric_difference(right))
                        if difference:
                            edge_id = difference[0]
                            found = (other, edge_id, 0 if edge_id in left else 1)
                            break
                    strict = (
                        found is None
                        and core_name == "cycle"
                        and len(core["sinks"]) == 1
                        and len(repair) == 1
                        and len([label for label in labels if label != "O"]) == 2
                        and len({tuple(arc) for arc in core["arcs"]}) == 1
                    )
                    if found is None and not strict:
                        raise VerificationError("independent base false focal is unseparated")
                    provenance = {
                        "core": core_name,
                        "repair": list(repair),
                        "routed_focal": routed,
                        "erased_false_focal": false_focal,
                    }
                    if found is None:
                        row = {
                            "case_id": case_id,
                            "provenance": provenance,
                            "remaining_selected_labels": [routed],
                            "pairwise_first_contact_triage": triage,
                            "contracted_first_contact_frontier_roles": list(frontier_roles),
                            "outcome": "reciprocal_strict_two_terminal_sister_cycle",
                            "source_erasure_separator": None,
                            "strict_exception_checks": {
                                "parallel_cycle_arms": True,
                                "two_local_terminals": True,
                                "no_pair_exposure_or_third_label": True,
                            },
                        }
                    else:
                        other, edge_id, positive = found
                        tail, head, _, _ = edges[edge_id]
                        row = {
                            "case_id": case_id,
                            "provenance": provenance,
                            "remaining_selected_labels": sorted((routed, other)),
                            "pairwise_first_contact_triage": triage,
                            "contracted_first_contact_frontier_roles": list(frontier_roles),
                            "outcome": "two_label_zero_positive_separator",
                            "source_erasure_separator": {
                                "observable_literal_cylinder": {
                                    "event": "first_merger",
                                    "pair": sorted((routed, other)),
                                    "open_chamber": [ranks[head], ranks[tail]],
                                    "no_unlisted_selected_merger": True,
                                },
                                "positive_component_index": positive,
                                "zero_component_index": 1 - positive,
                                "graph_origin_edge_id": edge_id,
                            },
                            "strict_exception_checks": None,
                        }
                    rows.append(row)
                    local.append(row)
            by_repair[key] = local
    return rows, by_repair, base_digests


def verify_expansion_retraction(
    section: Mapping[str, object],
    topology: Mapping[str, object],
    repairs: Mapping[str, Sequence[Sequence[int]]],
    counts: Mapping[str, object],
) -> None:
    if section.get("schema") != "nmsc-strong-expansion-retraction-falsification-v2":
        raise VerificationError("strong-expansion certificate schema changed")
    base_cases, by_repair, base_digests = expected_expansion_base_cases(
        topology, repairs
    )
    if section.get("base_false_focal_cases") != base_cases:
        raise VerificationError("strong-expansion base false-focal sweep differs")
    words = tuple(
        word for length in range(5) for word in product(("D", "P"), repeat=length)
    )
    centered_expected: list[dict[str, object]] = []
    centered_classification: dict[tuple[str, tuple[int, ...], str, int], str] = {}
    centered_triage: Counter[str] = Counter()
    for core_name in sorted(topology["cores"]):  # type: ignore[index]
        core = topology["cores"][core_name]  # type: ignore[index]
        for repair_value in repairs[core_name]:
            repair = tuple(repair_value)
            labels = expansion_base_labels(core, repair)
            for sink in sorted(map(str, core["sinks"])):
                routed = f"C_{sink}"
                for segment in range(len(core["arcs"])):
                    triage, frontiers, edges, components = expansion_triage(
                        core, repair, sink, segment
                    )
                    centered_classification[(core_name, repair, routed, segment)] = triage
                    centered_triage[triage] += 1
                    origins = list(range(len(edges)))
                    found: tuple[str, int, int] | None = None
                    for other in sorted(label for label in labels if label not in {"O", routed}):
                        result = expansion_separator_mapped(edges, origins, routed, other, components)
                        if result is not None:
                            found = (other, result[0], result[1])
                            break
                    if found is None:
                        raise VerificationError("independent centered port is unseparated")
                    other, edge_id, positive = found
                    ranks = expansion_ranks(edges, tuple(sorted((*labels, "Z"))))
                    tail, head, _, _ = edges[edge_id]
                    centered_expected.append(
                        {
                            "provenance": {
                                "core": core_name, "repair": list(repair),
                                "routed_focal": routed, "centered_port_segment": segment,
                            },
                            "classification": triage,
                            "contracted_first_contact_frontier_roles": list(frontiers),
                            "source_erasure_separator": {
                                "remaining_selected_labels": sorted((routed, other)),
                                "positive_component_index": positive,
                                "zero_component_index": 1 - positive,
                                "observable_literal_cylinder": {
                                    "event": "first_merger", "pair": sorted((routed, other)),
                                    "open_chamber": [ranks[head], ranks[tail]],
                                    "no_unlisted_selected_merger": True,
                                },
                            },
                            "triage_is_claimed_as_law_precode_eligibility": False,
                        }
                    )
    if section.get("centered_added_port_incidence_rows") != centered_expected:
        raise VerificationError("centered added-port incidence sweep differs")

    decoration_rows = section.get("decoration_rows")
    if not isinstance(decoration_rows, list) or len(decoration_rows) != 2480:
        raise VerificationError("strong-expansion one-site sweep is incomplete")
    row_index = 0
    total_checks = separated_total = reciprocal_total = 0
    base_check_total = added_check_total = 0
    decorated_triage: Counter[str] = Counter()
    for core_name in sorted(topology["cores"]):  # type: ignore[index]
        core = topology["cores"][core_name]  # type: ignore[index]
        for repair_value in repairs[core_name]:
            repair = tuple(repair_value)
            key = (core_name, repair)
            base_edges = expansion_graph(core, repair)
            base_origins = list(range(len(base_edges)))
            labels = expansion_base_labels(core, repair)
            base_language = expansion_origin_language_mapped(base_edges, labels, base_origins)
            local_cases = by_repair[key]
            sites = tuple(
                (segment, side)
                for segment in range(len(core["arcs"]))
                for side in (("above", "below") if segment in repair else ("whole",))
            )
            for segment, side in sites:
                for word in words:
                    edges, origins, ports = expansion_decorate(base_edges, segment, side, word)
                    full_labels = tuple(sorted((*labels, *ports)))
                    full_language = expansion_origin_language_mapped(edges, full_labels, origins)
                    direct = expansion_origin_language_mapped(edges, labels, origins)
                    keep = set(labels)
                    projected = []
                    for language_row in full_language:
                        involved = (
                            set(language_row["pair"])
                            if language_row["event"] == "first_merger"
                            else set(language_row["first_pair"]) | {language_row["third"]}
                        )
                        if involved.issubset(keep):
                            projected.append(language_row)
                    restriction_ok = direct == projected == base_language
                    ranks = expansion_ranks(edges, full_labels)
                    representative: dict[str, object] | None = None
                    check_rows: list[dict[str, object]] = []
                    separated_here = reciprocal_here = 0
                    for case in local_cases:
                        total_checks += 1
                        base_check_total += 1
                        provenance = case["provenance"]
                        routed = str(provenance["routed_focal"])
                        false_focal = str(provenance["erased_false_focal"])
                        triage = str(case["pairwise_first_contact_triage"])
                        decorated_triage[triage] += 1
                        sink = routed.removeprefix("C_")
                        components = tuple(
                            edge_id for edge_id, (_, head, _, kind) in enumerate(base_edges)
                            if head == sink and kind == "population"
                        )
                        source_separator = case["source_erasure_separator"]
                        result: tuple[int, int] | None = None
                        selected_other: str | None = None
                        if source_separator is not None:
                            selected_other = next(
                                label for label in case["remaining_selected_labels"] if label != routed
                            )
                            result = expansion_separator_mapped(
                                edges, origins, routed, selected_other, components,
                                int(source_separator["graph_origin_edge_id"]),
                            )
                            if result is None:
                                raise VerificationError("independent base separator vanished")
                        else:
                            for candidate in sorted(ports):
                                result = expansion_separator_mapped(
                                    edges, origins, routed, candidate, components
                                )
                                if result is not None:
                                    selected_other = candidate
                                    break
                            if (result is not None) != ("P" in word):
                                raise VerificationError("independent reciprocal exposure differs")
                        if result is None:
                            reciprocal_here += 1
                            reciprocal_total += 1
                            check_rows.append({
                                "routed_focal": routed,
                                "erased_false_focal": false_focal,
                                "false_focal_kind": "minimum-repair-anchor",
                                "pairwise_first_contact_triage": triage,
                                "outcome": "reciprocal_strict_two_terminal_sister_cycle",
                                "separator_other_label": None,
                                "separator_origin_edge": None,
                            })
                        else:
                            separated_here += 1
                            separated_total += 1
                            check_rows.append({
                                "routed_focal": routed,
                                "erased_false_focal": false_focal,
                                "false_focal_kind": "minimum-repair-anchor",
                                "pairwise_first_contact_triage": triage,
                                "outcome": "two_label_zero_positive_separator",
                                "separator_other_label": selected_other,
                                "separator_origin_edge": origins[result[0]],
                            })
                            if representative is None and selected_other is not None:
                                tail, head, _, _ = edges[result[0]]
                                representative = {
                                    "erased_false_focal": false_focal,
                                    "positive_component_index": result[1],
                                    "zero_component_index": 1 - result[1],
                                    "observable_literal_cylinder": {
                                        "event": "first_merger", "pair": sorted((routed, selected_other)),
                                        "open_chamber": [ranks[head], ranks[tail]],
                                        "no_unlisted_selected_merger": True,
                                    },
                                }
                    source_states: dict[str, tuple[int, ...]] = {}
                    for case in local_cases:
                        routed = str(case["provenance"]["routed_focal"])
                        sink = routed.removeprefix("C_")
                        source_states.setdefault(
                            routed,
                            tuple(edge_id for edge_id, (_, head, _, kind) in enumerate(base_edges) if head == sink and kind == "population"),
                        )
                    for routed, components in sorted(source_states.items()):
                        triage = centered_classification[(core_name, repair, routed, segment)]
                        for false_focal in ports:
                            total_checks += 1
                            added_check_total += 1
                            decorated_triage[triage] += 1
                            found = None
                            for other in sorted(label for label in (*labels, *ports) if label not in {"O", routed, false_focal}):
                                result = expansion_separator_mapped(edges, origins, routed, other, components)
                                if result is not None:
                                    found = (other, result[0], result[1])
                                    break
                            if found is None:
                                raise VerificationError("independent inserted port is unseparated")
                            other, edge_id, positive = found
                            separated_here += 1
                            separated_total += 1
                            check_rows.append({
                                "routed_focal": routed,
                                "erased_false_focal": false_focal,
                                "false_focal_kind": "inserted-port-sample",
                                "pairwise_first_contact_triage": triage,
                                "outcome": "two_label_zero_positive_separator",
                                "separator_other_label": other,
                                "separator_origin_edge": origins[edge_id],
                            })
                            if representative is None:
                                tail, head, _, _ = edges[edge_id]
                                representative = {
                                    "erased_false_focal": false_focal,
                                    "positive_component_index": positive,
                                    "zero_component_index": 1 - positive,
                                    "observable_literal_cylinder": {
                                        "event": "first_merger", "pair": sorted((routed, other)),
                                        "open_chamber": [ranks[head], ranks[tail]],
                                        "no_unlisted_selected_merger": True,
                                    },
                                }
                    expected_row = {
                        "provenance": {"core": core_name, "repair": list(repair), "primitive_segment": segment, "side": side, "word": list(word)},
                        "sampled_port_labels": list(ports),
                        "symbolic_word_invariant": expansion_word_invariant(segment, side, word, ports),
                        "restriction_commutes": restriction_ok,
                        "base_origin_language_digest": digest(base_language),
                        "restricted_origin_language_digest": digest(projected),
                        "full_origin_language_digest": digest(full_language),
                        "source_erasure_check_count": len(local_cases) + len(source_states) * len(ports),
                        "base_false_focal_check_count": len(local_cases),
                        "inserted_port_false_focal_check_count": len(source_states) * len(ports),
                        "separated_check_count": separated_here,
                        "strict_reciprocal_check_count": reciprocal_here,
                        "false_focal_check_digest": digest(check_rows),
                        "representative_separator": representative,
                    }
                    if decoration_rows[row_index] != expected_row:
                        raise VerificationError(f"strong-expansion decoration row {row_index} differs")
                    row_index += 1

    pointed_rows = section.get("pointed_two_sided_context_rows")
    if not isinstance(pointed_rows, list) or len(pointed_rows) != 126:
        raise VerificationError("pointed two-sided context sweep is incomplete")
    pointed_index = 0
    two_sided_contexts = 0
    for core_name in sorted(topology["cores"]):  # type: ignore[index]
        core = topology["cores"][core_name]  # type: ignore[index]
        for repair_value in repairs[core_name]:
            repair = tuple(repair_value)
            base_edges = expansion_graph(core, repair)
            base_origins = list(range(len(base_edges)))
            labels = expansion_base_labels(core, repair)
            base_paths = expansion_contracted_paths(base_edges, labels, base_origins)
            for sink in sorted(map(str, core["sinks"])):
                routed = f"C_{sink}"
                components = tuple(edge_id for edge_id, (_, head, _, kind) in enumerate(base_edges) if head == sink and kind == "population")
                sites = tuple(
                    (segment, side)
                    for segment in range(len(core["arcs"]))
                    for side in (("above", "below") if segment in repair else ("whole",))
                )
                for segment, pointed_side in sites:
                    hasher = sha256()
                    representative = None
                    local_count = local_restriction_failures = local_separator_failures = 0
                    for above_word in words:
                        for below_word in words:
                            local_count += 1
                            two_sided_contexts += 1
                            edges, origins = expansion_centered_context(base_edges, segment, pointed_side, above_word, below_word)
                            restriction_ok = expansion_contracted_paths(edges, labels, origins) == base_paths
                            if not restriction_ok:
                                local_restriction_failures += 1
                            found = None
                            for other in sorted(label for label in labels if label not in {"O", routed}):
                                result = expansion_separator_mapped(edges, origins, routed, other, components)
                                if result is not None:
                                    found = (other, result[0], result[1])
                                    break
                            if found is None:
                                local_separator_failures += 1
                            elif representative is None:
                                other, edge_id, positive = found
                                ranks = expansion_ranks(edges, tuple(sorted((*labels, "T"))))
                                tail, head, _, _ = edges[edge_id]
                                representative = {
                                    "above_word": list(above_word), "below_word": list(below_word),
                                    "remaining_selected_labels": sorted((routed, other)),
                                    "positive_component_index": positive, "zero_component_index": 1 - positive,
                                    "observable_literal_cylinder": {
                                        "event": "first_merger", "pair": sorted((routed, other)),
                                        "open_chamber": [ranks[head], ranks[tail]],
                                        "no_unlisted_selected_merger": True,
                                    },
                                }
                            hasher.update(canonical_json({
                                "above_word": above_word, "below_word": below_word,
                                "restriction_ok": restriction_ok,
                                "separator_other": None if found is None else found[0],
                                "separator_origin": None if found is None else origins[found[1]],
                            }).encode())
                    expected_row = {
                        "provenance": {"core": core_name, "repair": list(repair), "routed_focal": routed, "pointed_segment": segment, "pointed_side": pointed_side},
                        "pairwise_first_contact_triage": centered_classification[(core_name, repair, routed, segment)],
                        "above_word_count": 31, "below_word_count": 31,
                        "two_sided_context_count": local_count,
                        "restriction_failure_count": local_restriction_failures,
                        "source_erasure_separator_failure_count": local_separator_failures,
                        "context_digest": hasher.hexdigest(),
                        "representative_separator": representative,
                    }
                    if pointed_rows[pointed_index] != expected_row:
                        raise VerificationError(f"pointed two-sided row {pointed_index} differs")
                    pointed_index += 1

    base_triage = Counter(str(row["pairwise_first_contact_triage"]) for row in base_cases)
    summary = {
        "minimum_repair_row_count": 12,
        "minimum_row_candidate_false_focal_attempt_count": 30,
        "minimum_row_pairwise_two_frontier_attempt_count": base_triage["two_frontier_no_pair_exposure"],
        "centered_port_segment_sink_incidence_count": len(centered_expected),
        "centered_port_pairwise_two_frontier_incidence_count": centered_triage["two_frontier_no_pair_exposure"],
        "centered_port_intrinsic_pair_exposure_incidence_count": centered_triage["intrinsic_pair_exposure"],
        "centered_port_three_or_more_frontier_incidence_count": centered_triage["three_or_more_pairwise_frontiers"],
        "centered_port_one_frontier_incidence_count": centered_triage["one_pairwise_frontier"],
        "base_two_label_separator_count": 28,
        "base_strict_reciprocal_exception_count": 2,
        "maximum_separator_label_count_after_erasure": 2,
        "decoration_alphabet": ["D", "P"],
        "maximum_decoration_word_length": 4,
        "decoration_word_count_per_site": 31,
        "primitive_segment_interval_site_count": 80,
        "decoration_case_count": len(decoration_rows),
        "decorated_base_false_focal_check_count": base_check_total,
        "inserted_port_false_focal_check_count": added_check_total,
        "decorated_source_erasure_check_count": total_checks,
        "decorated_two_label_separator_count": separated_total,
        "decorated_strict_reciprocal_exception_count": reciprocal_total,
        "restriction_failure_count": 0,
        "decorated_pairwise_two_frontier_attempt_count": decorated_triage["two_frontier_no_pair_exposure"],
        "decorated_intrinsic_pair_exposure_attempt_count": decorated_triage["intrinsic_pair_exposure"],
        "decorated_three_or_more_frontier_attempt_count": decorated_triage["three_or_more_pairwise_frontiers"],
        "decorated_one_frontier_attempt_count": decorated_triage["one_pairwise_frontier"],
        "pointed_interval_sink_incidence_count": len(pointed_rows),
        "two_sided_context_count": two_sided_contexts,
        "two_sided_restriction_failure_count": 0,
        "two_sided_source_erasure_separator_failure_count": 0,
    }
    if section.get("summary") != summary:
        raise VerificationError("strong-expansion summary/count contract differs")
    if section.get("symbolic_q3_word_fixtures") != {
        "equal_adjacent_input": ["rho", "rho"],
        "equal_adjacent_normal_form": ["rho"],
        "unequal_adjacent_input": ["rho_0", "rho_1"],
        "unequal_adjacent_normal_form": ["rho_0", "rho_1"],
    }:
        raise VerificationError("symbolic Q3 word fixtures differ")
    triage_boundary = section.get("pairwise_triage_claim_boundary")
    if not isinstance(triage_boundary, str) or "not asserted equivalent" not in triage_boundary:
        raise VerificationError("pairwise triage was overclaimed")
    if section.get("exception_derivation") != {
        "seeded_from_declared_graph_q6_role_moves": False,
        "source_erasure_recomputed_for_every_theta_role": True,
        "theta_source_orbit_exception_count": 0,
        "cycle_source_orbit_exception_count": 2,
    }:
        raise VerificationError(
            "graph-Q6 moves were confused with source-coherent Q8 reciprocal exceptions"
        )
    if (
        counts.get("expansion_candidate_false_focal_attempt_count") != 30
        or counts.get("expansion_decoration_case_count") != 2480
        or counts.get("expansion_source_erasure_check_count") != 12932
    ):
        raise VerificationError("top-level strong-expansion counts differ")
    boundary = section.get("proof_boundary")
    if not isinstance(boundary, str) or "not a computational" not in boundary or "universal" not in boundary:
        raise VerificationError("strong-expansion finite proof boundary is missing")


def verify_certificate(
    certificate_path: Path, topology_path: Path
) -> dict[str, int]:
    certificate = json.loads(certificate_path.read_text())
    if certificate.get("schema") != SCHEMA or certificate.get("status") != "PASS":
        raise VerificationError("wrong schema or status")
    claimed = certificate.get("body_sha256")
    body = dict(certificate)
    body.pop("body_sha256", None)
    if claimed != digest(body):
        raise VerificationError("body digest mismatch")
    topology = json.loads(topology_path.read_text())
    source = certificate["input"]
    if (
        source["sha256"] != sha256(topology_path.read_bytes()).hexdigest()
        or source["stored_repairs_used_as_premise"] is not False
    ):
        raise VerificationError("input provenance/no-premise contract failed")
    repairs = {
        name: derive_repairs(core)
        for name, core in topology["cores"].items()
    }
    expected = [
        {
            "core": name,
            "derived_minimum_repairs": [list(row) for row in repairs[name]],
        }
        for name in sorted(repairs)
    ]
    if (
        certificate["repair_derivation"] != expected
        or sum(map(len, repairs.values())) != 12
    ):
        raise VerificationError("minimum repair derivation mismatch")
    walk_observables(certificate)

    counts = certificate["counts"]
    base = certificate["base_sweep"]
    if (
        counts["core_count"] != 5
        or counts["derived_minimum_repair_count"] != 12
        or len(base["rows"]) != counts["base_row_count"]
        or counts["base_row_count"] != 1996
        or counts["base_nonquotient_collision_count"] != 0
    ):
        raise VerificationError("complete-base sweep contract failed")
    row_by_id: dict[str, Mapping[str, object]] = {}
    for row in base["rows"]:
        observable = row["observable"]
        if (
            len(observable["language_digest"]) != 64
            or observable["literal_cylinder_count"] <= 0
        ):
            raise VerificationError("invalid complete merger-word row")
        if any(
            key in row
            for key in (
                "declared_semidirected_quotient_orbit_digest",
                "declared_q5_q6_q8_orbit_digest",
            )
        ):
            raise VerificationError("carrier digest was used as quotient evidence")
        row_id = str(row["row_id"])
        if row_id in row_by_id:
            raise VerificationError("duplicate base row id")
        row_by_id[row_id] = row
    collision_audit = base["explicit_declared_move_collision_audit"]
    if (
        len(collision_audit)
        != counts["base_explicit_move_audit_row_count"]
        or len(collision_audit) != 157
    ):
        raise VerificationError("explicit support-collision move audit is incomplete")
    allowed_families = {
        "parent-presentation and one bi-unary Q6 reversal",
        "repair-[3,4] core automorphism and bi-unary Q6 reversal",
        "parallel-parent presentation and C_X/L2 bi-unary Q6 reversal",
        "directed labelled core automorphism and Q8 reticulation-clock moves",
        "repair-2/4 core reversal, repaired-child Q6, and other-sink Q8 clock",
    }
    for audit in collision_audit:
        members = [str(value) for value in audit["member_row_ids"]]
        components = [
            [str(value) for value in component]
            for component in audit["checked_generator_components"]
        ]
        edges = audit["spanning_generator_edges"]
        if (
            audit["checked_generator_component_count"] != 1
            or len(components) != 1
            or sorted(components[0]) != sorted(members)
            or len(edges) != len(members) - 1
            or audit["declared_move_family"] not in allowed_families
            or audit["raw_time_preserving_orbit_count"] < 2
            or len(members) < 2
        ):
            raise VerificationError("support collision lacks one checked Q-generator tree")
        adjacency: dict[str, set[str]] = {member: set() for member in members}
        actual_names: set[str] = set()
        for edge in edges:
            left_id, right_id = str(edge["from_row_id"]), str(edge["to_row_id"])
            if left_id not in adjacency or right_id not in adjacency:
                raise VerificationError("generator edge leaves its support class")
            adjacency[left_id].add(right_id)
            adjacency[right_id].add(left_id)
            actual_names.update(str(value) for value in edge["generators"])
            verify_generator_edge(edge, row_by_id, topology)
        reached = {members[0]}
        queue: deque[str] = deque([members[0]])
        while queue:
            current = queue.popleft()
            for neighbor in adjacency[current] - reached:
                reached.add(neighbor)
                queue.append(neighbor)
        if reached != set(members) or sorted(actual_names) != audit["generator_names_used"]:
            raise VerificationError("stored generator forest is not a connected audit")
        if (
            audit["core"] == "theta2"
            and audit["directed_unranked_orbit_count"] != 1
        ):
            raise VerificationError("theta2 Q8 audit changed directed incidence")

    address = certificate["address_sweep"]
    if (
        len(address["rows"]) != 1580
        or counts["address_candidate_temporal_variant_count"] != 1580
        or counts["address_within_repair_distinct_cell_collision_count"] != 0
    ):
        raise VerificationError("address temporal/cell sweep failed")
    witnesses = address["literal_separation_witnesses"]
    if (
        len(witnesses)
        != counts["address_literal_separation_witness_count"]
        or not witnesses
    ):
        raise VerificationError("address witness manifest mismatch")
    for witness in witnesses:
        if bool(witness["left_positive"]) == bool(witness["right_positive"]):
            raise VerificationError("address witness does not separate")
        verify_cylinder(witness["cylinder"])

    words = certificate["word_rows"]
    if (
        len(words) != counts["word_order_case_count"]
        or counts["word_order_case_count"] != 6
        or sum(row["restriction_square_count"] for row in words)
        != counts["restriction_square_count"]
    ):
        raise VerificationError("word/restriction count mismatch")
    recovered_orders = set()
    for row in words:
        if row["selected_label_count"] != 8 or row["restriction_square_failures"]:
            raise VerificationError("word row exceeds eight or has failed square")
        observable = row["observable"]
        onsets = observable["singleton_onsets_from_cylinders"]
        recovered = tuple(sorted(onsets, key=lambda label: -onsets[label]))
        if (
            list(recovered) != observable["recovered_order"]
            or list(recovered) != row["declared_order_for_test_only"]
        ):
            raise VerificationError("word order was not recovered from onsets")
        recovered_orders.add(recovered)
    if len(recovered_orders) != 6:
        raise VerificationError("six strict orders were not exhausted")

    exposure = certificate["exposure_refinement"]
    labels = exposure["refinement_labels"]
    if (
        exposure["selected_label_count"] != 8
        or [(row["sample"], row["taxon"]) for row in labels[:2]]
        != [("x0", "x"), ("x1", "x")]
    ):
        raise VerificationError("B-union-D or duplicate-taxon contract failed")
    matrix = [
        [q(value) for value in row]
        for row in exposure["observable"]["fixed_cut_matrix"]
    ]
    determinant = (
        matrix[0][0] * matrix[1][1]
        - matrix[0][1] * matrix[1][0]
    )
    if (
        determinant != Fraction(1, 2048)
        or q(exposure["observable"]["determinant"]) != determinant
    ):
        raise VerificationError("fixed-cut determinant mismatch")
    for cylinder in exposure["observable"]["exclusive_cylinders"]:
        verify_cylinder(cylinder)

    incidence = certificate["observable_incidence_key_cases"]
    if len(incidence) != 4 or len({row["key_digest"] for row in incidence}) != 4:
        raise VerificationError("incidence keys are not injective")
    required = {
        "base_code_digest", "first_exclusive_cylinder",
        "second_exclusive_cylinder", "full_continuation_column_digest",
        "outlet_weight",
    }
    for row in incidence:
        key = row["observable_incidence_key"]
        if not required.issubset(key) or digest(key) != row["key_digest"]:
            raise VerificationError("incomplete/corrupt incidence key")
        verify_cylinder(key["first_exclusive_cylinder"])
        verify_cylinder(key["second_exclusive_cylinder"])

    verify_law_q6_q8_interface(certificate["law_only_q6_q8_interface"])
    if (
        counts["law_first_contact_precode_count"] != 2
        or counts["law_reciprocal_orbit_count"] != 1
    ):
        raise VerificationError("law-only precode/orbit count contract failed")

    verify_expansion_retraction(
        certificate["strong_expansion_retraction"], topology, repairs, counts
    )

    corridor = certificate["mixture_safe_corridor"]["observable"]
    physical = {
        name: tuple(q(value) for value in column)
        for name, column in corridor["physical_full_continuation_columns"].items()
    }
    mixing = tuple(
        tuple(q(value) for value in row)
        for row in corridor["invertible_mixing_matrix"]
    )
    raw = {
        name: tuple(
            sum(mixing[i][j] * column[j] for j in range(2))
            for i in range(2)
        )
        for name, column in physical.items()
    }
    stored_raw = {
        name: tuple(q(value) for value in column)
        for name, column in corridor["raw_mixed_columns"].items()
    }
    if raw != stored_raw:
        raise VerificationError("mixed columns were not recomputed")
    if (
        tuple(a * b for a, b in zip(physical["st"], physical["tu"]))
        != physical["su"]
        or tuple(a * b for a, b in zip(raw["st"], raw["tu"])) == raw["su"]
        or q(corridor["mixing_determinant"]) == 0
    ):
        raise VerificationError("mixture-safe corridor contract failed")
    for cylinder in corridor["literal_continuation_cylinders"]:
        verify_cylinder(cylinder)

    port_rows = certificate["finite_law_port_descent_rows"]
    if (
        len(port_rows) != counts["finite_port_row_count"]
        or counts["finite_port_row_count"] != 36
        or max(len(row["selected_labels"]) for row in port_rows) > 3
    ):
        raise VerificationError("finite law-port descent contract failed")
    for row in port_rows:
        verify_cylinder(row["observable_literal_witness"])

    if certificate["label_bound"] != {
        "finite_port_witness": 3,
        "atlas_base": 5,
        "base_plus_exposure_refinement": 8,
        "base_plus_single_probe": 6,
        "base_plus_pair_probe": 7,
        "base_plus_pair_and_routing_witness": 8,
        "maximum_selected_labels": 8,
    }:
        raise VerificationError("<=8 accounting changed")
    return {
        "base_rows": len(base["rows"]),
        "address_rows": len(address["rows"]),
        "witnesses": len(witnesses),
        "squares": counts["restriction_square_count"],
        "expansion_checks": counts["expansion_source_erasure_check_count"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--topology", type=Path, default=DEFAULT_TOPOLOGY)
    args = parser.parse_args()
    try:
        summary = verify_certificate(args.certificate, args.topology)
    except (
        VerificationError, KeyError, TypeError, ValueError, json.JSONDecodeError
    ) as error:
        raise SystemExit(
            f"FINITE_MARGINAL_ATLAS_LITERAL_CYLINDER_V3_REJECTED: {error}"
        )
    print(
        "FINITE_MARGINAL_ATLAS_LITERAL_CYLINDER_V3_VERIFIED "
        f"base_rows={summary['base_rows']} "
        f"address_rows={summary['address_rows']} "
        f"literal_witnesses={summary['witnesses']} "
        f"restriction_squares={summary['squares']}"
        f" expansion_checks={summary['expansion_checks']}"
    )


if __name__ == "__main__":
    main()
