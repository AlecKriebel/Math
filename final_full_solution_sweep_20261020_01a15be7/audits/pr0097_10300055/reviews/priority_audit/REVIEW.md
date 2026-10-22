# Independent priority and provenance audit of PR97 / 10300055

Timestamp: 2026-10-21T01:15:40.243956+00:00

**Disposition: NO NOVEL-PUBLICATION CLEARANCE.** The conditional smooth tightness claim has a checkable classical proof. Its affine contact family is literally covered by the 2012 Dathe-Khoule deformation criterion. Tightness then follows from the Eliashberg-Thurston neighborhood theorem and finite smooth Gray stability. The supplied C1-form regularization does not have established priority and is not an independently identified open problem. Preserve the argument as a correctly attributed observation; do not label this audit an independent discovery of a new open-problem solution or create a Zenodo record on this evidence.

This conclusion deliberately distinguishes (i) a direct consequence of published mathematics, which is established here, from (ii) a printed, historically first answer to Calegari's exact Question13.2, which has **not** been located or dated here. Lack of an exact printed match is not evidence of firstness. This is a novelty objection, not a counterexample or a claim that the smooth proof is invalid.

## Independence and boundaries

I read original_head/CANDIDATE.md and corrected_candidate/CANDIDATE.md as requested, treated their bibliographies as leads, and saved INITIAL_ASSESSMENT.md before consulting historical adjudications. I never opened any prior_* verdict, historical closing comment, or other review. I independently retrieved and read the relevant primary sources below. No other ongoing agent or individual was contacted; no shared Git/index/branch, PR, Sheet, or publication was changed. All created files remain inside this priority_audit directory. The root investigator supplied a live GWS duplicate check at01:08Z; I did not reperform or alter that check.

## Original problem and exact scope

Calegari's 2002 version0.78, arXiv:math/0209081v1, printed p.29, places Question13.2 after a minimal taut C2 foliation F of an atoroidal three-manifold with nonzero Godbillon-Vey evaluation. Its global defining form alpha and connection omega satisfy

\[
T\mathcal F=\ker\alpha,\qquad d\alpha=\alpha\wedge\omega.
\]

The conditional question is whether the contact structure ker(omega) is tight when such a contact omega exists. It does not ask for construction of omega: that existence/sign problem is the preceding Question13.1. The closed-oriented setting is the natural interpretation of its ordinary fundamental-class evaluation, not an extra phrase printed in Question13.2. A global nowhere-zero alpha supplies coorientation. I inspected the entire p.29 as PDF pixels as well as extracted text. [Original source](https://arxiv.org/pdf/math/0209081v1).

The candidate's closed cooriented taut setting addresses that conditional question under the usual smooth interpretation of a contact form. Atoroidality and the numerical Godbillon-Vey hypothesis are unnecessary for the argument. Minimality rules out spherical leaves. Nothing here answers the noncompact/boundary case or proves existence of a contact connection form.

## Independent derivation and translation of the antecedent

The identity d squared(alpha)=0, together with d(alpha)=alpha wedge omega, gives alpha wedge d(omega)=0. Also omega wedge d(alpha)=0 and alpha wedge d(alpha)=0. Thus the independently checked expansion is

\[
(\alpha+t\omega)\wedge d(\alpha+t\omega)
=t^2\omega\wedge d\omega.\tag{A}
\]

For every t>0 this is contact, of omega's sign, and ker(alpha+t omega) converges uniformly to T(F) as t decreases to0 on compact M. The rescaled form omega+s alpha, with s=1/t, is the same family of planes. A finite contact path connects omega to a sufficiently near-foliation member. In the smooth case, the latter is tight by the taut-foliation neighborhood theorem, and Gray stability transfers tightness. There is no need to apply Gray at the integrable endpoint.

**Exact specialization of Dathe-Khoule.** Their Definition2.1, printed p.102, permits alpha_t=C(t)alpha+B(t)beta, where C is positive and continuous at0 with C(0)=1, and B is nonnegative, continuous, strictly increasing with B(0)=0. Their Theorem2.2, pp.102-103, says an integrable nonsingular alpha on a compact positive-contact (2n+1)-manifold (V,beta,Z) admits this affine deformation precisely when

\[
\alpha\wedge(d\beta)^n+n\beta\wedge d\alpha\wedge(d\beta)^{n-1}\ge0.\tag{DK}
\]

For n=1, beta=omega, both summands vanish individually. The allowed C(t)=1, B(t)=t gives exactly (A). Their expansion includes the complete mixed term and the t-squared contact term. Hence the construction is a literal zero-mixed-term specialization, not a new deformation mechanism. [Author-uploaded original-article transcription](https://www.researchgate.net/publication/258228980_Sur_les_deformations_d%27un_feuilletage_de_codimension_1_en_structures_de_contact).

The article is H. Dathe and C. Khoule, *Sur les deformations d'un feuilletage de codimension1 en structures de contact*, African Diaspora Journal of Mathematics13(2),100-107(2012). I read its primary author-uploaded transcription, not its PDF pixels. The site distinguishes publication year2012 from author upload21August2026. Its original publisher PDF remains an access gap.

**Independent later primary reproduction.** Khoule-Manso-Ndiaye-War, arXiv:2503.00454v1 (1March2025), Theorem6.2 and proof, pp.32-33, reproduce (DK), explicitly attributing it to Dathe-Khoule in the C1 setting. Their Remark6.3 calls these CB-deformations. Their displayed equality after Eq.(62) omits a generally nonnegative mixed term: in general it must be an inequality. This typographic/algebraic issue does not affect the present zero-mixed-term specialization, which I verified directly in (A). I make no endorsement of that preprint's unrelated results. [Primary preprint](https://arxiv.org/pdf/2503.00454v1).

## Tightness argument: antecedent versus new ingredient

Vogel2011 printed p.42 explicitly states that any contact structure sufficiently C0-close to a taut foliation on a closed3-manifold is symplectically fillable and tight, attributing the theorem to Eliashberg-Thurston. This is the universal-neighborhood statement required by the proof, not just existence of one tight approximation. [Vogel, *Rigidity versus flexibility for tight confoliations*](https://msp.org/gt/2011/15-1/gt-v15-n1-p03-p.pdf).

Dathe-Rukimbira's author preprint arXiv:0812.3389, p.5, Proposition3.3 states the same neighborhood result and points to *Confoliations* p.50. Proposition3.4 already uses the argument “small deformation is near a taut foliation, then isotopy transfers tightness” for a closed nonsingular defining form alpha0. Closedness is a real restriction: it is not the present general integrable case. Their Proposition3.2 supplies a stronger form-isotopy statement in that closed setting. I use these as a method antecedent, not as a theorem literally covering arbitrary d(alpha)=alpha wedge omega. [Primary preprint](https://arxiv.org/pdf/0812.3389).

Vogel2016, Theorem2.9, printed p.2451, states smooth Gray stability on closed manifolds. Its Definition2.2, p.2448, allows C1 contact plane fields; that definition does not itself assert a C1 version of Gray's theorem. [Vogel, *On the uniqueness of the contact structure approximating a foliation*](https://msp.org/gt/2016/20-5/gt-v20-n5-p01-p.pdf).

Combining the literal (DK) specialization with the neighborhood theorem and ordinary finite-interval Gray stability proves the smooth claim without a new hard lemma. This is the positive priority finding: by the established affine theory and classical tightness facts the smooth conclusion is a direct consequence of existing literature. It does not prove the date at which someone first recognized this precise connection to Question13.2.

## C1 regularization supplement

The corrected candidate carefully limits its C1 conclusion to absence of an embedded C2 overtwisted disk with its stated boundary condition, and to usual tightness of every sufficiently C1-close smooth contact form. It does not claim equivalence with all possible notions of low-regularity tightness. That qualification matters.

The regularization argument uses a fixed compact parameter interval. Uniform positivity in (A) survives sufficiently small C1 approximations alpha->a and omega->eta. The smooth path eta+s a then has a tight endpoint and is tight throughout by smooth Gray. If the original C1 form had a C2 overtwisted disk, C2-smooth approximation of the embedding followed by the small boundary correction q_j(t)chi(u-u_j(t),v-v_j(t))dt gives a smooth contact form with an exactly Legendrian boundary and preserved boundary transversality. This contradicts the preceding neighborhood of smooth tight forms. I see no obvious priority-bearing new mechanism here: compactness, openness of contactness, smooth approximation, and a local boundary correction suffice.

The preexisting affine criterion is explicitly attributed in C1 regularity in the 2025 primary source. Thus merely lowering the regularity of the pencil is not new. The additional disk-preserving smoothing lemma is not literally the same statement as (DK), and I have not located a source printing this exact supplement. Its originality is therefore **unestablished**, not disproved. It cannot independently justify presenting the original smooth open question as a new solution. A paper built around that extra statement would need a clearly established new theorem, relevant established low-regularity definitions, and a separate novelty case.

## Broader searches, negative evidence, and access gaps

Searches included: Godbillon-Vey plus tight/contact/tightness; Calegari Question13.2; contact connection form; affine/linear/CB deformation; Dathe-Khoule; Dathe-Rukimbira; and contact Anosov/Godbillon-Vey terminology. Primary leads checked included Calegari's 2012 characteristic-classes exposition, the 2025 contact-symplectic-pair paper's reproduction of the Dathe-Khoule criterion, and the deformation discussion in Massoni's 2024/2026 contact-pair work. Those did not supply a located exact printed answer to Question13.2. These are bounded search observations, not an exhaustive priority theorem.

Sources supporting those bounded checks:

- [Calegari's author exposition,2012](https://lamington.wordpress.com/2012/02/21/characteristic-classes-of-foliations/).
- [Drame-Khoule-Ndiaye,2025, Theorem1](https://onlinelibrary.wiley.com/doi/full/10.1155/jom/6799367).
- [Massoni, arXiv:2405.15635v2](https://arxiv.org/html/2405.15635v2), introduction's approximation/deformation discussion.
- [Massoni, arXiv:2608.29989v1](https://arxiv.org/html/2608.29989v1), Section3.2.6.

Still unread: the final2003 AMS Calegari chapter (DOI10.1090/pspum/071/2024640; AMS returned403); the original Dathe-Khoule PDF pixels; *Confoliations* in full; the full2012 Khoule thesis/2016 CB monograph; the full paywalled2025 paper on pairs of confoliations; and a complete forward-citation search across subscription mathematical databases. I do not claim these sources contain a resolution. They prevent a positive claim that the historical exact application is novel or was still open in2026. Outside expert input could help with this historical gap; under the independent-research policy no outreach was prepared or initiated.

## Duplicate and publication status

The supplied live GWS check found the known Godbillon-Vey-number publication and pure-braid publication to be different results; it found no same-result row for this conditional tightness theorem. Those findings are supplied context, not independently revalidated by this reviewer. The successful public Zenodo search at this audit time returned five Godbillon hits, including the distinct existing Godbillon-Vey-number paper10.5281/zenodo.23357329; none represented this tightness theorem. Exact identifier/title queries returned no hit. Results are recorded in PUBLIC_ZENODO_SEARCH_FINAL.json. Initial API requests used a disallowed public page size100; retries with size25 completed successfully. A negative public text search cannot rule out drafts, differently titled records, or concurrent publication. No publication action is authorized by a no-match result alone.

## Exact remaining gap and recommendation

1. The smooth mathematical conclusion is supportable as a fully attributed classical corollary; absence of explicit recognition in inspected articles does not make its method new.
2. First explicit publication of the Question13.2 application is not established. Source-edition, thesis/book, and citation-chain gaps remain.
3. Novelty of the exact C1/C2-disk supplement is not established and is not part of the original question's usual smooth formulation.
4. Therefore no new original-full-solution Zenodo paper is justified on the current priority record. Preserve the correct proof and antecedent translation in repository research notes; classify the item as a classical deduction with novelty unverified, not as a falsified theorem, and do not silently promote “unverified novelty” into a verified current open-problem resolution.

Audit completion estimate:100% of this bounded independent priority assignment; novelty-publication eligibility remains uncleared. This is not a claim of100% exhaustive literature coverage.
