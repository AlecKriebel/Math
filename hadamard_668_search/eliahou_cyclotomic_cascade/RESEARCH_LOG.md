# Research log: Eliahou cyclotomic cascade

## 24 July 2026

- Recast the distance-41 anti-fold after row-pair normalization as the
  two-variable Hermitian equation
  `N(P)+N(Q)=167-N(R)-N(S)` in `Z[z]/(z^42+1)`.
- Made the factor cascade
  `Phi_4`, `Phi_4 Phi_12`, `Phi_4 Phi_28`, `Phi_84` explicit.
- Implemented an exact non-SAT residue-signature join for moduli 2 and 6.
  It factors support selection by residue, aggregates exact multiplicities
  by support weight and Hermitian norm signature, and joins the long and
  short blocks.
- Completed all 30 canonical support instances.  Every case survives both
  layers.  The `Phi_4 Phi_12` counts range from
  `48,953,783,073,014,748` to `107,996,012,316,872,012`.
- Calibrated the known cases.  Certified full-UNSAT case 0 retains
  `79,852,759,562,024,974` low-factor supports.  Solver-observed case 1
  retains `75,920,209,690,765,723`.
- Added representative recovery.  The Python verifier reconstructs every
  representative in the original four anti-fold rows, replays the claimed
  factor identity exactly, and confirms that it is not a full anti-fold
  solution.
- Independently recomputed the complete `Phi_4` census in Python.
- Measured the direct modulus-14 frontier without enumerating it.  The 26
  unique arithmetic block specifications contain `328,470,183,936` raw
  coefficient tuples; the support-weight and zero-lag bounds leave
  `328,145,957,800`.
  Direct `Phi_28` histogram construction was therefore stopped by design.
- Identified the next bounded decomposition: pair residues `j,j+7` and use
  the Gaussian seven-coordinate form at a primitive 28th root, split
  `3+4`, while carrying the existing `Phi_12` signature.
- Independent audit found that the first `3+4` estimate collapsed supports
  that agree modulo 14 but differ modulo 6.  Retaining
  `(weight, mod-14 removal, full mod-6 removal vector)` gives at most eight
  states per residue and 64 per Gaussian coordinate.  Exhaustive refined
  state counting gives sharp half-frontier maxima `262,144` and
  `8,388,608` for the deliberately ordered `3+4` split (generic
  four-coordinate bound `16,777,216`).  The exact low-factor censuses and
  the 328-billion growth census for the original direct method are
  unchanged.  Added this 60-specification enumeration and the concrete
  `L0/P` collision to the frozen certificate, verifier, and regression
  tests.
- Full verification completed in about 23 seconds at approximately 1.21 GB
  peak RSS.  No external communication, commit, or push was performed.
