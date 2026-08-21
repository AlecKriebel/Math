# Research log

## 2026-08-21 08:59 PDT

- Began a clean-room adversarial review of the weak-class sharpness package.
- Froze success criteria: independent graph encodings; all-edge rooting
  census; exact relation test; exact tensor and rank replay; physical CT
  checks; and a reversible all-(n) cherry induction.
- Estimated completion of this audit: 10%.

## 2026-08-21 09:06 PDT

- Independently recovered rooting censuses ((5,2,3)) and ((7,2,5)), including
  explicit trials on all reticulation edges.
- Exact incidence expansion found no isomorphism and no ordinary-triangle
  quotient match.
- Independent four-switch rational expansion reproduced the shared tensor and
  both nonzero rank-nine minors.
- Found one fail-closed weakness in the primary cherry-domain loop: it tests
  same-sector pairs rather than actual cross-sector physical edge pairs.  The
  stated actual pairs nevertheless pass the correct CT inequalities.
- Estimated completion of this audit: 75%.

## 2026-08-21 09:11 PDT

- Added an explicit analytic local inverse for the four cherry variables and
  recovery of all old tensor coordinates.
- Attached and pruned a cherry for every admissible rooting; all twelve TC
  statuses are preserved and every directed base graph is recovered exactly.
- Verified that added edges are bridges, triangle counts do not change, and
  the four-leaf extensions remain inequivalent.
- Rejected 20 targeted graph, role, census, parameter, tensor, minor, cherry,
  CT, and pruning mutations, plus optimized-mode execution.
- Exact replay: under 0.3 seconds and under 44 MB RSS.  Mutation replay: under
  1 second and under 50 MB RSS on the local M1 Pro.
- Result: PASS with no mathematical blocker.  Completion of the assigned
  weak-sharpness audit: 100%.  This percentage does not assess the separate
  global K2P-SAME closure program.
