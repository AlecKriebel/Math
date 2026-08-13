# Research log: hot--cold two-stage composition

## 2026-08-13 -- exact triangular classification

- Classified the minimal reversible diffuse trace containing neutral bulk,
  one singular cold Bd-gain type, and one non-cold relay type.
- Recorded and verified the exact temperature-adjoint involution
  `p'=p odot t`, `P'=D_t^-1 R`, which swaps `b` and `s` but also changes the
  initialization weights.  This shows why simply adjoining an adjoint
  complement does not cancel the response for free.
- Derived the two exact scalar endpoint equations for the relay and retained
  all uniform-start and bulk-coordinate corrections.
- Eliminating the relay temperature gives

  ```text
  x/r - G = [x b r + h(rb-r+1)^2]/[r(r-1)] >= 0,
  C - x(r-1)/r = (rs-r+1)^2/[r(r-1)(1-s)] >= 0.
  ```

  Therefore `C-(r-1)G>=0`; a finite hot relay strictly worsens the cold
  ray rather than compensating it.
- Recorded the general projective criterion for a positive matrix:

  ```text
  T_M(q)<q iff beta*q^2+(alpha-delta)*q-gamma>0.
  ```

- Recorded the exact signed-compensator criterion.  A hot increment
  `(G_h,C_h)` improves cold ratio `q_c` iff

  ```text
  C_h G_c < C_c G_h.
  ```

  For a true tradeoff compensator `(-u,-v)`, this is `v/u>q_c`.
- The canonical relay instead contributes `(-E_B,+E_D)`, with the wrong dB
  sign.  The surviving target is therefore a stage that transmits a
  conditional Bd event while multiplying the conditional adverse dB passage
  probability before uniform-start averaging.
- Quantifier checkpoint: the needed lower ray may satisfy ratio tending to
  zero for each fixed `r<2` while retaining ratio at least one at `r=2`.
  Endpoint-uniform convergence is neither needed nor expected.
- Best-guess completion of the exact-threshold program: **71%**.  This
  exactly closes the first non-cold triangular relay but does not yet build
  the required locked-history conditional attenuator.
