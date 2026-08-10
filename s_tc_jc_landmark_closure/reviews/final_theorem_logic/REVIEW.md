# Adversarial review of the final theorem logic

Date: 2026-08-10

Scope: theorem promotion only.  This review does not reproduce or accept the
unfinished local atlas.  It asks whether a correctly stated, independently
reproduced fixed-full local classification would actually imply Outcome P.

## Executive verdict

**CONDITIONAL YES.**  Outcome P follows from the corrected local theorem, but
only if “corrected local theorem” means the full fixed-relation statement in
`promotion_contract.json`.  Reproducing a bounded deck census, even with no
non-`T` survivor, is not enough.

The cut, bridge, localization, root, and ordinary-`T` gates already supply a
valid local-to-global promotion.  I found no residual nonlocal or bridge-gauge
counterexample.  The old marginal-lift inference must remain forbidden.

The current repository is nevertheless **not promotion-ready**.  The local
relation stream is not independently closed, its fixed-full path bindings are
not yet release artifacts, and the historical seven-port support bound is not
valid after allowing an independently rooted target with marginalized
incoming boundary.  A safe theorem bound is twelve tensor ports: at most five
ports in a source minimal support, at most five in a target minimal support,
and two order probes.

Thus the exact referee conclusion is:

```text
independently verified full local closure contract  =>  Outcome P;
current partial local artifacts                     !=> Outcome P.
```

No counterexample to Outcome P was found in this logic audit.

## Dependency verdicts

### 1. Fixed-full relation and finite unions — verified after correction

Fix the two complete labelled local factors before selecting any marginal.
Also fix one admissible incoming presentation of each factor and one minimum
target repair.  These choices may use different physical incoming labels.
They define one full decorated relation.

The global containment supplies one source-open set of complete tensors.  If
a finite presentation cover is used, semialgebraic dimension yields a member
containing a source-open **subgerm**, never the whole source germ.  Pull that
subgerm back to the already fixed full source relation and only then form all
larger prefix marginals.  Every prefix is therefore a direct marginal of the
same full containment.

It is false to start from containment of `Q` alone and infer containment of
`Q union D`.  The exact counterexample preserved by the hard-cover review is
decisive.  Any compiler record lacking a full-relation id, a parent-prefix id,
and a restored physical-label map is insufficient evidence for promotion.

In fact, after the verified root reduction, the mathematical proof can avoid
the finite-union ambiguity altogether: choose fixed admissible rootings of the
two full factors.  Full target `S_p` enumeration is still mandatory in the
certificate because the two chosen incoming labels need not coincide.

### 2. Marginal submersion — verified with one missing sentence supplied

The reviewed product map from physical edge multipliers to selected effective
edge variables is onto and has full differential throughout the positive
cube.  That parameter statement alone is not yet the model-image statement
needed by the proof.

Let `rho` be that product map and `psi` the selected descriptor-to-tensor map.
The selected image has a dense regular parameter locus on which `psi` has its
generic rank.  A source-open full tensor germ pulls back to a parameter-open
set.  Intersect it with `rho^{-1}` of the regular locus.  The submersion
theorem makes `rho` open there, and the constant-rank theorem makes `psi` open
onto the selected model manifold.  Hence every fixed prefix marginal contains
a source-relative open selected-model subgerm.  This proves exactly the
required marginal-submersion lemma without asserting that descriptor
coordinates are minimal.

### 3. Coherent support and port orders — conditionally verified, old bound rejected

The clean review proves pointwise rigidity and the one- and two-port order
lemma once both restricted factors share a core-retaining rigid support.  A
nonretaining target marginal does not initially satisfy that premise.

For one fixed full relation choose a source minimal support `Q_s` and a target
minimal support `Q_t`, each including the incoming boundary of its own rooted
presentation.  Restore every label of `Q_t minus Q_s` along the actual
fixed-full path.  If the hard cover does not separate that path, its terminal
relation identifies

```text
A = Q_s union Q_t
```

modulo ordinary `T`.  The set `A` is core-retaining and pointwise rigid on
both sides because it contains a rigid minimal support of each.  Every later
`A+p` and `A+p+q` identification restricts to the same map on `A`; pointwise
rigidity forbids probe-dependent transports.  Pair comparisons therefore
assemble to one total order on every segment.  The existing triangle case
split makes the `T` choice coherent.

The support table gives at most five tensor ports per minimal support
(incoming plus outgoing support).  Therefore

```text
|A| <= 10,       |A union {p,q}| <= 12.
```

This is a safe universal bound.  The historical seven-port statement cannot
be used after the fixed-IN correction.  A smaller optimized bound would need
a new proof; it is not needed for finiteness.

#### Proposed seven-port refinement — rejected as a uniform argument

From `H|A` and `H'|A` being **literally isomorphic**, restriction to the same
labelled subset `Q_s` does commute with that isomorphism.  In that branch the
target `Q_s` is core-retaining and the historical at-most-seven tensor-port
`Q_s+p/q` probes are enough.

The implication fails for a nontrivial `T` terminal.  Ordinary `T` preserves
the underlying pendant placements, but changes which triangle vertex is the
reticulation and hence which incident boundary is its sink.  Ancestral
restriction to `Q_s` can retain the source reticulation while deleting the
target sink and pruning the target reticulation.  Thus restriction and the
`T` quotient do not commute.  This is exactly the semantic content of a
non-core-retaining target completion; adding `Q_t` makes the target core
visible on `A` but does not retroactively change `H'|Q_s`.

Nor may the proof redirect `H'` first.  The separate ordinary-`T` theorem
supplies one common regular germ, not equality of complete stochastic images.
It gives no right to move the particular target realizations witnessing the
original containment to the redirected orientation.  Without the target core
on `Q_s`, pointwise rigidity there supplies no target core map whose
restriction must agree with the map on `A`.

Therefore seven tensor ports are valid only if the terminal is literal
isomorphism, or if the certificate independently proves that `Q_s` retains
the actual target orientation.  For nontrivial-`T`, target-nonretaining paths,
the safe proof must retain `A` (equivalently, restore `Q_t`) in every `p/q`
probe.  The uniform bound remains twelve unless the final census proves that
this branch is empty and binds that fact relation by relation.

The final local certificate must bind the base restoration and every `p/q`
probe to the same full relation and the same `Q_t`.  A census of canonical
states with those paths deduplicated away does not prove coherence.

#### Audit of the proposed terminal-extension compiler — accepted with exact conditions

Extending each allowed **raw path-bound** terminal on `A` is an exact finite
implementation of the preceding proof.  Insert a new fixed label `p` at a
subdivision of every admissible internal blob arc on each side; retain only
locked standard-strong children and regenerate their complete graph-to-algebra
records.  From each allowed child, repeat with `q`.  Every child record must
prove that deleting the new label returns the exact parent relation and must
carry the same restoration root, parent path, `Q_t`, and raw transports.

This is exhaustive because `A` already contains every source/target sink,
both chosen incoming boundaries, and a complete repair on both sides.  Every
remaining boundary is an ordinary subdivision port.  Inserting it on every
internal arc of the reduced terminal graph enumerates every interval between
anchors; sequential insertion of `q` enumerates both pair orders.  It is
therefore unnecessary to rerun factorial full-target-`S_p` completion
enumeration at outgoing sizes five and six.  Canonical graph/algebra states
may be shared only after the raw parent-child relations and transports are
stored.

This extension does **not** close the unequal-signature base gate.  The active
screens contain 110 and 776 unequal-but-necessary directed signature pairs at
outgoing sizes three and four.  Equal-signature restoration classifies none
of them.  Every decorated presentation relation represented by those pairs
still needs a graph-derived exact polynomial/sign or rank certificate.  The
active tree contains no `primary/certificates/bounded_relations_n*.jsonl.gz`
stream, so that mandatory gate remains unresolved.

There is a separate mandatory size-four source gate.  The support universe has
nine minimal records in total, distributed `1,5,3` over outgoing sizes
`2,3,4`.  The three size-four records are theta-2 supports.  No deletion of one
of their outgoing labels retains both source sinks and a complete two-segment
repair, so none satisfies the source hypothesis of the n=3 fixed-full theorem.
The n=3 hard cover cannot discharge them.  See `N4_SUPPORT_GATE.md` and its
exact 12-deletion replay.

#### Explicit arbitrary-word audit

This does cover every arbitrary source word, provided the bound relation
certificate has the stated path bindings.  Write an arbitrary source word on
each directed segment as the ordered concatenation of:

1. labels in `A`;
2. one additional label `p`; and
3. each pair `p,q` of labels not in `A` that lie on the same segment.

The `A+p` terminal relation fixes the target segment and the interval between
consecutive anchor labels containing `p`.  The `A+p+q` terminal relation fixes
the order of `p,q` whenever they occupy that same interval.  Every finite set
equipped with all pair comparisons inherited from a total order has one total
order; comparisons in different intervals or segments are irrelevant.  Thus
the probes recover the entire word, not merely its support or its multiset of
ports.  Every occupied repair segment required by the fixed source and target
supports is represented by its restored role; optional empty segments remain
explicit core edges and need no dummy.  Path-sink ports are in the minimal
supports, so there is no omitted vertex type.

This conclusion would fail if the compiler were allowed to choose a new
target support, a new full relation, or a new transport independently for
each probe.  Those are precisely the bindings required by the promotion
contract.

#### What terminal `T` does and does not prove

At the restored support or probe terminal, equality of labelled standard
mixed-graph codes after forgetting only the triangle arrowheads proves the
topological necessity statement: the compared restriction is isomorphic or
ordinary-`T`-related.  It supplies no stochastic parameter map.  Conversely,
the separate verified local ordinary-`T` certificate supplies a common
full-dimensional regular projective germ and arbitrary port grafting.  The
terminal code and the local germ are therefore complementary gates:

```text
terminal T-quotient code  -> necessity/topology;
verified local T germ     -> stochastic converse.
```

Neither gate can replace the other.

### 4. Root reduction — verified, with disjoint incoming labels allowed

The all-tree path argument, exact root suppression, LSA condition, retained
arrowheads, JC reversibility, and open multiplier splitting passed independent
review.  It gives each root factor some real incoming boundary.  It does not
give a boundary rootable on both factors.  The latter statement is false.

This is not a global obstruction.  Root the two factors independently and let
the corrected local relation carry the full physical port matching together
with both structural incoming roles.  Full target `S_p` and the
zero-character marginalized-incoming mode are therefore logical necessities,
not implementation options.

One incoming-boundary draft had a preserved implementation bug: it included
boundary leaves in the universal tree-child test, so a leaf with no child made
otherwise valid rootings fail.  The corrected census for the minimal
disjoint-incoming TT-nested witness is `(9,9)`—nine admissible rootings and
nine tree-child rootings—on each side.  This agrees with the committed clean
root/probe review.  The earlier proposed ordinary-`T` no-common-incoming
witness is also withdrawn because both sides share a physical incoming
boundary.  Neither erroneous datum is used here.

### 5. One-sided cut preservation — verified in both directions

The pointwise theorem says, at every open JC point, that a split is a cut if
and only if its Fourier flattening has rank at most four.  On a source-open
common set, a source cut and target noncut would require the same matrix to
have ranks at most four and at least five.  The same contradiction with the
roles reversed proves target-cut implies source-cut; it does not reverse the
one-sided relation.  Hence the complete labelled cut sets and reduced bridge
trees agree.

### 6. Full-incidence bridge quotient and local slices — verified

The exact positive contraction fiber is the full incidence action

```text
P_u -> a_(u,e) P_u,
P_v -> a_(v,e) P_v,
x_e -> x_e/(a_(u,e) a_(v,e)).
```

The reciprocal-only chart and physical bridge recovery are false.  Positive
anchors give local analytic slices on every retained component, and the
reduced bridge graph is a tree, so there is no scaling holonomy.  The
observable edge coordinate is an effective normalized scale.

### 7. No cross-blob compensation — verified

After cut equality, bridge peeling is an intrinsic analytic function of the
distribution.  A source product box projects openly onto each focal
projective local germ.  Every target realization of the same distribution has
the same extracted focal orbit by the exact bridge fiber.  Distant target
parameters therefore cannot change or cancel a projective local separator.
No continuous target-parameter choice is used.

### 8. Simultaneous ordinary-`T` gluing — verified conditionally

The ordinary triangle certificate supplies a port-labelled common regular
projective germ, not equality of complete open images.  Choose local common
slice points independently.  For each bridge choose an effective scale in a
sufficiently small interval so that both physical realizations remain in
`(0,1)`.  The bridge tree has no cycle and different factors use disjoint
parameters, so all choices glue simultaneously and dimensions add.

This proves the converse required for `preceq_JC` and `bowtie_JC`.  It does
not prove that every orientation in a `T` orbit realizes any fixed generic
distribution.

### 9. Exceptional locus — exact conditional construction

For fixed leaf set there are finitely many locked standard-strong binary
level-2 topologies.  Indeed tree-child paths give `r<=n-1`; binary degree
counting gives `t=n+r-2`, hence at most `4n-3` rooted vertices before standard
reduction.  For one topology `N`, let `V_N` be its irreducible complex model
closure (the closure of a polynomial image of an irreducible parameter
space), and define

```text
E_top(N) = union over N' not T-equivalent to N of
           ZariskiClosure(M_N intersect M_N') inside V_N.
```

If the local closure contract holds, every member is proper.  Otherwise a
semialgebraic intersection with Zariski closure `V_N` would have full real
dimension and hence relative interior in the regular source manifold, giving
`N preceq_JC N'`, contrary to the classification.  The finite union is thus a
proper algebraic subset.

For the reconstruction theorem enlarge it by the singular locus and the
closures of generic-rank critical values.  A release-computable, possibly
larger exceptional set is obtained by multiplying the graph-bound nonzero
source witnesses and chosen nonzero Jacobian minors emitted by the final local
certificate.  Irreducibility makes this finite product nonzero.  Strict-sign
and cut-mismatch cases add no stochastic common points.

This locus is precise but not claimed minimal.  The final release must publish
the transported witness factors and minors; a verbal reference to “generic
parameters” is not enough.

## Correct theorem that follows after local closure

Once the unresolved local contract is independently verified, the following
is proved:

> For locked binary standard semi-directed `S_TC` level-2 topologies `N,N'`,
> `N preceq_JC N'` if and only if their labelled bridge trees agree and every
> pair of corresponding nontrivial factors is labelled-isomorphic or differs
> by ordinary triangle redirection `T`.  Therefore no proper one-sided generic
> containment exists, and `N bowtie_JC N'` holds exactly for the same
> `T`-generated relation.

Together with the frozen all-`n` theorem in `W_TC minus S_TC`, this is Outcome
P and gives the claimed sharp boundary.

## Reconstruction consequence and one necessary correction

Outside the proper exceptional locus, exact data determine the labelled
bridge tree and one canonical `T`-quotient representative of every factor.
Bridge peeling recovers projective local tensors, the final local atlas
identifies each common anchor, and coherent probes recover all port words.

The algorithm may enumerate candidate cut splits and then use only bounded
local relation tests.  This is structural and terminating.  I do not accept
the draft's `O(n^7)` claim without a separate polynomial cut-listing proof and
an explicit arithmetic-input model.

The output is the canonical topology **modulo `T`**.  To list the orientations
that realize one particular distribution, test stochastic membership for the
finitely many `T` variants.  The common-germ theorem does not imply that all
variants realize every generic point.

## Release blockers

Only one load-bearing local-closure dependency remains, but it has several
substantial subgates:

1. independently regenerate every fixed-full local decorated relation under
   full target `S_p` and both incoming modes;
2. include the mandatory theta-2 n=4 minimal-support hard cover; n=3 is not a
   reduction of this case;
3. close every decorated relation represented by the 110/776 unequal
   necessary directed signature pairs with graph-bound exact witnesses;
4. bind every hard-cover and `p/q` path to one full relation and one common
   anchor;
5. close every mixed-sign or rank terminal exactly;
6. compare complete normalized primary and independent streams;
7. reject relation deletion, transport swaps, separator swaps, incoming-role
   changes, path deduplication, and source/target reversal mutations;
8. emit the witness/minor product used for the exceptional locus.

Until those items pass, the correct status is **UNRESOLVED**, not Outcome P.
