# Adversarial boundary and outside-domain checks

Evidence labels matter: the algebraic `m=3` statements below are deductive;
the eigenvalue calculations are floating-point falsification tests only.

## First-mode crossing direction

Direct eigenvalues of `A_m-tD_m` below the claimed onset `t=1` give a positive
real eigenvalue, consistent with transversality toward instability when the
diffusion multiplier is reduced:

| m | t | rightmost eigenvalue (floating point) |
|---:|---:|---:|
| 3 | 0.9999 | `+1.9274e-6` |
| 4 | 0.9999 | `+9.9235e-7` |
| 149 | 0.9999 | `+1.3908e-8` |
| 3 | 0.99 | `+1.9175e-4` |
| 4 | 0.99 | `+9.8684e-5` |
| 149 | 0.99 | `+1.3824e-6` |

## Scaled-family lower boundary is sufficient, not intrinsic

- For `m=3`, the exact homogeneous quotient is
  `gamma*lambda^3+(1+11 gamma)*lambda^2+(6+31 gamma)*lambda+(16 gamma-2)`
  with `gamma=91L/90`. At `L=45/364` one has `gamma=1/8`, so the constant
  coefficient vanishes and there is an additional homogeneous zero. For
  `L<45/364`, the constant coefficient is negative while the leading
  coefficient is positive, forcing a positive real root. This is an exact
  counterexample to extending homogeneous stability arbitrarily far downward;
  it does not challenge the certified interval, whose lower endpoint is
  `1/sqrt(3)`.
- At `m=4`, a test at `L=0.99 L0` remained homogeneously stable (rightmost
  nonzero eigenvalue about `-0.47635`). This supports the manuscript's careful
  statement that `L0` is a certificate boundary, not an intrinsic dynamical
  boundary.
- At `m=149`, the superseded value `L=1/21<L0` produced a conjugate pair
  `0.0001365497 +/- 0.8806783867 i` in an independently assembled floating-point
  matrix. This agrees with, but does not independently prove, the packet's
  rational Rouche enclosure. It confirms why extrapolating the spatial
  `nu L^2>=1/3` condition to homogeneous stability would be false.
