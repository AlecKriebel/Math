# Ideal-certificate research log

## 2026-10-01T05:02:10Z — first proof checkpoint

Task: independently certify local lengths, generator minima and resolutions
for finite PR11 stress examples, outside the matrix Koszul-rank calculation.

- Confirmed the proposed plane non-CI is actually a CI: the exact identity
  `v(u^2-v^3)-u(uv)=-v^4` eliminates the third generator. Length five,
  minimal generator count two.
- Constructed a genuinely nonhomogeneous replacement of length five:
  `(u^4,uv-u^3,v^2)`, coordinate-equivalent to `(a^4,ab,b^2)`.
  Derived its full two-column syzygy matrix and a divisibility proof of
  exactness, so its minimal generator count is three.
- Proved the nonlinear triangular-coordinate ideal is a length-six CI
  with three minimal generators.
- Established tensor-extension length and generator-count proofs. Selected
  dimensions four and five with length twenty and counts five and seven.
- Independent child adversary has verified the three-variable Gorenstein
  example, including characteristic two; awaiting its checkable report.
- Decision: the redundant plane example is a useful falsifier and must not
  be reported as a non-CI.

Best-guess completion toward this finite-certificate task: **75%**. Remaining:
executable exact identity/table checks and final reconciliation with the child
report. The general PR11 theorem is outside this percentage.

## 2026-10-01T05:15:53Z — final independent validation checkpoint

- The dependency-free exact script passed: polynomial identities, plane
  syzygy compositions and signed minors, triangular coordinate inverse,
  all seven finite quotient models, and 16,807 basis associativity checks.
- Independently proved the full Betti vector for `m^2` by decreasing-lex
  linear quotients and graded minimal mapping cones. The script verified
  every colon in dimensions one through seven (84 generators total).
  The dimension-five vector is `(1,15,40,45,24,5)`; length six, `mu=15`.
- Read the child Gorenstein derivation: exact middle-kernel calculation,
  injective final map, matching Hilbert series for remaining exactness,
  all-field Frobenius pairing and generator minimality. Reran its exact
  identity checker successfully.
- Child adversary also reviewed the replacement plane generator change,
  resolution matrix, characteristic-two signs, tensor generator minima,
  coefficient-shift cones, lex colon order, and mapping-cone grading.
  No mathematical error, hidden unit entry, or circular criterion was found.
- Added and checked the equal-squares Gorenstein complex coordinate map;
  seven identities passed exactly in `Q(i,sqrt(2))`. The complex isomorphism
  transports the resolution, and flat field extension preserves rational
  Betti ranks. The actual isomorphism is over C: over Q or R the
  equal-squares degree-one square form is anisotropic while J has nonzero
  square-zero degree-one classes. This field distinction does not affect
  the Betti-count conclusion.
- Adversarially reread the parent's additional certificates and report.
  Verified principal and algebraic local CIs, six-variable curvilinear
  coordinates, mixed CRT, epsilon-family ideal equality and basis,
  nonregular transposed-tuple falsifier, and the full-N size falsifier.
  Cross-checked all fourteen case dimensions, lengths, generator counts,
  Betti vectors and the N17 Cartesian candidate counts against its JSON.
  Verdict: PASS, no mathematical or data mismatch found.
- Parent independently reran both certificate scripts from a scratch copy;
  mathematical outputs matched. The child's final adversarial review is
  recorded in `gorenstein_falsifier/parent_report_adversarial_review.md`.
- Strongest result: all stated finite lengths and minimal generator counts
  are rigorous; all stated resolutions have independent exactness and
  minimality proofs. The general `m^2` Betti formula is separately proved,
  with finite checks used only as corroboration.
- Exact remaining gap: none in this certificate subtask. These examples do
  not settle the general PR11 matrix characterization, global lifting
  question, or source/priority audit.

Best-guess completion toward this finite-certificate task: **100%**.
All work remains within the assigned audit folder. No canonical snapshot
edit, Git action, or external communication was performed.
