# Marked one-sample r=2 branch: research log

Date: 2026-08-08 (America/Los_Angeles)

## Exact lift

- Introduced the midpoint marked measure
  `lambda_v=(sigma_v+nu_v)/2` and proved that it is stationary for a
  one-sample chain on `(C,v)`, where `v` is a marked hole.
- The chain samples `i~P_v`; a fair coin either keeps target `v` after
  adjoining `i`, or chooses a uniform occupied site as the next target and
  deletes it.  This removes the geometric burst from the transition rule.
- Proved the exact rank law
  `2 Lambda_k=(k+1)pi_(k+1)+k pi_k`.  The normalized complete marked law is
  exactly `Bin(n-1,1/2)`, and the active-event size law is
  `1+Bin(n-2,1/2)`.
- Identified the target as a literal collision probability: conditional on
  a stopping step, the probability that the new target is the just-sampled
  site is `1/m`.  Including the stopping coin gives total probability
  `1/(2m)`.
- Derived the alternating rank observable `psi` whose marked stationary
  expectation is exactly `1/m`, and the complete Poisson comparison (15) in
  the companion note.

## Hostile rank screen

- The strong conjecture that the active-event rank is stochastically
  dominated by `1+Bin(n-2,1/2)` passed the exact historical corpus: 54
  connected weighted triangles, 624 connected four-vertex graphs, and 48
  deterministic sparse/extreme five-vertex graphs.
- A directed/reversible floating search found a six-vertex violation.  It
  was simplified to the complete-support integer graph with lexicographic
  edge weights
  `(1,3,3,1000,30,1000,300,3,1,10,1,30,1,300,30)`.
- A full exact 62-state solve proves that the event-rank tail at two exceeds
  the complete tail by `0.001463330069...`.  This exactly closes the
  stochastic-domination route.
- The same solve gives `m=2.305291055...<80/31` and harmonic collision slack
  `0.046284704868...>0`.  It is not a fixation counterexample.

## Universal two-step theorem

- For every loopless row-stochastic kernel, proved an exact formula for
  `U M_P^2 t^K-U t^K` as a nonnegative combination of two graph defects.
  The first is `sum_(vi) P_(vi)^2-n/(n-1)`.  The second is
  `sum_i(column_i-1)^2+(1/2)sum_(vi)(P_(vi)-P_(iv))^2`.
- The two coefficients are explicitly nonnegative on `0<=t<=1`.  Integrating
  the formula and using the fact that one marked step annihilates rank parity
  proves `U M_P^2 psi>=U psi=1/m_K`, strictly off the complete kernel.
- The identity is valid without reversibility and has been independently
  checked by exact marked-state enumeration on rational directed kernels.
- Long-time monotonicity is false: extreme reversible kernels can have
  `U M_P^t psi` decrease at late times.  The surviving conjecture is the
  lower-envelope promotion `(lambda/m)psi>=U M_P^2 psi`, not monotonicity.

## Current boundary

The marked lift replaces the nonlinear geometric chain by a linear
single-sample chain, and the complete law is now a strict two-step global
minimum for the exact target observable.  The sole remaining step is to
promote this two-step lower bound to the stationary marked law.  A proof must
use time-homogeneous target/sample flow, a marked-chain tree theorem, or a
genuinely global collision/return-time inequality.  The exact universal r=2
upper bound remains open.
