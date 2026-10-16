#!/usr/bin/env python3
"""One-time bounded repair authoring; not a distributed automatic resealer."""
import datetime
import hashlib
import json
import shutil
from pathlib import Path

AUDIT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
DELIVERY = AUDIT / "preprint_v1_0"
KIT = DELIVERY / "verification_kit"


def require(test, message):
    if not test:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def freeze():
    before = json.loads((WORK / "IMMEDIATE_INPUT_PINS.json").read_text())["files"]
    for row in before:
        p = AUDIT / row["path"]
        require(p.stat().st_size == row["bytes"] and digest(p) == row["sha256"], "pre-mutation mismatch: " + row["path"])
    changed = [
        "preprint_v1_0/metadata.json", "preprint_v1_0/deposit_metadata.json",
        "preprint_v1_0/README.md", "preprint_v1_0/EXTERNAL_BINDING.json",
        "preprint_v1_0/verification_kit.zip",
        "preprint_v1_0/verification_kit/metadata.json",
        "preprint_v1_0/verification_kit/README.md",
        "preprint_v1_0/verification_kit/verify.py",
        "preprint_v1_0/verification_kit/build_archive.py",
        "preprint_v1_0/verification_kit/ALLOWLIST.json",
        "preprint_v1_0/verification_kit/MANIFEST.json",
    ]
    rows = []
    for name in changed:
        source = AUDIT / name
        dest = WORK / "before" / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
        require(source.read_bytes() == dest.read_bytes(), "before copy")
        target = KIT / "repair01_history/before" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append({"original_path": name, "source_snapshot": dest.relative_to(AUDIT).as_posix(),
                     "destination": target.relative_to(KIT).as_posix(), "bytes": source.stat().st_size,
                     "sha256": digest(source), "stage": "immediately before bounded repair01"})
    # Complete preceding whole-review evidence, plus the immutable preparation
    # accounting and root adoptions. Historical references to excluded bodies
    # receive individual omissions in the new resolution ledger.
    selected = [r["path"] for r in before if r["path"].startswith("reviews/package_01/")]
    selected += ["ROOT_WHOLE_PACKAGE_REVIEW_01.json", "ROOT_PREPRINT_REVIEW_01.json"]
    selected += ["preprint_v1_0/" + n for n in ["INPUT_PINS.json", "OUTPUT_PINS.json", "STATUS.json",
                 "PREPARATION_REPORT.md", "FINAL_VERIFICATION.json", "CLEAN_EXTRACTION_RESULTS.json",
                 "FAULT_RESULTS.json", "BINDING_VERIFICATION.json", "ARCHIVE_BUILD.json", "COMPILE_DIAGNOSTICS.json",
                 "PDF_VISUAL_QA.json", "RESEARCH_LOG.md"]]
    for name in sorted(set(selected)):
        source = AUDIT / name
        target = KIT / "repair01_history/captured_stage" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append({"original_path": name, "source_snapshot": name,
                     "destination": target.relative_to(KIT).as_posix(), "bytes": source.stat().st_size,
                     "sha256": digest(source), "stage": "captured before bounded repair01; immutable historical record"})
    dump(KIT / "REPAIR01_STAGE_COPIES.json", {"scope": "Exact old stages; no historical pin rewritten. Current files may differ only through explicitly authorized repairs.", "files": rows})
    dump(WORK / "BEFORE_COPIES.json", {"files": rows[:len(changed)]})
    return before, changed


def metadata():
    old = (WORK / "before/preprint_v1_0/metadata.json").read_bytes()
    require(old == (WORK / "before/preprint_v1_0/deposit_metadata.json").read_bytes() ==
            (WORK / "before/preprint_v1_0/verification_kit/metadata.json").read_bytes(), "old research objects differ")
    for p in [DELIVERY / "research_metadata.json", KIT / "research_metadata.json"]:
        p.write_bytes(old)
    data = {
        "title": "A credited finiteness deduction for restricted boundary-twist factorizations",
        "upload_type": "publication", "publication_type": "preprint",
        "creators": [{"name": "Kriebel, Alec", "affiliation": "Independent researcher", "orcid": "0009-0001-9320-500X"}],
        "description": (
            "For each fixed genus g ≥ 1, let S(g,1) be an oriented compact surface with one boundary component, "
            "and let maps and isotopies fix that boundary pointwise. We prove that ordered positive factorizations "
            "of one positive boundary Dehn twist, along non-null-homotopic simple closed curves with repetitions "
            "permitted and pairwise geometric intersection at most one, have finitely many simultaneous-conjugacy "
            "classes. Their maximal length M(g) is finite and attained, with M(g) ≥ 4g(2g+1). Peripheral factors "
            "occur only in the singleton factorization; otherwise all factors are nonseparating. The values "
            "M(1) = 12 and M(2) = 40 are credited deductions from prior work with the convention bridge stated. "
            "This gives a complete negative answer, under the stated conventions, to the separately printed "
            "restricted arbitrary-length clause in the Wajnryb/Farb problem collection. The full original "
            "maximum and classification bundle remains partial: exact M(g) for g ≥ 3, explicit upper formulas, "
            "an effective exhaustive-enumeration stopping criterion, extremizers, and Hurwitz, positive Artin, "
            "T-move and A5/D6 classifications remain unresolved in this work. "
            "The note is a credited deduction and exposition. Cossu and Tringali's arXiv:2208.05869v3, "
            "Corollary 4.13, supplies the generic finite-alphabet finiteness corollary through a normal reduced "
            "cone and nonerasing atomic expansions. The support and ribbon arguments explicitly build on "
            "Juvan–Malnič–Mohar, Malestein–Rivin–Theran, and Cahn–Fanoni–Petri. Honda–Kazez–Matić, Smith, "
            "the chain relation, and Baykur–Monden–Van Horn-Morris provide credited premises. Exact historical "
            "priority of the resulting surface application, novelty, and worldwide current-open status remain "
            "UNKNOWN; a bounded literature audit is not an absence proof. Extensive AI tools were used in "
            "mathematical and source checking, writing, code, and package preparation. This preprint is "
            "unrefereed, has no external human peer review, and is not formally certified. The accompanying "
            "verification kit provides written proof and source/custody records plus reproducible finite fault "
            "controls; those controls do not replace the universal proof or replay omitted historical inputs."
        ),
        "access_right": "open", "license": "cc-by-4.0", "publication_date": "2026-10-14",
        "version": "1.0", "language": "eng",
        "keywords": ["mapping class groups", "Dehn twist factorizations", "geometric intersection", "finite factorizations", "credited mathematical exposition"],
        "notes": "Prepared locally on 2026-10-14 before deposit or publication. One complete whole-candidate review has been completed; a fresh complete second review is required after the metadata and output-interface repair. Publication readiness has not been affirmed."
    }
    for p in [DELIVERY / "metadata.json", KIT / "metadata.json"]:
        dump(p, data)
    dump(DELIVERY / "deposit_metadata.json", {"metadata": data, "files": [
        {"path": "preprint.pdf", "name": "preprint.pdf"},
        {"path": "verification_kit.zip", "name": "verification_kit.zip"}]})
    status = {"as_of_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "stage": "bounded repair01 complete; fresh whole02 required",
              "whole_reviews_completed": 1, "minimum_whole_reviews": 2,
              "new_complete_review_required": True, "publication_ready": False, "published": False,
              "services_held_at": 1032, "math_research_completion_best_guess_percent": 60,
              "paper_tex_pdf_changed": False,
              "dated_history": "Old STATUS.json, preparation metadata and old verdicts retain their exact dated meaning; this current record supersedes their pending-review counts."}
    for p in [DELIVERY / "CURRENT_STATUS_REPAIR01.json", KIT / "CURRENT_STATUS_REPAIR01.json"]:
        dump(p, status)


def documents():
    outer = (WORK / "before/preprint_v1_0/README.md").read_text()
    outer = outer.replace("# PR1080, problem11000150: version 1.0 preparation candidate", "# PR1080, problem11000150: version 1.0 repaired candidate")
    outer = outer.replace("The candidate is unrefereed, has no external human peer review or formal certification, and awaits at least two fresh whole-candidate adversarial reviews. Publication readiness is false at this preparation checkpoint.",
        "The candidate is unrefereed, has no external human peer review or formal certification. One complete whole-candidate review found two package issues; this bounded repair fixes them and requires a fresh complete second review. Publication readiness remains false. `CURRENT_STATUS_REPAIR01.json` is the current successor to unchanged dated preparation records.")
    outer = outer.replace("`metadata.json`, `deposit_metadata.json` and the kit's `metadata.json` are byte-identical.",
        "`metadata.json` and the kit's `metadata.json` are byte-identical native Zenodo API objects. `deposit_metadata.json` is the repository upload manifest containing exactly `metadata` and `files`; its metadata object equals the two bare objects and its attachments are exactly the unchanged PDF and repaired ZIP. `research_metadata.json` preserves the old custom research object byte-for-byte, including its dated preparation checkpoint. This custom object is not an upload manifest.")
    outer += "\n## Current repair and local submission check\n\nThe exact TeX, PDF, mathematical theorem and source credits are unchanged. `repair01_history` in the kit retains the captured-before bytes of every changed old artifact and the complete whole01 outputs. `REPAIR01_HISTORY_RESOLUTION.json` individually resolves prior pins to exact stage copies or records a precise omission; `REPAIR01_STAGE_COPIES.json` verifies every delivered captured-stage copy. Earlier `INPUT_PINS.json` and `OUTPUT_PINS.json` stay unchanged historical records. Current repair custody and ordinary/optimized receipts are in `../repairs/package01`.\n\nFrom the repository root, the entirely local uploader validation is:\n\n```sh\npython3 -B zenodo_deposit_tool/zenodo.py check draft_pr_actual_claims_1000_1100_20261012/audits/pr1080_11000150/preprint_v1_0/deposit_metadata.json\n```\n\nNo deposition, publication, DOI, spreadsheet write or PR disposition has occurred for this candidate. Native metadata's dated preparation note does not certify final clearance. The external binding binds the kit manifest, native metadata, historical research object, upload manifest, and exact PDF/ZIP without placing the wrapper or binding inside the ZIP.\n"
    (DELIVERY / "README.md").write_text(outer)
    inner = (WORK / "before/preprint_v1_0/verification_kit/README.md").read_text()
    inner = inner.replace("version 1.0 preparation candidate", "version 1.0 repaired candidate")
    inner = inner.replace("The dated metadata records preparation on 14 October 2026 UTC, pending at least two fresh whole-candidate adversarial reviews; publication readiness has not been affirmed.",
        "The native metadata records local preparation on 14 October 2026 UTC. One complete whole-candidate review found two package issues; this repair requires a fresh complete second review. Publication readiness remains false. `CURRENT_STATUS_REPAIR01.json` supersedes dated pending-count statements without changing historical records.")
    inner = inner.replace("python3 -I fault_checks.py\n", "python3 -I fault_checks.py\npython3 -I output_guard_checks.py\n")
    inner += "\n## Native metadata, historical stage resolution, and output safety\n\n`metadata.json` is native Zenodo API metadata and equals the external bare metadata and the `metadata` object of the external `{metadata, files}` upload manifest. `research_metadata.json` preserves the original custom research object unchanged; it is historical research metadata rather than API metadata. The external binding checks both objects and the complete upload manifest before affirming attachment identities. Its manifest hashes have no cycle: native/custom metadata and captured-before stage copies are kit payloads; the live PDF, ZIP, upload manifest and binding remain external.\n\n`REPAIR01_STAGE_COPIES.json` enumerates exact immutable old-stage copies. `REPAIR01_HISTORY_RESOLUTION.json` checks all 309 immediate inputs, all 194 preparation inputs, all 90 preparation outputs, all 289 whole01 inputs and all 17 whole01 outputs against exact current/captured-stage copies or individual omissions. The prior 269-reference ledger is also checked unchanged. An omitted primary body is not represented as a delivered or replayed source. Captured old code and archives are history, not current executable instructions.\n\nThe archive builder accepts only a fresh output file outside the kit, with an existing ordinary parent directory. It rejects the unresolved leaf and every symlink ancestor before any archive write, including dangling symlinks and paths through aliases. Every existing destination is rejected, covering hardlinks to all kit inputs, external PDF/TeX, upload metadata, descriptors, and sentinels. Creation uses exclusive mode, so an existing file or leaf symlink appearing between preflight and open is not truncated. A fresh independent outside rebuild destination works in both Python modes. Rebuild commands require a fresh filename; remove only your own previous rebuild before repeating them.\n\n`output_guard_checks.py` exercises direct and nested protected paths, hardlinks to every kit input and external delivery-like files, outside symlink targets, symlinked ancestors (including paths containing `..`), and existing sentinels under normal and optimized Python. Rejections are checked against all protected input and sentinel hashes. Positive rebuilds are byte-identical. Other command interfaces expose no user-supplied file destination; reviewer calculations write only their own fresh temporary scratch. Direct Tectonic compilation is a separately documented source compilation command, not a writer offered by the kit CLI.\n"
    (KIT / "README.md").write_text(inner)


if __name__ == "__main__":
    freeze()
    metadata()
    documents()
    print("Initial bounded metadata, stage copies and documentation repair authored; code, pins and final controls follow.")
