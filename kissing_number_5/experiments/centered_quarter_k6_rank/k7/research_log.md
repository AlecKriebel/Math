# Research log

## 2026-07-24

- Froze the direct K6 source certificate at SHA-256
  `32e629ab5df91cf6e616aa1f7a61af22f853b78ccff50947738b5cab1394d0ba`.
- Its 51 distinct \(S_6\)-orbits expand to 26,820 labeled K6 matrices, with
  orbit sizes 180 (9 atoms), 360 (14 atoms), and 720 (28 atoms).
- Grouping labeled K6 faces by their common labeled K5 restriction gives
  22,677 keys and 39,630 compatible ordered pairs.  Trying all seven colors
  on the remaining edge gives 277,410 K7 trials.
- No trial has all seven K6 faces in the frozen support.  Thus the
  support-specific extension fails before rank or Schur tests are reached.
- Current estimated completion toward the full assigned K7 investigation:
  **40%**.
- Used a positive-definite five-vertex principal block of each K6 atom to
  enumerate new correlations through the exact Schur equation
  \(w^T\operatorname{adj}(B)w=4\det B\); the sixth correlation is then
  forced by the K6 nullspace/range identity.
- Extending the 51 explicit K6 atoms produced 2,012 labeled rank-five K7
  patterns and 1,782 distinct triangle-count vectors.
- A numerical LP found a 51-column basis with maximum residual
  \(1.11\cdot10^{-14}\).  Exact rational reconstruction gave 51 strictly
  positive weights satisfying every marginal equation.
- The independent standard-library verifier passed: every principal minor
  is nonnegative, every order-6 and order-7 determinant is zero, every atom
  has a positive fifth-order minor, and the uniform edge and triangle
  marginals are exactly \(\alpha/40\) and \(\nu/1560\).
- Five combined exact/tamper tests passed in 4.617 seconds.
- Final estimated completion toward the assigned K7 investigation:
  **100%**.
