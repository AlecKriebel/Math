#!/usr/bin/env python3
"""Strict portable publication checks; not a proof of the historical theorem."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
AUTHOR = "6f3763c7b21f9577a9145979b94eacc4fc124669d0ff326889350b4300eb1d81"
AUDIT = "91453f9aa72892de51dd1166d464e4840f126914f17ce639e673a2e670db3aa8"
COUNTS = {"affine_rotation_evaluation": 72,
          "positive_degree_translation_invariance": 24,
          "lacunary_finite_bloch_controls": 44,
          "lacunary_coefficient_controls": 22}


def require(value, label):
    if not value:
        raise ValueError(label)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root):
    require(root.is_dir() and not root.is_symlink(), "invalid root")
    files, dirs = set(), set()
    for path in root.rglob("*"):
        require(not path.is_symlink(), "symlink forbidden")
        require(path.is_file() or path.is_dir(), "nonregular object")
        name = path.relative_to(root).as_posix()
        (files if path.is_file() else dirs).add(name)
    expected_dirs = {str(p) for name in files for p in PurePosixPath(name).parents
                     if str(p) != "."}
    require(dirs == expected_dirs, "unexpected empty directory")
    return files


def entries(root, records):
    require(type(records) is list, "manifest entries must be a list")
    names = set()
    for rec in records:
        name = rec["path"]
        require(type(name) is str, "path must be a string")
        p = PurePosixPath(name)
        require(name and not p.is_absolute() and ".." not in p.parts and
                p.as_posix() == name and "\\" not in name, "unsafe path")
        require(name not in names, "duplicate manifest path")
        names.add(name)
        path = root / name
        require(path.is_file() and not path.is_symlink(), "missing or linked file")
        for parent in p.parents:
            require(not (root / parent).is_symlink(), "linked parent")
        raw = path.read_bytes()
        require(type(rec["bytes"]) is int and len(raw) == rec["bytes"], "byte count")
        require(hashlib.sha256(raw).hexdigest() == rec["sha256"], "file hash")
    return names


def verify(root):
    m = read_json(root / "PUBLICATION_MANIFEST.json")
    require((m["problem_id"], m["rank"], m["status"], m["turns"]) ==
            (2305033, 680, "already_solved", "1/5"), "target and disposition")
    names = entries(root, m["files"])
    require(inventory(root) == names | {"PUBLICATION_MANIFEST.json"}, "exact inventory")
    require(sha(root / "author/AUTHOR_MANIFEST.json") == AUTHOR, "author freeze")
    require(sha(root / "audit/AUDIT_MANIFEST.json") == AUDIT, "audit freeze")
    for folder, manifest in [("author", "AUTHOR_MANIFEST.json"),
                             ("audit", "AUDIT_MANIFEST.json")]:
        nested = read_json(root / folder / manifest)
        require(entries(root / folder, nested["files"]) | {manifest} ==
                inventory(root / folder), "nested inventory")
    binding = read_json(root / "BINDING.json")
    require(binding["author_manifest_sha256"] == AUTHOR and
            binding["audit_manifest_sha256"] == AUDIT, "binding identities")
    require((binding["campaign_response_turns"], binding["author_new_proof_search_turns"],
             binding["campaign_turn_limit"]) == (1, 0, 5), "separate turn counts")
    require(binding["original_1977_full_proof_inspected"] is False and
            binding["new_solution_claimed"] is False, "historical proof boundary")
    expected = read_json(root / "author/EXPECTED_CHECKS.json")
    require(expected["counts"] == COUNTS and expected["total_checks"] == 162 and
            expected["all_passed"] is True, "finite control categories")
    require(expected["historical_covering_theorem_independently_proved"] is False and
            expected["new_solution_claimed"] is False, "finite control scope")
    audit = read_json(root / "audit/AUDIT_BINDING.json")
    require(audit["author_manifest_sha256"] == AUTHOR and
            audit["verdict"] == "pass_source_verified_already_solved_with_explicit_limits",
            "independent audit binding")
    require(audit["credited_article"]["original_full_proof_read"] is False and
            audit["new_solution_claimed"] is False, "independent audit limits")
    return len(names) + 1


def replay(root):
    # -I ignores PYTHONOPTIMIZE and avoids inheriting the wrapper's -O flag.
    # The frozen author scripts use assertions, which must remain enabled.
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    env.pop("PYTHONOPTIMIZE", None)
    with tempfile.TemporaryDirectory(prefix="triangular-replay-") as tmp:
        target = Path(tmp) / "packet"
        shutil.copytree(root, target)
        require(verify(target) == 19, "portable inventory")
        probe = subprocess.run([sys.executable, "-I", "-B", "-c", "print(__debug__)"],
                               env=env, check=True, capture_output=True)
        require(probe.stdout == b"True\n", "assertions must be enabled")
        outputs = {}
        for name in ("author/verify.py", "author/verify_integrity.py", "audit/verify_audit.py"):
            result = subprocess.run([sys.executable, "-I", "-B", str(target / name)],
                                    cwd=tmp, env=env, check=True, capture_output=True)
            outputs[name] = result.stdout
        expected = (target / "author/EXPECTED_CHECKS.json").read_bytes()
        require(outputs["author/verify.py"] == expected ==
                (target / "audit/ACTUAL_CHECKS.json").read_bytes(), "exact replay output")
        for raw in outputs.values():
            require(json.loads(raw)["all_passed"] is True, "replay passed field")
        verify(target)
    return {"finite_controls": 162, "counts": COUNTS, "checks_byte_exact": True,
            "author_and_audit_scripts_passed": True, "assertions_enabled": True,
            "historical_theorem_proved": False}


def selftest(root):
    cases = ("extra_file", "empty_directory", "changed_file", "missing_file",
             "duplicate_entry", "unsafe_path", "symlink", "symlink_directory",
             "duplicate_json_key", "changed_author_binding", "changed_audit_binding",
             "changed_turn_count", "changed_proof_limit")
    rejected = []
    for case in cases:
        with tempfile.TemporaryDirectory(prefix="triangular-negative-") as tmp:
            target = Path(tmp) / "packet"
            shutil.copytree(root, target)
            path = target / "PUBLICATION_MANIFEST.json"
            m = read_json(path)
            changed = None
            if case == "extra_file":
                (target / "unexpected.txt").write_text("reject\n")
            elif case == "empty_directory":
                (target / "unexpected").mkdir()
            elif case == "changed_file":
                (target / "author/README.md").write_bytes(b"tampered\n")
            elif case == "missing_file":
                (target / "audit/INDEPENDENT_AUDIT.md").unlink()
            elif case == "duplicate_entry":
                m["files"].append(dict(m["files"][0]))
            elif case == "unsafe_path":
                m["files"][0]["path"] = "../outside"
            elif case == "symlink":
                (target / "linked").symlink_to(target / "README.md")
            elif case == "symlink_directory":
                (target / "linked_directory").symlink_to(target / "author", target_is_directory=True)
            elif case in ("changed_author_binding", "changed_audit_binding"):
                changed = ("author/AUTHOR_MANIFEST.json" if case == "changed_author_binding"
                           else "audit/AUDIT_MANIFEST.json")
                p = target / changed
                p.write_bytes(p.read_bytes() + b"\n")
            elif case in ("changed_turn_count", "changed_proof_limit"):
                changed = "BINDING.json"
                b = read_json(target / changed)
                if case == "changed_turn_count":
                    b["campaign_response_turns"] = 0
                else:
                    b["original_1977_full_proof_inspected"] = True
                (target / changed).write_text(json.dumps(b))
            if changed:
                p = target / changed
                for rec in m["files"]:
                    if rec["path"] == changed:
                        rec.update(bytes=p.stat().st_size, sha256=sha(p))
            encoded = json.dumps(m, indent=2) + "\n"
            if case == "duplicate_json_key":
                encoded = encoded.replace("{", '{"problem_id":2305033,', 1)
            path.write_text(encoded)
            try:
                verify(target)
            except (ValueError, KeyError, FileNotFoundError):
                rejected.append(case)
            else:
                raise ValueError("negative test accepted: " + case)
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    result = {"problem_id": 2305033, "status": "PASS", "files": verify(HERE)}
    if args.replay:
        result["replay"] = replay(HERE)
    if args.selftest:
        result["negative_tests_rejected"] = selftest(HERE)
    verify(HERE)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
