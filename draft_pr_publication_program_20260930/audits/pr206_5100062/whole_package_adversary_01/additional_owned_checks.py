"""Reproducibility, all JSON fields, manifest/ZIP and guarded-API audit."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import zipfile

OWN = Path(__file__).resolve().parent
PACKAGE = OWN.parent / "publication_package_v1"
PY = "/opt/homebrew/opt/python@3.14/bin/python3.14"
FLAGS = ["-E", "-S", "-B", "-P"]


def main():
    out = OWN / "additional_runs"
    out.mkdir(exist_ok=False)
    attempts = []

    def run(label, argv, source=None):
        p = subprocess.run(argv, capture_output=True, text=True, timeout=60, cwd=OWN)
        record = {"label":label,"utc":datetime.now(timezone.utc).isoformat(),"argv":argv,"cwd":str(OWN),"exit":p.returncode,"stdout":p.stdout,"stderr":p.stderr}
        if source:
            record["source_sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
        (out / (label+".json")).write_text(json.dumps(record,indent=2)+"\n")
        attempts.append(record)
        if p.returncode:
            raise RuntimeError(label+" failed")
        return p

    for opt in (False,True):
        source = OWN / "deep_api_checks.py"
        run("api_optimized" if opt else "api_normal",[PY]+FLAGS+(["-O"] if opt else [])+[str(source)],source)
    negsource = PACKAGE / "verification/run_negative_controls.py"
    p = run("negative_harness",[PY]+FLAGS+[str(negsource)],negsource)
    expected = (PACKAGE / "verification/negative_control_results.json").read_text()
    if p.stdout != expected:
        raise RuntimeError("Negative replay differs from distributed raw receipt")
    for mode in ("normal","optimized"):
        included = (PACKAGE / ("verification/results_"+mode+".json")).read_text()
        replay = json.loads((OWN / "owned_runs_v2" / (mode+".json")).read_text())["stdout"]
        if included != replay:
            raise RuntimeError("Positive replay differs from distributed raw receipt: "+mode)
        data = json.loads(included)
        if data["counts"] != data["expected_counts"] or sum(data["counts"].values()) != 245 or len(data["counts"]) != 27:
            raise RuntimeError("Ledger claims differ")
        if [c["name"] for c in data["controls"]] != ["H","V","diamond","rectangle"] or any(c["winding"] != 1 for c in data["controls"]):
            raise RuntimeError("Control identities differ")
    seal = json.loads((PACKAGE / "PACKAGE_SEAL.json").read_text())
    manifest = json.loads((PACKAGE / "PUBLIC_MATERIALS_MANIFEST.json").read_text())
    actual = {}
    for f in sorted(PACKAGE.rglob("*")):
        if f.is_symlink():
            raise RuntimeError("symlink in package")
        if f.is_file():
            b = f.read_bytes()
            actual[str(f.relative_to(PACKAGE))] = {"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
    if {n:v for n,v in actual.items() if n != "PACKAGE_SEAL.json"} != seal["files"]:
        raise RuntimeError("seal does not bind exact remaining members")
    if sum(v["bytes"] for n,v in actual.items() if n != "PACKAGE_SEAL.json") != seal["total_bytes_excluding_this_seal"]:
        raise RuntimeError("total size differs")
    with zipfile.ZipFile(PACKAGE / "verification-package.zip") as z:
        names = z.namelist()
        if len(names) != len(set(names)) or len(names) != 14:
            raise RuntimeError("ZIP duplicate or count")
        intended = set(manifest["archive_files_excluding_this_manifest"]) | {"PUBLIC_MATERIALS_MANIFEST.json"}
        if set(names) != intended:
            raise RuntimeError("ZIP membership mismatch")
        for name in names:
            if z.read(name) != (PACKAGE / name).read_bytes():
                raise RuntimeError("ZIP byte mismatch "+name)
            if ((z.getinfo(name).external_attr >> 16) & 0o170000) != 0o100000:
                raise RuntimeError("nonregular ZIP member")
        for name, record in manifest["archive_files_excluding_this_manifest"].items():
            if actual[name] != record:
                raise RuntimeError("manifest bytes differ")
    negative = json.loads(expected)
    if negative["attempt_count"] != 26 or len(negative["attempts"]) != 26:
        raise RuntimeError("negative count mismatch")
    for item in negative["attempts"]:
        child = json.loads(item["stdout"])
        if item["actual_exit"] != 1 or item["expected_exit"] != 1 or item["stderr"] or child["status"] != "FAIL":
            raise RuntimeError("negative result contradiction")
        if child["runtime"]["source_sha256"] != seal["current_portable_source_sha256"]:
            raise RuntimeError("negative source binding mismatch")
    summary = {"status":"PASS","positive_receipt_replays":"byte-identical","negative_harness_replay":"byte-identical","zip_members":len(names),"package_files":len(actual),"seal_manifest_bytes":"all match","api_modes":["normal","optimized"],"attempt_logs":len(attempts)}
    (out / "SUMMARY.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,sort_keys=True))


if __name__ == "__main__":
    main()
