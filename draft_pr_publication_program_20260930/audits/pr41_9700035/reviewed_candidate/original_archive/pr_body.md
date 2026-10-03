## Scoped partial result; original target remains unsolved

This package proves the expected in-square spanning-network length is asymptotic to ell·k under the usual SIRSN axioms. It also proves the full, untruncated asymptotic under the extra condition t^4 P(D1>t)→0, in particular when the unit-distance route length has finite fourth moment.

The proof separately controls the exterior: a dyadic major-road intensity estimate handles bounded excursions, while a pair-route tail estimate handles the far exterior. It includes the Poisson-to-binomial conversion. The first-moment assumption in the original axioms has not been shown to imply the added tail bound, so the unconditional problem remains unresolved.

## Exact source corrections

Span is the union of all prescribed pairwise routes, not a Steiner-minimal subnetwork. Ell is the edge intensity of the rate-one Poisson sampled network. The source is Open Problem 35 in the 2012 manuscript, but Open Problem 9 in the published 2014 paper, which explicitly asks which extra assumptions, if any, suffice. The historical imported report is preserved alongside these corrections.

Current model and geodesic literature is credited with its precise scope. No historical-priority or full-solution claim is made.

## Review and checks

The separate adversarial review passed the precise conditional scope, with 3,809 independent exact controls, and is included before this draft opens. The author checker passes 211 exact algebraic/distributional controls. These are finite diagnostics, not a SIRSN simulation or a verification of the missing general case.

Run: `python3 unsolved_math_prioritization/attempts/9700035/verify.py` with SymPy 1.14.0.

Actual research model: gpt-6-astra at xhigh. Two substantive attempts, then a precise stop at the distant-excursion integrability gap. Recommended queue status is unsolved; the coordinator handles the queue row.
