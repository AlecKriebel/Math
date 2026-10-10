# Independent validation report

All mathematical diagnostics were implemented independently of the candidate's code and executed in Python's normal, -O and -OO modes. Runtime checks use explicit exceptions rather than removable assertions. All three modes returned identical passing results.

## Exact projective-plane and deletion checks

- Constructed PG(2,11) from normalized triples with dot-product incidence: 133 points, 133 lines and 1,596 edges.
- Verified every degree is 12 and MM^T=11I+J with exact integer arithmetic.
- Checked connectivity and degree counts for all 266 one-vertex deletions. Every deletion has 12 vertices of degree 11 and 253 of degree 12.
- Verified the cleared-denominator normalized Gram identity after deletion and the block partition identities. They recover squared singular values 1, 1/12 and 11/144 with multiplicities 1, 11 and 120, plus one zero adjacency eigenvalue. The exact normalized gap is 1−1/√12>1/2.
- The proof's weaker deleted-gap bound and the degree guard 4·2=8<9 also pass exact checks.

## Polynomial conjugation matrices

- Independently constructed F_11[X]/(X³+X+4), verifying irreducibility and inverses for all nonzero field elements.
- Built all 133 nine-dimensional matrices from the constant-plus-t formula in LSV Equation (9).
- Verified determinant 1 at all 11 elements of F_11 for every generator. Since each determinant polynomial has degree at most 9, this proves determinant identically 1, rather than merely sampling it.
- Compared the formula against direct multiplication in the cyclic algebra on all nine basis vectors for every generator, at t=1 and t=2: 2,394 exact comparisons passed. These specialization comparisons are diagnostic checks of the displayed formula, not a substitute for its symbolic source derivation.
- A deliberately altered generator matrix failed the direct algebra comparison as expected.

## Homology, weighted energies and adverse controls

- A tetrahedral sphere has exact rational Betti numbers (1,0,1) and three-cycle links. It passes the local sphere test and fails the girth-six condition as expected.
- An independently generated periodic triangular torus has 25 vertices, 75 edges, 50 triangles, Betti numbers (1,2,1), and six-cycle links. It shows that gap equal to 1/2 does not force first-cohomology vanishing.
- A tetrahedral sphere with an extra triangle attached at a single vertex has global Betti numbers (1,0,1), but fails the local sphere test. This rejects the global-homology-only substitution.
- Exact rational cocycles on all three complexes verify sum of link energies equals E and sum of weighted link norms equals 2E, including an example with unequal edge triangle counts.
- The small-order q=2 deleted link has exact normalized gap 1−1/√3<1/2. It is an adverse control for applying the strict spectral argument indiscriminately.
- The polynomial t^8 is a direct adverse example for reducing depth from t^9 to t^8 in the degree-separation argument.

## Authentication and limits

The review authenticated the candidate inputs against recorded sizes and SHA-256 identities. The proof and source audit were reviewed byte-for-byte as identified in REVIEWED_FILES.json. The audit used a strict file inventory, external hash seal and corruption controls. Publication preparation reauthenticated the recorded inputs; it did not repeat the mathematical diagnostics or add source inspection.

No full finite quotient was generated, and no claim is made to have computed that quotient's entire homology. The proof remains symbolic. Source PDFs, copied source text, diagnostic code, raw results and coordination records are kept outside these authored public reports.
