#!/usr/bin/env python3
"""One-time terminal custody seal; candidate files are never written."""
import datetime
import hashlib
import json
from pathlib import Path

WORK = Path(__file__).resolve().parent
AUDIT = WORK.parents[1]


def require(test, message):
    if not test:
        raise RuntimeError(message)


def row(path, root):
    return {"path": path.relative_to(root).as_posix(), "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    require(not (WORK / "TERMINAL_SEAL.json").exists(), "Refuse automatic terminal reseal")
    verification = json.loads((WORK / "FINAL_VERIFICATION.json").read_text())
    require(verification["status"] == "PASS_DATED_METADATA_SUCCESSOR_PENDING_NEW_WHOLE02"
            and not verification["publication_ready"] and not verification["published"], "Gate status differs")
    current = json.loads((WORK / "CURRENT_INPUT_PINS.json").read_text())["files"]
    for record in current:
        require(row(AUDIT / record["path"], AUDIT) == record, "Current candidate changed before seal")
    names = []
    for p in sorted(WORK.rglob("*")):
        require(not p.is_symlink(), "Repair workspace symlink")
        if p.is_file() and not p.is_relative_to(WORK / "tmp") and p.name not in {"OUTPUT_PINS.json", "TERMINAL_SEAL.json"}:
            names.append(p)
    require(not any((WORK / "tmp").rglob("*")), "Disposable scratch not empty")
    pins = {"scope": "Complete bounded repair authored programs, exact before copies, final and intermediate receipts, report, diff and terminal custody; excludes only this inventory and its separate seal.",
            "files": [row(p, WORK) for p in names]}
    (WORK / "OUTPUT_PINS.json").write_text(json.dumps(pins, indent=2) + "\n")
    selected = ["preprint_v1_0/metadata.json", "preprint_v1_0/deposit_metadata.json",
                "preprint_v1_0/research_metadata.json", "preprint_v1_0/CURRENT_STATUS_REPAIR01.json",
                "preprint_v1_0/EXTERNAL_BINDING.json", "preprint_v1_0/preprint.tex",
                "preprint_v1_0/preprint.pdf", "preprint_v1_0/verification_kit.zip",
                "preprint_v1_0/verification_kit/ALLOWLIST.json", "preprint_v1_0/verification_kit/MANIFEST.json",
                "preprint_v1_0/verification_kit/METADATA_DATE02_ADMIN_STAGE.json",
                "preprint_v1_0/verification_kit/REPAIR01_STAGE_COPIES.json",
                "preprint_v1_0/verification_kit/REPAIR01_HISTORY_RESOLUTION.json"]
    seal = {"as_of_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "status": verification["status"], "pr": 1080,
            "head": "64b252b199f2692eef2545656190c14bcaf63889",
            "output_count": len(names), "output_inventory": row(WORK / "OUTPUT_PINS.json", WORK),
            "selected_current_candidate": [row(AUDIT / n, AUDIT) for n in selected],
            "publication_ready": False, "published": False, "whole_reviews_completed": 1,
            "minimum_whole_reviews": 2, "fresh_complete_whole02_required": True,
            "services_held_at": 1032, "substage_completion_percent": 100,
            "math_research_completion_best_guess_percent": 60,
            "scope": "Custody only. No new mathematical/priority/visual/full-package review or human certification is implied."}
    (WORK / "TERMINAL_SEAL.json").write_text(json.dumps(seal, indent=2) + "\n")
    for record in pins["files"]:
        require(row(WORK / record["path"], WORK) == record, "Output changed while sealing")
    require(row(WORK / "OUTPUT_PINS.json", WORK) == seal["output_inventory"], "Output inventory changed")
    print(json.dumps({"status": seal["status"], "output_count": len(names),
                      "output_pins_sha256": row(WORK / "OUTPUT_PINS.json", WORK)["sha256"],
                      "terminal_seal_sha256": row(WORK / "TERMINAL_SEAL.json", WORK)["sha256"],
                      "publication_ready": False, "new_whole02_required": True}, indent=2))


if __name__ == "__main__":
    main()
