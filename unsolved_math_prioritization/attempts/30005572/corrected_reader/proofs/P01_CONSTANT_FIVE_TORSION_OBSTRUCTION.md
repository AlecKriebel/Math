# Constant 5-torsion obstruction to the unmodified trace-fixed complex

Authored verification, 14 October 2026. Scope: the current construction attempt, PASS 1 only. This is an obstruction to a particular integral construction method, not a counterexample to the requested Eisenstein map or to either cited paper.

## 1. Convention and conclusion

Let `R = Z[1/6]`. Let `F` be an imaginary quadratic field with full integer ring `O`, and let `A = E_1 ×_L E_2` be a product of elliptic curves over a number field `L`, with the `O`-actions defined over `L`. Write

`C_2 = K_2(L(A)) ⊗ R`,

`C_1 = (⊕_{D ∈ A^(1)} K_1(L(D))) ⊗ R`,

`C_0 = (⊕_{x ∈ A^(2)} Z) ⊗ R`.

Their differentials are the Gersten residues. For a module with trace operators `T_α = [α]_*`, define

`M^tf = ⋃_{0 ≠ β ∈ O} {z ∈ M : T_α z = z whenever (α) + (β) = O}`.

This is the definition of the trace-fixed part in Lecouturier–Sharifi–Shih–Wang §3.2, with `R` substituted for their explicitly specified `Z[1/30]`. This union is a filtered union: enlarging the exceptional element weakens the condition. It is not a quotient that can kill a previously nonzero element.

**Verified conclusion.** If `F = Q(√−5)` and `E_1 = E_2 = E` has CM by `O = Z[√−5]`, then

`ker(C_2^tf → C_1^tf)`

contains an injected copy of `K_2(L)[5]`, and this group is nonzero. Thus the leftmost injectivity assertion in the naive `Z[1/6]` version of the cited trace-fixed exact sequence is false.

The companion proof `CONSTANT_QUOTIENT_REPAIR.md` strengthens this: for products of two fixed elliptic curves the displayed kernel is exactly the trace-fixed constants; with full maximal CM it is `K_2(L)[5]` if 5 ramifies in `F`, and zero if 5 is unramified. The latter does not by itself establish right-end exactness at `C_0`.

## 2. A nonzero order-5 element exists over every number field

The standard number-field localization sequence is

`0 → K_2(O_L) → K_2(L) → ⊕_v k(v)^× → 0`,

where `v` runs through finite places. The two extra inputs in this short exact form are `K_2(k(v)) = 0` for finite fields and `SK_1(O_L) = 0`; the latter is the Bass–Milnor–Serre theorem. Garland's finiteness theorem says that `K_2(O_L)` is finite. Source details are recorded in `SOURCE_VERIFICATION.md`.

Choose any prime `v` of `O_L` above the rational prime 11. Its residue cardinality is `11^f` for an integer `f ≥ 1`, so `5 | (11^f − 1)`. The cyclic group `k(v)^×` has an element `t` of exact order 5. Put `t` in the `v`-component and 1 in all other multiplicatively written components, and lift this tuple to `y ∈ K_2(L)` by surjectivity.

Then `5y ∈ K_2(O_L)`, so `5hy = 0`, where `h = |K_2(O_L)|`. Consequently `y` has finite exact order `N`, divisible by 5. The element `x = (N/5)y` has exact order 5.

This argument does **not** claim that the final `x` has nontrivial residue at the chosen place: it may instead lie in the tame kernel. Only its nonzero order is used. No splitting of localization, no division inside `K_2(L)`, and no prime-distribution theorem are needed.

## 3. Constants inject into the function field

More generally, let `X/L` be a smooth integral surface with an `L`-rational point `e`. The local ring `O_{X,e}` injects into its completion (Krull intersection), and formal parameters give an isomorphism of `L`-algebras

`Ō_{X,e} ≅ L[[u,v]]`.

Passing to fraction fields and expanding first in `v` gives inclusions

`L(X) ↪ Frac(L[[u,v]]) ↪ L((u))((v))`.

For any field `k` and uniformizer `t`, Milnor residues define a homomorphism

`s_t : K_2^M(k((t))) → K_2^M(k)`,

`s_t(z) = ∂_t({t} · z)`,

using the convention `∂_t({t,a,b}) = {ā,b̄}` for units `a,b`. It need not be a ring map and need not be independent of `t`; neither property is required. Its composite with the inclusion of constants is the identity on `K_2^M(k)`.

Thus restriction to the iterated Laurent series field followed by `s_v` and `s_u` is a left inverse to

`K_2^M(L) → K_2^M(L(X))`.

Matsumoto's theorem identifies these degree-two Milnor groups naturally with the Quillen `K_2` groups used in the Gersten complex. The constant inclusion on `K_2` is therefore split injective. For `A`, use the rational origin as `e`. Localization at 6 preserves this split injection and preserves every nonzero element of order 5.

## 4. Constants are unramified and their trace is the degree

Every constant `a ∈ L^×` is a unit in `O_{A,D}` for every divisor `D` on `A`. The tame residue of a symbol `{a,b}` with both entries constant is trivial. Such symbols generate `K_2(L)`, so the whole constant subgroup lies in `ker(C_2 → C_1)`.

The endomorphism `[α] : A → A` is a finite étale `L`-isogeny in characteristic zero. On each elliptic factor its degree is `N_{F/Q}(α)`, hence on `A` its degree is `N(α)^2`. Restriction followed by the field transfer is multiplication by this degree. Since `[α]^*` fixes constants,

`T_α(x_A) = N(α)^2 x_A`.

This is the ordinary transfer–restriction formula, equivalently the projection formula applied to the unit in `K_0`.

## 5. Full CM invariance when 5 ramifies

For `O = Z[√−5]`, write `α = a + b√−5`. Being prime to `(5)` is equivalent to `a ≠ 0 mod 5`, and

`N(α)^2 = (a² + 5b²)² ≡ a⁴ ≡ 1 mod 5`.

It follows that **every** `x ∈ K_2(L)[5]` is fixed by **every** `T_α` with `α` prime to `(5)`. The exceptional element `β = 5` is allowed in the exact definition above. This verifies full CM trace invariance, rather than merely invariance under rational integer multiplication.

Since the constant map is injective and `x` has order 5, its image is nonzero in `C_2^tf`. Section 4 gives zero residue. This proves the obstruction.

The same conclusion holds for any imaginary quadratic maximal order in which 5 ramifies. Indeed, `O/(5)` is the dual-number algebra `F_5[ε]/(ε²)`, and the norm of a unit `a+bε` is `a²` modulo 5.

## 6. Sharp constant-part distinction

For any nonzero exceptional element `β`, rational integers coprime to some integer `n` are prime to `β`. On constants their traces are multiplication by `m⁴`.

The ideal of `R` generated by `m⁴−1` for `(m,n)=1` contains 5 and is either `R` or `(5)`. To check this, no prime `q ≥ 7` divides every generator: choose, by the Chinese remainder theorem, an integer prime to `n` whose nonzero residue modulo `q` is not a fourth root of unity. Likewise choose `m ≡ 2 mod 25` and prime to `n` to see that the 5-adic valuation of the gcd is at most one. If `5 ∤ n`, one can also choose `m ≡ 0 mod 5`. The primes 2 and 3 are units in `R`.

Thus every eventually scalar-trace-fixed constant in `K_2(L) ⊗ R` is killed by 5. Its constant full-CM-fixed subgroup is therefore a subgroup of `K_2(L)[5]`.

If 5 is unramified in `F`, the norm map

`(O/(5))^× → F_5^×`

is surjective: in the split case it is `(a,b) ↦ ab`, and in the inert case it is the finite-field norm `F_25^× → F_5^×`. Choose a residue class of norm 2 and use CRT to lift it to `α ∈ O` prime to any prescribed `β`. Then `N(α)^2 ≡ 4 ≡ −1 mod 5`. A constant of order dividing 5 fixed by this trace must be zero.

Consequently

`(K_2(L) ⊗ R)^tf = K_2(L)[5]` if 5 ramifies in `F`,

`(K_2(L) ⊗ R)^tf = 0` if 5 is unramified in `F`.

These statements use the maximal order. They are not assertions about arbitrary nonmaximal CM orders with conductor divisible by 5.

## 7. Scope boundary

Sharifi–Venkatesh use `Z[1/(2g+1)!]` in Theorem 6.1.1 and Proposition 6.1.2, and explicitly use `Z[1/30]` in Lemma 6.2.1. Lecouturier–Sharifi–Shih–Wang retain `Z[1/30]` in §3.2. The order-5 classes here disappear with those coefficients, so there is no contradiction with those results.

This proof does not give a negative answer to the frozen construction contract. It identifies a genuine choice/normalization obstruction to one naive replacement of coefficients and motivates the precisely stated quotient repair in the companion note.
