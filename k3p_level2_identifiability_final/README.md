# K3P Level-2 Identifiability: Final Certification and Paper

This directory is the canonical local workstream for independently replaying,
certifying, writing, and releasing the K3P level-2 identifiability result.

The cloud-stage conclusion was treated as a hypothesis, not an assumption.
The local exact and rigorous-interval program has now independently certified
the mathematical outcome **K3P-SAME**.

Precisely, the structural equivalence requires equality of the labelled reduced
trees of blobs; corresponding complete factors must be labelled mixed-graph
isomorphic or ordinarily triangle-redirected, with coherent boundary
transports.

All source inputs are immutable copies under `input_frozen/`.  Reproduction
commands and final verification entry points live under `reproducibility/` and
must not depend on paths outside this project root.

The active evidence set is defined only by `ACTIVE_MANIFEST.json`.  The frozen
cloud-stage separator and its verifier (`input-023` and `input-032`) are
retained as provenance but explicitly excluded from active proof evidence;
the literal-map v2 separator replaces them.  Failed, superseded, or
exploratory artifacts belong under `history/` and are not active proof
evidence.

The fail-closed integrated gate freshly replays the 28/28 primary chain, the
38 raw records in 14 canonical four-port orbits plus two separately
quartic-separated sink swaps (`40=38+2`), the base weak-not-strong Krawczyk
certificate and all-`n` cherry extension,
ordinary/optimized/adversarial strong-class cut transfer, global analytic
infrastructure, all 574,535 one-/two-port probe rows, and complete fixed-full
K3P restoration.  Restoration has 36,568 minimal active K3P terminal rows;
36,792 is the distinct retained legacy/full-forest leaf census, with 32 legacy
continuations and 256 redundant depth-two edges.  The standalone restoration
replay imports no producer code and all 20 mutations are rejected.

The sharpness result is existential and exact: for every `n>=3` there are
labelled nonisomorphic, non-triangle-equivalent networks in
`W_TC\S_TC` whose strict-continuous-time images share a full-dimensional
regular germ of dimension `6n-3`.

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

This certification is not a submission-readiness claim.  The revised
manuscript, reader supplement, canonical PDFs, and page-by-page visual QA are
complete, and the deterministic fail-closed release tooling is implemented.
Its targeted-revision exact-HEAD quick/full/all-producer execution and archive
rebinding remain pending.  Execution records live under ignored release
work/transcript paths; journal packages remain deliberately `NOT_READY` until
their human metadata and upload artifacts are supplied.  No DOI, license,
submission, peer review, or completed human review is claimed.
