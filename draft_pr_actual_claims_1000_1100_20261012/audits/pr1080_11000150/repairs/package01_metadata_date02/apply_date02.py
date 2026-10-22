#!/usr/bin/env python3
"""One-time administrative successor; prior completed repair files are immutable."""
import collections
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

WORK = Path(__file__).resolve().parent
AUDIT = WORK.parents[1]
OLD = AUDIT / "repairs/package01"
DELIVERY = AUDIT / "preprint_v1_0"
KIT = DELIVERY / "verification_kit"
NOTES = ("Prepared locally on 2026-10-14 before deposit or publication. "
         "At the bounded-repair checkpoint on 2026-10-14, one complete whole-candidate review had been completed, "
         "a fresh complete second review was required, and publication readiness had not yet been affirmed. "
         "Later readiness/publication state is recorded separately.")
CHANGED = ["preprint_v1_0/metadata.json", "preprint_v1_0/deposit_metadata.json",
           "preprint_v1_0/README.md", "preprint_v1_0/EXTERNAL_BINDING.json",
           "preprint_v1_0/verification_kit.zip", "preprint_v1_0/verification_kit/metadata.json",
           "preprint_v1_0/verification_kit/README.md", "preprint_v1_0/verification_kit/ALLOWLIST.json",
           "preprint_v1_0/verification_kit/MANIFEST.json", "preprint_v1_0/verification_kit/REPAIR01_STAGE_COPIES.json",
           "preprint_v1_0/verification_kit/REPAIR01_HISTORY_RESOLUTION.json"]


def require(test, message):
    if not test:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row(path, root):
    return {"path": path.relative_to(root).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path)}


def dump(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def main():
    baseline = json.loads((WORK / "IMMEDIATE_INPUT_PINS.json").read_text())["files"]
    require(len(baseline) == 404, "Unexpected immediate stage")
    for r in baseline:
        require(row(AUDIT / r["path"], AUDIT) == r, "Input changed before administrative substage: " + r["path"])
    require(not (WORK / "BEFORE_COPIES.json").exists(), "Refuse repeated mutation")
    old_output = json.loads((OLD / "OUTPUT_PINS.json").read_text())["files"]
    require(len(old_output) == 42 and sha(OLD / "OUTPUT_PINS.json") == "8b5444acd30147e16af62d52067d2ef1395eed1e27f01b3c6ce9da0c5d47306a"
            and sha(OLD / "TERMINAL_SEAL.json") == "e5978cb4ddc9e41d7c00e54543085e6f5a862593b1bfb5df0f2b08950a85462b", "Prior repair seal differs")
    for r in old_output:
        require(row(OLD / r["path"], OLD) == r, "Prior output differs")
    copies = []

    def capture(name, source, destination, stage):
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        require(source.read_bytes() == destination.read_bytes(), "Captured-stage copy differs")
        copies.append({"original_path": name, "source_snapshot": source.relative_to(AUDIT).as_posix(),
                       "destination": destination.relative_to(KIT).as_posix(), "bytes": source.stat().st_size,
                       "sha256": sha(source), "stage": stage})

    for name in CHANGED:
        source = AUDIT / name
        saved = WORK / "before" / name
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, saved)
        capture(name, saved, KIT / "metadata_date02_history/before" / name, "Exact immediate bytes before dated-metadata substage02")
    dump(WORK / "BEFORE_COPIES.json", {"files": copies[:]})
    for p in [OLD / r["path"] for r in old_output] + [OLD / "OUTPUT_PINS.json", OLD / "TERMINAL_SEAL.json"]:
        capture(p.relative_to(AUDIT).as_posix(), p,
                KIT / "metadata_date02_history/prior_repair01" / p.relative_to(OLD),
                "Immutable completed repair01 output and separate inventory/seal")
    capture("repairs/package01_metadata_date02/IMMEDIATE_INPUT_PINS.json", WORK / "IMMEDIATE_INPUT_PINS.json",
            KIT / "metadata_date02_history/admin/IMMEDIATE_INPUT_PINS.json", "New substage immediate inventory; exact frozen bytes")

    previous = json.loads((WORK / "before/preprint_v1_0/metadata.json").read_text())
    require(previous == json.loads((WORK / "before/preprint_v1_0/verification_kit/metadata.json").read_text())
            == json.loads((WORK / "before/preprint_v1_0/deposit_metadata.json").read_text())["metadata"], "Prior native objects differ")
    native = dict(previous)
    native["notes"] = NOTES
    require({k: v for k, v in native.items() if k != "notes"} == {k: v for k, v in previous.items() if k != "notes"}, "Non-note native field changed")
    dump(DELIVERY / "metadata.json", native)
    dump(KIT / "metadata.json", native)
    wrapper = json.loads((WORK / "before/preprint_v1_0/deposit_metadata.json").read_text())
    wrapper["metadata"] = native
    dump(DELIVERY / "deposit_metadata.json", wrapper)
    for p in [DELIVERY / "README.md", KIT / "README.md"]:
        p.write_text(p.read_text() + "\n## Dated metadata administrative substage\n\n"
                     "Native metadata workflow notes now explicitly describe the bounded-repair checkpoint on 14 October 2026, in the past tense. "
                     "They do not assert a permanent pending review or nonpublication state. The title, description, authors, ORCID, publication date, version, license, mathematical paper and source credits are unchanged. "
                     "Later readiness/publication state is recorded separately. The dated-metadata substage on 15 October 2026 is still pending a NEW complete whole02; current readiness/publication remain false and services remain held at PR1032. "
                     "Completed repair01 outputs and its 42-output inventory/seal remain immutable captured stages. "
                     "The existing stage-copy ledger appends exact new before/captured-output copies, and the history-resolution ledger preserves every old row and appends exact successor-stage references with individual omissions. "
                     "`METADATA_DATE02_ADMIN_STAGE.json` records the dated successor checkpoint. No new compilation, rendering or page view occurred in this administrative substage.\n")
    dump(KIT / "METADATA_DATE02_ADMIN_STAGE.json", {
        "as_of_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "stage": "dated native workflow metadata successor",
        "scope": "Only native notes and dependent documentation/custody/archive changed; all other native bibliographic fields and paper bytes unchanged.",
        "native_notes": NOTES, "prior_repair_output_inventory_sha256": sha(OLD / "OUTPUT_PINS.json"),
        "prior_repair_terminal_seal_sha256": sha(OLD / "TERMINAL_SEAL.json"),
        "whole_reviews_completed": 1, "minimum_whole_reviews": 2, "fresh_whole02_required": True,
        "publication_ready": False, "published": False, "services_held_at": 1032,
        "historical_status_rule": "All older inventories, seals and dated workflow statements retain their exact captured-stage meaning; current or later state does not retroactively rewrite them."})
    stages = json.loads((WORK / "before/preprint_v1_0/verification_kit/REPAIR01_STAGE_COPIES.json").read_text())
    require(len(stages["files"]) == 44, "Prior stage-copy count differs")
    stages["files"] += copies
    stages["metadata_date02_append_scope"] = "Original 44 entries unchanged; 56 appended exact copies preserve the 11 immediate changed artifacts, all 42 prior repair outputs and their inventory/seal, plus the new frozen inventory."
    dump(KIT / "REPAIR01_STAGE_COPIES.json", stages)

    by_hash = {}
    for p in sorted(KIT.rglob("*")):
        if p.is_file() and p.relative_to(AUDIT).as_posix() not in CHANGED:
            by_hash.setdefault((p.stat().st_size, sha(p)), p.relative_to(KIT).as_posix())
    history = json.loads((WORK / "before/preprint_v1_0/verification_kit/REPAIR01_HISTORY_RESOLUTION.json").read_text())
    require(len(history["references"]) == 899, "Prior history count differs")
    inventories = [
        ("metadata-date02-immediate404", WORK / "IMMEDIATE_INPUT_PINS.json", ""),
        ("repair01-current360", OLD / "CURRENT_INPUT_PINS.json", ""),
        ("repair01-protected298", OLD / "PROTECTED_INPUT_PINS.json", ""),
        ("repair01-output42", OLD / "OUTPUT_PINS.json", "repairs/package01/"),
        ("repair01-immediate309", OLD / "IMMEDIATE_INPUT_PINS.json", "")]
    appended = []
    for stage, inventory, prefix in inventories:
        records = json.loads(inventory.read_text())["files"]
        history["inventory_counts"][stage] = len(records)
        for old in records:
            r = {"stage": stage, "inventory": inventory.relative_to(AUDIT).as_posix(), "original_path": prefix + old["path"],
                 "bytes": old["bytes"], "sha256": old["sha256"]}
            destination = by_hash.get((old["bytes"], old["sha256"]))
            if destination:
                r.update(disposition="exact_captured_stage_or_canonical_copy", destination=destination)
            else:
                r.update(disposition="omitted", reason="This exact source/body/image/raw capture or derivative workspace/admin path is individually excluded from the portable archive. Its original path, size and hash are retained; no delivered-body or complete historical execution claim is made.")
            appended.append(r)
    history["references"] += appended
    history["metadata_date02_append_scope"] = "All original 899 reference rows are unchanged. Additional exact rows preserve five successor/prior-repair inventories; each omitted path has an individual explanation."
    dump(KIT / "REPAIR01_HISTORY_RESOLUTION.json", history)
    names = sorted(p.relative_to(KIT).as_posix() for p in KIT.rglob("*") if p.is_file())
    dump(KIT / "ALLOWLIST.json", {"members": names})
    dump(KIT / "MANIFEST.json", {"self_hash_scope": "All allowlisted members except MANIFEST.json",
         "files": [row(KIT / name, KIT) for name in names if name != "MANIFEST.json"]})
    require(len(names) == 178 and len(stages["files"]) == 100 and len(history["references"]) == 2312, "Unexpected new payload/custody counts")
    binding = json.loads((WORK / "before/preprint_v1_0/EXTERNAL_BINDING.json").read_text())
    require(sha(DELIVERY / "EXTERNAL_BINDING.json") == sha(WORK / "before/preprint_v1_0/EXTERNAL_BINDING.json"), "Live binding changed unexpectedly")
    (DELIVERY / "EXTERNAL_BINDING.json").unlink()
    (WORK / "tmp").mkdir(exist_ok=True)
    target = WORK / "tmp/rebuilt.zip"
    argv = [sys.executable, "-I", "-B", str(KIT / "build_archive.py"), "--output", str(target)]
    result = subprocess.run(argv, capture_output=True, text=True, timeout=120)
    dump(WORK / "ARCHIVE_BUILD.json", {"argv": argv, "returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
    require(result.returncode == 0, "New archive build failed: " + result.stderr)
    os.replace(target, DELIVERY / "verification_kit.zip")
    binding["as_of_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    binding["manifest_sha256"] = sha(KIT / "MANIFEST.json")
    binding["metadata_sha256"] = sha(KIT / "metadata.json")
    binding["deposit_manifest_sha256"] = sha(DELIVERY / "deposit_metadata.json")
    binding["archive"].update(bytes=(DELIVERY / "verification_kit.zip").stat().st_size, sha256=sha(DELIVERY / "verification_kit.zip"))
    for r in binding["external_files"]:
        p = DELIVERY / r["filename"]
        r.update(bytes=p.stat().st_size, sha256=sha(p))
    dump(DELIVERY / "EXTERNAL_BINDING.json", binding)
    dump(WORK / "NEW_COPY_ROWS.json", {"files": copies})
    print(json.dumps({"native_notes": NOTES, "archive": row(DELIVERY / "verification_kit.zip", DELIVERY),
                      "members": len(names), "new_copies": len(copies), "stage_copies_total": len(stages["files"]),
                      "history_rows_total": len(history["references"]),
                      "appended_history_rows": len(appended), "appended_dispositions": dict(collections.Counter(r["disposition"] for r in appended)),
                      "previous42_outputs_unchanged": True, "paper_unchanged": True, "publication_ready": False}))


if __name__ == "__main__":
    main()
