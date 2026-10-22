#!/usr/bin/env python3
"""Reproduce the acceptance gate's positive and negative controls.

Usage: python -I -B test_controls.py AUTHOR_PUBLIC_DIR AUTHOR_FROZEN_ZIP
All mutations are temporary copies; the original packet is never edited.
"""
import argparse
import json
import pathlib
import runpy
import shutil
import stat
import subprocess
import sys
import tempfile
import warnings
import zipfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("author_directory", type=pathlib.Path)
    parser.add_argument("author_zip", type=pathlib.Path)
    args = parser.parse_args()
    root = pathlib.Path(__file__).resolve().parent
    gate = runpy.run_path(str(root / "verify_audit.py"))
    baseline = json.loads((root / "AUTHOR_BASELINE.json").read_text())
    cases = {}

    def case(name, operation, rejected):
        try:
            operation()
            actual_rejected = False
        except RuntimeError:
            actual_rejected = True
        if actual_rejected != rejected:
            raise RuntimeError("Unexpected control outcome: " + name)
        cases[name] = {"rejected": actual_rejected, "expected_rejection": rejected, "result": "PASS"}

    check_dir = gate["check_directory"]
    check_zip = gate["check_zip"]
    case("original_directory", lambda: check_dir(args.author_directory, baseline["files"]), False)
    case("original_zip", lambda: check_zip(args.author_zip, baseline["zip"], baseline["files"]), False)

    with tempfile.TemporaryDirectory(prefix="gradient-audit-controls-") as td:
        temp = pathlib.Path(td)
        def copy_case(name, mutate):
            target = temp / name
            shutil.copytree(args.author_directory, target)
            mutate(target)
            case(name, lambda: check_dir(target, baseline["files"]), True)

        copy_case("changed_report", lambda p: (p / "REPORT.md").write_bytes((p / "REPORT.md").read_bytes() + b"\ncontrol mutation\n"))
        copy_case("changed_manifest", lambda p: (p / "AUTHOR_MANIFEST.json").write_bytes((p / "AUTHOR_MANIFEST.json").read_bytes() + b" \n"))
        copy_case("extra_regular_file", lambda p: (p / "extra.txt").write_text("control"))
        copy_case("extra_empty_directory", lambda p: (p / "extra").mkdir())
        def populated(p):
            (p / "extra").mkdir()
            (p / "extra" / "private.txt").write_text("synthetic control, no private data")
        copy_case("extra_populated_directory", populated)
        def symlink(p):
            target = p / "REPORT.md"
            target.unlink()
            target.symlink_to(args.author_directory.resolve() / "REPORT.md")
        copy_case("same_byte_symlink_substitution", symlink)
        mutated_zip = temp / "mutated.zip"
        mutated_zip.write_bytes(args.author_zip.read_bytes() + b"trailing control bytes")
        case("changed_zip_bytes", lambda: check_zip(mutated_zip, baseline["zip"], baseline["files"]), True)

        # Re-pin synthetic ZIP bytes to exercise membership/type checks separately
        # from the outer fingerprint. This never authorizes changing the baseline.
        def zip_case(name, mutate):
            target = temp / (name + ".zip")
            shutil.copyfile(args.author_zip, target)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                with zipfile.ZipFile(target, "a") as z:
                    mutate(z)
            synthetic_digest = gate["digest"](target.read_bytes())
            case(name, lambda: check_zip(target, synthetic_digest, baseline["files"]), True)
        zip_case("zip_nested_extra_member", lambda z: z.writestr("extra/control.txt", "synthetic"))
        zip_case("zip_extra_directory_member", lambda z: z.writestr("extra/", ""))
        zip_case("zip_duplicate_member", lambda z: z.writestr("REPORT.md", (args.author_directory / "REPORT.md").read_bytes()))
        zip_case("zip_traversal_member", lambda z: z.writestr("../control.txt", "synthetic"))
        def comment(z):
            z.comment = b"synthetic control"
        zip_case("zip_unexpected_comment", comment)
        symlink_zip = temp / "zip_symlink_member.zip"
        with zipfile.ZipFile(args.author_zip) as source, zipfile.ZipFile(symlink_zip, "w") as dest:
            for info in source.infolist():
                if info.filename == "REPORT.md":
                    info.create_system = 3
                    info.external_attr = (stat.S_IFLNK | 0o777) << 16
                dest.writestr(info, source.read(info.filename))
        synthetic_digest = gate["digest"](symlink_zip.read_bytes())
        case("zip_same_byte_symlink_member", lambda: check_zip(symlink_zip, synthetic_digest, baseline["files"]), True)

        # Mutation of an actual witness value must fail even with assertions disabled.
        mutations = [
            ("independent_witness", root / "verify_independent.py", "-Q(309,10000)", "-Q(308,10000)"),
            ("author_witness", args.author_directory / "verify_exact.py", "-s.Rational(309,10000)", "-s.Rational(308,10000)")]
        for label, source, old, new in mutations:
            code = source.read_text()
            if code.count(old) != 1:
                raise RuntimeError("Mutation target not unique: " + label)
            script = temp / (label + ".py")
            script.write_text(code.replace(old, new))
            for optimized in (False, True):
                command = [sys.executable, "-I", "-B"] + (["-O"] if optimized else []) + [str(script)]
                result = subprocess.run(command, cwd=temp, text=True, capture_output=True)
                expected_message = "FAILED: parity exact negative witness"
                if result.returncode == 0 or expected_message not in result.stderr:
                    raise RuntimeError("Witness mutation did not fail as expected")
                cases[label + ("_optimized" if optimized else "_normal")] = {
                    "rejected": True, "expected_rejection": True,
                    "exit_code": result.returncode, "result": "PASS"}

    print(json.dumps({"result": "PASS", "cases": cases, "total_cases": len(cases),
                      "original_bytes_changed": False,
                      "scope": "Synthetic integrity and algebra negative controls; not mathematical counterexamples."},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
