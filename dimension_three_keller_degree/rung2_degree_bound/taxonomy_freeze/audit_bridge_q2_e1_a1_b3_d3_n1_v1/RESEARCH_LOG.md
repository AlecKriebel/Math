# Research log: bridge audit for `Q2-E1-A1-B3-D3-N1`

## 2026-07-26T09:47:30Z — frozen-only phase completed

- Began with, and read only,
  `../FROZEN_TAXONOMY_v1.md` and `../frozen_manifest_v1.json`.
- Re-derived the row intrinsically as
  \(H_4=\ell A(p,q)\), with \(\ell\) linear, \(p,q\) independent linear
  forms, and \(A\) a basepoint-free three-dimensional subsystem of
  \(H^0(\mathbb P^1,\mathcal O(3))\) whose image is a birational plane
  cubic.
- Classified the subsystem by projection of the rational normal cubic.
  The only basepoint-free birational cases are the nodal and cuspidal
  projection centres.  A centre on the rational normal cubic is the
  excluded basepoint case.
- Kept the marked factor \(\ell\) arbitrary.  Its intrinsic incidence with
  \(U=\langle p,q\rangle\) gives the exhaustive split
  \(\ell\in U\) (aligned) or \(\ell\notin U\) (transverse).  No stabilizer
  transitivity on an aligned marked factor was assumed.
- Derived the exact frozen coefficient routing.  Every target component is
  a nonzero quartic because the cubic coordinate system is linearly
  independent.  Hence only `C00`--`C14` can occur; `C15`--`C44` are empty.
  The division-free coefficient formulas and all route predicates are in
  `PRELEGACY_DERIVATION.md` and the checker.
- This entry closes the frozen-only phase.  Legacy exclusion notes may be
  located and opened after this timestamp.

## 2026-07-26T09:57:44Z — legacy assembly and strict replay completed

- Located the four expected theorem notes and their four SymPy/PARI pairs:
  transverse/aligned nodal and transverse/aligned cuspidal.
- Replayed all eight supplied implementations successfully.
- Audited lower-term scope.  The aligned nodal, transverse cuspidal, and
  aligned cuspidal checkers retain arbitrary lower coefficients after their
  complete degree-eight reductions.
- Found the smallest retained-evidence gap in the transverse nodal pair:
  both supplied scripts substitute the displayed \(H_2,L_0\), although the
  note says the raw rank-sixteen and rank-nine systems were solved.
- Closed that gap in
  `verify_bridge_q2_e1_a1_b3_d3_n1_v1.py`, starting from a general
  30-coefficient \(H_3\), general 18-coefficient \(H_2\), and general
  nine-entry \(L_0\).  Reconstructed ranks \(24,16,9\), the complete
  kernels/affine solutions, and the terminal \(E_5\) factor.
- `verify_strict.sh` passed the bridge checker, all eight supplied
  implementations, three required-failure mutations, and the optimized
  Python guard:
  `Q2_E1_A1_B3_D3_N1_STRICT_PASS_V1`.
- Final verdict: **PASS** for counterexample exclusion.  The scalar-aligned
  nodal regime is not empty; its proof forces every Keller map there to be
  an automorphism.
