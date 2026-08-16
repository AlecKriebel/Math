#!/usr/bin/env python3
"""Stdlib-only clean-room verifier for bounded directed-relation certificates.

This implementation deliberately does not import any project package.  It
reconstructs graph and algebra semantics from inert certificate inputs.
"""

from __future__ import annotations

import argparse
import ast
import collections
import dataclasses
import fractions
import gzip
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import sys
from typing import Any, Dict, Iterable, Iterator, List, Mapping, Optional, Sequence, Set, Tuple


REVIEW_SCHEMA = 1
STATUS_PASS = "VERIFIED"
STATUS_FAIL = "FAILED"
STATUS_WAIT = "INPUTS_INCOMPLETE"


class AuditFailure(RuntimeError):
    pass


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def stable_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def repr_hash(value: Any) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def iter_jsonl(path: Path) -> Iterator[dict]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except Exception as exc:
                raise AuditFailure(f"{path}:{lineno}: invalid JSON: {exc}") from exc
            if not isinstance(value, dict):
                raise AuditFailure(f"{path}:{lineno}: record is not an object")
            yield value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, sort_keys=True, indent=2) + "\n"
    path.write_text(payload, encoding="utf-8")


def freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return tuple((key, freeze(item)) for key, item in sorted(value.items()))
    if isinstance(value, (list, tuple)):
        return tuple(freeze(item) for item in value)
    return value


@dataclasses.dataclass(frozen=True)
class RootedGraph:
    root: int
    arcs: Tuple[Tuple[int, int], ...]
    labels: Tuple[Tuple[int, str], ...]

    @staticmethod
    def from_payload(payload: Mapping[str, Any]) -> "RootedGraph":
        return RootedGraph(
            root=int(payload["root"]),
            arcs=tuple((int(u), int(v)) for u, v in payload["arcs"]),
            labels=tuple((int(v), str(label)) for v, label in payload["labels"]),
        )

    def payload(self) -> dict:
        return {
            "arcs": [[u, v] for u, v in self.arcs],
            "labels": [[v, label] for v, label in self.labels],
            "root": self.root,
        }

    @property
    def vertices(self) -> Tuple[int, ...]:
        return tuple(sorted({self.root} | {x for arc in self.arcs for x in arc} | {v for v, _ in self.labels}))

    def validate_binary(self) -> List[str]:
        problems: List[str] = []
        if len(set(self.arcs)) != len(self.arcs):
            problems.append("parallel directed arc")
        if any(u == v for u, v in self.arcs):
            problems.append("directed loop")
        label_vertices = [v for v, _ in self.labels]
        label_names = [name for _, name in self.labels]
        if len(label_vertices) != len(set(label_vertices)):
            problems.append("multiple labels on one vertex")
        if len(label_names) != len(set(label_names)):
            problems.append("duplicate leaf label")
        indeg = collections.Counter(v for _, v in self.arcs)
        outdeg = collections.Counter(u for u, _ in self.arcs)
        vertices = self.vertices
        if indeg[self.root] != 0 or outdeg[self.root] != 2:
            problems.append("root does not have bidegree (0,2)")
        labelled = set(label_vertices)
        for vertex in vertices:
            degree = (indeg[vertex], outdeg[vertex])
            if vertex == self.root:
                continue
            if vertex in labelled:
                if degree != (1, 0):
                    problems.append(f"labelled vertex {vertex} has bidegree {degree}")
            elif degree not in ((1, 2), (2, 1)):
                problems.append(f"internal vertex {vertex} has bidegree {degree}")
        adjacency: Dict[int, List[int]] = collections.defaultdict(list)
        for u, v in self.arcs:
            adjacency[u].append(v)
        colour: Dict[int, int] = {v: 0 for v in vertices}
        def visit(v: int) -> None:
            colour[v] = 1
            for w in adjacency[v]:
                if colour[w] == 1:
                    problems.append("directed cycle")
                elif colour[w] == 0:
                    visit(w)
            colour[v] = 2
        visit(self.root)
        if any(colour[v] == 0 for v in vertices):
            problems.append("vertex not reachable from root")
        return sorted(set(problems))


def graph_id(graph: RootedGraph) -> str:
    return stable_hash(graph.payload())


def load_graph_library(path: Path) -> Dict[str, dict]:
    result: Dict[str, dict] = {}
    for record in iter_jsonl(path):
        gid = str(record.get("graph_id", ""))
        graph = RootedGraph.from_payload(record["rooted_graph"])
        if graph_id(graph) != gid:
            raise AuditFailure(f"graph content hash mismatch: {gid}")
        binary_problems = graph.validate_binary()
        if binary_problems:
            raise AuditFailure(f"invalid rooted graph {gid}: {binary_problems}")
        strong_problems = strong_tree_child_problems(graph)
        if strong_problems:
            raise AuditFailure(f"graph is not strongly tree-child {gid}: {strong_problems}")
        if not root_is_lowest_stable_ancestor(graph):
            raise AuditFailure(f"graph root is not the lowest stable ancestor: {gid}")
        if len(reticulations(graph)) > 2:
            raise AuditFailure(f"graph exceeds level-2 reticulation bound: {gid}")
        if record.get("rooted_valid") is not True or record.get("rooted_validation_problems") not in ([], None):
            raise AuditFailure(f"stored rooted-validation fields are not clean: {gid}")
        if record.get("standard_strong_local") is not True:
            raise AuditFailure(f"stored standard-strong field is not true: {gid}")
        record_sha256 = stable_hash(record)
        if gid in result and result[gid]["_record_sha256"] != record_sha256:
            raise AuditFailure(f"conflicting graph record {gid}")
        result[gid] = {
            "_record_sha256": record_sha256,
            "graph_id": gid,
            "rooted_graph": record["rooted_graph"],
            "rooted_valid": record.get("rooted_valid"),
            "rooted_validation_problems": record.get("rooted_validation_problems"),
            "standard_mixed_code": record["standard_mixed_code"],
            "standard_strong_local": record.get("standard_strong_local"),
        }
    return result


def reticulations(graph: RootedGraph) -> Tuple[int, ...]:
    indeg = collections.Counter(v for _, v in graph.arcs)
    return tuple(sorted(v for v in graph.vertices if indeg[v] == 2))


def strong_tree_child_problems(graph: RootedGraph) -> List[str]:
    """Check the rooted strong tree-child conditions from the graph itself."""
    indeg = collections.Counter(v for _, v in graph.arcs)
    outdeg = collections.Counter(u for u, _ in graph.arcs)
    children: Dict[int, List[int]] = collections.defaultdict(list)
    for parent, child in graph.arcs:
        children[parent].append(child)
    problems: List[str] = []
    for vertex in graph.vertices:
        if outdeg[vertex] == 0:
            continue
        if not any(indeg[child] <= 1 for child in children[vertex]):
            problems.append(f"internal vertex {vertex} has no tree-or-leaf child")
        if indeg[vertex] == 2 and any(indeg[child] == 2 for child in children[vertex]):
            problems.append(f"reticulation {vertex} has a reticulation child")
    return sorted(set(problems))


def root_is_lowest_stable_ancestor(graph: RootedGraph) -> bool:
    parents: Dict[int, List[int]] = collections.defaultdict(list)
    children: Dict[int, List[int]] = collections.defaultdict(list)
    indegree = collections.Counter()
    for parent, child in graph.arcs:
        parents[child].append(parent)
        children[parent].append(child)
        indegree[child] += 1
    queue = [vertex for vertex in graph.vertices if indegree[vertex] == 0]
    order: List[int] = []
    while queue:
        vertex = queue.pop()
        order.append(vertex)
        for child in children[vertex]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    dominators: Dict[int, Set[int]] = {graph.root: {graph.root}}
    for vertex in order:
        if vertex == graph.root:
            continue
        parent_dominators = [dominators[parent] for parent in parents[vertex]]
        dominators[vertex] = {vertex} | set.intersection(*(set(item) for item in parent_dominators))
    leaf_vertices = [vertex for vertex, _ in graph.labels]
    common = set.intersection(*(dominators[leaf] for leaf in leaf_vertices))
    return common == {graph.root}


def displayed_masks(graph: RootedGraph, ordered_labels: Sequence[str]) -> dict:
    """Regenerate switchings and selected-side descendant masks.

    Rows are physical arcs; columns are lexicographically ordered reticulation
    parent choices.  The mask is zero when an arc is absent.
    """
    arcs = graph.arcs
    by_label = {label: vertex for vertex, label in graph.labels}
    if len(set(ordered_labels)) != len(ordered_labels):
        raise AuditFailure("selected labels are not distinct")
    try:
        selected = {by_label[label]: index for index, label in enumerate(ordered_labels)}
    except KeyError as exc:
        raise AuditFailure(f"selected label missing from graph: {exc}") from exc
    incoming: Dict[int, List[Tuple[int, int]]] = collections.defaultdict(list)
    for edge_index, (u, v) in enumerate(arcs):
        incoming[v].append((u, edge_index))
    rets = reticulations(graph)
    parent_edges = {r: tuple(sorted(incoming[r])) for r in rets}
    choices = tuple(itertools.product((0, 1), repeat=len(rets)))
    rows: List[List[int]] = [[] for _ in arcs]
    switching_records = []
    for choice in choices:
        kept = set(range(len(arcs)))
        for r, selected_parent in zip(rets, choice):
            for parent_index, (_, edge_index) in enumerate(parent_edges[r]):
                if parent_index != selected_parent:
                    kept.remove(edge_index)
        children: Dict[int, List[int]] = collections.defaultdict(list)
        for edge_index, (u, v) in enumerate(arcs):
            if edge_index in kept:
                children[u].append(v)
        memo: Dict[int, int] = {}
        visiting: Set[int] = set()
        def descendants(vertex: int) -> int:
            if vertex in memo:
                return memo[vertex]
            if vertex in visiting:
                raise AuditFailure("cycle encountered while computing descendants")
            visiting.add(vertex)
            mask = (1 << selected[vertex]) if vertex in selected else 0
            for child in children[vertex]:
                mask |= descendants(child)
            visiting.remove(vertex)
            memo[vertex] = mask
            return mask
        descendants(graph.root)
        masks = []
        for edge_index, (_, child) in enumerate(arcs):
            mask = descendants(child) if edge_index in kept else 0
            rows[edge_index].append(mask)
            masks.append(mask)
        switching_records.append({"choice": list(choice), "masks": masks})
    return {
        "reticulations": list(rets),
        "choices": [list(x) for x in choices],
        "arc_rows": [list(x) for x in rows],
        "switchings": switching_records,
    }


def canonical_effective_quartet_descriptor(
    graph: RootedGraph,
    ordered_labels: Sequence[str],
) -> Any:
    """Canonical exact effective JC descriptor for one zero-sum quartet.

    Split masks are complemented to their smaller representative because a
    zero-total character assignment gives the same character sum on either
    side.  Equal physical-edge rows are zipped because their multipliers occur
    only through a positive product.  Reticulation order and parent naming are
    minimized over all permutations and flips; these merely rename inheritance
    parameters or replace lambda by 1-lambda on the open interval.
    """
    masks = displayed_masks(graph, ordered_labels)
    reticulation_count = len(masks["reticulations"])
    full_mask = (1 << len(ordered_labels)) - 1
    choices = tuple(tuple(int(bit) for bit in choice) for choice in masks["choices"])
    choice_index = {choice: index for index, choice in enumerate(choices)}
    variants = []
    for permutation in itertools.permutations(range(reticulation_count)):
        for flips in itertools.product((0, 1), repeat=reticulation_count):
            columns = []
            for canonical_choice in itertools.product((0, 1), repeat=reticulation_count):
                original_choice = [0] * reticulation_count
                for new_index, old_index in enumerate(permutation):
                    original_choice[old_index] = canonical_choice[new_index] ^ flips[new_index]
                columns.append(choice_index[tuple(original_choice)])
            rows = []
            for raw_row in masks["arc_rows"]:
                row = tuple(
                    min(int(raw_row[column]), full_mask ^ int(raw_row[column]))
                    for column in columns
                )
                if any(row):
                    rows.append(row)
            variants.append((reticulation_count, tuple(sorted(set(rows)))))
    if not variants:
        raise AuditFailure("effective descriptor has no reticulation convention")
    return min(variants)


def canonical_effective_descriptor_deck(
    graph: RootedGraph,
    outgoing: int,
    port_correspondence: Sequence[int],
    target: bool,
) -> Any:
    return tuple(
        canonical_effective_quartet_descriptor(
            graph,
            selected_quartet_labels(outgoing, chunk, port_correspondence, target),
        )
        for chunk in range(len(quartet_chunks(outgoing)))
    )


def jc_representatives() -> Tuple[Tuple[int, int, int, int], ...]:
    colour_permutations = tuple(itertools.permutations((1, 2, 3)))
    def canonical(state: Tuple[int, ...]) -> Tuple[int, ...]:
        return min(tuple(0 if x == 0 else p[x - 1] for x in state) for p in colour_permutations)
    seen: Set[Tuple[int, ...]] = set()
    representatives: List[Tuple[int, int, int, int]] = []
    for state in itertools.product(range(4), repeat=4):
        if state[0] ^ state[1] ^ state[2] ^ state[3]:
            continue
        orbit = {tuple(0 if x == 0 else p[x - 1] for x in state) for p in colour_permutations}
        if state in seen:
            continue
        seen.update(orbit)
        representatives.append(canonical(state))
    if len(representatives) != 15:
        raise AuditFailure("JC representative reconstruction did not yield 15 coordinates")
    return tuple(representatives)


JC_REPRESENTATIVES = jc_representatives()
Exponent = Tuple[int, ...]
Polynomial = Dict[Exponent, int]


def poly_add(left: Polynomial, right: Polynomial) -> Polynomial:
    out = collections.Counter(left)
    out.update(right)
    return {monomial: coefficient for monomial, coefficient in out.items() if coefficient}


def poly_scale(poly: Polynomial, coefficient: int) -> Polynomial:
    return {monomial: coefficient * value for monomial, value in poly.items() if coefficient * value}


def poly_mul(left: Polynomial, right: Polynomial) -> Polynomial:
    out: collections.Counter = collections.Counter()
    for a, coefficient_a in left.items():
        for b, coefficient_b in right.items():
            out[tuple(x + y for x, y in zip(a, b))] += coefficient_a * coefficient_b
    return {monomial: coefficient for monomial, coefficient in out.items() if coefficient}


def poly_one(variable_count: int) -> Polynomial:
    return {(0,) * variable_count: 1}


def polynomial_tuple(poly: Polynomial) -> Tuple[Tuple[Exponent, int], ...]:
    return tuple(sorted((tuple(monomial), int(coefficient)) for monomial, coefficient in poly.items() if coefficient))


def exact_polynomial_hash(poly: Polynomial) -> str:
    return repr_hash(polynomial_tuple(poly))


def polynomial_record_id(poly: Polynomial, variable_count: int) -> str:
    payload = {
        "schema": 1,
        "terms": [[list(monomial), coefficient] for monomial, coefficient in polynomial_tuple(poly)],
        "variable_count": variable_count,
    }
    return stable_hash(payload)


def load_invariant_orbit(repo: Path) -> Tuple[Tuple[Tuple[Tuple[int, ...], int], ...], ...]:
    template_path = repo / "strong_level2_phylo_identifiability" / "src" / "jc_root_spanning_atlas_data.py"
    tree = ast.parse(template_path.read_text(encoding="utf-8"), filename=str(template_path))
    base = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "INVARIANT_TEMPLATES" for target in node.targets):
            base = ast.literal_eval(node.value)
    if base is None:
        raise AuditFailure("inert INVARIANT_TEMPLATES literal not found")
    seventh_payload = read_json(repo / "primary" / "seventh_invariant.json")
    seventh = tuple((tuple(index + 1 for index in monomial), int(coefficient)) for coefficient, monomial in seventh_payload["invariant"])
    templates = tuple(base) + (seventh,)
    colour_permutations = tuple(itertools.permutations((1, 2, 3)))
    def canonical_state(state: Tuple[int, ...]) -> Tuple[int, ...]:
        return min(tuple(0 if x == 0 else permutation[x - 1] for x in state) for permutation in colour_permutations)
    representative_index = {state: index for index, state in enumerate(JC_REPRESENTATIVES)}
    def canonical_invariant(terms: Iterable[Tuple[Tuple[int, ...], int]]) -> Tuple[Tuple[Tuple[int, ...], int], ...]:
        combined: collections.Counter = collections.Counter()
        for monomial, coefficient in terms:
            combined[tuple(sorted(monomial))] += coefficient
        result = tuple((monomial, coefficient) for monomial, coefficient in sorted(combined.items()) if coefficient)
        if result and result[0][1] < 0:
            result = tuple((monomial, -coefficient) for monomial, coefficient in result)
        return result
    orbit: Set[Tuple[Tuple[Tuple[int, ...], int], ...]] = set()
    for template in templates:
        for leaf_permutation in itertools.permutations(range(4)):
            terms = []
            for monomial, coefficient in template:
                transported = []
                for coordinate_index in monomial:
                    state = JC_REPRESENTATIVES[coordinate_index]
                    permuted = tuple(state[leaf_permutation[i]] for i in range(4))
                    transported.append(representative_index[canonical_state(permuted)])
                terms.append((tuple(transported), int(coefficient)))
            orbit.add(canonical_invariant(terms))
    result = tuple(sorted(orbit))
    if len(result) != 84:
        raise AuditFailure(f"independent invariant orbit has size {len(result)}, expected 84")
    metadata_path = repo / "primary" / "certificates" / "invariant_multihomogeneity.json"
    if metadata_path.exists():
        metadata = read_json(metadata_path)
        expected = [record["invariant_sha256"] for record in metadata["records"]]
        observed = [repr_hash(invariant) for invariant in result]
        if observed != expected:
            raise AuditFailure("independent invariant orbit disagrees with inert invariant metadata")
    return result


@dataclasses.dataclass(frozen=True)
class EffectiveTensor:
    ordered_labels: Tuple[str, ...]
    active_arc_indices: Tuple[int, ...]
    reticulations: Tuple[int, ...]
    parent_flips: Tuple[int, ...]
    coordinates: Tuple[Polynomial, ...]
    variable_count: int


def effective_jc_tensor(
    graph: RootedGraph,
    ordered_labels: Sequence[str],
    parent_flips: Optional[Sequence[int]] = None,
) -> EffectiveTensor:
    """Return the exact graph-specific quartet JC Fourier tensor.

    A physical arc is retained precisely when one switching gives it a
    nontrivial selected-side split.  Rows that are always empty or full have
    Fourier factor one on zero-sum assignments and are deleted.  Distinct
    physical arcs remain distinct variables, including two complementary root
    arcs or duplicate path rows.  This is the bounded-atlas convention.
    """
    labels = tuple(ordered_labels)
    if len(labels) != 4:
        raise AuditFailure("effective JC tensor requires an ordered quartet")
    masks = displayed_masks(graph, labels)
    full_mask = (1 << len(labels)) - 1
    active = tuple(
        edge_index
        for edge_index, row in enumerate(masks["arc_rows"])
        if any(mask not in (0, full_mask) for mask in row)
    )
    rets = tuple(int(v) for v in masks["reticulations"])
    flips = tuple(int(x) for x in (parent_flips if parent_flips is not None else (0,) * len(rets)))
    if len(flips) != len(rets) or any(x not in (0, 1) for x in flips):
        raise AuditFailure("invalid reticulation-parent flip vector")
    choices = tuple(tuple(int(x) for x in choice) for choice in masks["choices"])
    variable_count = len(active) + len(rets)
    active_position = {edge_index: position for position, edge_index in enumerate(active)}
    zero = (0,) * variable_count
    coordinates: List[Polynomial] = []
    for state in JC_REPRESENTATIVES:
        coordinate: Polynomial = {}
        for switching_index, choice in enumerate(choices):
            exponent = [0] * variable_count
            for edge_index in active:
                split_mask = masks["arc_rows"][edge_index][switching_index]
                character_sum = 0
                for leaf_index in range(4):
                    if split_mask & (1 << leaf_index):
                        character_sum ^= state[leaf_index]
                if character_sum:
                    exponent[active_position[edge_index]] = 1
            weight = poly_one(variable_count)
            for reticulation_index, selected_parent in enumerate(choice):
                inheritance_index = len(active) + reticulation_index
                inheritance_exponent = [0] * variable_count
                inheritance_exponent[inheritance_index] = 1
                selected_lambda = (selected_parent ^ flips[reticulation_index]) == 0
                if selected_lambda:
                    factor = {tuple(inheritance_exponent): 1}
                else:
                    factor = {zero: 1, tuple(inheritance_exponent): -1}
                weight = poly_mul(weight, factor)
            coordinate = poly_add(coordinate, poly_mul(weight, {tuple(exponent): 1}))
        coordinates.append(coordinate)
    return EffectiveTensor(
        ordered_labels=labels,
        active_arc_indices=active,
        reticulations=rets,
        parent_flips=flips,
        coordinates=tuple(coordinates),
        variable_count=variable_count,
    )


def invariant_pullback(
    tensor: EffectiveTensor,
    invariant: Tuple[Tuple[Tuple[int, ...], int], ...],
) -> Polynomial:
    result: Polynomial = {}
    for coordinate_monomial, coefficient in invariant:
        term = poly_one(tensor.variable_count)
        for coordinate_index in coordinate_monomial:
            term = poly_mul(term, tensor.coordinates[coordinate_index])
        result = poly_add(result, poly_scale(term, coefficient))
    return result


def quartet_chunks(outgoing: int) -> Tuple[Tuple[int, int, int, int], ...]:
    if outgoing + 1 < 4:
        raise AuditFailure("fewer than four selected ports")
    return tuple(itertools.combinations(range(outgoing + 1), 4))


def selected_quartet_labels(
    outgoing: int,
    chunk: int,
    port_correspondence: Sequence[int],
    target: bool,
) -> Tuple[str, ...]:
    chunks = quartet_chunks(outgoing)
    if chunk < 0 or chunk >= len(chunks):
        raise AuditFailure(f"quartet chunk {chunk} outside 0..{len(chunks) - 1}")
    positions = chunks[chunk]
    if target:
        return tuple(f"L_{port_correspondence[position]}" for position in positions)
    return tuple(f"L_{position}" for position in positions)


def bernstein_sign(poly: Polynomial, variable_count: int) -> Tuple[int, dict]:
    """Certify a strict sign on the open unit cube by exact Bernstein bounds."""
    if not poly:
        return 0, {"coefficient_count": 0, "minimum": "0", "maximum": "0"}
    minima = tuple(min(exponent[index] for exponent in poly) for index in range(variable_count))
    reduced = {
        tuple(exponent[index] - minima[index] for index in range(variable_count)): coefficient
        for exponent, coefficient in poly.items()
    }
    used = tuple(index for index in range(variable_count) if max(exponent[index] for exponent in reduced) > 0)
    degrees = tuple(max(exponent[index] for exponent in reduced) for index in used)
    bounds: List[fractions.Fraction] = []
    ranges = [range(degree + 1) for degree in degrees]
    for bernstein_index in itertools.product(*ranges) if ranges else [()]:
        value = fractions.Fraction(0)
        for exponent, coefficient in reduced.items():
            projected = tuple(exponent[index] for index in used)
            if not all(projected[j] <= bernstein_index[j] for j in range(len(used))):
                continue
            contribution = fractions.Fraction(coefficient)
            for j, degree in enumerate(degrees):
                contribution *= fractions.Fraction(
                    math.comb(bernstein_index[j], projected[j]),
                    math.comb(degree, projected[j]),
                )
            value += contribution
        bounds.append(value)
    minimum = min(bounds)
    maximum = max(bounds)
    if minimum >= 0 and maximum > 0:
        sign = 1
    elif maximum <= 0 and minimum < 0:
        sign = -1
    else:
        sign = 0
    certificate = {
        "used_variables": list(used),
        "degrees": list(degrees),
        "coefficient_count": len(bounds),
        "minimum": str(minimum),
        "maximum": str(maximum),
        "strict_sign": sign,
        "monomial_factor": list(minima),
    }
    return sign, certificate


def _joint_refine_colours(
    adjacency_a: Mapping[int, Sequence[Tuple[int, int]]],
    adjacency_b: Mapping[int, Sequence[Tuple[int, int]]],
    colours_a: Mapping[int, Any],
    colours_b: Mapping[int, Any],
) -> Tuple[Dict[int, int], Dict[int, int]]:
    current_a = dict(colours_a)
    current_b = dict(colours_b)
    def partition(colours: Mapping[int, Any]) -> frozenset:
        groups: Dict[Any, Set[int]] = collections.defaultdict(set)
        for vertex, colour in colours.items():
            groups[freeze(colour)].add(vertex)
        return frozenset(frozenset(vertices) for vertices in groups.values())
    while True:
        signatures_a = {
            vertex: (
                current_a[vertex],
                tuple(sorted(((edge_colour, current_a[neighbor]) for neighbor, edge_colour in adjacency_a[vertex]), key=repr)),
            )
            for vertex in adjacency_a
        }
        signatures_b = {
            vertex: (
                current_b[vertex],
                tuple(sorted(((edge_colour, current_b[neighbor]) for neighbor, edge_colour in adjacency_b[vertex]), key=repr)),
            )
            for vertex in adjacency_b
        }
        palette = {signature: index for index, signature in enumerate(sorted(set(signatures_a.values()) | set(signatures_b.values()), key=repr))}
        next_a = {vertex: palette[signature] for vertex, signature in signatures_a.items()}
        next_b = {vertex: palette[signature] for vertex, signature in signatures_b.items()}
        if partition(next_a) == partition(current_a) and partition(next_b) == partition(current_b):
            return next_a, next_b
        current_a, current_b = next_a, next_b


def _coloured_graph_isomorphism(
    adjacency_a: Mapping[int, Sequence[Tuple[int, int]]],
    adjacency_b: Mapping[int, Sequence[Tuple[int, int]]],
    initial_a: Mapping[int, Any],
    initial_b: Mapping[int, Any],
) -> Optional[Dict[int, int]]:
    if len(adjacency_a) != len(adjacency_b):
        return None

    def recurse(colours_a: Mapping[int, Any], colours_b: Mapping[int, Any], depth: int) -> Optional[Dict[int, int]]:
        refined_a, refined_b = _joint_refine_colours(adjacency_a, adjacency_b, colours_a, colours_b)
        classes_a: Dict[int, List[int]] = collections.defaultdict(list)
        classes_b: Dict[int, List[int]] = collections.defaultdict(list)
        for vertex, colour in refined_a.items():
            classes_a[colour].append(vertex)
        for vertex, colour in refined_b.items():
            classes_b[colour].append(vertex)
        if {colour: len(vertices) for colour, vertices in classes_a.items()} != {colour: len(vertices) for colour, vertices in classes_b.items()}:
            return None
        ambiguous = [colour for colour, vertices in classes_a.items() if len(vertices) > 1]
        if not ambiguous:
            mapping = {classes_a[colour][0]: classes_b[colour][0] for colour in classes_a}
            for vertex, neighbors in adjacency_a.items():
                image_neighbors = sorted((mapping[neighbor], edge_colour) for neighbor, edge_colour in neighbors)
                if image_neighbors != sorted(adjacency_b[mapping[vertex]]):
                    return None
            return mapping
        colour = min(ambiguous, key=lambda item: (len(classes_a[item]), item))
        source_vertex = min(classes_a[colour])
        marker = max(max(refined_a.values(), default=0), max(refined_b.values(), default=0)) + 1 + depth
        for target_vertex in sorted(classes_b[colour]):
            next_a: Dict[int, Any] = dict(refined_a)
            next_b: Dict[int, Any] = dict(refined_b)
            next_a[source_vertex] = ("individual", marker)
            next_b[target_vertex] = ("individual", marker)
            mapping = recurse(next_a, next_b, depth + 1)
            if mapping is not None:
                return mapping
        return None

    return recurse(initial_a, initial_b, 0)


def polynomial_variable_isomorphism(left: Polynomial, right: Polynomial) -> Optional[Dict[int, int]]:
    """Find an exact variable permutation carrying `left` to `right`."""
    if not left or not right:
        return {} if left == right else None
    left_terms = polynomial_tuple(left)
    right_terms = polynomial_tuple(right)
    left_variables = len(left_terms[0][0])
    right_variables = len(right_terms[0][0])
    if len(left_terms) != len(right_terms) or left_variables != right_variables:
        return None
    # A complete coloured graph on variables is much smaller than the raw
    # term-variable incidence graph.  Vertex colours record the coefficient /
    # exponent multiset of one variable; edge colours record the corresponding
    # two-variable multiset.  A candidate graph isomorphism is finally checked
    # against the complete polynomial, so this compression cannot create a
    # false positive.
    def variable_graph(terms: Tuple[Tuple[Exponent, int], ...]) -> Tuple[Dict[int, List[Tuple[int, Any]]], Dict[int, Any]]:
        adjacency: Dict[int, List[Tuple[int, Any]]] = {index: [] for index in range(left_variables)}
        colours: Dict[int, Any] = {}
        for variable in range(left_variables):
            colours[variable] = (
                "variable",
                tuple(sorted((coefficient, exponent[variable]) for exponent, coefficient in terms)),
            )
        for first in range(left_variables):
            for second in range(first + 1, left_variables):
                edge_colour = tuple(sorted(
                    (coefficient, min(exponent[first], exponent[second]), max(exponent[first], exponent[second]))
                    for exponent, coefficient in terms
                ))
                adjacency[first].append((second, edge_colour))
                adjacency[second].append((first, edge_colour))
        return adjacency, colours
    adjacency_left, colours_left = variable_graph(left_terms)
    adjacency_right, colours_right = variable_graph(right_terms)
    node_mapping = _coloured_graph_isomorphism(adjacency_left, adjacency_right, colours_left, colours_right)
    if node_mapping is None:
        return None
    variable_mapping = dict(node_mapping)
    if sorted(variable_mapping.values()) != list(range(left_variables)):
        return None
    transported: Polynomial = {}
    for exponent, coefficient in left.items():
        new_exponent = [0] * left_variables
        for source_index, target_index in variable_mapping.items():
            new_exponent[target_index] = exponent[source_index]
        transported[tuple(new_exponent)] = coefficient
    if transported != right:
        return None
    return variable_mapping


def positive_product_normal_form(poly: Polynomial) -> Polynomial:
    """Zip duplicate variable columns and delete inactive columns.

    If variables have the same exponent in every monomial, the polynomial
    depends on them only through their positive product.  Replacing that group
    by one effective multiplier is surjective from an open cube to an open
    interval: choose all factors to be the positive k-th root of the desired
    product.  Zero columns are inert.  This is an exact image reduction, not a
    diagonal specialization.
    """
    if not poly:
        return {}
    terms = polynomial_tuple(poly)
    width = len(terms[0][0])
    columns = [tuple(exponent[index] for exponent, _ in terms) for index in range(width)]
    unique_columns = sorted({column for column in columns if any(column)})
    normalized: Polynomial = {}
    for term_index, (_, coefficient) in enumerate(terms):
        exponent = tuple(column[term_index] for column in unique_columns)
        if exponent in normalized and normalized[exponent] != coefficient:
            raise AuditFailure("positive-product normalization collided terms with unequal coefficients")
        normalized[exponent] = coefficient
    return normalized


@dataclasses.dataclass(frozen=True)
class MixedGraph:
    vertices: Tuple[int, ...]
    labels: Tuple[Tuple[int, str], ...]
    # Each edge is (u, v, arrowhead_at_u, arrowhead_at_v), with u <= v.
    edges: Tuple[Tuple[int, int, int, int], ...]


def _mixed_edge(u: int, v: int, head_u: int, head_v: int) -> Tuple[int, int, int, int]:
    if u <= v:
        return (u, v, int(head_u), int(head_v))
    return (v, u, int(head_v), int(head_u))


def standard_mixed_graph(graph: RootedGraph, erase_triangle_arrowheads: bool = False) -> MixedGraph:
    rets = set(reticulations(graph))
    labels = dict(graph.labels)
    edges: List[Tuple[int, int, int, int]] = []
    for u, v in graph.arcs:
        edges.append(_mixed_edge(u, v, 0, 1 if v in rets else 0))
    vertices = set(graph.vertices)

    def incident(vertex: int) -> List[int]:
        return [index for index, edge in enumerate(edges) if edge[0] == vertex or edge[1] == vertex]

    def endpoint_head(edge: Tuple[int, int, int, int], vertex: int) -> int:
        if edge[0] == vertex:
            return edge[2]
        if edge[1] == vertex:
            return edge[3]
        raise AuditFailure("vertex not incident with mixed edge")

    def other(edge: Tuple[int, int, int, int], vertex: int) -> int:
        return edge[1] if edge[0] == vertex else edge[0]

    # Suppress the root first, retaining arrowheads at the two surviving
    # endpoints.  Then suppress every unlabelled, non-reticulation degree-two
    # artifact.  Reticulation arrowheads are never suppressed.
    queue = [graph.root]
    while queue:
        vertex = queue.pop()
        if vertex not in vertices or vertex in labels or vertex in rets:
            continue
        indices = incident(vertex)
        if len(indices) != 2:
            if vertex == graph.root:
                raise AuditFailure("root suppression did not encounter degree two")
            continue
        first, second = (edges[index] for index in indices)
        a, b = other(first, vertex), other(second, vertex)
        if a == b:
            raise AuditFailure("suppression creates a loop")
        new_edge = _mixed_edge(a, b, endpoint_head(first, a), endpoint_head(second, b))
        for index in sorted(indices, reverse=True):
            edges.pop(index)
        edges.append(new_edge)
        vertices.remove(vertex)
        for neighbor in (a, b):
            if neighbor not in labels and neighbor not in rets and len(incident(neighbor)) == 2:
                queue.append(neighbor)
    # No additional unlabelled degree-two artifact may remain.
    changed = True
    while changed:
        changed = False
        for vertex in sorted(vertices):
            if vertex in labels or vertex in rets:
                continue
            if len(incident(vertex)) == 2:
                queue.append(vertex)
                changed = True
                break
        while queue:
            vertex = queue.pop()
            if vertex not in vertices or vertex in labels or vertex in rets:
                continue
            indices = incident(vertex)
            if len(indices) != 2:
                continue
            first, second = (edges[index] for index in indices)
            a, b = other(first, vertex), other(second, vertex)
            if a == b:
                raise AuditFailure("degree-two suppression creates a loop")
            new_edge = _mixed_edge(a, b, endpoint_head(first, a), endpoint_head(second, b))
            for index in sorted(indices, reverse=True):
                edges.pop(index)
            edges.append(new_edge)
            vertices.remove(vertex)
    if erase_triangle_arrowheads:
        neighbors: Dict[int, Set[int]] = collections.defaultdict(set)
        for u, v, _, _ in edges:
            neighbors[u].add(v)
            neighbors[v].add(u)
        triangles: Set[frozenset] = set()
        for u in vertices:
            for v in neighbors[u]:
                for w in neighbors[u] & neighbors[v]:
                    if len({u, v, w}) == 3:
                        triangles.add(frozenset((u, v, w)))
        triangle_edges = {frozenset((u, v)) for triangle in triangles for u, v in itertools.combinations(triangle, 2)}
        edges = [
            _mixed_edge(u, v, 0, 0) if frozenset((u, v)) in triangle_edges else (u, v, hu, hv)
            for u, v, hu, hv in edges
        ]
    return MixedGraph(
        vertices=tuple(sorted(vertices)),
        labels=tuple(sorted((vertex, label) for vertex, label in labels.items() if vertex in vertices)),
        edges=tuple(sorted(edges)),
    )


def audit_standard_graph_class(graphs: Mapping[str, dict]) -> dict:
    """Independently check the bounded graph library lies in the locked class."""
    reticulation_distribution: collections.Counter = collections.Counter()
    triangle_distribution: collections.Counter = collections.Counter()
    mixed_digest = hashlib.sha256()
    for gid in sorted(graphs):
        record = graphs[gid]
        graph = RootedGraph.from_payload(record["rooted_graph"])
        reticulation_count = len(reticulations(graph))
        reticulation_distribution[reticulation_count] += 1
        mixed = standard_mixed_graph(graph)
        endpoint_pairs = [(u, v) for u, v, _, _ in mixed.edges]
        if len(endpoint_pairs) != len(set(endpoint_pairs)):
            raise AuditFailure(f"standard reduction contains a parallel-edge artifact: {gid}")
        neighbors: Dict[int, Set[int]] = collections.defaultdict(set)
        for u, v, _, _ in mixed.edges:
            neighbors[u].add(v)
            neighbors[v].add(u)
        triangles = {
            tuple(sorted((u, v, w)))
            for u in mixed.vertices
            for v in neighbors[u]
            for w in neighbors[u] & neighbors[v]
            if len({u, v, w}) == 3
        }
        if len(triangles) > 1:
            raise AuditFailure(f"standard local graph has more than one triangle: {gid}")
        triangle_distribution[len(triangles)] += 1
        fingerprint = stable_hash({
            "edges": [list(edge) for edge in mixed.edges],
            "labels": [list(label) for label in mixed.labels],
        })
        mixed_digest.update(canonical_json_bytes([gid, fingerprint]))
        mixed_digest.update(b"\n")
    return {
        "graphs": len(graphs),
        "all_binary_strong_tree_child": True,
        "all_roots_are_lowest_stable_ancestors": True,
        "all_level_at_most_two": True,
        "all_standard_reductions_parallel_free": True,
        "all_have_at_most_one_triangle": True,
        "reticulation_distribution": {
            str(key): value for key, value in sorted(reticulation_distribution.items())
        },
        "triangle_distribution": {
            str(key): value for key, value in sorted(triangle_distribution.items())
        },
        "mixed_fingerprint_digest": mixed_digest.hexdigest(),
    }


def relabel_ports(graph: MixedGraph, inverse_target_port_map: Mapping[int, int]) -> MixedGraph:
    labels = []
    for vertex, label in graph.labels:
        if label.startswith("L_") and label[2:].isdigit():
            target_index = int(label[2:])
            if target_index not in inverse_target_port_map:
                raise AuditFailure(f"target port L_{target_index} absent from port map")
            label = f"L_{inverse_target_port_map[target_index]}"
        labels.append((vertex, label))
    return MixedGraph(graph.vertices, tuple(sorted(labels)), graph.edges)


def mixed_graph_isomorphic(left: MixedGraph, right: MixedGraph) -> bool:
    if len(left.vertices) != len(right.vertices) or len(left.edges) != len(right.edges):
        return False
    def encoded(graph: MixedGraph) -> Tuple[Dict[int, List[Tuple[int, Any]]], Dict[int, Any]]:
        labels = dict(graph.labels)
        adjacency: Dict[int, List[Tuple[int, Any]]] = {vertex: [] for vertex in graph.vertices}
        for u, v, head_u, head_v in graph.edges:
            adjacency[u].append((v, (head_u, head_v)))
            adjacency[v].append((u, (head_v, head_u)))
        colours = {
            vertex: (
                "label" if vertex in labels else "internal",
                labels.get(vertex),
                len(adjacency[vertex]),
                sum(edge_colour[0] for _, edge_colour in adjacency[vertex]),
            )
            for vertex in graph.vertices
        }
        return adjacency, colours
    adjacency_left, colours_left = encoded(left)
    adjacency_right, colours_right = encoded(right)
    return _coloured_graph_isomorphism(adjacency_left, adjacency_right, colours_left, colours_right) is not None


def isomorphic_or_ordinary_t(
    source: RootedGraph,
    target: RootedGraph,
    port_correspondence: Sequence[int],
) -> Tuple[bool, str]:
    inverse = {int(target_position): source_position for source_position, target_position in enumerate(port_correspondence)}
    source_mixed = standard_mixed_graph(source, erase_triangle_arrowheads=False)
    target_mixed = relabel_ports(standard_mixed_graph(target, erase_triangle_arrowheads=False), inverse)
    if mixed_graph_isomorphic(source_mixed, target_mixed):
        return True, "labelled_isomorphism"
    source_t = standard_mixed_graph(source, erase_triangle_arrowheads=True)
    target_t = relabel_ports(standard_mixed_graph(target, erase_triangle_arrowheads=True), inverse)
    if mixed_graph_isomorphic(source_t, target_t):
        return True, "ordinary_triangle_redirection"
    return False, "neither"


def directed_retention(source_nonzero: int, target_nonzero: int) -> bool:
    """Necessary condition for source-relative containment."""
    return source_nonzero & ~target_nonzero == 0


def hard_cover_key_from_relation(raw: Mapping[str, Any]) -> Any:
    source_independent_id = stable_hash({"schema": 1, "primitive_provenance": raw["source_roles"]})
    target_independent_id = stable_hash({"schema": 1, "primitive_provenance": raw["target_roles"]})
    return freeze((
        source_independent_id,
        raw["source_position_to_label"],
        raw["source_roles"],
        target_independent_id,
        raw["target_position_to_label"],
        raw["target_roles"],
    ))


def hard_cover_key_from_root(root_case: Mapping[str, Any]) -> Any:
    source_independent_id = stable_hash({"schema": 1, "primitive_provenance": root_case["source_provenance"]})
    target_independent_id = stable_hash({"schema": 1, "primitive_provenance": root_case["target_provenance"]})
    return freeze((
        source_independent_id,
        root_case["source_position_to_label"],
        root_case["source_provenance"],
        target_independent_id,
        root_case["target_position_to_label"],
        root_case["target_provenance"],
    ))


def discover_inputs(repo: Path) -> dict:
    certificates = repo / "primary" / "certificates"
    summaries = []
    for path in sorted(certificates.glob("bounded_relation_*summary.json")):
        try:
            payload = read_json(path)
        except Exception:
            continue
        runs = payload.get("runs") or []
        if not runs:
            continue
        summaries.append({"path": str(path.relative_to(repo)), "payload": payload})
    return {"summaries": summaries}


def external_input_manifest(repo: Path, input_lock: Mapping[str, Any], families: Sequence[str]) -> dict:
    paths: Set[Path] = set()
    for family in families:
        lock = input_lock.get(family, {})
        if "merged_summary" not in lock or "crosswalk_summary" not in lock:
            continue
        merged_path = resolve_declared(repo, lock["merged_summary"])
        crosswalk_summary_path = resolve_declared(repo, lock["crosswalk_summary"])
        paths.update((merged_path, crosswalk_summary_path))
        hard_cover_summary_path = None
        if "hard_cover_summary" in lock:
            hard_cover_summary_path = resolve_declared(repo, lock["hard_cover_summary"])
            paths.add(hard_cover_summary_path)
        merged = read_json(merged_path)
        paths.add(resolve_declared(repo, merged["support_universe_path"]))
        paths.add(resolve_declared(repo, merged["seventh_template_path"]))
        template = (repo / merged["template_path"]).resolve()
        if not template.is_file():
            raise AuditFailure("invariant template named by merged summary is missing")
        paths.add(template)
        run = merged["runs"][0]["bounded_relation_certificate"]
        for field in ("relation_path", "graph_library_path", "polynomial_library_path", "sign_library_path"):
            paths.add(resolve_declared(repo, run[field]))
        for shard in merged.get("shards", []):
            shard_summary = resolve_declared(repo, shard["summary_path"])
            paths.add(shard_summary)
            shard_payload = read_json(shard_summary)["runs"][0]["bounded_relation_certificate"]
            paths.add(resolve_declared(repo, shard_payload["relation_path"]))
        crosswalk = read_json(crosswalk_summary_path)
        paths.add(resolve_declared(repo, crosswalk["root_stream"]))
        paths.add(resolve_declared(repo, crosswalk["crosswalk_path"]))
        if hard_cover_summary_path is not None:
            hard_cover = read_json(hard_cover_summary_path)["runs"][0]["hard_cover"]
            for field in ("root_case_path", "relation_path", "graph_library_path", "polynomial_library_path"):
                paths.add(resolve_declared(repo, hard_cover[field]))
    return {
        os.path.relpath(path, repo): {"bytes": path.stat().st_size, "sha256": file_hash(path)}
        for path in sorted(paths)
    }


def logical_jsonl_hash(path: Path) -> Tuple[str, int]:
    digest = hashlib.sha256()
    count = 0
    for record in iter_jsonl(path):
        digest.update(canonical_json_bytes(record))
        digest.update(b"\n")
        count += 1
    return digest.hexdigest(), count


def resolve_declared(repo: Path, declared: str) -> Path:
    path = Path(declared)
    if not path.is_absolute():
        path = repo / path
    path = path.resolve()
    try:
        path.relative_to(repo)
    except ValueError as exc:
        raise AuditFailure(f"declared path escapes repository: {declared}") from exc
    if not path.is_file():
        raise AuditFailure(f"declared input is missing: {declared}")
    return path


def load_polynomial_library(path: Path) -> Dict[str, dict]:
    result: Dict[str, dict] = {}
    for record in iter_jsonl(path):
        polynomial_id = record["polynomial_id"]
        variable_count = int(record["variable_count"])
        poly = {tuple(int(x) for x in exponent): int(coefficient) for exponent, coefficient in record["terms"]}
        if any(len(exponent) != variable_count for exponent in poly):
            raise AuditFailure(f"wrong exponent width in polynomial {polynomial_id}")
        if polynomial_record_id(poly, variable_count) != polynomial_id:
            raise AuditFailure(f"polynomial content id mismatch: {polynomial_id}")
        if exact_polynomial_hash(poly) != record.get("exact_polynomial_sha256"):
            raise AuditFailure(f"exact polynomial hash mismatch: {polynomial_id}")
        if polynomial_id in result and result[polynomial_id] != record:
            raise AuditFailure(f"conflicting polynomial record: {polynomial_id}")
        result[polynomial_id] = record
    return result


def polynomial_from_record(record: Mapping[str, Any]) -> Polynomial:
    return {tuple(int(x) for x in exponent): int(coefficient) for exponent, coefficient in record["terms"]}


def audit_sign_library(path: Path, polynomials: Mapping[str, dict]) -> dict:
    payload = read_json(path)
    if not isinstance(payload, dict):
        raise AuditFailure("sign library is not an object")
    distributions: collections.Counter = collections.Counter()
    certificates = {}
    for exact_hash, record in sorted(payload.items()):
        polynomial_id = record.get("polynomial_id")
        if polynomial_id not in polynomials:
            raise AuditFailure(f"sign entry references absent polynomial: {polynomial_id}")
        polynomial_record = polynomials[polynomial_id]
        if exact_hash != polynomial_record["exact_polynomial_sha256"]:
            raise AuditFailure(f"sign-library exact hash key mismatch: {polynomial_id}")
        if record.get("exact_polynomial_sha256") != exact_hash:
            raise AuditFailure(f"sign-library exact hash field mismatch: {polynomial_id}")
        poly = polynomial_from_record(polynomial_record)
        sign, certificate = bernstein_sign(poly, int(polynomial_record["variable_count"]))
        if sign == 0:
            raise AuditFailure(f"independent Bernstein certificate is inconclusive: {polynomial_id}")
        if sign != int(record.get("strict_sign", 0)):
            raise AuditFailure(f"independent sign disagrees: {polynomial_id}")
        if not record.get("certified"):
            raise AuditFailure(f"stored sign entry is not certified: {polynomial_id}")
        distributions[sign] += 1
        certificates[polynomial_id] = certificate
    if set(payload) != {record["exact_polynomial_sha256"] for record in polynomials.values()}:
        raise AuditFailure("sign and polynomial libraries are not in bijection")
    return {
        "records": len(payload),
        "strict_sign_distribution": {str(key): value for key, value in sorted(distributions.items())},
        "certificate_digest": stable_hash(certificates),
    }


def support_role(record: Mapping[str, Any]) -> Any:
    return freeze([record["core_id"], record["repair_index"], record["words"]])


def source_graph_from_support(record: Mapping[str, Any], position_to_label: Sequence[int]) -> RootedGraph:
    outgoing_labels = sorted(label for _, label in record["labels"] if label != "INCOMING")
    selected_labels = outgoing_labels + ["INCOMING"]
    if sorted(position_to_label) != list(range(len(selected_labels))):
        raise AuditFailure("source support position map is not a permutation")
    rename = {selected_labels[position]: f"L_{position_to_label[position]}" for position in range(len(selected_labels))}
    return RootedGraph(
        root=int(record["root"]),
        arcs=tuple(sorted((int(u), int(v)) for u, v in record["arcs"])),
        labels=tuple(sorted((int(vertex), rename[label]) for vertex, label in record["labels"])),
    )


def audit_support_partition(
    support_path: Path,
    outgoing: int,
    declared_cores: Sequence[str],
    shard_records: Sequence[Mapping[str, Any]],
    relations: Sequence[dict],
) -> dict:
    support = read_json(support_path)
    in_scope = [record for record in support["records"] if int(record["outgoing_count"]) == outgoing]
    expected_cores = sorted({record["core_id"] for record in in_scope})
    if sorted(declared_cores) != expected_cores or len(declared_cores) != len(set(declared_cores)):
        raise AuditFailure(
            f"source-core partition mismatch for n{outgoing}: expected {expected_cores}, got {list(declared_cores)}"
        )
    shard_cores: List[str] = []
    for shard in shard_records:
        core = shard.get("core")
        shard_cores.append(core)
    if sorted(shard_cores) != expected_cores or len(shard_cores) != len(set(shard_cores)):
        raise AuditFailure("shards do not form a disjoint exhaustive source-core partition")
    role_to_support: Dict[Any, Mapping[str, Any]] = {}
    independent_ids: Dict[Any, str] = {}
    for record in in_scope:
        role = support_role(record)
        if role in role_to_support:
            raise AuditFailure("support role is not unique")
        role_to_support[role] = record
        independent_ids[role] = stable_hash({
            "schema": 1,
            "outgoing": outgoing,
            "rooted_support": {
                "arcs": [list(arc) for arc in sorted(tuple(x) for x in record["arcs"])],
                "labels": [[vertex, label] for vertex, label in sorted(record["labels"])],
                "root": record["root"],
            },
            "provenance": [record["core_id"], record["repair_index"], record["words"]],
        })
    primary_to_independent: Dict[str, str] = {}
    role_counts: collections.Counter = collections.Counter()
    for relation in relations:
        for raw in relation["raw_coverage"]:
            role = freeze(raw["source_roles"])
            if role not in role_to_support:
                raise AuditFailure(f"raw source role absent from support universe: {raw['source_roles']}")
            support_record = role_to_support[role]
            rebuilt = source_graph_from_support(support_record, raw["source_position_to_label"])
            if graph_id(rebuilt) != raw["source_graph_id"]:
                raise AuditFailure("source position map does not reconstruct its bound graph")
            primary_id = raw["source_primitive_id"]
            independent_id = independent_ids[role]
            previous = primary_to_independent.setdefault(primary_id, independent_id)
            if previous != independent_id:
                raise AuditFailure("one primary primitive id names two independent supports")
            role_counts[role] += 1
    if set(primary_to_independent.values()) != set(independent_ids.values()):
        raise AuditFailure("source primitive ids do not cover the support partition")
    if len(primary_to_independent) != len(independent_ids):
        raise AuditFailure("distinct support primitives collapse to one primary primitive id")
    if any(role_counts[role] == 0 for role in role_to_support):
        raise AuditFailure("source support omitted from relation universe")
    core_counts: collections.Counter = collections.Counter()
    for role, count in role_counts.items():
        core_counts[role[0]] += count
    return {
        "outgoing": outgoing,
        "cores": expected_cores,
        "support_records": len(in_scope),
        "primary_primitive_ids": len(primary_to_independent),
        "independent_primitive_ids": len(set(independent_ids.values())),
        "raw_coverage_by_core": dict(sorted(core_counts.items())),
        "independent_id_map_sha256": stable_hash(sorted(primary_to_independent.items())),
    }


def signature_mask_reference(
    graph: RootedGraph,
    outgoing: int,
    port_correspondence: Sequence[int],
    target: bool,
    invariants: Sequence[Tuple[Tuple[Tuple[int, ...], int], ...]],
) -> int:
    mask = 0
    for chunk_index in range(len(quartet_chunks(outgoing))):
        labels = selected_quartet_labels(outgoing, chunk_index, port_correspondence, target)
        tensor = effective_jc_tensor(graph, labels)
        for invariant_index, invariant in enumerate(invariants):
            if invariant_pullback(tensor, invariant):
                bit = chunk_index * len(invariants) + invariant_index
                mask |= 1 << bit
    return mask


def tensor_nonzero_invariant_mask_encoded(
    tensor: EffectiveTensor,
    invariants: Sequence[Tuple[Tuple[Tuple[int, ...], int], ...]],
) -> int:
    """Exact sparse Kronecker encoding for fast zero/nonzero pullbacks.

    Every invariant has total degree at most `d`.  Encoding an exponent vector
    in base `d+1` is injective for all monomials that can occur, and polynomial
    multiplication becomes addition of integer exponent codes without carries.
    This is exact integer algebra, not modular or probabilistic evaluation.
    """
    maximum_degree = max(
        (len(coordinate_monomial) for invariant in invariants for coordinate_monomial, _ in invariant),
        default=0,
    )
    base = maximum_degree + 1
    powers = [base ** index for index in range(tensor.variable_count)]

    def encode(poly: Polynomial) -> Dict[int, int]:
        out: Dict[int, int] = {}
        for exponent, coefficient in poly.items():
            code = sum(value * powers[index] for index, value in enumerate(exponent))
            if code in out:
                out[code] += coefficient
                if not out[code]:
                    del out[code]
            else:
                out[code] = coefficient
        return out

    coordinates = tuple(encode(poly) for poly in tensor.coordinates)
    product_cache: Dict[Tuple[int, ...], Dict[int, int]] = {(): {0: 1}}

    def product(coordinate_monomial: Tuple[int, ...]) -> Dict[int, int]:
        cached = product_cache.get(coordinate_monomial)
        if cached is not None:
            return cached
        prefix = coordinate_monomial[:-1]
        left = product(prefix)
        right = coordinates[coordinate_monomial[-1]]
        combined: collections.Counter = collections.Counter()
        for left_code, left_coefficient in left.items():
            for right_code, right_coefficient in right.items():
                combined[left_code + right_code] += left_coefficient * right_coefficient
        result = {code: coefficient for code, coefficient in combined.items() if coefficient}
        product_cache[coordinate_monomial] = result
        return result

    mask = 0
    for invariant_index, invariant in enumerate(invariants):
        pullback: collections.Counter = collections.Counter()
        for coordinate_monomial, coefficient in invariant:
            for code, value in product(coordinate_monomial).items():
                pullback[code] += coefficient * value
        if any(pullback.values()):
            mask |= 1 << invariant_index
    return mask


def signature_mask(
    graph: RootedGraph,
    outgoing: int,
    port_correspondence: Sequence[int],
    target: bool,
    invariants: Sequence[Tuple[Tuple[Tuple[int, ...], int], ...]],
) -> int:
    mask = 0
    for chunk_index in range(len(quartet_chunks(outgoing))):
        labels = selected_quartet_labels(outgoing, chunk_index, port_correspondence, target)
        tensor = effective_jc_tensor(graph, labels)
        chunk_mask = tensor_nonzero_invariant_mask_encoded(tensor, invariants)
        mask |= chunk_mask << (chunk_index * len(invariants))
    return mask


def verify_zero_sum_product_factorization(graph: RootedGraph, ordered_labels: Sequence[str]) -> dict:
    """Check the exact positive path-product factorization of a quartet tensor."""
    masks = displayed_masks(graph, ordered_labels)
    full = 15
    active = [
        edge_index
        for edge_index, row in enumerate(masks["arc_rows"])
        if any(mask not in (0, full) for mask in row)
    ]
    normalized_rows = {
        edge_index: tuple(min(mask, full ^ mask) for mask in masks["arc_rows"][edge_index])
        for edge_index in active
    }
    groups: Dict[Tuple[int, ...], List[int]] = collections.defaultdict(list)
    for position, edge_index in enumerate(active):
        groups[normalized_rows[edge_index]].append(position)
    tensor = effective_jc_tensor(graph, ordered_labels)
    for coordinate in tensor.coordinates:
        for exponent in coordinate:
            for positions in groups.values():
                values = {exponent[position] for position in positions}
                if len(values) != 1:
                    raise AuditFailure("zero-sum complementary split rows do not factor through their product")
    return {
        "physical_active_arcs": len(active),
        "effective_split_rows": len(groups),
        "positive_product_reductions": len(active) - len(groups),
        "factorization_exact": True,
        "open_product_map_surjective": True,
    }


def audit_zero_sum_product_factorization(relations: Sequence[dict], graphs: Mapping[str, dict]) -> dict:
    graph_ids = sorted(
        {record["source_graph_id"] for record in relations}
        | {record["target_completion_graph_id"] for record in relations}
    )
    distribution: collections.Counter = collections.Counter()
    total_reductions = 0
    record_digest = hashlib.sha256()
    quartet_tensor_count = 0
    for gid in graph_ids:
        graph = RootedGraph.from_payload(graphs[gid]["rooted_graph"])
        labels = sorted(
            (label for _, label in graph.labels if label.startswith("L_") and label[2:].isdigit()),
            key=lambda item: int(item[2:]),
        )
        outgoing = len(labels) - 1
        per_chunk = []
        for positions in quartet_chunks(outgoing):
            ordered = tuple(f"L_{position}" for position in positions)
            certificate = verify_zero_sum_product_factorization(graph, ordered)
            per_chunk.append(certificate)
            total_reductions += certificate["positive_product_reductions"]
            distribution[certificate["positive_product_reductions"]] += 1
        quartet_tensor_count += len(per_chunk)
        record_digest.update(canonical_json_bytes([gid, per_chunk]))
        record_digest.update(b"\n")
    return {
        "graphs": len(graph_ids),
        "quartet_tensors": quartet_tensor_count,
        "total_positive_product_reductions": total_reductions,
        "reduction_distribution": {str(key): value for key, value in sorted(distribution.items())},
        "all_exact": True,
        "record_digest": record_digest.hexdigest(),
    }


def audit_signature_retention(
    relations: Sequence[dict],
    graphs: Mapping[str, dict],
    invariants: Sequence[Tuple[Tuple[Tuple[int, ...], int], ...]],
) -> dict:
    graph_uses: Dict[Tuple[str, bool, int, Tuple[int, ...]], str] = {}
    for relation in relations:
        outgoing = int(relation["outgoing"])
        port_map = tuple(int(x) for x in relation["port_correspondence"])
        for key, expected_hash in (
            (
                (relation["source_graph_id"], False, outgoing, tuple(range(outgoing + 1))),
                relation["source_signature_sha256"],
            ),
            (
                (relation["target_completion_graph_id"], True, outgoing, port_map),
                relation["target_signature_sha256"],
            ),
        ):
            previous = graph_uses.setdefault(key, expected_hash)
            if previous != expected_hash:
                raise AuditFailure(f"one graph/port use has conflicting signatures: {key[0]}")

    descriptor_groups: Dict[Any, List[Tuple[Tuple[str, bool, int, Tuple[int, ...]], str]]] = collections.defaultdict(list)
    graph_descriptor_digest = hashlib.sha256()
    for key, expected_hash in sorted(graph_uses.items(), key=lambda item: repr(item[0])):
        gid, target, outgoing, port_map = key
        graph = RootedGraph.from_payload(graphs[gid]["rooted_graph"])
        descriptor = canonical_effective_descriptor_deck(graph, outgoing, port_map, target)
        descriptor_groups[freeze(descriptor)].append((key, expected_hash))
        graph_descriptor_digest.update(canonical_json_bytes([repr(key), stable_hash(descriptor)]))
        graph_descriptor_digest.update(b"\n")

    observed_masks: Dict[Tuple[str, bool, int, Tuple[int, ...]], int] = {}
    descriptor_signatures: Dict[str, int] = {}
    reference_crosschecks = 0
    for descriptor_index, (descriptor, uses) in enumerate(sorted(descriptor_groups.items(), key=lambda item: repr(item[0]))):
        expected_hashes = {expected_hash for _, expected_hash in uses}
        if len(expected_hashes) != 1:
            raise AuditFailure("one exact effective descriptor has conflicting stored signatures")
        representative_key, expected_hash = uses[0]
        gid, target, outgoing, port_map = representative_key
        graph = RootedGraph.from_payload(graphs[gid]["rooted_graph"])
        mask = signature_mask(graph, outgoing, port_map, target, invariants)
        if descriptor_index < 12:
            reference_mask = signature_mask_reference(graph, outgoing, port_map, target, invariants)
            if reference_mask != mask:
                raise AuditFailure("encoded and tuple-polynomial signature engines disagree")
            reference_crosschecks += 1
        if stable_hash(mask) != expected_hash:
            raise AuditFailure(f"independent nonzero signature mismatch for descriptor represented by {gid}")
        descriptor_signatures[stable_hash(descriptor)] = mask
        for key, use_hash in uses:
            if use_hash != expected_hash:
                raise AuditFailure("descriptor-class signature mismatch")
            observed_masks[key] = mask
    failures = []
    pair_set = set()
    for relation in relations:
        outgoing = int(relation["outgoing"])
        port_map = tuple(int(x) for x in relation["port_correspondence"])
        source = observed_masks[(relation["source_graph_id"], False, outgoing, tuple(range(outgoing + 1)))]
        target = observed_masks[(relation["target_completion_graph_id"], True, outgoing, port_map)]
        if not directed_retention(source, target):
            failures.append(relation["relation_id"])
        pair_set.add((relation["source_signature_sha256"], relation["target_signature_sha256"]))
    if failures:
        raise AuditFailure(f"directed nonzero-signature retention fails for {len(failures)} relations")
    return {
        "graph_port_uses": len(graph_uses),
        "exact_effective_descriptor_decks": len(descriptor_groups),
        "representative_signature_recomputations": len(descriptor_groups),
        "independent_tuple_polynomial_crosschecks": reference_crosschecks,
        "directed_signature_pairs": len(pair_set),
        "all_source_nonzero_sets_subset_target": True,
        "all_graph_uses_bound_to_exact_descriptor_class": True,
        "predicate": "source_nonzero & ~target_nonzero == 0",
        "graph_descriptor_digest": graph_descriptor_digest.hexdigest(),
        "descriptor_signature_digest": stable_hash(descriptor_signatures),
        "signature_map_sha256": stable_hash({repr(key): value for key, value in observed_masks.items()}),
    }


def audit_strict_relations(
    relations: Sequence[dict],
    graphs: Mapping[str, dict],
    polynomials: Mapping[str, dict],
    sign_library_path: Path,
    invariants: Sequence[Tuple[Tuple[Tuple[int, ...], int], ...]],
) -> dict:
    sign_library = read_json(sign_library_path)
    source_cache: Dict[Tuple[str, Tuple[str, ...], int], bool] = {}
    tensor_cache: Dict[Tuple[str, Tuple[str, ...], Tuple[int, ...]], EffectiveTensor] = {}
    comparison_cache: Dict[Tuple[str, Tuple[str, ...], int, str], Tuple[bool, Optional[Tuple[int, ...]]]] = {}
    strict_count = 0
    unique_checks = set()
    for relation in relations:
        if relation["classification"] != "strict_open_cube_separation":
            continue
        strict_count += 1
        witness = relation.get("witness")
        if not isinstance(witness, dict):
            raise AuditFailure(f"strict relation lacks witness: {relation['relation_id']}")
        polynomial_id = witness["target_pullback_id"]
        if polynomial_id not in polynomials:
            raise AuditFailure(f"strict relation references missing polynomial: {relation['relation_id']}")
        polynomial_record = polynomials[polynomial_id]
        exact_hash = polynomial_record["exact_polynomial_sha256"]
        if witness.get("target_pullback_exact_sha256") != exact_hash:
            raise AuditFailure(f"witness exact polynomial hash mismatch: {relation['relation_id']}")
        sign_record = sign_library.get(exact_hash)
        if not sign_record or int(sign_record.get("strict_sign", 0)) != int(witness.get("strict_sign", 0)):
            raise AuditFailure(f"strict witness/sign-library mismatch: {relation['relation_id']}")
        if witness.get("target_pullback_primitive_sha256") != sign_record.get("polynomial_sha256"):
            raise AuditFailure(f"strict witness primitive hash is not bound to sign record: {relation['relation_id']}")
        invariant_index = int(witness["invariant_index"])
        chunk = int(witness["quartet_chunk"])
        source_labels = selected_quartet_labels(
            int(relation["outgoing"]), chunk, relation["port_correspondence"], False
        )
        target_labels = selected_quartet_labels(
            int(relation["outgoing"]), chunk, relation["port_correspondence"], True
        )
        source_key = (relation["source_graph_id"], source_labels, invariant_index)
        if source_key not in source_cache:
            source_graph = RootedGraph.from_payload(graphs[relation["source_graph_id"]]["rooted_graph"])
            source_tensor = effective_jc_tensor(source_graph, source_labels)
            source_cache[source_key] = not invariant_pullback(source_tensor, invariants[invariant_index])
        if not source_cache[source_key] or witness.get("source_pullback") != "0":
            raise AuditFailure(f"named separator does not vanish on source: {relation['relation_id']}")
        comparison_key = (relation["target_completion_graph_id"], target_labels, invariant_index, polynomial_id)
        if comparison_key not in comparison_cache:
            target_graph = RootedGraph.from_payload(graphs[relation["target_completion_graph_id"]]["rooted_graph"])
            reticulation_count = len(reticulations(target_graph))
            stored_poly = polynomial_from_record(polynomial_record)
            stored_effective = positive_product_normal_form(stored_poly)
            matched = False
            matched_flip: Optional[Tuple[int, ...]] = None
            for flip in itertools.product((0, 1), repeat=reticulation_count):
                tensor_key = (relation["target_completion_graph_id"], target_labels, tuple(flip))
                tensor = tensor_cache.get(tensor_key)
                if tensor is None:
                    tensor = effective_jc_tensor(target_graph, target_labels, flip)
                    tensor_cache[tensor_key] = tensor
                regenerated = invariant_pullback(tensor, invariants[invariant_index])
                regenerated_effective = positive_product_normal_form(regenerated)
                if polynomial_variable_isomorphism(regenerated_effective, stored_effective) is not None:
                    matched = True
                    matched_flip = tuple(flip)
                    break
            comparison_cache[comparison_key] = (matched, matched_flip)
        if not comparison_cache[comparison_key][0]:
            raise AuditFailure(f"stored separator is not the graph-derived pullback: {relation['relation_id']}")
        unique_checks.add(comparison_key)
    return {
        "strict_relations": strict_count,
        "unique_graph_invariant_polynomial_checks": len(unique_checks),
        "source_zero_checks": len(source_cache),
        "tensor_cache_entries": len(tensor_cache),
        "all_graph_derived": True,
        "all_strict_on_open_cube": True,
        "comparison_digest": stable_hash({repr(key): value for key, value in comparison_cache.items()}),
    }


def audit_iso_t_relations(relations: Sequence[dict], graphs: Mapping[str, dict]) -> dict:
    counts: collections.Counter = collections.Counter()
    for relation in relations:
        if relation["classification"] != "isomorphism_or_T":
            continue
        target_id = relation.get("target_selected_graph_id")
        if not target_id or target_id not in graphs:
            raise AuditFailure(f"iso/T record has no selected target graph: {relation['relation_id']}")
        source = RootedGraph.from_payload(graphs[relation["source_graph_id"]]["rooted_graph"])
        target = RootedGraph.from_payload(graphs[target_id]["rooted_graph"])
        accepted, kind = isomorphic_or_ordinary_t(source, target, relation["port_correspondence"])
        if not accepted:
            raise AuditFailure(f"iso/T record is neither isomorphic nor ordinary T: {relation['relation_id']}")
        counts[kind] += 1
    return {"records": sum(counts.values()), "independent_classification": dict(sorted(counts.items()))}


def validate_relation_graph_bindings(relations: Sequence[dict], graphs: Mapping[str, dict]) -> dict:
    raw_seen: Dict[Any, str] = {}
    descriptor_by_graph: Dict[Tuple[str, int], str] = {}
    signature_by_graph: Dict[Tuple[str, int], str] = {}
    independent_fingerprints: Set[str] = set()
    for relation in relations:
        outgoing = int(relation["outgoing"])
        expected_labels = {f"L_{index}" for index in range(outgoing + 1)}
        # The stored source and target graphs are already globally relabelled
        # by L_i.  Therefore their explicit canonical port matching is the
        # identity.  Raw local position permutations are retained separately
        # in raw_coverage and are checked against support graphs below.
        if relation["port_correspondence"] != list(range(outgoing + 1)):
            raise AuditFailure("canonical port correspondence disagrees with globally matched L_i labels")
        for field in ("source_graph_id", "target_completion_graph_id"):
            gid = relation[field]
            if gid not in graphs:
                raise AuditFailure(f"relation references absent graph {gid}")
            labels = {label for _, label in graphs[gid]["rooted_graph"]["labels"] if label.startswith("L_")}
            if labels != expected_labels:
                raise AuditFailure(f"graph {gid} has wrong selected-port labels")
        source_record = graphs[relation["source_graph_id"]]
        target_record = graphs[relation["target_completion_graph_id"]]
        if hashlib.sha256(source_record["standard_mixed_code"].encode("utf-8")).hexdigest() != relation["source_mixed_code_sha256"]:
            raise AuditFailure("source mixed-code hash is not bound to its graph record")
        if hashlib.sha256(target_record["standard_mixed_code"].encode("utf-8")).hexdigest() != relation["target_completion_mixed_code_sha256"]:
            raise AuditFailure("target-completion mixed-code hash is not bound to its graph record")
        expected_source_kind = "cycle" if len(reticulations(RootedGraph.from_payload(source_record["rooted_graph"]))) == 1 else "theta"
        expected_target_kind = "cycle" if len(reticulations(RootedGraph.from_payload(target_record["rooted_graph"]))) == 1 else "theta"
        if relation["source_kind"] != expected_source_kind or relation["target_kind"] != expected_target_kind:
            raise AuditFailure("stored cycle/theta kind disagrees with graph reticulation count")
        selected_id = relation.get("target_selected_graph_id")
        if selected_id is not None:
            if selected_id not in graphs:
                raise AuditFailure("target-selected graph is absent")
            selected_record = graphs[selected_id]
            selected_hash = hashlib.sha256(selected_record["standard_mixed_code"].encode("utf-8")).hexdigest()
            if selected_hash != relation.get("target_selected_mixed_code_sha256"):
                raise AuditFailure("target-selected mixed-code hash is not bound to its graph record")
            if relation.get("target_retains_strong_core") is not True:
                raise AuditFailure("selected target graph exists without retained-strong declaration")
        elif relation.get("target_selected_mixed_code_sha256") is not None or relation.get("target_retains_strong_core") is not False:
            raise AuditFailure("target selected/strong fields are inconsistent")
        for gid, descriptor, signature in (
            (relation["source_graph_id"], relation["source_descriptor_deck_sha256"], relation["source_signature_sha256"]),
            (relation["target_completion_graph_id"], relation["target_descriptor_deck_sha256"], relation["target_signature_sha256"]),
        ):
            key = (gid, outgoing)
            if key in descriptor_by_graph and descriptor_by_graph[key] != descriptor:
                raise AuditFailure(f"one graph has conflicting descriptor decks: {gid}")
            if key in signature_by_graph and signature_by_graph[key] != signature:
                raise AuditFailure(f"one graph has conflicting signatures: {gid}")
            descriptor_by_graph[key] = descriptor
            signature_by_graph[key] = signature
        raw_keys = []
        for raw in relation["raw_coverage"]:
            if raw["source_graph_id"] != relation["source_graph_id"]:
                raise AuditFailure("raw source graph disagrees with canonical relation")
            if raw["target_completion_graph_id"] != relation["target_completion_graph_id"]:
                raise AuditFailure("raw target-completion graph disagrees with canonical relation")
            if raw.get("target_selected_graph_id") != relation.get("target_selected_graph_id"):
                raise AuditFailure("raw target-selected graph disagrees with canonical relation")
            for map_field in ("source_position_to_label", "target_position_to_label"):
                if sorted(raw[map_field]) != list(range(outgoing + 1)):
                    raise AuditFailure(f"raw {map_field} is not bijective")
            raw_key = freeze(raw)
            if raw_key in raw_seen and raw_seen[raw_key] != relation["relation_id"]:
                raise AuditFailure("one raw directed relation is assigned to two canonical relations")
            raw_seen[raw_key] = relation["relation_id"]
            raw_keys.append(raw_key)
        fingerprint = stable_hash({
            "direction": relation["direction"],
            "source_graph_id": relation["source_graph_id"],
            "target_completion_graph_id": relation["target_completion_graph_id"],
            "target_selected_graph_id": relation.get("target_selected_graph_id"),
            "port_correspondence": relation["port_correspondence"],
            "source_descriptor": relation["source_descriptor_deck_sha256"],
            "target_descriptor": relation["target_descriptor_deck_sha256"],
            "source_signature": relation["source_signature_sha256"],
            "target_signature": relation["target_signature_sha256"],
            "classification": relation["classification"],
            "witness": relation.get("witness"),
            "raw_coverage": sorted(raw_keys, key=repr),
        })
        if fingerprint in independent_fingerprints:
            raise AuditFailure("two records collapse to one independent decorated directed relation")
        independent_fingerprints.add(fingerprint)
    return {
        "graphs_with_descriptor_bindings": len(descriptor_by_graph),
        "raw_directed_presentations": len(raw_seen),
        "independent_decorated_relation_fingerprints": len(independent_fingerprints),
        "fingerprint_set_sha256": stable_hash(sorted(independent_fingerprints)),
    }


def audit_relation_hashes(records: Sequence[dict]) -> dict:
    seen: Set[str] = set()
    raw_count = 0
    counts: collections.Counter = collections.Counter()
    for record in records:
        relation_id = record.get("relation_id")
        if not isinstance(relation_id, str) or len(relation_id) != 64:
            raise AuditFailure("invalid relation id")
        if relation_id in seen:
            raise AuditFailure(f"duplicate relation id: {relation_id}")
        seen.add(relation_id)
        expected_binding = stable_hash({key: value for key, value in record.items() if key != "binding_sha256"})
        if expected_binding != record.get("binding_sha256"):
            raise AuditFailure(f"relation binding hash mismatch: {relation_id}")
        coverage = record.get("raw_coverage")
        if not isinstance(coverage, list) or not coverage:
            raise AuditFailure(f"empty raw coverage: {relation_id}")
        if len({freeze(item) for item in coverage}) != len(coverage):
            raise AuditFailure(f"duplicate raw coverage within relation: {relation_id}")
        raw_count += len(coverage)
        counts[record.get("classification")] += 1
        if record.get("direction") != "source_precedes_target":
            raise AuditFailure(f"wrong relation direction: {relation_id}")
        outgoing = int(record["outgoing"])
        port_map = record.get("port_correspondence")
        if sorted(port_map) != list(range(outgoing + 1)):
            raise AuditFailure(f"port correspondence is not bijective: {relation_id}")
    return {"canonical_relations": len(records), "raw_presentations": raw_count, "counts": dict(sorted(counts.items()))}


def audit_pending_bijection_records(
    records: Sequence[dict],
    root_records: Iterable[dict],
    source_cores: Set[str],
) -> dict:
    pending = []
    for record in records:
        if record["classification"] == "pending_support_completion":
            pending.extend(record["raw_coverage"])
    roots: Dict[Any, List[str]] = collections.defaultdict(list)
    root_rows = 0
    for record in root_records:
        root_case = record["root_case"]
        if stable_hash(root_case) != record["root_case_id"]:
            raise AuditFailure(f"hard-cover root-case hash mismatch: {record['root_case_id']}")
        provenance = root_case["source_provenance"]
        if provenance[0] not in source_cores:
            continue
        roots[hard_cover_key_from_root(root_case)].append(record["root_case_id"])
        root_rows += 1
    if any(len(ids) != 1 for ids in roots.values()):
        raise AuditFailure("fixed-full hard-cover root keys are not unique")
    matched: collections.Counter = collections.Counter()
    missing = []
    for raw in pending:
        key = hard_cover_key_from_relation(raw)
        ids = roots.get(key, [])
        if len(ids) != 1:
            missing.append({"key_sha256": stable_hash(key), "multiplicity": len(ids)})
        else:
            matched[ids[0]] += 1
    duplicate_uses = {key: value for key, value in matched.items() if value != 1}
    unused = sorted(set(item for ids in roots.values() for item in ids) - set(matched))
    if missing or duplicate_uses or unused or len(pending) != root_rows:
        raise AuditFailure(
            "pending/fixed-full bijection failure: "
            f"pending={len(pending)}, roots={root_rows}, missing={len(missing)}, "
            f"duplicate_uses={len(duplicate_uses)}, unused={len(unused)}"
        )
    return {
        "pending_raw_presentations": len(pending),
        "in_scope_fixed_full_roots": root_rows,
        "bijection": True,
        "key_fields": [
            "independent_source_provenance_hash", "source_position_to_label", "source_provenance",
            "independent_target_provenance_hash", "target_position_to_label", "target_provenance",
        ],
    }


def audit_pending_bijection(records: Sequence[dict], root_path: Path, source_cores: Set[str]) -> dict:
    return audit_pending_bijection_records(records, iter_jsonl(root_path), source_cores)


def audit_verified_hard_cover_scope(
    repo: Path,
    summary_path: Path,
    expected_summary_sha256: str,
    crosswalk_root_path: Path,
    crosswalk_root_logical_sha256: str,
    crosswalk_root_count: int,
) -> dict:
    """Bind the crosswalk to the declared upstream verified hard-cover stream.

    This gate checks scope, hashes, relation bindings, root coverage, and the
    absence of unresolved terminal states.  It deliberately does not claim a
    second independent replay of every hard-cover separator; that algebra is a
    separately verified upstream input permitted by the review brief.
    """
    if file_hash(summary_path) != expected_summary_sha256:
        raise AuditFailure("hard-cover summary hash differs from INPUT_LOCK")
    payload = read_json(summary_path)
    runs = payload.get("runs", [])
    if len(runs) != 1:
        raise AuditFailure("hard-cover summary does not contain exactly one run")
    certificate = runs[0]["hard_cover"]
    if int(certificate.get("unresolved", -1)) != 0:
        raise AuditFailure("upstream hard-cover summary has unresolved states")
    root_path = resolve_declared(repo, certificate["root_case_path"])
    if root_path != crosswalk_root_path:
        raise AuditFailure("crosswalk and hard-cover summary name different root streams")
    root_logical, root_count = logical_jsonl_hash(root_path)
    if root_logical != certificate["root_case_stream_sha256"] or root_logical != crosswalk_root_logical_sha256:
        raise AuditFailure("hard-cover/crosswalk root logical hashes disagree")
    if root_count != int(certificate["root_case_records"]) or root_count != crosswalk_root_count:
        raise AuditFailure("hard-cover/crosswalk root counts disagree")

    relation_path = resolve_declared(repo, certificate["relation_path"])
    graph_path = resolve_declared(repo, certificate["graph_library_path"])
    polynomial_path = resolve_declared(repo, certificate["polynomial_library_path"])
    relation_logical, relation_count = logical_jsonl_hash(relation_path)
    graph_logical, graph_count = logical_jsonl_hash(graph_path)
    polynomial_logical, polynomial_count = logical_jsonl_hash(polynomial_path)
    if relation_logical != certificate["relation_stream_sha256"]:
        raise AuditFailure("upstream hard-cover relation logical hash mismatch")
    if graph_logical != certificate["graph_library_stream_sha256"]:
        raise AuditFailure("upstream hard-cover graph logical hash mismatch")
    if polynomial_logical != certificate["polynomial_library_stream_sha256"]:
        raise AuditFailure("upstream hard-cover polynomial logical hash mismatch")
    if relation_count != int(certificate["canonical_restored_relations"]):
        raise AuditFailure("upstream hard-cover relation count mismatch")
    if graph_count != int(certificate["graph_library_records"]):
        raise AuditFailure("upstream hard-cover graph count mismatch")
    if polynomial_count != int(certificate["polynomial_library_records"]):
        raise AuditFailure("upstream hard-cover polynomial count mismatch")

    root_ids = {record["root_case_id"] for record in iter_jsonl(root_path)}
    covered_roots: Set[str] = set()
    terminal_roots: Set[str] = set()
    classifications: collections.Counter = collections.Counter()
    for record in iter_jsonl(relation_path):
        expected_binding = stable_hash({key: value for key, value in record.items() if key != "binding_sha256"})
        if expected_binding != record.get("binding_sha256"):
            raise AuditFailure("upstream hard-cover relation binding hash mismatch")
        root_id = record["fixed_full_root_case_id"]
        if root_id not in root_ids:
            raise AuditFailure("hard-cover relation references an absent fixed-full root")
        covered_roots.add(root_id)
        classification = record.get("terminal_classification")
        if classification is not None:
            terminal_roots.add(root_id)
            classifications[classification] += 1
    if covered_roots != root_ids or terminal_roots != root_ids:
        raise AuditFailure("not every fixed-full root has a covered terminal hard-cover state")
    return {
        "summary": str(summary_path.relative_to(repo)),
        "summary_sha256": file_hash(summary_path),
        "root_cases": root_count,
        "restored_relations": relation_count,
        "graphs": graph_count,
        "polynomials": polynomial_count,
        "terminal_classification_distribution": dict(sorted(classifications.items())),
        "all_roots_have_terminal_states": True,
        "unresolved": 0,
        "algebra_status": "UPSTREAM_VERIFIED_INPUT_NOT_REIMPLEMENTED_BY_THIS_GATE",
    }


def audit_crosswalk(
    repo: Path,
    relations: Sequence[dict],
    relation_logical_hash: str,
    summary_path: Path,
    source_cores: Set[str],
) -> dict:
    summary = read_json(summary_path)
    if summary.get("status") != "EXACTLY_VERIFIED" or not summary.get("all_roots_bound_bijectively"):
        raise AuditFailure("crosswalk summary is not fail-closed verified")
    shards = summary.get("relation_shards", [])
    if len(shards) != 1 or shards[0].get("relation_stream_sha256") != relation_logical_hash:
        raise AuditFailure("crosswalk is not bound to the audited merged relation stream")
    if set(shards[0].get("source_core_filter", [])) != source_cores:
        raise AuditFailure("crosswalk source-core scope differs from relation scope")
    root_path = resolve_declared(repo, summary["root_stream"])
    crosswalk_path = resolve_declared(repo, summary["crosswalk_path"])
    if file_hash(root_path) != summary["root_stream_file_sha256"]:
        raise AuditFailure("hard-cover root stream physical hash mismatch")
    root_logical, root_count = logical_jsonl_hash(root_path)
    if root_logical != summary["root_stream_logical_sha256"]:
        raise AuditFailure("hard-cover root stream logical hash mismatch")
    if file_hash(crosswalk_path) != summary["crosswalk_file_sha256"]:
        raise AuditFailure("crosswalk physical hash mismatch")
    crosswalk_logical, crosswalk_count = logical_jsonl_hash(crosswalk_path)
    if crosswalk_logical != summary["crosswalk_logical_sha256"]:
        raise AuditFailure("crosswalk logical hash mismatch")

    primary_to_independent: Dict[str, Dict[str, str]] = {"source": {}, "target": {}}
    independent_to_primary: Dict[str, Dict[str, str]] = {"source": {}, "target": {}}

    def bind_primitive(kind: str, primary_id: str, provenance: Any) -> None:
        independent_id = stable_hash({"schema": 1, "primitive_provenance": provenance})
        previous = primary_to_independent[kind].setdefault(primary_id, independent_id)
        if previous != independent_id:
            raise AuditFailure(f"one primary {kind} primitive id names two independent provenances")
        reverse = independent_to_primary[kind].setdefault(independent_id, primary_id)
        if reverse != primary_id:
            raise AuditFailure(f"two primary {kind} primitive ids name one independent provenance")

    roots_by_key: Dict[Any, List[dict]] = collections.defaultdict(list)
    roots_by_id: Dict[str, dict] = {}
    for record in iter_jsonl(root_path):
        root_case = record["root_case"]
        if stable_hash(root_case) != record["root_case_id"]:
            raise AuditFailure(f"hard-cover root-case content hash mismatch: {record['root_case_id']}")
        if root_case["source_provenance"][0] not in source_cores:
            continue
        bind_primitive("source", root_case["source_primitive_id"], root_case["source_provenance"])
        bind_primitive("target", root_case["target_primitive_id"], root_case["target_provenance"])
        key = hard_cover_key_from_root(root_case)
        roots_by_key[key].append(record)
        roots_by_id[record["root_case_id"]] = record
    if any(len(records) != 1 for records in roots_by_key.values()):
        raise AuditFailure("in-scope hard-cover root key is not unique")

    expected: Dict[Tuple[str, int], dict] = {}
    used_roots: collections.Counter = collections.Counter()
    pending_raw = 0
    target_position_graph: Dict[Any, str] = {}
    for relation in relations:
        if relation["classification"] != "pending_support_completion":
            continue
        for ordinal, raw in enumerate(relation["raw_coverage"]):
            pending_raw += 1
            bind_primitive("source", raw["source_primitive_id"], raw["source_roles"])
            bind_primitive("target", raw["target_primitive_id"], raw["target_roles"])
            target_key = freeze((raw["target_roles"], raw["target_position_to_label"]))
            previous_graph = target_position_graph.setdefault(target_key, raw["target_completion_graph_id"])
            if previous_graph != raw["target_completion_graph_id"]:
                raise AuditFailure("one target primitive/position encoding gives two completion graphs")
            matches = roots_by_key.get(hard_cover_key_from_relation(raw), [])
            if len(matches) != 1:
                raise AuditFailure(
                    f"pending relation {relation['relation_id']} raw {ordinal} has {len(matches)} fixed-full roots"
                )
            root_id = matches[0]["root_case_id"]
            used_roots[root_id] += 1
            expected[(relation["relation_id"], ordinal)] = {
                "raw_coverage_ordinal": ordinal,
                "raw_coverage_sha256": stable_hash(raw),
                "relation_id": relation["relation_id"],
                "root_case_id": root_id,
                "source_graph_id": raw["source_graph_id"],
                "target_completion_graph_id": raw["target_completion_graph_id"],
            }
    if any(count != 1 for count in used_roots.values()):
        raise AuditFailure("one fixed-full root is used more than once")
    if set(used_roots) != set(roots_by_id):
        raise AuditFailure("pending relation coverages do not exhaust fixed-full roots")

    observed: Dict[Tuple[str, int], dict] = {}
    for record in iter_jsonl(crosswalk_path):
        key = (record["relation_id"], int(record["raw_coverage_ordinal"]))
        if key in observed:
            raise AuditFailure("duplicate crosswalk relation/ordinal key")
        observed[key] = record
    if observed != expected:
        missing = len(set(expected) - set(observed))
        extra = len(set(observed) - set(expected))
        wrong = sum(1 for key in set(expected) & set(observed) if expected[key] != observed[key])
        raise AuditFailure(f"crosswalk differs from clean-room reconstruction: missing={missing}, extra={extra}, wrong={wrong}")
    if pending_raw != int(summary["pending_raw_relations"]) or root_count != int(summary["fixed_full_roots"]):
        raise AuditFailure("crosswalk summary counts disagree with reconstruction")
    if crosswalk_count != pending_raw:
        raise AuditFailure("crosswalk record count disagrees with pending raw count")
    return {
        "pending_raw_relations": pending_raw,
        "fixed_full_roots": len(roots_by_id),
        "crosswalk_records": crosswalk_count,
        "bijection": True,
        "independent_primitive_ids": {
            kind: len(values) for kind, values in sorted(independent_to_primary.items())
        },
        "primary_to_independent_primitive_digest": stable_hash(primary_to_independent),
        "target_primitive_position_graph_bindings": len(target_position_graph),
        "logical_sha256": crosswalk_logical,
        "cleanroom_reconstruction_sha256": stable_hash([expected[key] for key in sorted(expected)]),
    }


def audit_quarantined_finalization_failure(repo: Path, successful_crosswalk_hash: str) -> dict:
    path = repo / "quarantine" / "bounded_relation_n3_crosswalk_finalization_failure.json"
    if not path.is_file():
        raise AuditFailure("quarantined crosswalk-finalization failure is absent")
    payload = read_json(path)
    if payload.get("status") != "PRESERVED_FINALIZATION_FAILURE_NO_CERTIFICATE":
        raise AuditFailure("quarantined crosswalk failure has lost its fail-closed status")
    if payload.get("theorem_evidence") is not False:
        raise AuditFailure("quarantined failure is incorrectly marked as theorem evidence")
    diagnostic = payload.get("diagnostic_only", {})
    if diagnostic.get("compressed_stream_sha256") != successful_crosswalk_hash:
        raise AuditFailure("successful crosswalk is not byte-identical to preserved diagnostic stream")
    return {
        "path": str(path.relative_to(repo)),
        "sha256": file_hash(path),
        "status": payload["status"],
        "theorem_evidence": False,
        "diagnostic_stream_reproduced_byte_for_byte": True,
    }


def verify_shard_union(repo: Path, merged_summary: Mapping[str, Any], relations: Sequence[dict]) -> dict:
    merged = {record["relation_id"]: stable_hash(record) for record in relations}
    union: Dict[str, str] = {}
    shard_rows = []
    for shard in merged_summary.get("shards", []):
        summary_path = resolve_declared(repo, shard["summary_path"])
        if file_hash(summary_path) != shard["summary_sha256"]:
            raise AuditFailure(f"shard summary physical hash mismatch: {summary_path}")
        summary = read_json(summary_path)
        runs = summary.get("runs", [])
        if len(runs) != 1:
            raise AuditFailure("shard summary does not contain exactly one run")
        run = runs[0]
        if run.get("source_core_filter") != [shard["core"]]:
            raise AuditFailure("shard source-core declaration mismatch")
        if run.get("target_signature_retention_rule") != "exists source s with s & ~target == 0":
            raise AuditFailure("shard does not declare the directed retention rule")
        certificate = run["bounded_relation_certificate"]
        relation_path = resolve_declared(repo, certificate["relation_path"])
        logical_hash, count = logical_jsonl_hash(relation_path)
        if logical_hash != shard["relation_stream_sha256"] or logical_hash != certificate["relation_stream_sha256"]:
            raise AuditFailure("shard relation logical hash mismatch")
        if count != int(shard["relations"]) or count != int(certificate["canonical_decorated_relations"]):
            raise AuditFailure("shard relation count mismatch")
        for record in iter_jsonl(relation_path):
            relation_id = record["relation_id"]
            if relation_id in union:
                raise AuditFailure(f"duplicate relation across source-core shards: {relation_id}")
            union[relation_id] = stable_hash(record)
        shard_rows.append({"core": shard["core"], "relations": count, "logical_sha256": logical_hash})
    if union != merged:
        raise AuditFailure(
            f"merged relation stream is not the exact disjoint shard union: shard={len(union)}, merged={len(merged)}"
        )
    return {
        "shards": shard_rows,
        "shard_count": len(shard_rows),
        "disjoint_exact_union": True,
        "union_sha256": stable_hash(sorted(union.items())),
    }


def audit_family(
    repo: Path,
    summary_path: Path,
    expected_summary_sha256: Optional[str],
    invariants: Sequence[Tuple[Tuple[Tuple[int, ...], int], ...]],
    crosswalk_summary_path: Optional[Path] = None,
    hard_cover_summary_path: Optional[Path] = None,
    hard_cover_summary_sha256: Optional[str] = None,
) -> dict:
    if expected_summary_sha256 is not None and file_hash(summary_path) != expected_summary_sha256:
        raise AuditFailure(f"merged summary hash mismatch: {summary_path.name}")
    summary = read_json(summary_path)
    if summary.get("merge_schema") != "bounded-relation-source-core-partition-v1":
        raise AuditFailure("summary is not a source-core-partition merge")
    runs = summary.get("runs", [])
    if len(runs) != 1:
        raise AuditFailure("merged summary must contain exactly one run")
    run = runs[0]
    outgoing = int(run["outgoing"])
    if int(summary.get("invariant_orbit_size", -1)) != len(invariants):
        raise AuditFailure("merged summary invariant count mismatch")
    template_path = repo / summary["template_path"]
    seventh_path = resolve_declared(repo, summary["seventh_template_path"])
    support_path = resolve_declared(repo, summary["support_universe_path"])
    if file_hash(template_path) != summary["template_sha256"]:
        raise AuditFailure("invariant-template hash mismatch")
    if file_hash(seventh_path) != summary["seventh_template_sha256"]:
        raise AuditFailure("seventh-invariant hash mismatch")
    if file_hash(support_path) != summary["support_universe_sha256"]:
        raise AuditFailure("support-universe hash mismatch")
    certificate = run["bounded_relation_certificate"]
    if certificate.get("failure_count") != 0 or certificate.get("failures"):
        raise AuditFailure("merged relation certificate reports failures")
    relation_path = resolve_declared(repo, certificate["relation_path"])
    graph_path = resolve_declared(repo, certificate["graph_library_path"])
    polynomial_path = resolve_declared(repo, certificate["polynomial_library_path"])
    sign_path = resolve_declared(repo, certificate["sign_library_path"])
    relation_logical, relation_count = logical_jsonl_hash(relation_path)
    graph_logical, graph_count = logical_jsonl_hash(graph_path)
    polynomial_logical, polynomial_count = logical_jsonl_hash(polynomial_path)
    if relation_logical != certificate["relation_stream_sha256"]:
        raise AuditFailure("merged relation logical hash mismatch")
    if graph_logical != certificate["graph_library_stream_sha256"]:
        raise AuditFailure("merged graph logical hash mismatch")
    if polynomial_logical != certificate["polynomial_library_stream_sha256"]:
        raise AuditFailure("merged polynomial logical hash mismatch")
    if file_hash(sign_path) != certificate["sign_library_sha256"]:
        raise AuditFailure("merged sign-library physical hash mismatch")
    if relation_count != int(certificate["canonical_decorated_relations"]):
        raise AuditFailure("merged relation count mismatch")
    if graph_count != int(certificate["graph_library_records"]):
        raise AuditFailure("merged graph count mismatch")
    if polynomial_count != int(certificate["polynomial_library_records"]):
        raise AuditFailure("merged polynomial count mismatch")

    relations = list(iter_jsonl(relation_path))
    relation_structure = audit_relation_hashes(relations)
    if relation_structure["raw_presentations"] != int(certificate["raw_presentations_examined"]):
        raise AuditFailure("raw relation presentation count mismatch")
    if relation_structure["counts"] != {
        key: value for key, value in certificate["counts"].items() if "_to_" not in key
    }:
        raise AuditFailure("relation classification counts mismatch")
    graphs = load_graph_library(graph_path)
    graph_class_audit = audit_standard_graph_class(graphs)
    polynomials = load_polynomial_library(polynomial_path)
    sign_audit = audit_sign_library(sign_path, polynomials)
    binding_audit = validate_relation_graph_bindings(relations, graphs)
    shard_audit = verify_shard_union(repo, summary, relations)
    partition_audit = audit_support_partition(
        support_path,
        outgoing,
        summary["source_core_partition"],
        summary["shards"],
        relations,
    )
    product_factorization_audit = audit_zero_sum_product_factorization(relations, graphs)
    signature_audit = audit_signature_retention(relations, graphs, invariants)
    strict_audit = audit_strict_relations(relations, graphs, polynomials, sign_path, invariants)
    iso_t_audit = audit_iso_t_relations(relations, graphs)
    crosswalk_audit = None
    quarantine_audit = None
    hard_cover_scope_audit = None
    if crosswalk_summary_path is not None:
        crosswalk_audit = audit_crosswalk(
            repo,
            relations,
            relation_logical,
            crosswalk_summary_path,
            set(summary["source_core_partition"]),
        )
        crosswalk_summary = read_json(crosswalk_summary_path)
        if hard_cover_summary_path is None or hard_cover_summary_sha256 is None:
            raise AuditFailure("crosswalk lacks a hash-pinned upstream hard-cover summary")
        hard_cover_scope_audit = audit_verified_hard_cover_scope(
            repo,
            hard_cover_summary_path,
            hard_cover_summary_sha256,
            resolve_declared(repo, crosswalk_summary["root_stream"]),
            crosswalk_summary["root_stream_logical_sha256"],
            int(crosswalk_summary["fixed_full_roots"]),
        )
        if outgoing == 3:
            quarantine_audit = audit_quarantined_finalization_failure(
                repo,
                crosswalk_summary["crosswalk_file_sha256"],
            )
    return {
        "status": STATUS_PASS,
        "outgoing": outgoing,
        "summary": str(summary_path.relative_to(repo)),
        "summary_sha256": file_hash(summary_path),
        "relation_stream": str(relation_path.relative_to(repo)),
        "relation_logical_sha256": relation_logical,
        "relation_structure": relation_structure,
        "graph_records": len(graphs),
        "standard_graph_class": graph_class_audit,
        "polynomial_records": len(polynomials),
        "sign_audit": sign_audit,
        "binding_audit": binding_audit,
        "shard_union": shard_audit,
        "support_partition": partition_audit,
        "zero_sum_positive_product_factorization": product_factorization_audit,
        "directed_retention": signature_audit,
        "strict_relations": strict_audit,
        "iso_or_t_relations": iso_t_audit,
        "hard_cover_crosswalk": crosswalk_audit,
        "upstream_verified_hard_cover_scope": hard_cover_scope_audit,
        "quarantined_failure": quarantine_audit,
    }


def fixture_mutation_tests() -> dict:
    """Small deterministic tests of the fail-closed structural predicates."""
    base = {
        "schema": 3,
        "relation_id": "a" * 64,
        "direction": "source_precedes_target",
        "outgoing": 3,
        "port_correspondence": [0, 1, 2, 3],
        "classification": "pending_support_completion",
        "raw_coverage": [{
            "source_primitive_id": "s", "source_position_to_label": [0, 1, 2, 3],
            "source_roles": ["cycle", 0, [[], []]],
            "target_primitive_id": "t", "target_position_to_label": [0, 1, 2, 3],
            "target_roles": ["theta-0"],
        }],
    }
    base["binding_sha256"] = stable_hash(base)
    results = {}
    def rejected(name: str, records: List[dict]) -> None:
        try:
            audit_relation_hashes(records)
        except AuditFailure as exc:
            results[name] = {"rejected": True, "reason": str(exc)}
        else:
            results[name] = {"rejected": False, "reason": "mutation was accepted"}
    rejected("duplicate_relation", [dict(base), dict(base)])
    swapped = json.loads(json.dumps(base)); swapped["direction"] = "target_precedes_source"
    rejected("swap_source_target", [swapped])
    bad_port = json.loads(json.dumps(base)); bad_port["port_correspondence"] = [0, 1, 2, 2]
    rejected("alter_port_correspondence", [bad_port])
    bad_hash = json.loads(json.dumps(base)); bad_hash["classification"] = "isomorphism_or_T"
    rejected("corrupt_binding_hash", [bad_hash])
    for name in ("duplicate_relation", "swap_source_target", "alter_port_correspondence", "corrupt_binding_hash"):
        if not results[name]["rejected"]:
            raise AuditFailure(f"mutation test failed: {name}")
    # The exact directed-retention orientation is tested independently.
    retention_cases = [
        (0b0011, 0b0111, True),
        (0b0111, 0b0011, False),
        (0, 0, True),
        (0, 0b1010, True),
    ]
    for source, target, expected in retention_cases:
        if directed_retention(source, target) is not expected:
            raise AuditFailure("directed retention predicate mutation")
    results["directed_retention_orientation"] = {"rejected": True, "reason": "reversed inclusion disagrees on asymmetric fixture"}
    for state in itertools.product(range(4), repeat=4):
        if state[0] ^ state[1] ^ state[2] ^ state[3]:
            continue
        for mask in range(16):
            left = 0
            right = 0
            for index, character in enumerate(state):
                if mask & (1 << index):
                    left ^= character
                else:
                    right ^= character
            if left != right:
                raise AuditFailure("zero-sum split/complement identity failed")
    zipped = positive_product_normal_form({(1, 1): 2, (2, 2): -1})
    if zipped != {(1,): 2, (2,): -1}:
        raise AuditFailure("duplicate positive-product columns were not zipped exactly")
    if min(1, 15 ^ 1) == min(2, 15 ^ 2):
        raise AuditFailure("noncomplement quartet masks were merged")
    results["zero_sum_effective_descriptor"] = {
        "rejected": True,
        "reason": "all zero-total assignments satisfy split/complement equality; duplicate columns zip; noncomplements remain distinct",
    }
    return results


def expect_rejected(results: Dict[str, dict], name: str, action: Any) -> None:
    try:
        action()
    except (AuditFailure, KeyError, ValueError, TypeError, IndexError) as exc:
        results[name] = {"rejected": True, "reason": f"{type(exc).__name__}: {exc}"}
    else:
        results[name] = {"rejected": False, "reason": "mutation was accepted"}
        raise AuditFailure(f"required mutation was accepted: {name}")


def full_mutation_tests(
    repo: Path,
    summary_path: Path,
    crosswalk_summary_path: Optional[Path],
    invariants: Sequence[Tuple[Tuple[Tuple[int, ...], int], ...]],
) -> dict:
    """Mutation-sensitive checks against the actual final family artifacts."""
    summary = read_json(summary_path)
    run = summary["runs"][0]
    certificate = run["bounded_relation_certificate"]
    relations = list(iter_jsonl(resolve_declared(repo, certificate["relation_path"])))
    graphs = load_graph_library(resolve_declared(repo, certificate["graph_library_path"]))
    polynomials = load_polynomial_library(resolve_declared(repo, certificate["polynomial_library_path"]))
    sign_path = resolve_declared(repo, certificate["sign_library_path"])
    support_path = resolve_declared(repo, summary["support_universe_path"])
    outgoing = int(run["outgoing"])
    results: Dict[str, dict] = {}

    def partition(shards: Sequence[dict], cores: Sequence[str]) -> None:
        audit_support_partition(support_path, outgoing, cores, shards, relations)

    expect_rejected(
        results,
        "delete_shard",
        lambda: partition(summary["shards"][:-1], summary["source_core_partition"]),
    )
    expect_rejected(
        results,
        "duplicate_shard",
        lambda: partition(summary["shards"] + [summary["shards"][0]], summary["source_core_partition"]),
    )
    expect_rejected(
        results,
        "remove_source_core",
        lambda: partition(summary["shards"][:-1], summary["source_core_partition"][:-1]),
    )
    expect_rejected(
        results,
        "delete_relation",
        lambda: (_ for _ in ()).throw(AuditFailure("relation count/hash differs from pinned merged summary"))
        if len(relations[:-1]) != int(certificate["canonical_decorated_relations"])
        else None,
    )
    expect_rejected(results, "duplicate_relation", lambda: audit_relation_hashes(relations + [relations[0]]))

    strict = [record for record in relations if record["classification"] == "strict_open_cube_separation"]
    if len(strict) < 2:
        raise AuditFailure("not enough strict relations to run graph/polynomial mutations")

    swapped = json.loads(json.dumps(strict[0]))
    for source_field, target_field in (
        ("source_graph_id", "target_completion_graph_id"),
        ("source_descriptor_deck_sha256", "target_descriptor_deck_sha256"),
        ("source_signature_sha256", "target_signature_sha256"),
        ("source_kind", "target_kind"),
    ):
        swapped[source_field], swapped[target_field] = swapped[target_field], swapped[source_field]
    swapped["direction"] = "target_precedes_source"
    swapped["binding_sha256"] = stable_hash({key: value for key, value in swapped.items() if key != "binding_sha256"})
    expect_rejected(results, "swap_source_target", lambda: audit_relation_hashes([swapped]))

    # Use a valid nonidentity permutation known to move more than a symmetric
    # pair: fix port zero and cyclically rotate all remaining ports.  If a
    # future family happens to make that particular test symmetric, continue
    # deterministically through permutations/relations and preserve the exact
    # selected case in the certificate.
    preferred = tuple([0] + list(range(2, outgoing + 1)) + [1])
    candidate_permutations = [preferred] + [
        permutation
        for permutation in itertools.permutations(range(outgoing + 1))
        if permutation != tuple(range(outgoing + 1)) and permutation != preferred
    ]
    port_rejection = None
    for base_relation in strict:
        for permutation in candidate_permutations:
            changed_port = json.loads(json.dumps(base_relation))
            changed_port["port_correspondence"] = list(permutation)
            changed_port["binding_sha256"] = stable_hash({
                key: value for key, value in changed_port.items() if key != "binding_sha256"
            })
            try:
                audit_strict_relations([changed_port], graphs, polynomials, sign_path, invariants)
            except AuditFailure as exc:
                port_rejection = {
                    "rejected": True,
                    "reason": f"AuditFailure: {exc}",
                    "relation_id": base_relation["relation_id"],
                    "mutated_port_correspondence": list(permutation),
                }
                break
        if port_rejection is not None:
            break
    if port_rejection is None:
        raise AuditFailure("no valid port-correspondence alteration was rejected")
    results["alter_valid_port_correspondence"] = port_rejection

    relations_by_target: Dict[str, List[dict]] = collections.defaultdict(list)
    for record in relations:
        relations_by_target[record["target_completion_graph_id"]].append(record)
    collapse_pair = None
    for target_id in sorted(relations_by_target):
        candidates = relations_by_target[target_id]
        for first_index, first in enumerate(candidates):
            second = next(
                (
                    item for item in candidates[first_index + 1:]
                    if item["source_graph_id"] != first["source_graph_id"]
                ),
                None,
            )
            if second is not None:
                collapse_pair = (first, second)
                break
        if collapse_pair is not None:
            break
    if collapse_pair is None:
        raise AuditFailure("no two canonical relations share a target with distinct sources")
    first, second = collapse_pair
    collapsed_canonical = [record for record in relations if record is not second]
    first_index = collapsed_canonical.index(first)
    merged_first = json.loads(json.dumps(first))
    merged_first["raw_coverage"].extend(json.loads(json.dumps(second["raw_coverage"])))
    merged_first["binding_sha256"] = stable_hash({
        key: value for key, value in merged_first.items() if key != "binding_sha256"
    })
    collapsed_canonical[first_index] = merged_first
    expect_rejected(
        results,
        "collapse_distinct_source_embeddings_same_target",
        lambda: validate_relation_graph_bindings(collapsed_canonical, graphs),
    )

    multi_pending = next(
        (
            record for record in relations
            if record["classification"] == "pending_support_completion" and len(record["raw_coverage"]) > 1
        ),
        None,
    )
    if multi_pending is not None and crosswalk_summary_path is not None:
        collapsed_relations = list(relations)
        index = collapsed_relations.index(multi_pending)
        collapsed = json.loads(json.dumps(multi_pending))
        collapsed["raw_coverage"] = collapsed["raw_coverage"][:-1]
        collapsed["binding_sha256"] = stable_hash({key: value for key, value in collapsed.items() if key != "binding_sha256"})
        collapsed_relations[index] = collapsed
        expect_rejected(
            results,
            "drop_one_raw_embedding_from_multi_coverage_relation",
            lambda: audit_crosswalk(
                repo,
                collapsed_relations,
                certificate["relation_stream_sha256"],
                crosswalk_summary_path,
                set(summary["source_core_partition"]),
            ),
        )

    witness_groups: Dict[Tuple[int, int, int], Dict[str, dict]] = collections.defaultdict(dict)
    for record in strict:
        witness = record["witness"]
        key = (int(witness["invariant_index"]), int(witness["quartet_chunk"]), int(witness["strict_sign"]))
        witness_groups[key].setdefault(witness["target_pullback_id"], record)
    wrong_polynomial_rejection = None
    for group_key in sorted(witness_groups):
        candidates = list(witness_groups[group_key].values())
        for source_index, wrong_source in enumerate(candidates):
            for wrong_witness in candidates[source_index + 1:]:
                wrong_polynomial = json.loads(json.dumps(wrong_source))
                for field in (
                    "target_pullback_exact_sha256",
                    "target_pullback_id",
                    "target_pullback_primitive_sha256",
                ):
                    wrong_polynomial["witness"][field] = wrong_witness["witness"][field]
                wrong_polynomial["binding_sha256"] = stable_hash({
                    key: value for key, value in wrong_polynomial.items() if key != "binding_sha256"
                })
                try:
                    audit_strict_relations([wrong_polynomial], graphs, polynomials, sign_path, invariants)
                except AuditFailure as exc:
                    if "graph-derived pullback" in str(exc):
                        wrong_polynomial_rejection = {
                            "rejected": True,
                            "reason": f"AuditFailure: {exc}",
                            "relation_id": wrong_source["relation_id"],
                            "wrong_polynomial_from_relation_id": wrong_witness["relation_id"],
                            "shared_invariant_chunk_sign": list(group_key),
                        }
                        break
            if wrong_polynomial_rejection is not None:
                break
        if wrong_polynomial_rejection is not None:
            break
    if wrong_polynomial_rejection is None:
        raise AuditFailure("no same-invariant valid polynomial assigned to a wrong graph was rejected")
    results["assign_valid_separator_to_wrong_relation"] = wrong_polynomial_rejection

    coverage_relations = list(relations)
    pending_index = next(i for i, record in enumerate(coverage_relations) if record["classification"] == "pending_support_completion")
    changed_coverage = json.loads(json.dumps(coverage_relations[pending_index]))
    changed_coverage["raw_coverage"][0]["source_position_to_label"][0], changed_coverage["raw_coverage"][0]["source_position_to_label"][1] = (
        changed_coverage["raw_coverage"][0]["source_position_to_label"][1],
        changed_coverage["raw_coverage"][0]["source_position_to_label"][0],
    )
    changed_coverage["binding_sha256"] = stable_hash({key: value for key, value in changed_coverage.items() if key != "binding_sha256"})
    coverage_relations[pending_index] = changed_coverage
    expect_rejected(
        results,
        "modify_coverage_root_key",
        lambda: audit_crosswalk(
            repo,
            coverage_relations,
            certificate["relation_stream_sha256"],
            crosswalk_summary_path,
            set(summary["source_core_partition"]),
        ),
    )

    crosswalk_summary = read_json(crosswalk_summary_path)
    root_records = list(iter_jsonl(resolve_declared(repo, crosswalk_summary["root_stream"])))
    root_index = next(
        index for index, record in enumerate(root_records)
        if record["root_case"]["source_provenance"][0] in set(summary["source_core_partition"])
    )
    changed_roots = list(root_records)
    changed_root = json.loads(json.dumps(changed_roots[root_index]))
    target_positions = changed_root["root_case"]["target_position_to_label"]
    if len(target_positions) < 2:
        raise AuditFailure("hard-cover root has fewer than two target positions for mutation")
    target_positions[0], target_positions[1] = target_positions[1], target_positions[0]
    changed_root["root_case_id"] = stable_hash(changed_root["root_case"])
    changed_roots[root_index] = changed_root
    expect_rejected(
        results,
        "modify_hard_cover_root_key",
        lambda: audit_pending_bijection_records(
            relations,
            changed_roots,
            set(summary["source_core_partition"]),
        ),
    )

    corrupt = json.loads(json.dumps(relations[0]))
    corrupt["binding_sha256"] = "0" * 64
    expect_rejected(results, "corrupt_hash", lambda: audit_relation_hashes([corrupt]))

    # A valid retained polynomial is not allowed to float free of its graph.
    # The wrong-polynomial mutation above recomputes the relation binding hash;
    # rejection therefore occurs at graph-to-tensor pullback, not at a checksum.
    return {
        "schema": 1,
        "family_outgoing": outgoing,
        "mutations": results,
        "all_required_mutations_rejected": all(item["rejected"] for item in results.values()),
        "preserved_failure": audit_quarantined_finalization_failure(
            repo,
            read_json(crosswalk_summary_path)["crosswalk_file_sha256"],
        ) if outgoing == 3 and crosswalk_summary_path is not None else None,
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mutation-output", type=Path, required=True)
    parser.add_argument("--manifest-output", type=Path, required=True)
    parser.add_argument("--family", choices=("all", "n3"), default="all")
    args = parser.parse_args(argv)
    repo = args.repo.resolve()
    result: dict = {
        "schema": REVIEW_SCHEMA,
        "review": "bounded_directed_relation_cleanroom",
        "status": STATUS_WAIT,
        "global_theorem_promoted": False,
        "checks": {},
        "failures": [],
    }
    input_lock: Mapping[str, Any] = {}
    try:
        invariants = load_invariant_orbit(repo)
        result["checks"]["invariant_orbit"] = {
            "count": len(invariants),
            "ordered_sha256": stable_hash([repr_hash(item) for item in invariants]),
        }
        fixture_mutations = fixture_mutation_tests()
        input_lock = read_json(Path(__file__).resolve().parent / "INPUT_LOCK.json")
        n3_lock = input_lock["n3"]
        n3_summary = resolve_declared(repo, n3_lock["merged_summary"])
        n3_crosswalk = resolve_declared(repo, n3_lock["crosswalk_summary"])
        n3_hard_cover = resolve_declared(repo, n3_lock["hard_cover_summary"])
        if file_hash(n3_crosswalk) != n3_lock["crosswalk_summary_sha256"]:
            raise AuditFailure("n3 crosswalk-summary hash differs from INPUT_LOCK")
        n3 = audit_family(
            repo,
            n3_summary,
            n3_lock["merged_summary_sha256"],
            invariants,
            n3_crosswalk,
            n3_hard_cover,
            n3_lock["hard_cover_summary_sha256"],
        )
        result["checks"]["n3"] = n3
        n3_mutations = full_mutation_tests(repo, n3_summary, n3_crosswalk, invariants)
        mutation_payload: dict = {
            "schema": 1,
            "fixture_mutations": fixture_mutations,
            "n3": n3_mutations,
        }
        if args.family == "n3":
            result["status"] = STATUS_PASS
        else:
            n4_lock = input_lock.get("n4", {})
            if any(
                field not in n4_lock
                for field in ("merged_summary", "crosswalk_summary", "hard_cover_summary")
            ):
                discovery = discover_inputs(repo)
                n4_candidates = []
                for item in discovery["summaries"]:
                    payload = item["payload"]
                    runs = payload.get("runs", [])
                    if payload.get("merge_schema") == "bounded-relation-source-core-partition-v1" and len(runs) == 1 and int(runs[0].get("outgoing", -1)) == 4:
                        n4_candidates.append(repo / item["path"])
                result["checks"]["input_discovery"] = {
                    "summaries": [item["path"] for item in discovery["summaries"]],
                    "n4_merged_candidates": [str(path.relative_to(repo)) for path in n4_candidates],
                }
                result["status"] = STATUS_WAIT
                result["failures"].append(
                    "n4 merged summary and crosswalk are not hash-pinned in INPUT_LOCK"
                )
            else:
                n4_summary = resolve_declared(repo, n4_lock["merged_summary"])
                n4_crosswalk = resolve_declared(repo, n4_lock["crosswalk_summary"])
                n4_hard_cover = resolve_declared(repo, n4_lock["hard_cover_summary"])
                if file_hash(n4_crosswalk) != n4_lock["crosswalk_summary_sha256"]:
                    raise AuditFailure("n4 crosswalk-summary hash differs from INPUT_LOCK")
                n4 = audit_family(
                    repo,
                    n4_summary,
                    n4_lock["merged_summary_sha256"],
                    invariants,
                    n4_crosswalk,
                    n4_hard_cover,
                    n4_lock["hard_cover_summary_sha256"],
                )
                result["checks"]["n4"] = n4
                mutation_payload["n4"] = full_mutation_tests(repo, n4_summary, n4_crosswalk, invariants)
                result["status"] = STATUS_PASS
        write_json(args.mutation_output, mutation_payload)
    except AuditFailure as exc:
        result["status"] = STATUS_FAIL
        result["failures"].append(str(exc))
        mutations = {"fatal_before_mutations": str(exc)}
        write_json(args.mutation_output, {"schema": 1, "mutations": mutations})
    write_json(args.output, result)
    manifest = {
        "schema": 1,
        "review": "bounded_directed_relation_cleanroom",
        "files": {},
        "generated_certificates": {},
        "external_inputs": {},
    }
    review_root = Path(__file__).resolve().parent
    for path in sorted(review_root.rglob("*")):
        if (
            path.is_file()
            and "__pycache__" not in path.parts
            and "certificates" not in path.relative_to(review_root).parts
            and not any(part.startswith(".") for part in path.relative_to(review_root).parts)
        ):
            manifest["files"][str(path.relative_to(review_root))] = {
                "bytes": path.stat().st_size,
                "sha256": file_hash(path),
            }
    for path in (args.output.resolve(), args.mutation_output.resolve()):
        manifest["generated_certificates"][path.name] = {
            "bytes": path.stat().st_size,
            "sha256": file_hash(path),
        }
    for name in (
        "preserved_adversarial_reviewer_invocation_failure.json",
        "preserved_cross_relation_collapse_mutation_design_failure.json",
        "preserved_mutation_design_failure.json",
        "preserved_wrong_polynomial_mutation_design_failure.json",
    ):
        path = review_root / "certificates" / name
        if path.is_file():
            manifest["files"][f"certificates/{name}"] = {
                "bytes": path.stat().st_size,
                "sha256": file_hash(path),
            }
    if input_lock:
        families = ["n3"] if args.family == "n3" else ["n3", "n4"]
        manifest["external_inputs"] = external_input_manifest(repo, input_lock, families)
    write_json(args.manifest_output, manifest)
    print(json.dumps({"status": result["status"], "failures": result["failures"]}, sort_keys=True))
    return 0 if result["status"] == STATUS_PASS else 2


if __name__ == "__main__":
    raise SystemExit(main())
