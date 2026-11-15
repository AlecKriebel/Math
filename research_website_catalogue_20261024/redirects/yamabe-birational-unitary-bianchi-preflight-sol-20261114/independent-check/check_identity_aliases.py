"""Bounded independent identity check; no PDF extraction, network, or Git mutation.

Run with python -B. Outputs evidence ONLY beside this file. corpus() reads and
authenticates released Git blobs and pre-existing complete PDF text derivatives.
"""
from pathlib import Path
import datetime
import hashlib
import importlib.util
import json
import re
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PACKET = HERE.parent
spec = importlib.util.spec_from_file_location("preflight_core", PACKET / "preflight_core.py")
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

ALIASES = {
    "yamabe_aliases": r"heat.{0,12}trace|conformal.{0,15}(weight|laplacian)|round.{0,12}(three|3).{0,10}sphere|pinocchio|morpurgo|weighted.yamabe|2338395[12]|weighted-yamabe-heat-trace",
    "birational_aliases": r"prime.{0,15}field|totient|vivaldi|period.{0,15}distribut|triangular.{0,15}map|cycle.nonlimit|2353973[34]|fixed-birational|Oberwolfach.pdf|0902.3884|1803.01435|1308.5701|Roberts.pdf",
    "bianchi_aliases": r"\bbianchi\b|zero.{0,8}area|negative.{0,8}mass|dadhich|mukherjee|visser|burtscher|kiessling|tahvildar|harmonically.{0,12}regular|2332081[78]|weak-bianchi",
    "unitary_aliases": r"2292985[67]|AMR.066.0025|gromov.{0,15}unitary|unitary.{0,30}map|lipschitz.{0,25}(deform|contract)|Cayley|Mobius",
}

bindings, extracts, reps, html, data, raw = core.corpus()
by_path = {b["path"]: b for b in bindings}
evidence = {
    "UTC": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "completion_percent": 100,
    "goal": "bounded independent adversarial legacy correspondence check only",
    "commit": core.COMMIT,
    "docs_tree": core.TREE,
    "authenticated_counts": {"blobs": len(bindings), "reused_PDF_extracts": len(extracts), "representations": len(reps), "HTML": len(html)},
    "new_or_repeated_PDF_extractions": 0,
    "queries": ALIASES,
    "search_method": "core.norm then re.finditer with re.I; raw HTML omitted from alias display to avoid duplicating decoded visible HTML, but separately searched for attribute-only blindspots below",
    "hits": [],
    "raw_HTML_hits": [],
    "article_identities": html,
    "target_full_asset_comparisons": [],
}
for group, pattern in ALIASES.items():
    for item in reps:
        text = core.norm(item["text"])
        hits = [{"match": m.group(), "offset": m.start(), "context": text[max(0, m.start()-100):m.end()+160]} for m in re.finditer(pattern, text, re.I)]
        if hits:
            row = {"group": group, "path": item["path"], "kind": item["kind"], "released_binding": by_path[item["path"]], "hits": hits}
            key = "raw_HTML_hits" if item["kind"] == "raw_UTF8_blob" and item["path"].endswith(".html") else "hits"
            evidence[key].append(row)
for record_id in core.RECORDS:
    source = PACKET.parent.parent / "papers" / record_id / "sources"
    record = json.loads((source / "record.raw.json").read_text())
    for file in record["files"]:
        asset = source / file["key"]
        body = asset.read_bytes()
        digest = hashlib.sha256(body).hexdigest()
        evidence["target_full_asset_comparisons"].append({"record": record_id, "key": file["key"], "bytes": len(body), "sha256": digest, "exact_matches": [b for b in bindings if b["bytes"] == len(body) and b["sha256"] == digest]})
out = HERE / "ALIAS_IDENTITY_EVIDENCE.json"
out.write_text(json.dumps(evidence, indent=2) + "\n")
print(json.dumps({"evidence": str(out), "hits_by_group": {g: sum(len(x["hits"]) for x in evidence["hits"] if x["group"] == g) for g in ALIASES}, "raw_HTML_hits_by_group": {g: sum(len(x["hits"]) for x in evidence["raw_HTML_hits"] if x["group"] == g) for g in ALIASES}}, indent=2))
