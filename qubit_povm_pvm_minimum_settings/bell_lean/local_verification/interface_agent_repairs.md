# Compilation repair checkpoint

Checkpoint: 2026-09-11T01:48:30Z. Completion estimate: 100% of the assigned three-module
repair batch. This does not estimate completion of the full development.

The following modules successfully compiled with pinned Lean 4.19.0:

* `Bell.Scalars`: reduced the root import footprint; made the robust square
  identity unfold all nested polynomial definitions before `ring`.
* `Bell.Transportation`: reduced the root import footprint; explicitly reduced
  the final capacity row after simplification left a `Fin.cons` application.
* `Bell.ClassicalProduct`: reduced the root import footprint; simplified the
  normalized tail product before unfolding `pin`, preserving the matching
  hypothesis in the one-coordinate marginal proof.

All theorem statements and physical definitions are unchanged. No placeholder,
custom axiom, unsafe shortcut, or added theorem premise was introduced.

Successful command evidence is in `scalars_build.log`,
`transportation_build.log`, and `classical_product_build.log`. Each command was
`lake build Bell.<Module>` and completed successfully. Remaining output consists
of non-fatal linter warnings. No simultaneous build was needed for this batch.

## Second and third batches

Checkpoint: 2026-09-11T02:02:22Z. Completion estimate: 100% of the eight modules
assigned so far, without implying completion of the entire project.

`Bell.Discrimination`, `Bell.LocalSimulation`, `Bell.Targets`, `Bell.OneInput`,
and `Bell.DeterministicInput` now also compile successfully. Their corresponding
`*_build.log` files record actual pinned Lean runs. Changes repair complex
conjugation simplification, finite numeral and Boolean normalization, one
wrapped tactic-location syntax error, and preservation of linear expectation
wrappers before finite-sum rewrites. `binaryTernaryArchitecture` is now an
`abbrev` with exactly the same body; its transparent input/output counts let Lean
infer finite numeral instances. The complete 36-entry transportation table
reconstruction uses a local heartbeat allowance of 2,000,000 and no new premise.

`InterfaceAxioms.lean` and `interface_axioms.log` audit selected declarations
from these layers. The first seven compiled checks depend only on `propext`,
`Classical.choice`, and `Quot.sound`. All mathematical theorem statements remain
unchanged. The independently audited physical model and final target meanings
are retained.

## Residual physical bridge batch

Checkpoint: 2026-09-11T02:16:13Z. Completion estimate: 100% of all twelve modules
assigned to this agent; final whole-project validation remains with the parent.

The production targets `Bell.ResidualClosure`, `Bell.ResidualCoordinates`,
`Bell.ResidualEncoding`, and `Bell.ResidualStrategy` all successfully compiled.
The closure source required no changes. Coordinate repairs use the existing
checked projective-ray distinctness lemma, normalize finite constructor atoms,
use the correct matrix-vector and scalar API, and prove the affine metric
normal form by linear arithmetic. This avoids unnecessary nonlinear proof-term
growth without changing the claim. Encoding repairs make active-support and
submodule coercions explicit, preserve the original alphabets through the full
padding map, and reassociate matrix inverse cancellations in two checked steps.
The final physical strategy constructor repairs expand the actual steered
operator before its determinant calculation, check its normalization by linear
arithmetic, and handle all five active labels with exact support counts.

No physical definition was weakened, no main hypothesis was added, and no
placeholder or custom axiom was introduced. Source edits were handed off and
frozen immediately after the final successful production build. The separate
`Residual*Probe.lean` files and their logs are intermediate diagnostics, not the
production verification evidence. The final `residual_*_build.log` files are
the successful actual module build evidence.
