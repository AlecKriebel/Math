# Bounded directed-relation clean-room review log

This directory is an independent, fail-closed audit of the bounded `n3` and
`n4` directed-relation certificates.  It does not import or inspect the
primary relation compiler, merger, canonicalizer, separator-selection code,
or crosswalk code.

## 2026-08-10T06:00:00-07:00 — scope lock and input inventory

Status: **IN PROGRESS**.  Best estimate: 18% complete.

Permitted evidence was restricted to primitive graph encodings,
`support_universe.json`, inert invariant templates, final relation
streams/summaries, and verified hard-cover streams.  Existing primary and
other-review processes were left running; no competing memory-heavy replay
was started.

The available relation material was not yet a complete active n3/n4 release:

- an unfiltered n3 cycle-source stream was present;
- a filtered n3 cycle-source stream was still being generated;
- no complete n4 directed-relation summary was present;
- verified n3 full and n4 theta-2 hard-cover streams were present.

The reviewer is therefore being built fail-closed: absence of a declared,
complete source-core partition or a final merged summary cannot yield PASS.

## 2026-08-10T06:15:00-07:00 — first independent binding check

Status: **EXACTLY COMPUTED (candidate; to be replayed by the committed
verifier)**.  Best estimate: 24% complete.

Using only the unfiltered n3 relation stream and the verified n3 fixed-full
hard-cover root-case stream, the key

```
(source primitive id, source position map, source provenance,
 target primitive id, target position map, target provenance)
```

matched all 5,136 pending raw cycle-source presentations to all 5,136
cycle-source fixed-full roots bijectively.  Every key had multiplicity one on
both sides.  This is not yet a release verdict because the active filtered and
merged directed-relation products were still absent.

## Independence rules

- No project Python module may be imported.
- No prohibited primary/reviewer source may be opened or copied.
- Graph validation, switchings, descendant masks, Fourier tensors,
  invariant pullbacks, graph isomorphism/T tests, coverage keys, and mutation
  checks are implemented here with the Python standard library.
- Any unavailable, partial, internally inconsistent, or undeclared input is a
  hard failure, never an implicit skip.

## 2026-08-10T06:23:00-07:00 — first full n3 replay; mutation design failed closed

Status: **VERIFIED MATHEMATICAL REPLAY / FAILED MUTATION HARNESS**.  Best
estimate: 63% complete.

The complete n3 replay independently obtained all advertised counts and passed
the graph, tensor, signature, strict-sign, iso/T, source-partition, shard-union,
and 5,344-to-5,344 hard-cover binding checks.  In particular, all 5,284 strict
relations were regenerated from their bound graphs and all 800 stored strict
polynomials received independent exact Bernstein certificates.

The overall run nevertheless returned `FAILED`: the first valid-port-map
mutation used the fixed transposition `(0 1)` on a separator invariant under
that symmetry, so the altered witness remained mathematically valid.  This is
a defect in the adversarial fixture, not evidence for or against the atlas.
The exact failed design is preserved in
`certificates/preserved_mutation_design_failure.json`.  The repair searches
deterministically for a relation/permutation that changes the graph-derived
pullback before treating rejection as a mutation certificate.

## 2026-08-10T06:39:00-07:00 — corrected n3 replay and second mutation-design defect

Status: **n3 VERIFIED / n4 AWAITING COMPLETE INPUTS**.  Best estimate: 66%
complete for the combined gate.

The corrected port-map mutation was rejected by the independently regenerated
graph pullback.  A second preliminary mutation design also failed closed: it
selected the first different stored polynomial having the same invariant,
quartet chunk, and strict sign, but that polynomial represented the same
effective positive-product polynomial after exact variable-column
identification.  This is a legitimate algebraic coincidence, so it was not a
valid wrong-graph fixture.  The preserved defect is recorded in
`certificates/preserved_wrong_polynomial_mutation_design_failure.json`.

The repaired test searches deterministically for two same-invariant/chunk/sign
witnesses whose graph-derived effective pullbacks differ, assigns one to the
other relation, and requires rejection specifically at the graph-to-polynomial
binding.  It selected relations `013ba54...` and `105e8dc...` and rejected the
mutation as required.  Neither mutation-design failure is theorem evidence.

The substantive n3 audit remains clean: 10,466 canonical relations, 5,284
strict graph-derived separators, 5,344 pending raw coverages bijective with all
5,344 fixed-full roots, and 62 independently checked isomorphism/ordinary-T
relations.  The n4 source-core generation remains active, so no memory-heavy
n4 replay was started.

## 2026-08-10T07:02:00-07:00 — third mutation fixture failed closed

Status: **REVIEW HARNESS CORRECTED; MATHEMATICAL STATUS UNCHANGED**.

An attempted strengthening of the “collapse distinct source embeddings with
the same target” mutation required two *pending* canonical n3 relations with a
shared target and different source graphs.  The final n3 stream contains no
such pair, so the harness correctly stopped instead of pretending to test the
case.  This over-restrictive fixture design is preserved in
`certificates/preserved_cross_relation_collapse_mutation_design_failure.json`.

The repaired mutation uses two strict canonical relations with the same target
completion and different sources, merges their raw coverages into one record,
recomputes the binding hash, and is rejected by the independent decorated
graph binding because the imported raw source graph does not equal the
canonical source graph.  The original within-relation multi-embedding collapse
mutation remains separate and is rejected by the 5,344-root crosswalk.

## 2026-08-10T07:16:00-07:00 — strengthened n3 full replay passed

Status: **n3 VERIFIED / n4 AWAITING COMPLETE INPUTS**.  Best estimate: 72%
complete for the combined gate.

The final strengthened n3 replay returned `VERIFIED` with no failures.  Beyond
the earlier checks it independently certified all 7,726 bounded graphs as
binary, strongly tree-child, level at most two, parallel-artifact free after
standard reduction, and containing at most one triangle.  It assigned 7,734
graph/port uses to 124 exact zero-sum effective descriptor decks, recomputed
all 124 signatures, and cross-checked 12 through the separate tuple-polynomial
engine.

All 5,344 pending raw relations were rebound using independent provenance
hashes rather than primary primitive IDs.  The upstream hard-cover scope was
also pinned and replayed structurally: 5,344 roots, 68,584 restored relations,
14,482 graphs, 225 polynomials, every root terminal, and zero unresolved.
All 13 applicable actual-artifact mutations were rejected.  The complete
certificate is `certificates/n3_full_replay.json`.

## 2026-08-10T07:20:00-07:00 — interim reviewer invocation aborted safely

Status: **NO ADVERSARIAL VERDICT RECORDED; n3 CERTIFICATE UNAFFECTED**.

The first local reviewer invocation failed before startup because the installed
CLI did not recognize the configured `ultra` reasoning value.  A second
read-only invocation started, but attempted to launch `verify_all.sh` and
`verify_n3.sh` concurrently.  It was interrupted immediately to preserve the
sequential memory rule; process inspection confirmed no verifier child
remained, and no report was written.  Both operational failures are preserved
in `certificates/preserved_adversarial_reviewer_invocation_failure.json` and
are not theorem evidence.  The final adversarial reviewer will be restricted
to static certificate/code inspection and short probes after n4 closes.
