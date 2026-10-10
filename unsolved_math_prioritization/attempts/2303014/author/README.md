# Problem 2303014: new reconstruction

**Status: partial results only; general positive-mean target unresolved;
fresh independent audit pending.**

This packet reconstructs useful work on Baernstein's circle-minimum extremal
problem after the original proof files could not be recovered. It must not be
represented as the old frozen packet or as an audited replacement.

Read `PROOFS.md` for the precise boundary class and proofs:

- General L1 slit competitors establish nonemptiness of the interior-continuous,
  Poisson-majorized class.
- The a.e.-trace-only class is unbounded above at every nonzero evaluation point.
- Nonpositive-mean data have the unique optimizer P[F].
- Positive constant data have sharp value (4c/π) arctan√|z0|.
- Explicit controls show nonconvexity, failure of maximum closure, and why finitely
  many sampled radii cannot certify feasibility.

The positive-constant result is a credited consequence of the classical Beurling
projection theorem. No priority claim is made. Interior continuity and Poisson
majorization are explicit scope conditions, not silently attributed to the source.

Run the fresh exact algebra controls with:

    python verify_exact.py

The generated `CHECKS.json` distinguishes finite exact algebra checks from the
analytic proof. `source_manifest.json` records fresh source inspection metadata;
source documents themselves are excluded. `MANIFEST.json` binds only this new
packet's files, excluding itself. A later audit should cite its exact SHA-256.
