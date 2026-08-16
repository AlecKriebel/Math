# v1.1.1 referee-hardening log

## 2026-08-16T16:45:00-07:00 — report adjudicated

- Independently adjudicated every report item against the active manuscript.
- Confirmed two mandatory written-proof defects: missing componentwise
  all-zero bridge normalization and the omitted finite-target-type selection.
- Found no counterexample to the classification theorem and retained its
  scope.

## 2026-08-16T17:25:00-07:00 — targeted revision compiled

- Added bridge normalization, finite-cover selection, physical-section and
  tangent-space details, genericity notation, and the requested local
  certificate clarifications.
- Changed the title to state “generic-identifiability” explicitly.
- Moved all four Figure 2 theta labels from y=-2 to y=-2.35.
- Rebuilt a 31-page manuscript and six-page supplement without overfull boxes
  or unresolved references. Full-size inspection confirms that Figures 2 and
  4 have no overlap.
- Added an initial five-mutation fail-closed regression for the referee repairs.

## 2026-08-16T18:05:00-07:00 — second adversarial pass repaired

- A mathematical reviewer found no counterexample but caught a literal
  finite-cover overstatement; the proof now measures `U intersect Y_tau` and
  explicitly chooses a preimage in the smooth full-model locus.
- A release reviewer confirmed the visual repair and title synchronization,
  then deliberately broke the first regression using TeX comments and a
  moved graph node.  The regression now strips comments, measures geometric
  clearance, reads embedded PDF titles, and rejects eight mutations.
- Added the v1.1.1 node to the active dependency graph and crosswalk.  A fresh
  build, visual audit, core seal, immutable commit, and all three clean replay
  commands remain mandatory before release.
