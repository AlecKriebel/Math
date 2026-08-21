# Research log — quartic survivor construction

## 2026-07-26

- Opened a construction-only track inside the frozen
  `Q2-E2-A1-B2-D1-N2` binary line-double-cover denominator.
- Read the canonical 26-family registry
  `audit_delta_ge3_denominator/DENOMINATOR.json` and the exact
  `d3_construction_search` and `delta_ge3_survivor_probe` scripts.
- Compared the zero-binary full \(E_7/E_6\) fibres of representative
  unresolved degree-three families.  The least-constrained fibre occurs
  for frozen family `D3-BS-N1-CONTACT`,
  \[
  h=p^2,\qquad R=p(p^2+q^2).
  \]
  Its \(E_6\) compatibility ideal is
  \[
  y_0y_2=x y_0=0,
  \]
  so the component \(y_0=0\) retains the three independent top tangent
  parameters \(x,y_1,y_2\).  The other compared families had smaller
  conic/line or nonreduced fibres.
- Selected `D3-BS-N1-CONTACT` for the full homogeneous determinant
  construction attempt.  No BCW reduction is used.

## 2026-07-26 — full exact descent completed

- Restored arbitrary binary \(U_0,V_0,T_0\), arbitrary ternary quadratics
  \(A,B\), and arbitrary \(L\).
- Derived the complete division-free \(E_6\) compatibility ideal
  \[
  (3y_0-y_1)C,\ xC,\
  x(-u_1+9u_3+12v_3)+16y_0y_2,\
  xy_0,\ u_3y_2,\ u_3x,\ u_3y_0,
  \quad C=4t_1-3u_1-4v_1.
  \]
- Exhausted the normalized \(x\), \(y_2\), \(y_1\), mixed
  \(y_1+s y_2\), and \(y_0\ne0\) charts.  The only exceptional generic
  pivot, \(3s^2=1\), was recomputed over \(\mathbb Q(\sqrt3)\).
- Every nonzero tangent is inconsistent at \(E_5,E_4,E_3\) or forces
  \(\det L=0\).  The \(E_7\)-origin has
  \(A_r=0,B_r=\ell_8p\) and exits by the binary or degree-three-coordinate
  automorphism arguments.
- Conclusion: no quartic counterexample was constructed.  The whole frozen
  family `D3-BS-N1-CONTACT` is excluded as a counterexample family.
- Added `NOTE.md`, the exact verifier `verify_family_exclusion.py`, and the
  strict wrapper `verify_strict.sh`.  The terminal marker is
  `D3_BS_N1_CONTACT_FULL_FAMILY_EXCLUSION_PASS`.
