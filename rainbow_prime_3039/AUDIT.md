# Independent adversarial audit: prime-modulus rainbow 4AP partial results

Audit date: 2026-10-20 UTC. Scope: the exact target in `SCOPE.md`, and the analytic, quartic, and computation reports in this directory. This is a mathematical and implementation review, not a formal proof-assistant certificate or a novelty assessment. No external publication was performed by this audit.

## Verdict

The reviewed partial claims pass, subject to their stated restricted scopes. None proves that all sufficiently large primes have the required property for every almost-balanced four-coloring; none supplies counterexamples for unbounded primes. The full prime-modulus question remains unresolved by this work. Prime 31 is not an UNSAT result.

## 1. Exact counts and pair-marginal obstruction

I independently re-derived the equal-pair contributions of the five multiplicity types as 0,1,2,3,6. Their contributions to the pair-partition statistic are 0,0,1,0,3 and to the triple statistic 0,0,0,1,4. These establish the displayed inclusion-exclusion identities, including the negative six coefficient at the monochromatic term. Substitution of either possible almost-balanced size vector gives D=(p²+3)/4−p. Identifying the colors with F₂², xor zero selects precisely types 1111,22,4, so the Walsh identity has the asserted signs.

The pair-law construction is valid: the four initial type masses give equal-pair probability 1/4, hence every matrix entry is 1/16 by color symmetry. There are 12 count vectors of type 31 and four of type 4, with base weights 1/240 and 1/400. A weight perturbation of 4Δ_ij on 3e_i+e_j changes the desired off-diagonal entries by Δ_ij and diagonal i by 2Δ_ij. The stated correction at 4e_i cancels that diagonal excess. Total mass is preserved because the sum of every ordered-pair matrix is one. The bounds 4/p and 7/p on weight losses are safely smaller than the base masses at p≥10000. No integrality of the resulting probability weights is required.

This obstruction concerns a single abstract random color vector with prescribed pair marginals. Exchangeability and exact marginals do not establish simultaneous realizability on the overlapping APs of a cyclic group. The report correctly does not claim this.

Independent exact-rational regression checks tested every permutation of the balanced size vector for 13 odd values of p, including 10001–10021, 65537 and 1000003: 52 pair laws had strictly positive weights, total mass one, and all 16 pair entries correct. Primality is not needed for this abstract-law check. Additional independently authored checks verified the count/Walsh identities on 80 seeded random colorings for p=5,7,11,13.

## 2. U³ sufficient condition

The two-term telescoping identity is exact. After the first two terms, the remaining expectation involves at most two distinct AP positions; their joint distribution under all (a,d) is uniform because their separation is invertible for p>3. Thus centering eliminates those terms. Each surviving term is bounded by the generalized von Neumann inequality, and summing 1+α_i over 24 permutations gives 24+6Σ_iα_i=30, not 48 or 96. The degeneracy d=0 contributes no rainbow term, so R/p² has the correct normalization. Dividing 24 by 30 gives the threshold (4/5)∏α_i and limiting value 1/320.

I independently checked the cited generalized von Neumann statement in Tao's Exercise 23. For the four forms a+jd, the complexity-two application is valid over primes p>3: the required distinct-position coefficients/differences are nonzero. The report does not incorrectly infer U³-uniformity from balance. Independent rational tests verified the exact telescoping identity for all 24 color permutations on each of the above 80 colorings.

Source inspected: https://terrytao.wordpress.com/2010/04/23/254b-notes-3-linear-patterns/ .

## 3. Quartic character lemma

I checked Theorem A.1 in the cited primary article. Its distinct-root version applies here even when some or all nonzero exponents are 2: the polynomial is not a fourth power, because at least one root has multiplicity 1,2, or 3, and the character has exact order four. Replacing distinct-root count by total degree is unnecessary. The s=1 complete character sums vanish, consistent with the bound zero.

Restricting the expansion to U avoids 0^0. At omitted points exactly s contributions vanish; the remaining 4−s are bounded by one. Therefore the accumulated error is 513√p+252, and the additional four excluded points give p−256−513√p. Taking real parts before the triangle inequality justifies using possibly complex summands for a real count.

The squared inequality is legitimate at the stated positive threshold. Its polynomial p²−263681p+65536 is positive at 263681 and increasing thereafter. Thus the threshold and the weaker alternatives hold. Scaling a=dt uses the same t for every d and preserves distinct colors by multiplying character values by a common unit. The arbitrary color at zero is irrelevant because the chosen AP avoids zero. This applies only to quartic multiplicative-coset colorings with p≡1 mod 4.

As an independent computation, I found the first prime congruent to 1 mod 4 at or above the threshold, p=263729, constructed the quartic character using primitive root 3, and counted all prescribed four-position patterns directly. All 256 patterns occurred; the minimum count was 934. This is a consistency test, not the proof of the universal threshold.

Source inspected: https://link.springer.com/article/10.1007/s40879-021-00521-5 , Theorem A.1.

## 4. Exhaustive search and seam witnesses

I reviewed `search.cpp`, freshly compiled it with g++ -O3 -std=c++17, and reran the eight claimed completed primes. All reproduced UNSAT_EXHAUSTIVE. The node counts, respectively for 5,7,11,13,17,19,23,29, were 11,21,309,1113,9947,25051,180787,3086007, matching the existing report. The p=29 rerun took approximately 12.23 seconds. These are implementation-dependent exhaustive results, not externally checkable refutation certificates.

The affine normalization is valid because any balanced coloring uses distinct colors at some u,v and the nonzero difference v−u is invertible. It does not require the two named classes to have specified sizes. Edge deduplication changes no constraint. Every propagation step follows from either a forbidden all-different edge or necessary class-size bounds. In class-size propagation, values fixed/possible are computed before the two tests; this is safe: removing a color when fixed equals the upper bound leaves its possible count at least the fixed count, and cannot create an incorrectly triggered lower-bound forcing step. Repetition handles subsequent effects. Exhausted DFS explores all admissible residual assignments.

I also reran the separate Python enumeration, reproducing absence at 5,7,11,13,17 with node counts 13,47,1137,6959,160394. Its restricted-growth normalization only quotients color names and its tests at the last edge coordinate are sound. Minor documentation issue: the module docstring says “<=13”, although its explicit list and actual runs correctly include 17. This does not affect correctness.

Timeout checks occur every 1024 nodes, so the nominal 20-second budget is approximate, not a strict wall-clock deadline. Timeout must remain UNKNOWN. Relaxed lower-bound witnesses in the separate result file cannot be promoted to balanced witnesses.

For the four odd-length word families, I independently read off the beginning and end colors and checked the modular differences of every asserted witness. For residues 1,3,5,7 mod 8 the color words are DABC,DABC,DBAC,DABC and steps 1,2,1,2, respectively. The points are distinct for m≥1. The class counts are balanced directly by block counts. I reran all 400 tests for m=1,…,100. The argument establishes all m≥1, including composite lengths; primality is not used. It only defeats these four particular transferred interval constructions, not every possible prime coloring.

## Reproducibility

`audit/independent_checks.py` contains independently authored exact-rational identity, pair-law, and quartic histogram checks; its output is `audit/independent_results.json`. Existing C++ and Python search programs were rerun independently after source review. The report's computational conclusions should retain their explicit bounded/implementation-dependent language.

## 5. Structural attempt (reviewed after the initial sections)

`STRUCTURAL_ATTEMPT.md` also passes. The arc-consistency theorem has a precise and limited scope: separate constraints and unary domains, not arbitrary deductions from their conjunction. For a progression containing 0,1,2, their index positions satisfy r+t−2s=0 modulo p; its absolute value is at most six. At p≥17 this forces the ordinary integer equality, yielding only the two consecutive extensions. I checked every case of the domain-support argument: intersections of two size-three domains cannot be empty in a four-element color set, and a size-three domain meets any pair of seed colors. These facts provide the stated non-rainbow support without claiming the supports coincide across constraints.

The exact-cardinality support argument is valid, not merely a check of loose min/max bounds. After fixing the tested value, assigning each unassigned restricted point color 1 uses at most four units of color 1 and at most two of any other color. Every prescribed class size is at least four for p≥17. All residual vertices are unrestricted, so residual capacities can be filled exactly. Consequently the described domains truly form a generalized arc-consistency fixed point even when the single exact global cardinality constraint is included. The conditional assumption of a rainbow 3AP is explicitly stated; its existence is not smuggled into the proof.

The pair-link construction exactly captures rainbow APs as edges crossing C and D. All denominators s−r are nonzero for p>3, and disjoint A,B ensure nonzero d. Component-wise constancy is both necessary and sufficient, hence the subset-sum reformulation is exact. A component larger than ceil(p/4) would obstruct a balanced extension, but the required universal large-component assertion is not established. The p=23 disconnected example does not contradict that weaker sufficient assertion or the eventual-prime target.

I reran the structural script. Every individual AP constraint was arc-consistent at p=17,19,23,29,31,43, and the p=23 pair-link components reproduced exactly the reported sizes 11 and 1. The proof, rather than this finite sample, supports the all-prime local-consistency theorem.

A fresh independent p=31 C++ run terminated as UNKNOWN_TIMEOUT after approximately 20.0003 seconds and 4,619,264 nodes; its full output is `audit/prime31_rerun.json`. This reconfirms only the bounded run's non-completion, not nonexistence of a coloring.

## Final acceptance boundary

Accept the exact identities, abstract pair-law obstruction, conditional U³ criterion, restricted quartic-coset theorem, bounded exhaustive search, all-m seam witnesses, specified arc-consistency barrier, and exact pair-link reformulation as partial results. Do not label the original prime-modulus problem solved, do not count the p=31 timeout as absence, and do not mistake a proposed large-component lemma for a proved theorem.
