#!/usr/bin/env python3
"""Build the exact curated source supplement without network or publication."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import zipfile

PIN = "adc7f1241b42e322a6451854ab7e4b4c146bf78a"
UPSTREAM = "sources/upstream/Vanishing-of-higher-bounded-Hochschild-cohomology-September-23-2026"

# This is intentionally an explicit allowlist: no caches, acquisition
# inventories, credentials, third-party Roydor PDFs, or historical snapshots.
INPUT_PATHS = (
    "manuscript/main.tex",
    "THEOREM_LEDGER.md",
    "DEPENDENCY_LEDGER.md",
    "APPROACHES.md",
    "reproducibility/README.md",
    "reproducibility/build_paper.py",
    "publication/README.md",
    "publication/build_upload_kit.py",
    "zenodo-deposit.json",
    "research/priority_audit_20261007.md",
    "research/roydor_full_conventions_20261007.md",
    "research/roydor_full_proof_scope_attack_20261007.md",
    "research/nonseparable_typei_extension_20261007.md",
    "research/involutive_deformation_adversary_20261007.md",
    "reviews/cohomology_adversary.md",
    "research/cohomology_adversary_checks.py",
    "research/cohomology_adversary_checks.json",
    "research/draft_whole_review_1_checks.py",
    "research/draft_whole_review_1_checks.json",
    "research/revised_checkpoint_review_symbolic_central_homotopy/original_symbolic_check.py",
    "receipts/pinned_sources.json",
    "sources/upstream/ATTRIBUTION.md",
    "sources/upstream/LICENSE",
    "sources/upstream/lean_scope_295.md",
    f"{UPSTREAM}/README.md",
    f"{UPSTREAM}/paper.pdf",
    f"{UPSTREAM}/build/paper.tex",
    f"{UPSTREAM}/build/references.bib",
    f"{UPSTREAM}/build/references.tex",
    f"{UPSTREAM}/build/figures/proof-map.tex",
    f"{UPSTREAM}/build/supporting/typography-mappings.tex",
    f"{UPSTREAM}/build/sections/01-introduction.tex",
    f"{UPSTREAM}/build/sections/02-walk.tex",
    f"{UPSTREAM}/build/sections/03-liouville.tex",
    f"{UPSTREAM}/build/sections/04-rigidity.tex",
    f"{UPSTREAM}/build/sections/05-cohomology.tex",
)
LICENSING = {
    "cc-by-4.0": ("Creative Commons Attribution 4.0 International", "https://creativecommons.org/licenses/by/4.0/"),
    "cc-by-sa-4.0": ("Creative Commons Attribution-ShareAlike 4.0 International", "https://creativecommons.org/licenses/by-sa/4.0/"),
}


def digest(data):
    return sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def generated_members(license_id, confirmed):
    label, url = LICENSING[license_id]
    decision = "confirmed by the human user" if confirmed else "PROPOSED; human choice still pending"
    licenses = f"""# Licenses and attribution

License status for original project material: **{decision}**.

The intended license for original manuscript, prose and verification code is
**{label}** ({license_id}): {url}
Author: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X.
If the status above is proposed, no final license decision is represented and
the package is not cleared for publication.

## Unchanged upstream exception

OpenAI's family-295 manuscript, PDF, supplied README and source files, and the
Lean scope document under sources/upstream remain under Apache License 2.0.
Their exact unchanged license is sources/upstream/LICENSE. Preserve the
original OpenAI attribution and manuscript-specific citation in its README.
The project-written sources/upstream/ATTRIBUTION.md documents the pinned copy.
The proposed/selected Creative Commons license does not relicense this
third-party material. Upstream commit: {PIN}.

No redistribution license is inferred for Roydor's supplied publisher PDF,
the author slides, arXiv comparator PDFs, or other literature acquired during
research. Those files and their extracted text/renders are excluded; their
primary links, versions and hashes are recorded for independent inspection.
"""
    readme = """# Source and verification supplement

Paper: Ordinary Banach–Mazur rigidity of von Neumann algebras.
Author: Alec Kriebel; ORCID 0009-0001-9320-500X. Date: 7 October 2026.
Preparation snapshot: 7 October 2026. See VALIDATION_SCOPE.md for the scope
and timing of these preparation statements. Final complete-package reviews
and publication/tracker receipts are kept separately in the project repository.

Download paper.pdf separately from the deposit. The complete standalone
source is manuscript/main.tex, with an embedded bibliography. From this
extracted directory, using Python 3, Tectonic and Poppler on PATH:

    python3 reproducibility/build_paper.py --render

The helper copies the source to a fresh tmp/ directory, builds there, rejects
compiler errors and overfull boxes, and exports output/pdf/paper.pdf. The
tested runtime is Tectonic 0.16.9 and Poppler 26.08.0. PDF metadata timestamps
can change its byte hash; compare extracted text against the separately
downloaded reviewed PDF. Actual proof claims are justified by the written
proof and audited dependencies, not by a successful TeX build.

Read THEOREM_LEDGER.md and DEPENDENCY_LEDGER.md for exact hypotheses/scope;
APPROACHES.md for competing mechanisms and their gaps. The fresh priority
audit is research/priority_audit_20261007.md; its final-candidate addendum
updates the separately preserved initial checkpoint verdict.

The proof audits in research/ are internal AI checks of particular inputs
and mechanisms. reviews/cohomology_adversary.md is a dated mathematical
source audit of OpenAI's input, not a final-package approval. Its historical
formal-build assignment was not completed: no successful fresh Lean build
or axiom interrogation was reproduced. This follow-on is not claimed to be
formalized. A supplied upstream Lean scope document is not such a build.

Finite exact checks, Python standard library only (tested Python 3.14.6):

    python3 research/cohomology_adversary_checks.py
    python3 research/draft_whole_review_1_checks.py
    python3 research/revised_checkpoint_review_symbolic_central_homotopy/original_symbolic_check.py

These check 5,461 scalar central equations, 16 Catalan cases, 7 block cases,
260,416 noncommutative scalar equations, and 1,022 symbolic central patterns
in the stated finite degree ranges. The first two scripts write their JSON
results locally. Replay in a disposable copy when preserving archive bytes.
None is a computation of the infinite-dimensional theorem.

SOURCE_MANIFEST.json lists the size and SHA256 of every other archive member.
SOURCE_VERSIONS.json identifies pivotal primary texts; inspect those sources
independently. Unchanged OpenAI source is included under Apache-2.0 with its
README, original license and pinned hashes. Roydor/article slides and arXiv
literature PDFs, extractions and renders are not redistributed.

AI tools were used extensively in research, proof development, drafting and
verification. Internal adversarial AI review is not conventional human peer
review; the paper has not undergone conventional human refereeing. The
cohomology breakthrough, geometric and deformation machinery, and predual
reduction are attributed inherited work. The explicit fixed-source proof
assembly supplies the extension beyond the published separable-predual
theorem. No firstness, universal threshold or new cohomology proof is claimed.

Read LICENSES.md for the actual decision status and the upstream exception.
This archive makes no claim of an issued DOI or completed tracker operation.
"""
    validation = """# Validation scope and preparation snapshot

Preparation date: 7 October 2026. This file describes the evidence bundled
when the source supplement was prepared, rather than reporting the state
of later whole-package reviews, publication or tracker operations. Exact
subsequent frozen-version reviews, root responses and nonsecret publication
receipts are preserved separately in the project repository. A later
successful publication does not retroactively turn an earlier input audit
into a full-package review or a human referee report.

The bundled mathematical audits inspect the OpenAI family-295 manuscript
input, Roydor's complete supplied primary version and conventions, the
arbitrary-predual fixed-source proof arrangement, and the involutive
deformation calculation. Each dated report states what it actually checked.
The final-candidate addendum in the fresh 7 October priority report updates
its preserved initial verdict. Bounded literature searches do not certify
firstness or the absence of an equivalent proof.

The verification scripts use exact arithmetic on stated finite models.
They are falsification checks of mechanisms and do not establish the full
infinite-dimensional theorem. The main TeX source and clean build helper
are provided; PDF visual inspection and clean-package reproduction are
separately recorded by the root researcher. Merely constructing this ZIP
does not certify either check.

No successful fresh Lean kernel build/import or axiom interrogation was
reproduced. The argument relies on independently audited mathematical
proofs and attributed classical results. It does not claim formalization
of this follow-on theorem or verification of all classical inputs from
foundational axioms. AI tools were used extensively. Internal adversarial
AI audits are not conventional human peer review/refereeing.

No final license decision may be inferred from a proposed metadata value.
LICENSES.md and SOURCE_VERSIONS.json explicitly record the decision status.
Publication requires the actual human license choice and the required clean
fresh complete-package review of the exact intended payload and metadata.
The archive itself is not evidence of a Zenodo deposit, submitted record,
assigned DOI or tracker append.
"""
    versions = {
        "upstream": {
            "author": "OpenAI", "family": 295, "commit": PIN,
            "url": f"https://github.com/openai/math/tree/{PIN}/preprints/Vanishing-of-higher-bounded-Hochschild-cohomology-September-23-2026",
            "license": "Apache-2.0", "redistributed_unchanged": True,
            "formal_build_reproduced": False,
        },
        "roydor_article": {
            "author": "Jean Roydor", "doi": "10.1142/S1793525321500151",
            "version": "Complete 26-page December 2020 publisher-formatted Second Reading PDF supplied by user; not byte-compared to final 2022 issue",
            "bytes": 431430,
            "sha256": "2320e92723841bd9414c4d846a489bbe78d01a03403b8078ca43354407cfacb4",
            "url": "https://doi.org/10.1142/S1793525321500151",
            "redistributed": False,
        },
        "roydor_slides": {
            "version": "2020 author slides, 87 PDF pages",
            "sha256": "b9202a2b4b3b50efc84a3430c593823f8c15404e83a2987be80083dc9028c36a",
            "url": "https://www.cirm-math.fr/RepOrga/2169/Slides/Roydor_Slides.pdf",
            "redistributed": False,
        },
        "ricard_roydor": {
            "version": "arXiv:1108.1970v2, 24 June 2013",
            "sha256": "36eb3ae3204ff33c1e44f785358d743bbaf53b5671438e7e1a9a4fff66fb8a14",
            "url": "https://arxiv.org/pdf/1108.1970v2", "redistributed": False,
        },
        "own_license": {"id": license_id, "human_decision_confirmed": confirmed},
    }
    return {
        "README.md": readme.encode(),
        "LICENSES.md": licenses.encode(),
        "SOURCE_VERSIONS.json": json_bytes(versions),
        "VALIDATION_SCOPE.md": validation.encode(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--license", choices=LICENSING, default="cc-by-4.0")
    parser.add_argument("--license-confirmed", action="store_true",
                        help="record an already received human license choice; does not grant permission")
    args = parser.parse_args()
    root = args.root.resolve()
    metadata = json.loads((root / "zenodo-deposit.json").read_text())["metadata"]
    if metadata.get("license") != args.license:
        raise RuntimeError("Selected archive license differs from zenodo-deposit.json; propagate the actual decision first")
    if args.license_confirmed and "**CC BY 4.0 is a proposal" in (root / "publication/README.md").read_text():
        raise RuntimeError("Publication README still describes a pending license; update its decision status before building a confirmed archive")
    data = {}
    for relative in INPUT_PATHS:
        path = root / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f"Missing or nonregular curated input: {relative}")
        data[relative] = path.read_bytes()
    pinned = json.loads(data["receipts/pinned_sources.json"])
    if pinned["upstream_commit"] != PIN:
        raise RuntimeError("Pinned upstream commit differs")
    for entry in pinned["files"]:
        if entry["path"] not in data:
            raise RuntimeError(f"Pinned artifact omitted: {entry['path']}")
        actual = data[entry["path"]]
        if len(actual) != entry["bytes"] or digest(actual) != entry["sha256"]:
            raise RuntimeError(f"Pinned upstream bytes differ: {entry['path']}")
    data.update(generated_members(args.license, args.license_confirmed))
    members = [{"path": name, "bytes": len(content), "sha256": digest(content)}
               for name, content in sorted(data.items())]
    source_manifest = {"format": 1, "scope": "Every other archive member; manifest excludes itself",
                       "license_id": args.license,
                       "human_license_decision_confirmed": args.license_confirmed,
                       "files": members}
    data["SOURCE_MANIFEST.json"] = json_bytes(source_manifest)
    target = root / "publication/upload-kit/source-and-verification.zip"
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content in sorted(data.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 7, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (0o100644 << 16)
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None or sorted(archive.namelist()) != sorted(data):
            raise RuntimeError("Archive member or CRC verification failed")
        for name, content in data.items():
            if archive.read(name) != content:
                raise RuntimeError(f"Archive readback differs: {name}")
    for relative in INPUT_PATHS:
        if (root / relative).read_bytes() != data[relative]:
            raise RuntimeError(f"Curated input changed during build: {relative}")
    pdf = root / "output/pdf/paper.pdf"
    receipt = {
        "scope": "Deterministic curated archive construction/readback only; no publication/review/visual-inspection claim",
        "archive": {"path": str(target.relative_to(root)), "bytes": target.stat().st_size,
                    "sha256": digest(target.read_bytes()), "member_count": len(data)},
        "license_id": args.license, "human_license_decision_confirmed": args.license_confirmed,
        "inputs": members,
        "separately_downloadable_pdf": {"path": "output/pdf/paper.pdf", "bytes": pdf.stat().st_size,
                                        "sha256": digest(pdf.read_bytes())},
    }
    (target.parent / "build_receipt.json").write_bytes(json_bytes(receipt))
    print(json.dumps({"archive": receipt["archive"], "license_id": args.license,
                      "human_license_decision_confirmed": args.license_confirmed}, indent=2))


if __name__ == "__main__":
    main()
