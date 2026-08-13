# Sharp level-2 JC boundary: final theorem proof

Status: **CANDIDATE FOR FINAL ADVERSARIAL RELEASE**

This document gives the proof to be attacked by the final independent
reviewer.  It uses only the locked `sd_0` convention and the open JC domain.
No statement below concerns a broader root-cleanup convention, a physical
bridge multiplier, or equality of complete stochastic images.

## 1. Main classification theorem

Let `N` and `N'` be leaf-labelled, simple, binary, LSA-rootable
semi-directed mixed graphs obtained by the locked reticulation-preserving
`sd_0` reduction.  Assume that every admissible rooting is tree-child and
that every blob has at most two reticulations.  Equivalently, the mixed
graphs lie in the locked class `S_TC` and are level two.

Write `N ~_T N'` when their reduced labelled bridge trees are isomorphic and,
under that isomorphism, every pair of corresponding nontrivial ported blobs
is labelled-isomorphic after zero or one ordinary redirection of its unique
triangle.  Ordinary components and every pendant-component placement are
fixed.

The theorem is

```text
N preceq_JC N'  if and only if  N ~_T N'.                 (1)
```

Consequently:

1. the one-sided relation is symmetric on this class;
2. no proper one-sided generic containment occurs;
3. `N bowtie_JC N'` if and only if `N ~_T N'`; and
4. a generic exact JC distribution identifies one standard semi-directed
   topology modulo ordinary triangle redirection.

The right-to-left implication in (1) asserts a common full-dimensional
regular stochastic germ.  It does not assert equality of complete open
stochastic images, nor that every `T` orientation realizes every point of
one orientation's model.

## 2. The topology class is intrinsically finite-core

Choose an admissible rooting and expose one incoming boundary of a nonroot
blob.  If the blob has `t` tree vertices and `r` reticulations, summing local
indegrees gives cyclomatic number `r`.  A nontrivial level-two blob therefore
has cycle rank one or two.  Contracting every ordinary port-free bivalent
path gives a cycle in rank one.  In rank two, every surviving vertex has
degree three, and `e=v+1` gives `3v<=2e=2v+2`; biconnectedness and simplicity
leave two poles joined by three paths, namely a theta.

Along a directed theta path, source and reticulation-sink events alternate.
Both poles cannot be reticulations without creating a directed cycle.  Up to
path and pole symmetry there are exactly four event patterns, `theta-0`
through `theta-3`.  Every complete factor is recovered uniquely by ordered
words of port-bearing subdivisions on the directed core segments and one
real child boundary below each path-sink reticulation.  The no-omnian
criterion gives the finite list of minimum strong repairs recorded in
`GENERATOR_AND_SUPPORT_THEOREM.md`.

A cycle has one simple cycle.  A theta with path lengths `(l1,l2,l3)` has
cycle lengths `li+lj`.  Two triangles force `(1,1,2)` or `(1,2,2)`.  The
first has parallel edges and violates the simple lock.  The second is
`K4-e`.  Its four incoming reticulation arrowheads would require four
tree-child-compatible tails, while its rooted preimage has at most the two
ordinary vertices and the inserted root; using either vertex twice makes it
an omnian.  The independent complete rooting census reaches the same
conclusion.  Thus every blob in the theorem already has at most one
triangle; no extra one-triangle hypothesis is imposed.

Finally, following tree-or-leaf children from any admissible root reaches a
real boundary without crossing a reticulation.  Moving the root to that arm
reverses only ordinary edges, preserves all retained arrowheads and the LSA
condition, and suppresses back to the same mixed graph.  Since membership in
`S_TC` quantifies over every admissible rooting, the new rooting is
tree-child.  Uniform-root JC reversibility preserves every displayed
unrooted tree tensor; splitting or multiplying an arm parameter stays inside
`(0,1)`.  Hence root-containing factors are exactly covered, projectively,
by incoming-boundary factors.  Source and target incoming boundaries are
chosen independently.

## 3. Pointwise recovery of the bridge tree

For a split `A|A^c`, order the Fourier flattening by the total character on
`A`.  At a true cut, its four character blocks are positive rank-one outer
products, so the whole flattening has rank at most four.

The converse holds at every open JC point, not merely generically.  A
one-active noncut has one of the independently regenerated strict block
minors.  For the remaining crossing of two active three-port endpoint
tensors, write

```text
F=abc-t^2,       G=a-bc
```

and use capitals on the other endpoint.  Every permitted endpoint satisfies

```text
F>0,  or  F=0 and a>=bc,
```

with the ordinary trivalent endpoint included in the equality case.  If the
two endpoints are joined by `0<z<1`, rank one in every character block forces

```text
aA=z^2 bcBC,
F=0,
F'=0.
```

But `aA>=bcBC>z^2bcBC`, a contradiction.  Word compression reduces every
larger noncut to one of these cases while retaining a full strong completion.
Therefore

```text
A|A^c is a cut  iff  rank Flat_(A|A^c)(p)<=4             (2)
```

for every distribution in the open model.

If `N preceq_JC N'`, apply (2) on the common source-open set.  A source cut
cannot be a target noncut, and a target cut equation cannot hold at a source
noncut point.  Thus both cut sets are equal.  Their compatible labelled split
system gives the same reduced bridge tree.  A degree-three tree component is
distinguished from a three-sunlet by `F`: it is zero on the former and
strictly positive on the latter.  A theta factor has at least four boundaries
in `S_TC`.  The ordinary/nontrivial decorations therefore also agree.

## 4. Correct projective bridge localization

For a bridge `e=uv`, the complete positive factorization fiber is the full
incidence action

```text
P_u -> a_(u,e) P_u,
P_v -> a_(v,e) P_v,
x_e -> x_e/(a_(u,e)a_(v,e)).                             (3)
```

Sectorwise positive rank-one uniqueness proves that (3) is the whole fiber.
JC symmetry makes the three nonzero character scales equal.  Marked
components have one-character anchors for every incidence; unmarked retained
components have degree at least three and use pair anchors.  Their exponent
matrices have full rank, so positive real-analytic local slices exist.  The
bridge graph is a tree, hence no incidence gauge circulates around it.  The
slice edge coordinate is an effective scale, not a physical edge multiplier.

Apply intrinsic projective extraction to the common source-open set.  In a
source slice it contains a smaller product box of local factor germs and
effective bridge intervals.  Vary one factor while fixing all others.  Every
target realization of the resulting distribution has the same extracted
projective factor by the exact fiber theorem.  The finitely many target
incoming/completion types cover this focal box.  Semialgebraic dimension
therefore puts a source-relative full-dimensional open subgerm into one
target local type.  No continuous target parameter section is selected.

This proves that a global one-sided containment induces a one-sided
projective containment between every corresponding full blob factor.  A
distant factor cannot compensate for a focal separator because the focal
projective orbit is an intrinsic function of the distribution.

## 5. Complete local containment lemma

Let `H,H'` be corresponding complete nontrivial blob factors on the same
labelled physical boundary set, with independently chosen admissible
incoming presentations.  Then

```text
PM(H) preceq PM(H')
    iff H and H' are labelled-isomorphic or ordinary-T-related.            (4)
```

Here `PM` denotes the open JC boundary-tensor image modulo positive
port-incidence scaling.

### 5.1 Rigid supports

Select every reticulation-sink child and one labelled port on each segment of
a minimum repair.  This gives a core-retaining pointwise-rigid support.  Its
outgoing size is two for a cycle, three for `theta-0`, `theta-1`, and
`theta-3`, and four for `theta-2`.  A cycle with no further boundary is the
three-port case separated from an ordinary median by `F`; its three
orientations are exactly ordinary `T`.  A cycle with further boundaries is
included in the three-outgoing support gate.

### 5.2 Exact finite relation gate

Marginalize a hypothetical full containment to a source support.  The target
completion grammar distributes the selected labels in order on every
primitive segment, allows its incoming boundary either to be selected or to
have character zero, and restores every omitted sink or required repair role
by one zero-character dummy.  Omitted serial ports enter only through positive
products.  Conversely every full target reduces to exactly such a record.
Thus this finite grammar is onto all selected target tensors; it is not a
topology census assumption.

For the three-outgoing supports, an independent graph-to-algebra compiler
regenerates 10,466 canonical decorated directed relations from 10,826 raw
presentations.  Exact invariant pullbacks give 5,284 strict open-cube
separations.  The remaining 5,120 canonical relations have 5,344 raw
fixed-full coverages; every one is bound bijectively to a restoration root.
The exact restoration forest has 68,584 states and no unresolved terminal.
Its terminal paths are 120 labelled isomorphisms and 24 ordinary `T`
relations.  The remaining 62 direct residual relations independently reduce
to 34 labelled isomorphisms and 28 ordinary `T` relations.  Every one of the
800 distinct strict polynomial bodies is regenerated from its bound graph
and has an exact rational Bernstein/factor sign certificate.

For the four-outgoing `theta-2` supports, a second independent compiler
constructs all three source supports, both target incoming modes, all 6,138
completion bases, all relative five-port assignments, and the complete
84-invariant quartet deck.  The necessary inclusion

```text
S(source) subseteq S(target),
```

where `S` is the set of nonidentical invariant pullbacks, leaves exactly
three signature pairs, all equal.  At presentation level the 192 raw
survivors split intrinsically as follows:

```text
18  complete direct relations, all labelled mixed-graph isomorphisms;
42  selected-incoming nonretaining presentations, each explicitly
    transported to an existing standard relation class;
132 marginalized-incoming nonretaining presentations, exactly the frozen
    fixed-full root multiset.
```

The 132 fixed roots generate 2,106 graph-bound restoration states: 1,860
generic polynomial separations, 114 one-role refinements, and 132 labelled
isomorphism terminals.  There is no unresolved or non-`T` terminal.  The
selected-incoming duplicates are root-presentation variants only; the
independent mixed-graph quotient and explicit vertex/port transports forget
no labelled standard relation.

Why the signature filter is sufficient is elementary.  If an invariant
vanishes identically on the target but has a nonzero source pullback, a
source-full regular germ would lie in a proper algebraic subset of the
irreducible source closure.  This is impossible.  Every relation not removed
by that necessary filter is one of the explicitly bound direct or restoration
relations above.  Equality of signatures alone is never promoted as overlap.

### 5.3 Restoration and arbitrary subdivisions

For one fixed full relation, let `Q_s` and `Q_t` be source and target rigid
supports and put `A=Q_s union Q_t`.  Every dummy role is filled by its actual
physical label in the full comparison.  Each restoration prefix is a direct
marginal of the original full containment; containment is never lifted from
a smaller marginal.  Suppressed edge classes map to effective parameters by

```text
y_C=product_(e in C) x_e,
```

whose differential is nonzero throughout the open cube.  Intersecting with
the generic constant-rank locus proves that every prefix marginal is a
source-relative open selected-model subgerm.

Once `A` is identified, each `A+p` probe locates the segment and interval of
an extra port, and each `A+p+q` probe orders a pair in one interval.  Every
probe restricts one fixed anchor transport.  The pair comparisons come from
actual total words and therefore assemble uniquely.  If a probe subdivides
a triangle edge it fixes the literal orientation; otherwise one unique
triangle persists and the same ordinary `T` choice applies to every probe.
The largest required probe has ten tensor ports.  Independent compact and
verbose implementations agree on 101,148 three-outgoing and 168,582
`theta-2` probe relations, and mutation tests reject broken parents,
transports, orders, and probe-dependent `T` choices.

This proves the left-to-right implication of (4) for arbitrary finite words.

### 5.4 Local converse

Labelled isomorphism is immediate.  For ordinary `T`, the three labelled
three-sunlet orientations have one exact common interior Fourier tensor and
rank four, the maximal normalized three-port JC rank.  Their normalized and
projective tensor images therefore share an open regular germ `U`.  The
constant-rank theorem supplies analytic physical sections `s_i:U->Theta_i`
for every orientation.

For an unchanged external context, including the complementary path of a
theta, write the common tensor contraction as `Phi(Q,C)` and let `d` be its
generic rank.  A nonzero `d`-minor of `D Phi` cannot vanish throughout the
nonempty open product `U x C`.  At a point where it is nonzero, the chain rule
applied to `(s_i(Q),C)` gives physical rank `d` for both orientations.
Shrinking there yields a common full-dimensional regular projective blob
germ.  This completes (4).

## 6. Global synthesis

Suppose `N preceq_JC N'`.  Section 3 gives the same labelled decorated bridge
tree.  Section 4 localizes the containment to every pair of corresponding
projective factors.  Section 5 forces each pair to be labelled-isomorphic or
ordinary-`T`-related.  Hence `N ~_T N'`.

Conversely, choose a common regular projective germ for every corresponding
pair: the identical germ for an isomorphism and the certified common germ for
`T`.  Shrink so that both sides have positive analytic incidence
representatives.  For each bridge choose one common effective scale in a
sufficiently small positive interval; after division by the two endpoint
normalizers, both physical bridge multipliers remain in `(0,1)`.  Different
bridges are independent because their incidence graph is a tree.  The local
germs therefore glue to one common full-dimensional regular global germ.
This proves (1) and the assertions following it.

## 7. Generic exceptional locus

For a fixed leaf set there are finitely many locked `S_TC` level-two
topologies: tree-child paths give `r<=n-1`, binary degree counting gives
`t=n+r-2`, and a rooted presentation has at most `4n-3` vertices.  For fixed
`N`, let `V_N` be its irreducible complex model closure and define

```text
E_top(N) = union over N' not T-equivalent to N of
           ZariskiClosure(M_N intersect M_N') inside V_N.
```

Every member is proper.  Otherwise the semialgebraic intersection has full
real dimension on a regular source stratum and hence nonempty relative
interior, contradicting (1).  Put `d_N=dim V_N`.  Enlarge this finite union
by the singular locus, the Zariski closures of images of parameter loci on
which the Jacobian rank is less than `d_N`, and the zero sets of the
observable Fourier cut-anchor and atlas-witness polynomials.  The rank-drop
images have dimension at most `d_N-1` in characteristic zero, and every
observable witness is nonidentically zero on its intended stratum.  No
physical-parameter factor is projected to distribution space.  The result
`E_N` is a proper algebraic subset of `V_N`.  For every
`p in M_N minus E_N`, any locked
`S_TC` level-two topology realizing `p` is `T`-equivalent to `N`.

This is the precise generic statement.  It does not say that the common
`T`-germ is dense in every complete stochastic sheet.

## 8. Structural reconstruction

Given an exact generic pattern distribution known to arise in the class:

1. Fourier-transform it.
2. Test split flattenings using (2), recover the complete compatible cut
   system, and construct the labelled reduced bridge tree.
3. Use `F` to distinguish ordinary degree-three components from
   three-sunlets.
4. Factor positive rank-one cut blocks and impose the analytic incidence
   normalizers to recover every projective local tensor orbit and every
   effective bridge scale.
5. On each nontrivial factor, evaluate the bounded graph-derived invariant
   deck and restoration certificates to identify one rigid support modulo
   `T`.
6. Use the common-anchor `A+p` and `A+p+q` probes to recover every segment and
   every total port order.
7. Put each triangle into the lexicographically least labelled `T`
   orientation and assemble the canonical standard semi-directed graph.

Every loop is finite, every local probe uses at most ten tensor ports, and the
algorithm terminates.  A direct implementation uses at most `2^(n-1)-1`
split tests and `O(n^10)` bounded local probes, excluding exact-number bit
complexity.  Thus no unproved polynomial-in-`n` complexity claim is made,
while the combinatorial count is polynomial in the length of the explicit
`4^n` input table.  Steps 2--6 and the local theorem prove
correctness and completeness outside `E_N`.

The algorithm returns the canonical topology modulo `T`.  To list which
orientations realize this particular distribution, test open-model
membership for the finite `T` variants.  It does not recover physical bridge
multipliers.

## 9. Sharpness

The frozen independent package `../s_tc_jc_sharp_boundary/` supplies, for
every `n>=4`, two networks in `W_TC minus S_TC` that are nonisomorphic and
not ordinary-`T`-equivalent, while their open JC images share a
full-dimensional regular region of dimension `2n`.  At four leaves the
certificate checks all 256 Fourier coordinates at a strict quadratic
interior point and nonzero rank-eight minors on both sides.  Identical leaf
substitution has a positive analytic inverse and gives the all-`n` result.

Combining that theorem with Sections 1--8 yields the sharp boundary:

```text
strongly tree-child standard level-two JC networks are generically
identifiable modulo ordinary triangle redirection, whereas the immediately
larger weakly tree-child class is not.
```

The weak pair is not a move inside `S_TC`; it is the exact sharpness witness.
