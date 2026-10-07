# Independent formal scope audit of family 273

## Checkpoint 1 — source semantics inspected; compilation pending

Timestamp: 2026-10-06 21:13:51 America/Los_Angeles (2026-10-07 04:13:51 UTC).
Best-guess contribution to project mathematical resolution: 20%; publication package: 5%. These are estimates, not evidence.

The read-only upstream clone is exactly `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, with no tracked/untracked changes at initial inspection. The README, Lean README, scope document `lean/docs/273.md`, comparator instructions, comparator statement/JSON, toolchain and original configuration were read. The comparator statement deliberately has `sorry`; its JSON points to the real module `OAI.InformationTheory.PhotonNumber.Inequality`. The actual solution module ends in an ordinary proof.

The final real declaration is `OAI.EntropyPhotonNumber.entropy_photon_number_inequality`, in `lean/OAI/InformationTheory/PhotonNumber/Inequality.lean:689`. It quantifies over positive finite mode number `n`, three states, two finite-energy input hypotheses, transmissivity in `[0,1]`, and the explicit relation `IsBeamSplitterOutput`. It concludes

\[
\eta g^{-1}(S(\rho_A)/n)+(1-\eta)g^{-1}(S(\rho_B)/n)\le g^{-1}(S(\rho_C)/n).
\]

No input tensor-product structure **within** either n-mode input is assumed. Independence is between the two input ports. Finite energy is the finiteness of the expectation of the total number operator, with no Gaussianity, finite-rank or full-rank restriction at the final theorem.

## Semantic match

`Basic.lean` defines `NumberIndex n := Fin n → ℕ`, `Fock n := lp (fun _ : NumberIndex n => ℂ) 2`, and `State n` as a bounded positive operator whose number-basis diagonal has `HasSum ... 1`. For a positive operator on this separable full Fock space, that is the usual positive trace-class normalization criterion. There is no mode cutoff in the state type.

`FiniteEnergy` is `Summable (fun k => totalNumber k * Re <k|ρ|k>)`. `entropy` is the number-basis trace of the continuous functional calculus of `-t log t`, using natural logarithms. Finite-energy entropy summability and the thermal upper bound are proved in `Entropy.lean:902` and `:913`. Therefore the Lean total-series default value for nonsummable real series does not silently define a finite entropy for states used in the final theorem.

The beam coefficient is the factorial-normalized number-basis coefficient of the passive rotation of creation operators. `outputBlock` is the finite total-number-sector sum of the matrix entries of independent inputs, and `IsBeamSplitterOutput` demands a genuine convergent `HasSum` over the discarded number index. `Continuity.lean:42` constructs `beamOutput` as the partial trace of a unitary mixed root-column ensemble; `beamOutput_spec` proves the prescribed entries, and `output_eq` identifies every prescribed output with the construction. The Fock beam rotation and tensor/partial-trace infrastructure are actual mathematical definitions, not an abstract “channel satisfies entropy inequality” class.

The thermal mean-photon function is natural-log `g(t)=(t+1)log(t+1)-t log t`. `gInv` is a lower cut; the real inverse property on `[0,∞)` is proved in `Inequality.lean`. Conversion to bits for the proposed capacity manuscript is multiplication of every entropy by `1/log(2)` and must be stated explicitly.

## Auxiliary assumptions and removal

Regularization uses positive interior parameters, thermal mixing/replacement, and a quartic moment penalty. `Regularization`, `ThermalSetup`, `GibbsData`, `SpectralLogData`, `KrausFlow`, and `WeightedColumns` package explicit auxiliary data. They are not extra assumptions on the final states. In particular the faithful eigenbasis/Gibbs data are constructed for regularized minima by `minimum_gibbs`, and `ThermalSetup` is constructed explicitly from interior parameters in `Inequality.lean`.

The final argument proceeds through `ThermalSetup.base_nonnegative`, `ThermalInterior.entropy_tangent`, `entropy_tangent_beam`, `entropy_tangent_finiteEnergy`, `epni_entropy_interior`, and `epni_entropy_closed`. Number cutoffs replace discarded mass by vacuum, have all finite moments, and never increase energy (`Inequality.lean:464–570`). Energy-bounded entropy continuity proves convergence. The transmission endpoints are included by the final parameter limit. `epni_entropy_closed` already has the direct entropy form needed for a vacuum specialization.

The strongest verified result at this checkpoint is a precise, physically faithful **source statement and dependency structure**, not a reproduced formal build. None of these notes should yet be used to claim completed machine verification.

## Isolated build and exact artifacts

`create_harness.py` exports the 26 transitive OAI source modules from the exact pinned Git objects into the project-local `pinned_build/`; it never writes to the upstream clone. They total 1,401,086 bytes and have only external import `Mathlib`. `source_manifest.json` records module/path, Git object hash, SHA-256, bytes and imports for each module. A source scan of the complete OAI transitive closure finds no `sorry`, `axiom`, `admit`, or `unsafe` token.

The harness preserves original autoImplicit=false and Lean version 4.34.1, but intentionally has a reduced Lake package configuration: only the actual external dependency Mathlib at original pin `d13f23b723b8a846827a245b89c10fc7d3f11612`. The giant original package includes many unrelated packages/compatibility patches, none imported by these 26 modules. Original configurations are retained under `upstream_config/` for audit. This reduced harness is a reproducible selected-module check, not a reproduction of the entire published Lean library.

Observed Lake version: `Lake version 5.0.0-src+5045d00 (Lean version 4.34.1)`. Setup is in progress; diagnostic output is retained in `build_setup.log`. Pending final checks are (1) cache/dependency setup, (2) compilation of `OAI.InformationTheory.PhotonNumber.Inequality`, (3) `#print axioms` for the final real theorem, and (4) comparison or explicit exact statement/definition agreement. No comparator checker has yet run.
