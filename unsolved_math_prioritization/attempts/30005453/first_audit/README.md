# Independent review of subcritical reinforcement

The original frozen candidate passes the analytic audit for its precisely
stated strictly positive-equilibrium theorem, including almost-sure coordinatewise
convergence and vertex rates with no positive uniform lower bound.

Literal uniqueness among all nonnegative equilibria is false. The audit requires
the author description to identify positivity as an explicit corrected scope,
rather than a verified statement of the primary source's intention. A minor
initial-count equation reference also needs correction. A proposed v2 and exact
delta are bound here, but their acceptance requires a separate delta review.

## Contents

- AUDIT.md: complete analytic adversarial review and exact verdict
- CORRECTIONS.md: two required editorial corrections
- RESULT.json: machine-readable verdict with scope and exclusions
- SOURCE_CHECK.json: fresh source retrievals, inspection, and search limits
- PRIOR_WORK_CHECK.json: independent read-only repository checks
- results/provenance.json: full-corpus, catalog, source, and review-hash checks
- results/independent_checks.json: 56 independently rebuilt rational cases,
  2,168 base checks, and additional endpoint/fractional-exponent controls
- results/author_replay.json: separate replay of the author's diagnostic code
- PROPOSED_V2.diff, PROPOSED_V2_DELTA.json, PROPOSED_V2_BINDING.json: proposed
  editorial revision; not self-accepted by this reviewer
- code/: standard-library-only reproducible verification tools
- MANIFEST.json: safe-artifact file integrity and allowlist

## Reproduction

From this directory:

    python3 code/replay_audit.py

To recheck the original author ZIP and its archive negative controls:

    python3 code/replay_audit.py --author-zip /path/to/SUBCRITICAL_REINFORCEMENT_30005453_AUTHOR_SAFE_FREEZE.zip

The optional provenance verifier requires the two complete public corpus files,
the complete public catalog, and the three scholarly PDFs as private inputs:

    python3 code/verify_provenance.py --corpus-dir /path/to/corpora --catalog /path/to/catalog.json --scholarly-dir /path/to/pdfs --output /path/to/result.json

No source PDF, image, extracted source text, raw corpus, private source, or private
coordination file is included. Hash/size and inspection metadata are included.
The analytic proof is not certified by these finite programs. There is no claim
of novelty, publication, or external specialist acceptance. No remote writes
were performed in this audit.
