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

## Checkpoint 2 — statement equivalence established; build suspended

Timestamp: 2026-10-06T21:16:43.461220-07:00 (2026-10-07T04:16:43.461220+00:00 UTC).
Best-guess contribution to project mathematical resolution: 20%; publication package: 5%.

`statement_definition_comparison.json` establishes exact equality of the comparator and real theorem statement after whitespace normalization, and exact equality of all comparator/actual definitions after removing comments and normalizing whitespace. The sole original textual difference is the documentation for the `g` function's zero-log convention. This is a source comparison, not a `comparator`/`lean4export` check.

The 26-module OAI source closure was additionally scanned for `native_decide`, `ofReduceBool`, `implemented_by`, `extern`, `unsafe`, `sorry`, `admit`, `axiom`, `sorryAx`, and `declare_axiom`: no hits. No claim is made about axiom closure of compiled modules, because compilation did not run. The ordinary `DiagonalForms.System` abstraction packages source/target parameters, test vectors, a linear map, and summability; its `Comparison` predicates are proved for the physical maps at a regularized minimum, rather than postulated in the final theorem.

Build attempts:

1. `lake update` with the original Mathlib Git requirement failed fetching full history (`early EOF`).
2. A depth-one exact-pin Mathlib fetch succeeded and its detached checkout is at `d13f23b723b8a846827a245b89c10fc7d3f11612` (toolchain bump to v4.34.1).
3. Lake's next update unnecessarily tried `git fetch --tags --force origin` and failed with `No space left on device`. Only its own failed 269,774,847-byte `tmp_pack_yTuUV0` was removed. This restored free space from 116 MiB to 371 MiB; no unrelated or user data was removed.
4. The Lake harness was changed to a local path dependency pointing to that exact shallow checkout; another update exited 1 without useful output under disk pressure.
5. Per the lead researcher, all cache downloads/build setup are suspended until adequate space is available. No theorem, axiom printout, or comparator run completed.

The `pinned_build/OAI` selected source copy remains byte-identical to the 26 pinned source objects. The local mathlib source/dependency cache lives only in ignored `pinned_build/.lake/` (146 MiB); no generated file was written to the upstream clone. A final read-only upstream `git status --short --untracked-files=no` remained empty. Upstream's Apache-2.0 license was retained at `pinned_build/LICENSE` for the exported source files.

## Exact remaining gap and permitted claim

**Permitted claim:** the actual supplied EPnI source is an unconditional theorem with the intended full-Fock finite-energy multimode semantics, and contains an explicit, physically faithful proof dependency chain without visible placeholders or a theorem-assuming abstraction. Its comparator and actual definitions/statements agree.

**Not yet verified:** Lean elaboration/kernel acceptance of the pinned proof; exact final theorem axiom closure; comparator verification; whether every step of the substantial handwritten upstream proof is sound independently of Lean; the dynamic-capacity follow-on theorem; novelty/publication conditions.

A complete note may accurately cite the upstream theorem after independent mathematical review, but must not say that this project reproduced its formal verification. If relying specifically on machine verification as decisive validation, the current disk obstacle must be resolved and the stated build/axiom checks completed before promotion.
