# Corrected finite-universe release interface

This is the versioned interface between the regenerated four-port computation
and the final principal-`D_plus` theorem release.  It replaces every fixed
count derived from the revoked mixed-first tree--sunlet oracle.  In particular,
the number of restoration parents is an output of the corrected class ledger;
it is not used to control enumeration.  The independently frozen restoration
v3 package now derives 997 parents and cross-binds that result to the class
ledger.

The byte-locked locator `corrected_finite_universe_locator.json` has schema
`k2p-corrected-finite-universe-locator-v1` and is now `FROZEN`. It lists every
artifact below by project-relative path and SHA-256 and binds the unified
certificate, independent replay, and mutation report. Any future locator with
status `BLOCKED` is provenance only and must fail theorem promotion. Paths are
data, not constants in the verifier. Its release contract is
`k2p-corrected-finite-universe-release-v2`.

## Frozen artifact roles

A frozen locator retains the already bound raw-four overlay roles as historical
provenance:

- `raw4_full_map_auditor` and `raw4_full_map_truth_certificate`;
- `corrected_overlay` and `corrected_overlay_builder`;
- `corrected_overlay_verifier` and `corrected_overlay_replay`;
- `corrected_overlay_mutation_runner` and
  `corrected_overlay_mutation_report`.

Those overlay roles are not the promotion ledger.  A frozen locator must add
the shared corrected-composite generator, support module, independent verifier,
and mutation runner; the raw-four terminal-registry builder and registry; and
the family-specific raw-four/theta2 ledgers, summaries, independent replay
reports, and mutation reports under the stable role names in
`required_frozen_roles`.  Shared executables have one locator role each and
are never duplicated under family aliases.  It must additionally add the
replacement restoration ledger/forest, corrected cycle ledger, corrected
probe package, and their primary verifier, independent verifier/replay, and
mutation artifacts.  Finally it adds the cross-family corrected-universe
certificate, verifier, replay report, and mutation report.  The outer lock
discovers every path from that signed table, so no restoration, cycle, probe,
child, edge, leaf, anchor, or survivor count is compiled into the harness.

The frozen restoration roles are
`restoration_v3_generator`, `restoration_v3_builder`,
`restoration_v3_forest_certificate`,
`restoration_v3_historical_crosswalk`,
`restoration_v3_independent_verifier`, `restoration_v3_replay`,
`restoration_v3_mutation_runner`, and
`restoration_v3_mutation_report`.  Historical classifier fields occur only in
the explicitly named crosswalk and never in the clean forest certificate.

Every located artifact is independently included in the outer byte lock.
No historical probe, cycle-truth, or combined tree/sunlet path is a fixed
release input; the signed locator is the sole path authority for their
corrected replacements.

The old `work/restoration_forest/five_port_certificate.json`, its replay, and
its depth-one `RESTORATION_CLOSURE.md` narrative remain byte-bound only because
the corrected producer may read them as historical provenance. They are
explicitly quarantined by `HISTORICAL_ARTIFACT_REGISTRY.json`, are absent from
the promotion locator, and cannot discharge any promotion gate. Their only
authoritative replacements are the located corrected-v3 forest and independent
replay, which bind 36,824 physical edges including all 256 second children.

## Composite-ledger serialization

Both authoritative primitive ledgers are byte-stable canonical gzip JSONL.
The gzip header has `mtime = 0`; every line is UTF-8 compact JSON with sorted
keys and separators `(",", ":")`; lines are LF-terminated; and rows occur in
strictly increasing `raw_id` order.  The raw-four IDs are exactly
`0,...,405215`; the theta2 IDs are exactly `0,...,2946239`.  Each summary binds
the compressed ledger SHA-256, generator SHA-256, uncompressed stream SHA-256,
ordered row-hash root, ordered raw-ID root, serialization record, and every
input artifact SHA-256.  Regeneration must reproduce the compressed bytes.

Every row contains its row schema, raw ID, source index and descriptor digest,
target index, permutation index, full physical port permutation, corrected
category, exact reason, and evidence binding.  The evidence binding points to
the exact quartet witness, full-map `T_i` class and coefficient data, matched
rank lower/upper certificate, direct separator/isomorphism certificate, or
restoration parent/descendant record required by that category.  Missing or
multiply assigned evidence is forbidden.

The authoritative rows contain no historical selection field and no rooted
tree/sunlet field or reason.  In particular the strings `tree_sunlet`,
`strict_tree_sunlet_sign`, `tree_sunlet_pointwise_excluded`, and
`tree_sunlet_REVOKED` occur zero times in either composite ledger.  They may
remain only in separately locked historical-provenance artifacts that are not
used as the promotion partition.

Each composite summary has status `PASS`, zero duplicate/missing raw IDs,
zero missing/multiple evidence bindings, zero unresolved records, zero
forbidden rooted fields/reasons, and exact per-category row totals.  Its
independent replay regenerates primitive encodings without importing the
composite rows and agrees on every row hash and the final compressed bytes.
Its mutation report has zero survivors and includes omission, duplicate ID,
wrong permutation, category reassignment, evidence reassignment, forbidden
rooted-field reintroduction, and optimized-Python mutations.  All runs occur
in independent temporary copies and leave the source tree unchanged.

## Primitive composite censuses

The corrected raw-four composite contains exactly 405,216 rows and exactly
this partition:

| Corrected category | Rows | Required evidence |
|---|---:|---|
| `displayed_quartet_exclusion` | 360,408 | exact displayed-quartet witness |
| `full_map_Ti_strict_sign` | 16,974 | source strict sign and target zero on the complete four-port maps |
| `exact_rank_exclusion` | 23,822 | matched exact lower and symbolic upper rank certificates |
| `direct_terminal_presentation` | 1,472 | exact terminal-class ID and direct terminal certificate |
| `restoration_member_presentation` | 2,540 | exact restoration-parent ID and physical transport |

The 1,472 terminal presentations canonicalize into exactly 934 terminal
classes with presentation-multiplicity histogram
`{1:680, 2:150, 4:71, 5:14, 6:7, 8:12}`.  The 2,540 restoration-member
presentations canonicalize into exactly 997 parent classes with histogram
`{1:424, 2:112, 4:449, 8:12}`.  Every presentation has exactly one class link;
the ordered class and membership hash roots bind all multiplicities.  The
generator must derive these censuses from canonicalization rather than using
934 or 997 to control enumeration, and the independent replay must reproduce
them.  The 997 parent identities equal the root identities of the corrected
forest.

The corrected theta2 composite contains exactly 2,946,240 five-port raw rows
and exactly this partition:

| Corrected category | Rows | Required evidence |
|---|---:|---|
| `displayed_quartet_exclusion` | 2,942,592 | exact displayed-quartet witness |
| `full_map_Ti_strict_sign` | 2,528 | source zero and target strict sign on the complete five-port maps |
| `exact_rank_exclusion` | 800 | matched exact lower and symbolic upper rank certificates |
| `direct_quadratic_separator` | 240 | exact quadratic pullback certificate |
| `labelled_isomorphism` | 80 | exact labelled semi-directed isomorphism |

Every dummy-bearing isomorphism row also binds its complete physical
restoration descendants.  Descendant IDs are distinct, every descendant has
exactly one parent, every continuing child has a complete next layer, and all
leaves are exact quartet separators or labelled isomorphisms.  The descendant,
edge, and leaf counts are derived from the bound child ledger rather than
compiled into the outer release contract.

## Frozen corrected-composite package

The authoritative producer package is now frozen.  The raw-four ledger has
file SHA-256
`c6cd9d6b5b09371565fd3e58ff9ab3cd7266b6231b153d43f9d1e886af8eae27`
and summary payload
`3a49bfeeb244cba84cf2e42e2acf296f112d1586c5e17f40e2d2872722c3c988`.
Its independent primitive replay checks all 405,216 rows, including exact
whole-map replay of the 16,974 corrected sign rows, and has payload
`dfed35eab33dcc9983b38c8cedb79ed90b12c8a5cf04b58d251637b3fb2f1191`.
Its 14/14 verifier-facing mutation report contains 12 complete-ledger attacks,
an optimized-mode guard, and an aggregate source-immutability guard; it has
payload
`eec4a56b20faa3239044db49796fa724d60a5412a8d6e89a92db5d81e9656385`.

The theta2 ledger has file SHA-256
`805fc7f5a3de9dad2c63a210208075cf19910cf811ffd08878f32782ce71b659`
and summary payload
`c89dd764f7c66831db7f6a092fedf666a20f3594ef03647de3e85b5fbf04d0e8`.
Its independent primitive replay checks all 2,946,240 rows, including exact
whole-map replay of the 2,528 corrected sign rows, and has payload
`7e4283fe726083927b14d483d55644e2892a311b0179aa70d4766576c66ab545`.
Its 12/12 verifier-facing mutation report contains 10 complete-ledger attacks,
an optimized-mode guard, and an aggregate source-immutability guard; it has
payload
`5663b87d3f09eaac5e89db69ac5a1cf6069b308abf9bc4242650d0897ded1ff7`.
The descendant ledger derives 56 restored roots, 864 children, and 832 leaves;
these values are checked but are not enumeration controls.

The separately generated raw-four terminal registry has file SHA-256
`0a1818655429d60660c1ed87f3fbe412701f386b081562b3a4caa54079069f1d`
and derives all 934 terminal classes: 839 exact quadratics, 36
direct polynomial terminals, 35 ordinary triangles, 20 labelled
isomorphisms, and four hard `F2`/`F3`/`F4` terminals.  The package uses one
shared generator, support module, independent verifier, and mutation runner,
with no family-specific aliases for those executables.  Its frozen release-
contract replay has payload
`b746fb7a17e8ca9252c53dff0ba5722c1a00c56dc930d0c8456022ea34f60b6f`.
That report binds the producer's release-interface snapshot; the outer
verifier independently validates the live located bytes and their current
contract rather than assuming that snapshot and the outer verifier are the
same file.

## Count-free downstream family contract

The corrected-universe certificate contains one record for each of `raw4`,
`theta2`, `restoration`, `cycle`, and `probe`.  The two primitive censuses above
are exact release invariants.  Restoration, cycle, and probe counts are read
from the located family ledgers and checked only by equalities:

- input count equals distinct input IDs, with zero duplicate and missing IDs;
- every input row has exactly one exact reason and one bound exact evidence
  record, with zero false topology-oracle or graph-terminal conflicts;
- output category counts sum to the input count;
- generated-child count equals the length and distinct-ID count of the child
  ledger, and every child has exactly one parent;
- class-parent count equals the canonical-root and covered-canonical-root
  counts, while the restoration-presentation count equals the physical
  member-root and covered-member-root counts;
- edge count equals the exact-transport replay count;
- leaf category counts sum to the leaf count;
- probe anchor/survivor counts equal their derived root and deck ledgers;
- every probe survivor has exactly one parent, and every restriction is
  replayed from one fixed full containment using only root movement or an
  internal core arc, with bound edge and transport hash roots;
- all unresolved, cyclic, incoherent, false-oracle, and rooted-reason counts
  are zero.

Thus an additional restoration layer is accepted automatically when it is
fully enumerated and bound; its size is never a release constant.  The same
rule applies if corrected cycle or probe enumeration changes any historical
census.

## Raw-four full-map correction provenance

The overlay with schema `k2p-raw4-corrected-terminal-overlay-v2` is an input to
the composite generator and a separately replayed provenance artifact.  It is
never itself treated as the corrected ledger.  The outer verifier checks that
it contains exactly the 16,974 historical selections in increasing raw-ID
order with no omission or duplication, and then requires those same IDs to
appear in the authoritative composite only as `full_map_Ti_strict_sign` rows.

Every overlay row has `corrected_category = exact_exclusion`,
`corrected_reason = full_map_Ti_strict_sign`, and
`historical_reason = tree_sunlet_REVOKED`.  The overlay binds strict source
sign, identically zero target pullback, eight polynomial relation classes, and
no graph-isomorphism or ordinary-triangle conflict on the original full maps.
Its row hashes, aggregate root, descriptors, port transports, Bernstein
coefficients, and full-map adversarial certificate are all replayed.

No rooted-triple tree/sunlet label is an admissible composite field,
classification, or certificate kind.
The earlier 16,702-rank/88-quadratic/184-restoration preliminary split is kept
only as superseded provenance and contributes no row to the frozen partition.

## Dynamic class and forest ledgers

The outer verifier derives the four-port restoration-parent census from the
exact retained-class ledger, requiring distinct parent IDs and the
`restoration_parent` status.  The raw-four overlay adds zero parents.  The
derived 997 canonical parents expand to 2,540 physical member-root
presentations according to the exact multiplicity ledger.  A replacement
forest binds both layers separately: canonical-parent membership edges are
not confused with physical restoration edges from a member presentation to a
generated child.

The historical forest is revoked.  At least one claimed sign leaf,
`s0:c407:t2794:p1230` (incoming role, insertion 3, triple `(1,2,4)`), has all
three direct `T_i` pullbacks zero on both full five-port maps although its exact
graph relation is `none`.  A frozen replacement must repartition every row in
the located historical-selection ledger without using a rooted restriction,
discharge every resulting algebraic/restoration obligation, and bind the class
ledger.  It must report zero missing parents, missing children, unresolved
records, cycles, and incoherent transports.  Every edge must have a replayed
exact transport restriction.  Its leaves may be only exact separators,
labelled isomorphisms, or ordinary-triangle relations.

That replacement is now the frozen clean forest with schema
`k2p-corrected-restoration-forest-v3`.  It derives 997 canonical parents and
2,540 physical member roots, enumerates 36,568 first children, continues
exactly 32 of them, and enumerates all 256 second children.  The resulting
36,824-edge depth-two forest has 36,792 terminal leaves, zero missing children,
zero cycles, and zero unresolved rows.  Its terminal proof census is 36,006
displayed-quartet mismatches, 614 full-map `T_i` zero/strict-sign identities,
148 exact multihomogeneous quadratics, and 24 transported exact
`F_(2,112)` quartics.  Every terminal is therefore an exact separator.

The unified producer uses these deterministic identifiers and roots:

- a member-root ID is the `root_id` at its first occurrence in the ordered
  first-child ledger;
- `sS:cC:tT:pP` maps to canonical parent
  `source_S:class_CCCCCC`, with `C` zero-padded to six digits;
- the generated-child ID ledger is the ordered concatenation of the 36,568
  first-row hashes and 256 second-row hashes;
- a depth-one edge is `(member root ID, first-row hash)` and a depth-two edge
  is `(parent first-row hash, second-row hash)`;
- a depth-one transport binds its source and target parent-transport IDs,
  while a depth-two transport binds its source and target parent mixed-graph
  hashes.

Every record above is compact canonical JSON, individually SHA-256 hashed, and
the ordered list of record hashes is compact-canonical-JSON hashed again.  The
release verifier independently derives the canonical-parent, member-root,
class-membership, child, edge, transport, and leaf roots.  Raw-composite
presentation membership remains a separate root and is not conflated with the
physical class-to-member edge root.  The clean forest also reconciles the 54
dummy-bearing direct terminal presentations in 35 classes (including raw IDs
67161, 67167, 67401, and 67407); these do not intersect the restoration forest
and instead enter the probe-input package.

Every corrected restoration, cycle, and probe row carries an exact whole-map
reason or an exact graph terminal.  The strings `tree_sunlet` and
`strict_tree_sunlet_sign` are forbidden as proof reasons; they may occur only
inside an explicitly named historical-selection field ending in `_REVOKED`.

## Frozen corrected cycle package

The cycle promotion package authoritatively partitions 13,440 base records as
5,964 fixed-full restoration obligations, 7,452 full-map `T_i` strict-sign
separators, 8 labelled isomorphisms, and 16 ordinary triangle relations.  It
enumerates all 536,364 fixed-full children: 535,920 displayed-quartet
separators, 132 exact directional quadratics, 300 full-map `T_i` strict-sign
separators, and 12 labelled isomorphisms.  The independent whole-map replay
also checks all 24 repaired legacy witnesses, 92 sign-polynomial classes, and
12 bridge multihomogeneity invariants.  The promotion replay and 12-mutation
suite bind the clean row and transport roots with zero unresolved or rooted
rows.

## Frozen two-stage corrected probe

Probe-input v2 derives 176 physical equality anchors (143 isomorphisms and 33
ordinary triangle relations), 2,206 admissible sites on each side, 29,964
first-probe source--target pairs, and all 352 artificial-root-half
equivalences. The completed corrected probe then classifies all 29,964
one-port and 544,571 two-port rows, binds 2,107 second-stage parents and 32,729
reverse marginals, and replays 67,741 exact transports and 4,379 parent
restrictions. Its primary 15/15 mutation suite and independent primitive-graph
12/12 mutation suite both pass. Every restriction is certified as coming from
one fixed full containment using only root movement or an internal core arc;
all unresolved, incoherent, missing-parent, and new-triangle counts are zero.

## Independent replay and mutations

The raw-four independent report has schema
`k2p-raw4-corrected-independent-replay-v1`, status `PASS`, and replays all
16,974 rows directly from graph encodings and full Fourier maps.  The current
report binds overlay file SHA-256 `5003a861...`, payload `8898b79f...`, eight
sign classes, zero conflict/unresolved, and a class-ledger-derived parent
count.  The separate replacement-forest replay must cover raw generation,
terminal classification, child coverage, termination, and transport
coherence.

The raw-four mutation report has schema `k2p-raw4-corrected-mutations-v1`,
status `PASS`, and currently rejects 9/9 mutations: omitted/reassigned raw row,
wrong port transport, reassigned polynomial or descriptor certificate,
mutated Bernstein data, reversed sign, and optimized Python mode.  The
cross-layer suite additionally requires false-rank, missing-child,
wrong-parent, broken-transport, reassigned quadratic/cubic/quartic/quintic,
and `direct:raw4424` rooted-restriction reintroduction mutations. The unified
cross-family suite rejects all 22 required mutations, including the complete
corrected-forest and two-stage-probe cases, with zero survivors.

## Source-tree hygiene

All generators and mutation runners execute in temporary independent copies;
hard links are forbidden.  Before and after each dynamic package replay the
harness fingerprints the source certificate, verifier, manifest, and locked
inputs.  The fingerprint must be identical even when a mutation rejects or a
child process raises.  Temporary cleanup is guaranteed by `try/finally`.

This interface is restricted to the principal positive-eigenvalue domain.  It
makes no mixed-sign claim.
