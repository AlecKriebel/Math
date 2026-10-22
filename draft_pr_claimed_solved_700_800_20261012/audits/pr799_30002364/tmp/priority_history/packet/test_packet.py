#!/usr/bin/env python3
"""Replay integrity and execution controls after authenticating this file.

The trusted launcher's inventory check authenticates this script before use.
All transient files remain below the audit directory and are removed afterward.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("packet")
    parser.add_argument("manifest_sha256")
    parser.add_argument("checker_sha256")
    args = parser.parse_args()
    root = Path(os.path.abspath(args.packet))
    require(sha(root / "verify_packet.py") == args.checker_sha256, "external checker preflight")
    require(sha(root / "MANIFEST.json") == args.manifest_sha256, "external manifest preflight")
    results = []

    def run(label, path, expected=True, optimized=False, manifest=None, checker=None, cwd=None, env=None):
        # The checker itself must be trusted before execution, even on copied packets.
        require(sha(path / "verify_packet.py") == args.checker_sha256, "checker changed before launch")
        cmd = [sys.executable, "-I", "-S", "-B"] + (["-O"] if optimized else [])
        cmd += [str(path / "verify_packet.py"), str(path), manifest or args.manifest_sha256,
                checker or args.checker_sha256, "--execute"]
        out = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, env=env)
        passed = out.returncode == 0
        require(passed == expected, label + ": unexpected exit status")
        if expected:
            payload = json.loads(out.stdout)
            require(payload["integrity"] == "PASS" and payload["finite"]["status"] == "PASS", label)
        else:
            require("REJECT:" in out.stderr, label + ": no explicit rejection")
        results.append({"control": label, "expected": "PASS" if expected else "REJECT", "observed": "PASS" if passed else "REJECT"})

    run("normal authenticated execution", root)
    run("optimized authenticated execution", root, optimized=True)
    with tempfile.TemporaryDirectory(prefix="priority controls ", dir=root.parent) as tmp:
        base = Path(tmp)
        original = base / "relocated packet with spaces"
        shutil.copytree(root, original)
        run("relocation with spaces", original)
        hostile = base / "hostile cwd"
        hostile.mkdir()
        for name in ["json.py", "hashlib.py", "fractions.py", "sitecustomize.py"]:
            (hostile / name).write_text("raise RuntimeError('hostile import executed')\n")
        env = dict(os.environ, PYTHONPATH=str(hostile))
        run("optimized relocation hostile cwd and PYTHONPATH", original, optimized=True, cwd=hostile, env=env)
        run("wrong external manifest pin", original, expected=False, manifest="0" * 64)
        run("wrong external checker pin", original, expected=False, checker="0" * 64)

        def mutated(label, mutate):
            target = base / ("case " + str(len(results)))
            shutil.copytree(root, target)
            mutate(target)
            run(label, target, expected=False)

        mutated("changed authored report", lambda p: (p / "PRIORITY_REPORT.md").write_text("changed\n"))
        mutated("changed finite checker", lambda p: (p / "verify_finite.py").write_text("print('fake')\n"))
        mutated("changed source ledger metadata", lambda p: (p / "SOURCE_READING_LEDGER.json").write_text("{}\n"))
        mutated("extra cache file", lambda p: (p / "accidental.pdf").write_bytes(b"not a source"))
        mutated("extra directory", lambda p: (p / "__pycache__").mkdir())
        mutated("missing required ledger", lambda p: (p / "SOURCE_BYTE_LEDGER.json").unlink())
        mutated("rewritten manifest", lambda p: (p / "MANIFEST.json").write_text("{}\n"))

        def link_member(p):
            x = p / "PRIORITY_REPORT.md"
            x.unlink()
            x.symlink_to(root / "PRIORITY_REPORT.md")
        mutated("member symlink", link_member)
        link_root = base / "root symlink"
        link_root.symlink_to(original, target_is_directory=True)
        run("root symlink", link_root, expected=False)
        real_parent = base / "real parent"
        real_parent.mkdir()
        shutil.copytree(root, real_parent / "packet")
        link_parent = base / "parent symlink"
        link_parent.symlink_to(real_parent, target_is_directory=True)
        run("parent symlink", link_parent / "packet", expected=False)

        changed_checker = base / "checker substitution"
        shutil.copytree(root, changed_checker)
        (changed_checker / "verify_packet.py").write_text("print('fake PASS')\n")
        require(sha(changed_checker / "verify_packet.py") != args.checker_sha256, "substitution not detected")
        results.append({"control": "checker substitution rejected before execution", "expected": "REJECT", "observed": "REJECT"})
    require(len(results) == 17, "control count")
    print(json.dumps({"status": "PASS", "controls": results, "count": len(results)}, indent=2))


if __name__ == "__main__":
    main()
