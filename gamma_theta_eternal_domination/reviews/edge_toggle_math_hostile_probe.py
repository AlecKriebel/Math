#!/usr/bin/env python3
"""Standalone hostile replay of the edge-toggle mathematical certificate.

This probe intentionally imports no campaign package.  It decodes graph6,
checks domination, and computes the one-guard greatest fixed point with
frozenset configurations and ordinary set operations.
"""

from __future__ import annotations

import csv
from hashlib import sha256
from itertools import combinations, zip_longest
import json
from math import comb
from pathlib import Path
import sqlite3
import time


ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "results/checkpoints/edge_toggles.sqlite3"
CHECKPOINT = ROOT / "results/checkpoints/edge_toggles.json"
PROVENANCE = ROOT / "results/edge_toggles_provenance.csv"
UNIQUE = ROOT / "results/edge_toggles_unique.csv"
COVERAGE = ROOT / "results/edge_toggle_coverage_audit.json"
CERTIFICATE = ROOT / "results/edge_toggle_third_evaluation_certificates.ndjson"
REPORT = ROOT / "results/edge_toggle_third_evaluation_audit.json"
PARSER = ROOT / "src/coverage_checker/graph.py"

EXPECTED_ROWS = 19_136
EXPECTED_ORIGINS = 25_641
EXPECTED_HASHES = {
    "database": "2a6349452906cf2904a5e9e6284806f603619ad28ec66fa63fc383f2b833b258",
    "checkpoint": "f00b404fdfc09ac95f8b56325ef58a3399559b33eb1b659e304fdc81ed512ffc",
    "provenance": "378e867d5ec0d419f668f5169dbac6f2319cd2afc9ce3c5f63da2b9677dccba5",
    "unique": "a32505df6ba67479b5908a91711d21babb14fd8ac50cdfd0f0b92fc1001d4319",
    "coverage": "82c6918faec2105340205730a3e128d4be05b5c57190a58519e68b4cfe733679",
    "certificate": "b31eee468a8a45e0534fece7b54cb142ff126fb1f9155db5bbea98acaa948435",
    "report": "8877262c2ece90448106630b7e71909f3e39e4887f2455b5d1f089db1346b809",
    "parser": "cb60b10295aaa1e0a723e9fb3b1ecf497c461082bdcc8066044a664b4d76e731",
}
EXPECTED_BINDING = "b1a1fc061d973db9f90830427d0d7905b135f507abdb827afd7907abe52ea2de"
EXPECTED_SOURCE_SET = (
    "b2ba9d7a5e549e4da88542badf2d9948a54571dad925ad7f30ef89118574d76d"
)
EXPECTED_COVERAGE_BINDING = (
    "e5d78a868397589e11cf87ed5e248d6ee03bde452c01b7fc3d260f2999b181d9"
)
EXPECTED_ORIGIN_CHAIN = (
    "d00dff4e6e0ad40b37e14da89c5deb2616ed10e39b08c81b1d5837723df1f5bb"
)
EXPECTED_ROW_STREAM = (
    "fc929585dd5b9096dc9dca262093d2fc4f02e5784fc66f0e8ab39ec5f23336a3"
)

UNIQUE_HEADER = (
    "canonical_graph6",
    "n",
    "m",
    "connected",
    "origin_count",
    "first_seed_id",
    "first_pair_index",
    "first_raw_graph6",
    "gamma_a",
    "gamma_b",
    "alpha_a",
    "alpha_b",
    "gamma_infinity_a",
    "gamma_infinity_b",
    "theta_a",
    "theta_b",
    "category",
    "family_size",
    "family_sha256",
)
ROW_KEYS = {
    "deletion_rounds",
    "deletion_trace_sha256",
    "dominating_witness_mask",
    "gamma",
    "graph6",
    "initial_dominating_configurations",
    "ledger_row_sha256",
    "lower_blockers",
    "row_index",
    "type",
}


class ProbeError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ProbeError(message)


def file_sha(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def strict_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        require(isinstance(key, str) and key not in result, "duplicate JSON key")
        result[key] = value
    return result


def reject_constant(value: str) -> object:
    raise ProbeError(f"non-finite JSON constant {value}")


def parse_json_bytes(line: bytes, label: str) -> object:
    require(line.endswith(b"\n") and line not in (b"\n", b"\r\n"), f"{label}: line")
    try:
        text = line.decode("ascii")
        value = json.loads(
            text,
            object_pairs_hook=strict_pairs,
            parse_constant=reject_constant,
        )
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ProbeError(f"{label}: malformed JSON") from error
    require(canonical_line(value) == line, f"{label}: noncanonical JSON")
    return value


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def canonical_line(value: object) -> bytes:
    return canonical_bytes(value) + b"\n"


def object_digest(value: object) -> str:
    return sha256(canonical_bytes(value)).hexdigest()


def read_strict_json(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    require(raw.endswith(b"\n"), f"{path.name}: missing final newline")
    try:
        value = json.loads(
            raw.decode("ascii"),
            object_pairs_hook=strict_pairs,
            parse_constant=reject_constant,
        )
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ProbeError(f"{path.name}: malformed JSON") from error
    require(isinstance(value, dict), f"{path.name}: root is not object")
    return value


def decode_graph6(record: str) -> tuple[int, tuple[frozenset[int], ...]]:
    require(isinstance(record, str), "graph6 is not text")
    try:
        raw = record.encode("ascii")
    except UnicodeEncodeError as error:
        raise ProbeError("graph6 is not ASCII") from error
    require(raw and not raw.startswith(b">>graph6<<"), "noncanonical graph6 header")
    require(raw[0] != 126 and 63 <= raw[0] <= 125, "graph6 order byte")
    order = raw[0] - 63
    require(0 <= order <= 12, "graph6 order outside bounded universe")
    bit_count = order * (order - 1) // 2
    payload_count = (bit_count + 5) // 6
    require(len(raw) == payload_count + 1, "graph6 payload length")
    payload = raw[1:]
    require(all(63 <= byte <= 126 for byte in payload), "graph6 payload byte")
    padding = payload_count * 6 - bit_count
    if padding:
        require(((payload[-1] - 63) & ((1 << padding) - 1)) == 0, "graph6 padding")

    adjacency = [set() for _ in range(order)]
    position = 0
    for second in range(1, order):
        for first in range(second):
            value = payload[position // 6] - 63
            if (value >> (5 - position % 6)) & 1:
                adjacency[first].add(second)
                adjacency[second].add(first)
            position += 1
    graph = tuple(frozenset(row) for row in adjacency)
    require(encode_graph6(graph) == record, "graph6 round trip")
    return order, graph


def encode_graph6(graph: tuple[frozenset[int], ...]) -> str:
    order = len(graph)
    bits: list[int] = []
    for second in range(1, order):
        for first in range(second):
            bits.append(int(second in graph[first]))
    while len(bits) % 6:
        bits.append(0)
    output = bytearray([order + 63])
    for offset in range(0, len(bits), 6):
        value = 0
        for bit in bits[offset : offset + 6]:
            value = (value << 1) | bit
        output.append(value + 63)
    return output.decode("ascii")


def edge_count(graph: tuple[frozenset[int], ...]) -> int:
    return sum(map(len, graph)) // 2


def is_connected(graph: tuple[frozenset[int], ...]) -> bool:
    if not graph:
        return False
    reached = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for neighbor in graph[vertex] - reached:
            reached.add(neighbor)
            frontier.append(neighbor)
    return len(reached) == len(graph)


def dominates(
    graph: tuple[frozenset[int], ...], state: frozenset[int]
) -> bool:
    covered = set(state)
    for guard in state:
        covered.update(graph[guard])
    return len(covered) == len(graph)


def state_mask(state: frozenset[int]) -> int:
    return sum(1 << vertex for vertex in state)


def independent_gamma(
    graph: tuple[frozenset[int], ...],
) -> tuple[int, frozenset[int]]:
    vertices = range(len(graph))
    for size in (1, 2, 3):
        for values in combinations(vertices, size):
            state = frozenset(values)
            if dominates(graph, state):
                return size, state
    raise ProbeError("independent gamma is not in {1,2,3}")


def independent_empty_gfp(
    graph: tuple[frozenset[int], ...], guard_count: int
) -> tuple[int, list[list[list[int]]]]:
    vertices = frozenset(range(len(graph)))
    active = {
        frozenset(values)
        for values in combinations(range(len(graph)), guard_count)
        if dominates(graph, frozenset(values))
    }
    initial = len(active)
    rounds: list[list[list[int]]] = []
    while active:
        frozen = frozenset(active)
        doomed: list[list[int]] = []
        for state in sorted(frozen, key=state_mask):
            for attacked in sorted(vertices - state):
                response = False
                for guard in sorted(state):
                    if attacked not in graph[guard]:
                        continue
                    successor = frozenset((state - {guard}) | {attacked})
                    require(len(successor) == guard_count, "successor cardinality")
                    if successor in frozen and dominates(graph, successor):
                        response = True
                        break
                if not response:
                    doomed.append([state_mask(state), attacked])
                    break
        if not doomed:
            break
        rounds.append(doomed)
        active.difference_update(
            frozenset(
                vertex
                for vertex in range(len(graph))
                if mask & (1 << vertex)
            )
            for mask, _ in doomed
        )
    require(not active, "independent greatest fixed point is nonempty")
    return initial, rounds


def trace_digest(rounds: list[list[list[int]]]) -> str:
    digest = sha256()
    for round_index, records in enumerate(rounds):
        for state, attacked in records:
            digest.update(
                json.dumps(
                    [round_index, state, attacked],
                    separators=(",", ":"),
                ).encode("ascii")
                + b"\n"
            )
    return digest.hexdigest()


def csv_form(value: object) -> str:
    if value is None:
        return ""
    if type(value) is int:
        return str(value)
    require(isinstance(value, str), "unexpected SQLite value type")
    return value


def validate_blockers(
    graph: tuple[frozenset[int], ...],
    gamma: int,
    value: object,
) -> None:
    require(isinstance(value, list), "blockers not array")
    expected = list(combinations(range(len(graph)), gamma - 1))
    require(len(value) == len(expected) == comb(len(graph), gamma - 1), "blocker count")
    for vertices, record in zip(expected, value, strict=True):
        require(
            isinstance(record, list)
            and len(record) == 2
            and all(type(item) is int for item in record),
            "blocker shape",
        )
        subset = frozenset(vertices)
        mask, witness = record
        require(mask == state_mask(subset), "blocker subset order")
        require(0 <= witness < len(graph) and witness not in subset, "blocker witness")
        require(not (graph[witness] & subset), "blocker witness is adjacent")
        require(not dominates(graph, subset), "blocker subset dominates")


def main() -> None:
    started = time.monotonic()
    paths = {
        "database": DATABASE,
        "checkpoint": CHECKPOINT,
        "provenance": PROVENANCE,
        "unique": UNIQUE,
        "coverage": COVERAGE,
        "certificate": CERTIFICATE,
        "report": REPORT,
        "parser": PARSER,
    }
    actual_hashes = {name: file_sha(path) for name, path in paths.items()}
    require(actual_hashes == EXPECTED_HASHES, "frozen artifact hash differs")
    for suffix in ("-wal", "-shm", "-journal"):
        require(not Path(str(DATABASE) + suffix).exists(), "live SQLite companion")

    checkpoint = read_strict_json(CHECKPOINT)
    coverage = read_strict_json(COVERAGE)
    report = read_strict_json(REPORT)
    require(checkpoint.get("status") == "complete", "checkpoint incomplete")
    require(checkpoint.get("raw_expected") == EXPECTED_ORIGINS, "checkpoint expected")
    require(checkpoint.get("raw_processed") == EXPECTED_ORIGINS, "checkpoint processed")
    require(checkpoint.get("candidate_reference") is None, "checkpoint candidate")
    candidate_state = checkpoint.get("candidate_state")
    require(
        isinstance(candidate_state, dict) and candidate_state.get("pending") is False,
        "checkpoint pending candidate",
    )
    require(
        coverage.get("passed") is True
        and coverage.get("verified_origins") == EXPECTED_ORIGINS
        and coverage.get("unique_canonical_graphs") == EXPECTED_ROWS
        and coverage.get("binding_sha256") == EXPECTED_COVERAGE_BINDING
        and coverage.get("origin_chain_sha256") == EXPECTED_ORIGIN_CHAIN,
        "coverage report summary",
    )
    require(
        report.get("status") == "complete"
        and report.get("passed") is True
        and report.get("binding_sha256") == EXPECTED_BINDING
        and report.get("certificate_sha256") == EXPECTED_HASHES["certificate"],
        "mathematical report summary",
    )
    report_binding = report.get("binding")
    require(isinstance(report_binding, dict), "report binding absent")
    require(
        report_binding.get("checker_source_set_sha256") == EXPECTED_SOURCE_SET,
        "source-set binding",
    )
    require(
        report_binding.get("coverage_binding_sha256") == EXPECTED_COVERAGE_BINDING,
        "coverage binding in math report",
    )
    require(
        report_binding.get("coverage_origin_chain_sha256") == EXPECTED_ORIGIN_CHAIN,
        "coverage origin chain in math report",
    )

    uri = DATABASE.resolve().as_uri() + "?mode=ro&immutable=1"
    connection = sqlite3.connect(uri, uri=True)
    connection.execute("PRAGMA query_only=ON")
    try:
        require(
            connection.execute("PRAGMA integrity_check").fetchall() == [("ok",)],
            "SQLite integrity",
        )
        require(
            connection.execute("PRAGMA foreign_key_check").fetchall() == [],
            "SQLite foreign keys",
        )
        aggregate = connection.execute(
            """
            SELECT COUNT(*), COUNT(DISTINCT graph6), SUM(origin_count),
                   MIN(n), MAX(n), COUNT(DISTINCT category)
            FROM canonical_graphs
            """
        ).fetchone()
        require(
            aggregate == (EXPECTED_ROWS, EXPECTED_ROWS, EXPECTED_ORIGINS, 11, 12, 1),
            "canonical ledger aggregate",
        )
        origin_aggregate = connection.execute(
            """
            SELECT COUNT(*), COUNT(DISTINCT seed_id || ':' || pair_index)
            FROM origins
            """
        ).fetchone()
        require(
            origin_aggregate == (EXPECTED_ORIGINS, EXPECTED_ORIGINS),
            "origin-key uniqueness",
        )
        require(
            connection.execute(
                "SELECT DISTINCT category FROM canonical_graphs"
            ).fetchall()
            == [("gamma_below_eternal",)],
            "unexpected category",
        )

        query = """
            SELECT graph6, n, m, connected, origin_count, first_seed_id,
                   first_pair_index, first_raw_graph6, gamma_a, gamma_b,
                   alpha_a, alpha_b, gamma_infinity_a, gamma_infinity_b,
                   theta_a, theta_b, category, family_size, family_sha256
            FROM canonical_graphs ORDER BY n, graph6
        """
        cursor = connection.execute(query)
        row_digest = sha256()
        rows = 0
        origins = 0
        gamma_two = 0
        gamma_three = 0
        initial_total = 0
        deletion_round_total = 0
        maximum_initial = 0
        maximum_rounds = 0
        census: dict[str, int] = {}
        previous_key: tuple[int, str] | None = None

        with UNIQUE.open("r", encoding="utf-8", newline="") as csv_handle, (
            CERTIFICATE.open("rb")
        ) as certificate_handle:
            csv_reader = csv.reader(csv_handle, strict=True)
            require(tuple(next(csv_reader)) == UNIQUE_HEADER, "unique CSV header")
            header_line = certificate_handle.readline()
            header = parse_json_bytes(header_line, "certificate header")
            require(
                isinstance(header, dict)
                and header.get("type") == "header"
                and header.get("expected_rows") == EXPECTED_ROWS
                and header.get("binding_sha256") == EXPECTED_BINDING
                and header.get("binding") == report_binding,
                "certificate header binding",
            )

            sentinel = object()
            for database_row, csv_row in zip_longest(
                cursor, csv_reader, fillvalue=sentinel
            ):
                require(database_row is not sentinel, "CSV has extra row")
                require(csv_row is not sentinel, "CSV is truncated")
                require(isinstance(database_row, tuple), "SQLite row type")
                require(isinstance(csv_row, list), "CSV row type")
                require(
                    tuple(csv_row) == tuple(map(csv_form, database_row)),
                    f"CSV/database mismatch at {rows}",
                )

                graph6 = database_row[0]
                order = database_row[1]
                require(isinstance(graph6, str) and type(order) is int, "ledger types")
                key = (order, graph6)
                require(previous_key is None or previous_key < key, "ledger order/unique")
                previous_key = key
                decoded_order, graph = decode_graph6(graph6)
                require(decoded_order == order, f"order mismatch at {rows}")
                require(edge_count(graph) == database_row[2], f"size mismatch at {rows}")
                require(database_row[3] == 1 and is_connected(graph), f"connected at {rows}")
                require(type(database_row[4]) is int and database_row[4] >= 1, "origins")
                require(
                    database_row[8] == database_row[9]
                    and database_row[10] == database_row[11]
                    and database_row[12] == database_row[13]
                    and database_row[14] == database_row[15],
                    f"stored evaluator disagreement at {rows}",
                )
                require(database_row[16] == "gamma_below_eternal", "category logic")

                record_line = certificate_handle.readline()
                require(record_line, f"certificate truncated at row {rows}")
                record = parse_json_bytes(record_line, f"certificate row {rows}")
                require(isinstance(record, dict) and set(record) == ROW_KEYS, "row keys")
                require(
                    record.get("type") == "row"
                    and record.get("row_index") == rows
                    and record.get("graph6") == graph6
                    and record.get("ledger_row_sha256")
                    == object_digest(list(database_row)),
                    f"row binding at {rows}",
                )

                gamma, witness = independent_gamma(graph)
                require(gamma in (2, 3), f"gamma target at {rows}")
                require(
                    record.get("gamma") == gamma
                    and database_row[8] == gamma
                    and database_row[12] > gamma,
                    f"gamma/category reconciliation at {rows}",
                )
                witness_mask = record.get("dominating_witness_mask")
                require(type(witness_mask) is int, "dominating witness type")
                witness_state = frozenset(
                    vertex
                    for vertex in range(order)
                    if witness_mask & (1 << vertex)
                )
                require(
                    witness_mask >= 0
                    and witness_mask < (1 << order)
                    and len(witness_state) == gamma
                    and dominates(graph, witness_state),
                    f"dominating witness at {rows}",
                )
                require(dominates(graph, witness), "independent gamma witness")
                validate_blockers(graph, gamma, record.get("lower_blockers"))

                initial, independent_rounds = independent_empty_gfp(graph, gamma)
                require(
                    record.get("initial_dominating_configurations") == initial,
                    f"initial family at {rows}",
                )
                require(
                    record.get("deletion_rounds") == independent_rounds,
                    f"simultaneous deletion trace at {rows}",
                )
                require(
                    record.get("deletion_trace_sha256")
                    == trace_digest(independent_rounds),
                    f"trace hash at {rows}",
                )
                require(
                    sum(len(round_) for round_ in independent_rounds) == initial,
                    f"empty terminal at {rows}",
                )

                row_digest.update(record_line)
                rows += 1
                origins += database_row[4]
                gamma_two += gamma == 2
                gamma_three += gamma == 3
                initial_total += initial
                deletion_round_total += len(independent_rounds)
                maximum_initial = max(maximum_initial, initial)
                maximum_rounds = max(maximum_rounds, len(independent_rounds))
                parameter_key = (
                    f"gamma={database_row[8]},alpha={database_row[10]},"
                    f"gamma_infinity={database_row[12]},theta={database_row[14]},"
                    f"category={database_row[16]}"
                )
                census[parameter_key] = census.get(parameter_key, 0) + 1

            footer_line = certificate_handle.readline()
            footer = parse_json_bytes(footer_line, "certificate footer")
            require(not certificate_handle.read(1), "certificate trailing content")

        summary = {
            "rows": rows,
            "origins": origins,
            "gamma_2_rows": gamma_two,
            "gamma_3_rows": gamma_three,
            "initial_dominating_configurations": initial_total,
            "deletion_rounds": deletion_round_total,
            "deletion_records": initial_total,
            "maximum_initial_configurations": maximum_initial,
            "maximum_deletion_rounds": maximum_rounds,
            "row_stream_sha256": row_digest.hexdigest(),
            "stored_parameter_census": dict(sorted(census.items())),
        }
        require(rows == EXPECTED_ROWS and origins == EXPECTED_ORIGINS, "universe size")
        require(row_digest.hexdigest() == EXPECTED_ROW_STREAM, "row stream digest")
        require(
            footer
            == {
                "format": "gamma-theta-edge-toggle-third-math-certificates-v1",
                "summary": summary,
                "type": "footer",
            },
            "certificate footer",
        )
        require(report.get("summary") == summary, "report/certificate summary")
    finally:
        connection.close()

    print(
        json.dumps(
            {
                "status": "accepted",
                "independent_model": (
                    "frozenset configurations; unoccupied attacks; exactly one "
                    "adjacent guard; dominating active successor; simultaneous GFP"
                ),
                "rows": EXPECTED_ROWS,
                "origins": EXPECTED_ORIGINS,
                "certificate_sha256": EXPECTED_HASHES["certificate"],
                "report_sha256": EXPECTED_HASHES["report"],
                "row_stream_sha256": EXPECTED_ROW_STREAM,
                "wall_seconds": time.monotonic() - started,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
