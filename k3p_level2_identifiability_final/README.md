# K3P Level-2 Identifiability: Final Certification and Paper

This directory is the canonical local workstream for independently replaying,
certifying, writing, and releasing the K3P level-2 identifiability result.

The cloud-stage conclusion was treated as a hypothesis, not an assumption.
The local exact and rigorous-interval program has now independently certified
the mathematical outcome **K3P-SAME**.

All source inputs are immutable copies under `input_frozen/`.  Reproduction
commands and final verification entry points live under `reproducibility/` and
must not depend on paths outside this project root.

The active evidence set is defined only by `ACTIVE_MANIFEST.json`.  Failed,
superseded, or exploratory artifacts belong under `history/` and are not active
proof evidence.

The fail-closed integrated gate freshly replays the 28/28 primary chain, the
14 four-port orbits and `38+2` census, weak-not-strong Krawczyk sharpness,
ordinary/optimized/adversarial strong-class cut transfer, global analytic
infrastructure, all 574,535 one-/two-port probe rows, and complete fixed-full
K3P restoration.  Restoration has 36,568 minimal active K3P terminal rows;
36,792 is the distinct retained legacy/full-forest leaf census, with 32 legacy
continuations and 256 redundant depth-two edges.  The standalone restoration
replay imports no producer code and all 20 mutations are rejected.

The theorem is certified on both `D_{3,+}` and the strict continuous-time
domain.  For necessity, strict CT is an open full-dimensional subset of
`D_{3,+}` (`c=yz`, `g=xz`, `t=xy`), so every CT containment witness is a
principal-domain witness.  Strict-CT sufficiency uses the common relative
rank-14 `H14` triangle germ and simultaneous physical gluing; it does not use
an ambient-rank-15 triangle argument.

The former universal arbitrary-network pointwise cut-rank equivalence remains
withdrawn and unused.  The active theorem is the directional strong-class
cut-set equality under containment, and no proper one-sided containment occurs
inside the strong class.

Reproduce the mathematical promotion with:

```text
.venv/bin/python reproducibility/verify_k3p_same_classification.py
.venv/bin/python reproducibility/test_k3p_same_classification_mutations.py
```

This certification is not a submission-readiness claim.  The manuscript,
reader supplement, canonical PDFs, visual QA, deterministic archive tooling,
and fail-closed release checks are complete.  Exact-HEAD execution records live
under the ignored release work/transcript paths; journal packages remain
deliberately `NOT_READY` until their human metadata and upload artifacts are
supplied.  No DOI, license, submission, peer review, or completed human review
is claimed.
