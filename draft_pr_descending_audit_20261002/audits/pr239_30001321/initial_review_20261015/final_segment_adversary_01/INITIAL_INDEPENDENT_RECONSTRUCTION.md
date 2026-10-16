# Independent final-segment reconstruction

Recorded 2026-10-15 04:20 UTC. This record precedes reading any submitted
`independent_review` verdict or any other audit lane's opinions. Only
`PROOF.md`, `TURN_1.md`, `TURN_2.md`, and `check_turn3.py` have been read.

Scope: PR239, frozen head 7f17eef77c52b2d9b2ec3ad0803c016267fa6496,
problem 30001321 / OWR-4081-005. No priority or publication-status conclusion.

## Claim reconstructed

For each fixed iid law supported in (0,1), every deterministic diverging
interval length M_N and deterministic alignment, the environment tail of
the endpoint coarse L1 error above a fixed epsilon is O(N^-K) for every K.
The N threshold may depend on the entire selected M_N sequence. Constants
may depend on the fixed law; there is no uniform near-arrow assertion.

## Mechanism and sufficient inputs

1. A conditional occupation estimate for the replica overlap gives a single
   high-probability old-environment bound on sum_{s<m} I_s. Applied to a
   finite, prescribed family of Lipschitz interval majorants, the exposure
   martingale then makes each old-law strip weight at most N^-1/32 with
   superpolynomial failure probability. Relevant exponents are variance
   N^-7/32, deviation N^-1/32, and exponential power N^5/32.
2. Same-parity walks can be coupled in a common fresh environment by using
   independent coins until meeting and common coins afterward. Their
   annealed half-gap, before meeting, is homogeneous symmetric lazy with
   move probability q(1-q). Its survival bound C d/sqrt(ell) controls the
   expected L1 distance between two fresh kernels started within one
   auxiliary H-cell. This does not use delta in the gap before meeting.
3. Replace the old law inside H-cells by the annealed conditional law,
   retaining the old cell weights. The replacement differs from alpha_m
   in L1 by precisely the H-coarse discrepancy, while fresh evolution
   erases the within-cell replacement at expected cost C H/sqrt(ell).
   The earlier all-diverging-scale expected coarse bound applies to a
   mixture of translated fresh kernels, uniformly in target alignment.
   Thus the conditional expected target error is small, even for an
   arbitrarily slowly diverging M_N.
4. Kill a path from x when it leaves |X_{m+t}-x-vt| <= R. Fresh environment
   strips are determined by floor((y-vt)/R), so they are disjoint finite
   independent vectors even for irrational v. Every surviving path uses
   only strips meeting [x-R,x+R]. A strip change can change survival, but
   cannot affect any killed path kernel outside this starting-site
   influence interval: every path contributing to either killed kernel
   remains in the same deterministic tube. For affected starts, arbitrary
   subprobability kernels differ by at most 2 in L1. This supplies a
   strip oscillation at most 2 mu_m(J_k), including changed killing sets.
5. Conditional bounded differences gives upper tails exp(-c t^2/max w_k)
   because sum w_k <= 6. The unrestricted-minus-killed output is a
   nonnegative measure whose L1 norm equals lost mass. Its conditional
   expectation is at most exp(-c log^2 N), by an annealed maximal path
   inequality. Markov restoration is therefore superpolynomial.

## Initial mathematical assessment and outstanding checks

No central gap is apparent in this reconstruction. In particular, the
moving-strip argument does not require endpoint-cell independence or
independence of overlapping starting cones. The independent inputs are
environment vectors, conditional on the old environment. The H comparison
can use the earlier theorem with the fixed exponent 5/16, since H >= m^5/16.

Still to be checked independently: complete exact reproduction; negative
controls for opposite parity and endpoint-only killing; strip enumeration
with irrational tilt and site/time boundary contact; arbitrary changes of
one strip and support changes; restoration and replacement with clipped or
null parity cells; real target lengths; slow-M quantifiers; near-arrow
fixed-law constants. Finite computations will be labeled controls, never
an asymptotic proof.

Best-guess completion of this assigned adversarial audit: 35%.
