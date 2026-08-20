# Release manifest

This manifest describes the DOI-bearing public source package for version
1.2.0, dated 19 August 2026. Its version-specific DOI is
`10.5281/zenodo.22013710`. The preceding v1.1.3 record remains archived at
version DOI `10.5281/zenodo.21971507`; that DOI is not the identifier for this
revision. Human-only deposit and submission instructions are maintained
outside this public archive.

## Mathematical sources

- `main.tex` — paper source.
- `build_paper.sh` — reproducible Tectonic build command.
- `output/pdf/exceptional_ybe_d4.pdf` — typeset paper.
- `README.md` — construction and reproducibility overview.
- `PRIORITY_AUDIT.md` — historical primary-source search through 16 August.
- `CONCURRENT_WORK_AND_CHRONOLOGY_v1.2.0.md` — current source-backed public
  chronology, historical hashes, and concurrent-work audit.
- `GLOBAL_BRAID_SOURCE_AUDIT_v1.2.0.md` — exact source table for finite-image,
  Clifford, quaternionic-tower, coefficient-trace, and algorithmic claims.
- `TOPOLOGICAL_NORMALIZATION_AUDIT_v1.2.0.md` — line-by-line Turaev and
  Lickorish--Millett convention crosswalk.
- `GLOBAL_STRENGTHENING_ADJUDICATION_v1.2.0.md` — accepted, narrowed, and
  omitted claims in the final strengthening pass.
- `SECTION9_HARDENING_ADJUDICATION_v1.2.0.md` — itemized disposition of the
  final direct-versus-transported attribution and frame-clarity pass.
- `REVISION_AUDIT.md` — historical adjudication for version 1.1.0.
- `RELEASE_NOTES_v1.1.0.md` — prior version's historical release record.
- `RELEASE_NOTES_v1.1.1.md` — prior submission-hardening record.
- `RELEASE_NOTES_v1.1.2.md` — prior frontier-review record.
- `REVIEW_ADJUDICATION_v1.1.2.md` — historical itemized disposition of the
  two frontier-model reviews and adversarial re-audit.
- `RELEASE_NOTES_v1.1.3.md` and `CORRECTION_AUDIT_v1.1.3.md` — historical
  records for the preceding archived version.
- `RELEASE_NOTES_v1.2.0.md` — current scholarly-update and package record.
- `CHANGELOG_v1.2.0.md` — concise current change log.
- `SOURCE_SNAPSHOT.md` — provenance and hashes of supplied inputs.
- `RESEARCH_LOG.md` — timestamped audit and publication log.

## Verification

- `verify_supplied_original.py` — byte-for-byte preserved original discovery-era checker;
  archival only.
- `verify_supplied.py` — hardened supported SymPy route.
- `verify_exact.py` — separately written standard-library sparse exact matrices
  over \(\mathbb Q(\sqrt2,\sqrt3,i)\), including the GHR comparison.
- `verify_tensor_words.py` — matrix-free abstract Pauli-word certificate;
  no matrices.
- `verify_concurrent_equivalence.py` — independent exact
  \(\mathbb Q(\sqrt2,\sqrt3,i)\) encoding of the two concurrent operators,
  intrinsic quaternionic factorization, site swap, and displayed local unitary.
- `verify_braid_link.py` — separate exact intrinsic/comparison, enhancement,
  skein, local-order, two- and three-strand link, standard-frame witness,
  Clifford, reversal, and Garside checks.
- `run_all.sh` — runs all five routes.
- `test_failure_modes.py` — optimization and deliberate-mutation tests.
- `verify_checksums.py` — portable, path-safe package-integrity verifier.
- `verification_output.txt` — frozen output from the release run.
- `concurrent_equivalence_output.txt` — frozen standalone output of the new
  comparison route.
- `braid_link_output.txt` — frozen standalone output of the global
  braid-and-link route.
- `.python-version` and `requirements.txt` — pinned interpreter and
  hash-locked dependencies.
- `VERIFICATION_ENVIRONMENT.md` — reference toolchain and commands.
- `SHA256SUMS` — self-contained package-local hashes. It deliberately does not
  hash itself or repository website mirrors.

## Submission and licensing

- `LICENSE` — package-level dual-license notice.
- `LICENSE-MANUSCRIPT.txt` — CC BY 4.0 manuscript/documentation license.
- `LICENSE-CODE.txt` — MIT verifier/runner code license.
- `CITATION.cff` — v1.2.0 citation metadata with the reserved version DOI.
- `HIGHLIGHTS.txt` — Journal of Algebra highlights.
- `package_submission.py` — deterministic source/PDF/arXiv artifact builder.
- `submission/` — generated locally by `package_submission.py`; deliberately
  not nested inside the public source ZIP.

## Local-only operational materials

The private workspace retains `ZENODO_DEPOSIT.md`, `ARXIV_METADATA.md`,
`SUBMISSION_CHECKLIST.md`, and `JOURNAL_OF_ALGEBRA_COVER_LETTER.md`. These
handoff and strategy documents are intentionally absent from the public
source ZIP and its internal `SHA256SUMS` allowlist.

## Repository website mirrors

- `docs/papers/exceptional-ybe-d4/index.html` — article page outside the
  curated package tree.
- `docs/papers/exceptional-ybe-d4/paper.pdf` — byte-identical public PDF
  outside the curated package tree.

These deployment mirrors are updated in the repository, but they are excluded
from the self-contained source archive and its internal `SHA256SUMS` file.

Temporary downloaded sources, rendered pages, TeX intermediates, virtual
environments, and caches live under ignored or untracked temporary paths and
are not part of the package.
