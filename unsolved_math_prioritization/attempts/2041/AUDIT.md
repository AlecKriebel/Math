# Independent mathematical audit: EP-312 / problem 2041

## Publication and review scope

This is an unrefereed AI-assisted prose-only edition. “Accepted” means an independent internal AI audit of the explicitly stated partial result; no external human peer review, journal acceptance, or formal proof-assistant certification is claimed. The complete substantive candidate proof and independent mathematical audit are retained. No mathematical correction was required. Historical finite tests are described for context; their programs, detailed receipts, and certificate contents are not distributed, and this edition is not an executable reproduction package. Publication preparation did not rerun those mathematical tests or newly inspect scholarly sources.

## Decision

**ACCEPT AS A CORRECT ELEMENTARY PARTIAL RESULT. THE UNIVERSAL EXPONENTIAL TARGET REMAINS UNRESOLVED.**

The candidate's same-constant threshold removal, equivalence with its stated logarithmic-mass assertion, bounded-multiplicity theorem, and necessary restriction on a universal constant are mathematically correct. No proof correction is required. Acceptance is limited to these statements and the exact finite computations separately identified below. It does not certify Korsky's analytic proof, establish novelty, identify the optimal constant, or prove the missing logarithmic-mass bound.

The original audit independently reconstructed the arguments, examined the original quantifiers and cited primary sources, and used independently authored exact implementations. It neither imported nor executed the candidate's scripts. Source text and dataset contents are not distributed in this prose-only edition.

## 1. Immutable input and attribution

The audited object was the complete candidate package, with manifest SHA-256

`c6ff35a28d6f126e37b1cd4f8b0a37f118d1c3a4a2da90149532f42651a28452`.

Its original candidate proof document has 14,471 bytes and SHA-256

`1632cee679256e9ab1eceba1c1ca918c4b0a575f1e86d51fc1c9840767fca777`.

Historically, all 11 candidate members, all 96 members of the source manifest, and all 10 supplement members were independently checked for exact byte counts and SHA-256 matches against independently pinned source manifests. These were separate authenticated inputs. Their contents are not distributed here; public source hashes, sizes, and inspection limits are recorded in SOURCES.json.

The original [Erdős–Graham book, printed p. 40 / PDF p. 36](https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf) was visually inspected. Its occurrence-indexed question has a fixed mass parameter, sufficiently large sequence length, strict error bound, and permitted exact unit sum. The candidate's imported scope is every real K > 1, with the sequence-length threshold allowed to depend on K. The nearby density and distinct-denominator questions are different problems.

[Samuel Korsky's manuscript](https://arxiv.org/abs/2607.04157), *A Stretched-Exponential Bound for an Erdős–Graham Unit-Fraction Problem*, states an arbitrary-multiset bound ε(A) ≤ exp(−c√(K log K)) for R(A) > K ≥ K₀, without an additional cardinality threshold. Its optimal-complement and labelled-compression lemmas overlap the candidate's deterministic reductions and are properly attributed. This audit accepts neither its analytic argument nor any priority claim. The [27-page PDF](https://arxiv.org/pdf/2607.04157) displays July 7, 2026; the [HTML](https://arxiv.org/html/2607.04157v1) displays August 24, 2026. Both identify arXiv v1 / July 5. At the time of the original audit, fresh official-page reads corroborated those dates and the stated theorem, but did not establish byte identity between formats or refereed acceptance. The source metadata records the separately pinned artifacts and inspection scope.

## 2. Definitions and quantifier audit

A finite multiset is a finite list of labelled occurrences. Selecting one occurrence never permits selecting another occurrence for free. Let R(A) be its reciprocal mass and let q(A) be the largest reciprocal subsum at most 1, including the empty choice. Since the number of choices is finite, q(A) is attained and ε(A) = 1 − q(A) is well-defined.

For a fixed c > 0, define:

- P(c): for every K > 1 there is an integer T(K) such that every occurrence multiset A with |A| ≥ T(K) and R(A) > K satisfies ε(A) < exp(−cK).
- U(c): every finite A with R(A) > 1 satisfies ε(A) ≤ exp(−cR(A)).

The distinction between `<` in P(c) and `≤` in U(c) is necessary. No threshold is allowed to depend on A after K is fixed, and c is fixed before either K or A. The proof below uses precisely these quantifiers.

## 3. Independent padding proof and threshold removal

For finite labelled lists A and T, every sublist U of their occurrence union decomposes uniquely into U_A and U_T. If R(U) ≤ 1, positivity implies R(U_A) ≤ 1, so

R(U) ≤ q(A) + R(T).

Taking the maximum gives ε(A ∪ T) ≥ ε(A) − R(T). Also ε(A ∪ T) ≤ ε(A), since an optimal old selection remains available. Thus the deficit is Lipschitz from below under positive added reciprocal mass. The lower bound remains valid when its right side is negative.

Given any η > 0 and required number t of new occurrences, choose an integer D > t/η. The list of t copies of D has mass t/D < η. This handles arbitrarily large cardinality without a lower bound on the new reciprocal mass.

Assume P(c). Fix A with r = R(A) > 1 and then any K in (1,r). If ε(A) > exp(−cK), choose 0 < η < ε(A) − exp(−cK). Pad to any length at least T(K) with mass below η. The enlarged list still has mass greater than K and has deficit strictly greater than exp(−cK), contradicting P(c). Hence ε(A) ≤ exp(−cK) for every K in (1,r). Letting K increase to r yields U(c) by continuity, with the **same c**.

Conversely, U(c) and R(A) > K > 1 give

ε(A) ≤ exp(−cR(A)) < exp(−cK).

This proves P(c) for every cardinality. Equality at ε(A) = exp(−cR(A)) would therefore be compatible with the original strict target.

There is no density transfer hidden in this argument. Repeated denominators make length unrelated to the density of the set of denominator types. Even padding with many distinct, sufficiently large denominators would not yield the positive-density hypotheses of a set-valued representation theorem. Only reciprocal mass and deficit are transferred here.

## 4. Independent complement and compression audit

Assume R(A) = r > 1 and ε(A) = δ > 0. Choose an optimal occurrence selection S, with mass 1 − δ, and let B be its occurrence complement.

Any unused weight 1/n ≤ δ could be adjoined to S and would produce a strictly better selection with mass at most 1. This is impossible, including the boundary 1/n = δ, which would produce exact mass 1. Therefore every n in B satisfies n < 1/δ, strictly. Also

R(B) = r − 1 + δ > r − 1 > 0.

Every subsum of B is a subsum of A, so B avoids the whole interval (1 − δ,1], with its right endpoint included.

An occurrence of denominator 1 is impossible when δ > 0. All weights are therefore at most 1/2. In any ordering, the first prefix to reach 1/2 has mass at least 1/2 and strictly below 1, because its previous mass was below 1/2. Thus q(A) ≥ 1/2 and δ ≤ 1/2. In fact δ < 1/2: B is nonempty, and a denominator in B must satisfy 2 ≤ n < 1/δ, ruling out 1/δ = 2. This verifies the small-mass boundary needed later without a large-K assumption.

For compression, assign each formal item a disjoint bundle of original B occurrences. If p divides n and p formal items of denominator n exist, unite their bundles and replace them by one item of denominator n/p. The new item has exactly the same weight because p/n = 1/(n/p). Bundles continue to partition the original occurrences. Every formal subset consequently lifts to an original subset of exactly equal mass, even when formal denominators coincide.

Each operation decreases the number of formal items by p − 1, so termination is finite for any legal order. Denominators decrease by divisibility, preserving the strict upper cutoff. A formal denominator 1 would lift to an exact unit subset of A, forbidden by δ > 0. At termination, m_C(n) < p for every prime divisor p of n, hence m_C(n) < P⁻(n).

**The direction matters:** all compressed sums are original sums, but some original sums may disappear. For example, two copies of denominator 6 can be compressed to one denominator 3; the old value 1/6 then disappears. The candidate claims the correct one-way lifting statement, not equality of full sumsets. One-way lifting is exactly what gap avoidance needs. No unique terminal form is claimed or required.

## 5. The logarithmic-mass equivalence

Read N > 2 as a real parameter. Let L(C₀) assert that every stable multiset C of integers 2 ≤ n < N avoiding (1 − 1/N,1] has mass at most C₀ log N.

If P(c) holds, Section 3 gives U(c). When R(C) > 1, the interval avoidance condition implies ε(C) ≥ 1/N, and U(c) implies ε(C) ≤ exp(−cR(C)). Hence R(C) ≤ log N/c. When R(C) ≤ 1, the elementary inequality log N > log 2 gives R(C) ≤ log N/log 2. Therefore L(C₀) holds for C₀ = max(1/c,1/log 2). Empty multisets are covered by the second case.

Conversely, assume L(C₀). For any A with r > 1 and δ > 0, the construction in Section 4 supplies a stable C with mass r − 1 + δ. Put N = 1/δ and x = log N. We proved N > 2, and lifting supplies exactly the interval avoidance required by L(C₀). Thus

r = 1 − δ + R(C) < 1 + C₀x ≤ (C₀ + 1/log 2)x.

The last step uses x ≥ log 2. Rearranging and exponentiating gives

δ < exp(−r/(C₀ + 1/log 2)).

The case δ = 0 is immediate. Therefore P(c) follows with c = 1/(C₀ + 1/log 2). The constants are absolute in both directions, though not identical across the L formulation.

This proof does not invoke a density result, an analytic manuscript theorem, a square-logarithmic estimate, or finite denominator coverage. Stability alone is insufficient: at prime denominator p it permits p − 1 occurrences. The gap-avoidance assumption remains essential. The candidate explicitly leaves L(C₀) unproved.

## 6. Bounded multiplicity, rounding, and all K > 1

Fix an integer M ≥ 1 and assume every denominator in A occurs at most M times. The uncompressed complement B inherits that bound; compressed C need not, and is deliberately unused here.

For δ > 0 put N = 1/δ and J = ⌈N⌉ − 1. This is exactly the largest integer strictly less than N, both when N is integral and when it is not. Since B is nonempty, J ≥ 2. Therefore

R(B) ≤ M Σ(n = 2 to J) 1/n ≤ M log J < M log N.

The non-strict middle bound follows by integrating 1/x over each interval [n−1,n]; the final bound is strict because J < N and M > 0. This gives r < 1 + M log(1/δ). With x = log(1/δ) ≥ log 2,

r < (M + 1/log 2)x,

so δ < exp(−c_M r) < exp(−c_M K), where c_M = 1/(M + 1/log 2) and r > K > 1. Exact-unit inputs require no estimate. There is no omitted small-K range, empty-complement case, denominator-1 exception, floor/ceiling error, or asymptotic threshold in this proof.

For M = 1 this includes sets. Because c_M tends to zero with M, these infinitely many fixed-M theorems do not imply a positive universal constant for unbounded multiplicities.

## 7. Exact obstruction and arbitrarily large cardinality

For A₀ = {2,3,3,5,5,5,5}, multiply subset masses by 30. The possible numerators are 15a + 10b + 6d, with 0 ≤ a ≤ 1, 0 ≤ b ≤ 2, 0 ≤ d ≤ 4. Numerator 28 occurs at (a,b,d) = (0,1,3).

If the numerator were 29, parity would force a = 1 and leave 5b + 3d = 7. For b = 0,1,2 the corresponding d is respectively 7/3, 2/3, or −1, none allowed. If the numerator were 30, parity would force a = 0, and modulo 3 would force b = 0. Then d = 5, again outside the capacity. Thus the largest numerator at most 30 is 28, and ε(A₀) = 1/15 while R(A₀) = 59/30.

U(c) forces 1/15 ≤ exp(−59c/30), equivalent to

c ≤ (30/59) log 15.

The independent rational logarithm enclosure places this value strictly between 1.37697467852654 and 1.37697467852656. The candidate's displayed decimal is consistent with this certificate.

For any c larger than this bound, log(15)/c < 59/30. One can therefore choose K strictly between max(1,log(15)/c) and 59/30. This explicitly verifies the K > 1 requirement even when log(15)/c itself is at most 1. Then η = 1/15 − exp(−cK) is positive. Padding by arbitrarily many occurrences with total mass less than η produces arbitrarily large counterexamples to that particular c. Nothing here disproves the existence of a smaller positive universal c, and equality at the bound is not excluded.

For the candidate's concrete family, t copies of denominator 300t add exactly 1/300. The old optimal subset together with all t added occurrences has mass 14/15 + 1/300 = 281/300, below 1. The padding lower bound matches this witness, proving the exact deficit 19/300 for **every** integer t ≥ 1. Total mass is 197/100 > 19/10. The degree-12 Taylor sum for exp(57/20), calculated as a rational number, is greater than 300/19; positivity of the omitted terms proves exp(−57/20) < 19/300. This is a strict failure of c = 3/2 at K = 19/10 for unbounded cardinalities.

The modular shortcut warning also checks out. A numerator congruent to 29 modulo 30 forces (a,b,d) = (1,2,4) by reduction modulo 2,3,5; its actual mass is 59/30. Removing the integer part is not an allowed occurrence selection. Likewise, a signed difference is not a positive subset. These examples invalidate those proposed shortcuts, not the logarithmic-mass conjecture itself.

## 8. Historically recorded independent exact verification

The original audit used newly authored standard-library programs; no candidate implementation was imported or executed. They used explicit failures rather than Python assertions, so optimized Python did not disable checks. These programs, detailed receipts, and certificate contents are omitted from this prose-only edition. The following is a historical report, not a claim of executable reproduction from the distributed files.

The independent exact checker used meet-in-the-middle occurrence enumeration and binary search, independently of the candidate's subset-sum bitset and coefficient-product checks. It checked:

- All 19,448 multisets of length at most 7 with denominators 1 through 10, including 4,138 positive-gap inputs of mass greater than 1 and 12,834 inputs of mass greater than 1 with exact unit subsets.
- Complement cutoffs, occurrence witnesses, gap inheritance, and 2,189 distinct exact bounded-multiplicity log certificates. The logarithms use rational positive atanh expansions after exact powers-of-two range reduction, with rigorous geometric bounds on the tail; no floating comparison is used.
- 297 integer and noninteger ceiling-boundary cases.
- 170 compression runs using two legal move orders, 106 compression steps, and all 9,500 compressed occurrence subsets in those fixtures, with explicit disjoint-bundle lift checks.
- 605 general padding pairs, six distinct concrete padding parameters, the exact A₀ obstruction, the Taylor comparison, and four semantic negative controls involving the forbidden endpoint, wrong deficit, modular overshoot, and one-way compression.

The independent stable-search checker reconstructed the candidate's full finite denominator range using explicit integer reachable sets and coefficient expansion, with no bitset. It recovered 135,828 stable configurations without exact unit subsums, of which 131,864 have mass above 1, and 674 distinct positive deficits in the latter group. This confirms the reported combinatorial counts. It does not certify a global ordering of floating-point ratios or optimality beyond the finite range.

Each mathematical check ran normally, under `-O`, and under `-OO`, with byte-identical outputs within its check family. The independent integrity checker separately tested one valid fixture and 14 corruptions, including same-length changes, truncation, removal, extra files/directories, stale manifest pins, duplicate members/JSON keys, path escapes, and symlinks. Those three optimization modes also produced identical outcomes.

The finite tests support implementation correctness only. The infinite arguments are the proofs in Sections 3–7; none is inferred from a finite search.

## 9. Acceptance boundary and publication verification

No correction to the candidate result is required. A future summary must preserve all of these limits:

1. Status remains partial; the universal arbitrary-multiset exponential theorem is unresolved by this work.
2. The logarithmic-mass assertion is an equivalent missing estimate, not a proved theorem.
3. The fixed-M exponent depends on M.
4. The obstruction is an upper restriction on admissible c, not a negative solution of the existence question or an optimal constant.
5. Compression only guarantees lifting from compressed to original sums.
6. Korsky's analytic result remains an attributed manuscript claim, with the different PDF/HTML artifacts and dates preserved. No claim of novelty or complete literature coverage is established.

The original audit manifest authenticated its authored documents and local verification artifacts, with independent checks of candidate and source identities. Those original artifacts remain unchanged. The public MANIFEST.json for this edition lists the distributed prose and metadata members and hashes every other member; its own digest is recorded independently in the publication description. These identities establish exact bytes and provenance, not mathematical formalization. Historical finite-test identities and the limits of this edition appear in VERIFICATION.json.
