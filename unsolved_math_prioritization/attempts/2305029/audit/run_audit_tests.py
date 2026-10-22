#!/usr/bin/env python3
"""Exercise trusted original and independent verifiers on disposable copies.

Only supplied allowlisted packet bytes and optional three public PDFs are read.
Original inputs are never modified. Test output contains no source contents.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import stat
import subprocess
import sys
import tempfile

PIN = "cf5f178a46b580701522ce59ff4707c4179963ec5d2f8848a759261b1d974206"
NAMES = {"ACCEPTANCE_REPORT.md", "MANIFEST.json", "REPRODUCIBILITY.md", "RESULT.json", "SOURCES.json", "VALIDATION.json", "verify_packet.py"}
SOURCE_NAMES = {"danielyan2016_published.pdf", "danielyan2016_v1.pdf", "hayman2018_v2.pdf"}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def snapshot(root):
    return {p.name: (len(p.read_bytes()), digest(p.read_bytes())) for p in root.iterdir()}


def writable_remove(path):
    if path.exists():
        for base, dirs, files in os.walk(path):
            Path(base).chmod(0o755)
            for name in files:
                p = Path(base) / name
                if not p.is_symlink():
                    p.chmod(0o644)
        shutil.rmtree(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet-dir", required=True, type=Path)
    parser.add_argument("--source-dir", type=Path)
    args = parser.parse_args()
    if args.source_dir is not None:
        args.source_dir = args.source_dir.resolve(strict=True)
    require(hasattr(os, "geteuid") and os.geteuid() != 0, "Run as a non-root POSIX user")
    original = args.packet_dir.resolve(strict=True)
    checker = Path(__file__).resolve().with_name("verify_independent.py")
    author = original / "verify_packet.py"
    require({p.name for p in original.iterdir()} == NAMES, "Original input inventory is not the seven-file packet")
    initial = snapshot(original)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    rows = []
    workspace = Path(tempfile.mkdtemp(prefix="boundary-zero-audit-"))
    work = workspace / "unrelated-working-directory"
    work.mkdir()
    work.chmod(0o555)
    case = workspace / "case"
    source_case = workspace / "source-case"
    source_initial = None
    if args.source_dir is not None:
        source_initial = {name: digest((args.source_dir / name).read_bytes()) for name in SOURCE_NAMES}

    def run(label, kind, packet=original, pin=PIN, expected=0, mode="normal", source=None, omit_pin=False):
        flags = [] if mode == "normal" else ["-" + mode]
        cmd = [sys.executable, "-B", *flags, str(author if kind == "author" else checker), "--packet-dir", str(packet)]
        if not omit_pin:
            cmd += ["--expected-manifest-sha256", pin]
        if source is not None:
            cmd += ["--source-dir", str(source)]
        proc = subprocess.run(cmd, cwd=work, env=env, text=True, capture_output=True, timeout=15)
        stdout = proc.stdout.strip()
        stderr = proc.stderr.strip()
        # Receipts do not expose dynamic temporary directories or private inputs.
        for path in (workspace, original, args.source_dir, checker.parent):
            if path is not None:
                stdout = stdout.replace(str(path), "<test-input>")
                stderr = stderr.replace(str(path), "<test-input>")
        row = {"test": label, "verifier": kind, "python_mode": mode,
               "expected_exit": expected, "actual_exit": proc.returncode,
               "passed": proc.returncode == expected, "stdout": stdout, "stderr": stderr}
        rows.append(row)
        require(row["passed"], "Unexpected outcome: " + label + " / " + kind + " / " + mode)
        if expected == 0:
            parsed = json.loads(proc.stdout)
            require(parsed.get("packet_integrity") == "PASS" and parsed.get("mathematical_proof_check") == "not_performed", "Unexpected success schema")

    def helper(label, entry, raw, expected=1, mode="normal", expected_error=None):
        code = """import json, runpy, sys
ns = runpy.run_path(sys.argv[1])
try:
    obj = ns['strict_json'](sys.stdin.read())
    if sys.argv[2] == 'manifest':
        ns['validate_manifest'](obj)
    elif sys.argv[2] == 'sources':
        ns['validate_sources'](obj)
except (ValueError, TypeError, KeyError) as error:
    print(str(error), file=sys.stderr)
    sys.exit(1)
print('HELPER_VALIDATION_PASS')
"""
        flags = [] if mode == "normal" else ["-" + mode]
        proc = subprocess.run([sys.executable, "-B", *flags, "-c", code, str(checker), entry],
                              input=raw, text=True, capture_output=True, cwd=work, env=env, timeout=15)
        passed = proc.returncode == expected and (expected_error is None or expected_error in proc.stderr)
        rows.append({"test": "direct_helper_" + label, "verifier": "independent", "python_mode": mode,
                     "expected_exit": expected, "actual_exit": proc.returncode, "passed": passed,
                     "expected_error_contains": expected_error,
                     "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip()})
        require(passed, "Unexpected direct-helper outcome: " + label + " / " + mode)

    def reset():
        writable_remove(case)
        shutil.copytree(original, case)
        for p in case.iterdir():
            p.chmod(0o644)
        return case

    def both(label, expected=1, pin=PIN, modes=("normal", "O", "OO"), source=None):
        for mode in modes:
            for kind in ("author", "independent"):
                run(label, kind, case, pin, expected, mode, source)

    try:
        # Authenticate all original bytes before executing its verifier.
        run("trusted_input_guard", "independent")
        for mode in ("normal", "O", "OO"):
            for kind in ("author", "independent"):
                run("intact_original", kind, mode=mode)
                run("missing_external_pin", kind, expected=2, mode=mode, omit_pin=True)
                run("wrong_external_pin", kind, pin="0" * 64, expected=1, mode=mode)
                run("uppercase_external_pin", kind, pin=PIN.upper(), expected=1, mode=mode)

        reset()
        for p in case.iterdir():
            p.chmod(0o444)
        case.chmod(0o555)
        blocked = 0
        for operation in (lambda: (case / "RESULT.json").open("ab"), lambda: (case / "new-file").open("wb")):
            try:
                operation().close()
            except PermissionError:
                blocked += 1
        require(blocked == 2, "Read-only fixture is writable")
        both("nonroot_readonly_packet_and_cwd", expected=0)
        case.chmod(0o755)

        for name in ("ACCEPTANCE_REPORT.md", "verify_packet.py", "MANIFEST.json"):
            reset()
            p = case / name
            data = bytearray(p.read_bytes())
            data[-1] ^= 1
            p.write_bytes(data)
            both("same_size_mutation_" + name)
        reset()
        p = case / "RESULT.json"
        p.write_bytes(p.read_bytes()[:-1])
        both("truncated_payload")
        reset()
        (case / "RESULT.json").unlink()
        both("missing_payload")
        for name, is_dir in (("extra.pdf", False), (".hidden", False), ("subdirectory", True)):
            reset()
            (case / name).mkdir() if is_dir else (case / name).write_text("synthetic test fixture\n")
            both("extra_" + name)
        reset()
        (case / "RESULT.json").unlink()
        (case / "RESULT.json").mkdir()
        both("payload_directory")
        for name in ("RESULT.json", "MANIFEST.json"):
            reset()
            (case / name).unlink()
            (case / name).symlink_to(original / name)
            for mode in ("normal", "O", "OO"):
                run("symlink_" + name, "author", case, expected=0 if name == "MANIFEST.json" else 1, mode=mode)
                run("symlink_" + name, "independent", case, expected=1, mode=mode)

        root_link = workspace / "packet-root-link"
        root_link.symlink_to(original, target_is_directory=True)
        for mode in ("normal", "O", "OO"):
            run("symlink_packet_root", "author", root_link, expected=0, mode=mode)
            run("symlink_packet_root", "independent", root_link, expected=1, mode=mode)
        root_link.unlink()

        # Direct trusted helper tests reach structural checks without weakening
        # the production interface's fixed pin or constructing a new release.
        base_manifest = json.loads((original / "MANIFEST.json").read_text())
        base_sources = json.loads((original / "SOURCES.json").read_text())
        helper_cases = [
            ("valid_manifest", "manifest", json.dumps(base_manifest), 0, None),
            ("valid_sources", "sources", json.dumps(base_sources), 0, None),
            ("finite_json_number", "json", '{"finite":1.25}', 0, None),
            ("duplicate_json_key", "json", '{"a":1,"a":2}', 1, "Duplicate JSON key"),
            ("nested_duplicate_key", "json", '{"x":{"a":1,"a":2}}', 1, "Duplicate JSON key"),
            ("nan", "json", '{"x":NaN}', 1, "Nonfinite JSON number"),
            ("infinity", "json", '{"x":Infinity}', 1, "Nonfinite JSON number"),
            ("negative_infinity", "json", '{"x":-Infinity}', 1, "Nonfinite JSON number"),
            ("overflow_number", "json", '{"x":1e999}', 1, "Nonfinite JSON number"),
            ("manifest_array", "manifest", '[]', 1, "Unexpected manifest schema fields"),
        ]
        manifest_changes = [
            ("boolean_schema", lambda m: m.update(schema=True), "Invalid manifest schema version"),
            ("float_schema", lambda m: m.update(schema=1.0), "Invalid manifest schema version"),
            ("boolean_problem_id", lambda m: m.update(problem_id=True), "Invalid manifest problem ID"),
            ("float_problem_id", lambda m: m.update(problem_id=2305029.0), "Invalid manifest problem ID"),
            ("extra_manifest_field", lambda m: m.update(extra=1), "Unexpected manifest schema fields"),
            ("empty_inventory", lambda m: m.update(files=[]), "Incomplete reviewed manifest inventory"),
            ("duplicate_filename", lambda m: m["files"].append(m["files"][0]), "Duplicate manifest member"),
            ("boolean_byte_count", lambda m: m["files"][0].update(bytes=True), "Invalid manifest byte count"),
            ("float_byte_count", lambda m: m["files"][0].update(bytes=6530.0), "Invalid manifest byte count"),
            ("negative_byte_count", lambda m: m["files"][0].update(bytes=-1), "Invalid manifest byte count"),
            ("unsafe_name", lambda m: m["files"][0].update(name="../outside"), "Invalid manifest member name"),
            ("uppercase_digest", lambda m: m["files"][0].update(sha256=m["files"][0]["sha256"].upper()), "Invalid manifest digest"),
            ("extra_row_field", lambda m: m["files"][0].update(extra=1), "Unexpected manifest row fields"),
            ("null_row", lambda m: m["files"].__setitem__(0,None), "Unexpected manifest row fields"),
        ]
        for label, change, message in manifest_changes:
            obj = json.loads(json.dumps(base_manifest)); change(obj)
            helper_cases.append((label, "manifest", json.dumps(obj), 1, message))
        source_changes = [
            ("source_boolean_schema", lambda m: m.update(schema=True), "Invalid source schema version"),
            ("source_boolean_bytes", lambda m: m["pdfs"][0].update(bytes=True), "Invalid source byte count"),
            ("source_float_bytes", lambda m: m["pdfs"][0].update(bytes=105706.0), "Invalid source byte count"),
            ("source_duplicate_name", lambda m: m["pdfs"].append(m["pdfs"][0]), "Invalid or duplicate source name"),
            ("source_unsafe_name", lambda m: m["pdfs"][0].update(filename="../outside.pdf"), "Invalid or duplicate source name"),
            ("source_missing_inventory", lambda m: m.update(pdfs=[]), "Incomplete reviewed source inventory"),
        ]
        for label, change, message in source_changes:
            obj = json.loads(json.dumps(base_sources)); change(obj)
            helper_cases.append((label, "sources", json.dumps(obj), 1, message))
        for label, entry, raw, expected, message in helper_cases:
            for mode in ("normal", "O", "OO"):
                helper(label, entry, raw, expected, mode, message)

        # A deliberately changed trusted pin is not an attack against the original
        # external-pin guarantee. These cases map parser and semantic boundaries.
        malformed = [
            ("invalid_json", b"{", 1),
            ("root_array", [], 1),
            ("missing_schema", lambda m: m.pop("schema"), 1),
            ("unsupported_schema", lambda m: m.update(schema=2), 1),
            ("duplicate_filename", lambda m: m["files"].append(m["files"][0]), 1),
            ("traversal_filename", lambda m: m["files"][0].update(name="../outside"), 1),
            ("absolute_filename", lambda m: m["files"][0].update(name="/outside"), 1),
            ("manifest_self_entry", lambda m: m["files"][0].update(name="MANIFEST.json"), 1),
            ("negative_byte_count", lambda m: m["files"][0].update(bytes=-1), 1),
            ("string_byte_count", lambda m: m["files"][0].update(bytes="6530"), 1),
            ("invalid_file_hash", lambda m: m["files"][0].update(sha256="not-a-hash"), 1),
            ("null_files", lambda m: m.update(files=None), 1),
            ("null_row", lambda m: m["files"].__setitem__(0, None), 1),
            ("boolean_schema", lambda m: m.update(schema=True), 0),
            ("wrong_problem_id", lambda m: m.update(problem_id=0), 0),
            ("missing_problem_id", lambda m: m.pop("problem_id"), 0),
        ]
        for label, mutate, author_expected in malformed:
            reset()
            manifest = json.loads((case / "MANIFEST.json").read_text())
            if isinstance(mutate, bytes):
                raw = mutate
            elif callable(mutate):
                mutate(manifest)
                raw = json.dumps(manifest).encode()
            else:
                raw = json.dumps(mutate).encode()
            (case / "MANIFEST.json").write_bytes(raw)
            new_pin = digest(raw)
            for mode in ("normal", "O", "OO"):
                run("repinned_" + label, "author", case, pin=new_pin, expected=author_expected, mode=mode)
                run("repinned_" + label, "independent", case, pin=new_pin, expected=1, mode=mode)
        reset()
        raw = (case / "MANIFEST.json").read_bytes().replace(b'"schema": 1,', b'"schema": 2, "schema": 1,')
        (case / "MANIFEST.json").write_bytes(raw)
        for mode in ("normal", "O", "OO"):
            run("repinned_duplicate_json_key", "author", case, pin=digest(raw), expected=0, mode=mode)
            run("repinned_duplicate_json_key", "independent", case, pin=digest(raw), expected=1, mode=mode)
        reset()
        for p in case.iterdir():
            p.unlink()
        raw = b'{"schema":1,"files":[]}'
        (case / "MANIFEST.json").write_bytes(raw)
        for mode in ("normal", "O", "OO"):
            run("repinned_empty_inventory", "author", case, pin=digest(raw), expected=0, mode=mode)
            run("repinned_empty_inventory", "independent", case, pin=digest(raw), expected=1, mode=mode)

        if args.source_dir is not None:
            for mode in ("normal", "O", "OO"):
                for kind in ("author", "independent"):
                    run("three_source_byte_identities", kind, source=args.source_dir, mode=mode)
            source_link = workspace / "source-root-link"
            source_link.symlink_to(args.source_dir, target_is_directory=True)
            for mode in ("normal", "O", "OO"):
                run("symlink_source_root", "author", source=source_link, expected=0, mode=mode)
                run("symlink_source_root", "independent", source=source_link, expected=1, mode=mode)
            source_link.unlink()
            for action in ("same_size_mutation", "truncation", "missing", "symlink"):
                writable_remove(source_case)
                source_case.mkdir()
                for name in SOURCE_NAMES:
                    shutil.copyfile(args.source_dir / name, source_case / name)
                p = source_case / "danielyan2016_published.pdf"
                if action == "same_size_mutation":
                    data = bytearray(p.read_bytes()); data[-1] ^= 1; p.write_bytes(data)
                elif action == "truncation":
                    p.write_bytes(p.read_bytes()[:-1])
                elif action == "missing":
                    p.unlink()
                else:
                    p.unlink(); p.symlink_to((args.source_dir / p.name).resolve())
                for mode in ("normal", "O", "OO"):
                    for kind in ("author", "independent"):
                        run("source_" + action, kind, source=source_case, expected=0 if action == "symlink" and kind == "author" else 1, mode=mode)
        require(snapshot(original) == initial, "Original packet changed")
        if source_initial is not None:
            require({name: digest((args.source_dir / name).read_bytes()) for name in SOURCE_NAMES} == source_initial, "Original source bytes changed")
        require(not list(work.iterdir()), "Verifier wrote to read-only working directory")
        print(json.dumps({"schema": 1, "problem_id": 2305029, "verdict": "PASS",
                          "python_version": platform.python_version(), "nonroot": True,
                          "readonly_write_probes_blocked": blocked,
                          "original_packet_unchanged": True, "source_inputs_unchanged": source_initial is not None,
                          "source_tests_run": source_initial is not None,
                          "tests": rows, "test_count": len(rows),
                          "scope": "Finite byte/inventory/parser controls only; no analytic theorem computation"}, indent=2))
    finally:
        work.chmod(0o755)
        writable_remove(workspace)


if __name__ == "__main__":
    main()
