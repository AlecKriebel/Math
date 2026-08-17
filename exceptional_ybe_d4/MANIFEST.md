# Release manifest

This manifest describes submission package version 1.1.3, dated 16 August
2026. It is prepared for deposit through a fresh manual Zenodo record, not a GitHub
release or a pre-existing DOI family; `ZENODO_DEPOSIT.md` governs reservation
and insertion of its dedicated version DOI before publication.

## Mathematical sources

- `main.tex` — paper source.
- `build_paper.sh` — reproducible Tectonic build command.
- `output/pdf/exceptional_ybe_d4.pdf` — typeset paper.
- `README.md` — construction and reproducibility overview.
- `PRIORITY_AUDIT.md` — primary-source novelty and equivalence audit.
- `REVISION_AUDIT.md` — historical adjudication for version 1.1.0.
- `RELEASE_NOTES_v1.1.0.md` — prior version's historical release record.
- `RELEASE_NOTES_v1.1.1.md` — prior submission-hardening record.
- `RELEASE_NOTES_v1.1.2.md` — prior frontier-review record.
- `REVIEW_ADJUDICATION_v1.1.2.md` — historical itemized disposition of the
  two frontier-model reviews and adversarial re-audit.
- `RELEASE_NOTES_v1.1.3.md` — current correction and package-refresh record.
- `CORRECTION_AUDIT_v1.1.3.md` — source-checked disposition of the latest
  review and the final adversarial re-audit.
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
- `run_all.sh` — runs all three routes.
- `test_failure_modes.py` — optimization and deliberate-mutation tests.
- `verify_checksums.py` — portable, path-safe package-integrity verifier.
- `verification_output.txt` — frozen output from the release run.
- `.python-version` and `requirements.txt` — pinned interpreter and
  hash-locked dependencies.
- `VERIFICATION_ENVIRONMENT.md` — reference toolchain and commands.
- `SHA256SUMS` — self-contained package-local hashes. It deliberately does not
  hash itself or repository website mirrors.

## Submission and licensing

- `LICENSE` — package-level dual-license notice.
- `LICENSE-MANUSCRIPT.txt` — CC BY 4.0 manuscript/documentation license.
- `LICENSE-CODE.txt` — MIT verifier/runner code license.
- `CITATION.cff` — citation metadata without an invented DOI.
- `HIGHLIGHTS.txt` — Journal of Algebra highlights.
- `ZENODO_DEPOSIT.md`, `ARXIV_METADATA.md`, and
  `SUBMISSION_CHECKLIST.md` — exact handoff instructions and portal fields.
- `package_submission.py` — deterministic source/PDF/arXiv artifact builder.
- `submission/` — pre-reservation artifacts and their outer checksums; rebuild
  them after inserting the reserved DOI, as required by `ZENODO_DEPOSIT.md`.

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
