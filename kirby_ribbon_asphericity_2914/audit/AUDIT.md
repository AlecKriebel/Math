# Adversarial audit: 2914 / KP-4.38

**Date:** 2026-10-03. **Verdict:** PASS for the expressly unresolved, five-approach research record. **Required corrections:** none. This is not acceptance of a solution to ribbon-disk-complement asphericity.

The reviewed input is the seven-file bundle identified by the manifest SHA-256
`be95213c69677878ce0aa59d3e029fbbe046e11408d206be4ef400057158581e`.
Every input hash matches. The original verifier reproduces its recorded output byte for byte. The separate verifier in this audit supplies independent finite controls. Neither verifier substitutes for the general arguments reviewed below.

## 1. Question, category and source gate

The exact question and four accompanying remarks of K3 Problem 4.38 were checked in the text and image of printed page 221. The record correctly distinguishes the smooth/PL ribbon-disk question from the locally flat homotopy-ribbon variant. K3 explicitly identifies an incorrect historical general argument; the bundle does not rely on it. The original problem number is correctly recorded as Kirby 1997 Problem 1.103.

The 2026 Harlander–Rosebrock introduction and §4 describe the unrestricted LOT-asphericity question as unresolved and impose additional hypotheses on their results. This supports the bounded status statement, not a claim to exclude all subsequent literature. The unavailable Howie paper is not needed for any authored partial proof. This audit does not certify a fresh reading of that paper or rerun historical repository-search queries. Those limitations do not obstruct acceptance of this non-novelty, unresolved record.

The LOT presentation convention is consistent with the primary sources. Bedenikovic Appendix B writes a cyclic conjugate of the displayed relator; this change of attaching-word starting point preserves the presentation complex. The ribbon-to-LOT homotopy model is explained there and in §§1–2 and Appendix A. The converse realization assertion is supported explicitly by the statement that LOT complexes are ribbon-disk-complement spines in Harlander–Rosebrock 2026, §4. An arbitrary abstract tree, without its label/orientation data and this geometric model, would not alone justify that converse.

The five-vertex example is an actual LOT, and no planarity assumption about a classical knot diagram is inserted. Its failed graph test is only a failed sufficient criterion, regardless of which other methods might settle that example.

Primary sources checked:

- [K3, Problem 4.38, p. 221](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).
- [Bedenikovic 2011](https://doi.org/10.18910/4901): LOT model and conversion in §§1–2 and Appendices A–B; the separate conditional criteria in §§3–4 are not promoted to unconditional results.
- [Harlander–Rosebrock, 24-page v6 manuscript](https://arxiv.org/pdf/1212.1943v6): reductions in §1, Stallings and relative criteria in §3, reorientation/generator inversion in §4, and the injective theorem's induction in §5, including its fundamental-group injections.
- [Harlander–Rosebrock 2026](https://doi.org/10.4153/S0008439526102069): introduction and §4, including the reduced/injective, DR(2), quotient and sub-LOT restrictions.

The four primary-PDF fingerprints agree with SOURCE_GATE.md. The source PDFs and extracted texts are not part of this audit deliverable.

## 2. General mathematical arguments

### Ordinary homology and contractible enlargement

The exponent-sum boundary of an edge relator is the source basis vector minus the target basis vector, even if its label equals an endpoint. The root-deleted tree incidence matrix is unimodular. Leaf induction works with any root, and the one-vertex convention is correct. This proves circle homology, not universal-cover acyclicity.

Attaching the additional root-generator 2-cell really does kill every generator: each edge relation makes its endpoint generators conjugate, so triviality propagates along the connected tree regardless of the label. The enlarged ordinary boundary is unimodular. The enlarged complex is consequently simply connected and acyclic, hence contractible by the stated CW-complex Hurewicz/Whitehead argument. The bundle correctly refuses to infer asphericity of the original subcomplex from this fact.

### Infinite cyclic cover: nonzero determinant versus unit

For the relator s l t⁻¹ l⁻¹ the abelianized Fox coefficients are 1 at s, −t at the target, and t−1 at the label, with coincident contributions added. At t=1 the deleted-root minor is the incidence minor. Its determinant is nonzero because its value at 1 is ±1. Injectivity follows over the integral domain Z[t,t⁻¹]; surjectivity or a polynomial inverse is neither proved nor needed.

The five-vertex example provides an explicit control against confusing “nonzero” with “unit”: its minor is ±t(t²−t+1), which has more than one nonzero Laurent coefficient and is not a unit. All five deleted-root minors nevertheless define injective maps.

The deck group of this intermediate cover is Z and its fundamental group is [G,G]. Its H₂ vanishes, but it is universal only when G is already infinite cyclic. For that special case the simply connected two-dimensional cover is acyclic and contractible. The argument never applies simply connected Hurewicz directly to the original complex or to a non-simply-connected intermediate cover.

### Universal Fox boundary: side conventions

With a free left ZG-module written as row coefficients, the map is u ↦ uA. This is left-linear even though matrix entries appear on the right of the coefficients: (h u)A = h(uA). The boundary of a chosen oriented generator is x−1, and left translates give the usual Fox derivatives.

In ZG, the inverse-target derivative simplifies from −s l t⁻¹ to −l, while the final inverse-label contribution is −1. Thus the stated row is

1 at the source, s−1 at the label, and −l at the target.

The chain identity uses this multiplication order:

(s−1) + (s−1)(l−1) − l(t−1) = s l − l t = 0.

There is no unannounced transpose, anti-involution or conversion to a right-module convention. When the label is the source, the group relation identifies the endpoints and the row becomes s(e_source−e_target). When the label is the target, it becomes e_source−e_target. These checks agree with adding the coincident-index terms.

Since the universal cover has no 3-cells and is simply connected, H₂ and π₂ are precisely the kernel of this boundary. No determinant over the noncommutative group ring is asserted. Proving this kernel zero for every LOT, or producing a certified nonzero vector for one, remains the correct unresolved target.

### Augmentation argument and nonseparation

The normalization M U⁻¹ = 1+C is valid: U is an integral unimodular matrix and entries of C lie in the two-sided augmentation ideal I. If uM=0 then u=−uC, so iteration puts each coordinate in every Iᵏ. The argument uses only matrix multiplication in the indicated order, not a commutative determinant or an unjustified inverse in ZG.

For cyclic abelianization, the proof of γ₂G=γ₃G is sound. In G/γ₃G the commutator subgroup is central; every element is a power of a lift of the cyclic generator times an element of that central subgroup. Such elements commute. Equality of all later lower-central terms follows by induction.

The inclusion g∈γₖG ⇒ g−1∈Iᵏ has the stated direction. For the inductive step, if u−1∈Iᵏ and v−1∈I, both products in
(u−1)(v−1)−(v−1)(u−1) lie in Iᵏ⁺¹. Multiplication by units, products and inverses preserve the necessary ideal membership. No converse dimension-subgroup theorem is used.

For any nonabelian such group, a nonidentity commutator element supplies a nonzero group-ring element in every Iᵏ. Hence the completion map is not injective. This is genuinely an obstruction to the attempted completion argument, but it is not a Fox-kernel vector. The proof retains that distinction.

As an additional perspective, for these groups the augmentation intersection actually equals the kernel of ZG → Z[G_ab]. One inclusion follows because the kernel is generated by h−1 for h∈[G,G], and all these elements lie in every Iᵏ. For the other, the image lies in every (t−1)ᵏ in Z[t,t⁻¹]; a nonzero Laurent polynomial has finite order of vanishing at t=1. Thus the coordinate restriction does not give additional detection beyond the cyclic quotient. This does not invalidate the fifth approach: its substantive additional conclusion is that augmentation separation necessarily fails in the nonabelian case. No claim of five independent theorems is made.

## 3. Forest obstruction and its exact scope

For the path with successive labels c,e,a,c:

- Every label differs from its edge endpoints.
- Both leaf vertices occur as labels.
- Adjacent edges have different labels, which is sufficient for interior reducedness.
- The repeated label c prevents injectivity.
- Each of the nine proper nontrivial connected intervals has an edge labeled outside it.

The signed links are multigraphs: a parallel pair is a genuine cycle and must not be collapsed to a simple edge. Independent computation preserves these multiplicities.

Inverting a generator acts on all of its occurrences. The full Whitehead graph agrees with that of the LOT obtained by reversing every edge with that generator as label, as in Lemma 4.7. This equality was independently checked for all 32 inversion subsets, including the four choices of the two endpoint-only generators. Consequently the two c-labeled edges cannot be reversed independently by this operation.

All 32 inversion subsets have a positive or negative cycle. The eight displayed cycle certificates survive direct checks using the inverted relator words. Of the 16 independent edge reorientations, only (0,0,1,1) and (1,1,0,0) make both links forests. Both orient the two c-labeled edges inconsistently with generator inversion.

Those two successful reorientations cannot be imported as proofs about the original complex without establishing an appropriate equivalence. Conversely, failure of all generator inversions is not nonasphericity and does not exclude other presentation changes, weight tests, reductions after other operations, or geometric criteria. The bundle states this limitation correctly.

## 4. Reproduction and negative controls

The original verifier passes, and `replay-verification.json` exactly matches the frozen `verification.json`.

Run `python3 audit_verify.py` from this directory for the independent controls:

- All seven frozen file hashes and the manifest hash.
- Five polynomial minors, computed by recursive Laplace expansion.
- 512 incidence-minor checks covering all 16 labeled four-vertex trees, all eight orientations and all four deleted roots, using exact rational elimination.
- 100 abelian Fox triples, including endpoint-label coincidences.
- All 32 full-Whitehead-graph inversion equalities and two-forest failures.
- All eight hand-table cycle witnesses and all 16 independent reorientations.
- All nine proper subintervals and the stated reducedness conditions.
- Four noncommutative Fox rows evaluated in an explicit nonabelian A₄ representation. The correctly ordered chain product vanishes; reversing the multiplication order fails in all four rows.
- Two exact noncommutative commutator-ring identities.

The nonabelian representation also confirms that the five-vertex example is not accidentally a cyclic group. It is only a finite control: no representation calculation decides injectivity of the universal group-ring boundary.

## 5. Disposition

The five approaches are substantive and accurately terminated at their respective gaps. The supported outcome is **unsolved after five approaches**, with no target counterexample, no full-resolution claim and no novelty claim. No amendment of the frozen bundle is required for that classification.

The remaining mathematical problem is universal group-ring Fox-boundary injectivity. The passed finite checks and accepted elementary proofs do not settle it.
