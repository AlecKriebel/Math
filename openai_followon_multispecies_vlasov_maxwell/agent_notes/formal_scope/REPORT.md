# Family 362 formal-scope audit

Checkpoint: 2026-10-06 21:26 America/Los_Angeles (2026-10-07 04:26 UTC).

Best-guess project completion: mathematical resolution 5%; publication package 0%. These estimates express progress in understanding the prerequisites; they are not evidence for the multispecies target. Strongest verified result of this audit: exact static identification of the one-species formal statement and its hypotheses. **No Lean proof certificate was reproduced.**

## Pinned input and checked scope

Source repository: `/Users/alec/Desktop/math`, read only, commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The inspected source repository's HEAD was this commit and its status output was empty. Files were copied with `git archive` into `checks/formal_scope/lean`; no builds ran in the original clone.

I read the repository and Lean READMEs, `lean/docs/362.md`, comparator instructions and configuration, actual `Model.lean` and `Main.lean`, the top-level local-existence and continuation statements, and the concrete increment/selected-coefficient proof chain identified below. I did not line-by-line audit all 89,993 lines of the 207-module import closure.

All transitive local imports of `OAI.Analysis.VlasovMaxwell.Main` stay inside the 207-file VlasovMaxwell subtree. The only external import is `Mathlib`. A textual scan of that complete local closure found no `sorry`, `admit`, `axiom`, `unsafe`, `implemented_by`, or `extern`. A further search found no `native_decide`, custom `elab`, `run_cmd`, or `run_tac` in the family. This is a static screen, not a kernel dependency-axiom check.

File-level SHA-256 hashes, byte counts, the import closure, and the build receipt are in `checks/formal_scope/source_inventory.json`, `static_scan.json`, and `build_receipt.json`.

## Exact real declaration

`OAI.Analysis.VlasovMaxwell.Main.lean:44` declares

```lean
theorem global_classical_solution (d : Datum) (hd : Admissible d) :
  ∃ s : Solution, Classical d s ∧ SmoothOnFiniteHorizons s ∧
    ∀ s' : Solution, Classical d s' → SameNonnegativeTime s s'
```

There is no extra explicit global-existence, increment, field-bound, symmetry, smallness, or neutrality hypothesis on this declaration. The proof obtains the required uniform increment producer from `hd.population_increment` and passes it to the separate continuation theorem. The actual declaration ends with a proof term rather than an admission.

`ComparatorChallenges/VlasovMaxwell.lean` contains the intentionally admitted specification theorem. Its definitions from `abbrev Vec` through `SameNonnegativeTime` are **literally identical** to those in the actual `Model.lean`; this equality was checked by a script, not inferred from documentation. Its `sorry` is not a proof. The comparator JSON targets the real solution module and permits only `propext`, `Quot.sound`, and `Classical.choice`; `enable_nanoda` is false. The comparator executable, `landrun`, and `lean4export` were absent, and the comparator was not run.

## Semantic correspondence

The actual model is the positive-charge, unit-mass, one-species system in rationalized units with light speed one:

- `Vec = EuclideanSpace ℝ (Fin 3)` and `Phase = Vec × Vec`.
- `q(v) = sqrt(1 + ‖v‖²)` and `velocity(v) = v/q(v)`.
- `rho(g)(x) = ∫ g(x,v) dv`; `current(g)(x) = ∫ g(x,v) velocity(v) dv`.
- Transport acceleration is `E + velocity(v) × B`, with coefficient +1.
- Maxwell evolution is `∂t E - curl B = -current`, `∂t B + curl E = 0`.
- Both constraints are required initially and at every nonnegative time: `div E = rho`, `div B = 0`.

`Admissible` (`Model.lean:50`) means smooth compactly phase-supported nonnegative initial density; smooth initial fields with a uniform bound on every derivative order, including order zero; both fields in L² of space; and both Gauss constraints. It imposes no compact field support and no neutrality. These definitions match the scope document for this data class.

`Classical` (`Model.lean:89`) includes C¹ regularity on the closed time half-space, nonnegative particles, fields continuous into L² in time, a single compact phase-support set on each finite time horizon, all five PDE/constraint equations, and the prescribed initial values. The conclusion's uniqueness is within exactly this class. `SmoothOnFiniteHorizons` supplies joint spacetime smoothness on every closed finite slab. The equations use within derivatives at time zero; on positive times these agree with ordinary derivatives under the regularity hypothesis. Bochner integrals are total Lean operations, but the stated compact support and regularity are the relevant integrability safeguards, rather than an intended use of their value for nonintegrable functions.

This model contains **no species index, no arbitrary mass, and no signed charge coefficient**. Its theorem is not the requested multispecies theorem.

## Pivotal proof chain actually inspected

1. `LocalPDE/StrongLocalExistence.lean:38` constructs a bounded spatially smooth C¹ classical prefix from `Admissible` data through a Picard field limit, particle limit, uniform jets, limit equations, initial-value agreement, and L² control. At line 87 the temporal equations and spatial jets are used to obtain a jointly smooth bounded prefix. `Regularity/SlabEvolutionRegularity.lean:89` and `LocalPDE/SmoothLocalExistence.lean:20` expose local smooth existence. None of these inspected top-level statements assumes a solution as an additional datum. The bodies and declarations were inspected, not typechecked during this audit.
2. `Continuation/Bootstrap.lean:305`, `Admissible.signed_increment_strict`, produces constants M,A before the asymptotic momentum cap P, then assumes the coupled increment bootstrap for all supported labels and proves a strict improvement. The main estimate comes from `hd.force_bulk_uniform`. The direction-weight endpoint errors are bounded using the existing increment hypothesis, and the explicit coefficient inequalities close the strict improvement. `signed_bootstrap_propagation` at line 411 is the separate bootstrap-continuity mechanism.
3. `Bootstrap.lean:584` obtains `uniform_signed_increment`; line 608 gives `population_increment`. `PopulationIncrement` at line 102 uses a cap on **all** supported labels, then returns the receiver increment estimate. Its quantifiers do not assert independent uncoupled one-particle bounds.
4. `Population/BulkReceiverResidual.lean:17,67,112` assembles selected and unselected estimates, absorbs a receiver residual with the absolute direct-Lorentz estimate, and adds the initial boundary-field term. The same physical single-species flow is used throughout.
5. `Population/RepresentativeClosedBinSourceIndices.lean:118,295` contains the stable and deficit logarithmic coefficient-sum statements. The stable statement requires receiver and all-source increment bootstraps; both use one `PhaseFlowOn s.E s.B T`, an `EnergyPrefix s T`, and agreement of the initial density with `d.f₀`. `LocalPDE/GeometryCutoffDeficitLogSum.lean:37,117` adds cutoff/remainder estimates from these physical sums. These are actual authored proof declarations, not just names in a catalogue.
6. `Continuation/GlobalContinuation.lean:1030` is explicitly conditional on a uniform physical increment producer. `Main.lean` discharges that producer using `hd.population_increment`; it does not leave this as a final theorem hypothesis. The uniform population lemma is general in a family of solution prefixes, but its inputs are increment estimates for that family. This general abstract bootstrap does not derive the species-pair estimate.

The inspected dependency structure is a plausible noncircular bootstrap architecture on its face. Without a completed build and a deeper line-by-line audit, this observation does not certify the upstream argument.

## Exact missing bridge for the follow-on

The physical estimate declarations above have one density `s.f`, one unit-charge Lorentz phase flow `F`, and one kinetic energy `∫q(v) f`. Both source and receiver are labels of that same flow. The normalized multispecies model would instead require flows with accelerations `(e_a/m_a)(E + velocity(u) × B)`, sources `Σ_a e_a g_a`, and positive kinetic energy `Σ_a m_a∫q(u)g_a`. No inspected declaration covers two differently accelerated source/receiver flows, negative source charge, charge-zero transport, or mass weights. Generic labels and generic families in the abstract population bound do not repair this missing physical input.

Thus there is no formal certificate for the new target in these files, even if the full upstream one-species build is later reproduced. A follow-on theorem must prove its pairwise impulse and angular/selected-range estimates independently and then use an appropriately simultaneous bootstrap. Replacing this work with “sum the one-species theorem” would be unsupported.

## Build attempt and limits

The pinned toolchain ran successfully: Lean 4.34.1, compiler commit `5045d0056413266e57c625dcd7c365b10e377c52`, arm64-apple-darwin24.6.0. Lake was `5.0.0-src+5045d00`. The exact original full lake configuration and manifest are retained as `lakefile.upstream.lean` and `lake-manifest.upstream.json`. The audit used a separate minimal configuration requiring only Mathlib at the identical pinned revision, because all audited imports use only Mathlib plus the family subtree. This changed build configuration is documented; it is not claimed to reproduce the entire repository's configuration or unrelated families.

`lake update` resolved Mathlib at `d13f23b723b8a846827a245b89c10fc7d3f11612`; all nine relevant package revision checks matched the pins listed in the resolved manifest. The first update was stopped before its automatic cache extraction, then rerun with `MATHLIB_NO_CACHE_ON_UPDATE=1`. The cache utility itself built. A download-only `cache get- Mathlib` completed 8,908 compressed entries. Shared disk availability fell to approximately 1.34 GiB before extraction, below the agreed 1.5 GiB safe cap. Consequently no Mathlib cache was extracted, no Model proof elaboration succeeded, and Main, the axiom-print audit, and the comparator were not built or run.

`model_initial_check.log` records the failed import `unknown module prefix 'Mathlib'`. An independent direct compiler invocation after cleanup also exited **1**, recorded in `model_direct_check.log`. These are dependency-availability failures, not an observed Lean source error. Download success or building the cache utility is not proof validation.

Only the audit-owned generated cache and `.lake` downloads were removed after retaining versions, manifests and receipts. Free space then recovered to approximately 2.56 GiB. No source-clone file, shared researcher file, index, branch, commit, credential, or external individual was touched. No publication action occurred.

## Reproduction

With adequate free disk, use the preserved project-local `checks/formal_scope/lean` directory and run the supplied `checks/formal_scope/reproduce.sh`. It resolves the same minimal pinned dependency set, fetches Mathlib's default trusted cache, builds `OAI.Analysis.VlasovMaxwell.Main`, and runs `Audit.lean` to print the real declaration and axioms. Capture exit statuses and inspect the axiom output against the comparator's three permitted axioms. Full comparator certification still requires installing and running the separately documented comparator tools, and is not performed by this script.

The correct present status is **static semantic scope inspected; formal verification not reproduced; species-dependent physical bridge absent**.
