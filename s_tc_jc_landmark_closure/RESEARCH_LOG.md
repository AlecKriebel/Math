# Research log

## 2026-08-09T20:15:00-07:00 — final-closure program opened

- Created a dedicated closure directory and branch from the verified
  weak-class release.
- Froze the sharpness theorem and its two independent verifiers.
- Rejected the withdrawn reciprocal-only bridge chart and every old atlas
  table lacking a primitive decorated graph-to-polynomial binding.
- Locked the only terminal outcomes as a fully certified positive sharp
  boundary or an exact certified `S_TC` counterexample.
- Began parallel work on corrected projective peeling, one-sided cut
  preservation, primitive generator enumeration, decorated-relation
  compilation, and adversarial counterexample search.

## 2026-08-09T20:27:23-07:00 — frozen weak theorem replayed

- Ran `../s_tc_jc_sharp_boundary/reproducibility/verify_release.py` from the
  verified release at parent commit `0c66eefc`.
- The release verifier checked the 288-file manifest, graph/class membership,
  six invariant identities, the exact quadratic interior point, all 256
  Fourier and pattern coordinates, and nonzero rank-eight minors for both
  parameterizations.
- The independent certificate SHA-256 reported by the release is
  `38266537a7966d83bdb94c6fb90fa68f93fbd227b82579f1bf311005925366d7`.
- The verifier entry point has SHA-256
  `90901ab2111c2aecf9eb27989f7136dd44f936cf2e6f9929772a8bba575fbba5`.
- This replay freezes only the theorem in `W_TC \\ S_TC`; it supplies no
  positive-classification input for `S_TC`.

## 2026-08-09T20:32:00-07:00 — independent gates dispatched

- Assigned the bridge/cut theorem to an implementation that may write only
  under `independent/bridge_cut/`.
- Assigned primitive decorated-atlas regeneration to a separate implementation
  that may write only under `independent/decorated_atlas/`.
- Assigned bounded exact counterexample search to a third implementation that
  may write only under `independent/counterexample_search/`.
- The primary implementation will not share graph canonicalization,
  switching, descendant-mask, relation-assignment, or separator-selection code
  with those implementations.

## 2026-08-09T20:45:00-07:00 — root atlas structurally reduced

- Wrote a candidate structural proof that a root-containing `S_TC` factor is
  represented by an ordinary incoming-port factor in the projective tensor
  quotient.
- The proof uses uniform-root JC reversibility, positive edge splitting, and
  the definition of `S_TC` over every admissible rooting.
- This route avoids the historically failed root weak-target promotion chain.
- Status remains candidate until a separate adversarial implementation checks
  all primitive root sites and retained-arrowhead cases.

## 2026-08-09T21:05:00-07:00 — primary generator/support layer rebuilt

- A new primary event-and-direction enumerator derived 24 normalized valid
  theta presentations, four theta classes, and the cycle core.
- The minimum repair multiset is exactly `1,1,2,2,2` across cycle/theta cores.
- A new completion compiler independently regenerated the exact
  `831/1983/4155/7909` weak-completion counts for three through six selected
  outgoing ports; every full completion is rooted binary and passes the
  standard-strong local criterion.
- A new rigid-support compiler generated 304 five-outgoing and 216
  six-outgoing decorated source presentations.  The extra 24 five-port rows
  are the support-plus-one marginals of the four-support core that the older
  direct five-port file omitted and later derived indirectly.
- Proved candidate marginal-submersion and probe-coherence lemmas.  These
  remain unpromoted pending the independent atlas and adversarial review.

## 2026-08-09T21:18:00-07:00 — ordinary T germ independently replayed

- Replayed both the historical primary triangle verifier and the independent
  JC-only release verifier in the clean environment.
- The independent output matched its frozen certificate byte-for-byte with
  SHA-256 `97097fa36e00edbf4837bbef3a255ccd756aac99136138746168ec94630df4dc`.
- Promoted only the JC common regular germ under ordinary `T`; no complete
  stochastic-image equality or richer-model statement is imported.

## 2026-08-09T21:25:00-07:00 — root reduction corrected before promotion

- Rejected the first candidate formulation because an artificial incoming
  character at a uniform root would not be observable.
- Replaced it by a real-boundary theorem: following tree/leaf children from
  an admissible tree-child root reaches an existing labelled boundary along
  an all-tree path; rerooting there reverses only ordinary arcs.
- JC reversibility then identifies the complete real boundary tensor, with
  only the corrected incidence-scaling gauge on the chosen arm.
- The correction removes the fictitious-port gap and is now the version sent
  to adversarial review.

## 2026-08-09T21:35:00-07:00 — primary atlas defect caught and quarantined

- Before promoting the new bounded-atlas counts, an internal adversarial check
  found that the deck contained every symmetry of quartets using the incoming
  boundary but omitted four-outgoing-port marginals.  The affected counts and
  incomplete relation stream are not evidence and will be regenerated.
- Replaced the deck by every ordered restriction of every four-port subset of
  the complete boundary tensor.
- Added the seventh independent quartet invariant as inert coefficients, with
  its historical file hash recorded.  Its historical indices run over the
  fourteen nontrivial JC coordinates; the primary tensor engine includes the
  trivial coordinate at index zero, so every index must be transported by
  `+1`.  Omitting this transport falsely made the orbit nonhomogeneous.
- After the explicit transport, the full 84-element invariant orbit is exactly
  multihomogeneous in all four port arms.  This is now checked by
  `primary/verify_multihomogeneity.py`.
- Began a new graph-bound cycle-to-theta union-support compiler.  It retains
  the source graph, target graph, port relation, restored support roles, exact
  pullback, and strict sign witness for every completed directed relation.

## 2026-08-09T21:45:00-07:00 — first independent bridge/cut and falsification gates closed

- The clean-room bridge/cut implementation proved the complete positive
  incidence-scaling fiber, analytic slices on the reduced leaf-supported
  bridge tree, source-relative localization, and the pointwise rank-four cut
  characterization.  It regenerated 72 four-port endpoint tensors and 204
  strict wrong-split minors with no failures.
- Its final adversarial replay caught one omitted ordinary trivalent
  three-port endpoint.  The corrected endpoint universe has 76 nontrivial
  tensors plus the ordinary tensor.  The universal `F=0` implication is
  `a>=bc`, not strict `a>bc`; the two-active contradiction remains strict
  because the joining multiplier satisfies `0<z<1`.  The report and mutation
  suite were corrected before promotion.
- A separate clean-room census exhaustively generated 2,821 standard `S_TC`
  topologies through five leaves (1,667 ordinary-`T` classes), independently
  replayed the frozen weak pair, and found no exact strong non-`T`
  counterexample.  Its four-/five-leaf fitting results remain labelled only
  `NUMERICALLY OBSERVED`.
- The same reviewer independently proved that every standard weakly
  tree-child level-2 blob has at most one triangle and exactly separated the
  three-leaf tree from the 3-sunlet over the entire open JC cube.
- Dispatched new adversarial reviews of (i) root reduction/support/submersion/
  probe coherence and (ii) the bridge/cut/global-localization synthesis.

## 2026-08-09T21:48:00-07:00 — selected-core-retention binding defect preserved and corrected

- Rejected the first corrected-atlas strength flag `not dummy_labels`.  A
  selected restriction can already occupy one minimum strong repair while a
  different chosen completion inserts an irrelevant dummy on another repair.
  Thus dummy presence belongs to the completion witness, not to the selected
  topology.
- Replaced the flag by the core-retention criterion: every path-sink
  reticulation port is selected and the occupied ordinary segments contain at
  least one minimum repair.  The independent decorated-atlas agent separately
  derived the same criterion and is running a direct admissible-rooting review.
- The first rerun correctly failed because topology canonicalization still
  used the full dummy-bearing completion graph.  This failure was preserved;
  algebra had marginalized the dummy leaves while topology had not.
- Split every target record into a tensor-realization graph and, when the
  selected ports retain the primitive core strongly, an intrinsic selected
  topology graph.
  The latter is rebuilt from selected words before canonicalization and has
  no dummy labels.  A fresh three-outgoing replay then returned zero strong
  non-`T` equal-signature failures.
- Refactored the directed relation certificate so every source/target
  presentation is bound to graph-derived descriptors.  Core-retaining
  equal-signature targets must be isomorphic or `T`; nonretaining
  equal-signature targets are retained explicitly for the support-completion
  gate rather than promoted.
- A second independent reviewer exhibited the necessary semantic caveat:
  omitting a cycle sink and applying a broader marginal reduction can yield a
  smaller strong tree.  Therefore the criterion is not intrinsic `S_TC`
  membership after `red_*`; it certifies retention of the original primitive
  core.  The atlas logic uses only this latter property.

## 2026-08-09T21:56:00-07:00 — global bridge/localization gate adversarially closed

- The second clean-room bridge reviewer independently replayed the complete
  incidence kernel, stabilizers, analytic slices, all 77 endpoint cases, 204
  strict one-active minors, the two-active crossing identities, and all
  package mutations.
- It verified both cut-set inclusions under source-relative containment, hence
  equality of labelled bridge trees; verified projective localization without
  a continuous target-parameter selector; and verified that distant blobs
  cannot compensate after intrinsic extraction.
- It rejected one overstatement: a finite union of target role/completion
  images need not contain the *entire* focal source germ in one member.  Exact
  semialgebraic dimension guarantees a member containing a nonempty
  full-dimensional source-open subgerm, which is precisely sufficient for
  local `preceq_JC`.  The active global proof now uses only this corrected
  statement.
- It also verified simultaneous gluing of compatible local `T` germs using a
  sufficiently small nonempty effective-scale interval on each bridge.  No
  arbitrary-scale or physical-bridge-identifiability claim survives.

## 2026-08-09T22:24:00-07:00 — three-outgoing nonretaining completion discharged

- The corrected bounded census contains selected three-outgoing
  cycle-to-theta deck equalities whose target completion uses omitted real
  sink/repair roles.  These are not complete equal-boundary factor
  comparisons.
- Once the independently verified cut theorem fixes the same labelled bridge
  tree, a complete three-outgoing source factor and target factor have the
  same three real boundaries.  A full standard-strong target with no omitted
  sink/repair boundary is core-retaining, so the dummy completion cannot be
  used.  If the source has another boundary, its cycle support-plus-two
  restriction is the four-outgoing gate handled by the completion compiler.
- The local and global proof ledgers now record this degree argument
  explicitly; no three-outgoing dummy equality is promoted.

## 2026-08-09T22:28:00-07:00 — root/probe adversarial corrections integrated

- The clean-room reviewer verified root reduction, the one-cycle/four-theta
  primitive universe, automatic triangle exclusion, core-retaining support
  rigidity, the physical-to-descriptor parameter-cube submersion, completion
  coverage, and support-plus-one/two word reconstruction.
- It caught three proof overstatements.  Setwise support automorphisms can
  duplicate anchored representatives; selected core collapse can make
  descriptor inheritance coordinates tensor-redundant; and a probe that
  subdivides a support-triangle edge destroys that triangle rather than
  carrying the same `T` ambiguity.
- The active proof now uses only surjectivity of the anchored quotient, only
  the physical-to-descriptor source submersion, and a two-case coherence
  argument: a triangle-destroying probe fixes literal orientation, while
  otherwise one unique triangle persists globally.
- The root proof now explicitly suppresses the old root, preserves its
  possible reticulation arrowhead, and proves the rerooted presentation is
  again LSA-valid by finding labelled leaves on both sides of the new root.

## 2026-08-09T22:52:00-07:00 — fixed-incoming local quotient rejected

- Quarantined every bounded-atlas result that fixed the rooted incoming
  boundary on both sides.  The incoming role is presentation provenance, not
  a colour of the standard semi-directed factor.  After simultaneously
  anchoring the source, the relative target action is the full symmetric
  group on all real boundaries, not the subgroup fixing the incoming role.
- Two clean-room reviewers independently found a four-boundary TT-nested
  witness: the source rootable physical boundaries are `{A,B}`, the target
  rootable boundaries are `{C,D}`, and the physical port matching is fixed.
  Thus the two factors have no common admissible incoming boundary.  The
  relative permutation is `(2,3,0,1)`, outside the incoming-fixed subgroup.
- **WITHDRAWN by the independent review recorded below.** A purported
  four-boundary ordinary-`T` example was extracted from
  the primitive records.  Its source hash is
  `25e272478915938e49b980ad172aa4f590f44fba8d0c50aaecf826fef7f46623`,
  its target rooted-presentation hash is
  `2e3b531105573999bd129e4cfa105136cf074cf2924481e9d5f9aba13ae1932f`,
  and the full port map is `{0:2,1:3,2:0,3:1}`.  The source admits only
  physical boundary `0`, while the target admits only `1` or `2`, so no
  incoming-to-incoming representative exists.  This last assertion is false:
  both presentations admit physical boundary `1`.
- The primary compiler has been repaired to anchor all source boundaries and
  enumerate all target boundary permutations.  This repair is not promoted:
  the complete graph-bound relation streams and a clean-room normalized
  comparison must be regenerated under the larger universe.
- The root/probe reviewer modified the primary compiler while investigating
  this issue despite its declared read-only scope.  That independence breach
  is preserved.  Its graph-theoretic counterexample remains independently
  replayable, but the modified primary bytes are treated only as discovery
  code until the separate incoming-boundary reviewer agrees.

## 2026-08-09T22:56:29-07:00 — marginalized target incoming role added

- Full boundary permutations still do not cover a target rooted presentation
  whose incoming boundary lies outside the selected source support.  Added a
  second target-completion role in which that incoming leaf remains in the
  full standard-strong graph but carries character zero.
- The primary generator independently produced `1,983`, `4,155`, `7,909`,
  and `13,983` such full completions for four through seven selected tensor
  ports.  Every rooted graph and narrow standard reduction passes the exact
  strong criterion.
- Pilot four- and five-port runs introduce no new invariant-deck signature
  and no core-retaining non-`T` equality, but every source common signature
  now also has at least one non-core-retaining presentation.  Those equal
  presentations are not dismissed: restoring their omitted incoming/support
  roles is a new mandatory branch of the graph-bound hard cover.
- The clean-room relation reviewer was interrupted and redirected to generate
  this role independently.  No fixed-incoming or selected-incoming-only count
  remains a theorem input.

## 2026-08-10T00:02:00-07:00 — incoming-boundary counterexample corrected

- The dedicated incoming-boundary reviewer independently verified the
  TT-nested four-boundary example with disjoint admissible incoming sets.  It
  therefore confirms that the fixed-`INCOMING` quotient is false and that the
  target action must be the full boundary symmetric group.
- The same reviewer refuted the separate purported ordinary-`T` witness
  recorded at `2026-08-09T22:52:00-07:00`: both presentations admit physical
  incoming boundary `1`.  An exhaustive check of the stored four-boundary
  primitives found no replacement ordinary-`T` pair with disjoint incoming
  sets.  That illustrative witness is withdrawn; it is not needed for the
  fixed-`INCOMING` refutation.
- The reviewer independently confirmed that a target structural incoming
  boundary may lie outside the selected source support and must then be
  represented as a zero-character dummy.  Its finite algebraic replay was
  interrupted and is not used as a theorem certificate.

## 2026-08-10T00:28:00-07:00 — primary full-boundary hard cover closes

- Rebuilt the bounded local comparison with all source-anchored target
  boundary permutations and both selected and marginalized target incoming
  roles.  Every non-core-retaining equal selected tensor was followed through
  sequential restoration of all omitted `D_REPAIR`, `D_SINK`, and `INCOMING`
  roles, always bound to one fixed full source-target relation.
- The exact primary census contains `5,344` fixed root cases and `40,072`
  canonical restored relations.  It classifies them as `32,394` generic
  polynomial separations, `1,538` strict open-cube separations, `6,051`
  intermediate restoration states, `73` labelled-isomorphic rigid supports,
  and `16` ordinary-`T` rigid supports.  There are no unresolved terminals and
  no non-`T` survivor.
- The fixed-full precondition is essential.  The adversarial design review
  supplied an exact counterexample to lifting containment from a selected
  marginal alone.  The active proof descends every restored prefix directly
  from the same assumed full containment and never uses that false lift.
- Upgraded the producer to emit content-addressed rooted graphs, complete
  standard reductions, raw-to-canonical transports, exact polynomial bodies,
  root-case entry records, restoration-parent bindings, and graph-derived
  witness references.  A primary structural replay passes on a smoke shard.
- Status remains candidate: a combined final-schema regeneration, an
  independently written producer comparison, mutation tests, and the global
  proof-logic audit are active.  No positive theorem is promoted from the
  primary census alone.

## 2026-08-10T01:39:00-07:00 — four-outgoing minimum-support gap found

- The adversarial theorem-logic pass forced a recheck of the source-support
  sizes.  The support certificate has nine minimum presentations: the cycle
  has outgoing support size two; theta cores `0`, `1`, and `3` have size
  three; and `theta-2` has size four.  The running hard cover begins only with
  three outgoing boundaries and therefore does not, by itself, quantify over
  the `theta-2` minimum support.
- The earlier informal statement that the eight three-outgoing source
  signatures were all minimum supports was false.  It is withdrawn before
  theorem promotion.
- The completed three-outgoing computation remains valid as a scoped gate.
  The global theorem now additionally requires either a rigorous reduction
  of every four-outgoing `theta-2` fixed-full relation to that gate or a
  separate graph-bound restoration cover beginning at five tensor ports.
  The clean-room producer, artifact adversary, and theorem referee were all
  redirected to attack this exact issue.

## 2026-08-10T01:47:00-07:00 — unequal directed-pair certificate gap isolated

- The primary restoration compiler intentionally starts from common equal
  invariant signatures.  Rechecking the bounded compiler showed that the
  current three- and four-outgoing summaries also contain `110` and `776`
  unequal but zero-set-compatible directed signature pairs.
- The source contains a pair-level relation compiler intended to certify
  these by regenerated strict target signs, but no
  `bounded_relations_n*.jsonl.gz` or associated sign-library artifact exists
  in the active tree.  Summary counts therefore cannot be used in their
  place.
- Final local closure now explicitly has three algebraic pieces: graph-bound
  certificates for every unequal necessary direction; fixed-full restoration
  of every equal non-core-retaining direction from each minimum support size;
  and the core-retaining one-/two-port probe atlas.  All three require an
  independent normalized replay.

## 2026-08-10T02:08:00-07:00 — promotion logic accepted; theta-2 inventory regenerated

- The independent theorem-logic referee completed its adversarial pass.  It
  found no additional global obstruction: corrected incidence-projective
  peeling, both pointwise cut inclusions, localization without a continuous
  target selector, simultaneous `T` gluing, and the proper-exceptional-locus
  argument promote the desired theorem once the fixed-full local closure
  contract is independently certified.
- The referee accepted the efficient arbitrary-word implementation: extend
  every raw path-bound common anchor `A=Q_s union Q_t` by one physical port
  `p`, then by `q`, on every internal blob arc on both sides.  Each child must
  delete to its exact parent and retain the same restoration root, target
  support, and anchor transport.  This gives the safe twelve-tensor-port
  bound without factorial full-boundary enumeration at outgoing sizes five
  and six.
- Added an explicit source-stratum filter to the primary compiler and
  regenerated the mandatory theta-2 inventory.  Exactly three filtered
  source signatures produce 132 fixed full restoration roots.  This is an
  exact inventory only; the corresponding hard cover and independent replay
  remain pending.

## 2026-08-10T02:18:00-07:00 — path-bound probe algebra compiler added

- Added a primary `A+p`, `A+p+q` compiler following the referee-accepted
  contract.  It reads only allowed raw hard-cover terminal paths, inserts the
  new physical label on every nonbridge internal blob arc on both sides,
  verifies exact deletion to the parent, regenerates every quartet descriptor
  and invariant pullback, and permits a child only when its unique labelled
  isomorphism/ordinary-`T` transport restricts to the parent anchor map.
- Canonical child algebra, raw path bindings, rooted graph bodies, exact
  polynomial bodies, and all transports are emitted in separate
  content-addressed streams.  The code is syntax-checked and its
  insertion/deletion and identity-transport primitives pass exact unit
  replays.  It has not yet run on the complete final-schema n=3+n=4 base
  streams and is therefore not a theorem certificate.
- Hardened the unequal-directed-pair compiler to emit complete rooted graph
  and exact polynomial libraries, rather than only topology and polynomial
  hashes.  Its full n=3/n=4 runs and independent replay remain pending.

## 2026-08-10T02:25:00-07:00 — schema-2 rooted-provenance merge rejected

- The filtered theta-2 primary run terminated with 132 fixed roots, 1,518
  canonical states, zero unresolved terminals, and only 66 apparent labelled
  isomorphisms surviving.  This numerical closure is **not promoted**.
- The exact primary replay immediately failed because one canonical state
  contained raw coverage with a different target rooted graph ID from the
  graph used to derive the state's algebra.  The state key had included only
  semi-directed mixed codes and remaining roles, so distinct rooted
  presentations could merge even though their continuation trees and
  variable transports had not been proved identical.
- Preserved the complete failed n=4 stream under
  `quarantine/schema2_rooted_merge_failure/` and interrupted the still-running
  n=3 schema-2 regeneration before it emitted final artifacts.
- Schema 3 now includes the fixed-full root-case ID and exact source and
  target rooted graph IDs in every state identity.  Both covers must be
  regenerated, and independent reviewers have been instructed to reject any
  cross-root or cross-rooted-graph merge.

## 2026-08-10T02:33:00-07:00 — schema-3 theta-2 cover passes primary replay

- Regenerated all 132 filtered theta-2 fixed roots with schema 3.  The exact
  stream contains 2,106 path-bound states: 1,860 generic polynomial
  separations, 114 refinement states, and 132 labelled-isomorphism terminals.
  There is no ordinary-`T`, non-`T`, unsigned, or unresolved terminal.
- The strengthened primary verifier independently rereads all four streams,
  checks every graph and polynomial body, rebuilds every displayed-tree
  pullback, validates every path-specific parent/child relation, and reaches
  all states from the 132 root entries.  It reports `EXACTLY VERIFIED`.
- This closes the primary theta-2 base gate only.  Clean-room regeneration,
  adversarial mutations, the schema-3 n=3 cover, unequal directed pairs, and
  terminal probes are still required before promotion.

## 2026-08-10T02:43:00-07:00 — frozen weak-class theorem replayed

- Replayed `../s_tc_jc_sharp_boundary/reproducibility/verify_release.py` from
  the active environment.  The manifest, manuscript scope lock, primary
  symbolic verifier, and independent implementation all pass.
- The replay checks binary/LSA/tree-child rooted witnesses, level two,
  nonisomorphic non-`T` semi-directed reductions, all six exact invariants,
  all 256 Fourier coordinates at the algebraic interior point, and both
  rank-eight Jacobian minors.  The all-taxa weak-but-not-strong sharpness
  branch remains frozen and available for the final synthesis.

## 2026-08-10T02:48:00-07:00 — convention gate closed after correction

- The clean-room convention referee compared the exact definitions in
  Englander et al. v4, Holtgrefe et al. v2, and Brits et al. v2.  There is no
  single literal reduction map shared by all three sources.
- The locked reticulation-preserving `sd_0` map agrees with Englander v4 and
  is the binary LSA-valid specialization of Holtgrefe.  It is strictly
  narrower than the exhaustive degree-two/parallel cleanup in Brits; an
  exact LSA-valid level-2 fixture separates the two conventions.
- The theorem scope is therefore corrected to simple binary LSA-rootable
  mixed graphs produced by `sd_0`, level at most two, with no omnians.  No
  claim is made for every preimage of the broader cleanup map.
- The independent verifier checks all 12 primitive supports and all 100 of
  their admissible rootings, the weak Theta rooting counts, the `K4-e`
  double-triangle exclusion, and eight convention mutations.  The gate is
  `VERIFIED AFTER CORRECTION`; local algebra remains separately pending.

## 2026-08-10T03:31:00-07:00 — exact replay rejects mixed-code descriptor cache

- The first complete schema-3 three-outgoing merge was rejected by the
  strengthened graph-to-polynomial replay.  A target graph with content ID
  `83fbeab153b433dea88528707b25a74898a924b90b1eff000c5a7c10257c8dd8`
  cited a sparse polynomial generated from another rooted presentation with
  the same standard mixed code.  The regenerated and stored exact polynomial
  hashes differed, and their variable counts were 12 and 11.
- The cause was a descriptor cache keyed by selected-port count and standard
  mixed code.  A sparse polynomial's variables follow the exact rooted arc
  order, so no such cross-presentation cache is graph-bound.  The complete
  failed stream and the first affected state are quarantined; none of its
  counts is active evidence.
- The producer now keys descriptors by selected-port count and exact rooted
  graph ID.  The merger and replay reject any weaker declared cache scope.

## 2026-08-10T03:47:00-07:00 — zero-sum root quotient corrected

- A second adversarial check found that admissible root placements of one
  standard mixed graph can give descendant masks differing by split
  complement.  On the retained Fourier domain the boundary characters sum
  to zero, hence `xor(A)=xor(A^c)` exactly.  The hard-cover descriptor now
  replaces every quartet mask by `min(A,A^c)` before zipping duplicate edge
  rows; the two root arcs become the effective product edge.
- Added an exact regression using two root placements of one labelled
  quartet.  Their raw rooted descriptors differ, their standard mixed codes
  agree, and their complement-normalized descriptors and complete JC
  coordinate polynomials agree.  An independent clean-room proof and a
  separate audit of the bounded atlas's graph-specific physical convention
  are active.
- Every n=3/n=4 hard-cover and terminal-probe body generated before this
  correction is superseded.  Large obsolete streams were removed only after
  recording their SHA-256 digests in the quarantine README.

## 2026-08-10T04:18:00-07:00 — corrected n=4 base and compact probes pass primary replay

- The final complement-normalized theta-2 base contains 132 fixed roots and
  2,106 graph-bound states: 1,860 generic separators, 114 refinements, and
  132 labelled-isomorphism terminals.  Its summary SHA-256 is
  `915bed0a3add001c1a94d6d862a2359e6ad75b3489f8d71b7adf006952b5ce37`;
  the strengthened primary replay passes.
- The path-bound `A+p` and `A+p+q` universe was regenerated in four compact
  shards covering every one of the 132 terminal paths.  The primary exact
  replays decode all 168,582 child relations and report 153,072 generic
  polynomial separations and 15,510 coherent labelled isomorphisms, with no
  unresolved class.  This n=4 family has no ordinary-`T` terminal and does
  not by itself certify T-edge probe coherence.
- A verbose graph/state/binding representation is now being regenerated for
  record-by-record comparison with the compact encoding.  Clean-room review,
  mutation tests, n=3 closure, and unequal directed pairs remain mandatory;
  no global theorem is promoted.

## 2026-08-10T04:24:00-07:00 — simultaneous unequal-relation runs terminated

- The n=3 and n=4 graph-bound unequal-directed-relation compilers were run
  concurrently with four hard-cover shards and the verbose probe producer.
  Both processes received termination signal 15 before emitting a final
  summary.  Neither run is a certificate and no partial count is retained as
  evidence.
- This is recorded as a resource-scheduling failure, not an algebraic result.
  The relation compilers will be rerun sequentially after the hard-cover
  shards release memory.  The theorem gate remains fail-closed.

## 2026-08-10T04:31:00-07:00 — corrected n=3 cover merged after fail-closed metadata check

- All four disjoint root shards completed with zero unresolved terminals.
  The merger initially rejected shard 0 because it had been launched just
  before the producer began emitting the descriptive bounded-atlas field
  `descriptor_mask_convention`; shards 1--3 contained the field.
- Removing only that field and nondeterministic elapsed time makes all four
  bounded summaries exactly equal.  A hash-bound metadata-only migration adds
  the true convention label to shard 0 and changes no graph, polynomial,
  relation, or root stream byte.  This incident is preserved rather than
  bypassed in the merger.
- The merged cover has 5,344 roots, 68,584 graph-bound states, 14,482 rooted
  graphs, and 225 polynomial bodies.  Its terminal census is 56,055 generic
  separations, 4,036 strict open-cube separations, 8,349 refinements, 120
  labelled isomorphisms, and 24 ordinary-T relations, with zero unresolved
  class.  The merged summary SHA-256 is
  `791844a802af61f64cba937a5adbe9d1d381d3fd7e55165914d4e4c885908e65`.
- These remain primary counts until the exact merged replay and independent
  mutation-sensitive audit pass.

## 2026-08-10T04:45:00-07:00 — n=3 base and path probes close in primary replay

- The strengthened merged replay independently rebuilt all 68,584 n=3
  graph-to-polynomial records and verified the 56,055 generic, 4,036 strict,
  8,349 refinement, 120 isomorphism, and 24 ordinary-T classifications.  It
  found 9,721 standard mixed tensor descriptor orbits and no root-dependent
  complement-normalized descriptor.
- The complete path-bound one-/two-port universe has exactly 144 allowed
  terminal paths.  Four disjoint compact shards enumerate and replay 90,008
  generic polynomial separations, 624 strict open-cube separations, 9,676
  coherent labelled isomorphisms, and 840 coherent ordinary-T children, with
  no unresolved classification.
- Attempting all four semantic replays concurrently was rejected by the
  machine's resource envelope.  A measured single-shard replay peaks at
  6,289,457,152 bytes RSS; all four were therefore rerun sequentially and
  pass.  The terminated concurrent attempts emitted no certificate and are
  not mathematical evidence.
- A verbose n=3 graph/state/binding package is being generated for
  representation-level comparison, and the clean-room n=3 base audit is
  active.  Primary closure alone does not promote the theorem.

## 2026-08-10T04:57:00-07:00 — first sequential n=3 relation retry failed closed

- The first nominally sequential unequal-directed-relation retry overlapped
  the n=3 verbose probe producer and two independent semantic replays.  It
  terminated with exit status 1 after reporting 4,000 raw presentations,
  3,852 canonical relations, 330 regenerated sign bodies, and zero reported
  algebraic failures, but before writing any relation stream, summary, or bit
  cache.
- Those progress numbers are diagnostic only.  The attempt is recorded in
  `quarantine/bounded_relation_n3_retry1_failure.json` and contributes no
  theorem evidence.  A genuinely isolated retry will run only after the
  active probe and hard-cover replays release memory.

## 2026-08-10T05:14:00-07:00 — isolated cycle relation run failed at final serialization

- Sharding the n=3 relation universe by source core allowed the cycle shard
  to generate all of its graph, relation, polynomial, sign, and descriptor
  streams with zero reported algebraic failure.  The program then raised a
  `Path.relative_to` exception because the explicitly supplied bit-cache path
  was relative while the serializer expected an absolute path.  It therefore
  wrote no top-level summary and is not a certificate.
- The complete diagnostic counts, logical-stream commitments, compressed-file
  commitments, traceback, and cache hash are preserved in
  `quarantine/bounded_relation_n3_cycle_finalization_failure.json`.  The path
  bug was corrected by resolving output paths immediately after argument
  parsing.  The exact target-signature prefilter can now be disabled so an
  unfiltered/filtered equivalence regression can be replayed under one code
  version before the optimized stream is used.

## 2026-08-10T05:43:30-07:00 — n=3 cycle directed relations close in primary replay

- The failed-finalization streams were regenerated under the corrected code
  with the exact target-signature prefilter disabled.  The resulting
  top-level summary has SHA-256
  `f857fabc1bdcdfa0d7f91b0f68cc7a9a0fd0b519169f3eb8bf85c623e44a774d`,
  and every normalized graph, polynomial, sign, and relation body is bytewise
  equal to the preserved diagnostic stream.
- A second run retained only target signatures satisfying the necessary
  source-relative predicate `s & ~t == 0`.  It reduced 127 target signatures
  to 55 while reproducing exactly the same 9,036 decorated relation bodies,
  7,602 graph bodies, 677 polynomial bodies, and 677 strict-sign records.
  The relation census is 4,092 strict open-cube separations, 4,932 pending
  support completions, and 12 isomorphism-or-ordinary-T relations, with no
  compiler failure.
- The first strengthened replay failed because the in-memory sign certifier
  used tuples for `used_variables` and `degrees`, while the JSON certificate
  reloaded the same ordered arrays as lists.  This failure and its first exact
  relation/polynomial identifiers are preserved in
  `quarantine/bounded_relation_cycle_filtered_replay_failure.json`.  After a
  JSON-normalization step at that representation boundary, with every scalar,
  factor, sign, polynomial, and array entry still compared exactly, the full
  9,036-relation replay passes.
- This closes only the primary n=3 cycle source shard.  The theta source
  shards, complete hard-cover crosswalk, and clean-room relation audit remain
  load-bearing.

## 2026-08-10T05:51:07-07:00 — complete n=3 directed relation universe closes in primary

- The independently partitioned source-core shards `cycle`, `theta-0`,
  `theta-1`, and `theta-3` exhaust the verified three-outgoing support
  universe.  The fail-closed merger rejects missing or duplicate source cores
  and produced 10,466 canonical decorated directed relations: 5,284 strict
  open-cube separations, 5,120 pending support-completion relations, and 62
  labelled isomorphism-or-ordinary-T relations.  Its summary SHA-256 is
  `d94533afa40126b9623cccb29ed07f1fd0994377f86a80274f725613e4e25d87`.
- A complete merged replay regenerated all 7,726 rooted graph bodies, 800
  exact polynomial bodies, every strict sign certificate, all relation IDs,
  all port maps, and every classification with no discrepancy.
- The first hard-cover crosswalk report failed after writing its stream
  because its output path had not been resolved before `relative_to`; the
  diagnostic stream and traceback metadata are preserved in
  `quarantine/bounded_relation_n3_crosswalk_finalization_failure.json` and are
  not evidence.  After fixing only path normalization, deterministic
  regeneration produced the identical compressed stream hash
  `cfc128a65d5547416ec4e860cb55fdea2a1773a5d16385743f357521909c2e68`.
- Exactly 5,344 pending raw relation coverages bind bijectively to the 5,344
  fixed-full n=3 hard-cover roots.  Thus no equal-signature nonretaining
  presentation is lost by canonical relation merging.  Independent
  graph-to-algebra/crosswalk review and mutation rejection remain mandatory.

## 2026-08-10T06:02:22-07:00 — first n=4 cycle relation attempt stopped for machine safety

- The n=4 cycle-source compiler overlapped two long primary probe replays and
  two independent exact n=3 reviews.  During a target pullback expansion,
  dynamic swap reduced free data-volume space below 0.4 GiB.  The process was
  interrupted deliberately before the workstation could exhaust disk.
- It had reported 4,000 raw presentations, 3,779 canonical relations, 64
  cached signs, and zero reported failures, but had emitted no top-level
  summary or certificate stream.  Those counts are diagnostic only and are
  preserved in `quarantine/bounded_relation_n4_cycle_resource_stop.json`.
- One independent n=3 terminal routine was also stopped after a separate
  adversarial reviewer proved that routine incompatible with two active
  labels.  Its successful path-only audit remains usable; its terminal layer
  is withdrawn and independently replaced.  The n=4 relation census will be
  restarted from the beginning after memory and swap pressure subside.

## 2026-08-10T06:19:38-07:00 — exact certified-cache optimization regression

- The resource stop occurred while the compiler expanded every possible
  target-only pullback even when one candidate in the same relation already
  had a cached exact strict-sign certificate.  The selection order always
  ranks a cached candidate before any uncached candidate.  The compiler now
  selects the least cached certified candidate before expanding pullbacks
  that cannot affect the chosen witness; if none exists, it executes the
  original exhaustive search unchanged.
- A complete fresh n=3 cycle-source run under the optimized code reproduced
  exactly the prior 9,036 relation bodies, 7,602 graph bodies, 677 polynomial
  bodies, 677 sign records, every logical stream hash, and every selected
  witness.  The regression certificate is
  `primary/certificates/bounded_relation_n3_cycle_cacheopt_equivalence.json`.
- The compact-probe schema was corrected in response to independent review:
  evidence-format equivalence requires exact graph relation, direction,
  insertion, class, and transport, plus independent validation of each
  selected witness.  It no longer falsely requires two valid deterministic
  implementations to select the same separator when several exist.

## 2026-08-12T21:31:08-07:00 — proof-first closure replaces further atlas expansion

- No further large topology or relation search will be used on the active
  proof path.  Three independent adversarial proof audits agree that the
  corrected cut, incidence-gauge bridge, root-reduction, marginal-submersion,
  probe-coherence, and global no-compensation layers survive.  Their commits
  are `3a2bdfa3`, `9ad318ac`, and `adcf72bb`.
- The global theorem now has one exact mathematical premise, `L_blob`: a
  source-full projective JC containment between two complete standard-strong
  level-2 blob factors is labelled isomorphism or ordinary triangle
  redirection.  Source and target incoming presentations must be chosen
  independently.
- A proposed bridge decomposition of a triangle-bearing theta was rejected.
  Such a theta meets its complementary path at two hidden poles, not across a
  cut edge, and the resulting hidden-pair contraction has a gauge larger than
  the bridge incidence group.  This is an obstruction to that proof shortcut,
  not a JC counterexample.
- The active proof-first closure of `L_blob` is instead a finite grammar
  theorem.  Every source has a rigid core-preserving support: the three-port
  stream covers the cycle (with its separate three-sunlet base case) and
  `theta-0`, `theta-1`, `theta-3`; only the triangle-free `theta-2` core needs
  four outgoing support ports.  The frozen exact algebra and probe streams
  already classify these supports.  What remained from the reviews was an
  independent proof and normalized regeneration that the five-core repair,
  incoming-role, completion, port-transport, and restoration grammar maps
  onto every frozen fixed-full root relation.  That bounded independent gate
  is now running; it regenerates no Fourier atlas and performs no open-ended
  search.
- A separate quarnet/strong-repair proof is being tested as an independent
  conceptual route.  It must handle intrinsically weak induced quarnets and
  the two possible repairs of the weak Theta omnian; it will not be promoted
  unless it closes those cases without assuming the desired lifting.
- The release remains fail-closed.  Outcome P will be promoted only after the
  inventory theorem, exact local algebra crosswalk, and a fresh adversarial
  review agree.  Otherwise the first exact failure will be preserved and the
  counterexample route resumed.
## 2026-08-12T22:05:00-07:00 — theta-2 signature gate strengthened to presentation level

- The first independent five-port theta-2 signature replay regenerated the
  complete selected/marginalized-incoming completion grammar and found only
  the three expected necessary invariant-signature pairs.  A mutation audit
  correctly rejected that first release because its complement-width attack
  was semantically ineffective; the failed certificate is preserved.
- A stronger presentation-level comparison then exposed a gap hidden by the
  three signature hashes: the raw survivor stream has 192 presentations,
  whereas the frozen hard-cover inventory has 132 decorated roots.  The gate
  remains **FALSE / UNRESOLVED** until an independent canonicalization of the
  coloured source-target mixed relation determines whether the extra 60 are
  merely alternative root presentations or genuinely omitted relations.
- The count pattern is diagnostic but not yet evidence: for each of the three
  theta-2 source supports, the 64 raw survivors split as 44
  marginalized-incoming and 20 selected-incoming presentations, while the
  frozen inventory contains 44 roots.  A root-relocation quotient could
  explain the discrepancy, but it must be proved with explicit mixed-graph
  transports and mutation-sensitive relation keys.
- Outcome P is not promoted.  No broader topology search was started.

## 2026-08-12T22:30:00-07:00 — five-port theta-2 gate closes after fail-closed corrections

- The corrected independent exact signature replay regenerates the complete
  five-port theta-2 source and target grammar, both incoming modes, the
  84-invariant orbit, and every relative port assignment.  Only three
  necessary signature pairs survive, all equal.
- Equality of three hashes was not promoted.  Expanding all provenance gives
  192 raw presentations.  Independent mixed-graph canonicalization and
  explicit transports prove the intrinsic partition: 18 direct labelled
  isomorphisms, 42 selected-incoming root-presentation duplicates, and 132
  marginalized-incoming presentations equal to the frozen hard-cover root
  multiset.
- Two semantically ineffective mutation designs and the initial 192-versus-
  132 failure are preserved.  The corrected active mutations all reject.
- Together with the independently regenerated n3 directed relation universe,
  both schema-3 hard covers, and the common-anchor arbitrary-subdivision
  theorem, this proves the local blob-containment lemma.  Every mathematical
  dependency of Outcome P is now closed.  A fresh whole-proof adversarial
  review and clean release replay remain mandatory before final promotion.

## 2026-08-12T22:55:00-07:00 — first whole-proof referee withholds Outcome P

- The independent whole-proof referee at commit `5377048d` found no standard-
  strong counterexample and verified the convention, cut, bridge, root,
  theta-2, triangle, global-logic, and weak-sharpness layers.  It nevertheless
  returned **UNRESOLVED / HOLD SUBMISSION** for three exact reasons.
- The n3 clean-room gate checked every supplied relation but had not generated
  the completion/presentation universe independently.  The arbitrary-word
  package covered 144 restoration terminals but omitted the 62 direct
  residual anchors.  Finally, the large verbose probe streams were untracked,
  so a clean clone could not replay the claimed release.
- The report and all requested manuscript corrections are preserved in
  `reviews/final_outcome_p_referee/`.  No positive status was promoted.

## 2026-08-12T23:05:00-07:00 — independent n3 universe generation closes the first gap

- A clean implementation derives the eight source supports, 831 selected-
  incoming and 1,983 marginalized-incoming completions, every relative port
  assignment, and both source-to-target directions before reading the primary
  relation claim.
- It regenerates exactly 10,826 raw and 10,466 merged relations.  The raw and
  merged normalized multisets agree byte-for-byte with independent SHA-256
  commitments; multiplicities are 10,106 singleton and 360 double relations.
  Six deletion, duplication, direction, assignment, and coverage mutations
  are rejected.  Commit: `3f9af468`.

## 2026-08-12T23:40:00-07:00 — direct-anchor arbitrary words close exactly

- The 62 direct residual anchors have four ports and therefore cannot be
  identical to any of the 144 restoration terminals, which have five to seven
  ports.  A separate proof-forced compiler was required rather than a false
  crosswalk.
- The independent package classifies all 2,642 one-port relations and all
  18,224 two-port relations above the 314 surviving parents.  Exactly 34 base
  anchors are labelled isomorphisms and 28 are ordinary triangle
  redirections.  Every one of the 18,520 unequal child relations has a
  graph-derived exact JC separator; all surviving child transports restrict
  their unique parent.  Twelve semantic mutations are rejected.  Commit:
  `a33cb4b0`.

## 2026-08-13T00:05:00-07:00 — compact-only clean-clone probe gate

- The active release no longer consumes any untracked verbose
  `probe_extension_*` artifact.  A compact-only semantic replay reconstructs
  all graph insertions, switchings, masks, Fourier descriptors, invariant
  pullbacks, signs, and transports for 101,148 n3 and 168,582 theta-2 probe
  relations from 50 tracked byte-locked inputs.
- All nine mutations are rejected, the maximum attained probe size is ten
  ports, and a fresh `git archive HEAD` quick plus full replay succeeds.
  Commit: `d63289fa`.
- All mathematical and clean-input gates identified by the first referee are
  now closed.  A new whole-proof adversarial referee is running against the
  integrated candidate; Outcome P remains unpromoted until that verdict.

## 2026-08-13T01:10:00-07:00 — terminal whole-proof verdict verifies Outcome P

- The second independent adversarial referee returned **VERIFIED** and found
  no remaining load-bearing mathematical gap.  It independently confirms the
  one-sided and symmetric JC classification modulo ordinary `T`, the absence
  of proper generic one-sided containment, the arbitrary-subdivision closure,
  the projective bridge localization, and the frozen weak-class sharpness
  theorem.
- The report preserves all nonmathematical defects seen at the reviewed
  commit: absent final metadata, an intentionally fail-closed release wrapper,
  and local historical untracked artifacts that are not active inputs.
- `FINAL_OUTCOME.json` is now promoted to Outcome P.  Remaining work is purely
  mechanical: stable PDF, deterministic archive, and clean-worktree quick,
  full, and regeneration transcripts.

## 2026-08-13T01:35:00-07:00 — clean replay removes stale root wrapper

- The first clean `verify_full.sh` run exposed an active-script defect: it
  invoked the historical scope-limited `reviews/root_probe/verify_all.py`,
  whose obsolete primary-atlas assertions depend on files deliberately absent
  from the release.  The failure is preserved in the clean transcript.
- The active root theorem itself did not fail.  A new read-only wrapper now
  regenerates, in a temporary directory, exactly the independently accepted
  root-move, incoming-role, probe-coherence, and path-product-submersion
  certificates, requires byte-for-byte equality with the committed records,
  and excludes the superseded primary-atlas audit.  The release script and
  crosswalk now name this precise scope.

## 2026-08-13T02:05:00-07:00 — deterministic clean-tree normalization

- The repaired full gate passed every mathematical check but correctly failed
  its final clean-tree assertion.  Exactly two tracked records changed: the
  convention certificate embedded the absolute checkout path, and the n3
  manifest's recursive file walk treated a tracked dotfile differently under
  the clean environment's Python version.
- Both generators are now location/version invariant.  Convention source
  names are stored relative to the project or shared repository root, and the
  manifest explicitly excludes hidden administrative files.  No graph,
  polynomial, rank, sign, relation, or theorem datum changed.

## 2026-08-13T02:25:00-07:00 — regeneration uses the pinned interpreter

- The first clean all-record regeneration passed the n3 and theta-2 graph-to-
  algebra layers and both hard covers, then failed before direct-anchor
  compilation because its nested shell wrapper defaulted to the system
  `python3`, which lacked SymPy.
- The active regeneration command now passes the already bootstrapped pinned
  interpreter explicitly.  This changes no verifier semantics; it makes the
  declared dependency environment effective through the nested wrapper.

## 2026-08-13T02:40:00-07:00 — Outcome P release sealed from clean clones

- At exact commit `35291bba72f52ac800e99ea797ddad20d9852a67`, the quick,
  full, and all-record-regeneration commands all exited successfully in clean
  detached worktrees and left their tracked trees unchanged.
- Wall times were 49.06 seconds, 1,322.94 seconds, and 1,330.24 seconds,
  respectively.  The full gate regenerated 269,730 theorem-forced compact
  probe relations and rejected all semantic mutations.  The regeneration
  gate independently rebuilt every load-bearing bounded record.
- The 18-page manuscript was rendered afresh and inspected page by page; no
  clipping, overlap, missing page, placeholder, unresolved citation, or LaTeX
  layout warning was found.
- Exact transcripts, environment details, and archive reproduction metadata
  are recorded under `release/`.  Outcome P is publication-ready; no
  mathematical or release-engineering blocker remains.

## 2026-08-15T22:10:00-07:00 — workstream consolidated

- Moved every active, historical, audit, submission, and release-engineering
  directory for this project beneath `s_tc_jc_landmark_closure/`; the former
  root-level copies were moved rather than duplicated.
- Updated path-sensitive packaging scripts, verifier entry points, manifests,
  and ignore rules for the consolidated layout. The published v1.1.0 tag was
  left unchanged as an immutable release snapshot.
- File-organization work is complete (100%); no mathematical replay or PDF
  visual audit was performed for this organizational commit.

## 2026-08-16T17:25:00-07:00 — targeted v1.1.1 referee hardening

- Adjudicated the final adversarial report item by item without de-scoping the
  theorem.  The bridge locus is now explicitly componentwise normalized, and
  the finite target-completion union is connected to the bounded theorem by
  the semialgebraic finite-cover lemma.
- Expanded the physical analytic-section, image-tangent, genericity, triangle
  context, and simultaneous-gluing arguments at their exact handoff points.
- Updated the title to advertise generic identifiability precisely, synchronized
  the supplement and submission metadata, and removed the Figure 2 label
  overlap.
- A fail-closed regression and response table are under
  `reviews/v1_1_1_referee_revision/`.  Exact full replay and final adversarial
  release review are the remaining gates.
## 2026-08-16 — v1.1.2 public replay and submission-package hardening

- Accepted a fresh adversarial verdict that passed the mathematics but found
  stale public replay evidence, monorepository-breaking supplement commands,
  and one missing genericity qualifier.
- Corrected those issues without changing a theorem, network convention,
  model domain, local atlas, or sharpness family.
- Replaced reader-facing “independently implemented replay” with “separately
  implemented replay” and retained the explicit disclaimer that this is not
  independent human review.
- Moved the obsolete 18-page clean-replay record under immutable superseded
  history and prepared a current non-self-referential v1.1.2 GitHub Release.
- Built exact portal bundles for bioRxiv, Systematic Biology, and the Journal
  of Mathematical Biology, including cover letters, editable sources,
  metadata, checksums, upload maps, and human stop gates.
- Rendered every page of all delivered PDFs, inspected complete contact
  sheets and full-size critical pages, and verified all fonts are embedded.
- Added a fail-closed v1.1.2 package/provenance verifier with active mutation
  rejection and commissioned separate mathematical-scope and release-package
  adversarial reviews.
## 2026-08-16 — v1.1.2 release hardening and journal packages

- Accepted the external review's manuscript corrections: the Section 10
  biological summary now says “generic,” replay implementations are described
  as “separately implemented,” and supplement commands work from the public
  monorepository root.
- Moved the obsolete 18-page Outcome-P replay records to immutable history and
  added a local SHA-256 manifest.
- Added exact bioRxiv, Systematic Biology, and Journal of Mathematical Biology
  portal packages, metadata, cover letters, upload maps, human checklists, and
  deterministic source ZIPs. The JMB-specific supplement is Online Resource 1.
- Added a clean extracted-ZIP replay that executes the documented commands and
  reproduces all six submission PDFs byte for byte.
- Split offline candidate verification from the post-upload public-release
  gate and changed the public manifest to a flat seven-record commitment over
  the other downloaded assets. Publication remains gated on an annotated
  v1.1.2 tag, eight exact GitHub Release assets, and
  `PUBLIC_RELEASE_VERIFIED`.

## 2026-08-17 — v1.1.3 Englander-v4 crosswalk and submission hardening

- Audited the supplied Englander et al. v4 PDF line by line against the Omega
  comparison.  Both Omega networks are differently labelled type-(2c)
  quarnets up to reflection; no cited type-(2c)-versus-type-(2c) result
  separates them, and both fail the cited strong tree-child incidence
  criterion.
- Replaced the target-dimension handoff by the exact leaf-coordinate
  permutation argument, printed all four Omega rank-nine row/column witnesses,
  reconciled the `q123`/`q111` trinet notation, and added the 2025
  quartet-distance comparison.
- Added compact verifier-entrypoint capsules to all three submission-support
  directories.  The bioRxiv map uploads its capsule, while the Systematic
  Biology and Journal of Mathematical Biology maps route theirs to the
  external repository according to the journals' current instructions.
- Two successive adversarial reproducibility reviews found and forced repairs
  to the deterministic source-build environment, annotated-tag/archive byte
  binding, journal routing, clone-versus-archive commands, and current package
  manifest coverage.  Both failed reviews are preserved verbatim under
  `reviews/v1_1_3_englander_revision/`.
- The literal commands inside all three source ZIPs now reproduce all six
  article/supplement PDFs and both cover letters byte for byte without an
  inherited build epoch.  Every package manifest and targeted v1.1.3
  regression passes.  A third fresh adversarial release review rejected
  seventeen mutation classes and returned `PASS`.  No DOI has been requested,
  invented, or inserted.

## 2026-08-17 — v1.1.4 bounded proof, citation, and Figure 7 revision

- Inspected only the cited pages of the author-supplied 429-page
  Bochnak--Coste--Roy text.  Theorem 2.2.1 and Propositions 2.8.2, 2.8.4,
  2.8.5(i)--(ii), 2.8.13, and Theorem 2.8.8 match the uses recorded in
  `reviews/v1_1_4_bcr_and_figure_revision/BCR_CITATION_AUDIT.md`.
- Replaced the finite-cover proof by a chartwise semialgebraic argument that
  keeps the original arbitrary relatively open set and chooses a smaller
  semialgebraic neighborhood internally.  The local projective containment
  relation is now formally distinct from global JC containment.
- Removed the production-fragile box around the bounded atlas theorem,
  corrected the theorem label and bibliography metadata, narrowed the final
  Englander comparison, and printed the alternative Omega rooting arc array.
- Moved leaf 2 left of vertex D in both Figure 7 panels.  The final pendant
  edges are plainly visible in both Poppler and PDFium renderings.
- Rebuilt the bioRxiv and both journal packages.  Extracted source archives
  reproduce all eight delivered PDFs byte-for-byte; all pages were rerendered,
  all font programs are embedded and subsetted, and the updated visual audit
  is sealed under `release/final_biorxiv/`.
- No theorem statement, model domain, network class, sharpness family, or DOI
  claim changed in this bounded revision.

## 2026-08-19 — v1.1.5 curated proof-certificate release

- Replaced the broad development snapshot as the primary proof object by a
  curated reviewer-facing atlas bundle containing only primitive inputs,
  complete finite records, exact certificates/transports, primary and
  separately implemented verifiers, and archive-local entry points.
- Added a per-relation index for all 10,466 three-outgoing relations and all
  192 four-outgoing survivors, with distinct base and restoration-closure
  certificate/verifier fields.
- Added fail-closed package mutation tests and a two-run deterministic logical
  regeneration gate. Quick, full, and regenerate-all modes pass in isolated
  copies; complete run logs are distributed outside the self-authenticating
  archive.
- Reduced every manuscript/supplement certificate crosswalk to six active
  rows and removed audit reports and development-history paths from the
  evidentiary surface. Submission capsules are now navigation-only.
- Prepared a DOI finalization tool and Zenodo-first upload sequence without
  requesting, inventing, or publishing an identifier.
