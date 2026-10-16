# Reviewed quasi-conical pure point proof

Problem 30005613 / OWR-14297736-021, rank 800.

Independent adversarial AI audit: PASS for the complete existential theorem
in every dimension d≥2. No mathematical correction is required. The result
is not a formal proof certificate, human peer-review report, or historical
novelty claim.

The domain construction chooses both cube widths and shrinking positive
apertures. It produces a connected open quasi-conical Dirichlet domain
with a complete eigenbasis and spectrum [0,∞). It does not address every
preassigned tower or impose a smooth boundary.

## Contents

- author/ preserves the entire frozen author packet byte-for-byte.
- AUDIT.md gives the verdict, all-section review, failure-mode analysis,
  reproducibility results, and exact claim boundary.
- ANALYTIC_CHECKS.md supplies an independent detailed reconstruction of
  the critical analytic steps, including the dimension-two window limit.
- SOURCE_CHECKS.md records primary-source and bounded repository checks.
- acceptance.json is the structured audit disposition.
- verify_independent.py is the portable exact finite checker.
- verification.json records the full replay with optional source inputs.
- verification_portable.json records the self-contained package replay.
- MANIFEST.json lists all other safe files by byte count and SHA-256.

## Reproduce

With Python 3, from this directory:

    python verify_independent.py

This reproduces verification_portable.json: 2,911 exact finite and
integrity assertions, including a byte-identical rerun of the author's
4,187-assertion output. The author assertions are reported separately.

To additionally check the original author ZIP, complete source corpora,
and source PDF hashes, provide independently available input files:

    python verify_independent.py --author-zip AUTHOR.zip \
      --catalog catalog.json --problems problems.json \
      --research-results research_results.json --source-dir SOURCE_DIRECTORY

SOURCE_DIRECTORY must contain paper.pdf, report.pdf, and survey.pdf.
The expected hashes are in verification.json and the checker. The full
replay has 2,944 assertions. These optional external inputs are deliberately
excluded from the package. The program reads them without changing them
or copying their contents into its result.

The code does not verify the infinite-dimensional theorem, solve the PDE,
or compute window widths. Those claims rest on the mathematical proof and
the independent analytic audit. No source PDF, source excerpt, screenshot,
raw corpus, or private coordination record is distributed here. No remote
repository write was part of this audit.
