# Research log: positive set-memory obstruction

## 2026-08-13 -- monotone-coupling theorem

- Coupled a clean locked batch and an adverse locked batch by sharing the
  first source.  The adverse union contains the clean singleton pointwise.
- Proved that every positive OR/coverage statistic has conditional masses
  `u<=v<=(r+1)u`.  The upper bound is the submodular union bound together
  with the exact conditional mean `E(K | A)=r+1`.
- For any number of positive retained states, the prior-weighted handoff
  satisfies `H e_A >= (r-1) H e_F` componentwise.  Every common positive
  continuation and positive readout preserves this inequality.  Hence the
  factor `r-1` is preserved once, not powered to `(r-1)^L`.
- Reconciled the result with the exact soft `2 by 2` classifier.  Its hit
  row obeys adverse dominance.  Its clean-enriching no-hit row is precisely
  the affine complement with nonzero empty-set baseline.
- Proved that two positive coverage destinations which route every nonempty
  input completely are constant on the nonempty Boolean lattice.  Their
  handoff is rank one.  A full-rank positive router necessarily leaves a
  NOT/loss coordinate, but discarding that coordinate does not evade the
  monotone one-factor floor.
- Derived the exact two-state spectral bound

  ```text
  lambda_minus/lambda_plus
      <= (sqrt(r+1)-1)/(sqrt(r+1)+1).
  ```

  At `R_hyb` this is `0.225419...`, while `r-1=0.502856...`.  Any smaller
  sub-Perron mode is sign-changing and cannot be isolated by positive
  initialization/readout.
- **CLOSED:** finite or growing common positive OR/coverage set-memory
  handoffs as a way to power the locked-history factor.
- **OPEN:** signed/nonmonotone statistics, channel- or rule-dependent
  kernels, and direct graph responses not factoring through this handoff.
