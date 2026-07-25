# Research log: clean-room reconstruction of the marked \(h\ne s\) orbits

## 2026-07-25T22:57:49Z — scope frozen

- Created this dedicated folder for the frozen row
  `Q2-E2-A2-B1-D1-N1`.
- Forbidden during the independent derivation:
  - every file under
    `fixed_divisor_e2_quadratic_pencils/marked_h_distinct/`;
  - `taxonomy_freeze/READINESS_Q2_E2_A2_B1_D1_N1.md`;
  - all row-exclusion proofs.
- Read only:
  - the row definition and canonical-pencil principle in
    `taxonomy_freeze/FROZEN_TAXONOMY_v1.md`;
  - the statement of the all-vertical top-obstruction lemma;
  - the statement of the complete-row theorem, without its proof sections.
- The frozen row gives
  \[
  H_4=(hp,hq,0),\qquad
  \deg h=\deg p=\deg q=2,
  \]
  with a primitive minimal quadratic pencil.  The top theorem leaves
  \[
  p=h,\qquad
  s=\ell^2\in\langle h,q\rangle\text{ the unique double-line member},
  \qquad
  G=(H_3)_3=\ell r,\quad r\in\langle h,q\rangle .
  \]
  The present task is the clean classification of the marked case
  \(h\not\sim s\), including the companion point \([r]\) when \(G\ne0\).
- No existing marked-orbit branch name or readiness conclusion has been
  read.
- Best-guess completion toward this local reconstruction: **10%**.

## 2026-07-25T23:06:33Z — independent classification locked

- Completed and wrote the clean-room classification in `REPORT.md` before
  opening any forbidden comparison artifact.
- With \(s=x^2\), write
  \[
  h=a x^2+2xv^Tu+u^TCu,\qquad u=(y,z).
  \]
  Coprimality forces \(C\ne0\).  If \(\operatorname{rank}C=2\), a block
  shear gives either \(h=yz\) or \(h=x^2+yz\).  If
  \(\operatorname{rank}C=1\), vanishing \(xz\)-coupling produces a second
  double line, while nonvanishing coupling gives \(h=y^2+xz\).  Thus there
  are exactly three marked-pair orbits:
  ```text
  Q2-E2-A2-B1-D1-N1-MD-P21-HR2 : (s,h)=(x^2,yz)
  Q2-E2-A2-B1-D1-N1-MD-P21-HSM : (s,h)=(x^2,x^2+yz)
  Q2-E2-A2-B1-D1-N1-MD-P3-HSM  : (s,h)=(x^2,y^2+xz).
  ```
- Derived the source-induced action on each pencil.
  - For `P21-HR2`, the residual torus fixes the rank-one and rank-two
    singular members and has three companion orbits.
  - For `P21-HSM`, the marked points \(s\), the other singular member
    \(t\), and \(h\) fix three points of the pencil.  The residual action is
    trivial, so the companion has an intrinsic cross-ratio parameter
    \(\tau\in\mathbb P^1\); distinct \(\tau\)'s are inequivalent.
  - For `P3-HSM`, the pencil group is affine; after fixing \(h\), the
    residual torus again gives three companion orbits.
- Assigned stable, coordinate-free IDs using the discriminant partition,
  rank/location of \(h\), and companion position.  The middle family is
  explicitly `Q2-E2-A2-B1-D1-N1-MD-P21-HSM-CTAU` with a required
  `tau` field, not a falsely finite generic orbit.
- Added the dependency-free checker `verify_marked_orbits_exact.py`.  It
  verifies exact canonical ranks, the three discriminant polynomials,
  unique double lines over two odd test fields, the full parabolic
  stabilizer images over \(\mathbb F_5\), the affine `P3` translation, and
  the forbidden second-double-line degeneration.
- Exact run:
  ```text
  PASS: 3 marked-pair types, discriminants, unique double lines, and residual companion actions verified
  ```
- The existing marked package, readiness report, existing branch names,
  and exclusion proofs are still unread at this checkpoint.  The
  clean-room derivation is now complete, so name-only comparison may begin.
- Best-guess completion toward this local reconstruction: **75%**.

## 2026-07-25T23:10:49Z — final verification and handoff

- Performed the permitted post-derivation name-only comparison by listing
  filesystem paths under `marked_h_distinct/`.  The filenames contain no
  branch-specific nomenclature.  No file content there, and no content from
  `READINESS_Q2_E2_A2_B1_D1_N1.md`, was opened or searched.
- Promoted the independent IDs to the full frozen-row prefix
  `Q2-E2-A2-B1-D1-N1-MD-...` so they cannot collide with another
  \(e=2\) leaf.
- Made the continuous family machine-stable as
  `Q2-E2-A2-B1-D1-N1-MD-P21-HSM-CTAU` with a required
  `tau=<value>` field.  The special values \(0,-1,\infty\) retain their
  own endpoint IDs.
- Added the source-translation check: translation changes the cubic term by
  a directional derivative of \(H_4\), which lies in the leading target
  plane and hence vanishes in the normal quotient.  It cannot remove the
  cross-ratio modulus.
- Re-ran the dependency-free checker normally and with Python optimization
  enabled.  Both runs returned:
  ```text
  PASS: 3 marked-pair types, discriminants, unique double lines, and residual companion actions verified
  ```
- Checked all three new artifacts for trailing whitespace; none was found.
- Only this dedicated audit folder was edited.  No ledger, README, parent
  theorem, forbidden package, readiness report, or exclusion proof was
  edited.  No commit or push was made.
- Final completion for this local reconstruction: **100%**.
