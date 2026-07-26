# Research log

## 2026-07-26T05:35:49Z

- Reconstructed the normalized `D4-DN-3` weighted determinant directly in
  PARI/GP for the punctured common line and its origin.
- Certified the five punctured-chart pivots
  \(-279936k,192k^4,108k^3,3k^4,9k^2\), with all solution denominators
  supported only at \(k=0\).
- Added the previously missing fail-closed assertions for all three
  \(E_4\) coefficients forcing \(S=0\).
- Verified all six post-\(S\) \(E_5\) residuals and the \(kD^2\) branch,
  followed by complete \(E_5,E_4\) residual checks and the literal
  identity \(\det L=0\).
- Rebuilt the origin without specializing a punctured-chart solution,
  checked its constant \(E_6\) pivot, both \(E_4\) squares, and the complete
  binary collapse.
- Added a denominator-free adjugate computation that reduces the binary
  origin to an unconditional degree-at-most-four plane Keller map.
- Added a strict wrapper with two deliberately failing mutations.

## Scope

This is an independent PARI implementation for
`DN3-INTERSECTION-SNZ` and `DN3-ORIGIN`.  It is not a certification of the
two transverse plane interiors or of the complete frozen family.
