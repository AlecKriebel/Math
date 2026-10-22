# Quadratic Dirichlet moment swaps: scoped audit

AIM Problem 5.1, ID 20000691. Status: **UNSOLVED after five approaches**.
This is partial/expository work, not a claimed new solution or research novelty.

RESEARCH.md preserves the five mathematical investigations: finite-prime arithmetic,
square-diagonal asymptotics, normalized quadratic Poisson summation, shifted
smoothing and conductor transfer, and multiple-Dirichlet-series scope.
ARITHMETIC_REVIEW.md records the independent mathematical review's restricted
acceptance. SOURCE_METADATA.json contains public-source retrieval metadata only;
no source documents, dataset content, or source-text extracts are included.

Accepted partials include the finite-prime law, prime-2 arithmetic-factor ratio,
exact normalized truncated-sieve Poisson identity, elementary square-diagonal
harmonic asymptotic, and a k=1 shifted-Mellin counterexample. Principal swaps
produce the X-scale polynomial and are distinct from a cubic X^(3/4) secondary
term. No all-k central-moment theorem, higher-swap estimate, or rigorous AFE
transfer from length substitution is claimed.

## Reproduction

Python 3 standard library only. From this directory run:

    python3 verify_package.py
    python3 -O verify_package.py

The verifier checks the exact recursive inventory, copies each mathematical
check script to a temporary directory, runs normal and optimized Python, and
compares complete stdout and generated JSON bytes to the committed baselines.
It also rejects eight substantive mathematical mutations in both modes and
six inventory corruptions, including nested manifests, symlinks and unsafe names.
All guards remain enabled under -O. Temporary tests do not modify this package.

The original finite sanity checks were converted from assert statements to
explicit conditional exceptions, with full-program AST equivalence verified by
reversing that transformation. The added identity tests use exact rational
Laurent algebra and finite examples. The Gauss check uses floating-point
complex exponentials with a declared tolerance. Finite enumeration, formal
identities, AST comparison, and mutation tests are not analytic proofs. The
asymptotic proof and qualifications are in the report.

MANIFEST.json binds every other file and directory recursively; its own root
entry is the only exclusion. External receipt hashes bind the manifest itself.
The manifest is an integrity baseline, not a cryptographic signature or proof
that an attacker cannot replace both a file and its manifest.
