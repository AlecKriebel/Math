# Problem 6200007: prescribed boundaries of convergence actions

**Disposition: unresolved, five substantive author attempts.**

This AI-assisted research packet studies Kapovich's Problem 7, rank 548,
AMR-061-0007. It supplies complete proofs of scoped reductions and failed
construction mechanisms. It does not solve or refute the general problem,
and makes no historical-priority claim. Independent adversarial review is
required before any promotion of the claims.

## Main useful result

Every finite-orbit invariant annulus/triple-graph construction for the
PSL_2(Z) action on RP^1 has a bounded parabolic orbit and cannot have a
boundary equivariantly homeomorphic to RP^1. The same original action does
have its usual isometric realization on H^2. Consequently this result
locates a failure in the construction, not in the question.

This deduction builds on the established Bowditch-Sun construction and
Azemar's finite-boundary mechanism. It is explained and proved in TURN_4.md.

## Reading order

- RESULT.md: strongest scoped theorem and the unresolved original target
- SOURCE_GATE.md: identity, primary statement, literature and prior-work scope
- TURN_1.md: finite cases; countability, finite kernel and perfection reductions
- TURN_2.md: credited sufficient annular criterion and explicit graph bounds
- TURN_3.md: equicontinuity obstruction and exact failure of fixed-height lifts
- TURN_4.md: finite-annulus theorem, modular cusp, and positive H^2 control
- TURN_5.md: infinite-annulus and metric-aggregation failures; precise open gap
- ATTEMPT_LOG.md: the five distinct routes and their outcomes
- CLAIMS.json: machine-readable scope, without a full-solution label

## Reproduction

Run `python3 verify.py` from this directory. The standard-library-only script
prints a deterministic JSON report. `python3 verify.py --write` also writes
CHECKS.json. The checks use integers and rational arithmetic; they do not
replace any infinite, compactness, or boundary proof.

Run `python3 verify_manifest.py` to verify the frozen public author files.
SHA256SUMS.json intentionally excludes itself. Source PDFs, primary-source
text extractions, catalogue corpus files, and private preparation records
are excluded from the public packet.

This packet records author findings, not human peer review or formal
verification. The original target remains unresolved.
