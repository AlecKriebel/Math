#!/usr/bin/env python3
"""Authenticate this finite archive, then isolate and run reviewed checkers.
Only the named checkers run; archived provenance drivers are never executed.
Finite checks do not establish the analytic theorem or mathematical priority.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
SUITE = [
    ("submission/check_turn2.py", 50324, "historical"),
    ("submission/check_turn3.py", 17148, "historical"),
    ("submission/independent_review/independent_check.py", 31888, "historical"),
    ("audits/math_replica_family_01/independent_exact_checks.py", 37140, "replica"),
    ("audits/math_replica_family_01/excluded_boundary_checks.py", 197, "boundary"),
    ("audits/math_martingale_family_01/independent_exact_controls.py", 197758, "martingale"),
    ("audits/math_coalescence_family_01/independent_exact_checks.py", 22225, "coalescence"),
    ("audits/reproduction_history_family_01/independent_finite_check.py", 19340, "reproduction"),
]
OPTIONAL = ("submission/check_turn1.py", 486, "sympy")
def need(condition, message):
    if not condition:
        raise ValueError(message)
def sha(raw):
    return hashlib.sha256(raw).hexdigest()
def canonical(relative):
    need(isinstance(relative, str) and relative, "Empty or non-string archive path")
    p = PurePosixPath(relative)
    need(not p.is_absolute() and ".." not in p.parts and p.as_posix() == relative
         and "\\" not in relative, "Noncanonical archive path: " + relative)
    return p
def authenticate():
    mpath = ROOT / "MANIFEST.json"
    need(not mpath.is_symlink() and mpath.is_file(), "Manifest must be a regular file")
    manifest_raw = mpath.read_bytes()
    manifest = json.loads(manifest_raw)
    need(manifest.get("schema") == "pr239-portable-finite-verification-manifest-v1",
         "Unexpected manifest schema")
    entries = manifest["files"]
    need(isinstance(entries, list) and len(entries) == manifest["file_count"], "Bad finite file count")
    cache = {}
    native = []
    for e in entries:
        relative = e["path"]
        canonical(relative)
        need(relative != "MANIFEST.json" and relative not in cache, "Duplicate/self manifest entry")
        p = ROOT / relative
        for part in [p] + list(p.parents)[:len(PurePosixPath(relative).parts)-1]:
            need(not part.is_symlink(), "Symlink in archive path: " + relative)
        need(p.is_file() and stat.S_ISREG(p.stat().st_mode), "Missing regular file: " + relative)
        raw = p.read_bytes()
        need(type(e["bytes"]) is int and len(raw) == e["bytes"] and sha(raw) == e["sha256"],
             "Length/SHA256 mismatch: " + relative)
        if "native_blob" in e:
            blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            need(blob == e["native_blob"], "Historical native blob mismatch: " + relative)
            native.append(relative)
        cache[relative] = raw
    need(len(native) == manifest["native_input_count"] == 32
         and set(native) == {p for p in cache if p.startswith("submission/")},
         "Historical input native pins must cover exactly all32 submission files")
    found = set()
    for directory, dirs, files in os.walk(ROOT, followlinks=False):
        for name in dirs + files:
            p = Path(directory) / name
            mode = p.lstat().st_mode
            need(not stat.S_ISLNK(mode) and (stat.S_ISREG(mode) or stat.S_ISDIR(mode)),
                 "Nonregular archive member")
            if stat.S_ISREG(mode):
                found.add(p.relative_to(ROOT).as_posix())
    need(found == set(cache) | {"MANIFEST.json"}, "Unlisted or missing archive member")
    need(sum(len(raw) for raw in cache.values()) == manifest["total_payload_bytes"],
         "Total finite byte count mismatch")
    return cache, {"files": len(cache), "payload_bytes": manifest["total_payload_bytes"],
                   "native_historical_inputs": 32, "manifest_sha256": sha(manifest_raw)}
def count_families(value, key, family_key, expected):
    need(type(value.get(key)) is int and value[key] == expected, "Incorrect assertion count")
    families = value.get(family_key)
    need(isinstance(families, dict) and families
         and all(type(n) is int and n > 0 for n in families.values())
         and sum(families.values()) == expected, "Incorrect family count sum")
def run_one(item, cache):
    relative, expected, kind = item
    code = cache[relative]
    with tempfile.TemporaryDirectory(prefix="pr239-check-") as directory:
        work = Path(directory).resolve()
        script = work / PurePosixPath(relative).name
        script.write_bytes(code)
        script.chmod(0o444)
        flags = ["-E", "-B", "-P"] if kind == "sympy" else ["-E", "-S", "-B", "-P"]
        proc = subprocess.run([sys.executable] + flags + [str(script)], cwd=work,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=600)
        need(proc.returncode == 0 and not proc.stderr,
             relative + " failed: " + proc.stderr.decode(errors="replace")[:600])
        need(len(proc.stdout) <= 1000000, "Unexpectedly large checker output")
        value = json.loads(proc.stdout)
        expected_written = set()
        if kind in ("historical", "sympy", "martingale", "reproduction"):
            need(value.get("status") == "PASS", "Checker did not return PASS")
            count_families(value, "exact_assertions", "families", expected)
            if kind == "sympy":
                need(value.get("sympy_version") == "1.14.0", "SymPy version mismatch")
            if kind == "martingale":
                need(value.get("schema") == "independent-pr239-martingale-exact-finite-controls-v1"
                     and value.get("submission_code_imported") is False
                     and value.get("random_simulations") is False
                     and value.get("finite_controls_replace_analytic_proof") is False,
                     "Unexpected martingale result properties")
            if kind == "reproduction":
                need(value.get("parameter_laws") == 6 and value.get("path_geometry_cases") == 360,
                     "Unexpected reproduction parameter coverage")
        elif kind == "replica":
            expected_written = {"EXACT_RESULTS.json"}
            detail = json.loads((work / "EXACT_RESULTS.json").read_bytes())
            need(value.get("status") == detail.get("status") == "PASS"
                 and value.get("check_count") == expected and value.get("families") == 24
                 and value.get("laws") == 6 and value.get("result") == str(work / "EXACT_RESULTS.json")
                 and detail.get("schema") == "independent-pr239-replica-exact-controls-v1"
                 and len(detail.get("laws", [])) == 6, "Unexpected replica result properties")
            count_families(detail, "check_count", "checks", expected)
        elif kind == "boundary":
            expected_written = {"BOUNDARY_RESULTS.json"}
            detail = json.loads((work / "BOUNDARY_RESULTS.json").read_bytes())
            need(value.get("status") == detail.get("status") == "PASS"
                 and type(value.get("checks")) is int and value["checks"] == expected
                 and detail.get("checks") == expected
                 and detail.get("schema") == "independent-pr239-excluded-boundary-controls-v1"
                 and detail.get("opposite_parity_disjoint_through_64") is True
                 and detail.get("excluded_arrow_delta_zero_g_through_128") == "1 exactly",
                 "Unexpected excluded-boundary result properties")
        elif kind == "coalescence":
            need(value.get("schema") == "pr239-independent-exact-coalescence-strip-checks-v1"
                 and value.get("all_passed") is True and len(value.get("coalescence_samples", [])) == 24
                 and value.get("source") == {"bytes": len(code), "sha256": sha(code)},
                 "Unexpected coalescence result properties")
            count_families(value, "assertions", "counts", expected)
        else:
            raise ValueError("Unknown reviewed checker")
        need({p.name for p in work.iterdir()} == {script.name} | expected_written,
             "Unexpected isolated checker output files")
        return {"script": relative, "source_sha256": sha(code), "exact_assertions": expected,
                "status": "PASS", "exit_code": 0, "stderr_bytes": 0,
                "stdout_bytes": len(proc.stdout), "stdout_sha256": sha(proc.stdout),
                "isolated_temporary_source_copy": True,
                "output_validation": "Actual JSON schema/count/properties; no time/path-dependent byte comparison"}
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--with-sympy", action="store_true",
                        help="Also run the486-assertion historical checker; requires installed SymPy1.14.0")
    args = parser.parse_args()
    need(sys.version_info >= (3, 11), "Python3.11 or newer is required")
    cache, authentication = authenticate()  # Before any imported checker or optional dependency.
    selected = SUITE + ([OPTIONAL] if args.with_sympy else [])
    if args.with_sympy:
        probe = subprocess.run([sys.executable, "-E", "-B", "-P", "-c",
                                "import sympy; print(sympy.__version__)"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
        need(probe.returncode == 0 and not probe.stderr and probe.stdout.strip() == b"1.14.0",
             "Optional check requires preinstalled SymPy==1.14.0; see requirements-optional.txt")
    results = [run_one(item, cache) for item in selected]
    total = sum(r["exact_assertions"] for r in results)
    need(total == (376506 if args.with_sympy else 376020), "Unexpected suite total")
    print(json.dumps({"schema": "pr239-portable-finite-verification-result-v1",
                      "UTC": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                      "status": "PASS", "python": sys.version, "authentication": authentication,
                      "stdlib_scripts": 8, "stdlib_assertions": 376020,
                      "optional_sympy_scripts": int(args.with_sympy),
                      "optional_sympy_assertions": 486 if args.with_sympy else 0,
                      "exact_assertions": total, "results": results,
                      "scope": "Finite identities, inequalities and excluded-boundary controls only. These totals count parameter instances, not independent theorems. The analytic manuscript establishes any infinite-time claim. No novelty, historical reviewer independence, historical source-access or external publication certification follows."},
                     indent=2, sort_keys=True))
if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
        print("Verification failed: " + str(exc), file=sys.stderr)
        raise SystemExit(1)

