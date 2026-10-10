# 30005584: expander-degree source gate

Research in progress; zero substantive author turns at this checkpoint. No result claim, QUEUE promotion or result PR.

## Exact original target

Eric Chen, joint work with Richard Bamler, *Expanding Ricci solitons asymptotic to cones with non-negative scalar curvature*, in Oberwolfach Report 29/2023, *Differentialgeometrie im Grossen*, DOI 10.4171/OWR/2023/29, printed pp. 1663–1665. The question is on printed p. 1665 (PDF p. 49). The workshop was July 2–7, 2023. The report number and workshop year are 2023 even though the imported citation includes a 2024 publication label.

The two requested tasks are to relate the three unrestricted degrees of X₁, X₂ and their **boundary connected sum** X₁#∂X₂, and to compute the unrestricted degree of D³×S¹. The operation removes half four-balls at the boundaries and inserts a hemisphere-times-interval neck, so its boundary is ∂X₁#∂X₂. It is not an interior connected sum, a disjoint union or a graph-expander construction.

The same question reappears in OWR 11/2025, printed p. 498. The full original mathematical paper is Bamler–Chen, *Degree theory for 4-dimensional asymptotically conical gradient expanding solitons*, arXiv:2305.03154v3 (23 January 2025), subsequently Communications on Pure and Applied Mathematics 79 (2026), 1151–1298, DOI 10.1002/cpa.70024 (first online 16 December 2025). Its Questions 1.15 and 1.16 preserve the two tasks. The exact theorem numbering below refers to the complete arXiv v3 PDF, not an unread publisher PDF.

## Exact degree theory

The objects are compact smooth four-orbifolds X with isolated singularities and nonempty regular boundary. The boundary admits a positive-scalar-curvature metric. X must have a possibly infinite orbifold cover that is a smooth manifold with H₂(cover; Z)=0 and torsion-free H₁(cover; Z). These hypotheses are stated in §1.3; the equivalent noncompact ensemble is Definition 3.5. In particular, the invariant is sensitive to the **smooth** structure, not asserted to be invariant under arbitrary homeomorphisms.

The solitons are complete gradient Ricci expanders on Int(X), normalized by Ric_g+Hess_g f+(1/2)g=0. They are asymptotic, in fixed coordinates at infinity, to cone metrics γ=dr²+r²h. The degree uses the locus with nonnegative scalar curvature in both domain and target. Scalar nonnegativity is weaker than Ricci or curvature-operator nonnegativity. For a three-dimensional link, the cone's scalar condition is Scal_h≥6. Regularity k*≥30 (including infinity) enters the degree construction.

Definition 3.8 fixes the actual moduli space: triples (g,V,γ), with g C², V C¹, soliton equation Ric+(1/2)L_Vg+(1/2)g=0, V=−r∂r/2 outside a compact set, and r^m|∇^m(g−γ)|→0 for m=0,1,2. Quotient by compactly supported diffeomorphisms preserving these data. The gradient subspace has V=∇f; Definition 3.14 gives the equivalent compactification-relative-boundary description. Stronger asymptotics are consequences, not replacements for the definition.

Projection Π sends a soliton class to γ. The restricted gradient/nonnegative-scalar locus is proper, but may be singular. The construction enlarges the target to generalized cones dr²+r(dr⊗β+β⊗dr)+r²h and the domain to nongradient solitons, then takes a localized integer degree on suitable finite-dimensional slices. Neither an ordinary degree of the gradient locus as a Banach manifold nor an unqualified count is valid. Theorem 10.49 gives, **if the cone is a full regular value**, the signed formula sum_p (−1)^index(−L_p), where L_p=Δ−∇_(∇f)+2Rm on symmetric two-tensors. Regular values on the gradient subvariety need not exist, so this formula is not the primary definition.

Known exact input: deg_exp(D⁴/Γ)=1 (Theorem 1.5 / 10.51), and certain exotic/smoothly different fillings have degree zero (Theorem 1.14). Lemma 3.19 says a gradient expander asymptotic to a cone with nonnegative scalar curvature has nonnegative scalar curvature. These are credited prior theorems.

## Material current literature update

Abishek Rajan's *Cohomogeneity One Expanding Ricci Solitons and the Expander Degree* is now published in Journal of Geometric Analysis 36, article 344, **September 1, 2026**, DOI 10.1007/s12220-026-02593-9. Both the complete published PDF and arXiv:2510.15192v2 (22 October 2025) were recovered. Theorem 1.1 gives the **cohomogeneity-one** degree of S¹×D³ as 1; Theorem 1.2 gives the analogous degree of S²×D² as 0. Section 9's calculation is up to the orientation choice (Theorem 9.5 in the preprint). With standard ordered coordinates (a₀,−f₀) and (a′∞,b′∞), the one-dimensional reciprocal endpoint map has degree −1; this sign is not automatically Bamler–Chen's canonical orientation.

The restricted metrics are dr²+a(r)²g_S¹+b(r)²g_S², invariant under SO(3)×SO(2), with invariant f. Their ODE uses Ric+Hess f+g=0, a different normalization. Its proper two-parameter initial-data map F sends (a₀,−f₀) to the two asymptotic slopes. No nonnegative-scalar restriction is imposed on this entire restricted theory. Neither existence of symmetric solitons nor the restricted degree by itself computes the unrestricted degree.

Rajan's May 2026 Berkeley dissertation, *Expanding Ricci Solitons and the Expander Degree*, has a separate comparison chapter. The complete public thesis was recovered from the institution's PDF repository. Printed p. 66 (PDF p. 73) expressly says equality of the general and restricted degrees is expected but is not rigorously known. Its subsequent index discussion does not supply a theorem identifying the entire unrestricted contribution with the symmetric contribution. We will not infer a full answer from the title of that chapter.

Searches through October 1, 2026 found no general boundary-connected-sum law or completed unrestricted S¹×D³ computation in the identified primary sources. This negative search is a dated source assessment, not proof that no other result exists.

## Prior campaign gate and access

All-state GitHub PR searches for the numeric ID and source code returned zero; both target path histories were empty, as was the dedicated branch prefix. Local all-ref history has no target attempt. The imported research-results archive has no entry keyed by this source code. The current QUEUE row is rank 299, queued 0/5. Source triage is not an author proof turn.

Six complete primary PDFs are pinned in source_manifest.json. The original and later OWR, full Bamler–Chen arXiv paper, Rajan preprint, Rajan published paper and Rajan thesis are all available for reading. The Bamler–Chen publisher full-page endpoint was unreliable; publication metadata and indexed source passages were checked, while exact mathematical references use the complete v3 preprint. No publisher-PDF reading is claimed. The thesis landing page was unreliable, but the institution's public direct PDF downloaded successfully and its title, author, date and chapter content were verified.

No downloaded PDF, full-text extraction, rendered page or full imported record is included in the portable packet. No new discovery is claimed by this source checkpoint.
