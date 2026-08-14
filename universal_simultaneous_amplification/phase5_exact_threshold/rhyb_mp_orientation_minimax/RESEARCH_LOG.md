# Research log: orientation-preserving MP minimax

## 2026-08-13 — exact variational and pairwise equivalence

- Kept the Bd/dB root balance as one global scalar `lambda` and derived

  ```text
  Q_* = (1/4) inf_lambda min_theta
        (theta dot (lambda U + lambda^-1 eV))^2/(theta dot e).
  ```

  This is exact.  Minimizing separately at each root would be the stronger
  root-Hellinger route and would discard the orientation square.
- Proved that the inner minimizer has support at most two.  Therefore the
  exact all-portal `(MP)`/`(SRR)`/`(PTR)`, not merely `(RHR)`, is equivalent
  to its one-root and two-root restrictions.
- Derived the positive diagonal operator norm

  ```text
  Q_*^-1/2 = sup_lambda inf_t
    ||D_(lambda U + lambda^-1 eV)^-1 (tI+t^-1 E)||_infinity.
  ```

  The correct quantifier order is `for every lambda, there exists t`.
- Derived the exact pair criterion.  In normalized root variables it is

  ```text
  sqrt(h_i h_j) cosh(delta_ij)
    + sqrt((h_i-Q)(h_j-Q)) >= Q cosh(epsilon_ij).
  ```

  Replacing `cosh(delta_ij)` by one gives exactly the stronger existing
  root-Hellinger test.  The difference is the nonnegative swapped-root
  orientation square.
- Audited the zero-reward case `Q=0`, diagonal equality `h_i=Q`, degenerate
  interval boundaries, raw stationary normalization, singleton-root mass
  cancellation, and root-tree normalization.
- No graph, portal, or path-matching search was used.
- Best-guess completion: **100% for the assigned variational/minimax audit;
  roughly 45% for universal `(MP)` itself.**  The portal dimension is now
  closed exactly, but the full-chain pair inequality remains open.
