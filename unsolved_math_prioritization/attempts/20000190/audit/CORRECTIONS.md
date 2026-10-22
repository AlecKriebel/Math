# Corrections and scope notes

Target: 20000190. Author manifest SHA-256:
43493ad880a6f0a210fe75246301ab81d7575884050b182e63f4e4b71389cf2d.

## Mandatory corrections

None. No counterexample to a stated theorem or exact fixture was established.
The originals remain frozen and unchanged.

## Nonblocking clarifications for any future implementation

1. Rename the reusable `chart_count` function to `affine_chart_count`, or expose
   a projective wrapper. It deliberately omits infinity; the current text and
   test comments disclose that fact. A full-pencil caller must inspect G once.
2. State explicitly that executable exact arithmetic assumes rational input
   coefficients. The sign theorem itself works over the reals; the notation
   Q[z]/(r) and rational congruence implementation require the rational case.
3. Treat an independent pencil and rank-seven design as caller preconditions.
   The verifier is a research fixture, not a validated public input interface.
4. Retain `unclassified` for zero quartics. Do not simplify zero positive-chart
   count to real-camera impossibility without ruling out unclassified roots.
5. Preserve the distinction between matrix calibration, all-point cheirality,
   noisy estimation, pre-candidate checking, and post-candidate RFC.

## Audit-only test development correction

A preliminary audit assertion guessed that the exact t=-1 pole ideal might
retain a degenerate a=0 solution. Direct elimination returned the unit ideal
(1). The audit expectation was corrected before the final replay. This was an
auditor's exploratory expectation, not an error in the author packet. The
final artifact tests the computed unit ideal and preserves the stronger
no-finite-calibration conclusion as an audit observation.
