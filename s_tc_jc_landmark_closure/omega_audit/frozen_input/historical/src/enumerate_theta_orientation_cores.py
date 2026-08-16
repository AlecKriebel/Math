"""Exhaustive first-principles census of rooted theta orientation cores.

After suppressing ordinary degree-2 tree/port vertices, a rooted level-2 theta
blob has two degree-3 branch vertices U,V, one degree-2 source S (the global
root artifact or the unique incoming cut-edge vertex), and two reticulations.
A reticulation is either a branch vertex or a degree-2 sink X whose outgoing
cut edge leaves the blob.

The script enumerates every distribution and order of S and the path-sink
reticulations on the three theta paths, every compatible path orientation,
then enforces acyclicity and reachability from S.  It quotients by branch
reversal and path permutation without using a specialized network package.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from itertools import permutations, product
import json


def multiset_permutations(items):
    return sorted(set(permutations(items)))


def weak_compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total - first, parts - 1):
            yield (first,) + rest


def path_sequence_triples(event_types):
    triples = set()
    for word in multiset_permutations(event_types):
        for lengths in weak_compositions(len(word), 3):
            paths = []
            offset = 0
            for length in lengths:
                paths.append(tuple(word[offset : offset + length]))
                offset += length
            triples.add(tuple(paths))
    return sorted(triples)


def reversed_template(branches, paths):
    return (branches[::-1], tuple(tuple(reversed(path)) for path in paths))


def canonical_template(branches, paths):
    candidates = []
    for candidate_branches, candidate_paths in (
        (branches, paths),
        reversed_template(branches, paths),
    ):
        for permutation in permutations(range(3)):
            permuted = tuple(candidate_paths[index] for index in permutation)
            candidates.append((candidate_branches, permuted))
    return min(candidates)


def template_automorphism_order(branches, paths):
    count = 0
    for swap in (False, True):
        candidate_branches, candidate_paths = (
            reversed_template(branches, paths) if swap else (branches, paths)
        )
        for permutation in permutations(range(3)):
            permuted = tuple(candidate_paths[index] for index in permutation)
            if candidate_branches == branches and permuted == paths:
                count += 1
    return count


def event_segment_signs(path):
    """Return fixed U-to-V signs, with None only for an empty path.

    A sign +1 orients a segment left-to-right; -1 orients right-to-left.
    """
    if not path:
        return (None,)
    signs = []
    # U to first event.
    signs.append(-1 if path[0] == "S" else +1)
    for left, right in zip(path, path[1:]):
        required_by_left = +1 if left == "S" else -1
        required_by_right = -1 if right == "S" else +1
        if required_by_left != required_by_right:
            return None
        signs.append(required_by_left)
    # Last event to V.
    signs.append(+1 if path[-1] == "S" else -1)
    return tuple(signs)


def instantiate(branches, paths, empty_signs):
    vertices = {"U": branches[0], "V": branches[1]}
    directed_edges = []
    empty_index = 0
    x_index = 0
    for path_index, path in enumerate(paths):
        names = ["U"]
        for event_index, event in enumerate(path):
            if event == "S":
                name = "S"
            else:
                name = f"X{x_index}"
                x_index += 1
            vertices[name] = event
            names.append(name)
        names.append("V")
        signs = event_segment_signs(path)
        if signs is None:
            return None
        if not path:
            signs = (empty_signs[empty_index],)
            empty_index += 1
        for segment_index, (left, right, sign) in enumerate(zip(names, names[1:], signs)):
            tail, head = (left, right) if sign == +1 else (right, left)
            directed_edges.append(
                {
                    "tail": tail,
                    "head": head,
                    "path": path_index,
                    "segment": segment_index,
                }
            )
    return vertices, directed_edges


def degrees(vertices, edges):
    indegree = Counter()
    outdegree = Counter()
    for edge in edges:
        outdegree[edge["tail"]] += 1
        indegree[edge["head"]] += 1
    return {
        vertex: (indegree[vertex], outdegree[vertex])
        for vertex in vertices
    }


def is_acyclic_reachable(vertices, edges):
    outgoing = defaultdict(list)
    indegree = Counter()
    for edge in edges:
        outgoing[edge["tail"]].append(edge["head"])
        indegree[edge["head"]] += 1
    queue = deque(vertex for vertex in vertices if indegree[vertex] == 0)
    order = []
    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        for child in outgoing[vertex]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if len(order) != len(vertices):
        return False
    reachable = {"S"}
    queue = deque(("S",))
    while queue:
        vertex = queue.popleft()
        for child in outgoing[vertex]:
            if child not in reachable:
                reachable.add(child)
                queue.append(child)
    return reachable == set(vertices)


def degree_constraints_hold(vertices, edges):
    actual = degrees(vertices, edges)
    required = {
        "S": (0, 2),
        "X": (2, 0),
        "T": (1, 2),
        "R": (2, 1),
    }
    return all(actual[vertex] == required[color] for vertex, color in vertices.items())


def minimal_strong_repairs(vertices, edges):
    """Return minimal directed segments that must receive a tree-port vertex."""
    outgoing = defaultdict(list)
    for index, edge in enumerate(edges):
        outgoing[edge["tail"]].append((index, edge["head"]))

    obligations = []
    for vertex, color in vertices.items():
        children = outgoing[vertex]
        if color in {"T", "S"}:
            if not any(vertices[child] in {"T", "S"} for _index, child in children):
                obligations.append(tuple(index for index, _child in children))
        elif color == "R":
            assert len(children) == 1
            index, child = children[0]
            if vertices[child] in {"R", "X"}:
                obligations.append((index,))

    if not obligations:
        return ((),)
    edge_count = len(edges)
    repairs = []
    for mask in range(1 << edge_count):
        chosen = tuple(index for index in range(edge_count) if mask & (1 << index))
        if all(any(index in chosen for index in obligation) for obligation in obligations):
            repairs.append(chosen)
    minimum = min(map(len, repairs))
    return tuple(repair for repair in repairs if len(repair) == minimum)


def enumerate_cores():
    accepted = {}
    raw_valid = 0
    for branch_reticulations in (0, 1):
        branches = ("T", "T") if branch_reticulations == 0 else ("T", "R")
        events = ("S",) + ("X",) * (2 - branch_reticulations)
        for paths in path_sequence_triples(events):
            fixed_signs = [event_segment_signs(path) for path in paths]
            if any(signs is None for signs in fixed_signs):
                continue
            empty_count = sum(not path for path in paths)
            for empty_signs in product((-1, +1), repeat=empty_count):
                instantiated = instantiate(branches, paths, empty_signs)
                if instantiated is None:
                    continue
                vertices, edges = instantiated
                if not degree_constraints_hold(vertices, edges):
                    continue
                if not is_acyclic_reachable(vertices, edges):
                    continue
                raw_valid += 1
                canonical = canonical_template(branches, paths)
                if canonical in accepted:
                    continue
                repairs = minimal_strong_repairs(vertices, edges)
                accepted[canonical] = {
                    "branch_types": list(branches),
                    "path_event_sequences_U_to_V": [list(path) for path in paths],
                    "directed_segments": edges,
                    "vertex_types": vertices,
                    "template_automorphism_order": template_automorphism_order(branches, paths),
                    "minimum_tree_port_subdivisions": len(repairs[0]),
                    "minimal_repair_segment_sets": [
                        [
                            {
                                "tail": edges[index]["tail"],
                                "head": edges[index]["head"],
                                "path": edges[index]["path"],
                                "segment": edges[index]["segment"],
                            }
                            for index in repair
                        ]
                        for repair in repairs
                    ],
                }
    return raw_valid, list(accepted.values())


def main():
    raw_valid, cores = enumerate_cores()
    output = {
        "status": "EXACTLY COMPUTED",
        "raw_valid_orientations_before_isomorphism": raw_valid,
        "orientation_core_count": len(cores),
        "cores": cores,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

