#!/usr/bin/env python3
"""Stream-check the large decorated assignment tables and all cross-links.

This is intentionally a verifier of supplied tables, not a primitive atlas
generator.  Its report therefore cannot promote the theorem when generator
sources are missing.  It is useful for establishing exactly what the tables
do bind and for making direction/sign regressions mutation-sensitive.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import permutations
import json
import mmap
from pathlib import Path

from direction_sign_logic import compact_sha, necessary_containment_mask, verify_sign_record
from json_array_stream import iter_top_level_object_array, top_level_integer


def file_sha(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_relation(path: Path) -> dict[tuple[int, int], str]:
    rows: dict[tuple[int, int], str] = {}
    with path.open() as handle:
        header = handle.readline().rstrip("\n").split("\t")
        if header != ["source_index", "target_index", "relation"]:
            raise AssertionError(header)
        for line in handle:
            source, target, relation = line.rstrip("\n").split("\t")
            key = (int(source), int(target))
            if key in rows:
                raise AssertionError(f"duplicate TSV pair {key}")
            if relation not in {"equal", "strict"}:
                raise AssertionError(relation)
            rows[key] = relation
    return rows


class SignatureFiles:
    def __init__(self, source: Path, target: Path, width: int):
        self.width = width
        self._source_handle = source.open("rb")
        self._target_handle = target.open("rb")
        self.source = mmap.mmap(self._source_handle.fileno(), 0, access=mmap.ACCESS_READ)
        self.target = mmap.mmap(self._target_handle.fileno(), 0, access=mmap.ACCESS_READ)
        if len(self.source) % width or len(self.target) % width:
            raise AssertionError("signature width mismatch")

    def close(self) -> None:
        self.source.close(); self.target.close()
        self._source_handle.close(); self._target_handle.close()

    def pair(self, source: int, target: int) -> tuple[bytes, bytes]:
        a = source * self.width; b = target * self.width
        return self.source[a:a+self.width], self.target[b:b+self.width]


def bind_constraint(store: dict, key: tuple[str, int], graph: str, switching: str, t_hash: str | None = None) -> None:
    value = (graph, switching, t_hash)
    old = store.get(key)
    if old is None:
        store[key] = value
    elif old[0] != graph or old[1] != switching or (t_hash is not None and old[2] not in (None, t_hash)):
        raise AssertionError(f"inconsistent graph binding for {key}")


def audit_one(
    assignment: Path,
    relation_tsv: Path,
    sign_library: Path,
    outgoing: int,
    source_signatures: Path | None,
    target_signatures: Path | None,
) -> dict:
    library_data = json.loads(sign_library.read_text())
    library = library_data["records"]
    library_checks = [verify_sign_record(record) for record in library]
    relation = load_relation(relation_tsv)
    ordered_quartets = tuple(permutations(range(1, outgoing + 2), 4))
    width = len(ordered_quartets)
    signature_files = None
    if source_signatures is not None and target_signatures is not None:
        signature_files = SignatureFiles(source_signatures, target_signatures, width)

    pair_seen: set[tuple[int, int]] = set()
    graph_constraints: dict[tuple[str, int], tuple[str, str, str | None]] = {}
    equal_records = []
    exact_signature_checks = 0
    for record in iter_top_level_object_array(assignment, "equal_records"):
        pair = (int(record["source_index"]), int(record["target_index"]))
        if pair in pair_seen or relation.get(pair) != "equal":
            raise AssertionError(("bad equal pair", pair))
        pair_seen.add(pair); equal_records.append(record)
        if signature_files:
            source, target = signature_files.pair(*pair)
            if source != target or not necessary_containment_mask(source, target):
                raise AssertionError(("equal signature mismatch", pair))
            exact_signature_checks += 1

    strict_count = 0
    polynomial_hashes = set()
    for record in iter_top_level_object_array(assignment, "strict_records"):
        pair = (int(record["source_index"]), int(record["target_index"]))
        if pair in pair_seen or relation.get(pair) != "strict":
            raise AssertionError(("bad strict pair", pair))
        pair_seen.add(pair); strict_count += 1
        source_pullback = record["source_pullback"]
        target_pullback = record["target_pullback"]
        if not source_pullback["canonical"]["zero"] or source_pullback["expression"] != "0":
            raise AssertionError(("source is not the identity side", pair))
        if target_pullback["canonical"]["zero"] or target_pullback["expression"] == "0":
            raise AssertionError(("target is not strict", pair))
        lib_index = int(record["sign_library_record"])
        lib_record = library[lib_index]
        certificate = lib_record["certificate"]
        if compact_sha(certificate) != record["sign_certificate_sha256"]:
            raise AssertionError(("certificate hash", pair))
        if target_pullback["expression"] != certificate["expression"]:
            raise AssertionError(("polynomial/sign-library mismatch", pair))
        if record["target_tensor_type"] != lib_record["type_key"]:
            raise AssertionError(("tensor/sign-library mismatch", pair))
        canonical = target_pullback["canonical"]
        if sha256(json.dumps(canonical["terms"], separators=(",", ":")).encode()).hexdigest() != canonical["hash"]:
            raise AssertionError(("canonical polynomial hash", pair))
        if sha256(record["source_tensor_type"].encode()).hexdigest() != record["source_tensor_sha256"]:
            raise AssertionError(("source tensor hash", pair))
        if sha256(record["target_tensor_type"].encode()).hexdigest() != record["target_tensor_sha256"]:
            raise AssertionError(("target tensor hash", pair))
        quartet = ordered_quartets[int(record["feature_position"])]
        if quartet != tuple(record["ordered_quartet"]):
            raise AssertionError(("feature/quartet mismatch", pair))
        invariant = int(record["separator_invariant"])
        if signature_files:
            source, target = signature_files.pair(*pair)
            if not necessary_containment_mask(source, target) or source == target:
                raise AssertionError(("directed relation mismatch", pair))
            bit = 1 << invariant
            position = int(record["feature_position"])
            if source[position] & bit or not (target[position] & bit):
                raise AssertionError(("separator bit has wrong direction", pair))
            exact_signature_checks += 1
        bind_constraint(graph_constraints, ("source", pair[0]), record["source_graph_sha256"], record["source_switching_sha256"])
        bind_constraint(graph_constraints, ("target", pair[1]), record["target_graph_sha256"], record["target_switching_sha256"])
        polynomial_hashes.add(canonical["hash"])

    if signature_files:
        signature_files.close()
    if pair_seen != set(relation):
        missing = sorted(set(relation) - pair_seen)[:5]
        extra = sorted(pair_seen - set(relation))[:5]
        raise AssertionError(("pair universe mismatch", missing, extra))

    graph_records_checked = 0
    graph_values: dict[tuple[str, int], tuple[str, str, str]] = {}
    wanted = set(graph_constraints)
    equal_sources = {int(r["source_index"]) for r in equal_records}
    equal_targets = {int(r["target_index"]) for r in equal_records}
    wanted.update(("source", i) for i in equal_sources)
    wanted.update(("target", i) for i in equal_targets)
    for record in iter_top_level_object_array(assignment, "graph_records"):
        key = (record["side"], int(record["signature_index"]))
        if key not in wanted:
            continue
        graph_hash = sha256(record["graph_code"].encode()).hexdigest()
        switching_hash = compact_sha(record["switchings"])
        if graph_hash != record["graph_sha256"] or switching_hash != record["switching_sha256"]:
            raise AssertionError(("graph payload hash", key))
        if key in graph_constraints:
            expected = graph_constraints[key]
            if (record["graph_sha256"], record["switching_sha256"]) != expected[:2]:
                raise AssertionError(("pair-to-graph binding", key))
        graph_values[key] = (record["graph_sha256"], record["switching_sha256"], record["T_quotient_sha256"])
        graph_records_checked += 1
    if set(graph_values) != wanted:
        raise AssertionError(("missing graph records", sorted(wanted - set(graph_values))[:5]))
    for record in equal_records:
        source = graph_values[("source", int(record["source_index"]))]
        target = graph_values[("target", int(record["target_index"]))]
        if source[2] != record["T_quotient_sha256"] or target[2] != record["T_quotient_sha256"]:
            raise AssertionError(("equal pair is not T-identified", record["source_index"], record["target_index"]))

    expected_equal = top_level_integer(assignment, "equal_pairs")
    expected_strict = top_level_integer(assignment, "strict_pairs")
    if len(equal_records) != expected_equal or strict_count != expected_strict:
        raise AssertionError("top-level counts do not match arrays")
    return {
        "assignment": str(assignment),
        "assignment_sha256": file_sha(assignment),
        "equal_records": len(equal_records),
        "strict_records": strict_count,
        "relation_tsv_records": len(relation),
        "graph_records_replayed": graph_records_checked,
        "distinct_strict_polynomials": len(polynomial_hashes),
        "sign_library_records_recomputed": len(library_checks),
        "exact_signature_direction_checks": exact_signature_checks,
        "full_signature_bytes_available": signature_files is not None,
        "status": "EXACTLY COMPUTED",
        "limit": "table-consistency replay only; primitive graph generation is not performed",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--assignment", type=Path, required=True)
    parser.add_argument("--relation-tsv", type=Path, required=True)
    parser.add_argument("--sign-library", type=Path, required=True)
    parser.add_argument("--outgoing", type=int, required=True)
    parser.add_argument("--source-signatures", type=Path)
    parser.add_argument("--target-signatures", type=Path)
    args = parser.parse_args()
    if (args.source_signatures is None) != (args.target_signatures is None):
        parser.error("provide both signature files or neither")
    result = audit_one(
        args.assignment, args.relation_tsv, args.sign_library, args.outgoing,
        args.source_signatures, args.target_signatures,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
