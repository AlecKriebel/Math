#!/usr/bin/env python3
"""Local, allowlisted preparation only. No service, Git, or ledger mutations."""
from pathlib import Path, PurePosixPath
import datetime as dt
import hashlib
import json
import shutil
import stat
import sys
import zipfile

SUPPORT = Path(__file__).resolve().parent
AUDIT = SUPPORT.parent
PREPRINT = AUDIT / "preprint"
PACKAGE = PREPRINT / "package_source" / "birational-cycle-verification"
PUBLICATION = PREPRINT / "publication"
REPO = AUDIT.parents[2]
TITLE = "A fixed birational map without a prime-field cycle-distribution limit"
STEM = "fixed-birational-cycle-nonlimit"


def require(test, message):
    if not test:
        raise RuntimeError(message)


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def entry(path, root):
    require(path.is_file() and not path.is_symlink(), "Unsafe payload")
    b = path.read_bytes()
    return {"path": path.relative_to(root).as_posix(), "bytes": len(b),
            "sha256": hashlib.sha256(b).hexdigest()}


def copy_verified(source, dest, expected=None):
    require(source.is_file() and not source.is_symlink(), "Unsafe source copy")
    b = source.read_bytes()
    if expected is not None:
        require(len(b) == expected["bytes"] and hashlib.sha256(b).hexdigest() == expected["sha256"],
                "Pinned source changed: " + source.name)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(b)


def main():
    require(len(sys.argv) == 1, "No overrides accepted")
    require(PREPRINT.is_dir() and (PREPRINT / "output/main.pdf").is_file(), "Build the PDF first")
    require(json.loads((SUPPORT / "PREPARATION_DEDUP.json").read_text())["exact_target_found"] is False,
            "Unreconciled duplicate lead")
    if PACKAGE.exists():
        require(not PACKAGE.is_symlink() and PACKAGE.parent == PREPRINT / "package_source", "Unsafe staging path")
        shutil.rmtree(PACKAGE)
    PACKAGE.mkdir(parents=True)
    PUBLICATION.mkdir(exist_ok=True)

    snapshot = json.loads((AUDIT / "SOURCE_SNAPSHOT.json").read_text())
    require(snapshot["head"] == "091bdecef6f84154f5d5c205a4b07eeb6391b8f8" and len(snapshot["files"]) == 17,
            "Unexpected original snapshot")
    for f in snapshot["files"]:
        copy_verified(AUDIT / f["snapshot"], PACKAGE / f["snapshot"], f)
    copy_verified(AUDIT / "SOURCE_SNAPSHOT.json", PACKAGE / "SOURCE_SNAPSHOT.json")
    for family, manifest_name in [("arithmetic_falsification", "OUTPUT_MANIFEST.json"),
                                   ("source_quantifiers", "ARTIFACT_MANIFEST.json")]:
        source = AUDIT / "reviews" / family
        dest = PACKAGE / "historical_reviews" / family
        manifest = json.loads((source / manifest_name).read_text())
        for f in manifest["files"]:
            copy_verified(source / f["path"], dest / f["path"], f)
        copy_verified(source / manifest_name, dest / manifest_name)
    for name in ["check_math.py", "verify.py", "expected_checks.json", "REPLAY_RECEIPT.json",
                 "SOURCE_REFERENCES.json", "PRIORITY_SCOPE.md"]:
        copy_verified(SUPPORT / name, PACKAGE / name)
    copy_verified(SUPPORT / "PACKAGE_README.md", PACKAGE / "README.md")
    copy_verified(PREPRINT / "main.tex", PACKAGE / "paper/main.tex")
    (PACKAGE / "LICENSE.txt").write_text(
        "Authored text and code in this package are licensed under Creative Commons Attribution 4.0 International.\n"
        "https://creativecommons.org/licenses/by/4.0/\n"
        "Copyright 2026 Alec Kriebel. Preserve attribution and identify changes.\n"
        "Third-party cited works retain their own rights; full source bodies are not redistributed.\n")
    (PACKAGE / "CITATION.cff").write_text(
        'cff-version: 1.2.0\nmessage: "Please cite the associated preprint and its established source references."\n'
        'type: article\ntitle: "' + TITLE + '"\nversion: "1.0"\ndate-released: 2026-10-21\n'
        'authors:\n  - family-names: Kriebel\n    given-names: Alec\n'
        '    affiliation: Independent researcher\n    orcid: "https://orcid.org/0009-0001-9320-500X"\n'
        'license: CC-BY-4.0\n')
    files = sorted(p for p in PACKAGE.rglob("*") if p.is_file())
    require(not any(p.suffix.lower() in (".pdf", ".png", ".jpg", ".env") for p in files),
            "Unexpected third-party/media/secret body in source package")
    write_json(PACKAGE / "MANIFEST.json", {"schema": 1, "files": [entry(p, PACKAGE) for p in files]})

    pdf_name = STEM + ".pdf"
    tex_name = STEM + ".tex"
    zip_name = STEM + "-verification.zip"
    copy_verified(PREPRINT / "output/main.pdf", PUBLICATION / pdf_name)
    copy_verified(PREPRINT / "main.tex", PUBLICATION / tex_name)
    with zipfile.ZipFile(PUBLICATION / zip_name, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(q for q in PACKAGE.rglob("*") if q.is_file()):
            name = "birational-cycle-verification/" + p.relative_to(PACKAGE).as_posix()
            zi = zipfile.ZipInfo(name, date_time=(2026, 10, 21, 0, 0, 0))
            zi.create_system = 3
            zi.external_attr = (stat.S_IFREG | 0o644) << 16
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, p.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(PUBLICATION / zip_name) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), "Duplicate ZIP member")
        for n in names:
            p = PurePosixPath(n)
            require(not p.is_absolute() and ".." not in p.parts and "\\" not in n and str(p) == n,
                    "Unsafe ZIP path")
        require(z.testzip() is None, "ZIP CRC failure")

    description = (
        "<p>For the fixed birational map L(u,v)=(u,(u²+1)v), every prime p congruent to 3 modulo 4 "
        "gives a permutation of the full affine plane F_p². With point-weighted periods normalized by p, "
        "the distribution function at every fixed 1/2≤x&lt;1 equals 1−φ(p−1)/(p−1)+o(1), has limsup 1 and "
        "liminf at most 23/24. Neither these CDF values nor the period probability measures converge "
        "on any further admissible prime subset of positive upper relative density.</p>"
        "<p>This is a precisely scoped application to the broad existence assertion in Vivaldi's 2004 "
        "Oberwolfach contribution, joint work with Roberts. The triangular family, quadratic primitive-value "
        "machinery, shifted-prime totient mean and continuous scalar empirical law are established and "
        "credited to the actual sources. The positive-density selection conclusion uses the old atomless "
        "scalar law, not merely the existence of two subsequences. No new map family, character-sum theorem, "
        "arithmetic mean, scalar law, universal elliptic theorem, polynomial-automorphism theorem or "
        "prime-average cycle theorem is claimed.</p>"
        "<p>The bounded priority audit authenticated no earlier statement of this exact application in the "
        "inspected sources. The cited Neumärker–Roberts–Viallet–Vivaldi 2011 preprint body and version "
        "relationships remain unrecovered; no inference about its unseen contents is made. No worldwide "
        "novelty, current-open status or historical firstness is claimed.</p>"
        "<p>The source/verification ZIP preserves all 17 original research files and historical mathematical "
        "audit artifacts, supplies exact manifests and a new dependency-free standard-library checker. "
        "The latter passed 147,619 finite exact checks over 87 admissible primes through 1000, eight full "
        "affine orbit graphs with 6,088 points, six bad-reduction controls and a totient bound through 10,000. "
        "Historical 8,347,742 finite assertions and 230,780 analytic controls are separate retained runs. "
        "Original SymPy scripts were not successfully replayed in this preparation; the analytic proof "
        "and explicitly cited classical inputs establish the infinite-prime statements.</p>"
        "<p>AI systems were extensively involved in research, model and proof development, computation, "
        "literature investigation, writing and adversarial verification. This is an unrefereed preprint "
        "with no formal independent human peer review. Internal AI audits do not constitute human peer review.</p>"
    )
    metadata = {
        "title": TITLE, "upload_type": "publication", "publication_type": "preprint",
        "description": description,
        "creators": [{"name": "Kriebel, Alec", "affiliation": "Independent researcher",
                      "orcid": "0009-0001-9320-500X"}],
        "access_right": "open", "license": "cc-by-4.0", "publication_date": "2026-10-21",
        "version": "1.0", "language": "eng",
        "keywords": ["birational dynamics", "finite fields", "cycle distribution", "point periods",
                     "Euler totient", "primitive quadratic values", "positive-density primes",
                     "30000156", "OWR-768-006"],
        "related_identifiers": [
            {"identifier": "https://github.com/AlecKriebel/Math/pull/280", "relation": "isSupplementTo", "scheme": "url"},
            {"identifier": "10.4171/OWR/2004/54", "relation": "references", "scheme": "doi"},
            {"identifier": "10.1017/S1446788712000250", "relation": "references", "scheme": "doi"},
            {"identifier": "10.4064/aa8258-4-2016", "relation": "references", "scheme": "doi"}],
        "references": [
            "F. Vivaldi (joint work with J. A. G. Roberts), Maps over finite fields: integrability and reversibility, Oberwolfach Reports 54/2004, 2944–2945.",
            "A. Ostafe and I. E. Shparlinski, On the degree growth in some polynomial dynamical systems and nonlinear pseudorandom number generators, arXiv:0902.3884v3 (2009), Section 2.1.",
            "A. R. Booker, S. D. Cohen, N. Sutherland and T. Trudgian, Primitive values of quadratic polynomials in a finite field, arXiv:1803.01435v2 (2018), equations 5–6 and Lemma 1.",
            "L. Menici and C. Pehlivan, Average r-rank Artin conjecture, Acta Arithmetica 174(3) (2016), 255–276, doi:10.4064/aa8258-4-2016, Lemma 2.",
            "S. Aivazidis and E. Sofos, On the distribution of the density of maximal order elements in general linear groups, arXiv:1308.5701v2 (2014), Theorem 1.3(i) and Section 6.",
            "J.-M. Deshouillers and M. Hassani, A note on the distribution function of φ(p−1)/(p−1), Journal of the Australian Mathematical Society 93 (2012), 77–83; online 16 January 2013; doi:10.1017/S1446788712000250.",
            "J. A. G. Roberts, Order and symmetry in birational difference equations and their signatures over finite phase spaces, Future Directions in Difference Equations, Vigo (2011), 213–221, reference 9. The cited four-author 2011 manuscript body remains unrecovered."]
    }
    write_json(PUBLICATION / "zenodo-deposit.json", {"metadata": metadata,
               "files": [{"path": pdf_name, "name": pdf_name}, {"path": zip_name, "name": zip_name}]})
    (PUBLICATION / "README.md").write_text(
        "# Prepared PR280 preprint package\n\n" + TITLE + "\n\n"
        "Alec Kriebel; ORCID 0009-0001-9320-500X; version 1.0; 21 October 2026 UTC.\n\n"
        "This directory contains the paper, TeX source, verification archive and local metadata. "
        "Review, integration, publication and ledger outcomes are recorded separately in the repository "
        "audit receipts. This README does not itself certify those actions.\n\n"
        "The two intended uploads are the paper PDF and source/verification ZIP. The TeX source is also "
        "included inside the ZIP. zenodo-deposit.json is a conventional local metadata manifest for the "
        "existing repository client; loading it does not create or publish a record. RELEASE_FILES.json "
        "binds exactly the PDF, TeX, ZIP, metadata manifest and this README by length and SHA256.\n\n"
        "Extract the ZIP and run python3 -B verify.py inside birational-cycle-verification. It requires "
        "Python 3.9+ and the standard library, verifies the exact file set/hashes, rejects symlinks and "
        "replays 147,619 finite checks. Finite controls do not prove the analytic limiting assertions.\n\n"
        "The original 17 files are retained byte for byte. Historical mathematical/source audits retain "
        "their dates and former scope/priority qualifications. The current paper supplies the stronger "
        "positive-upper-density selection proof with classical credit. Original SymPy script replay is "
        "not claimed for this preparation. No third-party full source bodies, private account records, "
        "ledger bodies or credentials are included.\n\n"
        "The specific unrecovered Neumarker–Roberts–Viallet–Vivaldi 2011 manuscript remains a disclosed "
        "historical limit. No worldwide-firstness or current-open claim is made. AI involvement covers "
        "research, model/proof development, computation, literature, writing and audits; formal independent "
        "human peer review has not occurred.\n")
    # Read-only use of the canonical client verifies conventional metadata/files.
    sys.path.insert(0, str(REPO / "zenodo_deposit_tool"))
    import zenodo
    _, uploads = zenodo.load_manifest(PUBLICATION / "zenodo-deposit.json")
    require([u["name"] for u in uploads] == [pdf_name, zip_name], "Unexpected upload set")
    names = [pdf_name, tex_name, zip_name, "zenodo-deposit.json", "README.md"]
    release = {"timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "version": "1.0",
               "status": "Prepared complete package; fresh sequential independent package reviews pending",
               "publication_ready": False, "published": False,
               "archive_payloads": len(files), "archive_members": len(files) + 1,
               "intended_uploads": [pdf_name, zip_name],
               "files": [entry(PUBLICATION / n, PUBLICATION) for n in names]}
    write_json(PUBLICATION / "RELEASE_FILES.json", release)
    print(json.dumps({"publication_directory": str(PUBLICATION), "archive_payloads": len(files),
                      "archive_members": len(files) + 1, "intended_uploads": [pdf_name, zip_name],
                      "publication_ready": False}, indent=2))


if __name__ == "__main__":
    main()
