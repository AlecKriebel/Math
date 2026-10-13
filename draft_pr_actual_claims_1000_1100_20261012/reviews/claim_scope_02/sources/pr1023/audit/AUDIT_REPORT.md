# Independent audit: action dependence of measured free indecomposability

## Disposition

**ACCEPTED AS SCOPED PARTIAL RESULTS. THE SOURCE PROBLEM REMAINS UNRESOLVED.**

Target: OWR-2487-003, catalogue 30001092, rank 1099. The audited packet contains five completed approaches, with substantive count 5/5. This review is verification of those approaches, not an additional construction attempt. It establishes neither a pair of free actions with different FI behavior nor an impossibility theorem for such pairs.

The five authored inputs were frozen at 2026-10-09T00:01:21Z. Their byte counts and SHA-256 digests were independently checked against the supplied frozen manifest. The main proof input is `SCOPED_RESULTS.md`, 18,054 bytes, SHA-256 `4cc312645d36f3573d205adc9e862b2ccc7f91d9b3c891db36ff5417b10a5834`. No original was modified.

No substantive mathematical defect was found. A separate contextual supplement makes two delicate arguments more explicit and names the primary theorem behind the amenable-factor generator. These are supporting details for existing arguments; no conclusion or hypothesis has been changed.

## 1. Exact category and imported interfaces

The OWR report's ambient convention is countable groups and standard atomless probability spaces. Its Question 4 must be read with the preceding free-action definition. The published Alvarez–Gaboriau Question 4.16 explicitly asks about free p.m.p. actions. The frozen packet correctly restores that hypothesis and does not impose ergodicity on the original question.

The decomposition convention permits factors with smaller Borel domains. The frozen version correctly requires those domains to cover the ambient relation's domain. Inessentiality is a complete-section condition, not a demand that a factor equal the whole relation on a full-measure set in every case. In particular, invariant slicings and smooth connectors must remain inessential. All proofs were checked with these distinctions intact.

The source-interface checks were made against full primary documents, with the relevant definitions, theorem statements and surrounding arguments inspected. They do not amount to a fresh proof of every theorem in those papers.

- Alvarez–Gaboriau: measured conventions on pp. 60–61; decomposition and trivialization on pp. 61–66; aperiodic treeability and binary reduction on pp. 67–68; restrictions, stable orbit equivalence and locally bijective morphisms on pp. 68–70; zero-Betti criterion and the nonamenability interface on pp. 70–71.
- Tucker-Drob–Wróbel, arXiv:2410.11754v3: Section 5, pp. 16–18, including the proof of Lemma 5.1 and the essential-splitting definitions. **Ergodicity is present in the v3 statement.**
- Conley–Gaboriau–Marks–Tucker-Drob, arXiv:2104.07431v3: the strong-treeability statements on pp. 3–4 and 8–9, and the more precise statements on pp. 25–26. The v3 submission date is 19 March 2026.
- Peterson–Sinclair: the cocycle target classes and Corollary 1.2 on pp. 249–251; Section 4 on pp. 262–263, showing that the obstruction constructed there is circle-valued.
- Connes–Feldman–Weiss: the generator statement on p. 431; the measured definitions and single-generator characterization on pp. 433–434; Theorem 10 and its surrounding proof on pp. 443–444. No ergodicity of the amenable factor is needed.

Public bibliographic metadata and independent source hashes are recorded separately. Source documents, extracted source text and page images are not included in this authored audit packet.

## 2. Proposition 1: nonfree false positive and failed repair

**Accepted.** For H = F_2 × F_2, both factors are infinite, so the direct-product L2-Betti formula gives beta_1^(2)(H) = 0. H is nonamenable. Its atomless-base Bernoulli action is free and mixing, hence ergodic, and its relation meets the cited FI criterion.

Pullback along (H * Z) → H preserves the relation and its measure properties but kills every element of the Z factor. This violates essential freeness on the entire space. It cannot answer the source question.

For any free action of H * Z, the H- and Z-subrelation factorization is a genuine free product: a nonempty reduced alternating word cannot fix a point in the common free conull set. Both full-domain factors are aperiodic. If the decomposition were inessential, the full-domain aperiodic-factor consequence of the trivialization theorem would collapse the ambient relation to the H-subrelation. For a nonidentity z in Z, however, zx = hx would force h^(-1)z to fix x. The contradiction proves essentiality.

The diagonal repair is free because of its Bernoulli coordinate and ergodic because a weakly mixing action times an ergodic action is ergodic. Its relation is nevertheless non-FI by the preceding all-free-actions argument. Restricting the free Bernoulli action to H is mixing, since finite coordinate supports separate along the infinite subgroup H. Thus the stated failure of the FI-subrelation-to-ambient inference also checks out.

## 3. Proposition 2 and Corollaries 2.1–2.2

### Recurrence and canonical supports

**Accepted.** The recurrence argument uses a nonnegative Borel mass transport, and is valid without ergodicity. On the saturation of A_f, every point sends total mass one equally to the finitely many points of A_f in its class. Every point of A_f receives infinite mass. Finite total outgoing mass forces A_f to be null; the mass-transport identity also forces its saturation to be null. No recurrence conclusion is being made for an arbitrary non-p.m.p. countable relation.

In the necessity direction of the canonical criterion, first saturating the trivialization pieces inside their respective factors is essential. The cited proposition permits precisely that operation. A factor's restriction to the complement of its saturated piece is smooth and finite almost everywhere under the finite invariant measure. Its infinite-class support E_i is consequently contained in that piece modulo null sets. Conversely, recurrence for the ambient aperiodic relation and equality of the two restrictions make the factor aperiodic on its piece. The saturation condition then identifies the piece with E_i. This proves the claimed equivalence, including the completeness requirement for E.

All relevant supports and projected violation sets are Borel. Countably many exceptional sets may be removed along with their countable relation saturations. The conclusion is a measured characterization for a fixed decomposition, not a Borel classification of arbitrary decompositions.

### Countable mixtures

**Accepted.** Restriction to an invariant positive-measure summand gives the forward direction. For the reverse direction, a factor of a decomposition cannot leave an invariant summand. The corresponding trivialization pieces can therefore be united over the countably many summands, one factor index at a time. Positive weights permit normalization without changing null sets. This does not justify an uncountable union of independently chosen trivializations.

### Ergodic extraction

**Accepted.** The fixed essential binary splitting is the correct object to disintegrate. Almost every invariant ergodic conditional measure preserves the group action and gives full measure to the original free invariant conull set. Every partial isomorphism in a subrelation is piecewise a group element, so no extra invariance assumption on the factor relations is missing.

The supplement writes down explicit, countably many Borel failure sets using a fixed enumeration of the group. If the splitting were inessential for almost every conditional measure, each such set would have conditional measure zero almost everywhere. Integration would make every failure set null for the original measure, contradicting essentiality. Thus there are non-FI ergodic components on a set of positive decomposition measure. For a free action of an infinite group, an atom would have infinitely many equal-mass translates, so the chosen conditional probability measure is atomless.

The packet correctly declines to infer that an FI action has FI almost every ergodic component: the argument just checked handles one fixed decomposition, not a measurable choice of potentially different decompositions.

## 4. Proposition 3 and Corollary 3.1

**Accepted.** An equivariant factor map onto a free action is surjective on each orbit. If p(gx) = p(hx), target freeness forces g = h, proving orbitwise injectivity. The pushforward measure is exactly the target measure, which is stronger than the measure-class requirement of the locally bijective-morphism lemma.

The lemma's direction is FI source ⇒ FI target. Its contrapositive gives non-FI target ⇒ non-FI extension. The frozen packet uses precisely this direction. Product coordinate projections satisfy the hypotheses, and the product remains standard, atomless and free. No product ergodicity is needed.

The common-extension equivalence follows: an FI/non-FI pair gives a non-FI product extending the FI action, while such an extension already constitutes a pair. Consequently an unproved blanket assertion that FI passes upward through all same-group free extensions would assume the negative answer rather than prove it. The packet makes no such assertion.

## 5. Propositions 4.1–4.2 and Corollary 4.3

**Accepted.** The finite-index induction formula uses left-coset representatives consistently. It defines a p.m.p. action; its stabilizer calculation conjugates into H and hence proves freeness. The identity slice is a complete section and its restricted relation is exactly the input H-relation. Complete-section invariance therefore preserves either FI type. The ergodicity equivalence follows from the transitive permutation of the finite fibers and invariance on the identity slice.

For an infinite coset space, equal positive fiber weights cannot total one. This invalidates the particular counting-measure induction as a p.m.p. construction. It is not a claim against every possible coinduction, and the packet makes that distinction.

For a finite normal K, a Borel transversal exists for the finite K-orbits. Freeness gives disjoint equal-measure translates, so normalized restriction to the transversal agrees with quotient probability measure. A finite-to-one quotient of an atomless standard probability space is still atomless. The Gamma/K-action is free: gx = kx implies g = k on the free set. Restriction to the transversal is orbit equivalent to the quotient relation. Invariant sets upstairs are K-invariant and hence correspond to invariant sets downstairs, proving the ergodicity assertion.

For Gamma × K, the explicit product with the left-regular K-action supplies the reverse transport. The original relation appears on X × {1} as a complete-section restriction. No assertion about a reverse lift through an arbitrary nonsplit finite extension is present. The caution about measure-equivalence invariance of the all-actions property MFI is also correct.

## 6. Proposition 5: conditional integer-cocycle FI criterion

**Accepted under every hypothesis actually stated.** The group is countable and nonamenable, the action is free, ergodic and p.m.p., Hom(Gamma,Z) vanishes, and superrigidity is explicitly for all measurable integer-valued cocycles of that particular action.

1. Freeness and nonamenability give the needed nowhere-amenable relation; this interface is stated at the zero-Betti criterion in Alvarez–Gaboriau. The action supplies ergodicity. Binary essential splitting follows from the aperiodic non-FI assumption.
2. TW v3 Lemma 5.1 applies with those hypotheses. Its conclusion is an aperiodic amenable **free factor with full domain**, after removal of a null set. Neither a factor confined to a positive-measure subset nor a merely amenable subrelation would suffice for the proof as written.
3. The Connes–Feldman–Weiss generator theorem applies to this amenable countable measured relation even if it is not ergodic. Since its generator lies in the relation's full group, it preserves the given probability measure. Since its orbits equal the infinite relation classes, the generator has no nonzero periods almost everywhere. It therefore defines a free p.m.p. Z-action on the full conull domain.
4. The exponent cocycle on that factor and the zero cocycle on the complementary factor extend measurably by the free-product normal form. The supplement gives a countable Borel path construction. Collapsing consecutive edges in a factor uses its cocycle identity, while cancelling an edge with its reverse contributes zero. Thus the extension is well defined and additive.
5. Pullback to Gamma is a measurable cocycle with the convention fixed in the packet. Superrigidity and Hom(Gamma,Z)=0 yield a coboundary. Countability permits one conull set for all group elements, after which a point-dependent Borel choice of the element carrying x to Tx is legitimate.
6. The resulting identity b(Tx)−b(x)=1 is impossible for a Z-valued measurable b under a probability-preserving T: all integer level sets would have equal mass and their countable union has mass one. Neither integrability of b nor ergodicity of T is required.

This is a sufficient action-specific criterion. It neither constructs an action satisfying it in a candidate mixed group nor proves the criterion necessary. The realization problem remains completely open within the packet.

### Bernoulli obstruction

**Accepted with the frozen scope.** Peterson–Sinclair provides an obstruction to U_fin-cocycle superrigidity of a Bernoulli action at nonzero first L2-Betti number. Its Section 4 constructs a circle-valued obstruction. That does not supply an integer-valued obstruction. The packet correctly uses the stronger Bernoulli hypothesis only to force zero first L2-Betti number, after which the nonamenable all-actions FI criterion eliminates the desired second action. It does not extend that obstruction to Z-only superrigidity or to arbitrary actions.

## 7. Readiness exclusions and terminal boundary

**Accepted.** Finite free orbit relations are FI. Infinite amenable free actions yield aperiodic hyperfinite relations and hence are non-FI. Nonamenable zero-Betti groups have only FI free actions. For an infinite strongly treeable group, every free action is both aperiodic and treeable, and the exact aperiodic clause of Alvarez–Gaboriau Proposition 4.6 supplies an essential measured decomposition. Thus the cited strong-treeability classes cannot furnish the mixed pair. Finite members must be treated separately, as they are in the frozen packet.

The required witness would have to evade these exclusions, including the vanishing-Betti class. None is exhibited. Ordinary one-endedness, one treeable action, one FI subrelation, or a finite sampled orbit cannot replace that missing witness.

The bounded literature-search outcome is accepted only as a description of the recorded search, not as proof of current global openness, exhaustive priority or novelty. The audited disposition is **unresolved by this work, with five valid scoped routes and no sixth route attempted**.

## 8. Reproducibility and publication boundary

This is a proof-and-source audit, not a computational proof. No numerical solver, sampled graph or orbit test was used. Shell and standard PDF utilities were used only to inspect documents, render pages and compute file digests. No mathematical verification program was introduced; normal/-O/-OO and nonroot read-only execution tests are therefore not claims made by this packet.

The shareable audit files contain authored mathematical discussion, public citations, public-source hashes and input/output file hashes. They contain no copied source bodies, datasets, private sources, personal data or coordination records. Publication, GitHub and queue state were not changed in this audit.

## Public references

- Alvarez–Gaboriau, *Free products, orbit equivalence and measure equivalence rigidity*: https://ems.press/content/serial-article-files/29614
- OWR 49/2008, report pp. 2767–2770: https://ems.press/content/serial-article-files/46193
- Tucker-Drob–Wróbel, v3: https://arxiv.org/abs/2410.11754v3
- Conley–Gaboriau–Marks–Tucker-Drob, v3: https://arxiv.org/abs/2104.07431v3
- Peterson–Sinclair: https://math.vanderbilt.edu/peters10/petersonsinclair.pdf
- Connes–Feldman–Weiss, *An amenable equivalence relation is generated by a single transformation*, ETDS 1 (1981), 431–450: https://doi.org/10.1017/S014338570000136X
