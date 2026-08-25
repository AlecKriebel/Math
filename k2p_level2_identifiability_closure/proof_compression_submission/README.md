# K2P Proof Compression and Submission Reconstruction

This directory contains one bounded proof-compression and article-reconstruction
phase for the principal-domain `K2P-SAME` theorem.  The promoted theorem and
the principal-domain computational-evidence lock rooted at
`../work/final_theorem_release/RELEASE_LOCK.json` are immutable comparison
inputs.  Nothing in this directory changes the theorem statement or the
lock's byte-level authority.

The accepted target is `PC-PARTIAL`: replace ledger-first exposition by safe
finite-universe formulas, explicit polynomial/rank templates, restoration
outcome lemmas, and a general word-reconstruction theorem, while retaining
exact computation for exhaustive family assignment, exceptional rank fields,
direction-preserving transports, and any finite residue that does not admit a
proved quotient in one bounded attempt.

The phase explicitly forbids:

- the revoked rooted tree/sunlet classifier;
- treating ordinary-triangle redirection as a polynomial symmetry;
- unproved inheritance-complement, pole, sink, or source-target symmetries;
- changing the principal positive domain or theorem statement to simplify the
  proof;
- reopening mixed-sign K2P, K3P, or an unbounded invariant search; and
- modifying the frozen computational-evidence lock.

See `FEEDBACK_DISPOSITION.md` for the adversarial review audit and
`RESEARCH_LOG.md` for checkpoints and completion estimates.

## Final bounded outcome

The completed outcome is `PC-PARTIAL`, with zero unresolved mathematical
records. The exact restoration and probe ledgers remain load-bearing and are
not represented as a fictitious hand quotient. Primary reader artifacts are:

- `AI_REFEREE_PROMPT.md`, the neutral post-submission review protocol;
- `article/main.tex`, `article/references.bib`, and the compiled article in
  `output/`;
- `supplement/supplement.tex`, its required `compression_tables.tex` and
  `certificate_appendix.tex` inputs, and the compiled reader supplement in
  `output/`;
- `PDF_BUILD_REPORT.md` and `.json`, recording the final source/PDF hashes and
  the 50-page visual inspection;
- `COMPRESSED_BOUNDED_THEOREM.md`;
- `PROOF_COMPRESSION_RESULT.md` and `.json`;
- `THEOREM_TO_TEMPLATE_CROSSWALK.md` and `.json`;
- `templates/PRINTED_CERTIFICATE_APPENDIX.json` and the generated
  `supplement/certificate_appendix.tex`, with independent replay and mutations;
- `analysis/WEAK_SHARPNESS_COLUMN_CROSSWALK.json`, with independent graph and
  determinant replay;
- `crosswalk/THEOREM_ARTIFACT_CROSSWALK.md` and `.json`; and
- `adversarial_review/ADVERSARIAL_ARTICLE_AUDIT.md`.

From the project root, the compact qualification is:

```bash
.venv/bin/python -B proof_compression_submission/verify_compressed_release.py --check
.venv/bin/python -B proof_compression_submission/verify_old_new_equivalence.py --check
.venv/bin/python -B proof_compression_submission/run_compression_mutations.py --check
.venv/bin/python -B proof_compression_submission/crosswalk/check_revised_referee_bundle.py
```

The submission bundle requires a detached clean-checkout full primitive replay
of the exact source candidate. Its exact commit, layer count, runtime, memory,
report hash, and telemetry hash are recorded externally in
`output/FINAL_CLEAN_FULL_REPLAY.json`,
`output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json`, and the generated crosswalk;
they are not compiled into the five-file source set.

Submission metadata are finalized: corresponding email
`me@aleckriebel.com`; sole-author contribution statement approved; no specific
funding; no competing interests; CC BY 4.0 for the paper and data; MIT for
code; immutable source tag `k2p-same-biorxiv-v1.0.0`. No GitHub Release,
Zenodo deposit, or DOI is claimed in this version.

## Compile-complete bioRxiv source set

The exact text source set consists of five regular files:

- `article/main.tex`;
- `article/references.bib`;
- `supplement/supplement.tex`;
- `supplement/compression_tables.tex`; and
- `supplement/certificate_appendix.tex`.

Preserve the `article/` and `supplement/` directory layout. The supplement
loads its two generated tables locally and uses
`../article/references.bib`. No custom class, style, bibliography-style,
external figure, image, font, or shell-escape asset is required; all diagrams
are inline TikZ and the remaining dependencies are standard TeX-distribution
packages.
