#!/usr/bin/env python3
"""Clean-room exact audit of selected-parameter product maps.

The primary completion JSON is read only for its core records.  Completion
graphs, displayed switchings, descendant masks, signature classes, and
Jacobian ranks are regenerated here without importing project code.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter, defaultdict, deque
from fractions import Fraction
from pathlib import Path
from typing import Dict, Iterable, Iterator, Mapping, Sequence, Tuple

from verify_root_probe import canonical_json_bytes, sha256_bytes


def rational_rank(matrix: Sequence[Sequence[Fraction]]) -> int:
    if not matrix:
        return 0
    work = [[Fraction(value) for value in row] for row in matrix]
    height = len(work)
    width = len(work[0])
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, height) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        lead = work[pivot_row][column]
        work[pivot_row] = [value / lead for value in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                left - scale * right
                for left, right in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == height:
            break
    return pivot_row


def normalize_zero_sum_row(row: Sequence[int], full_mask: int) -> Tuple[int, ...]:
    """Return the JC split/complement class seen by zero-sum characters."""
    return tuple(
        0 if mask in (0, full_mask) else min(mask, full_mask ^ mask)
        for mask in row
    )


def normalization_mutation_tests() -> dict:
    """Reject the three normalization errors found by the referee audit."""
    full_mask = 0b1111
    invisible = normalize_zero_sum_row((full_mask, full_mask), full_mask)
    split = normalize_zero_sum_row((0b0001, 0b0010), full_mask)
    complement = normalize_zero_sum_row((0b1110, 0b1101), full_mask)
    distinct = normalize_zero_sum_row((0b0001, 0b0100), full_mask)
    tests = {
        "full_split_is_tensor_invisible": invisible == (0, 0),
        "complementary_splits_have_one_class": split == complement,
        "distinct_split_classes_are_not_merged": split != distinct,
    }
    if not all(tests.values()):
        raise AssertionError(tests)
    return {
        **tests,
        "full_mask": full_mask,
        "split_row": list(split),
        "complement_row": list(complement),
        "distinct_row": list(distinct),
        "all_mutations_rejected": True,
    }


def weak_compositions(total: int, bins: int) -> Iterator[Tuple[int, ...]]:
    if bins == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total - first, bins - 1):
            yield (first, *rest)


def source_and_sinks(arcs: Sequence[Tuple[str, str]]) -> Tuple[str, Tuple[str, ...]]:
    indeg = Counter(v for _, v in arcs)
    outdeg = Counter(u for u, _ in arcs)
    vertices = {x for arc in arcs for x in arc}
    sources = sorted(v for v in vertices if indeg[v] == 0)
    sinks = tuple(sorted(v for v in vertices if indeg[v] == 2 and outdeg[v] == 0))
    if len(sources) != 1:
        raise AssertionError(sources)
    return sources[0], sinks


def core_rows(core_data: dict) -> list[dict]:
    rows = []
    for core in core_data["cores"]:
        arcs = tuple((str(edge["tail"]), str(edge["head"])) for edge in core["segments"])
        rows.append({
            "id": core["id"],
            "arcs": arcs,
            "repairs": tuple(tuple(int(i) for i in row) for row in core["minimum_repairs"]),
        })
    return rows


def build_completion(
    core: dict,
    selected_count: int,
    sink_mask: int,
    counts: Sequence[int],
    repair_index: int | None,
    repair: Sequence[int],
) -> dict:
    arcs = core["arcs"]
    source, sinks = source_and_sinks(arcs)
    selected_sinks = {
        sink for i, sink in enumerate(sinks) if sink_mask & (1 << i)
    }
    ordinary_count = sum(counts)
    labels = iter(f"O_{i}" for i in range(ordinary_count))
    words = [list(next(labels) for _ in range(count)) for count in counts]
    dummy_labels = []
    for arc_index in repair:
        if not words[arc_index]:
            label = f"D_REPAIR_{repair_index}_{arc_index}"
            words[arc_index].append(label)
            dummy_labels.append(label)
    sink_labels = {}
    for i, sink in enumerate(sinks):
        if sink in selected_sinks:
            sink_labels[sink] = f"SINK_{i}"
        else:
            label = f"D_SINK_{i}"
            sink_labels[sink] = label
            dummy_labels.append(label)

    directed = []
    labels_by_leaf: Dict[str, str] = {}
    directed.extend((("ROOT", source), ("ROOT", "L:INCOMING")))
    labels_by_leaf["L:INCOMING"] = "INCOMING"
    for arc_index, ((tail, head), word) in enumerate(zip(arcs, words)):
        prior = tail
        for position, label in enumerate(word):
            node = f"W:{arc_index}:{position}:{label}"
            leaf = f"L:{label}"
            directed.extend(((prior, node), (node, leaf)))
            labels_by_leaf[leaf] = label
            prior = node
        directed.append((prior, head))
    for sink, label in sorted(sink_labels.items()):
        leaf = f"L:{label}"
        directed.append((sink, leaf))
        labels_by_leaf[leaf] = label
    selected_labels = tuple(sorted(
        label for label in labels_by_leaf.values() if not label.startswith("D_")
    ))
    if len(selected_labels) != selected_count + 1:
        raise AssertionError((selected_labels, selected_count))
    return {
        "arcs": tuple(directed),
        "labels": labels_by_leaf,
        "selected_labels": selected_labels,
        "dummy_labels": tuple(sorted(dummy_labels)),
        "words": tuple(tuple(row) for row in words),
        "sinks": sinks,
    }


def switching_signatures(graph: dict) -> dict:
    arcs = graph["arcs"]
    vertices = {x for arc in arcs for x in arc}
    indeg = Counter(v for _, v in arcs)
    retics = tuple(sorted(v for v in vertices if indeg[v] == 2))
    incoming = {
        r: tuple(i for i, (_u, v) in enumerate(arcs) if v == r)
        for r in retics
    }
    ordered_labels = graph["selected_labels"]
    label_index = {label: i for i, label in enumerate(ordered_labels)}
    leaf_bits = {
        leaf: (1 << label_index[label])
        for leaf, label in graph["labels"].items()
        if label in label_index
    }
    signatures = [[0] * (1 << len(retics)) for _ in arcs]
    for display_index, choices in enumerate(itertools.product((0, 1), repeat=len(retics))):
        removed = {incoming[r][1 - choice] for r, choice in zip(retics, choices)}
        active = [i for i in range(len(arcs)) if i not in removed]
        children: Dict[str, list[str]] = defaultdict(list)
        active_vertices = set(vertices)
        for i in active:
            u, v = arcs[i]
            children[u].append(v)
        cache: Dict[str, int] = {}

        def mask(node: str) -> int:
            if node in cache:
                return cache[node]
            value = leaf_bits.get(node, 0)
            for child in children[node]:
                value |= mask(child)
            cache[node] = value
            return value

        mask("ROOT")
        for i in active:
            signatures[i][display_index] = mask(arcs[i][1])
    full_mask = (1 << len(ordered_labels)) - 1
    raw_classes: Dict[Tuple[int, ...], list[int]] = defaultdict(list)
    normalized_classes: Dict[Tuple[int, ...], list[int]] = defaultdict(list)
    normalized_rows = []
    for edge_index, row in enumerate(signatures):
        raw_row = tuple(row)
        if any(raw_row):
            raw_classes[raw_row].append(edge_index)
        normalized = normalize_zero_sum_row(raw_row, full_mask)
        normalized_rows.append(normalized)
        if any(normalized):
            normalized_classes[normalized].append(edge_index)

    class_rows = tuple(sorted(normalized_classes))
    target_dimension = len(class_rows) + len(retics)
    physical_dimension = len(arcs) + len(retics)

    # Construct the actual Jacobian of y_C=product_{e in C} x_e together
    # with the inherited identity coordinates.  Evaluation at x_e=1/2 gives
    # the exact block entries 2^{-(|C|-1)}.  The selected columns form a
    # diagonal square minor, but its rank is computed independently below.
    jacobian = [
        [Fraction(0) for _ in range(physical_dimension)]
        for _ in range(target_dimension)
    ]
    selected_columns = []
    determinant = Fraction(1)
    for row_index, signature in enumerate(class_rows):
        members = normalized_classes[signature]
        derivative = Fraction(1, 2 ** (len(members) - 1))
        for edge_index in members:
            jacobian[row_index][edge_index] = derivative
        selected_columns.append(members[0])
        determinant *= derivative
    for reticulation_index in range(len(retics)):
        row_index = len(class_rows) + reticulation_index
        column_index = len(arcs) + reticulation_index
        jacobian[row_index][column_index] = Fraction(1)
        selected_columns.append(column_index)
    rank = rational_rank(jacobian)

    return {
        "reticulation_count": len(retics),
        "physical_edge_count": len(arcs),
        "raw_descendant_edge_class_count": len(raw_classes),
        "effective_edge_class_count": len(normalized_classes),
        "discarded_tensor_invisible_edge_count": (
            len(arcs) - sum(len(value) for value in normalized_classes.values())
        ),
        "class_sizes": sorted(len(v) for v in normalized_classes.values()),
        "signature_rows": [list(row) for row in class_rows],
        "jacobian_evaluation_point": "all visible physical edge multipliers = 1/2",
        "jacobian_row_rank_at_open_point": rank,
        "parameter_target_dimension": target_dimension,
        "physical_parameter_dimension": physical_dimension,
        "nonzero_minor": {
            "rows": list(range(target_dimension)),
            "physical_parameter_columns": selected_columns,
            "determinant_numerator": determinant.numerator,
            "determinant_denominator": determinant.denominator,
        },
        "raw_to_normalized_class_reduction": len(raw_classes) - len(normalized_classes),
        "zero_sum_normalization": (
            "each switching mask m maps to 0 for m in {0,full}, otherwise "
            "min(m,full xor m); complete normalized rows are then grouped"
        ),
    }


def enumerate_completions(core_data: dict, sizes: Sequence[int]) -> Iterator[dict]:
    for core in core_rows(core_data):
        _source, sinks = source_and_sinks(core["arcs"])
        for source_outgoing in sizes:
            for incoming_selected in (True, False):
                # A source relation with n outgoing ports has n+1 selected
                # tensor boundaries.  If the target's structural incoming is
                # zeroed, all n+1 selected boundaries occupy outgoing roles.
                selected_count = source_outgoing if incoming_selected else source_outgoing + 1
                for sink_mask in range(1 << len(sinks)):
                    ordinary = selected_count - bin(sink_mask).count("1")
                    if ordinary < 0:
                        continue
                    for counts in weak_compositions(ordinary, len(core["arcs"])):
                        presentations = ((None, ()),) if core["id"] == "cycle" else tuple(enumerate(core["repairs"]))
                        for repair_index, repair in presentations:
                            graph = build_completion(
                                core, selected_count, sink_mask, counts,
                                repair_index, repair,
                            )
                            if not incoming_selected:
                                graph["selected_labels"] = tuple(
                                    label for label in graph["selected_labels"]
                                    if label != "INCOMING"
                                )
                                graph["dummy_labels"] = tuple(sorted((
                                    *graph["dummy_labels"], "INCOMING",
                                )))
                            yield {
                                "core_id": core["id"],
                                "source_outgoing_count": source_outgoing,
                                "selected_tensor_port_count": source_outgoing + 1,
                                "incoming_selected": incoming_selected,
                                "selected_count_relative_to_target_root": selected_count,
                                "sink_mask": sink_mask,
                                "counts": counts,
                                "repair_index": repair_index,
                                "graph": graph,
                            }


def audit(core_data: dict) -> dict:
    commitment = hashlib.sha256()
    failures = []
    counts = Counter()
    normalization_reductions = Counter()
    invisible = Counter()
    max_class = 0
    max_fiber = 0
    redundant_example = None
    for index, row in enumerate(enumerate_completions(core_data, (3, 4, 5, 6))):
        signature = switching_signatures(row["graph"])
        counts[(
            row["source_outgoing_count"],
            "incoming_selected" if row["incoming_selected"] else "incoming_marginalized",
            row["core_id"],
        )] += 1
        if signature["jacobian_row_rank_at_open_point"] != signature["parameter_target_dimension"]:
            failures.append({"index": index, "row": row, "signature": signature})
        max_class = max(max_class, *(signature["class_sizes"] or [0]))
        max_fiber = max(
            max_fiber,
            signature["physical_parameter_dimension"] - signature["parameter_target_dimension"],
        )
        reduction = signature["raw_to_normalized_class_reduction"]
        normalization_reductions[str(reduction)] += 1
        if signature["discarded_tensor_invisible_edge_count"]:
            invisible["completion_count"] += 1
            invisible["physical_edge_count"] += signature[
                "discarded_tensor_invisible_edge_count"
            ]
        if redundant_example is None and (
            reduction or signature["discarded_tensor_invisible_edge_count"]
        ):
            redundant_example = {
                "core_id": row["core_id"],
                "source_outgoing_count": row["source_outgoing_count"],
                "incoming_selected": row["incoming_selected"],
                "sink_mask": row["sink_mask"],
                "counts": row["counts"],
                "dummy_labels": row["graph"]["dummy_labels"],
                "signature": signature,
            }
        record = {
            "core_id": row["core_id"],
            "source_outgoing_count": row["source_outgoing_count"],
            "selected_tensor_port_count": row["selected_tensor_port_count"],
            "incoming_selected": row["incoming_selected"],
            "selected_count_relative_to_target_root": row["selected_count_relative_to_target_root"],
            "sink_mask": row["sink_mask"],
            "counts": row["counts"],
            "repair_index": row["repair_index"],
            "dummy_labels": row["graph"]["dummy_labels"],
            "signature_sha256": sha256_bytes(canonical_json_bytes(signature)),
        }
        commitment.update(canonical_json_bytes(record))
    return {
        "completion_count": sum(counts.values()),
        "by_source_size_mode_and_core": {
            f"n{n}:{mode}:{core}": value
            for (n, mode, core), value in sorted(counts.items())
        },
        "full_row_rank_failure_count": len(failures),
        "failures": failures[:5],
        "maximum_effective_product_class_size_in_bounded_census": max_class,
        "maximum_parameter_fiber_dimension_in_bounded_census": max_fiber,
        "raw_to_normalized_class_reduction_counts": dict(
            sorted(normalization_reductions.items(), key=lambda row: int(row[0]))
        ),
        "tensor_invisible_parameter_counts": dict(sorted(invisible.items())),
        "redundant_parameter_example": redundant_example,
        "completion_signature_commitment_sha256": commitment.hexdigest(),
        "general_open_product_certificate": {
            "map": "y=product(x_i), lambda'=lambda or 1-lambda",
            "class_blocks_are_disjoint_by_equivalence_partition": True,
            "jacobian_constructed_and_ranked_over_Q": True,
            "exact_evaluation_point": "all visible edge multipliers = 1/2",
            "derivative_nonzero_for_every_positive_class_coordinate": True,
            "onto_witness": "x_i=y^(1/k) for each class of size k",
            "semialgebraic": True,
        },
        "normalization_mutation_tests": normalization_mutation_tests(),
        "interpretation_caveat": (
            "Full row rank is for the physical-to-descriptor parameter map. "
            "Some descriptor coordinates are tensor-invisible or inheritance-redundant "
            "after a core-collapsing marginal, so this is not a claim that the "
            "descriptor cube is a minimal-coordinate model-image manifold."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core-certificate", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("parameter_submersion_certificate.json"))
    args = parser.parse_args()
    before = hashlib.sha256(args.core_certificate.read_bytes()).hexdigest()
    core_data = json.loads(args.core_certificate.read_text())
    payload = {
        "schema": "selected-parameter-submersion-clean-room-v2",
        "core_certificate_sha256": before,
        **audit(core_data),
    }
    after = hashlib.sha256(args.core_certificate.read_bytes()).hexdigest()
    payload["input_stable_during_run"] = before == after
    raw = canonical_json_bytes(payload)
    args.output.write_bytes(raw)
    print(json.dumps({
        "output": str(args.output),
        "sha256": sha256_bytes(raw),
        "completion_count": payload["completion_count"],
        "full_row_rank_failures": payload["full_row_rank_failure_count"],
        "max_product_class": payload["maximum_effective_product_class_size_in_bounded_census"],
        "normalization_reductions": payload["raw_to_normalized_class_reduction_counts"],
        "invisible": payload["tensor_invisible_parameter_counts"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
