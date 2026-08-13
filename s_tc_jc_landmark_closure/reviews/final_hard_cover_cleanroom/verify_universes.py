#!/usr/bin/env python3
"""Regenerate and audit the clean-room n=3 and n=4 minimum universes."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import gzip
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from graph_model import digest, mixed_code, rooted_code, stable_json, standard_semidirected_audit
from relation_universe import (
    generate_completions, generate_sources, load_cores, load_support,
    templates, universe_summary,
)


EXPECTED = {
    "n3": {
        "source_supports": 8,
        "completion_bases": 1463,
        "completion_origins_before_quotient": 2814,
        "by_core": {"cycle": 13, "theta-0": 284, "theta-1": 149, "theta-2": 333, "theta-3": 684},
    },
    "n4_minimum": {
        "source_supports": 3,
        "completion_bases": 3026,
        "completion_origins_before_quotient": 6138,
        "by_core": {"cycle": 15, "theta-0": 532, "theta-1": 281, "theta-2": 698, "theta-3": 1500},
    },
}


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load_gzip_json(path):
    with gzip.open(path, "rt") as stream:
        return json.load(stream)


def essential_existing(payload):
    source = {
        x["source_id"]: {
            "rooted": rooted_code_from_object(x["graph"]),
            "core": x["core_id"],
            "words": tuple(map(tuple, x["words"])),
        }
        for x in payload["sources"]
    }
    completion = {
        x["completion_id"]: {
            "rooted": rooted_code_from_object(x["graph"]),
            "core": x["core_id"],
            "incoming_selected": x["incoming_selected"],
            "dummy_order": tuple(x["dummy_order"]),
            "origin_ids": tuple(x["origin_ids"]),
        }
        for x in payload["completions"]
    }
    return source, completion


def rooted_code_from_object(obj):
    from relation_universe import graph_from_object
    return rooted_code(graph_from_object(obj))[0]


def essential_regenerated(sources, completions):
    source = {
        x.source_id: {
            "rooted": rooted_code(x.graph)[0],
            "core": x.core_id,
            "words": tuple(x.words),
        }
        for x in sources
    }
    completion = {
        x.completion_id: {
            "rooted": rooted_code(x.graph)[0],
            "core": x.core_id,
            "incoming_selected": x.incoming_selected,
            "dummy_order": tuple(x.dummy_order),
            "origin_ids": tuple(x.origin_ids),
        }
        for x in completions
    }
    return source, completion


def audit_case(tag, records, ts, outgoing, selected, minimum):
    sources = generate_sources(records, outgoing, minimum)
    completions = generate_completions(ts, selected)
    summary = universe_summary(sources, completions)
    for key, value in EXPECTED[tag].items():
        if summary[key] != value:
            raise AssertionError((tag, key, summary[key], value))
    all_graphs = [x.graph for x in sources] + [x.graph for x in completions]
    failures = []
    for i, graph in enumerate(all_graphs):
        audit = standard_semidirected_audit(graph)
        if not audit["ok"]: failures.append((i, audit))
    if failures: raise AssertionError((tag, "standard S_TC failures", failures[:3]))
    rooted_codes = [rooted_code(x.graph)[0] for x in completions]
    if len(rooted_codes) != len(set(rooted_codes)):
        raise AssertionError((tag, "completion quotient is not duplicate-free"))

    frozen = load_gzip_json(HERE / "certificates" / f"universe_{tag}.json.gz")
    old_source, old_completion = essential_existing(frozen)
    new_source, new_completion = essential_regenerated(sources, completions)
    if old_source != new_source or old_completion != new_completion:
        raise AssertionError((tag, "frozen universe differs from regeneration"))
    return {
        "summary": summary,
        "source_commitment": digest(new_source),
        "completion_commitment": digest(new_completion),
        "standard_stc_graph_count": len(all_graphs),
        "standard_stc_failures": 0,
        "rooted_completion_codes_unique": True,
        "frozen_regeneration_equal": True,
    }


def main():
    support_path = ROOT / "primary/certificates/support_universe.json"
    core_path = ROOT / "primary/certificates/core_universe.json"
    records = load_support(support_path); cores = load_cores(core_path)
    ts = templates(records, cores)
    cert = {
        "schema": 1,
        "status": "VERIFIED",
        "input_sha256": {
            str(support_path.relative_to(ROOT)): sha(support_path),
            str(core_path.relative_to(ROOT)): sha(core_path),
        },
        "minimum_repair_template_count": len(ts),
        "cases": {
            "n3": audit_case("n3", records, ts, 3, 4, False),
            "n4_minimum": audit_case("n4_minimum", records, ts, 4, 5, True),
        },
        "criterion": (
            "rooted witness plus simple binary sd_0 plus every tail of a retained "
            "reticulation edge incident with two wholly undirected edges"
        ),
    }
    cert["normalized_sha256_without_hash"] = digest(cert)
    out = HERE / "certificates" / "universe_regeneration_certificate.json"
    out.write_text(stable_json(cert) + "\n")
    print(stable_json({
        "status": cert["status"],
        "counts": {k: v["summary"] for k, v in cert["cases"].items()},
        "hash": cert["normalized_sha256_without_hash"],
    }))


if __name__ == "__main__":
    main()
