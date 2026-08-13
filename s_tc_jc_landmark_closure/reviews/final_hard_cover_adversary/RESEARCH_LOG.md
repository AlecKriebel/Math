# Final hard-cover adversarial audit log

All timestamps use America/Los_Angeles.  This directory is an independent
review workspace.  No file under `primary/` was altered by this reviewer.

## 2026-08-10T01:20:00-07:00 — scope locked

- Began a clean-room audit of the n=3 hard-cover artifacts, fixed-root
  coverage, graph-to-polynomial association, strict signs, and arbitrary-port
  probe closure.
- Reimplemented rooted validation, standard semi-directed reduction, mixed
  graph canonicalization, displayed-tree descriptors, JC invariant pullbacks,
  and exact sign checking without importing a primary module.
- Locked the tree-child quantifier to internal vertices only.  Leaves are
  explicitly excluded and covered by a regression fixture.

## 2026-08-10T01:45:00-07:00 — independent coverage gaps

- **FALSE (artifact sufficiency):** n=3 alone cannot cover the theta-2 core,
  whose minimum rigid support has four outgoing ports.  Independently found
  132 theta-2 fixed n=4 root cases and no reduction to any n=3 source
  descriptor under all tested labelled one-port deletions.
- **FALSE (artifact sufficiency):** no graph-bound pair-level separator streams
  exist for the independently reconstructed 110 n=3 and 776 n=4 unequal
  necessary directed signature pairs.

## 2026-08-10T02:12:00-07:00 — schema-2 failure preserved

- The completed schema-2 theta-2 stream was quarantined by the primary team
  after a rooted-presentation merge was found.
- Stopped the obsolete clean-room job that would have accepted equal mixed
  codes as sufficient state identity.
- Independently replayed the quarantined bytes.  Exactly 276 of 1,518 states
  merge multiple fixed root cases and multiple exact target rooted graphs;
  1,452 raw rooted-binding mismatch events occur across 2,106 coverages.
- Marked the schema-2 stream **FALSE AS A FIXED-ROOT DECORATED-RELATION
  CERTIFICATE**.  The failure remains available as a regression fixture.

## 2026-08-10T02:23:00-07:00 — schema-3 acceptance rule

- Required state identity now contains the fixed-full root-case ID and exact
  rooted source/target graph IDs in addition to mixed codes, remaining roles,
  port count, and port matching.
- Updated the clean-room checker to reject every merge across a root case or
  rooted graph ID, even if the standard mixed graph codes agree.
- Updated child-set replay to regenerate each child ID from each exact rooted
  parent path using the same strengthened identity.
- Began independent full replay of the completed 132-root schema-3 theta-2
  n=4 stream.  Primary PASS output is not used as evidence.

## 2026-08-10T02:35:00-07:00 — adversarial regressions expanded

- Added explicit cross-root and equal-mixed-code/different-rooted-graph merge
  mutations.
- Added independent exact factor/Bernstein replay and a forged-`certified`
  mutation.  The n=4 theta-2 stream has no strict-sign rows, so historical
  n=3 strict rows are separately reconstructed as regression fixtures.
- Generalized the p/q probe audit to schema 3 and required exact root/graph
  identity before a topology terminal may seed a probe.

## 2026-08-10T02:46:00-07:00 — actual theta-2 probe package received

- Frozen the four streams named by
  `probe_extension_theta2_schema3_summary.json`: 168,582 states, 168,582
  path bindings, 23,400 graphs, and 29 polynomial bodies.
- The producer totals exactly match the earlier independent combinatorial
  census: 12,906 `A+p` relations and 155,676 conditional `A+p+q` relations.
  This agreement is not treated as an algebraic certificate.
- Added a full clean-room verifier for content addressing, all graph classes,
  exact deletion to parents, physical port maps, root/path coherence, rigid
  quotient transports, graph-derived JC pullbacks, and complete Cartesian
  p/q coverage.
- **VERIFIED (mutation sensitivity):** all 9 probe mutations were rejected:
  deletion, duplication, port-map change, source/target reversal, valid
  polynomial moved to the wrong graph, wrong transport, fabricated Jacobian
  field, wrong q parent, and a cross-root state merge.
- Jacobian verification is not applicable to this package: it makes no
  Jacobian or rank claim, and the state schema contains no such field.

## 2026-08-10T03:08:00-07:00 — theta-2 probe streams independently closed

- **VERIFIED:** all 23,400 graphs independently satisfy the locked rooted,
  LSA, internal-vertex tree-child, standard semi-directed, and level-2 class
  checks.  Every graph is triangle-free and has two reticulations.
- **VERIFIED:** all 168,582 state rows and all 168,582 path bindings are
  content-addressed, one-to-one, and tied to exactly one base root/path.  No
  state is multiply bound across roots or paths.
- **VERIFIED:** every inserted p or q port deletes exactly to its recorded
  parent; every insertion is on an independently recovered internal blob arc;
  all physical port labels, base roles, parent chains, and rigid quotient
  transports agree.
- **VERIFIED:** every generic separator was regenerated from its source and
  target graphs through displayed-tree JC descriptors.  The regenerated body
  agrees with the separately content-addressed polynomial library.
- **VERIFIED:** the exact expected and actual cover sets agree:
  12,906 `A+p` relations and 155,676 conditional `A+p+q` relations.
- This theta-2 package contains no triangle edge and therefore does not by
  itself certify insertion order on a redirected triangle edge.  That scope
  belongs to the full n=3 schema-3 package.
