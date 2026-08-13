# Research log

## 2026-08-10 — clean-room lock

- Restricted all implementation to this directory.
- Froze `core_universe.json` and `support_universe.json` as the only topology
  inputs.  Primary hard-cover streams are comparison inputs only.
- Implemented independent rooted validation, exact coloured-graph
  canonicalization, standard semi-directed reduction, skeleton stripping, and
  segment reconstruction.

## 2026-08-10 — completion census

- **EXACTLY COMPUTED:** eight pointwise-rigid source supports with three
  outgoing boundaries.
- **EXACTLY COMPUTED:** the four-selected-boundary completion grammar has 831
  incoming-selected and 1,983 marginalized-incoming raw constructions.  This
  independently matches the two corresponding frozen completion census
  entries.
- **EXACTLY COMPUTED:** after the reviewer's setwise coloured-graph quotient,
  those 2,814 constructions give 1,463 full completion graphs.
- **EXACTLY COMPUTED:** the omitted theta-2 minimum-support stratum has three
  source supports, 1,983 incoming-selected plus 4,155
  marginalized-incoming raw target constructions, and 3,026 reviewer
  completion graphs at five selected boundaries.

## 2026-08-10 — invariant derivation

- Derived the 15 JC quartet-character orbits from `Z2 x Z2`.
- Rejected a first clean-room family of 162 arm-homogeneous quadratic
  binomials as insufficient: it collapses several source supports.
- Replaced it by exact arm-homogeneous degree-at-most-three nullspaces derived
  directly from displayed-tree tensors and closed under all 24 quartet
  permutations.  The n=3 source family contains 1,852 exact relations; the
  theta-2 minimum-support family contains 1,474.  These are reviewer families,
  not copies of the primary 84-invariant selection.
- Every exact pullback and accepted strict sign is regenerated from graph
  switchings.  Primary sign flags are not read.

## 2026-08-10 — current primary stream binding failure

- **FALSE:** the current five n=3 streams do not bind every merged raw
  provenance to its regenerated children.
- Exact counts: 40,072 canonical states, 5,344 root cases, 55,665 path IDs,
  and 6,051 refined states.
- Among the refined states, 1,287 merge raw provenances with unequal emitted
  child-state sets; 2,118 raw paths have no emitted child provenance; the
  declared state-level child set disagrees with at least one merged path in
  all 1,287 cases.
- This is an artifact-completeness failure, not by itself a mathematical
  counterexample.  It prevents the current bytes from certifying fixed-full
  relation coherence.

## 2026-08-10 — additional mandatory coverage

- **UNRESOLVED:** the primary 5,344/40,072 total covers n=3 only and cannot
  cover theta-2's four-outgoing minimum support without a separate proved
  reduction.  No such reduction is assumed.
- **UNRESOLVED:** equal-deck root cases are not the complete directed
  containment universe.  The frozen summaries report 110 n=3 and 776 n=4
  unequal-but-necessary signature directions, but no pair-level relation
  streams are present for independent graph-to-polynomial replay.
- A corrected primary `candidate_full` regeneration was reported as active;
  no moving output is used as evidence.

## 2026-08-10 — p/q extension assessment

- **VERIFIED (conditional design):** after a fixed, path-bound allowed
  terminal `A = Q_s union Q_t`, inserting a new label in every directed blob
  segment position on both sides enumerates all `A+p` placements.  Repeating
  from each allowed `p` state enumerates all `A+p+q` placements and all
  same-segment orders.  The base relation ID, restoration path, and `Q_t`
  transport must remain immutable.  The argument does not repair an
  unresolved base terminal.
- **EXACTLY COMPUTED:** the executable replay covers every cyclic source and
  target arc pair on all eight `n=3` source supports and all three omitted
  theta-2 four-outgoing minimum supports.  Both orders of `p,q` on one segment
  occur.  Incomplete terminal matchings, unsafe port counts, and unapproved
  `p` paths are rejected.

## 2026-08-10 — standard semi-directed strongness check

- Replaced reliance on any all-rooting implementation by the locked exact
  local criterion, after separately checking that the supplied rooted graph
  is an LSA-valid witness and that `sd_0` is a simple binary mixed graph.
- **EXACTLY COMPUTED:** all 4,500 graphs in the regenerated `n=3` and omitted
  theta-2 `n=4`-minimum universes pass; no root-created parallel edge is
  silently overwritten.  The regenerated graph commitments equal the frozen
  clean-room universe commitments.

## 2026-08-10 — schema-2 n=4 failure preserved

- **FALSE:** the quarantined schema-2 theta-2 stream omitted the fixed root
  from state identity and merged exact rooted presentations.
- Exact categories: 1,518 missing fixed-root fields; 276 cross-root merges;
  276 cross-target-rooted-graph merges; 2,106 coverage/root mismatches; 588
  coverage graph mismatches; and 72 independently regenerated child-set
  mismatches.
- This is the concrete failure that motivated schema 3.  It is not repaired
  in place and remains under `quarantine/schema2_rooted_merge_failure/`.

## 2026-08-10 — corrected schema-3 n=4 theta-2 base stream

- **VERIFIED:** 132 fixed roots, 2,106 path states, and all per-path child
  sets agree with independent regeneration.
- **VERIFIED:** 1,860 nonisomorphic terminals have exact target-zero,
  source-nonzero polynomial pullbacks; 132 terminals are independently
  labelled-isomorphic; 114 states refine; no T or unresolved terminal occurs.
- Exact full-audit hash:
  `245321c8e17c6b27fc2c5230b4074459d106a3c37454c90e1ff84f902954a1a4`.
- An earlier clean-room pass incorrectly generated children for already
  terminal states and reported 822 false mismatches.  The bytes and correction
  are preserved under `history/implementation_failures/`.

## 2026-08-10 — actual schema-3 theta-2 p/q probe stream

- **VERIFIED:** all four summary commitments equal the decompressed JSONL
  streams exactly.
- **VERIFIED:** all 23,400 graphs independently satisfy the locked standard
  S_TC criterion and carry the independently recovered active-blob arc set.
- **VERIFIED:** all 168,582 states have exactly one path binding; all 12,906 p
  children cover the Cartesian arc products of 132 base paths; all 155,676 q
  children cover the Cartesian arc products of exactly 1,302 allowed
  isomorphic p paths.
- **VERIFIED:** all 15,510 topology terminals are labelled-isomorphic with
  semantically exact canonicalization, vertex, edge, reticulation, and port
  transports.  Every separated state is neither isomorphic nor T-related.
- **VERIFIED:** independent displayed-tree and descendant-mask regeneration
  gives exact target-zero/source-nonzero pullbacks for all 153,072 separated
  states.  The clean-room quadratic family closes 150,468; its independent
  degree-three family closes 2,604.  No strict-sign flag and no primary
  polynomial body is used for acceptance.
- **VERIFIED:** ten actual-stream mutations are rejected, including a valid
  polynomial moved to the wrong relation.
- **EXACTLY COMPUTED:** all 132 accepted base terminals have zero triangles on
  both sides.  The probe package therefore does not close T-edge subdivision
  coherence.
- Structural, algebra, and mutation hashes are respectively
  `e586e17213a37d075cca714d597b0d03a9fa0aa5fb8ed91a5567da3095c8425c`,
  `d954013945e74c99dc28c2ab55541531cf491e413473ada8931c45e74758f3a8`,
  and `93ed47297ec22b3ac8c50921c05ef6bfdc1f125992e1ca0508970d857bed4e18`.
- Three reviewer implementation failures—gzip hash semantics, exact versus
  isomorphic rooted presentations, and split-complement descriptor
  normalization—are preserved and explicitly labelled as reviewer errors.
- **ADVERSARIAL CROSS-CHECK:** after completion, the independent implementation
  in `reviews/final_hard_cover_adversary/` was compared post hoc.  It agrees on
  all graph/state/binding/class totals, the 110 + 776 gap, and the
  triangle-free-terminal limitation.  It was not used by this implementation.

## 2026-08-10 — current release boundary

- **UNRESOLVED:** no merged corrected schema-3 n=3 stream is present.
- **UNRESOLVED:** the reported 110 n=3 and 776 n=4 unequal-but-necessary
  directions are outside the equal-signature theta-2 streams audited above.
- **UNRESOLVED:** complete primitive-root exhaustiveness and the remaining
  cycle/cross-core directed relations are not certified by this subgate.
- **UNRESOLVED:** coherence of probes on an edge changed by ordinary T has no
  triangle-bearing accepted base in this stream.
- Therefore the n=4 theta-2 stream is promoted to **VERIFIED**, while the
  landmark global identifiability/containment theorem remains fail-closed.

## 2026-08-10 — scoped release finalized

- Added `MANIFEST.sha256` and a single `verify_all.sh` entry point that checks
  the frozen review artifacts before and after replay.
- **VERIFIED:** both release modes pass.  The final full replay independently
  regenerated the 2,106-state base cover, all 168,582 probe structures and
  exact terminal pullbacks, both actual-stream mutation suites, the clean-room
  universe, and the conditional p/q and generic mutation certificates; its
  closing manifest check also passed.
- **UNRESOLVED:** this release intentionally makes no promotion of n=3 or of
  the global theorem.  Those require a fresh, explicit gate.

## 2026-08-10 — release withdrawn before commit; audit paused

- **SUPERSEDED:** before commit, the primary producer disclosed that the n=4
  descriptor cache had not been keyed by exact rooted graph provenance.  The
  old base and 168,582-state p/q replay were moved intact to
  `history/superseded_pre_exact_rooted_descriptor_cache/`.
- **SUPERSEDED:** the first exact-rooted-graph regeneration had summary
  SHA-256
  `fd3b7a6a180a5569bf6d1f3056d8c31756d4b14eec8bf19805f37706748e9342`.
  A clean-room audit was started and then terminated before certificate
  output when a second issue was reported: admissible rootings can produce
  quartet masks differing by split complement.
- **REQUIRED CORRECTION:** active descriptors must canonicalize each zero-sum
  quartet split as `min(S,S^c)`, thereby zipping root-edge factors and
  restoring root-location invariance.
- **UNRESOLVED:** no active n=4 base or p/q verdict remains.  `verify_all.sh`
  now fails closed pending the final regenerated summary SHA.  No commit or
  primary edit was made by this review.

## 2026-08-10 — corrected schema-3 n=4 base gate independently closed

- Locked the final active summary at physical SHA-256
  `915bed0a3add001c1a94d6d862a2359e6ad75b3489f8d71b7adf006952b5ce37`.
- **VERIFIED:** independently regenerated complement-normalized descriptors
  from all 606 exact rooted graphs.  The active rule has zero failures across
  66 multi-root mixed-graph groups; removing it or complementing in the wrong
  universe breaks all 66.
- **VERIFIED:** all 2,106 stronger-identity states and all raw path bindings,
  including 114 complete child-set restorations.  There are zero normalized
  collisions and zero merged-provenance child disagreements.
- **VERIFIED:** 132 labelled-isomorphism terminals and 1,860 exact polynomial
  separations.  Every separation is rederived on its graph-bound primary
  quartet; 1,828 use the independent finite family and 32 use exact
  degree-five target-nullspace relations.  No fallback quartet is used.
- **VERIFIED:** all 19 primary polynomial records are referenced and
  conflict-free as stream bindings.  Primary flags are not used for the
  mathematical acceptance decision.
- **VERIFIED:** all 13 relation, provenance, polynomial, path, and
  split-complement mutations are rejected.
- Frozen full-audit and mutation commitments are respectively
  `5cea78208f1ccbce93b22fb7f5c71e73999a9abea51e23d7182b9cfa4f1be1c6`
  and
  `c5cceff673c84ff0f654438adc0ef9aead969101549a4daa645a26911d0ad2e6`.
- **UNRESOLVED:** p/q probe closure remains historical because its base-input
  hashes predate the corrected descriptor cache and split normalization.
- A post-hoc older adversary implementation was stopped to avoid consuming
  resources while it recomputed a stale invariant census.  It produced no
  verdict and is not evidence for or against this gate.

## 2026-08-10 — n=3 path gate verified; terminal attempt withdrawn

- **VERIFIED:** the independent graph/path replay completed over 5,344 roots,
  68,584 states, 14,482 exact rooted graphs, and 8,349 refinement states.
  It found zero failures, zero normalized-state collisions, and zero
  merged-provenance child-set disagreements.  Its commitment is
  `d9dfc6d5e6e300bff00bd940adbf55395f609031aba8adeae0f38494dacadee6`.
- **WITHDRAWN:** an attempted terminal routine emitted a zero-failure result,
  but an independent adversarial reviewer identified incompatibility with
  required two-active-label cases.  The process was stopped/confirmed absent,
  no heavy rerun was attempted, and all terminal outputs were moved to
  `history/withdrawn_n3_terminal_two_active_labels/`.
- **UNRESOLVED:** n=3 terminal algebra, topology/T terminals, and the complete
  n=3 hard-cover gate.  No global theorem is promoted from this subreview.
- Machine memory was released; no clean-room audit process remained active at
  the stop checkpoint.
