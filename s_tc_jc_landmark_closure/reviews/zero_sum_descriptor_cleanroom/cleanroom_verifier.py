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
    templates = parse_literal(TEMPLATE_FILE, "INVARIANT_TEMPLATES")
    seventh_payload = json.loads(SEVENTH_FILE.read_text())
    seventh = tuple(
        (tuple(int(index) + 1 for index in monomial), int(coefficient))
        for coefficient, monomial in seventh_payload["invariant"]
    )
    invariants = invariant_orbit((*templates, seventh))
    require(len(invariants) == 84, "invariant orbit did not have 84 members")
    return invariants


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

    start = jc.index("def all_port_quartet_deck(")
    end = jc.index("\n\n@lru_cache", start)
    all_port_body = jc[start:end]
    require("0b1111" not in all_port_body, "all_port_quartet_deck complement-normalizes")
    require("min(new_mask" not in all_port_body, "all_port_quartet_deck complement-normalizes")

    return {
        "schema": "source-inspection-v1",
        "status": "VERIFIED",
        "method": "text inspection only; no primary imports",
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


def split_math_certificate() -> dict:
    zero_sum_assignments = tuple(
        row for row in product(range(4), repeat=4) if row[0] ^ row[1] ^ row[2] ^ row[3] == 0
    )
    complement_failures = []
    for mask in range(16):
        complement = 15 ^ mask
        for assignment in zero_sum_assignments:
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
            for assignment in zero_sum_assignments:
                if xor_state(left, assignment) != xor_state(right, assignment):
                    witness = assignment
                    break
            require(witness is not None, f"noncomplement masks merged: {left}, {right}")
            separating_assignments[f"{left},{right}"] = list(witness)

    return {
        "schema": "zero-sum-split-math-v1",
        "status": "VERIFIED",
        "group": "JC Fourier characters represented as xor in Z2^2",
        "zero_sum_assignment_count": len(zero_sum_assignments),
        "canonical_representative_count": len(JC_REPS),
        "complement_identity_checked_masks": 16,
        "quotient_classes": {
            str(rep): masks for rep, masks in sorted(quotient_classes.items())
        },
        "noncomplement_pairs_separated": len(separating_assignments),
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


def atlas_submersion_certificate() -> dict:
    internal = internal_root_fixture()
    pendant = pendant_root_fixture()
    for graph in (internal, pendant):
        valid, problems = validate_rooted_graph(graph)
        require(valid and not problems, f"invalid root-relocation fixture: {problems}")
    raw_internal = quartet_deck(internal, 4, normalize=False)[0]
    raw_pendant = quartet_deck(pendant, 4, normalize=False)[0]
    norm_internal = quartet_deck(internal, 4, normalize=True)[0]
    norm_pendant = quartet_deck(pendant, 4, normalize=True)[0]
    require(raw_internal != raw_pendant, "rooted raw descriptors unexpectedly agree")
    require(norm_internal == norm_pendant, "normalized root-relocation descriptors differ")

    product_checks = []
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
        product_checks.append(
            {
                "presentation": name,
                "raw_descriptor": descriptor_json(raw_desc),
                "normalized_descriptor": descriptor_json(mapped_norm),
                "normalized_variable_to_raw_variables": [list(row) for row in mapping],
            }
        )

    # This is a symbolic open-cube sanity check for the product submersion:
    # q(z)=z(1-z) is strictly positive on 0<z<1, and q(xy)=xy(1-xy)
    # is strictly positive on 0<x,y<1.  Boundary points are rejected elsewhere.
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
        },
        "product_factorization_checks": product_checks,
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
            found[graph_id] = {
                "line_index_zero_based": line_index,
                "line_number_one_based": line_index + 1,
                "graph_id": graph_id,
                "standard_mixed_code_sha256": row["standard_mixed_code_sha256"],
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
        "same_mixed_code_sha256": MIXED_SHA,
        "selected_port_count": 6,
        "quartet_chunk": 5,
        "quartet_positions_for_chunk": list(tuple(combinations(range(6), 4))[5]),
        "invariant_index": 50,
        "invariant_term_count": len(invariants[50]),
        "graphs": {
            graph_id: {
                key: value
                for key, value in found[graph_id].items()
                if key != "rooted_graph"
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
                    if xor_state(left, assignment) != xor_state(right, assignment):
                        raise VerificationError(
                            "bad map merges noncomplement masks "
                            f"{left} and {right}, separated by {assignment}"
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

    mutations = [
        assert_mutation_rejected("omit_complement_normalization", omit_complement),
        assert_mutation_rejected("normalize_at_width_5_instead_of_quartet_width_4", wrong_width),
        assert_mutation_rejected("merge_noncomplement_masks", merge_noncomplements),
        assert_mutation_rejected("use_boundary_x_0_or_x_1", boundary_samples),
        assert_mutation_rejected("reuse_polynomial_from_wrong_graph", wrong_graph_polynomial_reuse),
    ]
    return {
        "schema": "zero-sum-cleanroom-mutations-v1",
        "status": "VERIFIED",
        "all_mutations_rejected": True,
        "mutations": mutations,
    }


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")


def build_certificates(certificate_dir: Path) -> dict:
    source = inspect_sources()
    split_math = split_math_certificate()
    atlas = atlas_submersion_certificate()
    invariants = load_invariants()
    quarantine = quarantine_regression_certificate(invariants)
    mutations = mutation_certificate(quarantine)

    certificates = {
        "source_inspection_certificate.json": source,
        "split_complement_math_certificate.json": split_math,
        "bounded_atlas_submersion_certificate.json": atlas,
        "quarantine_regression_certificate.json": quarantine,
        "mutation_certificate.json": mutations,
    }
    for filename, payload in certificates.items():
        write_json(certificate_dir / filename, payload)

    manifest_entries = []
    for filename in sorted(certificates):
        path = certificate_dir / filename
        manifest_entries.append(
            {
                "path": str(path.relative_to(REVIEW_DIR)),
                "sha256": sha256_file(path),
            }
        )
    verifier_path = REVIEW_DIR / "cleanroom_verifier.py"
    verify_script = REVIEW_DIR / "verify_all.sh"
    review_path = REVIEW_DIR / "REVIEW.md"
    research_log_path = REVIEW_DIR / "RESEARCH_LOG.md"
    manifest = {
        "schema": "zero-sum-cleanroom-manifest-v1",
        "status": "VERIFIED",
        "standard_library_only": True,
        "imports_primary_or_reviews": False,
        "repo_relative_review_dir": str(REVIEW_DIR.relative_to(REPO)),
        "review_artifacts": [
            {
                "path": str(path.relative_to(REVIEW_DIR)),
                "sha256": sha256_file(path),
            }
            for path in (review_path, research_log_path)
        ],
        "verifier": {
            "path": str(verifier_path.relative_to(REVIEW_DIR)),
            "sha256": sha256_file(verifier_path),
        },
        "verify_script": (
            {
                "path": str(verify_script.relative_to(REVIEW_DIR)),
                "sha256": sha256_file(verify_script),
            }
            if verify_script.exists()
            else None
        ),
        "certificates": manifest_entries,
        "release_verdicts": {
            "hard_cover_graph_id_cache_plus_normalization": "release_safe",
            "bounded_atlas_unnormalized_rooted_convention": (
                "release_safe_for_graph_specific_zero_nonzero_strict_sign_classification; "
                "not a canonical semidirected quotient descriptor"
            ),
        },
    }
    write_json(certificate_dir / "manifest.json", manifest)
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate-dir",
        type=Path,
        default=REVIEW_DIR / "certificates",
    )
    args = parser.parse_args(argv)
    try:
        manifest = build_certificates(args.certificate_dir)
    except VerificationError as exc:
        print(f"VERIFICATION FAILED: {exc}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "status": "VERIFIED",
                "manifest": str((args.certificate_dir / "manifest.json").relative_to(REVIEW_DIR)),
                "certificate_count": len(manifest["certificates"]),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
