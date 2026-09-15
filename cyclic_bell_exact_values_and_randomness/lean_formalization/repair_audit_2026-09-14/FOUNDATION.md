# Foundation audit

2026-09-15 UTC: Independently evaluated the coordinate physical definitions and all proofs in `CyclicBell/Model.lean` with the pinned Lean 4.19.0/mathlib environment. `lake env lean CyclicBell/Model.lean` exited 0 with no output. No source repair was necessary. The definitions give actual trace-one positive density matrices and complete orthogonal projective measurements; the Born rules and rank-one reductions are definitions/proofs rather than target-table assumptions. The four-outcome model is explicitly dimension-generic for the Hilbert spaces and specific to four outcome labels, as intended by this foundation; general outcome modules must be audited independently.

Checkpoint: Model verification complete (100% of this assigned module); this is not a claim about full-paper formalization.

2026-09-15 UTC: `lake build CyclicBell.Model` completed successfully. Then repaired `MatrixAlgebra.lean` and `TraceCalculus.lean` and completed `lake build CyclicBell.TraceCalculus` (which includes Model and MatrixAlgebra), exit 0; retained log `foundation_build.log`. Existing harmless unused-section-variable warnings remain.

Theorem statements and assumptions were preserved. Repairs: account explicitly for scalar order in matrix scalar multiplication; expand single-coordinate vectors for PSD diagonal positivity; fix swapped tensor summation indices; choose the correct diagonal in spectral-sum multiplication; replace ambiguous `congr` descent through function-valued matrices with `congrArg (spectralSum M)`; normalize the fourth power of the imaginary unit explicitly; use `Matrix.sum_apply` to evaluate matrix sums; reorder the three finite sums in expectation linearity in the correct sequence. No axioms, admitted proofs, omitted theorems, or new mathematical assumptions were introduced.

Checkpoint: all three assigned foundation modules compile (100% of this bounded module task). Full-paper coverage and remaining modules are separate pending work.
