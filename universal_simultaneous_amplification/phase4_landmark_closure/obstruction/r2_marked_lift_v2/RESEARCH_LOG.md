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

## Perron density reduction and hostile envelope audit

- Factored the marked transition as `M_P=A_P R`, with a fixed
  continue-or-retarget channel `R`.  Relative to the complete active law,
  the stationary active density is the Perron vector `g=T_P g` of an
  explicit positive operator `T_P=B_P Q`.
- The size-weighted mass of `g` is fixed.  The collision target is its
  unweighted mass.  Thus complete maximality is exactly `sum g>=|Y|`, and
  the two-step promotion is exactly `sum g>=sum T_P^2 1`.
- This exposes the indispensable coupling: `P_vi` must be the same for all
  cache states with target `v`.  Allowing state-dependent rows gives a
  finite linear-program counterexample with stationary target `1/(n-1)`.
- Exactified a reversible rational `K5` on which `U M_P^t psi` strictly
  decreases at a late time, and a separate reversible rational `K5` on
  which the stationary lower envelope is false for the rank-zero PGF.  The
  actual `psi` promotion remains strict on both witnesses.
- Averaging all vertex-permutation conjugates of `P` gives the complete
  kernel.  The two-step theorem is therefore an exact quenched-versus-
  annealed square.  A viable proof of promotion would extend this to the
  all-history Perron limit, probably through a two-replica or tree-
  homomorphism positivity statement.  This extension remains open.

## Current boundary

The marked lift replaces the nonlinear geometric chain by a linear
single-sample chain, and the complete law is now a strict two-step global
minimum for the exact target observable.  The sole remaining step is to
promote this two-step lower bound to the stationary marked law.  A proof must
use time-homogeneous target/sample flow, a marked-chain tree theorem, or a
genuinely global collision/return-time inequality.  The exact universal r=2
upper bound remains open.

## Final closure checkpoint

- Integrated the two-step sum of squares exactly.  For `n>=4`,
  `U M_P^2 psi` is the complete value plus positive rational coefficients
  `a_n,b_n` times the two defects already isolated in Proposition 2; for
  `n=3` the excess is `(R-3/2)/24`.
- Built the forward active chain `K_P=R A_P`.  Its exact rank-up and rank-down
  rates are `(1-P_vB)/2` and
  `(2|B|)^(-1) sum_(w in B) P_(wB)`.  Also proved pointwise `R psi=1/|B|`.
- Reduced stationary promotion equivalently to: (i) persistence of the
  two-step quenched gain in the Cesaro limit; (ii) the zero-reset limit of a
  rare-restart reward; and (iii) one signed active-arborescence cofactor sum,
  or determinant coefficient.  These are equivalent open inequalities, not
  a universal sign proof.
- Added an independent exact corpus audit.  Promotion is nonnegative on all
  54 connected triangle kernels from `{0,1,2,5}`, all 624 connected
  four-vertex kernels from `{0,1,2}`, 48 deterministic five-vertex graphs,
  and the frozen six-vertex split and rank-tail witnesses.  Equality in the
  exhaustive screens occurs only for repeated scalar presentations of the
  complete kernel.
- A final continuous hostile search also found no promotion violation, but
  this numerical observation is not used by the verifier or any theorem.
- **FINAL STATUS:** the exact r=2 complete-graph dB maximality theorem remains
  open.  The sole surviving promotion sign is (33)/(33e)/(33g)/(33h) in the
  companion note.
