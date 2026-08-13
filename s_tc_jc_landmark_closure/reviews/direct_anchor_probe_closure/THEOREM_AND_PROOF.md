# Direct-anchor probe-closure theorem

Status: **VERIFIED** for the bounded scope stated below.

## Locked scope

Let `D` be the 62 canonical directed relations in the tracked schema-3
three-outgoing stream whose bounded classification is `isomorphism_or_T`.
Each relation has four selected ports, source-to-target direction, and one
selected rooted graph on each side.  Graphs are reduced by the locked
reticulation-preserving standard semidirected convention.  An admissible
extension subdivides an internal nonbridge blob arc by a tree vertex and
attaches one new labelled port there.

For a direct anchor `d`, write `A` for its four-port support.  An `A+p` probe
inserts `p` independently on every admissible source and target arc.  An
`A+p+q` probe inserts `q` independently on every admissible source and target
arc of each `A+p` relation that remains a labelled isomorphism or ordinary
triangle redirection.  Every child transport is required to restrict to its
parent transport.

## Theorem

**VERIFIED.** The existing 144 path-bound terminal families do not literally
contain these anchors: every direct anchor has four selected ports, whereas
the tracked path-bound terminal anchors have five, six, or seven.  Nevertheless
the complete theorem-forced extension family of all 62 direct anchors is
finite and closes exactly as follows.

1. The 62 anchors have unique canonical transports and split into 34 labelled
   mixed-graph isomorphisms and 28 ordinary triangle redirections.
2. Their complete `A+p` family has 2,642 directed relations:

   - 202 labelled isomorphisms;
   - 112 ordinary triangle redirections;
   - 1,223 source-nonzero/target-zero exact JC polynomial separations; and
   - 1,105 source-zero/target-strict exact open-cube separations.

3. Continuing exactly the 314 surviving `A+p` relations gives 18,224
   `A+p+q` relations:

   - 1,472 labelled isomorphisms;
   - 560 ordinary triangle redirections;
   - 8,356 source-nonzero/target-zero exact JC polynomial separations; and
   - 7,836 source-zero/target-strict exact open-cube separations.

4. There is no unresolved relation, no proper one-sided containment, and no
   full-dimensional non-`T` overlap in this extension family.
5. Every surviving child transport extends one fixed parent transport.  Thus
   the one-port probes locate each extra port on a single directed segment,
   and the two-port probes recover the common order of every pair on that
   segment.  No probe-dependent isomorphism or triangle-redirection choice is
   possible.

Consequently the arbitrary-subdivision promotion theorem applies also to all
62 direct residual anchors.  Together with the previously audited 144
restoration-terminal families, this removes the direct-anchor omission
identified by the whole-proof referee.

## Proof

### 1. Why a new bounded family is required

The tracked hard-cover stream contains exactly 144 path-bound equality
terminals, distributed by selected-port count as

```text
5 ports: 92
6 ports: 44
7 ports:  8.
```

Every direct residual anchor has exactly four selected ports.  Labelled mixed
graphs with different labelled-port counts cannot be isomorphic, and ordinary
triangle redirection does not add or delete a port.  Hence no exact
anchor-level crosswalk exists.  This is a scope mismatch, not a mathematical
obstruction; it requires compiling the missing bounded extensions.

### 2. Unique anchor transports

For each relation the verifier reads the selected source and target rooted
graphs from the tracked graph stream, performs root suppression from first
principles, and backtracks over colour classes preserving labels, incidence,
and retained arrowheads.  In ordinary-`T` mode it forgets arrowheads only on
the unique triangle.  Every anchor has exactly one accepted map.  The literal
mixed maps give 34 isomorphisms; the remaining 28 maps preserve the labelled
underlying graph and all arrowheads off one triangle, hence are exactly
ordinary `T`.

The certificate records the complete vertex map, edge permutation, identity
port map, triangle pair, and reticulation transport outside the redirected
triangle.  These transports are regenerated rather than trusted.

### 3. Exhaustiveness of one- and two-port relations

Deleting a newly attached port and suppressing its parent recovers one unique
internal blob arc.  Conversely, subdividing any admissible internal blob arc
and attaching a labelled leaf gives one valid binary strong extension.  Thus
the Cartesian product of source and target admissible arcs is bijective with
the one-port relation universe.

For an `A+p` survivor the unique child map restricts to the unique anchor map.
Applying the same deletion/insertion bijection to that fixed child gives the
complete two-port universe.  No `q` continuation is required after a
separated `p` relation: marginalization already contradicts the proposed
source-relative containment.  Content-addressed parent ids record this
directional dependency.

The verifier reconstructs these Cartesian products and obtains 2,642 and
18,224 records.  Deleting a record, changing an arc, changing a parent, or
reversing the source and target is therefore detected without consulting a
stored count as an oracle.

### 4. Exact topological survivors

For a child relation, extend its fixed parent map by sending the new
subdivision vertex and leaf to their target counterparts.  Direct incidence
comparison gives a labelled isomorphism precisely when every mixed-edge
attribute is preserved.  If attributes differ, the relation is ordinary `T`
precisely when both graphs have one triangle, the fixed map sends one triangle
to the other, and every mismatch is confined to those three edges.  Any other
relation is topologically distinct under the fixed anchor.

This direct test yields the survivor counts in the theorem.  Because every
anchor map is unique, an alternative child map could not restrict to a
different anchor map; hence no surviving presentation is lost by fixing the
transport.

### 5. Graph-derived JC separation

For every topologically distinct child the compiler independently enumerates
all displayed trees.  For each switching it computes descendant-label masks
on every retained edge, then constructs the exact JC Fourier orbit tensor.
No stored pullback or separator assignment is used.

The fixed explicit family contains 1,852 degree-at-most-three relations in
the 15 quartet orbit coordinates.  Finite-field evaluations only propose a
candidate.  Acceptance always expands the candidate in the integer
polynomial ring of edge multipliers and inheritance probabilities.

Every separated child falls into one of two exact cases.

- `source_nonzero_target_zero`: the pullback is the zero polynomial on the
  target and a nonzero polynomial on the source.  A source-full germ cannot
  lie in the target because its source exceptional set is proper algebraic.
- `source_zero_target_strict`: the pullback is zero on the source and has one
  strict sign throughout the target open cube.  The target polynomial is
  factored over the integers.  Each factor's multivariate Bernstein
  coefficients on `[0,1]^d` have one weak sign and at least one strict
  coefficient; every Bernstein basis function is positive on `(0,1)^d`.
  Therefore each factor, and hence their product, is nonzero throughout the
  target's open parameter domain.  The two stochastic images are disjoint on
  this marginal.

The verifier regenerates all 8,816 distinct graph-bound witnesses, expands
every committed factor product, and recomputes every rational Bernstein
coefficient.  Hence a valid polynomial attached to the wrong relation is
rejected.

### 6. Promotion to arbitrary words

Fix the unique four-port anchor transport.  For an arbitrary extra port `p`,
marginalize every other extra port to character zero.  The positive path
product map is a submersion, so a source-full arbitrary-word containment
would induce a source-full `A+p` containment.  The exact bounded table forces
that probe to be isomorphic or `T`-related and fixes its segment under the
anchor transport.

For two extra ports `p,q`, the same argument gives an `A+p+q` containment.
The exact table forces the two-port relation to extend the already fixed
one-port transport.  Consequently all pairwise orders agree.  Pairwise order
on a finite directed segment determines one total order, and overlaps between
segments share the same anchor.  The recorded triangle is likewise fixed by
the parent transport, so one cannot mix different `T` choices between probes.

This is exactly the missing direct-anchor case of the existing marginal-
submersion and probe-coherence argument.

## Exact evidence

The active certificate is `certificates/summary.json`.  Its inputs are four
tracked files only: the bounded relation stream, its graph stream, the
hard-cover terminal stream, and the explicit invariant family.  The package
contains 1,420 unique rooted graphs and 8,816 distinct exact separator
witnesses.  All generated streams use deterministic gzip timestamps and
content addresses.

The mutation suite rejects all twelve required attacks, including deletion of
an anchor, alteration of a direct id or transport, reversal of source and
target, alteration of a `T` choice, deletion of a one- or two-port relation,
inconsistent `p/q` order, parent reassignment, arc mutation, and assignment of
a valid separator to the wrong directed relation.

## Scope boundary

This theorem closes only the direct-anchor arbitrary-subdivision omission.  It
does not independently regenerate the upstream 10,466-relation bounded
universe and does not by itself promote the global Outcome-P theorem.  Those
are separate dependency nodes.
