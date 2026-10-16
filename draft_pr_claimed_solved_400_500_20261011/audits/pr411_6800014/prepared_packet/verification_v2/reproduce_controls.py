"""Re-run adversarial controls in temporary copies; never change this bundle.

Pass --private-log-dir PATH to retain raw executions outside the delivery tree.
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
import zipfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent


def hashes(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "git_blob_sha1": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-log-dir", type=Path)
    args = parser.parse_args()
    logdir = args.private_log_dir.resolve() if args.private_log_dir else None
    if logdir:
        if logdir.is_relative_to(ROOT):
            raise RuntimeError("raw logs must be outside delivery bundle")
        logdir.mkdir(parents=True, exist_ok=True)
    results = []
    with tempfile.TemporaryDirectory(prefix="pr411 controls with spaces ") as work:
        work = Path(work)

        def run(name, folder, optimized, expected, relative="run_all.py", diagnostic=None):
            command = [sys.executable] + (["-O"] if optimized else []) + [str(folder / relative)]
            process = subprocess.run(command, cwd=work, capture_output=True, text=True,
                                     timeout=120, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
            match = (process.returncode == 0) if expected == "success" else (process.returncode != 0)
            if diagnostic:
                match = match and diagnostic in process.stderr
            if expected == "success" and relative == "run_all.py":
                parsed = json.loads(process.stdout)
                match = match and parsed["result"] == "PASS" and parsed["runtime_checkpoints"] == 54
            row = {"name": name, "optimized": optimized, "expected": expected,
                   "returncode": process.returncode, "matched_expectation": match,
                   "diagnostic_required": diagnostic,
                   "stdout_sha256": hashlib.sha256(process.stdout.encode()).hexdigest(),
                   "stderr_sha256": hashlib.sha256(process.stderr.encode()).hexdigest()}
            results.append(row)
            if logdir:
                (logdir / (name + ("__optimized" if optimized else "__normal") + ".json")).write_text(
                    json.dumps({"command": command, "cwd": str(work), "result": row,
                                "stdout": process.stdout, "stderr": process.stderr}, indent=2) + "\n")
            if not match:
                raise RuntimeError("control did not meet expectation: " + json.dumps(row) + process.stderr)

        def copied(name):
            target = work / name
            shutil.copytree(ROOT, target)
            return target

        for optimized in (False, True):
            run("baseline_foreign_cwd", ROOT, optimized, "success")
        # A fresh archive formed only from the positive whitelist and its two
        # explicitly separately custodied self-reference files is extracted.
        whitelist = json.loads((ROOT / "PUBLICATION_WHITELIST.json").read_text())
        paths = [e["path"] for e in whitelist["files"]] + whitelist["excluded_self_custody_files"]
        archive = work / "clean bundle.zip"
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
            for path in paths:
                z.write(ROOT / path, path)
        extracted = work / "clean relocated extraction with spaces"
        with zipfile.ZipFile(archive) as z:
            z.extractall(extracted)
        for optimized in (False, True):
            run("clean_relocated_extraction_spaces", extracted, optimized, "success")

        def replace(folder, relative, old, new):
            path = folder / relative
            text = path.read_text()
            if text.count(old) != 1:
                raise RuntimeError("control anchor must be unique: " + relative + " " + old)
            path.write_text(text.replace(old, new, 1))

        controls = [
            ("false_current_theorem_interval", "author_packet/attempts/turn02_slice_proof.md",
             "Fix `u₀` with `0<u₀<1/2`.", "Fix `u₀` with `0<u₀<2`."),
            ("frozen_proof_corruption", "author_packet/frozen_author/attempts/turn02_slice_proof.md", None, "\nCorruption control\n"),
            ("current_manifest_false_claim", "author_packet/PUBLICATION_MANIFEST.json",
             "Counterexample to the literal universal local-maximum solvsoliton assertion, with all nearby left-invariant metrics on the fixed group covered.", "F is 2/3 for all u>0"),
            ("frozen_metadata_corruption", "author_packet/FROZEN_AUTHOR_HASHES.json", None, " "),
            ("original_metadata_corruption", "SOURCE_RECEIPT.json", None, " "),
            ("candidate_script_corruption", "author_packet/verify.py", "norm2(S(A)) == u**2 / 2", "norm2(S(A)) == u**2 / 2 + 1"),
        ]
        for name, relative, old, new in controls:
            folder = copied(name)
            if old is None:
                with (folder / relative).open("a") as f:
                    f.write(new)
            else:
                replace(folder, relative, old, new)
            for optimized in (False, True):
                run(name, folder, optimized, "failure", diagnostic="metadata mismatch")
        for name, kind in (("extra_file", "extra"), ("missing_file", "missing")):
            folder = copied(name)
            if kind == "extra":
                (folder / "unlisted.txt").write_text("control")
            else:
                (folder / "author_packet/README.md").unlink()
            for optimized in (False, True):
                run(name, folder, optimized, "failure", diagnostic="positive package file-set mismatch")
        folder = copied("unlisted_fifo")
        os.mkfifo(folder / "unlisted_fifo")
        for optimized in (False, True):
            run("unlisted_fifo", folder, optimized, "failure",
                diagnostic="nonregular entry excluded from packet")
        folder = copied("whitelist_corruption")
        with (folder / "PUBLICATION_WHITELIST.json").open("a") as f:
            f.write(" ")
        for optimized in (False, True):
            run("whitelist_corruption", folder, optimized, "failure", diagnostic="whitelist seal mismatch")

        # Test the predicates themselves, beyond earlier hash rejection.
        direct = {
            "verify.py": ("norm2(S(A)) == u**2 / 2", "norm2(S(A)) == u**2 / 2 + 1"),
            "check_hessian.py": ("sp.factor(Rdd-expected)==0", "sp.factor(Rdd-expected)==1"),
            "audit/independent_checks.py": ("zero(Ric-expected)", "zero(Ric-expected+sp.eye(5))"),
        }
        for relative, (old, new) in direct.items():
            name = "false_exact_predicate_" + relative.replace("/", "_")
            folder = copied(name)
            replace(folder, "author_packet/" + relative, old, new)
            for optimized in (False, True):
                run(name, folder, optimized, "failure", "author_packet/" + relative,
                    diagnostic="AssertionError: mandatory checkpoint")
        folder = copied("direct_frozen_hash_corruption")
        with (folder / "author_packet/frozen_author/README.md").open("a") as f:
            f.write("\ncorruption\n")
        for optimized in (False, True):
            run("direct_frozen_hash_corruption", folder, optimized, "failure",
                "author_packet/audit/independent_checks.py", diagnostic="AssertionError: mandatory checkpoint")

        # False and / true or branches must not evaluate the division trap.
        for label, predicate, expected in (("lazy_and", "False and (1/0)", "failure"),
                                            ("lazy_or", "True or (1/0)", "success")):
            folder = copied(label)
            replace(folder, "author_packet/verify.py", "norm2(S(A)) == u**2 / 2", predicate)
            for optimized in (False, True):
                run(label, folder, optimized, expected, "author_packet/verify.py",
                    diagnostic="AssertionError: mandatory checkpoint" if expected == "failure" else None)

        # Even updating both attacker-controlled candidate hashes and custody
        # objects cannot turn a changed predicate into an exact guard repair.
        folder = copied("rehash_changed_predicate")
        replace(folder, "author_packet/verify.py", "norm2(S(A)) == u**2 / 2", "norm2(S(A)) == u**2 / 2 + 1")
        manifest_path = folder / "author_packet/PUBLICATION_MANIFEST.json"
        manifest = json.loads(manifest_path.read_text())
        for entry in manifest["files_except_this_manifest"]:
            entry.update(hashes(folder / "author_packet" / entry["path"]))
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        whitelist_path = folder / "PUBLICATION_WHITELIST.json"
        whitelist = json.loads(whitelist_path.read_text())
        for entry in whitelist["files"]:
            entry.update(hashes(folder / entry["path"]))
        whitelist_path.write_text(json.dumps(whitelist, indent=2) + "\n")
        seal_path = folder / "FINAL_SEAL.json"
        seal = json.loads(seal_path.read_text())
        seal["whitelist_sha256"] = hashes(whitelist_path)["sha256"]
        seal_path.write_text(json.dumps(seal, indent=2) + "\n")
        for optimized in (False, True):
            run("rehash_changed_predicate", folder, optimized, "failure",
                diagnostic="current code differs beyond mandatory guard replacement")
    print(json.dumps({"result": "PASS", "executions": len(results), "all_expectations_matched": True,
                      "raw_logs": "private/excluded when requested", "controls": results}, indent=2))


if __name__ == "__main__":
    main()
