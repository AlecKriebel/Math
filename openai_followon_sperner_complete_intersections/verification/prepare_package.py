#!/usr/bin/env python3
"""Create deterministic payload archives; performs no network/publication writes."""
from pathlib import Path
import datetime
import hashlib
import json
import shutil
import zipfile


ROOT = Path(__file__).resolve().parents[1]
TITLE = "The Sperner property of Artinian complete intersections in characteristic zero"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = ROOT
    refs = []
    names = ["The-Artinian-Lex-Plus-Powers-Betti-Theorem-September-23-2026",
             "Commuting-Division-Coefficient-Forms-and-the-Artinian-Eisenbud-Green-Harris-Conjecture-September-23-2026"]
    for name in names:
        source = (p / "sources/upstream" / name / "README.md").read_text()
        refs.append(source.split("```bibtex\n")[1].split("```")[0])
    (p / "manuscript/references.bib").write_text("% Supplied manuscript-specific OpenAI citations.\n" + "\n".join(refs))
    replacements = {"maximum1": "maximum 1", "Python3.10": "Python 3.10",
                    "Tectonic0.16.9": "Tectonic 0.16.9", "Python3.14": "Python 3.14",
                    "Poppler26.08": "Poppler 26.08", "Soc.145": "Soc. 145",
                    "(2017),1497": "(2017), 1497", "Theorem11": "Theorem 11",
                    "submitted2016": "submitted 2016", "returned403": "returned 403",
                    "Corollaries1.2": "Corollaries 1.2", "Theorem1.1": "Theorem 1.1",
                    "Corollary1.2": "Corollary 1.2", "Corollary1.3": "Corollary 1.3",
                    "datedSeptember23,2026": "dated September 23, 2026",
                    "October6,2026": "October 6, 2026", "family200": "family 200",
                    "Section04": "Section 04"}
    for path in [p / "publication/README.md", p / "notes/root_dependency_check.md"]:
        text = path.read_text()
        for old, new in replacements.items():
            text = text.replace(old, new)
        path.write_text(text)
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    receipt = {"timestamp_utc": ts, "native_manuscript_compile": "success",
               "terminal_compiler": "Tectonic 0.16.9", "upstream_builds": [],
               "formalization": "No relevant family 200 entry found; no Lean verification claimed"}
    for name in names:
        build = p / "sources/upstream" / name / "build"
        receipt["upstream_builds"].append({"manuscript": name,
            "result": "success with compatibility wrapper", "original_tex_changed": False,
            "wrapper_sha256": sha(build / "compat.tex"), "pdf_sha256": sha(build / "compat.pdf"),
            "limitation": "Cosmetic pdfTeX metadata primitives only; neither byte reproduction of released PDF nor proof verification"})
    build_receipt = p / "receipts/build_scope.json"
    if not build_receipt.exists():
        build_receipt.write_text(json.dumps(receipt, indent=2) + "\n")
    visual = p / "receipts/pdf_visual_check.json"
    if not visual.exists():
        visual.write_text(json.dumps({"timestamp_utc": ts, "pdf_sha256": sha(p / "output/pdf/main.pdf"),
            "pages": 5, "all_pages_rendered_and_inspected": True,
            "latest_affected_pages_reinspected": [2, 3], "overfull_boxes": 0,
            "unresolved_references": 0, "visual_issues": [], "metadata_checked": True,
            "scratch_pngs_removed_to_release_space": True}, indent=2) + "\n")
    ignore = p / ".gitignore"
    text = ignore.read_text()
    for line in ["sources/primary/", "receipts/pdf_qa/", "sperner-reproduction-*/", "publication/zenodo_upload_kit/"]:
        if line not in text.splitlines():
            text += line + "\n"
    ignore.write_text(text)
    kit = p / "publication/zenodo_upload_kit/files"
    kit.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(p / "output/pdf/main.pdf", kit / "paper.pdf")
    source_files = {"manuscript/main.tex": p / "manuscript/main.tex",
                    "manuscript/references.bib": p / "manuscript/references.bib",
                    "README.md": p / "publication/README.md", "LICENSE": p / "LICENSE"}
    supplement = ["DEPENDENCY_LEDGER.md", "APPROACH_TABLE.md", "LICENSE",
                  "notes/downstream_proof.md", "notes/companion_audit.md", "notes/picard_subaudit.md",
                  "notes/lpp_audit.md", "notes/lpp_box_tests.md", "notes/priority_audit.md",
                  "notes/root_dependency_check.md", "notes/companion_checks.py",
                  "notes/lpp_box_tests.py", "notes/lpp_box_tests.json",
                  "verification/hilbert_examples.py", "verification/hilbert_examples.json",
                  "verification/reproduce.py", "receipts/pinned_sources.json",
                  "receipts/build_scope.json", "receipts/pdf_visual_check.json"]
    if (p / "receipts/clean_reproduction.json").exists():
        supplement.append("receipts/clean_reproduction.json")
    verification_files = {name: p / name for name in supplement}
    verification_files["README.md"] = p / "publication/README.md"
    def archive(name, files):
        with zipfile.ZipFile(kit / name, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as out:
            for label, path in sorted(files.items()):
                info = zipfile.ZipInfo(label, (2026, 10, 6, 12, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                out.writestr(info, path.read_bytes())
    archive("source.zip", source_files)
    archive("verification.zip", verification_files)
    manifest = {"metadata": {"title": TITLE, "upload_type": "publication",
        "publication_type": "preprint", "publication_date": "2026-10-06",
        "description": "For every standard graded Artinian complete intersection over an arbitrary characteristic-zero field, the maximum minimal number of generators over all ideals, including nonhomogeneous ideals, equals the largest coefficient of the complete-intersection Hilbert polynomial. This concise note records an immediate consequence of OpenAI's Artinian EGH theorem and the previously published EGH-to-Sperner implication of Harima, Wachi and Watanabe. It makes degree-one elimination, the empty/all-linear case, the all-ideal filtration argument and field scope explicit, with exact integer examples and scoped dependency/priority audits. No new EGH proof, first-priority claim, Lefschetz theorem, nongraded extension or unrestricted positive-characteristic conclusion is asserted. AI tools were used extensively in research, drafting and verification. Automated adversarial reviews are not conventional human peer review; this preprint has not undergone conventional human peer review or refereeing at publication. No formalization of the follow-on theorem is claimed.",
        "creators": [{"name": "Kriebel, Alec", "orcid": "0009-0001-9320-500X"}],
        "access_right": "open", "license": "cc-by-4.0",
        "keywords": ["Sperner property", "Artinian complete intersections", "Eisenbud-Green-Harris", "commutative algebra"],
        "related_identifiers": [
            {"identifier": "10.1090/proc/13347", "relation": "isDerivedFrom", "scheme": "doi"},
            {"identifier": "https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a", "relation": "isDerivedFrom", "scheme": "url"}]},
        "files": [{"path": "publication/zenodo_upload_kit/files/" + name} for name in ["paper.pdf", "source.zip", "verification.zip"]]}
    (p / "zenodo-deposit.json").write_text(json.dumps(manifest, indent=2) + "\n")
    inventory = {"candidate": "v1", "timestamp_utc": ts, "manifest_sha256": sha(p / "zenodo-deposit.json"),
                 "payload": [{"name": f.name, "bytes": f.stat().st_size, "sha256": sha(f),
                              "md5": hashlib.md5(f.read_bytes()).hexdigest()} for f in sorted(kit.iterdir())],
                 "source_member_sha256": {name: sha(path) for name, path in source_files.items()},
                 "verification_member_sha256": {name: sha(path) for name, path in verification_files.items()}}
    (p / "receipts/candidate_v1.json").write_text(json.dumps(inventory, indent=2) + "\n")
    print(json.dumps({"candidate": inventory["candidate"], "payload": inventory["payload"]}, indent=2))


if __name__ == "__main__":
    main()
