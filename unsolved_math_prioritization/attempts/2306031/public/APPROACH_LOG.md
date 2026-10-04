# Five substantive approaches: Function Theory 6.31

All five approaches were explored on 2026-10-04 UTC. None resolves the whole target. The percentages below are subjective progress estimates toward the original mathematical problem, not success probabilities or formal measures. The five-turn allocation is exhausted; further verification may check the present artifacts but is not an additional search attempt.

## 1. Abel/Cesàro reformulation and phase-cancellation control

- Mechanism: factor out the double pole using B=(1-z)^2 f/z and identify the exact triangular coefficient sum.
- Result: formula (1) and the radial exponent cap ε=min(δ,1) are proved. An explicit analytic example obeys the radial assumption but fails coefficient convergence.
- Adversarial check: its derivative has a zero in (-1,0). It is excluded from S and is not offered as a counterexample to Duren's theorem.
- Exact gap: construction/control inside the univalent class.
- Target completion estimate: 5%.

## 2. Angular Cauchy-transfer approach

- Mechanism: a complex-plane remainder bound provides angular integrability on the coefficient circle.
- Result: Proposition 1 gives n^(-η), (log n)/n, or 1/n under the stated additional angular condition.
- Adversarial check: the original hypothesis is on a single radius. The stronger all-disk estimate is explicitly added and not inferred.
- Exact gap: obtain enough angular control from the original univalence and radial data.
- Target completion estimate: 10%.

## 3. Weighted Wiener coefficient moments

- Mechanism: bound the triangular sum by a weighted absolute moment of B's coefficients.
- Result: Proposition 2 proves a power rate, and a finite first moment yields a two-term expansion. Proposition 3 gives an exactly univalent rational example with δ=2 and exact coefficient error 1/(2n).
- Adversarial check: the rational family's injectivity is proved globally by a half-plane transformation. This only rules out universal o(1/n), and does not prove O(1/n) or logarithmic sharpness.
- Exact gap: derive the weighted moment or a sufficient weaker cancellation bound in general S.
- Target completion estimate: 15%.

## 4. Starlike Herglotz rigidity

- Mechanism: the atom in the positive measure for zf′/f determines the radial logarithmic growth exponent.
- Result: any starlike function with a nonzero quadratic radial limit along the positive axis is exactly the Koebe function.
- Adversarial check: the direction is fixed; rotated Koebe functions growing elsewhere have zero quadratic limit along this radius. The argument relies on positivity that fails for general S.
- Exact gap: an analogous admissible positive representation for arbitrary S.
- Target completion estimate: 15%.

## 5. Positive derivative measure and scale-by-scale coefficients

- Mechanism: restrict to Re((1-z)^2 f′)>0; positive radial kernels bound measure mass near the quadratic pole. An explicit coefficient kernel transfers local mass decay to rates.
- Result: Theorem 6 proves n^(-min(δ,1)) for δ<1, and (log n)/n at δ≥1; symmetry removes the endpoint logarithm. All these functions are proved univalent. This class contains non-Koebe examples.
- Adversarial checks: the measure atom is identified by dominated convergence, the subtracted measure stays positive, and the endpoint logarithm is retained absent symmetry. The restriction is not silently replaced by all close-to-convex or all univalent functions.
- Exact gap: the positive representation needed for the radial mass estimate is unavailable for general S. No full improvement or sharp lower construction is proved.
- Final target completion estimate: 20%. Status remains unsolved, 5/5 turns.

## Search/verification boundary

The literature pass checked the exact Hayman–Lingham problem/update, the 1974 paper's publisher record and indexed primary-paper excerpts, and targeted searches for later Tauberian/rate improvements. No full resolution was verified. Failure to find one is not proof that none exists. Full Duren paper retrieval was blocked or returned an HTML app shell, so no claim of an independent proof audit of the complete 1974 paper is made.
