# Five substantive approaches: 2305060 / AMR-022-5060

All times are UTC on 2026-10-04. The whole target remains **unsolved**. Estimates concern progress toward resolving the entire target; they are rough planning judgments, not probabilities. Five proof-attempt turns are consumed. Source triage was not counted as an additional turn.

## Source and duplicate checkpoint, 08:47–08:50

Read the exact primary statement and update on printed pages 107–108 of Hayman–Lingham; checked both page images. Read the complete imported statement and the complete prior report, which had done only statement/web triage and supplied no proof. The live repository queue showed rank 577, queued, 0/5 at baseline commit bd5c59ad2b9f2c57c82aa1fe7b0466fe3ea92e1b. Searches for numeric ID, code, and Sheil-Small in PRs, exact-ID code search, exact-ID branch search, and the attempt-directory listing found no prior work on this target. The related-target groups file did not list it. Other source records mentioning Hadamard convolution concern different claims (6.34, 6.112, 8.1). No outside individuals were contacted. Completion estimate: 5%.

## Turn 1: Root geometry in a bidisc, 08:50–08:52

Mechanism: replace the circular parameter by an independent variable and use two argument-principle homotopies. Derive the lowering operation F − u F_u/α. Factor polynomial slices to obtain Re(u F_u/F) < degree/2.

Result: proved the bidisc equivalence, reconstructed the known integer-α case, and proved the full requested implication for polynomial φ of degree N ≤ 2α. The same method is sharp for unrestricted zero-free polynomial slices: (1+u)^N fails under lowering if N > 2α. The latter is explicitly not a target counterexample because it lacks the required two-variable coefficient structure.

Status: rigorous partial result; no novelty claim. Exact gap: use the special coefficient structure to go beyond the degree bound. Completion estimate: 25%.

## Turn 2: Integral averaging / moment representation, 08:52–08:53

Mechanism: seek a universal finite measure on contractions u → tu which represents exponent lowering and might transfer nonvanishing.

Result: proved that for every noninteger α such a finite complex measure on the closed unit disc is impossible. Its moments would be 1 − n/α, contradicting bounded total variation. Also identified an explicit positive-average failure: ((1+u)^3+(1−u)^3)/2 has interior zeros although both summands are normalized and zero-free.

Status: this precise route is blocked. The obstruction does not rule out other integral representations or methods using extra sector information. Completion estimate: 20%.

## Turn 3: Differential equation and diagonal propagation, 08:53–08:54

Mechanism: exploit the coefficient coupling rather than arbitrary zero-free slices. Derive (u+v)F_uv = αF_v − βF_u and the exact diagonal formula F(−v,v) = φ*(1−z)^(α−β)(v).

Result: both identities are proved and checked algebraically. When α=β the diagonal is identically 1. The desired conclusion is precisely the avoidance uF_u/F ≠ α. A sufficient half-plane bound would close the problem, but no argument propagating this bound from the diagonal or the PDE was obtained.

Status: blocked at a clearly identified analytic estimate. The avoidance condition is not promoted as a solution or an independent theorem. Completion estimate: 25%.

## Turn 4: Compactness and rational approximation, 08:54–08:55

Mechanism: dilate a hypothetical analytic counterexample into the disc, approximate by Taylor polynomials on a closed bidisc, and retain a failed-conclusion zero by Rouché. Then perturb finite parameters and coefficients.

Result: proved that a counterexample, if one exists, can be chosen polynomial with a strict premise margin on the closed bidisc, noninteger rational α > 1, rational β ≥ 1, and Gaussian-rational coefficients. It must have degree > 2α. This is a complete reduction, not a counterexample.

Status: rigorous partial reduction. Exact gap: neither a uniform degree bound nor any example was obtained. Completion estimate: 30%.

## Turn 5: Bounded finite-polynomial falsification search, 08:54–08:55

Mechanism: compare the smallest root radius for the premise and lowered convolution as x moves over a unit-circle phase grid, for reproducibly generated polynomials. A smaller conclusion radius would nominate a rescaled counterexample for subsequent rigorous testing.

Run: 1,152 samples; α in {11/10,5/4,3/2,7/4,9/4}, β in {1,3/2,3}; degrees {3,4,6,8}, only N > 2α; 24 seeded Gaussian-integer coefficient vectors per eligible pair; 96 phase points. The ten most promising parameter/degree winners were rerun on 4,096 phase points. Seed: 2305060. Full outputs and dependency versions: SEARCH.json.

Result: no sampled ratio below 1. The smallest coarse ratio was 1.2108266594872017; the smallest ratio among refined cases was 1.2108944944008464. These are floating-point heuristic diagnostics only. Finite angular sampling cannot certify zero-freeness, and this is not exhaustive in coefficients, degree or parameters.

Status: no counterexample found and no theorem inferred from the search. Completion estimate: 30%.

## Validation and freeze checkpoint, 08:58–09:00

Saved self-contained proofs and the exact remaining gap. The standard-library verifier passed 208 exact rational algebra checks. The heuristic run completed successfully with NumPy 2.3.5 and Python 3.12.14. No complete candidate exists. The packet is frozen for independent review; no remote writes were made by this attempt. The proposed queue classification is `unsolved`, 5/5. Audit can assess these partial results but must not become an extra proof-search turn for the unresolved target.
