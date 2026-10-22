#!/usr/bin/env python3
"""Run meaningful custody/scope rejection controls on disposable owned copies."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def seal(root):
    rows = []
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.name != "MANIFEST.json":
            rows.append({"path": p.relative_to(root).as_posix(),
                         "bytes": p.stat().st_size, "sha256": sha(p)})
    (root / "MANIFEST.json").write_text(json.dumps({
        "schema": "pr789-priority-structural-manifest-v1", "files": rows}, indent=2) + "\n")
    return sha(root / "MANIFEST.json")


def alter_json(path, function):
    data = json.loads(path.read_text())
    function(data)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for name in ["packet-root", "input-root", "primary-root", "scratch", "out",
                 "manifest-sha256", "checker-sha256"]:
        ap.add_argument("--" + name, required=True)
    a = ap.parse_args()
    packet = Path(a.packet_root).absolute()
    intake = Path(a.input_root).absolute()
    primary = Path(a.primary_root).absolute()
    scratch = Path(a.scratch).absolute()
    scratch.mkdir(parents=True, exist_ok=True)
    cases = []

    def invoke(label, p, i=intake, b=None, mf=None, cp=None, checker=None,
               optimized=False, expected=0):
        cmd = [sys.executable, "-I", "-B"]
        if optimized:
            cmd.append("-O")
        cmd += [str(checker or p / "verify_priority.py"), "--packet-root", str(p),
                "--input-root", str(i), "--manifest-sha256", mf or a.manifest_sha256,
                "--checker-sha256", cp or a.checker_sha256]
        if b is not None:
            cmd += ["--primary-root", str(b)]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        passed = r.returncode == expected
        if expected == 0:
            try:
                passed = passed and json.loads(r.stdout)["result"] == "PASS"
            except (ValueError, KeyError):
                passed = False
        else:
            passed = passed and r.stderr.startswith("REJECT:")
        cases.append({"case": label, "expected_exit": expected,
                      "actual_exit": r.returncode, "pass": passed})

    invoke("core_normal", packet)
    invoke("core_optimized", packet, optimized=True)
    invoke("primary_normal", packet, b=primary)
    invoke("primary_optimized", packet, b=primary, optimized=True)
    invoke("wrong_manifest_pin", packet, mf="0" * 64, expected=2)
    invoke("wrong_checker_pin", packet, cp="0" * 64, expected=2)

    def copied(label, mutate, reseal=False, extra=None):
        with tempfile.TemporaryDirectory(prefix="pr789_" + label + "_", dir=scratch) as td:
            r = Path(td)
            p = r / "packet with spaces"
            shutil.copytree(packet, p)
            kw = mutate(p, r) or {}
            if reseal:
                kw["mf"] = seal(p)
            if extra:
                kw.update(extra)
            invoke(label, p, expected=2, **kw)

    copied("changed_report", lambda p, r: (p / "REPORT.md").write_text("changed\n") and None)
    copied("missing_report", lambda p, r: (p / "REPORT.md").unlink())
    copied("extra_file", lambda p, r: (p / "extra.txt").write_text("extra\n") and None)
    copied("empty_directory", lambda p, r: (p / "empty").mkdir())
    copied("manifest_duplicate_key", lambda p, r: (p / "MANIFEST.json").write_text(
        '{"schema":"x","schema":"y","files":[]}\n') and
        {"mf": sha(p / "MANIFEST.json")})
    copied("manifest_nonfinite", lambda p, r: (p / "MANIFEST.json").write_text(
        '{"schema":"x","files":NaN}\n') and
        {"mf": sha(p / "MANIFEST.json")})
    copied("manifest_path_traversal", lambda p, r: alter_json(p / "MANIFEST.json",
        lambda d: d["files"][0].update(path="../escape")) or
        {"mf": sha(p / "MANIFEST.json")})
    copied("manifest_duplicate_path", lambda p, r: alter_json(p / "MANIFEST.json",
        lambda d: d["files"].append(d["files"][0])) or
        {"mf": sha(p / "MANIFEST.json")})
    copied("promote_firstness_after_reseal", lambda p, r: alter_json(p / "VERDICT.json",
        lambda d: d.update(firstness_claim=True)), reseal=True)
    copied("promote_verdict_after_reseal", lambda p, r: alter_json(p / "VERDICT.json",
        lambda d: d.update(verdict="FIRST_NOVEL_FULL_SOLUTION")), reseal=True)
    copied("changed_provisional_after_reseal", lambda p, r:
        (p / "PROVISIONAL_INDEPENDENT_VERDICT.json").write_text("{}\n") and None,
        reseal=True)
    copied("input_path_traversal_after_reseal", lambda p, r: alter_json(p / "INPUT_BINDINGS.json",
        lambda d: d["files"][0].update(path="../escape")), reseal=True)
    copied("body_path_traversal_after_reseal", lambda p, r: alter_json(p / "PRIMARY_BODY_BINDINGS.json",
        lambda d: d["files"][0].update(path="../escape")), reseal=True)

    def report_special(p, r, kind):
        target = p / "REPORT.md"
        data = target.read_bytes()
        target.unlink()
        outside = r / "outside_report"
        outside.write_bytes(data)
        if kind == "symlink":
            target.symlink_to(outside)
        elif kind == "hardlink":
            os.link(outside, target)
        else:
            os.mkfifo(target)
    for kind in ["symlink", "hardlink", "fifo"]:
        copied("report_" + kind, lambda p, r, k=kind: report_special(p, r, k))

    def packet_link(p, r):
        link = r / "linked_packet"
        link.symlink_to(p, target_is_directory=True)
        return {"checker": link / "verify_priority.py"}
    copied("checker_symlink_ancestor", packet_link)

    def self_link(p, r):
        checker = p / "verify_priority.py"
        outside = r / "actual_checker.py"
        checker.rename(outside)
        checker.symlink_to(outside)
    copied("checker_self_symlink", self_link)

    def input_problem(p, r, kind):
        i = r / "intake"
        shutil.copytree(intake, i)
        selected = i / "SELECTED_PUBLIC_RECORD.json"
        if kind == "tamper":
            selected.write_text("{}\n")
        else:
            data = selected.read_bytes()
            selected.unlink()
            outside = r / "selected"
            outside.write_bytes(data)
            if kind == "symlink":
                selected.symlink_to(outside)
            elif kind == "hardlink":
                os.link(outside, selected)
            else:
                os.mkfifo(selected)
        return {"i": i}
    for kind in ["tamper", "symlink", "hardlink", "fifo"]:
        copied("selected_" + kind, lambda p, r, k=kind: input_problem(p, r, k))

    def primary_problem(p, r, kind):
        bank = r / "primary"
        bank.mkdir()
        rows = json.loads((p / "PRIMARY_BODY_BINDINGS.json").read_text())["files"]
        for row in rows:
            dest = bank / row["path"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(primary / row["path"], dest)
        first = bank / rows[0]["path"]
        if kind == "tamper":
            first.write_bytes(first.read_bytes() + b"x")
        else:
            first.unlink()
        return {"b": bank}
    for kind in ["tamper", "missing"]:
        copied("primary_" + kind, lambda p, r, k=kind: primary_problem(p, r, k))

    result = {"schema": "pr789-priority-custody-controls-v1",
              "result": "PASS" if all(x["pass"] for x in cases) else "FAIL",
              "positive_cases": sum(x["expected_exit"] == 0 for x in cases),
              "negative_cases": sum(x["expected_exit"] != 0 for x in cases),
              "cases": cases,
              "scope": "Trust-boundary and priority-promotion controls, not mathematical proof tests."}
    Path(a.out).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ["result", "positive_cases", "negative_cases"]}))
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
