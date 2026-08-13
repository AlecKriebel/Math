# Adversarial root/probe review

Status: **FINAL, SCOPE-LIMITED REVIEW — structural audit complete; local
algebraic hard cover not accepted in this scope**

## Scope and independence

This review treats the conclusions in
`ROOT_REDUCTION_THEOREM.md`, `GENERATOR_AND_SUPPORT_THEOREM.md`,
`LOCAL_ATLAS_THEOREM.md`, `GLOBAL_THEOREM_DRAFT.md`, and
`DEFINITIONS_LOCK.md` as hypotheses.  It also audits the primary
core/completion/support sources and certificates.

The mathematical graph model, forbidden RR-branch case, repair criterion,
root-move argument, selected-strength distinction, submersion criterion, and
probe-coherence falsification tests were fixed in `DERIVATION_LOCK.md` before
the corresponding primary implementation was read.  The incoming-role
quantifier was likewise locked before re-inspecting the label action for that
issue.  The clean verifiers import no primary module.  Primary code was
inspected only afterward to compare semantics.

All counterexamples were serialized under `counterexamples/` before any
correction was proposed.  No file outside this review directory was modified
by this review.

## Verdicts

| Major claim | Verdict | Exact conclusion |
|---|---|---|
| Real-boundary root reduction | **VERIFIED** | The all-tree path, exact narrow suppression, arrowheads, DAG, reachability, LSA, tree-childness, displayed-tree JC tensor, and open edge splitting all pass.  The revised proof now includes the required LSA and old-root-suppression arguments. |
| Root reduction supplies a matched incoming boundary for two factors | **FALSE** | It proves only that each factor has some rootable real boundary.  Exact supports admit physical matchings for which the two rootable sets are disjoint. |
| Primitive generator exhaustiveness | **VERIFIED** | One cycle plus four theta event cores are exhaustive.  The separately enumerated two-reticulate-branch case has zero classes. |
| Automatic at-most-one-triangle | **VERIFIED** | The only simple two-triangle theta is `K4-e`; all 54 reticulation-arrow markings give 25 admissible rootings and zero tree-child rootings. |
| Proposed sink-plus-minimum-repair criterion as generic `red_*`-reduced `S_TC` strength | **FALSE** | Omitting the cycle sink reduces to a strong two-boundary tree. |
| Sink-plus-minimum-repair criterion for **strong retention of the original primitive core** | **VERIFIED** | Across all five cores, every occupancy pattern and every alternate repair, it agrees exactly with the intrinsic all-rootings census when all genuine sinks are retained. |
| Pointwise rigidity of bounded supports | **VERIFIED** | Every alternate clean support and all 579 primary support/probe records have pointwise stabilizer one. |
| Support-plus-one/two reconstruction and conditional probe coherence | **VERIFIED** | No collision in 8,976 exact two-extra-port presentations; three-extra-label order decks are injective for all 24, 210, and 336 words on 2, 5, and 6 segments.  The revised proof contains the required triangle-destruction case split. |
| “Every probe-level `T` choice refers to a triangle present in every probe” | **FALSE** | Adding a port on an edge of the support triangle destroys that triangle.  Coherence survives because this probe has no `T` ambiguity and fixes literal orientation. |
| Selected physical-parameter to descriptor map is an onto semialgebraic submersion | **VERIFIED** | All 42,908 corrected bounded completion maps, in both incoming modes, have full row rank; the product-class proof works for arbitrary class size. |
| Descriptor cube is a minimal-coordinate selected model-image manifold | **FALSE** | 37,400 completions have repeated switching columns after core collapse; inheritance coordinates can be tensor-redundant. |
| Dummy-completion partition remains exhaustive under `red_*` | **VERIFIED** | Zero descriptor mismatch in 24,792 exact restrictions: 12,396 with structural incoming selected and 12,396 with it marginalized; 17,304 restrictions lose at least one reticulation. |
| Fixed-`INCOMING`, outgoing-only target quotient is exhaustive | **FALSE** | Among 2,808 exact support/bijection cases, 144 have no matched rootable boundary.  The four-port witness requires relative permutation `[2,3,0,1]`, outside the size-6 fixed-incoming subgroup. |
| Anchored source plus full target `S_p` boundary permutations | **VERIFIED** | Simultaneous relabelling gives an exhaustive relative-orbit representative only when all `p` physical target ports, including the structural incoming position, are permuted. |
| Marginalized target structural incoming completion | **VERIFIED** | If the target rootable port is outside the probe, retaining it as a zero-character dummy gives the exact selected descriptor in every clean restriction tested.  It is never promoted as a core-retaining topology. |
| Anchored-source representative is unique by pointwise rigidity | **FALSE** | Pointwise rigidity does not kill setwise label-action stabilizers.  Exact order-two exceptions occur.  They duplicate representatives but omit none. |
| Every non-core-retaining equality is discharged by the claimed cycle-source/theta-target completion gate | **UNRESOLVED** | Source routing is correct, but the cycle/theta union compiler still fixes incoming and omits marginalized-incoming completions; post-repair relation streams and an independent normalized comparison are absent. |
| Directed local atlas theorem | **UNRESOLVED** | Its structural, full-`S_p` quotient, parameter-map, and coherence mechanisms pass in the corrected bounded source; the proof ledger and hard-cover union have not yet absorbed or certified the incoming-role repair. |
| Candidate global theorem | **UNRESOLVED** | The scoped root/generator/support gates pass, but incoming-role promotion and the local hard cover are unfinished; other global dependencies were not re-audited here. |

## 1. Root reduction

Let

```text
r=v_0 -> v_1 -> ... -> v_k -> i
```

be a path obtained by taking a tree/leaf child at every step.  No edge on the
path enters a reticulation, so every reversed edge is ordinary.  A new cycle
would require an old directed re-entry into a path tree vertex; that would be
a second parent, or would already have made an old directed cycle.  Thus the
rerooted graph is acyclic.

The root move must suppress the old root after reversal.  Its off-path child
edge becomes the same edge produced by the original `sd_0`; if that child is a
reticulation, the arrowhead at that child is retained.  Suppressing the new
root returns the identical mixed graph, not merely an isomorphic cleanup.

The revised theorem's LSA argument is valid: the chosen boundary cut side
contains a labelled leaf by construction.  Its complement also contains a
labelled leaf, because otherwise the boundary-side descendant would have been a proper stable
ancestor of every original leaf, contradicting that the old root was the
LSA.  Each new-root child therefore has a leaf avoided by the other child, so
no proper descendant is stable for all labels.

For every reticulation switching, rerooting selects the same unrooted
displayed tree.  Uniform JC is reversible, so its Fourier monomial depends on
the unrooted edge splits.  Moving the root multiplies the two old root halves
and splits the new site.  For `0<x<1`, `x=sqrt(x)*sqrt(x)` stays in the open
cube; conversely a product of two open multipliers is open.  Inheritance
parent indexing may be complemented, which replaces `lambda` by `1-lambda`
and also stays open.

The clean census tested every all-tree endpoint from every admissible rooting
of every alternate primitive support.  There were no DAG, LSA, arrowhead,
tree-child, site-admissibility, or inverse-suppression failures.

This is an existential statement for one factor, not a simultaneous statement
for two factors.  If `R(H)` denotes the real boundary ports that are admissible
root sites and `pi` is the fixed physical port matching, the proof gives only
`R(H) != empty` and `R(H') != empty`; the atlas would need
`R(H) intersect pi^{-1}(R(H')) != empty` to fix the same physical incoming
label.  That implication is false.  The exact counterexample in
`counterexamples/fixed_incoming_relative_role.json` uses a four-boundary
TT-nested support whose rootable roles are its structural incoming and repair
ports.  A second labelled copy puts the same physical labels on the two sink
roles, making the matched rootable sets disjoint.  Both copies have nine
admissible rootings and every one is tree-child.

## 2. Primitive cores and triangles

For one incoming factor boundary,

```text
e=t+2r-1=v+r-1,
```

so blob cycle rank is `r`.  An incoming reticulation edge cannot be a cut
edge: the two root-to-reticulation parent paths give an undirected bypass.
Thus the unique incoming cut boundary meets a tree source `S`, while a
degree-two-in-the-blob reticulation is a path sink `X` with an outgoing child
port.

Suppressing ordinary unported degree-two vertices in a biconnected subcubic
rank-two graph leaves two cubic branch vertices and three internally
disjoint paths.  With tree branches the retained event multiset is
`{S,X,X}`; with one reticulate branch it is `{S,X}`.  Directly exhausting the
case of two reticulate branches gives no reachable DAG.  Event placements and
all segment orientations produce exactly TT-nested, TT-separated, TR-nested,
and TR-separated, plus the unique rank-one cycle.

The primary five records have exactly the same canonical event keys as the
clean universe.  Their complete alternate repair families also agree with
the intrinsic all-rootings test.  The primary completion counts are
independently recovered as `831, 1983, 4155, 7909`.

Two theta triangles force path lengths `(1,1,2)` or `(1,2,2)`.  The first has
parallel branch edges.  The second is `K4-e`.  A tree-child rooting with two
reticulations would need four incoming reticulation arcs, while each of the
two nonreticulate internal vertices and the root can tail at most one; leaves
cannot be parents.  The exact complete marking/rooting census confirms zero
tree-child rootings.

## 3. Intrinsic selected strength and `red_*`

There are two different predicates:

1. ordinary `S_TC` membership of the fully `red_*`-reduced selected topology;
2. strong retention of the **same primitive core** by the selected ports.

The proposed sink-plus-repair test is false for (1) and exact for (2).  The
preserved cycle counterexample omits the unique sink, prunes the reticulation,
and leaves a two-boundary tree.  That tree has one admissible rooting and it is
tree-child, but it no longer carries the cycle core.

The atlas needs predicate (2), not predicate (1).  A source support must keep
the source core so that its labelled pointwise rigidity fixes one core map and
the probes can name directed segments.  A smaller-core selected topology,
even if intrinsically strong after reduction, cannot perform that anchoring
job.  It must remain a non-core-retaining target completion until omitted
roles are restored.

The target completion partition remains exhaustive.  Every restriction of a
full strong target determines:

- whether the target's structural incoming boundary is selected or has
  character zero;
- its original primitive core;
- the selected path-sink mask;
- the ordered selected subword on every segment; and
- at least one minimum repair contained in the full occupancy.

The corrected bounded source enumerates every such mask and word tuple and
every minimum repair.  It inserts a zero-character dummy for an omitted
structural incoming boundary, each omitted sink, and each empty segment in the
chosen repair.  Omitted ordinary port vertices have the same complete
switching-mask row as the adjacent serial edge and are absorbed by a product.
Therefore the dummy graph's selected tensor descriptor equals the actual
marginal descriptor even when the literal `red_*` graph has fewer
reticulations.  The independent census tested 12,396 restrictions in each
incoming mode, 24,792 total, and found zero mismatches; 17,304 reduced to a
strictly smaller reticulation core.

No reduced smaller-core target is discarded by the current routing logic.
Strict signature candidates remain algebraic relation candidates; equal
non-core-retaining candidates are marked `pending_support_completion`.
Every marginalized-incoming target is conservatively non-core-retaining,
because its selected ports do not carry the structural source role used to
anchor the directed primitive presentation.
What remains unproved is the finite assertion that every pending equality is
exactly the claimed cycle-source/theta-target family and that every completed
relation is separated.  The historical five-through-seven-outgoing range did
not include an omitted structural incoming role; its corrected maximum must
be recomputed.  That is an artifact gate, not a completion-partition defect.

## 4. Exact selected-parameter submersion

Fix the displayed-choice indexing and selected labels.  Each physical edge
has one complete vector of descendant masks.  Equality of these vectors is an
equivalence relation on edges, so distinct classes are disjoint.  The map to
one effective coordinate per nonzero class is

```text
y_C = product_{e in C} x_e.
```

At every point of `(0,1)^E`, the `C` row of the Jacobian is supported only on
the variables in `C` and has strictly positive entries.  The rows therefore
have full rank.  Reticulation permutations/flips append an identity or signed
permutation block `lambda -> lambda` or `1-lambda`.  Surjectivity is witnessed
by `x_e=y_C^(1/|C|)` in each class.  Positive roots are semialgebraic.

This verifies the map between **parameter cubes** used by the atlas.  It must
not be described as a minimal-coordinate map between model-image manifolds.
For example, after omitting the cycle sink, both switching columns are
identical and the inheritance coordinate is tensor-redundant.  Such
redundancy occurred in 37,400 of the 42,908 corrected completion
presentations, while the physical-to-descriptor Jacobian still had full row
rank in every case.  This census includes targets whose structural incoming
boundary is selected and targets for which it has character zero.

For arbitrary-word promotion, only the core-retaining source marginal needs
to map an open source parameter set onto an open bounded descriptor set.  A
target may be redundant or core-collapsed; no continuous target parameter
selection is required.

## 5. Rigid supports and probe coherence

Every clean alternate minimum support has pointwise stabilizer one.  An
independent re-read of all 579 primary support/probe records confirmed binary
rooted validity, LSA, tree-childness, exact narrow suppression, the arrow-tail
criterion, and pointwise automorphism count one.

Once the labelled `Q` restriction is fixed on both sides, pointwise rigidity
makes its literal core map unique.  `Q+p` then fixes the segment and anchor
side of `p`; `Q+p+q` fixes each same-segment pair order.  Pair comparisons
coming from actual total orders assemble uniquely.  Exact clean tests found
no deck collision.

The earlier triangle sentence was false.  A cycle support `Q` can be a
triangle, while adding `p` on its unsubdivided edge makes `Q+p` a four-cycle.
The revised coherence proof now uses the correct case split:

- if some extra label subdivides a support-triangle edge, its one-port probe
  has no triangle and forces literal orientation agreement;
- if no extra label subdivides any triangle edge, the same triangle persists
  in the full graph and one global ordinary `T` is allowed.

Since every strong full graph has at most one triangle and the `T` quotient of
every primary support/probe still has pointwise stabilizer one, there is no
remaining automorphism or multi-triangle mixing obstruction.

## 6. Incoming role and simultaneous-label quotient

Rootability is not a retained physical port colour.  Let `alpha` and `beta`
be assignments of all `p` physical boundary labels, including the boundary
used as structural incoming in each independently rooted presentation.
Simultaneous relabelling by `alpha^{-1}` sends the pair to

```text
(source_identity, alpha^{-1} beta).
```

Thus anchoring the source and enumerating the full target group `S_p` is
surjective.  Each relative permutation has `p!` preimages among the
`(p!)^2` simultaneous assignment pairs.  The subgroup that fixes structural
incoming has only `(p-1)!` elements and is not exhaustive.

The failure is realized, not merely set-theoretic.  Across 2,808 ordered
bijections between alternate minimal supports, 144 have no physical boundary
rootable on both sides.  In the smallest four-port witness, the source puts
physical labels `A,B` on its rootable incoming/repair roles and `C,D` on its
two nonrootable sink roles; the target copy does the reverse.  The required
relative target permutation is `[2,3,0,1]`.  It belongs to `S_4` but not the
six-element subgroup fixing position zero.

The current bounded compiler source has the correct repair: it anchors all
source boundary positions, enumerates `permutations(range(n+1))` on the
target, and records the actual physical label occupying each structural
incoming position.  If the target's structural incoming boundary is outside
the selected probe, the corrected completion source retains that real
boundary with character zero and treats all selected physical labels as
outgoing relative to the target rooting.  The 24,792-case descriptor census
verifies this two-mode partition.  The cycle/theta union compiler has not yet
adopted either change: it still uses `completions(4)` and
`permutations(range(4))`.

The claimed uniqueness does not follow from pointwise rigidity.  A setwise
graph automorphism may permute the leaf labels even when no nonidentity
automorphism fixes every label.  Exact exceptions include:

- primary theta-2 support record 208: pointwise order `1`, literal setwise
  order `2`, swapping `Q_REPAIR_0` and `Q_REPAIR_1`;
- two other canonical theta-2 base supports with literal setwise order `2`;
- the cycle and theta-0 base supports, whose setwise order rises from `1` to
  `2` after forgetting the triangle orientation in the `T` quotient.

These symmetries cause duplicate anchored representatives only once full
`S_p` is enumerated.  Pointwise rigidity remains exactly the condition needed
for a unique fixed-label core transport in the probe argument; it neither
creates a common rootable boundary nor justifies the fixed-incoming subgroup.

## 7. Minimal remaining corrections

The six previously requested mathematical wording corrections are present in
the active theorem documents and pass this review.  The remaining corrections
are:

1. Replace the `K4-e` proof's claim that only two nonreticulate tails are
   available.  An inserted root is a third possible tail, but tree-childness
   lets it tail at most one reticulation edge; three available tails still
   cannot supply four incoming reticulation arcs.
2. In the generator/local/global ledgers, distinguish a presentation's
   structural incoming role from its physical boundary label.  State that the
   target action is full `S_p`, not the subgroup fixing `INCOMING`, and include
   the exact disjoint-rootability obstruction.
3. Include marginalized-structural-incoming target completions in every
   bounded and completion-union gate.  Such records are completion tensors,
   never core-retaining topology representatives.
4. Update the cycle/theta union compiler to consume the full target action and
   both incoming modes.  The extra omitted incoming role means the historical
   at-most-seven-outgoing completion bound is not certified; the naive bound
   rises to eight and must be recomputed from the exact survivor census.
5. Regenerate all bounded relation streams and the cycle/theta union from
   source bytes containing these repairs, then require strict-sign, mutation,
   binding, and independent normalized-record checks with final hashes before
   promoting either local or global theorem.

## 8. Certificates

- `root_probe_certificate.json`: primitive/root/repair/K4 census.
- `probe_coherence_certificate.json`: alternate supports, `T`, and word decks.
- `incoming_coverage_certificate.json`: exact rootable-port sets, every support
  boundary bijection, the fixed-incoming counterexample, and the full-`S_p`
  group check.
- `parameter_submersion_certificate.json`: all completion parameter maps.
- `redstar_partition_certificate.json`: `red_*` completion coverage and route
  audit.
- `primary_artifact_audit.json`: clean read of primary artifacts and label
  quotient.
- `counterexamples/`: preserved exact boundary cases.
- `INPUTS.sha256`: exact audited repository-input hashes, with absent hard-cover
  outputs recorded as `MISSING` rather than silently ignored.
- `MANIFEST.sha256`: final byte hashes for every review artifact.
