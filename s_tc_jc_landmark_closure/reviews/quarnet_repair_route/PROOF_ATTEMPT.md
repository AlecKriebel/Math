# Quarnet-and-repair route to standard-strong JC identifiability

Status: **PARTIAL PROOF; GLOBAL CLOSURE NOT ESTABLISHED**

This note is an independent proof-first reduction.  It does not import the
project's graph generator, Fourier engine, atlas compiler, canonicalizer, or
separator library.  The only executable calculation is the explicitly
bounded `2 x 2` minimal-repair check in `check_minimal_repairs.py`.

## 1. Locked setting and source statements

The topology convention is the locked simple binary LSA-rootable
semi-directed convention `sd_0`.  The class `S_TC` consists of the level-at-
most-two mixed graphs with at least one admissible rooting and no omnian.  The
JC domain is

```text
0 < x_e < 1,       0 < lambda_r < 1.
```

Induced subnetworks use the broader marginal reduction `red_*`: take the
union of up-down paths and then exhaustively suppress ordinary degree-two
vertices, parallel artifacts, and 2-blobs.  This is the operation in
Englander et al., Definition 2.4.  It is not the operation defining
membership in `S_TC`.

The exact local Englander v4 XML source states the following.

1. **Proposition 2.8.**  If two induced subnetworks on the same selected leaf
   set are distinguishable, then the original networks are distinguishable.
2. **Theorem 2.11.**  If two induced quarnets have different sets of displayed
   quartets, then their open JC (indeed JC or K2P) images are disjoint.
3. **Corollary 2.12.**  Different trees of blobs imply disjoint open images.
4. **Lemma 2.14 and Corollary 2.17.**  Several explicitly named quarnet and
   quinnet pairs are distinguishable.
5. **Proposition 2.15.**  A three-leaf tree is strictly separated from a
   strict level-1 or level-2 trinet by the stated JC inequality.
6. **Theorem 3.2.**  Triangle-free strongly tree-child binary level-2
   semi-directed networks are generically identifiable under JC.

Huber--van Iersel--Jones--Moulton--Veenema-Nipius, Theorem 6.2, states that a
binary semi-directed level-2 phylogenetic network with at least four leaves
is encoded by its **exact** induced quarnet deck.  In symbols,

```text
Q(N) isomorphic to Q(N')  implies  N isomorphic to N'.          (H)
```

The word `exact` is load-bearing: (H) does not state encoding by quarnets
modulo triangle redirection, nor encoding by quarnet model varieties.

## 2. Why distinguishable marginals rule out one-sided containment

Let `N preceq_JC N'` denote source-relative full-dimensional regular
stochastic containment.  Such a containment makes the source parameter
preimage of the common model set positive-dimensional and, on a source-open
regular region, full-dimensional.  Consequently the pair is not
distinguishable in the sense of Englander et al., Definition 2.5.

Taking the contrapositive of Proposition 2.8 gives:

> **Marginal obstruction.**  If some induced pair `N|S, N'|S` is
> distinguishable, then neither `N preceq_JC N'` nor `N' preceq_JC N` can
> hold.

Thus a bounded distinguishable marginal is enough for both symmetric overlap
and directed containment.  No equality of Zariski closures is used here.

## 3. The conditional six-leaf reduction

Write `q ~_T q'` when two quarnets are isomorphic after a finite sequence of
ordinary triangle redirections.  The following three statements would close
the proof-first route.

### Q: four-leaf stochastic dichotomy

> If two level-at-most-two quarnets are not `T`-equivalent, then they are
> distinguishable under open JC, except for the certified weak-Theta pair.

### R: strong-repair lift of weak Theta

> Let `N,N'` be standard-strong level-2 networks and let `Q` be four labels
> for which `N|Q,N'|Q` are the weak-Theta pair.  Then there is a label set
> `S` with `Q subset S` and `|S| <= 6` such that `N|S,N'|S` are
> distinguishable.

The two extra labels are allowed to be one repair witness selected from each
network.  They need not coincide.

### TQ: coherence of quarnet-wise triangle redirection

> If every corresponding induced quarnet of two binary level-2 networks is
> isomorphic or `T`-related, then the two complete networks are related by a
> coherent set of ordinary triangle redirections.

Assuming Q, R, and TQ, the global theorem follows in four lines.  If `N,N'`
are not globally `T`-equivalent, TQ supplies a four-set `Q` for which the
quarnets are neither isomorphic nor `T`-related.  By Q, that pair is either
distinguishable or is weak Theta.  In the first case Proposition 2.8 lifts the
distinction.  In the second case R supplies a distinguishable marginal on at
most six labels, which Proposition 2.8 again lifts.  Therefore no directed
containment can occur.  The already-audited ordinary-`T` local common germ and
context gluing give the converse common-germ direction.

This proves the following precise conditional statement.

> **Conditional theorem.**  Q + R + TQ imply that every pair of non-`T`-
> equivalent standard-strong binary level-2 networks has a distinguishable
> marginal on at most six labels.  In particular there is no symmetric
> full-dimensional overlap and no one-sided full-dimensional containment
> outside ordinary `T`.

## 4. Exact strong repairs of the weak-Theta omnian

Use the inherited rooted weak-Theta presentation with internal arcs

```text
rho->A, rho->C, A->B, B->C, C->D, D->E, A->F, E->F,
```

reticulations `C,F`, and source attachments

```text
B:1, D:2, F:3, E:4,
```

versus target attachments

```text
E:1, D:2, F:3, B:4.
```

After root suppression the vertex `A` is the common tail of the two incoming
reticulation edges `A->C` and `A->F`; hence it is an omnian.  A minimal
one-vertex tree-child repair which keeps the same two reticulations must
subdivide one of exactly these two outgoing sides and give the new tree
vertex a labelled child.  There are therefore exactly two minimal repair
types.

1. **A-C repair.**  The root is inserted on `A--R`, with
   `rho->A,rho->R,R->C,R->0`.  Its `sd_0` image contains `A--R->C`.  This
   destroys the triangle.
2. **A-F repair.**  Replace `A->F` by `A->R->F` and attach `R->0`.  The
   triangle `A-B-C-A` remains.

In both cases the reduced mixed graph is simple and binary and has no omnian.
The exact cycle-length multisets are

```text
A-C repair: 4,6,6;
A-F repair: 3,6,7.
```

This proves the two-repair assertion for the **minimal lift of this fixed
six-vertex core**.  Section 6 explains why promoting it to every occurrence
created by an arbitrary induced-subnetwork reduction requires an additional
lemma.

## 5. Exact `2 x 2` minimal-repair result

The independent standard-library verifier constructs the four repaired
rooted DAGs, checks acyclicity, binarity, rooted tree-childness, the locked
one-step `sd_0` reduction, simplicity, and the no-omnian criterion.  It then
enumerates the four displayed trees and every displayed quartet split.

For the ordered repair label `0`, all four source-target comparisons differ
on the quartet `{0,1,2,3}`:

| source repair | target repair | source displayed splits | target displayed splits |
|---|---|---|---|
| A-C | A-C | `01|23, 02|13, 03|12` | `02|13, 03|12` |
| A-C | A-F | `01|23, 02|13, 03|12` | `02|13, 03|12` |
| A-F | A-C | `01|23, 03|12` | `02|13, 03|12` |
| A-F | A-F | `01|23, 03|12` | `02|13, 03|12` |

By Englander et al., Theorem 2.11:

> **Proved minimal-repair lemma.**  If the same fifth taxon is attached at
> the repair vertex in both members of the weak-Theta pair, then every one of
> the four A-C/A-F repair combinations has disjoint open JC model images.

The fourth row independently recovers a stronger topological explanation for
the previously known strict A-F repair obstruction.  The earlier invariant
factorization remains useful, but is not needed for this aligned minimal
case.

Reproduction:

```text
python3 reviews/quarnet_repair_route/check_minimal_repairs.py
```

## 6. Why this does not yet prove R

The minimal check assumes a single label `0` repairs the omnian in **both**
networks.  A global strong pair need not have that alignment.  If the source
repair is witnessed by taxon `a` and the target repair by taxon `b`, then:

* `a` may lie on an unrelated side, in another pendant block, or outside the
  corresponding blob in the target;
* `b` may behave symmetrically in the source;
* marginalizing to `Q union {a}` can suppress the target's actual repair and
  recreate a weak, non-strong quarnet; and
* the `red_*` operation can use degree-two, parallel, and 2-blob suppression,
  so an arbitrary strong ancestor is not automatically one of the four
  minimal five-leaf DAGs checked above.

What is needed is not another large atlas but the following exact structural
extension lemma.

> **Aligned-or-separated repair lemma (UNRESOLVED).**  For any two
> standard-strong level-2 extensions whose restriction on `Q` is the weak-
> Theta pair, choose one omitted descendant taxon witnessing the repair of
> each induced omnian.  On `Q` together with those one or two taxa, either the
> repair roles align and reduce to the proved `2 x 2` lemma, or a displayed-
> quartet, tree-of-blobs, or strict JC invariant separates the two
> restrictions.

This lemma must explicitly cover the effects of the marginal BLS/PAS/degree-
two reductions.  It is a bounded structural theorem (at most six taxa), but
it is not contained in the exact sources read here.

## 7. What the published small-network results do and do not imply

Theorem 2.11, Corollary 2.12, Lemma 2.14, Proposition 2.15, and Corollary 2.17
provide many exact separators.  They do **not** state an exhaustive pairwise
classification of all sixteen labelled simple level-2 quarnet types.  In
particular:

* Lemma 2.14 handles specified same-type label changes for types `1b`, `2a`,
  `3a`, `3c`, and `3d`, plus one five-leaf pair;
* Corollary 2.17 separates one stated eight-type group from another and
  separates distinct prune leaves inside the first group;
* neither result states that every same-displayed-quartet, same-blob-tree
  pair omitted from those clauses is `T` or weak Theta; and
* Theorem 3.2 obtains the triangle-free global theorem by additional
  generator-specific reasoning and a five-leaf case.  It cannot be read
  backwards as a complete quarnet atlas with triangles.

Therefore Q is not proved merely by citing these results.  It requires either
a concise case-free invariant argument or a separately certified finite
four-leaf theorem.  The latter could be small, but it must be a complete
graph-to-polynomial proof, not a frozen signature census.

## 8. Coherence of `T`

Huber et al. prove exact quarnet encoding.  Replacing exact equality by
quarnet-wise `T` is not formal.  Different overlapping four-sets might select
different orientations of the same global triangle, or might map local
triangles to incompatible global triangles.  Erasing the internal triangle
arrowheads also leaves the category of semi-directed networks to which their
Theorem 6.2 directly applies.

The required proof can be isolated as follows.

> **Triangle-quotient encoding lemma (UNRESOLVED).**  For binary level-2
> standard semi-directed networks with at most one triangle per blob, the
> deck of induced quarnets modulo ordinary `T` encodes the complete network
> modulo a coherent collection of ordinary `T` moves.

A valid proof should adapt the generator-side and side-order reconstruction
in Huber et al., Propositions 4.3--4.5 and Theorem 6.2, showing that every
recovered datum outside the three internal triangle arrowheads is unchanged
and that overlap of the selected four-sets forces one consistent choice per
global triangle.  Rootability and admissibility of the resulting global
choices must be checked; they cannot be inferred from quarnet-wise validity.

## 9. Verdict

The quarnet route is promising and sharply bounded, but the cited theorems
plus the known weak-Theta obstruction do **not** yet prove the desired
standard-strong classification.

What has been achieved is a proof-first reduction of the global problem to
three explicit statements Q, R, and TQ, together with a complete exact proof
of the aligned minimal `2 x 2` repair case.  The most economical next step is
to prove R and TQ structurally and to close Q with a human-readable
four-leaf dichotomy.  Until all three are established, the positive global
theorem must remain unpromoted.
