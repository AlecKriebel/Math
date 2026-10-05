#!/usr/bin/env python3
"""Strict portable packet checks, not a counterexample or full-proof certificate."""
import argparse
import difflib
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
FINAL = "0a24a3780c51b133f7366a19d3ebba122dc5bfd4a2ade6fddae9857f83083c0a"
ORIGINAL = "a70b48ea0fd5980c2c1de003d2e9b6142f57b62c954652c52f66dfa27238e644"
FREEZE = "69423e1c76f714e900e26bc8a52c3d6420a7d82ba0af19df9fae9586c68c0666"


def require(value, label):
    if not value:
        raise ValueError(label)


def unique_object(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, "duplicate JSON key")
        out[key] = value
    return out


def read_json(path):
    return json.loads(path.read_text(), object_pairs_hook=unique_object)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root):
    require(root.is_dir() and not root.is_symlink(), "invalid inventory root")
    found = set()
    for path in root.rglob("*"):
        require(not path.is_symlink(), "symbolic links forbidden")
        require(path.is_dir() or path.is_file(), "nonregular object forbidden")
        if path.is_file():
            found.add(path.relative_to(root).as_posix())
    return found


def entries(root, records):
    found = set()
    for rec in records:
        name = rec["path"]
        p = PurePosixPath(name)
        require(name and not p.is_absolute() and ".." not in p.parts and
                p.as_posix() == name and "\\" not in name, "unsafe path")
        require(name not in found, "duplicate manifest path")
        found.add(name)
        path = root / name
        require(path.is_file() and not path.is_symlink(), "missing or linked file: " + name)
        data = path.read_bytes()
        require(type(rec["bytes"]) is int and len(data) == rec["bytes"], "byte count: " + name)
        require(hashlib.sha256(data).hexdigest() == rec["sha256"], "hash: " + name)
    return found


def correction_diff(root):
    result = []
    for path in sorted((root / "pre_edit").iterdir()):
        after = root / "final" / path.name
        if after.is_file():
            result.extend(difflib.unified_diff(
                path.read_text().splitlines(keepends=True),
                after.read_text().splitlines(keepends=True),
                fromfile="pre_edit/" + path.name, tofile="final/" + path.name))
    return "".join(result).encode()


def verify(root):
    m = read_json(root / "PUBLICATION_MANIFEST.json")
    require((m["problem_id"], m["rank"], m["status"], m["turns"]) ==
            (2304029, 678, "already_solved", "1/5"), "problem/disposition")
    require(m["basis"] == "prior_resolution_attribution_only", "attribution scope")
    paths = entries(root, m["files"])
    require(inventory(root) == paths | {"PUBLICATION_MANIFEST.json"}, "exact inventory")
    require(sha(root / "final/FILE_MANIFEST.json") == FINAL, "final manifest binding")
    require(sha(root / "pre_edit/FILE_MANIFEST.json") == ORIGINAL, "original manifest binding")
    require(sha(root / "final/ORIGINAL_PACKET_MANIFEST.json") == FREEZE, "freeze binding")
    for folder in ("final", "pre_edit"):
        nested = read_json(root / folder / "FILE_MANIFEST.json")
        require(entries(root / folder, nested["files"]) | {"FILE_MANIFEST.json"} ==
                inventory(root / folder), folder + " inventory")
    frozen = read_json(root / "final/ORIGINAL_PACKET_MANIFEST.json")
    require(entries(root / "pre_edit", frozen["files"]) == inventory(root / "pre_edit"),
            "frozen original inventory")
    binding = read_json(root / "BINDING.json")
    require(binding["final_manifest_sha256"] == FINAL and
            binding["original_manifest_sha256"] == ORIGINAL and
            binding["freeze_manifest_sha256"] == FREEZE, "binding identities")
    require(entries(root, binding["snapshot_files"]) ==
            {p for p in paths if p.startswith(("final/", "pre_edit/"))}, "snapshot binding")
    require((root / "CORRECTIONS.diff").read_bytes() == correction_diff(root), "exact correction diff")
    require(binding["correction_diff_sha256"] == sha(root / "CORRECTIONS.diff"), "diff binding")
    audit = read_json(root / "final/INDEPENDENT_AUDIT.json")
    require(audit["decision"] == "already_solved" and
            audit["decision_basis"] == "prior_resolution_attribution_only", "audit decision")
    for key in ("full_source_proof_independently_verified",
                "explicit_counterexample_independently_verified", "lost_historical_audit_recovered"):
        require(audit[key] is False, "proof/recovery boundary")
    require(audit["original_manifest_sha256"] == ORIGINAL, "audit original identity")
    require(audit["verifier_review"]["final_verifier"]["sha256"] ==
            sha(root / "final/verify_factored_witness.py"), "audited verifier binding")
    require(audit["dataset_binding"]["upstream_statement_hash_independently_recomputed"] is False and
            audit["dataset_binding"]["complete_upstream_corpus_match_verified"] is False,
            "dataset boundary")
    return len(paths) + 1


def replay(root):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    results = {}
    with tempfile.TemporaryDirectory(prefix="roitman-replay-") as tmp:
        for folder in ("pre_edit", "final"):
            shutil.copytree(root / folder, Path(tmp) / folder)
        final = Path(tmp) / "final"
        for key, script, expected, flags in [
            ("self_tests", "verify_factored_witness.py", "VERIFIER_TEST_RESULT.json", []),
            ("independent", "test_factored_witness_independent.py", "INDEPENDENT_TEST_RESULT.json", []),
            ("optimized_independent", "test_factored_witness_independent.py", "INDEPENDENT_TEST_RESULT.json", ["-O"]),
        ]:
            run = subprocess.run([sys.executable, *flags, "-B", script], cwd=final, env=env,
                                 check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            require(run.stdout == (final / expected).read_bytes(), "replay output: " + key)
            results[key] = json.loads(run.stdout)
        # Preserve and reproduce the pre-edit input-control defect without
        # promoting any historical check to a current counterexample claim.
        code = ("import sympy as s; import verify_factored_witness as v; "
                "r=v.verify([v.z-s.Float('1.000000000000001')],[1],[1]); "
                "print(r['equal_zero_sets'])")
        old = subprocess.run([sys.executable, "-B", "-c", code], cwd=Path(tmp) / "pre_edit",
                             env=env, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        new = subprocess.run([sys.executable, "-B", "-c", code], cwd=final,
                             env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        require(old.stdout == b"True\n", "original Float acceptance not reproduced")
        require(new.returncode != 0 and b"floats are not allowed" in new.stderr,
                "final Float rejection not reproduced")
        results["historical_float_acceptance_and_final_rejection"] = True
    return results


def selftest(root):
    outcomes = []
    for case in ("extra_file", "changed_file", "missing_file", "duplicate_entry", "unsafe_path",
                 "changed_final_binding", "changed_original_binding", "changed_freeze_binding",
                 "changed_correction_diff", "symbolic_link", "duplicate_json_key"):
        with tempfile.TemporaryDirectory(prefix="roitman-negative-") as tmp:
            target = Path(tmp) / "packet"
            shutil.copytree(root, target)
            mpath = target / "PUBLICATION_MANIFEST.json"
            m = read_json(mpath)
            changed = None
            if case == "extra_file":
                (target / "unexpected.txt").write_text("reject\n")
            elif case == "changed_file":
                with (target / "final/STATUS.md").open("ab") as stream:
                    stream.write(b"\n")
            elif case == "missing_file":
                (target / "pre_edit/STATUS.md").unlink()
            elif case == "duplicate_entry":
                m["files"].append(dict(m["files"][0]))
            elif case == "unsafe_path":
                m["files"][0]["path"] = "../outside"
            elif case == "symbolic_link":
                (target / "linked").symlink_to(target / "README.md")
            elif case == "duplicate_json_key":
                pass
            else:
                changed = {"changed_final_binding": "final/FILE_MANIFEST.json",
                           "changed_original_binding": "pre_edit/FILE_MANIFEST.json",
                           "changed_freeze_binding": "final/ORIGINAL_PACKET_MANIFEST.json",
                           "changed_correction_diff": "CORRECTIONS.diff"}[case]
                path = target / changed
                path.write_bytes(path.read_bytes() + b"\n")
                for rec in m["files"]:
                    if rec["path"] == changed:
                        rec.update(bytes=path.stat().st_size, sha256=sha(path))
            encoded = json.dumps(m, indent=2) + "\n"
            if case == "duplicate_json_key":
                encoded = encoded.replace('{', '{"problem_id":2304029,', 1)
            mpath.write_text(encoded)
            try:
                verify(target)
            except (ValueError, KeyError, FileNotFoundError):
                outcomes.append(case)
            else:
                raise ValueError("negative test accepted: " + case)
    return outcomes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    result = {"problem_id": 2304029, "status": "PASS", "files": verify(HERE)}
    if args.replay:
        result["replay"] = replay(HERE)
    if args.selftest:
        result["negative_tests_rejected"] = selftest(HERE)
    verify(HERE)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
