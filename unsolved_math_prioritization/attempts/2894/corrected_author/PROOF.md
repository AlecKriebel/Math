# Proof of the literature implication and scope audit

## Target

K3 Problem 4.18 concerns smooth, closed manifolds of dimension four. Part (a) asks for homotopy-equivalent manifolds between which no simple homotopy equivalence exists. Part (b) instead requires a smooth h-cobordism and excludes every smooth s-cobordism between the endpoints. No orientability restriction is imposed by the problem; oriented examples qualify. Smooth compact manifolds have finite triangulations, so ordinary finite-complex simple homotopy theory applies here. These are existence questions about pairs, not assertions about a prescribed map or cobordism.

## Accepted literature inputs

HU, Corollary D (page 5), supplies a finite 2-group G with the strict inclusion ker(κ₂ˢ) ⊊ ker(κ₂ʰ) in H₂(G; Z/2). Corollary 4.9 (page 16) identifies G = SmallGroup(128,1377) as a witness: κ₂ˢ is nonzero and κ₂ʰ is zero. These are accepted source theorems, not computations independently reproduced by this packet.

KNV, Theorem C (page 3; proof pages 20–21), states that such a finitely presented group exists exactly when there exist closed oriented smooth four-manifolds that are homotopy equivalent but are not simple homotopy equivalent even after stabilization by S² × S². Its proof produces manifold fundamental group G * G; the finite witness group must not be misreported as the manifold fundamental group. [HU](https://arxiv.org/pdf/2602.05003v1), [KNV](https://arxiv.org/pdf/2405.06637v2).

HU uses the standard oriented involution g ↦ g⁻¹ and L-groups localized at 2. KNV uses the corresponding oriented assembly components into L₄ˢ(ZG) and L₄ʰ(ZG). These are compatible: the source H₂(G; Z/2) has exponent 2, so every assembly image is killed by 2 and localization at 2 preserves its vanishing. Thus HU’s statement supplies the integral kernel inequality KNV needs. The degree-two class w used later in KNV is normal 1-type data, not a nontrivial orientation character.

## Deduction of part (a)

A finite group is finitely presented: introduce one generator u_g for each group element, impose u_1 = 1 and u_g u_h = u_(gh) for every pair. There are finitely many generators and relations, and the evident maps to and from the group are inverse.

Apply this observation to the HU witness. Its strictly nested kernels satisfy KNV's group hypothesis. KNV consequently gives a smooth closed oriented pair M,N with an actual homotopy equivalence, and with no simple homotopy equivalence after any allowed stabilizations. Taking zero stabilizations excludes a simple homotopy equivalence M → N. Forgetting the extra orientation structure leaves smooth closed four-manifolds satisfying part (a).

The conclusion is an unmarked manifold distinction. KNV's proof checks the obstruction for all normal 1-smoothings, rather than only one marked map. It separates a nonzero mod-2 tertiary class from the zero class of a nullbordant comparison manifold, so orientation reversal does not turn this distinction into zero. This also prevents silently weakening the target to orientation-preserving maps only.

This is a proof from two cited theorem inputs, not a new independent proof of either surgery-theoretic theorem, a rerun of HU's group computations, or a new construction of Kirby diagrams.

## Why a nonsimple map alone would not suffice

For finite connected CW complexes, fix a homotopy equivalence f:X → Y. Let T(X) be the set of torsions of all self-homotopy equivalences of X. The torsion composition rule gives

τ(f ∘ a) = τ(f) + f_*τ(a).

Every homotopy equivalence g:X → Y is homotopic to f ∘ a for a self-homotopy equivalence a: take a = f⁻¹ ∘ g. Therefore X and Y are simple homotopy equivalent if and only if 0 belongs to τ(f) + f_*T(X). This is a set criterion; T(X) need not be called a subgroup. In particular τ(f) ≠ 0 does not exclude another simple equivalence. The zero-torsion characterization and composition rule are standard; see [NNP, Section 2](https://arxiv.org/pdf/2312.00322v4).

## Part (b): exact unresolved gap

The result above does not assert a smooth h-cobordism between M and N. Thus its exclusion of simple homotopy equivalence cannot supply the missing hypothesis in part (b).

A smooth s-cobordism always supplies a simple equivalence between its endpoints: compose one simple boundary inclusion with a homotopy inverse of the other. Hence a smoothly h-cobordant pair with no simple equivalence would suffice. No such smooth h-cobordism is established here. Conversely, exhibiting a single h-cobordism with nonzero torsion excludes only that particular cobordism from being an s-cobordism; it does not exclude another s-cobordism with the same endpoints.

KP Question 1.2 explicitly leaves the general implication open. Theorem A and Corollary B establish it when a connected oriented M has finite fundamental group and one of the following holds: SK₁ vanishes and L₅ˢ → L₅ʰ is injective; SK₁ vanishes and M is topologically pre-stabilized; or M is smoothly pre-stabilized. Finite cyclic groups satisfy the first condition. Orientation and finite-group hypotheses must be retained. [KP, pages 1–2](https://arxiv.org/pdf/2604.27635v2).

Final mathematical disposition: affirmative prior result for (a), unresolved (b), no full resolution and no novelty claim.
