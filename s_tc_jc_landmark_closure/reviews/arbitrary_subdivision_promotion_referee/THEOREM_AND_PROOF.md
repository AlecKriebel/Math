# Arbitrary-subdivision promotion theorem

Status: **VERIFIED AFTER CORRECTION**, conditional only on the frozen,
independently verified n3/n4 fixed-full terminal and probe certificates listed
in `INPUT_LOCK.json`.

This note proves the promotion step. It does not regenerate the graph algebra
of the finite atlases and does not promote the global level-2 theorem.

## 1. Locked objects

A tensor port is the structural incoming boundary or one selected outgoing
boundary of a local factor. Let `Q_s` and `Q_t` be the independently chosen
minimal rigid supports in a fixed full source-target relation. The anchor is

```text
A = Q_s union Q_t,
```

with the exact physical labels, restoration root, restoration path, and
source-to-target transport carried by one frozen terminal record. This union,
not `Q_s` alone, is the object held fixed in all probes.

Every boundary outside `A` is an ordinary port at a subdivision tree vertex
of one internal blob segment. Indeed, `A` already contains both structural
incoming boundaries, every reticulation-sink child boundary, and one complete
strong repair on each side. Binary degree constraints leave no other event
site at which an omitted boundary can occur.

Ordinary `T` means one redirection of the unique triangle, with every port
label and every arrowhead outside that triangle retained. A `T` transport is
an isomorphism after forgetting only the triangle arrowheads.

## 2. The theorem

### Theorem (arbitrary-subdivision promotion)

Let `H,H'` be full labelled ported factors in the locked standard-strong
level-2 local universe. Assume their fixed-full restoration path is in one of
the frozen n3 or theta2-n4 terminal families. If a source-relative regular
open germ of the projective JC model of `H` is contained in the projective JC
image of `H'`, then the complete ported factors are labelled-isomorphic or
ordinary-`T`-related.

If they are not, some base, one-port, or two-port restriction separates the
directed containment. Every such restriction has at most **10 tensor ports**.
The bound 10 is attained by 38,016 certified n4 two-port relations. It is the
exact maximum of this exhaustive certificate scheme; no claim is made that a
different proof could not use a smaller universal bound.

## 3. Path products and marginal submersion

Fix a selected boundary set `Y` containing the source support. For every
displayed reticulation choice, restrict each physical edge's descendant mask
to `Y` and apply the locked zero-sum split/complement normalization. Physical
edges with one surviving identical signature form a nonempty class `C`; the
effective JC coordinate is

```text
y_C = product_{e in C} x_e.
```

The classes partition the participating physical edges. Therefore different
rows of the Jacobian use disjoint variable blocks, and

```text
partial y_C / partial x_e = y_C / x_e > 0       (e in C).
```

The Jacobian has one independent row per class at every point of the open
cube. The map is onto: for prescribed `0<y_C<1`, set every member of `C` to
the positive `|C|`-th root of `y_C`. This section is semialgebraic. Retained
inheritance coordinates contribute identity coordinates or the open-cube
involution `lambda -> 1-lambda`. Tensor-invisible inheritance coordinates
may remain redundant; they do not reduce the rank of the effective
coordinates used here.

Thus the physical-to-effective restriction is an everywhere submersive
semialgebraic map. The statement on model images is generically, rather than
everywhere, submersive. Write

```text
Phi_full : Theta_H -> M_H,
rho_Y    : Theta_H -> D_Y,
Psi_Y    : D_Y -> M_(H|Y),
```

so that marginalization satisfies

```text
m_Y o Phi_full = Psi_Y o rho_Y.
```

The generic-rank locus of `Psi_Y` is a nonempty Zariski-open subset of its
parameter space. Surjectivity and submersivity of `rho_Y` make its preimage
nonempty and Zariski open. Intersect it with the regular locus of `Phi_full`.
On the resulting dense regular open source locus, the differential of `m_Y`
has the full rank of the selected source model. The relative constant-rank
theorem then makes `m_Y` an open map onto a selected-model germ.

This proves claim (1). The parameter-product part is everywhere submersive;
the induced model-image marginal is a submersion on a dense regular open
locus.

## 4. Direction of containment descent

Suppose `U` is a source-relative full-dimensional regular germ in

```text
M_H intersect M_H'.
```

Its parameter preimage contains a nonempty parameter-open set. The dense
regular locus from Section 3 meets that set. After shrinking around such a
point, `m_Y(U)` contains a relative-open germ of the selected source model.
Every point of `U` has at least one target realization, so its marginal lies
pointwise in the selected target tensor image. Consequently

```text
H|Y preceq_JC H'|Y
```

in precisely the source-to-target direction used by the finite separator.

No target parameter is selected continuously. No openness of the target
parameter-to-tensor map is required. This distinction is what makes the
argument valid for a target restriction with redundant inheritance
coordinates or a collapsed core.

This proves claim (6).

## 5. One fixed anchor map

Under the assumed full containment, every marginal along the actual
fixed-full restoration path inherits source-relative containment by Section
4. Hence that path cannot terminate at either kind of certified separator:

- target identity and source nonzero excludes containment outside a proper
  source algebraic subset;
- source identity and target strict sign excludes every open common point.

It reaches one of the 276 accepted path-bound anchors. The frozen families
contain 252 labelled-isomorphism anchors and 24 ordinary-`T` anchors. Their
clean-room certificates establish a unique fixed-label quotient transport.

For any extra physical label `p`, marginalize the original full containment
directly to `A+p`. The actual relation is one cell in the exhaustive p arc
pair array. It cannot be a generic or strict separator, so it is an allowed
isomorphism or `T` cell. The audited child transport restricts exactly to the
one anchor transport. Thus all one-port probes use the same support
identification and assign `p` to one definite mapped anchor interval.

The finite replay checked 10,516 n3 and 15,510 n4 allowed child transports.
There was no restriction failure. This proves claim (2), with the necessary
correction that the fixed support is the exact union anchor `A`.

Pointwise rigidity is essential. A nontrivial automorphism fixing the anchor
labels would permit two extensions of the same one-port record. The frozen
clean-room terminal/probe certificates independently found unique transports;
the mutation suite rejects a second anchor transport and a cross-anchor map.

## 6. Two ports reconstruct every word

For two labels `p,q`, first use the actual allowed `A+p` parent and marginalize
the original containment to `A+p+q`. Conditional q rows enumerate every
internal source-target arc pair of that exact parent. The surviving child
transport restricts to the p transport, hence to the fixed anchor map.

If `p,q` lie in different anchor intervals, their one-port records already
locate them. If they lie in one interval, inserting `q` on the two sides of
the p subdivision distinguishes the two orders. Therefore all two-port
restrictions recover every pairwise comparison in each interval. These
comparisons are the restrictions of the actual finite source order and of
the actual finite target order under one fixed endpoint map, so they are
transitive. A finite strict total order is uniquely determined by all of its
pairwise comparisons.

This covers empty anchor segments and arbitrarily many repeated subdivisions:
an empty segment is still one anchor arc, the first one-port probe names it,
and later two-port probes order every pair on it. Simplicity excludes
parallel-edge ambiguity. Pointwise rigidity excludes a symmetric exchange of
two empty segments.

As a finite adversarial check, the independent script enumerates all ordered
words of three and four labels on each of 2, 5, and 6 primitive segments,
including empty segments and repeated same-segment placements. Their complete
one-/two-port signatures are injective in all 5,394 cases. The proof above is
for any finite number of labels; the census is a falsification check, not its
logical basis.

This proves claim (3).

## 7. Coherence of ordinary triangle redirection

There is at most one triangle. All allowed maps restrict to one unique
anchor `T`-quotient map, so probes cannot redirect different triangles. Two
cases remain.

1. An extra port subdivides an anchor-triangle edge. The three-cycle then
   disappears in that probe. There is no ordinary-`T` quotient at that child;
   an allowed child would have to be a literal labelled isomorphism fixing
   the orientation. Thus a genuinely redirected anchor cannot survive such a
   full relation.
2. No extra port subdivides a triangle edge. The same triangle survives in
   every probe and in the full factor. Every child transport restricts to the
   same quotient map, so there is exactly one global redirection.

The final n3 family exercises this issue. Each of its 24 `T` anchors has
exactly 5 allowed p cells and 30 allowed conditional q cells. All 840 allowed
descendants are again `T`; none changes to labelled isomorphism, and every
transport restricts to its parent. The independently regenerated triangle
counts are one on both sides of every `T` relation. Changing the transported
outside reticulation or switching one probe to an isomorphism is rejected by
the mutation suite.

This also handles a change of triangle sink: both source and target supports,
including their sink labels, are already in `A`, and the raw vertex and
outside-reticulation transports are fixed there. A probe cannot choose a new
sink map.

This proves claim (4).

## 8. Exact finite tensor-port bound

The exact accepted anchor and probe distributions are:

| family | anchor ports | p-relation ports | q-relation ports | maximum |
|---|---|---|---|---:|
| n3 | 5: 92; 6: 44; 7: 8 | 6: 4,952; 7: 3,564; 8: 800 | 7: 42,552; 8: 39,600; 9: 9,680 | 9 |
| theta2-n4 | 6: 42; 7: 66; 8: 24 | 7: 3,402; 8: 6,600; 9: 2,904 | 8: 37,800; 9: 79,860; 10: 38,016 | 10 |

The four shard ranges in each family are disjoint, gapless, and cover all 144
n3 and 132 n4 anchors. Their 269,730 relations are in record-by-record
semantic bijection with the final verbose packages. Thus **10 total tensor
ports**—one structural incoming boundary and nine outgoing boundaries—not the
old crude 12, is the exact attained certificate bound.

This proves claim (5).

## 9. Nonstrong target restrictions

Before the target support has been restored, an intrinsic selected target
restriction may prune a reticulation or fail the strong condition. It is not
discarded and is not called a standard-strong topology. Its selected tensor is
represented by the following completion grammar:

1. record whether the independently chosen structural incoming boundary is
   selected;
2. record the selected reticulation-sink mask and each ordered selected
   segment subword;
3. choose one minimum repair in the full strong target;
4. insert a zero-character dummy for an omitted incoming boundary, omitted
   sink child, or still-empty selected repair segment;
5. absorb every other omitted ordinary subdivision into its adjacent serial
   edge product.

A zero-character dummy contributes `a_e(0)=1`, and serial suppression replaces
open multipliers by their product, still in `(0,1)`. Thus the completion has
exactly the target marginal tensor. Redundant inheritance choices are harmless
because only membership in the target image is needed.

The pre-existing independent partition certificate exhausted 24,792 selected
restrictions and found zero descriptor mismatch, including 17,304 restrictions
with a strictly smaller reticulation core. The final streams then bind this
grammar to 68,584 n3 and 2,106 n4 relation records. The present clean-room
schema check found zero failure in incoming, sink, repair, restoration, and
remaining-role partitions. Both selected and marginalized incoming modes
occur in n3; the relevant n4 family uses the marginalized mode.

Once `A` is reached it already contains `Q_t`; therefore the final p/q target
probes are core-retaining. The weak grammar is needed for restoration prefixes,
not as permission to compare against a nonstandard full target topology.

This proves claim (7), with that interpretation locked.

## 10. Conclusion and reliance boundary

All seven promotion claims survive after two corrections:

- use the exact path-bound union anchor `A=Q_s union Q_t`, especially across a
  triangle sink change;
- replace the historical safe bound 12 by the exact attained bound 10.

No counterexample to arbitrary-subdivision promotion was found. The theorem
is conditional on the verified fixed-full n3/n4 terminal universes and their
verified graph-derived classifications. It says nothing by itself about cut
recovery, bridge localization, root reduction, exhaustion of a different
local universe, or the final global identifiability theorem.
