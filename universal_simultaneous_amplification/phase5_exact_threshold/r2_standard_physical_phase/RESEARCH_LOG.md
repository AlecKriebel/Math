# Research log

## 2026-08-20 -- normalization audit and corrected scalar

- Unwound the earlier signed standard quotient to the physical
  two-feature Hessian system.
- Found that the earlier displayed reward corresponds to gradients
  `1/[k^2(k+1)]`, not to the radial Poisson gradients required by the
  stationary Hessian.
- Derived the corrected physical reward `gamma(d)` and the exact factor
  `Phi_N(d)=4(N+1)^2(N-1) lambda_std`.

## 2026-08-20 -- all-order phase proof

- Found the bad-reward supersolution
  `W_1=2N^2d_1`, `W_2=2Nd_1`,
  `W_k=4N(k-1)d_(k-1)/k`.
- Reduced its only all-order interior sign to the positive polynomial in
  equation (31) of `PHYSICAL_STANDARD_PHASE_THEOREM.md`.
- Proved the reward-independent re-entry contraction
  `A 1 <= 2/(N+1) 1` using
  `z(P_k)=1/N`, `z(R_k)=2/(N+k)`.
- Established `0<=f_0<=8N` and `sigma f_0>=2N` for `N>=7`.
- Summed the entire alternating re-entry series, giving the explicit lower
  bound `Phi_N(d)>=2N(N-9)/(N-1)>0` for `N>=10`.
- Exact Schur elimination closes `2<=N<=9`.
- No broad graph or parameter search was used.

## 2026-08-20 -- hostile-audit repair and independent replay

- A hostile check correctly showed that the supersolution `W` alone does
  not prove the lower comparison with `ell(P)=0`, `ell(R)=2N`: at `N=7`
  the `R_1` residual is negative.
- Separated the two logically different uses of the bad resolvent.  The
  `W` comparison proves only `r_0>=0`.  The lower first-phase bound instead
  uses the independent constant supersolution
  `(I-Q)(4N 1)>=q`, hence `R_Qq<=4N 1`.  This gives the required `R_1`
  inequality sharply at `N=7` and the remaining `R_k` inequalities for
  every `N>=7`.
- Added `verify_physical_standard_phase.py`, with no imports from discovery
  scripts.  It independently reconstructs the signed quotient and physical
  two-feature operator, verifies their exact conjugacy and normalization,
  audits every symbolic polynomial identity and vector barrier, and
  reproduces the exact `Phi_N(d)` values for `2<=N<=9`.
- Clean replay completed with exact rational/symbolic arithmetic; no
  floating-point or sampled extrapolation is used in an all-order step.
- Two independent hostile derivations checked the physical normalization
  against the full labelled chain in small orders and checked the radial,
  Schur, barrier, polynomial, tail, and finite-closure calculations.  No
  mathematical discrepancy remained after the constant-resolvent repair.
