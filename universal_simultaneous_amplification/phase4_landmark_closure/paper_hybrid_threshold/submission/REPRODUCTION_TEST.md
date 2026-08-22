# Clean-bundle reproduction test

## 2026-08-22 post-referee clean-room checkpoint

The reduced development-tree replay and submission static audit both exited
zero after the package scripts were installed.  The replay covered:

1. exact Sturm isolation, quadratic minimization, tangency, and monotonicity;
2. all 512 labelled configurations and 108 orbit fibres of the finite hybrid
   audit graph under both update rules;
3. exact pair and pendant response coefficients, rational endpoint margins,
   and the rational-edge-family threshold; and
4. paper-level reconstruction of the response functions and claim-boundary
   markers; and
5. fail-closed checks under optimized Python plus disposable early exact-
   identity and late integration-marker mutations.

The frozen archive was generated twice from the corrected source and the two
outputs were byte-for-byte identical.  It contains 23 regular members and has
SHA-256
`d2145513f8abe295e9e7fab62f062fa9d0f7a6282de95e8155f3db4621485274`.
After extraction into a new temporary directory, every entry in
`MANIFEST.sha256` passed.  The root bootstrap created a fresh Python 3.14.6
environment with package-index access disabled, installed the bundled
hash-pinned SymPy 1.14.0 and mpmath 1.3.0 wheels, and the complete replay and
failure-regression suite exited zero.  A subsequent plain `release_bundle.sh`
invocation automatically reused that environment and reproduced the archive
byte-for-byte.  Negative tests also rejected optimized replay/bootstrap/release
invocations, altered identities, a corrupted wheel, incorrect source modes, a
corrupted archive payload, and malformed, unsafe, or duplicate internal-
manifest entries.

The PDF rebuilt from the extracted source with Tectonic 0.16.9 and Poppler
26.08.0 was byte-for-byte identical to the repository PDF.  The 21-page PDF
has SHA-256
`4e86597bb0baff388e8ce7ccf6ffd808f86b5ea846acf6f2188b31016fd2572c`.
Its compiler log has no undefined references or citations and no material
box warnings; all fonts are embedded.  Every page was rendered and visually
inspected for clipping, overlap, missing glyphs, malformed equations, stale
content, and link/layout defects.

The source link and integration marker name the planned annotated, unsigned
tag `simultaneous-amplification-beyond-three-halves-v2.0.2`.  This checkpoint
becomes the frozen record only after that tag is placed on the exact scientific
commit and its remote peeled commit is verified.

This file records tested checkpoints, not an immutable public release.  A
prior v1 archive or PDF hash is not evidence for the current superseding
package.
