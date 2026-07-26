# Research log

## 2026-07-26 (America/Los_Angeles)

- Began an isolated clean-room reconstruction.  No pre-existing file under
  `power_fibre/` was inspected.
- Read only the frozen external incidence denominator
  `delta_ge3_universal/{denominator.json,FREEZE.json}`.  It records the
  normalized dependent-gradient leaf `PF-BS` as
  \(h=p^2,\ R=p^3\); this is used only as a target to independently rederive,
  not as evidence for any Keller conclusion.
- Directly expanded the homogeneous determinant equation.  The degree-seven
  equation is
  \[
    2p^4q(4p\,\partial_r(H_2)_3-3\,\partial_r(H_3)_1)=0,
  \]
  hence
  \[
    (H_3)_1=\frac43p(H_2)_3+A(p,q)
  \]
  for a binary cubic \(A\).  This is the first top-contact identity and uses
  no division by a parameter.
- Next: derive the degree-six identity exactly, stratify the quadratic
  \((H_2)_3\), and audit the allowed source/target stabilizer before any pivot
  normalization.

## 2026-07-26 00:42 PDT

- Hostile check caught a PARI/GP scripting hazard: an early scratch file used
  a determinant sum split across physical lines.  GP treated only the first
  line as the assignment.  The resulting provisional product formula for
  \(E_6\) was **wrong and is retracted**.  The final verifier keeps every sum
  on one assignment line and is independently checked by a dependency-free
  sparse engine.
- The corrected degree-six identity, after
  \((H_3)_1=\frac43pZ+a(p,q)\), is
  \[
  E_6=8\lambda p^5q-6p^4qX_r+3p^2a_qB_r
      +2pq(pa_p-qa_q)Z_r+\frac83p^2qZZ_r.
  \]
  Both exact engines verify this universal identity.
- Recorded a complete, no-pivot parameterization: choose
  \(U=B_r\), form the numerator \(N\) consisting of the four positive
  terms above, require the literal coefficient-space membership
  \(N\in6p^4qV_1\), and then set
  \(X_r=N/(6p^4q)\).  Binary integration constants are free.  This is
  an affine-kernel description and loses no endpoint.
- Proved a stronger standalone lemma.  For
  \(f=p^3+Q_2+L_1\), writing the quadratic transverse block in
  \(y=(q,r)\) as a symmetric \(2\times2\) matrix \(M\):
  rank two always gives a critical point; rank one is nonsingular only
  when the null variable has a nonzero constant linear coefficient,
  in which case \(f\) is visibly a coordinate; rank zero splits by the
  dependence of the two coefficient vectors and is either visibly a
  coordinate or has an explicit critical point.
- Consequently a Keller map in the requested family has \(F_3\) as a
  coordinate with inverse degree at most three.  After changing source
  coordinates, each \(F_3=w_0\) fibre is a plane Keller map of degree
  at most \(9\) in the fixed family (and at most \(12\) by the general
  composition bound).  Moh's safe plane range \(<100\) makes
  every fibre an automorphism; fibrewise injectivity and
  Ax--Grothendieck finish the three-variable map.
- Verdict: **PASS**, with no counterexample.
- Directly checked the frozen canonical denominator
  `audit_delta_ge3_denominator/DENOMINATOR.json` (SHA-256
  `440df4694f98b1b361a09e136afb4365c3aa302c5532e5291f4b76a2a068c65a`).
  The cube-component corollaries are exactly
  `PF-BRANCH-FOURTH-THIRD`, `D4-DN-3`, `D3-BB-30`,
  `D3-OB-300`, and the retained \(z=3\) pivot (only) in
  `D3-SF-20C`.
- Added the exact PARI verifier, independent sparse verifier, frozen
  denominator checker, and strict wrapper with four required-failure
  mutations.  The strict marker passes.
