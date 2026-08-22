# K2P Proof Compression and Submission Reconstruction

This directory contains one bounded proof-compression and article-reconstruction
phase for the principal-domain `K2P-SAME` theorem.  The promoted theorem and
the release rooted at
`../work/final_theorem_release/RELEASE_LOCK.json` are immutable comparison
inputs.  Nothing in this directory changes their mathematical or byte-level
authority.

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
- modifying the frozen theorem release.

See `FEEDBACK_DISPOSITION.md` for the adversarial review audit and
`RESEARCH_LOG.md` for checkpoints and completion estimates.

## Final bounded outcome

The completed outcome is `PC-PARTIAL`, with zero unresolved mathematical
records. The exact restoration and probe ledgers remain load-bearing and are
not represented as a fictitious hand quotient. Primary reader artifacts are:

- `article/main.tex` and the compiled article in `output/`;
- `supplement/supplement.tex` and the compiled reader supplement in `output/`;
- `PDF_BUILD_REPORT.md` and `.json`, recording the final source/PDF hashes and
  the 37-page visual inspection;
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

Corresponding email, author-contribution approval, funding,
competing-interests, license, public-tag, and DOI decisions remain explicitly
pending human confirmation.
