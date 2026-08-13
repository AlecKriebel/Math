#!/usr/bin/env python3
"""Independent exact equal-deck root-relation screen, shardable by completion."""

from pathlib import Path
import argparse
import gzip
import itertools
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from family_engine import classify_containment_pair, exact_family_deck
from graph_model import digest, mixed_code, rooted_code, stable_json
from jc_exact import deck_hash, descriptor_from_graph, permute_descriptor
from relation_universe import graph_from_object, relabel_selected


def load_gz(path):
    with gzip.open(path, "rt") as f: return json.load(f)


def family_tuple(obj):
    return tuple(tuple((int(c), tuple(int(i) for i in mon)) for c, mon in rel) for rel in obj["relations"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--start", type=int, required=True)
    ap.add_argument("--stop", type=int, required=True)
    ap.add_argument("--mode", choices=("equal", "containment"), default="containment")
    args = ap.parse_args()
    U = load_gz(HERE / f"certificates/universe_{args.tag}.json.gz")
    Fobj = load_gz(HERE / f"certificates/family_{args.tag}.json.gz"); family = family_tuple(Fobj)
    sources = []
    for x in U["sources"]:
        g = graph_from_object(x["graph"]); d = descriptor_from_graph(g)
        deck = exact_family_deck(d, U["selected_total"], family)
        sources.append((x, g, deck, rooted_code(g)[0], mixed_code(g)[0]))
    records = {}; descriptor_count = 0; accepted_raw = 0
    class_counts = {"equal_deck": 0, "unequal_necessary": 0, "generic_identity_separation": 0, "strict_sign_separation": 0}
    completions = U["completions"][args.start:min(args.stop, len(U["completions"]))]
    for local_i, c in enumerate(completions):
        if not c["dummy_order"]: continue
        g0 = graph_from_object(c["graph"]); d0 = descriptor_from_graph(g0)
        for perm in itertools.permutations(range(U["selected_total"])):
            d = permute_descriptor(d0, perm)
            descriptor_count += 1
            accepted = []
            for sx, sg, sd, sr, sm in sources:
                if args.mode == "equal":
                    deck = exact_family_deck(d, U["selected_total"], family)
                    if sd == deck: accepted.append((sx, sg, sd, sr, sm, "equal_deck", None, 0))
                    continue
                result = classify_containment_pair(sd, d, U["selected_total"], family)
                category = result["classification"]
                if category in ("generic_identity_separation", "strict_sign_separation"):
                    class_counts[category] += 1; continue
                deck = result["target_deck"]
                accepted.append((sx, sg, sd, sr, sm, category, None, result["target_only_unsigned_count"]))
            if not accepted: continue
            tg = relabel_selected(g0, perm); tr, _ = rooted_code(tg); tm, _ = mixed_code(tg)
            for sx, sg, sd, sr, sm, category, witness, target_only_count in accepted:
                accepted_raw += 1; class_counts[category] += 1
                key_obj = {
                    "source_rooted": sr, "source_mixed": sm,
                    "target_full_rooted": tr, "target_full_mixed": tm,
                    "dummy_order": c["dummy_order"],
                }
                rid = digest(key_obj)
                provenance = {
                    "completion_id": c["completion_id"], "completion_origin_ids": c["origin_ids"],
                    "permutation_old_to_physical": list(perm), "source_id": sx["source_id"],
                }
                if rid not in records:
                    records[rid] = {
                        "schema": 1, "relation_id": rid, **key_obj,
                        "selected_deck_sha256": deck_hash(deck), "provenances": [],
                        "candidate_classification": category,
                        "target_only_unsigned_count": target_only_count,
                    }
                elif records[rid]["candidate_classification"] != category:
                    raise AssertionError("canonical relation received inconsistent classification")
                records[rid]["provenances"].append(provenance)
        if (local_i + 1) % 25 == 0:
            print(stable_json({"processed": args.start + local_i + 1, "relations": len(records), "accepted_raw": accepted_raw}), flush=True)
    for rec in records.values():
        rec["provenances"] = sorted(rec["provenances"], key=stable_json)
        rec["binding_sha256"] = digest({k: v for k, v in rec.items() if k != "binding_sha256"})
    mode_tag = "eq" if args.mode == "equal" else "contain"
    out = HERE / "certificates" / f"root_{args.tag}_{mode_tag}_{args.start:04d}_{args.stop:04d}.jsonl.gz"
    with gzip.GzipFile(filename=str(out), mode="wb", mtime=0) as f:
        for rid in sorted(records): f.write((stable_json(records[rid]) + "\n").encode())
    summary = {
        "schema": 1, "tag": args.tag, "start": args.start, "stop": args.stop,
        "canonical_relations": len(records), "accepted_raw": accepted_raw,
        "classification_requests": class_counts, "mode": args.mode,
        "descriptor_requests": descriptor_count,
        "family_sha256": Fobj["normalized_sha256_without_hash"],
        "record_commitment": digest([records[x]["binding_sha256"] for x in sorted(records)]),
    }
    (HERE / "certificates" / f"root_{args.tag}_{mode_tag}_{args.start:04d}_{args.stop:04d}.summary.json").write_text(stable_json(summary) + "\n")
    print(stable_json(summary))


if __name__ == "__main__": main()
