# Research log

## 2026-07-23

- Froze the direct K8 source certificate at SHA-256
  `9499977c14f3de72cd0b55d83872a645f2727f120182d010967832106b65b195`.
- Its 51 distinct \(S_8\)-orbits expand to 1,824,480 labeled K8 matrices,
  with orbit sizes 10,080 (1 atom), 20,160 (10 atoms), and 40,320
  (40 atoms).
- Grouping labeled K8 faces by their common labeled K7 restriction gives
  1,635,480 keys and 2,502,360 compatible ordered pairs.  Trying all seven
  colors on the remaining edge gives 17,516,520 K9 trials.
- No trial has all nine K8 faces in the frozen support.  Thus the
  support-specific extension fails before rank equations are reached.
- Used a positive-definite five-vertex principal block of each K8 atom to
  enumerate a new vector through the exact Schur norm equation.  The three
  omitted correlations are forced by exact range equations.
- Extending the 51 explicit K8 atoms produced 1,926 labeled rank-five K9
  patterns and 1,811 distinct triangle-count vectors.
- A numerical LP found a 51-column basis with maximum residual
  \(2.85\cdot10^{-14}\).  Exact rational reconstruction gave 51 strictly
  positive weights satisfying every marginal equation.
- The direct and fixed-support verifiers passed, followed by eight combined
  exact, tamper, reference-determinant, constant-support, and independent
  Python-bruteforce/core-comparison tests in 7.305 seconds.
- The direct certificate SHA-256 is
  `b0ead73d99ea050a002a36bfd78f549348d37d19244c147228bee26ad692b148`;
  the fixed-support certificate SHA-256 is
  `98d25daea169831dc75caaf5686dd46767006c44d16c80be9a9959eb96c14ac4`.
- Replayed the deterministic discovery pipeline byte-for-byte.
- Final estimated completion toward the assigned K9 investigation:
  **100%**.
