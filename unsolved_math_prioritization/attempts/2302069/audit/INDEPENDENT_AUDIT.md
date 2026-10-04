# Independent adversarial audit: Problem 2302069

Date: 2026-10-04 UTC. Rank 566. AMR-022-2069 / Function Theory 2.69.

## Verdict and mandatory queue correction

**PASS as a scoped partial investigation, subject to the queue correction below. The original problem remains unsolved by this packet.**

No mathematical gap was found in the stated auxiliary results after independent adversarial reading. A second mathematical reader independently checked Propositions 3–8 and their dependencies and reached the same conclusion. This is an AI-assisted audit, not human peer review or formal certification. It does not establish originality, a universal positive order threshold, or a family of counterexamples with orders tending to zero.

For publication, the required queue outcome is **Status `unsolved`, Turns `5/5`**, changing **only rank 566's own Status and Turns cells**. The frozen author's proposed literal queue status `partial` in STATUS.json, SOURCE_GATE.md and ATTEMPT_LOG.md is not the campaign queue outcome and must not be copied into the queue. The descriptive term “partial investigation” is mathematically accurate and can remain in the frozen narrative. This audit supplies the queue correction without changing any frozen author file. Preserve every other row and every other cell, including Chat, Findings and DOI. No queue or remote write was performed during this audit.

The five approaches are substantively distinct: a dilation comparison, canonical-product/angular-loss analysis, restricted real-zero geometry, a finite-radius obstruction, and an attempted order-lowering construction. All five remain incomplete for the universal existence question. Their percentage estimates are author judgments, not verified probabilities or quantitative mathematical progress measures.

## Frozen input and reproducibility

The reviewed FROZEN_MANIFEST.json has SHA-256:

`802b73b274b6941a4f93679fef7c0c8e34817d22a9f2f4fc968e10e15bbaceee`

All eight listed author files matched both their recorded sizes and SHA-256 hashes. The manifest deliberately excludes itself and all material outside public/. It makes no integrity claim about the private source receipts. The manifest itself was separately matched against the assignment's expected hash.

Running `python3 public/verify.py` succeeded and reproduced checks.json exactly. A before/after digest comparison established that no frozen file changed. The replay comprises 5,682 finite exact controls:

- Loss/gain scalar identities: 3,721
- Fractional-kernel algebra: 1,271
- Real-zero logarithmic derivatives: 550
- Polynomial identities: 17
- Ramification chain rule: 24
- Dilation stationarity: 99

These finite tests supplement the mathematical arguments. They do not establish universal quantification, interchange of infinite limits, Hadamard factorization, or asymptotic claims. The 16,384-point midpoint quadrature is unvalidated floating-point illustration. Its sampled minimum cannot certify a minimum on the full circle. The analytic argument in Proposition 7, rather than the samples, supplies that certificate. For c=1 the diagnostic predicted limit ratio is approximately 1.184140444; the N=381 sample is approximately 1.170354837. No finite N is asserted to realize the asymptotic limit. The N=3 ratio below 1 is fully compatible with the stated eventual limiting result.

## Exact question and quantifiers

The packet correctly asks whether one constant d>0 works for every transcendental entire f of upper order strictly below d, with liminf T(r,f)/T(r,f') at most 1. Neither a lower-order-dependent estimate approaching 1 as the lower order tends to zero, nor a varying family with better behavior, answers that quantifier pattern.

The upper-order restriction is strict. Known counterexamples for each order above 1/2 imply that any successful d is at most 1/2. A counterexample of order exactly 1/2 would not alone rule out d=1/2. The packet does not confuse these boundary cases. Under order below 1, Proposition 5 independently proves L(f)>=1, so the requested inequality there would be equality; this stronger reformulation does not settle existence of d.

## Mathematical review

### Lemmas 1–2 and Proposition 3: lower-order comparison

The Poisson majorant gives the stated maximum-modulus/characteristic bound. Taking nonzero Taylor coefficients of arbitrarily high degree proves T(r,F)/log r tends to infinity for a transcendental entire function, uniformly in the sense needed to absorb the subsequent logarithmic errors. The derivative is also transcendental.

Cauchy's derivative bound and radial integration compare the two characteristics at fixed dilations in both directions. Fixed dilations do not change upper or lower order, and the additive logarithmic term is negligible by the preceding growth result. The asserted equality of the lower orders is therefore justified rather than assumed.

The good-radius lemma is valid: an eventual strict lower dilation bound would, by iteration and monotonicity between geometric radii, force lower order at least sigma. Applying it to T(r,f') yields the bound C(lambda). For a fixed k, one may first take sigma down to lambda and then optimize k; no common sequence for all k is needed for this liminf upper bound.

The stationary equation lambda/k=2/(k^2-1) has the displayed unique positive admissible root. For lambda>0 the objective tends to infinity at both ends and exceeds 1 at every k, so its attained minimum is strictly above 1. For lambda=0 the infimum is 1. Sending lambda to zero is not an allowed substitute for establishing a result for every function below some fixed positive upper order. The packet explicitly recognizes this gap.

### Propositions 4–5: forward proximity and angular loss

The stated genus-zero Hadamard factorization and zero summability are standard foundational inputs; they are not proved in this packet. Given (5), absolute summability of reciprocal zeros follows from p<1. The logarithmic derivative expansion then converges normally away from the zeros.

The uniform angular kernel estimate is sound, including when the circle passes through a zero. Its local singularity has exponent p<1 and is integrable. Scaling produces the summable majorant A_p|a_n|^(-p). For each fixed zero the integral tends to zero; dominated convergence over the zero index is justified by that summable majorant. Subadditivity for 0<p<1, passage to the convergent series away from finitely many circle zeros, and Tonelli's theorem for the nonnegative majorant justify the integral estimate. Thus the forward proximity tends to zero along all radii, not merely outside an exceptional set.

The loss/gain identity is exact. Gain is bounded by forward proximity, whereas the loss need not be small. Writing x=T(r,f')/T(r,f) gives x=1-B_f/T(r,f)+o(1), with 0<=B_f/T<=1. Therefore limsup x=1-liminf B_f/T; the reciprocal relation gives L(f)>=1 and equivalence (10), including the extended case limsup x=0. No illegitimate exchange of liminf with a reciprocal occurs. An o(1) upper estimate for f'/f supplies no lower bound against cancellation. The packet correctly leaves the normalized angular-loss estimate open.

### Proposition 6: real-zero subclass

For nonreal z, every real-zero summand has imaginary part of the same sign. The normally convergent series preserves this fact. A chosen zero at 0 is covered by m>=1; a nonzero chosen zero is covered by one summand, and multiplicity only strengthens the bound. A zero exists because a zero-free entire function of order below 1 would be constant by the stated factorization.

The resulting lower bound for |f'/f| gives the displayed reciprocal proximity estimate. Since (r+|a|)^2/r>=1 for r>=1 and |sin theta|<=1, taking logarithmic positive parts introduces no missing term. The two real-axis points have measure zero, and log(1/|sin theta|) has the finite mean log 2. Combining the O(log r) reverse estimate with the o(1) forward estimate and transcendental growth proves a full limit equal to 1. Rotating a line through the origin preserves both characteristics, since the derivative gains only a unit-modulus scalar. Arbitrary noncollinear zeros are outside this theorem.

### Proposition 7: normalized varying-polynomial obstruction

The geometry w=1-z=2 cos(t) exp(it) correctly parametrizes the shifted unit circle, with the origin handled separately. If |w^N-1|<1/4, then 3/4<|w|^N<5/4 and the claimed logarithmic bound follows. The modulus bound forces |t|>pi/4. On the interval joining |t| to pi/3 the absolute derivative of log(2 cos t) is at least 1, so the phase N|t| is within log(4/3) of N*pi/3. For N=3 mod 6 the latter is an odd multiple of pi; hence Re(w^N)<0, contradicting Re(w^N)>3/4. This proves the global 1/4 bound, independently of quadrature.

Except at the two points |w|=1, the normalized numerator has limit c+u^+. Its nonnegative values are bounded by c+log 2+(log 2)/N. The derivative's normalized logarithmic positive part is bounded by c+(log N)/N+log 2, hence by a constant for N>=3. These bounds justify both dominated-convergence steps, including the logarithmic singularity of u at theta=0. The displayed positive limiting gap follows pointwise on u<0, a set of positive measure. The limiting denominator is strictly positive because u>0 on a set of positive measure.

Crucially, N varies and the radius remains 1. Every F_N is a polynomial. This is a valid obstruction to the particular local inference from minimum modulus and F_N(0)=0; it is neither a transcendental entire counterexample nor a fixed-function r-to-infinity counterexample. The packet's warning is essential and accurate.

### Proposition 8: ramification

The angular substitution proves the exact characteristic identity. The derivative multiplier has constant circle modulus q*r^(q-1)>=1, which yields both bounds without an omitted sign condition. Its logarithm is negligible relative to T(r^q,f') by Lemma 1. Thus the derivative characteristic changes by a relative o(1), preserving the liminf ratio even if that liminf is infinite. Substitution R=r^q ranges over all sufficiently large radii. Both orders multiply by q.

The coefficient criterion for a reverse single-valued entire substitution is correct. Rotation averaging can enforce that criterion but does not preserve the needed lower characteristic bound; an odd entire function averaged over z and -z indeed vanishes. The construction angle cited from Langley collapses at order 1/2, but this is only a limitation of that method. It does not prove impossibility of different constructions.

## Source provenance and limits

All four local source copies matched the byte counts and SHA-256 hashes in SOURCE_MANIFEST.json. The selected numeric dataset record also matched exactly against the full pinned corpus, independently of the author's extracted record. A hash identifies retrieved bytes; it does not establish authority or redistribution rights. No source PDFs, page images, dataset corpus, or raw connector receipts are part of this audit's publication deliverables.

- **Hayman–Lingham:** Independently opened the primary arXiv PDF, checked Problem and Update 2.69, and visually inspected printed pages 48–49. These confirm the exact question and the above-1/2 update. The 2018 update does not establish exhaustive present-day open status. Source: [Research Problems in Function Theory, version 2](https://arxiv.org/pdf/1809.07200v2).
- **Langley:** Independently inspected the local text through the complete relevant Sections 2–4 and visually checked Theorem 2 and Lemma B on printed page 153. The theorem, proof architecture, and angle restriction agree with the packet. Keldysh/Mergelyan approximation inputs were not independently reproved. The DOI open failed in this audit, but the independently located official Cambridge record confirmed the statement, DOI and February 1993 bibliographic metadata; the PDF masthead says 1992. Source: [Cambridge publication record](https://www.cambridge.org/core/journals/proceedings-of-the-edinburgh-mathematical-society/article/on-the-deficiencies-of-composite-entire-functions/96E57199482C34AE16CAFFCD9C139440).
- **Toppila:** Independently read the four-page local extracted text. Scanned formulas have OCR corruption; the exact numerical constant was not independently certified or used. The historical order-one result is corroborated by the primary problem collection and Langley. The DOI destination returned a bot-check page. Source PDF: [Original four-page paper](https://www.acadsci.fi/mathematica/Vol03/vol03pp131-134.pdf).
- **Dataset/catalogue:** The pinned corpus supplies identity and wording, while generated research/status labels remain non-authoritative. The matching extracted record omits the Langley update from its statement, making the primary check material. This audit did not bypass or retry the catalogue access denial. Source: [Pinned dataset](https://huggingface.co/datasets/ulamai/UnsolvedMath/blob/372682f27c1b0d3d39e75fa63ad7932c7a2e1bde/problems.json).
- **Repository history:** Reviewed the saved evidence for the pinned main/queue, untruncated 112-entry root tree, 54-entry attempts tree, 652-entry problems tree, and actual desk-review record. The recorded trees have no matching ID/title paths, and the desk review is only a suggested approach. This audit did not independently recreate every remote code, branch, commit, PR or history search and does not certify exhaustive absence of prior attempts. The author's disclosed failed full-directory fetch must remain a limitation.

The evidence supports publishing an honestly scoped unrefereed partial investigation. It does not support “solved,” “already solved,” novel-result priority, complete literature coverage, or formal verification. The source gate already discloses those limits; retain them with this audit.

## Publication boundary

Keep the author packet frozen and publish this audit separately if publication is otherwise authorized. Apply the own-row queue correction to `unsolved`, `5/5` in the publication operation, rather than changing any hashed author artifact. No merge, release, DOI deposit, external correspondence, or source redistribution is authorized or performed by this audit.

AUDIT_RESULT.json records the replay and provenance checks. AUDIT_SHA256SUMS.txt binds this report, the result file, and the frozen author artifacts. Its own digest is reported separately to the parent.
