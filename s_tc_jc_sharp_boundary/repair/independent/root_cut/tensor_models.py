"""Independent finite JC tensor universes used by the Gate 3 audit."""

from __future__ import annotations

import itertools
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Iterable, Iterator, Mapping, Sequence

from graph_conventions import rooted_checks, suppress_root_once, validate_literal_standard


Tensor = tuple[tuple[int, ...], ...]


def weak_compositions(total: int, parts: int) -> Iterator[tuple[int, ...]]:
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for remainder in weak_compositions(total - first, parts - 1):
            yield (first,) + remainder


def cube_actions() -> tuple[tuple[int, ...], ...]:
    choices = tuple(itertools.product((0, 1), repeat=2))
    lookup = {choice: index for index, choice in enumerate(choices)}
    actions = set()
    for order in itertools.permutations((0, 1)):
        for flips in itertools.product((0, 1), repeat=2):
            actions.add(
                tuple(
                    lookup[
                        tuple(
                            choice[order[index]] ^ flips[index]
                            for index in range(2)
                        )
                    ]
                    for choice in choices
                )
            )
    return tuple(sorted(actions))


CUBE_ACTIONS = cube_actions()


@dataclass(frozen=True)
class Core:
    name: str
    arcs: tuple[tuple[str, str], ...]
    repairs: tuple[tuple[int, ...], ...]
    source: str
    sinks: tuple[str, ...]
    reticulation_count: int


@dataclass(frozen=True)
class BuiltNetwork:
    root: str
    arcs: tuple[tuple[str, str], ...]
    selected_labels: tuple[tuple[str, int], ...]
    full_labels: tuple[tuple[str, int], ...]
    core: str
    role: str

    def selected_map(self) -> dict[str, int]:
        return dict(self.selected_labels)

    def full_map(self) -> dict[str, int]:
        return dict(self.full_labels)


def source_and_sinks(arcs: Sequence[tuple[str, str]]) -> tuple[str, tuple[str, ...]]:
    vertices = {vertex for edge in arcs for vertex in edge}
    indegree = Counter(head for _, head in arcs)
    outdegree = Counter(tail for tail, _ in arcs)
    sources = [
        vertex
        for vertex in vertices
        if (indegree[vertex], outdegree[vertex]) == (0, 2)
    ]
    sinks = tuple(
        sorted(
            vertex
            for vertex in vertices
            if (indegree[vertex], outdegree[vertex]) == (2, 0)
        )
    )
    if len(sources) != 1 or not sinks:
        raise ValueError("core does not have one source and a path sink")
    return sources[0], sinks


def load_cores(raw: Mapping[str, object]) -> tuple[Core, ...]:
    cycle = raw["cycle_class"]
    result = [
        Core(
            str(cycle["id"]),
            (("S", "X"), ("S", "X")),
            tuple(tuple(int(index) for index in row) for row in cycle["minimum_repair_sets"]),
            "S",
            ("X",),
            1,
        )
    ]
    for row in raw["theta_classes"]:
        arcs = tuple((str(tail), str(head)) for tail, head in row["arcs"])
        source, sinks = source_and_sinks(arcs)
        result.append(
            Core(
                str(row["id"]),
                arcs,
                tuple(
                    tuple(int(index) for index in repair)
                    for repair in row["minimum_repair_sets"]
                ),
                source,
                sinks,
                2,
            )
        )
    if len(result) != 5:
        raise ValueError("expected one cycle and four theta cores")
    return tuple(result)


def displayed_signature(
    arcs: Sequence[tuple[str, str]],
    selected_labels: Mapping[str, int],
    force_four_columns: bool = False,
) -> Tensor:
    indegree = Counter(head for _, head in arcs)
    outdegree = Counter(tail for tail, _ in arcs)
    reticulations = tuple(
        sorted(
            vertex
            for vertex in set(indegree) | set(outdegree)
            if (indegree[vertex], outdegree[vertex]) == (2, 1)
        )
    )
    if len(reticulations) not in {1, 2}:
        raise ValueError("tensor must have one or two reticulations")
    incoming = {
        reticulation: tuple(
            index
            for index, (_tail, head) in enumerate(arcs)
            if head == reticulation
        )
        for reticulation in reticulations
    }
    displayed_rows: list[list[int]] = []
    for choice in itertools.product((0, 1), repeat=len(reticulations)):
        excluded = {
            incoming[reticulation][1 - bit]
            for reticulation, bit in zip(reticulations, choice)
        }
        children: dict[str, list[str]] = defaultdict(list)
        for index, (tail, head) in enumerate(arcs):
            if index not in excluded:
                children[tail].append(head)
        memo: dict[str, int] = {}

        def descendant_mask(vertex: str) -> int:
            if vertex in memo:
                return memo[vertex]
            value = (
                1 << (selected_labels[vertex] - 1)
                if vertex in selected_labels
                else 0
            )
            for child in children[vertex]:
                value |= descendant_mask(child)
            memo[vertex] = value
            return value

        displayed_rows.append(
            [
                0 if index in excluded else descendant_mask(head)
                for index, (_tail, head) in enumerate(arcs)
            ]
        )
    signatures = []
    for edge_index in range(len(arcs)):
        row = tuple(displayed[edge_index] for displayed in displayed_rows)
        if len(row) == 2 and force_four_columns:
            row = (row[0], row[0], row[1], row[1])
        if any(row):
            signatures.append(row)
    signature = tuple(sorted(set(signatures)))
    if len(signature[0]) == 2:
        return min(
            signature,
            tuple(sorted((right, left) for left, right in signature)),
        )
    if len(signature[0]) == 4:
        return min(
            tuple(
                sorted(tuple(row[index] for index in action) for row in signature)
            )
            for action in CUBE_ACTIONS
        )
    raise ValueError("unexpected displayed-choice width")


def literal_class_check(network: BuiltNetwork) -> dict[str, object]:
    rooted = rooted_checks(network.root, network.arcs, network.full_map())
    literal_edges, _ = suppress_root_once(network.root, network.arcs)
    mixed = validate_literal_standard(literal_edges, network.full_map())
    return {
        "rooted": rooted,
        "mixed": mixed,
        "valid": bool(rooted["valid"] and mixed["valid_standard_strong"]),
    }


def _build_root_theta(
    core: Core,
    selected_sinks: Sequence[int],
    counts: Sequence[int],
    dummy_segments: set[int],
) -> BuiltNetwork:
    selected_sink_vertices = {core.sinks[index] for index in selected_sinks}
    arcs: list[tuple[str, str]] = []
    selected: list[str] = []
    dummy: list[str] = []
    for segment, ((tail, head), count) in enumerate(zip(core.arcs, counts)):
        chain = [tail]
        for position in range(count):
            parent = f"P_{segment}_{position}"
            leaf = f"L_SELECTED_{len(selected)}"
            chain.append(parent)
            arcs.append((parent, leaf))
            selected.append(leaf)
        if segment in dummy_segments:
            parent = f"P_DUMMY_{segment}"
            leaf = f"L_DUMMY_{len(dummy)}"
            chain.append(parent)
            arcs.append((parent, leaf))
            dummy.append(leaf)
        chain.append(head)
        arcs.extend(zip(chain, chain[1:]))
    for sink in core.sinks:
        if sink in selected_sink_vertices:
            leaf = f"L_SELECTED_{len(selected)}"
            selected.append(leaf)
        else:
            leaf = f"L_DUMMY_{len(dummy)}"
            dummy.append(leaf)
        arcs.append((sink, leaf))
    selected_labels = {leaf: index for index, leaf in enumerate(selected, 1)}
    full_labels = {
        leaf: index for index, leaf in enumerate(selected + dummy, 1)
    }
    return BuiltNetwork(
        core.source,
        tuple(arcs),
        tuple(sorted(selected_labels.items())),
        tuple(sorted(full_labels.items())),
        core.name,
        "root",
    )


def _build_root_cycle(
    core: Core,
    selected_sink: bool,
    counts: Sequence[int],
    dummy_segments: set[int],
) -> BuiltNetwork:
    arcs: list[tuple[str, str]] = []
    selected: list[str] = []
    dummy: list[str] = []
    for segment, count in enumerate(counts):
        chain = [core.source]
        for position in range(count):
            parent = f"P_{segment}_{position}"
            leaf = f"L_SELECTED_{len(selected)}"
            chain.append(parent)
            arcs.append((parent, leaf))
            selected.append(leaf)
        if segment in dummy_segments:
            parent = f"P_DUMMY_{segment}"
            leaf = f"L_DUMMY_{len(dummy)}"
            chain.append(parent)
            arcs.append((parent, leaf))
            dummy.append(leaf)
        chain.append(core.sinks[0])
        arcs.extend(zip(chain, chain[1:]))
    if selected_sink:
        leaf = f"L_SELECTED_{len(selected)}"
        selected.append(leaf)
    else:
        leaf = f"L_DUMMY_{len(dummy)}"
        dummy.append(leaf)
    arcs.append((core.sinks[0], leaf))
    selected_labels = {leaf: index for index, leaf in enumerate(selected, 1)}
    full_labels = {
        leaf: index for index, leaf in enumerate(selected + dummy, 1)
    }
    return BuiltNetwork(
        core.source,
        tuple(arcs),
        tuple(sorted(selected_labels.items())),
        tuple(sorted(full_labels.items())),
        core.name,
        "root",
    )


def enumerate_root_tensors(
    cores: Sequence[Core], selected_count: int = 4, force_four_columns: bool = True
) -> tuple[set[Tensor], dict[str, object], dict[Tensor, BuiltNetwork]]:
    tensors: set[Tensor] = set()
    witnesses: dict[Tensor, BuiltNetwork] = {}
    attempts = rooted_valid = literal_valid = 0
    invalid_literal = 0
    invalid_literal_tensors: set[Tensor] = set()
    literal_failure_rows: list[dict[str, object]] = []
    for core in cores:
        if core.reticulation_count == 1:
            for selected_sink in (False, True):
                for counts in weak_compositions(
                    selected_count - int(selected_sink), len(core.arcs)
                ):
                    available = [index for index, count in enumerate(counts) if not count]
                    for size in range(len(available) + 1):
                        for dummy_segments in itertools.combinations(available, size):
                            attempts += 1
                            network = _build_root_cycle(
                                core, selected_sink, counts, set(dummy_segments)
                            )
                            rooted = rooted_checks(
                                network.root, network.arcs, network.full_map()
                            )
                            if not rooted["valid"]:
                                continue
                            rooted_valid += 1
                            check = literal_class_check(network)
                            if not check["valid"]:
                                invalid_literal += 1
                                invalid_literal_tensors.add(
                                    displayed_signature(
                                        network.arcs,
                                        network.selected_map(),
                                        force_four_columns=force_four_columns,
                                    )
                                )
                                literal_failure_rows.append(
                                    {
                                        "core": network.core,
                                        "role": network.role,
                                        "root": network.root,
                                        "arcs": [list(edge) for edge in network.arcs],
                                        "full_labels": dict(network.full_labels),
                                        "failures": check,
                                    }
                                )
                                continue
                            literal_valid += 1
                            tensor = displayed_signature(
                                network.arcs,
                                network.selected_map(),
                                force_four_columns=force_four_columns,
                            )
                            tensors.add(tensor)
                            witnesses.setdefault(tensor, network)
            continue

        for selected_sink_count in range(len(core.sinks) + 1):
            for selected_sinks in itertools.combinations(
                range(len(core.sinks)), selected_sink_count
            ):
                for counts in weak_compositions(
                    selected_count - selected_sink_count, len(core.arcs)
                ):
                    available = [index for index, count in enumerate(counts) if not count]
                    for size in range(len(available) + 1):
                        for dummy_segments in itertools.combinations(available, size):
                            attempts += 1
                            network = _build_root_theta(
                                core, selected_sinks, counts, set(dummy_segments)
                            )
                            rooted = rooted_checks(
                                network.root, network.arcs, network.full_map()
                            )
                            if not rooted["valid"]:
                                continue
                            rooted_valid += 1
                            check = literal_class_check(network)
                            if not check["valid"]:
                                invalid_literal += 1
                                invalid_literal_tensors.add(
                                    displayed_signature(
                                        network.arcs,
                                        network.selected_map(),
                                        force_four_columns=force_four_columns,
                                    )
                                )
                                literal_failure_rows.append(
                                    {
                                        "core": network.core,
                                        "role": network.role,
                                        "root": network.root,
                                        "arcs": [list(edge) for edge in network.arcs],
                                        "full_labels": dict(network.full_labels),
                                        "failures": check,
                                    }
                                )
                                continue
                            literal_valid += 1
                            tensor = displayed_signature(
                                network.arcs,
                                network.selected_map(),
                                force_four_columns=force_four_columns,
                            )
                            tensors.add(tensor)
                            witnesses.setdefault(tensor, network)
    return tensors, {
        "attempts": attempts,
        "rooted_valid_presentations": rooted_valid,
        "literal_standard_strong_presentations": literal_valid,
        "rooted_valid_but_literal_invalid_presentations": invalid_literal,
        "invalid_presentation_tensor_types": len(invalid_literal_tensors),
        "invalid_presentation_tensor_types_without_literal_valid_witness": len(
            invalid_literal_tensors - tensors
        ),
        "literal_failure_rows": literal_failure_rows,
        "tensor_types": len(tensors),
    }, witnesses


def _build_nonroot_theta(
    core: Core,
    selected_sinks: Sequence[int],
    counts: Sequence[int],
    repair: set[int],
) -> BuiltNetwork:
    selected_sink_vertices = {core.sinks[index] for index in selected_sinks}
    occupied = {index for index, count in enumerate(counts) if count}
    arcs: list[tuple[str, str]] = []
    selected: list[str] = []
    dummy: list[str] = []
    for segment, ((tail, head), count) in enumerate(zip(core.arcs, counts)):
        chain = [tail]
        for position in range(count):
            parent = f"P_{segment}_{position}"
            leaf = f"L_SELECTED_{len(selected)}"
            chain.append(parent)
            arcs.append((parent, leaf))
            selected.append(leaf)
        if segment in repair and segment not in occupied:
            parent = f"P_DUMMY_{segment}"
            leaf = f"L_DUMMY_{len(dummy)}"
            chain.append(parent)
            arcs.append((parent, leaf))
            dummy.append(leaf)
        chain.append(head)
        arcs.extend(zip(chain, chain[1:]))
    for sink in core.sinks:
        if sink in selected_sink_vertices:
            leaf = f"L_SELECTED_{len(selected)}"
            selected.append(leaf)
        else:
            leaf = f"L_DUMMY_{len(dummy)}"
            dummy.append(leaf)
        arcs.append((sink, leaf))
    root = "AUDIT_ROOT"
    incoming = "L_INCOMING"
    arcs.extend(((root, core.source), (root, incoming)))
    selected_labels = {leaf: index for index, leaf in enumerate(selected, 1)}
    selected_labels[incoming] = len(selected) + 1
    all_leaves = selected + [incoming] + dummy
    full_labels = {leaf: index for index, leaf in enumerate(all_leaves, 1)}
    return BuiltNetwork(
        root,
        tuple(arcs),
        tuple(sorted(selected_labels.items())),
        tuple(sorted(full_labels.items())),
        core.name,
        "nonroot",
    )


def _build_nonroot_cycle(
    core: Core, outgoing_count: int, selected_sink: bool, left_count: int
) -> BuiltNetwork:
    ordinary_count = outgoing_count - int(selected_sink)
    counts = (left_count, ordinary_count - left_count)
    arcs: list[tuple[str, str]] = []
    selected: list[str] = []
    dummy: list[str] = []
    for segment, count in enumerate(counts):
        chain = [core.source]
        for position in range(count):
            parent = f"C_P_{segment}_{position}"
            leaf = f"L_SELECTED_{len(selected)}"
            chain.append(parent)
            arcs.append((parent, leaf))
            selected.append(leaf)
        chain.append(core.sinks[0])
        arcs.extend(zip(chain, chain[1:]))
    if selected_sink:
        leaf = f"L_SELECTED_{len(selected)}"
        selected.append(leaf)
    else:
        leaf = "L_DUMMY_SINK"
        dummy.append(leaf)
    arcs.append((core.sinks[0], leaf))
    root = "AUDIT_ROOT"
    incoming = "L_INCOMING"
    arcs.extend(((root, core.source), (root, incoming)))
    selected_labels = {leaf: index for index, leaf in enumerate(selected, 1)}
    selected_labels[incoming] = outgoing_count + 1
    all_leaves = selected + [incoming] + dummy
    full_labels = {leaf: index for index, leaf in enumerate(all_leaves, 1)}
    return BuiltNetwork(
        root,
        tuple(arcs),
        tuple(sorted(selected_labels.items())),
        tuple(sorted(full_labels.items())),
        core.name,
        "nonroot",
    )


def enumerate_nonroot_tensors(
    cores: Sequence[Core], outgoing_count: int, include_incoming: bool
) -> tuple[set[Tensor], dict[str, object], dict[Tensor, BuiltNetwork]]:
    tensors: set[Tensor] = set()
    witnesses: dict[Tensor, BuiltNetwork] = {}
    attempts = valid = 0
    for core in cores:
        if core.reticulation_count == 1:
            for selected_sink in (False, True):
                ordinary = outgoing_count - int(selected_sink)
                for left_count in range(ordinary + 1):
                    attempts += 1
                    network = _build_nonroot_cycle(
                        core, outgoing_count, selected_sink, left_count
                    )
                    check = literal_class_check(network)
                    if not check["valid"]:
                        raise AssertionError((core.name, check))
                    valid += 1
                    selected = network.selected_map()
                    quartet = (
                        set(range(1, outgoing_count + 2))
                        if include_incoming
                        else set(range(1, outgoing_count + 1))
                    )
                    restricted = {
                        leaf: label
                        for leaf, label in selected.items()
                        if label in quartet
                    }
                    tensor = displayed_signature(network.arcs, restricted)
                    tensors.add(tensor)
                    witnesses.setdefault(tensor, network)
            continue

        for selected_sink_count in range(len(core.sinks) + 1):
            for selected_sinks in itertools.combinations(
                range(len(core.sinks)), selected_sink_count
            ):
                ordinary = outgoing_count - selected_sink_count
                if ordinary < 0:
                    continue
                for counts in weak_compositions(ordinary, len(core.arcs)):
                    for repair in core.repairs:
                        attempts += 1
                        network = _build_nonroot_theta(
                            core, selected_sinks, counts, set(repair)
                        )
                        check = literal_class_check(network)
                        if not check["valid"]:
                            raise AssertionError((core.name, check))
                        valid += 1
                        selected = network.selected_map()
                        quartet = (
                            set(range(1, outgoing_count + 2))
                            if include_incoming
                            else set(range(1, outgoing_count + 1))
                        )
                        restricted = {
                            leaf: label
                            for leaf, label in selected.items()
                            if label in quartet
                        }
                        tensor = displayed_signature(network.arcs, restricted)
                        tensors.add(tensor)
                        witnesses.setdefault(tensor, network)
    return tensors, {
        "attempts": attempts,
        "literal_standard_strong_presentations": valid,
        "tensor_types": len(tensors),
    }, witnesses


TREE_TENSOR: Tensor = tuple((mask,) for mask in (1, 2, 3, 4, 8, 12))


def _relabel_mask(mask: int, old_positions_in_new_order: Sequence[int]) -> int:
    result = 0
    for new_position, old_position in enumerate(old_positions_in_new_order):
        if mask & (1 << old_position):
            result |= 1 << new_position
    return result


def three_port_structural_variants(tensor: Tensor) -> set[tuple[int, Tensor]]:
    """Designate each boundary in turn as the central connector boundary.

    The two remaining boundaries are quotiented by their swap.  Reticulation
    choices are quotiented by axis permutation and complementation, exactly as
    structural edge-mask data (not by complementary split masks).
    """

    width = len(tensor[0])
    if width == 2:
        reticulations = 1
        actions = ((0, 1), (1, 0))
    elif width == 4:
        reticulations = 2
        actions = CUBE_ACTIONS
    else:
        raise ValueError("three-port tensor has unexpected choice width")
    variants: set[tuple[int, Tensor]] = set()
    for central in range(3):
        outer = [position for position in range(3) if position != central]
        boundary_order = outer + [central]
        relabelled = tuple(
            tuple(_relabel_mask(mask, boundary_order) for mask in row)
            for row in tensor
        )
        candidates = []
        for action in actions:
            for outer_swap in (False, True):
                rows = []
                for row in relabelled:
                    transformed = []
                    for index in action:
                        mask = row[index]
                        if outer_swap:
                            mask = (mask & 0b100) | ((mask & 0b001) << 1) | ((mask & 0b010) >> 1)
                        transformed.append(mask)
                    rows.append(tuple(transformed))
                candidates.append(tuple(sorted(rows)))
        variants.add((reticulations, min(candidates)))
    return variants
