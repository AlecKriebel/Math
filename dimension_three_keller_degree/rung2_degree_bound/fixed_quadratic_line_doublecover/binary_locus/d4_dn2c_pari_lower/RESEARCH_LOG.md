# Research log — direct PARI lower descent for `D4-DN-2C`

## 2026-07-26 — clean-room reconstruction

- Read only the frozen contact atlas in `d4_dn2c_full_rebuild/NOTE.md`;
  no file in `d4_dn2c_full_descent` was inspected.
- Rebuilt the weighted determinant directly in PARI/GP with every lower
  coefficient present.
- Found three lower-variable-free transverse \(E_5\) coefficients.  Their
  exact projective gcd is the common-line equation \(2k+3s\), excluding
  both plane interiors.
- Recomputed the punctured common line with pivot chain
  \[
  186624k,\quad -16k^3/3,\quad 32k^3,\quad 2k,\quad -4k^2.
  \]
- Resolved the complete compatibility tree:
  \(S=0\), \(T_\Delta=0\), \(YB=0\), then \(B=0\), then \(YW=0\).
  The \(W=0\) branch forces \(\det L=0\); on \(Y=0,W\ne0\),
  \(E_3=kWH\) and the final residuals are \(-kW^2/2\), a contradiction.
- At the origin, two \(E_4\) squares force \(b_{qr}=L_{33}=0\);
  all five \(E_6\)-pivot variables then vanish.  Added a direct adjugate
  verification of the plane exit.
- Added and ran a strict wrapper with two required-failure mutations.
  Terminal marker:
  `D4_DN2C_DIRECT_PARI_LOWER_STRICT_PASS`.

## 2026-07-26 — independent contact-atlas reconstruction

- Extended the clean-room PARI calculation upward to the raw top forms,
  without inspecting or importing the primary SymPy descent.
- Reconstructed the three \(E_7\) blocks with ranks \(2,3,4\), nullities
  \(0,2,4\), and exhibited a six-parameter kernel spanning the full
  nullity.
- Derived the \(E_6\), \(r^3\) equations forcing the first two contact
  parameters to vanish.
- Reconstructed the constant \(6\times2\) contact matrix, selected the
  independent pivot \(-144\), and obtained the reduced compatibility
  equations \(g=2b+3y=0\) and \(f=0\).
- Factored the reduced quadratic over \(\eta^2=-2\) into two distinct
  conjugate hyperplanes.  Verified directly that their intersection is
  \(2k+3s=0\), with punctured line and origin as the only boundary
  charts.
- Reconstructed the complete 13-equation \(E_6\) system in all 18 lower
  variables.  Exact ranks and pivots are \(7\) with
  \(93312(\eta-1)(2k+3s)^2\) on one plane (and its conjugate), \(6\)
  with \(186624k\) on the punctured line, and \(5\) with \(-31104\) at
  the origin.  Full residual solves vanish on every chart.
- Added the contact certificate to the strict wrapper and a third
  required-failure mutation corrupting the doubled contact hyperplane.
  The full wrapper passed at `2026-07-26T07:08:33Z` with terminal marker
  `D4_DN2C_DIRECT_PARI_FULL_FAMILY_STRICT_PASS`.
