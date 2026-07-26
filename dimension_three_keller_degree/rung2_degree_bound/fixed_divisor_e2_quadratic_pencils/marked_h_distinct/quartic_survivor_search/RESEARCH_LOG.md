# Research log

## 2026-07-26 — finite nonzero smooth-secant family

- Began from the released complete \(E_7\) normal form for
  \(r=h+kx^2\), \(k\ne0\).
- Reconstructed the weighted determinant without imposing any lower-degree
  ansatz beyond that normal form.
- Found that \(E_6\) is triangular: its twelve nonzero coefficients force
  ten lower coefficients to zero.  The only saturation factor is \(k^2\),
  so its sole exceptional chart is the already-frozen \(k=0\) boundary.
- Found that reduced \(E_5\) has six coefficients and forces the remaining
  entries in columns two and three of \(L\) to zero.  Hence \(\det L=0\).
- The obstruction is uniform in \(A,B,T\) and every finite \(k\ne0\); no
  candidate survives to \(E_4\).
- Added exact SymPy and independent PARI/GP reconstructions plus an
  all-parameter modular scan over nine prime fields.
- Scope: `CTAU` and its finite `CT` boundary only.  The parent row and
  the \(k=0,\infty\) boundaries remain outside this result.

## 2026-07-26 — six endpoint audit

- Independently continued all six released `CH/CS` normal forms over every
  field-valued component of their \(E_6\) compatibility radicals.
- Five force \(\det L=0\) at \(E_5\).
- Found an explicit counterexample to the provisional claim that all six
  die at \(E_5\): the `MD-P3-HSM-CH` slice has an invertible through-\(E_5\)
  witness.
- Solved its complete surviving \(E_5\) family.  Its determinant is
  \(T\ell_7(6Bb_3\ell_6+a_3\ell_3-b_3\ell_0)\).
- Two \(E_4\) coefficients, \(-8\ell_8^2\) and then \(4\ell_7^2\), exclude
  that last family.
- Added independent exact SymPy and PARI/GP reconstructions and retained
  the sharp through-\(E_5\) witness as a regression.
- Combined directory scope is now eight of thirteen frozen
  marked-distinct internal strata.  The two `CO` and three `C0` strata
  remain outside this package.
