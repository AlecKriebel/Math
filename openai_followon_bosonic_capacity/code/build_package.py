"""Build an explicit owned-file source/verification kit. Python standard library.

PDF compilation is a separate step. No third-party source or secrets included.
"""
from pathlib import Path
import hashlib, json, shutil, zipfile

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    "README.md", "LICENSES.md", "CURRENT_THEOREM.md", "DEPENDENCY_LEDGER.md",
    "APPROACH_TABLE.md", "zenodo-deposit.json", "manuscript/main.tex", "manuscript/upstream-citation.bib",
    "sources/SOURCE_MANIFEST.json", "code/verify_certificates.py",
    "code/certificate_results.json", "code/build_package.py",
    "notes/upstream_proof/REPORT.md", "notes/upstream_proof/new_operational_check.md",
    "notes/upstream_proof/check_interpolation.py",
    "notes/upstream_proof/check_interpolation_results.json",
    "notes/upstream_proof/upstream_current_history.json",
    "notes/formal_scope/REPORT.md", "notes/formal_scope/VACUUM_BRIDGE.md",
    "notes/formal_scope/source_manifest.json", "notes/formal_scope/build_status.json",
    "notes/formal_scope/statement_definition_comparison.json",
    "notes/formal_scope/create_harness.py",
    "notes/capacity_proof/CONDITIONAL_DERIVATION.md",
    "notes/capacity_proof/ACHIEVABILITY_AND_COST.md",
    "notes/capacity_proof/PRIVATE_SECURITY_DEFECT_AND_REPAIR.md",
    "notes/capacity_proof/SOURCE_HASHES.sha256",
    "notes/operational_adversary/REPORT.md",
    "notes/operational_adversary/ENERGY_ACHIEVABILITY.md",
    "notes/operational_adversary/SOURCE_HASHES.json",
    "notes/coding_repair/DIRECT_CODING.md", "notes/coding_repair/SOURCE_HASHES.json",
    "notes/alternate_priority/PRIORITY_AND_ROUTES.md",
    "notes/alternate_priority/SECURITY_CRITERION_PRIORITY.md",
    "notes/alternate_priority/DEGRADABLE_CONVERSE_REPAIR.md",
    "notes/alternate_priority/source_hashes.json",
    "notes/alternate_priority/release_provenance.json",
    "notes/alternate_priority/repair_identity_audit/REVIEW.md",
    "notes/alternate_priority/repair_identity_audit/symbolic_checks.py",
]

def main():
    dest = ROOT / "publication"
    dest.mkdir(exist_ok=True)
    shutil.copyfile(ROOT / "manuscript/main.pdf", dest / "paper.pdf")
    records = []
    archive = dest / "zenodo-upload-kit.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for name in sorted(FILES):
            raw = (ROOT / name).read_bytes()
            records.append({"path":name,"bytes":len(raw),
                            "sha256":hashlib.sha256(raw).hexdigest()})
            info = zipfile.ZipInfo(name, date_time=(2026,10,6,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, raw)
        info = zipfile.ZipInfo("SOURCE_INVENTORY.json", date_time=(2026,10,6,0,0,0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        z.writestr(info, json.dumps(records,indent=2)+"\n")
    uploads = []
    for name in ("paper.pdf", "zenodo-upload-kit.zip"):
        raw = (dest/name).read_bytes()
        uploads.append({"path":"publication/"+name,"bytes":len(raw),
                        "sha256":hashlib.sha256(raw).hexdigest(),
                        "md5":hashlib.md5(raw).hexdigest()})
    inventory = {"source_files":records,"uploads":uploads,
                 "manifest_sha256":hashlib.sha256((ROOT/"zenodo-deposit.json").read_bytes()).hexdigest()}
    (dest/"PACKAGE_INVENTORY.json").write_text(json.dumps(inventory,indent=2)+"\n")
    print(json.dumps({"source_files":len(records),"uploads":uploads},indent=2))

if __name__ == "__main__":
    main()
