# Direct finite-orbit normalization of the ordinary cocycle

Authored PASS 2 supplement, 14 October 2026. This gives a shorter second annihilator for the ordinary lifting theorem. It does not prove trace-fixed lifting.

Use `R,C,C_2,Γ,Z_c,η,θ̄` as in `ORDINARY_LIFT_AND_REMAINING_TRACE_OBSTRUCTION.md`. Let `S` be any finite reduced `Γ`-stable closed subscheme of `A`, disjoint from the support of `Z_c`. Write

`D=deg_L S=Σ_{s∈|S|}[k(s):L]`.

Here `|S|` is the finite set of closed points over `L`, not a selection of geometric orbits. All its points are retained.

## Construction

For each `s∈|S|`, let `B_s=O_{A,s}`. Since the local residue of `η` at `s` is zero, exactness of the regular-local Gersten sequence gives an element

`a_s∈K_2(L(A))⊗R`

whose Gersten residues at height-one points of `Spec B_s` equal those of `η`.

Choose ordinary representatives `x_γ∈C_2` of `θ̄(γ)`, and write `k=dx∈Z²(Γ,C)`. The convention for the induced action on indexed local objects is

`(γa)_s=γ(a_{γ^{-1}s})`.

For each `γ,s`, the element

`z_{γ,s}=x_γ−(γa_{γ^{-1}s}−a_s)`

has zero local Gersten residues at `s`. It therefore belongs to `K_2(B_s)⊗R`. Define

`r_S(γ)=Σ_{s∈|S|} Norm_{k(s)/L}(e_s^*z_{γ,s}) ∈ C`,

where `e_s^*:K_2(B_s)→K_2(k(s))` is residue-field pullback.

For clarity, the local-field equivariance used here is an actual ring-and-field statement. An `L`-automorphism `γ` identifies the local ring at `γ^{-1}s` with the local ring at `s` under the adopted module convention. It identifies their maximal ideals and induces an `L`-field isomorphism `k(γ^{-1}s)→k(s)`. The square of local rings and their residue fields commutes. Therefore K-theory functoriality gives `e_s^*(γu)=γ(e_{γ^{-1}s}^*u)`, and naturality of finite-field-extension transfer under an `L`-isomorphism gives

`Norm_{k(s)/L}(e_s^*(γu))=Norm_{k(γ^{-1}s)/L}(e_{γ^{-1}s}^*u)`.

Thus the direct sum of the local evaluation maps, followed by the sum of field transfers, is `Γ`-equivariant. Its target `C` has trivial `Γ`-action. Applying it to the group coboundary of `z` gives

`d r_S = D k`.

Indeed, the coboundary of `γa−a` is zero, and a constant class restricts and then transfers at `s` to `[k(s):L]` times that class. Therefore

`Ψ_S = D x−r_S`

is a genuine ordinary cocycle in `C_2` lifting `Dθ̄`, with residue `D(γη−η)`.

## Choice independence of this multiple

The cocycle `Ψ_S` is independent of the ordinary representatives `x_γ`: replacing them by `x_γ+c_γ` adds `D c_γ` to `r_S(γ)`, so the difference cancels.

It is also independent of the local Gersten primitives `a_s`. If `a_s′−a_s=u_s`, then `u_s∈K_2(B_s)⊗R`. The change in `r_S` is the negative group coboundary of

`Σ_s Norm_{k(s)/L}(e_s^*u_s) ∈ C`.

Since `Γ` acts trivially on `C`, this coboundary is zero. Thus `Ψ_S` is canonical for the specified `η` and `S` (with the quotient cocycle already determined by `η`). No independence of `S` is asserted.

If `η′=η+∂q` for `q∈Q` and `x` is adjusted by the corresponding quotient coboundary, the construction changes by an ordinary coboundary; this also follows by making the local primitive choices after adding an ordinary representative of `q`. This statement is about cocycle classes for a fixed `S` disjoint from both zero-cycles; it is not trace normalization.

## Application to the CM auxiliary cycle

Choose a prime ideal `q` prime to `c` with `Nq≡2 or3 mod5`, as in §4 of the main proof, and take

`S=A[q]−{0}`.

This is reduced and finite étale over the characteristic-zero field `L`; it is `Γ`-stable because `Γ` is `O`-linear. It misses `A[c]`, and

`D=(Nq)^2−1`

is prime to five. Hence the direct finite-orbit construction proves `Dδ[θ̄]=0`. Combining it with `5δ[θ̄]=0` proves ordinary lifting, without adjoining any torsion field or choosing any stabilizer subgroup.

More explicitly, let `S_βθ̄` be the genuine fivefold trace-fixed cocycle from the main proof. For any integers `a,b` with `5a+Db=1`,

`Θ=a(S_βθ̄)+bΨ_S`

is an ordinary cocycle lifting `θ̄` itself, with the prescribed residue. No degree is inverted. The full lift can depend on `B_β`, `S`, and the Bézout choice. These are precisely why this ordinary construction is not a canonical trace-fixed or isogeny-compatible theta normalization.

For `F=Q(√−5)` and `c` prime to `q=(2,1+√−5)`, take `Nq=2`. Then `D=3`, already a unit of `R`, so `Ψ_S/3` is an ordinary lift directly. This is a particularly small genuine CM test case. It still supplies no invariance under all scalar trace norms.
