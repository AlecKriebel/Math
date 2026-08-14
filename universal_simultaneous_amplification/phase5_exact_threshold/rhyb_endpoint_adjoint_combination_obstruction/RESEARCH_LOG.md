# Research log

## 2026-08-13 18:22 PDT — proof-first reduction

- Restricted the task to the endpoint gap
  `G=E_p[h-(1+r(r-1)Rq)^(-1)]`; no kernel or graph search was performed.
- Derived the temperature-adjoint averages exactly:
  `U^dagger=c E_p(th)-E_p[t(1-q1)]`,
  `G^dagger=E_p[t(q-q1)]`, and
  `M^dagger=E_p(td^dagger)=U^dagger+G^dagger`.
- Put both reciprocal cross terms in the original edge orientation and found
  the uncancelled residual
  `d-d^dagger=(r-2)(q-h)`.
- On the conceptual reversible two-state eigenmode family, derived the exact
  quadratic data in both orientations.  The non-mean fluctuation part of the
  reciprocal cross contribution plus the retained positive square is the same
  strictly negative number `C` in both orientations for
  `3/2<=r<=151/100` and `-1<=lambda<0`.
- Found the exact projected Farkas witness `M_2=M_2^dagger=0`: both
  scaled-first rows are positive while the endpoint target is negative.
- Independently replayed the expansion and audited the essential scope:
  the witness belongs to the scalar relaxation, not the physical endpoint
  image.  The actual family has `M_2>0` and `G_2>0`.

## Checkpoint assessment

- **Result:** theorem-sized quadratic projected obstruction to every
  nonnegative scalar combination of the two proved scaled-first sign rows
  after all endpoint data except the two mean residuals are discarded.
- **Not proved:** the universal endpoint sign `G>=0`; no counterexample was
  found.
- **Estimated completion of this bounded subtask:** 100% after exact replay,
  clean-diff audit, commit, and push.
- **Estimated completion of the surrounding endpoint program:** about 70%.
  The upper scaled-first half is proved and this tempting two-orientation
  closure is now ruled out, but the lower endpoint gap still requires a new
  coupled estimate.
