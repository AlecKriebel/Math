# Independent source-scope review: Cramér–Wold measures with an origin singularity

**Verdict: PASS_CREDITED_SOURCE_CORRECTION. Recommended original-source disposition: already_solved, 0/5 original proof turns.** No mandatory correction. The packet faithfully supplies established sufficient classes and an established nonuniqueness example; it does not supply or claim an exhaustive iff classification of every possible injective measure class.

Reviewed 2026-10-01 UTC by a separate reviewer uninvolved in drafting the packet or deriving its source application. Theorems are credited to Boman–Lindskog and their cited Radon support-theorem literature, not to this campaign. This is not an independent reproof of the full distribution-theoretic support theorems.

## Exact frozen inputs

- `STATUS_CORRECTION.md` SHA-256 `2bbe8f282566f9595da93ae13c11446fbaa3b9a78de116bb9e43acf58fbbcd53`
- Author `MANIFEST.json` SHA-256 `737c644dbf84fa8eab9a59ef89594babcf98d67b976b10ecd870e6fb8283b3c6`
- All nine bound author files match their hashes and byte lengths
- Both complete source PDFs match the source manifest
- The author checker was inspected, then its 130-assertion receipt replayed byte-for-byte
- The separately authored `independent_check.py` passes **350 exact assertions**, checking inverse-power line primitives, endpoints, real density, homogeneity, tail and near-origin integrability, and projective-cone algebra. It is self-contained apart from pre-existing SymPy1.14.0 and has no absolute file dependency. Run `python independent_check.py`

The finite controls verify transcription and elementary algebra only, not the imported analytic uniqueness theorems.

## Source identity and completeness

The pinned statement asks under what conditions a Cramér–Wold uniqueness analogue holds for signed measures with possibly infinite origin mass. It does not explicitly require a necessary-and-sufficient classification. The actual OWR10/2007 contribution, printed pp.582–583, was read, and the p.582 image inspected: its opening question is immediately followed by an announcement of the decay and cone-support answers, along with unrestricted failure. The next page's regular-variation application is not a new unanswered classification bundled into this target.

The full Boman–Lindskog arXiv0802.4373v1 manuscript supplies the relevant measure conventions, Definition1, Theorems2/3a/4, and Section5 counterexamples. The statements of Theorems2–4 were also visually checked. The publisher record independently confirms the 2008 online publication and 2009 journal issue, volume22, pages683–710, DOI10.1007/s10959-008-0151-0. Full final-typeset PDF access was not available, and the packet correctly attributes exact theorem numbers and proof access to the complete author manuscript. Its later PDF compilation date does not change the arXiv version or publication dates.

Thus correcting the imported open-status triage is supported by the exact source passage plus complete primary theorem statements, rather than only an abstract or a similarly titled paper.

## Measure and data domain audit

The locally signed measure is defined on X=R^d minus the origin. Locally finite total variation, even when both signs have infinite variation near zero, is meaningful as an order-zero functional on compactly supported tests in X. The packet never subtracts two globally infinite masses as a finite number.

Finite variation outside every radius-epsilon ball is stronger than local finiteness on X and is required where used. It makes each open halfspace H(omega,p), p<0, absolutely measurable with finite variation. The condition that the **closure** avoids zero is correct; it is not replaced by the weaker assertion that the boundary plane misses zero. Unrestricted one-dimensional pushforwards through zero are not presumed finite.

The conclusion is equality on X. No invisible origin atom or origin-supported distribution is recovered. The example in dimension2 disproves an unrestricted general assertion; it does not assert failure in every dimension, including the elementary one-dimensional case.

## Application of the three credited alternatives

**Rapid tail decay:** Definition1's cutoff norm is equivalent to the stated total-variation tail estimates, since the tail outside r is bounded above by the cutoff norm and the latter by the tail outside r−1. Compact annuli plus a finite distant tail yield finite variation outside each origin ball. The difference of two rapidly decaying measures satisfies the same condition, so Theorem2 applies. There is no missing positivity or near-zero moment hypothesis.

**Common cone:** The packet uses the exact source condition that one common closed cone, minus zero, lies in an open linear halfspace. Its difference measure remains in that cone and has finite variation away from zero, exactly as required by Theorem4. Two unrelated cones are not silently combined; a whole closed halfspace with boundary lines is not substituted for the strict cone. No rapid-decay assumption is added to this alternative.

**Fixed nonintegral homogeneous degree:** The density degree alpha and the measure scaling exponent d+alpha are correctly distinguished. For alpha<−d, the outer-annulus total variations form a convergent geometric series, so exterior integrability follows. Subtraction preserves the same fixed homogeneous degree, allowing Theorem3a. The more general data-homogeneity statement in Theorem3b requires nonnegativity and is correctly not applied to arbitrary signed measures. No universal necessity of these three alternatives is inferred.

The paper permits almost-everywhere halfspace equality; the packet's all-halfspace formulation is a valid, weaker corollary.

## Published kernel example

The real part of z^(−3) is exactly (x³−3xy²)/(x²+y²)³. It is nonzero, smooth off zero, has homogeneous degree−3, and absolute value at most r^(−3). Its exterior total variation in dimension2 is 4/epsilon, finite for every positive epsilon; its variation near zero is infinite. This satisfies the intended finite-away class. The lower-power z^(−2) example would not have an absolutely finite exterior tail, and the packet correctly chooses power3.

Every line at nonzero signed distance p is a constant unit rotation of p+it. The displayed primitive i/[2(p+it)²] differentiates to (p+it)^(−3), with zero endpoints at both infinities. Taking real parts and then applying absolutely justified Fubini over a halfspace with p<0 gives zero halfspace data. Therefore this nonzero signed measure and the zero measure have the same allowed data. Its integer homogeneity, nonrapid tail, and lack of the required strict-cone support do not contradict the cited sufficient classes.

The example belongs to the published complex-power family. It is a reproducible credited illustration, not a new counterexample or author proof turn.

## Publication disposition

The unchanged source correction is suitable for an already_solved0/5 draft for this exact motivating OWR target. Preserve the class-restricted sufficient conclusions, the common-cone and total-variation conditions, the punctured-space conclusion, the absence of an exhaustive iff classification, and the explicit final-PDF access limitation. No further original proof turns are needed to validate this credited source resolution.
