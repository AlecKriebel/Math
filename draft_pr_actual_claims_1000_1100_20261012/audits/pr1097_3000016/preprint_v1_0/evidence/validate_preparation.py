#!/usr/bin/env python3
"""Preparation-only validation harness. Writes only this new preparation and its own scratch.

Not a supported distributed kit writer. No service or Git operation is performed.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import datetime
import hashlib
import io
import json
import os
import shutil
import subprocess
import tempfile
import zipfile

P = Path(__file__).resolve().parent.parent
R = P.parent
K = P / "kit"
E = P / "evidence"
PY = sys.executable
receipts = []

def need(q, msg):
    if not q:
        raise ValueError(msg)

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def pin(path):
    p = Path(path)
    return {"bytes": p.stat().st_size, "sha256": digest(p)}

def write(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")

def command(args, cwd, expect=0, label=None):
    run = subprocess.run([str(v) for v in args], cwd=cwd, capture_output=True, check=False)
    receipts.append({"label": label, "command": [str(v) for v in args], "cwd": str(cwd),
                     "exit": run.returncode, "stdout_bytes": len(run.stdout), "stderr_bytes": len(run.stderr),
                     "stdout_sha256": hashlib.sha256(run.stdout).hexdigest(),
                     "stderr_sha256": hashlib.sha256(run.stderr).hexdigest()})
    need((run.returncode == 0) if expect == 0 else (run.returncode != 0),
         "unexpected command result " + str(args) + ": " + run.stderr.decode(errors="replace"))
    return run

def scan(base):
    return {q.relative_to(base).as_posix(): pin(q) for q in sorted(base.rglob("*")) if q.is_file()}

def validate():
    base = json.loads((P / "INPUT_PINS.json").read_text())
    for row in base["entries"]:
        need(pin(R / row["path"]) == {"bytes": row["bytes"], "sha256": row["sha256"]}, "initial baseline mismatch")
    original_kit = scan(K)
    scratch = Path(tempfile.mkdtemp(prefix="pr1097-preparation-", dir="/private/tmp"))
    try:
        archive_path = scratch / "support.zip"
        command([PY, "-B", K / "scripts/verify.py"], P, label="canonical optional binding before construction")
        command([PY, "-B", K / "scripts/build_support.py", "--out", archive_path], P, label="initial actual builder")
        raw = archive_path.read_bytes()
        files = sorted(original_kit)
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            need(archive.namelist() == files and archive.testzip() is None and not archive.comment, "ZIP member/CRC list")
            for info in archive.infolist():
                need(info.date_time == (1980,1,1,0,0,0) and info.compress_type == zipfile.ZIP_STORED,
                     "ZIP timestamp/compression")
                need(info.create_system == 3 and info.external_attr == 0o100644 << 16 and not info.extra and not info.comment,
                     "ZIP header mode/extra/comment")
                need(archive.read(info.filename) == (K / info.filename).read_bytes(), "ZIP payload bytes")
        independently = io.BytesIO()
        with zipfile.ZipFile(independently, "w", compression=zipfile.ZIP_STORED) as archive:
            for name in files:
                info = zipfile.ZipInfo(name, (1980,1,1,0,0,0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                archive.writestr(info, (K / name).read_bytes())
        # Compare only after the archive writer has closed and written its directory.
        need(independently.getvalue() == raw, "independent CLOSED ZIP bytes")
        shutil.copyfile(archive_path, P / "pr1097_support_v1_0.zip")
        metadata = json.loads((K / "metadata.json").read_text())
        native = {"metadata": metadata, "files": [{"path": name, "name": name} for name in ("paper.pdf", "pr1097_support_v1_0.zip")]}
        write(P / "zenodo-deposit.json", native)
        binding = {"schema": 1, "metadata": metadata, "kit_manifest_sha256": digest(K / "MANIFEST.json"),
                   "files": [{"name": name, **pin(P / name)} for name in ("paper.pdf", "pr1097_support_v1_0.zip")],
                   "native_manifest": "zenodo-deposit.json"}
        write(P / "DEPOSIT_BINDING.json", binding)
        delivery = scratch / "delivery"
        delivery.mkdir()
        clean = delivery / "kit"
        clean.mkdir()
        with zipfile.ZipFile(archive_path) as archive:
            archive.extractall(clean)
        expected = json.loads((K / "EXPECTED_RESULTS.json").read_text())
        results = {}
        for optimized in (False, True):
            mode = "optimized" if optimized else "normal"
            flags = ["-O", "-B"] if optimized else ["-B"]
            prefix = [PY] + flags
            read = command(prefix + [clean / "scripts/verify.py"], clean, label=mode + " clean optional absent")
            need(json.loads(read.stdout)["binding"]["state"] == "ABSENT_OPTIONAL", "missing binding semantics")
            command(prefix + [clean / "scripts/verify.py", "--require-binding"], clean, expect=1, label=mode + " missing required")
            run = command(prefix + [clean / "scripts/run_checks.py"], clean, label=mode + " fresh exact proof controls")
            result = json.loads(run.stdout)
            need(result == expected, "full exact result mismatch")
            write(E / ("CHECK_" + mode.upper() + ".json"), result)
            results[mode] = result
            command(prefix + [clean / "scripts/run_checks.py", "--inject-failure"], clean, expect=1, label=mode + " unconditional fault")
            rebuilt = scratch / (mode + ".zip")
            command(prefix + [clean / "scripts/build_support.py", "--out", rebuilt], clean, label=mode + " clean actual ZIP rebuild")
            need(rebuilt.read_bytes() == raw, "clean ZIP determinism")
            compile_run = command(prefix + [clean / "scripts/rebuild_pdf.py", "--out-dir", scratch / ("pdf-" + mode)],
                                  clean, label=mode + " actual clean PDF regeneration")
            compile_value = json.loads(compile_run.stdout)
            need(compile_value["matches_distributed_pdf"], "actual clean PDF byte mismatch")
        need(results["normal"] == results["optimized"], "optimized result mismatch")
        for name in ("paper.pdf", "pr1097_support_v1_0.zip", ".zenodo.json", "zenodo-metadata.json", "zenodo-deposit.json", "DEPOSIT_BINDING.json"):
            shutil.copyfile(P / name, delivery / name)
        alias_tests = []
        for optimized in (False, True):
            mode = "optimized" if optimized else "normal"
            prefix = [PY] + (["-O", "-B"] if optimized else ["-B"])
            for args in ([], ["--require-binding"], ["--binding", delivery / "DEPOSIT_BINDING.json", "--require-binding"]):
                out = command(prefix + [clean / "scripts/verify.py"] + args, clean, label=mode + " present delivery " + repr(args))
                need(json.loads(out.stdout)["binding"]["state"] == "PRESENT_VERIFIED", "present binding not checked")
            canonical = [R / "submitted/MATHEMATICAL_REPORT.md", P / "paper.pdf", P / "zenodo-deposit.json", P / "DEPOSIT_BINDING.json", clean / "paper.tex"]
            # Every existing output leaf is rejected, including hardlinks to original,
            # canonical paper and external upload descriptors.
            for i, target in enumerate(canonical):
                alias = scratch / (mode + "-hard-" + str(i))
                os.link(target, alias)
                before = pin(target)
                command(prefix + [clean / "scripts/build_support.py", "--out", alias], clean, expect=1,
                        label=mode + " hardlink output protected target " + str(target))
                command(prefix + [clean / "scripts/rebuild_pdf.py", "--out-dir", alias], clean, expect=1,
                        label=mode + " PDF hardlink/existing leaf " + str(target))
                need(pin(target) == before, "protected hardlink target mutated")
                alias.unlink()
                alias_tests.append({"mode": mode, "kind": "hardlink_existing_leaf", "target": str(target), "unchanged": True})
            symlink = scratch / (mode + "-leaf-link")
            symlink.symlink_to(clean / "paper.tex")
            command(prefix + [clean / "scripts/build_support.py", "--out", symlink], clean, expect=1, label=mode + " leaf symlink")
            symlink.unlink()
            parent_link = scratch / (mode + "-ancestor-link")
            parent_link.symlink_to(clean, target_is_directory=True)
            for script, option, dest in (("build_support.py", "--out", parent_link / "new.zip"),
                                         ("rebuild_pdf.py", "--out-dir", parent_link / "new-pdf"),
                                         ("build_support.py", "--out", clean / "nested-new.zip"),
                                         ("rebuild_pdf.py", "--out-dir", clean / "nested-new-pdf"),
                                         ("build_support.py", "--out", R / "original-new.zip"),
                                         ("rebuild_pdf.py", "--out-dir", R / "original-new-pdf")):
                command(prefix + [clean / "scripts" / script, option, dest], clean, expect=1, label=mode + " ancestor/nested preflight")
                need(not os.path.lexists(dest), "rejected writer created a path")
            parent_link.unlink()
            existing = scratch / (mode + "-existing-compiler-dir")
            existing.mkdir()
            for name in ("paper.tex", "paper.pdf", "compile.stdout.txt", "compile.stderr.txt", "paper.log"):
                os.link(P / "paper.pdf", existing / name)
            before = pin(P / "paper.pdf")
            command(prefix + [clean / "scripts/rebuild_pdf.py", "--out-dir", existing], clean, expect=1,
                    label=mode + " existing compiler child stdout/log/PDF aliases")
            need(pin(P / "paper.pdf") == before, "compiler child alias mutated canonical PDF")
            for script in ("run_checks.py", "verify.py"):
                command(prefix + [clean / "scripts" / script, "--out", P / "paper.pdf"], clean, expect=1,
                        label=mode + " no unsupported file writer option")
            # Identical-byte manifest symlink must fail BEFORE parsing/bootstrap;
            # both builders must also fail without opening their output.
            manifest = clean / "MANIFEST.json"
            saved = manifest.read_bytes()
            original = scratch / (mode + "-same-manifest.json")
            original.write_bytes(saved)
            manifest.unlink()
            manifest.symlink_to(original)
            for script, args in (("verify.py", []), ("build_support.py", ["--out", scratch / (mode + "-forbidden.zip")]),
                                 ("rebuild_pdf.py", ["--out-dir", scratch / (mode + "-forbidden-pdf")])):
                command(prefix + [clean / "scripts" / script] + args, clean, expect=1, label=mode + " identical manifest symlink")
            need(not (scratch / (mode + "-forbidden.zip")).exists() and not (scratch / (mode + "-forbidden-pdf")).exists(),
                 "bootstrap rejection wrote output")
            manifest.unlink()
            manifest.write_bytes(saved)
            # A present descriptor is always checked; no silent fallback to absent mode.
            bp = delivery / "DEPOSIT_BINDING.json"
            saved = bp.read_bytes()
            bad = json.loads(saved)
            bad["metadata"]["title"] += " invalid"
            write(bp, bad)
            command(prefix + [clean / "scripts/verify.py"], clean, expect=1, label=mode + " present invalid binding")
            bp.write_bytes(saved)
            bp.rename(delivery / "binding-regular.json")
            bp.symlink_to(delivery / "binding-regular.json")
            command(prefix + [clean / "scripts/verify.py"], clean, expect=1, label=mode + " present binding symlink")
            bp.unlink()
            (delivery / "binding-regular.json").rename(bp)
            command(prefix + [clean / "scripts/verify.py", "--require-binding"], clean, label=mode + " final restored strict delivery")
        repo = R.parents[2]
        local = command([PY, "-B", repo / "zenodo_deposit_tool/zenodo.py", "check", P / "zenodo-deposit.json"], repo,
                        label="actual repository entirely LOCAL native uploader check")
        (E / "REPOSITORY_TOOL_LOCAL_CHECK.stdout.json").write_bytes(local.stdout)
        need(scan(K) == original_kit and scan(clean) == original_kit, "kit or clean extraction mutated")
        for row in base["entries"]:
            need(pin(R / row["path"]) == {"bytes": row["bytes"], "sha256": row["sha256"]}, "final original baseline mutation")
        summary = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "status": "PASS",
                   "actual_commands": len(receipts), "expected_rejections": sum(r["exit"] != 0 for r in receipts),
                   "baseline_unchanged": len(base["entries"]), "kit_files_unchanged": len(original_kit),
                   "exact_results_normal_optimized": True, "real_clean_PDF_regeneration_both_modes_byte_equal": True,
                   "independent_CLOSED_ZIP_every_member_header_payload_CRC": True, "ZIP_members": len(files),
                   "archive": pin(P / "pr1097_support_v1_0.zip"), "paper": pin(P / "paper.pdf"),
                   "hardlink_alias_targets_unchanged": alias_tests, "services_or_git_actions": False,
                   "fresh_whole_package_reviews_of_new_edition": 0, "publication_ready": False,
                   "ordered_service_hold_pr": 1032}
        write(E / "FINAL_VERIFICATION.json", summary)
        return summary
    finally:
        write(E / "COMMAND_RECEIPTS.json", {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "entries": receipts})
        shutil.rmtree(scratch)

if __name__ == "__main__":
    print(json.dumps(validate(), sort_keys=True))
