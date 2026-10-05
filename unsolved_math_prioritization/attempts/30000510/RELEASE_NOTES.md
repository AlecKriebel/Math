# Baby Teichmüller space: attributed prior result, singular scope

Rank 657, ID 30000510, OWR-1275-010. Disposition: **already_solved / prior result verified, singular scope only**, with **one substantive approach out of five**. This draft package records a reconstruction and independent adversarial audit; it makes no novelty, historical-priority, human-peer-review, or formal-machine-proof claim.

## Result and credit

For every integer n >= 3, there are exactly n-1 connected and path components. For every constant abelian coefficient group A, ordinary singular cohomology is A^(n-1) in degree zero, has one additional A in degree n-3 when n is even, and is zero in every other positive degree. Singular homology has the same degree pattern. The result is already present in Alper Ferudun, *Components and Cohomology of Fock's Baby Teichmüller Space*, version 1.0, 1 October 2026, [DOI 10.5281/zenodo.23071801](https://doi.org/10.5281/zenodo.23071801), Theorem 1.1(iv) and its inspected proof dependencies. The public manuscript is unrefereed and discloses AI-assisted preparation.

The original problem is Fock's Problem 6, printed page 1607 of [Teichmüller Space (Classical and Quantum)](https://ems.press/journals/owr/articles/1275), Oberwolfach Reports 3 (2006). It leaves the cohomology theory and coefficients unspecified. The audit approves ordinary singular (co)homology only; no Čech, sheaf, de Rham, compact-support, twisted-local-system, orbifold/stack, or all-theories conclusion is asserted. Additional claims elsewhere in the prior preprint are not certified here.

## Two nonblocking wording clarifications

1. The original source does not print n >= 3. That is the nonempty positive-integer range inferred from its requirement of at least three image points. For n = 1,2 the space is empty; no n = 0 claim is made.
2. In the frozen proof's n = 4 example, read “singular homotopy type” as **weak homotopy type**. The theorem already states the correct weak conclusion. The strong deformation retraction concerns the normalized slice alone. No strong homotopy equivalence of the potentially non-Hausdorff quotient is claimed.

## Immutable history and current audit decision

The ten author files and their original archive/manifest are byte-for-byte unchanged. The eight safe audit files and their original archive/manifest/binding are also unchanged. Historical statements that an audit or publication is pending describe the frozen author checkpoint; the later [audit decision](audit/AUDIT_RESULT.json) is PASS for the precise singular scope above. The complete [audit](audit/AUDIT.md), not merely its verdict, is included.

The draft changes only this problem's Status, Turns, and previously blank Findings cells in QUEUE.md. Every other cell, row, link, and the existing malformed embedded header are retained. No queue regeneration, merge, release, new DOI, or outreach is part of this package.

## Reproduction

From this directory run:

    python3 -B verify_release.py

Python 3 and its standard library suffice. The release verifier rejects optimized execution, checks every package file and both archives, pins the original author/audit identities, and replays both independently authored finite-control programs with exact byte comparison. No network requests are made. Finite tests supplement the universal proof and are not a proof by enumeration.

For isolated archive replay, copy author-packet.zip and audit-packet.zip into the same empty directory, extract both there while retaining the archives, then run:

    python3 -B audit/verify_audit.py --author-root .

Only authored mathematics, local code/results, full safe audit, and public verification metadata are included. No scholarly source text/PDF/archive, dataset content, credentials, private source, or private coordination file is distributed.
