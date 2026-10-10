# Compact quotient correction and known models for Artin–Tate spectra

This note concerns AIM Problem 3.2, ID 20000032 / AIM-ALGEBRAIC_GEOMETRY-0032. It gives the compact Verdier-quotient formula with its essential tensor-ideal denominator, proves strictness against ordinary thick closure, and records the precise scope of known filtered and odd-prime models. The intrinsic-recognition problem remains unresolved by this work; no novelty is claimed.

## 1. Filtered model: correct, but already explicit in BHS

The displayed presentation

A ≃ Mod_{Φ^{C₂}R_•}(Fil(Sp))

is stated in the proof of BHS Proposition 7.6, arXiv v2 p.54. Here R_• is the even-slice décalage of the MUR,2 Adams resolution, as in Theorem 4.3. The coefficient ring is obtained by applying geometric fixed points levelwise to the already-totalized filtered algebra. This is a valid consequence of Galois reconstruction and monoidal localization. It is not a newly obtained recognizable model.

The formulation in Fil(Sp_i2) is compatible with BHS's i2-linear conventions; Fil(Sp) is the least ambiguous base used in their proof. Neither convention permits replacing the coefficient ring by geometric fixed points applied inside an infinite totalization. BHS constructs a comparison map through that limit and subsequent connective covers, not an equivalence. The resulting F₂-synthetic functor does not solve the recognition problem.

## 2. Compact quotient: the tensor-ideal qualification is essential

The correct compact quotient is

A^ω ≃ ( C^ω / thick^⊗_C(Ca) )^natural,

where C = SH(R)^AT_i2 and Ca is the cofiber of a. The notation thick^⊗_C(Ca) means the thick tensor ideal inside C^ω, allowing tensor products only with compact objects of C. It does not allow arbitrary noncompact tensor factors. Equivalently, the denominator is the ordinary thick closure of all Ca⊗S₂^{r,q,w}. Writing only ordinary thick(Ca) is insufficient. A formula written with an unqualified thick(Ca) is correct only if that notation is explicitly defined to mean this tensor ideal; with ordinary thick closure, the formula is false.

Here is a concrete proof of strictness. Let E = Ca⊗Cta and consider exact extension of scalars

F : C → Mod_C(E).

Under complex base change, Ca is the finite étale algebra Spec(C), and Ca⊗Ca ≃ Ca⊕Ca. Moreover, ta becomes the complex deformation parameter τ (BHS Theorem 2.1). Consequently Mod_C(E) identifies with Cτ-modules in the complex Artin–Tate category, and

F(Ca) ≃ E⊕E,

F(Ca⊗S₂^{0,0,1}) ≃ E(1)⊕E(1),

where E(1) is the weight-one twist of E. It is nonzero because it is an invertible twist of the nonzero unit of Mod_C(E).

For every integer k,

π_k Map_E(E,E(1)) = π^C_{k,-1}(Cτ) = 0.

The vanishing follows either from BHS Theorem 10.1(5), after complex base change, or from the Cτ Ext description with negative internal weight. Hence E(1) is right-orthogonal to E. An object in thick(E) that is right-orthogonal to E is zero: the same orthogonality holds for all objects in thick(E), and then for its own identity. Therefore E(1) is not in thick(E). Nor is E(1)⊕E(1), since E(1) is a retract of that sum.

If Ca⊗S₂^{0,0,1} were in ordinary thick(Ca), exactness and retract preservation would put E(1)⊕E(1) in thick(E), a contradiction. Thus

Ca⊗S₂^{0,0,1} ∉ thick(Ca),

although it belongs to thick^⊗(Ca) and is killed by a-inversion. This establishes the actual error under the ordinary-thick reading.

The cofiber expression Σ(S^C)⁻¹⊗Spec(C) is compatible with the usual Ca≃Spec(C): the representation-sphere twist restricts to ordinary suspension on the free Artin orbit. It is not itself an error.

## 3. Telescope and compactness conventions

For i2-linear objects the telescope formula with index q−n is correct. Inverting a identifies q-shifts, and compact localized sphere twists remain compact because the local inclusion preserves colimits. These statements cannot simply be transplanted to the full derived 2-complete category, whose sphere unit need not be compact.

The [companion proof](PROOF.md) gives a separate argument in the genuinely completed category using mod-2 Moore twists H_w. This resolves the completion issue without assuming that completion and a-localization commute.

## 4. Odd-prime claim

The odd-primary conclusion A_p ≃ Sp_ip follows formally from BHS's odd-prime splitting: a vanishes on the η-complete factor (Lemma 9.4) and is invertible on the real-realization factor. This is a credited low-novelty consequence, not progress on the 2-primary intrinsic-recognition problem. The two complex factors in Proposition 9.1 should not be silently described as a componentwise symmetric monoidal product; the argument only needs the first central-idempotent split and the vanishing of a on its whole η-complete factor.

## 5. Scope and freshness

The original AIM problem inverts a. The Borel-deformation paper models an a-complete category. Its retained v3 discussion continues to separate the a-local sphere from that completed result. Neither completion nor the odd-prime splitting settles the 2-primary recognition question.

Agreement of a generic and a special fiber does not by itself identify the deformation: such an inference would require gluing data. Likewise, saying an arbitrary equivalence with spectra is excluded solely because a specified parameter has a nonzero cofiber would omit compatibility assumptions. The companion proof supplies the stronger, invariant obstruction: no compact generator exists, so even an unstructured stable-category equivalence to an ordinary ring-spectrum module category is impossible.

## Conclusion

Retain the filtered module presentation, telescope sign and carefully scoped odd-prime consequence as known/formal facts. Correct the compact Verdier-quotient denominator to a thick tensor ideal. These presentations do not solve the intrinsic-recognition problem. The compact-generation obstruction and the completion-safe proof give a structural restriction, with novelty explicitly unclaimed.
