# Kirby Problem 5.17: reviewed partial investigation

**Status: unsolved, 5/5.** This packet does not solve or refute the general fixed-symplectic-form Weinstein-homotopy question. No novelty or human peer-review claim is made.

The [preserved research note](artifacts/PROOF.md) gives five substantive approaches, elementary sufficient conditions, a fully explicit failure of the affine-interpolation shortcut, and the precise remaining gap. Its compact-annulus endpoints have an exact primitive difference and a periodic affine midpoint, but an alternative Weinstein homotopy connects them. This example is therefore not a counterexample to the original question. Complete fixed-form cylinder homotopies also show why the cohomology class of a primitive difference alone is not an obstruction.

A [separate mathematical audit](audit/AUDIT.md) accepted the partial results with two minor bibliographic findings, recorded in [ERRATA.md](ERRATA.md). The audit's full report and exact replay output are included. The frozen author README and STATUS retain their historical pending-audit labels; the completed report records the later review. Nothing in the audit upgrades the problem's status.

## Reproduction

Python 3, standard library only:

    cd artifacts
    python3 verify.py
    sha256sum -c SHA256SUMS
    cd ../audit
    sha256sum -c SHA256SUMS
    cd ..
    sha256sum -c PUBLICATION_SHA256SUMS

The author verifier and audit replay both pass 44 exact assertions with byte-identical JSON. These are algebraic and rational-bound checks, not formal verification of the complete proofs or a universal classification.

Only this problem's public mathematical packet is added. The queue change is limited to its status and turn cells. Source PDFs, source-text copies, corpus data and private research records are excluded. This is a draft for human review.
