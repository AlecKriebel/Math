# Irrational maxima of fractional-part autocorrelation

**Problem:** 30002497 / OWR-12866-004  
**Status:** unsolved after five substantive approaches.

The exact question asks whether
\(A(x)=\int_0^\infty\{t\}\{xt\}\,dt/t^2\)
has a strict local maximum at any positive irrational argument.

This packet does not answer that question. It records:

- a proof, using Balazard–Martin's parity-specific secants, that every
  irrational local maximum must be a stationary Wilton point;
- an exact derivative identity excluding the positive quadratic roots of
  \(x^2+mx=1\), \(m\ge1\);
- analytic bounds and reproducible interval controls also excluding their
  reciprocals;
- the precise gap in finite-convexity, Hilbert-space, rational-cusp, and
  second-order stationary-point arguments.

No novelty or full-resolution claim is made. The partial theorem requires
independent audit before promotion.

## Reproduce

With Python 3 and mpmath 1.3.0:

    python verify_controls.py --cutoff 2048 --dps 40 --output control_results.json

A second run at cutoff 4096 and 60 decimal digits is saved in
`control_results_high_precision.json`; all eleven derivative enclosures
are nested in the first-run enclosures, with identical signs.

The script performs interval integration over exact algebraic breakpoint
expressions, verifies event ordering, and appends the analytic tail bound
\([0,1/T]\). It stops if any ordering is undecidable at the selected
precision. The controls are validated numerics, not a proof assistant
formalization or a search over all irrational arguments.

- `PROOF.md`: definitions, deductions, source dependencies, exact gap
- `SOURCES.md`: primary sources and bounded literature/duplicate checks
- `RESEARCH_LOG.md`: five approaches and completion estimates
- `RESULT.json`: machine-readable outcome
- `verify_controls.py`, `control_results.json`: executable checks and results

Author: Alec Kriebel, https://orcid.org/0009-0001-9320-500X
