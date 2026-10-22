"""Integrity-bound normal/optimized replay of the exact PR411 candidate.

Authenticate the distributed seal independently before trusting executable code.
The unkeyed manifest detects corruption under that custody assumption, not an
attacker who can replace the complete code, whitelist, and seal together.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
from guard_relation import PATH_COUNTS, RUNTIME_COUNTS, relation

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def metadata(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": digest(data),
            "git_blob_sha1": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()}


def safe_path(root, relative):
    require(isinstance(relative, str), "non-string manifest path")
    p = Path(relative)
    require(not p.is_absolute() and p.as_posix() == relative and ".." not in p.parts,
            "unsafe manifest path: " + relative)
    target = root / p
    require(target.is_file() and not target.is_symlink(), "missing/nonregular file: " + relative)
    require(target.resolve().is_relative_to(root.resolve()), "escaped manifest path")
    return target


def check_entries(root, entries, expected_paths):
    require(isinstance(entries, list), "manifest entries must be a list")
    paths = [e["path"] for e in entries]
    require(len(paths) == len(set(paths)) and set(paths) == set(expected_paths),
            "manifest path coverage mismatch")
    for entry in entries:
        actual = metadata(safe_path(root, entry["path"]))
        for key in ("bytes", "sha256", "git_blob_sha1"):
            if key in entry:
                require(actual[key] == entry[key], "metadata mismatch " + entry["path"] + " " + key)
        require("bytes" in entry and "sha256" in entry, "incomplete integrity entry")


def main():
    require(len(sys.argv) == 1, "run_all.py accepts no arguments; authenticate the seal before execution")
    seal = json.loads((ROOT / "FINAL_SEAL.json").read_text())
    whitelist_bytes = (ROOT / "PUBLICATION_WHITELIST.json").read_bytes()
    require(digest(whitelist_bytes) == seal["whitelist_sha256"], "whitelist seal mismatch")
    whitelist = json.loads(whitelist_bytes)
    require(whitelist["schema"] == "pr411-verification-positive-whitelist-v2", "whitelist schema")
    excluded = {"PUBLICATION_WHITELIST.json", "FINAL_SEAL.json"}
    require(set(whitelist["excluded_self_custody_files"]) == excluded, "self-custody exclusion mismatch")
    all_paths = set()
    for path in ROOT.rglob("*"):
        require(not path.is_symlink(), "symlink excluded from packet: " + str(path))
        require(path.is_dir() or path.is_file(), "nonregular entry excluded from packet: " + str(path))
        if path.is_file():
            all_paths.add(path.relative_to(ROOT).as_posix())
    listed = [entry["path"] for entry in whitelist["files"]]
    require(all_paths == set(listed) | excluded, "positive package file-set mismatch")
    check_entries(ROOT, whitelist["files"], all_paths - excluded)
    require(seal["file_count"] == len(listed), "seal file count mismatch")

    receipt = json.loads((ROOT / "SOURCE_RECEIPT.json").read_text())
    require(receipt["source_head"] == "ac8b960bdda61c154cc30d7e3aba70389a9b139e"
            and receipt["status"] == "claimed_solved" and receipt["author_turns"] == "2/5",
            "original PR source identity changed")
    prefix = "unsolved_math_prioritization/attempts/6800014/"
    original_entries = [{"path": e["remote_path"].removeprefix(prefix), "bytes": e["size"],
                         "sha256": e["sha256"], "git_blob_sha1": e["blob_sha"]}
                        for e in receipt["files"]]
    require(all(e["remote_path"].startswith(prefix) for e in receipt["files"]), "source scope mismatch")
    original = ROOT / "original_packet"
    current = ROOT / "author_packet"
    expected = {e["path"] for e in original_entries}
    require(len(expected) == 19, "nineteen original author files required")
    check_entries(original, original_entries, expected)
    for directory in (original, current):
        require({p.relative_to(directory).as_posix() for p in directory.rglob("*") if p.is_file()} == expected,
                "nineteen-file author inventory mismatch")
        publication = json.loads((directory / "PUBLICATION_MANIFEST.json").read_text())
        require(publication["problem_id"] == 6800014 and publication["status"] == "claimed_solved"
                and publication["substantive_attempts"] == 2 and publication["attempt_budget"] == 5
                and publication["mathematical_repairs_after_audit"] is False,
                "publication claim/accounting metadata changed")
        check_entries(directory, publication["files_except_this_manifest"], expected - {"PUBLICATION_MANIFEST.json"})
        require(publication["audit_sha256"] == metadata(directory / "audit/INDEPENDENT_AUDIT.md")["sha256"],
                "historical audit metadata mismatch")
        frozen = json.loads((directory / "FROZEN_AUTHOR_HASHES.json").read_text())
        frozen_paths = {p.removeprefix("frozen_author/") for p in expected if p.startswith("frozen_author/")}
        require(len(frozen_paths) == 6, "six frozen author objects required")
        check_entries(directory / "frozen_author", frozen["publication_allowed_files"], frozen_paths)
    allowed_changes = set(PATH_COUNTS) | {"README.md", "EDITORIAL_CHANGES.md", "RESEARCH_LOG.md", "PUBLICATION_MANIFEST.json", "SOURCE_AUDIT.md"}
    for path in sorted(expected - allowed_changes):
        require((current / path).read_bytes() == (original / path).read_bytes(), "unauthorized original/proof change: " + path)
    relations = [relation((original / path).read_text(), (current / path).read_text(), path) for path in PATH_COUNTS]

    import sympy
    require(sympy.__version__ == "1.14.0", "SymPy 1.14.0 required for exact recorded replay")
    reference = json.loads((ROOT / "REFERENCE_RESULTS.json").read_text())
    require(set(reference["scripts"]) == set(PATH_COUNTS), "reference script coverage mismatch")
    runs = []
    for path in PATH_COUNTS:
        command = [sys.executable] + (["-O"] if sys.flags.optimize else []) + [
            str(ROOT / "run_checked.py"), str(current / path), str(RUNTIME_COUNTS[path])]
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        process = subprocess.run(command, capture_output=True, text=True, env=env, timeout=120)
        require(process.returncode == 0, "current checker failed " + path + ": " + process.stderr)
        require(process.stderr == "", "unexpected current checker stderr: " + path)
        result = json.loads(process.stdout)
        require(result["runtime_checkpoints"] == RUNTIME_COUNTS[path]
                and result["static_checkpoints_reached"] == PATH_COUNTS[path], "runtime checkpoint coverage mismatch")
        require(result["stdout_sha256"] == reference["scripts"][path]["stdout_sha256"], "regenerated output mismatch: " + path)
        runs.append({"path": path, "runtime_checkpoints": result["runtime_checkpoints"],
                     "stdout_sha256": result["stdout_sha256"], "output_matches_recorded": True})
    print(json.dumps({"result": "PASS", "optimized": bool(sys.flags.optimize),
                      "positive_whitelist_files": len(listed), "original_author_files": 19,
                      "current_author_files": 19, "current_publication_entries": 18,
                      "frozen_author_files": 6, "sympy": sympy.__version__,
                      "guard_relations": relations, "runtime_checkpoints": 54,
                      "runs": runs, "mathematical_proof_changed": False,
                      "historical_missing_objects": "UNATTESTED",
                      "historical_optimized_validation": "NOT CERTIFIED",
                      "trust_boundary": "independently authenticated package custody; exact algebra plus byte binding, not semantic proof of prose"},
                     indent=2))


if __name__ == "__main__":
    main()
