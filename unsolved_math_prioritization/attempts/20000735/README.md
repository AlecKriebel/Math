# Chebyshev Nahm family and ordinary Bloch information loss

For problem 20000735, this packet records an accepted, known family-level result relevant to AIM Problem 2.4. The broad AIM program remains unresolved by this work.

For every integer r ≥ 1, the matrix A_ij = 2 min(i,j) has a unique positive Nahm solution given by Chebyshev polynomials. Its ordinary Bloch symbol sum is torsion over a totally real number field. The r+1 Andrews–Gordon terminal choices have distinct unshifted q-series but share this A-dependent solution and ordinary class.

## Contents

- `STANDALONE_PROOF.md`: the complete proof, unchanged from the accepted mathematical reconstruction, including all conventions, limitations, and named dependencies
- `AUDIT_REPORT.md`: the complete mathematical audit and bounded exact-check findings
- `ACCEPTANCE.md`: the accepted claims and scope boundary
- `SOURCE_PINS.json`: public scholarly sources, version and inspection history, PDF byte counts and SHA-256 hashes
- `CHECK_SUMMARY.json`: aggregate finite diagnostic results in normal Python, -O, and -OO
- `MANIFEST.json`: the closed inventory of the six authored or metadata payload files, with exact byte counts and SHA-256 hashes

## Scope

The ordinary Bloch group uses the antisymmetric tensor quotient, whose diagonal classes may have 2-torsion. The even diagonal entries of A eliminate these terms. Lee's complementary variables and rationalized quotient are distinguished explicitly, as are extended Bloch groups with logarithm-branch data. No identification of these groups is asserted.

The Andrews–Gordon identity and the Borel–Suslin number-field rank theorem are established dependencies. No novelty, exact torsion order, general Bailey-pair correspondence, or general modularity criterion is claimed. Finite computations are diagnostics rather than proofs at arbitrary rank.

The source problem is AIM Problem 2.4 in [Mock modular forms](https://aimath.org/WWN/mockmodular/mockmodular.pdf), p. 2. The proof gives precise reading pins for every cited dependency. No copied source PDF, source extract, page image, dataset contents, raw computational coefficients, or checker script is included.

The manifest does not hash itself. Its exact bytes are authenticated by the separately retained preparation seal. A manifest alone is an integrity inventory, not an independent mathematical certificate or a self-authenticating trust anchor.
