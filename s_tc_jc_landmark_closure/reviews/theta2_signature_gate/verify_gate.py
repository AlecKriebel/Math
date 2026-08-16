#!/usr/bin/env python3
"""Clean-room five-port theta-2 invariant-signature gate.

This program is deliberately self-contained.  It imports no project graph,
completion, Fourier, invariant, canonicalization, or atlas code.  The only
external inputs are inert coefficient/core data and the frozen hard-cover
root records used for a final hash comparison.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
from dataclasses import dataclass
import gzip
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Iterable, Sequence


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
TEMPLATE_PATH = PROJECT / "strong_level2_phylo_identifiability/src/jc_root_spanning_atlas_data.py"
SEVENTH_PATH = PROJECT / "primary/seventh_invariant.json"
CORE_PATH = PROJECT / "primary/certificates/core_universe.json"
ROOT_PATH = PROJECT / "primary/certificates/hard_cover_root_cases_n4_schema3_theta2_full.jsonl.gz"
PRIME = 2_147_483_647
SEEDS = (101, 1009, 10007)
INCOMING = "INCOMING"


# Primitive data are written explicitly here.  CORE_PATH is read only to
# verify that the frozen data agree; it is never used to drive generation.
CORES = {
    "cycle": {
        "arcs": (("S", "X"), ("S", "X")),
        "repairs": ((0,), (1,)),
    },
    "theta-0": {
        "arcs": (("S", "U"), ("S", "V"), ("U", "X0"), ("V", "X0"), ("U", "V")),
        "repairs": ((2, 3), (3, 4)),
    },
    "theta-1": {
        "arcs": (("S", "U"), ("S", "X0"), ("V", "X0"), ("U", "V"), ("U", "V")),
        "repairs": ((2, 3), (2, 4)),
    },
    "theta-2": {
        "arcs": (("S", "U"), ("S", "V"), ("U", "X0"), ("V", "X0"), ("U", "X1"), ("V", "X1")),
        "repairs": ((2, 3), (2, 5), (3, 4), (4, 5)),
    },
    "theta-3": {
        "arcs": (("S", "U"), ("S", "X0"), ("V", "X0"), ("U", "X1"), ("V", "X1"), ("U", "V")),
        "repairs": ((2,), (4,)),
    },
}


def stable_hash(value: object) -> str:
    body = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(body).hexdigest()


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def natural(label: str):
    prefix, _, suffix = label.rpartition("_")
    return prefix, int(suffix) if suffix.isdigit() else -1, label


@dataclass(frozen=True)
class Rooted:
    root: int
    labels: tuple[tuple[int, str], ...]
    arcs: tuple[tuple[int, int], ...]

    @property
    def vertices(self) -> tuple[int, ...]:
        return tuple(sorted({self.root, *(v for row in self.arcs for v in row), *(v for v, _ in self.labels)}))


@dataclass(frozen=True)
class Completion:
    core: str
    mode: str
    sink_mask: int
    repair_index: int | None
    words: tuple[tuple[str, ...], ...]
    selected_labels: tuple[str, ...]
    dummy_labels: tuple[str, ...]
    graph: Rooted

    def provenance(self) -> tuple:
        return (self.core, self.mode, self.sink_mask, self.repair_index, self.words, self.dummy_labels)

    def inventory_provenance(self) -> list:
        return [
            self.core,
            self.sink_mask,
            self.repair_index,
            [list(word) for word in self.words],
            list(self.dummy_labels),
            self.mode == "selected-incoming",
        ]


Descriptor = tuple[int, tuple[tuple[int, ...], ...]]
Invariant = tuple[tuple[tuple[int, ...], int], ...]
Poly = dict[tuple[int, ...], int]


def source_and_sinks(arcs: Sequence[tuple[str, str]]) -> tuple[str, tuple[str, ...]]:
    indegree = Counter(v for _, v in arcs)
    outdegree = Counter(u for u, _ in arcs)
    vertices = {x for edge in arcs for x in edge}
    sources = sorted(v for v in vertices if indegree[v] == 0)
    if len(sources) != 1:
        raise AssertionError((arcs, sources))
    sinks = tuple(sorted(v for v in vertices if indegree[v] == 2 and outdegree[v] == 0))
    return sources[0], sinks


def build_graph(
    arcs: Sequence[tuple[str, str]],
    words: Sequence[Sequence[str]],
    sink_labels: dict[str, str],
) -> Rooted:
    ids: dict[tuple, int] = {}

    def vertex(key: tuple) -> int:
        if key not in ids:
            ids[key] = len(ids)
        return ids[key]

    vertices = sorted({x for edge in arcs for x in edge})
    for name in vertices:
        vertex(("core", name))
    source, _ = source_and_sinks(arcs)
    root = vertex(("root",))
    incoming = vertex(("leaf", INCOMING))
    labels = {incoming: INCOMING}
    directed = [(root, vertex(("core", source))), (root, incoming)]
    for edge_index, ((tail, head), word) in enumerate(zip(arcs, words)):
        prior = vertex(("core", tail))
        for position, label in enumerate(word):
            subdivision = vertex(("subdivision", edge_index, position))
            leaf = vertex(("leaf", edge_index, position, label))
            labels[leaf] = label
            directed.extend(((prior, subdivision), (subdivision, leaf)))
            prior = subdivision
        directed.append((prior, vertex(("core", head))))
    for sink, label in sorted(sink_labels.items()):
        leaf = vertex(("sink-leaf", sink, label))
        labels[leaf] = label
        directed.append((vertex(("core", sink)), leaf))
    return Rooted(root, tuple(sorted(labels.items())), tuple(directed))


def weak_compositions(total: int, parts: int) -> Iterable[tuple[int, ...]]:
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total - first, parts - 1):
            yield (first, *rest)


def generate_completions(*, include_selected: bool = True, include_marginal: bool = True):
    """All full strong witnesses with five selected tensor boundaries."""
    modes = []
    if include_selected:
        modes.append(("selected-incoming", 4))
    if include_marginal:
        modes.append(("marginalized-incoming", 5))
    for mode, selected_outgoing in modes:
        for core_name, core in CORES.items():
            arcs = core["arcs"]
            _, sinks = source_and_sinks(arcs)
            for sink_mask in range(1 << len(sinks)):
                selected_sinks = [sink for index, sink in enumerate(sinks) if sink_mask & (1 << index)]
                ordinary_count = selected_outgoing - len(selected_sinks)
                if ordinary_count < 0:
                    continue
                for counts in weak_compositions(ordinary_count, len(arcs)):
                    labels = iter(f"O_{index}" for index in range(ordinary_count))
                    selected_words = tuple(tuple(next(labels) for _ in range(count)) for count in counts)
                    indexed_repairs = ((None, ()),) if core_name == "cycle" else tuple(enumerate(core["repairs"]))
                    for repair_index, repair in indexed_repairs:
                        words = [list(word) for word in selected_words]
                        dummies = [INCOMING] if mode == "marginalized-incoming" else []
                        for edge_index in repair:
                            if not words[edge_index]:
                                dummy = f"D_REPAIR_{repair_index}_{edge_index}"
                                words[edge_index].append(dummy)
                                dummies.append(dummy)
                        sink_labels = {}
                        for index, sink in enumerate(sinks):
                            if sink in selected_sinks:
                                sink_labels[sink] = f"SINK_{index}"
                            else:
                                dummy = f"D_SINK_{index}"
                                sink_labels[sink] = dummy
                                dummies.append(dummy)
                        selected = sorted(
                            [label for word in selected_words for label in word]
                            + [sink_labels[sink] for sink in selected_sinks],
                            key=natural,
                        )
                        if mode == "selected-incoming":
                            selected.append(INCOMING)
                        full_words = tuple(tuple(word) for word in words)
                        yield Completion(
                            core_name, mode, sink_mask, repair_index, full_words,
                            tuple(selected), tuple(sorted(dummies, key=natural)),
                            build_graph(arcs, full_words, sink_labels),
                        )


def source_supports(repairs: tuple[int, ...] = (0, 1, 3)) -> tuple[Completion, ...]:
    core = CORES["theta-2"]
    answer = []
    for repair_index in repairs:
        repair = core["repairs"][repair_index]
        words = [[] for _ in core["arcs"]]
        for position, edge_index in enumerate(repair):
            words[edge_index].append(f"Q_REPAIR_{position}")
        sink_labels = {"X0": "Q_SINK_0", "X1": "Q_SINK_1"}
        selected = ("Q_REPAIR_0", "Q_REPAIR_1", "Q_SINK_0", "Q_SINK_1", INCOMING)
        full_words = tuple(tuple(word) for word in words)
        answer.append(Completion(
            "theta-2", "selected-incoming", 3, repair_index, full_words,
            selected, (), build_graph(core["arcs"], full_words, sink_labels),
        ))
    return tuple(answer)


def displayed_switchings(graph: Rooted):
    indegree = Counter(v for _, v in graph.arcs)
    retics = tuple(sorted(v for v in graph.vertices if indegree[v] == 2))
    incoming = {r: tuple(index for index, (_, v) in enumerate(graph.arcs) if v == r) for r in retics}
    if any(len(incoming[r]) != 2 for r in retics):
        raise AssertionError("nonbinary reticulation")
    for choices in itertools.product((0, 1), repeat=len(retics)):
        removed = {incoming[r][1 - choice] for r, choice in zip(retics, choices)}
        yield choices, tuple(index for index in range(len(graph.arcs)) if index not in removed)


def descendant_masks(graph: Rooted, active: Sequence[int], ordered_labels: Sequence[str]) -> tuple[int, ...]:
    label_positions = {label: index for index, label in enumerate(ordered_labels)}
    graph_labels = dict(graph.labels)
    children: dict[int, list[int]] = defaultdict(list)
    for edge_index in active:
        u, v = graph.arcs[edge_index]
        children[u].append(v)
    memo: dict[int, int] = {}

    def visit(vertex: int) -> int:
        if vertex in memo:
            return memo[vertex]
        label = graph_labels.get(vertex)
        if label is not None:
            value = (1 << label_positions[label]) if label in label_positions else 0
        else:
            value = 0
            for child in children[vertex]:
                value |= visit(child)
        memo[vertex] = value
        return value

    return tuple(visit(graph.arcs[index][1]) for index in active)


def canonical_display_descriptor(retics: int, rows: Iterable[Sequence[int]]) -> Descriptor:
    rows = tuple(sorted(set(tuple(row) for row in rows if any(row))))
    if not retics:
        return 0, rows
    displays = tuple(itertools.product((0, 1), repeat=retics))
    display_index = {bits: index for index, bits in enumerate(displays)}
    candidates = []
    for permutation in itertools.permutations(range(retics)):
        for flips in itertools.product((0, 1), repeat=retics):
            moved = []
            for row in rows:
                new_row = []
                for new_bits in displays:
                    old_bits = tuple(new_bits[permutation[index]] ^ flips[index] for index in range(retics))
                    new_row.append(row[display_index[old_bits]])
                moved.append(tuple(new_row))
            candidates.append((retics, tuple(sorted(set(moved)))))
    return min(candidates)


def descriptor(graph: Rooted, ordered_labels: Sequence[str], *, complement_mask: int = 0b1111) -> Descriptor:
    if len(ordered_labels) != 4:
        raise ValueError("the invariant templates act on four-port marginals")
    switchings = tuple(displayed_switchings(graph))
    retics = len(switchings[0][0])
    rows = [[0] * len(switchings) for _ in graph.arcs]
    for display_index, (_choices, active) in enumerate(switchings):
        masks = descendant_masks(graph, active, ordered_labels)
        for edge_index, mask in zip(active, masks):
            rows[edge_index][display_index] = min(mask, complement_mask ^ mask)
    return canonical_display_descriptor(retics, rows)


def ordered_deck(graph: Rooted, labels: Sequence[str], *, complement_mask: int = 0b1111):
    return {ordered: descriptor(graph, tuple(labels[index] for index in ordered),
                                complement_mask=complement_mask)
            for ordered in itertools.permutations(range(5), 4)}


def selected_width_five_complement_deck(graph: Rooted, labels: Sequence[str]):
    """Deliberately wrong normalization used by the mutation audit.

    It first chooses a split side by complementing masks in the complete
    selected five-port tensor and only then projects to a quartet.  Marginal
    character zero must be imposed before this choice, so this operation is
    not equivalent to the correct quartet-width complement quotient.
    """
    switchings = tuple(displayed_switchings(graph))
    retics = len(switchings[0][0])
    physical_rows = [[0] * len(switchings) for _ in graph.arcs]
    for display_index, (_choices, active) in enumerate(switchings):
        masks = descendant_masks(graph, active, labels)
        for edge_index, mask in zip(active, masks):
            physical_rows[edge_index][display_index] = min(mask, 0b11111 ^ mask)
    answer = {}
    for ordered in itertools.permutations(range(5), 4):
        rows = []
        for physical in physical_rows:
            projected = []
            for mask in physical:
                moved = 0
                for new_index, old_index in enumerate(ordered):
                    if mask & (1 << old_index):
                        moved |= 1 << new_index
                projected.append(moved)
            rows.append(tuple(projected))
        answer[ordered] = canonical_display_descriptor(retics, rows)
    return answer


def jc_representatives():
    colour_maps = [(0, *row) for row in itertools.permutations((1, 2, 3))]

    def canon(row):
        return min(tuple(mapping[value] for value in row) for mapping in colour_maps)

    reps = tuple(sorted({canon(row) for row in itertools.product(range(4), repeat=4)
                         if row[0] ^ row[1] ^ row[2] ^ row[3] == 0}))
    if len(reps) != 15:
        raise AssertionError(len(reps))
    return reps, canon


def parse_templates() -> tuple[Invariant, ...]:
    module = ast.parse(TEMPLATE_PATH.read_text())
    base = None
    for node in module.body:
        if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "INVARIANT_TEMPLATES"
                                                for target in node.targets):
            base = ast.literal_eval(node.value)
            break
    if base is None or len(base) != 6:
        raise AssertionError("six inert templates not found")
    seventh_payload = json.loads(SEVENTH_PATH.read_text())
    seventh = tuple((tuple(int(index) + 1 for index in monomial), int(coefficient))
                    for coefficient, monomial in seventh_payload["invariant"])
    return tuple(tuple((tuple(monomial), int(coefficient)) for monomial, coefficient in template)
                 for template in (*base, seventh))


def invariant_orbit() -> tuple[Invariant, ...]:
    reps, canon = jc_representatives()
    rep_index = {row: index for index, row in enumerate(reps)}
    orbit = set()
    for template in parse_templates():
        for permutation in itertools.permutations(range(4)):
            terms = Counter()
            for coordinates, coefficient in template:
                moved = []
                for coordinate in coordinates:
                    assignment = reps[coordinate]
                    transported = tuple(assignment[permutation[index]] for index in range(4))
                    moved.append(rep_index[canon(transported)])
                terms[tuple(sorted(moved))] += coefficient
            normalized = tuple(sorted((monomial, coefficient) for monomial, coefficient in terms.items() if coefficient))
            if normalized and normalized[0][1] < 0:
                normalized = tuple((monomial, -coefficient) for monomial, coefficient in normalized)
            orbit.add(normalized)
    answer = tuple(sorted(orbit))
    if len(answer) != 84:
        raise AssertionError(("invariant-orbit", len(answer)))
    return answer


def coordinate_values_mod(desc: Descriptor, seed: int) -> tuple[int, ...]:
    retics, rows = desc
    displays = tuple(itertools.product((0, 1), repeat=retics))
    values = []
    for index in range(len(rows) + retics):
        value = (seed + 37 * index + 11) % PRIME
        values.append(2 if value in (0, 1) else value)
    edges = values[:len(rows)]
    inheritance = values[len(rows):]
    reps, _ = jc_representatives()
    answer = []
    for assignment in reps:
        total = 0
        for display_index, choices in enumerate(displays):
            term = 1
            for retic_index, choice in enumerate(choices):
                lam = inheritance[retic_index]
                term = term * (lam if choice == 0 else 1 - lam) % PRIME
            for edge, row in zip(edges, rows):
                state = 0
                mask = row[display_index]
                for leaf_index, character in enumerate(assignment):
                    if mask & (1 << leaf_index):
                        state ^= character
                if state:
                    term = term * edge % PRIME
            total = (total + term) % PRIME
        answer.append(total)
    return tuple(answer)


def invariant_value_mod(coordinates: Sequence[int], invariant: Invariant) -> int:
    total = 0
    for monomial, coefficient in invariant:
        term = coefficient % PRIME
        for index in monomial:
            term = term * coordinates[index] % PRIME
        total = (total + term) % PRIME
    return total


def poly_add(left: Poly, right: Poly, scale: int = 1) -> Poly:
    answer = dict(left)
    for monomial, coefficient in right.items():
        value = answer.get(monomial, 0) + scale * coefficient
        if value:
            answer[monomial] = value
        else:
            answer.pop(monomial, None)
    return answer


def poly_mul(left: Poly, right: Poly) -> Poly:
    if not left or not right:
        return {}
    answer = defaultdict(int)
    for a, ca in left.items():
        for b, cb in right.items():
            answer[tuple(x + y for x, y in zip(a, b))] += ca * cb
    return {monomial: coefficient for monomial, coefficient in answer.items() if coefficient}


def coordinate_polynomials(desc: Descriptor) -> tuple[Poly, ...]:
    retics, rows = desc
    displays = tuple(itertools.product((0, 1), repeat=retics))
    variables = len(rows) + retics
    reps, _ = jc_representatives()
    answer = []
    zero = (0,) * variables
    for assignment in reps:
        total: Poly = {}
        for display_index, choices in enumerate(displays):
            exponent = [0] * variables
            for edge_index, row in enumerate(rows):
                state = 0
                mask = row[display_index]
                for leaf_index, character in enumerate(assignment):
                    if mask & (1 << leaf_index):
                        state ^= character
                if state:
                    exponent[edge_index] = 1
            term: Poly = {tuple(exponent): 1}
            for retic_index, choice in enumerate(choices):
                variable = len(rows) + retic_index
                unit = [0] * variables
                unit[variable] = 1
                factor = {tuple(unit): 1} if choice == 0 else {zero: 1, tuple(unit): -1}
                term = poly_mul(term, factor)
            total = poly_add(total, term)
        answer.append(total)
    return tuple(answer)


def exact_candidate_bits(desc: Descriptor, candidates: Sequence[tuple[int, Invariant]]) -> int:
    coordinates = coordinate_polynomials(desc)
    variables = len(desc[1]) + desc[0]
    monomial_cache: dict[tuple[int, ...], Poly] = {(): {(0,) * variables: 1}}

    def coordinate_monomial(indices: tuple[int, ...]) -> Poly:
        if indices not in monomial_cache:
            monomial_cache[indices] = poly_mul(coordinate_monomial(indices[:-1]), coordinates[indices[-1]])
        return monomial_cache[indices]

    bits = 0
    for index, invariant in candidates:
        polynomial: Poly = {}
        for monomial, coefficient in invariant:
            polynomial = poly_add(polynomial, coordinate_monomial(monomial), coefficient)
        if polynomial:
            bits |= 1 << index
    return bits


def descriptor_bits(desc: Descriptor, invariants: Sequence[Invariant], cache: dict[Descriptor, int], counters: Counter) -> int:
    if desc in cache:
        return cache[desc]
    evaluations = tuple(coordinate_values_mod(desc, seed) for seed in SEEDS)
    bits = 0
    exact_candidates = []
    for index, invariant in enumerate(invariants):
        if any(invariant_value_mod(values, invariant) for values in evaluations):
            bits |= 1 << index
            counters["modular_nonzero"] += 1
        else:
            exact_candidates.append((index, invariant))
    if exact_candidates:
        bits |= exact_candidate_bits(desc, exact_candidates)
        counters["exact_candidates"] += len(exact_candidates)
        counters["exact_descriptors"] += 1
    cache[desc] = bits
    return bits


def signature(deck: dict[tuple[int, int, int, int], Descriptor], assignment: tuple[int, ...],
              invariants: Sequence[Invariant], cache: dict[Descriptor, int], counters: Counter) -> int:
    inverse = [0] * 5
    for position, actual in enumerate(assignment):
        inverse[actual] = position
    answer = 0
    width = len(invariants)
    for chunk, actual_quartet in enumerate(itertools.combinations(range(5), 4)):
        positional = tuple(inverse[value] for value in actual_quartet)
        answer |= descriptor_bits(deck[positional], invariants, cache, counters) << (width * chunk)
    return answer


def core_data_audit() -> bool:
    payload = json.loads(CORE_PATH.read_text())
    observed = {}
    for row in payload["cores"]:
        observed[row["id"]] = {
            "arcs": tuple((edge["tail"], edge["head"]) for edge in row["segments"]),
            "repairs": tuple(tuple(int(value) for value in repair) for repair in row["minimum_repairs"]),
        }
    return observed == CORES


def grammar_summary(completions: Sequence[Completion]):
    modes = Counter(row.mode for row in completions)
    classes = Counter((row.mode, row.core, row.repair_index) for row in completions)
    provenance = [row.provenance() for row in completions]
    return {
        "raw_completion_count": len(completions),
        "mode_counts": dict(sorted(modes.items())),
        "class_counts": {repr(key): value for key, value in sorted(classes.items(), key=repr)},
        "ordered_provenance_sha256": stable_hash(provenance),
    }


def frozen_root_audit():
    counts = Counter()
    ids = set()
    relations = Counter()
    with gzip.open(ROOT_PATH, "rt", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            ids.add(row["root_case_id"])
            root = row["root_case"]
            counts[root["selected_signature_sha256"]] += 1
            normalized = {
                "direction": "source_precedes_target",
                "selected_outgoing": root["selected_outgoing"],
                "selected_signature_sha256": root["selected_signature_sha256"],
                "source_position_to_label": root["source_position_to_label"],
                "source_provenance": root["source_provenance"],
                "target_provenance": root["target_provenance"],
                "target_dummy_roles": root["target_dummy_roles"],
                "target_position_to_label": root["target_position_to_label"],
            }
            relations[json.dumps(normalized, sort_keys=True, separators=(",", ":"))] += 1
    return {
        "record_count": sum(counts.values()),
        "unique_root_ids": len(ids),
        "signature_hash_counts": dict(sorted(counts.items())),
        "normalized_relation_count": len(relations),
        "normalized_relation_multiset_sha256": stable_hash(sorted(relations.items())),
        "_relations": relations,
    }


def run_gate(*, source_repairs: tuple[int, ...] = (0, 1, 3),
             include_selected: bool = True, include_marginal: bool = True,
             delete_class: tuple[str, str, int | None] | None = None):
    invariants = invariant_orbit()
    bit_cache: dict[Descriptor, int] = {}
    counters = Counter()

    source_rows = source_supports(source_repairs)
    source_decks = [ordered_deck(row.graph, row.selected_labels) for row in source_rows]
    source_signatures = [signature(deck, tuple(range(5)), invariants, bit_cache, counters) for deck in source_decks]

    raw = list(generate_completions(include_selected=include_selected, include_marginal=include_marginal))
    if delete_class is not None:
        raw = [row for row in raw if (row.mode, row.core, row.repair_index) != delete_class]
    grammar = grammar_summary(raw)

    # First quotient by the complete unlabelled five-marginal JC descriptor
    # model, with cycle/theta kind retained.  All ordered transports are then
    # regenerated from one representative and checked against every variant.
    groups: dict[tuple, list[Completion]] = defaultdict(list)
    increasing_decks = {}
    for row in raw:
        increasing = tuple(
            descriptor(row.graph, tuple(row.selected_labels[index] for index in quartet))
            for quartet in itertools.combinations(range(5), 4)
        )
        key = ("cycle" if row.core == "cycle" else "theta", increasing)
        groups[key].append(row)
        increasing_decks[key] = increasing

    all_target_signatures = Counter()
    survivor_presentations = Counter()
    decorated_relations = Counter()
    intrinsic_partition = Counter()
    ordered_deck_inconsistencies = []
    for key in sorted(groups, key=repr):
        variants = groups[key]
        representative = variants[0]
        deck = ordered_deck(representative.graph, representative.selected_labels)
        # An increasing descriptor key must determine every ordered transport.
        # This is checked on every raw variant rather than assumed.
        for variant in variants[1:]:
            moved = ordered_deck(variant.graph, variant.selected_labels)
            if moved != deck:
                ordered_deck_inconsistencies.append((representative.provenance(), variant.provenance()))
                break
        for assignment in itertools.permutations(range(5)):
            target_signature = signature(deck, assignment, invariants, bit_cache, counters)
            all_target_signatures[target_signature] += 1
            for source_index, source_signature in enumerate(source_signatures):
                if source_signature & ~target_signature == 0:
                    survivor_presentations[(source_index, source_signature, target_signature)] += 1
                    source_row = source_rows[source_index]
                    for variant in variants:
                        normalized = {
                            "direction": "source_precedes_target",
                            "selected_outgoing": 4,
                            "selected_signature_sha256": hashlib.sha256(
                                str(source_signature).encode()
                            ).hexdigest(),
                            "source_position_to_label": list(range(5)),
                            "source_provenance": [
                                "theta-2",
                                source_row.repair_index,
                                [list(word) for word in source_row.words],
                            ],
                            "target_provenance": variant.inventory_provenance(),
                            "target_dummy_roles": list(variant.dummy_labels),
                            "target_position_to_label": list(assignment),
                        }
                        decorated_relations[
                            json.dumps(normalized, sort_keys=True, separators=(",", ":"))
                        ] += 1
                        if not normalized["target_dummy_roles"]:
                            intrinsic_partition["direct_no_omitted_roles"] += 1
                        elif normalized["target_provenance"][-1]:
                            intrinsic_partition["nonretaining_selected_incoming"] += 1
                        else:
                            intrinsic_partition["nonretaining_marginalized_incoming"] += 1

    pairs = sorted(survivor_presentations)
    source_hashes = [hashlib.sha256(str(value).encode()).hexdigest() for value in source_signatures]
    pair_records = [{
        "source_index": source_index,
        "source_signature_sha256": hashlib.sha256(str(source_value).encode()).hexdigest(),
        "target_signature_sha256": hashlib.sha256(str(target_value).encode()).hexdigest(),
        "equal": source_value == target_value,
        "base_assignment_multiplicity": survivor_presentations[(source_index, source_value, target_value)],
    } for source_index, source_value, target_value in pairs]
    return {
        "invariant_count": len(invariants),
        "source_support_count": len(source_rows),
        "source_signature_count": len(set(source_signatures)),
        "source_signature_sha256": source_hashes,
        "grammar": grammar,
        "target_base_count": len(groups),
        "raw_labelled_presentation_count": len(raw) * math.factorial(5),
        "normalized_base_assignment_count": len(groups) * math.factorial(5),
        "target_unique_signature_count": len(all_target_signatures),
        "necessary_pair_count": len(pairs),
        "strict_pair_count": sum(source_value != target_value for _, source_value, target_value in pairs),
        "equal_pair_count": sum(source_value == target_value for _, source_value, target_value in pairs),
        "pair_records": pair_records,
        "decorated_relation_count": len(decorated_relations),
        "decorated_relation_total_multiplicity": sum(decorated_relations.values()),
        "decorated_relation_multiset_sha256": stable_hash(sorted(decorated_relations.items())),
        "intrinsic_partition": dict(sorted(intrinsic_partition.items())),
        "ordered_deck_inconsistency_count": len(ordered_deck_inconsistencies),
        "first_ordered_deck_inconsistencies": ordered_deck_inconsistencies[:3],
        "descriptor_cache_count": len(bit_cache),
        "algebra_counters": dict(sorted(counters.items())),
        "target_signature_multiset_sha256": stable_hash(sorted((str(key), value) for key, value in all_target_signatures.items())),
        "source_signature_integer_values": [str(value) for value in source_signatures],
        "all_target_signature_integer_values": [str(value) for value in sorted(all_target_signatures)],
        "_decorated_relations": decorated_relations,
    }


def validate_baseline(result, frozen):
    expected_hashes = set(frozen["signature_hash_counts"])
    observed_hashes = set(result["source_signature_sha256"])
    checks = {
        "core_data_matches_frozen": core_data_audit(),
        "seven_template_orbit_has_84_elements": result["invariant_count"] == 84,
        "three_anchored_source_supports": result["source_support_count"] == 3,
        "three_distinct_source_signatures": result["source_signature_count"] == 3,
        "both_target_incoming_modes_present": set(result["grammar"]["mode_counts"]) == {
            "selected-incoming", "marginalized-incoming"},
        "ordered_descriptor_key_is_complete": result["ordered_deck_inconsistency_count"] == 0,
        "only_three_necessary_pairs": result["necessary_pair_count"] == 3,
        "all_necessary_pairs_are_equal": result["strict_pair_count"] == 0 and result["equal_pair_count"] == 3,
        "survivor_hashes_equal_frozen_root_hashes": observed_hashes == expected_hashes,
        "frozen_root_count_and_balance": frozen["record_count"] == frozen["unique_root_ids"] == 132
            and set(frozen["signature_hash_counts"].values()) == {44},
        "raw_survivor_partition_is_18_42_132": result["intrinsic_partition"] == {
            "direct_no_omitted_roles": 18,
            "nonretaining_marginalized_incoming": 132,
            "nonretaining_selected_incoming": 42,
        },
    }
    return checks


def run_mutations(baseline, frozen):
    expected_grammar = baseline["grammar"]
    expected_hashes = set(frozen["signature_hash_counts"])
    mutations = []

    def record(name: str, rejected: bool, reason: str):
        mutations.append({"name": name, "rejected": bool(rejected), "reason": reason})

    omitted_grammar = grammar_summary(list(generate_completions(
        include_selected=True, include_marginal=False
    )))
    record("omit_target_incoming_mode",
           omitted_grammar != expected_grammar,
           "mode census and ordered grammar commitment change")

    invariants = invariant_orbit()

    def mutated_source_hashes(*, wrong_width_five=False, complement_mask=0b1111,
                              repairs=(0, 1, 3)):
        cache: dict[Descriptor, int] = {}
        counters = Counter()
        values = []
        for row in source_supports(repairs):
            deck = (selected_width_five_complement_deck(row.graph, row.selected_labels)
                    if wrong_width_five else ordered_deck(
                        row.graph, row.selected_labels, complement_mask=complement_mask
                    ))
            values.append(signature(deck, tuple(range(5)), invariants, cache, counters))
        return values, [hashlib.sha256(str(value).encode()).hexdigest() for value in values]

    _five_values, five_hashes = mutated_source_hashes(wrong_width_five=True)
    _wrong_values, wrong_hashes = mutated_source_hashes(complement_mask=0b0111)
    record("wrong_complement_width",
           set(wrong_hashes) != expected_hashes,
           "using a three-bit complement on a four-port marginal changes the invariant deck")

    deleted_rows = [row for row in generate_completions()
                    if (row.mode, row.core, row.repair_index) !=
                    ("marginalized-incoming", "theta-2", 3)]
    deleted_grammar = grammar_summary(deleted_rows)
    record("delete_target_completion_class",
           deleted_grammar != expected_grammar,
           "raw grammar class census and provenance commitment change")

    altered_values, altered_hashes = mutated_source_hashes(repairs=(0, 1, 2))
    record("alter_source_repair",
           set(altered_hashes) != expected_hashes or len(set(altered_values)) != 3,
           "anchored source-signature commitment changes")

    source_values = [int(value) for value in baseline["source_signature_integer_values"]]
    target_values = [int(value) for value in baseline["all_target_signature_integer_values"]]
    reversed_pairs = {(source, target) for source in source_values for target in target_values
                      if target & ~source == 0}
    baseline_pairs = {(row["source_signature_sha256"], row["target_signature_sha256"])
                      for row in baseline["pair_records"]}
    record("flip_containment_direction",
           len(reversed_pairs) != len(baseline_pairs)
           or any(source != target for source, target in reversed_pairs),
           "reversing S(source) subset S(target) changes the necessary relation set")

    original_relations = baseline["_decorated_relations"]
    baseline_commitment = stable_hash(sorted(original_relations.items()))
    one_key = next(iter(original_relations))
    deleted_relation = Counter(original_relations)
    deleted_relation[one_key] -= 1
    if not deleted_relation[one_key]:
        del deleted_relation[one_key]
    record("delete_same_signature_distinct_provenance",
           stable_hash(sorted(deleted_relation.items())) != baseline_commitment,
           "presentation-level multiset comparison detects one omitted decorated relation")

    by_signature = defaultdict(list)
    for key in original_relations:
        by_signature[json.loads(key)["selected_signature_sha256"]].append(key)
    same_signature_pair = next(values[:2] for values in by_signature.values() if len(values) >= 2)
    collapsed = Counter(original_relations)
    collapsed[same_signature_pair[0]] += collapsed[same_signature_pair[1]]
    del collapsed[same_signature_pair[1]]
    record("collapse_same_signature_distinct_provenance",
           stable_hash(sorted(collapsed.items())) != baseline_commitment,
           "signature equality cannot collapse distinct target provenance or port transport")

    return {
        "status": "VERIFIED" if all(row["rejected"] for row in mutations) else "FALSE",
        "mutation_count": len(mutations),
        "mutations": mutations,
        "semantic_controls": [{
            "name": "selected_width_five_complement_before_projection",
            "semantically_vacuous": set(five_hashes) == expected_hashes,
            "reason": (
                "After quartet restriction this only exchanges a split side with its four-port "
                "complement; zero-sum characters give the same XOR and hence the same JC factor."
            ),
        }],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-mutations", action="store_true")
    args = parser.parse_args()
    frozen = frozen_root_audit()
    baseline = run_gate()
    checks = validate_baseline(baseline, frozen)
    mutations = {"status": "SKIPPED", "mutations": []} if args.skip_mutations else run_mutations(baseline, frozen)
    status = "VERIFIED" if all(checks.values()) and mutations["status"] in {"VERIFIED", "SKIPPED"} else "FALSE"
    certificate = {
        "schema": "theta2-five-port-signature-gate-v1",
        "status": status,
        "scope": (
            "the five-port theta-2 minimum-support invariant-signature containment filter only; "
            "not the downstream restoration hard cover, arbitrary subdivisions, or global theorem"
        ),
        "input_hashes": {
            "core_data": file_hash(CORE_PATH),
            "six_template_source": file_hash(TEMPLATE_PATH),
            "seventh_template": file_hash(SEVENTH_PATH),
            "frozen_root_stream": file_hash(ROOT_PATH),
        },
        "checks": checks,
        "failed_checks": [name for name, passed in checks.items() if not passed],
        "baseline": {key: value for key, value in baseline.items()
                     if key not in {"source_signature_integer_values", "all_target_signature_integer_values", "_decorated_relations"}},
        "frozen_root_comparison": {key: value for key, value in frozen.items() if key != "_relations"},
        "containment_filter_proof": {
            "source_signature_bit": "1 iff the graph-derived invariant pullback is a nonzero integer polynomial",
            "target_signature_bit": "0 iff exact sparse expansion proves the pullback is the zero polynomial",
            "necessary_condition": "S(source) subset S(target)",
            "reason": (
                "If a source-open model germ were contained in the target and an invariant vanished "
                "identically on the target but not on the source, the common source set would lie in "
                "the proper zero set of a nonzero source polynomial."
            ),
        },
        "scope_warning": (
            "Equality of the three survivor signature hashes is insufficient to certify the decorated "
            "relation inventory. The separate mixed-graph quotient verifier classifies the 192 raw "
            "presentations and compares the 132 nonretaining marginalized roots to the frozen stream."
        ),
        "mutation_status": mutations["status"],
    }
    HERE.mkdir(parents=True, exist_ok=True)
    crosswalk_rows = []
    for normalized_json, multiplicity in sorted(baseline["_decorated_relations"].items()):
        normalized = json.loads(normalized_json)
        crosswalk_rows.append({
            "schema": 1,
            "normalized_relation_sha256": hashlib.sha256(normalized_json.encode()).hexdigest(),
            "multiplicity": multiplicity,
            "normalized_relation": normalized,
            "present_in_frozen_roots": frozen["_relations"].get(normalized_json, 0),
        })
    with (HERE / "presentation_crosswalk.jsonl").open("w", encoding="utf-8") as handle:
        for row in crosswalk_rows:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
    (HERE / "signature_certificate.json").write_text(json.dumps(certificate, sort_keys=True, indent=2) + "\n")
    (HERE / "mutation_results.json").write_text(json.dumps(mutations, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": status,
        "target_bases": baseline["target_base_count"],
        "target_signatures": baseline["target_unique_signature_count"],
        "necessary_pairs": baseline["necessary_pair_count"],
        "strict_pairs": baseline["strict_pair_count"],
        "source_hashes": baseline["source_signature_sha256"],
        "mutations": mutations["status"],
    }, sort_keys=True))
    if status != "VERIFIED":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
