#!/usr/bin/env python3
"""Actual dated-metadata successor controls; no compilation or canonical mutations."""
import hashlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

AUDIT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
DELIVERY = AUDIT / "preprint_v1_0"
REPO = AUDIT.parents[2]
RECEIPTS = WORK / "REPRODUCTION_RECEIPTS.jsonl"


def require(test, message):
    if not test:
        raise RuntimeError(message)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def capture(argv, cwd, expected=0):
    r = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=300)
    row = {"argv": [str(x) for x in argv], "cwd": str(cwd), "returncode": r.returncode,
           "stdout": r.stdout, "stderr": r.stderr, "expected": expected}
    with RECEIPTS.open("a") as stream:
        stream.write(json.dumps(row) + "\n")
    require(r.returncode == expected if expected == 0 else r.returncode != 0, "unexpected command outcome: " + str(argv) + r.stderr)
    return r


def main():
    require(not RECEIPTS.exists(), "Refuse silently replacing execution receipts")
    initial = {p.relative_to(AUDIT).as_posix(): sha(p) for p in AUDIT.rglob("*")
               if p.is_file() and not p.is_relative_to(WORK)}
    (WORK / "tmp").mkdir(exist_ok=True)
    positives = []
    with tempfile.TemporaryDirectory(prefix="clean-", dir=WORK / "tmp") as temp:
        base = Path(temp)
        with zipfile.ZipFile(DELIVERY / "verification_kit.zip") as archive:
            archive.extractall(base)
        kit = base / "verification_kit"
        names = json.loads((kit / "ALLOWLIST.json").read_text())["members"]
        # Independent reconstruction uses a separate closed ZipFile, not builder.
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_STORED) as z:
            for name in names:
                zi = zipfile.ZipInfo("verification_kit/" + name, (2026, 10, 14, 0, 0, 0))
                zi.create_system = 3
                zi.external_attr = 0o100644 << 16
                zi.compress_type = zipfile.ZIP_STORED
                zi.flag_bits = 0
                z.writestr(zi, (kit / name).read_bytes())
        require(buf.getvalue() == (DELIVERY / "verification_kit.zip").read_bytes(), "independent closed ZIP differs")
        headers = []
        with zipfile.ZipFile(DELIVERY / "verification_kit.zip") as z:
            require(z.testzip() is None and z.comment == b"", "ZIP CRC/comment")
            require(z.namelist() == ["verification_kit/" + n for n in names], "ZIP order")
            for info in z.infolist():
                require(info.date_time == (2026, 10, 14, 0, 0, 0) and info.create_system == 3
                        and info.external_attr == 0o100644 << 16 and info.compress_type == zipfile.ZIP_STORED
                        and not info.extra and not info.comment and not info.is_dir(), "ZIP member headers")
                headers.append({"path": info.filename, "bytes": info.file_size,
                                "sha256": hashlib.sha256(z.read(info)).hexdigest()})
        for optimized in [False, True]:
            prefix = [sys.executable, "-I", "-B"] + (["-O"] if optimized else [])
            capture(prefix + ["verify.py"], kit)
            r = capture(prefix + ["run_checks.py"], kit)
            positives.append(json.loads(r.stdout))
            capture(prefix + ["fault_checks.py"], kit)
            guards = capture(prefix + ["output_guard_checks.py"], kit)
            guard = json.loads(guards.stdout)
            require(guard["status"] == "PASS" and guard["rejection_count"] == 386, "output fault count differs")
            out = base / "rebuilt.zip"
            capture(prefix + ["build_archive.py", "--output", str(out)], kit)
            capture(["cmp", str(out), str(DELIVERY / "verification_kit.zip")], base)
            capture(prefix + ["verify.py", "--require-binding", "--binding", str(DELIVERY / "EXTERNAL_BINDING.json"),
                              "--pdf", str(DELIVERY / "preprint.pdf"), "--archive", str(out)], kit)
            out.unlink()
            capture(prefix + ["verify.py", "--require-binding"], kit, expected=1)
            # Concrete bootstrap preflight faults leave all original evidence
            # unchanged. No coherent manifest refresh is performed or claimed.
            for name in ["ALLOWLIST.json", "MANIFEST.json"]:
                p = kit / name
                saved = p.read_bytes()
                target = base / "bootstrap-identical.json"
                target.write_bytes(saved)
                p.unlink()
                p.symlink_to(target)
                capture(prefix + ["verify.py"], kit, expected=1)
                capture(prefix + ["build_archive.py", "--output", str(base / "not-created.zip")], kit, expected=1)
                require(not (base / "not-created.zip").exists(), "bootstrap fault created output")
                p.unlink()
                p.write_bytes(saved)
                target.unlink()
            # Binding is strict for altered external uploader metadata.
            mirror = base / "delivery-mirror"
            mirror.mkdir()
            for name in ["EXTERNAL_BINDING.json", "metadata.json", "research_metadata.json", "CURRENT_STATUS_REPAIR01.json", "deposit_metadata.json", "preprint.tex", "README.md"]:
                shutil.copyfile(DELIVERY / name, mirror / name)
            wrapper = mirror / "deposit_metadata.json"
            data = json.loads(wrapper.read_text())
            data["metadata"]["title"] += " fault"
            wrapper.write_text(json.dumps(data))
            capture(prefix + ["verify.py", "--binding", str(mirror / "EXTERNAL_BINDING.json"),
                              "--pdf", str(DELIVERY / "preprint.pdf"), "--archive", str(DELIVERY / "verification_kit.zip")], kit, expected=1)
            shutil.rmtree(mirror)
        require(positives[0] == positives[1], "complete normal/optimized positive JSON differs")
        native = capture([sys.executable, "-B", str(REPO / "zenodo_deposit_tool/zenodo.py"), "check", str(DELIVERY / "deposit_metadata.json")], REPO)
        (WORK / "REPOSITORY_LOCAL_CHECK.json").write_text(native.stdout)
        summary = {"status": "PASS", "archive_members": len(names), "independent_closed_rebuild_byte_exact": True,
                   "zip_headers_payload_crcs_checked": True, "archive_sha256": sha(DELIVERY / "verification_kit.zip"),
                   "normal_optimized_full_check_json_equal": True, "guard_script_rejections_each_invocation": 386,
                   "guard_script_invocations": 2, "commands": sum(1 for _ in RECEIPTS.open()),
                   "paper_unchanged": True, "actual_current_compilation": False, "new_page_views": False,
                   "local_uploader_check_only": True, "published": False, "publication_ready": False,
                   "whole_reviews_completed": 1, "minimum_whole_reviews": 2}
        (WORK / "ARCHIVE_PAYLOAD_CHECKS.json").write_text(json.dumps({"headers_and_payloads": headers}, indent=2) + "\n")
    final = {p.relative_to(AUDIT).as_posix(): sha(p) for p in AUDIT.rglob("*")
             if p.is_file() and not p.is_relative_to(WORK)}
    require(initial == final, "Reproduction mutated canonical audit files")
    summary["canonical_inputs_unchanged_during_reproduction"] = len(initial)
    (WORK / "REPRODUCTION_SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
