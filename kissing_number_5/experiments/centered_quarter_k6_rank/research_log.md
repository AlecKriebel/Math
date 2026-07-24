# Research log

## 2026-07-24

- Started a fresh K6 rank-consistency investigation, separate from the K5
  certificate and all central status files.
- Detected that the untracked K5 certificate was replaced concurrently after
  the first read.  The initial version expanded to 4,080 labeled matrices;
  the current SHA-256 `133e8b50...` version expands to 2,940.  The K6
  enumerator records the exact support count in its output and will be tied
  to a full source hash before any conclusion is stated.
- Current estimated completion toward resolving the fixed-support K6
  extension question: **20%**.
- For the current source hash, the brute-force sixth-vertex enumeration
  tested 49,412,580 rows and found 240 support-compatible labeled matrices.
  All 240 have determinant zero and form four \(S_6\)-orbits.
- An independent K4-gluing enumeration reduces completeness checking to
  48,594 color trials and reproduces the same result in 1.9 seconds.
- The four K6 face-count vectors are \(6e_0,6e_{21},6e_{39},6e_{46}\).
  Since stored K5 orbit 1 has positive weight
  \(193319639973/2080000000000\), the exact Farkas vector \(-e_1\) proves
  infeasibility.
- The fixed-support question is therefore **100% complete**.  This
  obstruction is caused by the chosen support; the rank condition eliminates
  none of the 240 support-compatible matrices.
- Current estimated completion toward the broader direct K6
  triangle-marginal exploration: **35%**.
- Developed a Schur-adjugate enumeration mechanism.  Among the 105,930 K5
  triangle-vector representatives, 101,272 are positive definite.  For a
  positive-definite base \(G\), the bordered K6 matrix is PSD of rank five
  exactly when \(z^T\operatorname{adj}(G)z=4\det G\), an integer quadratic
  equation on the seven-color grid.
- Sampling 5,000 evenly spaced positive-definite bases produced 157,083
  labeled rank-five extensions and 137,296 distinct triangle-count vectors.
  A 51-column numerical LP basis matched the target with maximum residual
  \(1.78\cdot10^{-15}\).
- Exact rational reconstruction succeeded with all 51 weights positive.
  The independent verifier checks every principal minor, full determinant,
  triangle count, edge count, and rational marginal.  It passed; the
  minimum positive scaled fifth-order minor is 6.
- Three direct-extension tests passed, including edge and weight tampering.
- A separate 500,000-clique random sample in the suggested 90-vector
  integer alphabet produced 43,128 triangle-count vectors but its sampled
  cone did not contain the target.  This is numerical evidence only and was
  not escalated because the broader exact Schur construction already
  succeeds.
- Final estimated completion toward the assigned fixed-support and direct
  K6 investigation: **100%**.
