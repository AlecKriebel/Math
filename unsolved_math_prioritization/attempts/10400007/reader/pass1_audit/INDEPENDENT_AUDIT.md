# Independent adversarial audit of shared pass 1

**Edition note.** This records the accepted PASS1 transported construction and its scope at that stage. The mathematical theorem remains valid. The later direct geometric definition and current qualified acceptance are in [the reader](../JONES_RESEARCH_READER.md) and [PASS2 scope report](../pass2_scope/SCOPE_ADJUDICATION.md); the former imported-state objection does not apply to that strengthened definition.

14 October 2026 UTC. Roberts Problem 1.7, row 1786 / problem 10400007. This audit adopts the supplied construction contract and operational formulation. It is an audit of one shared mathematical pass, not an additional attempt, a novelty certificate, or an assertion about the present-day literature status.

## Decision

**Accepted: an explicit formal realization of the full Jones polynomial through genuine local-system H₀ and transported intrinsic WRT/CFT operations, together with several precise route obstructions and reductions. Not accepted: a novelty claim or an authenticated resolution of Roberts’s qualitative intended homological explanation.**

The contract does not require positive-degree homology, categorification, complement configuration spaces, a fixed particle number, rank-one coefficients, or a chain-level infinity-functor. It does require geometrically defined genuine local systems, specified homology and extraction, naturality for oriented knot pairs, and full source-normalized Jones equality for every knot without inserting an already known Jones polynomial. A complete canonical geometric comparison may transport operations; transport alone is neither circular nor disqualifying.

## 1. Accepted stabilization obstruction

Let X_n be the unordered configuration space of n points in the plane with 2n punctures. For any rank-r field local system E,

    χ(X_n; E) = r (−1)^n binomial(3n−2,n).

The finite-CW cellular argument makes this independent of monodromy. Forgetting ordered points gives Euler factors 1−2n−j, and division by the n!-sheeted free covering gives the formula. The unordered interior is an oriented real 2n-manifold, so Borel–Moore Euler characteristic has the same value. The statement is not being extended to an unspecified relative pair or to an outer-boundary support convention.

For rank one, adjacent absolute values strictly increase: their ratio is

    3(3n−1)(3n+1) / [2(n+1)(2n−1)] > 1.

Thus the full complexes cannot be related by quasi-isomorphisms implementing plat stabilization, even with degree shifts, monomial multiplication, or a rank-one Jones specialization. At n=2→3, a finite tensor-factor repair would require an integral Euler characteristic of absolute value 35/6. This is impossible.

This accepts exactly the full-complex obstruction in the descent report. It does not obstruct pairings on selected groups, relative theories, subquotients, cones, correspondences, or non-equivalence homotopy colimits. A homotopy colimit also needs its indexing topology and extraction handled; the example of a constant k-diagram over BZ producing C_*(S¹;k) is correct, and is not a universal obstruction to such constructions.

## 2. Accepted configuration topology and generic acyclicity

Let M=S³∖K for a smooth/tame oriented knot, G=π₁(M), F_n(M) its ordered configuration space and C_n(M) its unordered configuration space.

Removing the collision diagonals, which have real codimension three, induces π₁(F_n(M))≅G^n: loops and their two-dimensional homotopies can be made disjoint from the diagonals. A small embedded three-ball supplies a section of π₁(C_n(M))→S_n. With coherent basepoint paths inside that ball, the action permutes factors. Hence π₁(C_n(M))≅G^n⋊S_n. For n≥2 its abelianization is Z⊕Z/2; rank-one characters have a common meridional scalar and an exchange scalar ε satisfying ε²=1. This blocks a freely varying braid-exchange scalar in this precise configuration family. It does not block higher-rank coefficients, pairings, or other geometric spaces.

Work over F=Q(t), and let L_r have meridional monodromy t^r. For r≠0 the ordinary homology of M with coefficients L_r vanishes. One justification uses the finite two-dimensional homotopy model of the knot exterior, torsion of its Alexander module, and nonvanishing of Δ_K(t^r). H₀ vanishes because t^r−1 is invertible, H₁ vanishes after localization, and χ(M)=0 forces H₂=0. The complement deformation retracts onto the compact exterior. Duality gives the corresponding compact-support acyclicity.

On M^n use the external product of L_{w_i}. Assume only that the total integer charge W=∑_i w_i is nonzero. Every intersection of collision diagonals is indexed by a partition π, and its restricted system is an external product with weights ∑_{i∈B}w_i over the blocks B of π. At least one block has nonzero charge, because all block charges sum to W. One acyclic factor suffices to kill the entire compact-support Künneth product; the other factors may have charge zero. The finite closed collision arrangement admits the compact-support Mayer–Vietoris/Čech resolution (equivalently a compatible finite triangulation argument); therefore its union is acyclic. Open–closed localization makes H_c^*(F_n(M);L)=0, and oriented Poincaré duality gives ordinary homology vanishing. Apply the same argument to the dual weights and duality to obtain Borel–Moore vanishing too.

For uniform weights, the system descends to the unordered space, with either exchange sign. In characteristic zero, the finite covering's invariants/coinvariants are exact, so the same acyclicity follows. This proof is for rational-function coefficients and the specified systems. It does not prove integral or Laurent-module acyclicity, rule out torsion extraction, or apply to arbitrary relative pairs.

An important exact escape is w=(1,−1). M² is acyclic with the external-product system, but its diagonal has trivial coefficients. The oriented normal bundle has rank three. The relative Thom isomorphism and the long exact sequence give

    H_i(F₂(M); L₁⊠L₋₁) ≅ H_{i−2}(M;F).

Thus ordinary homology is F in degrees 2 and 3 and zero otherwise; applying the same result to the dual system gives Borel–Moore groups F in degrees 3 and 4. This verifies that the nonzero-total-charge hypothesis is substantive. The initially stronger all-subset-sums hypothesis was corrected during this audit. It neither extracts Jones nor shows that every possible pairing on these groups is constant.

### Accepted minimal-neutral-charge extension

For n≥2, suppose the total charge is zero but every nonempty proper subset has nonzero charge, for example (1,…,1,−(n−1)). Then only the full diagonal survives the collision Čech spectral sequence. The remaining incidence complex is the relative cochain complex of the full edge simplex Σ_n modulo the disconnected-graph subcomplex Disc_n. The checked graph-complex theorem places its cohomology T_n in degree n−2, with dimension (n−1)!. The spectral sequence has one surviving column and the open–closed sequence adds one degree. Therefore

    H_i(F_n(M);A_w) ≅ H_{i−2(n−1)}(M;F) ⊗ T_n.

Ordinary groups have dimension (n−1)! in degrees 2n−2 and 2n−1, and Borel–Moore groups in degrees n+1 and n+2. The n=2 and n=3 differentials and shifts agree with the explicit opposite-charge and k³→k calculations. This is accepted as a graded-vector-space calculation, without claiming a preferred basis, a Jones pairing, or coverage of neutral vectors with proper neutral subsets.

The graph input is Proposition 2.1(i) of Babson–Björner–Linusson–Shareshian–Welker, *Complexes of not i-connected graphs*: https://arxiv.org/pdf/math/9705219 . The configuration/local-system reduction is supplied in the report's proof rather than attributed to that source.

## 3. Accepted pure-gauge localization reduction

In Anghel–Juhász v4, Definition 8.26, the two-variable differential is the ordinary hat knot-Floer differential with a term x→y multiplied by

    U^[B(x)−B(y)] V^[C(x)−C(y)].

After adjoining U⁻¹,V⁻¹, set e_x=U^−B(x)V^−C(x)x. Expressing the differential in the e_y basis cancels both exponents exactly. Hence this localized complex is the ordinary hat knot-Floer complex tensored with F₂[U±1,V±1]. This is an explicit change of basis, not an inference from Euler polynomials.

The source assigns Jones degrees deg(U)=−1 and deg(V)=1. Since B−C=Q and J(x)=A(x)−Q(x), the new basis has J(e_x)=A(x). Therefore this particular localization absorbs the Jones refinement into the invertible coefficient grading. It does not furnish the requested full Jones extraction. Formal x,d grading variables in the Euler polynomial are not automatically a coefficient-module action; substituting d=−x⁻¹ in that polynomial does not define a chain-level base-change functor.

This does not rule out another quotient, relative construction, filtration, or correspondence. Nor does the manuscript's unspecialized Markov noninvariance imply failure of its stated Jones polynomial specialization. The mirror in Theorem 1.13 remains essential.

## 4. Skein, mapping-class and conformal-block routes

De Renzi–Martel's genuine twisted-configuration homology comparison with quantum mapping-class representations is accepted as relevant prior work, not a complete knot-pair construction. A representation comparison by itself has not supplied the additional knot/handlebody states and extraction in this pass. The root-of-unity nature of a candidate is not an inherent defect: sufficiently many exact values plus an independent Laurent-degree bound determine a polynomial.

The Andersen–Ueno conformal-field-theory route needs different treatment. Their 2014 comparison is an isomorphism of modular functors compatible with their structures, and their introduction explicitly describes the resulting geometric WRT TQFT. It would be incorrect to claim that this literature contains no gluing theorem or no TQFT. The anomaly-corrected flat bundles over marked Teichmüller spaces give genuine local systems; on a connected simply connected base, horizontal sections and H₀ are canonically identified via evaluation and parallel transport. Neither degree zero nor canonical transport of states is prohibited by the adopted contract.

### Accepted formal CFT/WRT assembly

The final skein construction candidate supplies the following explicit assembly. Let T=∂E_K with its oriented meridian m and preferred longitude ℓ, and use the extended surface Lagrangian Qm. At level k≥1, take the independently constructed sl₂ vacua bundle with its abelian ghost-line correction over the marked Teichmüller space. The source's zero-labeled-point propagation removes any stabilizing marked-point choice. Its ordinary singular local-system H₀ has the explicit fiber/path-transport quotient; horizontal sections map canonically to it. Composing this map with the AU comparison gives ν_Σ from the WRT state space to H₀.

For every decorated extended cobordism W, the rule

    Zᴴ(W)=ν_out Z^RT(W) ν_in^−1

defines an exact functor on the actual homology objects. Intermediate ν maps cancel under composition. It coherently transports the existing states, fillings and relations; it is not claimed to be the pushforward of a single continuous map between Teichmüller spaces. Requiring that stronger property would add an unadopted restriction.

The exterior E_K is a weight-zero outgoing cobordism and its complementary solid torus is a weight-zero incoming cobordism with zero-framed fundamental-colored core. Their interface Maslov correction in the checked Gilmer–Masbaum convention is

    μ_T(Qℓ,Qm,Qm)=0.

The contraction is therefore the weight-zero decorated S³ value. Dividing by the corresponding unknot contraction is legitimate because its quantum-dimension factor is 2cos(π/(k+2))≠0. All peripheral data, framing and states transport under oriented knot-pair diffeomorphisms; tubular-neighborhood changes are absorbed by this naturality.

The actual AU skein/twist page was rendered and inspected. Its N=2 conventions give θ=q^(3/4) and

    q^(1/4)F₊−q^(−1/4)F₋=(q^(1/2)−q^(−1/2))F₀.

After the total-writhe correction, qP₊−q⁻¹P₋=(q^(1/2)−q^(−1/2))P₀. Multiplying the link normalization by (−1)^(components−1) and setting t=q⁻¹ yields precisely the source skein relation. For knots the component factor is +1 and the writhe correction is the preferred zero-framing correction. Consequently the normalized contraction is V_K(exp(−2πi/(k+2))). The distinction between total-writhe link normalization and zero framing of each separate link component does not affect the knot-only claim.

Finally, for a c-crossing knot diagram, the state expansion bounds the corrected A-exponents by 6c, so the deliberately coarse Jones bound [−2c,2c] is valid. The 4c+1 distinct level roots k=1,…,4c+1 determine t^(2c)V_K by exact Lagrange interpolation. No coefficients or evaluated Jones values are taken from the diagram or a lookup. Equality to the source-normalized polynomial proves integrality and independence of the auxiliary degree bound, including c=0.

**Mathematical acceptance:** all named objects, homology, operations, naturality, anomaly, normalization and full-polynomial extraction are supplied by established inputs plus the explicit assembly. No previously computed Jones scalar defines a coefficient system or state. The accepted result is therefore a formal local-system-homology realization of prior WRT/CFT theory under the operational formulation's allowance of H₀ and canonical transport.

**Interpretive limit:** the Teichmüller base is contractible and the knot-dependent states are inherited through a quantum TQFT. The homological content is therefore indirect. This audit does not certify that Roberts or the literature regards such a realization as the intended answer to Problem 1.7. It would be unjustified either to advertise an authenticated historical resolution or to reject the assembly by silently adding a positive-degree, direct-cycle, or complement-space condition. A source-intent determination is distinct from the now-checked mathematical theorem.

## 5. Exact independent computational checks

The accompanying Python file uses integer Laurent-polynomial dictionaries and rational arithmetic. It verifies the two-braid skein recurrence through eleven crossings, yielding V_T(2,3)(t)=t+t³−t⁴ and its distinct mirror; computes the first thirty plat Euler values and exact ratios; and checks the gauge/degree cancellation on representative integer exponents. These finite checks are sanity tests. The proofs above, rather than finite enumeration, support the quantified claims. I also reran the validation report’s 511 exact smoothing/TL₂ comparisons and 127 source-skein cases, the Floer report’s sign, quotient-factor and gauge checks; the descent Euler checks through n=100; and the neutral-graph exact rational matrix checks for n=2,…,5; all passed. The independent audit script retains explicit checks under Python optimization.

The validation report’s trefoil/mirror module obstruction is also accepted: both infinite-cyclic H₁ modules are Λ/(t²−t+1), while their Jones polynomials are distinct. The unit entry in each stated Seifert presentation gives this module calculation directly. This excludes extraction through those unadorned module isomorphism classes only, not Blanchfield/peripheral/chain enhancements.

## 6. Acceptance boundaries

- No accepted result here proves that an intrinsic Jones local-system construction is impossible.
- No accepted result identifies an error in the published Jones formulas, source problem, or cited mathematical theorems.
- No scalar-only presentation formula has been promoted to the requested intrinsic construction.
- No unverified stabilized-unknot Floer rank comparison is used as a theorem.
- A local-system/functorial comparison must be judged on its actual mathematical content, not discarded because a theorem uses auxiliary surfaces, degree zero, or transported operations.
- The accepted CFT/WRT assembly includes that full root-normalization and recovery check. Its mathematical acceptance does not decide the original qualitative interpretation.

## Sources inspected for this audit

- The supplied source contract, operational formulation and independent source adjudication.
- Anghel–Juhász, *Quantum braid Floer homology*, arXiv:2601.08805v4, Definitions 8.24 and 8.26 and Proposition 8.25, using the retained complete primary text: https://arxiv.org/pdf/2601.08805v4
- De Renzi–Martel, *Homological Construction of Quantum Representations of Mapping Class Groups*, arXiv:2212.10940v2, introduction and main-theorem scope: https://arxiv.org/html/2212.10940v2
- Andersen–Ueno, *Construction of the Witten–Reshetikhin–Turaev TQFT from conformal field theory*, arXiv:1110.5027v2, introduction, Theorem 1.1 and modular-functor conventions: https://arxiv.org/html/1110.5027v2
- Andersen–Ueno, *Geometric construction of modular functors from Conformal Field Theory*, retained complete v2 text, Theorem 11.4, Definition 11.3 and vacuum propagation: https://arxiv.org/pdf/math/0306235v2
- Gilmer–Masbaum, *Maslov index, Lagrangians, Mapping Class Groups and TQFT*, §2: https://arxiv.org/html/0912.4706v3
- Babson–Björner–Linusson–Shareshian–Welker, *Complexes of not i-connected graphs*, Proposition 2.1(i): https://arxiv.org/pdf/math/9705219

Canonical authored files and byte/hash pins are listed in the accompanying audit manifest after final review. No copied source text, private coordination or raw source files are part of this authored mathematical audit.
