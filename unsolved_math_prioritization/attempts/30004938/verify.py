#!/usr/bin/env python3
"""Offline artifact, exact patch, and computation replay; not formal verification."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
AUTHOR = "nonnegative_critical_varieties_30004938"
AUDIT = "critical_variety_audit"
TARGET = AUTHOR + "/authored/02_bowtie_product_topology.md"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def pins(root, rows):
    for row in rows:
        rel = Path(row["path"])
        require(not rel.is_absolute() and ".." not in rel.parts, "Unsafe pin path")
        require(not (root / rel).is_symlink(), "Symlink in artifact set")
        require(pin(root / rel) == {key: row[key] for key in ("bytes", "sha256")},
                "Pin mismatch: " + str(rel))


def run(script, cwd):
    proc = subprocess.run([sys.executable, str(script)], cwd=cwd,
                          capture_output=True, text=True)
    require(proc.returncode == 0,
            str(script.name) + " failed:\n" + proc.stdout + proc.stderr)


def main():
    manifest = json.loads((ROOT / "PUBLIC_MANIFEST.json").read_text())
    require(manifest["status"] == "unsolved" and manifest["author_approaches"] == 5,
            "Unexpected disposition")
    expected = {row["path"] for row in manifest["files"]} | {"PUBLIC_MANIFEST.json"}
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file()}
    require(actual == expected, "Public allowlist mismatch")
    pins(ROOT, manifest["files"])
    author = json.loads((ROOT / AUTHOR / "MANIFEST.json").read_text())
    audit = json.loads((ROOT / AUDIT / "AUDIT_MANIFEST.json").read_text())
    pins(ROOT / AUTHOR, author["public_files"])
    pins(ROOT / AUDIT, audit["files"])
    input_pins = json.loads((ROOT / AUDIT / "INPUT_PINS.json").read_text())
    pins(ROOT / AUTHOR, input_pins["files"])
    require(pin(ROOT / AUTHOR / "MANIFEST.json")["sha256"] ==
            input_pins["manifest_sha256"], "Original manifest pin mismatch")
    require(pin(ROOT / AUDIT / "REPORT.md")["sha256"] ==
            "c564c146b0d4356c25b2491f7ce3c5a1e9b7b26bd42d1bef533c44789d22f32f",
            "Accepted report mismatch")

    with tempfile.TemporaryDirectory(prefix="critical-varieties-replay-") as td:
        temp = Path(td)
        shutil.copytree(ROOT / AUTHOR, temp / AUTHOR)
        shutil.copytree(ROOT / AUDIT, temp / AUDIT)
        for name in ("bowtie_minors.py", "verify_product_model.py", "enumerate_strands.py",
                     "enumerate_bowtie_tubes.py", "enumerate_bowtie_faces.py"):
            run(temp / AUTHOR / "checks" / name, temp)
        pins(temp / AUTHOR, author["public_files"])
        run(temp / AUDIT / "checks/independent_audit_checks.py", temp)
        run(temp / AUDIT / "tubes/independent_audit.py", temp)
        pins(temp / AUDIT, audit["files"])
        before = {str(p.relative_to(temp / AUTHOR)): pin(p)
                  for p in (temp / AUTHOR).rglob("*") if p.is_file()}
        patch = temp / AUDIT / "patches/01_necklace_terminology.patch"
        lines = patch.read_text().splitlines()
        require(lines[0] == "--- a/" + TARGET and lines[1] == "+++ b/" + TARGET,
                "Wrong patch target")
        require(sum(line.startswith("--- ") for line in lines) == 1 and
                sum(line.startswith("+++ ") for line in lines) == 1,
                "Unexpected multi-file patch")
        proc = subprocess.run(["patch", "--batch", "--fuzz=0", "-p1", "-i", str(patch)],
                              cwd=temp, capture_output=True, text=True)
        require(proc.returncode == 0, "Patch failed: " + proc.stdout + proc.stderr)
        after = {str(p.relative_to(temp / AUTHOR)): pin(p)
                 for p in (temp / AUTHOR).rglob("*") if p.is_file()}
        changed = {key for key in set(before) | set(after) if before.get(key) != after.get(key)}
        require(changed == {"authored/02_bowtie_product_topology.md"},
                "Patch changed unexpected files")
        require((temp / TARGET).read_bytes() ==
                (temp / AUDIT / "patches/02_bowtie_product_topology.corrected.md").read_bytes(),
                "Patched result differs from corrected standalone copy")
        original = (ROOT / TARGET).read_text()
        corrected = (temp / TARGET).read_text()
        old = "Grassmann-necklace complements"
        new = "reduced Grassmann-necklace sets J_r = I_r \\ {r}"
        require(original.count(old) == 1 and original.replace(old, new) == corrected,
                "Correction is not the specified terminology-only replacement")
    print(json.dumps({"status": "PASS", "author_approaches": 5,
                      "problem_status": "unsolved", "original_checker_replays": 5,
                      "independent_checker_replays": 2,
                      "exact_patch_target_only": True,
                      "source_documents_required": False,
                      "universal_resolution_verified": False,
                      "geometric_face_image_surjectivity_verified": False}, indent=2))


if __name__ == "__main__":
    main()
