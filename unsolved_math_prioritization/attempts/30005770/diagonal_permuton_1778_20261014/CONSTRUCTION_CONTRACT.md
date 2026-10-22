# Diagonal permuton limit target and acceptance contract

Source-scope review dated 14 October 2026. Target identifier: 30005770 / OWR-14298158-015. This contract fixes the statement to be assessed and the scope of the cited results. It does not certify a proof, a disproof, novelty, or literature-exhaustive openness.

## Frozen target

Fix an integer m >= 1 and a permutation alpha in S_m, independently of n. Define tau = alpha skew-sum 1 by tau(i) = alpha(i) + 1 for 1 <= i <= m and tau(m+1) = 1. Avoidance means classical subsequence-pattern avoidance. For every positive integer n, let Pi_n have exactly the uniform distribution on Av_n(tau).

For pi in S_n, use the permuton with density n on the n squares

Q_i = [(i-1)/n, i/n] x [(pi(i)-1)/n, pi(i)/n],  1 <= i <= n,

and density zero elsewhere. Each square has mass 1/n; shared boundaries have zero area. Thus mu_pi(E) = n sum_i area(E intersect Q_i). The target limit is mu_I = Law(U,U), where U is uniform on [0,1].

The assertion is that, for every fixed nonempty alpha, mu_{Pi_n} converges in distribution as a random element of the space of probability measures on [0,1]^2 with its weak topology to the deterministic mu_I. Equivalently, for every epsilon > 0,

P(d_BL(mu_{Pi_n}, mu_I) > epsilon) tends to 0 as n tends to infinity,

where d_BL(mu,nu) = sup {|integral f dmu - integral f dnu| : ||f||_infinity <= 1 and Lip(f) <= 1}, using the Euclidean metric on the square. This is weak convergence in probability. No rate uniform over alpha, growing pattern alpha_n, independence across n, or almost-sure coupling is included. Existence and identification of the limit are both part of the assertion.

The original conjecture is on printed p.298 (PDF p.26) of Troyka's contribution, joint with Bevan; the uniform-class model is explicit on printed p.281 (PDF p.9) of Bevan's contribution. [OWR report](https://ems.press/content/serial-article-files/48646?nt=1#page=26)

## Exact credited partial coverage

Write I_k for the increasing pattern of length k, J_k for the decreasing pattern, and use the empty middle block when b = 0. Hohmeier and Slivken, arXiv:2502.19541v3, Theorem 1.1 (p.3), assert the anti-diagonal limit Law(U,1-U) for the uniform class avoiding

J_a direct-sum I_b direct-sum J_c,  a,c >= 1, b >= 0,

with parameters fixed and convergence in distribution in the weak topology. Complementing the permutation is a bijection of the corresponding finite avoidance classes and reflects the limit. Consequently, their theorem gives the diagonal limit for avoidance of I_a skew-sum J_b skew-sum I_c. This symmetry translation is credited interpretation, not a new limit theorem. [Theorem 1.1](https://arxiv.org/pdf/2502.19541v3#page=3)

Setting c = 1 yields exactly the directly applicable subfamily

alpha = I_a skew-sum J_b,  a >= 1, b >= 0.

This includes all increasing or decreasing alpha, and in particular alpha = 1, 12, 21, 123, 231, 321. It does not justify replacing alpha by an arbitrary permutation. This is an exact description of this displayed theorem's direct target subfamily, not a complete catalog of all known cases from all sources. A Wilf-equivalence count alone does not identify the permuton law.

The same v3 manuscript, Section 6 (p.12), treats the anti-diagonal limits for 1342 and 1324 as conjectural. Reversing 1342 gives 2431 = 132 skew-sum 1, an explicit target case not resolved by that assertion. The paper's discussion of 2413 concerns a different pattern type and supplies no target counterexample. [Section 6](https://arxiv.org/pdf/2502.19541v3#page=12)

## Chronology to preserve

The July 2023 conference booklet, p.123, announced an anti-diagonal result for uniform 1342 avoiders; Bevan's problem slide 1 correspondingly credited a 2431 result. Both are genuine historical records. The later Hohmeier-Slivken v3 manuscript instead reports that their 1342 investigation had not established a limit and presents the proposed limit as conjectural. The 2023 announcement must therefore not be used alone to certify that case as solved. No reason for the discrepancy or formal withdrawal is inferred. [Conference abstract](https://2023.permutationpatterns.com/booklet/bookletco.pdf#page=123), [Bevan slide](https://2023.permutationpatterns.com/p/problem_session/bevan_scalinglimitproblem.pdf#page=1)

The arXiv record checked on 14 October 2026 identifies v3, dated 24 February 2026, as the latest version, after v1 on 26 February 2025 and v2 on 20 November 2025. This is a version pin, not a publication or correctness certificate. [Version history](https://arxiv.org/abs/2502.19541)

## Acceptance cautions

1. A positive resolution must prove the frozen universal statement for the exact uniform finite-class law. A restricted family is partial progress. A limit conditional on its existence is insufficient. If a bijection or random generator is used, its induced distribution and the complete target class must be justified.
2. A counterexample must fix one nonempty alpha and exhibit failure under the uniform law. One acceptable failure certificate is fixed epsilon, delta > 0 and n_k tending to infinity with P(d_BL(mu_{Pi_{n_k}},mu_I) > epsilon) >= delta for every k. An atypical deterministic sequence, finite enumeration, or a growing alpha_n does not meet that requirement.
3. Use a metric for weak convergence, continuous test functions, or justified continuity-set arguments. Do not substitute total variation, convergence on every measurable set, almost-sure convergence under an unspecified coupling, or a claim about every avoider. The v3 p.2 total-variation definition conflicts with its p.3 weak-topology theorem wording. This source inconsistency is not a disproof of the intended weak statement; the paper's full proof has not been independently audited here.
4. Madras-Yildirim's Theorem 1(a), p.5, concerns exponential rarity near (0,1) when the forbidden pattern starts with its maximum; Theorem 17(a), p.25, concerns the nonrare region and its convex hull with (0,0) and (1,1). Reverse-complement symmetry transfers these statements to patterns ending in 1 and the opposite corner. These statements do not identify a limiting permuton's support or prove the target. [Published paper](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v24i4p13/pdf/)
5. OWR pp.298-299 have adjacent formulation errors: an ambient interval in place of the square, (0,1) in place of the cited theorem's diagonal endpoint (1,1), a displayed o(n) despite surrounding o(1/n), and an overly broad measurable-set description of weak convergence. Any later use needs the actual hypotheses and justified rate/uniformity. These errors neither alter the frozen conjecture nor count as its resolution. The older Atapour-Madras 2014 full text was not inspected in this review.
6. Do not silently expand the target to arbitrary forbidden bases or all skew-decomposable forbidden patterns. Those stronger conjectures appear on OWR p.282. That page also records vanishing expected inversion density as a sufficient criterion; it is credited background, not progress made by this source review.

PDF byte counts, SHA-256 values, and inspected-page pins are recorded separately in SOURCE_PINS.json. The cited scope is based on inspected primary statements; no literature-exhaustive openness or priority claim is made.
