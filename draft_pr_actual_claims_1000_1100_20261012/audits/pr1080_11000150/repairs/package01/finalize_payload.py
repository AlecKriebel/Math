#!/usr/bin/env python3
"""One-time bounded repair stage resolution and deterministic payload seal."""
import hashlib
import json
from pathlib import Path

AUDIT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
KIT = AUDIT / "preprint_v1_0/verification_kit"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def dump(p, d):
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")


def main():
    # Locate exact historical bytes among current canonical or captured-stage
    # files. No reference is resolved by comparing it to a changed live path.
    by_hash = {}
    for p in sorted(KIT.rglob("*")):
        if p.is_file():
            by_hash.setdefault((p.stat().st_size, sha(p)), p.relative_to(KIT).as_posix())
    refs = []
    inventories = [
        ("immediate-before-repair01", WORK / "IMMEDIATE_INPUT_PINS.json", ""),
        ("preparation-input194", AUDIT / "preprint_v1_0/INPUT_PINS.json", ""),
        ("preparation-output90", AUDIT / "preprint_v1_0/OUTPUT_PINS.json", "preprint_v1_0/"),
        ("whole01-input289", AUDIT / "reviews/package_01/INPUT_PINS.json", ""),
        ("whole01-output17", AUDIT / "reviews/package_01/OUTPUT_PINS.json", "reviews/package_01/"),
    ]
    counts = {}
    for stage, inventory, prefix in inventories:
        rows = json.loads(inventory.read_text())["files"]
        counts[stage] = len(rows)
        for old in rows:
            r = {"stage": stage, "inventory": inventory.relative_to(AUDIT).as_posix(),
                 "original_path": prefix + old["path"], "bytes": old["bytes"], "sha256": old["sha256"]}
            destination = by_hash.get((old["bytes"], old["sha256"]))
            if destination:
                r.update(disposition="exact_captured_stage_or_canonical_copy", destination=destination)
            else:
                name = r["original_path"]
                if "/sources/" in name or "/sources_raw/" in name or name.endswith((".pdf", ".png")):
                    reason = "Third-party body, extract or visual derivative is excluded from distribution; exact historical custody is preserved by this individual path/size/hash, without delivered-body or replay claims."
                elif "LIVE_PR" in name or "/inputs/git/" in name or "/inputs/submitted/" in name or "/root_reproduction/" in "/" + name:
                    reason = "Raw service/Git or duplicate workspace reproduction is not distributed; authored canonical evidence is retained. This particular path is individually omitted, not recreated."
                else:
                    reason = "Earlier administrative or derivative workspace artifact is individually omitted from the portable kit; its exact historical path/size/hash is recorded without claiming historical full-seal replay."
                r.update(disposition="omitted", reason=reason)
            refs.append(r)
    dump(KIT / "REPAIR01_HISTORY_RESOLUTION.json", {"scope": "Historical stage references retain original hashes. Exact copied bytes resolve changed paths; all omissions are individual and disclosed. The unchanged original 269-reference ledger is verified separately.",
        "inventory_counts": counts, "references": refs})
    names = sorted(p.relative_to(KIT).as_posix() for p in KIT.rglob("*") if p.is_file())
    names = sorted(set(names) | {"ALLOWLIST.json", "MANIFEST.json"})
    dump(KIT / "ALLOWLIST.json", {"members": names})
    dump(KIT / "MANIFEST.json", {"self_hash_scope": "All allowlisted members except MANIFEST.json",
         "files": [{"path": n, "bytes": (KIT / n).stat().st_size, "sha256": sha(KIT / n)} for n in names if n != "MANIFEST.json"]})
    print(json.dumps({"members": len(names), "historical_inventory_counts": counts,
                      "exact_resolutions": sum(r["disposition"] != "omitted" for r in refs),
                      "omissions": sum(r["disposition"] == "omitted" for r in refs),
                      "manifest_sha256": sha(KIT / "MANIFEST.json")}))


if __name__ == "__main__":
    main()
