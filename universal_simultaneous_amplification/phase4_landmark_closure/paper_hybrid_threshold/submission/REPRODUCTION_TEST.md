# Clean-bundle reproduction test

## 2026-08-20 final clean-room checkpoint

The reduced development-tree replay and submission static audit both exited
zero after the package scripts were installed.  The replay covered:

1. exact Sturm isolation, quadratic minimization, tangency, and monotonicity;
2. all 512 labelled configurations and 108 orbit fibres of the finite hybrid
   audit graph under both update rules;
3. exact pair and pendant response coefficients, rational endpoint margins,
   and the rational-family threshold; and
4. paper-level reconstruction of the response functions and claim-boundary
   markers.

The frozen archive was generated twice from the final source and the two
outputs were byte-for-byte identical.  It contains 19 regular members and has
SHA-256
`ad6164df555e029d69c1abb698a4e50e94c848866f95f6ce65f3fec8fb2292d0`.
After extraction into a new temporary directory, every entry in
`MANIFEST.sha256` passed.  The root bootstrap created a fresh Python 3.14.6
environment, installed SymPy 1.14.0 and mpmath 1.3.0, and the complete replay
exited zero.

The PDF rebuilt from the extracted source with Tectonic 0.16.9 and Poppler
26.08.0 was byte-for-byte identical to the repository PDF.  The 15-page PDF
has SHA-256
`6d379ad45c20bae1ba8d4e22617571c1712f141b1fc9d626f27885bab2a92318`.
Its compiler log has no undefined references or citations and no material
box warnings; all fonts are embedded.  Every page was rendered and visually
inspected for clipping, overlap, missing glyphs, malformed equations, stale
content, and link/layout defects.

This file records tested checkpoints, not an immutable public release.  A
prior v1 archive or PDF hash is not evidence for the current superseding
package.
