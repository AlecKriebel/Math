# Five-approach attempt log

Date: 2026-10-04. Status: **unsolved**. The estimates below are heuristic judgments of progress toward the full mathematical target, not calibrated probabilities, and do not count packet preparation as mathematical completion.

## Source and scope checkpoint, 14:45-14:48 UTC

- The catalogue URL was attempted first; live readability failed.
- The pinned selected statement and prior report were read, and the source PDF's exact statement was checked.
- Live repository row, state, attempt directory, ID/title PR searches, branch search, and related-target groups were checked.
- No existing attempt or PR was found. The full global target includes all real parameters and nonhyperbolic cycles.
- Estimated mathematical completion: 5%.

The following five substantive approaches were carried out in this attempt. Symbolic derivation began by 14:48 UTC; the controls completed by 14:51 UTC. The consolidated proof record was written at 14:53-14:55 UTC.

## 1. Scalar return map and Schwarzian geometry

Mechanism: differentiate the flow three times and use fixed sign of C to make 1/sqrt(P') strictly convex or concave. Pair negative auxiliary solutions with positive ones.

Result: a self-contained at-most-one and hyperbolicity proof for e=0,d nonzero; complete no-limit-cycle treatment of d=e=0.

Exact gap: e nonzero makes C indefinite, and the Schwarzian's weighted integral has no proved uniform sign.

Estimated completion toward full target: 10%. Route stops at the indefinite case.

## 2. Reciprocal-square linearization

Mechanism: remove the cubic nonlinearity by z=r^(-2) in the b=c=0 sector.

Result: explicit periodic z, necessary-and-sufficient strict positivity criterion, exact multiplier, and complete handling of a=0 and the equality boundary.

Exact gap: nonzero linear spatial terms produce a square-root term, destroying the linear equation. This subclass cannot replace the target.

Estimated completion: 15%.

## 3. Degenerate Hopf perturbation

Mechanism: weighted small-parameter expansion with a of order epsilon^4, d of order epsilon^2, and radius of order epsilon.

Result: symbolic moments give the order-four rescaled return polynomial; two simple positive zeros persist analytically, with unstable inner and stable outer cycles. Thus at least two cycles are rigorously reproduced for sufficiently small epsilon.

Exact gap: no exclusion of distant cycles. The lower bound is known in the literature, so reproducing it is a control, not a new solution.

Estimated completion: 15%.

## 4. Global pairwise identities and parameter monotonicity

Mechanism: period integrals of reciprocal/logarithmic coordinates, exact Floquet exponent, difference of two periodic radii, and monotonicity with respect to a.

Result: necessary equations (9)-(12) in PROOF.md. Three cycles force cancellation against a positive weight, which is compatible with sign-changing C. Trace-parameter monotonicity is proved but does not count identity crossings.

Exact gap: a global weighted-oscillation or displacement-zero bound is missing. Promoting this to a proof would be circular.

Estimated completion: 10% after recognizing the global obstruction.

## 5. Reproducible numerical falsification probe

Mechanism: Poincare shooting with the first variational equation, exact controls, tolerance refinement, and a seeded bounded indefinite-parameter scan.

Result: correct center and exact one-cycle controls; two roots with correct stability for three small-parameter controls. The 24-vector scan found no three-root candidate, but 227 sampled flows were incomplete. All parameters and results are retained.

Exact gap: ordinary floating point and sign-change bracketing do not exclude tangent, missed, large-radius, or near-boundary cycles. No validated global search or interval certificate was produced.

Estimated completion: 10%. Full target remains unsolved after the fifth approach; no sixth proof-search approach is included.

## Final checkpoint, 14:55 UTC

The 2024 Gasull survey was downloaded and its explicit open-status page visually checked. Source and computed artifacts were separated. A safe authored packet was frozen for fresh independent audit before any remote write. Independent verification is a separate gate; this log does not claim it has passed.
