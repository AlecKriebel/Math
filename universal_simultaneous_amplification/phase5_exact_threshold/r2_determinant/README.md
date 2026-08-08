# Fitness-two active determinant

This branch isolates the determinant coefficient exactly equivalent to
universal dB complete-graph maximality at fitness two and distinguishes it
from the stronger stationary-promotion coefficient.

## Scope and status

The package proves four finite algebraic facts: the exact target/promotion
implication, transfer to the smaller subset determinant, the centered
triangle forest certificate, and explicit obstructions to uncentered
coefficient/root shortcuts.  It does **not** prove or refute the universal
active-tree sign for arbitrary order.  That sign remains the sole theorem
target of this branch.

Run the exact symbolic audit from the phase-4 obstruction environment:

```text
../../phase4_landmark_closure/obstruction/.venv/bin/python \
  r2_determinant/verify_r2_determinant.py
```

The verifier reconstructs the nine-state active chain for a symbolic
weighted triangle, expands every rooted cofactor, checks the determinant
coefficient, and verifies the centered squared-difference certificate.

Run the independent subset-root-polynomial hostile audit with

```text
../../phase4_landmark_closure/obstruction/.venv/bin/python \
  r2_determinant/verify_root_polynomial_obstructions.py
```

It certifies failures of real-rootedness, ultra-log-concavity, ordinary
log-concavity, and direct level-tail domination.

Status:

- **PROVED:** exact target/promotion implication audit;
- **PROVED:** exact active-tree coefficient for the true target;
- **PROVED:** centered positive triangle certificate;
- **EXACTLY REFUTED:** raw edge-monomial coefficient positivity;
- **OPEN:** the arbitrary-order active-tree coefficient.
