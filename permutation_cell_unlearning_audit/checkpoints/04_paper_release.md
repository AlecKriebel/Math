# Checkpoint 4 — Paper Release

**Date:** 2026-07-28  
**Status:** PASS after proof, scope, numerical, and visual adversarial review

## Released manuscript

**Title:** *Permutation-Cell Auditing: Target-free falsification of all-order
retrain equivalence in sequential machine unlearning*

- Source: `paper/paper.tex`
- References: `paper/references.bib`
- Final PDF: `output/pdf/paper.pdf`
- Length: 12 US-letter pages
- PDF SHA-256:
  `9de53aaae3639dcaaaa152c508c5880c4cc3c3d633367e456614496dcda34979`

## Review result

The paper received three independent final PASS verdicts:

1. proof fidelity and numerical consistency;
2. novelty boundary, quantifier scope, and reviewer recognizability; and
3. source/PDF/JSON synchronization, build reproducibility, and page-by-page
   visual quality.

The release review itself caught and repaired a conclusion quantifier
inversion, stochastic-table target-semantics error, missing directional-failure
actions, ill-typed set unions, and one overlapping first-pass diagram.

## Defensible solved claim

For a fixed observed family of externally equivalent deletion-order outputs,
PC-Audit gives the sharp population lower bound on worst-route distance to
every otherwise unconstrained common reset target. A certified lower bound
above tolerance falsifies the universal all-order target claim without
computing the target. A finite-sample bounded-kernel specialization supplies a
conservative stochastic rejection rule with family-wise error control.

The result is a one-sided falsifier, not a successful-forgetting certificate.
The case study demonstrates mathematical usefulness and reproducibility, not
deployed-system prevalence.
