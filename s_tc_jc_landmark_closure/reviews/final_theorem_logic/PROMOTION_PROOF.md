# Conditional promotion proof for Outcome P

This note records the exact theorem implication established by the referee
audit.  Its single unproved hypothesis is the local closure theorem `L` below.

## Local closure hypothesis L

For any two fixed full labelled nontrivial local factors `H,H'` induced by
locked standard semi-directed `S_TC` level-2 topologies on the same boundary
set, choose admissible incoming presentations independently.  If a
source-relative open regular germ of the projective JC model of `H` lies in
the projective JC image of `H'`, then `H,H'` are labelled-isomorphic modulo
ordinary triangle redirection `T`.

The certificate for `L` must satisfy `promotion_contract.json`.  In
particular, `L` is a fixed-full theorem for arbitrary subdivision words, not a
statement inferred from one selected marginal.

The equal-signature restoration cover is only one part of `L`.  The current
three- and four-outgoing screens also contain respectively 110 and 776
unequal-but-necessary directed signature pairs.  Every decorated relation
represented by those pairs requires its own regenerated graph-bound exact
polynomial/sign or rank certificate.  Equal-signature terminal closure says
nothing about them.

## Lemma 1 — selected-prefix openness

Let `U` be a source-open germ in the full projective local model of `H`, and
let `Y` be any fixed boundary subset.  Assume `Y` retains the selected source
descriptor used in a relation path.  Then, after shrinking `U`, its `Y`
marginal contains a relative-open germ in the selected source model.

### Proof

On physical source parameters the restriction factors as

```text
full parameters --rho_Y--> effective selected parameters --psi_Y--> tensor.
```

The fibers of `rho_Y` are disjoint serial edge classes; every coordinate is a
positive product.  Its Jacobian has disjoint nonzero rows and is therefore a
submersion throughout the open cube.  The polynomial map `psi_Y` has a dense
regular locus of its generic rank.  Pull `U` back to a parameter-open set and
intersect with the inverse image of that regular locus.  The submersion and
constant-rank theorems show that the composite image contains a relative-open
selected-model germ.  No minimality of effective parameters is asserted.

## Lemma 2 — fixed-full restoration

Fix source and target minimal rigid supports `Q_s,Q_t` for their independently
chosen incoming presentations.  Every label in `Q_t minus Q_s` is a real
boundary label of the same full relation.  On the source it is either already
selected or lies at one definite position of one ordinary segment.  Every
prefix marginal is taken directly from the original full containment, so
Lemma 1 applies at every prefix.

The actual full relation therefore follows one path in any restoration tree
that inserts every missing target role into all source positions.  A
target-identity/source-nonzero polynomial excludes a source-open containment;
a source-identity/strictly-signed-target polynomial excludes even a common
open point.  If all non-`T` paths are so certified, the actual path terminates
in labelled isomorphism modulo `T` on `A=Q_s union Q_t`.

This argument never lifts containment from the preceding marginal.

## Lemma 3 — common-anchor coherence

The union `A=Q_s union Q_t` is core-retaining and pointwise rigid on both
sides: an automorphism fixing `A` fixes the rigid subset belonging to that
side.  It has at most ten tensor ports.  For every remaining label `p`, extend
the exact path-bound terminal relation on `A` by inserting `p` on every
admissible internal blob arc of the source and target rooted graphs.  For
every allowed `A+p` child, do the same with `q`.  Recompute each decorated
relation from graph to switching masks, tensor, pullbacks, signs, and ranks.
Deleting the new label must recover the exact parent relation, including its
restoration root, parent path, `Q_t`, and raw transport.  The resulting
terminal sets are `A+p` and `A+p+q`, of size at most eleven and twelve.

Every terminal labelled isomorphism restricts to the unique map on `A`.
Thus all one-port probes assign the same segment to each label and all
two-port probes give compatible pair orders.  These are restrictions of the
actual source and target total words, so they assemble uniquely.  If a probe
subdivides a triangle edge it forces literal orientation; otherwise the
unique triangle persists and one ordinary `T` choice is coherent.  Hence the
full ported factors are isomorphic modulo `T`.

To see that no arbitrary source word is missed, partition the nonanchor labels
by source segment and by the open intervals between consecutive anchor labels.
An `A+p` probe determines the part containing `p`.  For every pair in one
part, `A+p+q` determines its comparison.  These comparisons are inherited
from the actual source total order and, at every allowed terminal, from the
actual target total order.  They therefore define one identical finite total
order on that part.  Taking all parts reconstructs every complete word.
No new target support or graph transport may be chosen between probes.

This terminal-extension construction is exhaustive.  Once `A` contains both
minimal supports, every reticulation sink, both structural incoming
boundaries, and the selected source/target repairs are already present.
Every remaining boundary is therefore an ordinary port at one subdivision
vertex of an internal blob arc.  Restriction to `A+p` suppresses all other
ordinary subdivisions, so reinserting `p` on every internal arc gives every
possible marginal exactly.  Sequential insertion of `q` gives both orders on
every shared interval.  Because `A` is fixed and pointwise rigid, no full
boundary permutation remains to enumerate.

One cannot generally replace `A+p/q` by `Q_s+p/q` after a terminal ordinary
`T`.  Literal isomorphism commutes with restriction, but nontrivial triangle
redirection need not: it changes the reticulation sink, so deleting
`A minus Q_s` can prune the target reticulation while retaining the source
one.  The local `T` common-germ theorem is not complete-image equality and
cannot move the original containment to a reoriented target.  The smaller
probe is justified only on terminals where the actual target `Q_s` is
independently core-retaining.

Lemmas 1--3 explain the arbitrary-subdivision content required of `L` and the
safe twelve-port theorem object.

The n=3 hard cover does not cover every `Q_s` in Lemma 2.  Theta-2 has three
canonical minimal supports with four outgoing labels: two sinks and two repair
labels.  Removing a sink loses sink completeness; removing a repair leaves no
two-segment minimum repair.  Hence no three-outgoing restriction retains the
source theta-2 core, and the fixed-full theorem cannot be applied there.  The
local hypothesis `L` must include a genuine n=4 theta-2 hard cover.  The
path-bound terminal extension above then supplies the `+1/+2` probes directly;
factorial full-`S_p` completion enumeration at outgoing sizes five and six is
not required.

## Lemma 4 — equality of bridge trees under one-sided containment

Let `N preceq_JC N'` with witness source-open set `U`.  The pointwise cut
theorem states that a split has Fourier flattening rank at most four exactly
when it is a cut, at every open parameter point.

If a source cut were a target noncut, a common distribution in `U` would have
rank both at most four and at least five.  If a target cut were a source
noncut, the same contradiction follows with the cut equation pulled back to
the source-open set.  Therefore the cut sets, and hence the reduced labelled
bridge trees, agree.

## Lemma 5 — localization

On the common bridge tree, the exact contraction kernel is the full positive
incidence-scaling action.  Positive anchors give analytic slices and one
effective scale per bridge.  Intrinsic peeling identifies the global source
germ locally with

```text
product(projective local source germs) x product(effective bridge intervals).
```

Shrink the containment witness to a product box.  Vary one local source
coordinate while fixing all others.  Every resulting distribution lies in
the target image, and every target factorization has the same intrinsically
extracted focal projective orbit.  The focal source box therefore lies in the
target focal projective image.  Apply root reduction where one side is the
root factor; independently chosen incoming labels are allowed by `L`.

No target preimage is selected continuously and no distant component can
compensate for the focal orbit.

## Theorem 6 — necessity

Under `L`, if `N preceq_JC N'`, Lemma 4 gives the same labelled bridge tree.
Lemma 5 gives a source-relative projective local containment at each
corresponding nontrivial factor.  Hypothesis `L` makes each pair
labelled-isomorphic modulo ordinary `T`.  Ordinary tree components are already
fixed by the bridge tree.  This proves the necessary direction.

## Lemma 7 — simultaneous converse gluing

For an isomorphic local pair use the same projective germ.  For a `T` pair use
the independently verified port-labelled common full-dimensional regular
germ.  Shrink all finitely many local germs so that both incidence
representatives stay positive and bounded.

For a bridge `e=uv`, let the two endpoint incidence factors in realization
`k` be `a_(u,e)^k,a_(v,e)^k`.  Choose a common effective scale

```text
0 < z_e < min_k a_(u,e)^k a_(v,e)^k.
```

Then `x_e^k=z_e/(a_(u,e)^k a_(v,e)^k)` lies in `(0,1)` for both realizations.
The bridge graph is a tree, so all bridge choices are independent.  The
analytic extraction inverse proves that the glued common set has full global
dimension and contains points regular for both models.

The terminal `T`-quotient code used in Lemmas 2--3 proves only the allowed
topological relation.  The independently verified local `T` germ used here is
the distinct stochastic input.  No equality of complete local images is
inferred from the terminal code.

## Theorem 8 — classification

Under `L`,

```text
N preceq_JC N'
iff
the labelled bridge trees agree and corresponding factors are
labelled-isomorphic or ordinary-T-related.
```

The right side is symmetric and Lemma 7 supplies a common full-dimensional
regular germ in both directions.  Hence there are no proper one-sided generic
containments, and the same condition classifies `bowtie_JC`.

## Corollary 9 — proper algebraic exceptional set

Fix `N` and the taxon set.  Tree-child paths give `r<=n-1`; with
`t=n+r-2`, a rooted binary presentation has at most `4n-3` vertices.  There
are therefore finitely many locked binary standard-strong level-2 topologies
on that set.  The complex closure `V_N` is irreducible because it is the
closure of the polynomial image of an irreducible parameter space.  For every non-`T` topology
`N'`, the semialgebraic intersection `M_N intersect M_N'` has dimension less
than `dim M_N`; otherwise it would contain source-relative interior and give
`N preceq_JC N'`.  Its Zariski closure inside the irreducible variety `V_N` is
therefore proper.  Their finite union is a proper algebraic set `E_top(N)`.

Adjoin the singular locus and generic-rank critical-value closures to obtain
`E_rec(N)`.  Outside it, exact data determine one canonical standard
semi-directed topology modulo `T`.  The final local certificate can emit an
explicit nonzero witness/minor product whose zero set is a release-computable
overapproximation of `E_rec(N)`.

## Corollary 10 — sharp boundary

The frozen weak-class theorem supplies, for every `n>=4`, a nonisomorphic
non-`T` pair in `W_TC minus S_TC` with a full-dimensional regular JC overlap.
Combining it with Theorem 8 gives Outcome P: strong tree-childness is the sharp
generic-identifiability boundary in the locked level-2 standard class.

The corollary identifies a quotient.  It does not say that every `T`
orientation realizes every fixed generic distribution.
