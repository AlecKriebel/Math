# Crosswalk and bundle research log

## 2026-08-21 21:30 PDT — Exact crosswalk and draft bundle recipe

- Reconstructed the full 370-file, 434,661,763-byte frozen evidence ledger
  from the outer lock, two nested SHA manifests, and both direct-closure locks.
- Bound 13 theorem layers to exact authority, producer, replay, mutation,
  environment, schema, and file-hash fields.
- Preserved recorded component timings only where a locked JSON field exists;
  quick/full end-to-end runtimes remain explicitly unknown.
- Added the optional supplement compression table at its anticipated input
  point, with the restoration and probe residues labelled `PC-PARTIAL`.
- Built primary and independent manifest checkers, eight semantic mutations,
  optimized-mode rejection, and an explicit no-`assert` AST scan.
- Did not create the large ZIP archive.

Best-guess completion of the crosswalk/bundle subtask: **95%**.  The remaining
5% is the mandatory final reseal after concurrent article and integration
edits stop; the checker is intended to fail until that reseal is performed.
