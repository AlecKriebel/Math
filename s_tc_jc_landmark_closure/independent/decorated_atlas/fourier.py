#!/usr/bin/env python3
"""Exact displayed-tree and JC Fourier compiler for primitive records."""

from __future__ import annotations

from hashlib import sha256
from itertools import permutations, product
from typing import Any, Iterable, Mapping, Sequence

from graphcanon import canonical_json, digest


COMPILER_VERSION = "clean-room-jc-fourier-v1"
MODULUS = 2_147_483_647


def _choice_tuples(reticulation_count: int) -> tuple[tuple[int, ...], ...]:
    return tuple(product((0, 1), repeat=reticulation_count))


def compile_switchings(record: Mapping[str, Any]) -> dict[str, Any]:
    edges = [tuple(item) for item in record["canonical_edges"]]
    directed = {
        int(edge_index): (int(tail), int(head))
        for edge_index, tail, head in record["directed_edges"]
    }
    if set(directed) != set(range(len(edges))):
        raise ValueError("directed presentation must orient every canonical edge")
    port_vertices = {int(label): int(vertex) for label, vertex in record["port_label_vertices"].items()}
    if set(port_vertices) != set(range(int(record["port_count"]))):
        raise ValueError("port labels must be exactly 0,...,p-1")
    root = port_vertices[0]
    parent_edges = [tuple(int(x) for x in pair) for pair in record["incoming_parent_edges"]]
    reticulations = [int(v) for v in record["reticulations"]]
    if len(parent_edges) != len(reticulations):
        raise ValueError("reticulation/parent-edge count mismatch")

    choices = _choice_tuples(len(reticulations))
    switchings: list[dict[str, Any]] = []
    for choice in choices:
        deleted: set[int] = set()
        selected_parent_edges: list[int] = []
        for bit, pair in zip(choice, parent_edges):
            if len(pair) != 2:
                raise ValueError("each reticulation needs exactly two parent edges")
            selected_parent_edges.append(pair[bit])
            deleted.add(pair[1 - bit])
        selected = [index for index in range(len(edges)) if index not in deleted]
        children: dict[int, list[tuple[int, int]]] = {}
        indegree: dict[int, int] = {i: 0 for i in range(int(record["canonical_graph"]["order_size"]))}
        for edge_index in selected:
            tail, head = directed[edge_index]
            children.setdefault(tail, []).append((edge_index, head))
            indegree[head] += 1
        if indegree[root] != 0 or any(
            indegree[vertex] != 1 for vertex in indegree if vertex != root
        ):
            raise ValueError(("displayed switching is not an arborescence", choice, indegree))

        seen: set[int] = set()
        postorder: list[int] = []

        def traverse(vertex: int) -> None:
            if vertex in seen:
                raise ValueError("displayed switching contains a directed cycle")
            seen.add(vertex)
            for _edge_index, child in children.get(vertex, ()):
                traverse(child)
            postorder.append(vertex)

        traverse(root)
        if len(seen) != len(indegree):
            raise ValueError("displayed switching is disconnected")
        label_at = {vertex: label for label, vertex in port_vertices.items()}
        descendant: dict[int, int] = {}
        edge_masks = [0] * len(edges)
        for vertex in postorder:
            mask = (1 << label_at[vertex]) if vertex in label_at else 0
            for edge_index, child in children.get(vertex, ()):
                mask |= descendant[child]
                edge_masks[edge_index] = descendant[child]
            descendant[vertex] = mask
        expected = (1 << int(record["port_count"])) - 1
        if descendant[root] != expected:
            raise ValueError("displayed tree does not span every port")
        switchings.append(
            {
                "choice": list(choice),
                "selected_parent_edges": selected_parent_edges,
                "deleted_edges": sorted(deleted),
                "edge_descendant_masks": edge_masks,
            }
        )
    return {
        "compiler": COMPILER_VERSION,
        "choices": [list(choice) for choice in choices],
        "switchings": switchings,
    }


def _cube_actions(reticulation_count: int) -> tuple[dict[str, Any], ...]:
    choices = _choice_tuples(reticulation_count)
    index = {choice: i for i, choice in enumerate(choices)}
    actions: list[dict[str, Any]] = []
    for order in permutations(range(reticulation_count)):
        for flips in product((0, 1), repeat=reticulation_count):
            old_to_new = []
            for old in choices:
                new = tuple(old[order[i]] ^ flips[i] for i in range(reticulation_count))
                old_to_new.append(index[new])
            actions.append(
                {
                    "reticulation_order": list(order),
                    "parent_flips": list(flips),
                    "old_to_new_choice": old_to_new,
                }
            )
    unique = {tuple(action["old_to_new_choice"]): action for action in actions}
    return tuple(unique[key] for key in sorted(unique))


def displayed_parameter_signature(record: Mapping[str, Any]) -> dict[str, Any]:
    compiled = compile_switchings(record)
    signatures = []
    edge_count = len(record["canonical_edges"])
    for edge_index in range(edge_count):
        signatures.append(
            tuple(
                switching["edge_descendant_masks"][edge_index]
                for switching in compiled["switchings"]
            )
        )
    best: tuple[tuple[int, ...], ...] | None = None
    best_action: dict[str, Any] | None = None
    best_edge_order: list[int] | None = None
    for action in _cube_actions(len(record["reticulations"])):
        transformed = []
        old_to_new = action["old_to_new_choice"]
        for edge_index, signature in enumerate(signatures):
            item = [0] * len(signature)
            for old_index, new_index in enumerate(old_to_new):
                item[new_index] = signature[old_index]
            transformed.append((tuple(item), edge_index))
        transformed.sort()
        candidate = tuple(item for item, _edge_index in transformed)
        if best is None or candidate < best:
            best = candidate
            best_action = action
            best_edge_order = [edge_index for _item, edge_index in transformed]
    assert best is not None and best_action is not None and best_edge_order is not None
    body = {
        "port_count": int(record["port_count"]),
        "reticulation_count": len(record["reticulations"]),
        "switching_count": len(compiled["switchings"]),
        "canonical_edge_mask_signatures": [list(item) for item in best],
    }
    return {
        "signature": body,
        "signature_hash": digest(body),
        "normalizing_action": best_action,
        "canonical_to_raw_edge_order": best_edge_order,
        "switchings": compiled,
    }


def _xor_on_mask(assignment: Sequence[int], mask: int) -> int:
    value = 0
    for index, character in enumerate(assignment):
        if mask >> index & 1:
            value ^= int(character)
    return value


def coordinate_polynomial(
    record: Mapping[str, Any], assignment: Sequence[int], compiled: Mapping[str, Any] | None = None
) -> tuple[tuple[tuple[int, ...], int], ...]:
    """Return a sparse exact integer polynomial.

    Variables are ordered as all canonical edge multipliers followed by one
    inheritance parameter per canonical reticulation.  Parent-edge index zero
    has weight lambda and parent-edge index one has weight 1-lambda.
    """

    assignment = tuple(int(value) for value in assignment)
    if len(assignment) != int(record["port_count"]):
        raise ValueError("wrong character-assignment length")
    if any(value not in (0, 1, 2, 3) for value in assignment):
        raise ValueError("characters must be encoded by 0,1,2,3")
    if _xor_on_mask(assignment, (1 << len(assignment)) - 1) != 0:
        return tuple()
    compiled = compiled or compile_switchings(record)
    edge_count = len(record["canonical_edges"])
    reticulation_count = len(record["reticulations"])
    polynomial: dict[tuple[int, ...], int] = {}
    for switching in compiled["switchings"]:
        edge_exponents = [
            int(_xor_on_mask(assignment, mask) != 0)
            for mask in switching["edge_descendant_masks"]
        ]
        inheritance_terms: dict[tuple[int, ...], int] = {(0,) * reticulation_count: 1}
        for index, bit in enumerate(switching["choice"]):
            updated: dict[tuple[int, ...], int] = {}
            for exponents, coefficient in inheritance_terms.items():
                if bit == 0:
                    item = list(exponents)
                    item[index] += 1
                    key = tuple(item)
                    updated[key] = updated.get(key, 0) + coefficient
                else:
                    updated[exponents] = updated.get(exponents, 0) + coefficient
                    item = list(exponents)
                    item[index] += 1
                    key = tuple(item)
                    updated[key] = updated.get(key, 0) - coefficient
            inheritance_terms = {key: value for key, value in updated.items() if value}
        for inheritance_exponents, coefficient in inheritance_terms.items():
            monomial = tuple(edge_exponents) + inheritance_exponents
            polynomial[monomial] = polynomial.get(monomial, 0) + coefficient
    return tuple(sorted((monomial, coefficient) for monomial, coefficient in polynomial.items() if coefficient))


def zero_sum_assignments(port_count: int) -> Iterable[tuple[int, ...]]:
    for prefix in product((0, 1, 2, 3), repeat=port_count - 1):
        total = 0
        for value in prefix:
            total ^= value
        yield tuple(prefix) + (total,)


def complete_tensor_hash(record: Mapping[str, Any]) -> str:
    compiled = compile_switchings(record)
    hasher = sha256()
    hasher.update(COMPILER_VERSION.encode())
    for assignment in zero_sum_assignments(int(record["port_count"])):
        polynomial = coordinate_polynomial(record, assignment, compiled)
        hasher.update(canonical_json([list(assignment), polynomial]).encode())
        hasher.update(b"\n")
    return hasher.hexdigest()


def tensor_probe_hash(record: Mapping[str, Any]) -> str:
    """Bounded regression hash; not a substitute for `complete_tensor_hash`."""

    p = int(record["port_count"])
    probes = [(0,) * p]
    for i in range(1, p):
        assignment = [0] * p
        assignment[0] = 1
        assignment[i] = 1
        probes.append(tuple(assignment))
    if p >= 4:
        assignment = [0] * p
        assignment[:4] = [1, 2, 3, 0]
        probes.append(tuple(assignment))
    compiled = compile_switchings(record)
    return digest(
        [
            [list(assignment), coordinate_polynomial(record, assignment, compiled)]
            for assignment in probes
        ]
    )


def parameter_permutation_witness(
    source: Mapping[str, Any], target: Mapping[str, Any]
) -> dict[str, Any] | None:
    left = displayed_parameter_signature(source)
    right = displayed_parameter_signature(target)
    if left["signature_hash"] != right["signature_hash"]:
        return None
    left_order = left["canonical_to_raw_edge_order"]
    right_order = right["canonical_to_raw_edge_order"]
    edge_map = {left_order[index]: right_order[index] for index in range(len(left_order))}

    # Compose each graph's old-choice -> canonical-choice action.  This is an
    # explicit switching-cube bijection; the reticulation permutation and
    # parent flips can be read from the two stored normalizers.
    left_action = left["normalizing_action"]["old_to_new_choice"]
    right_action = right["normalizing_action"]["old_to_new_choice"]
    inverse_right = {new: old for old, new in enumerate(right_action)}
    switching_map = {old: inverse_right[new] for old, new in enumerate(left_action)}
    return {
        "edge_parameter_map": {str(k): v for k, v in sorted(edge_map.items())},
        "switching_index_map": {str(k): v for k, v in sorted(switching_map.items())},
        "source_normalizer": left["normalizing_action"],
        "target_normalizer": right["normalizing_action"],
    }


def verify_parameter_permutation_witness(
    source: Mapping[str, Any], target: Mapping[str, Any], witness: Mapping[str, Any]
) -> bool:
    source_signature = displayed_parameter_signature(source)
    target_signature = displayed_parameter_signature(target)
    source_normalizer = source_signature["normalizing_action"]
    target_normalizer = target_signature["normalizing_action"]
    if witness.get("source_normalizer") != source_normalizer:
        return False
    if witness.get("target_normalizer") != target_normalizer:
        return False

    source_compiled = compile_switchings(source)
    target_compiled = compile_switchings(target)
    edge_map = {int(k): int(v) for k, v in witness["edge_parameter_map"].items()}
    switching_map = {int(k): int(v) for k, v in witness["switching_index_map"].items()}
    if set(edge_map) != set(range(len(source["canonical_edges"]))) or set(edge_map.values()) != set(
        range(len(target["canonical_edges"]))
    ):
        return False
    if set(switching_map) != set(range(len(source_compiled["switchings"]))) or set(
        switching_map.values()
    ) != set(range(len(target_compiled["switchings"]))):
        return False

    expected_edge_map = {
        source_signature["canonical_to_raw_edge_order"][index]:
        target_signature["canonical_to_raw_edge_order"][index]
        for index in range(len(source_signature["canonical_to_raw_edge_order"]))
    }
    if edge_map != expected_edge_map:
        return False
    inverse_target_action = {
        new: old
        for old, new in enumerate(target_normalizer["old_to_new_choice"])
    }
    expected_switching_map = {
        old: inverse_target_action[new]
        for old, new in enumerate(source_normalizer["old_to_new_choice"])
    }
    if switching_map != expected_switching_map:
        return False

    for source_edge, target_edge in edge_map.items():
        for source_switching, target_switching in switching_map.items():
            left_mask = source_compiled["switchings"][source_switching]["edge_descendant_masks"][source_edge]
            right_mask = target_compiled["switchings"][target_switching]["edge_descendant_masks"][target_edge]
            if left_mask != right_mask:
                return False
    return True
