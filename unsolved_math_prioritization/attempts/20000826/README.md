# 20000826: connected multigraded Hilbert schemes

**Unsolved, 5/5 approaches.** This draft publishes scoped partial results and an independently audited literature update. The arbitrary-grading three-variable question remains unresolved. No novelty is claimed.

Start with `author/REPORT.md`, `author/PROOFS.md`, and `independent_audit/AUDIT_REPORT.md`. The independent audit found no mandatory mathematical corrections and passed only the stated scope.

## Explicit Theorem 1 clarification

Vanishing of h in degrees not attained by monomials is an explicit additional nonemptiness condition. Support in weights zero through two alone does not imply it. Read the frozen theorem's “In particular” sentence with this explicit condition; its displayed classification already includes this condition and the empty alternative. The original files and both ZIP freezes are preserved byte-for-byte.

## Boundaries

- The weighted 0–2 classification requires a positive integer coarsening, the stated support and rank bounds, and vanishing in unattained degrees. It is smooth and geometrically irreducible if nonempty.
- The cubic result is standard-graded geometric connectedness, valid in every characteristic. It is not an irreducibility assertion or a result for arbitrary finer gradings.
- The dual-of-multiplication and nonreduced-base arguments are retained. The cited two-component comparison keeps its characteristic exclusions.
- Cid-Ruiz's 2026 five-variable construction is a preprint result, not a three-variable answer, a toric-function assertion, or a minimum-variable theorem. The polynomial-to-function transfer uses a uniform upper-orthant truncation extended by zero; the original saturated ideals do not share their full Hilbert functions.
- Positive finite-support reduction does not yield a weight-two or weight-three cutoff. Nonpositive gradings remain outside the partial classifications.

## Reproduce

From any working directory, with Python 3.8 or newer:

    python /path/to/20000826/verify_publication.py

Compare stdout with `VERIFICATION_RESULTS.json`. The wrapper verifies the exact closed file inventory, all manifest entries, both ZIP byte pins and members, scoped disposition, author replay, independent replay in ordinary and optimized Python, and all five mathematical negative mutations. It uses only the standard library and no network, source PDFs, datasets or computer algebra system. Author and mutation subprocesses run with assertions enabled even when the wrapper itself is invoked with `-O`.

Frozen author “audit pending” and audit “no remote writes” fields are historical checkpoint statements. `PUBLICATION.json` gives the current scoped disposition. Finite computations are controls, not a proof of general connectedness. Public bibliography and inspection metadata remain bounded to the inspections recorded in the frozen bundles.
