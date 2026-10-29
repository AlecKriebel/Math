# Final adversarial review of the closure assessment

Review date: 2026-10-28. Reviewer: independent statistical adversary. Reviewed `CLOSURE_PLAN.md` against `STATISTICAL_CLOSURE.md`, `CODE_AUDIT.md`, and `SCIENTIFIC_CLOSURE.md`. This review concerns promotion of the **assessment**, not promotion of any docking or biological result.

## Verdict: PASS for the stated assessment scope

No blocking correction is required in `CLOSURE_PLAN.md`. It correctly identifies the committed evidence as an incomplete implementation rather than a completed benchmark; separates site discovery, pose recovery, and assay-backed specificity; and does not promise universal biological closure.

The plan preserves the statistically material caveats:

- The 24–36-complex / 12-family proposal is an initial inventory rather than a power guarantee.
- The 12/12 illustration is explicitly an independent-binomial calculation and is not misrepresented as a confidence interval for fractional family-macro scores. Its stated two-sided 95% lower bound, 73.5%, agrees with `0.025^(1/12) = 0.7353515306`.
- Seeds, poses, and symmetry copies are not counted as independent biological replications.
- Reliability decisions require prespecified useful-performance boundaries and uncertainty; inconclusive results remain possible.
- Candidate-pool absence is not mislabeled as a proven internal sampling failure.
- Structural decoys do not replace tested nonbinding alternatives; missing specificity evidence remains an exact open gap.
- A validated counterexample refutes an absolute guarantee without implying universal algorithm failure or low average performance.
- Novelty distinctions are described as candidates requiring an overlap audit rather than proven novel contributions.

## Requirements before a future confirmatory study

These are implementation/preregistration requirements, not defects preventing publication of this assessment:

1. Choose exact estimands, confidence procedures, confidence levels, independent-unit assumptions, family definitions/weights, and utility floors or improvement margins. Specify how multiple separate confirmatory claims are controlled. A family bootstrap with very few families, especially all-success observations, must not be the sole basis of an assurance claim.
2. Freeze cohort eligibility, handling of unsupported chemistry and missing output, specificity label uncertainty/censoring, assay prevalence, and all denominator definitions. Retain both workflow-level coverage and conditional accuracy.
3. Make any sample-size enlargement or sequential stopping rule valid before examining confirmatory outcomes; the plan already prohibits chasing a favorable interval.
4. Verify the newly cited preprint and public assay data at exact versions and establish actual usable data availability before claiming they supply the required cohort. The plan appropriately treats their relevance as conditional.

The exact empirical gap remains unchanged: valid references and assay labels, repaired and independently checked code, frozen held-out execution, and sufficiently precise reproducible results. The assessment has not closed that gap and does not claim to have done so.
