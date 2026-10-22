# Harmonic circle fibrations: source-scope acceptance

13 October 2026. Independent source and prior-result adjudication for 30003375 / OWR-15208-029, normal queue row 1766. This review checks the scope and applicability of the existing proposed theorem transfer. It adds no substantive proof-search pass and makes no remote change.

## Decision

**Accept the affirmative answer to E, the explicitly adopted unrestricted metric-existence reading, as a credited prior-theorem consequence. Recommend `already_solved` for that normalized target, with the E-only qualification in the same queue row. Do not report a new open-problem solution.**

The mathematical content is that every closed smooth manifold homeomorphic to S¹×CP³, in either primitive integral first-cohomology class, has a smooth metric whose harmonic circle representative is a smooth fibration. The metric is chosen for this purpose. This includes every genuinely exotic smooth total space in the stated topological class; no particular connected-sum representative has to be proved exotic to obtain the universal implication.

This acceptance does not authenticate Farrell's unstated metric quantifier or certify all possible readings of his question. It does not answer the arbitrary-metric assertion U, a prescribed-metric question G, or the neighbouring curvature-rigidity questions C. Neither leaving E labelled unsolved nor turning U or C into the original target by fiat is justified.

## What the source actually fixes

The decisive passage is F. Thomas Farrell's TF contribution in the Day 5 discussion, printed p.164 of *Mini-Workshop: Spaces and Moduli Spaces of Riemannian Metrics*, Oberwolfach Reports 14 (2017), 133–166. It asks: “Can this map be a fibration in the exotic cases?” Its preceding instruction equips the manifold with a Riemannian metric and considers a harmonic map to the circle. No metric quantifier or homotopy class is specified. [Primary report](https://ems.press/content/serial-article-files/46667), [publisher record](https://ems.press/journals/owr/articles/15208).

The preceding SY paragraph, pp.163–164, discusses detecting the standard smooth product among exotic possibilities. Its two geometric alternatives are nonnegative sectional curvature on the total space and smoothly varying positive-sectional-curvature fibre metrics. The TF paragraph does not repeat either curvature condition. Su's earlier contribution, pp.157–158, separately states the circle-fibering construction and those curvature questions. These passages were independently read and visually inspected.

It is defensible to adopt E for the catalogue's unrestricted “can” wording. The publication must call that an adopted interpretation. Context creates a real boundary; it supplies no licence either to silently retain curvature or to claim that curvature was conclusively discarded by the author.

## Exact accepted normalization

Fix S¹=R/Z with its standard flat metric. Let M be a closed connected smooth manifold homeomorphic to S¹×CP³ and let u be either primitive generator of H¹(M;Z). The adopted assertion E is:

> There is a smooth Riemannian metric g on M for which the harmonic map h:(M,g)→S¹ in class u is a smooth submersion, and hence a smooth locally trivial fibration.

The class is part of the normalization. A Riemannian metric by itself does not select a single circle-valued harmonic map. On a closed connected M, the harmonic representative of a fixed integral class is unique up to rotation of S¹. Reversing the primitive generator changes no submersion question. Choosing a primitive class rules out a constant map and gives connected fibres.

These choices make the existence question precise; they are not definitions printed in the source. The theorem is universal over the stated smooth total spaces and the two primitive classes, but existential over metrics. It is not universal over metrics.

## Prior-theorem transfer and its applicability

### Smooth fibering

Browder–Levine, *Fibering manifolds over a circle*, Commentarii Mathematici Helvetici 40 (1965/66), 153–160, Theorem 1.4 on p.154, gives a smooth circle-fibre map in a specified nonzero integral H¹ class when a compact smooth manifold has dimension greater than five, infinite cyclic fundamental group, and finitely generated homotopy groups. Its boundary-extension condition is vacuous for a closed manifold. The theorem statement was independently visually inspected. [Institutional copy](https://www.maths.ed.ac.uk/~v1ranick/papers/browlev.pdf), [bibliographic record](https://eudml.org/doc/139300).

All these conditions hold here. The dimension is seven and π₁(M)=Z. For i≥2, a homeomorphism with S¹×CP³ identifies πᵢ(M) with πᵢ(CP³). A simply connected finite CW complex has finitely generated homotopy groups in each degree, so these groups satisfy the theorem's hypothesis. The chosen u is nonzero. Thus there is a smooth bundle projection p:M→S¹ with p*([dθ])=u. The primitive class makes p* on fundamental groups surjective and the homotopy exact sequence gives a connected fibre.

This application uses only the smooth structure on M and its topological homotopy type. It does not transport a Riemannian metric through a nonsmooth homeomorphism. It requires neither a product diffeomorphism nor trivial monodromy. It also does not require identification of the fibre with CP³.

### Harmonicity for a chosen metric

Katz, *Harmonic forms and near-minimal singular foliations*, Commentarii Mathematici Helvetici 77 (2002), 39–77, pp.39–40, explicitly recalls that a nonsingular closed one-form on a closed manifold is harmonic for a suitable Riemannian metric, and credits Calabi's intrinsic-harmonicity criterion. These two pages were independently read and visually inspected. [Katz article](https://ems.press/content/serial-article-files/42917).

Apply this to α=p*dθ. Since p is a submersion, α is smooth, closed and nowhere zero. There is a metric g with δgα=0. For the flat circle target, the circle map p is harmonic exactly when its pullback of dθ is co-closed: locally p lifts to a real-valued function and this is its Laplace–Beltrami equation. The map has not changed, so it remains a submersion. Its differential is the unique g-harmonic one-form in u, and every harmonic map in that class differs from p by a target rotation. Consequently the accepted normalized statement follows.

The original Calabi chapter was not directly inspected in this adjudication. Attribution should say “Calabi's intrinsic-harmonicity result, as recalled by Katz,” rather than claim direct verification of Calabi's proof. Its bibliographic title is *An intrinsic characterization of harmonic one-forms*, Global Analysis (1969), 101–117. [Chapter DOI](https://doi.org/10.1515/9781400871230-006).

If a specific CP³-bundle projection p is already part of the source setup, the same argument applies immediately to that p. This stronger preservation statement avoids any concern about Browder–Levine identifying a different six-dimensional fibre: the supplied projection itself can be made harmonic. An explicit mapping-torus metric construction may be useful exposition, but does not remove the prior-result attribution or establish novelty.

## Exotic smooth structures: the exact remaining distinction

Calling a homotopy-sphere summand nonstandard does not alone prove that its connected sum with S¹×CP³ is a nonstandard total space. Inertia can identify connected sums. The accepted theorem avoids that inference: it quantifies over every smooth M homeomorphic to the product and therefore applies whenever M is exotic as a total space.

The source's classification discussion is not needed as an unproved metric-construction premise. In particular, the earlier OWR theorem's H₃ hypothesis concerns the universal cover; replacing it by H₃(M)=0 would be wrong. The direct Browder–Levine application above avoids that transcription error as well.

A separate claim exhibiting distinct exotic total spaces may cite Basu–Kasilingam–Sarkar, *Enumerating Smooth Structures on CP³×Sᵏ*, arXiv:2503.16267v2, Theorem 3.5(ii), p.22. The inspected statement classifies the oriented smooth manifolds in this homeomorphism class using the product and three nonzero elements of a Z/4 subgroup of Θ₇. The arXiv record currently identifies v2, dated 2 April 2025; no journal acceptance or independent proof audit was verified. Do not identify its representatives numerically with the OWR sphere indices without a convention check. [Versioned preprint](https://arxiv.org/abs/2503.16267v2).

Thus there is no missing exotic-total-space hypothesis in the universal E theorem. A new explicit example claimed exotic would have a separate classification obligation; this transfer does not need to make that claim.

## Boundaries which must survive publication

- U asks whether every metric's harmonic representative is nonsingular. The existence of one suitable metric does not answer it.
- G fixes a particular metric. Replacing that metric is not a solution; the report supplies no specific metric to test.
- C may retain nonnegative sectional curvature on M or positive sectional curvature on the fibres. Neither Calabi's existence theorem nor the proposed fixed-volume mapping-torus construction establishes either curvature property.
- A family of fibre metrics alone does not specify the complete metric on M used in the harmonic equation. No Riemannian-submersion or isometric-monodromy hypothesis may be silently added.
- The separate curvature records 30003356 / OWR-15208-010 and 30003374 / OWR-15208-028 are not resolved or duplicated away by this E result.
- No first express answer to Farrell's named question, worldwide priority finding, or author-endorsed clarification was verified. Those are different claims from checking the prior-theorem implication.

## Queue disposition

The inspected queue README reserves full resolution for the entire exact adopted claim and identifies `already_solved` as the disposition for known resolutions. The pinned state ledger uses `already_solved` for credited published-theorem consequences even when express historical named-answer priority is unverified. `prior_result` was not present as a canonical status in that inspected ledger; it is an appropriate result classification.

Recommended Status: **`already_solved`**.

Recommended Findings:

> Prior-theorem resolution of adopted E only: every smooth M homeomorphic to S¹×CP³ and every primitive H¹ class admits a harmonic circle fibration for some metric (Browder–Levine; Calabi, as recalled by Katz). No new theorem claimed; the metric quantifier and curvature inheritance in Farrell's wording are unspecified. Arbitrary/prescribed metrics and the preceding curvature-rigidity questions are not settled.

This is a qualified disposition of the normalized catalogue target. It must not be converted into “the full historical Farrell problem is solved” or `full_source_solved=true` without the same explicit interpretation boundary. If a downstream system defines a single status as an unconditional certification of every possible historical reading and cannot retain the E qualifier, `partial` is the conservative source-level status, with E separately marked `prior_result`. The present qualified row need not remain indefinitely blocked on author intent.

`claimed_solved` is inappropriate as an achievement label here: the positive existence mechanism is already supplied by credited literature. `unsolved` is also inaccurate for E. The source-level uncertainty is a quantifier/scope issue, not a mathematical gap in E or evidence that any named stronger variant is still open worldwide.

The turn count must report actual substantive effort only; this source adjudication adds zero. No prior lifetime count is certified by this review. Publication should contain the authored theorem, explanation, citations and safe verification metadata only, with source bodies and private coordination excluded.
