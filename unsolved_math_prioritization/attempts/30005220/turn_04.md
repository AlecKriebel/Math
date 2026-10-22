# Attempt 4: Mackey induction and the monomial case

This route reconstructs the induction mechanism used in Isaacs–Navarro (2024) and Hung–Schaeffer Fry (2026), Lemmas 4.2–4.3. It explains precisely what induction does preserve and why that does not settle arbitrary irreducible characters.

Use the order-based numbers s_i of Attempt 3. For i≥2 they agree modulo p with the degree of the level-i part Δ_i used in those references: a nonlinear constituent has p-divisible degree, and a linear character of order p^i has conductor p^i at these levels.

## Lemma 1: proper p-subgroup induction

Let H<P be a proper subgroup of a finite p-group and let θ be an ordinary character of H. For every i≥2,

s_i(Ind_H^P θ)≡0 (mod p).

Proof. By Frobenius reciprocity, a linear character λ of P contributes according to the multiplicity of λ_H in θ. For each linear constituent η of θ, its extensions to P either do not exist or form a coset λ_0 A, where A is the group of linear characters of P trivial on H. Here A is dual to P/(HP′) and is a nontrivial p-group. Indeed HP′=P would imply HΦ(P)=P and then H=P, a contradiction.

For any j≥1, the intersection of λ_0 A with the subgroup of characters of order dividing p^j is empty or a coset of A[p^j]. In either event its cardinality is divisible by p. The number of extensions of order exactly p^i is the difference of the counts for j=i and j=i−1, hence divisible by p for i≥2. Weight by the multiplicity of η and sum. ∎

The exclusion of i=1 is necessary: inducing 1 from the trivial subgroup of C_p gives 1 trivial and p−1 order-p constituents.

## Lemma 2: p′-index induction

Let P≤K≤G, P∈Syl_p(G), and Ψ=Ind_K^G ψ for an ordinary character ψ. Then, for each i≥2,

s_i(Ψ_P)≡[N_G(P):N_K(P)]s_i(ψ_P) (mod p).

Proof. Apply Mackey's formula. Terms induced from proper subgroups of P contribute 0 modulo p by Lemma 1. The remaining terms correspond to P-fixed cosets in G/K. Such cosets are represented by N_G(P)/N_K(P), by Sylow conjugacy within K. Each remaining term is ψ_P twisted by an automorphism of P, so it has the same order-i multiplicity count. The normalizer index is prime to p. ∎

## Corollary: p′-degree monomial characters

Let χ=Ind_K^G λ be irreducible, λ linear, and p∤χ(1). Then the conjecture holds for χ.

Proof. Since [G:K]=χ(1) is prime to p, conjugate K so that it contains P. Let λ_P have order p^b. If b≤1, induction shows c(χ)_p≤p and the target is automatic. Assume b≥2. Lemma 2 gives s_b(χ_P)≡[N_G(P):N_K(P)]≠0 (mod p).

We claim that the p-part p^a of c(χ) has a≥b. If a<b, χ_P has values in Q_(p^a). Lift Gal(Q_(p^e)/Q_(p^max(a,1))) to a cyclotomic field containing the constituents of χ_P, where exp(P)=p^e. This is a p-group and has no fixed order-p^b linear character. Therefore it partitions such constituents into p-divisible orbits with constant multiplicity, giving s_b≡0, a contradiction. On the other hand c(χ) divides c(λ) by the induction formula, and c(λ)_p=p^b. Hence a=b. Apply the sufficient criterion from Attempt 3. ∎

This proof works for a monomial χ of arbitrary p′-degree, even if G itself is not p-solvable. It is a direct consequence of the published induction lemmas; no novelty claim is made. Hung–Schaeffer Fry use the prime-index instance in their Theorem 4.4 as part of their established result for prime-degree characters.

## Why general induction does not close

For χ=Ind_K^G ψ with ψ nonlinear, one obtains preservation of the nonzero-mod-p high-level multiplicity pattern. One does not automatically know that its highest index equals the conductor level of ψ. The unproved equality is exactly the stronger condition isolated in Attempt 3. Nor does ordinary irreducible induction cover primitive characters. Calling the induction lemma a complete reduction to known p-solvable cases would therefore be incorrect.

Status: complete special case and exact induction congruence, both within existing theory; no full resolution.
