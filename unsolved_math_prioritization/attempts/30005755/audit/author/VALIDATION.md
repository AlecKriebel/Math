# Author verification

The author-side reproducibility check is complete. It is not an independent mathematical acceptance report.

## Reproducible checks

`python3 verification.py --check expected_results.json` passes using only the Python standard library. It verifies:

- the displayed 6 by 6 block matrix has exact integer determinant 1;
- a direct polynomial determinant expansion vanishes in Z[x1,x2,x3];
- all 503 coefficient triples over F_2, F_3, F_5 and F_7 have the expected alternating-matrix rank, and the block has rank 6 in each field;
- the complete submodule-dimension list for the one-dimensional-at-each-vertex witness Y and the corresponding quotient values;
- the annihilating plane and a 2,197-point integer consistency grid for the two strict inequalities and one equality.

The finite-field checks are corroborative. The determinant-one identity, alternating-matrix polynomial, exhaustive one-dimensional subspace argument, and proof's module witnesses establish the claims uniformly over the stated fields. Neither finite testing nor the integer grid establishes a TF class on its own.

## Mathematical dependency checks

The calculation distinguishes the projective-basis g-vector from a module dimension vector. It uses right modules consistently; the arrow-block transpose convention does not alter the determinant. The double decomposition need not assume that 2g is indecomposable. The proof of eta's indecomposability uses sign coherence plus all three possible binary-split obstructions. Positive scaling and all-real reverse inclusion are explicit. The n=3 algebra is defined by triangular multiplication, avoiding transcription errors in an older quiver picture.

The only non-elementary dependencies are the generic-decomposition criterion, uniqueness and sign coherence, and the established positive-combination TF theorem. The new preprint's stronger cone claims and the withdrawn note are not dependencies. The source hashes authenticate consulted bytes and do not certify mathematical correctness.

## Outcome

The explicit wild-example equality and the stated elementary lemmas are the strongest authored results. The general conjecture is unresolved in this investigation. Independent adversarial review of the proof is outstanding. No novelty or acceptance claim is asserted.
