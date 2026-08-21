#!/usr/bin/env python3
"""Stream a compact, path-bound ``A+p``/``A+p+q`` certificate.

Unlike :mod:`probe_extension_compiler`, this producer does not materialize a
graph, state, and binding row for every cell.  The exact child graph is the
deterministic insertion into the exact path-bound parent, so a complete
row-major matrix of insertion-arc pairs is sufficient.  Separator witnesses
and rigid quotient transports are stored in local content-addressed
libraries.  See ``COMPACT_PROBE_SCHEMA.md``.
"""

from __future__ import annotations

import argparse
import base64
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import struct

from atlas_compiler import load_bit_cache, stable_hash
from graph_model import RootedGraph, canonical_mixed, sd0
from hard_cover_compiler import (
    exact_poly_hash,
    full_deck,
    load_invariants,
    relation_witness,
)
from probe_extension_compiler import (
    ALLOWED_BASE,
    ALLOWED_CHILD,
    SEPARATED,
    admissible_internal_arcs,
    graph_from_row,
    insert_port,
    quotient_transport,
    restricts_to,
    transport_metadata,
)


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
CLASS_CODE = {
    "generic_polynomial_separation": 0,
    "strict_open_cube_separation": 1,
    "labelled_isomorphism": 2,
    "ordinary_T": 3,
}
INDEX_MASK = (1 << 29) - 1


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def normalized_path(path: Path) -> str:
    path = path.resolve()
    try:
        return str(path.relative_to(PROJECT.resolve()))
    except ValueError:
        return str(path)


def resolve(path: str | Path, *, relative_to: Path | None = None) -> Path:
    path = Path(path)
    if path.is_absolute():
        return path
    candidates = []
    if relative_to is not None:
        candidates.append(relative_to.resolve().parent / path)
    candidates.append(PROJECT / path)
    candidates.append(path)
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    return candidates[0].resolve()


def stable_bytes(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()


def normalized_json_for_commitment(value):
    """Discard run-local metadata while preserving mathematical content."""
    if isinstance(value, dict):
        return {
            key: normalized_json_for_commitment(item)
            for key, item in sorted(value.items())
            if key not in {"elapsed_seconds", "merged_shard_inputs"}
        }
    if isinstance(value, list):
        return [normalized_json_for_commitment(item) for item in value]
    return value


def semantic_json_sha256(path: Path) -> str:
    payload = normalized_json_for_commitment(
        json.loads(path.read_text(encoding="utf-8"))
    )
    return hashlib.sha256(stable_bytes(payload)).hexdigest()


class JsonlGzipWriter:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.raw = path.open("wb")
        self.stream = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        self.digest = hashlib.sha256()
        self.records = 0

    def write(self, payload: dict) -> None:
        line = stable_bytes(payload) + b"\n"
        self.stream.write(line)
        self.digest.update(line)
        self.records += 1

    def close(self) -> dict:
        self.stream.close()
        self.raw.close()
        return {
            "path": normalized_path(self.path),
            "records": self.records,
            "sha256": self.digest.hexdigest(),
            "file_sha256": sha256(self.path),
        }


def load_jsonl(path: Path, key: str) -> dict[str, dict]:
    answer = {}
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            identifier = str(row[key])
            if identifier in answer:
                raise AssertionError((path, "duplicate", identifier))
            answer[identifier] = row
    return answer


def graph_payload(graph: RootedGraph) -> dict:
    return {
        "root": int(graph.root),
        "labels": tuple(sorted((int(v), str(label)) for v, label in graph.labels)),
        "arcs": tuple(sorted((int(u), int(v)) for u, v in graph.arcs)),
    }


def graph_id(graph: RootedGraph) -> str:
    return stable_hash(graph_payload(graph))


def pack_words(words: list[int]) -> str:
    if not words:
        return ""
    return base64.b64encode(struct.pack(f"<{len(words)}I", *words)).decode("ascii")


def inventory_commitment(rows: list[dict]) -> str:
    digest = hashlib.sha256()
    for row in rows:
        digest.update(stable_bytes(row) + b"\n")
    return digest.hexdigest()


def collect_base_paths(summary_paths: list[Path]):
    """Return one exact ordered inventory entry per allowed raw terminal path."""
    inventory = []
    input_hashes = {}
    summaries = sorted((path.resolve() for path in summary_paths), key=normalized_path)
    for summary_path in summaries:
        summary = json.loads(summary_path.read_text())
        input_hashes[normalized_path(summary_path)] = semantic_json_sha256(
            summary_path
        )
        for run_index, run in enumerate(summary["runs"]):
            cover = run["hard_cover"]
            state_path = resolve(cover["relation_path"], relative_to=summary_path)
            graph_path = resolve(cover["graph_library_path"], relative_to=summary_path)
            input_hashes[normalized_path(state_path)] = sha256(state_path)
            input_hashes[normalized_path(graph_path)] = sha256(graph_path)
            states = load_jsonl(state_path, "state_id")
            graphs = load_jsonl(graph_path, "graph_id")
            for state_id in sorted(states):
                state = states[state_id]
                if state["terminal_classification"] not in ALLOWED_BASE:
                    continue
                for coverage in sorted(
                    state["raw_coverage"], key=lambda row: row["path_binding_id"]
                ):
                    source_id = str(coverage["source_graph_id"])
                    target_id = str(coverage["target_graph_id"])
                    source = graph_from_row(graphs[source_id])
                    target = graph_from_row(graphs[target_id])
                    inventory.append({
                        "base_summary": normalized_path(summary_path),
                        "base_run_index": run_index,
                        "base_state_id": state_id,
                        "base_path_binding_id": str(coverage["path_binding_id"]),
                        "fixed_full_root_case_id": str(coverage["root_case_id"]),
                        "selected_port_count": int(state["selected_port_count"]),
                        "source_parent_graph_id": source_id,
                        "target_parent_graph_id": target_id,
                        "source_parent_normalized_graph_id": graph_id(source),
                        "target_parent_normalized_graph_id": graph_id(target),
                        "base_dummy_order": coverage["dummy_order"],
                        "base_restored_role_to_label": coverage["restored_role_to_label"],
                        "source": source,
                        "target": target,
                    })
    inventory.sort(key=lambda row: (
        row["base_summary"], row["base_run_index"], row["base_state_id"],
        row["base_path_binding_id"],
    ))
    commitment_rows = []
    for index, row in enumerate(inventory):
        commitment_rows.append({
            "path_index": index,
            **{key: row[key] for key in (
                "base_summary", "base_run_index", "base_state_id",
                "base_path_binding_id", "fixed_full_root_case_id",
                "selected_port_count", "source_parent_graph_id",
                "target_parent_graph_id", "source_parent_normalized_graph_id",
                "target_parent_normalized_graph_id", "base_dummy_order",
                "base_restored_role_to_label",
            )},
        })
    return inventory, commitment_rows, input_hashes


class CompactCompiler:
    def __init__(self, bit_cache, witness_writer, transport_writer, polynomial_writer):
        self.invariants = load_invariants()
        self.bit_cache = bit_cache
        self.witness_writer = witness_writer
        self.transport_writer = transport_writer
        self.polynomial_writer = polynomial_writer
        self.sign_cache = {}
        self.witness_index = {}
        self.transport_index = {}
        self.polynomial_ids = set()
        self.counts = Counter()
        self.unresolved = set()

    def register_polynomial(self, poly) -> str:
        terms = tuple(
            (tuple(int(value) for value in exponent), int(coefficient))
            for exponent, coefficient in sorted(poly.items())
        )
        payload = {
            "schema": 1,
            "variable_count": len(terms[0][0]) if terms else 0,
            "terms": terms,
        }
        identifier = stable_hash(payload)
        if identifier not in self.polynomial_ids:
            self.polynomial_ids.add(identifier)
            self.polynomial_writer.write({
                "schema": 1,
                "polynomial_id": identifier,
                **payload,
            })
        return identifier

    def register_witness(self, relation: dict) -> int:
        payload = {
            "classification": relation["classification"],
            "probe_classification": relation["probe_classification"],
            "probe_witness": relation["probe_witness"],
        }
        identifier = stable_hash(payload)
        if identifier not in self.witness_index:
            index = len(self.witness_index)
            if index > INDEX_MASK:
                raise OverflowError("witness library exceeds compact index")
            self.witness_index[identifier] = index
            self.witness_writer.write({
                "schema": 1,
                "witness_index": index,
                "witness_id": identifier,
                **payload,
            })
        return self.witness_index[identifier]

    def register_transport(self, relation: dict) -> int:
        payload = {
            "classification": relation["classification"],
            "transport": relation["transport"],
            "canonicalization": relation["canonicalization"],
            "fourier_coordinate_transport": "identity_on_fixed_port_labels",
        }
        identifier = stable_hash(payload)
        if identifier not in self.transport_index:
            index = len(self.transport_index)
            if index > INDEX_MASK:
                raise OverflowError("transport library exceeds compact index")
            self.transport_index[identifier] = index
            self.transport_writer.write({
                "schema": 1,
                "transport_index": index,
                "transport_id": identifier,
                **payload,
            })
        return self.transport_index[identifier]

    def word(self, relation: dict) -> int:
        classification = relation["classification"]
        if classification not in CLASS_CODE:
            self.unresolved.add(classification)
            # Preserve the row shape, but make the run fail closed.
            return (7 << 29)
        if classification in SEPARATED:
            index = self.register_witness(relation)
        else:
            index = self.register_transport(relation)
        self.counts[classification] += 1
        return (CLASS_CODE[classification] << 29) | index

    def compile_path(self, entry: dict, path_index: int) -> dict:
        deck_cache = {}
        insertion_cache = {}
        relation_cache = {}

        def deck(gid: str, graph: RootedGraph, p: int):
            key = gid, p
            if key not in deck_cache:
                deck_cache[key] = full_deck(graph, p)
            return deck_cache[key]

        def inserted(parent_id: str, parent: RootedGraph, arc, label):
            key = parent_id, tuple(arc), label
            if key not in insertion_cache:
                child, deletion = insert_port(parent, tuple(arc), label)
                insertion_cache[key] = graph_id(child), child, deletion
            return insertion_cache[key]

        def classify(source_id, source, target_id, target, p, parent_transport):
            key = source_id, target_id, p, parent_transport
            if key in relation_cache:
                return relation_cache[key]
            probe, witness = relation_witness(
                deck(source_id, source, p), deck(target_id, target, p),
                self.invariants, self.bit_cache, self.sign_cache,
                register_polynomial=self.register_polynomial,
                exact_sign=True,
            )
            relation = {
                "probe_classification": probe,
                "probe_witness": witness,
            }
            if probe in SEPARATED:
                relation["classification"] = probe
            elif probe == "equal_invariant_signature":
                source_code = canonical_mixed(sd0(source))[0]
                target_code = canonical_mixed(sd0(target))[0]
                try:
                    _code, child_transport, canonical = quotient_transport(source, target)
                except ValueError:
                    relation["classification"] = "unresolved_equal_non_T"
                else:
                    if not restricts_to(child_transport, parent_transport):
                        relation["classification"] = "incoherent_isomorphism_or_T"
                    else:
                        relation["classification"] = (
                            "labelled_isomorphism"
                            if source_code == target_code else "ordinary_T"
                        )
                        relation["transport"] = transport_metadata(
                            source, target, child_transport
                        )
                        relation["canonicalization"] = canonical
            else:
                relation["classification"] = probe
            relation_cache[key] = relation
            return relation

        source_parent = entry["source"]
        target_parent = entry["target"]
        source_parent_id = graph_id(source_parent)
        target_parent_id = graph_id(target_parent)
        if source_parent_id != entry["source_parent_normalized_graph_id"]:
            raise AssertionError((path_index, "source normalized base graph ID"))
        if target_parent_id != entry["target_parent_normalized_graph_id"]:
            raise AssertionError((path_index, "target normalized base graph ID"))

        _code, base_transport, base_canonical = quotient_transport(
            source_parent, target_parent
        )
        base_relation = {
            "classification": (
                "labelled_isomorphism"
                if canonical_mixed(sd0(source_parent))[0]
                == canonical_mixed(sd0(target_parent))[0]
                else "ordinary_T"
            ),
            "transport": transport_metadata(
                source_parent, target_parent, base_transport
            ),
            "canonicalization": base_canonical,
        }
        base_transport_index = self.register_transport(base_relation)

        p0 = int(entry["selected_port_count"])
        p_label = f"L_{p0}"
        source_p_arcs = admissible_internal_arcs(source_parent)
        target_p_arcs = admissible_internal_arcs(target_parent)
        p_words = []
        q_words = []
        q_shapes = []
        allowed_p_indices = []
        for source_arc in source_p_arcs:
            source_p_id, source_p, _source_delete = inserted(
                source_parent_id, source_parent, source_arc, p_label
            )
            for target_arc in target_p_arcs:
                target_p_id, target_p, _target_delete = inserted(
                    target_parent_id, target_parent, target_arc, p_label
                )
                relation_p = classify(
                    source_p_id, source_p, target_p_id, target_p,
                    p0 + 1, base_transport,
                )
                p_flat = len(p_words)
                p_words.append(self.word(relation_p))
                if relation_p["classification"] not in ALLOWED_CHILD:
                    continue
                allowed_p_indices.append(p_flat)
                child_transport = tuple(
                    tuple(pair)
                    for pair in relation_p["transport"]["vertex_transport"]
                )
                source_q_arcs = admissible_internal_arcs(source_p)
                target_q_arcs = admissible_internal_arcs(target_p)
                q_shapes.append((len(source_q_arcs), len(target_q_arcs)))
                q_label = f"L_{p0 + 1}"
                for source_q_arc in source_q_arcs:
                    source_q_id, source_q, _source_q_delete = inserted(
                        source_p_id, source_p, source_q_arc, q_label
                    )
                    for target_q_arc in target_q_arcs:
                        target_q_id, target_q, _target_q_delete = inserted(
                            target_p_id, target_p, target_q_arc, q_label
                        )
                        relation_q = classify(
                            source_q_id, source_q, target_q_id, target_q,
                            p0 + 2, child_transport,
                        )
                        q_words.append(self.word(relation_q))

        row_payload = {
            "schema": 1,
            "path_index": path_index,
            **{key: entry[key] for key in (
                "base_summary", "base_run_index", "base_state_id",
                "base_path_binding_id", "fixed_full_root_case_id",
                "selected_port_count", "source_parent_graph_id",
                "target_parent_graph_id", "source_parent_normalized_graph_id",
                "target_parent_normalized_graph_id", "base_dummy_order",
                "base_restored_role_to_label",
            )},
            "base_transport_index": base_transport_index,
            "source_p_arcs": source_p_arcs,
            "target_p_arcs": target_p_arcs,
            "p_word_count": len(p_words),
            "p_words_base64_le_u32": pack_words(p_words),
            "allowed_p_flat_indices": allowed_p_indices,
            "q_shapes": q_shapes,
            "q_word_count": len(q_words),
            "q_words_base64_le_u32": pack_words(q_words),
        }
        return {
            "path_record_id": stable_hash(row_payload),
            **row_payload,
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-summary", action="append", type=Path, required=True)
    parser.add_argument("--bit-cache", type=Path, required=True)
    parser.add_argument("--path-start", type=int, default=0)
    parser.add_argument("--path-stop", type=int)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    inventory, commitment_rows, input_hashes = collect_base_paths(args.base_summary)
    inventory_count = len(inventory)
    start = int(args.path_start)
    stop = inventory_count if args.path_stop is None else int(args.path_stop)
    if not (0 <= start <= stop <= inventory_count):
        raise SystemExit(("invalid path range", start, stop, inventory_count))

    cert = HERE / "certificates"
    paths_writer = JsonlGzipWriter(cert / f"compact_probe_paths_{args.tag}.jsonl.gz")
    witness_writer = JsonlGzipWriter(cert / f"compact_probe_witnesses_{args.tag}.jsonl.gz")
    transport_writer = JsonlGzipWriter(cert / f"compact_probe_transports_{args.tag}.jsonl.gz")
    polynomial_writer = JsonlGzipWriter(cert / f"compact_probe_polynomials_{args.tag}.jsonl.gz")
    compiler = CompactCompiler(
        load_bit_cache(args.bit_cache), witness_writer, transport_writer,
        polynomial_writer,
    )

    for path_index in range(start, stop):
        row = compiler.compile_path(inventory[path_index], path_index)
        paths_writer.write(row)
        if (path_index - start + 1) % 10 == 0:
            print(json.dumps({
                "compact_probe_progress": {
                    "completed_paths": path_index - start + 1,
                    "shard_paths": stop - start,
                    "global_path_index": path_index,
                    "classification_counts": dict(sorted(compiler.counts.items())),
                }
            }, sort_keys=True), flush=True)

    streams = {
        "paths": paths_writer.close(),
        "witnesses": witness_writer.close(),
        "transports": transport_writer.close(),
        "polynomials": polynomial_writer.close(),
    }
    summary = {
        "schema": "compact-path-bound-probe-extension-v1",
        "status": "UNRESOLVED" if compiler.unresolved else "EXACTLY_COMPUTED",
        "schema_specification": normalized_path(HERE / "COMPACT_PROBE_SCHEMA.md"),
        "schema_specification_sha256": sha256(HERE / "COMPACT_PROBE_SCHEMA.md"),
        "base_summaries": sorted(
            normalized_path(path) for path in args.base_summary
        ),
        "input_sha256": dict(sorted(input_hashes.items())),
        "bit_cache": {
            "path": normalized_path(args.bit_cache),
            "sha256": sha256(args.bit_cache),
        },
        "path_inventory_count": inventory_count,
        "path_inventory_sha256": inventory_commitment(commitment_rows),
        "path_range": [start, stop],
        "path_records": stop - start,
        "counts": dict(sorted(compiler.counts.items())),
        "unresolved_classifications": sorted(compiler.unresolved),
        "streams": streams,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": summary["status"],
        "path_range": summary["path_range"],
        "counts": summary["counts"],
        "output": normalized_path(args.output),
        "sha256": sha256(args.output),
    }, sort_keys=True), flush=True)
    if compiler.unresolved:
        raise SystemExit(("unresolved compact probe classifications", sorted(compiler.unresolved)))


if __name__ == "__main__":
    main()
