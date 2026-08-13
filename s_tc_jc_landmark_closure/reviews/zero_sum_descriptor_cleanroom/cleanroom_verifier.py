#!/usr/bin/env python3
"""Independent verifier for zero-sum descriptor normalization.

This script intentionally imports no project modules.  It reads primary source
files only as text and reconstructs the graph, descriptor, and JC polynomial
logic with the Python standard library.
"""

from __future__ import annotations

import argparse
import ast
from collections import defaultdict, deque
from fractions import Fraction
import gzip
import hashlib
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys


REVIEW_DIR = Path(__file__).resolve().parent
REPO = REVIEW_DIR.parent.parent
PRIMARY = REPO / "primary"
QUARANTINE = REPO / "quarantine" / "descriptor_cache_scope_failure"
SCHEMA3_N3 = QUARANTINE / "schema3_n3"
TEMPLATE_FILE = (
    REPO.parent
    / "strong_level2_phylo_identifiability"
    / "src"
    / "jc_root_spanning_atlas_data.py"
)
SEVENTH_FILE = PRIMARY / "seventh_invariant.json"

GRAPH_A = "513afdd7dd8826c2bba2eaff47af1d37bacf98fd3a2906de825bf5705a70f2a2"
GRAPH_B = "83fbeab153b433dea88528707b25a74898a924b90b1eff000c5a7c10257c8dd8"
MIXED_SHA = "a58f001a0a653d0d7e5391ca9dbd22a9ee9d6a3baabfcd5e3fa6e5c2ad5e0926"
OLD_STORED_POLY_HASH = "e53478b6c8595bbdf39dcafea73bf788327aaca0ebf6702eef7d3677c77e9b44"
REGENERATED_POLY_HASH = "07014184f631b5e7bc9dca1a8c93a0ae25ac0a0a7e9aa89295a43bb89bc09e29"
EXPECTED_TEMPLATE_SHA = "dd4b47f018d8f261fe296430513cedc1691b39cdb57fa075e42d884ecfba9ee3"
EXPECTED_SEVENTH_SHA = "f737f9bee9cc04045355416b95629c18cb5aa9bc31d9719e319eb0a3907babed"


class VerificationError(AssertionError):
    """Raised when a clean-room check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def stable_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def exact_poly_hash(poly: dict[tuple[int, ...], int]) -> str:
    return hashlib.sha256(repr(tuple(sorted(poly.items()))).encode()).hexdigest()


def line_of(text: str, needle: str) -> int:
    for index, line in enumerate(text.splitlines(), 1):
        if needle in line:
            return index
    raise VerificationError(f"missing source marker: {needle}")


def parse_literal(path: Path, name: str) -> object:
    module = ast.parse(path.read_text())
    for node in module.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return ast.literal_eval(node.value)
    raise VerificationError(f"{name} not found in {path}")


def descriptor_json(descriptor: tuple[int, tuple[tuple[int, ...], ...]]) -> dict:
    retics, rows = descriptor
    return {"reticulations": retics, "rows": [list(row) for row in rows]}


def poly_json(poly: dict[tuple[int, ...], int]) -> dict:
    return {
        "terms": [
            {"exponents": list(exponents), "coefficient": coefficient}
            for exponents, coefficient in sorted(poly.items())
        ],
        "term_count": len(poly),
        "exact_sha256": exact_poly_hash(poly),
    }


def graph_payload(raw: dict) -> dict:
    return {
        "root": int(raw["root"]),
        "labels": tuple((int(v), str(label)) for v, label in raw["labels"]),
        "arcs": tuple((int(u), int(v)) for u, v in raw["arcs"]),
    }


def graph_from_raw(raw: dict) -> dict:
    return {
        "root": int(raw["root"]),
        "labels": tuple((int(v), str(label)) for v, label in raw["labels"]),
        "arcs": tuple((int(u), int(v)) for u, v in raw["arcs"]),
    }


def graph_vertices(graph: dict) -> tuple[int, ...]:
    vertices = {graph["root"]}
    vertices.update(v for v, _label in graph["labels"])
    for u, v in graph["arcs"]:
        vertices.add(u)
        vertices.add(v)
    return tuple(sorted(vertices))


def graph_degrees(graph: dict) -> tuple[dict[int, int], dict[int, int]]:
    indegree = {v: 0 for v in graph_vertices(graph)}
    outdegree = {v: 0 for v in graph_vertices(graph)}
    for u, v in graph["arcs"]:
        outdegree[u] += 1
        indegree[v] += 1
    return indegree, outdegree


def validate_rooted_graph(graph: dict) -> tuple[bool, tuple[str, ...]]:
    problems: list[str] = []
    indegree, outdegree = graph_degrees(graph)
    labels = dict(graph["labels"])
    if len(set(graph["arcs"])) != len(graph["arcs"]):
        problems.append("parallel arc")
    if len(labels) != len({label for _v, label in graph["labels"]}):
        problems.append("duplicate label")
    if (indegree[graph["root"]], outdegree[graph["root"]]) != (0, 2):
        problems.append("root bidegree")
    for vertex in graph_vertices(graph):
        degree = indegree[vertex], outdegree[vertex]
        if vertex == graph["root"]:
            continue
        if vertex in labels:
            if degree != (1, 0):
                problems.append(f"leaf {labels[vertex]} bidegree {degree}")
        elif degree not in {(1, 2), (2, 1)}:
            problems.append(f"internal {vertex} bidegree {degree}")
    children: dict[int, list[int]] = defaultdict(list)
    for u, v in graph["arcs"]:
        children[u].append(v)
    work = dict(indegree)
    queue = deque(sorted(v for v in graph_vertices(graph) if work[v] == 0))
    order = []
    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        for child in children[vertex]:
            work[child] -= 1
            if work[child] == 0:
                queue.append(child)
    if len(order) != len(graph_vertices(graph)):
        problems.append("directed cycle")
    reached = {graph["root"]}
    queue = deque([graph["root"]])
    while queue:
        vertex = queue.popleft()
        for child in children[vertex]:
            if child not in reached:
                reached.add(child)
                queue.append(child)
    if reached != set(graph_vertices(graph)):
        problems.append("not root reachable")
    return not problems, tuple(problems)


def root_is_lsa(graph: dict) -> bool:
    """Check that no proper vertex is stable above every labelled leaf."""
    labels = set(dict(graph["labels"]))
    children: dict[int, list[int]] = defaultdict(list)
    for u, v in graph["arcs"]:
        children[u].append(v)
    for omitted in graph_vertices(graph):
        if omitted == graph["root"]:
            continue
        reached = {graph["root"]}
        queue = deque([graph["root"]])
        while queue:
            vertex = queue.popleft()
            for child in children[vertex]:
                if child != omitted and child not in reached:
                    reached.add(child)
                    queue.append(child)
        if not (labels & reached):
            return False
    return True


def rooted_tree_child(graph: dict) -> bool:
    indegree, outdegree = graph_degrees(graph)
    labels = set(dict(graph["labels"]))
    children: dict[int, list[int]] = defaultdict(list)
    for u, v in graph["arcs"]:
        children[u].append(v)
    good = labels | {
        vertex
        for vertex in graph_vertices(graph)
        if (indegree[vertex], outdegree[vertex]) == (1, 2)
    }
    return all(
        any(child in good for child in children[vertex])
        for vertex in graph_vertices(graph)
        if outdegree[vertex]
    )


def mixed_edge(u: int, v: int, heads=()) -> tuple[int, int, int, int]:
    head_set = set(heads)
    if u < v:
        return u, v, int(u in head_set), int(v in head_set)
    return v, u, int(v in head_set), int(u in head_set)


def mixed_edge_heads(edge: tuple[int, int, int, int]) -> tuple[int, ...]:
    u, v, head_u, head_v = edge
    return tuple(vertex for vertex, bit in ((u, head_u), (v, head_v)) if bit)


def mixed_edge_other(edge: tuple[int, int, int, int], vertex: int) -> int:
    if edge[0] == vertex:
        return edge[1]
    if edge[1] == vertex:
        return edge[0]
    raise VerificationError("vertex is not incident to mixed edge")


def standard_mixed_reduction(graph: dict) -> dict:
    """Independently suppress the binary root and retain reticulation heads."""
    valid, problems = validate_rooted_graph(graph)
    require(valid and not problems, f"cannot reduce invalid rooted graph: {problems}")
    indegree, _outdegree = graph_degrees(graph)
    edges = [
        mixed_edge(u, v, (v,) if indegree[v] == 2 else ())
        for u, v in graph["arcs"]
    ]
    incident = [edge for edge in edges if graph["root"] in edge[:2]]
    require(len(incident) == 2, "root does not have two mixed incidences")
    retained = [edge for edge in edges if graph["root"] not in edge[:2]]
    first, second = incident
    left = mixed_edge_other(first, graph["root"])
    right = mixed_edge_other(second, graph["root"])
    require(left != right, "root suppression creates loop")
    heads = set(mixed_edge_heads(first)) | set(mixed_edge_heads(second))
    heads.discard(graph["root"])
    retained.append(mixed_edge(left, right, heads))
    require(len(retained) == len(set(retained)), "root suppression creates parallel edge")
    labels = tuple(sorted(graph["labels"]))
    vertices = {v for v, _label in labels}
    for edge in retained:
        vertices.update(edge[:2])
    incidence = {vertex: 0 for vertex in vertices}
    for u, v, _head_u, _head_v in retained:
        incidence[u] += 1
        incidence[v] += 1
    label_vertices = set(dict(labels))
    require(
        all(incidence[v] == (1 if v in label_vertices else 3) for v in vertices),
        "suppressed mixed graph is not simple binary",
    )
    return {"labels": labels, "edges": tuple(sorted(retained))}


def canonical_mixed_encoding(mixed: dict) -> tuple:
    """Brute-force labelled, arrowhead-preserving mixed-graph canonical form."""
    labels = dict(mixed["labels"])
    vertices = set(labels)
    head_counts: dict[int, int] = defaultdict(int)
    for edge in mixed["edges"]:
        vertices.update(edge[:2])
        for head in mixed_edge_heads(edge):
            head_counts[head] += 1
    labelled_order = tuple(v for v, _label in sorted(labels.items(), key=lambda row: row[1]))
    retics = tuple(sorted(v for v in vertices if v not in labels and head_counts[v] == 2))
    ordinary = tuple(sorted(v for v in vertices if v not in labels and head_counts[v] != 2))
    best = None
    for retic_order in permutations(retics):
        for ordinary_order in permutations(ordinary):
            order = (*labelled_order, *retic_order, *ordinary_order)
            mapping = {old: new for new, old in enumerate(order)}
            moved_labels = tuple(sorted((mapping[v], label) for v, label in labels.items()))
            moved_edges = []
            for edge in mixed["edges"]:
                heads = {mapping[v] for v in mixed_edge_heads(edge)}
                moved_edges.append(mixed_edge(mapping[edge[0]], mapping[edge[1]], heads))
            candidate = moved_labels, tuple(sorted(moved_edges))
            if best is None or candidate < best:
                best = candidate
    require(best is not None, "mixed canonicalization produced no candidate")
    return best


def displayed_switchings(graph: dict):
    indegree, _outdegree = graph_degrees(graph)
    retics = tuple(sorted(v for v in graph_vertices(graph) if indegree[v] == 2))
    incoming = {
        retic: tuple(i for i, (_u, v) in enumerate(graph["arcs"]) if v == retic)
        for retic in retics
    }
    for choices in product((0, 1), repeat=len(retics)):
        removed = {incoming[retic][1 - choice] for retic, choice in zip(retics, choices)}
        active = tuple(i for i in range(len(graph["arcs"])) if i not in removed)
        yield choices, active


def descendant_masks(graph: dict, active: tuple[int, ...], ordered_labels: tuple[str, ...]):
    label_index = {label: i for i, label in enumerate(ordered_labels)}
    labels = dict(graph["labels"])
    retained_leaves = {
        vertex: label_index[label]
        for vertex, label in labels.items()
        if label in label_index
    }
    children: dict[int, list[int]] = defaultdict(list)
    for edge_index in active:
        u, v = graph["arcs"][edge_index]
        children[u].append(v)
    cache: dict[int, int] = {}

    def visit(vertex: int) -> int:
        if vertex in cache:
            return cache[vertex]
        if vertex in labels:
            value = (1 << retained_leaves[vertex]) if vertex in retained_leaves else 0
        else:
            value = 0
            for child in children[vertex]:
                value |= visit(child)
        cache[vertex] = value
        return value

    return tuple(visit(graph["arcs"][edge_index][1]) for edge_index in active)


def raw_descriptor(graph: dict, ordered_labels: tuple[str, ...]):
    indegree, _outdegree = graph_degrees(graph)
    retics = tuple(sorted(v for v in graph_vertices(graph) if indegree[v] == 2))
    displays = tuple(product((0, 1), repeat=len(retics)))
    signatures = [[0] * len(displays) for _arc in graph["arcs"]]
    for display_index, (_choices, active) in enumerate(displayed_switchings(graph)):
        masks = descendant_masks(graph, active, ordered_labels)
        for edge_index, mask in zip(active, masks):
            signatures[edge_index][display_index] = mask
    return len(retics), tuple(sorted(tuple(row) for row in signatures if any(row)))


def canonicalize_rows(retics: int, signatures):
    signatures = tuple(sorted(set(tuple(row) for row in signatures if any(row))))
    if not retics:
        return 0, signatures
    displays = tuple(product((0, 1), repeat=retics))
    display_index = {bits: index for index, bits in enumerate(displays)}
    best = None
    for permutation in permutations(range(retics)):
        for flips in product((0, 1), repeat=retics):
            moved = []
            for signature in signatures:
                row = [0] * len(displays)
                for old_index, old_bits in enumerate(displays):
                    new_bits = tuple(
                        old_bits[permutation[j]] ^ flips[j] for j in range(retics)
                    )
                    row[display_index[new_bits]] = signature[old_index]
                moved.append(tuple(row))
            candidate = (retics, tuple(sorted(set(moved))))
            if best is None or candidate < best:
                best = candidate
    require(best is not None, "retic canonicalization produced no candidate")
    return best


def normalize_mask(mask: int, width: int = 4) -> int:
    return min(mask, ((1 << width) - 1) ^ mask)


def quartet_deck(graph: dict, port_count: int, *, normalize: bool, width: int = 4):
    labels = tuple(f"L_{index}" for index in range(port_count))
    retics, signatures = raw_descriptor(graph, labels)
    answer = []
    for quartet in combinations(range(port_count), 4):
        rows = []
        for signature in signatures:
            moved = []
            for mask in signature:
                new_mask = 0
                for new_index, old_index in enumerate(quartet):
                    if mask & (1 << old_index):
                        new_mask |= 1 << new_index
                if normalize:
                    new_mask = normalize_mask(new_mask, width=width)
                moved.append(new_mask)
            rows.append(tuple(moved))
        answer.append(canonicalize_rows(retics, rows))
    return tuple(answer)


def port_count(graph: dict) -> int:
    values = [
        int(label.split("_", 1)[1])
        for _vertex, label in graph["labels"]
        if label.startswith("L_")
    ]
    return max(values) + 1


def jc_representatives():
    colour_maps = [(0, *row) for row in permutations((1, 2, 3))]

    def canon(row: tuple[int, ...]) -> tuple[int, ...]:
        return min(tuple(mapping[value] for value in row) for mapping in colour_maps)

    reps = sorted(
        {
            canon(row)
            for row in product(range(4), repeat=4)
            if row[0] ^ row[1] ^ row[2] ^ row[3] == 0
        }
    )
    require(len(reps) == 15, "unexpected JC representative count")
    return tuple(reps)


JC_REPS = jc_representatives()


def poly_add(a: dict[tuple[int, ...], int], b: dict[tuple[int, ...], int], scale: int = 1):
    out = dict(a)
    for monomial, coefficient in b.items():
        value = out.get(monomial, 0) + scale * coefficient
        if value:
            out[monomial] = value
        else:
            out.pop(monomial, None)
    return out


def poly_mul(a: dict[tuple[int, ...], int], b: dict[tuple[int, ...], int]):
    if not a or not b:
        return {}
    out: dict[tuple[int, ...], int] = defaultdict(int)
    for ma, ca in a.items():
        for mb, cb in b.items():
            out[tuple(x + y for x, y in zip(ma, mb))] += ca * cb
    return {monomial: coefficient for monomial, coefficient in out.items() if coefficient}


def poly_const(value: int, variables: int):
    return {} if not value else {(0,) * variables: value}


_COORD_CACHE: dict[tuple[int, tuple[tuple[int, ...], ...]], tuple[dict[tuple[int, ...], int], ...]] = {}


def coordinate_polynomials(descriptor: tuple[int, tuple[tuple[int, ...], ...]]):
    if descriptor in _COORD_CACHE:
        return _COORD_CACHE[descriptor]
    retics, signatures = descriptor
    displays = tuple(product((0, 1), repeat=retics))
    variables = len(signatures) + retics
    coordinates = []
    for assignment in JC_REPS:
        total: dict[tuple[int, ...], int] = {}
        for display_index, choices in enumerate(displays):
            exponent = [0] * variables
            for variable, signature in enumerate(signatures):
                mask = signature[display_index]
                state = 0
                for leaf_index, character in enumerate(assignment):
                    if mask & (1 << leaf_index):
                        state ^= character
                if state:
                    exponent[variable] = 1
            term = {tuple(exponent): 1}
            for retic_index, choice in enumerate(choices):
                variable = len(signatures) + retic_index
                row = [0] * variables
                row[variable] = 1
                factor = (
                    {tuple(row): 1}
                    if choice == 0
                    else {(0,) * variables: 1, tuple(row): -1}
                )
                term = poly_mul(term, factor)
            total = poly_add(total, term)
        coordinates.append(total)
    _COORD_CACHE[descriptor] = tuple(coordinates)
    return _COORD_CACHE[descriptor]


def pullback(descriptor: tuple[int, tuple[tuple[int, ...], ...]], invariant):
    coordinates = coordinate_polynomials(descriptor)
    variables = len(descriptor[1]) + descriptor[0]
    cache: dict[tuple[int, ...], dict[tuple[int, ...], int]] = {
        (): poly_const(1, variables)
    }

    def monomial(indices: tuple[int, ...]):
        if indices not in cache:
            cache[indices] = poly_mul(monomial(indices[:-1]), coordinates[indices[-1]])
        return cache[indices]

    answer: dict[tuple[int, ...], int] = {}
    for indices, coefficient in invariant:
        answer = poly_add(answer, monomial(tuple(indices)), int(coefficient))
    return answer


def invariant_orbit(templates):
    rep_index = {row: index for index, row in enumerate(JC_REPS)}
    colour_maps = [(0, *row) for row in permutations((1, 2, 3))]

    def canon(row: tuple[int, ...]):
        return min(tuple(mapping[value] for value in row) for mapping in colour_maps)

    orbit = set()
    for template in templates:
        for leaf_permutation in permutations(range(4)):
            terms: dict[tuple[int, ...], int] = defaultdict(int)
            for indices, coefficient in template:
                moved = []
                for coordinate in indices:
                    assignment = JC_REPS[coordinate]
                    transported = tuple(
                        assignment[leaf_permutation[i]] for i in range(4)
                    )
                    moved.append(rep_index[canon(transported)])
                terms[tuple(sorted(moved))] += int(coefficient)
            normalized = tuple(sorted((m, c) for m, c in terms.items() if c))
            if normalized and normalized[0][1] < 0:
                normalized = tuple((m, -c) for m, c in normalized)
            orbit.add(normalized)
    return tuple(sorted(orbit))


def load_invariants():
    require(
        sha256_file(TEMPLATE_FILE) == EXPECTED_TEMPLATE_SHA,
        "invariant template input has changed",
    )
    require(
        sha256_file(SEVENTH_FILE) == EXPECTED_SEVENTH_SHA,
        "seventh invariant input has changed",
    )
    templates = parse_literal(TEMPLATE_FILE, "INVARIANT_TEMPLATES")
    seventh_payload = json.loads(SEVENTH_FILE.read_text())
    seventh = tuple(
        (tuple(int(index) + 1 for index in monomial), int(coefficient))
        for coefficient, monomial in seventh_payload["invariant"]
    )
    invariants = invariant_orbit((*templates, seventh))
    require(len(invariants) == 84, "invariant orbit did not have 84 members")
    return invariants


def function_node(tree: ast.AST, name: str) -> ast.FunctionDef:
    matches = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == name
    ]
    require(len(matches) == 1, f"expected one function named {name}")
    return matches[0]


def parent_map(root: ast.AST) -> dict[ast.AST, ast.AST]:
    return {
        child: parent
        for parent in ast.walk(root)
        for child in ast.iter_child_nodes(parent)
    }


def statically_reachable(
    node: ast.AST,
    function: ast.FunctionDef,
    parents: dict[ast.AST, ast.AST],
) -> bool:
    """Reject declarations hidden in nested functions or literal-dead arms."""

    def literal_truth(test: ast.AST) -> bool | None:
        try:
            value = ast.literal_eval(test)
        except (ValueError, TypeError):
            return None
        return bool(value)

    child = node
    while child is not function:
        parent = parents.get(child)
        require(parent is not None, "AST node escaped its enclosing function")
        if isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            if parent is not function:
                return False
        if isinstance(parent, ast.If):
            truth = literal_truth(parent.test)
            if truth is False and child in parent.body:
                return False
            if truth is True and child in parent.orelse:
                return False
        if isinstance(parent, ast.While):
            truth = literal_truth(parent.test)
            if truth is False and child in parent.body:
                return False
        child = parent
    return True


def reachable_nodes(function: ast.FunctionDef):
    parents = parent_map(function)
    return tuple(
        node
        for node in ast.walk(function)
        if statically_reachable(node, function, parents)
    )


def assignment_value(function: ast.FunctionDef, target_name: str):
    values = []
    for node in reachable_nodes(function):
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == target_name for target in node.targets):
            values.append(node.value)
    return values


def exact_quartet_complement_assignment(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "min"
        and len(node.args) == 2
        and isinstance(node.args[0], ast.Name)
        and node.args[0].id == "new_mask"
        and isinstance(node.args[1], ast.BinOp)
        and isinstance(node.args[1].op, ast.BitXor)
        and isinstance(node.args[1].left, ast.Constant)
        and node.args[1].left.value == 15
        and isinstance(node.args[1].right, ast.Name)
        and node.args[1].right.id == "new_mask"
    )


def writes_name(node: ast.AST, name: str) -> bool:
    for child in ast.walk(node):
        if isinstance(child, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):
            targets = (
                child.targets
                if isinstance(child, ast.Assign)
                else (child.target,)
            )
            if any(isinstance(target, ast.Name) and target.id == name for target in targets):
                return True
        if (
            isinstance(child, ast.AugAssign)
            and isinstance(child.target, ast.Name)
            and child.target.id == name
        ):
            return True
    return False


def is_append_of_name(statement: ast.stmt, list_name: str, value_name: str) -> bool:
    return (
        isinstance(statement, ast.Expr)
        and isinstance(statement.value, ast.Call)
        and isinstance(statement.value.func, ast.Attribute)
        and isinstance(statement.value.func.value, ast.Name)
        and statement.value.func.value.id == list_name
        and statement.value.func.attr == "append"
        and len(statement.value.args) == 1
        and isinstance(statement.value.args[0], ast.Name)
        and statement.value.args[0].id == value_name
    )


def exact_normalization_to_append_flow(function: ast.FunctionDef) -> dict | None:
    """Find a direct mask-loop normalization flowing unchanged to append."""
    parents = parent_map(function)
    candidates = []
    for loop in ast.walk(function):
        if not isinstance(loop, ast.For):
            continue
        if not statically_reachable(loop, function, parents):
            continue
        if not isinstance(loop.target, ast.Name) or loop.target.id != "mask":
            continue
        normalization_indices = [
            index
            for index, statement in enumerate(loop.body)
            if isinstance(statement, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == "new_mask"
                for target in statement.targets
            )
            and exact_quartet_complement_assignment(statement.value)
        ]
        append_indices = [
            index
            for index, statement in enumerate(loop.body)
            if is_append_of_name(statement, "moved", "new_mask")
        ]
        for normalization_index in normalization_indices:
            for append_index in append_indices:
                if append_index <= normalization_index:
                    continue
                intervening = loop.body[normalization_index + 1 : append_index]
                if any(writes_name(statement, "new_mask") for statement in intervening):
                    continue
                candidates.append(
                    {
                        "mask_loop_line": loop.lineno,
                        "normalization_line": loop.body[normalization_index].lineno,
                        "append_line": loop.body[append_index].lineno,
                    }
                )
    require(len(candidates) <= 1, "ambiguous normalization-to-append dataflow")
    return candidates[0] if candidates else None


def exact_cache_key_flow(function: ast.FunctionDef) -> dict | None:
    """Require `(p,graph_id)` to flow unchanged through cache lookup and return."""
    key_assignments = [
        (index, statement)
        for index, statement in enumerate(function.body)
        if isinstance(statement, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "key"
            for target in statement.targets
        )
        and isinstance(statement.value, ast.Tuple)
        and len(statement.value.elts) == 2
        and all(isinstance(elt, ast.Name) for elt in statement.value.elts)
        and [elt.id for elt in statement.value.elts] == ["p", "graph_id"]
    ]
    if len(key_assignments) != 1:
        return None
    assignment_index, assignment = key_assignments[0]
    if_nodes = [
        (index, statement)
        for index, statement in enumerate(function.body)
        if index > assignment_index
        and isinstance(statement, ast.If)
        and isinstance(statement.test, ast.Compare)
        and isinstance(statement.test.left, ast.Name)
        and statement.test.left.id == "key"
        and len(statement.test.ops) == 1
        and isinstance(statement.test.ops[0], ast.NotIn)
        and len(statement.test.comparators) == 1
        and isinstance(statement.test.comparators[0], ast.Name)
        and statement.test.comparators[0].id == "deck_cache"
    ]
    return_nodes = [
        (index, statement)
        for index, statement in enumerate(function.body)
        if isinstance(statement, ast.Return)
        and isinstance(statement.value, ast.Subscript)
        and isinstance(statement.value.value, ast.Name)
        and statement.value.value.id == "deck_cache"
        and isinstance(statement.value.slice, ast.Name)
        and statement.value.slice.id == "key"
    ]
    if len(if_nodes) != 1 or len(return_nodes) != 1:
        return None
    if_index, if_node = if_nodes[0]
    return_index, return_node = return_nodes[0]
    if not assignment_index < if_index < return_index:
        return None
    if any(
        writes_name(statement, "key")
        for statement in function.body[assignment_index + 1 : return_index]
    ):
        return None
    cache_sets = [
        statement
        for statement in if_node.body
        if isinstance(statement, ast.Assign)
        and any(
            isinstance(target, ast.Subscript)
            and isinstance(target.value, ast.Name)
            and target.value.id == "deck_cache"
            and isinstance(target.slice, ast.Name)
            and target.slice.id == "key"
            for target in statement.targets
        )
        and isinstance(statement.value, ast.Call)
        and isinstance(statement.value.func, ast.Name)
        and statement.value.func.id == "full_deck"
    ]
    if len(cache_sets) != 1:
        return None
    return {
        "assignment_line": assignment.lineno,
        "lookup_line": if_node.lineno,
        "return_line": return_node.lineno,
    }


def cached_deck_assignment(
    statement: ast.stmt,
    target_name: str,
    graph_name: str,
    graph_id_name: str,
) -> bool:
    return (
        isinstance(statement, ast.Assign)
        and len(statement.targets) == 1
        and isinstance(statement.targets[0], ast.Name)
        and statement.targets[0].id == target_name
        and isinstance(statement.value, ast.Call)
        and isinstance(statement.value.func, ast.Name)
        and statement.value.func.id == "cached_deck"
        and len(statement.value.args) == 3
        and isinstance(statement.value.args[0], ast.Name)
        and statement.value.args[0].id == graph_name
        and isinstance(statement.value.args[2], ast.Name)
        and statement.value.args[2].id == graph_id_name
    )


def exact_graph_id_call_flow(function: ast.FunctionDef) -> dict | None:
    """Bind the two live visit call sites to their corresponding graph ids."""
    loops = [
        node
        for node in ast.walk(function)
        if isinstance(node, ast.For)
        and isinstance(node.target, ast.Name)
        and node.target.id == "extended_words"
    ]
    if len(loops) != 1:
        return None
    loop = loops[0]
    source_calls = [
        statement
        for statement in loop.body
        if cached_deck_assignment(
            statement,
            "source_descriptors",
            "source_graph",
            "source_graph_id",
        )
    ]
    target_calls = []
    for statement in loop.body:
        if not isinstance(statement, ast.If):
            continue
        if not (
            isinstance(statement.test, ast.Compare)
            and isinstance(statement.test.left, ast.Name)
            and statement.test.left.id == "target_descriptors"
            and len(statement.test.ops) == 1
            and isinstance(statement.test.ops[0], ast.Is)
            and len(statement.test.comparators) == 1
            and isinstance(statement.test.comparators[0], ast.Constant)
            and statement.test.comparators[0].value is None
        ):
            continue
        target_calls.extend(
            child
            for child in statement.body
            if cached_deck_assignment(
                child,
                "target_descriptors",
                "target_graph",
                "target_graph_id",
            )
        )
    all_live_calls = [
        call
        for call in reachable_nodes(function)
        if isinstance(call, ast.Call)
        and isinstance(call.func, ast.Name)
        and call.func.id == "cached_deck"
    ]
    if len(source_calls) != 1 or len(target_calls) != 1 or len(all_live_calls) != 2:
        return None
    expected = {
        ("source_graph", "source_graph_id"),
        ("target_graph", "target_graph_id"),
    }
    actual = {
        (call.args[0].id, call.args[2].id)
        for call in all_live_calls
        if len(call.args) == 3
        and isinstance(call.args[0], ast.Name)
        and isinstance(call.args[2], ast.Name)
    }
    if actual != expected:
        return None
    return {
        "source_call_line": source_calls[0].lineno,
        "target_call_line": target_calls[0].lineno,
        "live_cached_deck_call_count": len(all_live_calls),
    }


def validate_source_semantics(hard: str, atlas: str, jc: str) -> dict:
    """AST-bind the declarations to the active functions, not dead text."""
    hard_tree = ast.parse(hard)
    atlas_tree = ast.parse(atlas)
    jc_tree = ast.parse(jc)
    full_deck = function_node(hard_tree, "full_deck")
    cached_deck = function_node(hard_tree, "cached_deck")
    register_graph = function_node(hard_tree, "register_graph")
    visit = function_node(hard_tree, "visit")
    all_port = function_node(jc_tree, "all_port_quartet_deck")
    atlas_deck = function_node(atlas_tree, "deck")

    normalization_flow = exact_normalization_to_append_flow(full_deck)
    require(
        normalization_flow is not None,
        (
            "active hard-cover full_deck lacks an exact width-4 complement "
            "normalization flowing unchanged to moved.append"
        ),
    )
    require(
        not any(
            exact_quartet_complement_assignment(value)
            for value in assignment_value(all_port, "new_mask")
        ),
        "active all_port_quartet_deck unexpectedly complement-normalizes",
    )

    cache_flow = exact_cache_key_flow(cached_deck)
    require(
        cache_flow is not None,
        "active cached_deck does not carry (p,graph_id) unchanged through the cache",
    )
    graph_ids = assignment_value(register_graph, "graph_id")
    require(
        any(
            isinstance(value, ast.Call)
            and isinstance(value.func, ast.Name)
            and value.func.id == "stable_hash"
            and len(value.args) == 1
            and isinstance(value.args[0], ast.Name)
            and value.args[0].id == "rooted_payload"
            for value in graph_ids
        ),
        "graph_id is not the content hash of rooted_payload",
    )
    payload_values = assignment_value(register_graph, "rooted_payload")
    require(
        any(
            isinstance(value, ast.Dict)
            and {
                key.value
                for key in value.keys
                if isinstance(key, ast.Constant) and isinstance(key.value, str)
            }
            == {"root", "labels", "arcs"}
            for value in payload_values
        ),
        "rooted graph payload does not bind root, labels, and arcs exactly",
    )
    graph_id_call_flow = exact_graph_id_call_flow(visit)
    require(
        graph_id_call_flow is not None,
        "the two live cached_deck call sites are not bound to their exact graph ids",
    )
    require(
        any(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "all_port_quartet_deck"
            for node in reachable_nodes(atlas_deck)
        ),
        "atlas deck does not call all_port_quartet_deck",
    )
    return {
        "hard_cover_full_deck_ast_bound_width": 4,
        "hard_cover_normalization_dataflow": normalization_flow,
        "hard_cover_cache_ast_key": ["selected_port_count", "exact_rooted_graph_id"],
        "hard_cover_cache_key_dataflow": cache_flow,
        "graph_id_payload_ast_keys": ["arcs", "labels", "root"],
        "cached_call_graph_ids": ["source_graph_id", "target_graph_id"],
        "cached_call_graph_id_dataflow": graph_id_call_flow,
        "atlas_deck_ast_calls_all_port_quartet_deck": True,
        "all_port_ast_has_complement_normalization": False,
    }


def inspect_sources() -> dict:
    hard_path = PRIMARY / "hard_cover_compiler.py"
    atlas_path = PRIMARY / "atlas_compiler.py"
    jc_path = PRIMARY / "jc_tensor.py"
    hard = hard_path.read_text()
    atlas = atlas_path.read_text()
    jc = jc_path.read_text()

    required_hard = {
        "full_deck": "def full_deck(graph: RootedGraph, port_count: int):",
        "complement_normalization": "new_mask = min(new_mask, 0b1111 ^ new_mask)",
        "graph_id_cache_key": "key = p, graph_id",
        "cache_scope_metadata": '"descriptor_cache_scope": "selected_port_count_and_exact_rooted_graph_id"',
        "mask_metadata": "minimum_of_quartet_side_and_complement_on_zero_sum_characters",
    }
    required_atlas = {
        "atlas_delegates_to_all_port": "return all_port_quartet_deck(graph, labels[:-1], labels[-1])",
        "atlas_raw_convention": "rooted_selected_side_masks_before_zero_sum_complement_zip",
        "source_graph_binding": '"source_graph_id": source_graph_id',
        "target_graph_binding": '"target_completion_graph_id": target_completion_graph_id',
    }
    required_jc = {
        "all_port_quartet_deck": "def all_port_quartet_deck(",
        "raw_mask_append": "moved.append(new_mask)",
        "row_zip": "tuple(sorted(set(tuple(row) for row in signatures if any(row))))",
    }
    hard_lines = {name: line_of(hard, marker) for name, marker in required_hard.items()}
    atlas_lines = {name: line_of(atlas, marker) for name, marker in required_atlas.items()}
    jc_lines = {name: line_of(jc, marker) for name, marker in required_jc.items()}

    structural = validate_source_semantics(hard, atlas, jc)

    return {
        "schema": "source-inspection-v1",
        "status": "VERIFIED",
        "method": "text plus AST inspection only; no primary imports",
        "active_function_structure": structural,
        "hard_cover_compiler": {
            "path": str(hard_path.relative_to(REPO)),
            "sha256": sha256_file(hard_path),
            "line_markers": hard_lines,
        },
        "atlas_compiler": {
            "path": str(atlas_path.relative_to(REPO)),
            "sha256": sha256_file(atlas_path),
            "line_markers": atlas_lines,
        },
        "jc_tensor": {
            "path": str(jc_path.relative_to(REPO)),
            "sha256": sha256_file(jc_path),
            "line_markers": jc_lines,
            "all_port_quartet_deck_has_complement_normalization": False,
        },
    }


def xor_state(mask: int, assignment: tuple[int, int, int, int]) -> int:
    state = 0
    for index, character in enumerate(assignment):
        if mask & (1 << index):
            state ^= character
    return state


ZERO_SUM_ASSIGNMENTS = tuple(
    row
    for row in product(range(4), repeat=4)
    if row[0] ^ row[1] ^ row[2] ^ row[3] == 0
)


def split_math_certificate() -> dict:
    complement_failures = []
    for mask in range(16):
        complement = 15 ^ mask
        for assignment in ZERO_SUM_ASSIGNMENTS:
            if xor_state(mask, assignment) != xor_state(complement, assignment):
                complement_failures.append([mask, complement, list(assignment)])
    require(not complement_failures, "mask/complement identity failed")

    quotient_classes: dict[int, list[int]] = defaultdict(list)
    for mask in range(16):
        quotient_classes[normalize_mask(mask)].append(mask)
    for representative, masks in quotient_classes.items():
        require(
            sorted(masks) == sorted({representative, 15 ^ representative}),
            "normalization class is not exactly complement-paired",
        )

    separating_assignments = {}
    for left in range(16):
        for right in range(left + 1, 16):
            if right == (15 ^ left):
                continue
            witness = None
            for assignment in ZERO_SUM_ASSIGNMENTS:
                # JC sees only whether the split sum is zero, not which of
                # the three nonzero group elements occurs.  The witness must
                # therefore separate the two zero/nonzero indicators.
                if (xor_state(left, assignment) != 0) != (
                    xor_state(right, assignment) != 0
                ):
                    witness = assignment
                    break
            require(
                witness is not None,
                f"noncomplement masks have the same JC factor: {left}, {right}",
            )
            separating_assignments[f"{left},{right}"] = list(witness)

    return {
        "schema": "zero-sum-split-math-v1",
        "status": "VERIFIED",
        "group": "JC Fourier characters represented as xor in Z2^2",
        "zero_sum_assignment_count": len(ZERO_SUM_ASSIGNMENTS),
        "canonical_representative_count": len(JC_REPS),
        "complement_identity_checked_masks": 16,
        "quotient_classes": {
            str(rep): masks for rep, masks in sorted(quotient_classes.items())
        },
        "noncomplement_pairs_separated_by_jc_zero_nonzero_factor": len(
            separating_assignments
        ),
        "sample_separators": {
            key: separating_assignments[key]
            for key in sorted(separating_assignments)[:10]
        },
    }


def internal_root_fixture() -> dict:
    return {
        "root": 6,
        "labels": ((0, "L_0"), (1, "L_1"), (2, "L_2"), (3, "L_3")),
        "arcs": ((6, 4), (6, 5), (4, 0), (4, 1), (5, 2), (5, 3)),
    }


def pendant_root_fixture() -> dict:
    return {
        "root": 6,
        "labels": ((0, "L_0"), (1, "L_1"), (2, "L_2"), (3, "L_3")),
        "arcs": ((6, 0), (6, 4), (4, 1), (4, 5), (5, 2), (5, 3)),
    }


def root_to_reticulation_fixture() -> dict:
    """A valid strong quartet network whose second root arc enters a reticulation."""
    return {
        "root": 8,
        "labels": ((0, "L_0"), (1, "L_1"), (2, "L_2"), (3, "L_3")),
        "arcs": (
            (8, 4),
            (8, 6),
            (4, 5),
            (4, 0),
            (5, 6),
            (5, 1),
            (6, 7),
            (7, 2),
            (7, 3),
        ),
    }


def relocated_root_to_reticulation_fixture() -> dict:
    """The same standard mixed graph, rooted instead on the L_0 pendant edge."""
    return {
        "root": 8,
        "labels": ((0, "L_0"), (1, "L_1"), (2, "L_2"), (3, "L_3")),
        "arcs": (
            (8, 4),
            (8, 0),
            (4, 5),
            (4, 6),
            (5, 6),
            (5, 1),
            (6, 7),
            (7, 2),
            (7, 3),
        ),
    }


def tree_product_mapping(raw_desc):
    retics, rows = raw_desc
    require(retics == 0, "tree product mapping expects no reticulations")
    normalized_rows = []
    for row in rows:
        require(len(row) == 1, "tree row should have one display")
        normalized = (normalize_mask(row[0]),)
        if any(normalized):
            normalized_rows.append(normalized)
    norm_desc = canonicalize_rows(0, normalized_rows)
    norm_index = {row: index for index, row in enumerate(norm_desc[1])}
    mapping = [[] for _row in norm_desc[1]]
    for raw_index, row in enumerate(rows):
        normalized = (normalize_mask(row[0]),)
        if any(normalized):
            mapping[norm_index[normalized]].append(raw_index)
    return norm_desc, tuple(tuple(values) for values in mapping)


def substitute_product(poly, mapping, raw_variable_count: int):
    out: dict[tuple[int, ...], int] = {}
    for monomial, coefficient in poly.items():
        exponent = [0] * raw_variable_count
        for norm_index, power in enumerate(monomial):
            for raw_index in mapping[norm_index]:
                exponent[raw_index] += power
        out = poly_add(out, {tuple(exponent): coefficient})
    return out


def descriptor_product_mapping(raw_desc):
    """Quotient arbitrary reticulate edge rows without changing display axes."""
    retics, rows = raw_desc
    normalized_rows = [
        tuple(normalize_mask(mask) for mask in row)
        for row in rows
    ]
    effective_rows = tuple(sorted(set(row for row in normalized_rows if any(row))))
    effective_index = {row: index for index, row in enumerate(effective_rows)}
    mapping = [[] for _row in effective_rows]
    for raw_index, row in enumerate(normalized_rows):
        if any(row):
            mapping[effective_index[row]].append(raw_index)
    return (
        (retics, effective_rows),
        tuple(tuple(values) for values in mapping),
    )


def substitute_descriptor_product(poly, mapping, raw_edges: int, retics: int):
    """Pull an effective descriptor polynomial back by edge-class products."""
    effective_edges = len(mapping)
    out: dict[tuple[int, ...], int] = {}
    for monomial, coefficient in poly.items():
        require(
            len(monomial) == effective_edges + retics,
            "effective polynomial has the wrong variable count",
        )
        exponent = [0] * (raw_edges + retics)
        for effective_index, raw_indices in enumerate(mapping):
            for raw_index in raw_indices:
                exponent[raw_index] += monomial[effective_index]
        for retic_index in range(retics):
            exponent[raw_edges + retic_index] = monomial[
                effective_edges + retic_index
            ]
        out = poly_add(out, {tuple(exponent): coefficient})
    return out


def descriptor_product_factorization_certificate(
    graph: dict, ordered_labels: tuple[str, ...]
) -> dict:
    """Regenerate all JC coordinates and prove the path-product quotient."""
    raw_desc = raw_descriptor(graph, ordered_labels)
    effective_desc, mapping = descriptor_product_mapping(raw_desc)
    raw_coordinates = coordinate_polynomials(raw_desc)
    effective_coordinates = coordinate_polynomials(effective_desc)
    require(
        len(raw_coordinates) == len(effective_coordinates) == len(JC_REPS),
        "unexpected coordinate count in product-factorization check",
    )
    for coordinate_index, effective_poly in enumerate(effective_coordinates):
        pulled = substitute_descriptor_product(
            effective_poly,
            mapping,
            len(raw_desc[1]),
            raw_desc[0],
        )
        require(
            pulled == raw_coordinates[coordinate_index],
            f"reticulate coordinate {coordinate_index} does not factor by products",
        )
    require(
        all(mapping),
        "an effective descriptor row has no physical edge preimage",
    )
    return {
        "reticulations": raw_desc[0],
        "physical_edge_rows": len(raw_desc[1]),
        "effective_nonzero_edge_rows": len(effective_desc[1]),
        "discarded_zero_factor_rows": (
            len(raw_desc[1]) - sum(len(indices) for indices in mapping)
        ),
        "product_class_sizes": [len(indices) for indices in mapping],
        "jc_coordinate_pullbacks_checked": len(raw_coordinates),
        "raw_descriptor_sha256": stable_hash(descriptor_json(raw_desc)),
        "effective_descriptor_sha256": stable_hash(descriptor_json(effective_desc)),
    }


def retic_flip_permutation_certificate() -> dict:
    one_retic = canonicalize_rows(1, ((1, 2), (3, 4), (5, 6)))
    one_retic_flipped = canonicalize_rows(1, ((2, 1), (4, 3), (6, 5)))
    require(one_retic == one_retic_flipped, "single retic parent flip changed descriptor")

    base_rows = ((1, 2, 3, 4), (5, 6, 7, 8), (1, 5, 9, 13))
    swapped_and_flipped = []
    # Displays are lexicographic: 00, 01, 10, 11.  Swap the two retic axes and
    # flip the new first axis.
    displays = tuple(product((0, 1), repeat=2))
    display_index = {bits: index for index, bits in enumerate(displays)}
    for row in base_rows:
        moved = [0] * 4
        for old_index, old_bits in enumerate(displays):
            new_bits = (old_bits[1] ^ 1, old_bits[0])
            moved[display_index[new_bits]] = row[old_index]
        swapped_and_flipped.append(tuple(moved))
    two_retic = canonicalize_rows(2, base_rows)
    two_retic_moved = canonicalize_rows(2, swapped_and_flipped)
    require(two_retic == two_retic_moved, "retic permutation/flip changed descriptor")
    return {
        "single_retic_flip_descriptor": descriptor_json(one_retic),
        "two_retic_permutation_flip_descriptor": descriptor_json(two_retic),
    }


def reverse_retic_parent_arc_order(graph: dict) -> dict:
    """Reorder each reticulation's two incoming arcs without changing the DAG."""
    indegree, _outdegree = graph_degrees(graph)
    arcs = list(graph["arcs"])
    for retic in sorted(v for v in graph_vertices(graph) if indegree[v] == 2):
        positions = [index for index, (_u, v) in enumerate(arcs) if v == retic]
        require(len(positions) == 2, "reticulation does not have two parent arcs")
        left, right = positions
        arcs[left], arcs[right] = arcs[right], arcs[left]
    return {**graph, "arcs": tuple(arcs)}


def root_arc_jc_factor_certificate(graph: dict, ordered_labels: tuple[str, ...]) -> dict:
    """Check both root arcs have the same JC exponent in every switching."""
    require(len(ordered_labels) == 4, "root-arc factor probe must be a quartet")
    root_arcs = tuple(
        index for index, (u, _v) in enumerate(graph["arcs"]) if u == graph["root"]
    )
    require(len(root_arcs) == 2, "fixture does not have two root arcs")
    indegree, _outdegree = graph_degrees(graph)
    switchings = 0
    factor_checks = 0
    observed_mask_pairs = set()
    for _choices, active in displayed_switchings(graph):
        masks = descendant_masks(graph, active, ordered_labels)
        by_arc = dict(zip(active, masks))
        left_mask = by_arc.get(root_arcs[0], 0)
        right_mask = by_arc.get(root_arcs[1], 0)
        observed_mask_pairs.add((left_mask, right_mask))
        for assignment in ZERO_SUM_ASSIGNMENTS:
            left_factor = xor_state(left_mask, assignment) != 0
            right_factor = xor_state(right_mask, assignment) != 0
            require(
                left_factor == right_factor,
                "root arcs do not factor through one effective edge",
            )
            factor_checks += 1
        switchings += 1
    return {
        "displayed_switchings": switchings,
        "zero_sum_assignments_per_switching": len(ZERO_SUM_ASSIGNMENTS),
        "jc_factor_equalities_checked": factor_checks,
        "root_arc_enters_reticulation": [
            indegree[graph["arcs"][edge_index][1]] == 2
            for edge_index in root_arcs
        ],
        "observed_root_arc_mask_pairs": [
            list(pair) for pair in sorted(observed_mask_pairs)
        ],
    }


def polynomial_multiply(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    answer = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            answer[i + j] += a * b
    return tuple(answer)


def positive_product_section_certificate() -> dict:
    """Exact rational global section for (x_l,x_r) -> x_l*x_r."""
    # x_l=(1+y)/2 and x_r=2y/(1+y).  Coefficient tuples are in ascending
    # powers of y.  Cross multiplication proves x_l*x_r=y exactly.
    left_num, left_den = (1, 1), (2,)
    right_num, right_den = (0, 2), (1, 1)
    product_num = polynomial_multiply(left_num, right_num)
    product_den = polynomial_multiply(left_den, right_den)
    require(product_num == (0, *product_den), "rational product section is not exact")

    # Each listed affine numerator is nonnegative at both closed endpoints
    # and is not identically zero, hence is strictly positive on 0<y<1.
    positivity_numerators = {
        "x_left": left_num,
        "1_minus_x_left": (1, -1),
        "x_right": right_num,
        "1_minus_x_right": (1, -1),
        "right_denominator": right_den,
    }
    endpoint_checks = {}
    for name, coefficients in positivity_numerators.items():
        at_zero = coefficients[0]
        at_one = sum(coefficients)
        require(at_zero >= 0 and at_one >= 0, f"{name} is negative at an endpoint")
        require(any(coefficients), f"{name} is the zero polynomial")
        endpoint_checks[name] = [at_zero, at_one]

    samples = []
    for y in (Fraction(1, 7), Fraction(1, 2), Fraction(11, 13)):
        left = (1 + y) / 2
        right = 2 * y / (1 + y)
        require(Fraction(0) < left < Fraction(1), "section left factor is not interior")
        require(Fraction(0) < right < Fraction(1), "section right factor is not interior")
        require(left * right == y, "section sample does not multiply to y")
        samples.append({"y": str(y), "x_left": str(left), "x_right": str(right)})
    return {
        "map": "pi(x_left,x_right)=x_left*x_right",
        "global_rational_section": {
            "x_left": "(1+y)/2",
            "x_right": "2*y/(1+y)",
        },
        "cross_multiplied_product_numerator": list(product_num),
        "cross_multiplied_product_denominator": list(product_den),
        "open_interval_affine_endpoint_checks": endpoint_checks,
        "submersion_witness": "partial pi / partial x_left = x_right > 0",
        "exact_samples": samples,
    }


def atlas_submersion_certificate() -> dict:
    internal = internal_root_fixture()
    pendant = pendant_root_fixture()
    root_retic = root_to_reticulation_fixture()
    relocated_root_retic = relocated_root_to_reticulation_fixture()
    for graph in (internal, pendant, root_retic, relocated_root_retic):
        valid, problems = validate_rooted_graph(graph)
        require(valid and not problems, f"invalid root-relocation fixture: {problems}")
        require(root_is_lsa(graph), "root-relocation fixture is not LSA-valid")
        require(rooted_tree_child(graph), "root-relocation fixture is not tree-child")
    raw_internal = quartet_deck(internal, 4, normalize=False)[0]
    raw_pendant = quartet_deck(pendant, 4, normalize=False)[0]
    norm_internal = quartet_deck(internal, 4, normalize=True)[0]
    norm_pendant = quartet_deck(pendant, 4, normalize=True)[0]
    require(raw_internal != raw_pendant, "rooted raw descriptors unexpectedly agree")
    require(norm_internal == norm_pendant, "normalized root-relocation descriptors differ")
    mixed_internal = canonical_mixed_encoding(standard_mixed_reduction(internal))
    mixed_pendant = canonical_mixed_encoding(standard_mixed_reduction(pendant))
    require(
        mixed_internal == mixed_pendant,
        "root-relocation fixtures do not independently reduce to one mixed graph",
    )

    raw_root_retic = quartet_deck(root_retic, 4, normalize=False)[0]
    raw_relocated_root_retic = quartet_deck(
        relocated_root_retic, 4, normalize=False
    )[0]
    norm_root_retic = quartet_deck(root_retic, 4, normalize=True)[0]
    norm_relocated_root_retic = quartet_deck(
        relocated_root_retic, 4, normalize=True
    )[0]
    require(
        raw_root_retic != raw_relocated_root_retic,
        "root-to-reticulation raw descriptors unexpectedly agree",
    )
    require(
        norm_root_retic == norm_relocated_root_retic,
        "root-to-reticulation normalized descriptors differ after relocation",
    )
    mixed_root_retic = canonical_mixed_encoding(standard_mixed_reduction(root_retic))
    mixed_relocated_root_retic = canonical_mixed_encoding(
        standard_mixed_reduction(relocated_root_retic)
    )
    require(
        mixed_root_retic == mixed_relocated_root_retic,
        "root-to-reticulation fixtures do not reduce to one mixed graph",
    )
    root_retic_factor = root_arc_jc_factor_certificate(
        root_retic, ("L_0", "L_1", "L_2", "L_3")
    )
    relocated_root_retic_factor = root_arc_jc_factor_certificate(
        relocated_root_retic, ("L_0", "L_1", "L_2", "L_3")
    )
    require(
        any(root_retic_factor["root_arc_enters_reticulation"]),
        "dedicated fixture does not actually have a root-to-reticulation arc",
    )
    require(
        not any(relocated_root_retic_factor["root_arc_enters_reticulation"]),
        "relocated fixture unexpectedly retains a root-to-reticulation arc",
    )
    require(
        quartet_deck(root_retic, 4, normalize=True)
        == quartet_deck(reverse_retic_parent_arc_order(root_retic), 4, normalize=True),
        "root-to-reticulation descriptor changed after reticulation-parent flip",
    )

    tree_product_checks = []
    for name, raw_desc in (("internal_root", raw_internal), ("pendant_root", raw_pendant)):
        mapped_norm, mapping = tree_product_mapping(raw_desc)
        require(mapped_norm == norm_internal, f"{name} product map gives wrong normalized descriptor")
        raw_coordinates = coordinate_polynomials(raw_desc)
        norm_coordinates = coordinate_polynomials(norm_internal)
        for coordinate_index, norm_poly in enumerate(norm_coordinates):
            pulled = substitute_product(norm_poly, mapping, len(raw_desc[1]))
            require(
                pulled == raw_coordinates[coordinate_index],
                f"{name} coordinate {coordinate_index} does not factor through product map",
            )
        tree_product_checks.append(
            {
                "presentation": name,
                "raw_descriptor": descriptor_json(raw_desc),
                "normalized_descriptor": descriptor_json(mapped_norm),
                "normalized_variable_to_raw_variables": [list(row) for row in mapping],
            }
        )

    # This is an additional strict-sign sanity check.  Surjectivity and the
    # submersion theorem are certified separately by an exact rational global
    # section, rather than inferred from samples.
    interior_samples = (
        (Fraction(1, 2), Fraction(1, 2)),
        (Fraction(2, 3), Fraction(3, 5)),
        (Fraction(7, 11), Fraction(5, 13)),
    )
    strict_values = []
    for left, right in interior_samples:
        value = left * right * (1 - left * right)
        require(value > 0, "strict product polynomial failed at interior sample")
        strict_values.append({"x_left": str(left), "x_right": str(right), "value": str(value)})

    _graph_path, witness_graphs = load_witness_graphs()
    retic_graph_checks = {}
    for graph_id in (GRAPH_A, GRAPH_B):
        graph = witness_graphs[graph_id]["rooted_graph"]
        labels = tuple(f"L_{index}" for index in range(6))
        quartet_checks = []
        retic_product_checks = []
        for quartet in combinations(range(6), 4):
            selected = tuple(labels[index] for index in quartet)
            quartet_checks.append(root_arc_jc_factor_certificate(graph, selected))
            retic_product_checks.append(
                descriptor_product_factorization_certificate(graph, selected)
            )
        reordered = reverse_retic_parent_arc_order(graph)
        require(
            quartet_deck(graph, 6, normalize=True)
            == quartet_deck(reordered, 6, normalize=True),
            "actual reticulation-parent arc reorder changed normalized deck",
        )
        retic_graph_checks[graph_id] = {
            "quartets_checked": len(quartet_checks),
            "displayed_switchings_checked": sum(
                row["displayed_switchings"] for row in quartet_checks
            ),
            "jc_factor_equalities_checked": sum(
                row["jc_factor_equalities_checked"] for row in quartet_checks
            ),
            "complete_jc_coordinate_product_pullbacks_checked": sum(
                row["jc_coordinate_pullbacks_checked"]
                for row in retic_product_checks
            ),
            "maximum_physical_edges_in_one_product_class": max(
                max(row["product_class_sizes"], default=0)
                for row in retic_product_checks
            ),
            "product_factorization_certificate_sha256": stable_hash(retic_product_checks),
            "normalized_deck_invariant_under_parent_arc_reordering": True,
        }

    cert = {
        "schema": "bounded-atlas-submersion-v1",
        "status": "VERIFIED",
        "theorem": (
            "For a fixed rooted presentation, raw rooted selected-side "
            "pullbacks equal standard semidirected pullbacks after the positive "
            "surjective submersion (x_left,x_right,...) -> "
            "(x_left*x_right,...).  Zero, nonzero, and strict sign are preserved."
        ),
        "counterexample_to_quotient_invariance": {
            "raw_internal_root": descriptor_json(raw_internal),
            "raw_pendant_root": descriptor_json(raw_pendant),
            "same_after_complement_normalization": descriptor_json(norm_internal),
            "independently_equal_standard_mixed_encoding_sha256": stable_hash(
                mixed_internal
            ),
        },
        "tree_product_factorization_checks": tree_product_checks,
        "root_to_reticulation_fixture": {
            "rooted_presentation": {
                "raw_descriptor": descriptor_json(raw_root_retic),
                "normalized_descriptor": descriptor_json(norm_root_retic),
                "root_arc_factor": root_retic_factor,
                "complete_jc_coordinate_product_pullback": (
                    descriptor_product_factorization_certificate(
                        root_retic, ("L_0", "L_1", "L_2", "L_3")
                    )
                ),
            },
            "relocated_presentation": {
                "raw_descriptor": descriptor_json(raw_relocated_root_retic),
                "normalized_descriptor": descriptor_json(norm_relocated_root_retic),
                "root_arc_factor": relocated_root_retic_factor,
                "complete_jc_coordinate_product_pullback": (
                    descriptor_product_factorization_certificate(
                        relocated_root_retic, ("L_0", "L_1", "L_2", "L_3")
                    )
                ),
            },
            "same_standard_mixed_encoding_sha256": stable_hash(mixed_root_retic),
            "normalized_decks_equal": True,
            "parent_flip_invariant": True,
        },
        "positive_product_submersion": positive_product_section_certificate(),
        "root_arc_factor_checks": {
            "internal_tree_root": root_arc_jc_factor_certificate(
                internal, ("L_0", "L_1", "L_2", "L_3")
            ),
            "pendant_tree_root": root_arc_jc_factor_certificate(
                pendant, ("L_0", "L_1", "L_2", "L_3")
            ),
            "reticulate_quarantine_graphs": retic_graph_checks,
        },
        "retic_parent_flip_checks": retic_flip_permutation_certificate(),
        "strict_open_cube_sample_values": strict_values,
        "verdict": {
            "graph_specific_pullbacks": "sound",
            "standard_semidirected_quotient_invariance": "raw rooted descriptors are not invariant",
            "bounded_atlas_regeneration_required": False,
        },
    }
    return cert


def load_witness_graphs():
    graph_path = SCHEMA3_N3 / "hard_cover_graphs_n3_schema3_n3_full.jsonl.gz"
    wanted = {GRAPH_A, GRAPH_B}
    found = {}
    with gzip.open(graph_path, "rt", encoding="utf-8") as handle:
        for line_index, line in enumerate(handle):
            row = json.loads(line)
            graph_id = row["graph_id"]
            if graph_id not in wanted:
                continue
            graph = graph_from_raw(row["rooted_graph"])
            payload = graph_payload(row["rooted_graph"])
            require(stable_hash(payload) == graph_id, f"graph id mismatch for {graph_id}")
            valid, problems = validate_rooted_graph(graph)
            require(valid and not problems, f"invalid quarantined graph {graph_id}: {problems}")
            require(root_is_lsa(graph), f"quarantined graph {graph_id} is not LSA-valid")
            mixed = standard_mixed_reduction(graph)
            mixed_encoding = canonical_mixed_encoding(mixed)
            found[graph_id] = {
                "line_index_zero_based": line_index,
                "line_number_one_based": line_index + 1,
                "graph_id": graph_id,
                "standard_mixed_code_sha256": row["standard_mixed_code_sha256"],
                "independent_standard_mixed_encoding_sha256": stable_hash(mixed_encoding),
                "independent_standard_mixed_encoding": mixed_encoding,
                "root_is_lsa": True,
                "rooted_tree_child": rooted_tree_child(graph),
                "rooted_graph": graph,
                "rooted_graph_json": {
                    "root": graph["root"],
                    "labels": [list(row) for row in graph["labels"]],
                    "arcs": [list(row) for row in graph["arcs"]],
                },
            }
    require(set(found) == wanted, "did not find both quarantined witness graphs")
    return graph_path, found


def quarantine_regression_certificate(invariants) -> dict:
    readme_path = QUARANTINE / "README.md"
    readme = readme_path.read_text()
    for marker in (GRAPH_B, OLD_STORED_POLY_HASH, REGENERATED_POLY_HASH):
        require(marker in readme, f"quarantine README missing marker {marker}")

    graph_path, found = load_witness_graphs()
    for record in found.values():
        require(
            record["standard_mixed_code_sha256"] == MIXED_SHA,
            "witness graph does not have expected mixed-code hash",
        )
        require(port_count(record["rooted_graph"]) == 6, "witness graph is not six-port")
    independent_mixed_a = found[GRAPH_A]["independent_standard_mixed_encoding"]
    independent_mixed_b = found[GRAPH_B]["independent_standard_mixed_encoding"]
    require(
        independent_mixed_a == independent_mixed_b,
        "independent standard mixed reductions are not labelled-isomorphic",
    )

    decks = {}
    for graph_id, record in found.items():
        graph = record["rooted_graph"]
        raw_deck = quartet_deck(graph, 6, normalize=False)
        norm_deck = quartet_deck(graph, 6, normalize=True)
        raw_chunk = raw_deck[5]
        norm_chunk = norm_deck[5]
        raw_poly = pullback(raw_chunk, invariants[50])
        norm_poly = pullback(norm_chunk, invariants[50])
        decks[graph_id] = {
            "raw_deck": raw_deck,
            "normalized_deck": norm_deck,
            "raw_chunk": raw_chunk,
            "normalized_chunk": norm_chunk,
            "raw_poly": raw_poly,
            "normalized_poly": norm_poly,
        }

    raw_a = decks[GRAPH_A]
    raw_b = decks[GRAPH_B]
    require(raw_a["raw_deck"] != raw_b["raw_deck"], "raw decks unexpectedly agree")
    require(
        raw_a["normalized_deck"] == raw_b["normalized_deck"],
        "normalized decks do not agree",
    )
    require(raw_a["raw_chunk"] != raw_b["raw_chunk"], "raw witness chunk unexpectedly agrees")
    require(
        raw_a["normalized_chunk"] == raw_b["normalized_chunk"],
        "normalized witness chunk does not agree",
    )
    require(
        exact_poly_hash(raw_a["raw_poly"]) == OLD_STORED_POLY_HASH,
        "graph A raw polynomial does not reproduce old stored hash",
    )
    require(
        exact_poly_hash(raw_b["raw_poly"]) == REGENERATED_POLY_HASH,
        "graph B raw polynomial does not reproduce regenerated hash",
    )
    require(raw_a["raw_poly"] != raw_b["raw_poly"], "raw pullbacks unexpectedly agree")
    require(
        raw_a["normalized_poly"] == raw_b["normalized_poly"],
        "normalized pullbacks do not agree",
    )

    return {
        "schema": "quarantined-descriptor-cache-regression-v1",
        "status": "VERIFIED",
        "source_stream": {
            "path": str(graph_path.relative_to(REPO)),
            "gzip_sha256": sha256_file(graph_path),
        },
        "quarantine_readme": {
            "path": str(readme_path.relative_to(REPO)),
            "sha256": sha256_file(readme_path),
            "referenced_target_graph": GRAPH_B,
            "referenced_chunk": 5,
            "referenced_invariant": 50,
            "referenced_old_stored_polynomial_hash": OLD_STORED_POLY_HASH,
            "referenced_regenerated_polynomial_hash": REGENERATED_POLY_HASH,
        },
        "invariant_inputs": {
            "base_templates": {
                "path_from_bundle_root": str(TEMPLATE_FILE.relative_to(REPO.parent)),
                "sha256": sha256_file(TEMPLATE_FILE),
                "expected_sha256": EXPECTED_TEMPLATE_SHA,
            },
            "seventh_invariant": {
                "path_from_repository": str(SEVENTH_FILE.relative_to(REPO)),
                "sha256": sha256_file(SEVENTH_FILE),
                "expected_sha256": EXPECTED_SEVENTH_SHA,
            },
        },
        "same_mixed_code_sha256": MIXED_SHA,
        "independent_standard_mixed_reconstruction": {
            "method": (
                "undirect non-reticulation arcs, retain arrowheads entering "
                "reticulations, suppress the binary root, and brute-force a "
                "label- and arrowhead-preserving canonical encoding"
            ),
            "equal": True,
            "canonical_encoding_sha256": stable_hash(independent_mixed_a),
            "stored_mixed_hash_used_as_evidence": False,
            "stored_mixed_hash_checked_only_as_regression_metadata": True,
        },
        "selected_port_count": 6,
        "quartet_chunk": 5,
        "quartet_positions_for_chunk": list(tuple(combinations(range(6), 4))[5]),
        "invariant_index": 50,
        "invariant_term_count": len(invariants[50]),
        "graphs": {
            graph_id: {
                key: value
                for key, value in found[graph_id].items()
                if key not in {"rooted_graph", "independent_standard_mixed_encoding"}
            }
            for graph_id in (GRAPH_A, GRAPH_B)
        },
        "raw_descriptor_deck_sha256": {
            GRAPH_A: stable_hash(raw_a["raw_deck"]),
            GRAPH_B: stable_hash(raw_b["raw_deck"]),
        },
        "normalized_descriptor_deck_sha256": stable_hash(raw_a["normalized_deck"]),
        "raw_chunk_descriptors": {
            GRAPH_A: descriptor_json(raw_a["raw_chunk"]),
            GRAPH_B: descriptor_json(raw_b["raw_chunk"]),
        },
        "normalized_chunk_descriptor": descriptor_json(raw_a["normalized_chunk"]),
        "raw_pullbacks": {
            GRAPH_A: poly_json(raw_a["raw_poly"]),
            GRAPH_B: poly_json(raw_b["raw_poly"]),
        },
        "normalized_pullback": poly_json(raw_a["normalized_poly"]),
        "wrong_graph_reuse_would_bind": {
            "cache_key_that_failed": "selected_port_count_and_standard_mixed_code",
            "wrong_source_graph": GRAPH_A,
            "target_graph": GRAPH_B,
            "wrong_hash": exact_poly_hash(raw_a["raw_poly"]),
            "correct_hash": exact_poly_hash(raw_b["raw_poly"]),
            "hashes_differ": exact_poly_hash(raw_a["raw_poly"]) != exact_poly_hash(raw_b["raw_poly"]),
        },
    }


def validate_open_cube_samples(samples):
    for sample in samples:
        for value in sample:
            if not (Fraction(0) < value < Fraction(1)):
                raise VerificationError(f"boundary/non-open sample rejected: {sample}")


def assert_mutation_rejected(name: str, fn):
    try:
        fn()
    except VerificationError as exc:
        return {"name": name, "status": "REJECTED", "reason": str(exc)}
    raise VerificationError(f"mutation was not rejected: {name}")


def mutation_certificate(quarantine_cert: dict) -> dict:
    internal = internal_root_fixture()
    pendant = pendant_root_fixture()
    hard_source = (PRIMARY / "hard_cover_compiler.py").read_text()
    atlas_source = (PRIMARY / "atlas_compiler.py").read_text()
    jc_source = (PRIMARY / "jc_tensor.py").read_text()
    normalization_line = "new_mask = min(new_mask, 0b1111 ^ new_mask)"

    def validate_mutated_hard(mutated: str):
        validate_source_semantics(mutated, atlas_source, jc_source)

    def omit_complement():
        raw_internal = quartet_deck(internal, 4, normalize=False)
        raw_pendant = quartet_deck(pendant, 4, normalize=False)
        require(
            raw_internal == raw_pendant,
            "omitting complement normalization leaves root-relocated decks unequal",
        )

    def wrong_width():
        wrong_internal = quartet_deck(internal, 4, normalize=True, width=5)
        wrong_pendant = quartet_deck(pendant, 4, normalize=True, width=5)
        require(
            wrong_internal == wrong_pendant,
            "width-5 normalization fails the quartet-width-4 root-relocation check",
        )

    def merge_noncomplements():
        def bad_map(mask: int) -> int:
            value = normalize_mask(mask)
            return 1 if value in (1, 2) else value

        for left in range(16):
            for right in range(left + 1, 16):
                if bad_map(left) != bad_map(right):
                    continue
                if normalize_mask(left) == normalize_mask(right):
                    continue
                for assignment in product(range(4), repeat=4):
                    if assignment[0] ^ assignment[1] ^ assignment[2] ^ assignment[3]:
                        continue
                    if (xor_state(left, assignment) != 0) != (
                        xor_state(right, assignment) != 0
                    ):
                        raise VerificationError(
                            "bad map merges noncomplement masks "
                            f"{left} and {right}, JC-factor-separated by {assignment}"
                        )
        require(False, "bad noncomplement merge was not detected")

    def boundary_samples():
        validate_open_cube_samples(
            (
                (Fraction(0), Fraction(1, 2)),
                (Fraction(1, 2), Fraction(1)),
            )
        )

    def wrong_graph_polynomial_reuse():
        reuse = quarantine_cert["wrong_graph_reuse_would_bind"]
        require(
            reuse["wrong_hash"] == reuse["correct_hash"],
            "mixed-code cache would reuse a polynomial from the wrong rooted graph",
        )

    def wrong_live_graph_ids_with_if_zero_decoys():
        source_call = (
            "source_descriptors = cached_deck(\n"
            "                source_graph, current_p + 1, source_graph_id\n"
            "            )"
        )
        source_replacement = (
            "if 0:\n"
            "                source_descriptors = cached_deck(\n"
            "                    source_graph, current_p + 1, source_graph_id\n"
            "                )\n"
            "            source_descriptors = cached_deck(\n"
            "                source_graph, current_p + 1, source_code\n"
            "            )"
        )
        target_call = (
            "target_descriptors = cached_deck(\n"
            "                    target_graph, current_p + 1, target_graph_id\n"
            "                )"
        )
        target_replacement = (
            "if 0:\n"
            "                    target_descriptors = cached_deck(\n"
            "                        target_graph, current_p + 1, target_graph_id\n"
            "                    )\n"
            "                target_descriptors = cached_deck(\n"
            "                    target_graph, current_p + 1, target_code\n"
            "                )"
        )
        require(source_call in hard_source, "source cached_deck call mutation anchor missing")
        require(target_call in hard_source, "target cached_deck call mutation anchor missing")
        mutated = hard_source.replace(source_call, source_replacement, 1)
        mutated = mutated.replace(target_call, target_replacement, 1)
        validate_mutated_hard(mutated)

    source_mutations = [
        assert_mutation_rejected(
            "source_remove_complement_normalization",
            lambda: validate_mutated_hard(
                hard_source.replace(normalization_line, "new_mask = new_mask", 1)
            ),
        ),
        assert_mutation_rejected(
            "source_hide_normalization_in_literal_dead_branch",
            lambda: validate_mutated_hard(
                hard_source.replace(
                    normalization_line,
                    (
                        "if False:\n"
                        "                    new_mask = min(new_mask, 0b1111 ^ new_mask)\n"
                        "                new_mask = new_mask"
                    ),
                    1,
                )
            ),
        ),
        assert_mutation_rejected(
            "source_overwrite_normalized_mask_before_append",
            lambda: validate_mutated_hard(
                hard_source.replace(
                    "moved.append(new_mask)",
                    "new_mask = 0\n                moved.append(new_mask)",
                    1,
                )
            ),
        ),
        assert_mutation_rejected(
            "source_normalize_against_width_5",
            lambda: validate_mutated_hard(
                hard_source.replace("0b1111 ^ new_mask", "0b11111 ^ new_mask", 1)
            ),
        ),
        assert_mutation_rejected(
            "source_merge_noncomplement_masks",
            lambda: validate_mutated_hard(
                hard_source.replace(
                    normalization_line,
                    (
                        "new_mask = (1 if min(new_mask, 0b1111 ^ new_mask) "
                        "in (1, 2) else min(new_mask, 0b1111 ^ new_mask))"
                    ),
                    1,
                )
            ),
        ),
        assert_mutation_rejected(
            "source_restore_non_graph_specific_cache_key",
            lambda: validate_mutated_hard(
                hard_source.replace("key = p, graph_id", "key = p, mixed_code", 1)
            ),
        ),
        assert_mutation_rejected(
            "source_overwrite_graph_specific_cache_key_before_lookup",
            lambda: validate_mutated_hard(
                hard_source.replace(
                    "if key not in deck_cache:",
                    "key = p\n        if key not in deck_cache:",
                    1,
                )
            ),
        ),
        assert_mutation_rejected(
            "source_wrong_live_graph_ids_with_if_zero_correct_decoys",
            wrong_live_graph_ids_with_if_zero_decoys,
        ),
    ]

    mutations = [
        assert_mutation_rejected("omit_complement_normalization", omit_complement),
        assert_mutation_rejected("normalize_at_width_5_instead_of_quartet_width_4", wrong_width),
        assert_mutation_rejected("merge_noncomplement_masks", merge_noncomplements),
        assert_mutation_rejected("use_boundary_x_0_or_x_1", boundary_samples),
        assert_mutation_rejected("reuse_polynomial_from_wrong_graph", wrong_graph_polynomial_reuse),
    ]
    return {
        "schema": "zero-sum-cleanroom-mutations-v2",
        "status": "VERIFIED",
        "all_mutations_rejected": True,
        "active_source_mutations": source_mutations,
        "mutations": mutations,
    }


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")


def json_bytes(payload: object) -> bytes:
    return (json.dumps(payload, sort_keys=True, indent=2) + "\n").encode()


def certificate_payloads() -> dict[str, object]:
    source = inspect_sources()
    split_math = split_math_certificate()
    atlas = atlas_submersion_certificate()
    invariants = load_invariants()
    quarantine = quarantine_regression_certificate(invariants)
    mutations = mutation_certificate(quarantine)
    return {
        "source_inspection_certificate.json": source,
        "split_complement_math_certificate.json": split_math,
        "bounded_atlas_submersion_certificate.json": atlas,
        "quarantine_regression_certificate.json": quarantine,
        "mutation_certificate.json": mutations,
    }


def input_provenance_entry(path: Path) -> dict:
    try:
        display_path = str(path.relative_to(REPO))
        scope = "repository"
    except ValueError:
        display_path = str(path.relative_to(REPO.parent))
        scope = "repository_bundle_root"
    return {
        "scope": scope,
        "path": display_path,
        "sha256": sha256_file(path),
    }


def manifest_payload(certificates: dict[str, object]) -> dict:
    manifest_entries = [
        {
            "path": f"certificates/{filename}",
            "sha256": sha256_bytes(json_bytes(certificates[filename])),
        }
        for filename in sorted(certificates)
    ]
    verifier_path = REVIEW_DIR / "cleanroom_verifier.py"
    verify_script = REVIEW_DIR / "verify_all.sh"
    artifact_paths = tuple(
        REVIEW_DIR / filename
        for filename in (
            "REVIEW.md",
            "RESEARCH_LOG.md",
            "ADVERSARIAL_REVIEW_PROMPT.md",
            "ADVERSARIAL_REVIEW_RESULT.md",
        )
    )
    for path in (*artifact_paths, verifier_path, verify_script):
        require(path.exists(), f"manifest input is missing: {path.name}")
    return {
        "schema": "zero-sum-cleanroom-manifest-v3",
        "status": "VERIFIED_AFTER_CORRECTION",
        "standard_library_only": True,
        "imports_primary_or_reviews": False,
        "verification_mode": "fail_closed_exact_byte_comparison",
        "repo_relative_review_dir": str(REVIEW_DIR.relative_to(REPO)),
        "first_class_input_artifacts": [
            input_provenance_entry(path)
            for path in (
                PRIMARY / "hard_cover_compiler.py",
                PRIMARY / "atlas_compiler.py",
                PRIMARY / "jc_tensor.py",
                TEMPLATE_FILE,
                SEVENTH_FILE,
                QUARANTINE / "README.md",
                SCHEMA3_N3 / "hard_cover_graphs_n3_schema3_n3_full.jsonl.gz",
            )
        ],
        "review_artifacts": [
            {
                "path": path.name,
                "sha256": sha256_file(path),
            }
            for path in artifact_paths
        ],
        "verifier": {
            "path": verifier_path.name,
            "sha256": sha256_file(verifier_path),
        },
        "verify_script": {
            "path": verify_script.name,
            "sha256": sha256_file(verify_script),
        },
        "certificates": manifest_entries,
        "release_verdicts": {
            "hard_cover_graph_id_cache_plus_normalization": "release_safe",
            "bounded_atlas_unnormalized_rooted_convention": (
                "release_safe_for_graph_specific_zero_nonzero_strict_sign_classification; "
                "not_a_canonical_semidirected_quotient_descriptor"
            ),
        },
    }


def regenerate_certificates(certificate_dir: Path) -> dict:
    certificates = certificate_payloads()
    for filename, payload in certificates.items():
        write_json(certificate_dir / filename, payload)
    manifest = manifest_payload(certificates)
    write_json(certificate_dir / "manifest.json", manifest)
    return manifest


def check_certificates(certificate_dir: Path) -> dict:
    """Recompute everything in memory and reject any stale or altered byte."""
    certificates = certificate_payloads()
    for filename, payload in certificates.items():
        path = certificate_dir / filename
        require(path.exists(), f"certificate is missing: {filename}")
        expected = json_bytes(payload)
        actual = path.read_bytes()
        require(
            actual == expected,
            (
                f"stale or altered certificate: {filename}; "
                f"expected {sha256_bytes(expected)}, found {sha256_bytes(actual)}"
            ),
        )
    manifest = manifest_payload(certificates)
    manifest_path = certificate_dir / "manifest.json"
    require(manifest_path.exists(), "certificate manifest is missing")
    expected_manifest = json_bytes(manifest)
    actual_manifest = manifest_path.read_bytes()
    require(
        actual_manifest == expected_manifest,
        (
            "stale or altered manifest; "
            f"expected {sha256_bytes(expected_manifest)}, "
            f"found {sha256_bytes(actual_manifest)}"
        ),
    )
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate-dir",
        type=Path,
        default=REVIEW_DIR / "certificates",
    )
    parser.add_argument(
        "--regenerate",
        action="store_true",
        help="rewrite deterministic certificates; default mode is fail-closed checking",
    )
    args = parser.parse_args(argv)
    try:
        manifest = (
            regenerate_certificates(args.certificate_dir)
            if args.regenerate
            else check_certificates(args.certificate_dir)
        )
    except VerificationError as exc:
        print(f"VERIFICATION FAILED: {exc}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "status": "VERIFIED_AFTER_CORRECTION",
                "mode": "regenerate" if args.regenerate else "check",
                "manifest": str((args.certificate_dir / "manifest.json").relative_to(REVIEW_DIR)),
                "certificate_count": len(manifest["certificates"]),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
