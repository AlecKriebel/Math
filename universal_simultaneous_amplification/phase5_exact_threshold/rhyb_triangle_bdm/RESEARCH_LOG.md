# Research log: triangle portal product at `R_hyb`

Started: 2026-08-13 (America/Los_Angeles).

No external communication was used.

## 2026-08-13: stronger BDM route reduced, then corrected

- Derived exact three-by-three Schur recurrences for the individual Bd and
  dB singleton/doubleton fixation values on a weighted triangle.
- Reduced arbitrary-portal BDM to a copositive matrix and found a stronger
  six-entry target.  Hostile tests supported it, but the resulting rational
  expressions had no clean edge-order extremizer: singleton-product order
  changes inside a fixed edge chamber.
- Quantified the conceptual issue: at the equal triangle the old stationary
  product target is about `0.49%` below the Hellinger BDM target.  BDM is an
  over-strengthening of the actual gate disjunction.
- Checkpointed the exact BDM reduction and obstruction separately; no BDM
  theorem is claimed.

## 2026-08-13: minimal product theorem

- Replaced the Hellinger target by the exact gate target

  \[
  r^3[\rho_{Bd}-p]_+[\rho_{dB}-p]_+,
  \qquad p=(r-1)/r.
  \]

- Used edge sorting and scale invariance to write every positive triangle as
  `(pq,q,1)` with `0<p,q<=1`.
- For `q<=1/2000`, proved the dB excess is negative using 150 exact rational
  tensor-Bernstein coefficients.
- For `q>=1/2000`, cleared positive denominators, reduced all six portal-entry
  numerators modulo the hybrid sextic, sharpened the root interval to width
  `10^-20`, and verified 39,570 strictly positive rational tensor-Bernstein
  coefficients.
- Independently audited the Schur recurrences and type-complement identity
  against a labelled nonregular six-state chain.

Status: **PROVED** for every positive weighted triangle and every nonzero
nonnegative portal vector.  The stronger triangle BDM statement remains
open and is no longer needed for the local disjunction.
