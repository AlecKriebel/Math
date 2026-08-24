# PDE rereview research log

## 2026-08-23 20:45 PDT — checkpoint 1 (5%)

- Scope fixed: independently assess the v1.0.8 repairs to the fixed-mass
  Fourier/Fredholm, high-mode inverse, sectorial/center-manifold, positivity,
  complementary spectral-gap, and local exponential-stability argument.
- Read-only target:
  `../source_snapshot`; no stored PASS marker will be treated as evidence.
- Prior comparison point: v1.0.7 nonlinear/PDE report, especially defect D5
  (the functional-analytic argument was mathematically credible but too
  compressed for a self-contained proof).
- Work is isolated in this directory; no snapshot or live-source edits.

## 2026-08-23 20:52 PDT — checkpoint 2 (55%)

- Diffed v1.0.8 against the preserved v1.0.7 source.  The PDE repair is
  concentrated in `manuscript/main.tex`, `manuscript/supplement.tex`, and
  `proof_audit/branch_stability.tex`; the unrelated SCC/core-minor repair was
  excluded from this review.
- Read the complete revised unit-family proof, scaled-family transfer, S10,
  branch-stability proof aid, conservation proof aids, and robustness proof.
- Rendered and visually inspected manuscript PDF pages 10–12 and supplement
  PDF pages 17–19.  The new equations and prose are present and legible.
- Reconstructed the Fourier blocks directly.  The displayed factorization is
  correct, and the stated Neumann-series threshold yields the asserted
  `k^-2` inverse estimate.  Together with the finite compatible blocks this is
  enough for surjectivity onto the codimension-one range and closed range.
- Wrote and ran `independent_pde_checks.py` (no project imports): exit 0 in
  1.90 s.  Exact checks at `m=3,4,7` and numerical falsification checks at
  `m=3,4,149`, for the unit profile and both scaling endpoints, confirmed the
  zero-mode restriction, critical kernels/adjoints/transversality, positive
  complementary gaps, and high-mode inverse bound.
- Script SHA-256:
  `cf60cd864ce631ff1bda2a690d20e50742ad4921ac205c1a1581b6da16e049a4`.
  Result SHA-256:
  `7a82a35db4783c08ebc725176fb863a9c50e8b77ba5feb0e8d68749c14d5b302`.
- Current assessment: the former D5 expository defect appears repaired.  The
  remaining task is an adversarial theorem-by-theorem hypothesis audit,
  especially the patterned-branch spectral continuation and fixed-mass
  fractional phase space.

## 2026-08-23 20:57 PDT — checkpoint 3 (100%)

- Completed the independent functional-analytic reconstruction.  On the
  closed fixed-mass `L^2` subspace, positive diagonal Neumann diffusion has
  fixed domain `H_N^2`, compact resolvent, and half-order domain `H^1`; the
  quadratic mass-action map is smooth `H^1 -> L^2` in one dimension.
- Checked that the patterned-branch argument does not incorrectly retain a
  Fourier decomposition.  It instead uses a fixed-domain sectorial family,
  bounded multiplication perturbations, uniform elliptic tail estimates, and
  finite Riesz-projection continuation, which is the correct mechanism.
- Verified that the scaled family has conservation covector `H^{-1}c`, leading
  diffusion `H Delta_m`, the same high-mode Neumann factor, and positive
  invertible diagonal scaling at both inclusive endpoints.
- Checked that the robustness proposition remains pointwise in fixed `m,L`,
  stays on the positive-equilibrium realization manifold, retunes exactly one
  scalar multiplier, and makes no dimension-uniform or global claim.
- Official publisher records confirm that the cited Henry chapters cover
  linearized stability and invariant manifolds and that the cited Kato
  chapters cover stability and analytic perturbation; the original
  Crandall--Rabinowitz paper has the claimed simple-eigenvalue scope.
- Final result: D5 is closed; no mathematical repair or theorem change is
  needed.  One cosmetic typo remains in `supplement.tex:980-982`, where
  `Delta` should read `Delta_m`.
- Wrote `PDE_REREVIEW.md` (SHA-256
  `c7bfffc838b90b415d8b570d245deeadd1d8f82a37fe7db67c20f4de1e110cc4`).
- No source snapshot or live-source file was edited, and no commit or external
  communication was made.
