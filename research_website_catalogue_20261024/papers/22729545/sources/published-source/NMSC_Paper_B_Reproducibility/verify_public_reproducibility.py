#!/usr/bin/env python3
"""Verify an exact public inventory and replay mathematical checks in a temporary copy."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile

MANIFEST = "REPRODUCIBILITY_MANIFEST.json"

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def safe(name):
    p = PurePosixPath(name)
    return bool(name) and not p.is_absolute() and ".." not in p.parts and "\\" not in name and "\0" not in name and p.as_posix() == name

def inventory(root):
    require(not root.is_symlink(), "Root must not be a symlink")
    files = {}
    for current, dirs, names in os.walk(root, followlinks=False):
        for name in dirs:
            require(not (Path(current) / name).is_symlink(), "Symlink directory is unsupported")
        for name in names:
            path = Path(current) / name
            require(path.is_file() and not path.is_symlink(), "Only ordinary files are supported")
            relative = path.relative_to(root).as_posix()
            require(safe(relative), "Unsafe relative path")
            files[relative] = path.read_bytes()
    require(MANIFEST in files and "CHECKSUMS.sha256" in files, "Missing public integrity files")
    manifest = json.loads(files[MANIFEST])
    require(manifest.get("schema") == "nmsc-public-reproducibility-v1", "Unknown manifest schema")
    require(set(files) == set(manifest["files"]) | {MANIFEST, "CHECKSUMS.sha256"}, "Public inventory mismatch")
    for name, record in manifest["files"].items():
        require(safe(name) and record["sha256"] == digest(files[name]) and record["bytes"] == len(files[name]), "Hash/size mismatch: " + name)
    checksums = {}
    for line in files["CHECKSUMS.sha256"].decode().splitlines():
        value, name = line.split("  ", 1)
        require(name not in checksums and safe(name), "Invalid checksum index")
        checksums[name] = value
    require(set(checksums) == set(files) - {"CHECKSUMS.sha256"}, "Incomplete checksum index")
    require(all(digest(files[name]) == value for name, value in checksums.items()), "Checksum mismatch")
    return manifest

def environment():
    env = dict(os.environ)
    for key in ("PYTHONOPTIMIZE", "PYTHONPATH", "PYTHONHOME"):
        env.pop(key, None)
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0")
    return env

def read_json(path):
    content = path.read_text()
    return [json.loads(line) for line in content.splitlines() if line.strip()] if path.suffix == ".jsonl" else json.loads(content)

def run_job(root, job, python, timeout):
    expected = {name: read_json(root / name) for name in job.get("compare_json", [])}
    started = time.monotonic()
    cmd = [python, "-B", job["script"], *job.get("args", [])]
    proc = subprocess.run(cmd, cwd=root / job.get("cwd", "."), env=environment(), capture_output=True, text=True, timeout=timeout)
    require(proc.returncode == 0, job["name"] + ": " + (proc.stdout + proc.stderr)[-3000:])
    for marker in job.get("stdout_contains", []):
        require(marker in proc.stdout, job["name"] + ": missing success marker " + marker)
    if "stdout_json" in job:
        require(json.loads(proc.stdout) == json.loads((root / job["stdout_json"]).read_text()), job["name"] + ": exact stdout changed")
    for name, original in expected.items():
        require(read_json(root / name) == original, job["name"] + ": recomputed evidence differs: " + name)
    return {"name": job["name"], "status": "PASS", "seconds": round(time.monotonic() - started, 3), "scope": job["scope"]}

def rebuild_source(scratch, manifest, submitted):
    require(submitted is not None, "--build-source requires --submission-dir containing the downloaded main, supplement and source files")
    for name, expected in manifest["submission_files"].items():
        require((submitted / name).is_file() and digest((submitted / name).read_bytes()) == expected, "Companion submission file mismatch: " + name)
    source = submitted / ("NMSC_Paper_" + manifest["paper"] + "_Source.zip")
    build = scratch / "source-rebuild"
    build.mkdir()
    with zipfile.ZipFile(source) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)) and set(names) == {"build_submission.sh", "manuscript/main.tex", "manuscript/references.bib", "supplement/technical_supplement.tex", "navigation/technical_summary.tex", "navigation/theorem_graph.tex"}, "Unexpected source archive inventory")
        for name in names:
            require(safe(name), "Unsafe source path")
            target = build / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(name))
    env = environment()
    env["SOURCE_DATE_EPOCH"] = str(manifest["source_date_epoch"])
    proc = subprocess.run(["bash", "build_submission.sh"], cwd=build, env=env, capture_output=True, text=True, timeout=180)
    require(proc.returncode == 0, "Source rebuild failed: " + (proc.stdout + proc.stderr)[-3000:])
    for relative, label in (("manuscript/main.pdf", "Main"), ("supplement/technical_supplement.pdf", "Supplement")):
        name = "NMSC_Paper_" + manifest["paper"] + "_" + label + ".pdf"
        require((build / relative).read_bytes() == (submitted / name).read_bytes(), "Source PDF differs: " + name)
    return {"name": "source rebuild", "status": "PASS", "scope": "Main and supplement PDFs byte-identical to the supplied six-file source archive rebuild"}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--inventory-only", action="store_true")
    parser.add_argument("--full", action="store_true", help="Also run the canonical symbolic regression/negative/mutation suites")
    parser.add_argument("--tier0", action="store_true", help="Paper B only: freshly run all twelve bounded handoff jobs, without resume")
    parser.add_argument("--python", default=sys.executable, help="Standard-library interpreter for bounded checks")
    parser.add_argument("--exact-python", help="Interpreter with the paper's pinned symbolic dependencies")
    parser.add_argument("--tier0-python", help="Python >=3.11,<3.14 with SymPy 1.14.0 and NetworkX 3.5")
    parser.add_argument("--build-source", action="store_true")
    parser.add_argument("--submission-dir", type=Path)
    parser.add_argument("--report", type=Path, help="JSON report path outside the verified input tree")
    parser.add_argument("--timeout", type=int, default=900)
    args = parser.parse_args()
    require(__debug__, "Invoke without -O or -OO")
    root = args.root.resolve()
    require(args.timeout > 0, "Timeout must be positive")
    if args.report:
        require(not args.report.resolve().is_relative_to(root), "Write report outside the delivered tree")
    manifest = inventory(root)
    require(not args.tier0 or manifest["paper"] == "B", "Tier 0 is only supplied for B")
    records = []
    if not args.inventory_only:
        with tempfile.TemporaryDirectory(prefix="nmsc-public-replay-") as temporary:
            scratch = Path(temporary)
            copied = scratch / "reproducibility"
            shutil.copytree(root, copied)
            for job in manifest["quick_jobs"]:
                records.append(run_job(copied, job, args.python, args.timeout))
                print("PASS:", job["name"], flush=True)
            if args.full:
                for job in manifest["full_jobs"]:
                    records.append(run_job(copied, job, args.exact_python or args.python, args.timeout))
                    print("PASS:", job["name"], flush=True)
            if args.tier0:
                records.append(run_job(copied, manifest["tier0_job"], args.tier0_python or args.python, args.timeout))
                print("PASS: twelve fresh Tier-0 jobs", flush=True)
            if args.build_source:
                records.append(rebuild_source(scratch, manifest, args.submission_dir.resolve() if args.submission_dir else None))
                print("PASS: source rebuild", flush=True)
    report = {"schema": "nmsc-public-replay-v1", "paper": manifest["paper"], "status": "PASS", "inventory_files": len(manifest["files"]), "manifest_sha256": digest((root / MANIFEST).read_bytes()), "checks": records, "scope": "Exact inventory and selected bounded computations; no universal theorem certification"}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("PUBLIC_REPRODUCIBILITY_PASS paper=" + manifest["paper"] + " groups=" + str(len(records)))

if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired, zipfile.BadZipFile) as error:
        print("PUBLIC_REPRODUCIBILITY_FAILED:", error, file=sys.stderr)
        raise SystemExit(1)
