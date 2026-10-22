# Acceptance report for problem 2497 and Erdős Problem 1110

Date: 11 October 2026. Outcome: **the mathematical partial result passes within the corrected scope recorded below.** PROOF.md supplies a complete corrected standalone argument. This is not acceptance of a full solution, novelty claim, or exact inspection of Yu–Chen's theorem.

## Reviewed versions

The earlier candidate was independently hashed at SHA-256 411b603d21ef2ec8ed592dc982f0acd99e857fd588a9b1dac9ef6d49d595d274 (3,292 bytes) and remains unchanged. The complete corrected proof in PROOF.md is preserved byte-for-byte from the accepted audit, at SHA-256 9ffee49c0f6746c495a1db6c10ca2198e946c67d64e03b5b08c86c7427412118 (9,717 bytes). The separately frozen correction is identified below and in SOURCE_PINS.json.

## Required correction

The hypotheses permit composite, coprime integer bases. Outside the three proved density ranges, the non-(3,2) pairs are exactly

**(4,3), (5,3), (5,2), (7,2), (9,2).**

The candidate lists only the last four. The omitted (4,3) is a real scope omission, not a defect in the bound on the stated ranges. Likewise, when comparing with the tracker's broader coprime-failure attribution, both **(4,3) and (7,2)** are extra pairs outside this density proof. Any claim that only (7,2) is extra must be corrected. These are boundaries of this proof, not a declaration of the entire current literature's unresolved cases.

The separately frozen correction has SHA-256 c1ed8229057061f12977da29ced08357aa90ecba56a8b02e7d173ff4f3dca0d2 (2,137 bytes). CORRECTION.md is its public editorial copy; only workflow and provenance wording has changed, and its own byte identity is recorded in MANIFEST.json. The original correction is included in the audit input checks. The earlier candidate **together with that correction** is accepted within the boundaries below.

## Mathematical checks

1. Nonnegative integer exponents, finite sets, positive summands and coprime bases greater than one are the exact hypotheses used. Primality is unnecessary. Valuations at one prime divisor of each base prove the divisibility/product-order equivalence and uniqueness of exponent pairs.
2. Every summand of a represented integer at most N is at most N. The exponent rectangle is therefore a valid overcount even though it contains individually overlarge products and sets with overlarge sums.
3. An s-element antichain chooses s distinct coordinates on each axis and has a unique decreasing matching. The resulting binomial-sum identity is exact. Collisions of antichain sums do not invalidate the upper bound.
4. The binomial-theorem bound includes the constant 1/[t(1−t)]. Floors only decrease the exponents. Exact integer inequalities verify every strict logarithmic comparison; the narrow p=11,q=2 margin is positive.
5. The conclusion concerns the count of **representable** positive integers. It gives natural density zero for that set and natural density one for its complement. The reversed imported background is erroneous.
6. For every fixed M, numbers coprime to M have positive density. Removing a density-zero set still leaves arbitrarily many. Taking M=pq times all prior choices produces pairwise-coprime failures, each coprime to pq. M may change between induction steps; no uniform-in-M estimate is needed.
7. The classical (3,2) induction is supplied separately for completeness. Nothing in the density proof establishes the five other exceptional pairs.

Local finite arithmetic and antichain checks support the audit. They do not replace the analytic proof or establish an asymptotic theorem by finite computation. The mathematical argument and exact inequalities are supplied in PROOF.md.

## Primary-source and attribution audit

- Erdős–Lewin, *d-Complete Sequences of Integers*, Mathematics of Computation 65(214), April 1996, 837–840: the actual five-page facsimile was checked. Its first PDF page is a JSTOR cover. PDF pages 2, 3 and 5 correspond to printed pp. 837, 838 and 840. The definition uses nonnegative exponents; p. 837 gives the classical (3,2) induction. Printed p. 838 states failure propagation under multiplication by either coprime base. Printed p. 840 asks about density and infinitely many coprime failures. It supplies no density direction for the present ranges. The comma in the displayed two-base set on p. 840 is read in the context of the paper's product set, not adopted as a union-of-powers hypothesis.
- Yu–Chen, *On a conjecture of Erdős and Lewin*, Journal of Number Theory 238 (September 2022), 763–778, DOI 10.1016/j.jnt.2021.09.018: publisher metadata identifies a published research article, with an open-archive label. Its abstract describes partial answers to two questions and an affirmative answer to another conjecture. That does not identify the latter as a full solution of Problem 1110.
- The publisher's direct article and abstract URLs returned HTTP 403 during this audit. The inherited 195-byte HTML object is an unusable stub, not a paper or usable theorem text. Full Yu–Chen PDF bytes, theorem number, exact theorem hypotheses, and proof inspection remain **unverified**. There is no PDF hash to report for that paper.
- A search-indexed copy of the Erdős1110 tracker, checked today, attributes the three zero-density representability ranges to Yu–Chen and additionally credits coprime failures for (4,3) and (7,2). This is secondary attribution and is labelled as such. The index displayed a last edit of 1 April 2026; direct live access returned HTTP 403. Its listed open status is not proof of the absence of later literature. The present analytic proof is independent of that status and of the unavailable paper.

Public citations and source byte pins appear in SOURCE_PINS.json and PROOF.md. Source documents, source text, page images, raw search results and datasets are not reproduced in this packet.

## Acceptance boundary

Accepted: the three stated quantitative ranges; zero density of representables; density one of failures; the pairwise-coprime sequence consequence; and the imported density-direction correction.

Corrections incorporated here: the exceptional list and the description of the two extra tracker-attributed coprime cases. The separately pinned correction addresses both, and PROOF.md states the corrected scope.

Not accepted or claimed: a full resolution of Erdős1110, novelty, a proof of density in any of the five uncovered pairs, exact Yu–Chen theorem inspection, or an exhaustive present-day literature-status determination.

This proof reconstruction, audit and editorial preparation were AI-assisted. No external human review or formal proof-assistant certification has been obtained. Acceptance here denotes the bounded mathematical audit described above; it is not peer review or certification. No source-author code was executed.
