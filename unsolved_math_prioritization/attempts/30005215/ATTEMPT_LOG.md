# Attempt log

All times UTC on 2026-10-04. One substantive author turn used out of five.
Percentages are rough progress estimates, not probabilities of mathematical truth.

## Turn 1: source recovery, prior resolution, and complete robust proof

- 07:04-07:07: Catalogue fetch failed with HTTP 403; recovered the exact record
  from the pinned public dataset. Read the full Lorenz contribution. Checked
  actual repository paths/PRs separately from the queued row. Progress: 25%.
- 07:05-07:10: Located matching primary articles by Bresch, Lorenz, Schneppe,
  and Winkler, verified latest arXiv versions, and read the convergence proofs
  and their needed hypotheses. Confirmed that both questions have been treated
  since the report. Detected specific rank-one and probability-bound problems
  in the inspected mismatch proof; did not accept generated or abstract-only
  resolution claims. Progress: 55%.
- 07:10-07:15: Wrote a self-contained compact random-plane formulation with
  at-most-2-by-2 singular-value maximization. A direct uniform-cap lemma gives
  almost-sure norm convergence without exceptional-denominator claims,
  singular-value assumptions, or a stationary-point argument. Covers zero,
  rank-one, repeated singular values, and dimensions one. Credited the prior
  authors; no novelty claim. Progress: 90%, subject to independent review.
- Verification: 600 exact rational identities, 600 geometric floating-point
  identities, and 11 bounded numerical tests passed. These tests check algebra,
  oracle restrictions, call counts, and degenerate behavior; the written proof
  establishes convergence. Public packet frozen for independent review.

## Approach accounting

The five-turn budget is a maximum, with early termination on full or prior
resolution. Only one substantive turn is charged. The source check found prior
papers that match both target questions, and the packet provides a complete
proof without relying on the identified proof cautions. Further attempts to
invent a new answer would be inappropriate. No fabricated turns are counted.

The main mathematical mechanism is compact random-plane maximization. The
single-oracle Gram-matrix specialization and the asymmetric bilinear 2-by-2
SVD implementation are treated in the same theorem-level investigation.

## Remaining work and limits

Independent adversarial review and authorized publication remain. There is no
remaining analytic gap in the finite-dimensional exact-oracle theorem claimed
here. Efficient high-dimensional rates, deterministic stopping certificates,
floating-point certification, arbitrary infinite-dimensional operators, and
full convergence of every proposed stochastic-gradient schedule are outside
this result. Qualified expert review remains necessary.
