# Independent nonlinear/PDE audit log

## 2026-08-22T22:00:03-07:00 — Scope and setup (5%)

- Began an independent audit of the nonlinear bifurcation, spatial spectral,
  equilibrium-scaled-family, robustness, and functional-analytic stability
  claims in packet v1.0.7.
- Work is confined to this directory. The packet is read-only source material;
  no author helper is accepted as proof without semantic inspection.
- Evidence classes will be kept distinct: deduction, independently reconstructed
  exact algebra, finite exact computation, floating-point falsification, and
  author-code consistency checks.
- Immediate goals: read the manuscript and supplement completely; reconstruct
  the relevant theorem dependencies; then build a small independent exact
  checker that does not import project modules.

## 2026-08-22T22:05:42-07:00 — Complete document read and dependency reconstruction (22%)

- Read `manuscript/main.tex` (1,217 lines) and `manuscript/supplement.tex`
  (971 lines) completely. I used no supplied review map to infer dependencies.
- Reconstructed the nonlinear chain: reaction-list Hessian -> homogeneous and
  modal determinant identities -> simple first-mode kernel/cokernel and
  transversality -> fixed-mass zero/second-harmonic solves -> cubic projection
  -> equivariant center manifold/Crandall--Rabinowitz branch -> exchange of
  stability -> semilinear H^1 stability.
- Reconstructed the scaled-family chain: physical equilibrium/rates and
  diffusion -> normalized row-scaled operator -> transformed adjoint and
  physical conservation covector -> separate homogeneous and t>=1 modulus
  certificates -> gauge-corrected zero mode -> uniform cubic sign -> positive
  stable branch -> exact contrasts and within-family endpoint optimum.
- Initial paper proof inspection finds the Fourier factors `-1/4` and `1/2`,
  the distinction between reduced flow and stationary Lyapunov--Schmidt
  equation, and the physical-to-normalized conservation gauge internally
  consistent. These remain hypotheses under adversarial exact reconstruction.
- Noted an important evidence limitation to investigate: the shipped harmonic
  and cubic entrypoints reconstruct full matrices only in finitely many
  dimensions; their all-dimensional conclusion also relies on printed
  recurrences and hard-coded closed forms. I will independently check those
  generic identities rather than treating the finite runs as a proof.

## 2026-08-22T22:17:09-07:00 — Independent exact reconstruction (64%)

- Wrote `independent_exact_checks.py`; it imports no packet/repository module
  and reads no stored certificate. It reconstructs Gamma, Y, A, and B from the
  indexed reaction list.
- Closed the principal all-dimensional audit gap independently. With symbolic
  `m` and an abstract harmonic sum `h`, I verified the printed `w0` boundary
  equations and gauge, the four-variable `w2` boundary system and determinant,
  and the interior recurrence. The recurrence gives
  `w2[i-1]-w2[i]=4*w2[i]/K_i+sigma`, while
  `T_i/(K_{i-1}K_i)=K_{i-3}K_{i-2}/(K_{-1}K_0K_1K_2)`.
  Summing the resulting quadratic polynomial and reciprocal remainder derives,
  rather than assumes, `N_m=R_m+C_m*h_m`; the symbolic difference is exactly
  zero. I likewise derived `S_m=ell^T B(r,rho)` exactly.
- Rebuilt E35, E77, E84, and E22 from their defining boundary polynomials.
  Exact coefficient tests reproduced 35, 77, 84, and 22 grouped terms and the
  stated equality cases. At the E22 boundary `U=0`, the linear x and z
  coefficients vanish, but positive pure x^2 and z^2 terms still force the
  unique equality point; the manuscript's equality claim is sound.
- Reconstructed homogeneous and damped determinant identities directly from
  reaction matrices at m=3,4,5. Checked exact kernels, adjoints,
  transversality, w0/w2 equations, gauges, and negative cubic signs at
  m=3,4,7,149. The m=149 exact check is a high-dimensional regression, not the
  all-m proof; the preceding symbolic reduction supplies the all-m step.
- Independently checked both certified scaling endpoints exactly at m=3 and
  m=4, including transformed adjoints, nonzero gauge denominators, corrected
  zero modes, transversality, and positive cubic numerators.
- Numerical falsification at m=3,4,149 tested L0, midpoint, L1, modes
  t=0,1,1.0001,4,9,25, and additional t>1 values. No competing real or wave
  instability was found. The rightmost noncritical gaps become small at m=149
  (e.g. about -9.08e-4 for the homogeneous L1 case), consistent with claims
  being fixed-dimension rather than uniform.
- Run: `python agent_nonlinear_pde/independent_exact_checks.py`, exit 0,
  88.87 s. Script SHA-256
  `61023d352594537217a43f4b32f1c33a4e162b514f06eb83af2ed62bc5d370c5`;
  result SHA-256
  `a1d3556db29b57f87dfa28cec931fb00f499d2667014be85a06d0be6a3408e1f`.
- Software-semantics finding: shipped `verify_cubic_sign.py` and its `dd_`
  twin test full contractions only at m=3,4,5,6,8,10 and compare against a
  hard-coded `N_formula`; the exposition verifier compares hard-coded copies.
  Those programs alone do not prove the all-m bridge. The bridge is nonetheless
  valid by the independent symbolic derivation above, so this is a verifier
  coverage/documentation defect, not a mathematical gap.

## 2026-08-22T22:27:33-07:00 — Final scoped referee assessment (100%)

- Re-ran the completed standalone campaign after adding generic all-m
  kernel/adjoint/transversality identities and independently reconstructed
  scalar sign certificates. Exit 0; runtime 90.81 s.
- Final script SHA-256:
  `18054a60d2f4273623143d7635a71800c690de8721ef5878ff5f7888c21a5584`.
  Final result SHA-256:
  `57c26e7a403ac1dccceb904888b53923307007117c06fcecb55d94524833ce88`.
- Inspected and ran the load-bearing unit/scaled mode, harmonic, cubic, branch
  regression, and Pareto-family entrypoints. All exited zero. Four selected
  coefficient/endpoint/Fourier mutation tests were rejected (`4 passed`).
- Assessed the fixed-mass Fredholm, sectorial, reflection, center-manifold,
  Crandall--Rabinowitz, exchange-of-stability, robustness, and H^1
  linearized-stability steps independently. Their hypotheses are satisfied;
  these conclusions remain explicitly conditional on the cited standard
  functional-analytic theorems rather than on executable checks.
- Produced `NONLINEAR_PDE_FINDINGS.md` (358 lines), SHA-256
  `e80566a609b1d8da78a33d9cb3d4780c9950049ba2f06c46054bc3c1e2b49b36`.
- Scoped verdict: nonlinear/PDE and scaled-family mathematics valid as stated.
  No mathematical repair or headline change is required. Minor repairs should
  clarify that the shipped all-m cubic verification is finite/hard-coded,
  duplicate `dd_` entrypoints are not independent implementations, and the
  branch-stability script is a floating finite regression. A short explicit
  fixed-mass Fourier/Fredholm paragraph would improve exposition only.
