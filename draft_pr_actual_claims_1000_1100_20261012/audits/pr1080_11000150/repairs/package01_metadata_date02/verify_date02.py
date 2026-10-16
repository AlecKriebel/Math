#!/usr/bin/env python3
"""Check complete current/before/history custody for the dated notes successor."""
import collections
import difflib
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
WORK = Path(__file__).resolve().parent
AUDIT = WORK.parents[1]
OLD = AUDIT / "repairs/package01"
DELIVERY = AUDIT / "preprint_v1_0"
KIT = DELIVERY / "verification_kit"


def require(test, message):
    if not test:
        raise RuntimeError(message)


def obj(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row(path, root):
    return {"path": path.relative_to(root).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path)}


def matches(path, record):
    return path.is_file() and not path.is_symlink() and path.stat().st_size == record["bytes"] and sha(path) == record["sha256"]


def dump(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def main():
    require(not (WORK / "TERMINAL_SEAL.json").exists(), "No automatic sealed-stage rewrite")
    baseline = obj(WORK / "IMMEDIATE_INPUT_PINS.json")["files"]
    before = {r["original_path"]: r for r in obj(WORK / "BEFORE_COPIES.json")["files"]}
    current = {p.relative_to(AUDIT).as_posix(): p for p in AUDIT.rglob("*") if p.is_file() and not p.is_relative_to(WORK)}
    protected = []
    changed = []
    for r in baseline:
        name = r["path"]
        require(name in current, "Missing immediate input")
        if matches(current[name], r):
            protected.append(r)
        else:
            require(name in before, "Unauthorized change: " + name)
            b = before[name]
            require((b["bytes"], b["sha256"]) == (r["bytes"], r["sha256"]), "Before record differs")
            require(matches(AUDIT / b["source_snapshot"], b) and matches(KIT / b["destination"], b), "Exact before copies differ")
            changed.append({"path": name, "before": r, "after": row(current[name], AUDIT), "source_snapshot": b["source_snapshot"], "destination": b["destination"]})
    new = sorted(set(current) - {r["path"] for r in baseline})
    require((len(baseline), len(changed), len(protected), len(new), len(current)) == (404, 11, 393, 57, 461), "Current accounting differs")
    require(set(before) == {r["path"] for r in changed}, "Changed set differs from captured before set")
    dump(WORK / "CHANGE_ACCOUNTING.json", {"baseline_count": 404, "changed_count": 11, "unchanged_count": 393, "new_count": 57, "current_count": 461, "changes": changed, "new_files": [row(current[n], AUDIT) for n in new]})
    dump(WORK / "PROTECTED_INPUT_PINS.json", {"scope": "All 393 unchanged immediate files, including every prior repair01 output/seal, paper/source and current executable.", "files": protected})
    dump(WORK / "CURRENT_INPUT_PINS.json", {"scope": "Current complete audit outside this administrative workspace; historical inventories are not rewritten.", "files": [row(current[n], AUDIT) for n in sorted(current)]})
    old_outputs = obj(OLD / "OUTPUT_PINS.json")["files"]
    require(len(old_outputs) == 42 and sha(OLD / "OUTPUT_PINS.json") == "8b5444acd30147e16af62d52067d2ef1395eed1e27f01b3c6ce9da0c5d47306a" and sha(OLD / "TERMINAL_SEAL.json") == "e5978cb4ddc9e41d7c00e54543085e6f5a862593b1bfb5df0f2b08950a85462b", "Prior sealed stage differs")
    for r in old_outputs:
        require(matches(OLD / r["path"], r), "Prior sealed output differs")
    previous_native = obj(WORK / "before/preprint_v1_0/metadata.json")
    native = obj(DELIVERY / "metadata.json")
    wrapper = obj(DELIVERY / "deposit_metadata.json")
    require((DELIVERY / "metadata.json").read_bytes() == (KIT / "metadata.json").read_bytes(), "Native bare copies differ")
    require(set(wrapper) == {"metadata", "files"} and wrapper["metadata"] == native and wrapper["files"] == obj(WORK / "before/preprint_v1_0/deposit_metadata.json")["files"], "Native wrapper differs")
    require({k: v for k, v in native.items() if k != "notes"} == {k: v for k, v in previous_native.items() if k != "notes"}, "Non-note native field changed")
    expected_notes = ("Prepared locally on 2026-10-14 before deposit or publication. At the bounded-repair checkpoint on 2026-10-14, one complete whole-candidate review had been completed, a fresh complete second review was required, and publication readiness had not yet been affirmed. Later readiness/publication state is recorded separately.")
    require(native["notes"] == expected_notes and previous_native["notes"] != expected_notes, "Dated historical notes differ")
    stage = obj(KIT / "METADATA_DATE02_ADMIN_STAGE.json")
    require(stage["native_notes"] == expected_notes and stage["whole_reviews_completed"] == 1 and stage["minimum_whole_reviews"] == 2 and stage["fresh_whole02_required"] and not stage["publication_ready"] and not stage["published"] and stage["services_held_at"] == 1032, "Administrative stage flags differ")
    copies = obj(KIT / "REPAIR01_STAGE_COPIES.json")["files"]
    previous_copies = obj(WORK / "before/preprint_v1_0/verification_kit/REPAIR01_STAGE_COPIES.json")["files"]
    new_copies = obj(WORK / "NEW_COPY_ROWS.json")["files"]
    require(len(copies) == 100 and copies[:44] == previous_copies and copies[44:] == new_copies and len(new_copies) == 56, "Captured copy prefix/append differs")
    for r in copies:
        require(matches(AUDIT / r["source_snapshot"], r) and matches(KIT / r["destination"], r), "Exact stage source/copy differs")
    history = obj(KIT / "REPAIR01_HISTORY_RESOLUTION.json")
    previous_history = obj(WORK / "before/preprint_v1_0/verification_kit/REPAIR01_HISTORY_RESOLUTION.json")
    require(history["references"][:899] == previous_history["references"] and len(history["references"]) == 2312, "Previous reference rows changed")
    prefixes = {"immediate-before-repair01": "", "preparation-input194": "", "preparation-output90": "preprint_v1_0/", "whole01-input289": "", "whole01-output17": "reviews/package_01/", "metadata-date02-immediate404": "", "repair01-current360": "", "repair01-protected298": "", "repair01-output42": "repairs/package01/", "repair01-immediate309": ""}
    groups = collections.defaultdict(list)
    for r in history["references"]:
        groups[r["stage"]].append(r)
        if r["disposition"] == "exact_captured_stage_or_canonical_copy":
            require(matches(KIT / r["destination"], r), "History destination differs")
        else:
            require(r["disposition"] == "omitted" and bool(r["reason"]), "Missing individual omission")
    require(set(groups) == set(prefixes), "History stage set differs")
    history_counts = {}
    for name, refs in groups.items():
        source = obj(AUDIT / refs[0]["inventory"])["files"]
        require([(prefixes[name] + r["path"], r["bytes"], r["sha256"]) for r in source] == [(r["original_path"], r["bytes"], r["sha256"]) for r in refs] and len(refs) == history["inventory_counts"][name], "Exact historical inventory mismatch: " + name)
        history_counts[name] = dict(collections.Counter(r["disposition"] for r in refs))
    names = obj(KIT / "ALLOWLIST.json")["members"]
    require(len(names) == 178 and len(obj(KIT / "MANIFEST.json")["files"]) == 177, "Payload counts differ")
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_STORED) as z:
        for name in names:
            record = zipfile.ZipInfo("verification_kit/" + name, (2026, 10, 14, 0, 0, 0))
            record.create_system = 3
            record.external_attr = 0o100644 << 16
            record.compress_type = zipfile.ZIP_STORED
            z.writestr(record, (KIT / name).read_bytes())
    require(buf.getvalue() == (DELIVERY / "verification_kit.zip").read_bytes(), "Independent closed archive differs")
    saved = obj(WORK / "ARCHIVE_PAYLOAD_CHECKS.json")["headers_and_payloads"]
    with zipfile.ZipFile(DELIVERY / "verification_kit.zip") as z:
        require(z.namelist() == ["verification_kit/" + n for n in names] and z.testzip() is None and not z.comment, "Archive order/CRC")
        actual = []
        for info in z.infolist():
            require(info.date_time == (2026, 10, 14, 0, 0, 0) and info.create_system == 3 and info.external_attr == 0o100644 << 16 and info.compress_type == zipfile.ZIP_STORED and not info.extra and not info.comment and not info.is_dir(), "Archive header")
            body = z.read(info)
            require(body == (KIT / info.filename.removeprefix("verification_kit/")).read_bytes(), "Archive/source mismatch")
            actual.append({"path": info.filename, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()})
        require(actual == saved, "Actual reproduction payloads differ")
    receipts = [json.loads(line) for line in (WORK / "REPRODUCTION_RECEIPTS.jsonl").read_text().splitlines()]
    require(len(receipts) == 27 and all(r["returncode"] == 0 if r["expected"] == 0 else r["returncode"] != 0 for r in receipts), "Actual reproduction failure")
    guards = [json.loads(r["stdout"]) for r in receipts if "output_guard_checks.py" in r["argv"]]
    require(len(guards) == 2 and all(g["status"] == "PASS" and g["rejection_count"] == 386 and g["protected_file_count"] == 184 for g in guards), "Alias guard receipts differ")
    positives = [json.loads(r["stdout"]) for r in receipts if "run_checks.py" in r["argv"]]
    require(len(positives) == 2 and positives[0] == positives[1], "Complete Python mode result differs")
    summary = obj(WORK / "REPRODUCTION_SUMMARY.json")
    require(summary["status"] == "PASS" and summary["archive_sha256"] == sha(DELIVERY / "verification_kit.zip") and summary["canonical_inputs_unchanged_during_reproduction"] == 461, "Reproduction stage differs")
    patch = []
    for name in sorted(before):
        if name.endswith(("/ALLOWLIST.json", "/MANIFEST.json", "/REPAIR01_STAGE_COPIES.json", "/REPAIR01_HISTORY_RESOLUTION.json", ".zip")):
            continue
        old = (AUDIT / before[name]["source_snapshot"]).read_text().splitlines(keepends=True)
        patch.extend(difflib.unified_diff(old, (AUDIT / name).read_text().splitlines(keepends=True), fromfile="before/" + name, tofile="after/" + name))
    p = KIT / "METADATA_DATE02_ADMIN_STAGE.json"
    patch.extend(difflib.unified_diff([], p.read_text().splitlines(keepends=True), fromfile="/dev/null", tofile="after/" + p.relative_to(AUDIT).as_posix()))
    (WORK / "COMPLETE_CODE_PROSE_DIFF.patch").write_text("".join(patch))
    verification = {"status": "PASS_DATED_METADATA_SUCCESSOR_PENDING_NEW_WHOLE02", "baseline_count": 404,
        "authorized_changed_files": 11, "unchanged_protected_files": 393, "new_files": 57, "current_files": 461,
        "before_snapshots": 11, "previous42_outputs_inventory_and_seal_unchanged": True,
        "only_native_notes_changed": True, "native_metadata_exact_notes": expected_notes,
        "native_bare_metadata_bytes_equal": True, "native_wrapper_metadata_object_equal": True,
        "old_stage_copy_rows_unchanged": 44, "new_stage_copy_rows": 56, "total_stage_copy_rows": 100,
        "old_history_rows_unchanged": 899, "appended_history_rows": 1413, "total_history_rows": 2312,
        "history_counts": history_counts, "archive": row(DELIVERY / "verification_kit.zip", DELIVERY),
        "archive_members": 178, "manifest_hashed_payloads": 177, "independent_closed_zip_byte_exact": True,
        "all_headers_payloads_crcs_checked": True, "pdf": row(DELIVERY / "preprint.pdf", DELIVERY),
        "tex": row(DELIVERY / "preprint.tex", DELIVERY), "all_current_executable_bytes_unchanged": True,
        "actual_clean_commands": 27, "guard_invocations": 2, "guard_rejections_each": 386,
        "guard_rejections_total": 772, "guard_protected_files": 184, "guard_each_invocation_both_python_modes": True,
        "normal_optimized_full_result_json_equal": True, "actual_local_native_uploader_check_passed": True,
        "paper_compilation_rendering_or_page_view_performed": False,
        "whole_reviews_completed": 1, "minimum_whole_reviews": 2, "fresh_complete_whole02_required": True,
        "publication_ready": False, "published": False, "services_held_at": 1032,
        "substage_completion_percent": 100, "math_research_completion_best_guess_percent": 60}
    dump(WORK / "FINAL_VERIFICATION.json", verification)
    print(json.dumps(verification, indent=2))


if __name__ == "__main__":
    main()
