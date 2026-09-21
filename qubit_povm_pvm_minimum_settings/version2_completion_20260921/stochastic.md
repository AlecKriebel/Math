# Stochastic output processing: implementation and verification

Checkpoint: 2026-09-21T14:25:03+00:00. Completion estimate for the assigned core stochastic-processing task: **100%**.

## Exact claims and scope

`Bell/StochasticProcessing.lean` defines `StochasticFamily I O` as a family of nonnegative normalized real rows over arbitrary dependent finite output types. The row-index type need not be finite for the definition or existence theorem; finite row-index types are used for finite product decompositions. `StochasticChannel S T` is its ordinary source/target specialization.

For every channel between finite types, `StochasticChannel.decomposition` provides the explicit weight `w(f) = ∏ s, K(s,f(s))` over complete deterministic functions `f : S → T`. The weights are nonnegative, sum exactly to one, and reconstruct every channel entry. No positive-probability hypothesis or division occurs.

`StochasticProcessing A B` supplies a channel for every local input, with input-dependent source and target output counts; it also permits deterministic input selection. Its `behavior` is a real linear map on the full ambient behavior space, with the usual two local channel coefficients multiplying each source behavior entry.

The global random variable is `T.Selector`: a pair of functions assigning an output to every `(input, source outcome)` row on Alice and Bob. Its weight is independent of the observed input pair. `behavior_decomposition` is an equality of entire behavior tables using this single distribution. `deterministic_branch_mem_rawPVM` reuses the checked `StrategyMap` construction and its `coarsenPVM` projectors, including non-injective mergers. `mem_convexPVM` applies convexity to the same complete-strategy mixture. `rawPVM_mem_convexPVM` records the raw-to-convex consequence. **No closure claim for stochastic processing of raw PVMs is made.**

## Boundary cases

- `StochasticFamily.nonempty_iff`: a family exists exactly when every target row alphabet is nonempty.
- `StochasticChannel.nonempty_iff`: a channel exists exactly when nonempty source implies nonempty target.
- An empty source admits a channel even to an empty target, with one empty selector of weight one.
- A nonempty source admits no channel to an empty target.
- Any selector choosing a zero-probability entry has exactly zero weight; declared zero-probability output labels remain in the target architecture.
- Inputs with impossible physical source measurements cannot introduce spurious target PVM strategies: the closure theorem retains actual convex-PVM membership as its premise.

## Verification

Commands run from `bell_lean` with the pinned Lean 4.19.0 toolchain:

- `lake build Bell.StochasticProcessing`: successful production build, recorded in `evidence/stochastic_build.log`.
- `lake env lean validation/StochasticContracts.lean`: exit 0, no diagnostics (`evidence/stochastic_contracts.log` is therefore empty).
- `lake env lean --stdin` with eighteen `#print axioms` commands: every listed dependency closure contains only `propext`, `Classical.choice`, and `Quot.sound`, recorded in `evidence/stochastic_axioms.log`.

The anonymous contracts cover arbitrary finite channel alphabets, both empty-source examples, the forbidden nonempty-source/empty-target case, zero selector weights, actual merged-projector idempotence, full-table reconstruction, and convex-PVM preservation.

An independent semantic review by the calculus agent found no defect in the global selector, reconstruction mechanism, or boundary cases. The finite-label agent is implementing the separate `Bell/FiniteStochastic.lean` wrapper to transport physical processing through the arbitrary-finite-label behavior/hull equivalence. That integration is outside this assigned core module and avoids cyclic imports.

No existing theorem statements or shared aggregate/build scripts were edited. No commits or external communication were performed by this agent.
