# Self-audit, not an independent-agent review

The following inspections were performed by the same assistant that wrote
the source candidates. They are not evidence of a separate agent or peer review.

* State/PVM/Strategy fields do not contain a score, bound, maximum, or table.
* The universal target propositions quantify nA,nB independently and require
  positivity of each dimension. The witness specialization to four is separate.
* The density state is built from Phi4 using a general positive outer-product
  construction; it is not defined by assuming a target probability.
* The table is a separate expression from targetBorn. The candidate proof uses
  a general rank-one Born lemma and then finite exact arithmetic.
* The literal swap (0,1,3,2), its algebraic phase weights, and q recurrence are
  separate declarations. The source exponential-phase bridge is still missing.
* Bob transpose/conjugation mistakes can preserve the d=4 parity pattern, so
  observable encodings and eigenvectors were checked separately in the exact
  computation, and encoding theorems are present as Lean candidates.
* The first reduced Bell normalization has no extra 1/4. The second SOS uses
  1/8; its l=0 coefficient is positive, not negative. The exact negative control
  detects a doubled SOS prefactor.
* The symbolic algebra retains noncommuting same-party generators. No first
  universal bound is inferred from attaining a value or annihilating squares.
* No source candidate asserts that the target realization is a Bell maximizer.
  The fixed-pair success definition does not optimize Eve across realizations.
* The standard root imports all candidate and audit files. Intentionally false
  controls are separate from that root. Their compilation is unexecuted.
* The existing qubit project's real local certification was distinguished from
  its stale draft comment. Its fixed Fin 2 model was not reused as an arbitrary-
  dimensional theorem.
* A pinned Matrix.trace API inspection exposed the need to unfold
  Matrix.diag_apply in the generic pure/mixed trace proof. This was repaired
  before packaging, but no compiler pass is claimed for the repair.
* The build runner refuses absent or additional axiom reports and custom
  axioms. Its Python tests pass, but these tests do not validate Lean proofs.

No contradiction or arithmetic failure was found in the scoped exact checks.
This is not a correctness verdict on the whole manuscript or on uncompiled
proof scripts. The principal open review gate remains actual Lean execution.
