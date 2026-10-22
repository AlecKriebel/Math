# Research log

All timestamps are UTC on 2026-10-04. Completion estimates describe progress toward the full statistical question; they are not correctness probabilities or claims that part of an open problem has a canonical percentage solved.

## 13:45–13:47: Source and scope (10%)

Attempted the catalogue page, verified the pinned record and obtained the official OWR report. The full source asks for an optimality principle without a specified comparator class. Read the corresponding full manuscript, its formal exact-versus-upper-bound distinction and follow-on literature. The existing desk assessment had already warned that the greatest-minorant identity was insufficient.

## Attempt 1, 13:47–13:48: Order-theoretic characterization (15%)

Proved the greatest-nondecreasing-minorant characterization, idempotence and elementary stability. Checked direction: greatest risk minorant is not smallest achievable statistical risk. The characterization is already in the underlying paper. Exact gap: a statistical comparison class and lower bound. This route does not supply new optimality.

## Attempt 2, 13:48–13:50: Selection and cross-validation (25%)

Derived a simultaneous lower bound for all data-dependent selectors from a uniform deterministic equivalent. Matched it with a validation upper bound and a bounded-loss concentration condition. Kept grid approximation separate and explicit. Exact gap: the uniform lower bound is a genuine extra condition, and the result excludes prediction averaging or refitting. This is a restricted theorem, not full resolution.

## Attempt 3, 13:49–13:51: Rare events and failure of uniformization (25%)

Constructed a symmetric base learner from cumulative uniforms modulo one. All deterministic aspect-ratio limits equal 2, yet a growing candidate collection contains a risk-1 fit with probability tending to one. The torus transformation proves independence, and a telescoping product gives the exact probability. Validation still succeeds with bounded squared loss. The construction refutes substitution of pointwise limits for uniform control, without contradicting the manuscript's strong formal assumptions.

## Attempt 4, 13:50–13:53: Explicit Gaussian improvement (30%)

Derived the minimum-norm risk envelope at signal energy 4 and noise variance 1, then shrank a half-sample fit by 2/3. Proved the conditional limit 11/3 versus envelope 4 by projection concentration, an inverse-Wishart quadratic-form representation and vanishing cross terms. The exact finite expectation was independently expressed and checked algebraically. The mechanism gives a concrete failure of unrestricted optimality, consistent with prior improvement results.

## Attempt 5, 13:52–13:54: Minimax quantifiers and profile insufficiency (25%)

Constructed two models with the same base learner and exactly equal profiles, but different Bayes-optimality conclusions. Proved the valid fixed-dimension sample-discard minimax monotonicity statement and identified the missing expected-risk, parameter-uniformity and adaptation hypotheses. Exact gap: no nontrivial exact minimax or admissibility statement for the broad source question follows from the profile assumptions alone.

## 13:53–13:57: Controls and bounded conclusion (25%)

Ran 1,024 profile controls, 7,770 admissible-minorant checks and 49,506 exact selector checks, including ties. Checked exact rare-event probabilities, finite torus bijections, Gaussian rational identities and minimax order. Visually checked the report's printed p.2679. Rechecked source attribution and the current target record. No full resolution was found or claimed.

Final disposition: **unsolved after five substantive approaches**. The strongest retained outcomes are the conditional selection theorem and explicit obstructions to stronger interpretations. The remaining task is to formulate and prove an appropriately nontrivial statistical optimality principle with an admissible model/procedure class; the elementary envelope identity cannot stand in for it.
