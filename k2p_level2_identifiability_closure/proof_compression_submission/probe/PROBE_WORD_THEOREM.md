# Coherent probe word theorem

## Theorem

Let \(A\) be a physical equality anchor on one of the six primitive
semi-directed support types

\[
\mathsf{Tree},\quad \mathsf{Cycle},\quad
\Theta_0,\quad\Theta_1,\quad\Theta_2,\quad\Theta_3.
\]

Suppose two physical K2P component presentations have the anchored relation
recorded for \(A\), and add arbitrary finite labelled attachment words to their
suppressed semi-directed mixed edges.  If the resulting component varieties
are in the directed relation under consideration, then the anchor transport
extends coherently to the attachment words:

1. each added label lies on the transported mixed-edge segment;
2. labels on the same segment have the same linear order;
3. incoming-boundary, reticulation-incoming, root-suppressed, and pendant-arm
   sites are all included;
4. any ambiguity from a support automorphism is exactly the action of a
   recorded labelled mixed-graph automorphism, not an extra attachment gauge;
   and
5. the only ordinary-triangle relation is the one already present in the
   anchor, transported with its common-reticulation arrowhead witness.

Consequently the complete one-/two-port closure reconstructs every arbitrary
attachment word.  There is no additional word exception table.

The theorem is uniform.  Its finite hypotheses are the exact corrected probe
ledgers, which remain load-bearing and are not replaced by this compression.

## 1. Objects and conventions

### 1.1 Suppressed mixed-edge sites

Delete the artificial root of a rooted presentation, retain every arrowhead at
a reticulation endpoint, and suppress the resulting unlabelled degree-two
vertices.  An attachment site is an edge of this semi-directed mixed graph.
The frozen enumeration represents the sites in four diagnostic classes:

- an unheaded core edge;
- a pendant arm;
- an edge entering a reticulation; or
- the single mixed edge obtained by suppressing the artificial root.

These names help audit the enumeration, but the invariant object is the mixed
edge together with its arrowhead endpoints.  Root movement can change a
diagnostic name.  Every claimed equality therefore carries an exact vertex
and mixed-edge map; no conclusion is inferred from site-type names alone.

For a component with \(k\) labelled boundaries and \(r\) reticulations, the
complete site count is

\[
  2k+3r-3.
\]

The input contract verifies this formula on both sides of all 176 anchors.
It contains 2,206 source sites and 2,206 target sites.

### 1.2 The root-suppressed and incoming sites

The two arcs leaving the artificial root are two rooted representatives of
one semi-directed mixed edge.  Subdividing either half and attaching a new
label gives exactly isomorphic semi-directed graphs after suppression.  The
352 half-equivalence checks certify this assertion on the two sides of every
anchor.  Thus root-adjacent attachments are neither omitted nor double
counted.

The existing incoming boundary and the core become the two endpoints of the
single root-suppressed mixed edge.  That site is therefore the complete
incoming-boundary attachment site; it is not counted again as a pendant arm.
The pendant-arm sites are the remaining labelled boundary arms.  Both the
incoming convention and the ordinary pendant operations are consequently
covered without omission or double counting.

### 1.3 Words

On every maximal core segment, list the attached boundary labels in path
order.  This list is the attachment word of the segment.  Attaching on a
pendant arm creates the corresponding subdivided arm/cherry operation;
attaching on a reticulation-incoming edge retains the arrowhead at the
reticulation.  We use “word” for the combined data of segment choice,
within-segment order, and these arm operations.

Because labels are arbitrary, any chosen new label or ordered pair of new
labels may be renamed to the canonical probe labels.  Hence the finite
one-/two-port calculation applies to every label or label pair in an arbitrary
larger component.

## 2. Exact finite premises

The word theorem uses the following corrected premises.

| Gate | Exact result |
|---|---:|
| physical anchor records | 176 |
| canonical anchor classes | 39 |
| isomorphic / ordinary-triangle anchors | 143 / 33 |
| one-port pairs | 29,964 |
| one-port equalities | 2,107 |
| canonical one-port equality classes | 469 |
| two-port pairs above equality parents | 544,571 |
| two-port equalities | 32,729 |
| reversed one-port marginals checked | 32,729 |
| exact labelled mixed-graph transports | 67,741 |
| exact parent restrictions | 4,379 |
| unresolved / incoherent | 0 / 0 |

Every nonrelation is separated in the following fail-closed order:

1. exact labelled isomorphism or ordinary triangle is tested first;
2. otherwise a displayed-quartet mismatch is sought;
3. otherwise \(T_i\) is pulled back on the original full Fourier maps over
   every triple and orientation, with coefficientwise zero on one side and an
   exact tensor-Bernstein strict sign on the other; and
4. failure to certify one of these outcomes is fatal.

There are 638 displayed-quartet certificate classes, 156 canonical whole-map
\(T_i\) relation certificates, and 118 strict-pullback polynomial classes.
Every \(T_i\) certificate has boundary-incidence weights \(s^2g,s^2g,g^2\)
on its three selected arms and zero on all other arms.  It therefore survives
the complete physical two-sector bridge action.

## 3. One-port segment lemma

**Lemma 1.** Fix a recorded anchor transport \(\phi:A\to A'\).  If the
one-port extensions \(A+p\) and \(A'+p\) have the directed relation, then the
new label subdivides a source site \(e\) and its exact transported target site
\(\phi(e)\).  The child transport restricts to \(\phi\) after deleting \(p\).

**Proof.** Marginalizing the child relation over \(p\) recovers the anchor
relation.  The labelled leaf \(p\) fixes its incident subdivision vertex, so an
exact child transport must map the subdivided source mixed edge to the
subdivided target mixed edge.  The complete one-port product tests every
source/target site pair.  All pairs other than the 2,107 exact equalities have
an exact quartet or full-map separator.  A relation cannot lie in a separated
row.  Every surviving row stores an exact transport and two parent restriction
certificates, proving the claim. \(\square\)

This lemma determines the segment of every added label.  It also covers
pendant arms, reticulation-incoming edges, and the root-suppressed edge because
none is removed from the site product.

## 4. Two-port order lemma

**Lemma 2.** Fix a surviving one-port parent \(A+p\to A'+p\).  If the
two-port extensions \(A+p+q\) and \(A'+p+q\) have the relation, their exact
transport restricts to the stored \(A+p\) transport.  Deleting \(p\) also
recovers a certified equality for the reversed one-port marginal \(A+q\).
When \(p\) and \(q\) lie on the same segment, their order is therefore the
same on both sides.

**Proof.** The two-port inventory takes the complete Cartesian product of
mixed-edge sites above every one-port equality parent.  Its 2,107 products
contain exactly 544,571 rows.  All nonrelations have exact separators.  Each
of the 32,729 equality rows contains an exact child transport restricting to
the chosen parent transport and a reversed-marginal certificate over the same
base anchor.  On a path, an incidence-preserving labelled mixed-graph map
cannot reverse only the interval between \(p\) and \(q\) while fixing the
parent endpoints and attachment incidences.  Thus the pair order agrees.
\(\square\)

The reversed-marginal condition matters: without it, a locally chosen
extension above \(A+p\) need not be compatible with the extension obtained by
starting from \(A+q\).  All 32,729 reversed checks pass and none is missing.

## 5. Arbitrary-word induction

**Lemma 3.** Lemmas 1 and 2 determine a unique transported word on every
segment, up to an automorphism already present at the anchor.

**Proof.** Marginalize an arbitrary component relation to the anchor together
with one extra label \(p\).  Lemma 1 determines the transported segment/site
of \(p\).  Repeat for every extra label.  For every pair \(p,q\) assigned to
the same segment, marginalize to \(A+p+q\).  The one-port marginal is a
survivor, so this pair is in the enumerated two-port universe; Lemma 2 fixes
the order of \(p,q\).

The source and target attachments are actual linear words.  Agreement of all
pairwise comparisons therefore gives the same total order.  Equivalently, one
may insert the labels successively: the two-port certificate fixes which
interval of the current word is subdivided, and its two parent restrictions
make the insertion independent of whether the older or newer label is
marginalized first.  Induction on word length proves the result. \(\square\)

No finite bound on the ultimate word length is used: at each induction step
only one label or one ordered pair is retained in addition to the fixed
anchor.

## 6. The six primitive supports

### Ordinary tree

The three-port tree identity anchor has no reticulation and five mixed-edge
sites.  Its one-/two-port products include all core and pendant operations.
Lemmas 1--3 therefore reduce to the usual recovery of paths, cherries, and
their linear subdivision order.

### Cycle

The cycle contributes 24 physical three-port anchors and 12 restored
four-port anchors.  Both its core edges and its incoming and pendant sites are
present.  The same segment/order induction applies; the restored anchors cover
the rigid presentations not represented by the minimal three-port state.

### \(\Theta_0\), \(\Theta_2\), and \(\Theta_3\)

For each theta kernel, the physical anchor inventory contains every repair and
restoration depth required by its rigid support.  Reticulation-incoming sites
are distinguished by their arrowhead endpoints, while unheaded paths and
pendant arms are enumerated separately.  Exact edge maps, rather than rooted
arc names, transport these sites.  Lemmas 1--3 apply segment by segment.

### \(\Theta_1\) and its parallel segments

The \(\Theta_1\) core has two parallel \(U\)-to-\(V\) segments.  The frozen
source universe has two repair presentations: source index 2 repairs segment
3, and source index 3 repairs segment 4.  The anchor contract contains eight
records for each presentation.

The two parallel segments are not merged by a site-type key.  Their mixed-edge
incidences, arrowhead endpoints, repair boundaries, and exact parent edge map
remain in every transport.  If an actual kernel automorphism exchanges the
parallel segments, it exchanges their full words as a block.  Once a labelled
attachment breaks that symmetry, the one-port subdivision fixes its image;
the two-port rows then fix the order on that chosen segment.  Thus parallelism
creates only the recorded support automorphism, not an unobserved word swap.

Together these cases cover the ordinary tree and all five non-tree kernels.

## 7. Automorphisms and transport choices

An anchor can admit more than one graph automorphism.  The proof does not
claim a unique vertex map before quotienting by that automorphism group.
Instead, fix a recorded exact anchor transport.  Each surviving one-port row
stores its extension, and each surviving two-port row stores an extension
restricting to the chosen parent.  A different initial choice differs by an
exact anchor automorphism and acts equivariantly on the site and word data.

This is why the exact edge-map registry is essential.  A cache keyed only by
kernel name or site type would collapse inequivalent choices.  The registry
contains 67,741 referenced transports with zero missing or unreferenced
records, and the 4,379 marginal restrictions give zero incoherent overlaps.

## 8. Ordinary triangles

An ordinary triangle here is a common-germ graph relation: three displayed
mixed edges with exactly two arrowheads entering one common reticulation on
each side.  It is not asserted to be an isomorphism or a polynomial symmetry.

Every one of the 3,745 triangle transports in the anchor, one-port, two-port,
and reverse-marginal registries carries the two headed edges, their common
reticulation, and the three triangle edges on both sides.  The closure creates
zero triangles above an isomorphic parent.  Hence an anchor triangle is
transported coherently through its attachment words, while no local probe can
introduce a second independent triangle.  This proves the recorded
one-global-triangle gate.

## 9. Conclusion and compression boundary

Lemmas 1--3, together with the six support cases, prove the theorem.  Quartet
and whole-map separators exclude every wrong segment or order; exact
restriction transports glue the surviving choices; bridge
multihomogeneity preserves the algebraic exclusions in physical components.

This gives a compact proof of arbitrary-word recovery.  It does not compress
the finite premises into a small hand table.  The exact residue remains:

- 176 physical anchor records;
- 29,964 one-port rows;
- 544,571 two-port rows;
- 67,741 exact transports; and
- 4,379 parent restrictions.

The bounded attempt found no smaller exact exception/archetype theorem that
implies these premises.  The correct submission status is therefore:

- word theorem: **proved from the frozen finite premises**;
- ledger compression: **`PC-PARTIAL`**;
- unresolved mathematical records: **zero**.

## Reproduction

From the project root:

```bash
.venv/bin/python proof_compression_submission/probe/verify_probe_word_theorem.py --check
```

The verifier streams every ledger, replays its ordered hash root, checks every
proof identifier, reconstructs the complete Cartesian products, validates all
parent/reverse restrictions, checks the exact transport registry and every
ordinary-triangle arrowhead witness, and rejects optimized mode.

Its live atlas dependency is scope-limited to the ordered six-source primitive
grammar, fingerprinted as
`cadbb4187f501ab53620b3f15deaccb60bed582dfe8fdbefd7c1ba10f5329047`.
The relation and transport claims come from the exact frozen ledgers themselves
and their independent current-atlas replays, so an unrelated atlas-kernel edit
does not silently relabel this reader-level proof.

Current coverage artifact:

- file SHA-256:
  `3791e4bb829976aa78289281b9998bfe0605ba4a20518f1e8dd660d7d1a91bb8`;
- logical payload:
  `1d4248028b38f6b731f066960d9e584240de68a17323539fe5b47f119a8086f6`.
