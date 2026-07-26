# Research log

## 2026-07-26 (America/Los_Angeles)

- Draft freeze timestamp: `2026-07-26T07:53:50Z`.
- First public release timestamp: `2026-07-26T08:13:13Z`.
- Isolated the cube-component argument from the quartic power-fibre audit.
- Proved over every algebraically closed field of characteristic zero:
  if \(f=C+\ell^3+Q_2+L_1\in k[x,y,z]\) has no critical point, then
  \(f\) is a polynomial coordinate.  After sending \(\ell\) to \(x\),
  the proof is the exhaustive rank \(2/1/0\) classification of the
  quadratic block transverse to \(x\).  Every surviving chart has an
  explicit inverse of degree at most three.
- An independent hostile audit reproduced the same rank classification
  and found no missing pivot boundary.
- Verified the primary preprint Guccione--Guccione--Horruitiner--Valqui,
  arXiv:2204.14178.  Its abstract says the lower floor for a possible
  plane counterexample is raised from \(100\) to \(108\); equivalently,
  the plane Keller conclusion is available for maximum degree \(<108\).
  Thus \(3d\le105<108\) gives the complex Keller corollary for
  \(d\le35\).  The peer-reviewed publication status of this preprint
  was not located; the conservative Moh fallback is \(d\le33\), since
  \(3d\le99<100\).
- Checked the frozen canonical denominator at
  `fixed_quadratic_line_doublecover/audit_delta_ge3_denominator/DENOMINATOR.json`.
  It has exactly 26 families and SHA-256
  `440df4694f98b1b361a09e136afb4365c3aa302c5532e5291f4b76a2a068c65a`.
  The bridge scope is exactly three newly excluded whole-family points
  (`PF-BRANCH-FOURTH-THIRD`, `D3-BB-30`, `D3-OB-300`), one already
  excluded point (`D4-DN-3`), and only the retained \(z=3\) pivot in
  `D3-SF-20C`.
- Literature searches located broad work on cubic polynomials and
  polynomial variables (including Ribeiro's classification at infinity
  and Kaliman's general-fibre results), but did not locate this precise
  elementary cube-leading submersion lemma.  Worldwide priority remains
  unresolved.
- No files in this artifact have been committed or pushed.
- Release review strengthened the Keller hypothesis from a literal
  component to any nonzero target-linear combination
  \(\alpha\!\cdot\!F\).  Extending \(\alpha\) to a target
  \(\mathrm{GL}_3\)-change makes it a component and shows its gradient
  is nowhere zero.
- Expanded both the note and paper into a division-safe atlas with
  explicit critical witnesses and coordinate inverses for every
  rank-one and rank-zero pivot boundary.
- Added `verify_all_strict.sh` as an aggregate, fail-closed wrapper.  It
  first requires `CUBE_COMPONENT_EXIT_STRICT_PASS` from the primary
  suite, then `CUBE_COMPONENT_HOSTILE_AUDIT_PASS` from the separately
  implemented hostile suite, and only then prints
  `CUBE_COMPONENT_ALL_STRICT_PASS`.  The primary `verify_strict.sh`
  remains the main verifier.
- A second independent geometry/reference audit checked the full rank
  atlas, the ordering \(F\mapsto TF\mapsto (TF)\circ\sigma^{-1}\), the
  strict \(d=35/36\) boundary, and the fibrewise implication.  It found
  no mathematical defect and no exact prior-art collision, while
  explicitly declining a novelty claim.
- The fibre lemma was expanded to avoid shorthand: Ax--Grothendieck
  supplies surjectivity, while the Keller condition and injectivity make
  the map a universally injective étale morphism, hence an open
  immersion and therefore an isomorphism.
- The frozen fine-family consequence is \(9/26\) rather than \(6/26\):
  three whole families are newly counted, `D4-DN-3` is redundant, and
  only one retained pivot of `D3-SF-20C` is covered.  The containing row,
  the global \(4/14,4/14,6/14\) status, and the universal degree floor
  four do not change.
