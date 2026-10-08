# The source-level comparison problem

Problem 30001285 / OWR-3481-002, queue rank 972. Scope checked 2026-10-07.

The primary source is Bruno Kahn's contribution, pp. 1754–1755 of *Algebraic K-Theory and Motivic Cohomology*, Oberwolfach Reports 31/2009, DOI [10.4171/OWR/2009/31](https://doi.org/10.4171/OWR/2009/31). It asks to compare constructions; it does not assert that three already identically normalized homomorphisms must always agree.

## Hypotheses and notation

In that contribution, F is a field and A is a central division F-algebra of degree d prime to char(F). Let [A] be its Brauer class. For i=1,2, SK_i(A) is the kernel of the reduced norm K_i(A)→K_i(F). Passage from a central simple algebra to its division representative is by Morita invariance. Degree-dependent varieties and coefficients must still be named explicitly; Morita invariance does not identify every generalized Severi–Brauer variety.

Write

    B_1(F)=H^4(F,Q/Z(3)),       D_{1,r}(F)=r[A] cup K_2^M(F),
    B_2(F)=H^5(F,Q/Z(4)),       D_{2,r}(F)=r[A] cup K_3^M(F),
    Q_{i,r}(F)=B_i(F)/D_{i,r}(F).

In positive characteristic only the prime-to-characteristic coefficient part used by the cited constructions is intended. The concrete negative example below has characteristic zero. The integral étale-motivic descriptions are B_1=H_et^5(F,Z(3)) and B_2=H_et^6(F,Z(4)). The shift of one is important. The denominators in the report are r[A]H_et^2(F,Z(2)) and r[A]H_et^3(F,Z(3)); these identify with the displayed Milnor K-products. The Brauer class lies in H_et^3(F,Z(1)), not H_et^2(F,Z(1)). These conventions are checked directly in Kahn–Levine §6.9 and Kahn's 2010 introduction.

For all SK_2 comparisons in this packet, retain the report's extra hypothesis that F contains an algebraically closed subfield. The later papers can use a separably closed subfield, but that enlargement is unnecessary here. In particular, the Q_5 Laurent-series example is only an SK_1 example.

## The maps being compared

* beta_i: SK_i(A)→Q_{i,1}(F) denotes Kahn–Levine's étale Bloch–Lichtenbaum spectral-sequence invariant.
* sigma_r^i: SK_i(A)→Q_{i,r}(F) denotes Kahn's generalized Severi–Brauer construction, with r dividing d. The clean prime-power formulation and finite-coefficient refinements are in Kahn's Theorems A and B, §§7.B–7.D.
* c_A: SK_1(A_L)→B_1(L), natural for extensions L/F of the fixed base algebra A, denotes the normalized field-valued SL_1 invariant of Kahn's Theorem C and §10. For d>2, it is obtained from the positive reduced étale-motivic generator and evaluation. For the division degrees d=1 or d=2, define c_A=0: every ind(A_L) divides d and is square-free, so SK_1(A_L)=0 by Wang's theorem (Kahn, introduction, Theorem 1). The positive-generator description is not invoked in these low degrees; Kahn §10.A explicitly assumes deg(A)>2 for that construction.

The third construction above is explicitly an SK_1 invariant. The report's displayed formula involving H_et^5(SL_1(A),Z(3)) does not, by itself, define a third SK_2 invariant. We do not invent one.

Although the report labels the SL_1 target by r=d, c_A is **not** sigma_d^1. Indeed SB(d,A) is a point and the geometric map sigma_d^i is zero (Kahn Lemma 7.6); c_A can be nonzero.

## Equality requires a comparison map

Let q_r:B_i→Q_{i,r}. If s divides r then D_{i,r}⊆D_{i,s}, giving a natural projection Q_{i,r}→Q_{i,s}. These arrows alone do not identify the constructed invariants.

One precise, but false in general, candidate would be

    beta_1 = sigma_1^1 = q_1 c_A.

Another comparison uses multiplication in the opposite direction: if e kills D_{i,r}, the map mu_e:Q_{i,r}→B_i sends b+D_{i,r} to eb. It is not the quotient projection and is not usually its inverse. Finite-coefficient reduction maps also require their own normalization. Confusing these arrows changes the mathematical assertion.

## Literature-based disposition

Wouters gives a negative example for projection lifting, whereas Kahn proves c_A=sigma_2^1 when exp(A)=2<ind(A). Neither fact identifies beta_1 with sigma_1^1 in general. The packet reconstructs the negative example and proves further scoped comparison criteria. It does not solve the original general comparison problem, classify all equality cases, prove injectivity of the general invariants, or produce a new solution of Suslin's conjecture.

The current literature check found no theorem settling the full source-level request. This is a bounded search conclusion, not proof that no such theorem exists. Sources and versions are identified in SOURCES.json and LITERATURE.md. COEFFICIENTS.md fixes the finite, integral and Q/Z arrows. The product/residue reduction in approach 5 is explicitly conditional on a common normalization; it is not asserted as an established beta-versus-sigma comparison.
