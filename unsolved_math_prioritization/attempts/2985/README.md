# Kirby Problem 4.109: a connected counterexample candidate

**Status: complete candidate counterexample, separate review pending.**
One substantive attempt has been used. Historical novelty is unconfirmed.

[CANDIDATE.md](CANDIDATE.md) constructs a connected genus-three symplectic
surface in a free quotient of the four-torus, with integral symplectic class
equal to the surface's Poincaré dual. The complement has a connected double
cover with nonzero third homology, obstructing every Weinstein structure.
This is a proposed negative answer to the prescribed-surface question,
including a connected surface and degree one. It does not decide whether
some different degree-one surface in that manifold has Weinstein complement.

The construction builds on Auroux's disconnected examples as presented by
Giroux. [SOURCE_AUDIT.md](SOURCE_AUDIT.md) records the exact original scope
and attribution. [readiness.json](readiness.json) records the prior-attempt
gate, actual model and remaining review requirement.

Run `python verify.py` from this directory. Its 13,236 exact assertions
check affine equations, orientations, exterior products, the local smoothing
formulas and elementary quotient arithmetic. The expected output is
[verification.json](verification.json). The checker hashes the frozen proof;
retain `CANDIDATE.md` beside it. The finite controls supplement the written
topological proof and do not certify it by themselves.

No source PDFs are redistributed in this package. No first-discovery or
human peer-review claim is made.
