# Release manifest

This manifest describes version 1.1.0, tagged
`exceptional-ybe-d4-v1.1.0`.

## Mathematical sources

- `main.tex` — paper source.
- `build_paper.sh` — reproducible Tectonic build command.
- `output/pdf/exceptional_ybe_d4.pdf` — typeset paper.
- `README.md` — construction and reproducibility overview.
- `PRIORITY_AUDIT.md` — primary-source novelty and equivalence audit.
- `REVISION_AUDIT.md` — adjudication of the independent revision proposals.
- `RELEASE_NOTES_v1.1.0.md` — version-specific change and scope record.
- `SOURCE_SNAPSHOT.md` — provenance and hashes of supplied inputs.
- `RESEARCH_LOG.md` — timestamped audit and publication log.

## Verification

- `verify_supplied.py` — byte-for-byte preserved user attachment; SymPy.
- `verify_exact.py` — independent standard-library sparse exact matrices
  over \(\mathbb Q(\sqrt2,\sqrt3,i)\).
- `verify_tensor_words.py` — independent abstract Pauli-word certificate;
  no matrices.
- `run_all.sh` — runs all three routes.
- `verification_output.txt` — frozen output from the release run.
- `requirements.txt` — pinned dependency for the supplied checker.
- `SHA256SUMS` — release hashes, including byte-identical public copies.

## Public page

- `docs/papers/exceptional-ybe-d4/index.html` — article page in the
  repository root.
- `docs/papers/exceptional-ybe-d4/paper.pdf` — byte-identical public PDF.

Temporary downloaded sources, rendered source-paper pages, TeX build files,
and caches live under ignored or untracked temporary paths and are not part
of the release.
