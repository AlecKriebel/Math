# General finite-dimensional physical models and witness repair

2026-09-15 UTC. Scope: `GeneralModel.lean` and `GeneralWitness.lean`.

Both files now pass real Lean 4.19.0 compilation using the pinned Mathlib dependency and ordinary Lake targets. See `general_model_build.log` and `general_witness_build.log`. This checkpoint completes the assigned two-module repair (100%); it does not establish whole-paper completeness.

Preserved all definitions and theorem statements. No axioms, admissions, hypotheses, or theorem deletions added.

GeneralModel repairs: make double-sum ordering explicit for tensor multiplication and correlator expansion; use Matrix.sum_apply rather than the inapplicable function-sum simplifier; normalize scalar-action multiplication in spectral calculus; use the actual Complex conjugation normal form for real trace and norm-square identities.

GeneralWitness repairs: explicitly transport real inverse-square-root equality into complex numbers; replace nonexistent star_ite; supply both orientations of finite equality-sum simplification; use Matrix.sum_apply; explicitly commute character arguments and complex factors; fix signs in the elementary zero-coefficient equivalence; identify the constant-phase basis extensionally; quote the reserved identifier `«prefix»` (the declaration name remains `CyclicBell.General.prefix`); fix star-product factor order and dependent-dimension rewriting in the cyclic prefix recurrence.

Verified endpoints include actual PVM encoding, order/unitarity, rank-one Born probability from density matrices, normalized Fourier distribution/marginals, full weighted-cycle eigenbasis, and cyclic prefix recurrence. Semantic assumptions remain explicit: nonzero outcome number, finite coordinate spaces, positive trace-one density, projective complete measurements, unimodular phase weights and product-one recurrence as appropriate.

2026-09-15 UTC second checkpoint: `GeneralCycles.lean`, `GeneralChirp.lean`, and `GeneralPolarPhases.lean` repaired and compiled as ordinary Lake targets (100% of this next three-module assignment). Cycle repairs instantiate product/sum reindexing functions explicitly, normalize conjugation of conditional expressions, and explicitly name residue dimension/numeral before cast normalization. Chirp repairs normalize integer/natural casts in the character formula and quote the reserved prefix name. Polar repairs avoid simplifier unfolding of cis before its unit identity, rewrite the factor only in the intended expression, and correctly instantiate the translated finite-product equivalence. All original mathematical statements retained; no admissions or new assumptions.

2026-09-15 UTC third checkpoint: `GeneralCycleCharpoly`, `GeneralExposure`, `GeneralPermutation`, and `GeneralFirstWitness` now compile through normal Lake targets. Source repairs preserved intended types (Exposure required explicit `Ix d → ℂ` annotations for `Pi.single`, preventing a typeclass timeout). GeneralPermutation required pointwise continuous-map normalization, transparent local CFC notation, translated-product arguments, and a direct weighted-cycle expression for the attained score. The first-family all-dimensional counterexample now checks end to end against the universal bound; this is a meaningful proved endpoint, but other paper endpoints are still undergoing repair.
