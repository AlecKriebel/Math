# Research log: scaled first orbit at `R_hyb`

## 2026-08-13 — proof-first reduction and exact certificate

- Recast the target as `E_p phi_r(Rq)>=0`, where
  `phi_r(z)=(r-1)^2 z(rz-1)/(1+r(r-1)z)` is strictly convex.
- Generalized the fitness-two flow-null architecture without searching over
  kernels.  The linear multiplier

  ```text
  lambda_r(x)=(r-1)/r - 2(r-1)(x-1/r)/r
  ```

  makes the pointwise edge slack nonnegative uniformly on
  `3/2 <= r <= 151/100`.
- Certified the cleared slack by exact three-variable Bernstein coefficients
  on eight outer cells.  On the central cell, exact Bernstein bounds make the
  label Hessian positive definite, and the moving point `(1/r,1/r)` is its
  stationary zero.
- The result proves the requested scalar-flow inequality at `R_hyb` and is
  stronger than requested because neither reversibility nor the sextic
  relation is used beyond locating `R_hyb` in the rational interval.
- Exact remaining gap: this is a first-orbit theorem only; the passage to the
  limiting dB endpoint/diffuse support inequality is not supplied by this
  argument.  In particular, it proves only the upper half of the surrounding
  `T` sandwich, not `T>=0`.
- Best-guess completion: **100% for the assigned scalar-flow lemma; roughly
  50% for the surrounding diffuse-support branch**, whose fixed-point passage
  remains open.
