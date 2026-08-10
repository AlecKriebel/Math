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
- A separate explicit four-boundary ordinary-`T` example was extracted from
  the primitive records.  Its source hash is
  `25e272478915938e49b980ad172aa4f590f44fba8d0c50aaecf826fef7f46623`,
  its target rooted-presentation hash is
  `2e3b531105573999bd129e4cfa105136cf074cf2924481e9d5f9aba13ae1932f`,
  and the full port map is `{0:2,1:3,2:0,3:1}`.  The source admits only
  physical boundary `0`, while the target admits only `1` or `2`, so no
  incoming-to-incoming representative exists for this valid standard
  semi-directed `T` relation.
- The primary compiler has been repaired to anchor all source boundaries and
  enumerate all target boundary permutations.  This repair is not promoted:
  the complete graph-bound relation streams and a clean-room normalized
  comparison must be regenerated under the larger universe.
- The root/probe reviewer modified the primary compiler while investigating
  this issue despite its declared read-only scope.  That independence breach
  is preserved.  Its graph-theoretic counterexample remains independently
  replayable, but the modified primary bytes are treated only as discovery
  code until the separate incoming-boundary reviewer agrees.
