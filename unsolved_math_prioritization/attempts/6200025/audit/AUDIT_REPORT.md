# Independent adversarial audit: rank 646 / 6200025

## Verdict

**PASS, with one minor bibliographic correction.** The frozen note establishes a negative answer to the exact equivariant question by a consequence of already published mathematics. Accept `already_solved`, negative, with 3 of the maximum 5 substantive approaches used. No substantive proof gap or need for another research approach was identified.

The reviewed author manifest is exactly 2,037 bytes, SHA-256 `c9a24f4c45b730d60d2ee9668372c729515be65be0425042d5f227e29b613feb`, binding 13 payload files. Originals were preserved throughout. This audit made no remote repository changes and used no additional reviewers.

The conclusion is restricted to failure of equivariant uniqueness. In the example both boundaries are ordinary topological 2-spheres. This is not a classification of all EZ-boundaries, not a claim of topological non-homeomorphism for this example, and not a novelty or earliest-priority claim.

## What was independently checked

The complete `PRIOR_RESOLUTION.md` and all other author payloads were read. The target was compared with the complete selected record and its prior report, then with the original author-hosted problem list. The definitions and Problem 25 on PDF page 8 were rendered and visually inspected. The original question includes a compact Euclidean retract, a homotopically negligible remainder, a cocompact covering action, nullity for every compact subset, and an action extension. Farrell-Lafont Definition 1.1 resolves the abbreviated wording about extension by requiring extension over the compactification.

The prior report's general uniqueness and cell-like-equivalence assertions were not accepted as established facts. They are unnecessary for the decisive route. Repository duplicate and queue gates were not repeated in this mathematical audit; their descriptions remain author provenance, not a new remote audit result.

The decisive published GHP PDF was freshly retrieved from EMS. Its 606,280 bytes and SHA-256 `e6cbee379bfe5701e8a0363da16aed6826a709749017187085d14563a33c42f1` exactly match the author's source metadata. Journal page 898 was independently rendered from those fresh bytes and visually inspected. The publisher's authors, DOI, volume, pages, and publication date also match the note. Nine locally available source PDFs matched all nine scholarly-source hash/size entries. The two exact-title correction/erratum searches found no relevant correction; this bounded search is not an exhaustive absence certificate.

## Adversarial issues and outcomes

### 1. Does the whole group fix the poles?

Yes. Theorem 1.6 alone is insufficient to identify the action, so the explicit section 7.1 action was checked. Both kinds of generators act by suspension maps with unchanged suspension coordinate. Every element of the fiber subgroup fixes each pole, and the stable letter fixes each pole. Products and inverses do also.

This is stronger than the invalid shortcut of checking only the stable letter. A new negative control constructs a genuine C6 × Z action in which the stable letter fixes both endpoint labels while a fiber generator swaps them. It is correctly rejected as evidence of whole-group fixed points. In the actual action, the fiber subgroup has no common fixed point on its canonical circle, so the global fixed set consists of exactly the two poles.

The chosen relation t⁻¹ g t = φ(g) is the published convention. The inverse-monodromy choice causes no obstruction: both monodromies are pseudo-Anosov. In the boundary relation only h_C needs to be a homeomorphism; the frozen note never wrongly assumes an arbitrary cellular homotopy equivalence is invertible on X.

### 2. Is the original finite-dimensional ER requirement really met?

Yes. The surface has a finite 2-dimensional aspherical CW model. A cellular representative of its induced automorphism gives a finite 3-dimensional mapping torus, whose universal cover is the locally finite 3-dimensional telescope Y. This is the covering space used by the torsion-free construction.

The compactification Ybar is a metric AR, and its remainder B is suspension(S¹), hence 2-dimensional. Exhaust Y by compact subcomplexes K_n. Every K_n is compact, hence closed in the Hausdorff space Ybar, and has dimension at most 3. The remainder is closed. Therefore the countable closed-sum theorem, applied to B together with the K_n, gives dim(Ybar) ≤ 3. There is no illegitimate application to nonclosed summands and no assumption that finite-dimensional interior alone forces finite-dimensional compactification.

The Euclidean embedding theorem embeds this compact metric space in R⁷. Its image is closed by compactness. The AR property then gives a retraction of R⁷ onto the image. Thus the original ER condition, not only an infinite-dimensional AR relaxation, holds. Precise textbook locators are Engelking, *Dimension Theory*, Theorems 3.1.8 and 1.11.4. Guilbault-Moran section 2, Remark 2, independently states the finite-dimensional AR/ER convention.

### 3. Free covering action, cocompactness, and nullity

The group is torsion-free and the telescope is the universal cover of the finite mapping torus, so the action is by free covering transformations with compact quotient. The argument does not substitute a possibly nonfree proper action allowed by the broader GHP definition.

For the compactification, the proof dependencies were traced through GHP Lemma 2.11; section 3; Theorem 4.2, Propositions 4.8-4.12, and Lemma 4.13; Proposition 5.4 and Claims 5.6-5.7; and the closing proof of Theorem 1.1. In particular, nullity is a conclusion of the controlled compactification construction, not a consequence of merely adjoining a suspension. The action extension was traced through Theorem 7.1, Lemmas 7.2-7.5, Claims 7.6-7.7, and section 7.5. The quasi-geodesic case suffices here, so no non-quasi-geodesic or torsion generalization is required.

As an additional defense against hidden model assumptions, `SPECIAL_CASE_CHECK.md` provides a direct smooth-surface model. A lifted diffeomorphism is bilipschitz; double-logarithmic radial compression compactifies H² × R to a closed 3-ball. The note proves extension, including pole continuity, and proves nullity for arbitrary compact sets by separating near-axis and far-axis translates. It independently checks the original axioms without needing the generic boundary-swapping machinery for this special example.

This supplement is not a claim that the cellular-model compactification in the author note is necessarily a ball. It constructs a particular smooth model and identifies its boundary action with the required suspension action.

### 4. Continuity at poles and source shorthand

The non-pole convergence criterion using a chosen z in the base boundary should not be read literally at a suspension pole: a sequence can converge to a pole while its base coordinate remains bounded. The supplement explicitly treats bounded and unbounded base-coordinate subsequences and confirms pole continuity. Similarly, using an actual lifted diffeomorphism with h = f⁻¹ avoids any issue with inverse notation for a general homotopy equivalence. These clarifications do not change the frozen proof's reliance on the published EZ theorem or its correct boundary formulas.

### 5. Hyperbolicity and absence of canonical fixed points

The fiber is closed, not punctured. Thurston Theorem 0.1, Proposition 2.6, and the section 5 proof imply that its pseudo-Anosov mapping torus is a closed hyperbolic 3-manifold. The compact quotient gives a proper cocompact isometric action on H³, hence a word-hyperbolic group with canonical boundary S². The surface subgroup ensures non-elementarity.

Thurston's page-3 minimality statement and Kapovich-Benakli Proposition 4.2(2) were checked for the relevant non-elementary case. A nonempty proper singleton would contradict minimality on this S². Therefore the canonical boundary has no global fixed point.

An equivariant map would send a globally fixed pole to a global fixed point. Thus there is no equivariant function from the constructed boundary to the canonical one, even before continuity or bijectivity is considered.

### 6. Sphere topology, homology, and local dimension

The explicit suspension-to-sphere homeomorphism in the supplement shows that the poles are ordinary manifold points topologically. Every point has local dimension 2 and local integral homology of a 2-manifold. The reduced integral cohomology is Z in degree 2. There is no conflict with the cohomology or local-dimension restrictions for this closed 3-manifold group.

Fourteen independent finite simplicial suspensions of polygons were checked over the rational numbers. Each has Betti numbers (1,0,1), Euler characteristic 2, and circular vertex links, including both poles. Deleting a face destroys the expected top homology and link condition and is detected. These controls supplement, and do not replace, the explicit topological proof.

### 7. Attribution and scope

The 2026 Kandybo-Świątkowski text was checked where it invokes Bestvina Example 3.1. The original Bestvina paper remains uninspected in this audit. Accordingly neither an EZ upgrade nor earliest priority is certified from that citation. The GHP route is independent of it.

An arbitrary EZ action is not required by the original axioms to be minimal or a uniform convergence action. Consequently Bowditch's characterization cannot be used to infer equivariant uniqueness here. The example is consistent with the canonical convergence-action theory and with ordinary topological sphere uniqueness in this case.

## Replay and corrections

- All 13 author payload hashes and byte counts matched the pinned manifest.
- The author manifest verifier passed, and its exact finite control output matched the stored result: 5,461 words through length 6; 120 conjugacy changes; 17 relation points; both negative controls.
- Independent controls passed: 55,223 C7 semidirect composition checks, 23 relation points, the stable-letter-only negative control, 14 triangulated suspension spheres, a deleted-face mutation, and 77 exact rational sphere-coordinate checks.
- The portable verifier also rejects byte mutation, an extra file, a missing file, and a changed author manifest in disposable copies.
- The sole correction is the GHP locator **Section 3.2 → Section 3**, including the source inspection entry. The cited page range is already correct. See `CORRECTIONS.md`.

## Limits

This is an independent mathematical audit, not formal verification. It checks theorem hypotheses, cited proof locations, elementary deductions, an explicit special-case construction, and reproducible finite controls. It does not re-prove all external deep results, including hyperbolization, nor survey all historical literature. No source PDF, extracted source text, source-page image, corpus record, or private coordination file is included in this audit package.

## Public references

- Original Problem 25 and definitions: https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf
- Published GHP article: https://doi.org/10.4171/GGD/750
- Published GHP PDF: https://ems.press/content/serial-article-files/47884?nt=1
- Farrell-Lafont Definition 1.1: https://arxiv.org/abs/math/0405260
- Thurston: https://arxiv.org/abs/math/9801045
- Kapovich-Benakli: https://arxiv.org/abs/math/0202286
- Guilbault-Moran: https://arxiv.org/abs/1707.07760
- Engelking, *Dimension Theory*: https://webhomes.maths.ed.ac.uk/~v1ranick/papers/engelking.pdf
- 2026 attribution caveat: https://arxiv.org/abs/2603.05742
