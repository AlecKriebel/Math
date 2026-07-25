# Research log: exact `C37` carry switches

## 2026-07-25 PDT

- Derived the signed carry-change identity

  ```text
  R(D')+R(D)
   = (D*Delta+Delta*D+Delta^2+Delta)/2 mod 2.
  ```

  Replayed it exactly on all 2,997 ordered coefficients between the two
  frozen support witnesses.
- Proved from the integral quotient equation that every carry block has
  even augmentation.  This forces the nine lag-zero diagonal carries to
  vanish as well.
- Reduced an ordinary four-cycle switch to an invariant-plane test:
  `A+B` preserves `A^2+A=I+J` exactly when the two pair-vectors span an
  `A`-invariant plane.
- Exhausted all 55,278 unordered vertex pairs in each witness.  The
  minimum column-difference weights are 136 and 138, so neither witness
  has an equation-preserving four-cycle switch.
- Distinguished ordinary switches from semiregular `C37`-orbit moves.
  Exhausted 1,332 binomial isotropic directions against 37 small fixed
  scalars, or 49,284 exact Hermitian transvections per witness.
- Every transvection remained loopless and satisfied the complete
  characteristic-two projection equation.  None preserved the prescribed
  block margins.  Exact `6/3` trace-law counts were 1,492 for type 1 and
  1,604 for type 2.
- The best member for both types was the monomial involution `c=1,s=0`,
  which is merely a fiber transposition.  It preserved the trace law but
  missed four block margins by total absolute deviation eight.
- Repeated the transvection census on the optimized 672-defect type-1
  support.  It likewise had zero exact-margin members.
- Removed caller paths from both semantic payloads after an independent
  replay exposed path-dependent hashes.  The frozen reports now use only
  stable witness basenames and reproduce identically before and after
  promotion.
- No generic solver or random search was used.  Peak resident memory was
  about 25 MB, far below the 4 GB cap.  No external communication
  occurred.
