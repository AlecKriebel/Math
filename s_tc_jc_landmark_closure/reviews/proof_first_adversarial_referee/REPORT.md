# Proof-first adversarial referee report

Date: 2026-08-12

Repository commit reviewed: `f29b6057`

Scope: the locked `sd_0` standard-strong class, open JC parameter domain,
projective bridge/cut/root reductions, primitive cycle/theta cores, bounded
local theorem, and arbitrary-subdivision promotion.  I used conceptual graph
and tensor arguments and tiny exact checks only.  I did not run or extend a
large topology census.

## Executive verdict

**No exact counterexample to the desired standard-strong theorem was found.**
The bridge, cut, root, and arbitrary-subdivision arguments survive the attacks
below after their already-recorded corrections.  In particular, I found no
way for a distant blob or a bridge scale to compensate for a genuinely
different projective local tensor.

However, the current proof tree does **not yet justify promotion of Outcome
P from the prose documents alone**.  The remaining mathematical hinge is the
fixed-full directed local theorem: every projective one-sided containment
between minimal standard-strong cycle/theta factors must be labelled
isomorphism or ordinary triangle redirection.  The active local theorem still
states this as a candidate, and the independent relation reviews explicitly
condition their conclusions on frozen root inventories rather than deriving
the complete source-target relation universe from first principles.

Thus my adversarial conclusion is:

> **THEOREM PLAUSIBLE; NO COUNTEREXAMPLE; LOCAL NECESSITY STILL REQUIRES ONE
> CLOSED PROOF OR END-TO-END INDEPENDENT CERTIFICATE.**

This is not evidence for Outcome C.  It is a release blocker for claiming
Outcome P before the local core-recognition implication is made
self-contained.

## Inputs locked for this review

| file | SHA-256 |
|---|---|
| `docs/DEFINITIONS_LOCK.md` | `3108a20e924a37b069cc4aeb53b051b03463176eafce9d590dfec378e2ad16a2` |
| `docs/GENERATOR_AND_SUPPORT_THEOREM.md` | `a6b195d158972ba842c7995ddf97898272db533d8505f5fbb4299f1a296f79e9` |
| `docs/LOCAL_ATLAS_THEOREM.md` | `34b8eccfa16100f6b25ccbca68320387d339c2264d78ba0eea61ceaa115cf217` |
| `docs/ROOT_REDUCTION_THEOREM.md` | `720f4b63f2a88ce4d4b8247b856a6f0b7f9939494e342915747c86e0173eb836` |
| `docs/TRIANGLE_MOVE_LOCK.md` | `59f832bbd7499e6e53066b8a05f5ef6bba5c170f9544c32c0808440b8bcab451` |
| `docs/GLOBAL_THEOREM_DRAFT.md` | `618361383f5123127147ffbf4efca74be490453298b0e0b59fa6dbd7ef9024e5` |
| `reviews/global_bridge/REVIEW.md` | `f6a9a608e841796d98999dfa639716c091cdcef8d1895b85c7f7597023fa05db` |
| `reviews/root_probe/REVIEW.md` | `dd6e6cd380791108390b20960e23bb0a5bd7b0539b81b54046fc2203900a0108` |
| `reviews/final_theorem_logic/REVIEW.md` | `246ecdb1570a272303adf45751aaa00e8289e15d3de921ac432a0ec1e16e7f0f` |
| `reviews/arbitrary_subdivision_promotion_referee/THEOREM_AND_PROOF.md` | `4a5c4f474df719f07bbf46b4d1e65c876f49765962883d7ea7de3f8ad5469f37` |
| `reviews/base_gate_adversarial_referee_n3/REVIEW.md` | `71ff1a9347726ab83628f60dd47377d2580e9f3b580369cc5ae2e4c9dbc0e191` |
| `reviews/base_gate_adversarial_referee/REVIEW.md` | `0596be556015cce577e286d2177403ca8c5d04f8022ccc75f070add621613f77` |
| `reviews/bounded_directed_relation_cleanroom/REVIEW.md` | `629983a516b17a2fa98c22e175efa68a418ff6e8b8ec65e7210e0f0310e40af5` |
| `primary/certificates/core_universe.json` | `f7ebe0b0ebc93f58cfa5bc2086f55a518b0ce8774da57667fe4c1f169ff39e10` |

## Proved objections and required corrections

### 1. The fixed-full local implication is still the only load-bearing gap

The global necessity argument reduces a global containment to a projective
source-relative containment of one corresponding local factor.  The
arbitrary-subdivision theorem then reduces an arbitrary word to a fixed-full
minimal-support relation plus one- and two-port probes.  Neither statement
classifies the fixed-full relation itself.

The n=3 and theta-2 n=4 base reviews are strong exact audits, but each states
an explicit reliance boundary: the review is conditional on a frozen root
inventory.  The bounded directed-relation clean-room report says that its
combined gate is unresolved.  What is still needed is one of the following:

1. a proof-first local core-recognition theorem covering the five primitive
   families and both containment directions; or
2. an independent derivation proving that every full target permutation,
   independently chosen incoming role, selected/marginalized incoming mode,
   sink mask, repair choice, and source-to-target port transport occurs in
   exactly one audited fixed-full relation.

Checking the algebra of every stored relation is not a proof that no relation
was omitted.  Conversely, the structural completion grammar proves
surjectivity only after it is explicitly bound to the frozen inventories.

This is a proof-completeness objection, not a counterexample to the theorem.

### 2. The written `K4-e` tail count omits the inserted root

The double-triangle conclusion is correct, but the proof in
`GENERATOR_AND_SUPPORT_THEOREM.md` says that four incoming reticulation arcs
would require four distinct nonreticulate tails while the graph has only two
nonreticulate vertices.  In an admissible rooted presentation the inserted
root can also be the tail of one reticulation edge.

The corrected argument is still immediate.  Strong tree-childness permits
each ordinary internal vertex and the root to have at most one reticulation
child, while a reticulation cannot tail an edge entering another
reticulation.  `K4-e` has two ordinary internal vertices, so there are at most
three possible tails (the two ordinary vertices and the root), fewer than the
four incoming reticulation arcs required by two reticulations.  Hence no
tree-child admissible rooting exists.

Status: **proof wording false; theorem conclusion repaired**.

### 3. Root reduction is existential on each side, not a common-port theorem

The all-tree-path rerooting proof is sound.  It supplies at least one real
incoming boundary for each factor separately.  It does not supply a single
physical boundary that is rootable on both source and target.

The exact four-boundary TT-nested fixture at
`reviews/root_probe/counterexamples/fixed_incoming_relative_role.json`
(SHA-256
`72e9c8a8d031dbc583473ee5b193b1516cff3cf7b2acbcdfd5fab899b9da209e`)
has disjoint source and target rootable physical-label sets.  Therefore the
final local statement must carry:

- the source incoming role;
- the target incoming role, possibly on a different physical label; and
- the complete physical port matching.

The full target symmetric-group action and the zero-character marginalized
incoming mode are mathematically necessary.  Any proof that silently fixes a
common incoming label is false.  The corrected compiler design accounts for
this, but the final theorem statement should say it explicitly.

### 4. A common `T` germ does not list all compatible orientations at each
generic distribution

The ordinary triangle certificate proves a common full-dimensional regular
germ.  It does not prove equality of complete open stochastic images.  In
general, two same-dimensional semialgebraic images may share an open set and
still each have another open region not contained in the other.

Consequently, the last sentence of `GLOBAL_THEOREM_DRAFT.md`, which says the
complete compatible topology set is exactly the finite set of coherent
`T` variants, is too strong if read pointwise.  The valid reconstruction
output is the canonical topology **modulo `T`**.  To list the orientations
realizing a particular distribution, stochastic membership must be tested
orientation by orientation.

This does not weaken identifiability modulo `T`; it prevents an unsupported
pointwise multiplicity claim.

### 5. A triangle-bearing theta is not a bridge decomposition of a sunlet
and a triangle-free factor

There is no proof-first shortcut that simply applies a level-1 triangle
theorem to the triangle and a triangle-free level-2 theorem to the remaining
path.  In a theta graph the third path joins the same two branch vertices as
the two paths forming the triangle.  The triangle and the remaining path are
not separated by a cut edge, and bridge peeling does not produce their two
tensors independently.

One may cut the three external incidences of the triangle and view it as a
three-port tensor; this is enough for the **converse** ordinary-`T` move.
It is not an inverse factorization that recognizes every triangle-bearing
theta topology from data.  The necessity direction still needs a direct
local tensor invariant/core-recognition argument.

Status: **invalid shortcut excluded; current draft does not rely on it**.

## Load-bearing arguments that survived

### Incidence gauge

The withdrawn reciprocal-only bridge chart is indeed false, while the full
incidence action explains the standard regression exactly:

```text
(1/2)(1/2)(1/2) = 1/8,
(3/5)(3/5)(25/72) = 1/8.
```

Taking the two endpoint incidence scales to be `6/5` sends

```text
1/2 -> (1/2)/((6/5)(6/5)) = 25/72.
```

This is a two-sided incidence rescaling, not a reciprocal-only action.  The
exact positive rank-one fiber argument and the absence of degree-two
unmarked retained components leave no gauge that can circulate around the
bridge tree.

### One-sided cut preservation

The two inclusions use different equations but are both valid.  A source cut
and target noncut contradict the pointwise target rank lower bound.  A target
cut and source noncut contradict the same rank lower bound on the source,
because the target cut minors vanish on every common source point.  No
reversal of the one-sided relation is assumed.

### No cross-blob compensation

After the bridge tree is fixed, projective peeling is an intrinsic function
of the observed distribution.  A target preimage need not vary continuously:
every preimage has the same extracted projective factor orbit.  Hence a
distant target factor cannot cancel a polynomial or strict-sign separator at
the focal factor.

### Root rerouting

Reversing the all-ordinary path from the old root to a leaf-bearing cut side
preserves reticulation arrowheads and cannot create a directed cycle: a
re-entry into a path tree vertex would either provide a second parent or
already form an old directed cycle.  The two new root sides each contain a
leaf inaccessible from the other side, so the new root is again the LSA.
JC reversibility and positive edge splitting preserve the boundary tensor
germ.  The only required correction is the independent-incoming-role
quantifier above.

### Marginal submersion and word reconstruction

For every nonempty serial class, the product coordinate has nonzero
differential on the open cube.  Because the classes use disjoint edge sets,
the physical-to-effective map is submersive.  At a generic regular source
point this descends a source-open containment to the selected marginal in
the correct direction without choosing target parameters continuously.

Once the exact union anchor `A=Q_s union Q_t` and one transport are fixed,
one-port probes locate every extra label and two-port probes determine all
same-interval pair orders.  Those comparisons come from actual total words,
so there is no transitivity gap.  I found no conceptual counterexample to the
corrected promotion theorem.

## Targeted counterexample search

I tested only structurally dangerous small configurations:

1. the two-sided bridge-scale regression above;
2. the `K4-e` two-triangle core, including the omitted-root tail;
3. independently rootable but physically disjoint incoming roles on a
   minimal TT-nested support;
4. a triangle inside a theta whose third path reconnects both triangle branch
   vertices;
5. a source-open containment against a target cut equation in both cut-set
   directions;
6. probe insertion on an edge of the unique triangle, which destroys the
   triangle and therefore forces literal orientation agreement.

None yields a standard-strong open-JC counterexample.  No counterexample
verifier is included because no exact counterexample was found.

## Speculative risks, not established objections

1. A proper one-sided containment between two different minimal theta
   orientations remains the most plausible place for a surprise.  Dimension
   counting cannot rule it out when the target model has equal or larger
   dimension.  It must be excluded by an identity or a strict open-cube sign.
2. Cycle-to-theta containment after a target marginal drops a sink or repair
   role is dangerous unless the omitted role is restored within the same
   fixed-full relation.  A common selected invariant deck is not evidence of
   containment.
3. A proof-first local theorem should not infer topology from the target
   mixed-graph hash alone.  It must retain the directed source-target port
   relation and independently chosen incoming roles.
4. The proper algebraic exceptional locus is valid conditionally, but the
   promised release-computable witness/minor product has not been emitted in
   the reviewed proof ledger.

These are reasons to demand the final local proof, not evidence that the
headline theorem is false.

## Minimal proof-first closure recommendation

The least risky route is a five-family **local core-recognition lemma**:

> On the minimal rigid support of each of the cycle, TT-nested,
> TT-separated, TR-nested, and TR-separated cores, the projective JC tensor
> determines the labelled core, incoming role, sink roles, and repair roles,
> modulo ordinary redirection of the unique triangle.  In both directed
> containment orientations, every unequal core/role relation is excluded by
> a graph-derived identity or a strict open-cube inequality.

This lemma should be proved family-by-family from explicit trinet/quartet
coordinates, not by another large topology search.  Once it is established,
the already-corrected full target-role grammar supplies the finite role
quantifiers, and the verified arbitrary-subdivision theorem recovers every
port word.  The bridge/cut/root/global arguments then give Outcome P.

Until that lemma or an equivalent end-to-end independent relation-universe
certificate is present, the mathematically honest release status is:

```text
no S_TC counterexample found;
global theorem conditional on fixed-full local core recognition;
Outcome P not yet promoted.
```
