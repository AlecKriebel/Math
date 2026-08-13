# Research log: R_hyb separator sanity

## 2026-08-13 -- stored witness refutes the hybrid tangent

- Derived the unique tangent functional forced by the ordinary-leaf vector:

  ```text
  S_r(B,D)=D+(r-1)B.
  ```

  At `r=R_hyb`, it also annihilates the optimized strong-pair vector.
- Evaluated only the already stored exact weak-cut `K_2--K_20` witness with
  internal degree ratio `19/137`; no graph optimization or architecture
  search was performed.
- Exact Sturm/root isolation proves

  ```text
  (y-1)+(R_hyb-1)(x-1) > 0
  ```

  for this witness.  The value is approximately `8.4365e-5`, but the sign
  is established over exact rational polynomials.
- Therefore the dilute-hybrid tangent is not a universal affine separator.
  The witness has `x<1<y`, so it does not refute `R_sim=R_hyb`.
- Formulated the minimally sufficient matching upper theorem as the
  nonlinear endpoint disjunction `liminf min(X_k,Y_k)<=1` for every graph
  sequence.
- Isolated one structural route: a compactness theorem reducing every
  hypothetical simultaneous endpoint sequence, after negligible deletion,
  to the closed cone of exact dilute module responses.  Failure of this
  theorem would itself locate the only remaining lower mechanisms.
- Best-guess completion of the exact-threshold program: **72%**.  The
  `R_hyb` hypothesis remains viable, but its upper proof cannot be a global
  supporting line.
