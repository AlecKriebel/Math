# Weinstein fillings of exact four dimensional two handlebodies

## Result and scope

**KP-4.110, problem 2986, remains unresolved in this investigation.** Four bounded mathematical approaches produce an explicit warning example, two elementary topological exclusions, and a conditional mixed-torus reduction. None constructs the requested filling or proves its universal nonexistence. No novelty or priority claim is made for these elementary observations.

The target is a compact smooth four-manifold W admitting a handle decomposition with indices 0, 1, and 2 only, together with a one-form λ such that dλ is symplectic, its Liouville vector field is outward transverse to the boundary, and the induced contact manifold (∂W, ker(λ|∂W)) cannot be filled by any Weinstein structure on that same smooth W. This is the question recorded in K3, printed page 282 [K3]. A contact structure admitting no Weinstein filling on any manifold would be a stronger obstruction.

The following distinctions are essential:

* A particular Liouville vector field failing to be gradient-like is weaker than its primitive failing to be Liouville-homotopic to a Weinstein primitive.
* Even failure of that homotopy would not by itself rule out a different Weinstein structure on W inducing the same boundary contact structure.
* A two-dimensional CW homotopy type is necessary for a smooth four-dimensional 2-handlebody but is not a substitute for an actual smooth handle decomposition.
* Homotopy through nondegenerate two-forms is a formal condition. It is not the same as a Liouville homotopy with convex boundary, nor does it prescribe the boundary contact structure.

## 1 An explicit periodic Liouville orbit on the standard ball

**Proposition 1.** The standard symplectic four-ball admits a Liouville primitive whose vector field has a nonconstant periodic orbit, while its symplectic form and boundary contact form agree with the standard Weinstein ball. The primitive is Liouville-homotopic to the standard primitive through a path fixed near the boundary.

**Proof.** Write q=(q₁,q₂), p=(p₁,p₂), let

    B⁴ = {|q|² + |p|² ≤ 1},
    ω₀ = dq₁∧dp₁ + dq₂∧dp₂,
    λ₀ = (q₁dp₁ + q₂dp₂ − p₁dq₁ − p₂dq₂)/2,
    J(q₁,q₂) = (−q₂,q₁).

Choose a smooth function χ(s) equal to 1 for s≤1/2 and to 0 for s≥3/4. An explicit choice is

    η(u) = 0 for u≤0, and exp(−1/u) for u>0,
    χ(s) = η(3/4−s) / [η(3/4−s) + η(s−1/2)].

The denominator is positive for every real s: its two arguments cannot both be nonpositive. Define

    f(q,p) = p·Jq − (p·q)/2,
    F(q,p) = χ(|q|²+|p|²) f(q,p),
    λₜ = λ₀ + t dF,     0≤t≤1.

Since d²F=0, we have dλₜ=ω₀ for every t. On a neighborhood of ∂B⁴, F=0, so every λₜ equals λ₀ there. The associated Liouville vector field is therefore the outward radial field near the boundary. This proves that the entire path consists of Liouville domains with the same boundary contact form.

On the region s<1/2, F=f. For a vector field X=(a,b) in q,p coordinates, ι_Xω₀=a·dp−b·dq. Direct differentiation gives, at t=1,

    λ₁ = (−p₁+p₂)dq₁ + (−p₁−p₂)dq₂ − q₂dp₁ + q₁dp₂,
    X₁(q,p) = (Jq, p+Jp).

Consequently

    γ(θ) = ((cos θ)/2, (sin θ)/2, 0, 0)

is an integral curve of X₁, with period 2π. Its squared radius is 1/4, so the complete orbit remains in the region where χ=1. It is nonconstant and X₁ is nonzero on it.

If X₁ were gradient-like for a Weinstein Morse function φ, then dφ(X₁)>0 along this orbit. Integration over one period would give φ(γ(2π))−φ(γ(0))>0, contradicting periodicity. Thus this particular primitive is not Weinstein. On the other hand, λ₀ is Weinstein: its vector field is X₀=(q,p)/2, and φ₀=|q|²+|p|² is a Morse function with a single index-zero critical point and X₀φ₀=|q|²+|p|². Reversing λₜ gives the asserted Liouville homotopy. ∎

This is a counterexample to a proposed obstruction test, **not a counterexample to KP-4.110**. It even uses the same symplectic form and the same contact form, not merely contactomorphic boundaries. Detecting a periodic orbit in one primitive therefore cannot settle the target.

The algebraic diagnostic accompanying this note differentiates the polynomial f exactly over rational coefficients. The smooth cutoff, the existence of the periodic integral curve, and the gradient-like contradiction are proved above, rather than inferred from numerical trajectory sampling.

## 2 Cover homology cannot distinguish the requested handlebodies

**Proposition 2.** If W has a handle decomposition using only handles of indices at most 2, then every covering space W̃ of W has the homotopy type of a CW complex of dimension at most 2. In particular Hₖ(W̃;A)=0 for every k>2 and every constant coefficient group A. The analogous assertion holds for homology with any local coefficient system on W.

**Proof.** The cores of the handles give W the homotopy type of a CW complex K with one cell of the corresponding index for each handle. Pulling a cover back along a homotopy equivalence K→W gives a covering CW complex K̃→K and a homotopy equivalence K̃→W̃. Its cells are lifts of cells of K, so no cells have dimension above 2, even if the cover is infinite. Its cellular chain groups in those degrees vanish. For local coefficients on W, the cellular chains are formed from the cellular chains of the universal cover by tensoring with the coefficient module; the zero chain groups remain zero. ∎

In particular, a finite cover with nonzero third homology would disprove the 2-handlebody hypothesis itself. It would not provide a genuinely new obstruction separating exact and Weinstein structures within that hypothesis. Conversely, vanishing third homology, even in many covers, does not construct a smooth 2-handlebody decomposition.

## 3 Attaching low index handles cannot repair the known third homology defect

**Proposition 3.** Let X′ be obtained from a compact manifold X by attaching finitely many ordinary handles of indices at most 2. Then Hₖ(X;A)→Hₖ(X′;A) is an isomorphism for every k≥3 and every constant coefficient group A.

**Proof.** The pair (X′,X) has a relative CW model with cells only in dimensions 0, 1, and 2. Hence both Hₖ₊₁(X′,X;A) and Hₖ(X′,X;A) vanish for k≥3. The long exact sequence of the pair gives the claimed isomorphism. ∎

If M is a closed connected oriented three-manifold, then H₃(M×[0,1];Z)=Z. Therefore adding any finite collection of 1- and 2-handles to M×[0,1] leaves a nonzero third homology group. The resulting four-manifold cannot be a 2-handlebody.

This applies to the product-and-1-handle construction discussed explicitly in Bowden's Section 3 [B]. It also applies to adding round symplectic 1-handles: Christian–Menke identify each such attachment with a Weinstein 1-handle followed by a Weinstein 2-handle [CM, Remark 2.6]. Thus simply attaching those handles to the known product examples cannot meet the target. The claim concerns attachment. It does not rule out a different construction using removal, replacement, or a genuine 3-handle; those operations require a separate symplectic and boundary analysis.

## 4 A conditional reduction along a mixed torus

Christian–Menke's current theorem [CM, Theorem 1.1] splits an exact filling along a mixed torus into an exact filling W′ and reconstructs W by a round symplectic 1-handle. The allowed splitting slope is constrained by the contact neighborhood; a merely convex torus is insufficient.

**Proposition 4.** Suppose an exact filling (W,λ) has a splitting of this kind. Suppose every connected component of W′ admits a Weinstein structure inducing the same cooriented boundary contact structure under a boundary identification which preserves the marked round-handle attaching data. Then W admits a Weinstein structure inducing the original boundary contact structure.

**Proof.** Use the hypothesized Weinstein structures on the disjoint union W′. The boundary contact identification transports the marked Legendrian attaching knots and their standard neighborhoods. Contactomorphic boundary neighborhoods have compatible symplectization collars: if their contact forms differ by a positive factor, translate by the logarithm of that factor in the symplectization coordinate. Thus the prescribed contact handle attachments can be made using the replacement Weinstein structures. By [CM, Remark 2.6], first attach a Weinstein 1-handle and then the specified Weinstein 2-handle. The result is Weinstein. The marked smooth attaching data agree with those reconstructing W, so its underlying smooth manifold is W. Contact handle attachment determines the outgoing boundary contact structure from the incoming contact data, so it agrees with the original one up to the prescribed contact identification. ∎

The markings cannot be discarded: knowing only that an unmarked boundary manifold is Weinstein fillable does not produce a Weinstein structure on the particular split filling with the needed boundary identification.

If W were a positive example for KP-4.110 and such a mixed-torus split existed, at least one split component would fail the compatible Weinstein-replacement hypothesis. Furthermore Proposition 3 gives H₃(W′;Z)=H₃(W;Z)=0. This does not show that W′ is itself a smooth 2-handlebody: deleting a 1-/2-handle pair from one decomposition is not a theorem cancelling all higher handles in an arbitrary presentation of W′. Neither the existence of a mixed torus nor a classification of the relevant split fillings has been established here.

There are genuine special cases where this route already forces a Weinstein filling. For example, [CM, Theorem 1.4 and Corollary 1.5] treat Legendrian surgery on a knot in the standard contact three-sphere stabilized with both signs. Their classification reconstructs exact fillings by the corresponding symplectic 2-handle from the standard sphere's filling. This is an attributed special-case exclusion, not an extension to every contact boundary in KP-4.110.

## Literature and hypothesis audit

The inspection date is 6 October 2026. This was a bounded primary-source check, not a claim to exhaustive literature coverage.

* [K3], printed page 282, states the target and explains why known 3-handle examples do not supply it. The author preliminary PDF was downloaded, hashed, text-inspected, rendered, and visually inspected at the relevant page.
* [B] distinguishes a particular non-Stein exact filling from a contact manifold with no Stein filling. Section 3 retains third homology in the natural construction; Section 4 supplies contact-boundary obstructions. Neither fact removes the 2-handlebody requirement.
* [CM] is arXiv:1807.03420v4, 21 May 2025. Theorem 1.1 concerns exact or weak fillings. Remark 1.3 explicitly corrects the former strong-filling statement. This note uses only the exact case. K3 also points to [S], the 2019 higher-genus splitting preprint. We do not transplant its old strong-filling phrasing into the current mixed-torus theorem.
* [CE, Theorems 1.2 and 5.2] assume real dimension greater than four. Its four-dimensional cobordism alternative in Theorem 5.1 has an extra overtwisted negative-boundary hypothesis. These are not a general existence theorem for the compact four-dimensional exact fillings here. Even a formal existence theorem without control of the positive boundary would leave the target's contact-boundary condition to prove.
* [BC] v3, 12 October 2025, states acceptance by the Journal of Topology and proves stable Weinstein results for particular torus-bundle Liouville domains. Stabilization changes dimension. Its Liouville-homotopy questions also differ from unrestricted existence of a Weinstein structure on a fixed W with its fixed contact boundary. We do not apply its informal introduction's general existence wording as a dimension-four theorem.
* [H] studies Liouville interpolation systems and persistent three-dimensional skeleta, including a classification under additional transversality hypotheses. The product-type objects and theorem scope inspected do not supply the required compact 2-handlebody.

The problem's web page was requested but returned an access error through the available retrieval routes. The exact inherited statement and the directly inspected K3 primary problem statement agree. No assertion about the current contents of the inaccessible web page is made.

Bounded repository checks found no exact-ID PR, branch, commit, or default-branch code result for 2986. A thematic PR search returned work on separate IDs 2985 and 3024; neither was treated as a solution or a prior attempt for this ID. Search silence is not proof of novelty.

## Remaining gap and stopping decision

For a positive solution one must construct W and λ satisfying all four requirements simultaneously: a verified smooth handle decomposition with indices at most 2, an everywhere nondegenerate exact form, a convex boundary carrying the stated contact structure, and an obstruction to every Weinstein filling structure on that W with that contact boundary. For a negative solution one must prove the corresponding Weinstein existence theorem for every such pair.

Proposition 1 defeats a primitive-level obstruction. Propositions 2 and 3 exclude easy topology-based constructions. Proposition 4 reduces a suitable example to a precise boundary-marked filling problem, without solving that problem. No candidate survives all requirements, and no universal theorem is established. The investigation stops as **partial, stalled after 4 of 5 permitted approaches**, rather than inventing a fifth approach without a concrete route. The partial results are authored elementary proofs; their novelty is unassessed. Automated checking does not constitute formal proof verification or human peer review.

## References

[K3] *K3: A New Problem List in Low-Dimensional Topology*, author preliminary version, Problem 4.110, printed p. 282. https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf

[B] Jonathan Bowden, *Exactly fillable contact structures without Stein fillings*, Algebraic & Geometric Topology 12 (2012), 1803–1810, doi:10.2140/agt.2012.12.1803. Inspected arXiv v3: https://arxiv.org/pdf/1201.6550v3

[CM] Austin Christian and Michael Menke, *A JSJ-type decomposition theorem for symplectic fillings of contact 3-manifolds*, arXiv:1807.03420v4 (21 May 2025), Theorem 1.1, Remark 1.3, Theorem 1.4, Corollary 1.5, Remark 2.6. https://arxiv.org/pdf/1807.03420v4

[S] Austin Christian and Michael Menke, *Splitting symplectic fillings*, arXiv:1909.00420v1 (1 September 2019). https://arxiv.org/pdf/1909.00420v1

[CE] Kai Cieliebak and Yakov Eliashberg, *Flexible Weinstein manifolds*, MSRI Publications 62 (2014), 1–42. https://library.slmath.org/books/Book62/files/eliashberg.pdf

[BC] Joseph Breen and Austin Christian, *Torus bundle Liouville domains are stably Weinstein*, arXiv:2109.07615v3 (12 October 2025), accepted-version status stated by authors. https://arxiv.org/abs/2109.07615v3

[H] Surena Hozoori, *Regularity and persistence in non-Weinstein Liouville geometry via hyperbolic dynamics*, arXiv:2409.15592v1 (23 September 2024). https://arxiv.org/abs/2409.15592v1
