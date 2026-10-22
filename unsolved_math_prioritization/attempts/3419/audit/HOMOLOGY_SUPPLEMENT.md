# Supplement: the rational second Betti number is exactly seven

This independent calculation strengthens the frozen lower bound without changing its conclusion. It concerns only the group Γ₆ constructed in [Kegel–Li–Ren, arXiv:2609.10461v1](https://arxiv.org/abs/2609.10461). The HNN decompositions and the edge presentations are the same cited inputs as in Proposition 5. No novelty or solution of OPG-37237 is claimed.

Write bᵢ(G)=dim_Q Hᵢ(G;Q) and δ(G)=b₂(G)−b₁(G). All vertex groups here are finitely presented, so the dimensions used are finite.

## Exact-sequence identity

For an injective HNN extension J of V with edge group W, let ρᵢ be the rank of the difference map Hᵢ(W;Q)→Hᵢ(V;Q). When b₁(W) is finite, the homology sequence gives

    b₂(J) = b₂(V) − ρ₂ + b₁(W) − ρ₁,
    b₁(J) = b₁(V) − ρ₁ + 1.

Consequently

    δ(J) = δ(V) + b₁(W) − ρ₂ − 1.

For a centralizing extension, ρ₂=0, even without any assumption that W is free or has finite-dimensional H₂. For a general edge with finite b₂(W), ρ₂≤b₂(W).

## The extra information about Δ

Put p=P⁻¹tP. Re-express Γ₃ as the extension of Γ₂ in which p centralizes P⁻¹⟨c,d⟩P. The subgroup B=⟨c,e⟩ of Γ₂ is free on c,e. The elementary subgroup lemma for an identity-centralizing HNN extension, applied to B, identifies

    Δ=⟨B,p | [p,h]=1 for h in B∩P⁻¹⟨c,d⟩P⟩.

This does not identify the intersection or assume it is trivial. Nevertheless every additional relation is a commutator, and B has no relations on c,e. Hence

    Δ_ab ≅ Z³,
    b₁(Δ)=3.

The subgroup lemma follows directly from Britton reduction: a word in B and p has a pinch in the ambient group exactly when its intervening B element lies in the indicated intersection. Since the associated map is the identity, reduction stays in B.

## Tracking δ instead of only b₂

The first stage has b₂(Γ₁)=b₁(Γ₁)=2, so δ(Γ₁)=0.

- The F₅ edge for Γ₂ has H₂=0, giving δ(Γ₂)=0+5−1=4.
- The F₂ centralizing edge for Γ₃ gives δ(Γ₃)=4+2−1=5.
- Centralizing Δ gives δ(Γ₄)=5+3−1=7.
- The Γ₅ edge A has b₁(A)=3 and b₂(A)=3. Thus δ(Γ₅)≥7+3−3−1=6.
- The Γ₆ edge C=F₂×Z has b₁(C)=3 and b₂(C)=2. Thus δ(Γ₆)≥6+3−2−1=6.

For A, the abelianization can also be read directly: d and e have order dividing three, while s,c,t contribute three free summands. The b₂(A)=3 computation is the one independently checked in the main audit.

The abelianization of Γ₆ is Z, as established in the frozen proof. Therefore

    b₂(Γ₆)=δ(Γ₆)+1≥7.

## Matching upper bound

The source gives a presentation of Γ₆ with three generators and nine relators. Its presentation 2-complex X has one 0-cell, three 1-cells and nine 2-cells. Since H₁(X;Q)=H₁(Γ₆;Q)=Q, the cellular boundary C₂→C₁ has rank two, so b₂(X)=9−2=7.

The Hopf exact sequence surjects H₂(X;Q) onto H₂(Γ₆;Q), whence b₂(Γ₆)≤7. Combining both bounds proves

    dim_Q H₂(Γ₆;Q)=7.

This uses only a presentation-complex upper bound, not an inference that the presentation is aspherical or realizes the abstract group deficiency. It makes the sphere-knot obstruction stronger but does not address the missing 2-knot realization of any replacement group.
