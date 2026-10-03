# Research log

All times UTC, 3 October 2026. Completion percentages are informal estimates of this investigation's deliverable, not probabilities of mathematical correctness.

## Source and readiness checks, 14:09–14:14

Recovered the target from the official Oberwolfach report after the catalogue page was inaccessible. Verified the precise threshold and the empty-to-negative-energy path class. Checked the live queue and prior-attempt sources. Found no genuine duplicate attempt. The catalogue's stale minimal-surface/open summary does not accurately describe the target.

Located Mazurowski–Zhu's February 2025 preprint and verified the direct strict-width argument in the proof of Theorem 4.3, with its sweepout input Proposition 2.1. Discovered the printed difference between its weighted-C³ decay assumption and the original referenced preprint's unweighted smooth convergence. A direct citation without addressing that mismatch would be incomplete.

Checkpoint: source reconstruction 100%; candidate proof and scope verification 45%.

## Substantive attempt 1, 14:14–14:23

**Mechanism.** Derive the original-convention statement from the known smooth point-emerging inverse mean curvature flow theorem by transplanting increasingly large, increasingly Euclidean metric neighborhoods into one fixed auxiliary weighted-C³ asymptotically flat metric. Use uniform annulus bounds to trap a flow inside a neighborhood where scalar curvature is nonnegative. Transfer that flow back isometrically.

**Main checks.** The auxiliary metric is complete and satisfies the later theorem's precise derivative assumptions. No global scalar-curvature sign is asserted for it. The smooth-flow theorem, spatial bounds, and initial Hawking-mass limit do not require such a sign. Nonnegative scalar curvature is used only on the trapped flow; the strict equality case is ruled out by non-flatness at its initial point. Pointwise strict isoperimetry becomes a strict mountain-pass maximum by continuity on a compact parameter interval. The Euclidean normalization and negative-endpoint requirement are checked separately.

**Outcome.** Complete source-dependent affirmative candidate saved in `PROOF.md`; search stopped at 1/5 rather than inventing four unnecessary attempts. Its principal input already appears in the 2025 literature. No novelty claim is made. Both the source application and the original-decay transplantation reduction require a fresh independent audit before closure.

**Blocked/rejected shortcut.** Quoting only the CMC existence theorem would not establish the requested width inequality. Quoting only Proposition 2.1 would leave the derivative convention unexplained. Trying to repair the metric separately near each point would give uncontrolled point-dependent regularity thresholds. The single fixed auxiliary metric avoids that quantifier error.

**Verification limits.** Exact algebra controls check normalizations and elementary identities only. They do not establish geometric regularity or replace review of the analytical proof. No exhaustive numerical search was run.

Checkpoint: candidate deliverable 100%; independent audit pending. Status proposed after a successful audit: credited literature-based `already_solved`, 1/5. Until then the broader original-convention result remains a candidate.
