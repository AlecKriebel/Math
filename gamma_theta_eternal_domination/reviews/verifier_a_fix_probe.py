#!/usr/bin/env python3
"""Adversarial regression for verifier A's graph6 and certificate hardening."""

from __future__ import annotations

import json
import random
import sys
from dataclasses import replace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from verifier_a.core import (  # noqa: E402
    BitGraph,
    EternalResult,
    eternal_fixed_point,
    verify_eternal_result,
)


def require_value_error(record: str | bytes) -> None:
    try:
        BitGraph.from_graph6(record)
    except ValueError:
        return
    raise AssertionError(f"malformed graph6 record was accepted: {record!r}")


def mutate_padding(record: str, order: int) -> str:
    edge_slots = order * (order - 1) // 2
    padding = (-edge_slots) % 6
    if padding == 0:
        raise ValueError("record has no padding bit to mutate")
    last_value = ord(record[-1]) - 63
    if last_value & ((1 << padding) - 1):
        raise AssertionError("writer emitted nonzero padding")
    return record[:-1] + chr(last_value + 1 + 63)


def check_graph6() -> dict[str, object]:
    generator = random.Random(314159)
    valid_records = 0
    short_rejections = 0
    overlong_rejections = 0
    padding_rejections = 0

    for order in range(21):
        graph = BitGraph.from_edges(
            order,
            (
                (first, second)
                for first in range(order)
                for second in range(first + 1, order)
                if generator.random() < 0.43
            ),
        )
        record = graph.to_graph6()
        assert BitGraph.from_graph6(record) == graph
        assert BitGraph.from_graph6(record.encode("ascii")) == graph
        assert BitGraph.from_graph6(">>graph6<<" + record) == graph
        valid_records += 3

        require_value_error(record[:-1])
        short_rejections += 1
        for suffix in ("?", "~"):
            require_value_error(record + suffix)
            require_value_error((">>graph6<<" + record + suffix).encode("ascii"))
            overlong_rejections += 2

        edge_slots = order * (order - 1) // 2
        if edge_slots and edge_slots % 6:
            require_value_error(mutate_padding(record, order))
            padding_rejections += 1

    # Exercise the 18-bit order header at its smallest canonical order.
    extended = BitGraph.edgeless(63)
    extended_record = extended.to_graph6()
    assert extended_record.startswith("~")
    assert BitGraph.from_graph6(extended_record) == extended
    valid_records += 1
    require_value_error(extended_record[:-1])
    short_rejections += 1
    require_value_error(extended_record + "?")
    overlong_rejections += 1
    require_value_error(mutate_padding(extended_record, 63))
    padding_rejections += 1

    for malformed in (
        "",
        ">>graph6<<",
        "~",
        "~?",
        "~??",
        "~~",
        "~~?",
        "~~??",
        "~~???",
        "~~????",
        "~~?????",
        "B",
        "B??",
        "Bw?",
        "??",
        "@?",
        "B@",
        "A@",  # one edge bit followed by nonzero padding
        "Dhc?",  # valid C5 plus one zero payload character
        "Dhc~",  # valid C5 plus one nonzero payload character
        "B ?",
        b"\x00",
        b"\xff",
    ):
        require_value_error(malformed)

    # Remaining input-normalization issue: both size headers below are
    # noncanonical encodings of order zero, yet verifier A accepts them.
    noncanonical_headers: dict[str, str] = {}
    for record in ("~???", "~~??????"):
        try:
            parsed = BitGraph.from_graph6(record)
        except ValueError:
            continue
        noncanonical_headers[record] = parsed.to_graph6()

    return {
        "valid_records_checked": valid_records,
        "short_payloads_rejected": short_rejections,
        "overlong_payloads_rejected": overlong_rejections,
        "nonzero_padding_rejected": padding_rejections,
        "explicit_malformed_records_rejected": 23,
        "noncanonical_order_headers_still_accepted": noncanonical_headers,
    }


def check_certificate() -> dict[str, object]:
    graph = BitGraph.cycle(5)
    valid = eternal_fixed_point(graph, 3)
    assert verify_eternal_result(graph, valid)

    malformed: list[tuple[str, object]] = []
    malformed.extend(
        (
            (f"k={value!r}", replace(valid, k=value))
            for value in (-1, graph.n + 1, True, False, 3.0, "3", None)
        )
    )
    malformed.extend(
        (
            ("empty family", replace(valid, family=())),
            ("noniterable family", replace(valid, family=1)),
            ("unhashable family member", replace(valid, family=([0],))),
            ("boolean configuration", replace(valid, family=(True,))),
            ("negative configuration", replace(valid, family=(-1,))),
            ("out-of-range configuration", replace(valid, family=(1 << graph.n,))),
            ("string configuration", replace(valid, family=("x",))),
            ("responses None", replace(valid, responses=None)),
            ("responses list", replace(valid, responses=[])),
            ("responses tuple", replace(valid, responses=())),
            ("responses string", replace(valid, responses="x")),
        )
    )

    key = next(iter(valid.responses))
    guard, successor = valid.responses[key]

    def changed_response(label: str, response: object) -> None:
        responses = dict(valid.responses)
        responses[key] = response
        malformed.append((label, replace(valid, responses=responses)))

    for bad_guard in (-1, graph.n, True, False, 1.0, "0", None):
        changed_response(f"guard={bad_guard!r}", (bad_guard, successor))
    for bad_successor in (
        -1,
        1 << graph.n,
        True,
        False,
        1.0,
        "0",
        None,
    ):
        changed_response(f"successor={bad_successor!r}", (guard, bad_successor))
    for response in ([], (), (guard,), (guard, successor, 0), "bad", None):
        changed_response(f"response={response!r}", response)

    source, attack = key
    unoccupied_guard = next(
        vertex for vertex in range(graph.n) if not source & (1 << vertex)
    )
    changed_response("in-range guard not occupied", (unoccupied_guard, successor))
    changed_response("wrong in-range successor", (guard, source))

    nonadjacent_case = None
    for candidate_key, candidate_response in valid.responses.items():
        candidate_source, candidate_attack = candidate_key
        for candidate_guard in range(graph.n):
            if (
                candidate_source & (1 << candidate_guard)
                and not graph.adj[candidate_attack] & (1 << candidate_guard)
            ):
                nonadjacent_case = (
                    candidate_key,
                    (candidate_guard, candidate_response[1]),
                )
                break
        if nonadjacent_case is not None:
            break
    assert nonadjacent_case is not None
    responses = dict(valid.responses)
    responses[nonadjacent_case[0]] = nonadjacent_case[1]
    malformed.append(
        ("occupied but nonadjacent guard", replace(valid, responses=responses))
    )

    missing = dict(valid.responses)
    del missing[key]
    malformed.append(("missing response", replace(valid, responses=missing)))
    extra = dict(valid.responses)
    extra[(0, 0)] = (0, 0)
    malformed.append(("extra response", replace(valid, responses=extra)))
    malformed.extend((("not EternalResult", value) for value in (None, {}, (), 1)))

    failures: list[str] = []
    for label, candidate in malformed:
        try:
            accepted = verify_eternal_result(graph, candidate)  # type: ignore[arg-type]
        except BaseException as error:
            failures.append(f"{label}: raised {type(error).__name__}: {error}")
            continue
        if accepted:
            failures.append(f"{label}: accepted")
    if failures:
        raise AssertionError(failures)

    for graph_with_vacuous_responses, guard_count in (
        (BitGraph.edgeless(0), 0),
        (BitGraph.complete(1), 1),
        (BitGraph.complete(4), 4),
    ):
        certificate = eternal_fixed_point(
            graph_with_vacuous_responses, guard_count
        )
        assert verify_eternal_result(graph_with_vacuous_responses, certificate)

    return {
        "valid_certificate_accepted": True,
        "malformed_certificate_cases_rejected_without_exception": len(malformed),
        "vacuous_response_certificates_accepted": 3,
    }


def main() -> None:
    print(
        json.dumps(
            {
                "graph6": check_graph6(),
                "certificate": check_certificate(),
                "outcome": (
                    "requested fixes pass; noncanonical graph6 order headers "
                    "remain accepted"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
