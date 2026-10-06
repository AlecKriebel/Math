# PR97 novelty and disposition audit

**No demonstrably new research contribution has been established. Closing PR97 without publication is mathematically honest. The defensible reason is that the ordinary smooth result is a classical corollary of prior results, while novelty of the explicitly qualified regularity supplement is unestablished. A bare `already_solved` label would overstate the evidence if it means that an earlier exact full-scope answer or historical resolution has been authenticated.**

This bounded audit verifies disposition, not a new solution. It reads the repaired current candidate and contingent short note, not a claim that their text occurs in the original submitted head. Central proof-search turns: **0**; original2/5 and extra0 are preserved. No Git, PR, QUEUE, service, manuscript, or prior-evidence write was performed. Internal agent reporting is the only communication made; there was no outreach.

## Exact target and distinction

The actual 2002 Calegari preprint, printed p.29, makes Question13.2 conditional on a choice of defining form whose connection form is contact. It inherits a minimal taut C2 foliation on an atoroidal three-manifold with nonzero Godbillon–Vey evaluation. Its Question13.1 separately concerns attaining a weak sign. Our claim does not construct such a form or solve Question13.1. The ordinary fundamental-class evaluation supports the closed oriented interpretation used by the candidate, but the source does not explicitly settle all regularity/compactness conventions there. Its full final2003 chapter was not read. [Primary source](https://arxiv.org/abs/math/0209081v1).

The audited ordinary theorem is: on a closed oriented smooth three-manifold, if a cooriented taut C2 foliation without spherical leaves has a global nonvanishing C1 defining form alpha and a **smooth contact form omega** satisfying `d alpha = alpha wedge omega`, then `ker omega` is tight in the usual smooth sense. It covers the standard smooth interpretation of the conditional question, with weaker extraneous hypotheses than the question.

The longer candidate also treats **C1 omega**, proving (i) every sufficiently C1-close smooth contact form is tight, and (ii) no embedded C2 disk has Legendrian boundary and tangent planes distinct from the contact planes along that boundary. The short note's theorem expressly omits those extras. Neither artifact identifies this disk criterion with every other low-regularity definition of tightness.

## Checkable covering map

| Candidate content | Prior coverage or direct check | Disposition |
|---|---|---|
| Contact path for integrable, possibly nonclosed alpha | Dathe–Khoule2012 Definition2.1/Theorem2.2, printed102–103, already allows C=1,B=t and nonnegative mixed coefficient | Known contact mechanism; closedness and strictly positive first variation are unnecessary |
| Zero mixed coefficient under the Godbillon–Vey relation | Direct consequence of the given relation and d squared=0 | Simple specialization of that criterion, no distinct mechanism |
| Tightness for smooth omega and alpha | Same contact path + ET neighborhood theorem + finite smooth Gray | Standard derived corollary of previously established results; exact earlier printed Question13.2 conclusion not located |
| Smooth omega with C1 alpha | Smooth approximation on one fixed finite contact interval; openness preserves contactness and the endpoint neighborhood | Routine regularization of the preceding corollary |
| Every nearby smooth contact eta is tight, for C1 omega | Same finite-interval approximation applied to eta+s a | Verified additional argument relative to the literal criterion; historical novelty unestablished |
| No stipulated C2 overtwisted disk for C1 omega | Simultaneous disk/form smoothing with a boundary correction | Verified qualified supplement; exact prior statement not located, which does not prove novelty |
| Existence of contact omega, or weak-sign attainment | Not proved by any row | Remains outside this conditional implication |

I independently re-read the original2012 transcription's definition, theorem, and expansion, and the relevant2025 primary-paper reproduction. The original assumes integrability and its inequality admits zero. The2025 text explicitly attributes a C1 version to2012; the original transcription itself does not print an explicit C1 threshold. [Original article transcription](https://www.researchgate.net/publication/258228980_Sur_les_deformations_d%27un_feuilletage_de_codimension_1_en_structures_de_contact), [2025 reproduction, Theorem6.2](https://arxiv.org/abs/2503.00454v1).

Independent dimension-three check, with `V = omega wedge d omega`:

```text
omega wedge d alpha = omega wedge alpha wedge omega = 0,
0 = d(d alpha) = d(alpha wedge omega) = -alpha wedge d omega,
Q = alpha wedge d omega + omega wedge d alpha = 0,
(alpha+t omega) wedge d(alpha+t omega) = t^2 V,
(omega+s alpha) wedge d(omega+s alpha) = V.
```

For C1 forms, `d squared alpha=0` holds distributionally; the product has a continuous classical derivative, so its vanishing distribution gives the pointwise identity. The same planes occur after multiplying `omega+s alpha` by `1/s`, with `t=1/s>0`. On a compact manifold these planes approach the foliation uniformly. A **finite** endpoint lies in the ET tightness neighborhood; smooth Gray along a finite contact path transfers its tightness to omega. For C1 alpha, approximate it by smooth a on that fixed interval; no low-regularity Gray theorem is assumed. The contact-volume error is bounded by `2 B delta + delta^2` when form and derivative errors are at most delta, so a positive compact lower bound preserves contactness. Negative sign is handled componentwise by orientation reversal.

These imports are explicit primary-paper statements: Vogel2011 p.42 and Dathe–Rukimbira2008 Proposition3.3 give the tightness neighborhood; Vogel2016 Theorem2.9 gives smooth Gray. Dathe–Rukimbira2008 Proposition3.4 already uses a near-foliation/contact-path tightness argument for a **closed** defining form. That narrower proposition alone does not establish the nonclosed case. [Vogel2011](https://doi.org/10.2140/gt.2011.15.41), [Dathe–Rukimbira2008](https://arxiv.org/abs/0812.3389v1), [Vogel2016](https://doi.org/10.2140/gt.2016.20.2439).

The2025 normalized-equality display after its Eq.(62) omits the mixed coefficient in general; the correct normalized quantity is `V+(C/B)Q >= V`. Here Q=0, so equality is correct. Original2012 uses the inequality correctly. That typo and unrelated source results do not invalidate this independently checked specialization.

## What the regularity supplement adds

In the longer candidate's lemma, let smooth theta_j approach a C1 theta and smooth disk embeddings D_j approach a C2 D. In fixed smooth tubular coordinates, reparametrize each boundary as a graph gamma_j(t). Its failure of the Legendrian condition is `q_j(t)=theta_j(gamma_j'(t))`. The derivative contains only first derivatives of theta_j and second derivatives of gamma_j, so q_j tends to0 in C1. Subtract `q_j(t) chi(u-u_j(t),v-v_j(t)) dt`. Its C1 norm tends to0, it annihilates the boundary tangent exactly, and contactness and strict boundary transversality persist. This would produce arbitrarily close smooth overtwisted forms, contradicting the nearby-smooth tightness assertion. I found no gap in this bounded check.

This is an explicit regularization proof that the affine criterion does not literally print. Calling it **our written supplement** is accurate. Calling it **a proven novel theorem** is unsupported. First-derivative openness, smooth approximation, Gray stability and boundary correction are standard tools; an earlier exact statement was not located in the inspected sources. Vogel2016 already defines contact structures as C1 plane fields (Definition2.2); merely using C1 forms cannot itself certify a new regularity threshold. Conversely, known tools alone do not logically prove that every exact consequence has already appeared or has no possible scholarly value. I am not proving a universal negative about the literature.

## Recommended disposition and wording

Recommend **close without publication: no established novel contribution; known mechanism/classical corollary in the audited ordinary smooth conditional scope**. The positive correctness findings can be retained as research notes. A lack of novelty is a sufficient reason to decline publication even when no proof error exists; the older root adjudication's `mathematical_failure_or_reason_to_close_PR=false` does not rule out this new novelty-based disposition.

If the workflow defines `already_solved` as **already implied by established results**, that label is defensible only with an explicit scope-qualified reason. If it means **an authenticated earlier exact full-original-problem resolution**, the label is not established. A bare global status may be consumed without its qualifying text, so the more conservative disposition leaves the queued original problem's global historical status unchanged and records the PR closure reason precisely. Root reports the native target row as queued0/5; this audit does not independently inspect or change that row.

Concrete closure reason suitable for a record:

> Closing without publication. The ordinary smooth conditional result is a classical corollary of Dathe–Khoule's 2012 affine criterion, the Eliashberg–Thurston tightness neighborhood theorem, and smooth Gray stability. The C1-form/C2-disk supplement has no established historical novelty. We have not authenticated a literally printed earlier exact answer or a full original-scope historical resolution.

The first sentence about absence of demonstrated novelty is epistemic, not the false stronger assertion that no part can possibly be new. Closing on this basis is honest and does not require locating a literal earlier answer. Publishing an explanatory note could be a separate human choice, but this audit supplies no new-research priority clearance.

## Limitations and source locators

This is a bounded audit conditional on the classical imported theorems, not a reproof of ET or Gray. It uses an author-uploaded original2012 transcription, not original PDF pixels/publisher issue; the prior root audit records the publication authentication. It does not verify all results in the2025 preprint. The final2003 Calegari chapter, full ET book, final Dathe–Rukimbira2011 body and other previously identified literature gaps remain unread. The repaired candidate is not certified as the original submitted commit. No wrapper/PDF audit was repeated.

Checkable borrowed-input locators (hashes in INPUTS.json):

- Calegari cached text: lines1432–1477, especially Question13.2 lines1476–1477; initial tautness convention lines32–33.
- Original2012 reconstruction retains web markers L491–L529 (definition/criterion) and L662–L679 (expansion/inequality); fresh public opens at requested lines490 and653 corroborated these excerpts.
- KMNW2025 cached text: lines1620–1699 (reproduction and C1 attribution).
- DR2008 cached text: lines240–258 (Propositions3.3–3.4).
- Vogel2011 cached text: lines54–62 (ET statement); Vogel2016 cached text: lines408–419 (C1 convention), lines547–548 (Gray).
- Candidate Sections1–4; short note Theorem1 and final scope discussion; preceding audit REPORT/OWN_ANALYSIS and root adjudication were read as context, with the above primary passages and derivations checked independently.
