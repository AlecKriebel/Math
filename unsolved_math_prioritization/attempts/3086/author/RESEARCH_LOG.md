# Bounded investigation log

Problem 3086 / OPG-37327. All times UTC, 2026-10-05.

- 19:03: Requested UnsolvedMath URL failed. Recovered the exact OPG statement,
  independently hashed the supplied datasets, and identified the matching record.
- 19:04-19:07: Read pinned repository metadata, current source pages and recent
  papers. No actual earlier target attempt was found in the inspected repository
  attempt directory, target searches or user-history check. A source-imported
  note and queued desk-review record were not treated as actual proof attempts.
- 19:07: Corrected the stale literature boundary: n=3 was already proved in 2009;
  a September 2026 preprint claims n=4. It is not evidence of journal acceptance.
- 19:08: A numerical single-tile probe found a candidate violation of a source
  local lemma. It was used only to discover a candidate, never as a certificate.
- 19:10: Independently inspected rendered PDF pages 2-3, the exact definitions,
  Lemma 2 and its proof. Positive boundary contact and an additional internal
  horizontal grid intersection confirm the overlooked configuration.
- 19:13: Replaced the numerical candidate by exact Q(sqrt(2)) coordinates, a
  written derivation, generic polygon/segment clipping, exact area verification,
  nearby exact controls and rejecting negative controls. All replay checks pass.

## Four substantive approaches

1. **Area and overlap budget.** Derived the exact multiplicity-weighted loss
   identity. It bounds possible enlargement, but gives no contradiction for an
   arbitrarily small enlargement. Blocked on a uniform geometric loss bound.
2. **Separated point counting and angle constraints.** Proved the axis-parallel
   case, at least 2n rotated tiles in a hypothetical cover, and an angle threshold
   for tiles carrying pairs of test points. The threshold tends to zero, so no
   fixed positive loss follows. Blocked on interaction among those rotated tiles.
3. **Corner-pair boundary estimate.** Gave a self-contained n=1 proof from the
   total top/bottom boundary length covered by a tile containing two corners.
   For larger n, corner tiles do not control the interior. No all-n extension.
4. **Perimeter plus grid-length approach.** Tested the key recent local estimate,
   found and exactly proved its failure, and identified its use in the n=4
   argument. Proved a valid coarse replacement and an all-n scalar feasibility
   family showing why the remaining elementary inequalities do not suffice.
   No unsupported repair of the source theorem was promoted.

## Completion estimate and stopping point

The bounded investigation and author-side certificate replay are complete.
The original all-n research goal remains unresolved; these deductions do not
justify a numerical estimate of proximity to a full solution. A fresh independent
audit is the next verification gate. No external communications or repository
writes were performed by this investigation.

## Audit targets

- Check the closed-square and arbitrary-rotation quantifiers.
- Rebuild the diamond-square example independently of `verify.py`.
- Confirm its only target-side intersection has positive length, its sides have
  length one, and the three grid lengths sum without positive-length double count.
- Compare the exact source definition and Lemma 2, including the unrestricted
  local nature of the estimate, and Section 5's dependence on it.
- Distinguish the local-lemma counterexample from a counterexample to the original
  covering conjecture and from a disproof of the n=4 conclusion.
- Verify the n=1 support-coordinate argument and all-n counting observations.
- Recompute source identities and package hashes. Exclude all raw source files.
