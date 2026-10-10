#!/usr/bin/env python3
"""Strict portable inventory/replay checks; not a mathematical proof certificate."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
AUTHOR = "00c2df973bfdae3a3db40076994feba13ae06c6cc7914a86a31ff488ed0dca34"
AUDIT = "eaea8cd717c562c2e6311210344ac8a2a1e555bddbcfb9f54a3962c1ab1cfd15"


def require(value, label):
    if not value:
        raise ValueError(label)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root):
    found = set()
    for path in root.rglob("*"):
        require(not path.is_symlink(), "symbolic links are forbidden")
        if path.is_file():
            found.add(path.relative_to(root).as_posix())
    return found


def entries(root, records):
    paths = set()
    for record in records:
        name = record["path"]
        p = PurePosixPath(name)
        require(name and not p.is_absolute() and ".." not in p.parts and
                p.as_posix() == name and "\\" not in name, "unsafe path")
        require(name not in paths, "duplicate manifest path")
        paths.add(name)
        path = root / name
        require(path.is_file() and not path.is_symlink(), "missing or linked file: " + name)
        data = path.read_bytes()
        require(len(data) == record["bytes"], "byte count mismatch: " + name)
        require(hashlib.sha256(data).hexdigest() == record["sha256"], "hash mismatch: " + name)
    return paths


def verify(root):
    manifest = json.loads((root / "PUBLICATION_MANIFEST.json").read_text())
    require(manifest["problem_id"] == 2303014 and manifest["rank"] == 676, "problem identity")
    require(manifest["status"] == "unsolved" and manifest["turns"] == "5/5", "disposition")
    paths = entries(root, manifest["files"])
    require(inventory(root) == paths | {"PUBLICATION_MANIFEST.json"}, "exact inventory mismatch")
    require(sha(root / "author/MANIFEST.json") == AUTHOR, "author manifest binding")
    require(sha(root / "audit/BINDING.json") == AUDIT, "fresh audit binding")
    am = json.loads((root / "author/MANIFEST.json").read_text())
    require(entries(root / "author", am["files"]) | {"MANIFEST.json"} ==
            inventory(root / "author"), "author inventory")
    ab = json.loads((root / "audit/BINDING.json").read_text())
    require(ab["audited_manifest"]["sha256"] == AUTHOR, "audit target")
    require(entries(root / "author", ab["audited_packet_files"]) ==
            inventory(root / "author"), "audited author inventory")
    require(entries(root / "audit", ab["portable_audit_files"]) | {"BINDING.json"} ==
            inventory(root / "audit"), "audit inventory")
    require(ab["audited_packet_total_bytes"] == sum(
        p.stat().st_size for p in (root / "author").iterdir()), "audited author bytes")
    result = json.loads((root / "audit/AUDIT.json").read_text())
    require(result["fresh_independent_audit"] and not result["historical_results_inherited"], "audit generation")
    require(result["verdict"] == "PASS_PARTIAL_RESULTS_WITH_MINOR_PRECISION_NOTES", "audit scope")
    require(result["claims"][-1] == {"id": "C6", "verdict": "UNRESOLVED", "scope":
        "General positive-mean nonconstant-data sharp problem remains unresolved by this packet and audit."}, "unresolved target")
    return len(paths) + 1


def replay(root):
    counts = {}
    with tempfile.TemporaryDirectory(prefix="circle-minimum-replay-") as tmp:
        for folder, script, output, count in [
            ("author", "verify_exact.py", "CHECKS.json", 30254),
            ("audit", "audit_controls.py", "AUDIT_CHECKS.json", 47419),
        ]:
            target = Path(tmp) / folder
            shutil.copytree(root / folder, target)
            subprocess.run([sys.executable, str(target / script)], cwd=target,
                           check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            require((target / output).read_bytes() == (root / folder / output).read_bytes(),
                    "replay bytes mismatch: " + folder)
            got = json.loads((target / output).read_text())
            require(got["exact_checks"] == count and got["status"] == "PASS", "replay result")
            counts[folder] = count
    return counts


def selftest(root):
    outcomes = []
    for case in ("extra_file", "changed_file", "missing_file", "duplicate_entry",
                 "unsafe_path", "changed_author_binding", "symbolic_link"):
        with tempfile.TemporaryDirectory(prefix="circle-minimum-negative-") as tmp:
            target = Path(tmp) / "packet"
            shutil.copytree(root, target)
            mpath = target / "PUBLICATION_MANIFEST.json"
            manifest = json.loads(mpath.read_text())
            if case == "extra_file":
                (target / "unexpected.txt").write_text("must reject\n")
            elif case == "changed_file":
                with (target / "author/PROOFS.md").open("ab") as stream:
                    stream.write(b"\n")
            elif case == "missing_file":
                (target / "audit/CORRECTIONS.md").unlink()
            elif case == "duplicate_entry":
                manifest["files"].append(dict(manifest["files"][0]))
            elif case == "unsafe_path":
                manifest["files"][0]["path"] = "../outside"
            elif case == "changed_author_binding":
                path = target / "author/MANIFEST.json"
                path.write_bytes(path.read_bytes() + b"\n")
                for record in manifest["files"]:
                    if record["path"] == "author/MANIFEST.json":
                        record["bytes"] = path.stat().st_size
                        record["sha256"] = sha(path)
            else:
                (target / "linked").symlink_to(target / "README.md")
            mpath.write_text(json.dumps(manifest, indent=2) + "\n")
            try:
                verify(target)
            except (ValueError, KeyError, FileNotFoundError):
                outcomes.append(case)
            else:
                raise ValueError("negative test was accepted: " + case)
    return outcomes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    result = {"problem_id": 2303014, "status": "PASS", "files": verify(HERE)}
    if args.replay:
        result["replay_exact_checks"] = replay(HERE)
    if args.selftest:
        result["negative_tests_rejected"] = selftest(HERE)
    verify(HERE)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
