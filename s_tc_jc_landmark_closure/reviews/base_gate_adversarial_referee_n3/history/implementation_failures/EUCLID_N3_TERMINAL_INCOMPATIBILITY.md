# Preserved upstream terminal-audit incompatibility

Status: **UNRESOLVED in the frozen Euclid routine; independently replaced in
this referee package.**

The active n=3 relation stream uses these terminal labels:

- `generic_polynomial_separation`;
- `refined_by_next_restoration`;
- `strict_open_cube_separation`;
- `support_prefix_labelled_isomorphism`;
- `support_prefix_ordinary_T`.

The frozen Euclid routine
`reviews/final_hard_cover_cleanroom/audit_candidate_stream.py`, at reviewed
commit `1018701d04d8656fe9ac92bb201413e043b802a1`, recognizes the isomorphism
label and the generic-polynomial label, but its terminal dispatch recognizes
triangle redirection only as `support_prefix_triangle_redirection` or
`ordinary_triangle_redirection`. It does not recognize
`support_prefix_ordinary_T`, and it has no branch for
`strict_open_cube_separation`.

An attempted full replay of that routine against the active n=3 streams was
therefore not accepted as evidence. The run was manually interrupted after
approximately twenty minutes while it was still deriving generic separators;
the interruption produced a `KeyboardInterrupt` traceback inside the dynamic
separator calculation. No output from that interrupted run is used by this
package.

The useful, already-completed Euclid artifact is restricted to the path layer:
`certificates/schema3_n3_path_audit.json` has SHA-256
`6e304691ffeea6d9bc1118b59d778a1051e8fc1f9c3430e06b77fe48c82d8a97`,
reports `VERIFIED`, and explicitly records that the terminal audit was
skipped.

This package independently replaces the unsupported terminal layer. Its
stdlib verifier reconstructs the active graph algebra, all 246 active
descriptor/invariant classes, all 225 stored polynomial bodies, all 280 exact
zero-side classes, all 40 strict-active classes, all 27 strict-sign bodies,
and all 120 isomorphism
plus 24 ordinary-`T` terminal topologies. Consequently, the Euclid terminal
incompatibility is a limitation of an upstream review tool, not a repair to
the candidate relation stream and not a mathematical assumption in the
verdict.
