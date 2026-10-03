# Research note for Kirby Problem 5.17

**Unresolved, five substantive attempts.** No general solution, first-resolution claim, or human peer-review claim is made.

The note proves elementary sufficient conditions and supplies explicit checks on two tempting approaches:

- Two Weinstein structures on a fixed compact symplectic annulus have an exact primitive difference, yet their affine midpoint has a periodic orbit and admits no Lyapunov function. An explicit alternative homotopy connects them, so this is not a counterexample to the original problem.
- Complete fixed-form Weinstein homotopies on T*S¹ can change the cohomology class of the difference of primitives.

The remaining gap is identified in PROOF.md. SOURCE_GATE.md records primary-source inspection and its limits; RESEARCH_LOG.md records all five approaches.

## Reproduce

Requires Python 3, standard library only. Run from this directory:

    python3 verify.py
    sha256sum -c SHA256SUMS

The verifier writes deterministic verification.json and checks 44 exact identities or rational bounds. It performs no numerical search. It does not prove the universal homotopy assertion or formally verify external theorems.

The author packet is frozen for an independent mathematical audit. Audit completion is not asserted by this version. Source PDFs and raw research records are not part of this packet.
