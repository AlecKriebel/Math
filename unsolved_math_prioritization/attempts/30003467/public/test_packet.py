#!/usr/bin/env python3
"""Adversarial controls against disposable packet copies; never modifies the original."""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

def require(condition, message):
    if not condition:
        raise ValueError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def rebind(root):
    write_json(root / "MANIFEST.json", {"schema": 1, "files": [
        {"name": p.name, "bytes": p.stat().st_size, "sha256": digest(p)}
        for p in sorted(root.iterdir()) if p.name != "MANIFEST.json"]})

def run(root, mode, pin, args=()):
    cmd = [sys.executable, "-B"] + ([mode] if mode else [])
    return subprocess.run(cmd + [str(root / "verify_packet.py"), "--expected-manifest", pin] + list(args),
                          cwd=root.parent, capture_output=True, text=True,
                          env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})

def main():
    original = Path(__file__).resolve().parent
    original_hashes = {p.name: digest(p) for p in original.iterdir()}
    successes = 0
    rejections = 0
    modes = ["", "-O", "-OO"]
    with tempfile.TemporaryDirectory(prefix="pseudodisk-packet-") as tmp:
        temp = Path(tmp)
        for mode in modes:
            root = temp / ("valid" + (mode or "normal"))
            shutil.copytree(original, root)
            result = run(root, mode, digest(root / "MANIFEST.json"))
            require(result.returncode == 0, "Valid packet rejected: " + result.stderr)
            successes += 1
        mutations = ["proof_bytes", "missing_file", "extra_file", "symlink", "duplicate_entry",
                     "unsafe_member", "boolean_byte_count", "duplicate_json_key", "bad_json",
                     "nonfinite_json", "wrong_pin", "wrong_threshold", "wrong_primal_dual",
                     "wrong_radius_scope", "wrong_novelty", "wrong_solved_direction", "wrong_attempt_count",
                     "boolean_threshold", "malformed_claim", "wrong_math_receipt", "missing_sources"]
        for mode in modes:
            for name in mutations:
                root = temp / ((mode or "normal") + "_" + name)
                shutil.copytree(original, root)
                pin = digest(root / "MANIFEST.json")
                extra_args = []
                if name == "proof_bytes":
                    (root / "PROOF.md").write_bytes(b"Wrong target proof\n")
                elif name == "missing_file":
                    (root / "PROOF.md").unlink()
                elif name == "extra_file":
                    (root / "unlisted.txt").write_text("unlisted")
                elif name == "symlink":
                    (root / "PROOF.md").unlink()
                    (root / "PROOF.md").symlink_to(original / "PROOF.md")
                elif name in ["duplicate_entry", "unsafe_member", "boolean_byte_count"]:
                    m = json.loads((root / "MANIFEST.json").read_text())
                    if name == "duplicate_entry": m["files"].append(copy.deepcopy(m["files"][0]))
                    if name == "unsafe_member": m["files"][0]["name"] = "../PROOF.md"
                    if name == "boolean_byte_count": m["files"][0]["bytes"] = True
                    write_json(root / "MANIFEST.json", m)
                    pin = digest(root / "MANIFEST.json")
                elif name in ["duplicate_json_key", "bad_json", "nonfinite_json"]:
                    value = {"duplicate_json_key": '{"schema":1,"schema":1,"files":[]}',
                             "bad_json": '{', "nonfinite_json": '{"schema":NaN,"files":[]}'}[name]
                    (root / "MANIFEST.json").write_text(value)
                    pin = digest(root / "MANIFEST.json")
                elif name == "wrong_pin": pin = "0" * 64
                elif name == "wrong_math_receipt":
                    r = json.loads((root / "MATH_RESULTS.json").read_text()); r["disk_cases"] += 1
                    write_json(root / "MATH_RESULTS.json", r); rebind(root); pin = digest(root / "MANIFEST.json")
                elif name == "missing_sources": extra_args = ["--source-root", str(temp / "absent")]
                else:
                    c = json.loads((root / "CLAIM.json").read_text())
                    changes = {"wrong_threshold": ("threshold", 3), "wrong_primal_dual": ("coloring", "dual_regions"),
                               "wrong_radius_scope": ("fixed_radius_counterexample_claim", True),
                               "wrong_novelty": ("novelty_claim", True), "wrong_solved_direction": ("answer", "positive"),
                               "wrong_attempt_count": ("approaches", 1), "boolean_threshold": ("threshold", True)}
                    if name == "malformed_claim": c = []
                    else: k, v = changes[name]; c[k] = v
                    write_json(root / "CLAIM.json", c); rebind(root); pin = digest(root / "MANIFEST.json")
                result = run(root, mode, pin, extra_args)
                require(result.returncode != 0, "Invalid packet accepted: " + mode + ":" + name)
                rejections += 1
        relocated = temp / "relocated_readonly"
        shutil.copytree(original, relocated)
        before = {p.name: digest(p) for p in relocated.iterdir()}
        for p in relocated.iterdir(): p.chmod(0o444)
        relocated.chmod(0o555)
        try:
            for mode in modes:
                result = run(relocated, mode, digest(relocated / "MANIFEST.json"))
                require(result.returncode == 0, "Read-only relocation rejected: " + result.stderr)
                successes += 1
            require(before == {p.name: digest(p) for p in relocated.iterdir()}, "Read-only packet changed")
        finally:
            relocated.chmod(0o755)
            for p in relocated.iterdir(): p.chmod(0o644)
    require(original_hashes == {p.name: digest(p) for p in original.iterdir()}, "Original packet changed")
    print(json.dumps({"valid_and_readonly_runs": successes, "invalid_controls_rejected": rejections,
                      "modes": ["normal", "-O", "-OO"], "writes_to_original": 0,
                      "scope": "packet_and_explicit_claim_guards_not_geometric_existence"}, sort_keys=True, indent=2))

if __name__ == "__main__":
    main()
