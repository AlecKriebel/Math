# Research log

## 2026-07-23

- Froze the direct K9 source certificate at SHA-256
  `b0ead73d99ea050a002a36bfd78f549348d37d19244c147228bee26ad692b148`.
- Exact automorphism and canonical-orbit enumeration gives 16,057,440
  labeled matrices in its 51 \(S_9\)-orbits: 38 full orbits, 12 half
  orbits, and one quarter orbit.
- Any K8-overlap gluing has at least 112,402,080 missing-edge color trials.
  A 16-byte packed support array alone occupies 256,919,040 bytes.  The full
  frozen-support enumeration was skipped under the explicit growth-control
  instruction; no obstruction is claimed.
- Exact five-basis Schur/range enumeration of the 51 K9 atoms produced 1,783
  labeled rank-five K10 patterns and 1,650 distinct triangle-count vectors.
- A numerical LP found a 51-column basis with maximum residual
  \(1.07\cdot10^{-14}\).  Exact rational reconstruction gave 51 strictly
  positive weights satisfying every marginal equation.
- The direct and size-audit verifiers passed, followed by seven exact,
  tamper, reference-determinant, and toy-orbit tests in 5.236 seconds.
- The direct certificate SHA-256 is
  `542f3061bfe282d98580955e62e756bfd9646890a45747f0baad8b11f750cc28`;
  the frozen-support size certificate SHA-256 is
  `d2f3a627ad4757f44f1382282027835c289cec422c7cb09bd0d771113e428eda`.
- Replayed the deterministic discovery pipeline byte-for-byte.
- Final estimated completion toward the assigned K10 investigation:
  **100%**.
