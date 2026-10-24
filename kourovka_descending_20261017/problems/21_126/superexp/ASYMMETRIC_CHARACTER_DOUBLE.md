# A genuinely different-character double remains coabelian

Status: new route requested after the initial family report. A fresh independent delta audit passed; see review/ASYMMETRIC_CHARACTER_AUDIT.md and its exact-input receipt. It is an obstruction to this attempted super-exponential construction, not a solution of 21.126 or a novelty claim.

## General extendable-character lemma

Let A be a finitely presented automatic group, Φ:A→B a homomorphism to a finitely generated abelian group, and G=ker Φ finitely presented. Let χ:G→Z be onto, with finitely generated kernel N. Suppose χ extends to a homomorphism χ̃:A→Z. Put ε:F(u,v)→Z, ε(u)=ε(v)=1.

The normal double D=G *_N G is isomorphic to the coabelian subgroup

    ker Ψ ≤ A×F(u,v),
    Ψ(a,w)=(Φ(a), χ̃(a)−ε(w)) ∈ B×Z.

To prove equality of the subgroup, first use the injective fold/quotient map

    D → G×F(u,v).

Its image lies in {(g,w):χ(g)=ε(w)}. For the converse choose t∈G with χ(t)=1. Given a pair (g,w) with common value k, lift each u to the first-copy t, each v to the second-copy t, and inverses accordingly. The resulting element of D has image (t^k,w). Multiplying by the common-kernel element g t^{-k} gives (g,w). Thus the image is exactly that fiber product. Inside A×F₂ the equations Ψ=0 say precisely a∈G and χ(a)=ε(w), proving the asserted kernel identity.

The double is finitely presented: two finite presentations of G plus the finitely many identifications of generators of N suffice. Finite presentation of N is not assumed. The group A×F₂ is automatic, because direct products preserve automaticity (one may use the synchronous structure; asynchronously automatic factors are also covered by the cited theorem if an applicable product structure is supplied).

The directly inspected primary theorem is Llosa Isenrich, *From the second BNSR invariant to Dehn functions of coabelian subgroups*, arXiv:2404.12334v2 (October 30, 2024), **Corollary 1.3**, printed p.2. It states that a finitely presented kernel of a homomorphism from a finitely presented automatic group to a finitely generated abelian group has an exponential Dehn upper bound. It does not require the displayed homomorphism to be surjective. Apply it to Ψ:

    δ_D(n) ≤ C^n    for some C>1.

Therefore the proposed double does not have super-exponential Dehn function. This conclusion uses the actual intrinsic coabelian theorem, not the invalid inference from the upper estimate δ_G(exp n) to a lower bound.

The same proof works if only a positive integer multiple mχ extends to χ̃:A→Z: replace χ̃(a)−ε(w) by χ̃(a)−mε(w). On a∈G, its vanishing is equivalent to χ(a)=ε(w). This rational-extension variant still has finitely generated abelian target, so no surjectivity issue arises.

## The new character on the known exponential example

Let Σ₁,Σ₂ be two copies of a finitely generated surface group Σ. Let φ∈Aut(Σ) define an automatic mapping-torus group Γ=Σ⋊_φ⟨t⟩, for example the group of a closed fibered hyperbolic 3-manifold. Take E=Γ₁×Γ₂ and let h_i:Γ_i→Z be the stable-letter height. Then

    G=ker(h₁−h₂:E→Z)
     =(Σ₁×Σ₂)⋊_{(φ,φ)}⟨τ=(t₁,t₂)⟩.

This is the classical exponential-Dehn subgroup used in the RAAG examples after finite-index passage. For the argument below only its explicit semidirect-product presentation and finite presentability are required; no claim that every φ produces exponential Dehn growth is needed.

**Every integral character χ:G→Z extends to E.** To see this, let λ_i be its restriction to Σ_i, and c=χ(τ). The conjugation relation by τ forces λ_i∘φ=λ_i separately, since the two surface factors are independent. Hence λ_i extends to a homomorphism λ̃_i:Γ_i→Z by λ̃_i(t_i)=0. Set

    χ̃(g₁,g₂)=λ̃₁(g₁)+λ̃₂(g₂)+c h₁(g₁).

On the diagonal-height subgroup this agrees exactly with χ, as follows by writing each element (s₁,s₂)τ^k. Thus even a character nonzero on one or both surface factors, independent of the original diagonal height, meets the general lemma's extension hypothesis.

If χ is onto and kerχ is finitely generated, the double D is finitely presented and has the explicit coabelian realization

    D=ker[(Γ₁×Γ₂×F₂)→Z²],
    (g₁,g₂,w)↦(h₁(g₁)−h₂(g₂),χ̃(g₁,g₂)−ε(w)).

The ambient group is automatic. Corollary 1.3 therefore proves δ_D≤exponential, regardless of whether kerχ is finitely presented. Invariant cohomology of φ can provide many different characters, but it does not evade the coabelian ceiling. A nonprimitive nonzero character is first divided by its positive image generator; its kernel is unchanged and the normalized character also extends by the same formula. The zero character simply gives the degenerate double G.

## Iteration and precise escape condition

Suppose one repeats the construction a finite number of times. At each step use a finitely presented coabelian subgroup of the current automatic ambient group and a primitive character with finitely generated kernel whose positive multiple extends to that ambient group. The displayed kernel formula realizes the next double as another coabelian subgroup of the previous ambient group times F₂. Induction and Corollary 1.3 give the same exponential upper bound at every stage.

This does **not** prove that every character of every later doubled subgroup extends, or that an arbitrary asymmetric iterated construction is coabelian. A future route must produce a genuinely nonextendable character (and prove a super-exponential intrinsic lower bound), or another mechanism. In the original surface-product example, however, all characters extend, so the first proposed different-character amplification is rigorously excluded. No such escape construction was obtained here.
