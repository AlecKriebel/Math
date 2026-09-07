# Verification-output provenance

These files are stored evidence, not additional theorem statements.  Their
scope and generating commands are listed in `PROVENANCE.tsv`.

Evidence classes are intentionally distinguished:

- **exact generation**: byte-deterministic JSON or TeX regeneration;
- **exact aggregate/interface regression**: exact assertions, sometimes over
  selected dimensions or against separately printed formulas;
- **mutation/regression test**: failure-sensitive software coverage;
- **numerical illustration or spectral regression**: finite floating-point
  evidence, never an all-dimensional proof;
- **source/PDF/stale-string audit**: release-presentation hygiene.

The full-tree and portable stale-claim audits have different file counts and
must not be interchanged.  Public packaging regenerates the portable audit from
the staged public tree.  The downloaded release manifest is likewise distinct
from `replay_self_consistency_manifest.txt`: the former is an immutable
baseline, while the latter records the tree produced by a particular replay.

The current sidecar records the completed v1.0.11 qualification campaign.
Entries explicitly labeled `current-release-qualification` are preserved
negative-control or exhaustive-entrypoint results from the pristine candidate;
portable replay does not misrepresent them as newly generated evidence.
