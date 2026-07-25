# Research log

## 2026-07-24

- Froze the direct K7 source certificate at SHA-256
  `e666aea9882e10b25be7d73bd288a959f3df7bf8dd8f68dc6bb02f2fdf96ce19`.
- Its 51 distinct \(S_7\)-orbits expand to 221,340 labeled K7 matrices, with
  orbit sizes 840 (1 atom), 1,260 (1 atom), 2,520 (11 atoms), and 5,040
  (38 atoms).
- Grouping labeled K7 faces by their common labeled K6 restriction gives
  192,045 keys and 298,500 compatible ordered pairs.  Trying all seven
  colors on the remaining edge gives 2,089,500 K8 trials.
- No trial has all eight K7 faces in the frozen support.  Thus the
  support-specific extension fails before rank or Schur tests are reached.
- Current estimated completion toward the full assigned K8 investigation:
  **40%**.
- Used a positive-definite five-vertex principal block of each K7 atom to
  enumerate a new vector through the exact Schur norm equation.  The two
  omitted correlations are forced by exact range equations.
- Extending the 51 explicit K7 atoms produced 2,064 labeled rank-five K8
  patterns and 1,908 distinct triangle-count vectors.
- A numerical LP found a 51-column basis with maximum residual
  \(8.89\cdot10^{-15}\).  Exact rational reconstruction gave 51 strictly
  positive weights satisfying every marginal equation.
- The independent standard-library verifier checks every principal minor,
  exact rank five, all exact weights, and the pair/triple marginals.
- The fixed-support and direct verifiers passed, followed by six combined
  exact/tamper/reference-determinant tests in 14.719 seconds.  The direct
  certificate SHA-256 is
  `9499977c14f3de72cd0b55d83872a645f2727f120182d010967832106b65b195`;
  the fixed-support certificate SHA-256 is
  `d33ec89e5067d2fbd177e83f2a6dc45708368bd01dfc573c9c8a297172b035d0`.
- Final estimated completion toward the assigned K8 investigation:
  **100%**.
