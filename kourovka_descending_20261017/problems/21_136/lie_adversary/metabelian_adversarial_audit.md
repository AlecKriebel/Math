# Adversarial audit of the metabelian P0 theorem

Checkpoint: 2026-10-24 17:28 UTC. Assigned subclass proof audit completion: **100%**. Full Problem 21.136 completion estimate: **10%**. Outcome: the precise partial theorem below survives this audit; no full resolution or originality claim.

Reviewed source: `strong_subclass/metabelian_locality.md`, authored by the independent child `strong_coset_subclass`. The reviewer had independently worked on the weak-condition obstruction and nilpotent subclasses before receiving the child's new metabelian mechanism. This is an AI mathematical audit, not human peer review or formal verification.

## Exact checked theorem

If a virtually metabelian pro-p group has P0 (every open subgroup contains an open coset of bounded exponent), then it has finite exponent and is locally finite. No finite generation, countable basis, finite rank or finite-dimensional representation hypothesis is used.

## Attempts to break the proof

1. **A not contained in later open H.** The argument keeps A=closed G' fixed. For every subgroup U open in G, A intersect U has finite index in A, so some p^r A lies inside it. Hence (A intersect U) tensor Q_p spans V=A tensor Q_p. This repairs the possible inheritance error: P0 is used only in open ambient subgroups, never in A or arbitrary closed subgroups.

2. **Torsion exponent may not be divisible by action exponent.** If the selected coset has exponent m and action exponent divides q, replace m by M=lcm(m,q). The same group identity holds at exponent M, and N_M(T)=(M/q)N_q(T). The nonzero scalar M/q is invertible over Q_p. Therefore N_q(T)=0 is justified.

3. **Noncentral A and power formula conventions.** For b in xU and a in A intersect U, both b and ba belong to xU. Expanding (ba)^M with A abelian produces the conjugation norm. Replacing T by T^(-1) only multiplies this norm by an invertible power of T, so left/right conjugation convention cannot change the vanishing assertion.

4. **Infinite-dimensional V.** Only the two operators T_x and T_u are diagonalized at a time. They commute and satisfy T_x^q=T_u^q=1, so generate a finite abelian group E (order at most q^2). Over Q_p(mu_q), its finitely many Fourier idempotents decompose an arbitrary vector space, regardless of dimension. No unproved decomposition for an infinite compact acting group is used. Extension of scalars is faithful.

5. **Exact character implication.** For each nonzero simultaneous character space with scalars xi,eta, norm vanishing for x u^i and every i gives xi eta^i≠1. If eta has exact order q, its cyclic group is all mu_q, which contains xi, contradiction. Thus every eigenvalue of T_u has order at most q/p. Since T_u is semisimple, T_u^(q/p)=1 on V. No assertion about intermediate non-p-divisors is needed, since q is a p-power.

6. **Iteration and exceptional q=1.** P0 is applied recursively inside open H_i. The action remains commuting, and its exponent drops one p-power at each step. At q=1 the final coset directly gives M Id_V=0. The case A=1 is harmless: B=G is already bounded-exponent abelian.

7. **Tensor zero versus bounded torsion.** Localization at p gives V=0 exactly when each individual element of A has finite p-power order. Baire then supplies a bounded-exponent open subgroup of the compact abelian group A; its finite quotient bounds the exponent of A. Uniformity is derived, not assumed from tensor zero.

8. **Local finiteness.** Every finitely generated abstract F≤G maps to a finite subgroup of bounded-exponent abelian B. Schreier makes F intersect A finitely generated. That subgroup is torsion abelian and hence finite. Thus F finite. For a finite extension, intersect F with the metabelian open subgroup and apply the same finite-index argument. This part does not require invoking the full Zelmanov compact torsion theorem.

9. **Boundary controls.** The earlier augmentation-module weak counterexample is metabelian but fails P0 inside A, so there is no conflict. Infinite elementary abelian compact groups satisfy P0 and are correctly allowed by the conclusion (bounded exponent and local finiteness, not finiteness). Infinite p-adic analytic groups cannot satisfy P0 because an open torsion-free subgroup contains no bounded-torsion open coset. All primes, including p=2, are covered.

10. **Attempted extension to arbitrary bounded-exponent quotient.** This is invalid without new input: the faithful two-dimensional Q8 representation has no eigenvalue 1 on the coset i<j>, while <j> still has exponent 4. Thus the abelian action hypothesis is mathematically essential to the presented drop lemma. The proof does not cover general solvable derived length≥3, nor arbitrary pro-p groups.

## Verdict

No substantive mathematical objection remains to the exact partial theorem after the above checks. The general Kourovka problem is not settled, and no novelty certification has been made. Any promotion beyond a research log should use a fresh reviewer and a dedicated priority audit.
