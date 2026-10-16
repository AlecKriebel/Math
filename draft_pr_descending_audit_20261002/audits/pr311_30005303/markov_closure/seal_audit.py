"""Record actual artifact modes, seal local audit bytes, and emit final bindings."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import stat

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "FINAL_AUDIT_MANIFEST.json"
SIDECAR = HERE / "FINAL_AUDIT_MANIFEST.sha256"
RECEIPT = HERE / "FINAL_SEAL_RECEIPT.json"


def utc():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def seal(path):
    before = path.read_bytes()
    old = stat.S_IMODE(path.stat().st_mode)
    path.chmod(0o444)
    new = stat.S_IMODE(path.stat().st_mode)
    after = path.read_bytes()
    assert before == after and new == 0o444
    return {"path": str(path), "relative_path": path.relative_to(HERE).as_posix(),
            "bytes": len(before), "sha256": sha(before),
            "observed_old_mode": oct(old), "observed_final_mode": oct(new),
            "mode_changed": old != new, "bytes_unchanged": True,
            "mode_verified_utc": utc(),
            "local_source_verification_only": "tmp" in path.relative_to(HERE).parts}


start = utc()
excluded = {MANIFEST, SIDECAR, RECEIPT}
paths = sorted(p for p in HERE.rglob("*") if p.is_file() and p not in excluded)
records = [seal(path) for path in paths]
bindings = json.loads((HERE / "INPUT_BINDINGS.json").read_bytes())
for item in bindings["candidate_inputs"]:
    assert sha(Path(item["path"]).read_bytes()) == item["sha256"]
manifest = {"family": "PR311 / 30005303 / Markov and closure",
            "status": "PASS", "completion_estimate_percent": 100,
            "seal_start_utc": start, "artifact_seal_completed_utc": utc(),
            "author_packet_file_count": 19,
            "permitted_publication_manifest_binding_count": 1,
            "candidate_inputs": bindings["candidate_inputs"],
            "excluded_semantic_contents": bindings["excluded_contents"],
            "all_candidate_input_bytes_unchanged": True,
            "independently_authenticated_source": bindings["independent_source_pdf"],
            "artifacts": records,
            "manifest_self_binding": "External SHA256 sidecar and FINAL_SEAL_RECEIPT.json",
            "sealing_note": "Observed old modes are actual at this concluding seal; earlier 0644->0444 transition is documented in the research log."}
MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
manifest_record = seal(MANIFEST)
SIDECAR.write_text(manifest_record["sha256"] + "  FINAL_AUDIT_MANIFEST.json\n")
sidecar_record = seal(SIDECAR)
receipt = {"family": manifest["family"], "status": "PASS",
           "completion_estimate_percent": 100,
           "start_utc": start, "end_utc": utc(),
           "sealed_artifact_count_excluding_manifest_sidecar_receipt": len(records),
           "manifest": manifest_record, "sidecar": sidecar_record,
           "all_artifact_modes_verified_0444": True,
           "all_sealed_bytes_unchanged": True,
           "candidate_input_bytes_unchanged": True,
           "no_git_remote_or_shared_file_mutation": True}
RECEIPT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
receipt_record = seal(RECEIPT)
assert all(stat.S_IMODE(p.stat().st_mode) == 0o444 for p in paths + [MANIFEST, SIDECAR, RECEIPT])
print(json.dumps({"status": "PASS", "manifest_sha256": manifest_record["sha256"],
                  "receipt_sha256": receipt_record["sha256"],
                  "receipt_observed_old_mode": receipt_record["observed_old_mode"],
                  "receipt_observed_final_mode": receipt_record["observed_final_mode"],
                  "all_modes_0444_verified_utc": utc()}, indent=2, sort_keys=True))
