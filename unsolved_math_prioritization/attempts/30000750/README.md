# 30000750 — Reduced Length and Mahler-Measure Inequality

**Result:** already solved in the literature. **Turns:** 1/5. **Novelty claim:** none.

`PROOF.md` contains the complete deduction of the exact target from Dobrowolski (2012), Theorem 2.1. `SOURCE_CHECK.md` records the primary source, the later theorem, literature limits, and duplication checks. `APPROACH_LOG.md` records the approach and adversarial checks. `PROVENANCE.json` pins retrieval evidence without redistributing source texts.

## Reproduction

From this directory, with Python 3.10 or later and no third-party packages:

```sh
python3 check_controls.py > /tmp/30000750-control-results.json
cmp control_results.json /tmp/30000750-control-results.json
```

The controls use exact rational arithmetic: 21,420 product inequalities, 27 equality cases, one zero-polynomial case, and two hypothesis-deletion negative controls. They are finite sanity checks, not a universal proof, and they do not calculate an infimum over multipliers. The universal proof uses the stated published theorem.

From this attempt directory, verify the final-layout public manifest with `sha256sum -c SHA256SUMS`; from `independent-audit/`, verify the original audit delivery with `sha256sum -c AUDIT_SHA256SUMS`. The public manifest excludes itself. Scholarly PDFs and full dataset corpora are not part of this package.

## External-proof boundary

Acceptance is at the published-theorem dependency level. The full independent audit documents printed linear-algebra defects in the 2012 source and checks a local algebra/regularity repair without certifying the entire deformation argument. No complete independent re-proof or novelty claim is made. See `independent-audit/AUDIT.md` for the full caveat. The corrected proof uses exactly the audit's editorial notation patch. `CORRECTIONS.diff` records all changes from the initial seven-file freeze; that original freeze is preserved separately.

To rerun the independent finite controls from this directory:

```sh
python3 independent-audit/independent_controls.py > /tmp/30000750-independent-results.json
cmp independent-audit/independent_controls.json /tmp/30000750-independent-results.json
```
