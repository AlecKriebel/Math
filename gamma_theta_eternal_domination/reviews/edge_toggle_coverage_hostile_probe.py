#!/usr/bin/env python3
"""Hostile probes for the independent edge-toggle coverage audit.

This script has two deliberately separate parts:

* a standard-library-only reconstruction of the production origin universe
  and every saved isomorphism receipt; and
* mutation probes against the audit implementation's fail-closed checks.

It does not import the edge-toggle search engine or either mathematical
evaluator.  It writes only temporary copies.
"""

from __future__ import annotations

import csv
from dataclasses import replace
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import shutil
import sqlite3
import sys
import tempfile
import time


CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from edge_toggle_coverage_checker.audit import (  # noqa: E402
    AuditError,
    AuditPaths,
    _audit_binding,
    _expected_origins,
    _open_immutable_database,
    _production_origins,
    _replay_state,
    _validate_no_candidate_freeze,
    _validate_origin,
    load_seed_universe,
)
from edge_toggle_coverage_checker.graph import (  # noqa: E402
    Graph,
    Graph6Error,
    find_isomorphism,
    verify_isomorphism,
)


EXPECTED_HASHES = {
    "results/extensions_unique.csv":
        "e7f0ffa459d74a67a3a647e19ee5669652ff1679302b3b62daaef299ee02945e",
    "results/extension_coverage_audit.json":
        "523b3a57ef9afac2b8c921564afcf3fcd8fdbe7719984014f3b0f8e80da8e7cb",
    "results/extensions_evaluation_audit.json":
        "75c999e19fb3e877083e4612dd2550079480ad610b67a5caefb0fbf6d303678e",
    "results/checkpoints/edge_toggles.sqlite3":
        "2a6349452906cf2904a5e9e6284806f603619ad28ec66fa63fc383f2b833b258",
    "results/checkpoints/edge_toggles.json":
        "f00b404fdfc09ac95f8b56325ef58a3399559b33eb1b659e304fdc81ed512ffc",
    "results/edge_toggles_provenance.csv":
        "378e867d5ec0d419f668f5169dbac6f2319cd2afc9ce3c5f63da2b9677dccba5",
    "results/edge_toggles_unique.csv":
        "a32505df6ba67479b5908a91711d21babb14fd8ac50cdfd0f0b92fc1001d4319",
}
SELECTED = {
    "eternal_false_without_private_obstruction",
    "private_obstruction_eternal_false",
}


def file_hash(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        while block := handle.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def strict_graph6(record: str) -> tuple[int, tuple[int, ...]]:
    """Small independent graph6 decoder, restricted to n <= 12."""

    raw = record.encode("ascii")
    if not raw or raw.startswith(b">>graph6<<") or raw[0] == 126:
        raise ValueError("not strict headerless small graph6")
    if not 63 <= raw[0] <= 75:
        raise ValueError("order byte outside n <= 12")
    order = raw[0] - 63
    bit_count = order * (order - 1) // 2
    payload_length = (bit_count + 5) // 6
    if len(raw) != 1 + payload_length:
        raise ValueError("wrong graph6 length")
    if any(not 63 <= value <= 126 for value in raw[1:]):
        raise ValueError("bad graph6 payload")
    padding = payload_length * 6 - bit_count
    if padding and ((raw[-1] - 63) & ((1 << padding) - 1)):
        raise ValueError("nonzero graph6 padding")
    rows = [0] * order
    position = 0
    for second in range(1, order):
        for first in range(second):
            value = raw[1 + position // 6] - 63
            if value & (1 << (5 - position % 6)):
                rows[first] |= 1 << second
                rows[second] |= 1 << first
            position += 1
    return order, tuple(rows)


def encode_graph6(rows: tuple[int, ...]) -> str:
    order = len(rows)
    bits = [
        int(bool(rows[first] & (1 << second)))
        for second in range(1, order)
        for first in range(second)
    ]
    while len(bits) % 6:
        bits.append(0)
    output = bytearray([order + 63])
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start:start + 6]:
            value = (value << 1) | bit
        output.append(value + 63)
    return output.decode("ascii")


def toggle(rows: tuple[int, ...], first: int, second: int) -> tuple[int, ...]:
    changed = list(rows)
    changed[first] ^= 1 << second
    changed[second] ^= 1 << first
    return tuple(changed)


def direct_mapping_valid(
    raw_rows: tuple[int, ...],
    canonical_rows: tuple[int, ...],
    mapping: list[int],
) -> bool:
    order = len(raw_rows)
    if (
        len(canonical_rows) != order
        or len(mapping) != order
        or set(mapping) != set(range(order))
        or any(type(value) is not int for value in mapping)
    ):
        return False
    for first in range(order):
        for second in range(first + 1, order):
            raw_edge = bool(raw_rows[first] & (1 << second))
            canonical_edge = bool(
                canonical_rows[mapping[first]] & (1 << mapping[second])
            )
            if raw_edge != canonical_edge:
                return False
    return True


def default_paths() -> AuditPaths:
    return AuditPaths(
        campaign_root=CAMPAIGN,
        seed_input=CAMPAIGN / "results/extensions_unique.csv",
        extension_coverage_audit=(
            CAMPAIGN / "results/extension_coverage_audit.json"
        ),
        extension_evaluation_audit=(
            CAMPAIGN / "results/extensions_evaluation_audit.json"
        ),
        database=CAMPAIGN / "results/checkpoints/edge_toggles.sqlite3",
        checkpoint=CAMPAIGN / "results/checkpoints/edge_toggles.json",
        provenance_csv=CAMPAIGN / "results/edge_toggles_provenance.csv",
        unique_csv=CAMPAIGN / "results/edge_toggles_unique.csv",
        candidate_directory=(
            CAMPAIGN / "certificates/frozen_edge_toggle_candidates"
        ),
        state_database=(
            CAMPAIGN
            / "results/checkpoints/edge_toggle_coverage_audit.sqlite3"
        ),
        report=CAMPAIGN / "results/edge_toggle_coverage_audit.json",
    )


def independent_full_reconstruction(paths: AuditPaths) -> dict[str, object]:
    for relative, expected in EXPECTED_HASHES.items():
        actual = file_hash(CAMPAIGN / relative)
        assert actual == expected, (relative, actual, expected)

    selected: list[tuple[str, int, int, str]] = []
    category_counts: dict[str, int] = {}
    with paths.seed_input.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            category = row["category"]
            category_counts[category] = category_counts.get(category, 0) + 1
            if category in SELECTED:
                order, rows = strict_graph6(row["canonical_graph6"])
                size = sum(value.bit_count() for value in rows) // 2
                assert order == int(row["n"])
                assert size == int(row["m"])
                assert row["gamma"] == row["alpha"] == "3"
                assert row["eternal_a"] == row["eternal_b"] == "0"
                selected.append(
                    (
                        row["canonical_graph6"],
                        order,
                        size,
                        category,
                    )
                )
    assert len(selected) == 391
    assert sum(order * (order - 1) // 2 for _, order, _, _ in selected) == 25_641
    assert sum(order == 11 for _, order, _, _ in selected) == 15
    assert sum(order == 12 for _, order, _, _ in selected) == 376

    search = sqlite3.connect(f"file:{paths.database}?mode=ro", uri=True)
    state = sqlite3.connect(f"file:{paths.state_database}?mode=ro", uri=True)
    try:
        origin_rows = tuple(
            search.execute(
                """
                SELECT s.seed_index,o.seed_id,o.pair_index,o.first_vertex,
                       o.second_vertex,o.toggle_action,o.raw_graph6,
                       o.canonical_graph6,o.category
                FROM origins o JOIN seeds s ON s.seed_id=o.seed_id
                ORDER BY s.seed_index,o.pair_index
                """
            )
        )
        receipts = tuple(
            state.execute(
                """
                SELECT global_index,seed_index,seed_id,pair_index,
                       first_vertex,second_vertex,toggle_action,raw_graph6,
                       canonical_graph6,category,mapping_json,chain_sha256
                FROM origin_receipts ORDER BY global_index
                """
            )
        )
        assert len(origin_rows) == len(receipts) == 25_641
        multiplicities: dict[str, int] = {}
        firsts: dict[str, tuple[int, str, int, str]] = {}
        chain = sha256(
            b"gamma-theta-edge-toggle-origin-chain-v1\0"
        ).hexdigest()
        global_index = 0
        for seed_index, (graph6, order, _, _) in enumerate(selected):
            decoded_order, seed_rows = strict_graph6(graph6)
            assert decoded_order == order
            seed_id = f"ET-{seed_index + 1:04d}"
            for pair_index, (first, second) in enumerate(
                combinations(range(order), 2)
            ):
                row = origin_rows[global_index]
                receipt = receipts[global_index]
                assert row[:5] == (
                    seed_index, seed_id, pair_index, first, second
                )
                raw_rows = toggle(seed_rows, first, second)
                raw_graph6 = encode_graph6(raw_rows)
                expected_action = (
                    "delete"
                    if seed_rows[first] & (1 << second)
                    else "add"
                )
                assert row[5] == expected_action
                assert row[6] == raw_graph6
                _, canonical_rows = strict_graph6(row[7])
                mapping = json.loads(receipt[10])
                assert direct_mapping_valid(raw_rows, canonical_rows, mapping)
                assert receipt[:10] == (
                    global_index,
                    seed_index,
                    seed_id,
                    pair_index,
                    first,
                    second,
                    expected_action,
                    raw_graph6,
                    row[7],
                    row[8],
                )
                receipt_payload = {
                    "global_index": global_index,
                    "seed_index": seed_index,
                    "seed_id": seed_id,
                    "pair_index": pair_index,
                    "first_vertex": first,
                    "second_vertex": second,
                    "toggle_action": expected_action,
                    "raw_graph6": raw_graph6,
                    "canonical_graph6": row[7],
                    "category": row[8],
                    "mapping": mapping,
                }
                chain = sha256(
                    bytes.fromhex(chain)
                    + json.dumps(
                        receipt_payload,
                        sort_keys=True,
                        separators=(",", ":"),
                        ensure_ascii=True,
                        allow_nan=False,
                    ).encode("ascii")
                ).hexdigest()
                assert receipt[11] == chain
                multiplicities[row[7]] = multiplicities.get(row[7], 0) + 1
                firsts.setdefault(
                    row[7], (global_index, seed_id, pair_index, raw_graph6)
                )
                global_index += 1
        assert global_index == 25_641
        assert len(multiplicities) == 19_136
        assert chain == (
            "d00dff4e6e0ad40b37e14da89c5deb2616ed10e39b08c81b1d5837723df1f5bb"
        )
        assert state.execute(
            """
            SELECT status,verified_origins,origin_chain_sha256
            FROM progress WHERE singleton=1
            """
        ).fetchone() == ("complete", 25_641, chain)
        state_counts = {
            row[0]: row[1:]
            for row in state.execute(
                """
                SELECT graph6,origin_count,first_global_index,
                       first_seed_index,first_seed_id,first_pair_index,
                       first_raw_graph6
                FROM canonical_counts
                """
            )
        }
        assert set(state_counts) == set(multiplicities)
        for graph6, origin_count in multiplicities.items():
            first_global, first_seed_id, first_pair, first_raw = firsts[graph6]
            first_seed_index = int(first_seed_id[3:]) - 1
            assert state_counts[graph6] == (
                origin_count,
                first_global,
                first_seed_index,
                first_seed_id,
                first_pair,
                first_raw,
            )

        canonical_rows = tuple(
            search.execute(
                """
                SELECT graph6,n,m,connected,origin_count,first_seed_id,
                       first_pair_index,first_raw_graph6,gamma_a,gamma_b,
                       alpha_a,alpha_b,gamma_infinity_a,gamma_infinity_b,
                       theta_a,theta_b,category,family_size,family_sha256
                FROM canonical_graphs ORDER BY n,graph6
                """
            )
        )
        assert len(canonical_rows) == len(multiplicities)
        parameter_counts: dict[str, int] = {}
        for row in canonical_rows:
            graph6 = row[0]
            assert row[4] == multiplicities[graph6]
            assert row[5:8] == firsts[graph6][1:]
            assert row[3] == 1
            assert row[8] == row[9]
            assert row[10] == row[11]
            assert row[12] == row[13]
            assert row[14] == row[15]
            assert row[8] <= row[10] <= row[12] <= row[14]
            assert row[16] == "gamma_below_eternal"
            key = f"{row[8]},{row[10]},{row[12]},{row[14]}"
            parameter_counts[key] = parameter_counts.get(key, 0) + 1

        with paths.provenance_csv.open(encoding="utf-8", newline="") as handle:
            exported = csv.reader(handle)
            header = next(exported)
            assert header == [
                "seed_id", "pair_index", "first_vertex", "second_vertex",
                "toggle_action", "raw_graph6", "canonical_graph6", "category",
            ]
            exported_rows = tuple(exported)
        assert exported_rows == tuple(
            [str(value) for value in row[1:]]
            for row in origin_rows
        )

        with paths.unique_csv.open(encoding="utf-8", newline="") as handle:
            exported = csv.reader(handle)
            header = next(exported)
            assert header == [
                "canonical_graph6", "n", "m", "connected", "origin_count",
                "first_seed_id", "first_pair_index", "first_raw_graph6",
                "gamma_a", "gamma_b", "alpha_a", "alpha_b",
                "gamma_infinity_a", "gamma_infinity_b", "theta_a", "theta_b",
                "category", "family_size", "family_sha256",
            ]
            exported_rows = tuple(exported)
        assert exported_rows == tuple(
            ["" if value is None else str(value) for value in row]
            for row in canonical_rows
        )

        marker = search.execute(
            "SELECT value FROM metadata WHERE key='candidate_frozen_path'"
        ).fetchone()
        assert marker == ("",)
        assert search.execute(
            """
            SELECT COUNT(*) FROM canonical_graphs
            WHERE category='candidate_gamma_equals_eternal_below_theta'
            """
        ).fetchone() == (0,)
        assert search.execute(
            """
            SELECT COUNT(*) FROM origins
            WHERE category='candidate_gamma_equals_eternal_below_theta'
            """
        ).fetchone() == (0,)
    finally:
        search.close()
        state.close()

    if paths.candidate_directory.exists():
        assert paths.candidate_directory.is_dir()
        assert not any(paths.candidate_directory.iterdir())
    return {
        "selected_seeds": len(selected),
        "origins": global_index,
        "canonical_graphs": len(multiplicities),
        "origin_chain_sha256": chain,
        "parameter_counts": dict(sorted(parameter_counts.items())),
        "source_category_counts": dict(sorted(category_counts.items())),
    }


def expect_audit_error(label: str, function) -> str:
    try:
        function()
    except (AuditError, Graph6Error, ValueError, sqlite3.Error) as error:
        return f"{label}: rejected ({type(error).__name__}: {error})"
    raise AssertionError(f"{label}: mutation was accepted")


def mutation_probes(paths: AuditPaths) -> list[str]:
    results: list[str] = []
    seeds = load_seed_universe(paths)
    expected = _expected_origins(seeds)
    production = _open_immutable_database(paths.database)
    try:
        rows = _production_origins(production)
        base = list(rows[0])
        for label, position, replacement in (
            ("pair-index", 2, 1),
            ("first-vertex", 3, 1),
            ("toggle-action", 5, (
                "add" if base[5] == "delete" else "delete"
            )),
            ("raw-reconstruction", 6, seeds[0].graph6),
            ("canonical-key", 7, seeds[0].graph6),
        ):
            mutated = list(base)
            mutated[position] = replacement
            results.append(
                expect_audit_error(
                    label,
                    lambda mutated=mutated: _validate_origin(
                        expected[0], tuple(mutated)
                    ),
                )
            )

        raw = Graph.from_graph6(str(base[6]))
        permutation = tuple(
            [1, 2, 0] + list(range(3, raw.order))
        )
        relabeled = raw.relabeled(permutation)
        witness = find_isomorphism(raw, relabeled)
        assert witness is not None
        assert verify_isomorphism(raw, relabeled, witness)
        inverse = tuple(permutation.index(index) for index in range(raw.order))
        if verify_isomorphism(raw, relabeled, inverse):
            inverse = tuple(reversed(range(raw.order)))
        assert not verify_isomorphism(raw, relabeled, inverse)
        results.append("isomorphism-direction: accepted forward, rejected wrong direction")

        for malformed in ("", "~??", "D?", "Dzz", "D~|"):
            results.append(
                expect_audit_error(
                    f"graph6-{malformed!r}",
                    lambda malformed=malformed: Graph.from_graph6(malformed),
                )
            )

        with tempfile.TemporaryDirectory() as temporary_name:
            temporary = Path(temporary_name)
            state_copy = temporary / "state.sqlite3"
            shutil.copy2(paths.state_database, state_copy)
            state = sqlite3.connect(state_copy)
            try:
                state.execute(
                    """
                    UPDATE canonical_counts SET origin_count=origin_count+1
                    WHERE graph6=(SELECT graph6 FROM canonical_counts LIMIT 1)
                    """
                )
                state.commit()
                results.append(
                    expect_audit_error(
                        "multiplicity-receipt-replay",
                        lambda: _replay_state(state, expected, rows),
                    )
                )
            finally:
                state.close()

            state_copy = temporary / "state-mapping.sqlite3"
            shutil.copy2(paths.state_database, state_copy)
            state = sqlite3.connect(state_copy)
            try:
                state.execute(
                    "UPDATE origin_receipts SET mapping_json='[]' WHERE global_index=0"
                )
                state.commit()
                results.append(
                    expect_audit_error(
                        "resume-mapping-receipt",
                        lambda: _replay_state(state, expected, rows),
                    )
                )
            finally:
                state.close()

            state_copy = temporary / "state-chain.sqlite3"
            shutil.copy2(paths.state_database, state_copy)
            state = sqlite3.connect(state_copy)
            try:
                state.execute(
                    "UPDATE origin_receipts SET chain_sha256=? WHERE global_index=0",
                    ("0" * 64,),
                )
                state.commit()
                results.append(
                    expect_audit_error(
                        "resume-chain-receipt",
                        lambda: _replay_state(state, expected, rows),
                    )
                )
            finally:
                state.close()

            modified_seed = temporary / "extensions_unique.csv"
            modified_seed.write_bytes(paths.seed_input.read_bytes() + b"\n")
            results.append(
                expect_audit_error(
                    "seed-input-byte-binding",
                    lambda: load_seed_universe(
                        replace(paths, seed_input=modified_seed)
                    ),
                )
            )

            fake_candidate = temporary / "candidate"
            fake_candidate.mkdir()
            (fake_candidate / "orphan.json").write_text("{}", encoding="utf-8")
            results.append(
                expect_audit_error(
                    "candidate-file-present",
                    lambda: _validate_no_candidate_freeze(
                        production, "", fake_candidate
                    ),
                )
            )

            provenance_copy = temporary / "provenance.csv"
            shutil.copy2(paths.provenance_csv, provenance_copy)
            rebound = replace(paths, provenance_csv=provenance_copy)
            configuration_hash = json.loads(
                paths.report.read_text(encoding="utf-8")
            )["binding"]["configuration_sha256"]
            search_manifest = tuple(
                tuple(item)
                for item in json.loads(
                    paths.report.read_text(encoding="utf-8")
                )["binding"]["search_runtime_source_manifest"]
            )
            before, before_digest = _audit_binding(
                paths=rebound,
                configuration_sha256=configuration_hash,
                database_sha256=file_hash(paths.database),
                checkpoint_sha256=file_hash(paths.checkpoint),
                search_manifest=search_manifest,
            )
            with provenance_copy.open("ab") as handle:
                handle.write(b"\n")
            after, after_digest = _audit_binding(
                paths=rebound,
                configuration_sha256=configuration_hash,
                database_sha256=file_hash(paths.database),
                checkpoint_sha256=file_hash(paths.checkpoint),
                search_manifest=search_manifest,
            )
            assert before != after and before_digest != after_digest
            results.append("concurrent-bound-input-mutation: changed final binding")

            empty_candidate = temporary / "empty-candidate"
            empty_candidate.mkdir()
            candidate_rebound = replace(paths, candidate_directory=empty_candidate)
            candidate_before, candidate_before_digest = _audit_binding(
                paths=candidate_rebound,
                configuration_sha256=configuration_hash,
                database_sha256=file_hash(paths.database),
                checkpoint_sha256=file_hash(paths.checkpoint),
                search_manifest=search_manifest,
            )
            (empty_candidate / "late.json").write_text("{}", encoding="utf-8")
            candidate_after, candidate_after_digest = _audit_binding(
                paths=candidate_rebound,
                configuration_sha256=configuration_hash,
                database_sha256=file_hash(paths.database),
                checkpoint_sha256=file_hash(paths.checkpoint),
                search_manifest=search_manifest,
            )
            assert (
                candidate_before == candidate_after
                and candidate_before_digest == candidate_after_digest
            )
            results.append(
                "candidate-directory-late-mutation: NOT in final binding "
                "(documented low-severity TOCTOU finding)"
            )
    finally:
        production.close()
    return results


def main() -> int:
    started = time.perf_counter()
    paths = default_paths()
    reconstruction = independent_full_reconstruction(paths)
    mutations = mutation_probes(paths)
    payload = {
        "status": "passed_with_low_severity_finding",
        "reconstruction": reconstruction,
        "mutation_probes": mutations,
        "wall_seconds": time.perf_counter() - started,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
