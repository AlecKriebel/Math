# Integral constant-quotient repair for a product of two elliptic curves

Authored proof candidate, 14 October 2026, current PASS 1. The argument below proves left exactness of a corrected complex over `R = Z[1/6]`, and a conditional quotient-valued cocycle construction. It does not assert the desired integral Eisenstein map, existence of every required degree-zero residue lift, auxiliary removal, or compactification.

## 1. Setup and claims

Let `A = E_1 ×_L E_2`, with each `E_i` an elliptic curve over a characteristic-zero field `L`. For the full-CM statements assume both curves have actions of the full integer ring `O` of an imaginary quadratic field `F`, defined over `L`. Define `C_2,C_1,C_0` as in the companion obstruction note, with `R` coefficients, and set

`C = image(K_2(L) ⊗ R → C_2)`,

`U = ker(C_2 → C_1) = H²(A,R(2))`,

`Z_1 = ker(C_1 → C_0)`,

`V = Z_1 / image(C_2 → C_1) = H³(A,R(2))`.

The constant map is injective by the rational-origin argument in the companion note. Constants lie in `U`, and all these groups and maps carry the commuting trace operators `T_α = [α]_*`. A superscript `tf` always means invariance under all `α` prime to some nonzero exceptional element, with a filtered union over exceptional elements.

**Theorem A (constant-quotient repair).** There is an exact sequence

`0 → (C_2/C)^tf → C_1^tf → C_0^tf`,

where exactness is asserted at the first two nonzero terms only. The quotient is taken **before** the trace-fixed subgroup. In general it is not justified to replace it by `C_2^tf/C^tf`.

**Theorem B (original left kernel).** The original left kernel is exactly the trace-fixed constants:

`ker(C_2^tf → C_1^tf) = C^tf`.

With maximal CM, this is `K_2(L)[5]` when 5 ramifies in `F`, and zero when 5 is unramified (for number-field `L`, or with `[5]` interpreted on `K_2(L) ⊗ R` over a general field).

**Theorem C (unramified-5 original repair).** If 5 is unramified in the imaginary quadratic maximal order, then the unquotiented sequence

`0 → C_2^tf → C_1^tf → C_0^tf`

is exact at its first two nonzero terms over `R`.

Theorems A and B also work with scalar-integer trace invariance, with scalar-fixed constants replacing full-CM-fixed constants in B. C requires the additional full-CM traces. All three apply to `E_1 × E_2`; the two factors need not be the same curve.

## 2. Integral curve projectors, without rational cancellation

For an elliptic curve `E/L` with origin `e`, put in `CH¹(E×E)`

`π_0 = [e×E]`, `π_2 = [E×e]`, `π_1 = [Δ_E] − π_0 − π_2`.

Use the convention that a correspondence `Z` acts on motivic cohomology by

`z ↦ (p_2)_*(p_1^*z · [Z])`.

Thus the graph `Γ_f` of a finite morphism acts by `f_*`. The three `π_i` are integral, pairwise orthogonal idempotents and sum to the identity. For the cross compositions, one intersection pushes forward with a dimension drop and the other is the self-intersection of the origin divisor, whose normal bundle is a one-dimensional vector space over `L` and has zero first Chern class. The remaining compositions are immediate from the degree-one rational origin.

Here is the crucial **integral** correspondence identity, for every integer `m ≥ 1`:

`[Γ_[m]] = m²π_0 + mπ_1 + π_2` in `CH¹(E×E)`.

To prove it, set `M = O_E(e)` and

`P = O_{E×E}(Δ_E − e×E − E×e)`.

Up to the usual sign in the principal self-duality of `E`, `P` is the normalized Poincaré bundle. Its biextension property gives

`([m]×id)^*P ≅ P^⊗m`.

The symmetric degree-one bundle satisfies `[m]^*M ≅ M^⊗m²`. Both are line-bundle identities over `L`, not numerical or rational equivalences with a hidden denominator. Now `Γ_[m] = ([m]×id)^{-1}(Δ_E)`, so

`O(Γ_[m]) ≅ P^⊗m ⊗ p_1^*M^⊗m² ⊗ p_2^*M`.

Taking its integral divisor class gives

`[Γ_[m]] = m[Δ_E] + (m²−m)[e×E] + (1−m)[E×e]`,

which is the stated identity. In particular, pushforward by `[m]` has eigenvalues `m²,m,1` on the three actual integral direct summands. No conclusion is obtained merely by canceling a power of `m` in a torsion group.

## 3. Product weights and the two extreme summands

External products of the curve projectors, with the factors reordered, give integral orthogonal idempotents

`Π_r = Σ_{i+j=r} π_i^(1) ⊠ π_j^(2)`, for `0 ≤ r ≤ 4`,

in `CH²(A×A)`. Their sum is `Δ_A`, and scalar trace `T_m` acts on the image of `Π_r` by `m^(4−r)`.

The `Π_0` summand of `H^j(A,R(2))` is the pullback of `H^j(L,R(2))`. The `Π_4` summand is the image of the origin Gysin map and is `H^(j−4)(L,R(0))`. These identifications can be checked directly using origin pullback and structure-map pushforward, whose relevant composites are the identity. Chow correspondences act on integral higher Chow groups, so these are actual integral splittings of the motivic cohomology groups used here.

For `j=2`, the first extreme summand is `K_2(L) ⊗ R = C`, and the other is `H^−2(L,R(0)) = 0`. For `j=3`, both extreme summands vanish:

`H³(L,R(2)) = CH²(Spec L,1) ⊗ R = 0`,

`H^−1(L,R(0)) = 0`.

The former vanishing is elementary: the degree-one higher-Chow simplex over a field has dimension one and has no codimension-two cycles. The latter is the ordinary vanishing of negative cohomology of the weight-zero constant motivic complex.

Consequently **both `U/C` and `V` are direct sums of scalar trace weights 1, 2, and 3**. In particular, for every positive integer `m`,

`P_m(T_m) = (T_m−m)(T_m−m²)(T_m−m³)`

annihilates both groups. This statement uses only scalar multiplication. No assertion that the individual product projectors are compatible with every CM isogeny is needed below.

## 4. An annihilator with augmentation one

Fix an exceptional element `β ∈ O−{0}`. Choose a positive integer `n` such that every rational integer prime to `n` is prime to `β`; taking `n` divisible by the rational primes dividing `N(β)` suffices. Let `M_β = {α ∈ O−{0} : (α,β)=1}`.

In the commutative monoid algebra `R[M_β]`, augmentation sends each formal trace operator to 1. The augmentation of `P_m(T_m)` is

`r(m) = (1−m)(1−m²)(1−m³)`.

As `m` ranges over positive integers prime to `n`, these numbers generate the unit ideal of `R`. Indeed, for any rational prime `q ≥ 5`, choose a primitive root modulo `q`, whose order `q−1` exceeds 3, and use CRT to choose `m` in that class and prime to `n`. Then no factor of `r(m)` is divisible by `q`. The primes 2 and 3 have been inverted. The gcd is nonzero because some admissible `m>1` exists, and any ideal in `R` is finitely generated.

Hence there are finitely many admissible `m_j` and `a_j ∈ R` with

`Σ_j a_j r(m_j) = 1`.

Set `Φ = Σ_j a_j P_(m_j)(T_(m_j))`. Then

- `ε(Φ)=1`, so `Φ` fixes every `M_β`-fixed element of every trace module;
- `Φ(U/C)=0` and `Φ(V)=0`;
- `Φ` commutes with every full-CM trace `T_α`.

As a check, when `n=5`, the integers 2 and 3 are admissible and `99r(2)−5r(3)=1` because `r(2)=−21` and `r(3)=−416`. No use of this special choice is required for the theorem.

## 5. Proofs of A and B

First, an `M_β`-fixed element of `U/C` is both fixed and killed by `Φ`; it is zero. Passing to the filtered union gives `(U/C)^tf = 0`.

This proves injectivity in A. It also proves B: if `u ∈ U^tf`, its class in `(U/C)^tf` is zero, so `u ∈ C`; its trace invariance is then precisely membership in `C^tf`. The reverse inclusion is immediate.

For exactness at `C_1^tf`, let `y ∈ Z_1` be fixed by `M_β`. Its image in `V` is fixed; since `Φ` kills `V`, that image is zero. Choose `z ∈ C_2` with `∂z=y`, and let `z̄` denote its class in `C_2/C`.

For each `α ∈ M_β`, the element `(T_α−1)z̄` lies in `U/C`. Therefore

`(T_α−1)Φz̄ = Φ(T_α−1)z̄ = 0`.

Thus `Φz̄` is `M_β`-fixed, and

`∂(Φz̄) = Φy = y`.

This is the required invariant lift. It proves A on each fixed module, hence on the filtered union.

The explicit computation of `C^tf` in B is supplied by §6 of `CONSTANT_FIVE_TORSION_OBSTRUCTION.md`.

## 6. Proof of C when 5 is unramified

For `α ∈ M_β`, set `d_α = N(α)²`. The operator `T_α−d_α` kills all constants and has augmentation `1−d_α`.

The numbers `1−d_α`, for `α ∈ M_β`, generate the unit ideal of `R` when 5 is unramified. To see this, scalar integers already show that a common prime divisor outside 2 and 3 can only be 5: for any `q ≥ 7`, CRT supplies an admissible scalar whose fourth power is not 1 modulo `q`. For 5, norm surjectivity in the split or inert algebra `O/(5)` supplies a unit of norm 2, and CRT with the other prime ideals dividing `β` gives an admissible `α` with `d_α ≡ 4 mod 5`.

Choose finitely many `b_α ∈ R` such that

`Σ_α b_α(1−d_α)=1`,

and put `B = Σ_α b_α(T_α−d_α)`.

Then `ε(B)=1` and `B(C)=0`. Section 4 gives `Φ(U) ⊂ C`, so `Ψ=BΦ` annihilates all of `U`; it also kills `V`, has augmentation 1, and commutes with all traces in `M_β`.

For `y ∈ Z_1^(M_β)`, its image in `V` is zero. Choose an ordinary lift `z ∈ C_2`. As `(T_α−1)z ∈ U` for all `α ∈ M_β`, the element `Ψz` is fixed by every such trace, with residue `y`. This proves middle exactness of the unquotiented sequence. Injectivity follows from `U^(M_β)=0`, either by the same operator or by Theorem B.

Nothing in this proof establishes that every fixed degree-zero zero-cycle is already the residue of a fixed element of `C_1`.

## 7. Conditional quotient-valued cocycle and its precise lifting obstruction

Let `Γ` act on the complex by `L`-automorphisms of `A` commuting with the full-CM scalar action. In particular this applies to each geometric automorphism group used before the Hecke extensions in the source. The filtered trace-fixed parts are then `Γ`-stable. Set

`Q = (C_2/C)^tf`.

Suppose `Z ∈ C_0^tf` is `Γ`-invariant and that a specific `η ∈ C_1^tf` satisfying `∂η=Z` has been constructed. Theorem A gives a **unique** `θ̄(γ) ∈ Q` with

`∂θ̄(γ) = γη−η`.

Injectivity of `Q → C_1^tf` proves the cocycle identity. If another such `η′` is chosen, exactness writes `η′−η=∂q` for a unique `q ∈ Q`, so the new cocycle differs by the coboundary `γq−q`. Therefore the class `[θ̄] ∈ H¹(Γ,Q)` is independent of this residue-lift choice.

This is a legitimate cocycle construction in a changed target. It is not yet a `K_2`-valued cocycle.

For the precise ordinary lifting question, let `G` be the inverse image of `Q` in `C_2`. Then

`0 → C → G → Q → 0`

is an exact sequence of `Γ`-modules. The long exact group-cohomology sequence gives an obstruction

`δ[θ̄] ∈ H²(Γ,C)`.

An ordinary `G`-valued cocycle class lifting `[θ̄]` exists **if and only if** this obstruction vanishes. When it vanishes, the set of lift classes is a torsor under the image of `H¹(Γ,C)` in `H¹(Γ,G)`; the action need not be free on the whole `H¹(Γ,C)`. Since the geometric `Γ` action fixes constants, constant-valued cocycles can supply genuine ambiguity.

There is a logically earlier, different requirement if one insists that all lifted values already lie in `C_2^tf`: surjectivity of

`C_2^tf → Q`

has not been proved in the ramified-5 case. Taking fixed parts is not right exact. For a fixed monoid `M_β`, the obstruction to an invariant lift of a given element of `(C_2/C)^(M_β)` is the usual connecting class in

`Ext¹_(R[M_β])(R,C)`

from the exact sequence `0→C→C_2→C_2/C→0`. One must allow the exceptional element to enlarge for eventual invariance. Only after proving this invariant-lifting surjectivity can one substitute a short exact sequence with kernel `C^tf` and use `H²(Γ,C^tf)` for the trace-fixed cocycle-lifting problem.

## 8. What is still missing for the construction contract

1. A trace-fixed `η` for each required invariant degree-zero cycle, over exactly `R`, with the component, level, and CM compatibility needed by the source. Theorem A stops before the right-end degree map. The source's complete exact sequence uses `Z[1/30]` and cannot simply be invoked with new coefficients.
2. In the ramified-5 cases, a rigorous normalization or vanishing result for the constant-valued lifting obstruction, together with a compatible choice of lift. Theorem A does not make the constant ambiguity disappear from the intended target.
3. If evaluation at a torsion point is defined on a suitable open, a quotient-valued class specializes naturally only to `K_2(L′)⊗R / image(K_2(L)⊗R)`, not canonically to `K_2(L′)⊗R`. Adding a constant before evaluation changes its specialized value by that same constant. If `L′=L`, this quotient can erase the entire desired field target.
4. The original relative formula, CM/ray-field descent, auxiliary removal, absolute integrality, compactification, every level/character component, and the adopted bad-prime identities remain separate demands. None follows merely from this repaired left-exact complex.

**Sharp conclusion.** Quotienting the entire constant `K_2(L)` group before taking fixed parts genuinely repairs the first two nonzero terms for products of elliptic curves. It provides a canonical quotient cocycle once the residue input exists. It does not resolve the original constant-sensitive specialization problem. When 5 is unramified, full CM trace operators additionally restore the original left-exact complex over `Z[1/6]`; the unrestricted field ambition still includes ramified-5 fields, where the unmodified left kernel is nonzero.
