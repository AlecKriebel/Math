# Reproducibility and control scope

The original exact script was hardened for this package. All ten original top-level assert conditions were replaced with numbered explicit checks raising RuntimeError; they therefore run under Python -O. The mathematical matrices and positive expected values are unchanged. Added checks tie the displayed graph basis to T and verify the exact cone generator formulas and separating coordinate bounds. The manifest verifier uses relative paths anchored to the checker file, not the caller's working directory.

Path changes: the checker and proof reports are colocated at the package root. The command does not reference research/recovery directories. The mathematical audit is retained with its original scope; its original assertion-based script rerun is not represented as a review of this hardening. All original universal arguments remain in the proof reports.

Controls run normal and optimized Python. Four negative tests alter actual mathematical data: graph coefficient 2 to 3, one witness coefficient sqrt(2) to sqrt(3), the arrow matrix entry 2 to 3, and H-cone generator coefficient 4 to 3. Each must raise an explicit guard failure. Five manifest controls modify bytes, remove a listed file, add an unexpected file, falsify a digest, and falsify a byte count. Each must fail. Tests operate on temporary copies and do not mutate the frozen package.

The normal and optimized positive checks verify exact SymPy ranks, irreducibility over Q, real witness value 6, rational ambient value 7, graph consistency, and cone-generator identities and inequalities. The written proofs, not finite tests, establish exclusion of every rational threshold-6 witness and the general projective equivalence. No finite enumeration is used as a proof of universal rational infeasibility.

The manifest does not hash itself, and is an integrity inventory rather than an authenticity signature. The public source metadata records source PDF hashes without redistributing those PDFs. A separate package review is required for the editorial synthesis and packaging modifications.

## Executed results

On 2026-10-21 UTC, Python 3.12.14 with SymPy 1.14.0 completed both positive executions and all 18 negative controls: 8 actual matrix/generator mutations and 10 manifest corruptions. Every required rejection occurred under both normal and optimized execution. This records executed checks, not a substitute for independent package acceptance.
