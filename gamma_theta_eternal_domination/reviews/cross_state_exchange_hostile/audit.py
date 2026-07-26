#!/usr/bin/env python3
"""Independent finite audit for the cross-state exchange notes.

This checker deliberately imports no campaign evaluator or search code.
It exhausts all abstract exchange systems through rank three and literally
checks the two displayed one-guard response tables.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]
EXCHANGE_NOTE = CAMPAIGN / "math/working/cross_state_response_exchange.md"
ORDER_NOTE = (
    CAMPAIGN / "math/working/cross_state_base_orderability_obstruction.md"
)
OUTPUT = HERE / "evidence.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_graph6(record: str) -> tuple[frozenset[int], ...]:
    data = record.encode("ascii")
    if not data or data[0] < 63 or data[0] > 125:
        raise ValueError("only short graph6 records are supported")
    order = data[0] - 63
    bits: list[int] = []
    for byte in data[1:]:
        value = byte - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    graph = [set() for _ in range(order)]
    position = 0
    for high in range(1, order):
        for low in range(high):
            if bits[position]:
                graph[low].add(high)
                graph[high].add(low)
            position += 1
    return tuple(frozenset(row) for row in graph)


def edge_set(graph: tuple[frozenset[object], ...] | dict[object, set[object]]):
    if isinstance(graph, tuple):
        return {
            frozenset((u, v))
            for u, row in enumerate(graph)
            for v in row
            if u != v
        }
    return {
        frozenset((u, v))
        for u, row in graph.items()
        for v in row
        if u != v
    }


def vertices(graph):
    return set(range(len(graph))) if isinstance(graph, tuple) else set(graph)


def neighborhood(graph, vertex):
    return set(graph[vertex])


def dominates(graph, state: frozenset[object]) -> bool:
    covered = set(state)
    for guard in state:
        covered.update(neighborhood(graph, guard))
    return vertices(graph) <= covered


def independent(graph, state: frozenset[object]) -> bool:
    return all(
        second not in neighborhood(graph, first)
        for first, second in itertools.combinations(state, 2)
    )


def domination_number(graph) -> int:
    domain = sorted(vertices(graph), key=str)
    for size in range(len(domain) + 1):
        if any(
            dominates(graph, frozenset(state))
            for state in itertools.combinations(domain, size)
        ):
            return size
    raise AssertionError("full vertex set must dominate")


def independence_number(graph) -> int:
    domain = sorted(vertices(graph), key=str)
    for size in range(len(domain), -1, -1):
        if any(
            independent(graph, frozenset(state))
            for state in itertools.combinations(domain, size)
        ):
            return size
    raise AssertionError("empty set must be independent")


def independent_domination_number(graph) -> int:
    domain = sorted(vertices(graph), key=str)
    for size in range(len(domain) + 1):
        for state in itertools.combinations(domain, size):
            candidate = frozenset(state)
            if independent(graph, candidate) and dominates(graph, candidate):
                return size
    raise AssertionError("a maximal independent set must exist")


def complement(graph):
    domain = sorted(vertices(graph), key=str)
    return {
        vertex: set(domain) - {vertex} - neighborhood(graph, vertex)
        for vertex in domain
    }


def colorable(graph, color_count: int) -> bool:
    domain = sorted(vertices(graph), key=str)
    assignment: dict[object, int] = {}

    def search() -> bool:
        if len(assignment) == len(domain):
            return True
        unassigned = [v for v in domain if v not in assignment]
        vertex = max(
            unassigned,
            key=lambda v: (
                len({assignment[n] for n in neighborhood(graph, v) if n in assignment}),
                len(neighborhood(graph, v)),
            ),
        )
        blocked = {
            assignment[neighbor]
            for neighbor in neighborhood(graph, vertex)
            if neighbor in assignment
        }
        for color in range(color_count):
            if color in blocked:
                continue
            assignment[vertex] = color
            if search():
                return True
            del assignment[vertex]
        return False

    return search()


def clique_cover_number(graph) -> int:
    target = complement(graph)
    for count in range(1, len(vertices(graph)) + 1):
        if colorable(target, count):
            return count
    raise AssertionError("one color per vertex must work")


def greatest_family(graph, guard_count: int) -> frozenset[frozenset[object]]:
    domain = sorted(vertices(graph), key=str)
    family = frozenset(
        frozenset(state)
        for state in itertools.combinations(domain, guard_count)
        if dominates(graph, frozenset(state))
    )
    while family:
        retained = frozenset(
            state
            for state in family
            if all(
                any(
                    state - {guard} | {attack} in family
                    for guard in state & neighborhood(graph, attack)
                )
                for attack in vertices(graph) - state
            )
        )
        if retained == family:
            return family
        family = retained
    return frozenset()


def eternal_domination_number(graph) -> int:
    for size in range(1, len(vertices(graph)) + 1):
        if greatest_family(graph, size):
            return size
    raise AssertionError("all vertices form an eternal family")


def parse_state(token: str, numeric: bool) -> frozenset[object]:
    return frozenset(int(char) if numeric else char for char in token)


def parse_response_table(raw: str, numeric: bool):
    table = {}
    for line in raw.strip().splitlines():
        fields = line.split()
        state = parse_state(fields[0], numeric)
        responses = {}
        for field in fields[1:]:
            attack_text, move = field.split(":")
            guard_text, successor_text = move.split(">")
            attack = int(attack_text) if numeric else attack_text
            guard = int(guard_text) if numeric else guard_text
            responses[attack] = (
                guard,
                parse_state(successor_text, numeric),
            )
        table[state] = responses
    return table


def audit_response_table(graph, family, raw: str, numeric: bool):
    table = parse_response_table(raw, numeric)
    assert set(table) == set(family)
    obligations = 0
    for state in family:
        assert len(state) == 3
        assert dominates(graph, state)
        attacks = vertices(graph) - state
        assert set(table[state]) == attacks
        for attack, (guard, successor) in table[state].items():
            obligations += 1
            assert attack not in state
            assert guard in state
            assert attack in neighborhood(graph, guard)
            assert successor == state - {guard} | {attack}
            assert successor in family
            assert dominates(graph, successor)
    return obligations


def abstract_states(rank: int):
    return [
        (sum(1 << a for a in removed), sum(1 << b for b in inserted))
        for level in range(rank + 1)
        for removed in itertools.combinations(range(rank), level)
        for inserted in itertools.combinations(range(rank), level)
    ]


def exchange_axioms_hold(system: frozenset[tuple[int, int]], rank: int) -> bool:
    full = (1 << rank) - 1
    if (0, 0) not in system or (full, full) not in system:
        return False
    for removed, inserted in system:
        for b in range(rank):
            if inserted & (1 << b):
                continue
            if not any(
                not removed & (1 << a)
                and (removed | (1 << a), inserted | (1 << b)) in system
                for a in range(rank)
            ):
                return False
        for a in range(rank):
            if not removed & (1 << a):
                continue
            if not any(
                inserted & (1 << b)
                and (removed & ~(1 << a), inserted & ~(1 << b)) in system
                for b in range(rank)
            ):
                return False
    return True


def base_ordering(system: frozenset[tuple[int, int]], rank: int):
    for permutation in itertools.permutations(range(rank)):
        holds = True
        for removed in range(1 << rank):
            inserted = sum(
                1 << permutation[a]
                for a in range(rank)
                if removed & (1 << a)
            )
            if (removed, inserted) not in system:
                holds = False
                break
        if holds:
            return permutation
    return None


def enumerate_abstract(rank: int):
    full = (1 << rank) - 1
    endpoint = {(0, 0), (full, full)}
    middle = [
        state
        for state in abstract_states(rank)
        if state not in endpoint
    ]
    valid = 0
    nonbase = 0
    nonbase_sizes: Counter[int] = Counter()
    for mask in range(1 << len(middle)):
        system = frozenset(
            endpoint
            | {
                state
                for index, state in enumerate(middle)
                if mask & (1 << index)
            }
        )
        if not exchange_axioms_hold(system, rank):
            continue
        valid += 1
        if base_ordering(system, rank) is None:
            nonbase += 1
            nonbase_sizes[len(system)] += 1
    return {
        "middle_state_slots": len(middle),
        "valid_systems": valid,
        "non_base_orderable_systems": nonbase,
        "non_base_orderable_size_histogram": {
            str(size): count for size, count in sorted(nonbase_sizes.items())
        },
        "minimum_non_base_orderable_size": (
            min(nonbase_sizes) if nonbase_sizes else None
        ),
    }


K_TABLE = """
abc x:b>acx y:a>bcy z:a>bcz
abx c:x>abc y:a>bxy z:b>axz
acx b:x>abc y:c>axy z:a>cxz
acy b:y>abc x:c>axy z:a>cyz
axy b:y>abx c:x>acy z:a>xyz
axz b:z>abx c:z>acx y:a>xyz
bcy a:y>abc x:c>bxy z:b>cyz
bcz a:z>abc x:b>cxz y:b>cyz
bxy a:y>abx c:x>bcy z:b>xyz
cxz a:z>acx b:x>bcz y:c>xyz
cyz a:z>acy b:y>bcz x:c>xyz
xyz a:y>axz b:z>bxy c:x>cyz
"""

FC_TABLE = """
012 3:0>123 4:2>014 5:1>025 6:2>016
014 2:4>012 3:0>134 5:1>045 6:4>016
016 2:6>012 3:0>136 4:6>014 5:1>056
024 1:4>012 3:0>234 5:2>045 6:4>026
025 1:5>012 3:0>235 4:2>045 6:2>056
026 1:6>012 3:0>236 4:6>024 5:2>056
045 1:5>014 2:5>024 3:0>345 6:4>056
056 1:5>016 2:6>025 3:0>356 4:6>045
123 0:3>012 4:2>134 5:1>235 6:2>136
134 0:3>014 2:4>123 5:1>345 6:4>136
136 0:3>016 2:6>123 4:6>134 5:1>356
234 0:3>024 1:4>123 5:2>345 6:4>236
235 0:3>025 1:5>123 4:2>345 6:2>356
236 0:3>026 1:6>123 4:6>234 5:2>356
345 0:3>045 1:5>134 2:5>234 6:4>356
356 0:3>056 1:5>136 2:6>235 4:6>345
"""


def main() -> None:
    part_a = set("abc")
    part_b = set("xyz")
    k_graph = {vertex: set() for vertex in part_a | part_b}
    for first in part_a:
        for second in part_b:
            if {first, second} == {"a", "x"}:
                continue
            k_graph[first].add(second)
            k_graph[second].add(first)
    k_family = frozenset(parse_state(line.split()[0], False) for line in K_TABLE.strip().splitlines())
    k_obligations = audit_response_table(k_graph, k_family, K_TABLE, False)

    e_relation = {(0, 1), (0, 2), (1, 0), (1, 1), (2, 0)}
    f_relation = {(0, 1), (0, 2), (1, 2), (2, 0), (2, 1)}
    q0 = {(0, 0), (7, 7)}
    q0 |= {(1 << a, 1 << b) for a, b in e_relation}
    q0 |= {(7 & ~(1 << a), 7 & ~(1 << b)) for a, b in f_relation}
    q0 = frozenset(q0)
    assert len(q0) == 12
    assert exchange_axioms_hold(q0, 3)
    assert base_ordering(q0, 3) is None
    assert not any(
        all((a, permutation[a]) in e_relation & f_relation for a in range(3))
        for permutation in itertools.permutations(range(3))
    )

    fc_graph = decode_graph6("FCXfO")
    expected_fc_edges = {
        frozenset(edge)
        for edge in [
            (0, 3), (0, 6), (1, 4), (1, 5), (1, 6),
            (2, 4), (2, 5), (2, 6), (4, 6),
        ]
    }
    assert edge_set(fc_graph) == expected_fc_edges
    fc_family = frozenset(parse_state(line.split()[0], True) for line in FC_TABLE.strip().splitlines())
    fc_obligations = audit_response_table(fc_graph, fc_family, FC_TABLE, True)

    witness_tokens = """
    01:2 02:1 03:1 04:5 05:4 06:5 12:0
    13:2 14:0 15:0 16:3 23:1 24:0 25:0
    26:3 34:5 35:4 36:5 45:0 46:3 56:3
    """.split()
    pair_witnesses = {
        frozenset(map(int, pair)): int(witness)
        for token in witness_tokens
        for pair, witness in [token.split(":")]
    }
    all_pairs = {
        frozenset(pair) for pair in itertools.combinations(range(7), 2)
    }
    assert set(pair_witnesses) == all_pairs
    for pair, witness in pair_witnesses.items():
        assert witness not in pair
        assert not (set(pair) & set(fc_graph[witness]))
        assert not dominates(fc_graph, pair)

    fc_greatest_three = greatest_family(fc_graph, 3)
    state_135 = frozenset({1, 3, 5})
    assert state_135 not in fc_family
    assert state_135 in fc_greatest_three
    source = frozenset({0, 1, 2})
    target = frozenset({3, 4, 5})
    assert source - {1} | {4} in fc_family
    assert target - {4} | {1} not in fc_family
    phi = {0: 3, 1: 5, 2: 4}
    cube = {
        source - set(removed) | {phi[u] for u in removed}
        for size in range(4)
        for removed in itertools.combinations(source, size)
    }
    assert cube <= fc_family

    abstract = {
        str(rank): enumerate_abstract(rank) for rank in (1, 2, 3)
    }
    assert abstract["1"]["non_base_orderable_systems"] == 0
    assert abstract["2"]["non_base_orderable_systems"] == 0
    assert abstract["3"]["minimum_non_base_orderable_size"] == 12

    k_parameters = {
        "gamma": domination_number(k_graph),
        "i": independent_domination_number(k_graph),
        "alpha": independence_number(k_graph),
        "gamma_infinity": eternal_domination_number(k_graph),
        "theta": clique_cover_number(k_graph),
    }
    fc_parameters = {
        "gamma": domination_number(fc_graph),
        "i": independent_domination_number(fc_graph),
        "alpha": independence_number(fc_graph),
        "gamma_infinity": eternal_domination_number(fc_graph),
        "theta": clique_cover_number(fc_graph),
    }
    assert k_parameters == {
        "gamma": 2, "i": 2, "alpha": 3, "gamma_infinity": 3, "theta": 3
    }
    assert fc_parameters == {
        "gamma": 3, "i": 3, "alpha": 3, "gamma_infinity": 3, "theta": 3
    }

    result = {
        "schema": "cross-state-exchange-hostile-audit-v1",
        "status": "PASS",
        "source_bindings": {
            str(EXCHANGE_NOTE.relative_to(CAMPAIGN)): sha256(EXCHANGE_NOTE),
            str(ORDER_NOTE.relative_to(CAMPAIGN)): sha256(ORDER_NOTE),
        },
        "checker": {
            "path": str(Path(__file__).relative_to(CAMPAIGN)),
            "sha256": sha256(Path(__file__)),
            "imports_campaign_evaluator": False,
        },
        "abstract_exhaustion": abstract,
        "q0": {
            "state_count": len(q0),
            "exchange_axioms": True,
            "base_orderable": False,
            "response_obligations_checked": k_obligations,
        },
        "K3_3_minus_edge": {
            "parameters": k_parameters,
            "family_state_count": len(k_family),
            "literal_response_obligations_checked": k_obligations,
            "all_states_dominate": True,
        },
        "FCXfO": {
            "graph6_edge_set_matches_note": True,
            "parameters": fc_parameters,
            "family_state_count": len(fc_family),
            "literal_response_obligations_checked": fc_obligations,
            "all_21_no_dominating_pair_witnesses_checked": True,
            "nonreciprocal_exchange_checked": True,
            "displayed_base_ordering_checked": True,
            "greatest_three_family_size": len(fc_greatest_three),
            "chosen_family_is_strict_subfamily": fc_family < fc_greatest_three,
            "state_135_in_greatest_but_not_chosen_family": True,
        },
        "interpretation": {
            "proved": (
                "The note's symbolic proofs establish the universal exchange, "
                "ridge-covariance, and rank-minimality statements."
            ),
            "certified_finite": (
                "This checker independently exhausts ranks <=3 and checks the "
                "two displayed finite response/parameter certificates."
            ),
            "observed": (
                "The separate ordinary-set n<=8 probe is supporting finite "
                "evidence only and is not used to prove the universal theorems."
            ),
            "open": (
                "Base-orderability for every pair of independent triples in "
                "an equality graph's arbitrary eternal family remains open."
            ),
        },
    }
    OUTPUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
