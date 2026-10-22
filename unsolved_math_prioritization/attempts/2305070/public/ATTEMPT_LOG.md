# Five-turn attempt log: 2305070

Recorded 2026-10-04 UTC. All five substantive approaches below are charged to the target's five-turn budget. The prior imported report only recorded source/web triage and supplied no proof. No previous repository attempt folder or matching pull request was found in the read-only checks. These approaches were developed in one research pass; they are not represented as independent reviews or independent discoveries.

The goal is a full answer to the original existence question. The percentages below are subjective planning estimates of progress toward that goal, not measured confidence, proof coverage, or probability of truth. The auxiliary proofs are in PROOF.md.

## Turn 1: Regular-value smoothing and component tracking

- Mechanism: move away from the at most countably many critical moduli, then try to retain infinite length of the branched example.
- Work: derived the exact local logarithmic normal form Re(w^m)=0; analyzed the saddle pairing for m=2; then built the explicit bounded F=exp(exp(-W)) countercontrol.
- Proved outcome: unbranching is easy generically, but a regular level can have infinite total length with every component finite. The example even has F' nowhere zero and bounded reciprocal. Its components and their exact lengths are computed.
- Exact gap: no argument preserves a single infinite-length component under a level shift or perturbation. An infinite sum over components is insufficient.
- Disposition: blocked as a deduction from regularity and total length alone. Completion estimate: 5%.

## Turn 2: Algebraic approximation and intersection counting

- Mechanism: search among rational functions or exponentials of rational functions; use increasing algebraic complexity to force long levels.
- Work: derived the real polynomial equations for both modulus and real-part levels. Proved the Crofton degree bound, treating exceptional lines and singular points.
- Proved outcome: every such total level has length at most 2*pi*n when the rational degree is at most n. This includes finite sums of boundary-pole Herglotz kernels and some functions with essential boundary singularities after exponentiation.
- Exact gap: increasing degree removes the uniform bound; the finite-degree argument neither constructs nor rules out a limiting infinite-length component.
- Disposition: no finite rational formula can settle the target. Completion estimate: 3%.

## Turn 3: Conformal pullback and infinite coverings

- Mechanism: pull back a line or circle through a conformal map, or use the infinitely sheeted exponential covering of the punctured disc.
- Work: checked the exact line/circle hypothesis of Hayman–Wu's theorem; separately calculated the one-atom singular inner function's complete modulus-level length.
- Proved/cited outcome: univalent pullbacks of these particular curves have finite length. The simple infinite covering has Euclidean length 2*pi/(s+1), despite unlimited winding and infinite hyperbolic length.
- Exact gap: a useful covering would require additional global geometry. Nonzero derivative alone provides no applicable Hayman–Wu bound, and infinite covering degree provides no divergent Euclidean length.
- Disposition: the simplest conformal and covering constructions are excluded. Completion estimate: 2%.

## Turn 4: Infinite positive harmonic superposition

- Mechanism: choose an infinite finite-mass atomic measure, use its Herglotz transform H, and seek one long regular component of Re H=s; exponentiation supplies boundedness automatically.
- Work: proved locally uniform convergence and exact function/derivative tail bounds. Derived the finite truncations' cleared algebraic equations and checked them with exact rational arithmetic for one through eight atoms.
- Proved outcome: summable masses guarantee a bounded zero-free analytic function, and tails can protect compact regular pieces. Countability of critical levels is available, but H can be constant for some non-atomic measures, so nonconstancy must be separately maintained.
- Exact gap: no explicit atomic data force one fixed-level component to make length-divergent excursions through infinitely many shells. The estimates control local perturbations, not remote connectivity.
- Disposition: a quantitatively specified construction route remains unfinished; no candidate solution. Completion estimate: 5%.

## Turn 5: Prescribed nodal geometry and normal-family passage

- Mechanism: prescribe an embedded oscillatory analytic arc of infinite length approaching one boundary point, realize it locally as a level, then extend or take a bounded analytic limit.
- Work: constructed gamma(t)=1-1/t+i*sin(t^2)/t, proved injectivity, disc containment and length divergence, and proved local holomorphic level realization by the inverse function theorem. Tested the limiting strategy against F_n=exp(z^n-exp(-n^2)).
- Proved outcome: the desired curve geometry is locally compatible with analytic levels. However, regular finite-stage levels can have total length at least 2n(1-exp(-n)) while the uniformly bounded analytic functions tend to a constant.
- Exact gap: local realizations do not supply a globally bounded analytic function; compact convergence must preserve nonconstancy, a regular seed, and all length-forcing pieces in the same component. None is supplied by length growth alone.
- Disposition: unfinished after five substantive approaches. Completion estimate: 3%.

## Final assessment

Status: **unsolved, 5/5**. The report contains complete auxiliary proofs and reproducible finite controls. It contains neither a solution nor a verified prior resolution of the full question. No additional exploratory turn is claimed or reserved. Independent checking may assess the saved artifacts without extending the search budget.
