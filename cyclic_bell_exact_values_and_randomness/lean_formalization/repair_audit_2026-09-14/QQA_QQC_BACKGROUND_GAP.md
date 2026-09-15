> Historical assessment, superseded in part by the subsequent construction effort: `GeneralCoverageGNS` and `GeneralCoverageReconstruction` now compile. They construct actual complete Hilbert spaces and commuting PVM models from limit word kernels. The earlier statement that no implementation was attempted records the initial audit checkpoint only; consult `GNS_RESEARCH_LOG.md` and the final integrated report for the closure-wrapper status.

# Qqa subset Qqc: pinned-library feasibility and dependency audit

Timestamp: 2026-09-15T03:54:38.984686+00:00

The pinned Mathlib source does not offer a concise existing theorem that fills this gap. I searched the actual local checkout at `c44e0c8ee63ca166450922a373c7409c5d26b00b` for GNS/Gelfand–Naimark–Segal, cyclic state representations, positive-definite kernel reconstruction, analytic Hilbert ultraproducts, and operator-topology compactness. No GNS or Hilbert-ultraproduct construction was found. No axiom, model-definition change, or conditional replacement theorem was introduced.

## What is actually missing

`GeneralCorrelationValues.lean` defines Qq using arbitrary finite-dimensional tensor-product state/PVM realizations, Qqa as the actual product-topology closure of Qq, and Qqc using genuine commuting PVM vector states on complete complex Hilbert spaces. `Qq_subset_Qqc` is proved by the explicit finite-to-commuting purification construction. The missing assertion is

```
Qqa d α β ⊆ Qqc d α β
```

for the existing definitions. A sufficient theorem is that Qqc is closed; then closure monotonicity with the proved Qq inclusion finishes. Merely supplying `Qqa_subset_Qqc_of_isClosed` would transfer the whole unsolved construction to an assumption, so it would not close the gap.

The manuscript displays the inclusion chain near `main.tex:233–239` as general background. Consequently this remains a missing displayed mathematical assertion if “full formalization” means every assertion including standard background. It does not remain an unsupported premise of any currently proved main exact-value endpoint.

## Actual available Mathlib components

- `Analysis/InnerProductSpace/Defs.lean`: `PreInnerProductSpace.Core` provides conjugate symmetry, positivity, additivity and conjugate linearity; its `toSeminormedAddCommGroup` and `toSeminormedSpace` construct the seminorm infrastructure.
- `Analysis/InnerProductSpace/Completion.lean`: inner products descend through `SeparationQuotient` and extend to `UniformSpace.Completion`; `inner_coe` identifies the dense embedded pairing.
- `Order/Filter/Ultrafilter/Defs.lean`: `Ultrafilter.exists_le`/`Filter.exists_ultrafilter_le` refine a nontrivial filter.
- `Topology/Compactness/Compact.lean`: compact ultrafilter convergence, including `IsCompact.ultrafilter_le_nhds` and `Ultrafilter.le_nhds_lim`.
- `Analysis/InnerProductSpace/WeakOperatorTopology.lean`: characterization of weak-operator convergence using matrix coefficients. It does not construct the required limit PVM representation.
- `ModelTheory/Ultraproducts.lean`: ordinary first-order ultraproducts and Łoś's theorem over `Filter.Product`. This is not an analytic Hilbert ultraproduct: it does not quotient bounded vectors by zero limiting norm or supply a complex Hilbert space with bounded operators.

These are useful building blocks, but a new representation/analytic quotient construction is still necessary.

## A valid constructive route

One can prove closedness of Qqc directly, or restrict to finite input alphabets and a convergent sequence from Qq for the paper's cases. A Hilbert-ultraproduct route has these exact obligations:

1. From a closure point p obtain a nontrivial convergent filter of realized behaviors. For finite alphabets, a sequence suffices. Choose each actual state vector and commuting PVM realization; for Qq use the already proved purification map first.
2. Form the complex vector space V of uniformly bounded sections across the varying Hilbert spaces. Define its pairing by the ultrafilter limit of the coordinate inner products. Compactness of a sufficiently large closed complex disk gives existence of each limit. Prove conjugate symmetry, sesquilinearity, and nonnegative self-pairing from coordinate identities.
3. Equip V with the induced seminorm, quotient zero-norm vectors (or use the separation/completion machinery), and complete to a genuine complex Hilbert space H. Prove the inner-product formula for the canonical embedding. The section of unit state vectors has norm exactly one in H.
4. Each coordinate projection acts on bounded sections with norm at most one. Prove it preserves zero-norm vectors, define its bounded linear action on the quotient, and extend it to H. Prove that adjoint/selfadjointness, idempotence, same-input orthogonality, completeness and cross-party commutation persist. These are essential: positivity/normalization of a limit table alone is insufficient.
5. Prove that the resulting vector-state joint probabilities equal the limits of the given probabilities, coordinate by coordinate. Bundle the operators and vector into the existing `CommutingOn` structure and produce the existential witness required by `Qqc`.

An alternative is a moment/GNS construction: take limits of all finite words in the projection generators, build the positive semidefinite word-pairing on the free complex span, quotient its nullspace, complete, and extend left multiplication by generators as bounded projections. This still needs the same missing positivity-to-Hilbert representation and bounded-operator extension work; it is not reduced to finite matrix checks.

A tempting shortcut is to embed all finite strategies in one Hilbert space and take weak-operator limits of their projections separately. This does not prove the result: multiplication is not jointly continuous in the weak operator topology, so idempotence, commutation, and the joint-probability products do not automatically survive. Keeping all word moments or using the norm quotient is precisely what avoids that failure.

## Why the main theorem proofs do not depend on this gap

`GeneralBehavior.three_model_suprema` takes only Qq⊆Qqc, an upper bound for every Qqc behavior, a continuous Bell functional, and an attaining finite-dimensional witness. It obtains the Qq bound by inclusion, the Qqa bound by `continuous_bound_on_closure`, and lower bounds from the same finite-dimensional witness. It never invokes Qqa⊆Qqc or closedness of Qqc.

`GeneralCorrelationValues` applies that construction separately to the first/second reduced/augmented functionals. Thus the equal q/qa/qc values are genuinely proved without the missing general inclusion. The adversarial implementation likewise defines `GuessQa` as the closure of the extended finite tripartite behaviors and extends normalization/closed scalar conditions directly; it does not silently substitute arbitrary extensions of a Qqa marginal or assume that all GuessQa behaviors admit a Qqc realization.

## Assessment

This is standard-background coverage work, not a newly discovered counterexample or an error in the paper's inclusion. In this pinned library there is no verified small API-based completion available. A dedicated Hilbert-ultraproduct or positive-kernel reconstruction module is a substantial independent formalization task. I did not start an untested skeleton or add a placeholder that could be mistaken for completion. The gap must remain explicitly listed until the actual realization construction above is kernel-checked.

Best estimate: feasibility/dependency assessment is 100% complete; the missing general inclusion itself is 0% newly formalized in this assessment.
