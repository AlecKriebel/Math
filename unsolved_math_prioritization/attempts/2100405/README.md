# Two rational caustics: scoped obstruction and source audit

This is an AI-assisted, unrefereed mathematical draft. Acceptance means an internal AI mathematical audit accepted the explicitly scoped arguments; it is not human peer review or formal proof-assistant certification. This is a prose proof-and-audit edition, not a computational reproduction package. No novelty, priority, or worldwide-current-openness claim is made.

## Result and exact unresolved target

The original question has two separate existence parts: find smooth closed strictly convex nonelliptic planar tables having two different rational caustics for (I) the Euclidean inner billiard and (O) the outer midpoint-reflection billiard. A rational caustic here means a whole periodic invariant phase circle, not an isolated periodic orbit. Reversing the same inner geometric caustic does not count twice. The source expressly allows the period-two invariant family of a constant-width table.

Both I and O remain UNRESOLVED in this edition. The accepted result is a restricted obstruction: if a C¹ embedded closed curve obeys a constant tangent-offset identity with a rational rigid parameter shift, it must be an ellipse. The proof uses a complete cyclotomic tangent-slope argument and Fourier uniqueness; no analyticity, smallness, finite Fourier cutoff, or first-mode assumption is imposed.

The target is corpus ID 2100405 / AMR-020-0405. The correct source locations are Question 3.7, PDF21 of arXiv:1804.03737v1, and Question 4.7, PDF17 of v2. The original item label Question 4.5 does not identify this question. [Source v1](https://arxiv.org/pdf/1804.03737v1) · [Source v2](https://arxiv.org/pdf/1804.03737v2)

## Complete contents

- [PROOF.md](PROOF.md): all three complete authored arguments. Part I gives the arithmetic lemma, Fourier rigidity, and exact restricted outer application. Part II gives the analytic nonellipse with one period-two caustic, the necessary first-order filter, and the exact paired inner and outer systems. Part III gives the full versioned source-audit appendices.
- [AUDIT.md](AUDIT.md): the independent internal mathematical audit, including hypothesis and scope challenges.
- [ACCEPTANCE.md](ACCEPTANCE.md) and [ACCEPTANCE.json](ACCEPTANCE.json): accepted claims, unresolved questions, and exact document bindings.
- [SOURCES.json](SOURCES.json): public titles and versioned URLs, PDF and text byte identities, retrieval/inspection history, and limits.
- [VERIFICATION.json](VERIFICATION.json): proof provenance, finite-check history, and verification boundaries.
- [MANIFEST.json](MANIFEST.json): all eight filenames and the other seven hashes. The draft-PR body separately pins the manifest itself.

## Why the original questions remain unresolved

General rational outer caustics allow variable tangent offsets and finite-order parameter maps. Conjugating one map to a rigid rotation does not make its offset constant or simultaneously normalize a second map. The obstruction cannot exclude that general setting.

For inner billiards, h(θ)=1+ε cos(5θ), with 0<|ε|<1/24, is a positive-curvature analytic nonellipse of constant width. It has the permitted period-two family and passes the period-three first-order necessary filter. No actual second caustic is established. Exact global nonlinear equations, convergence, convexity, closure, and two distinct rotations still have to be verified for a full construction.

## Versioned source boundaries

The inspected arXiv:1103.5072v1 general sine-ratio lemma and arXiv:2107.03499v1 complex-autocorrelation/real-valuedness inference admit elementary counterexamples. Neither finding refutes a main geometric conclusion. The required Cyr tangent conclusion is independently proved here. The published AMS proof was inaccessible and was not inspected; no claim about its wording is made. No correction, priority, novelty, or worldwide current-openness certificate is asserted.

Only authored mathematical prose and public verification/source metadata are distributed. No copied third-party source documents, extracted source text, source-page images, source code, datasets, or private coordination material are included. Complete retention and hash agreement establish byte identity, not complete inspection or mathematical truth.
