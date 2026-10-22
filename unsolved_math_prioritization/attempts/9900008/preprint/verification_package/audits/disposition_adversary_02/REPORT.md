# Independent adversarial review of the repaired PR883 disposition

Audit scope: PR883 / PID9900008 only. Frozen original source head: `af25d26e21945a1a132aace5e600485152777070`. The 26 attempt-source files, including the two ZIPs, match the supplied source manifest byte for byte. The QUEUE row is separate in the PR metadata. Original proof-search effort remains **1/5**. This audit neither adds a proof-search turn nor changes status.

## Decision and exact scope of approval

**ISSUES: two repairable disposition/presentation points; the mathematical and source account passes.** I independently verified the periodic counterexample and the full old-input implication before reading the final priority reports. No substantive mathematical gap was found. Historical first recognition, exact periodic-formula priority and worldwide current openness remain unestablished. Neither a positive novelty finding nor a claim that a named prior source already announced the target theorem is justified.

Retaining the existing `claimed_solved` label while completing a faithful, fully credited package is a reasonable conservative operational action. I do **not** recommend reclassification to `already_solved` on the present record. The repaired proposal should nevertheless avoid silently turning historical recognition into a new necessary condition in the user's definition of `already_solved`. Its global credit contract should also explicitly include the 2023 parallel-line obstruction. The two exact corrections below resolve the issues without new research or a status mutation.

This is a disposition gate only. It does not approve the current historical package as a publishable preprint, certify a future paper's exact bytes, or substitute for the two NEW successive whole-package adversarial reviews required after repairs and sealing.

## Required correction 1: status rationale must remain an interpretation, not an added definition

Loci: repaired disposition lines 15–19. The sentence making the relevant bibliographic question an **earlier recognized resolution** is too categorical. The user's wording is:

- `claimed_solved`: “we believe we have a full resolution of the open problem”.
- `already_solved`: “the open problem was not actually open and we found a priority audit issue”.

The user did not define `already_solved` as requiring an explicit prior recognition event, nor require novelty or firstness for `claimed_solved`. A complete elementary corollary of old theorems is strong evidence against a *new-discovery* claim, but it is not automatically documentary evidence of an earlier resolution event. Conversely, failing to locate such an event is not a certificate that the question was actually open when this work began. The supplied definitions leave the treatment of an unannounced elementary old-input corollary interpretive. A disposition should acknowledge this boundary instead of resolving the ambiguity through an unstated recognition requirement.

The existing label may be preserved on the narrower, affirmative ground that the exact historically posed question has a full verified answer here, with no user-supplied novelty requirement. That permits the conditional requested work to proceed without asserting current openness or disregarding the prior-implication priority finding. It does not license keeping a label after new evidence genuinely establishes the user's excluded category.

Suggested replacement substance for lines 15–19:

> The complete old-input deduction establishes the negative answer and defeats any claim of a new mathematical discovery. It does not establish a prior explicit recognition event, and the absence of such a located event does not establish current openness. The user's definitions do not expressly decide how to classify an unannounced elementary corollary of old results. Preserve the current `claimed_solved` status on the limited ground that a full answer to the exact historical source question is verified and the user supplied no novelty requirement. This is an operational status decision, not a finding of worldwide openness, firstness, or priority clearance. Do not reinterpret `already_solved` as requiring historical recognition. Any later genuinely established non-`claimed_solved` status triggers the user's immediate exclusion rule.

The note may give a decisive negative answer to the problem **as historically posed**, with the complete classical implication prominent. It can therefore satisfy the user's demand for a decisive answer without claiming that the problem remained unresolved until this work. The final title, abstract, metadata and tracker description must not use phrases such as “previously unresolved until this work”, “first solution”, or “new resolution”. The repaired proposal already prohibits these stronger implications; preserve that prohibition. No extra novelty requirement or new approval question should be invented.

This is a wording/inference correction, not a finding that the theorem is false, a recommendation to close the sound PR, or authorization to process any excluded PR.

## Required correction 2: complete the direct primary-source credit contract

Loci: repaired disposition lines 9, 27 and 37. The mandatory global requirements name LT2009, LT2014/2015 and KM2025 but omit **Last–Thorisson (2023), Section 8 and Remark 8.1**, which the final recent report explicitly requires. This paper contains the directly relevant canonical Poisson parallel-line construction and identifies the invariant-direction obstruction. Its result concerns balancing two stationary measures, so it must not be described as directly stating the target self-preserving-law counterexample.

Add to the mandatory credit bullet and primary-source list:

> The continuous invariant-direction obstruction for canonical diffuse parallel-line measures is explicit in Last–Thorisson (2023), Section 8 and Remark 8.1. Khezeli–Mellick (2025), Remark 3.2, explicitly identifies the product/atomic-quotient allocation reduction. These are balancing-existence results; the target's full negative characterization corollary follows from LT2009 Example 7.1, LT2014v1/LT2015 Proposition 1 and the displayed allocation-transfer proof.

A current priority notice and concise note should carry this credit directly. The final reports' reference links alone should not be the only place it appears. This does not require changing any frozen historical file or following its reference to another repository PR.

## Independent periodic proof check

Let `nu = sum_n delta_n + 2 sum_n delta_(n+1/2)` and `mu=lambda_1 tensor nu` on R². The observable phase space is R/Z, the action adds the vertical translation modulo one, X is constant and Q is the point mass at phase zero. The phase-to-measure map is continuous and injective; compactness gives a Borel inverse onto its canonical orbit. Thus no extra state information supplies randomness. Local finiteness, nonzero mass, singleton diffuseness and root support all hold. Singularity and the stabilizer R×Z are allowed by the source assumptions.

An arbitrary pointwise-covariant allocation has the displacement representation `tau_u(s)=s+pi(theta_s u)`. At phase zero every light source line is translated by the same `(a0,b0)` and every heavy line by `(a1,b1)`. Its pushforward is the horizontal Lebesgue factor times the vertical two-family translated measure. Preservation at the sole Q-supported state therefore gives the finite **per-period** identity

    delta_[b0] + 2 delta_[1/2+b1] = delta_0 + 2 delta_1/2.

Positivity excludes targets outside the two support residues. A collision gives mass three at a target; a swap gives incorrect weights. Thus `b0,b1` are integers. There is only one light source family per period, so a weight-two target cannot be made from two independently movable light families. No injectivity assumption is made. The root displacement belongs to R×Z and fixes the complete observed state. This proves universal allocation invariance even if preservation is demanded only Q-a.s.

For the defining joint mass experiment with `C=[0,1)^2`, the restricted mass is three a.s. and the mass-selected line is heavy with probability 2/3. The measurable statistic `H(eta)=eta([0,1) times {0})` is initially one a.s. and is two with probability 2/3 after the required shift. Hence even a first marginal changes. This disproves the full joint identity; it does not replace that identity with a marginal definition. Pointwise covariance ties the root's displacement to an entire positive-mass line, so a null singleton cannot be arbitrarily reassigned.

The conclusion answers Thorisson's historical Problem 4.1 and LT2009 Problem 7.5 in the specified original-state measurable class. It says nothing contrary to the positive one-dimensional or density results, free/no-invariant-direction variants, background-augmented tests or the neighboring all-Markov question. A fractional Markov kernel can move the light family to the heavy one and split the heavy family, defeating this allocation-only law. The repaired boundary language is sound.

## Independent full prior-implication check

For a base measure zeta on R^d, let `J(zeta)=zeta tensor lambda_1` and make the added coordinate act trivially on the entire observable state. For **any** product-state displacement with components `a(zeta),b(zeta)`, pointwise covariance forces

    tauhat_zeta(s,u) = (rho_zeta(s), u+b(theta_s zeta)),
    rho_zeta(s) = s+a(theta_s zeta).

Tonelli and translation invariance of Lebesgue measure give, for Borel A and an interval I of positive finite length,

    (tauhat_*(zeta tensor lambda_1))(A times I)
      = |I| (rho_* zeta)(A).

Thus product preservation implies base preservation, with no bijectivity, finite-preimage, regularity or freeness assumption. At the root the extra displacement acts trivially, so every product test is covered by base allocation invariance. The argument is not restricted to selected lifted rules.

The canonical-space details also check. J is continuous for the vague topologies, by integrating a compactly supported continuous test over the extra coordinate. The cylinder map `D(eta)(A)=eta(A times [0,1))` is measurable and locally finite; `DJ` is the identity. The product image is the invariant Borel equalizer `eta=J(D(eta))`. Rules pulled back or extended with zero displacement off this image are measurable; their covariance-generated allocations are identity off image. There is no hidden larger observable sigma-field or unmeasurable selection.

LT2009 Example 7.1 can be taken on R with independent Poisson components and unequal irrational weights. Every allocation measurable from their weighted sum is a rule on the source's full pair state, so the source's stronger invariance passes to the sum factor. Failure remains observable from the root atom's weight. Almost surely disjoint simple configurations allow the weighted sum to recover both types, though this stronger recovery is not needed to pass invariance to the factor.

For a product window, projection of the complete joint mass-stationarity identity through D and the base coordinate of U+V recovers the base identity. Hence failure reflects to the product. LT2014v1 Section 8 Proposition 1 expressly states the product equivalence; v2 retains it. The v1 proof's `[0,1)` versus `[0,n)` window typo does not affect its statement, and v2 has the consistent n-window. The needed reflection also follows directly from the product-window experiment just described.

Combining the old atomic example with this transfer proves the **entire unrestricted existential diffuse negative conclusion**. This is stronger than sharing ingredients, and no unsupported central theorem remains. It establishes neither the date/person of first recognition nor prior appearance of the exact rational periodic formula. The repaired proposal correctly keeps those questions separate.

## Primary-body and report readback

The following extracted bodies were read in full: the supplied Thorisson note; LT2009 arXiv0906.2062; LT2014v1 arXiv1405.7566v1; LT2015v2 arXiv1405.7566; KM2025 final; and, after the initial independent reconstruction, the supplied LT2023 v2 body. Key original pages were visually checked: Thorisson pp5–6; LT2009 pp9,18,22–24; LT2014v1 p14; LT2015v2 pp14–15; KM2025 final pp1333–1334. Source binaries and extracts remain private. The 2014/2015 edition dates come from the arXiv edition headers, not later generated title-page dates.

Primary links: [Thorisson note](https://cms.dm.uba.ar/depto/public/Some%20Open%20Problems-preprint.pdf), [LT2009](https://arxiv.org/abs/0906.2062), [LT2014v1](https://arxiv.org/abs/1405.7566v1), [LT2015v2](https://arxiv.org/abs/1405.7566v2), [LT2023](https://arxiv.org/abs/2112.13053v2), [KM2025 final](https://alea.impa.br/articles/v22/22-51.pdf).

The final classical and recent priority reports were read only after `INDEPENDENT_RECONSTRUCTION.md` was saved. Their mathematical full-implication conclusions match the independent calculation. Their failure to locate an explicit named earlier answer remains bounded evidence, not an exhaustive literature or current-openness certificate. I did not reperform their searches or authenticate inaccessible sources. The old disposition proposal was read only as explicitly rejected history; it supplies no present policy authority. No sibling disposition adversary was read.

## Faithful continuation and exact remaining gates

After the two local corrections, the following disposition is supported: keep the existing eligible label and 1/5 effort unchanged; prepare a short, fully credited answer to the historically posed question; retain the frozen original evidence; and make the full classical corollary route govern every current canonical description. Do not call this a newly discovered general resolution. The note may be useful analytically without a novelty certificate.

No status change, PR comment, closure, merge, paper creation, deposit, DOI, sheet entry, external contact, other-chat access, other-PR access, Git action or new central proof search occurred in this subaudit. All writes are within this auditor's assigned folder. The statement that the live PR remained unchanged is based on the supplied frozen gate and parent's instruction; this auditor did not re-query live state.

The actual paper and portable verification package do not yet exist in reviewed final bytes. They must undergo presentation repair, parent sealing and two NEW successive whole-package adversaries. Those reviews must include current code/guard trust, exact metadata, credits, scope, proof and reproducibility. This audit is not either of those reviews. If a non-`claimed_solved` status is genuinely established later, the user's prohibition applies immediately; this audit authorizes no work on any such PR.

Remaining mathematical gap: none found for the stated negative theorem or old-input implication. Remaining priority gap: historical first explicit recognition and exact periodic-formula priority. Remaining disposition repairs: the two corrections above. This disposition subaudit is complete (100%); completion of the overall PR process is not asserted.
