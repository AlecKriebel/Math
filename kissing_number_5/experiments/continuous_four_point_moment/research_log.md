# Research log

## 2026-07-23

- Re-derived the ordered \(N=41\) pair, triple, and four-point measure
  normalizations and their projection factors \(39\) and \(38\).
- Formulated the degree-four full-interval moment and localizer system
  with no finite support assumption.
- Derived the universal edge-conditioned covariance block
  \(38\int\phi\phi^{\mathsf T}d\nu-
  \int\phi_k\phi_\ell^{\mathsf T}d\rho\succeq0\).
- Encoded one closed semialgebraic cap/product flag with
  \(B=[-3/10,-6/25]\), \(b_0=49/100\), \(\delta'=1/301\), and capacity
  \(M=3\).  The projected-height-square margin above \(5/8\) is exactly
  \(13/1900\).
- Identified an exact obstruction to separation: the authenticated
  74-atom rank-five \(K_6\) product extension induces the global-scale
  measures
  \(\alpha=(4/3)\alpha_6\), \(\nu=13\nu_6\),
  \(\rho=(494/3)\rho_6\).
- Proved atomwise that every polynomial edge-covariance block is PSD:
  its local contribution is
  \((494/3)\sum_{i<j}(v_i-v_j)(v_i-v_j)^{\mathsf T}\).
- Checked exact strict depth and cap slack and exact zero product slack.
- Recomputed all 27 sharp harmonic trace residuals; every one is
  positive.
- Added a standalone standard-library rational verifier and regression
  test.

## Status

**COMPUTATIONALLY CERTIFIED:** the stated continuous-support
four-point/edge-conditioned relaxation is feasible at \(N=41\).

**Exact bottleneck:** constraints determined by one symmetric rank-five
\(K_6\) marginal do not enforce consistency of overlapping six-subsets
inside a single 41-point Gram matrix.  A new seven-point overlap flag,
global cross-base rank identity, or a new nonlinear count inequality is
required.

## 2026-07-23 — factorial-moment strengthening

- Used the integer cap bound \(\Gamma\le3\) to derive
  \(\binom{3-\Gamma}{2}\ge0\).
- Converted it exactly under four-of-39 and five-of-39 sampling.  The
  resulting rows separate respectively the 74-atom K6 and 53-atom K7
  witnesses.
- Generalized every integer cap or depth bound to unbiased estimators of
  \(\binom{\Gamma}{a}\binom{M-\Gamma}{b}\) and
  \(\binom{H-r}{a}\binom{39-H}{b}\).
- The K6 witness violates 11 of 98 cap rows and 292 of 7,840 depth rows.
  The K7 witness violates 19 of 140 cap rows and 647 of 11,200 depth
  rows.
- Extracted a two-row exact Farkas contradiction for the authenticated
  1,782-column K7 pool.
- Added an explicit rank-five K7 atom with a zero base and four common
  endpoint neighbors.  Numerically, the augmented pool repairs all cap
  factorial rows and all 560 product rows.
- Imposed a full degree-five joint moment extension on
  \(H\ge7,\Gamma\le M,H+\Gamma\le39\).  Even the first
  \((q,b,M)=(-3/4,1/4,6)\) stratum makes the augmented pool infeasible.
  A three-multiplier exact Farkas ray was reconstructed.

## 2026-07-23 — continuous audit of the joint Farkas ray

- Factored the representing-state coefficient as
  \[
  \Gamma(H-7)(H+4)(H^2-3H+30)/6552\ge0.
  \]
- Identified the separate atom coefficient
  \(g-n_{155}-2109\binom h4g\), which vanished on every pool column.
- Constructed an exact rational 7-by-7 Gram matrix of rank five with
  \(h=4,g=n_{155}=1\), giving atom value \(-2109\).
- Verified Gram PSD by all principal minors and independently by a
  base-edge Schur complement equal to one half of a duplicated regular
  tetrahedron Gram matrix.
- Conclusion: the zero atom coefficient used an accidental
  quarter-pool support exclusion.  It is not implied by continuous
  rank-five Gram PSD.
