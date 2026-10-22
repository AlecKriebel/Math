# Research log: 9700042 / AMR-096-0042

## 2026-10-07: supported author budget and scope

The supported author-attempt count is five: one historical approach followed by
C1, C2, C3, and C4. This records the budget used, not a reconstruction or fresh
authentication of unavailable historical manuscripts. C2 and C3 are excluded
from this proof packet because they are unnecessary to the accepted argument.
No additional proof search is performed by packaging or finite replay checks.

## 2026-10-07T14:16:05Z: partial C1 audit

The C1 audit accepts the upper bound with normalized limsup at most e/2. It
checks exact directed planar duality and marked-list counting, and supplies an
optional clarification patch. C1 alone does not establish the sharp constant.
Proof-goal completion estimate at that checkpoint: 70%, a subjective planning
estimate rather than a probability of correctness.

## 2026-10-07: revised C4 and two full-scope audits

The revised C4 combines the stronger marked-edge/backtracking budget, sparse
fixed-box convergence, classical Poisson-chain inputs, first-hitting skeletons,
and disjoint closed-edge witnesses through BK. It supplies both the upper bound
and a fresh lower bound. The original-to-revised patch corrects local indexing,
inequality, rectangle-positivity, and mean-convergence presentation points.

Full audits A and B accept the exact 20,646-byte revision with SHA-256
`8da7cf366948e8d4fc63e3399cc4fe804ed786ea99b01479619efbdbacfedf3a`.
The full canonical asymptotic is the claimed result. The finite C1 prerequisites
and explicit external probability inputs remain visible dependencies.
Proof-goal completion estimate: 100% of the scoped authored argument has been
accepted by both audits. This is not a probability of correctness or a claim
of human peer review, formal verification, novelty, or exhaustive literature
coverage.

## 2026-10-07: focused publication checkpoint

Frozen originals, revisions, actual patches, all three mathematical reports,
their manifests, five finite checkers and expected outputs, and public source
pins form the packet. A separate verifier authenticates files before execution,
keeps assertions active under optimization, replays patches, and tests negative
controls. Finite replay is diagnostic and does not establish an infinite-volume
theorem. The current README controls interpretation of historical status text.
Package-preparation completion estimate: 100% after the recorded successful
replay; remote publication verification is reported separately by the PR.
