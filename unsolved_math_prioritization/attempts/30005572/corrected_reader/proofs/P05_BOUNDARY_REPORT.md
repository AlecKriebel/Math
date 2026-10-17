# PASS1 result: boundary-depth mechanism and the remaining K₂ identity

## Result first

A self-contained local calculation proves that both standard opposite bad-level Hecke operators are **nilpotent** on the K₁(πⁿ)-invariants of a principal series whose two inducing characters are ramified. On oldvectors they need not be zero. This gives the precise spectral mechanism anticipated in Remark 5.2.10 and proves the boundary-only vanishing statement below at arbitrary depth.

It does **not** prove Π_N∘(U_q*−1)=0 for the actual specialized K₂ map. Consequently no unrestricted-depth compactified K₂ map is claimed. The same residual-character exclusions remain; they cannot be discarded by the spectral argument supplied here. The exact additional parabolicity and bad-Hecke lemmas are stated below.

The geometric group/coarse-space comparison works over Z[1/6], since imaginary-quadratic GL₂ has no finite stabilizers of order divisible by 5. That does not repair the motivic-complex inversion of 5 in the existing construction.

## 1. Sources and comparison of the two manuscripts

[S2] E. Lecouturier, R. Sharifi, S.-C. Shih, J. Wang, *Eisenstein cocycles for imaginary quadratic fields*, arXiv:2504.19125v1, 46 pages: https://arxiv.org/pdf/2504.19125v1

[S3] Distinct author-hosted manuscript, same title, 47 pages, retrieved 14 October 2026; no explicit revision label located: https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf

Both inspected versions have the same relevant boundaries:

- Lemma 5.2.2 describes boundary cohomology by induced representations and gives good-prime eigenvalues Nq μ₁(q)+μ₂(q), with S_q eigenvalue μ₁μ₂(q). S2 pp.40–41; S3 pp.41–42.
- Remark 5.2.5 gives the forward ramification/restriction implications used below. Its converses require a single power at the prime in question. S2 p.42; S3 p.43.
- Proposition 5.2.8 and Theorem 5.2.9 impose the depth and residual-character restrictions. S2 pp.43–44; S3 p.44.
- Remark 5.2.10 anticipates a bad-U identity and the corresponding removal of the depth condition while retaining the same residual-character exclusions. S2 p.44; S3 p.45. Its proposed assertion that the operator is zero on a doubly ramified boundary constituent needs the oldvector qualification explained in the local calculation.
- Auxiliary removal is already broader than χ≠ω²: Theorem 4.3.5 covers the whole p-part if (p)∤N² or p∤h; Corollary 4.3.6 assembles the resulting Z[1/30] statement under its exact class-number condition. S2/S3 pp.35–36. These theorems do not by themselves establish parabolicity or the bad-U relation.

All statements below retain the complete adelic space, hence all h class-group components. Statements involving the already constructed auxiliary K₂ maps are limited to the source’s admissible levels, including its assumption that O×→(O/N)× is injective. The local calculation, boundary proposition, and geometric stabilizer argument do not impose that assumption; this distinction does not construct the missing small-level K₂ maps.

## 2. A proved boundary-only statement without a depth bound

Fix p≥7, and use the coefficient prime P, prime 𝔭=P∩O, residue characters ξ, ξ̄, and prime-to-p ray-class character χ of §5.2 of S2/S3. Let

M = H¹(∂X₁^BS(N),Z_p).

At each q|N above p, adjoin one of the two standard opposite level double-coset operators defined in LOCAL_BAD_LEVEL_LEMMA.md. Denote the chosen operator by V_q. Keep the actual integral geometric operator; the local lemma also applies to an inverse-correspondence convention, through its central scalar action on each characteristic-zero constituent.

Consider maximal ideals of the resulting commutative Hecke algebra containing p and

T_l − (Nl+S_l),
S_l − χ(l)             for l∤Np,
V_q − 1                for q|N, q|p.

Here χ(l) may be read after extending coefficients to a finite integer ring containing its values. The formulation via the S_l congruences avoids imposing an additional, unproved ray-class action convention on the homology. It is the residual χ-selection used in the proof of Proposition 5.2.8.

**Boundary proposition.** Without any restriction on v_q(N), the localization of M at every such maximal ideal is zero provided that:

- if p splits, χ|(O/𝔭)× is not ξ and χ|(O/𝔭̄)× is not ξ̄ modulo P;
- if p is inert, χ|(O/p)× is neither ξ nor ξᵖ modulo P;
- if p ramifies, χ|(O/𝔭)× is not ξ modulo P.

The statement is unchanged if all bad primes, rather than only those above p, are included.

### Proof: integral support first

Extend Z_p to a finite complete discrete valuation ring large enough to contain all the needed character and Hecke eigenvalues. The boundary module is finite and torsion-free. Let A be the image of the commutative algebra of the specified Hecke operators in its endomorphism ring. Then A is finite and torsion-free over that valuation ring.

If a localization M_m were nonzero, a minimal prime of A contained in m would avoid p: p is a nonzero divisor in A. The corresponding generic-fiber character occurs on M because A acts faithfully. After a finite field extension, this is a simultaneous characteristic-zero Hecke eigencharacter specializing to m. This elementary argument uses actual maximal ideals; it does not require distinct ordered pairs of residual characters to define distinct maximal ideals.

The boundary induced-representation description in the proof of Lemma 5.2.2 is compatible with finite double-coset correspondences: on the finite-adelic induced functions they act by the corresponding right-translation sums. Choose one pair μ=(μ₁,μ₂) yielding the lifted eigensystem, including its companion μ′=(μ₂N⁻¹,μ₁N) if necessary. The companions have the same ramification places with the two inducing characters exchanged. If both μ₁ and μ₂ are ramified at a prime q above p, the local lemma makes V_q nilpotent on the entire local invariant space, not just the newvector line. Its eigenvalue is therefore zero and cannot specialize to 1. Thus, for this constituent, **at least one inducing character is unramified at every prime above p**. At primes above p not dividing N this already follows from the conductor condition.

### Proof: residual character calculation

Let ν₁,ν₂ be the reductions of μ₁,μ₂ in the conventions of §5.2. The good-prime congruences give

ων₁+ν₂ = ω+ν₁ν₂,
ν₁ν₂ = χ.

These equalities hold as characters on the relevant finite prime-to-p quotient, by the same prime-ideal density argument as in Proposition 5.2.8. Independence of distinct characters shows

ν₁=1 or ν₂=ω.                                           (1)

If ν₁=1, μ₁ cannot be unramified at 𝔭: the forward implication of Remark 5.2.5 would give ν₁|(O/𝔭)×=ξ⁻¹, which is nontrivial. Hence μ₂ is unramified there, by the preceding ordinary-support argument. It follows that ν₂|(O/𝔭)×=ξ, and therefore χ|(O/𝔭)×=ξ.

If ν₂=ω and p splits, μ₂ cannot be unramified at 𝔭̄, since unramifiedness would give the trivial restriction there, whereas ω restricts to ξ̄. Thus μ₁ is unramified at 𝔭̄ and ν₁ restricts trivially there. Consequently χ|(O/𝔭̄)×=ξ̄.

If ν₂=ω and p is inert or ramified, its restriction is respectively ξᵖ⁺¹ or ξ². Neither equals ξ for p≥7. Hence μ₂ cannot be unramified at 𝔭, and μ₁ must be. Its restriction is ξ⁻¹, so χ restricts to ξᵖ in the inert case and to ξ in the ramified case.

Every alternative contradicts the stated exclusions. No single-power converse from Remark 5.2.5 was used. This proves the proposition. ∎

### Scope of this advance

This fills in a boundary spectral calculation anticipated by the authors; no literature-level novelty claim is made. It is a theorem about a boundary localization for explicitly defined double-coset operators. Applying it to the K₂ map still requires the corresponding relation with eigenvalue 1 on that map, together with the correct transpose convention between boundary cohomology and homology. The local proof covers both opposite conventions, but it cannot determine which convention makes the geometric K₂ identity true.

## 3. Why this does not prove the actual bad-U relation

The known specialized cocycle is obtained from a Δ₀(N)-module system by evaluation at (0,P), where P has exact N-order. For a matrix [[a,b],[c,d]] in that monoid, c≡0 mod N and d is a unit mod N, so the specialization stays in the primitive torsion orbit. Proposition 4.1.2 identifies the resulting transport with the Artin action of d. Corollary 4.1.5 then transports the cocycle Hecke identity.

At a bad prime, these hypotheses cannot be silently recycled:

- In the direction represented locally by diag(1,π), the lower-right entry is not a unit. The point is sent to (0,πP), with smaller q-primary order. There is no Artin automorphism R_N(π) that repairs this. For a nonprincipal q this is stated through the corresponding CM isogeny between the appropriate ideal-class components.
- In the opposite direction, which preserves the primitive specialization orbit, the level double coset has Q representatives rather than the Q+1 unramified representatives. The proof of Corollary 4.1.6 explicitly uses equality of the full-level and Γ₀(N) double-coset decompositions only away from N. The omitted branch cannot be discarded from the motivic cycle relation without calculation.

A proof must therefore establish a genuine bad-level distribution/transfer relation, including the changed torsion order and all CM-component/field norm identifications. Neither the local principal-series calculation nor good-prime Eisenstein eigenvalues supply that relation.

### Exact finite-coset form of the missing lemma

Fix the convention for U_q* on homology and take its transpose cohomological correspondence with **constant** target coefficients A_c=K₂(O′(N))⊗Z[1/30]. On a source component r, choose right representatives h_tΓ_s for that correspondence. For γ∈Γ₁(N)_r write

γh_t = h_{σ_γ(t)} τ_t(γ),  τ_t(γ)∈Γ₁(N)_s.

The Artin and component identifications are those used to place all the maps in the common field target in §5.1. Then the required auxiliary bad-Hecke lemma is the following equality for the paper's specific specialized homomorphisms:

Σ_t cΘ_{s,N}(τ_t(γ)) = cΘ_{r,N}(γ)     in A_c, for every γ and every r.     (U)

If the correspondence has several target components, the sum is indexed by its actual target component s(t), with exactly the same formula. This is the usual restriction/conjugation/transfer formula, using constant-coefficient transpose action; it is not an assumption that a nonunit matrix acts through an Artin automorphism. Substituting the Gersten-residue representative from (3.4) and the descended specialization from Proposition 4.1.4 makes (U) a concrete cocycle distribution identity.

At χ≠ω², choose an invertible auxiliary factor as in Theorem 4.3.3. Then (U) implies the unaugmented relation by cancellation, since that target endomorphism commutes with precomposition by the homology correspondence. Existing Theorem 4.3.5 must also be used wherever it gives the entire p-part. No proof of (U) has been obtained in this pass.

## 4. Residual-character exclusions and the exact obstruction

The spectral argument proves only that any surviving ordinary Eisenstein boundary eigensystem must lie on the listed exceptional residual-character loci. It does not prove that every such locus is nonzero, nor that the particular K₂-valued class has nonzero boundary there. Thus these exclusions are sufficient hypotheses in the known proof, not established obstructions to the desired construction.

To remove them, one can prove the stronger concrete cusp lemma (P) in STABILIZERS_AND_OBSTRUCTION.md: the actual specialized cocycle must vanish on the two lattice generators of every cusp unipotent subgroup, in every class-group component. This is equivalent to vanishing of its particular boundary homomorphism. It would remain meaningful when the ambient localized boundary module is nonzero.

No such unrestricted vanishing calculation has been obtained. Neither auxiliary-factor cancellation nor an ordinary bad-U relation alone supplies it at the remaining character loci.

## 5. Acceptance status under the frozen construction contract

Proved here:

1. A full, elementary oldvector/support computation of both local level operators; a nilpotence correction to the zero-operator heuristic at excess depth.
2. The resulting arbitrary-depth **boundary-only** ordinary Eisenstein localization vanishing under the existing residual-character exclusions.
3. A no-order-five stabilizer lemma and the resulting geometric comparison over R=Z[1/6].
4. Exact cusp and finite-coset tests isolating the unresolved compactification and bad-U assertions.

Not proved here:

- the bad-U identity (U) for the specialized K₂ construction;
- unrestricted parabolicity (P), including excluded residual characters;
- an R-valued motivic cocycle or recovery of the missing 5-primary information;
- the integral absolute K₂ target at prime-power levels;
- the relative theta-symbol construction and its descent/relations;
- the missing small-level K₂ construction where the source’s unit-injectivity assumption fails;
- a complete all-field/all-level result satisfying the frozen contract.

In particular this is partial mathematical progress within PASS1, not a completed construction and not a counterexample to the original question. The local depth mechanism was anticipated in S2/S3; the present work makes that mechanism precise and records its remaining logical dependency.
