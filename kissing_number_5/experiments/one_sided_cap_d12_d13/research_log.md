# Research log

## 2026-07-23

- Created a dedicated degree-12/13 continuation of the exact degree-11
  one-sided cap program.
- Kept the certified degree-11 artifacts immutable.
- Added separate mixed-height, symmetry-ridge, determinant-sheet, contact,
  pole, random, and diagonal sampling/audit machinery.
- Current estimated completion toward deciding whether this kernel family
  certifies \(B(5)\leq33\): **15%**.
- Coarse reconnaissance gave sampled objectives 33.9531414 at degree 12 and
  33.9573571 at degree 13, but independent audits found violations
  \(F=-0.9650551\) and \(F=-0.9726103\), respectively, on the full
  \(u=0\) slice.  Safe rescaling therefore gave only 35.1464 and 34.8855.
  These candidates are rejected, not certificates.
- Added a dedicated dense \(u=0\) training mesh before the next solve.
- Revised estimated completion toward deciding this kernel family:
  **30%**.
- A 19,838-constraint degree-12 solve returned sampled objective
  34.0254780; its independent audited/rescaled objective was 34.3259500.
  This is a numerical barrier, not a proof that the degree-12 optimum is at
  least 34.
- A 19,837-constraint degree-13 solve failed numerically.  A reduced
  15,558-constraint solve returned sampled objective 34.0212836, while a
  missed high-height contact ridge made its audited/rescaled objective
  36.5288474.  Degree escalation is therefore stopped.
- Added a discovery-only robustness scan of the certified degree-11 kernel
  on enlarged caps \(u\geq-\varepsilon\).
- Revised estimated completion toward the assigned degree-12/13 and
  robustness sweep: **65%**.
- A denser threshold scan found audited objectives 34.770816 at
  \(\varepsilon=1/400\), 34.936166 at \(\varepsilon=1/300\), and
  35.075868 at \(\varepsilon=1/250\).  These values guided but did not enter
  the proof.
- The unchanged exact degree-11 Gram factors were successfully certified on
  the enlarged cap \(u\geq-1/300\), with exact off-diagonal target
  \(-121/125\), diagonal target \(3291/100\), and objective
  \(16939/484=35-1/484\).
- The exact three-variable tree has 6,053 leaves (2,914
  determinant-infeasible and 3,139 proved), maximum depth 30, and digest
  `8c61e175b7cd3b83e5140becb278c47a2c413bdf3e0cc034a0891f1e41b79eab`.
  The exact diagonal tree has five leaves and maximum depth three.
- The packaged four-test suite passed in 754.303 seconds, including exact
  affine-substitution and two tamper-rejection tests.  The root agent also
  reported an independent successful standalone verifier run.
- Final estimated completion toward the assigned degree-12/13 and
  robustness sweep: **100%**.  The degree-12/13 route is numerically blocked;
  the enlarged-cap strengthening is computationally certified.
