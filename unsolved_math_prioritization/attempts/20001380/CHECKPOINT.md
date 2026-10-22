# Single-root differents and a proposed ramification consequence

**Research checkpoint, not a reviewed result.** The full arboreal image remains unresolved. The zero basepoint is an explicit interpretation of AIM12.2; the literal source does not state it. Existing imported valuation and sign-quotient calculations are prior work. No novelty is asserted.

Let f(x)=x²+1, P_n=fⁿ, and choose a compatible branch α₀=0, f(α_n)=α_{n−1}. Set E_n=Q₂(α_n), and let L_n be the splitting field of P_n. Normalize v₂(2)=1.

## Exact monogenic calculation

Put ε_n=0 for even n and ε_n=1 for odd n. Modulo2,

P_n(x)=x^(2ⁿ)+(n mod2).

Consequently P_n(x+ε_n) reduces to x^(2ⁿ). Its constant term is fⁿ(0) for even n and fⁿ(1)=fⁿ⁺¹(0) for odd n. The critical orbit alternates between1 and2 modulo4, so this constant term has valuation one. The shifted polynomial is therefore Eisenstein. Thus E_n/Q₂ is totally ramified of degree2ⁿ, π_n=α_n−ε_n is a uniformizer, and its ring of integers is Z₂[π_n].

The monogenic different formula gives

d(E_n/Q₂)=v_{E_n}(P_n′(α_n)).

Since P_n′(α_n)=2ⁿ∏_{j=1}ⁿα_j, the Eisenstein uniformizers show v₂(α_j)=2^(−j) for even j and zero for odd j. Therefore, with m=⌊n/2⌋,

d(E_n/Q₂)=2ⁿ[n+(1−4^(−m))/3].

This is the different exponent of the **single-root field**, not the discriminant exponent of the full splitting field. Its first values are2,9,26,69.

## Proposed splitting-field consequence to audit

Let e_n=e(L_n/Q₂), d_n=d(L_n/Q₂), and let b_n be the largest upper ramification break. Transitivity of differents gives

d_n/e_n ≥ n+(1−4^(−m))/3.

For a finite Galois extension, Hilbert's different formula and the Herbrand change of variables give

d_n/e_n = 1−1/e_n + ∫₀^∞(1−1/|G_n^u|)du ≤ 1−1/e_n+b_n.

Hence

b_n ≥ n−1+(1−4^(−m))/3+1/e_n,

in particular b_n tends to infinity. Upper-numbering compatibility with quotients would imply that every upper ramification subgroup of Gal(∪L_n/Q₂) is nontrivial, and in fact infinite: a finite such subgroup would have a descending filtration that eventually becomes trivial, contradicting the unbounded finite-level breaks.

The standard ramification conventions and every displayed formula will be checked against primary references before freezing a publication candidate. This does not determine |Gal(L_n/Q₂)|, exact splitting-field breaks, or the full image in the binary-tree automorphism group.
