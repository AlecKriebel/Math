# Function Theory 6.65: bounded starlike third coefficients

UnsolvedMath 2306065 / AMR-022-6065. Status: **unsolved; five substantive approaches completed**.

The exact supremum for every e<M<5 has not been found. The verified partial result is

    0.9073297832 ≤ B(3) < 0.957,

where B(M) is the largest third Taylor-coefficient modulus among normalized M-bounded starlike univalent disk maps. The lower bound is a rational-coefficient exponential-polynomial construction; the upper bound is an exact rational Fejér/LP-dual certificate. Neither is asserted sharp or novel.

Read PROOF.md for the mathematical argument, ATTEMPT_LOG.md for five distinct approaches and their gaps, and SOURCE_GATE.md for source/status checks. This is provisional AI-assisted work requiring independent expert review.

Run the proof controls with Python 3.10 or later, without third-party packages:

    python verify.py
    python verify_manifest.py

The first command verifies the rational construction, all 64 upper-bound slabs, exact coefficient identities, and rejection controls. The second checks the frozen public-file inventory and hashes. They do not formally verify the analytic dependencies, the historical literature, or global sharpness.

The optional reproduce_* scripts need NumPy and SciPy and rerun exploratory searches. They write fresh search output beside themselves; that output is not part of the frozen inventory, so run them in a copy when preserving the freeze. Optimizers, grids, and quadrature are discovery tools only. The stored certificates and verifiers are the proof-bearing computational artifacts.

Only original notes, code and generated numerical/certificate data are included. Source PDFs, corpus snapshots and private research coordination are excluded. No outside researchers were contacted.
