#!/usr/bin/env python3
"""Independent hostile probe for the frozen extension-coverage artifact.

This file intentionally imports no campaign package.  It checks the completed
production ledger with a separately written graph6 codec and verifies every
stored raw-to-canonical permutation directly.  It is read-only: no production
artifact is opened for writing.
"""

from __future__ import annotations

import csv
from hashlib import sha256
from itertools import zip_longest
import json
from pathlib import Path
import sqlite3
from typing import Iterable, Iterator


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "instances/mmv2022_table9.csv"
PARAMETERS = ROOT / "results/mmv2022_parameters.csv"
SEARCH_DB = ROOT / "results/checkpoints/extensions.sqlite3"
STATE_DB = ROOT / "results/checkpoints/extensions_coverage_audit.sqlite3"
CHECKPOINT = ROOT / "results/checkpoints/extensions.json"
PROVENANCE = ROOT / "results/extensions_provenance.csv"
UNIQUE = ROOT / "results/extensions_unique.csv"
REPORT = ROOT / "results/extension_coverage_audit.json"

CATALOG_HASH = (
    "801f054853d07652c795fb16217425869f857d7f5d74e427165d554faf4eae1d"
)
PARAMETERS_HASH = (
    "ef74175dfd81542a167feed5a2d7f66be723846993642fb65344d08655b594c6"
)
ORIGIN_DOMAIN = b"gamma-theta-extension-origin-chain-v1\0"
EXPECTED_ORIGINS = 110_537
EXPECTED_HOSTS = 55
EXPECTED_UNIQUE = 54_216

CATALOG_HEADER = ("catalog_id", "n", "graph6", "source")
PARAMETERS_HEADER = (
    "catalog_id",
    "n",
    "m",
    "graph6",
    "gamma",
    "i",
    "alpha",
    "gamma_infinity_one_guard",
    "theta",
    "gamma_witness",
    "minimum_dominating_set_count",
    "i_witness",
    "alpha_witness",
    "greatest_eternal_family_size",
    "greatest_eternal_family_sha256",
)
PROVENANCE_HEADER = (
    "host_id",
    "neighborhood_mask",
    "neighborhood_size",
    "raw_graph6",
    "canonical_graph6",
    "gamma_delta",
    "alpha_delta",
    "category",
)
UNIQUE_HEADER = (
    "canonical_graph6",
    "n",
    "m",
    "origin_count",
    "first_host_id",
    "first_neighborhood_mask",
    "first_raw_graph6",
    "gamma",
    "alpha",
    "category",
    "private_obstruction_json",
    "eternal_a",
    "eternal_b",
    "family_a_size",
    "family_b_size",
    "family_a_sha256",
    "family_b_sha256",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def file_hash(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def reject_constant(value: str) -> object:
    raise AssertionError(f"non-finite JSON value {value}")


def strict_json_text(text: str) -> object:
    return json.loads(
        text,
        object_pairs_hook=strict_object,
        parse_constant=reject_constant,
    )


def strict_json(path: Path) -> object:
    return strict_json_text(path.read_text(encoding="utf-8"))


def canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def json_hash(value: object) -> str:
    return sha256(canonical_json(value)).hexdigest()


def decode_graph6(record: str) -> tuple[int, tuple[int, ...]]:
    """Separate strict ordinary-graph6 decoder, bounded to order 12."""

    require(type(record) is str, "graph6 is not text")
    try:
        raw = record.encode("ascii")
    except UnicodeEncodeError as error:
        raise AssertionError("graph6 is not ASCII") from error
    require(raw and not raw.startswith(b">>graph6<<"), "header/empty graph6")
    require(raw[0] != 126 and 63 <= raw[0] <= 125, "bad graph6 order")
    order = raw[0] - 63
    require(order <= 12, "graph6 exceeds hostile-probe bound")
    edge_bits = order * (order - 1) // 2
    payload_length = (edge_bits + 5) // 6
    require(len(raw) == payload_length + 1, "wrong graph6 length")
    payload = raw[1:]
    require(all(63 <= byte <= 126 for byte in payload), "bad graph6 byte")
    padding = 6 * payload_length - edge_bits
    if padding and payload:
        require(
            ((payload[-1] - 63) & ((1 << padding) - 1)) == 0,
            "nonzero graph6 padding",
        )
    rows = [0] * order
    position = 0
    for second in range(1, order):
        for first in range(second):
            word = payload[position // 6] - 63
            if (word >> (5 - position % 6)) & 1:
                rows[first] |= 1 << second
                rows[second] |= 1 << first
            position += 1
    return order, tuple(rows)


def encode_graph6(order: int, rows: tuple[int, ...]) -> str:
    bits: list[int] = []
    for second in range(1, order):
        for first in range(second):
            bits.append((rows[first] >> second) & 1)
    while len(bits) % 6:
        bits.append(0)
    output = bytearray((order + 63,))
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        output.append(63 + value)
    return output.decode("ascii")


def extend(
    host_order: int, host_rows: tuple[int, ...], mask: int
) -> tuple[int, tuple[int, ...]]:
    require(1 <= mask < 1 << host_order, "extension mask out of range")
    rows = list(host_rows)
    for vertex in range(host_order):
        if mask & (1 << vertex):
            rows[vertex] |= 1 << host_order
    rows.append(mask)
    return host_order + 1, tuple(rows)


def relabel(
    order: int, rows: tuple[int, ...], old_to_new: tuple[int, ...]
) -> tuple[int, ...]:
    require(
        len(old_to_new) == order
        and set(old_to_new) == set(range(order))
        and all(type(value) is int for value in old_to_new),
        "mapping is not a permutation",
    )
    result = [0] * order
    for first in range(order):
        for second in range(first + 1, order):
            if rows[first] & (1 << second):
                image_first = old_to_new[first]
                image_second = old_to_new[second]
                result[image_first] |= 1 << image_second
                result[image_second] |= 1 << image_first
    return tuple(result)


def edge_count(rows: tuple[int, ...]) -> int:
    return sum(row.bit_count() for row in rows) // 2


def read_csv_dicts(
    path: Path, expected_header: tuple[str, ...]
) -> tuple[dict[str, str], ...]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, strict=True)
        require(tuple(next(reader)) == expected_header, f"bad header: {path}")
        result = []
        for row in reader:
            require(len(row) == len(expected_header), f"bad width: {path}")
            result.append(dict(zip(expected_header, row, strict=True)))
    return tuple(result)


def open_immutable(path: Path) -> sqlite3.Connection:
    for suffix in ("-wal", "-shm", "-journal"):
        require(not Path(str(path) + suffix).exists(), f"companion: {path}{suffix}")
    connection = sqlite3.connect(path.resolve().as_uri() + "?mode=ro&immutable=1", uri=True)
    connection.execute("PRAGMA query_only=ON")
    return connection


def expected_positions(
    hosts: tuple[dict[str, object], ...]
) -> Iterator[tuple[dict[str, object], int]]:
    for host in hosts:
        order = int(host["order"])
        for mask in range(1, 1 << order):
            yield host, mask


def sqlite_value(value: object) -> str:
    if value is None:
        return ""
    require(type(value) in (int, str), f"unexpected CSV value type {type(value)}")
    return str(value)


def compare_csv(
    path: Path,
    header: tuple[str, ...],
    rows: Iterable[tuple[object, ...]],
) -> int:
    sentinel = object()
    count = 0
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, strict=True)
        require(tuple(next(reader)) == header, f"bad export header: {path}")
        for csv_row, db_row in zip_longest(reader, rows, fillvalue=sentinel):
            require(csv_row is not sentinel and db_row is not sentinel, f"row count: {path}")
            require(
                tuple(csv_row) == tuple(sqlite_value(value) for value in db_row),
                f"row mismatch at {path}:{count + 2}",
            )
            count += 1
    return count


def main() -> None:
    immutable_paths = (
        CATALOG,
        PARAMETERS,
        SEARCH_DB,
        STATE_DB,
        CHECKPOINT,
        PROVENANCE,
        UNIQUE,
        REPORT,
    )
    before = {str(path): file_hash(path) for path in immutable_paths}
    require(before[str(CATALOG)] == CATALOG_HASH, "catalog pin differs")
    require(before[str(PARAMETERS)] == PARAMETERS_HASH, "parameter pin differs")

    report_value = strict_json(REPORT)
    require(isinstance(report_value, dict), "report is not an object")
    report = report_value
    require(report.get("status") == "complete" and report.get("passed") is True, "report not complete")
    require(report.get("verified_origins") == EXPECTED_ORIGINS, "report origin total")
    require(report.get("expected_origins") == EXPECTED_ORIGINS, "report expected total")
    require(report.get("expected_hosts") == EXPECTED_HOSTS, "report host total")
    require(report.get("unique_canonical_graphs") == EXPECTED_UNIQUE, "report unique total")

    binding_value = report.get("audit_binding")
    require(isinstance(binding_value, dict), "report binding is not an object")
    binding = binding_value
    require(json_hash(binding) == report.get("audit_binding_sha256"), "binding digest")
    bound_paths = {
        "catalog": CATALOG,
        "parameters": PARAMETERS,
        "database": SEARCH_DB,
        "checkpoint": CHECKPOINT,
        "provenance": PROVENANCE,
        "unique": UNIQUE,
    }
    for role, path in bound_paths.items():
        require(
            binding.get(f"{role}_path") == str(path.resolve()),
            f"{role} path binding",
        )
        require(
            binding.get(f"{role}_sha256") == before[str(path)],
            f"{role} byte binding",
        )
    checker_manifest = binding.get("checker_source_manifest")
    require(isinstance(checker_manifest, list), "checker manifest shape")
    manifest_digest = sha256()
    for item in checker_manifest:
        require(
            isinstance(item, list)
            and len(item) == 2
            and all(isinstance(value, str) for value in item),
            "checker manifest row",
        )
        relative, expected_hash = item
        actual_hash = file_hash(ROOT / relative)
        require(actual_hash == expected_hash, f"checker source hash {relative}")
        manifest_digest.update(f"{relative} {expected_hash}\n".encode("ascii"))
    require(
        manifest_digest.hexdigest() == binding.get("checker_source_set_sha256"),
        "checker source-set digest",
    )
    require(report.get("database_sha256") == before[str(SEARCH_DB)], "database report hash")
    require(report.get("state_database_sha256") == before[str(STATE_DB)], "state report hash")

    catalog_rows = read_csv_dicts(CATALOG, CATALOG_HEADER)
    parameter_rows = read_csv_dicts(PARAMETERS, PARAMETERS_HEADER)
    require(len(catalog_rows) == len(parameter_rows) == 56, "input row count")
    require(
        tuple(row["catalog_id"] for row in catalog_rows)
        == tuple(row["catalog_id"] for row in parameter_rows),
        "catalog/parameter order",
    )
    hosts_list: list[dict[str, object]] = []
    distribution: dict[tuple[int, int], int] = {}
    for catalog_row, parameter_row in zip(catalog_rows, parameter_rows, strict=True):
        require(catalog_row["graph6"] == parameter_row["graph6"], "catalog join graph6")
        require(catalog_row["n"] == parameter_row["n"], "catalog join order")
        alpha = int(parameter_row["alpha"])
        eternal = int(parameter_row["gamma_infinity_one_guard"])
        theta = int(parameter_row["theta"])
        if alpha == eternal == 3 and eternal < theta:
            order, rows = decode_graph6(catalog_row["graph6"])
            gamma = int(parameter_row["gamma"])
            require(order == int(catalog_row["n"]), "host encoded order")
            require(edge_count(rows) == int(parameter_row["m"]), "host encoded size")
            record: dict[str, object] = {
                "index": len(hosts_list),
                "id": catalog_row["catalog_id"],
                "order": order,
                "graph6": catalog_row["graph6"],
                "rows": rows,
                "gamma": gamma,
                "alpha": alpha,
                "eternal": eternal,
                "theta": theta,
            }
            hosts_list.append(record)
            distribution[(order, gamma)] = distribution.get((order, gamma), 0) + 1
    hosts = tuple(hosts_list)
    require(len(hosts) == EXPECTED_HOSTS, "selected host count")
    require(
        distribution == {(10, 2): 2, (11, 1): 2, (11, 2): 51},
        "host distribution",
    )
    require(
        sum((1 << int(host["order"])) - 1 for host in hosts) == EXPECTED_ORIGINS,
        "derived origin universe",
    )

    search = open_immutable(SEARCH_DB)
    state = open_immutable(STATE_DB)
    try:
        require(tuple(search.execute("PRAGMA integrity_check")) == (("ok",),), "search integrity")
        require(tuple(state.execute("PRAGMA integrity_check")) == (("ok",),), "state integrity")
        db_hosts = tuple(
            search.execute(
                """
                SELECT host_index, catalog_id, n, graph6, gamma, alpha,
                       gamma_infinity, theta, raw_expected, next_mask, status,
                       canonical_stream_sha256
                FROM hosts ORDER BY host_index
                """
            )
        )
        require(len(db_hosts) == len(hosts), "database host count")
        stored_stream_hashes: dict[str, str] = {}
        for host, db_host in zip(hosts, db_hosts, strict=True):
            fixed = (
                host["index"],
                host["id"],
                host["order"],
                host["graph6"],
                host["gamma"],
                host["alpha"],
                host["eternal"],
                host["theta"],
                (1 << int(host["order"])) - 1,
                1 << int(host["order"]),
                "complete",
            )
            require(db_host[:11] == fixed, f"database host row {host['id']}")
            stored_stream_hashes[str(host["id"])] = str(db_host[11])

        origin_rows = search.execute(
            """
            SELECT h.host_index, o.host_id, o.neighborhood_mask,
                   o.neighborhood_size, o.raw_graph6, o.canonical_graph6,
                   o.gamma_delta, o.alpha_delta, o.category,
                   g.gamma, g.alpha, g.category
            FROM origins AS o
            JOIN hosts AS h ON h.catalog_id = o.host_id
            JOIN canonical_graphs AS g ON g.graph6 = o.canonical_graph6
            ORDER BY h.host_index, o.neighborhood_mask
            """
        )
        receipt_rows = state.execute(
            """
            SELECT host_index, host_id, neighborhood_mask, raw_graph6,
                   canonical_graph6, mapping_json, chain_sha256
            FROM origin_receipts ORDER BY host_index, neighborhood_mask
            """
        )
        sentinel = object()
        chain = sha256(ORIGIN_DOMAIN).hexdigest()
        multiplicities: dict[str, int] = {}
        first_origin: dict[str, tuple[int, str, int, str]] = {}
        stream_digests = {
            str(host["id"]): sha256() for host in hosts
        }
        verified = 0
        for expected, origin, receipt in zip_longest(
            expected_positions(hosts),
            origin_rows,
            receipt_rows,
            fillvalue=sentinel,
        ):
            require(
                expected is not sentinel
                and origin is not sentinel
                and receipt is not sentinel,
                "origin/receipt sequence length",
            )
            host, mask = expected
            host_index = int(host["index"])
            host_id = str(host["id"])
            require(origin[:3] == (host_index, host_id, mask), "origin sequence")
            require(receipt[:3] == (host_index, host_id, mask), "receipt sequence")
            require(origin[3] == mask.bit_count(), "neighborhood size")
            expected_order, expected_rows = extend(
                int(host["order"]), host["rows"], mask  # type: ignore[arg-type]
            )
            expected_raw = encode_graph6(expected_order, expected_rows)
            require(origin[4] == expected_raw, "raw extension reconstruction")
            require(receipt[3] == origin[4] and receipt[4] == origin[5], "receipt graph binding")
            canonical_order, canonical_rows = decode_graph6(origin[5])
            require(canonical_order == expected_order, "canonical order")
            mapping_value = strict_json_text(receipt[5])
            require(
                isinstance(mapping_value, list)
                and canonical_json(mapping_value).decode("ascii") == receipt[5],
                "mapping JSON",
            )
            mapping = tuple(mapping_value)
            require(
                relabel(expected_order, expected_rows, mapping) == canonical_rows,
                "stored mapping is not an isomorphism",
            )
            require(origin[6] == origin[9] - int(host["gamma"]), "gamma delta")
            require(origin[7] == origin[10] - int(host["alpha"]), "alpha delta")
            require(origin[8] == origin[11], "category inheritance")
            payload = {
                "host_index": host_index,
                "host_id": host_id,
                "neighborhood_mask": mask,
                "neighborhood_size": origin[3],
                "raw_graph6": origin[4],
                "canonical_graph6": origin[5],
                "gamma_delta": origin[6],
                "alpha_delta": origin[7],
                "category": origin[8],
                "raw_to_canonical_mapping": mapping_value,
            }
            chain = sha256(
                bytes.fromhex(chain) + b"\0" + canonical_json(payload)
            ).hexdigest()
            require(receipt[6] == chain, "receipt chain")
            canonical = str(origin[5])
            multiplicities[canonical] = multiplicities.get(canonical, 0) + 1
            first_origin.setdefault(
                canonical, (host_index, host_id, mask, expected_raw)
            )
            stream_digests[host_id].update(canonical.encode("ascii") + b"\n")
            verified += 1

        require(verified == EXPECTED_ORIGINS, "verified origin count")
        require(len(multiplicities) == EXPECTED_UNIQUE, "independent unique count")
        progress = state.execute(
            """
            SELECT status, last_host_index, last_mask, verified_origins,
                   origin_chain_sha256
            FROM progress WHERE singleton=1
            """
        ).fetchone()
        require(
            progress == ("complete", 54, 2047, EXPECTED_ORIGINS, chain),
            "state progress/chain",
        )
        require(report.get("origin_chain_sha256") == chain, "report origin chain")

        state_counts = tuple(
            state.execute(
                """
                SELECT graph6, origin_count, first_host_index, first_host_id,
                       first_neighborhood_mask, first_raw_graph6
                FROM canonical_counts ORDER BY graph6
                """
            )
        )
        require(len(state_counts) == EXPECTED_UNIQUE, "state unique count")
        for graph6, count, first_index, first_host, first_mask, first_raw in state_counts:
            require(multiplicities.get(graph6) == count, "state multiplicity")
            require(
                first_origin.get(graph6)
                == (first_index, first_host, first_mask, first_raw),
                "state first provenance",
            )

        canonical_rows_all = tuple(
            search.execute(
                """
                SELECT graph6, n, m, origin_count, first_host_id,
                       first_neighborhood_mask, first_raw_graph6, gamma, alpha,
                       category, private_obstruction_json, eternal_a, eternal_b,
                       family_a_size, family_b_size, family_a_sha256,
                       family_b_sha256
                FROM canonical_graphs ORDER BY graph6
                """
            )
        )
        require(len(canonical_rows_all) == EXPECTED_UNIQUE, "database unique count")
        category_counts: dict[str, int] = {}
        category_origins: dict[str, int] = {}
        for row in canonical_rows_all:
            graph6, order, size, count = row[:4]
            decoded_order, decoded_rows = decode_graph6(graph6)
            require(
                decoded_order == order and edge_count(decoded_rows) == size,
                "canonical graph metadata",
            )
            require(multiplicities.get(graph6) == count, "database multiplicity")
            first = first_origin[graph6]
            require(row[4:7] == first[1:], "database first provenance")
            category = str(row[9])
            category_counts[category] = category_counts.get(category, 0) + 1
            category_origins[category] = category_origins.get(category, 0) + int(count)
        require(sum(multiplicities.values()) == EXPECTED_ORIGINS, "multiplicity total")

        actual_stream_hashes = {
            identifier: digest.hexdigest()
            for identifier, digest in stream_digests.items()
        }
        require(actual_stream_hashes == stored_stream_hashes, "database host stream hashes")
        require(
            actual_stream_hashes == report.get("host_canonical_stream_sha256"),
            "report host stream hashes",
        )

        provenance_count = compare_csv(
            PROVENANCE,
            PROVENANCE_HEADER,
            search.execute(
                """
                SELECT o.host_id, o.neighborhood_mask, o.neighborhood_size,
                       o.raw_graph6, o.canonical_graph6, o.gamma_delta,
                       o.alpha_delta, o.category
                FROM origins AS o JOIN hosts AS h ON h.catalog_id=o.host_id
                ORDER BY h.host_index, o.neighborhood_mask
                """
            ),
        )
        unique_count = compare_csv(
            UNIQUE,
            UNIQUE_HEADER,
            search.execute(
                """
                SELECT graph6, n, m, origin_count, first_host_id,
                       first_neighborhood_mask, first_raw_graph6, gamma, alpha,
                       category, private_obstruction_json, eternal_a, eternal_b,
                       family_a_size, family_b_size, family_a_sha256,
                       family_b_sha256
                FROM canonical_graphs ORDER BY n, graph6
                """
            ),
        )
        require(provenance_count == EXPECTED_ORIGINS, "provenance CSV count")
        require(unique_count == EXPECTED_UNIQUE, "unique CSV count")
    finally:
        state.close()
        search.close()

    checkpoint_value = strict_json(CHECKPOINT)
    require(isinstance(checkpoint_value, dict), "checkpoint shape")
    checkpoint = checkpoint_value
    require(checkpoint.get("status") == "complete", "checkpoint status")
    require(checkpoint.get("database_sha256") == before[str(SEARCH_DB)], "checkpoint database hash")
    require(
        checkpoint.get("output_sha256")
        == {
            str(PROVENANCE.resolve()): before[str(PROVENANCE)],
            str(UNIQUE.resolve()): before[str(UNIQUE)],
        },
        "checkpoint export hashes",
    )

    after = {str(path): file_hash(path) for path in immutable_paths}
    require(before == after, "a production artifact changed during hostile probe")
    print(
        json.dumps(
            {
                "status": "PASS",
                "production_files_unchanged": True,
                "hosts": EXPECTED_HOSTS,
                "origins": EXPECTED_ORIGINS,
                "unique_canonical_graphs": EXPECTED_UNIQUE,
                "origin_chain_sha256": chain,
                "category_unique_counts": category_counts,
                "category_origin_counts": category_origins,
                "report_sha256": before[str(REPORT)],
                "search_database_sha256": before[str(SEARCH_DB)],
                "state_database_sha256": before[str(STATE_DB)],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
