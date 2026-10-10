# Validation report

The proof supplies the complete construction and all mathematical hypotheses symbolically. No complete finite quotient or its boundary matrices were materialized. The following supplementary diagnostics passed in normal Python, Python -O, and Python -OO; all checks use explicit exceptions, not removable assert statements.

- Exact construction of PG(2,11): 133 points, 133 lines, 1,596 incidences; every degree is 12.
- Exact integer verification of MM^T=11I+J, which proves the stated spectrum and rules out four-cycles. Bipartiteness rules out odd cycles.
- Every one of the 266 vertex deletions is connected. Each has 12 vertices of degree 11 and 253 of degree 12.
- The proved deleted-link gap bound is (11−√11)/12>7/12>1/2. Numerical diagonalization for representative point and line deletions gives about 0.711324865405; these approximate numbers are not used in the proof.
- An exact rational cocycle on a tetrahedral boundary verifies both double-counting identities: the sum of link energies is E, and the sum of link weighted squared norms is 2E.
- The positive sphere control (tetrahedral boundary) has Betti numbers (1,0,1) and correct local sphere links. It fails the girth-six condition, as it must.
- A 16-vertex triangulated torus has Betti numbers (1,2,1), all vertex links six-cycles, and Euler characteristic zero. It demonstrates why the expansion inequality must be strict: its cycle links have normalized gap exactly 1/2.
- A tetrahedral sphere with an extra triangle attached at one vertex has the global rational homology of a sphere but fails the local-link sphere test. This guards against the forbidden global-only substitution.
- Order q=2 fails the proof's sufficient deleted-link lower-bound test. The diagnostic makes no claim that this alone disproves another property of that small-order example.
- The finite-reduction degree guard checks 4·2=8<9; the justification that these are the correct matrix and path degrees is source-based and is recorded separately.

Source verification: the complete LSV PDF was retrieved successfully during the candidate investigation and inspected as described in SOURCE_AUDIT.md. The source metadata records its exact hash and byte count. Publication preparation adds no new source retrieval or inspection.

Publication boundary: the authored proof, scope, source metadata and this validation report contain original writing and public citations. Source PDFs, extracted text, page images, diagnostic code, raw results, integrity certificates and coordination/history records are separate private material.
