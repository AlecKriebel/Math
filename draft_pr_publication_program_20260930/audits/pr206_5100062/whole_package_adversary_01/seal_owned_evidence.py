"""Seal authored audit evidence only; never touches the reviewed package."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

OWN = Path(__file__).resolve().parent
EXCLUDE = {
    "final_readbacks/results.json": "Partial preserved raw API-object readback; narrow SAFE_RESULTS.json is included instead.",
    "SAFE_MANIFEST.json": "Self-excluded manifest.",
    "AUDIT_SEAL.json": "Self-excluded seal.",
}


def digest(path):
    data = path.read_bytes()
    return {"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}


def main():
    if (OWN / "SAFE_MANIFEST.json").exists() or (OWN / "AUDIT_SEAL.json").exists():
        raise RuntimeError("Audit already sealed")
    records = {}
    excluded = {}
    for f in sorted(OWN.rglob("*")):
        if f.is_symlink():
            raise RuntimeError("Symlink fixture remains: "+str(f))
        if not f.is_file():
            continue
        name = str(f.relative_to(OWN))
        if name in EXCLUDE:
            excluded[name] = {"reason":EXCLUDE[name],**digest(f)}
            continue
        if "__pycache__" in f.parts or f.suffix == ".pyc" or ".git" in f.parts or "private_acquisition_cache" in f.parts:
            raise RuntimeError("Unsafe or mutable member: "+name)
        records[name] = digest(f)
    manifest = {"schema":"pr206-whole-package-adversary-01-safe-manifest-v1","utc":datetime.now(timezone.utc).isoformat(),"scope":"Authored research notes, adversarial code, raw own execution logs and own-paper QA/rebuild artifacts only.","files":records,"file_count":len(records),"total_bytes":sum(x["bytes"] for x in records.values()),"exclusions":excluded,"excluded_by_policy":["full third-party primary materials","dependencies","credentials","temporary fixture symlinks","mutable caches","raw private API response objects"],"no_symlinks_or_bytecode":True}
    (OWN / "SAFE_MANIFEST.json").write_text(json.dumps(manifest,indent=2)+"\n")
    seal = {"schema":"pr206-whole-package-adversary-01-audit-seal-v1","frozen_utc":datetime.now(timezone.utc).isoformat(),"outcome":"NO_MANDATORY_DEFECT_IDENTIFIED_WITHIN_STATED_SCOPE","audit_completion_best_guess_percent":100,"report":{"path":"WHOLE_PACKAGE_REPORT.md",**digest(OWN / "WHOLE_PACKAGE_REPORT.md")},"safe_manifest":{"path":"SAFE_MANIFEST.json",**digest(OWN / "SAFE_MANIFEST.json")},"plan":{"path":"FROZEN_ADVERSARIAL_PLAN.md",**digest(OWN / "FROZEN_ADVERSARIAL_PLAN.md")},"primary_assessment":{"path":"PRIMARY_SCIENTIFIC_ASSESSMENT.md",**digest(OWN / "PRIMARY_SCIENTIFIC_ASSESSMENT.md")},"reviewed_package_seal_sha256":"85d422ae10dbcf6b3f5b2ec21798df48ecaaef98d9fc3e3f6991071597e54531","reviewed_package_manifest_sha256":"7dc8de3a050d087f2dc15a151d7841c8d2e97b425f80afad76d34da2095b8cae","reviewed_package_bytes_and_zip_member_map_unchanged":True,"root_permission_only_lock_disclosed":True,"root_favorable_assessment_read":False,"canonical_acceptance_created":False,"publication_decision_created":False,"conventional_human_review":False,"formal_proof_certificate":False,"another_new_whole_package_review_required":True,"limitations":["strict proper confocal elliptic regime only","four convex finite controls; higher stars analytic","bounded primary-source/priority comparison and access gaps","AI adversarial review; unrefereed","auditor corrections disclosed in INITIAL_ATTEMPT_LOG.md"]}
    (OWN / "AUDIT_SEAL.json").write_text(json.dumps(seal,indent=2)+"\n")
    for name, pin in records.items():
        if digest(OWN / name) != pin:
            raise RuntimeError("File changed while sealing: "+name)
    print(json.dumps({"report":seal["report"],"manifest":seal["safe_manifest"],"seal":{"path":"AUDIT_SEAL.json",**digest(OWN / "AUDIT_SEAL.json")},"safe_file_count":len(records),"safe_total_bytes":manifest["total_bytes"],"outcome":seal["outcome"]},indent=2))


if __name__ == "__main__":
    main()
