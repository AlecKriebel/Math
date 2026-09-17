# Exact scalar and four-dimensional repair log

2026-09-15T03:30:35Z — ScalarData builds on the pinned Lean 4.19.0/mathlib revision. Assigned scalar/target module scope approximately 35% complete; downstream D4 and Phases still under compilation. This percentage is not an estimate of whole-paper completion.

Repairs retain every original definition and theorem statement:

- Proved the sine-square constant through the double-angle cosine identity; the submitted `norm_num` had rewritten away the sine term needed to use its proposed half-angle lemma.
- Unfolded the `k = sqrt 2` bridge in the sine/cosine product proof.
- Replaced a failing tactic-branch layout in the 16-entry root-of-unity table with explicit checked power decompositions.
- Preserved the real trigonometric arguments and their casts when reducing the source coefficient formula; identified integer powers with natural powers using `zpow_ofNat` after finite index reduction.
- Replaced unsuitable nonlinear arithmetic normalization in `k_alpha`/`k_beta` with exact polynomial combinations.

The source coefficients still use their original exponential embedding, real sine denominators, and integer exponent convention. No axiom, placeholder proof, statement weakening, or numerical approximation was added.

Build evidence: `scalars_build.log` (updated by subsequent builds in this work stream).

2026-09-15T03:33Z — Assigned ScalarData/D4/Phases scope 100% repaired and compiled. `lake build CyclicBell.D4 CyclicBell.Phases` reports success, after compiling repaired ScalarData. D4 required local simplifier facts for vector indices 2/3, finite-index addition reduction, and a complex component proof of state normalization. All original statements remain identical. In particular the actual density/projector Born rule computes the target table; the target measurement endpoint still deliberately makes no universal maximality claim.

2026-09-15T03:39Z — Expanded ownership to Cycle4, Witness, Attainment, Guessing, Endpoints, Regression. Cycle4 and Witness now compile (expanded d4 witness chain approximately 60% repaired; not a whole-paper estimate). Replaced matrix-entry simplification with matrix sum/diagonal API, computed maximally-entangled trace by finite-sum delta elimination, and verified the manuscript's D_l bridge by exact exponent congruences modulo16. All theorem statements preserved. The initial five axiom reports in `scalar_axioms.log` contain only `propext`, `Classical.choice`, and `Quot.sound`.

2026-09-15T03:44Z — Expanded assigned d4 module scope 100% repaired and compiled. `lake build CyclicBell.Regression` succeeds through Attainment, Guessing, Endpoints and Regression. Both first- and second-family d4 physical counterexample endpoints now combine their original universal bounds with explicit state/PVM attainment and the computed nonuniform Born table. This does not establish the all-dimensional/general-model portion of the package.

Attainment repairs enforce staged exact root-of-unity reduction before complex coordinate expansion, use matrix-entry sum identities, and discharge the finite sums in the actual residual-annihilation proof. Guessing repairs evaluate its actual one-dimensional Eve conditional states via nested sum identities. Regression's canonical table and conjugation/adjoint negative controls compile. All original definitions and theorem statements in the assigned modules are preserved; `Endpoints.lean` and `Phases.lean` required no edits. No new assumptions or axioms were introduced.

Endpoint axiom evidence: `D4AxiomCheck.lean` and `d4_axioms.log` explicitly check both complete counterexamples, combined endpoint, source D compression, full validity, actual Eve bridges, and two negative controls.
