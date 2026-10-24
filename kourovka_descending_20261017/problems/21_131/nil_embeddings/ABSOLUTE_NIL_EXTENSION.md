# Optional homogeneous and residually finite source strengthening

Private independent derivation, 2026-10-24 18:47 UTC. Completion estimate: 95% for this optional strengthening, pending another reader's check of the base-change argument. The original verified broad proof in EMBEDDING_PROOF.md is unchanged. No new agent was spawned for this task; no Git, publication, or outreach occurred.

## Statement

For the locally finite p target H of the tree family, the requested epimorphism can be chosen with source a subgroup of a **classical homogeneous Golod group**, itself finitely generated and residually finite. More generally, every countably infinite locally finite p-group is a quotient of a subgroup of such a classical homogeneous Golod group.

This is a source strengthening of the original verified result. It gives an epimorphism from a source subgroup; it does not claim that the target embeds in a residually finite classical Golod group by this lifting argument.

The only new external input is Hammoudi, *Quotients of nilalgebras and their associated groups*, Pacific J. Math. 212(1) (2003), 93–101, DOI https://doi.org/10.2140/pjm.2003.212.93, Theorem 3 (p.96) and Corollary 3 (p.97). The actual primary PDF is retained under sources/Hammoudi_2003.pdf. Its exact assumption is absolute nilness, not merely stable nilness. We therefore establish absolute nilness for the particular algebra in the original construction by tracking the explicit AAJZ construction under field extensions.

Write F=F_p. An F-algebra A is **absolutely stable nil** here if M_n(A⊗_F E) is nil for every extension field E/F and every finite n. This is an explicit descriptive definition for this note, not a named theorem assumed from the literature.

## 1. The input augmentation ideal is absolutely stable nil

Let K be the countable locally finite p overgroup used in the original proof, and A=Δ(F[K]). For every extension E/F there is a canonical isomorphism

    A⊗_F E ≅ Δ(E[K]).

Indeed F[K]=F·1 ⊕ A by the augmentation map, and tensoring gives E[K]=E·1 ⊕ (A⊗E), with the same augmentation. Every finite set of entries in Δ(E[K]) is supported in a finite p-subgroup P of K. The same central-element induction as in the original proof shows Δ(E[P]) nilpotent: if z is central of order p, then (z−1)^p=0, and the quotient by its central ideal is E[P/⟨z⟩]. This argument uses only characteristic p and works for every E, including uncountable extensions. Thus every M_n(A⊗E) is nil, so A is absolutely stable nil.

## 2. One AAJZ seed works over all extension fields

The following conclusion is obtained from the construction in AAJZ Lemma 4.4 (pp.17–18), not from the generally invalid inference “stable nil implies absolutely nil.”

Let

    P = F[t_1,t_2,...] ⊗_F M_∞(F),

with the usual commuting polynomial variables. AAJZ Lemma 4.3 constructs a finitely generated infinite-dimensional F-algebra B_0 satisfying the GS condition such that B_0⊗P is nil. This P has locally subexponential growth, as required by that lemma: any finite set involves finitely many polynomial variables and one finite matrix corner, so its generated algebra has polynomial growth.

Fix any extension E/F and any X in M_n(B_0⊗E). It can be written, with finite s, as

    X = ∑_{l=1}^s b_l ⊗ α_l ⊗ Y_l,
    b_l∈B_0, α_l∈E, Y_l∈M_n(F).

In B_0⊗P, the element

    X_univ = ∑_{l=1}^s b_l ⊗ t_l ⊗ Y_l

is nilpotent. Evaluate each t_l at α_l, and view the finite n×n corner in M_∞(E). This algebra homomorphism sends X_univ to X, so X is nilpotent. Therefore the **same** finitely generated F-algebra B_0 is absolutely stable nil. The quantifiers are important: B_0 is selected once over F, before E is specified.

The nilness of B_0 itself also follows by using the constant polynomial and a single diagonal matrix unit in P; it does not rely on P having an identity as an infinite matrix algebra.

## 3. The auxiliary finite-dimensional wreath extension

AAJZ Lemma 4.1 replaces A by

    A_tilde = A wr N,
    N = F u + F u², u³=0.

It is the external semidirect sum N + M_2(A). Its finite-dimensional second factor makes scalar extension commute with this construction: with the fixed basis u,u² of N,

    A_tilde⊗E ≅ N_E + M_2(A_E),
    A_E=A⊗E, N_E=N⊗E,

and the wreath bimodule actions are obtained by extending their structure constants. There is an ideal M_2(A_E), with quotient N_E. For any n, M_n(M_2(A_E))≅M_{2n}(A_E) is nil by Section 1, whereas M_n(N_E) is nilpotent since N_E³=0. An extension of a nil ideal by a nil algebra is nil: for an element x, first x^r belongs to the ideal and then (x^r)^s=0. Consequently every M_n(A_tilde⊗E) is nil. Thus A_tilde is absolutely stable nil.

AAJZ's corner embedding A→A_tilde u (or u A_tilde, according to convention) is over F. The already established containment proof in AAJZ Theorem 4.3 will still put A in the finitely generated containing algebra below. No new assertion about an arbitrary nil auxiliary algebra is used.

## 4. Precise base change for finite-row matrices

Put V=B_hat_0=F·1⊕B_0 and fix an F-basis (v_i)_{i∈I}, including 1. Let S_F(A_tilde,V) be the algebra of I×I matrices over A_tilde with only finitely many nonzero rows. Equivalently, these are the F-linear maps V→V⊗A_tilde whose images have first-factor support in a finite-dimensional subspace. This is AAJZ's algebra S(A_tilde,V).

For every E/F there is a natural E-linear algebra map

    Φ_E: S_F(A_tilde,V)⊗E → S_E(A_tilde_E,V_E),

given entrywise by scalar extension in the fixed basis. It need not be onto, and surjectivity is not claimed.

**Finite-row property.** An element on the left is a finite sum of tensors. The union of the finite row supports of its finitely many matrix factors is finite, so its image belongs to the right side.

**Injectivity.** Rewrite a tensor as ∑_{l=1}^s M_l⊗α_l with the α_l F-linearly independent. If its image is zero, every matrix entry gives

    ∑_l (M_l)_{ij}⊗α_l = 0 in A_tilde⊗E.

Independence of the α_l implies (M_l)_{ij}=0 for every i,j,l (apply coordinate functionals on the finite-dimensional span of the α_l, extended F-linearly to E). Thus every M_l=0, and the tensor is zero. This argument avoids the false identification of scalar extension of an infinite Hom-space with the full Hom-space after extension.

**Multiplication.** For finite-row matrices M,N, the (i,j) entry of MN sums only over the finite nonzero row support of N. All sums are therefore finite, and the entrywise extension preserves products. No convergence or infinite-sum interchange is involved.

The same construction sends b⊗α in B_0⊗E to b_E in B_{0,E}. The left and right B_0-actions on S are given by left multiplication on V and precomposition with left multiplication on V. Extending these operators to V_E gives exactly the actions of B_{0,E}. Hence Φ_E and the identity on B_{0,E} give an injective algebra map of **external semidirect sums**

    (B_0 + S_F(A_tilde,V))⊗E
       → B_{0,E} + S_E(A_tilde_E,V_E).

Keeping the external B component is essential: we do not assume that its left-multiplication image has trivial intersection with the finite-row matrices. No such intersection assertion is needed here.

## 5. All matrix algebras of the extended ambient algebra are nil

Write S_E=S_E(A_tilde_E,V_E) and R_E=B_{0,E}+S_E, the external semidirect sum. The bimodule actions preserve finite row support: postcomposition with a fixed left multiplication sends a finite-dimensional output space into another finite-dimensional output space, and precomposition does not enlarge the output space. Thus S_E is an ideal of R_E.

For each n, M_n(S_E) embeds faithfully into the finite-row matrices over A_tilde_E indexed by {1,...,n}×I: use the block entry (r,i),(s,j) for the (i,j) coefficient of the (r,s) block. A finite block matrix has finitely many blocks, and the union of their finite row supports is finite. Block multiplication agrees with matrix multiplication by the same finite-sum argument.

Any finite-row matrix over a stable nil algebra is nil. To check this directly, for its finite row support T, take the T×T corner. The corner map is an algebra homomorphism on matrices whose row support lies in T, and its kernel has square zero: a kernel matrix has zero entries in columns T and all rows outside T zero. Since the corner algebra M_T(A_tilde_E) is nil, each original matrix is nilpotent. Section 3 gives the required stable nilness over E. Hence M_n(S_E) is a nil ideal of M_n(R_E).

The quotient M_n(R_E)/M_n(S_E) is M_n(B_{0,E}), nil by Section 2. The nil-ideal/nil-quotient argument shows M_n(R_E) nil for every n and every E.

## 6. The finitely generated containing algebra is absolutely stable nil

Now choose the AAJZ generating map γ:V→A_tilde and define the finite-generator algebra

    B_1 = ⟨B_0, c_γ, e_11(u)⟩
         ≤ B_0 + S_F(A_tilde,V)

exactly as in the proof of AAJZ Theorem 4.3. The two displayed additional elements have finite row support (one row for c_γ and one matrix entry for e_11(u)). AAJZ's algebraic containment argument embeds A in B_1. The construction is over F and uses one fixed γ; no different choice for each E is made.

Since scalar extension by a field is flat, the inclusion B_1→B_0+S_F stays injective after tensoring. Composing with Section 4 gives

    B_1⊗E ↪ R_E.

Then M_n(B_1⊗E) injects into the nil algebra M_n(R_E) of Section 5. Thus **the finitely generated containing algebra B_1 can be chosen absolutely stable nil** for this input. More generally the same proof works for every countable-dimensional absolutely stable nil F-algebra A, with the universal seed of Section 2.

In the original elementary-group construction use this B_1 as B. Let C be the nonunital algebra generated by the finitely many canonical differences c_i in M_3(B_1). For every E, flatness gives

    C⊗E ↪ M_3(B_1)⊗E ≅ M_3(B_1⊗E).

The latter algebra is nil. Therefore C is absolutely nil (in fact absolutely stable nil). It is finitely generated, nil, and nonnilpotent exactly as established in the unchanged original proof.

## 7. Homogeneous Golod cover and subgroup epimorphism

Present C=F⟨x_1,...,x_r⟩_+/I using the original finite canonical generating list c_1,...,c_r, with r≥2. Hammoudi Theorem 3 applies because C is absolutely nil. It provides a homogeneous ideal J⊂I such that

    D=F⟨x_1,...,x_r⟩_+/J

is a classical Golod nil algebra satisfying that paper's Lemma 1; its algebra map onto C sends each x_i+J to c_i. Hence the group

    Γ=⟨1+x_1+J,...,1+x_r+J⟩≤1+D

maps **onto** L=⟨1+c_1,...,1+c_r⟩. This is also the content of Hammoudi Corollary 3, but the same-generator algebra quotient proves the precise group map needed here.

Because J is homogeneous, D is positively graded with finite-dimensional homogeneous components. For m≥1 its degree truncation D/D_{≥m} is a finite-dimensional nilpotent algebra over F_p and therefore a finite set. Distinct elements of D are separated by these truncations, since every polynomial has only finitely many homogeneous components. The induced finite p-group maps on Γ consequently separate its nonidentity elements. Thus Γ is residually finite. It is infinite since it surjects onto L containing the infinite H.

Let ι:H↪L be the original verified embedding, and let ρ:Γ→L be the surjection just constructed. The subgroup

    P=ρ^{-1}(ι(H))≤Γ

has the epimorphism ι^{-1}∘ρ|_P onto H. Surjectivity is immediate: for any h∈H, take a preimage in Γ of ι(h); that preimage belongs to P by definition.

This supplies the requested map with a classical homogeneous residually finite Golod source. For the tree family's explicit H, combine with its proof of the original infinite-support longitudinal AT condition. No compatibility of finite approximation epimorphisms, inverse-limit lifting, or arbitrary quotient preserving residual finiteness is assumed.

## Self-adversarial checks and exact status

- The source strengthening relies on absolute nilness of C. Stable nilness alone is not substituted into Hammoudi's hypothesis.
- The universal auxiliary seed is fixed over F before choosing E; using a different seed for each E would not prove absolute nilness of one containing algebra.
- Scalar extension of S is proved injective, not identified surjectively with every finite-row matrix over the extension. Infinite Hom base change is handled explicitly.
- All matrix products used to extend S and its actions have finite sums. The ambient semidirect algebra keeps B_0 externally, so no unsupported faithful finite-rank separation is used.
- Stable nilness of A_tilde_E, not merely nilness, is required for the finite-row argument and is proved in Section 3.
- We lift the AT subgroup by inverse image under a surjection. We do not infer that a quotient of a residually finite group is residually finite.
- The conclusion is an epimorphism from a subgroup of Γ. It is not an embedding of H in Γ; those statements differ, especially for locally finite groups with divisible subgroups.
- No mathematical defect was found in this independent derivation. A second-reader check of the explicit base-change passage remains appropriate before promoting the optional strengthening. The original verified broad result does not depend on this note.
