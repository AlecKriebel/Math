# A ramification restriction for the original weak almost-rational condition

**Target:** 30001149 / OWR-3388-008. **Status:** accepted scoped partial theorem after independent AI mathematical audit, not a classification. Written 2026-10-10 UTC. The known strong orbit-field classification is credited and is not assumed below.

## 1. Exact assumptions and claim

Let k be algebraically closed of characteristic 2, and let σ be a k-automorphism of k[[t]] of exact order 2^n, n≥2. Suppose σ(t) belongs to an Artin–Schreier extension E₀/k(t) of degree 2 contained in k((t)), as in Definition 1 of Chinburg's 2009 report. Define

b₀ = v_t(σ(t)−t)−1,   b₁ = v_t(σ²(t)−t)−1.

**Theorem.** Necessarily

(b₀,b₁) ∈ {(1,3),(1,5)}.

This does not assert that the second pair occurs under the weak hypothesis. It does not bound n by 2, establish σ-stability of k(t,σ(t)), or classify any still-possible conjugacy classes.

## 2. The minimal relation has bidegree (2,2)

Put t_i=σ^i(t), with indices modulo N=2^n. Each t_i is algebraic over k(t): apply σ repeatedly to the algebraic relation for t₁ over k(t₀), and use transitivity of algebraicity. Consequently

L=k(t₀,t₁,…,t_{N−1})

is a finite extension of k(t₀), stable under σ. In particular,

[L:k(t₀)] = [L:k(t₁)].

We have t₁∉k(t₀). Indeed if t₁=R(t₀) is rational, the identity R^{∘N}(t)=t forces deg(R)=1, so R is a Möbius map. A nontrivial finite 2-power-order Möbius map in characteristic 2 has order 2: its two eigenvalue ratio is either a root of unity, whose order is odd, or it is a nontrivial unipotent projective transformation, whose square is the identity. This contradicts N≥4.

Thus E=k(t₀,t₁)=E₀ and [E:k(t₀)]=2. The tower law inside L gives [E:k(t₁)]=2 as well. Let P(X,Y)∈k[X,Y] be the irreducible polynomial, unique up to nonzero scalar, cutting out the affine image of t↦(t,σ(t)). Its degrees in X and Y are each 2. Its bihomogenization defines an integral curve C⊂P¹×P¹ of class (2,2), with function field E. No action of σ on C or E has been used or asserted.

The equality of the two degrees is the usual degree-equals-height argument; over finite fields it is explicitly recorded in Byszewski et al., Proposition 9.2.1. Its proof applies unchanged here.

## 3. The curve and its transpose are distinct

Let Cᵀ be the transpose curve P(Y,X)=0. The formal graph Y=σ⁻¹(X) is a branch of Cᵀ at (0,0), since substituting σ⁻¹(t) into P(t,σ(t))=0 gives P(σ⁻¹(t),t)=0.

First observe

v_t(σ(t)−σ⁻¹(t)) = v_t(σ²(t)−t) = b₁+1.       (1)

Indeed substitution by σ preserves t-adic valuation and sends the expression on the left to σ²(t)−t.

Suppose C=Cᵀ. Then both σ(t) and σ⁻¹(t) are roots of the quadratic P(t,Y). They are distinct, because equality would imply σ²(t)=t. Write

P(t,Y)=A(t)Y²+B(t)Y+D(t),

where A≠0 and deg A, deg B≤2. This quadratic is separable: E/k(t) is Artin–Schreier, so B≠0. The root-sum formula in characteristic 2 now gives

σ(t)+σ⁻¹(t)=B(t)/A(t).

Its valuation is at most 2, since v_t(B)≤deg B≤2 and v_t(A)≥0. On the other hand, ramification theory gives b₀≥1 and b₁≥3b₀, so (1) has valuation at least 4. Contradiction. Therefore C and Cᵀ are distinct integral curves, so they have no common component.

## 4. Intersection of the selected formal branches

On the smooth surface P¹×P¹, the intersection number of C and Cᵀ is

(2,2)·(2,2)=2·2+2·2=8.

All local intersection multiplicities are nonnegative, so their local intersection multiplicity at (0,0) is at most 8.

This local intersection is at least the intersection multiplicity of the two selected graph branches Y=σ(X) and Y=σ⁻¹(X). To see the inequality without assuming that C is smooth at (0,0), work in k[[X,Y]]. Formal division by the monic linear polynomial Y−σ(X) shows that it divides P(X,Y); likewise Y−σ⁻¹(X) divides P(Y,X). Local intersection multiplicity of two reduced plane curves without common components is additive over their formal branches, and all branch contributions are nonnegative. The chosen contribution equals

length k[[X,Y]]/(Y−σ(X),Y−σ⁻¹(X))
 = length k[[X]]/(σ(X)−σ⁻¹(X))
 = b₁+1.

The two selected factors are distinct by N≥4. Consequently

b₁+1≤8,   hence b₁≤7.                         (2)

Equivalently one may compute the local intersection after normalization and sum the orders of the transverse equation. This is only an intersection argument about the graph correspondence; it never makes σ an automorphism of its pair curve.

## 5. Ramification arithmetic

For a finite cyclic 2-power action over an algebraically closed field of characteristic 2, the first upper break is u₀=b₀ and the second is

u₁=(b₁+b₀)/2.

Here b₀ is positive and odd, u₁≥2b₀, and if u₁>2b₀ then u₁ is odd. These are the standard cyclic equal-characteristic ramification conditions, recalled in Bleher–Chinburg–Poonen–Symonds, §3.D. In particular b₁≥3b₀.

Together with (2), this gives b₀≤7/3. Since b₀ is positive odd, b₀=1. Then b₁ is odd, 3≤b₁≤7, so b₁∈{3,5,7}. The value 7 would give u₁=4>2u₀ with u₁ even, forbidden by the stated ramification condition. The only possibilities are therefore (1,3) and (1,5), as claimed.

## 6. What remains

The original question quantifies over every prime and all orders p^n>p. The theorem above addresses only characteristic 2 and only the first two ramification breaks. It leaves the (1,5) possibility, all higher-order possibilities consistent with these initial breaks, and all odd-characteristic cases open. In particular, it is not legitimate to apply the later whole-orbit theorem to E without proving that L=E.

## Primary sources

- Ted Chinburg, joint-work contribution in *The Arithmetic of Fields*, Oberwolfach Report 05/2009, pp.325–327. Definition 1 and the final question on pp.326–327. https://doi.org/10.4171/owr/2009/05
- Frauke M. Bleher, Ted Chinburg, Bjorn Poonen, Peter Symonds, *Automorphisms of Harbater–Katz–Gabber curves*, DOI 10.1007/s00208-016-1490-2. Definition 1.1/Theorem 1.2 distinguish the strong condition; §3.D supplies the ramification conditions used here. Author manuscript: https://math.mit.edu/~poonen/papers/AutK.pdf
- Jakub Byszewski et al., *Automata and finite order elements in the Nottingham group*, Journal of Algebra 602 (2022), 484–554, DOI 10.1016/j.jalgebra.2022.03.019, Proposition 9.2.1 (degree equals height). Institutional primary copy: https://research-portal.uu.nl/ws/files/149368215/1_s2.0_S002186932200134X_main.pdf

The equal-degree observation and standard intersection/ramification tools are credited; no global novelty certification is asserted for this partial consequence.
