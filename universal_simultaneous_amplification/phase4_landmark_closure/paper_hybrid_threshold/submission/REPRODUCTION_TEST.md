# Clean-bundle reproduction test

## 2026-08-20 final clean-room checkpoint

The reduced development-tree replay and submission static audit both exited
zero after the package scripts were installed.  The replay covered:

1. exact Sturm isolation, quadratic minimization, tangency, and monotonicity;
2. all 512 labelled configurations and 108 orbit fibres of the finite hybrid
   audit graph under both update rules;
3. exact pair and pendant response coefficients, rational endpoint margins,
   and the rational-edge-family threshold; and
4. paper-level reconstruction of the response functions and claim-boundary
   markers.

The frozen archive was generated twice from the final source and the two
outputs were byte-for-byte identical.  It contains 19 regular members and has
SHA-256
`76916d91fcc96bceeb4e7a9516571839d4871a0fa63e32fbe25d4a19ebb8cfc6`.
After extraction into a new temporary directory, every entry in
`MANIFEST.sha256` passed.  The root bootstrap created a fresh Python 3.14.6
environment, installed SymPy 1.14.0 and mpmath 1.3.0, and the complete replay
exited zero.

The PDF rebuilt from the extracted source with Tectonic 0.16.9 and Poppler
26.08.0 was byte-for-byte identical to the repository PDF.  The 19-page PDF
has SHA-256
`602e41f0959cde299c6bd0d7acad5dfc3b6a5afc501d4721c4015f3c8ec31dcf`.
Its compiler log has no undefined references or citations and no material
box warnings; all fonts are embedded.  Every page was rendered and visually
inspected for clipping, overlap, missing glyphs, malformed equations, stale
content, and link/layout defects.

This file records tested checkpoints, not an immutable public release.  A
prior v1 archive or PDF hash is not evidence for the current superseding
package.
