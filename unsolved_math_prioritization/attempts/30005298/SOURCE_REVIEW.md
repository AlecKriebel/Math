# Exact-source and scope audit

Checked 10 October 2026, approximately 10:27–10:39 UTC. This is an authored audit, not a statement that an external referee accepted any new result.

## Problem identity and exact target

- Numeric ID: 30005298. Alias: **OWR-11695864-003**.
- Title: Dimensions of General Weddle Loci.
- Original question: OWR 54/2022, printed p. 3103 (PDF p. 11), Question 1. The definition is on printed p. 3102 (PDF p. 10). It takes the closure of the outside-Z locus where the dimension of degree-d cone forms jumps above its generic minimum.
- The adjacent Question 2 concerns arbitrary projective three-dimensional systems of quadrics and Weddle quartic characterization. It is a different target and is not resolved or used here.

## Primary sources and current status

1. Luca Chiantini, “Generalized Weddle loci,” OWR 54/2022, printed pp. 3102–3104. Official source: https://doi.org/10.4171/owr/2022/54 ; PDF https://ems.press/content/serial-article-files/46990 . Original definition, Question 1, the neighboring Question 2, and the report's source references were read in context.
2. Chiantini, Farnik, Favacchio, Harbourne, Migliore, Szemberg and Szpond, *Weddle schemes*, https://arxiv.org/abs/2606.25060v1 . The arXiv landing page checked during the historical source review exposed v1, submitted 23 June 2026, and no later version. The theorem text, proofs and surrounding material in Sections 1–7 were inspected from the retained PDF/text, with the central Sections 3 and 5 read in detail; the appendices were read for target separation. Large displayed matrices were inspected as part of the representation discussion, not independently recomputed from their printed entries. The current HTML was also checked: https://arxiv.org/html/2606.25060v1 . No verified later full resolution or journal publication was found in the bounded searches. This is a preprint, not an externally accepted resolution.
3. The original OWR reference [3] is the same authors' *Configurations of points in projective space and their projections*, https://arxiv.org/abs/2209.04820 . Its primary landing page was checked for provenance. The present source review does not claim a full independent audit of that book's proofs. The hypersurface regime was already reported as known in OWR; the 2026 paper is not credited with first discovering that result here.

The accompanying mathematical audit accepts the partial dimension conclusions at their stated scope. Historical literature status, search snippets and source-reported random computations are not treated as proof of a full all-parameter solution. No exhaustive current-literature or priority certification is made.

## Source claims versus what this edition proves

Let N=binomial(d+n−1,n−1) in ambient P^n. In P^3 write N=binomial(d+2,2) and q=binomial(d+2,3).

- [WS] Theorem 3.2 uses ambient P^{n+1} and r=binomial(d+n,n), with degree binomial(d+n,n+1). Reindexing gives r=N and degree binomial(d+n−1,n) in ambient P^n. The abstract's ambient/index wording is inconsistent with the theorem; it was not used as a formula. Theorem A independently proves dimension n−1 in this regime and makes no degree claim.
- [WS] Theorem 5.1 claims generic uniqueness of the degree-d projected curve on each component at r=N in P^3. Its proof uses an inductive point-deletion/general-position assertion. The proof does not assume that assertion and does not require accepting that proof.
- [WS] Proposition 5.2 claims the N+1 locus is an ACM curve of degree binomial(q,2). This corrects the degree formula quoted by the original OWR report; for d=3 the new value is 45 versus the older 52. Theorem A independently establishes dimension 1 but does not assert the degree, ACMness, or reducedness.
- [WS] Proposition 5.3 at N−1 is explicitly conditional on codimension two. The displayed degree binomial(q+1,2) and ACM assertion may not be treated as unconditional before that hypothesis is established. Theorem B supplies an independently audited proof of the locus-dimension assertion, for all n≥3,d≥2, with no scheme-degree conclusion.
- [WS] Conjecture 5.4 is still presented as a conjecture in the current primary text. Remark 5.5 states small cases d=2,3,4, with the latter two obtained by random computer calculations and semicontinuity. Historical verification produced seven exact finite-field certificates, including independent witnesses for those cases and d=5, but the uniform proof is the incidence-and-factor argument, not finite sampling.
- [WS] Proposition 5.6 claims a zero-dimensional N+2 scheme of degree binomial(q,3). Theorem A independently proves nonempty dimension zero, without a degree claim.
- [WS] Proposition 5.7 correctly exhibits secant lines in the N−2 locus, ruling out the naive expected codimension three in P^3. Our P^3 dimension corollary is compatible with this obstruction; expected codimension alone is not accepted as an answer.
- [WS] Section 5.5 distinguishes curve and isolated contributions for eight general points. Our classification is only of maximum dimension and does not remove or classify isolated components.
- [WS] Remark 7.1 reports a computer calculation for eight general points in P^4, with a degree-35 curve and a degree-7 residual after the 28 secants. This is a specific source-reported regime inside the conservative residual range; the present work does not reverify that entire scheme calculation.
- [WS] Appendix B concerns projection to rational normal curves, a different prescribed-target condition. Its surface assertion is not a theorem for every d-Weddle hypersurface jumping locus.

## Authored source-reading correction

An earlier authored reading said that Conjecture 5.4 displayed “expected dimension.” That reading was wrong and is withdrawn. The source wording is “expected codimension, namely 2.”

Original-resolution visual inspection and OCR of the retained page images, a fresh rendering of the hash-matched PDF, its extracted text and the primary arXiv HTML agree on codimension. A same-resolution fresh rendering was byte-for-byte identical to the earlier retained image. No source-image discrepancy, source change or current-paper typo is established. No cause for the earlier incorrect reading is inferred.

The defensible source account is that Conjecture 5.4 asks for codimension two and remains presented as a conjecture in the inspected version. The correction concerns the authored reading; it changes no formula or mathematical argument in [PROOF.md](PROOF.md). Public PDF identities and historical inspection methods appear in [SOURCE_METADATA.json](SOURCE_METADATA.json); no source text or images are distributed.

## Accepted partial result and remaining boundary

The accepted partial argument is the common-factor-stratified pencil upper bound: for r=N−1 and n≥3,d≥2, the jumping locus has dimension n−2. A common-factor pencil is counted only after bounding how many general original points can lie on its lower-degree factor cone. The exceptional n=3,d=2 calculation uses the sharper no-four-coplanar bound. Monotonicity then gives the whole subcritical dimension range in P^3. Supercritical dimensions are proved independently by a cone incidence and projective intersection argument, with centers in Z excluded by a separate boundary count.

The all-n problem stays OPEN. In particular this edition does not claim an all-parameter answer for n≥4 and the lower-cardinality regime. It makes no novelty, journal-acceptance or external-human-peer-review claim. Source text, dataset contents and private coordination material are not distributed.
