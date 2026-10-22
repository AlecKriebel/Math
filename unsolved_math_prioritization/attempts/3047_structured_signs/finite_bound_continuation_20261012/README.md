# Explicit finite bounds for partition digit signs

12 October 2026. For every ternary-digit or base-four-digit assignment of signs in every original unrestricted-partition factor, some total product coefficient lies outside \(\{-1,0,1\}\) in degrees 1 through
\[
150\,994\,944=36\cdot2048^2.
\]
This explicit coefficient-only upper bound is deliberately conservative and is not claimed to be sharp. It supplements the preceding full-family exclusions by controlling the unknown coefficient tail beyond a finite good prefix. The unrestricted independent-sign problem remains unresolved by this work. No novelty or priority claim is made.

## Families covered

The total product is \(\prod_{m\ge1}F_m(q)\), with every positive integer factor present. Either
\[
F_m(q)=\prod_{j\ge0}(1+u_{m,j}q^{m3^j}+v_{m,j}q^{2m3^j}),
\qquad u_{m,j},v_{m,j}\in\{-1,1\},
\]
or
\[
F_m(q)=\prod_{j\ge0}(1+a_{m,j}q^{m4^j}+b_{m,j}q^{2m4^j}+c_{m,j}q^{3m4^j}),
\qquad a_{m,j},b_{m,j},c_{m,j}\in\{-1,1\}.
\]
Every indicated digit sign is free, and no finite cap on noncyclotomic blocks is imposed. Unique base expansion makes every original local coefficient a sign. Arbitrary independent signs on all original local coefficients are a larger class that the theorem does not cover.

## Complete reading order

1. [Acceptance and exact scope](ACCEPTANCE.md) states the theorem, its dependencies and its limitations.
2. [Full finite-bound proof](FINITE_COEFFICIENT_OBSTRUCTIONS.md) derives the elementary partition bound, the unknown-tail estimate, both strict-margin estimates, exact envelope inflation and the complete-search contradiction.
3. [Full substantive independent review](REVIEW_FINITE_COEFFICIENT_OBSTRUCTIONS.md) retains the analytic, algebraic, complete-state and sanitized-replay checks.
4. [Machine-readable acceptance summary](ACCEPTANCE_REPORT.json) records the same theorem, constants, aggregate counts and verification scope without identifying undistributed computational artifacts.
5. [Correction history](CORRECTION_HISTORY.md) explains exactly what the finite bound adds and how the earlier endpoints must be read.
6. [Dated source scope](SOURCE_SCOPE.md) identifies the original question and distinguishes public context from the authored mathematical dependencies.

## How the finite bridge works

The universal estimate \(|A_n|\le p(n)\le e^{3\sqrt n}\) bounds the unknown squared-norm tail at each of 21 fixed rational radii strictly below \(2^{-73717}\). A good prefix through the stated cutoff therefore satisfies the earlier Jensen upper envelopes enlarged by \(\eta=2^{-32768}\).

Every strict old rejection has margin greater than \(2^{-31318}\) in the ternary case, by an explicit integer norm in the golden-ratio field, or greater than \(2^{-31780}\) in the base-four case, by rational denominator bounds. Thus inflation removes no old rejection and creates none. The complete retained searches are unchanged: 831,371 ternary states and 11,151,089 base-four states, with first empty combined frontiers at 59 and 77. These endpoints are not asserted to be sharp coefficient-only failure thresholds.

## Dependencies and computational evidence

This appendix depends on the earlier general interior-zero proof, the full-ternary proof and review, and the full-base-four proof and review. Those appendices provide the original exact recurrence, complete state domains, deferred-choice realization arguments, zero classifications, and exhaustive search evidence. The present appendix proves the finite-tail extension; it does not replace or silently strengthen those earlier proofs.

The accepted historical audit compared complete retained state streams, not merely totals. It independently checked exact inflation and all domain-wide separation bounds, and fresh sanitized replays reproduced all retained states and diagnostic output. The full review explains the parameter controls and why rejecting an uncertified parameter choice is not a claim that its mathematical conclusion is false.

Programs, raw state certificates, detailed computational records and copied third-party sources are not distributed in this appendix. The complete proof and substantive review support independent reimplementation, but this is not an executable public replay package. The [manifest](MANIFEST.json) authenticates only the distributed files; it is not independent evidence of exhaustive search.

The mathematical review is AI-assisted and unrefereed. It is not external human peer review, journal acceptance or proof-assistant certification. No unrestricted impossibility, unrestricted finite-search record, general unboundedness of coefficients or sharpness of the explicit cutoff is claimed.
