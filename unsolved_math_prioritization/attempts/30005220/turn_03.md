# Attempt 3: Modular multiplicities and an exact obstruction to a naive proof

For a character Ψ of a p-group P, define L_i(Ψ) as the sum, with multiplicity, of the linear constituents of order exactly p^i; set s_i(Ψ)=L_i(Ψ)(1). Nonlinear constituents have degree divisible by p. Thus Ψ(1) prime to p implies at least one s_i is nonzero modulo p, but gives no information about which i is largest.

## A sufficient condition

Suppose χ∈Irr(G) has conductor p^a m with a≥2 and p∤m. If s_a(χ_P) is not divisible by p, then the target conjecture holds.

Proof. Let E=Q(χ_P), E⊆Q_(p^a). Let S be a Sylow p-subgroup of Gal(Q_(p^a)/E). Extend S to the p-primary cyclotomic field containing all values of Irr(P): a Sylow p-subgroup of the inverse-image group maps onto S. This extension fixes χ_P and permutes its order-p^a linear constituents, preserving multiplicities. Nonfixed orbits have p-divisible weighted cardinality. Since s_a is prime to p, there is a constituent fixed by the whole lifted p-group. Its values generate Q_(p^a), forcing S to be trivial. ∎

This is the local mechanism behind the Isaacs–Navarro invariant. The hard missing statement is that the top global conductor level is detected by a nonzero-mod-p count of these linear constituents. It is Question 5.3 in Hung's 2026 survey, stronger than the target conjecture.

## Exact obstruction when irreducibility is omitted

Fix any prime p and a prime q>p. Let G=C_(p^2)×C_q, with generators x,y. Choose linear characters λ(x)=ζ_(p^2), μ(y)=ζ_q, and define the ordinary, reducible character

Ψ=1+Σ_(j=0)^(p−1) λ^(1+pj) μ^j.

Its degree is p+1, prime to p. On P=〈x〉,

Ψ(x^k)=1+ζ_(p^2)^k Σ_(j=0)^(p−1) ζ_p^(jk).

This equals 1 when p∤k, and equals 1+pζ_p^t when k=pt. Thus Q(Ψ_P)=Q_p (equal to Q for p=2).

In contrast, Q(Ψ)=Q_(p^2 q). Indeed a cyclotomic automorphism fixing Ψ must permute its distinct linear constituents. The unique nontrivial constituent with trivial C_q component is λ; hence the automorphism is 1 modulo p^2. The p constituents have distinct C_(p^2) components, so each is now individually fixed. The j=1 constituent then forces the automorphism to be 1 modulo q. Its stabilizer is trivial.

Therefore c(Ψ)=p^2 q and

[Q_(p^2):Q(Ψ_P)]=p.

This is NOT a counterexample to the actual problem: Ψ has p+1 distinct linear constituents and inner product 〈Ψ,Ψ〉=p+1>1. It demonstrates exactly why ordinary-character positivity, p′-degree, and local orbit counting alone are insufficient. The local top-order count is s_2=p, which vanishes modulo p, while s_0=1.

## Binary warning

For p=2 the character 1+λ+λ^(-1) of C_8 has odd degree 3 and field Q(√2). Its global and local conductors both equal 8, yet its index in Q_8 is 2. Thus a proof that only preserves the conductor level would still leave the i-inclusion issue at p=2.

The standard-library verifier checks this family exactly at p=2,3,5,7,11, using Galois actions on exponent multiplicities, and explicitly verifies reducibility.

Status: sufficient criterion proved and false shortcuts ruled out. No original irreducible counterexample and no full proof.
