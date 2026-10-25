"""Seal this worker's own complete packet, after a final original-byte recheck.

Only writes or chmods files inside this adversarial namespace. Foreign full-text
cache is excluded. This file and checks.py were inspected before execution.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import runpy

HERE = Path(__file__).resolve().parent


def h(blob):
    return sha256(blob).hexdigest()


def new_json(path, value):
    if path.exists():
        raise RuntimeError(f"Refusing overwrite: {path}")
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    required = ["EARLY_LEDGER.md", "EARLY_SEAL.json", "RESEARCH_LOG.md",
                "ORIGINAL_BINDING_RECEIPT.json", "EXACT_CONTROLS.json",
                "PRIMARY_INTERFACES.json", "ATTACK_LEDGER.md", "REPORT.md",
                "verdict.json", "checks.py", "finalize.py"]
    assert all((HERE / name).is_file() for name in required)
    early = json.loads((HERE / "EARLY_SEAL.json").read_text())
    assert h((HERE / early["ledger"]).read_bytes()) == early["sha256"]
    assert h((HERE / "EARLY_SEAL.json").read_bytes()) == "7d2f1a1698c7146af31c3b857df8e0e3d6b2d1420751acf645ba125b4593d0a4"
    for path in HERE.glob("*.json"):
        json.loads(path.read_text())
    primaries = json.loads((HERE / "PRIMARY_INTERFACES.json").read_text())
    for primary in primaries["primary_objects"]:
        blob = Path(primary["local_pdf"]).read_bytes()
        assert len(blob) == primary["bytes"] and h(blob) == primary["sha256"]
        assert h((HERE / primary["own_ignored_text"]).read_bytes()) == primary["text_sha256"]
    independent_checks = runpy.run_path(str(HERE / "checks.py"))
    final_custody = independent_checks["custody"]()
    new_json(HERE / "FINAL_ORIGINAL_BINDING_RECEIPT.json", final_custody)
    files = []
    for path in sorted(HERE.iterdir()):
        if path.is_file() and path.name not in {"FINAL_MANIFEST.json", "FINAL_SEAL.json"}:
            blob = path.read_bytes()
            files.append({"path": path.name, "bytes": len(blob), "sha256": h(blob)})
            path.chmod(0o444)
    manifest = {
        "utc": datetime.now(timezone.utc).isoformat(),
        "status": "COMPLETE_IMMUTABLE_BOUNDED_ADVERSARIAL_PACKET",
        "record_id": 23074543, "row": 91,
        "bounded_review_completion_percent": 100,
        "source_ready_seal_sha256": early["source_ready_seal_sha256"],
        "whole_original_bindings_rechecked": 97,
        "original_zip_members_CRC_rechecked": 87,
        "foreign_full_text_cache_excluded": "replay-work/primary",
        "all_authored_evidence_read_only": True,
        "files": files,
    }
    new_json(HERE / "FINAL_MANIFEST.json", manifest)
    (HERE / "FINAL_MANIFEST.json").chmod(0o444)
    by_name = {entry["path"]: entry for entry in files}
    seal = {
        "utc": datetime.now(timezone.utc).isoformat(),
        "status": "COMPLETE_SEALED_NO_PROMOTION_AUTHORITY",
        "manifest": "FINAL_MANIFEST.json",
        "manifest_sha256": h((HERE / "FINAL_MANIFEST.json").read_bytes()),
        "report": "REPORT.md", "report_sha256": by_name["REPORT.md"]["sha256"],
        "verdict_sha256": by_name["verdict.json"]["sha256"],
        "early_seal_sha256": h((HERE / "EARLY_SEAL.json").read_bytes()),
        "all_97_original_bindings_and_87_members_unchanged": True,
        "public_promotion_authority": False,
        "overall_203_paper_goal": "ONGOING",
    }
    new_json(HERE / "FINAL_SEAL.json", seal)
    (HERE / "FINAL_SEAL.json").chmod(0o444)
    print(json.dumps({"manifest_sha256": seal["manifest_sha256"],
                      "seal_sha256": h((HERE / "FINAL_SEAL.json").read_bytes()),
                      "report_sha256": seal["report_sha256"],
                      "verdict_sha256": seal["verdict_sha256"]}, indent=2))
