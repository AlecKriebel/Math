# Research log: global one-third endpoint separator, cycle 2

Date: 2026-08-08 (America/Los_Angeles)

No literature search or external communication is used during discovery.

## Frozen starting point

- [PROVED] At fitness `r=3/2`, the universal candidate is
  `(x+2y)/3 <= 1`, where `x,y` are the Bd and dB fixation probabilities
  normalized by their complete-graph baselines.
- [PROVED] The candidate is equivalent to the exact Green--Poisson sign
  `T_2+2C <= 2E`.
- [PROVED] Any universal convex affine separator has Bd coefficient at most
  `1/3`; weighted triangles obey the one-third separator strictly unless
  they are isothermal.
- [FALSIFIED ROUTES] Pointwise/common potentials, independent orientation
  and batching terms, fixed-rank signs, projected low-degree Green systems,
  and operator-order signs of high-mode Schur feedback.
- [OPEN] Either prove the configuration-resolved global sign, or produce an
  exact graph with `(x+2y)/3>1`.

## Executable plan

1. Rebuild the exact fixation and Green primitives and freeze a hostile
   witness screen for any proposed global inequality.
2. Search globally for endpoint violations using full subset-chain solves,
   emphasizing topology/weight regimes not covered by local or modular
   ansatz searches.  Exactify every positive candidate before interpretation.
3. In parallel derive path-reversal, spanning-forest, and full LP-dual
   representations whose certificates retain all Johnson modes.

## Exact separator refutation

- [NUMERICALLY DISCOVERED, THEN EXACTLY REBUILT] A separated two-class
  search found a score above one for class orders `2,20`.  Freezing the
  simple rational weights `w_AA=137`, `w_BB=1`, and `w_AB=1/500` gives an
  order-22 complete-support graph.
- [PROVED] Exact FLINT solution of the full 61-state orbit chains gives
  `x=0.9334417185...`, `y=1.0336117074...`, and
  `(x+2y)/3-1=0.0002217111...>1/5000`.
- [INDEPENDENTLY EXACTLY VERIFIED] A second implementation aggregates the
  actual discrete-time labelled event probabilities and solves with SymPy
  DomainMatrix.  It reproduces both fixation hashes and the affine gap.
- [PROVED] The affine crossing is
  `theta_0=0.3355466820...>1/3`.  Combined with the earlier proved upper
  requirement `theta<=1/3`, this proves that no universal fixed convex
  affine separator exists.
- [OPEN] The witness has `x<1<y`, so the endpoint disjunction remains open.

## Construction implication under active audit

- [DERIVED LEADING THEORY / NOT YET A THEOREM] Combining a dilute population
  of these weak `K_2` satellites with a dilute growing hub-leaf population
  gives formal leading corrections
  `F_B+lambda/(r-1)` and `F_D-lambda`.  Their feasible interval persists
  slightly above `3/2`; a complete post-establishment and uniform-error
  proof is being developed separately.  No construction claim is made here.
