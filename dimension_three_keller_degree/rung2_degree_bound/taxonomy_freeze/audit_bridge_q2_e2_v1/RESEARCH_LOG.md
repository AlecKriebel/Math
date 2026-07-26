# Research log — hostile clean-room audit of Q2-E2-A2-B1-D1-N1

## 2026-07-25T17:04:17-07:00 — checkpoint 0

- Began a clean-room audit from the frozen taxonomy and the explicitly
  permitted pre-freeze packages.
- Excluded from review: `BRIDGE_Q2_E2_A2_B1_D1_N1_v1.md`, all root
  `explore_*` files, `marked_h_distinct/co_closure/`, and
  `marked_h_distinct/endpoint_closure/`.
- First task is to reconstruct the meaning of the frozen row and locate the
  permitted top-obstruction, marked-equal, `C_tau`, and endpoint inputs without
  using the proposed bridge.
- Best-guess completion: 3%.

## 2026-07-25T17:15:14-07:00 — checkpoint 1

- Confirmed the task root is the `Math-kissing5` main worktree.
- Reconstructed the global route without consulting the proposed bridge:
  the frozen coefficient pivot selects a nonzero leading coefficient;
  intrinsic gcd extraction gives a degree-two factor \(h\); the primitive
  quadratic component matrix has rank two; a first-nonzero \(2\times2\)
  minor selects a legal target chart; and relative closure supplies the
  minimal pencil.
- The horizontal-divisor theorem and all-vertical top obstruction leave
  only
  \[
  H_4=(h^2,hs,0),\quad s=\ell^2,\quad
  (H_3)_3=\ell r,\quad [r]\in\mathbb P\langle h,s\rangle
  \]
  when the cubic normal component is nonzero.
- The marked-equal case \(h=s\) is exactly the previously audited package.
  For \(h\ne s\), the frozen \(4+5+4\) taxonomy is disjoint and exhaustive.
- Independently computed both missing `CO` raw \(E_7\) systems.  Each is
  \(36\times26\), has rank \(18\), nullity \(8\), a five-dimensional
  legal gauge subspace, and a three-dimensional quotient.
- `P21-HR2-CO` quotient:
  \[
  (U,V,W)=(Ax^3,Bx^3,Tx^2).
  \]
  Its division-free \(E_6\) and \(E_5\) chains zero columns two and three
  of \(L\).
- `P3-HSM-CO` quotient, with \(h=y^2+xz\):
  \[
  (U,V,W)=(Ax^3+2Czh,\;Bx^3+Cx^2z,\;Cxz).
  \]
  Here \(E_6\) gives
  \[
  a_1=a_4=b_1=b_4=b_5=\ell_7=\ell_8=0,\quad
  a_2=a_3,\ a_5=C^2,\ b_2=b_3,
  \]
  and \(E_5\) gives
  \[
  \ell_1=\ell_4=0,\quad \ell_2=Ca_3,\quad\ell_5=Cb_3.
  \]
  The second column of \(L\) is zero.
- Exact internal count is
  \(3\ \mathrm{C0}+6\ \mathrm{CH/CS}+1\ \mathrm{CT}
  +1\ \mathrm{CTAU}+2\ \mathrm{CO}=13\).
- Scope correction: each `C0` branch is an automorphism exit, not a
  contradiction to the existence of a nonzero constant Jacobian.  The
  row theorem can only say “Keller implies automorphism”; the stronger
  blanket nonexistence statement is false in scope.
- Best-guess completion: 68%.

## 2026-07-25T17:24:57-07:00 — final checkpoint

- Completed the explicit frozen `C_0,...,C_44` route and the disjoint
  first-nonzero `M_0,...,M_44` intrinsic-minor route.
- Checked every global boundary, both marked-equal pencils, all thirteen
  marked-distinct strata, and the middle projective points
  \(0,-1,\infty\).
- Wrote a dependency-free exact sparse-polynomial checker and strict
  wrapper.  The replay ends with
  `AUDIT_BRIDGE_Q2_E2_STRICT_PASS_D9347B`.
- Final hostile verdict: PASS for exclusion as a counterexample row, with
  the mandatory correction that the three `C0` strata are automorphism
  exits and do not prove nonexistence of constant-Jacobian maps.
- No omitted case, invalid localization, or surviving nonzero-companion
  lower-identity branch was found.
- Best-guess completion: 100%.

## 2026-07-25T17:30:20-07:00 — mandatory pivot correction

- Corrected an outer-route error: `C_30,...,C_44` do not reach the
  intrinsic minor router.  Their prefix-zero guards force
  \(H_{4,1}=H_{4,2}=0\) and \(H_{4,3}\ne0\), hence
  \(\operatorname{rank}JH_4\le1\).  All fifteen are empty in this rank-two
  row.
- The corrected outer count is 30 rank-two-possible coefficient pivots
  plus 15 certified-empty pivots.  The 45 intrinsic \(2\times2\)-minor
  charts remain the disjoint refinement of the rank-two locus reached from
  the first 30 pivots.
- Updated the checker to attest both counts and the component-rank reason,
  and rotated the exact and strict PASS markers.
- This correction removes a contradiction between the coefficient-pivot
  table and the intrinsic rank-two hypothesis; it does not change any
  lower-identity exclusion or the final PASS.
- Best-guess completion: 100%.
