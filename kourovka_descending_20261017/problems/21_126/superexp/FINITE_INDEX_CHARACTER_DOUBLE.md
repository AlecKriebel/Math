# Different-character doubles after arbitrary finite-index passage

Status: strengthening of ASYMMETRIC_CHARACTER_DOUBLE.md; the independent delta audit passed after making the finite-type fiber hypothesis explicit. See review/FINITE_INDEX_CHARACTER_AUDIT.md and its exact-input receipt. This remains a partial obstruction, not a resolution of 21.126.

Let Σ_i be finitely generated (hence finitely presented) fundamental groups of compact surfaces, and let Γ_i=Σ_i⋊⟨t_i⟩ be automatic surface-by-cyclic groups with height h_i onto Z; the closed fibered hyperbolic 3-manifold examples suffice. Let E=Γ₁×Γ₂ and G=ker(h₁−h₂). For every finite-index G₀≤G and primitive χ:G₀→Z with finitely generated kernel N, the double D₀=G₀ *_N G₀ has at-most-exponential intrinsic Dehn function.

The claim does not assert that χ extends to the original E or that G₁ *_N∩G₁ G₁ has finite index in D₀. Both shortcuts are unnecessary.

## 1. Place a finite-index part of G₀ in a product ambient

Since G is finitely generated, it has only finitely many subgroups of each fixed finite index (use the finitely many permutation representations on a set of that size). Let C be the core of G₀ in G. Since G◁E, every E-conjugate of C is a subgroup of G of the same index. Intersect the finitely many such conjugates to get K◁E with K≤G₀ and [G:K]<∞.

The quotient E/K fits into 1→F=G/K→E/K→Z→1 with F finite. Choose t mapping to1∈Z. This extension splits, E/K=F⋊⟨t⟩. The conjugation action of t on F has finite order r. There is a finite quotient F⋊(Z/rZ) retaining F injectively. The inverse image E₀≤E of the kernel of this quotient has finite index and E₀∩G=K. (For trivial action take r=1.)

Every finite-index subgroup of Γ₁×Γ₂ contains a finite-index product Γ₁′×Γ₂′: take Γ₁′={g:(g,1)∈E₀} and Γ₂′={g:(1,g)∈E₀}. Set G₁=G∩(Γ₁′×Γ₂′). Then G₁ has finite index in G and lies in G₀.

## 2. Align heights without losing G₁

Write h_i(Γ_i′)=l_i Z, l_i≥1, and Σ_i′=Γ_i′∩Σ_i. Choose z_i∈Γ_i′ with height l_i. Thus Γ_i′=Σ_i′⋊⟨z_i⟩. Put L=lcm(l₁,l₂) and

    Λ_i=⟨Σ_i′, z_i^{L/l_i}⟩.

Each Λ_i has finite index in Γ_i′. Every element of G₁ already has common height divisible by L, so

    G₁=G∩(Λ₁×Λ₂)
      =(Σ₁′×Σ₂′)⋊⟨τ=(z₁^{L/l₁},z₂^{L/l₂})⟩.

The two monodromy automorphisms need not coincide. Each height is normalized by L on Λ_i, so G₁ is the kernel of their difference map Λ₁×Λ₂→Z.

Every character of this displayed G₁ extends to Λ₁×Λ₂, by the same exact argument as in ASYMMETRIC_CHARACTER_DOUBLE.md: its restrictions to Σ₁′ and Σ₂′ are invariant under their corresponding monodromies separately. Extend those restrictions by value0 on each normalized stable lift, then add the value on τ times the first normalized height.

## 3. Use a finite-index subgroup of the actual double image

Since G₁ has finite index in G₀ and χ is onto, χ(G₁)=kZ for some k≥1. Let χ₁=χ|G₁/k, a primitive integral character, and let χ̃₁:Λ₁×Λ₂→Z be its extension just constructed.

The previously proved fold/quotient injection identifies D₀ with

    {(g,w)∈G₀×F(u,v):χ(g)=ε(w)},  ε(u)=ε(v)=1.

Let F′=ε⁻¹(kZ), a finite-index finitely generated free subgroup of F₂, and ε₁=ε|F′/k. Intersect the *actual image* of D₀ with G₁×F′. The result D′ has finite index in D₀ and is exactly

    {(g,w)∈G₁×F′:χ₁(g)=ε₁(w)}.

It is the kernel in Λ₁×Λ₂×F′ of the map

    (a₁,a₂,w)↦( h₁(a₁)/L−h₂(a₂)/L,
                    χ̃₁(a₁,a₂)−ε₁(w) ) ∈ Z².

The ambient group is automatic: finite-index subgroups of automatic groups and their finite direct products are automatic, and F′ is free. The group D₀ is finitely presented, using finite presentability of G₀ and finite generation of N. Therefore its finite-index subgroup D′ is finitely presented as well. Apply the directly inspected Llosa Isenrich2404.12334v2 Corollary1.3 to this coabelian kernel. It gives δ_D′≤exponential. Finite-index invariance of the Dehn equivalence class yields the same upper bound for D₀.

This is an intrinsic Dehn proof and does not require N to be finitely presented. It excludes the proposed first different-character amplification even after arbitrary finite-index passage in the original surface-product example. The proof does not establish that all later iterated subgroups have this product-fiber structure; a later genuinely different construction remains outside this statement.
