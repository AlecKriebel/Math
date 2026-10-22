# Disk-light checkpoint review

Reviewed statically, 2026-10-21. Review complete (100% for this scoped tooling
review, not for the sweep). Source SHA-256:
`2cb00c6cf41c52315b38673b9b70b7b6705081459061aa2921cb9c004a1d97f3`.
No production execution, API mutation, external interaction, large allocation,
credential inspection, or shared Git mutation occurred. This small report is
the only review write.

The core overlay/concurrency mechanism is sound on static inspection: explicit
owned paths, symlink/traversal rejection, stable per-file reads, contiguous
cursor/journal check, fresh parent/tree, full owned-folder leaf comparison,
single-parent commit verification, non-forced main update, retry after a main
advance, and descendant/identity confirmation. Unselected owned-folder leaves
are compared by `(mode,type,sha)`. The API does not create a release or a Zenodo
record. Upload inputs are supplied through structured stdin, not shell text.

Two small guard repairs are recommended before first execution:

1. **Pin `gh api` to `--hostname github.com`.** `verify_destination()` validates
   Git transport configuration, while every actual mutation here uses the
   GitHub CLI's independently selected API host. A `GH_HOST` environment value
   could redirect requests to another server's same-named repository despite
   passing the Git URL check. The current review environment has no `GH_HOST`,
   so this is not an observed wrong-host incident. Explicit host binding removes
   that dependence and matches the intended publication destination.

2. **Compare every unselected root entry's full `(mode,type,sha)` tuple.** The
   root comparison currently compares only SHA. For example an unrelated
   `100644` blob can become `100755` with the same SHA and pass that check.
   The request's valid `base_tree` overlay should preserve those modes, so no
   such change is observed or expected from normal GitHub behavior. However,
   the promised independent preservation check should detect it, as the nested
   leaf check already does. Reuse the same tuple comparison at root level.

Scope limitations: selected files are snapshotted once; avoid concurrent writers
to this program's selected files during the invocation. State/journal validation
checks numeric contiguity, not agreement of every record's contents. The
four-digit receipt filename regex covers the currently observed PR range but
should become `\d{4,}` if PR numbering ever exceeds 9999. None of these points
authorizes overwriting selected files owned by another effort; the whitelist
and dedicated-folder ownership remain essential.

The successful remote receipt is printed before the final local JSON write,
which is appropriate under ENOSPC. A local write failure after the ref update
must be reported as a saved remote checkpoint with a local receipt failure,
rather than retried as though no commit was pushed. The next dry run's
`already_recorded` detection and live main comparison provide recovery paths.
