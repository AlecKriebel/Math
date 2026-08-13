#!/usr/bin/env python3
"""Primary first-principles level-2 orientation-core enumerator.

This program deliberately shares no code with the implementation under
``independent/decorated_atlas``.  It generates event placements and segment
directions, rather than reading the historical five-core list.
"""

from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass
from itertools import combinations, permutations, product
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "certificates" / "core_universe.json"


@dataclass(frozen=True)
class Segment:
    tail: str
    head: str
    path: int
    position: int


@dataclass(frozen=True)
class Candidate:
    branch_roles: tuple[str, str]
    path_words: tuple[tuple[str, ...], ...]
    segments: tuple[Segment, ...]
    roles: tuple[tuple[str, str], ...]

    @property
    def role_map(self) -> dict[str, str]:
        return dict(self.roles)


def weak_compositions(total: int, bins: int):
    if bins == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for suffix in weak_compositions(total - first, bins - 1):
            yield (first,) + suffix


def event_path_words(events: tuple[str, ...]):
    """All ordered distributions of one named event list over three paths."""
    seen: set[tuple[tuple[str, ...], ...]] = set()
    for order in set(permutations(events)):
        for sizes in weak_compositions(len(events), 3):
            cursor = 0
            row = []
            for size in sizes:
                row.append(tuple(order[cursor : cursor + size]))
                cursor += size
            seen.add(tuple(row))
    yield from sorted(seen)


def instantiate(
    branch_roles: tuple[str, str],
    path_words: tuple[tuple[str, ...], ...],
    directions: tuple[int, ...],
) -> Candidate:
    """Instantiate one direction for every segment of the path template."""
    roles: dict[str, str] = {"U": branch_roles[0], "V": branch_roles[1]}
    paths: list[list[str]] = []
    x_counter = 0
    for word in path_words:
        vertices = ["U"]
        for event in word:
            if event == "S":
                name = "S"
            else:
                name = f"X{x_counter}"
                x_counter += 1
            roles[name] = event
            vertices.append(name)
        vertices.append("V")
        paths.append(vertices)
    segment_count = sum(len(path) - 1 for path in paths)
    assert len(directions) == segment_count
    segments: list[Segment] = []
    cursor = 0
    for path_index, path in enumerate(paths):
        for position, (left, right) in enumerate(zip(path, path[1:])):
            tail, head = (left, right) if directions[cursor] else (right, left)
            segments.append(Segment(tail, head, path_index, position))
            cursor += 1
    return Candidate(
        branch_roles,
        path_words,
        tuple(segments),
        tuple(sorted(roles.items())),
    )


def valid_candidate(candidate: Candidate) -> bool:
    roles = candidate.role_map
    indegree = Counter(s.head for s in candidate.segments)
    outdegree = Counter(s.tail for s in candidate.segments)
    required = {"S": (0, 2), "X": (2, 0), "T": (1, 2), "R": (2, 1)}
    if any((indegree[v], outdegree[v]) != required[role] for v, role in roles.items()):
        return False
    # Kahn acyclicity.
    work = {v: indegree[v] for v in roles}
    children: dict[str, list[str]] = {v: [] for v in roles}
    for segment in candidate.segments:
        children[segment.tail].append(segment.head)
    queue = deque(sorted(v for v in roles if work[v] == 0))
    visited: list[str] = []
    while queue:
        v = queue.popleft()
        visited.append(v)
        for w in children[v]:
            work[w] -= 1
            if work[w] == 0:
                queue.append(w)
    if len(visited) != len(roles):
        return False
    reached = {"S"}
    queue = deque(["S"])
    while queue:
        v = queue.popleft()
        for w in children[v]:
            if w not in reached:
                reached.add(w)
                queue.append(w)
    return reached == set(roles)


def canonical(candidate: Candidate):
    """Canonical path-template code under path permutation and branch swap."""
    # Work with role words plus directed signs.  X names are intentionally
    # forgotten; their role and path order contain all relevant information.
    role = candidate.role_map
    by_path: dict[int, list[Segment]] = {i: [] for i in range(3)}
    for segment in candidate.segments:
        by_path[segment.path].append(segment)
    for values in by_path.values():
        values.sort(key=lambda s: s.position)

    def path_code(index: int, reverse: bool):
        segments = by_path[index]
        # Segment order already fixes orientation relative to U-to-V: an edge
        # points forward iff its tail is the left endpoint in the reconstructed
        # path.  Reconstruct endpoint chain directly from the template names.
        endpoint_chain = ["U"]
        for segment in segments:
            left_candidates = {segment.tail, segment.head}
            left = endpoint_chain[-1]
            if left not in left_candidates:
                raise AssertionError("broken path")
            endpoint_chain.append(segment.head if segment.tail == left else segment.tail)
        signs = [
            1 if segment.tail == endpoint_chain[j] else 0
            for j, segment in enumerate(segments)
        ]
        event_roles = tuple(role[v] for v in endpoint_chain[1:-1])
        if reverse:
            event_roles = tuple(reversed(event_roles))
            signs = [1 - value for value in reversed(signs)]
        return event_roles, tuple(signs)

    encodings = []
    for reverse in (False, True):
        branches = candidate.branch_roles[::-1] if reverse else candidate.branch_roles
        rows = [path_code(i, reverse) for i in range(3)]
        for order in permutations(range(3)):
            encodings.append((branches, tuple(rows[i] for i in order)))
    return min(encodings)


def repair_sets(candidate: Candidate):
    """Minimum segment subdivisions making the lifted core tree-child/simple."""
    roles = candidate.role_map
    children: dict[str, list[tuple[int, str]]] = {v: [] for v in roles}
    for index, segment in enumerate(candidate.segments):
        children[segment.tail].append((index, segment.head))
    obligations: list[set[int]] = []
    for vertex, vertex_role in roles.items():
        if vertex_role in {"S", "T"}:
            good = [i for i, child in children[vertex] if roles[child] in {"S", "T"}]
            if not good:
                obligations.append({i for i, _ in children[vertex]})
        elif vertex_role == "R":
            [(index, child)] = children[vertex]
            if roles[child] in {"R", "X"}:
                obligations.append({index})
    # One of each set of parallel U--V core segments must be subdivided until
    # no two unsubdivided segments have the same unordered endpoint pair.
    parallel: dict[tuple[str, str], list[int]] = {}
    for index, segment in enumerate(candidate.segments):
        key = tuple(sorted((segment.tail, segment.head)))
        parallel.setdefault(key, []).append(index)
    for indices in parallel.values():
        if len(indices) > 1:
            for pair in combinations(indices, 2):
                obligations.append(set(pair))
    valid = []
    for size in range(len(candidate.segments) + 1):
        for selected in combinations(range(len(candidate.segments)), size):
            chosen = set(selected)
            if all(chosen & obligation for obligation in obligations):
                valid.append(selected)
        if valid:
            return tuple(valid)
    raise AssertionError("no repair")


def enumerate_theta():
    raw: list[Candidate] = []
    for branch_roles, events in ((('T', 'T'), ('S', 'X', 'X')), (('T', 'R'), ('S', 'X'))):
        for words in event_path_words(events):
            count = sum(len(word) + 1 for word in words)
            for directions in product((0, 1), repeat=count):
                candidate = instantiate(branch_roles, words, directions)
                if valid_candidate(candidate):
                    raw.append(candidate)
    classes: dict[object, list[Candidate]] = {}
    for candidate in raw:
        classes.setdefault(canonical(candidate), []).append(candidate)
    return raw, classes


def cycle_record():
    # Two parallel directed S-to-X paths before binary subdivisions.
    return {
        "id": "cycle",
        "branch_roles": [],
        "path_event_sequences": [[], []],
        "segments": [
            {"tail": "S", "head": "X", "path": 0, "position": 0},
            {"tail": "S", "head": "X", "path": 1, "position": 0},
        ],
        "minimum_repairs": [[0], [1]],
        "minimum_repair_size": 1,
        "path_template_automorphism_order": 2,
    }


def main() -> None:
    raw, classes = enumerate_theta()
    records = []
    for index, (code, members) in enumerate(sorted(classes.items(), key=lambda x: repr(x[0]))):
        representative = min(members, key=lambda c: repr((c.path_words, c.segments)))
        repairs = repair_sets(representative)
        records.append({
            "id": f"theta-{index}",
            "canonical_template": code,
            "branch_roles": representative.branch_roles,
            "path_event_sequences": representative.path_words,
            "segments": [s.__dict__ for s in representative.segments],
            "minimum_repairs": repairs,
            "minimum_repair_size": len(repairs[0]),
            "raw_members": len(members),
        })
    payload = {
        "schema": 1,
        "method": "exhaustive event allocation and all segment directions",
        "theta_raw_valid_branch_labelled": len(raw),
        "theta_classes": len(classes),
        "cores": [cycle_record(), *records],
        "assertions": {
            "theta_class_count": len(classes) == 4,
            "minimum_repair_multiset": sorted(r["minimum_repair_size"] for r in records) == [1, 2, 2, 2],
        },
    }
    raw_json = json.dumps(payload, sort_keys=True, indent=2) + "\n"
    payload["payload_sha256_without_hash"] = hashlib.sha256(raw_json.encode()).hexdigest()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    if not all(payload["assertions"].values()):
        raise SystemExit("core assertions failed")
    print(json.dumps({
        "output": str(OUT),
        "raw_valid": len(raw),
        "theta_classes": len(classes),
        "minimum_repairs": [r["minimum_repair_size"] for r in records],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
