# Research log

## 2026-08-02 (America/Los_Angeles)

* Stress-tested the component and aggregate stationary-odds inequalities on
  extreme directed and symmetric kernels through six vertices.  No strict
  violation was found; this is numerical discovery evidence only.
* Derived the sufficient nonnegative additive-potential system
  `c>=0`, `(I-H)c>=1/q-2`.
* Found a positive-support symmetric five-vertex graph for which this system
  is infeasible, then exactified the obstruction with the short rational
  Farkas vector `(0,1,1977/2000,0,3/100)`.
* Verified over exact rationals that the same graph has strictly positive
  component and aggregate odds slacks.  Therefore only the proposed proof
  architecture is closed; the inequalities remain open.

## 2026-08-02 10:53 PDT -- independent integration audit

* Re-derived the additive-potential identity and checked that
  `c>=0`, `(I-H)c>=1/q-2` is sufficient by maximizing each hole sum at the
  singleton state.
* Verified the Farkas implication directly: the displayed nonnegative `y`
  has `H^T y-y>0` componentwise and `y^T(1/q-2)>0`, contradicting feasibility.
* Ran the full 31-state exact verifier under both the system interpreter and
  the project environment.  All marginal bounds, component slacks,
  stationarity equations, and aggregate identities pass.
* **OPEN:** the component and aggregate odds inequalities themselves; the
  obstruction applies only to this nonnegative additive certificate.
