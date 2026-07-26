# Research log: hostile cube-component audit

All timestamps are UTC.

## 2026-07-26T07:45:00Z — independent rank proof

- Received the proposed cube-leading submersion statement, but no proof
  details or verifier.
- Before reading `cube_component_exit/verify_theorem.py`, normalized
  \(f\) to
  \[
  x^3+a x^2+x(by+cz)+q(y,z)+dx+ey+gz
  \]
  and independently split by the rank \(2,1,0\) of the transverse
  Hessian of \(q\).
- Rank two forces a critical point because the final \(f_x\) equation is
  quadratic with leading coefficient \(3\).
- Rank one was checked on both kernel pivots: \(c\ne0\) gives a critical
  point by three successive linear solves; \(c=0=g\) leaves a genuine
  quadratic.  The sole submersion chart is triangular with \(g\ne0\).
- Rank zero was split at \(bg-ce\).  The zero determinant gives a
  critical point in the separate \(b\ne0\) and \(b=0,c\ne0\) charts; the
  nonzero determinant gives the explicit coordinates
  \(Y=by+cz,Z=ey+gz\) and \(f=h(x)+xY+Z\).
- No counterexample or missing zero-denominator boundary survived.

## 2026-07-26T07:52:00Z — conditional Keller fibre lemma

- Observed independently that the coordinate inverse has degree at most
  three in every surviving chart.
- If a nonzero target-linear combination \(\alpha\mathbin{\cdot}F\) is
  cube-leading, a target \(\mathrm{GL}_3\) change first makes it a literal
  component.  Straightening it in a degree-\(d\) Keller map gives
  \((G_1,G_2,w)\) of degree at most \(3d\).
- Whenever a proved plane Keller range covers \(3d\), fibrewise
  injectivity plus Ax--Grothendieck and étaleness makes the threefold map
  an automorphism.
- Recorded this only as a conditional cube-component lemma, not as a
  quartic-row or unconditional global degree claim.

## 2026-07-26T07:56:00Z — plane floor and frozen scope

- Checked the primary manuscript arXiv:2204.14178.  Its Theorem 2.1 leaves
  only degree pair \((72,108)\), its transpose, or maximum degree at least
  \(125\).  Hence the proved plane range is maximum degree \(<108\).
- Derived the exact corollary \(3d\le105<108\) for \(d\le35\), and
  recorded that \(d=36\) reaches the excluded boundary rather than falling
  below it.
- A peer-reviewed publication record for the 108-floor manuscript was not
  located.
- If the newer preprint is not taken as an input, Moh's established
  plane range \(<100\) gives the conservative endpoint \(d\le33\);
  \(d=34\) reaches degree \(102\) and is not covered by that fallback.
- Bound the frozen 26-family denominator at SHA-256
  `440df4694f98b1b361a09e136afb4365c3aa302c5532e5291f4b76a2a068c65a`.
  The new whole-family count is exactly three:
  `PF-BRANCH-FOURTH-THIRD`, `D3-BB-30`, and `D3-OB-300`.
  `D4-DN-3` is redundant.  Only \(z=3\), not \(z=1/3\) or the whole
  `D3-SF-20C` curve, is a cube pivot.

## 2026-07-26T07:59:54Z — independent exact release artifact

- Read the primary `verify_theorem.py` only after the proof and branch
  classification above were complete.
- Implemented `verify_cube_hostile.gp` in PARI/GP with a general symbolic
  rank-two Hessian and explicit rational inverses.  It shares no code or
  polynomial representation with the primary Python verifier.
- Added `verify_scope.py` and a fail-closed strict wrapper.
- Injected the wrong sign into the rank-one inverse and required rejection.
- Strict terminal run:
  `CUBE_COMPONENT_HOSTILE_AUDIT_PASS`.
- Per task instruction, no commit or push was made.

## 2026-07-26T08:03:01Z — final scope audit

- Removed an over-broad application from this standalone package.  The
  retained result is the coordinate theorem, its target-covector fibre
  lemma, and the stated frozen bridge only.
- Added an explicit limitation that no whole quartic row or
  unconditional Keller degree bound is claimed.
- Re-ran the strict suite after removing the stray out-of-scope
  arithmetic check.  It again terminated with
  `CUBE_COMPONENT_HOSTILE_AUDIT_PASS`, including rejection of the
  inverse-sign mutation and optimized-Python assertion bypass.
- Per instruction, made no commit and no push.
