# Final release audit

## Final verdict

**VERIFIED — release 2.0.0 is a submission-ready sharpness package.**

This verdict applies only to the manuscript *Full-Dimensional Jukes--Cantor
Ambiguity in Weakly Tree-Child Level-2 Networks*.  The earlier positive
classification of standard strongly tree-child level-2 networks is
**UNRESOLVED**, not refuted, and is not asserted by this release.

## Theorem retained

For every `n >= 4`, the release gives two explicit leaf-labelled binary
level-2 semi-directed networks in `W_TC \ S_TC` that are nonisomorphic and
not related by ordinary triangle redirection, while their open JC models in
`Theta_0` share a regular relatively open region of full dimension `2n`.

The four-leaf case is supported by an exact quadratic-algebraic common point,
strict interior inequalities, equality of all 256 Fourier and pattern
coordinates, a common irreducible eight-dimensional locus, and exact nonzero
rank-eight Jacobian minors.  A positive real-analytic inverse for repeated
cherry substitution proves the all-taxa statement.

## Independent verification

- The primary verifier derives displayed-tree Fourier maps from rooted arc
  lists using pinned SymPy and NetworkX versions.
- A separately written standard-library verifier shares no graph, Fourier,
  number-field, isomorphism, or rank modules with the primary implementation.
- The independent certificate is byte-deterministic under three distinct
  Python hash seeds and is locked at
  `38266537a7966d83bdb94c6fb90fa68f93fbd227b82579f1bf311005925366d7`.
- The adversarial sharpness review and manuscript rereview found no remaining
  mathematical defect.  Every P1/P2 manuscript or release issue identified
  by those reviews was corrected before the final manifest was generated.
- Two consecutive Tectonic builds are byte-identical.  All ten pages were
  rendered and inspected, and all font resources are embedded.
- Both deterministic ZIP archives were extracted and checked; the extracted
  reproducibility package passed its exact driver, and the extracted source
  rebuilt the distributed PDF byte for byte.
- The complete release driver passed from a clean Git worktree.

## Withdrawn and excluded claims

No active file asserts a complete finite atlas, bridge-tree reconstruction,
one-sided-containment classification, automatic triangle bound, positive
theorem for `S_TC`, K2P/K3P extension, or efficient inference algorithm.
Contradictory historical generations are isolated under
`quarantine/withdrawn_positive_v1.1.1/` and are evidence of the audit history,
not submission materials.

The constructed pair contains a triangle as well as failing strong
tree-childness.  It therefore does not settle either the standard strongly
tree-child class or the triangle-free weakly tree-child subclass.

## Remaining human submission choices

The mathematical and reproducibility package is complete.  Journal choice,
house style, affiliation, correspondence address, ORCID, funding and conflict
statements, and a journal-specific cover letter remain for the author to
select before transmission to a venue.
