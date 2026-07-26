# Research log — blinded audit of the exact-\(\delta\ge3\) denominator

## 2026-07-25T17:47:10-07:00 — checkpoint 0

- Began an independent incidence-taxonomy reconstruction for the frozen
  quadratic-pencil, line-double-cover row.
- Forbidden input:
  `binary_locus/delta_ge3_universal/` and all primary-agent messages or
  results.  None has been read.
- Permitted starting inputs are the frozen row definition, the next-row
  readiness `REPORT.md`, and artifacts that predate the forbidden package.
- The audit concerns only the exact incidence denominator for the binary
  data \((h,R)\).  No lower Keller-equation exclusion will be attempted.
- Best-guess completion: 2%.

## 2026-07-25T18:07:44-07:00 — checkpoint 1

- Derived a local valuation formula for every root of
  \(g=\gcd(J(Q,R),-J(P,R),J(P,Q))\).  Since
  \(J(P,Q)=8h^2pq\), common factors can occur only at fixed roots of
  \(h\) and the two branch points \(p=0,q=0\).
- The four fixed-divisor orbit charts give a finite exhaustive split:
  branch square, two branch roots, one branch root, and the no-branch
  family, with the doubled nonbranch fibre separated at \(\kappa=4\).
- Exact \(\delta=3\) currently has 19 disjoint parameterized incidence
  families:
  \(4+2+6+4+3\) across those five charts.
- Exact \(\delta=4\) has six isolated orbit types: three squarefree
  special-modulus types and three doubled-nonbranch types.
- Constant dependence gives one further power-fibre orbit
  \(h=p^2,R=p^3\), up to the branch swap.
- The squarefree double-fixed/contact incidence is a single
  \(z\)-parameter family with
  \(\kappa=z+2+z^{-1}\).  It has two inequivalent values over generic
  \(\kappa\), ramifies at the \(\kappa=0\) stabilizer jump, and must not be
  frozen as two overlapping sheets.
- The proposed refined denominator is therefore
  \[
  19+6+1=26
  \]
  parameterized families.  The dependency-free checker currently passes
  exact rational/number-field representatives and exhaustive finite-field
  regressions.
- Best-guess completion: 72%.

## 2026-07-25T18:19:18-07:00 — checkpoint 2 (final freeze)

- Completed the blinded hostile reconstruction without reading
  `binary_locus/delta_ge3_universal/` or any primary-agent result.
- Froze 26 disjoint parameterized families in `DENOMINATOR.json`:
  19 exact-\(\delta=3\), six exact-\(\delta=4\), and one dependent power
  fibre.  The ledger records every normal form, parameter guard, quotient
  identification, retained stabilizer/coordinate pivot, and exit boundary.
- Corrected an important quotient distinction in the prose: the
  squarefree root cover descends to \(\kappa\) only when the incidence
  forgets relative fixed-root/branch orientation.  `D3-SF-20C` remembers
  that orientation and is one \(z\)-curve with two generic orbits over a
  \(\kappa\)-value.
- Added compactification arrows at the squarefree \(\kappa=\infty\)
  boundary and explicit within-coarse-stratum orbit-closure pivots.
- The dependency-free strict replay passed with terminal marker
  `DELTA_GE3_DENOMINATOR_STRICT_PASS_26`.
- No lower Keller equation was examined or excluded.  No external
  communication, commit, or push was performed.
- Completion: 100%.
