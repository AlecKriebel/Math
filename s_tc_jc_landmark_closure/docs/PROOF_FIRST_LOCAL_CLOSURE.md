# Proof-first local closure

Status: **PROVED; independently regenerated and adversarially reviewed**

This note isolates the one local statement needed by the global theorem and
shows how the audited exact algebra proves it after the finite grammar is
independently bound to the frozen relation streams.  It is not a new topology
search and it does not use a triangle/complement factorization.

## 1. Local theorem

Let `H` and `H'` be complete nontrivial blob factors of locked `sd_0`
standard-strong binary level-2 semi-directed networks.  Their physical
boundary blocks carry the same fixed labels.  Choose an admissible incoming
boundary for each factor independently.  Write `PM(H)` for the open JC
boundary-tensor image modulo the positive port-incidence action

```text
P(g_1,...,g_k) -> P(g_1,...,g_k)
                    product_j a_j^[g_j != 0].
```

The statement to prove is

```text
a source-full regular germ of PM(H) is contained in PM(H')
    iff
H and H' are labelled-isomorphic or differ by ordinary triangle
redirection T.
```

In particular, there is no proper one-sided projective local containment.
The right-to-left implication means a common full-dimensional regular germ;
it does not assert equality of complete open images.

## 2. Finite source supports

The primitive-core theorem gives exactly the cycle and the four directed
theta cores `theta-0`, ..., `theta-3`.  A full factor is one of these cores
with a finite ordered word of port-bearing ordinary subdivisions on every
directed segment and a real child port below every path-sink reticulation.

Choose one labelled port on every segment of a minimum strong repair and
every path-sink child.  This gives a core-preserving rigid support.  There are
only three support widths relevant to the proof:

| source family | outgoing support used | total tensor ports |
|---|---:|---:|
| three-sunlet with no further outgoing port | 2 | 3 |
| cycle with a further port; `theta-0`, `theta-1`, `theta-3` | 3 | 4 |
| `theta-2` | 4 | 5 |

For the cycle, the two-port support is handled directly by the trinet
polynomial

```text
F = q011 q101 q110 - q123^2.
```

It vanishes on an ordinary median and its three-sunlet pullback is strictly
positive throughout the open JC cube.  The three possible sunlet
reticulation choices are precisely ordinary `T`.  If the cycle has another
outgoing boundary, include one such boundary to obtain the rigid
three-outgoing source used by the four-port certificate.

For `theta-0`, `theta-1`, and `theta-3`, minimum repair plus sink children has
three outgoing labels.  For `theta-2`, it has four.  These claims follow
directly from the repair table and do not depend on the lengths of the other
port words.

## 3. Why the target completion grammar is exact

Marginalize the common full tensor to a selected source support.  A target
preimage can place its admissible incoming boundary at a different physical
port, so the target grammar has two cases:

1. its structural incoming boundary is selected; or
2. it is unselected and has character zero.

On every target segment, the selected real labels form an ordered subword.
Every omitted ordinary port has character zero.  Consecutive edges with the
same complete displayed-switching descendant-mask row enter every JC
coordinate only through the product of their multipliers, so all omitted
ordinary ports are absorbed into positive serial products.  If a path-sink
child or every port on a chosen minimum repair segment was omitted, restore
one zero-character dummy at that role.  This produces a full binary strong
completion without changing the selected tensor.  Conversely, deleting the
dummies and taking serial products recovers the selected tensor of every full
target.  Hence the completion grammar is onto, not merely dominant.

Every physical boundary matching is retained: source labels are anchored
simultaneously, while the target uses the full symmetric group on all
selected boundaries, including the independently chosen incoming position.
Thus anchoring loses no directed labelled relation.

## 4. Restoration is exhaustive

If the selected target already contains every path-sink child and one whole
minimum repair, it retains its primitive core and is a fixed-full relation.
Otherwise each dummy role represents an actual boundary label of the full
source-target comparison.  Restore the roles one at a time.  At each step,
the label can occupy every directed source segment and every position in that
segment, and is bound to each eligible target dummy role.  Induction on the
number of dummies proves that every complete relation extends exactly one raw
restoration path before canonical duplicate removal.  A terminal path has no
dummy and therefore compares two complete core-retaining labelled factors.

The independent inventory crosswalk verifies this mathematical grammar
against the frozen root streams.  The fixed-root inventories are `5,344`
four-port roots and `132` five-port `theta-2` roots.  These counts are
checksums of the grammar, not premises of the proof.

## 5. Exact algebraic cover

For each decorated relation, displayed reticulation switchings and edge
descendant masks regenerate the complete zero-sum JC tensor.  The exact
certificate applies the port-permutation orbit of seven explicit
multihomogeneous invariants.  Every terminal relation has exactly one of the
following graph-derived certificates.

1. **Generic separation.**  A target pullback is the zero polynomial and the
   source pullback is a nonzero integer polynomial.
2. **Strict stochastic separation.**  The source pullback is zero and the
   target pullback has a factor/Bernstein certificate of one strict sign on
   the entire open parameter cube (or the same statement with the roles
   recorded in the opposite directed relation).
3. **Topology equality.**  Independent mixed-graph canonicalization proves
   labelled isomorphism or equality after forgetting only the three
   arrowheads of one triangle, namely ordinary `T`.

The independently audited four-port stream contains `68,584` restoration
states:

```text
56,055  generic polynomial separations
 8,349  nonterminal one-role refinements
 4,036  strict open-cube separations
   120  labelled-isomorphism terminals
    24  ordinary-T terminals.
```

The independently audited five-port `theta-2` stream contains `2,106`
states:

```text
1,860  generic polynomial separations
  114  nonterminal one-role refinements
  132  labelled-isomorphism terminals.
```

There is no unresolved terminal in either stream.  Every polynomial body is
regenerated from its bound graph, switching, mask, marginal, and invariant;
no topology identifier selects a stored polynomial.

The independent upstream five-port signature gate regenerates all three
`theta-2` supports, both target incoming modes, 6,138 completion bases, every
relative five-port assignment, and the complete 84-invariant quartet deck.
The necessary containment filter leaves exactly three equal signature pairs.
Expanding them gives 192 raw presentations, partitioned intrinsically into
18 direct labelled isomorphisms, 42 selected-incoming root-presentation
duplicates, and 132 marginalized-incoming restoration roots.  Explicit
mixed-graph transports identify every one of the 42 duplicates with an
already represented standard relation, while the 132 marginalized
presentations equal the frozen root multiset exactly.  Thus the downstream
five-port hard cover omits no algebraically necessary decorated relation.

For generic separation, let `V_H` be the complex closure of the source
projective model.  It is irreducible because it is the closure of the image
of an irreducible parameter space.  A nonzero source pullback means the
invariant is nonzero in the coordinate ring of `V_H`.  Its zero set in
`V_H` is therefore proper and cannot contain a source-full regular germ.
This is an image-dimension argument, not merely a measure-zero statement in
a redundant parameter space.  A strict-sign certificate is stronger: the
two relevant open stochastic loci do not meet.

## 6. Arbitrary words

Let `Q_s` and `Q_t` be rigid supports for the two complete factors and use
the exact union anchor `A=Q_s union Q_t`.  Restriction to `A`, `A+p`, and
`A+p+q` is a semialgebraic submersion on a dense regular open set.  On each
serial edge class the only new effective coordinate is a product, and

```text
d(x_1 ... x_m)
  = sum_i (product_(j != i) x_j) dx_i
```

is nonzero on `(0,1)^m`; different classes use disjoint variables.
Consequently a source-full containment of arbitrary words descends in the
required direction to the bounded relation.

After one rigid anchor transport is fixed, every `A+p` probe determines the
segment of `p`, and every `A+p+q` probe determines the order of a pair on one
segment.  These comparisons come from actual total words and hence assemble
to a unique total order.  If a probe subdivides a triangle edge, its selected
topology is triangle-free and fixes the literal orientation.  Otherwise the
same unique triangle persists, so all probe-level `T` choices are one
coherent redirection.  The audited probe streams have no non-isomorphism,
non-`T` terminal.

This promotes the fixed-support algebra to all finite port words.

## 7. Converse

Labelled isomorphism gives the same local model.  The independent ordinary
triangle certificate gives a common full-dimensional regular projective germ
for the three orientations of a port-labelled triangle.  Contracting that
local equality with the unchanged remainder of the blob proves the same for
an embedded triangle.  Positivity holds after shrinking to the certified
open parameter neighborhood.  No equality of complete stochastic images is
claimed.

Sections 2--7 prove the local theorem.  The independent inventory and
signature crosswalks confirm that the grammar in Sections 2--4 is exactly the
grammar consumed by the frozen algebra and probe certificates.

## 8. Prohibited shortcut

A triangle-bearing theta is not a bridge gluing of a three-sunlet and a
triangle-free factor.  The triangle and the complementary pole-to-pole path
meet at both theta poles, and the hidden-pair contraction has an ambient
gauge larger than the bridge incidence action.  The proof above classifies
the complete theta tensor directly; it never extracts those two pieces
separately.
