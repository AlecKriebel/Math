#!/usr/bin/env python3
"""Bounded, reproducible prewrite controls in one disposable extraction."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent


def require(test, message):
    if not test:
        raise RuntimeError(message)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def pins(paths):
    return {str(p): sha(p) for p in paths}


def main():
    observations = []
    with tempfile.TemporaryDirectory(prefix="pr1080-output-guards-") as temp:
        base = Path(temp).resolve()
        kit = base / "verification_kit"
        shutil.copytree(ROOT, kit)
        outside = base / "outside"
        outside.mkdir()
        extra = []
        for name in ["preprint.pdf", "preprint.tex", "deposit_metadata.json", "metadata.json", "EXTERNAL_BINDING.json", "sentinel.txt"]:
            p = outside / name
            p.write_text("protected external-like input " + name + "\n")
            extra.append(p)
        protected = sorted(p for p in kit.rglob("*") if p.is_file()) + extra
        expected = pins(protected)
        positive_hashes = []
        for optimized in [False, True]:
            prefix = [sys.executable, "-I", "-B"] + (["-O"] if optimized else [])

            def command(dest, script_root=kit):
                return subprocess.run(prefix + [str(script_root / "build_archive.py"), "--output", str(dest)],
                                      capture_output=True, text=True, timeout=120)

            def reject(kind, dest, cleanup=None, script_root=kit):
                result = command(dest, script_root)
                require(result.returncode != 0, "output fault accepted: " + kind)
                require("archive" in result.stderr, "unexpected rejection reason: " + kind)
                require(pins(protected) == expected, "protected input/sentinel changed: " + kind)
                observations.append({"fault": kind, "optimized": optimized, "returncode": result.returncode,
                                     "all_protected_bytes_unchanged": True})
                if cleanup:
                    cleanup()

            for index, target in enumerate(protected):
                alias = outside / "hardlink-output.zip"
                os.link(target, alias)
                reject("hardlink:" + str(target.relative_to(base)), alias, alias.unlink)
            reject("direct-kit-file", kit / "preprint.tex")
            reject("protected-descendant", kit / "originals/submitted/new-output.zip")
            reject("external-file-descendant", outside / "preprint.pdf/new-output.zip")
            reject("existing-independent-sentinel", outside / "sentinel.txt")
            leaf = outside / "leaf-symlink.zip"
            leaf.symlink_to(outside / "sentinel.txt")
            reject("outside-leaf-symlink", leaf, leaf.unlink)
            leaf.symlink_to(outside / "absent-target.zip")
            reject("dangling-leaf-symlink", leaf, leaf.unlink)
            ancestor = base / "ancestor-alias"
            ancestor.symlink_to(outside, target_is_directory=True)
            reject("ancestor-alias-fresh", ancestor / "fresh-output.zip")
            alias = outside / "hardlink-output.zip"
            os.link(kit / "preprint.tex", alias)
            reject("ancestor-alias-hardlink", ancestor / alias.name, alias.unlink)
            # Do not normalize away the aliased component before checking it.
            reject("ancestor-alias-dotdot", ancestor / ".." / "fresh-output.zip")
            ancestor.unlink()
            case_kit = kit.with_name(kit.name.swapcase())
            case_available = case_kit.exists() and case_kit.samefile(kit)
            if case_available:
                for kind, dest, script_root in [
                    ("physical-case-root", case_kit / "fresh-case.zip", kit),
                    ("physical-case-nested", case_kit / "originals" / "fresh-case.zip", kit),
                    ("physical-case-absent-parent", case_kit / "absent-parent" / "fresh-case.zip", kit),
                    ("physical-case-traversal", case_kit / "originals" / ".." / "fresh-case.zip", kit),
                    ("physical-case-reverse-root", kit / "fresh-case.zip", case_kit),
                    ("physical-case-reverse-absent-parent", kit / "absent-parent" / "fresh-case.zip", case_kit),
                ]:
                    reject(kind, dest, script_root=script_root)
                    require(not dest.exists(), "rejected physical case output was created")
                require(not (kit / "absent-parent").exists(), "rejected absent parent was created")
            observations.append({"control": "physical-case-alias-availability", "optimized": optimized,
                                 "same_physical_directory": case_available})
            dest = outside / ("fresh-optimized.zip" if optimized else "fresh-normal.zip")
            result = command(dest)
            require(result.returncode == 0, "fresh outside rebuild failed: " + result.stderr)
            positive_hashes.append(sha(dest))
            require(pins(protected) == expected, "positive rebuild changed protected inputs")
            dest.unlink()
            case_outside = outside.with_name(outside.name.swapcase())
            if case_outside.exists() and case_outside.samefile(outside):
                dest = case_outside / "fresh-case-outside.zip"
                result = command(dest)
                require(result.returncode == 0, "fresh physical outside case rebuild failed: " + result.stderr)
                positive_hashes.append(sha(dest))
                require(pins(protected) == expected, "case outside rebuild changed protected inputs")
                dest.unlink()
        require(len(set(positive_hashes)) == 1, "normal/optimized archives differ")
    print(json.dumps({"status": "PASS", "rejections": observations,
                      "rejection_count": sum("fault" in r for r in observations), "protected_file_count": len(protected),
                      "positive_normal_optimized_archive_sha256": positive_hashes,
                      "scope": "Concrete CLI prewrite controls; no mathematical theorem or concurrency-lock certification."}, indent=2))


if __name__ == "__main__":
    main()
