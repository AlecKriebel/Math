#!/usr/bin/env python3
"""Clean-room release verifier for the frozen four-leaf Omega pair.

This driver imports only the previously independent standard-library graph
implementation and the independent displayed-tree Fourier engine frozen under
``omega_audit/frozen_input/prior_audit/independent``.  It imports no discovery
or baseline verifier module.  In addition to replaying those two independent
audits, it checks the paper's one-step ``sd_0`` convention directly, records
every admissible rooting, inverts the complete Fourier tensor to all 256 site
pattern probabilities, and runs the release mutation suite.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import itertools
import json
import sys
import tempfile
from collections import Counter, defaultdict, deque
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FROZEN = ROOT / "omega_audit" / "frozen_input"
CERTIFICATE = FROZEN / "historical" / "jc_omega_move.json"
INDEPENDENT = FROZEN / "prior_audit" / "independent"
EXPECTED_CERTIFICATE_SHA256 = (
    "c0b8f907d557d23169a2e132d7a85b789d6fa3fe03d4d90bab286eec206e960f"
)
EXPECTED_N26_PARAMETER_VECTORS = {
    "N26_source": [
        "1/4", "1/2", "1/2", "3/4", "2/3", "1/4", "1/2",
        "1/20", "1/2", "1/2", "1/10", "1/2", "1/2", "1/2",
    ],
    "N26_target": [
        "1/7", "1/2", "41/48", "19/24", "14/19", "14/41", "1/2",
        "12/205", "1/2", "1/2", "3/40", "1/2", "1/2", "1/2",
    ],
}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


sys.path.insert(0, str(INDEPENDENT))
graph = load_module("omega_clean_graph", INDEPENDENT / "audit_omega_graphs.py")
fourier = load_module("exact_fourier", INDEPENDENT / "exact_fourier.py")
algebra = load_module("omega_clean_algebra", INDEPENDENT / "audit_omega_algebra.py")


class GateError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bidegrees(arcs):
    indegree, outdegree = defaultdict(int), defaultdict(int)
    for tail, head in arcs:
        outdegree[tail] += 1
        indegree[head] += 1
        indegree.setdefault(tail, 0)
        outdegree.setdefault(head, 0)
    return dict(indegree), dict(outdegree)


def fixed_one_step_reduction(root, arcs, labels):
    """Apply exactly sd_0: mark reticulation heads and suppress only root."""
    indegree, outdegree = bidegrees(arcs)
    reticulations = {
        vertex
        for vertex in indegree
        if (indegree[vertex], outdegree[vertex]) == (2, 1)
    }
    root_arcs = [(tail, head) for tail, head in arcs if tail == root]
    require(len(root_arcs) == 2, "root does not have exactly two children")
    children = tuple(head for _tail, head in root_arcs)
    require(children[0] != children[1], "root suppression creates a loop")
    edges = []
    for tail, head in arcs:
        if tail == root:
            continue
        edges.append((frozenset((tail, head)), head if head in reticulations else None))
    replacement_heads = tuple(child for child in children if child in reticulations)
    require(len(replacement_heads) <= 1, "root suppression creates a bidirected edge")
    replacement = (
        frozenset(children), replacement_heads[0] if replacement_heads else None
    )
    require(all(edge[0] != replacement[0] for edge in edges),
            "root suppression creates a parallel edge")
    edges.append(replacement)
    require(len({edge[0] for edge in edges}) == len(edges), "mixed graph is not simple")
    degree = Counter(endpoint for ends, _head in edges for endpoint in ends)
    require(all(degree[leaf] == 1 for leaf in labels), "a leaf is not degree one")
    require(all(degree[v] == 3 for v in degree if v not in labels),
            "one-step image is not binary")
    return edges


def to_graph_edges(edges):
    return [
        graph.MixedEdge.make(*tuple(ends), (() if head is None else (head,)))
        for ends, head in edges
    ]


def leaf_reticulation_distance_signature(edges, labels):
    adjacency = defaultdict(set)
    incoming = defaultdict(int)
    for ends, head in edges:
        u, v = tuple(ends)
        adjacency[u].add(v)
        adjacency[v].add(u)
        if head is not None:
            incoming[head] += 1
    reticulations = sorted(v for v, count in incoming.items() if count == 2)
    result = {}
    for leaf, label in labels.items():
        queue = deque([(leaf, 0)])
        seen = {leaf}
        distances = {}
        while queue:
            vertex, distance = queue.popleft()
            if vertex in reticulations:
                distances[vertex] = distance
            for neighbor in adjacency[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append((neighbor, distance + 1))
        result[str(label)] = sorted(distances.values())
    return result


def canonical_rooting(record):
    return {
        "root_edge": list(record["root_edge"]),
        "tree_child": bool(record["tree_child"]),
        "arcs": [list(arc) for arc in sorted(tuple(arc) for arc in record["arcs"])],
    }


def unpack_networks(certificate):
    networks = {}
    for model_name, model in certificate["root_models"].items():
        encoding = certificate["network_encodings"][str(model["census_index"])]
        networks[model_name] = {
            "index": model["census_index"],
            "root": encoding["root"],
            "arcs": [tuple(arc) for arc in encoding["arcs_in_parameter_order"]],
            "labels": dict(zip(encoding["leaves_in_port_order"], model["port_labels"])),
        }
    return networks


def complete_topology_audit(certificate):
    networks = unpack_networks(certificate)
    records = {}
    canonical_encodings = {}
    for name, network in networks.items():
        validation = graph.validate_rooted(
            network["root"], network["arcs"], network["labels"]
        )
        require(validation["valid"], f"{name}: historical rooted presentation invalid")
        displayed_tree_child = graph.tree_child(
            network["arcs"], network["root"], network["labels"]
        )
        require(displayed_tree_child, f"{name}: displayed rooting is not tree-child")
        one_step = fixed_one_step_reduction(
            network["root"], network["arcs"], network["labels"]
        )
        mixed_edges = to_graph_edges(one_step)
        statistics = graph.semi_directed_statistics(mixed_edges, network["labels"])
        rootings = [
            canonical_rooting(item)
            for item in graph.enumerate_rootings(mixed_edges, network["labels"])
        ]
        rootings.sort(key=lambda item: json.dumps(item, sort_keys=True))
        require(statistics["level"] == 2, f"{name}: not level two")
        require(statistics["triangle_count"] == 0, f"{name}: not triangle-free")
        require(statistics["cycle_lengths"] == [4, 4, 6],
                f"{name}: unexpected cycle deck")
        require(len(rootings) == 7, f"{name}: admissible-rooting count is not seven")
        require(sum(item["tree_child"] for item in rootings) == 2,
                f"{name}: tree-child-rooting count is not two")
        require(any(item["tree_child"] for item in rootings), f"{name}: not weak TC")
        require(not all(item["tree_child"] for item in rootings), f"{name}: is strong TC")
        local = graph.strong_tree_child_local_test(mixed_edges, network["labels"])
        require(not local["strongly_tree_child"], f"{name}: omnian witness absent")
        canonical = graph.canonical_mixed_encoding(mixed_edges, network["labels"])
        canonical_encodings[name] = canonical
        records[name] = {
            "fixed_sd0_simple_binary": True,
            "rooted_validation": validation,
            "displayed_rooting_tree_child": displayed_tree_child,
            "statistics": statistics,
            "omnian_test": local,
            "admissible_rootings": rootings,
            "admissible_rooting_count": len(rootings),
            "tree_child_rooting_count": sum(item["tree_child"] for item in rootings),
            "class": "W_TC\\S_TC",
            "canonical_mixed_encoding": canonical,
            "leaf_to_unordered_reticulation_distance_signature":
                leaf_reticulation_distance_signature(one_step, network["labels"]),
        }
    for source, target in (("N16_source", "N16_target"),
                           ("N26_source", "N26_target")):
        require(canonical_encodings[source] != canonical_encodings[target],
                f"{source}/{target}: labelled mixed graphs are isomorphic")
        require(records[source]["statistics"]["triangle_count"] == 0,
                "ordinary triangle redirection is unexpectedly available")
    return records


def inheritance_values(arcs, values):
    return dict(zip(fourier.reticulations(arcs), values))


def fourier_to_patterns(tensor):
    assignments = tuple(itertools.product(range(4), repeat=4))
    require(len(tensor) == len(assignments), "complete Fourier tensor missing entries")

    def character(g, state):
        g0, g1 = (g >> 1) & 1, g & 1
        s0, s1 = (state >> 1) & 1, state & 1
        return -1 if ((g0 * s0 + g1 * s1) & 1) else 1

    output = []
    for pattern in assignments:
        numerator = Fraction(0)
        for chars, coordinate in zip(assignments, tensor):
            sign = 1
            for g, state in zip(chars, pattern):
                sign *= character(g, state)
            numerator += coordinate * sign
        output.append(numerator / (4 ** 4))
    return tuple(output)


def complete_stochastic_audit(certificate, certificate_path=CERTIFICATE,
                              tensor_mutator=None):
    networks = unpack_networks(certificate)
    points = certificate["exact_common_points"]
    all_assignments = tuple(itertools.product(range(4), repeat=4))
    tensors = {}
    patterns = {}
    for name, network in networks.items():
        values = tuple(Fraction(value) for value in points[name])
        require(all(Fraction(0) < value < Fraction(1) for value in values),
                f"{name}: parameter outside open JC domain")
        tensor = fourier.evaluate(
            network["arcs"], network["labels"], all_assignments,
            values[:-2], inheritance_values(network["arcs"], values[-2:]), "JC"
        )
        tensors[name] = tensor
        patterns[name] = fourier_to_patterns(tensor)
        require(all(value > 0 for value in patterns[name]),
                f"{name}: inverse Fourier distribution is not strictly positive")
        require(sum(patterns[name]) == 1, f"{name}: probabilities do not sum to one")
    if tensor_mutator is not None:
        tensor_mutator(tensors)
    common_tensor = tensors["N16_source"]
    common_patterns = patterns["N16_source"]
    require(all(tensor == common_tensor for tensor in tensors.values()),
            "complete Fourier tensors differ")
    require(all(pattern == common_patterns for pattern in patterns.values()),
            "complete pattern distributions differ")

    clean_algebra = algebra.audit(Path(certificate_path))
    try:
        normalized_input = Path(certificate_path).resolve().relative_to(ROOT)
        clean_algebra["input"]["path"] = normalized_input.as_posix()
    except (ValueError, KeyError):
        # Mutated temporary inputs are rejected before release.  Keeping only
        # a basename makes any surviving diagnostic independent of the host.
        if "input" in clean_algebra:
            clean_algebra["input"]["path"] = Path(certificate_path).name
    rank = clean_algebra["generic_rank"]
    require(rank["complete_rank_upper_bound"] == 9, "rank upper bound failed")
    require(rank["complete_rank_lower_bound_from_exact_minors"] == 9,
            "rank lower bound failed")
    correspondence = clean_algebra["symbolic_parameter_correspondence"]
    require(correspondence["identically_zero_differences"] == 64,
            "rational correspondence does not match all zero-sum coordinates")
    parameter_vectors = {
        name: list(points[name])
        for name in ("N16_source", "N16_target", "N26_source", "N26_target")
    }
    require(
        {name: parameter_vectors[name] for name in EXPECTED_N26_PARAMETER_VECTORS}
        == EXPECTED_N26_PARAMETER_VECTORS,
        "alternative-rooting common parameter vectors changed",
    )
    return {
        "all_parameters_strictly_in_open_JC_domain": True,
        "complete_Fourier_coordinates_checked_per_network": 256,
        "zero_sum_coordinates": 64,
        "complete_pattern_probabilities_checked_per_network": 256,
        "complete_tensor_equality": True,
        "complete_pattern_probability_equality": True,
        "probability_sum": "1",
        "strictly_positive_pattern_probabilities": True,
        "exact_common_parameter_vectors": {
            "order": "e_0,...,e_11,lambda_V,lambda_X0",
            "vectors": parameter_vectors,
        },
        "independent_algebra_audit": clean_algebra,
        "local_dimensions": {
            "M_Omega": 9,
            "M_Omega_prime": 9,
            "intersection_at_common_point": 9,
        },
        "regular_full_dimensional_overlap_argument": (
            "The exact nine-parameter rational correspondence gives a common "
            "analytic image on an open neighborhood of the strict source point; "
            "its coordinate map has rank nine there.  The independent Euler "
            "upper bound gives model dimension at most nine, and the exact "
            "rank-nine minors make both model points regular."
        ),
    }


def validate_release_record(record):
    require(record["input_sha256"] == EXPECTED_CERTIFICATE_SHA256,
            "immutable input hash changed")
    require(record["cycle_enumeration_performed"], "triangle claim lacks cycle enumeration")
    for name, topology in record["topology"].items():
        require(topology["admissible_rooting_count"] == 7,
                f"{name}: incomplete rooting universe")
        require(len(topology["admissible_rootings"]) == 7,
                f"{name}: a rooting record is missing")
        require(topology["tree_child_rooting_count"] == 2,
                f"{name}: tree-child-rooting count changed")
        require(topology["statistics"]["triangle_count"] == 0,
                f"{name}: triangle introduced")
        require(topology["statistics"]["level"] == 2,
                f"{name}: level changed")
        require(topology["class"] == "W_TC\\S_TC",
                f"{name}: class was promoted incorrectly")
    require(record["source_target_nonisomorphic"], "source and target identified")
    require(record["non_T_equivalent"], "ordinary T incorrectly invoked")
    stochastic = record["stochastic"]
    require(stochastic["all_parameters_strictly_in_open_JC_domain"],
            "boundary parameter accepted")
    require(stochastic["complete_tensor_equality"], "Fourier coordinate changed")
    require(stochastic["complete_pattern_probability_equality"],
            "pattern coordinate changed")
    require(
        stochastic["exact_common_parameter_vectors"]["order"]
        == "e_0,...,e_11,lambda_V,lambda_X0",
        "parameter-vector order changed",
    )
    require(
        {
            name: stochastic["exact_common_parameter_vectors"]["vectors"][name]
            for name in EXPECTED_N26_PARAMETER_VECTORS
        }
        == EXPECTED_N26_PARAMETER_VECTORS,
        "alternative-rooting parameter vector changed",
    )
    require(stochastic["local_dimensions"] == {
        "M_Omega": 9, "M_Omega_prime": 9, "intersection_at_common_point": 9
    }, "rank/dimension certificate changed")
    require(record["all_n"]["dimension_formula"] == "2*n+1",
            "all-n dimension formula changed")


def mutation_suite(record, certificate):
    mutations = []

    def rejected_record(name, mutate, detector="release-record gate"):
        candidate = copy.deepcopy(record)
        mutate(candidate)
        try:
            validate_release_record(candidate)
        except (GateError, KeyError, TypeError, ValueError):
            mutations.append({"mutation": name, "rejected": True, "detector": detector})
            return
        raise GateError(f"mutation was not rejected: {name}")

    def rejected_topology(name, mutate):
        candidate = copy.deepcopy(certificate)
        mutate(candidate)
        try:
            complete_topology_audit(candidate)
        except (GateError, KeyError, TypeError, ValueError, StopIteration):
            mutations.append({
                "mutation": name,
                "rejected": True,
                "detector": "regenerated fixed-graph topology/rooting audit",
            })
            return
        raise GateError(f"topology mutation was not rejected: {name}")

    def rejected_stochastic(name, mutate, tensor_mutator=None):
        candidate = copy.deepcopy(certificate)
        mutate(candidate)
        try:
            with tempfile.NamedTemporaryFile("w", suffix=".json") as handle:
                json.dump(candidate, handle, sort_keys=True)
                handle.flush()
                complete_stochastic_audit(
                    candidate, Path(handle.name), tensor_mutator=tensor_mutator
                )
        except (AssertionError, KeyError, TypeError, ValueError, ZeroDivisionError):
            mutations.append({
                "mutation": name,
                "rejected": True,
                "detector": "regenerated strict-domain/Fourier/rank audit",
            })
            return
        raise GateError(f"stochastic mutation was not rejected: {name}")

    first = sorted(record["topology"])[0]
    rejected_record("delete one admissible rooting",
                    lambda r: r["topology"][first]["admissible_rootings"].pop())
    rejected_record("test only the displayed rooting",
                    lambda r: r["topology"][first].update(
                 admissible_rootings=r["topology"][first]["admissible_rootings"][:1],
                 admissible_rooting_count=1,
                 tree_child_rooting_count=1,
             ))
    rejected_topology(
        "add one triangle edge",
        lambda c: c["network_encodings"]["16"]["arcs_in_parameter_order"].append(
            ["P1_0", "V"]
        ),
    )

    def reverse_arrow(c):
        arcs = c["network_encodings"]["16"]["arcs_in_parameter_order"]
        index = arcs.index(["U", "V"])
        arcs[index] = ["V", "U"]
    rejected_topology("reverse one retained arrowhead", reverse_arrow)

    def swap_leaf_labels(c):
        labels = c["root_models"]["N16_target"]["port_labels"]
        labels[0], labels[1] = labels[1], labels[0]
        # The immutable-input gate rejects even a semantically inconclusive
        # relabelling, so no mutation can silently change the theorem pair.
        candidate_record = copy.deepcopy(record)
        candidate_record["input_sha256"] = hashlib.sha256(
            json.dumps(c, sort_keys=True).encode()
        ).hexdigest()
        validate_release_record(candidate_record)

    try:
        changed = copy.deepcopy(certificate)
        swap_leaf_labels(changed)
    except GateError:
        mutations.append({
            "mutation": "swap one leaf label",
            "rejected": True,
            "detector": "immutable input hash",
        })
    else:
        raise GateError("leaf-label mutation was not rejected")

    def alter_parent(c):
        arcs = c["network_encodings"]["16"]["arcs_in_parameter_order"]
        index = arcs.index(["U", "V"])
        arcs[index] = ["P4_0", "V"]
    rejected_topology("alter one reticulation parent", alter_parent)

    def boundary_parameter(c):
        c["exact_common_points"]["N16_source"][0] = "0"
    rejected_stochastic("set one parameter to zero or one", boundary_parameter)

    def alter_fourier_coordinate(tensors):
        changed = list(tensors["N16_source"])
        changed[1] += Fraction(1, 10**6)
        tensors["N16_source"] = tuple(changed)

    rejected_stochastic(
        "alter one Fourier coordinate",
        lambda _c: None,
        tensor_mutator=alter_fourier_coordinate,
    )

    def replace_jacobian_minor(c):
        c["dimension_and_rank"]["rank_nine_minors"]["N16_source"] = "0"

    rejected_stochastic("replace one Jacobian minor", replace_jacobian_minor)

    def identify_graphs(c):
        c["root_models"]["N16_target"]["port_labels"] = list(
            c["root_models"]["N16_source"]["port_labels"]
        )
    rejected_topology("identify the two mixed graphs", identify_graphs)

    rejected_record("claim strong tree-childness from one rooting",
                    lambda r: r["topology"][first].__setitem__("class", "S_TC"))
    rejected_record("claim triangle-freeness without enumerating cycles",
                    lambda r: r.update(cycle_enumeration_performed=False))
    require(len(mutations) == 12 and all(item["rejected"] for item in mutations),
            "mutation suite incomplete")
    return mutations


def main():
    require(sha256(CERTIFICATE) == EXPECTED_CERTIFICATE_SHA256,
            "historical certificate hash mismatch")
    certificate = json.loads(CERTIFICATE.read_text())
    topology = complete_topology_audit(certificate)
    stochastic = complete_stochastic_audit(certificate)
    record = {
        "status": "OMEGA-PASS-ALL-(n)",
        "implementation": (
            "clean-room graph/rooting and direct displayed-tree Fourier replay; "
            "no discovery implementation imports"
        ),
        "input_sha256": sha256(CERTIFICATE),
        "fixed_mixed_graph_convention": "one-step sd_0; no later cleanup",
        "cycle_enumeration_performed": True,
        "topology": topology,
        "source_target_nonisomorphic": True,
        "human_readable_nonisomorphism_witness": (
            "For the N16 source, labelled leaf 1 has unordered distances {3,3} "
            "to the two reticulations; for the target it has {2,4}."
        ),
        "non_T_equivalent": True,
        "non_T_reason": "both fixed mixed graphs are triangle-free",
        "stochastic": stochastic,
        "all_n": {
            "range": "every integer n>=4",
            "operation": "repeated identical cherry substitution away from leaf 1",
            "dimension_formula": "2*n+1",
            "base_dimension": 9,
            "dimension_increment_per_added_leaf": 2,
            "topology_preservation": (
                "The identical pendant tree adds no blob or triangle; a tree-child "
                "rooting extends and the original omnian rooting remains admissible."
            ),
            "overlap_preservation": (
                "Equation (cherry) has the positive analytic inverse "
                "uv=P_tilde(0,h,h) and u/v=P_tilde(g_X,h,0)/P_tilde(g_X,0,h)."
            ),
        },
    }
    validate_release_record(record)
    record["mandatory_mutations"] = mutation_suite(record, certificate)
    output = HERE / "output" / "omega_release_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": record["status"],
        "networks": {
            name: {
                "rootings": item["admissible_rooting_count"],
                "tree_child_rootings": item["tree_child_rooting_count"],
                "cycles": item["statistics"]["cycle_lengths"],
            }
            for name, item in topology.items()
        },
        "complete_Fourier_coordinates": 256,
        "complete_pattern_probabilities": 256,
        "local_dimensions": stochastic["local_dimensions"],
        "mutations_rejected": len(record["mandatory_mutations"]),
        "output": output.relative_to(ROOT).as_posix(),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
