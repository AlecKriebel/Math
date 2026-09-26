#!/usr/bin/env python3
"""Assemble only the reviewed, explicitly allowlisted journal deliverables."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import zipfile
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
UPLOAD = ROOT / "upload"
OUTPUT = ROOT / "output"
STAMP = (2026, 9, 26, 4, 0, 0)
SNAPSHOT = "be0f06ee0c61739dcda5629e2c4223e7da7951d3"
REPO = ("https://github.com/AlecKriebel/Math/tree/" + SNAPSHOT +
        "/kourovka_16_45/journal_submission_2026_09_25/supplement")

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def archive(destination, members):
    if len({name for name, _ in members}) != len(members):
        raise ValueError("Duplicate archive member")
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, path in sorted(members):
            if name.startswith("/") or ".." in Path(name).parts or path.is_symlink():
                raise ValueError("Unsafe archive path")
            info = zipfile.ZipInfo(name, STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, path.read_bytes())

def main():
    UPLOAD.mkdir(exist_ok=True)
    main_pdf = ROOT / "output/pdf/kourovka_16_45.pdf"
    note_pdf = ROOT / "output/pdf/verification_note.pdf"
    counts = {"main": len(PdfReader(main_pdf).pages),
              "verification_note": len(PdfReader(note_pdf).pages)}
    if counts != {"main": 7, "verification_note": 3}:
        raise ValueError(f"Unexpected reviewed pagination: {counts}")
    tex = (ROOT / "manuscript/kourovka_16_45.tex").read_text()
    if SNAPSHOT not in tex:
        raise ValueError("Missing immutable reproducibility link")
    for rel in ["output/pdf/kourovka_16_45.log", "output/pdf/verification_note.log"]:
        log = (ROOT / rel).read_text()
        if re.search(r"Overfull|Underfull|undefined references|Citation .* undefined|^!", log, re.M):
            raise ValueError(f"Unresolved compiler diagnostic in {rel}")
    if digest(ROOT / "manuscript/baustms.cls") != "b5e53c7510ed44cd2673e30f7c60b2c09d4fdb77d057e9d61979ed537202fad3":
        raise ValueError("Official journal class has changed")
    shutil.copyfile(main_pdf, UPLOAD / "01_Manuscript.pdf")
    shutil.copyfile(note_pdf, ROOT / "supplement/verification_note.pdf")

    supplement_files = ["README.md", "LICENSES.md", "Makefile", "independent_exact.py",
        "verification_note.tex", "verification_note.pdf",
        "src/verify_counterexample.py", "src/verify_counterexample.cpp",
        "src/compare_certificates.py", "src/compare_results.py",
        "expected/finite_certificate.json", "expected/independent_exact.json",
        "expected/independent_subgroups.json", "expected/subgroups_cpp.txt",
        "expected/verification_cpp.txt", "expected/verification_python.json"]
    archive(UPLOAD / "02_Reproducibility.zip",
            [(f"Kourovka16_45_Verification/{f}", ROOT / "supplement" / f) for f in supplement_files])
    archive(UPLOAD / "03_LaTeX_Source.zip",
            [(f"Kourovka16_45_Source/{f}", ROOT / "manuscript" / f)
             for f in ["kourovka_16_45.tex", "baustms.cls", "README.md"]])

    abstract = ("Let b(G) be the largest size of an inclusion-minimal base over all "
        "permutation representations of a finite group G, with bases taken for the "
        "permutation image, and let μ′(G) be the largest size of an independent "
        "subset of G. We construct an explicit affine group of order 100920 for "
        "which b(G) = 3 < 4 = μ′(G), giving a negative answer to Kourovka Notebook "
        "Problem 16.45. The maximum remains three when restricted to faithful "
        "representations. The proof is structural: every subgroup missing the "
        "translation subgroup has faithful base invariant at most two, and every "
        "nontrivial normal subgroup contains the translations. The independent "
        "four-set gives an irredundant intersection family whose intersection is "
        "central in the complement but not normal in the affine group.")
    if len(abstract.split()) > 150:
        raise ValueError("Abstract exceeds conservative 150-word limit")
    ai = ("OpenAI Codex (https://openai.com/codex/) was used during 19–25 September "
        "2026 to develop and check the construction and proofs, generate manuscript "
        "text and exact verification programs, search and check references, and "
        "prepare the submission. Separate AI agents performed adversarial "
        "structural, computational, and source reviews. Historical application "
        "and model build identifiers were not consistently recorded. These checks "
        "are not external peer review or proof-assistant certification. The author "
        "is responsible for the mathematical claims and the submitted text.")
    fields = {
        "Journal": "Bulletin of the Australian Mathematical Society",
        "Section": "Articles",
        "Title": "A counterexample to Kourovka Notebook Problem 16.45",
        "Running title": "Kourovka Notebook Problem 16.45",
        "Author and corresponding author": "Alec Kriebel",
        "Given name": "Alec", "Family name": "Kriebel",
        "Email": "me@aleckriebel.com",
        "Affiliation": "Independent researcher, San Francisco, USA",
        "ORCID": "https://orcid.org/0009-0001-9320-500X",
        "Language": "English",
        "Primary MSC2020": "20B05",
        "Secondary MSC2020": "20D30; 20D60",
        "Keywords": "Permutation bases; independent sets; finite groups; subgroup lattices; Kourovka Notebook",
        "Abstract": abstract,
        "Funding": "This research received no external funding.",
        "Competing interests": "The author declares no competing interests.",
        "AI-use disclosure": ai,
        "Previous preprint": "https://doi.org/10.5281/zenodo.22929486 (unrefereed version 1.0.1)",
        "Current reproducibility snapshot": REPO,
        "Preferred publication route": "Ordinary Green Open Access; no publication charge under current journal policy.",
        "Optional subject editor preference": "John Cossey (Group theory), if the form asks and there is no relevant personal conflict.",
    }
    text = "COPY-READY SUBMISSION METADATA\n\n" + "\n\n".join(k+"\n"+v for k,v in fields.items())
    text += ("\n\nAUTHOR CHECK BEFORE FINAL SUBMISSION\n"
        "Confirm originality, completeness of authorship, personal approval and "
        "accountability, and that no other journal is currently considering the "
        "paper. Add postal details directly in the portal if requested. Historical "
        "AI build identifiers are disclosed as unrecorded; add reliable details if "
        "you have them. Do not invent versions.\n")
    (UPLOAD / "05_Submission_Metadata.txt").write_text(text)

    files = ["01_Manuscript.pdf", "02_Reproducibility.zip", "03_LaTeX_Source.zip",
             "04_Cover_Letter.txt", "05_Submission_Metadata.txt", "START_HERE.md",
             "Review_Summary.md"]
    (UPLOAD / "SHA256SUMS").write_text("".join(digest(UPLOAD/f)+"  "+f+"\n" for f in files))
    archive(OUTPUT / "Kourovka16_45_Bulletin_Submission_Kit.zip",
            [("Kourovka16_45_Bulletin_Submission_Kit/"+f, UPLOAD/f) for f in files+["SHA256SUMS"]])
    manifest = {"package_version":"1.1-submission", "target":fields["Journal"],
        "reproducibility_commit":SNAPSHOT, "page_counts":counts,
        "abstract_words":len(abstract.split()),
        "files":{f:digest(UPLOAD/f) for f in files+["SHA256SUMS"]},
        "kit_sha256":digest(OUTPUT / "Kourovka16_45_Bulletin_Submission_Kit.zip"),
        "manuscript_source_sha256":digest(ROOT / "manuscript/kourovka_16_45.tex"),
        "supplement_source_sha256":digest(ROOT / "supplement/verification_note.tex")}
    (ROOT / "evidence/package_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print(json.dumps({"kit":str(OUTPUT / "Kourovka16_45_Bulletin_Submission_Kit.zip"),
                      "pages":counts,"abstract_words":len(abstract.split())},indent=2))

if __name__ == "__main__":
    main()
