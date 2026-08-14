# Research log: soft coverage transfer obstruction

## 2026-08-13 19:29 PDT -- exact soft-transfer theorem

- Replaced the perfect singleton-versus-nonsingleton router by an ideal
  random ancestral coverage tester and derived its exact `2 by 2` transfer.
  If `c` is clean no-hit throughput, then adverse no-hit throughput is

  ```text
  d = E[X^2/(r-(r-1)X)].
  ```

- Proved the sharp data-processing/throughput inequality

  ```text
  d/c >= c/(r-(r-1)c) >= c^r.
  ```

  Consequently a cascade has additional projective retention
  `Delta >= C^r`, where `C` is its absolute clean throughput.

- Retained the exact source-collision law.  Conditional on an adverse
  geometric batch, singleton collision has probability
  `1/(rm-(r-1))`, giving the projective floor
  `(r-1)/(rm-(r-1))`.

- Proved that the full two-output classifier has total-variation separation
  at most `r/(1+sqrt(r))^2`, although its rare no-hit output can have a much
  better likelihood ratio.

- Identified the precise correction to the earlier coverage no-go: weak
  soft tests can improve a one-stage posterior ratio without vanishing
  classification error.  This scalar improvement is real, but is not a
  composable physical transfer by itself.

- Closed the clean-enriching **no-hit complement** workaround at physical
  response scale.  It carries unit empty-set baseline.  At depth `n`, its
  baseline/clean-process-signal ratio is `1/C`; against the formal all-F
  cylinder it is `r^n/C`.  Positive multiplicity and uniform dilution cannot
  change either ratio.

- Audited the tempting baseline-free hit route.  In the concentrated regime
  its one-stage posterior ratio is

  ```text
  q_hit = (r-1)(r+x)/(r-(r-1)x).
  ```

  This number can be below one, but its powers are not the physical cascade:
  F/A are resampled subevents inside each geometric batch, not two fixed
  global models.  A hit followed by common reset has rank-one matrix

  ```text
  R = (1/r) (1,r-1)^T (1-c,1-d),
  R^n = ((1-c)+(r-1)(1-d))^(n-1)/r^(n-1) * R.
  ```

  Every latent output after reset has adverse/favorable ratio exactly `r-1`.
  The actual full-geometric versus clean one-sample hit ratio is

  ```text
  chi_hit = [(1-c)+(r-1)(1-d)]/[r(1-c)] >= 1.
  ```

  Thus the baseline-free hit output is physically in the wrong direction.

- Expanded the physical success multiplier as a binomial sum.  The desired
  all-clean and all-adverse cylinders are only its two extreme terms; reset
  merges all mixed histories, which dominate even when absolute survival
  tends to one.

- For no-hit, proved the physical composable tradeoff

  ```text
  chi_nohit = [c+(r-1)d]/(rc)
              >= 1/[r-(r-1)c] >= c^(r-1).
  ```

  Hence a cascade with clean throughput `C` has full/clean ratio at least
  `C^(r-1)`.  Exponential suppression forces exponential clean attenuation,
  while no-hit is the affine complement with unmatched unit baseline.

- Proved the exact all-depth mark-erasure identity for honest binary
  classifiers:

  ```text
  K_n...K_1(1,-1)^T = product_i(c_i-d_i) (1,-1)^T,
  |c_i-d_i| <= r/(1+sqrt(r))^2 < 1.
  ```

  Hence an inhomogeneous sequence erases the channel distinction
  exponentially and cannot approximate the diagonal history transfer.

- **CLOSED:** memoryless positive iid-union soft coverage tests or
  complements as a replacement for the channel-preserving locked-history
  transfer.
- **OPEN:** a genuine physical memory/multi-output state, signed common
  control, non-OR dynamics, or a direct graph response not factoring through
  this hidden bit.
