# Research log

## 2026-08-21 15:46 PDT — independent full-probe closure

- Reconstructed all 176 primitive physical anchors and all 2,206 sites per
  side from the frozen v2 input contract; primitive replay payload
  `96d14bae9b20646abfe64b85a7ac0f61377182f75479031f621ea0dbe2096fce`.
- Independently streamed all 29,964 one-port and 544,571 two-port rows.
- Proved and replayed the exact site-transport partition: incompatible pairs
  are precisely quartet rows; compatible pairs are precisely labelled
  isomorphisms, inherited ordinary triangles, or direct full-map `T_i`
  separators.
- Applied all 67,741 exact transport records to rebuilt graphs, reconstructed
  all 4,379 marginal commitments, replayed every reverse restriction and
  global triangle, and checked all quartet and exact Bernstein data.
- Rejected 12/12 targeted mutations; zero unresolved, incoherent, missing,
  duplicated, cyclic, orphaned, or legacy-rooted records remain.
- The first resource-instrumented pass was stopped below the 4 GB guard after
  identifying a graph-specific Fourier pullback cache.  The final program
  clears that cache per parent and completed in 617.91 seconds with peak RSS
  2,181,349,376 bytes.  This is an auxiliary clean-room audit.  The official
  builder/verifier remain the referee path at 451,903,488 bytes and about
  72 MB respectively.
- Final graph-audit payload:
  `65160636abfa33de47136a222081ac70bd7b6fae0e029b7a7c379e2d8653df74`.

Best-guess completion toward the corrected full-probe audit goal: **100%**.
Best-guess completion toward unconditional theorem promotion from this layer:
**100%**; no probe-layer blocker remains.

## 2026-08-22 12:38 PDT — stable-source rebind replay

- Replayed the audit after removing wall-clock telemetry from the primary
  certificate bytes. The mathematical primary payload remains `674853fa...`;
  its deterministic file SHA-256 is now `93de7b0d...`.
- All 176 anchors, 29,964 one-port rows, 544,571 two-port rows, 67,741 exact
  transports, 4,379 restrictions, and 12 mutations passed again with no census
  change. The refreshed audit payload is `4492860f...`.
- Runtime was 456.41 seconds. `/usr/bin/time -l` recorded peak memory footprint
  2,136,999,808 bytes; the auxiliary audit remains below its 4 GB guard.

Completion remains **100%** for the corrected full-probe audit goal.
