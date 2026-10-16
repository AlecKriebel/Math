# Independent checkable operator-algebra derivation

Audit input: PR 742, problem 30005356, reported frozen head `77be9cbd8b58358919f42c204d9dd829ccd5d60f`. The proof below was reconstructed independently after reading the governing proof, without reading old audit material or code. It proves a negative universal statement, not an endomorphism classification.

## A. Abstract scalar obstruction

Let K be an algebraically closed field of characteristic p>0, and let G=K×. Let E be the ring of definable group endomorphisms of G. The same algebra works in the ring of all group endomorphisms. Write its operations as

    (f+g)(x)=f(x)g(x),       (fg)(x)=f(g(x)).

The ring zero is x↦1. Its identity is x↦x. Its integer scalar [n] is x↦xⁿ for every n∈Z. For negative n, this notation uses the ordinary group inverse; no inverse operator θ is involved. Every group homomorphism f obeys f(xⁿ)=f(x)ⁿ, including n<0, so [n] is central in E.

E has characteristic zero, even though K has characteristic p. Indeed, for n≠0, the nonzero polynomial T^|n|−1 has finitely many roots, while K is infinite. Some x∈K× therefore has xⁿ≠1, so [n] is not the ring zero. This also rules out the tempting reduction of integer coefficients modulo p. In characteristic two, for example, [-1] is still distinct from [1] on K×.

The scalar [p] is bijective: algebraic closedness gives existence of p-th roots, and (u−v)^p=u^p−v^p gives uniqueness. Its inverse ρ is defined by the parameter-free formula y^p=x. If a,b∈K, the equalities

    (ρ(a)ρ(b))^p=ab,       (ρ(a)+ρ(b))^p=a+b

prove multiplicativity and additivity by uniqueness. Thus ρ is a field automorphism; its restriction to G belongs to E. Since the inverse of a central unit is central, ρ commutes with every group endomorphism of G, not just θ. At zero this commutation persists whenever θ(0)=0.

Now suppose θ∈E and evaluation Φ:Z[X]→E, X↦θ, is injective. If ρ=Φ(P), then

    0_E=[p]ρ−Id=Φ(pP−1).

Injectivity would force pP−1=0 in Z[X]. Its constant coefficient is pa₀−1≡−1 (mod p), which is nonzero. Hence ρ∉Z[θ]. This uses no classification of definable maps, no assumption that θ preserves addition, and no assumption that θ is injective.

The other scalar units are exactly [±p^r] for integers r≥0. These are bijective by Frobenius and inversion. If n≠0 has a prime factor ℓ≠p, separability of T^ℓ−1 gives a nontrivial ℓ-th root of unity, killed by [n], so [n] is not injective. Scalar inversion therefore forces Z[1/p], not all rational coefficients. This conclusion is independent of genericity.

## B. Direct existential witness, avoiding any quoted faithfulness theorem

Assume now that (K,θ) is existentially closed among algebraically closed fields equipped with an arbitrary multiplicative group endomorphism, extended by θ(0)=0. Fix an integral polynomial P(X)=∑ᵢ₌₀ᵈ aᵢXⁱ. Suppose for contradiction that P(θ)=ρ on K×.

Adjoin algebraically independent t₀,…,t_d over K, and let L be an algebraic closure of K(t₀,…,t_d). On the subgroup

    H=K×⟨t₀,…,t_(d−1)⟩⊆L×

define h(c∏tᵢ^mᵢ)=θ(c)∏t_(i+1)^mᵢ. For d=0 use H=K×. Laurent monomial independence makes each displayed representation unique, so h is a well-defined homomorphism extending θ.

Here is the group-theoretic extension step in full. A homomorphism h:B→D, with B⊆A abelian and D divisible, admits a maximal extension by Zorn's lemma. If a is outside its domain B, the integers k with a^k∈B form either {0} or nZ for a positive n. In the first case choose any d∈D. In the second choose d∈D with d^n=h(a^n). The rule h(ba^k)=h(b)d^k is well-defined, because any two representations differ by a relation with k in the displayed subgroup, and the chosen root enforces that relation. It contradicts maximality unless the domain is all A. Apply this with A=L× and D=L×, divisible because L is algebraically closed. This yields θ_L extending θ, with θ_Lⁱ(t₀)=tᵢ for 0≤i≤d. It need not be additive, injective, or surjective; the base theory requires none of these.

In the extension, the equation P(θ_L)(t₀)^p=t₀ would be the Laurent relation

    t₀^(pa₀−1) ∏ᵢ₌₁ᵈ tᵢ^(paᵢ)=1.

Its t₀ exponent is nonzero. Algebraic independence rules out the relation in every characteristic: multiplying by a Laurent monomial to clear negative exponents produces two distinct monomials in a polynomial, even if p=2. Thus the existential assertion

    ∃x (x≠0 ∧ P(θ)(x)^p≠x)

holds in the base-theory extension and hence, by existential closedness, already in K. It contradicts the assumed identity P(θ)=ρ. Degree zero, zero coefficients, and arbitrary negative coefficients are included.

The identical construction with any nonzero Q(X)=∑bᵢXⁱ instead supplies the witness ∏tᵢ^bᵢ≠1 and proves Φ injective. Neither witness requires saturation, existential closedness among only ACFH extensions, or an injective extension of θ. A base-theory extension suffices.

## C. The localization inclusion, with its exact limit

For each finite denominator p^r define

    Ψ(P/p^r)=ρ^r P(θ).

This is a definable endomorphism because it is a finite composition/product of definable maps. It is well-defined: equal fractions yield an integral polynomial equality after multiplication by a common p-power, and that p-power is an invertible central operator. The same centrality proves addition and composition correspond to fraction addition and multiplication. Its image is the subring generated by Z[θ] and ρ.

If Ψ(P/p^r)=0_E, multiply by [p^r] to obtain P(θ)=0_E. Faithfulness from B gives P=0. Thus

    Z[1/p][X] ≅ Z[1/p][θ] ⊆ E,
    Z[θ] ⊊ Z[1/p][θ].

This is an inclusion. It leaves open whether E has further operators. In characteristic zero, root equations y^n=x have n distinct solutions for n>1, so this unique-root construction does not supply scalar inverses or a counterexample there.

## D. Definable functions versus rational or regular maps

The graph y^p=x is a quantifier-free algebraic relation with exactly one output y for each x. That is enough for first-order definability; a language term or a regular morphism is not required.

ρ cannot be a rational function on K×. If a rational function r(T) equaled ρ on every nonzero K-point, infinitude would imply the rational identity r(T)^p=T. The order at T=0 of the left side would be p times an integer, while the right side has order one. This is impossible. Hence ρ is not a regular morphism either. Its regularity failure does not disqualify it from a ring explicitly defined using first-order definability.

## E. Counterexamples to overgeneralization

Genericity-free existence and centrality of ρ do not imply genericity-free nonmembership. On the base-theory model (F_p^alg,θ=ρ), one has ρ=θ∈Z[θ] and (pX−1)(θ)=0. This supplies an infinite algebraically closed counterexample to dropping faithfulness/existential closedness.

On GF(p^r), inverse Frobenius is the integral power x↦x^(p^(r−1)), since x^(p^r)=x. A finite-field experiment therefore cannot establish the proposed nonmembership. `controls.py` intentionally checks these contrary finite examples, as well as centrality under powers, negative exponents, and nonadditive/noninjective choices of θ. These tests are neither ACFH simulations nor substitutes for B.
