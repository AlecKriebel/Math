# PASS1 independent validation: scoped local-system obstructions and normalization

Date: 14 October 2026 UTC. Scope: ordinary tame/smooth knots in oriented S³, with the operational acceptance formulation supplied for this pass. This report validates limited deductions and examples. It is **not** a construction of Roberts's invariant and is **not** a negative resolution of his question.

## Results

1. The source normalization gives V(right trefoil)=t+t³−t⁴ and V(left trefoil)=t⁻¹+t⁻³−t⁻⁴. Both have symmetric Alexander polynomial t−1+t⁻¹. Their ordinary infinite-cyclic homology modules are also isomorphic as Z[t,t⁻¹]-modules. Consequently neither the Alexander polynomial alone nor these unadorned modules determine Jones.
2. For configurations of points in a 3-manifold, the independent exchange monodromy available in a punctured-disc braid model disappears: a local exchange has order two. This obstructs transporting a free exchange Laurent variable unchanged, not all configuration-space constructions.
3. Ordered meridional systems with nonzero total integer charge have zero ordinary and Borel–Moore homology over Q(t); this includes the identical generic meridian system for every particle number. The corresponding unordered systems, including the sign twist, also have zero ordinary homology. The proof is given below.
4. A resonance exception shows why that theorem must retain its coefficient hypothesis: on ordered two-point configurations, the system L_t⊠L_t⁻¹ has homology of rank one in degrees 2 and 3.
5. Anghel–Juhász v4 recovers the mirror Jones polynomial. Formal evaluation of its graded Euler series is not automatically a base change of a chain complex. Inverting both Rees variables in the complex of Definition 8.26 explicitly removes its extra weights by a generatorwise gauge transformation.

## 1. Independent finite computations and conventions

The companion script `verify_examples.py` uses integer Laurent dictionaries, not a knot package or a CAS. It implements two separate bracket computations on closures of two-strand braid words:

- Direct enumeration of the 2^m smoothing states, with disjoint-set union counting the resulting circles.
- Multiplication in TL₂, with E²=δE, δ=−A²−A⁻², closure traces tr(I)=δ and tr(E)=1.

A positive crossing is A·I+A⁻¹·E. Multiplication by (−A³)⁻ʷ and substitution A=t⁻¹/⁴ supplies the normalized Jones polynomial. The script checks both algorithms on all 511 signed words of lengths 0 through 8, cancellation of an adjacent inverse pair, both one-crossing unknot closures, the two-component unlink, and 127 source-skein instances. These are finite implementation checks; they do not establish any universal topological statement by experiment.

For T=closure(σ₁³), the computed polynomials are

- V_T(t)=t+t³−t⁴;
- V_mirror(T)(t)=t⁻¹+t⁻³−t⁻⁴.

The verified skein convention is exactly t⁻¹V_+−tV_-=(t¹/²−t⁻¹/²)V_0, with V_unknot=1. Anghel–Juhász Remark 2.9 independently states this convention and identifies the positive trefoil polynomial. The Knot Atlas primary computational table identifies its displayed trefoil as the negative three-crossing braid and gives the reciprocal polynomial, consistent with the calculation. Thus the chirality labels are not inferred from an unlabeled polynomial table.

A genus-one Seifert matrix S=((1,0),(−1,1)) yields

tS−Sᵀ = ((t−1,1),(−t,t−1)), det(tS−Sᵀ)=t²−t+1.

The mirror matrix −Sᵀ gives the same determinant. Each presentation contains a unit, so elementary row/column elimination identifies its cokernel with Λ/(t²−t+1), Λ=Z[t,t⁻¹]. Both trefoils have H₀ of the infinite-cyclic local system Λ/(t−1), H₁=Λ/(t²−t+1), and no higher homology. These statements also follow from the punctured-torus fibration. Therefore any extraction factoring only through the isomorphism class of those graded modules takes the same value on these knots and cannot equal Jones for every knot.

The statement deliberately excludes peripheral enhancements, chain-level or simple-homotopy data, duality pairings, Blanchfield forms, additional natural classes and nonabelian representations. Such information need not be determined by a module's isomorphism class.

As a second elementary pair, connected-sum multiplicativity gives the right-handed granny T#T and square T#mirror(T) the same Alexander polynomial (t−1+t⁻¹)², but different Jones polynomials. The exact coefficient lists are in `EXACT_CHECK_RESULTS.json`. No new claim about prime knots or a knot database classification is needed.

## 2. Configuration monodromy in dimension three

Let M be a connected smooth manifold of dimension d≥3 and G=π₁(M). Write F_n(M) for ordered configurations and C_n(M)=F_n(M)/S_n for unordered configurations.

### Proposition 2.1

The inclusion F_n(M)→M^n induces an isomorphism π₁(F_n(M))≅G^n.

**Proof.** The deleted set is a finite union of pairwise diagonals, each of codimension d≥3, with higher intersections of at least that codimension. A loop in M^n can be put in general position relative to every diagonal, avoiding them because 1<d. A homotopy of loops can likewise avoid them relative to its prescribed boundary because 2<d. These observations give surjectivity and injectivity, respectively. Basepoints and their connecting paths only alter the usual identification by conjugacy. ∎

### Proposition 2.2

π₁(C_n(M))≅G^n⋊S_n, with S_n permuting the factors. For n≥2,

H₁(C_n(M);Z)≅H₁(M;Z)⊕Z/2.

**Proof.** The ordered covering gives the extension with kernel G^n and quotient S_n. Choose all base particles in an embedded ball B. Ordered F_n(B) is simply connected by Proposition 2.1, so π₁(C_n(B))→S_n is an isomorphism and its inclusion splits the extension. Using paths in B to identify the particle basepoints identifies conjugation by that splitting with permutation of the G factors. Abelianization takes coinvariants of H₁(M)^n under the transitive permutation action and adds S_n^ab=Z/2. ∎

For a knot complement H₁(M)=Z, a rank-one local system over a commutative field is therefore specified by a common meridian scalar a and an exchange scalar ε with ε²=1. Over Q(t), ε=±1. In the ordered case the individual meridian scalars may differ.

**Precisely scoped obstruction.** A free Laurent exchange parameter d cannot be assigned unchanged to a local particle exchange in C_n(M), because this would require d²=1. This says nothing against nonabelian local systems, additional geometric data, or extracting invariants from higher configuration homology. Indeed F₂(R³)≃S² has nonzero H₂ even though its fundamental group is trivial. Monodromy information alone does not determine configuration homology.

## 3. Generic identical-meridian acyclicity

Let M=S³∖K and F=Q(t). Let L_r be the rank-one system with meridian t^r, where r is a nonzero integer.

### Base fact

H_*(M;L_r)=0. The usual infinite-cyclic complex is a finite free Λ-complex with torsion homology: H₀ has order t−1, H₁ has the nonzero Alexander polynomial as its order, and higher homology vanishes. Localizing to Q(t) therefore gives zero. Substituting t↦t^r preserves nonzero Laurent polynomials and gives the asserted version. Equivalently, use a Seifert matrix; det(tS−Sᵀ) is nonzero because its value at t=1 is ±1. Both L_r and its dual L_−r are acyclic. Twisted Poincaré duality also makes their compactly supported cohomology zero.

### Theorem 3.1

For every n≥1, the restriction to F_n(M) of L_1⊠⋯⊠L_1 on M^n has zero ordinary homology over F in every degree. The same holds on C_n(M) for each rank-one system whose common meridian is t and whose exchange scalar is +1 or −1.

**Proof.** Put X=M^n and let D be the union of pairwise diagonals. Künneth and the base fact imply H_c^*(X;L)=0. Every nonempty intersection of diagonals is the submanifold associated to a set partition π of {1,…,n}, namely M^{|π|}. Restriction of L to a block of size r is L_r. Every such r is positive, so Künneth again gives zero compactly supported cohomology for each intersection.

The finite closed cover of D by its pairwise diagonals has the compact-support Mayer–Vietoris/Čech spectral sequence. Its first page consists of those zero groups, so H_c^*(D;L|D)=0. One may justify the sequence using the exact closed-cover Čech resolution: at a point its stalk is the augmented cochain complex of the simplex indexing the diagonals containing that point. Closed inclusions are proper, so compact supports agree with compact supports on each intersection. The open–closed localization sequence for F_n(M)⊂X now yields H_c^*(F_n(M);L)=0. Ordered F_n(M) is an oriented 3n-manifold, and twisted Poincaré duality yields the claimed ordinary-homology vanishing. If conventions dualize the coefficient representation, apply the same argument to L^∨; all negative block powers are also acyclic.

For unordered configurations, pullback of either rank-one system is L. The covering-chain complex with its appropriate deck action computes the downstairs homology by S_n-coinvariants. Coinvariants are exact over Q(t), since averaging divides by n!. Thus the upstairs vanishing implies the downstairs vanishing, including the sign twist. This does not assume that unordered configurations are orientable. ∎

The stronger ordered version requires only nonzero total charge Σa_i≠0 when particle i carries t^{a_i}. For every partition, some block has nonzero charge because the block charges sum to that total; its one acyclic factor makes the entire external tensor product acyclic. This applies to X as well. Individual charges and proper subset sums may vanish. The identical-meridian theorem is the case a_i=1. The same proof for the dual coefficients, followed by linear duality and Borel–Moore Poincaré duality, proves Borel–Moore vanishing too; unordered descent again uses the finite proper covering.

**Consequence and scope.** An extraction depending only on these localized ordinary homology groups sees zero for every knot, so it cannot give Jones. This obstruction does not eliminate torsion over Λ, Reidemeister torsion, relative or Borel–Moore pairings with extra boundary/stratified data, non-generic specializations, other local systems, or other geometrically defined spaces. In particular an acyclic chain complex can carry nontrivial torsion; ordinary homology vanishing alone does not trivialize all invariants of that complex.

### Sharp resonance check: opposite meridians

On X=M² take E=L_1⊠L_−1. Künneth still makes X acyclic, but E restricts to the trivial F-system on the diagonal Δ≅M. The diagonal has oriented normal rank three. The Thom isomorphism and long exact sequence of (X,X∖Δ) give

H_j(F₂(M);E)≅H_{j−2}(M;F).

For a knot complement, the right-hand side has rank one at j=2 and j=3 and is zero elsewhere. This is a proof, not a numerical experiment. It explicitly falsifies an assertion that all ordered rank-one systems with individually transcendental meridian eigenvalues are acyclic. This particular assignment does not descend to an unordered rank-one system, because the two meridian scalars disagree.

## 4. Euler characteristic and extraction sanity checks

For a finite CW model of a compact knot exterior and any rank-r field local system, χ(H_*(M;E))=rχ(M)=0: each cellular chain group has dimension r times the number of cells. Consequently the ordinary ungraded Euler characteristic cannot recover even V_unknot=1. Renormalizations, torsion and genuine additional gradings are different extraction rules and must be considered separately.

A Laurent grading variable in an Euler series is not, merely by appearing there, an action of a Laurent polynomial ring on the underlying vector space. An evaluation such as d=−x⁻¹ therefore determines a regraded signed Euler sum; a chain-level scalar-extension claim requires an actual module structure and compatible differential.

## 5. Anghel–Juhász v4: independent algebraic audit

The inspected primary version is arXiv:2601.08805v4, *Quantum braid Floer homology*. Rendered pages 8 and 14 verify the mirror overbar and source skein convention. Definition 8.26 uses F₂[U,V]; its differential weights are b(u)=B(x)−B(y) and c(u)=C(x)−C(y). Section 9 supplies the trefoil test and Markov counterexamples. These checks use the retained authenticated PDF; current web PDF retrieval failed, which does not invalidate the locally hash-verified source.

**Authored deduction.** Extend that Rees complex to S=F₂[U^{±1},V^{±1}]. For each generator set e_x=U^{−B(x)}V^{−C(x)}x. Every weighted differential term transforms as

U^{−B(x)}V^{−C(x)} U^{B(x)−B(y)}V^{C(x)−C(y)} y = e_y.

Thus the localized complex is explicitly isomorphic to the unweighted knot Floer complex tensored with S. Since B−C=Q and the Jones degree is J=A−Q, while deg(U)=−1 and deg(V)=1, the transformed generator has degree J(e_x)=J(x)+B(x)−C(x)=A(x). The extra Jones refinement has disappeared in this particular localization. If the Jones parity is p=M+Q and U,V are assigned odd parity, the same change of basis has parity p(e_x)=M+Q+B+C=M modulo two. No claim is made that every other specialization or derived construction must have this behavior.

For the five-generator positive-trefoil example, the only unweighted boundary joins a=(A,Q,M)=(2,3,1) to b=(2,4,0). With n=1 one has R=0; their W-values are 0 and 1. Hence B(a)=B(b)=3, C(a)=0, C(b)=−1, and the Rees differential is ∂a=Vb. It is zero at U=V=0, contributes a polynomial-ring torsion summand S₀/(V), S₀=F₂[U,V], and becomes an acyclic pair when V is inverted. The script checks its gauge transformation and grading. This is a direct concrete illustration of the lost information.

For a generator of gradings (A,Q,M), substituting d=−x⁻¹ changes its Euler term to (−1)^{M+Q}x^{A−Q}. The script sums the five trefoil terms independently and obtains the mirror polynomial t⁻¹+t⁻³−t⁻⁴. To recover V_K from the stated formula for a braid with closure K, use Ω^q_β(t⁻¹,−t), equivalently apply the formula to a mirror braid. Merely writing Ω^q_β(t,−t⁻¹)=V_K is a convention error.

The rank of a homology group cannot be read from its Euler polynomial without additional input: cancellation can conceal generators. This report therefore does not infer the rank of qHFB(σ₁) solely from its three-term polynomial, and does not use such an unverified rank comparison as a descent obstruction.

## Primary sources and reproducibility

- T. Ohtsuki, editor, *Problems on invariants of knots and 3-manifolds*, GTM 4, source normalization at printed p380 and Problem 1.7 at p385: https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf
- C. Anghel and A. Juhász, *Quantum braid Floer homology*, arXiv:2601.08805v4, Theorem 1.13, Remark 2.9, Definition 8.26 and §9: https://arxiv.org/pdf/2601.08805v4
- Knot Atlas, trefoil computational entry, braid and polynomial sections: https://katlas.org/wiki/3_1
- KnotInfo, Jones conventions and mirror rule: https://knotinfo.org/descriptions/jones_polynomial.html

Run `python verify_examples.py` from this directory, or use its full path. `EXACT_CHECK_RESULTS.json` records the successful finite checks. The general configuration propositions and acyclicity arguments above are mathematical proofs; the script is not presented as verification of their universal quantifiers. No broad present-day literature-status or novelty claim is made.
