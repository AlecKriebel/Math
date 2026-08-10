# STC-JC final repair research log

This log records the fail-closed repair of the proposed standard strongly
tree-child level-2 Jukes--Cantor identifiability theorem.

## 2026-08-09T00:00:00-07:00 -- repair program opened

- Authoritative starting status: **Outcome B; positive theorem unresolved and
  withheld**.
- Created an isolated worktree from `origin/main` because the existing `main`
  worktree contains unrelated uncommitted research.
- The target theorem is treated as a hypothesis, not as an inherited fact.
- Historical positive manuscripts, cover letters, referee guides, and release
  certificates are quarantined as non-authoritative until regenerated.
- Required gates: locked standard conventions; corrected bridge quotient with
  exact kernel; decorated primitive pair atlas; arbitrary-subdivision
  promotion; directed local-to-global theorem; clean independent replay;
  manuscript/source/PDF consistency.
- Initial completion estimate: **5%**.  The exact Theta sharpness result and
  several local identities survive, but the flagship proof has multiple
  load-bearing gaps.

## 2026-08-09T17:47:45-07:00 -- public status corrected; salvage replay begun

- Replaced the misleading top-level “author-ready” status with an explicit
  submission hold.  Historical manuscript and release files remain preserved
  but are quarantined as evidence, not endorsed outputs.
- Replayed the historical release verifier.  It prints `PASS`, but inspection
  confirms that its synthesis stage trusts frozen status strings and its
  seven-port stage proves only a conditional `192 -> 1,686` calculation.
- Located later, self-contained Gate 1, Gate 2, and Gate 3 implementations in
  the earlier research directory.  Their claims are being replayed from the
  isolated repair worktree before any file is promoted.
- Started the independent nonroot Gate 2 replay.  It uses one CPU core and
  bounded memory; no large frozen signature dump is being copied.
- Machine note: only about 9.7 GiB of free disk remains.  The repair will copy
  only theorem-bearing source and compact certificates, not the 531 MiB
  omnibus research tree.
- Completion estimate: **7%**.

## 2026-08-09T18:18:40-07:00 -- definitions and 2-sub-blob gate audited

- Completed the independent definitions audit without changing the
  manuscript.  The review is recorded in
  `repair/reviews/DEFINITIONS_GATE_REVIEW.md`; the standalone finite validator
  is `repair/independent/definitions/validate_standard_definitions.py`.
- **Load-bearing correction:** the cyclomatic no-subblob lemma is valid for a
  connected induced gadget with exactly two external incident edges, but that
  is stronger than the literal 2-sub-blob definition in Brits et al., which
  specifies two boundary vertices.  A standard strongly-tree-child 4-sunlet
  has a literal two-boundary-vertex subgraph with four external incidences.
  This is a definition/suppression inconsistency, not by itself a JC model
  counterexample.
- The exact two-edge case is fully closed.  Degree counting leaves only
  `K4-e`; an independent Python census and a separately written C++ census
  both find 25 LSA-valid binary acyclic rootings and zero tree-child rootings.
- Found a second exact convention counterexample: if the manuscript's
  undefined parallel-artifact rule is read as broad exhaustive
  root/parallel/degree-two cleanup, it cannot define all admissible rootings
  while retaining the narrower local `S_TC` arrow-tail criterion.  A narrow
  reticulation-preserving reading excludes the witness but must be stated.
- An independent read-only adversarial reviewer agreed with both P0 findings,
  accepted the corrected cyclomatic proof, and found no additional defect in
  the finite `K4-e` conclusion.  Its report is preserved at
  `repair/independent/definitions/ADVERSARIAL_REVIEW.md`.
- Gate D remains **OPEN/FAILED**.  The full positive theorem stays withheld.
  The maximal definitionally safe scope is an explicitly narrow-standard,
  operationally 2-subblob-reduced class, or a theorem modulo a separately
  defined 2-subblob quotient with root-trapping arrows treated one-sidedly.
- Definitions-audit task completion: **100%**.  Overall final-repair program
  completion estimate: **9%**; this checkpoint removes an ambiguity but does
  not verify any of the remaining global theorem gates.
## 2026-08-09T18:14:14-07:00 — bridge gate closed conditionally; fallback scope locked

- The independent bridge reviewer proved the exact full-incidence scaling
  fiber on leaf-supported component trees and a direct marginal-localization
  theorem that avoids the withdrawn physical-bridge chart.
- The reviewer also produced an exact retained-bivalent-factor counterexample
  to the unrestricted product chart.  The positive theorem therefore still
  depends on the standard-reduction/2-sub-blob gate and the complete local
  atlas.
- Structural inspection of the long Gate-2 replay found that its claimed
  arbitrary-subdivision closure includes finite regressions and prose rather
  than an executable quantified proof; a PASS from that program will not be
  promoted without the separate atlas reviewer.
- The original four-leaf counterexample and all-`n` extension replayed under
  the local pinned environment.  A fresh independent reviewer is rebuilding
  the sharpness theorem, including exact positivity and dimension bounds.
- Added `FALLBACK_SUBMISSION_SCOPE.md`.  If the positive atlas gate remains
  unresolved, the release will be a standalone, honest sharpness paper rather
  than another conditional positive manuscript.

Estimated mathematical closure: 15%.  The bridge necessity mechanism is now
sound; the finite atlas remains the critical positive-theorem blocker.

## 2026-08-09T18:29:00-07:00 -- independent atlas gate fails; Endpoint B selected

- The independent atlas reviewer completed an adversarial, mutation-sensitive
  audit.  Exact internal replay supports the stored `k=5`, `k=6`, and cut
  table algebra, including containment direction and every referenced sign
  factor.
- The positive release nevertheless fails its end-to-end gate.  Nine inputs
  required by the advertised compiler are absent from all supplied folders,
  archives, and Git histories.  No durable artifact binds each primitive
  source-target topology pair to its displayed-tree pullbacks and separator.
- The `1,152` and `1,686` seven-port counts concern target-only graph
  quotients, not decorated directed pairs.  Deleting 4,176 of the 4,368
  upstream census records leaves both historical seven-port checks passing,
  proving that those checks do not certify the load-bearing reduction.
- The later Gate-2 script contains substantial exact algebra but records no
  successful pair-level bindings and promotes arbitrary subdivisions from
  finite tests plus prose.  Its independent crosscheck failed with a broken
  pipe.  Even a successful primary replay cannot repair these structural
  omissions.
- No mathematical counterexample to the intended standard-class theorem was
  found.  Its correct status is **UNRESOLVED**, not false.
- Endpoint B is now selected: prepare a standalone all-taxa Theta sharpness
  submission in `W_TC \\ S_TC`, with the positive theorem mentioned only as
  unresolved background.

Atlas audit: **100% complete**.  Positive classification: **withheld**.
Endpoint-B release preparation: **approximately 55% complete**, pending the
fresh sharpness reviewer, clean reproducibility package, and final PDF audit.
