# PASS1 skein/TQFT construction: transported CFT local-system construction

**Edition note.** This records the accepted PASS1 transported construction and its scope at that stage. The mathematical theorem remains valid. The later direct geometric definition and current qualified acceptance are in [the reader](../JONES_RESEARCH_READER.md) and [PASS2 scope report](../pass2_scope/SCOPE_ADJUDICATION.md); the former imported-state objection does not apply to that strengthened definition.

14 October 2026 UTC. This is an authored assembly of established constructions, not a claim of novelty or an authenticated historical resolution of Roberts's qualitative question. The principal acceptance issue is stated in §8. It must not be replaced by a blanket ban on degree-zero homology, quantum fibers, auxiliary surfaces, or transport through canonical comparison isomorphisms.

## 1. Outcome

There is a substantially stronger candidate than the statement that a skein quotient is homology. Independently defined conformal-block bundles, corrected by the abelian ghost theory, give genuine flat local systems over marked Teichmüller spaces. Their ordinary local-system H_0 is naturally the WRT state space. A knot exterior supplies a state, the fundamental-colored solid torus supplies a filling functional, and their contraction recovers an exact Jones evaluation. Finitely many evaluations recover the entire Laurent polynomial with an explicit bound depending only on a diagram's crossing count.

The construction below specifies the spaces, local systems, ordinary H_0, state/filling maps, anomaly convention, naturality, normalization, and finite extraction. It uses the existing geometric WRT/CFT comparison to transport the three-dimensional operations. No missing TQFT or gluing theorem is asserted: those are established inputs. It does not use a previously computed Jones scalar to define a local system.

The remaining interpretive question is whether this transported degree-zero realization supplies the intended homological explanation, or is too close to a sophisticated repackaging of WRT. The operational formulation alone must not be strengthened silently to exclude it. Independent assessment should focus on the actual construction below.

## 2. Established ingredients and their exact scope

**A. Geometric flat bundle.** Andersen–Ueno, *Geometric construction of modular functors from Conformal Field Theory*, arXiv:math/0306235v2, Definition 11.2, Theorem 11.4, Definition 11.3, Remark 11.4 (PDF p60), construct flat bundles on the Teichmüller spaces of labeled marked surfaces. The bundle is the vacua bundle tensored with the indicated fractional power of the abelian theory. The modular functor takes horizontal sections. Contractibility of the base is explicitly used. Their §12 supplies sewing and §13 verifies the modular-functor axioms. [Primary PDF](https://arxiv.org/pdf/math/0306235v2)

**B. Comparison, including structures.** Andersen–Ueno, *Construction of the Witten–Reshetikhin–Turaev TQFT from conformal field theory*, arXiv:1110.5027v2, Theorem 1.1 (PDF p2), gives an isomorphism I from the skein/WRT modular functor to the vacua modular functor compatible with all modular-functor structures. Their introduction explains the consequent geometric WRT construction; duality and unitarity are transported, rather than claimed there to have independent geometric constructions. Label-dependent scalar choices are explicitly described. Section 3.2, equation (1), fixes the framed skein conventions. [Primary PDF](https://arxiv.org/pdf/1110.5027v2)

**C. Actual three-dimensional functor.** The semisimple SU(2) WRT TQFT assigns vector spaces to extended surfaces, linear maps to decorated cobordisms, and satisfies gluing. BHMV constructs it from the bracket, including states of manifolds with boundary and banded-link insertions. Its original anomaly convention uses p_1-structures. [BHMV primary paper](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/bhmv.pdf)

**D. Explicit anomaly convention.** We use the equivalent extended-manifold formulation reviewed by Gilmer–Masbaum, arXiv:0912.4706v3, §2, equation (1), rather than leaving a projective scalar ambiguous. A surface carries a rational Lagrangian and a 3-cobordism an integer weight. Lemma 2.1 says the Maslov index vanishes when two entries agree. Their knot-neighborhood discussion explicitly uses the meridian Lagrangian for regluing. [Primary PDF](https://arxiv.org/pdf/0912.4706v3)

These are prior theorems, not conjectural new bridges. The use of an established TQFT on a larger category is a method; this attempted answer asserts only the required knot-in-S³ output.

## 3. Input, flat coefficients, and genuine local-system homology

Let (S³,K) be a smooth oriented knot pair in oriented S³. Choose a closed tubular neighborhood N_K, put E_K=S³\int(N_K), and let T_K=∂E_K with its boundary orientation. Write m and ℓ for meridian and preferred zero-linking longitude. Equip T_K with the rational Lagrangian Λ=Q m. The preferred longitude specifies the zero-framing of the core of N_K. Tubular-neighborhood choices are related by isotopies of the pair.

Fix an integer level k≥1. Let T(Σ) denote the marked Teichmüller space in Andersen–Ueno's convention for an extended surface Σ. For the actual output we need Σ=T_K and the empty surface. Vacuum-labeled auxiliary marked points may be added to enter the stable convention; propagation of vacua removes dependence on them.

Let (E_k(Σ),∇_k) be the anomaly-corrected flat vacua bundle from ingredient A, for the Lie algebra sl₂ and level k. Its fiber is defined by affine-Lie-algebra conformal blocks on the marked complex curve, tensored with the ghost-line correction. This definition precedes the knot and does not contain V_K, a knot lookup, or a chosen skein scalar. The conformal-block central charge is c=3k/(k+2), and the correction is the power −c/2 in the source's notation. Set

  L_k(Σ)=ker ∇_k,
  H_k(Σ)=H_0(T(Σ); L_k(Σ); C).

This is ordinary singular homology with a finite-rank complex local system, in degree zero, with no relative or locally-finite support condition. More explicitly it is the quotient of the direct sum of fibers L_{k,x} by the genuine parallel-transport relations

  [y,P_γ(v)] − [x,v],

for paths γ:x→y. No skein relation is inserted into this chain boundary. The base is contractible, so its π₁-monodromy is trivial; the nontrivial information retained by the construction includes the geometrically specified mapping-class equivariance and the distinguished exterior state. Nontrivial π₁-monodromy is not an axiom of the operational formulation.

There is a canonical isomorphism

  θ_Σ:H⁰(T(Σ);L_k(Σ)) → H_k(Σ),  s↦[x,s(x)].

Independence of x follows from horizontal transport; existence and uniqueness of a global horizontal section through any fiber vector prove bijectivity. This is natural for maps of flat bundles covering diffeomorphism-induced maps of Teichmüller spaces.

Compose θ with the comparison of ingredient B:

  ν_Σ=θ_Σ I_Σ : V_k^RT(Σ) → H_k(Σ).

For the empty surface use the usual normalized unit identification H_k(∅)=C. For an unmarked torus the label-scalar ambiguity described in B has an empty product; more generally all such comparison changes cancel in conjugated composite operations.

## 4. The three-dimensional state and filling operation

For every decorated extended cobordism W:Σ₀→Σ₁ needed here, define

  Z_k^H(W)=ν_{Σ₁} Z_k^RT(W) ν_{Σ₀}^{−1}.

This is a specified operation on genuine local-system homology. It is not asserted to be a pushforward induced by one continuous map between the Teichmüller spaces. The operational formulation allows a stated extraction operation and homology classes/pairings; demanding that every cobordism map be a single ordinary homology pushforward would be an additional restriction.

Functoriality is immediate and exact:

  Z_k^H(W₂)Z_k^H(W₁)
  =ν₂ Z_k^RT(W₂) Z_k^RT(W₁) ν₀^{−1}
  =Z_k^H(W₂∘W₁).

The same argument transports duality, tensor products, handlebody states, all sewing operations, and all relations among decompositions. Thus the knot-exterior map is an intrinsic cobordism map before choosing a surgery or Heegaard calculation. It is stronger data than a scalar whose invariance under diagram moves has merely been checked.

Regard E_K, with weight zero, as ∅→T_K, and N_K, with the zero-framed oriented core colored by the fundamental sl₂ label 1 and weight zero, as T_K→∅. Define

  h_k(K)=Z_k^H(E_K)(1) ∈ H_k(T_K),
  f_k(K)=Z_k^H(N_K,core₁) : H_k(T_K)→C.

The local filling is the same fundamental-colored solid-torus operation for every knot; equivalently its vector can be specified by the label-1 summand of torus factorization. The entire knot dependence is in the peripheral exterior state and its gluing to the prescribed filling.

**Anomaly calculation.** In convention D,

  w(E_K∪_T N_K)=w(E_K)+w(N_K)
    −μ_T(Λ_{E_K}(T), Λ(T), Λ_{N_K}(T)).

Here Λ_{E_K}=Qℓ, Λ(T)=Qm and Λ_{N_K}=Qm. Thus the correction is μ_T(Qℓ,Qm,Qm)=0, and the composite is the decorated S³ of weight zero. This removes the projective-trace ambiguity instead of ignoring it.

Set a_k(K)=f_k(K)(h_k(K)). Define the normalized evaluation

  z_k(K)=a_k(K)/a_k(U),

where U is the zero-framed unknot with the identical fundamental label and weight-zero convention. The denominator is a nonzero vacuum normalization times [2]=2cos(π/(k+2)), so is nonzero for every k≥1.

An orientation-preserving diffeomorphism of knot pairs transports m, ℓ, the preferred framing, E_K, N_K, and all the extended data. Naturality of ν and the TQFT imply transport of h and f and equality of their contraction. Changing a tubular neighborhood, a peripheral parametrization through the induced isotopies, an auxiliary vacuum insertion, or a computational decomposition therefore does not change z_k. No arbitrary-3-manifold output is required.

## 5. Exact Jones convention

Let q=exp(2πi/(k+2)) with the specified fractional powers in AU §3. Their N=2 framed skein convention has

  q^(1/4)F₊−q^(−1/4)F₋=(q^(1/2)−q^(−1/2))F₀,
  θ=q^(3/4),   F(U)=[2]=q^(1/2)+q^(−1/2).

For an oriented diagram D, let w(D) be its writhe and put P_L=θ^(−w(D))F_D/[2]. The framing correction gives

  q P₊−q^(−1)P₋=(q^(1/2)−q^(−1/2))P₀.

For this convention define J_L=(-1)^(number_of_components(L)−1)P_L. In a skein triple, smoothing changes component-number parity, whereas switching the crossing does not. Therefore, setting t=q^(−1),

  t^(−1)J₊−tJ₋=(t^(1/2)−t^(−1/2))J₀,
  J_U=1.

Thus the source-normalized Jones invariant is J_L. For knots the component sign equals +1. The zero-framed decorated S³ ratio above is P_K, hence

  z_k(K)=V_K(exp(−2πi/(k+2))).

The sign reversal in the link case is essential. It is not legitimate simply to identify AU's positive quantum dimension with the source's split-link convention. As a normalization check, the positive 2-braid trefoil has normalized value q^(−1)+q^(−3)−q^(−4), which becomes t+t³−t⁴.

Here P_L for a multi-component link uses total writhe; it is not being identified with the invariant obtained by zero-framing every component separately. The filling equality is claimed only for knots, where total writhe is the self-framing correction.

This equality is a comparison theorem, not the definition of L_k or of h_k. All local systems and operations were defined before consulting the target polynomial.

## 6. Finite reconstruction, with proof

Let D be any c-crossing diagram of K. The normalized Kauffman state expansion has terms

  A^(a−b)(−A²−A^(−2))^(s−1),

where a+b=c and s is the number of smoothed circles. Starting from one component, each smoothing changes the component count by at most one, so s≤c+1. Every A-exponent in the normalized bracket has absolute value at most c+2c=3c. Multiplication by the writhe correction (−A³)^(−w), with |w|≤c, enlarges this to at most 6c. Because V_K(A^(−4)) is a Laurent polynomial in A⁴, its t-exponents have absolute value at most 3c/2. We use the simpler integral bound

  B=2c,   supp(V_K)⊂[−B,B].

The standard state formula is due to Kauffman; the deliberately coarse bound and interpolation argument here are elementary deductions, not claims of new knot theory. [Kauffman primary paper](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/kauffmanjones.pdf)

Take k=1,…,2B+1 and x_k=exp(−2πi/(k+2)). These are distinct and nonzero. Define the finite expression

  P_K(t)=t^(−B) Σ_{k=1}^{2B+1}
    x_k^B z_k(K) ∏_{j≠k}(t−x_j)/(x_k−x_j).

The polynomial t^B V_K(t) has degree at most 2B, and its values at all these nodes equal those used in the expression. Lagrange interpolation proves P_K=V_K exactly. Consequently the expression belongs to Z[t,t^(−1)], despite being written over cyclotomic complex numbers. This is an exact algebraic extraction, not numerical interpolation.

The diagram supplies only a bound c, never coefficients or values of V_K. A different diagram or a larger bound gives the same polynomial by the same theorem. For c=0, B=0 and one evaluation suffices. Thus infinitely many levels are not an essential computational requirement: 4c+1 levels suffice with this coarse bound.

Optional general observation: if a construction instead gives the exact Taylor jet of P(e^h), the same support bound makes the first 2B+1 derivatives sufficient, since d^n/dh^n P(e^h)|₀=Σ_{j=−B}^B a_j j^n is an invertible Vandermonde system for the coefficients a_j. A finite arbitrary truncation without such a bound is insufficient.

## 7. What is established, and what is not claimed

The flat bundle, its geometric definition independent of K, modular-functor comparison, WRT cobordism maps, anomaly conventions, and skein normalization are prior theory. The H⁰↔H_0 identification, conjugation construction, exterior-filling formula, anomaly cancellation, and finite reconstruction are the explicit assembly made here.

There is no claimed new configuration-space theory of the knot complement, no claimed local-system chain complex on the character variety of E_K, and no claimed independent geometric formula for the duality that AU themselves transport. Those are different, stronger goals. Their absence cannot be called a mathematical defect unless that stronger requirement is adopted and stated.

This candidate genuinely puts the scalar extraction through ordinary local-system homology and natural three-dimensional states; the coefficient system is not chosen from V_K. Nevertheless its knot-state maps are inherited through an existing quantum TQFT. That is the important limitation to expose.

## 8. Acceptance boundary requiring independent adjudication

Two statements should be kept distinct:

1. **Formal operational realization:** allowing a geometrically defined flat system, H_0, and coherent transport of intrinsically defined three-dimensional operations, the above supplies all named mathematical objects and the full Jones polynomial. It is not obstructed merely by roots of unity, projective monodromy, or lack of a general gluing theorem.
2. **Roberts-intended homological explanation:** it is not established here that the literature or Roberts regards this CFT/TQFT-to-H_0 realization as answering the intended question. Because the base is contractible and the 3D maps are transported, an evaluator might reasonably find its homological content too indirect. That judgment is an interpretation of the qualitative target, not an unavailable-map theorem and not a proof of impossibility.

If the construction is rejected, the rejection must state the extra substantive criterion it fails, such as a requirement that exterior states and pairings be realized directly by geometric local-system cycles/correspondences rather than transported TQFT maps. Such a criterion is not automatically present in the current five-part operational formulation. No present-day openness, novelty, or impossibility certificate follows from this approach.
