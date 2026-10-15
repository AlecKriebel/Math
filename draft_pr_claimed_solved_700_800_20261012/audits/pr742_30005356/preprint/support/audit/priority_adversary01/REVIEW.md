# Independent adversarial priority and scope review of PR742

Review date: 2026-10-14 UTC (2026-10-13 America/Los_Angeles). Reviewer: independent adversary01. Frozen PR head: `77be9cbd8b58358919f42c204d9dd829ccd5d60f`.

**Verdict:** No fatal mathematical or literal-source scope problem found in the characteristic-p theorem. A concise note can honestly give a negative answer to the unrestricted integral equality in the inspected printed and versioned sources. Historical priority is unresolved. Final journal wording has not been verified. Promotion is defensible only with those qualifications and the limited theorem stated explicitly.

## Exact audited claim and success criterion

For every prime p and every characteristic-p model (K, theta) of ACFH, the map rho defined by rho(x)^p = x is a parameter-free definable multiplicative-group endomorphism of K* and does not belong to the image of Z[X] under polynomial evaluation at theta. The map extends to a field automorphism commuting with theta. A verified counterexample in any permitted positive characteristic falsifies the equality proposed without a characteristic restriction; it does not classify all definable endomorphisms.

I read the frozen proof directly. Its 10,155 bytes have SHA-256 `f5cd976e4ce93da68cf018fc801b2bcc52b0373693ed798f19bbd8476303ba9b`. `INPUT_RECEIPT.json` identifies its absolute path. I formed and recorded `FIRST_PASS_VERDICT.json` before reading any sibling review conclusions. No sibling mathematical or priority-review conclusions were consulted. I later inspected only the root's bounded Zenodo metadata receipt.

## Source comparison and chronology

The following descriptions are deliberately limited to what the retrieved primary sources establish.

| Source | Verified content relevant to scope | Chronology / limit |
| --- | --- | --- |
| [OWR report 2/2023, printed pp. 97–98](https://ems.press/content/serial-article-files/46996) | Specifies field operations plus theta, algebraically closed fields and multiplicative-group endomorphisms. The displayed polynomial coefficient ring is Z[X]. Its question asks whether every definable endomorphism lies in Z[theta]. There is no explicit characteristic-zero restriction on those pages. | 2023 printed report; January 8–14 workshop. PDF pp. 7–8 visually inspected. |
| [d'Elbée arXiv:2212.02115v4](https://arxiv.org/pdf/2212.02115v4), §5.1, Cor. 5.7, Q. 5.8 | §5.1 defines Endd using first-order definability on K*, with pointwise product and composition. Cor. 5.7 makes integral polynomial evaluation faithful. Q. 5.8 asks equality. The inspected question has no characteristic restriction. | [Version history](https://arxiv.org/abs/2212.02115): v1 Dec. 5, 2022; v2 Apr. 27, 2023; v3 Oct. 17, 2023; v4 Jan. 17, 2025. PDF printed pp. 22 and 25 visually inspected. |
| [Chini arXiv:2607.17014v1](https://arxiv.org/pdf/2607.17014), Thm. 4.10 / Q. 4.11, printed pp. 18–19 | Thm. 4.10 classifies endomorphisms definable in the vector-space/operator reduct. The subsequent warning distinguishes the richer base language, where additional pre-existing definable endomorphisms can supply counterexamples. Q. 4.11 proposes generation also by base-language endomorphisms, and refers to d'Elbée's Q. 5.8. His example is multiplication by pi on a Q-vector space, not inverse Frobenius on K*. | [First posted](https://arxiv.org/abs/2607.17014) July 19, 2026. Both relevant pages visually inspected. |
| [Chini arXiv:2502.13667v3](https://arxiv.org/pdf/2502.13667v3), Rmk. 2.20, printed pp. 16–17 | Discusses multiplicative groups through the Q-vector-space quotient by torsion, explains the need for integral polynomials on the group, and proposes adapting the vector-space framework. The generalization is presented as an expectation, not as a proved classification for ACFH. | [Version history](https://arxiv.org/abs/2502.13667v3): v1 Feb. 19, 2025; v2 June 10, 2025; v3 July 15, 2026. Both pages visually inspected. |

The exact downloaded PDF hashes and sizes are in `SOURCE_RECEIPTS.json`. Local private PDFs, text extractions, and page renders are removed before closure. The hashes identify what was inspected, not the version of record.

## Independent checkable derivation

This derivation checks the mathematical claim rather than assuming that a printed question must be false.

1. Since K is algebraically closed of characteristic p, x -> x^p is surjective. If a^p = b^p, then (a-b)^p = 0, hence a = b. Thus y^p = x defines a unique y without parameters. If x is nonzero, y is nonzero.
2. The equality (rho(x)rho(z))^p = xz and uniqueness give rho(xz) = rho(x)rho(z). Likewise (rho(x)+rho(z))^p = x+z gives additivity. Rho fixes 1 and is bijective, so it is a field automorphism.
3. Multiplicativity of theta gives theta(rho(x))^p = theta(rho(x)^p) = theta(x). Uniqueness gives theta rho = rho theta, including at zero.
4. Let [n] denote x -> x^n on K*. In the endomorphism ring, the integer p denotes [p], not the zero map. If rho = P(theta) for P in Z[X], composing with [p] yields (pP-1)(theta) = 0_E. Faithfulness yields pP-1 = 0 in Z[X]. Its constant coefficient is p a_0 - 1, impossible for an integer a_0.

Faithfulness can also be checked without relying on a classification theorem. Given nonzero Q = sum b_i X^i of degree d, choose algebraically independent t_0,...,t_d over K and an algebraic closure L of K(t_0,...,t_d). On the subgroup generated by K* and t_0,...,t_(d-1), define theta_L(c product t_i^m_i) = theta(c) product t_(i+1)^m_i. Laurent-monomial independence makes this well-defined. Divisibility of L* permits extension of this homomorphism to all of L*: the extension follows by adjoining one group element at a time and choosing a root if some positive power already lies in the previous domain, followed by Zorn's lemma. Then Q(theta_L)(t_0) = product t_i^b_i differs from 1. The existential statement asserting such a nonzero witness transfers to K by existential closedness. For d = 0 only the original subgroup K* is needed; t_0 still witnesses the nonzero constant polynomial. Negative coefficients are group inverses and cause no issue.

This avoids circularly presuming the classification being challenged. It uses existential closedness for extensions in the base theory, not a finite-field computation. It has no saturation requirement. Positive-characteristic instances exist by applying the model-companion embedding to a base model of that characteristic; the characteristic is preserved under field extension.

## Adversarial scope checks

**First-order definability versus rational morphisms.** The graph y^p = x is definable in the pure field language. It is not a rational function of x: if r(X) in K(X) obeyed r(X)^p = X, the X-adic valuation would give p v_X(r) = 1, contrary to v_X(r) being an integer. The inspected ring uses first-order definability, so absence of a rational formula does not disqualify rho. A separately restricted algebraic-group/rational-morphism question would be different.

**Characteristic-zero intent.** Motivation using nonstandard power functions on C may suggest a characteristic-zero research interest. It does not change the stated unrestricted model class. The note should state exactly which unrestricted assertion it falsifies and leave any intended characteristic-zero assertion open.

**Localized coefficients.** Because [p] is invertible, adjoining rho yields a faithful copy of Z[1/p][X] in End_def(K*): P/p^n maps to rho^n composed with P(theta). Clearing powers of p verifies equality and injectivity. This inclusion is strict over Z[theta]. No surjectivity onto the full definable endomorphism ring follows.

**Chini's mechanism versus this exact result.** On K*/Tor(K*), rho induces the Q-scalar 1/p, already in the vector coefficient ring. On K*, prime-to-p torsion prevents arbitrary Q-scalars, although [p] is invertible. Excluding rho from integral Z[theta] on the full group remains essential. Chini's vector-reduct theorem does not supply this exclusion; his related base-language warning deserves citation. The inspected passages do not present rho or the full exclusion argument. This limited finding neither proves priority nor exhausts his work.

## Final-publication access and bounded priority search

The [author's public publication page](https://choum.net/~chris/page_perso/) links this paper to arXiv and an Elsevier article endpoint. Its journal link `https://authors.elsevier.com/sd/article/S0168-0072%2825%2900003-X` returned HTTP 403 in the web tool. The DOI open and ordinary ScienceDirect open also failed to yield full text. No denial workaround, alternate identity, authentication bypass, or rate-limit workaround was used.

Successful [Crossref DOI metadata](https://api.crossref.org/works/10.1016%2Fj.apal.2025.103554) confirms APAL 176(4), 103554, issue April 2025; the DOI record was created January 16, 2025 and deposited February 24, 2025. It advertises version-of-record text-mining links but does not provide the text itself. Successful [OpenAlex metadata](https://api.openalex.org/works/https://doi.org/10.1016/j.apal.2025.103554) lists the publisher and arXiv, with no separate accepted-manuscript repository location. Successful HAL exact-DOI and exact-title requests returned zero matches. The author page and [Modnet index](https://modnet.imj-prg.fr/preprints/) point to the preprint; neither establishes final-text identity. Metadata differences in dates do not establish a correction.

No independently accessible final or accepted manuscript was retrieved, and no correction was identified in the bounded searches recorded in `SEARCH_SCOPE.json`. Neither result establishes that the final journal statement is unchanged, that no correction exists, or that no earlier answer exists. A final/accepted manuscript or an authenticated correction record could materially improve this comparison. No outreach is prepared or initiated.

After preserving my independent first-pass verdict, I read the root's Zenodo receipt. Its nine successful bounded requests contain 32 distinct record IDs; unsuccessful initial size-50 requests are not negative evidence. This corroborates search coverage only. It does not certify priority. `ROOT_REGISTRY_RECONCILIATION.json` records the source hash and interpretation.

## Material findings, repair, and allowed promotion language

There is no verified fatal problem for the exact theorem. The following are material restrictions on presentation:

- Do not describe the result as a classification of all definable endomorphisms, a solution of the characteristic-zero case, or a proof of equality with Z[1/p][theta].
- Do not assert first historical priority, lack of an earlier solution, or that the journal question remains unchanged/currently open. Current full-text comparison is incomplete.
- Cite Chini's related distinction and explain the full-group versus quotient/vector-reduct boundary. Do not claim originality for the general observation that base-language definable endomorphisms must be included.
- State that the counterexample addresses the literal unrestricted formulation in the inspected OWR and arXiv versions. It is acceptable to name the final publication bibliographically while distinguishing the inspected version.

An honest concise formulation is: "In positive characteristic, inverse Frobenius gives a parameter-free definable multiplicative endomorphism outside the integral ring Z[theta]. This gives a negative answer to the unrestricted equality stated in the Oberwolfach report and in arXiv:2212.02115v4, Question 5.8. The characteristic-zero case and the corresponding localized classification are not established here. We have not verified the final journal wording or first historical priority."

Strongest verified result: the complete characteristic-p counterexample in every ACFH model of that characteristic. Exact remaining gaps: historical priority and final-publication text comparison, plus the mathematically separate characteristic-zero and full localized classifications. This review is not editorial acceptance, a human review, or novelty certification.

Final best-guess progress: 100% of this bounded independent adversarial audit; 80% of preparing a conservatively scoped note, with the final-source comparison still unresolved. No percentage is assigned to proving historical novelty.
