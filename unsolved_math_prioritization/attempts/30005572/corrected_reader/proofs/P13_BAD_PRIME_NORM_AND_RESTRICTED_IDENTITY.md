# A bad-prime norm identity and a restricted arithmetic U* theorem

Shared PASS 2/5, row 1777 / 30005572. This is a partial construction result. The original all-field/all-level problem remains **UNSOLVED**. This file proves an identity for the actual auxiliary CM K₂ map, and then removes the auxiliary ideal where the source permits cancellation. It does not replace that map by an arbitrary Eisenstein homomorphism.

## 1. Result and precise scope

Let F be imaginary quadratic, let p ≥ 7, and retain **all class-group components** of the LSSW construction. Write L_A = F(A), and use the actual maps

  f_{c,A} = cΠ_A : H₁(Y₁(A), Z_p) → K₂(L_A) ⊗ Z_p.

Their values already belong to the source's subgroup K₂(O′(A)) ⊗ Z_p. Throughout, c is an auxiliary ideal coprime to every level in use. We retain the source's admissibility condition that O× → (O/A)× is injective.

Fix a **principal prime ideal** q = (π). Put Q = Nq and

  N = M qⁿ,  n ≥ 1,  (M,q) = 1.

Assume that M is a proper ideal and is itself admissible. Choose the level markings coherently so that multiplication by π takes the primitive point at level Mqʲ to that at level Mqʲ⁻¹. This is possible for a principal q; changing these markings changes the formulas by the corresponding compatible Artin actions.

Let U*_{q,N} be the unnormalized homology correspondence whose transpose on constant-coefficient group cohomology is the double coset of diag(1,π). More explicitly, its transpose is the transfer formula in §2. This fixes the previously unspecified dual convention; it is the adjoint correspondence to the diag(π,1) convention, since diag(1,π)=π diag(π,1)⁻¹ and rational scalar matrices act trivially on the symmetric space. No division by Q is made. In adelic language one must retain the central factor when comparing an inverse correspondence with the integral opposite matrix; an unannounced tame diamond twist would change the statement.

**Theorem A (unconditional norm-kernel statement, in this principal-prime range).**

  Cor_{L_N/L_M} ∘ f_{c,N} ∘ (U*_{q,N} − 1) = 0.                 (A)

This is a statement about the specialized, descended arithmetic map, not merely a boundary calculation.

Set I = Gal(L_N/L_M). Its order is

  d = Qⁿ⁻¹(Q−1).

**Theorem B (actual bad-U identity on inflated characters).** Suppose p does not divide d, and let χ be a character of the prime-to-p part of Gal(L_N/F) that is trivial on I. Then

  f^χ_{c,N} ∘ (U*_{q,N} − 1) = 0.                            (B)

If the unaugmented source map Π_N^χ exists by Theorem 4.3.3, equivalently with its χ ≠ ω² condition interpreted exactly as in that source, then

  Π_N^χ ∘ (U*_{q,N} − 1) = 0.                               (C)

The same conclusion is tautologically valid on any exceptional component which the proof of source Theorem 4.3.5 shows is zero. We do not cancel an auxiliary factor on an arbitrary exceptional component merely because an unaugmented class exists there.

For n=1, the arithmetic restriction is p ∤ (Q−1); this allows q above p. For arbitrary n≥2 it requires both p ∤ Q and p ∤ (Q−1). In every case the character is unramified at q in the precise sense of inflation from the q-free level M. We impose no class-number-one or Euclidean assumption.

Whenever the source map already factors through X₁(N), (C) holds for that compactified map too, because the finite correspondence preserves the cusp set and descends to the compactification. This theorem alone does not establish unrestricted parabolicity or repair the original coefficient ring Z[1/6].

The proof is given below. The limitations in §8 are substantive: in particular, this does not remove the p-power-depth obstruction on arbitrary characters at q|p.

## 2. Group and Hecke conventions

On component r, put a = a_r. It is convenient to work first with the strict group

  Γ_A^s = { γ = [[a₀,b],[c₀,d₀]] ∈ Aut_O(a ⊕ O), acting on row vectors :
              c₀ ∈ A a, d₀ ≡ 1 mod A }.

Thus b ∈ a⁻¹, c₀ ∈ a, and det γ ∈ O×. The source allows d₀ to be congruent to any element of O×. At an admissible level its group is the direct product of Γ_A^s and its central scalar unit subgroup: divide a matrix by the unique unit represented by its lower-right entry. That central subgroup has order dividing 6. Passing to H₁ with Z_p coefficients, p≥7, therefore gives the same homology and compatible finite correspondences. Working with strict groups loses no p-primary information in the source map.

Temporarily write N=Aq, with A proper and admissible, whether or not q divides A. Set

  α = diag(1,π),   β = diag(π,1).

There are two maps on component homology from level N to A:

  F : induced by γ ↦ γ;
  D : induced by γ ↦ α⁻¹γα.

The second conjugation sends [[a₀,b],[c₀,d₀]] to [[a₀,πb],[c₀/π,d₀]], hence does map Γ_N^s into Γ_A^s.

Choose representatives ℓ_t for the rank-one O-module

  N a / π N a.

There are Q representatives. A right-coset decomposition of Γ_N^s α Γ_N^s is given by

  h_t = [[1,0],[ℓ_t,π]] = α k_t,
  k_t = [[1,0],[ℓ_t/π,1]] ∈ Γ_A^s.                           (2.1)

For γ ∈ Γ_N^s, write

  γ h_t = h_{s_γ(t)} τ_t(γ),  τ_t(γ) ∈ Γ_N^s.

If f:Γ_N^s→B is a homomorphism with constant target coefficients, then

  (f ∘ U*_{q,N})(γ) = Σ_t f(τ_t(γ)).                         (2.2)

This is restriction/conjugation/transfer. It is independent of the coset representatives on homology. It does **not** assign an Artin automorphism to π at level N.

The coset count follows locally from the additional condition c₀∈qN a in Γ_N^s ∩ αΓ_N^sα⁻¹. Globally the lower-unipotent elements in (2.1) realize the quotient, since a is locally free of rank one. This works on every ideal-class component.

## 3. The one-coordinate CM trace calculation

This section supplies the arithmetic input which is absent from a mere boundary eigenvalue argument.

Work over one auxiliary CM definition field F(f), with f coprime to N. On

  E = E_r × E₁,

the source's unspecialized degree-one Gersten primitive is

  v_c = cθ_r ⊠ E₁[c] + Nc (0) ⊠ cθ₁,

with boundary e_c = (Nc)²(0) − E[c]. Here Nc denotes the absolute ideal norm; (Nc)² is its square.

The isogeny α acts as identity on E_r and multiplication by π on E₁. Since q is coprime to c, it bijects E₁[c], and

  [π]_* cθ₁ = cθ₁.

To justify the last identity, pushforward preserves the divisor Nc(0)−E₁[c], and it preserves trace-fixedness. The trace-fixed theta primitive with that divisor is unique in the source's coefficient range. Consequently

  α_* v_c = v_c,   α_* e_c = e_c.                            (3.1)

This is one-coordinate trace compatibility, stronger than simply saying that the K₂ class is fixed by simultaneous scalar traces.

### Compatible moving primitives

Let P_N and P_A be the coherent primitive points, with πP_N=P_A. Choose

  x ∈ c Hom(E₁,E_r)

whose reduction is a unit at A. Since A is proper, xP_A≠0. For the low level use

  μ_A = [[1,0],[x,1]],

and for the high level use

  μ_N = [[1,0],[πx,1]].

Then μ_N α = α μ_A, and proper pushforward/base change gives

  α_* μ_N* v_c = μ_A* v_c.                                 (3.2)

Although πx is not a unit at N, this high-level moving primitive is valid: at every point (0,R) in the α-fiber above (0,P_A),

  (πx)R = xP_A ≠ 0.

Also R does not belong to E₁[c], since its image P_A does not. The two supports in the moved primitive therefore avoid the whole fiber, not merely one chosen point. For γ∈Γ_N^s the fiber is γ-stable after conjugating the target action, so the same statement holds for the support of its γ-pullback.

Let C_N and C_A denote the generic trace-fixed cocycles obtained from these two moved primitives. For γ∈Γ_N^s, set γ_A=α⁻¹γα. Naturality of residues, (3.2), and injectivity of the left map in the trace-fixed Gersten complex imply

  α_* C_N(γ) = C_A(γ_A).                                   (3.3)

Indeed, their residues are equal because α_*γ*=γ_A*α_*; the difference is a trace-fixed unramified class, hence zero over Z[1/30], and therefore after tensoring with Z_p for p≥7.

The use of a different moving matrix does not change the resulting homomorphism on Γ_N^s. The difference of its two degree-one primitives has zero boundary and is supported away from the primitive specialization orbit. Its unique trace-fixed K₂ primitive is therefore regular on that orbit. The two cocycles differ by its coboundary, whose specialization on Γ_N^s is zero because that group fixes (0,P_N). The same argument applies at A. Thus the maps in (3.3), after specialization, are the **source's actual** f_{c,N} and f_{c,A}.

## 4. Exact norm compatibility, including the missing lower-order branch

Take the fiber of α above λ_A=(0,P_A).

### Case q|A

All Q points in the fiber have exact N-order. Over F(Af), the fiber is Spec F(Nf): the relative ray group has order Q and acts simply transitively on the lifts. Proper base change for K₂ and (3.3) give

  Cor_{L_N/L_A} f_{c,N} = f_{c,A} ∘ D.                     (4.1)

### Case q∤A

There is one point in that fiber whose second coordinate has exact A-order, namely

  R₀ = [π]⁻¹ P_A ∈ E₁[A].

The other Q−1 points have exact N-order and form the relative ray-field orbit. Thus the fiber over F(Af) is the disjoint union of Spec F(Nf) and one rational point. If

  σ = R_A((π)) ∈ Gal(L_A/F),

then specialization at (0,R₀) is σ⁻¹ f_{c,A}, by the source's prime-to-A specialization/Artin comparison. Hence

  Cor_{L_N/L_A} f_{c,N}
     = f_{c,A} ∘ D − σ⁻¹ f_{c,A} ∘ F.                     (4.2)

The second term must not be omitted. The statement involves σ only at the **lower**, q-free level. No R_N(q) is defined or used.

### Descent is verified, not inferred from invariance

The calculation above can be made after restriction to F(Nf) and F(Af), but this alone is insufficient if restriction has a p-primary kernel. Choose a rational prime l≡2 mod p, outside the finite set dividing N, the fixed class representatives a_r, and the discriminant, with l>3, and let f be a prime above l. Its residue degree is 1 or 2, so |(O/f)×| is congruent to 1 or 3 modulo p and is prime to p. Such a choice also makes the unit reduction injective. The source's Proposition 4.1.4 then identifies the descended maps after an extension of degree prime to p; restriction is injective on K₂⊗Z_p by cor∘res=[extension degree].

The field base-change square has the required full degree. Chinese remaindering in the ray class exact sequence, using injectivity of O×→(O/A)×, identifies the relative ray kernel for Nf over A with the product of its q-part and its f-part. The two factors have trivial intersection. Thus F(Nf)=F(N)F(Af) and F(N)∩F(Af)=F(A). Consistently, the ray class number formula gives

  [F(Nf):F(Af)] = [F(N):F(A)],

so this is the actual base change of F(N)/F(A), with no reduced degree. Thus restriction commutes with the corestrictions in (4.1)–(4.2). Their equality after restriction descends to L_A. This also explains why the small-level/unit-injectivity hypotheses have been retained rather than silently removed.

## 5. The exact degeneracy identities

We prove the required identities on homomorphisms; equivalently they hold on homology with the indicated coefficient actions.

### Identity 1: the first degeneracy map

For any homomorphism f_A:Γ_A^s→B, (2.1) gives

  τ_t(γ) = k_{s_γ(t)}⁻¹ (α⁻¹γα) k_t.

The k-terms cancel in the sum. Therefore

  f_A F U*_{q,N} = Q f_A D.                                (5.1)

### Identity 2: a prime already dividing the lower level

If q|A, conjugating h_t by α gives

  α⁻¹h_tα = [[1,0],[ℓ_t/π,π]].

These are exactly Q representatives for the same dual correspondence at level A. Conjugating the finite-coset equations proves

  D U*_{q,N} = U*_{q,A} D.                                 (5.2)

### Identity 3: the first appearance of q in the level

Assume q∤A. Let T*_{q,A} denote the **constant-coefficient** homology correspondence of α at level A. It has Q+1 branches. The Q conjugated representatives in Identity 2 are all but one of them.

Choose w∈Γ_A^s whose upper-left entry is divisible by π and which reduces at q to a Weyl-type element. Strong approximation supplies w on every class-group component, since q∤A. Put

  δ = β⁻¹ w α.

It is integral on a⊕O, has unit determinant, and lies in Γ₀(A); its lower-right entry is congruent to π modulo A. The missing right representative is

  h_∞ = wα = βδ.

For γ_A=α⁻¹γα, this branch is fixed and its residual group element is

  h_∞⁻¹ γ_A h_∞ = δ⁻¹ γ δ.

The source cocycle on Γ₀(A) has coefficient action R_A(d₀). Since γ has trivial coefficient action, the cocycle identity gives the exact conjugation formula

  f_{c,A}(δ⁻¹ γ δ) = σ⁻¹ f_{c,A}(γ).

There is no omitted coboundary term in this equality. Consequently

  f_{c,A} D U*_{q,N}
     = f_{c,A} T*_{q,A} D − σ⁻¹ f_{c,A} F.                (5.3)

For clarity, w can be chosen by prescribing its reduction in the q-local lattice basis, and then using the surjectivity furnished by strong approximation for the associated SL₂ arithmetic lattice. Integrality of δ is precisely the divisibility of w's upper-left entry by π; its other entries already have the correct a⁻¹ and a memberships for the upper-right and lower-left entries, respectively. The coset claim can also be checked at q, where the Q displayed lower-unipotent translates and the Weyl branch are the Q+1 lines. Away from q the change is invertible.

The known good-prime identity has, in this **dual** convention, the form

  f_{c,A} T*_{q,A} = (1 + Qσ⁻¹) f_{c,A}.                   (5.4)

One must not substitute Q+σ into (5.4). To verify the normalization directly, the motivic pullback Hecke operator of α has eigenvalue Q+[π]* on the source cocycle. On specialization its left-hand side is σ times the constant-coefficient transfer; its right-hand side is Q+σ. Division by the invertible Artin automorphism σ gives (5.4). The full and level-A coset decompositions agree because q∤A, as in source Remark 3.4.2 and Corollary 4.1.6.

## 6. Proof of Theorems A and B

At N=Aq with q∤A, abbreviate f=f_{c,A} and C=fD−σ⁻¹fF. By (5.1), (5.3), and (5.4),

  C U*_{q,N}
    = (1+Qσ⁻¹)fD − σ⁻¹fF − Qσ⁻¹fD
    = fD − σ⁻¹fF
    = C.

By (4.2), C=Cor_{L_N/L_A} f_{c,N}. This proves (A) at depth one.

At a higher step N=Aq with q|A, (4.1) and (5.2) give the exact recursive defect formula

  Cor_{L_N/L_A}[f_{c,N}(U*_{q,N}−1)]
      = [f_{c,A}(U*_{q,A}−1)] D.                          (6.1)

Corestrictions compose. Iterating (6.1) down to the first q-step, where the preceding calculation applies, proves (A) for every n≥1.

For Theorem B, p∤d makes I a prime-to-p subgroup. If χ is trivial on I, I acts trivially on the χ-component of the arithmetic target. For z in that component,

  res_{L_N/L_M} Cor_{L_N/L_M}(z) = Σ_{g∈I} g z = d z.

Since d is a p-adic unit, corestriction is injective on that component. Apply this to each value of the defect in (A). This proves (B).

Finally choose c with (Nc)²−R_N(c) invertible on the χ-component, as provided by source Corollary 4.3.2. Calibration says

  ((Nc)²−R_N(c)) Π_N^χ = f^χ_{c,N}.

This target endomorphism commutes with precomposition by U*. Cancelling it in (B) proves (C). No assertion that a norm is injective on the entire arithmetic target has been used.

Because K₂(O′(N)) injects into K₂(L_N), vanishing proved in the field target is the same vanishing for the source's existing integral/localized target. This observation does not improve O′(N) to O(N) when those rings differ.

## 7. What remains for nonprincipal primes

The one-coordinate trace calculation itself has a clean nonprincipal form. Let

  φ:E_s→E_t

be the q-isogeny between the actual CM ideal-class components, and put α=id×φ. For c prime to q, pushforward gives

  φ_* cθ_s = cθ_t,
  α_* v_{c,(r,s)} = v_{c,(r,t)}.

Choose a lower-level point P_t and a high-level lift P_s with φ(P_s)=P_t. A moving entry x:E_t→E_r gives the compatible high-level entry x∘φ:E_s→E_r. The identical support argument proves the generic trace identity and, after specialization, the intrinsic norm identity for these **marked product components**. If q∤A, the extra term is evaluation at the unique A-torsion preimage φ⁻¹(P_t), and it must be retained.

This does not yet identify every term with the paper's fixed r↦(r,1) Bianchi tuple and its fixed torsion markings. The isogeny changes the second CM class, and re-identifying E_r×E_t with an (s,1)-component requires a determinant-compatible lattice isomorphism and a verified level-point/Artin identification. The adelic degeneracy shifts the component class by [q]⁻¹; treating q as a scalar on the original curve erases this shift and is invalid.

An intrinsic statement with its actual marked components is established by the preceding argument. A standard all-nonprincipal-prime version of Theorems A and B would additionally have to assemble these identifications and the corresponding missing-branch relation into the fixed adelic convention. That final assembly is **not claimed proved here**. In particular, the principal-prime hypothesis in Theorems A and B has not been dropped.

## 8. Exact remaining obstruction and comparison with the cyclotomic argument

In the proved principal-prime range define

  Δ_{c,N,q} = f_{c,N}(U*_{q,N}−1).

Theorem A locates every value of this **specific** defect in

  ker[Cor_{L_N/L_M}:K₂(L_N)⊗Z_p → K₂(L_M)⊗Z_p].            (8.1)

The defect is zero exactly when its values vanish inside (8.1). This sharpens PASS1's finite-coset obstruction: the same explicit finite-coset defect now has a proved arithmetic norm-kernel constraint, as well as the recursive formula (6.1).

This is not a proof on the remaining character pieces:

- If a prime-to-p relative character is nontrivial, its entire component maps to zero under the norm. The norm identity has no injectivity content there.
- If p divides d, the norm can have p-primary kernel even on invariant elements. The relation res∘cor=d does not allow cancellation. For instance, on a trivial Z/p-module the trace of a group of order p is zero. This is a formal warning, not a claimed nonzero value of the CM defect.
- At q|p and n≥2 the q-primary relative ray extension has precisely the problematic p-power degree.
- If deleting q leaves the unit ideal or a nonadmissible level, the low-level specialization used here is not supplied by the source. Evaluating the theta primitive at its origin is not an acceptable replacement.
- Source restrictions on p, auxiliary removal, compactification characters, and the localized absolute target remain distinct.

The cyclotomic comparison confirms why a norm argument alone cannot be promoted to a full Bianchi theorem. Lecouturier–Wang's proof combines their level compatibility with an **already established** Fukaya–Kato bad-prime theorem at a larger p-divisible level and a surjectivity theorem for a degeneracy-map combination. Neither Bianchi substitute has been proved here. The recent Sharifi survey reports that cyclotomic result; it is not a Bianchi transfer theorem.

## 9. Sources and verification boundary

- Lecouturier–Sharifi–Shih–Wang, *Eisenstein cocycles for imaginary quadratic fields*, arXiv:2504.19125v1, §§2.1–2.3, 3.2–3.4, 4.1, 4.3, 5.1–5.2: https://arxiv.org/pdf/2504.19125v1 . The distinct retained author manuscript has the same ingredients and leaves Remark 5.2.10 as an expectation: https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf . Its extra page and different bytes are not called an arXiv v2.
- Lecouturier–Wang, *Level compatibility in Sharifi's conjecture*, arXiv:2208.06921v1, especially Lemma 4.1 and §4.3: https://arxiv.org/pdf/2208.06921v1 . The published version is Canad. Math. Bull. 66 (2023), 1194–1212, https://doi.org/10.4153/S0008439523000267 ; its numbering differs. We used the explicitly numbered retained arXiv version for the comparison.
- Sharifi, *Through the lens of the Eisenstein ideal*, arXiv:2610.04943v1, discussion after Theorem 1: https://arxiv.org/html/2610.04943v1 . This was checked as a pointer to the preceding cyclotomic result, not used as a proof of a Bianchi assertion.

This file supplies the displayed norm and coset arguments. It uses the already constructed LSSW cocycle, its trace-fixed Gersten exactness over Z[1/30], its descent and prime-to-level Hecke theorem. It is not a reproof of those foundational source results, a novelty certificate, or a solution to the frozen full construction contract.
