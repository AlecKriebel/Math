#!/usr/bin/env python3
"""Generate immutable clean-room universes and derived invariant families."""

from pathlib import Path
import argparse
import gzip
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from derived_invariants import derive_family, family_metadata
from graph_model import digest, stable_json
from relation_universe import (
    completion_object, generate_completions, generate_sources, load_cores,
    load_support, source_object, templates, universe_summary,
)


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


def write_gzip_json(path, obj):
    data = (stable_json(obj) + "\n").encode()
    with gzip.GzipFile(filename=str(path), mode="wb", mtime=0) as f: f.write(data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selected-total", type=int, required=True)
    ap.add_argument("--source-outgoing", type=int, required=True)
    ap.add_argument("--minimum-only", action="store_true")
    ap.add_argument("--tag", required=True)
    args = ap.parse_args()
    support_path = ROOT / "primary/certificates/support_universe.json"
    core_path = ROOT / "primary/certificates/core_universe.json"
    records = load_support(support_path); cores = load_cores(core_path); ts = templates(records, cores)
    sources = generate_sources(records, args.source_outgoing, args.minimum_only)
    completions = generate_completions(ts, args.selected_total)
    family = derive_family([x.graph for x in sources], max_degree=3)
    outdir = HERE / "certificates"; outdir.mkdir(exist_ok=True)
    payload = {
        "schema": 1, "tag": args.tag,
        "inputs": {str(support_path.relative_to(ROOT)): sha(support_path), str(core_path.relative_to(ROOT)): sha(core_path)},
        "selected_total": args.selected_total, "source_outgoing": args.source_outgoing,
        "minimum_only": args.minimum_only,
        "summary": universe_summary(sources, completions),
        "sources": [source_object(x) for x in sources],
        "completions": [completion_object(x) for x in completions],
    }
    payload["normalized_sha256_without_hash"] = digest(payload)
    write_gzip_json(outdir / f"universe_{args.tag}.json.gz", payload)
    fam = {"schema": 1, "tag": args.tag, "metadata": family_metadata(family), "relations": family}
    fam["normalized_sha256_without_hash"] = digest(fam)
    write_gzip_json(outdir / f"family_{args.tag}.json.gz", fam)
    print(stable_json({"universe": payload["summary"], "family": fam["metadata"], "hash": payload["normalized_sha256_without_hash"]}))


if __name__ == "__main__": main()

