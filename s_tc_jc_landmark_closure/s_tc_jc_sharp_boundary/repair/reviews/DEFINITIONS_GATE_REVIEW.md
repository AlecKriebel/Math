# Definitions gate and 2-sub-blob review

Date: 2026-08-09  
Scope: graph conventions only; the manuscript was not modified  
Release status: **FAIL — Gate D remains open**

Path convention: references beginning `AUDIT/` resolve under
`/Users/alec/Documents/Math/strong_level2_phylo_identifiability/`; all other
relative paths resolve from this repository root.

## Executive verdict

The load-bearing conclusion splits in two.

1. **VERIFIED AFTER CORRECTION.** The cyclomatic argument in
   `AUDIT/STANDARD_JC_FINAL_CLOSURE.md` §3 is valid for an *operational
   two-terminal subgraph*: a connected induced subgraph with exactly two
   external incident edges in total, one at each boundary vertex, whose
   contraction therefore creates an unlabelled degree-two vertex.  In a
   simple binary level-2 network the only possible whole-blob case is
   `K4` minus the edge between the two boundary vertices.  An independent
   complete rooting census finds 25 LSA-valid binary acyclic rootings and
   zero tree-child rootings.  No such operational suppressible gadget can
   occur in the locked strong class.

2. **FALSE AS A CLAIM ABOUT THE LITERAL PRIOR-WORK DEFINITION.** Brits et
   al., §5.1, define a 2-sub-blob by *two vertices of `W` adjacent outside*;
   they do not say that the edge boundary has size two.  Those conditions do
   not imply that contraction creates a degree-two vertex.  A strongly
   tree-child binary 4-sunlet gives a finite exact counterexample: for two
   adjacent cycle vertices `W={v0,v1}`, the literal three conditions hold,
   but four edges leave `W`, so the contracted vertex has degree four and
   ordinary suppression is undefined.  The closure note silently replaces
   this literal definition by the stronger two-edge condition.

Accordingly, the §3 lemma does **not** presently reconcile the manuscript
with every object called a “2-sub-blob” in the cited source.  It does close
the actual two-port/non-root-blob obstruction used by Sullivant.  The paper
must define the operational two-edge notion itself and avoid claiming it is
identical to the literal Brits definition.  If the theorem is intended to
use the broader prior-work quotient, its safe current scope is the explicitly
2-sub-blob-reduced class described below, or else its equivalence relation
must include well-defined 2-sub-blob suppression in addition to triangle
redirection.

There is a second independent convention failure: the manuscript's undefined
“standard parallel root artifact” rewrite admits a Brits-style exhaustive
root/parallel/degree-two reading, while its word “ordinary” also admits a
narrow reticulation-preserving reading.  Under the broad reading, an exact
LSA-valid binary level-2 rooted counterexample reduces to an ordinary two-leaf
edge while its rooted presentation is not tree-child, contradicting use of the
narrower Englander local criterion.  Under the narrow reading that rooted DAG
is simply not an admissible preimage.  The paper must choose and formalize the
latter before the local criterion, generator list, or sharp boundary can be
promoted.

## Ranked findings

### P0 — the lemma proves a narrower two-edge notion, not the literal prior-work 2-sub-blob class

**Status: FALSE AS A PRIOR-WORK EQUIVALENCE / LOAD-BEARING**

The source definition says:

- `B=N[W]` is connected;
- `B` contains no globally cut edge; and
- `W` contains exactly two vertices adjacent to `V\W`.

See the extracted primary-source text at
`AUDIT/PRIOR_WORK/brits_full_identifiability_v2.clean.txt:1335-1346`.
The same page then says to contract `B` and suppress the contracted vertex.
Nothing in the three conditions bounds the number of external edges incident
with either boundary vertex.

By contrast, the candidate closure lemma explicitly defines “suppressible”
as exactly two external attachment edges at
`AUDIT/STANDARD_JC_FINAL_CLOSURE.md:125-128`, and its degree sum
`2|E(B)|=3|W|-2` at lines 132-138 uses precisely that stronger hypothesis.
The final sentence at lines 171-173 acknowledges the distinction but does not
explain that it has narrowed the cited term.

This is not a pedantic possibility.  Let the ambient network be the standard
semi-directed 4-sunlet

```text
v0--v1--v2--v3--v0,
vi--Li  (i=0,1,2,3),
v1 -> v0 <- v3.
```

It is a simple binary level-1 topology.  Each arrow tail has two incident
undirected edges, so it satisfies the cited local strong criterion.  A rooted
LSA-valid tree-child witness is

```text
rho->v2, rho->L2,
v2->v1, v2->v3,
v1->v0, v3->v0,
v0->L0, v1->L1, v3->L3.
```

For `W={v0,v1}`, `N[W]` is connected, its sole internal edge is not a global
cut edge, and exactly the two vertices in `W` have neighbours outside `W`.
But the four edges

```text
v0-v3, v0-L0, v1-v2, v1-L1
```

leave `W`.  Contraction gives degree four, not degree two.  Thus the literal
definition and the operational suppression rule are not equivalent even
inside a strongly-tree-child simple binary phylogenetic network.

This example does **not** show a new JC model equivalence: the suppression
operation asserted by the literal wording is not defined in the ordinary
degree-two sense.  It does show that the candidate paper cannot use the
literal prior-work definition as a completed load-bearing quotient without
an additional incidence hypothesis.

### P0 — the parallel-artifact rule is ambiguous, and its broad reading is incompatible with the local `S_TC` criterion

**Status: UNRESOLVED / LOAD-BEARING**

The manuscript's reduction at `source/paper/sections/02_definitions.tex:7-9`
suppresses the root, says that a “standard parallel root artifact” is
“resolved,” and then suppresses unlabelled ordinary degree-two vertices.  It
does not define either the parallel rewrite or whether a former reticulation
that loses an arrowhead may become suppressible.  Its admissible rootings at
lines 13-15 are all binary DAG preimages under that unspecified reduction.
The local criterion at lines 29-37 is imported from a narrower convention in
which the semi-directed network is obtained by undirecting ordinary edges and
suppressing the former root, while the resulting network is already simple.

The following rooted DAG is an exact counterexample to the *broad* reading
combined with “every rooted preimage”:

```text
rho->a, rho->r1,
a->r1, a->b,
r1->r2, b->r2,
b->L1, r2->L2,
```

where `a,b` are tree vertices and `r1,r2` are reticulations.  It is binary,
acyclic, has no parallel directed arcs, its root is the LSA, and its one
nontrivial blob has cycle rank two.  It is not tree-child because `r1` has
reticulation child `r2`.  Broad root suppression creates a parallel edge;
parallel identification followed by exhaustive degree-two suppression
reduces the graph to the plain labelled edge `L1-L2`, whose mixed graph has
no outgoing retained arrow and hence vacuously satisfies the local criterion.

Under Englander et al. Definition 2.2 this rooted DAG is not a rooting of that
plain edge: suppressing only the former root first creates a forbidden
parallel mixed graph.  Under the broader Brits reduction it is.  If
“ordinary” in the manuscript means that every reticulation vertex and
arrowhead must survive, then the counterexample is excluded, but the parallel
rewrite still needs an exact rule showing this.  The current text does not
choose between the two conventions.

Required correction: define separate maps.  A defensible choice is

- `sd_0`: the reticulation-preserving semi-deorientation/root suppression
  used to define admissible rootings and `S_TC`; only rooted partners whose
  result is already a valid simple binary mixed graph are admitted; and
- `red_*`: any broader displayed-network/restriction cleanup that identifies
  root-created parallels and suppresses later degree-two artifacts.

Do not quantify `S_TC` over arbitrary preimages of `red_*`.

### P1 — LSA is absent from the manuscript's rooted definition and admissible-rooting definition

**Status: CONVENTION-DEPENDENT**

Both primary network definitions require the root to be the lowest stable
ancestor: see
`AUDIT/PRIOR_WORK/englander_level2_v4.clean.txt:261-273` and
`AUDIT/PRIOR_WORK/brits_full_identifiability_v2.clean.txt:102-116`.
The manuscript's rooted definition at
`source/paper/sections/02_definitions.tex:5` does not.  Its admissible-rooting
definition at lines 13-15 does not restore the condition.

Tree-child rooted networks automatically satisfy the LSA condition: follow
tree-or-leaf children from the two root children; the two resulting ordinary
paths cannot merge below the root because ordinary vertices have indegree
one.  That observation does not remove the omission from `S_TC`, which
quantifies over non-tree-child candidate rootings too.  “Admissible” must
explicitly require an LSA root.

### P1 — the blob and generator wording must distinguish edge-blocks, vertex blocks, and port-bearing degree-two vertices

**Status: VERIFIED AFTER CORRECTION / EDIT REQUIRED**

The primary sources define a blob as a maximal connected subgraph without
global cut edges (Sullivant says “2-connected” and immediately glosses it as
not disconnected by deleting an edge).  The manuscript says “maximal
biconnected subgraph” at `source/paper/sections/02_definitions.tex:43` without
specifying vertex- or edge-biconnectivity.

For a simple binary standard topology the distinction does not create an
extra core: a bridge-free connected subcubic graph cannot have an articulation
vertex, since each of two incident bridge-free blocks would require two
incidences at that vertex, forcing degree at least four.  This equivalence
should be stated rather than assumed.

The core proof at `source/paper/sections/06_support.tex:15-35` first suppresses
only *unported* degree-two blob vertices, then says every remaining core vertex
has degree three.  A port-bearing binary tree vertex has degree two within the
blob and one external bridge, so that sentence is false literally.  The cubic
calculation applies to the unported kernel obtained after temporarily
contracting all degree-two path vertices while recording ports as ordered
subdivision marks.  The generator conclusion is repairable, but the two
objects must be named separately.

### P1 — the prose proof of the `K4-e` case includes a nonexistent external-root subcase

**Status: VERIFIED AFTER CORRECTION**

The conclusion is correct, but the case split at
`AUDIT/STANDARD_JC_FINAL_CLOSURE.md:157-166` is not the clean proof.  When the
two nonadjacent reticulations are the degree-two attachment vertices, an
external bridge cannot enter either reticulation: the other incoming parent
would provide an alternate root-to-parent route and make an incoming
reticulation edge non-bridging.  Therefore no root-outside presentation exists
for that reticulation pair.  The independent census agrees: all five valid
nonadjacent-pair presentations have the root on one of the five internal
edges, and each has a tree vertex whose two children are reticulations.

For adjacent reticulations, all 20 valid presentations retain a
reticulation-to-reticulation edge and fail by a reticulation child.  Proposed
root insertion on their common edge does not complete to an LSA-valid binary
acyclic orientation in this whole-blob attachment pattern; it need not be
treated as a surviving mixed graph.

## Detailed audit of Lemma 3.1

### Exact hypotheses needed

Let `N` be a finite simple binary standard mixed graph after the narrow
semi-directed reduction, and let `B=N[W]` be nontrivial.  The proof needs:

1. every vertex of `W` is an unlabelled internal cubic vertex of `N`;
2. `B` is connected;
3. every edge of `B` is non-cut in `N`;
4. exactly two edges of `N` have one endpoint in `W`;
5. those two edges meet two distinct vertices of `W`; and
6. the blob containing `B` has cycle rank at most two.

Hypothesis 4, not merely “two boundary vertices,” is the essential one.
Hypothesis 5 is what makes the contracted vertex an ordinary two-valent
vertex rather than a loop/parallel artifact requiring a separate rule.

### Cyclomatic count

Under 1, 4, and 5, the internal degree sum is exactly

```text
2|E(B)| = 3|W| - 2.
```

Since `B` is connected,

```text
beta(B) = |E(B)|-|W|+1 = |W|/2.
```

Thus `|W|` is even and a nontrivial `B` has `beta(B)>=1`.  Since the
containing level-2 blob has cycle rank at most two, only `|W|=2` or `4` can
occur.  This arithmetic is exact.

The closure note says the cycle rank of an orientable binary blob “equals its
reticulation number.”  Equality is standard here, but the proof needs only
`beta(H)<=r(H)<=2`, which follows by deleting one incoming edge per
reticulation.  Using the weaker inequality avoids importing an unnecessary
equality claim.

### Proper-subblob case

If `B` is proper in its containing no-cut-edge blob `H`, both boundary edges
belong to `H`; otherwise `B` itself is separated from the rest of `H` by a
cut edge and is the whole relevant blob.  The no-cut-edge property provides
an attachment-to-attachment path in `H` whose interior lies outside `W`.
Adding that path to connected `B` contributes at least one independent cycle,
so

```text
beta(B)+1 <= beta(H) <= 2.
```

Therefore `beta(B)=1`, `|W|=2`, and `|E(B)|=2`.  This is a parallel pair,
excluded by a simple mixed graph.  The proper case is valid once the
two-edge boundary and the meaning of containing blob are explicit.

### Whole-blob cases

If `B=H`, then:

- `beta(B)=1` again gives two vertices joined by two parallel edges;
- `beta(B)=2` gives four vertices, five edges, and degree sequence
  `(2,2,3,3)` within `B`.

There is a unique simple graph with that degree sequence: `K4` minus the edge
between the two degree-two boundary vertices.  An independent enumeration of
all six reticulation pairs, both external root-entry choices, all five
internal root-edge choices, and every orientation of the remaining core edges
performed 864 raw orientation attempts.  Exactly 25 are binary and acyclic;
all 25 have the root as LSA; none is tree-child:

| root mode | reticulation pair | valid | failure |
|---|---:|---:|---|
| external | adjacent | 4 | reticulation child |
| internal | adjacent | 16 | reticulation child |
| internal | nonadjacent attachment pair | 5 | a tree/root vertex has only reticulation children |

The five internal root sites contribute `4,4,4,4,5` valid presentations; the
two external sides contribute two each.  The census imports no atlas,
canonicalizer, or discovery graph code.

### Lemma status

| statement | status |
|---|---|
| No exact-two-external-edge operational 2-sub-blob occurs in the simple binary standard `S_TC` level-2 class | **VERIFIED AFTER CORRECTION** |
| No object satisfying the literal Brits 2-sub-blob definition occurs in that class | **FALSE** |
| Every literal Brits 2-sub-blob contracts to an ordinary degree-two vertex | **FALSE** |
| The manuscript may ignore all prior-work 2-sub-blob issues solely by citing closure-note Lemma 3.1 | **FALSE** |

## Automatic triangle exclusion

**Status: VERIFIED AFTER CORRECTION under the narrow simple convention**

For theta path lengths `l1<=l2<=l3`, two distinct triangle sums force either
`(1,1,2)` or `(1,2,2)`.  The first has two pole-to-pole edges and is a parallel
multigraph, so it is not a standard simple semi-directed topology.  The
second is the simple `K4-e` case exhaustively closed above.  The independent
path enumerator checks all triples through length 16 and finds no other case.

For completeness, the old pre-reduction `(1,1,2)` graph was also enumerated:
four edge-copy records reduce to two distinct rooted DAGs, and neither has an
LSA root or is tree-child.  It must nevertheless be described as a
pre-reduction parallel artifact, not as a standard topology excluded only by
tree-childness.

The reduction from an arbitrary level-2 blob to a cycle or theta kernel is
valid after correcting the port/kernel wording above.  In a binary subcubic
blob, edge-biconnected and vertex-biconnected notions coincide, preventing a
figure-eight multi-triangle exception.

## Theta sharpness membership

**Status: VERIFIED AFTER CORRECTION**

Adding the LSA requirement does not remove the inherited Theta sharpness pair.
For each labelled topology, independent enumeration finds five admissible
binary rootings; all five have an LSA root, two are tree-child, and three are
not.  The tree-child root sites are the `A-C` and `A-F` edges.  Thus the pair
still lies in `W_TC \ S_TC` under the narrow standard convention.

This membership statement does not repair the positive theorem; it only shows
that the advertised weak/strong sharpness example survives the corrected LSA
filter.

## Required theorem repair

### Preferred reduced-class statement

Until the conventions are harmonized, the strongest safe positive theorem
should be stated for the explicitly reduced class

```text
C_red = {binary level-2 simple mixed graphs N such that:
  (i) N is obtained by the narrow, reticulation-preserving sd_0 reduction
      from at least one LSA-valid rooted binary network;
  (ii) S_TC quantifies only over those sd_0-rootings;
  (iii) all labelled leaves and every retained reticulation vertex survive
        sd_0;
  (iv) N contains no nontrivial connected induced B=N[W] for which
       every edge of B is globally noncut and contraction of B followed by
       ordinary degree-two suppression is well-defined; equivalently in the
       simple binary setting, the edge boundary delta(W) has exactly two
       edges at two distinct boundary vertices.
}
```

For this exact operational condition, the corrected cyclomatic lemma proves
that clause (iv) is automatic at strong level two.  Writing it into the class
still matters: it states the convention that the proof actually uses and
prevents the broader literal term from silently changing the quotient.

The candidate headline may then be:

> For networks in `C_red`, generic standard semi-directed JC topology is
> identifiable modulo ordinary triangle redirection, conditional on the
> remaining algebraic and global gates.

It must not currently say “all networks under the 2-sub-blob convention of
Brits et al.”

### Alternative quotient statement

If the intended object is the topology after prior-work 2-sub-blob cleanup,
define a deterministic, terminating reduction and state the theorem for its
reduced representatives.  The observational relation must then be enlarged:

```text
generated symmetric moves = T
  + every well-defined non-root-trapping 2-sub-blob suppression/inverse;

one-sided arrows = every well-defined root-trapping 2-sub-blob suppression
  in the direction certified by the model-containment theorem.
```

Confluence or canonical minimality of repeated suppression must be proved.
Root-trapping suppression cannot be put into a symmetric equivalence class:
the cited result gives containment and equal topological closure, not equality
of open model images.

### What is not acceptable

- Calling two boundary vertices “equivalently two external edges.”
- Declaring three- or four-edge-boundary sets “covered by the atlas” without
  separating that atlas fact from the prior-work suppression claim.
- Quantifying `S_TC` over broad artifact-reduction preimages while invoking
  the narrow local arrow-tail criterion.
- Treating the K4-e census alone as a proof about the broader literal
  2-sub-blob definition.

## Locked definition recommendations

1. **Rooted network.** Add the LSA condition and retain the prohibition on
   parallel directed arcs.
2. **Narrow semi-directed topology.** Undirect non-reticulation edges,
   preserve incoming reticulation arrowheads, suppress the former root once,
   and admit the rooted presentation only if the result is already the stated
   simple binary mixed graph after one explicitly specified root-edge rewrite.
3. **Artifact/restriction reduction.** Define separately any exhaustive
   parallel identification and degree-two cleanup.  State exactly how mixed
   arrowheads combine and reject conflicting patterns.
4. **Admissible rooting.** Require LSA, binary bidegrees, acyclicity, correct
   retained arrowheads, and exact inversion of the narrow reduction.
5. **Strong tree-childness.** Quantify over narrow admissible rootings.  Then
   the local criterion “each arrow tail has two incident undirected edges” is
   valid.
6. **Blob.** Use maximal connected subgraph without global cut edges, and
   state the subcubic equivalence with vertex-biconnected components.
7. **2-sub-blob.** Keep separate:
   - the literal two-boundary-vertex definition in Brits et al.; and
   - the operational two-external-edge gadget used in the cyclomatic lemma.
8. **Generator core.** Distinguish the cubic unported kernel from its ported
   subdivision, whose port-bearing vertices have blob-degree two.

## Independent replay

The standalone validator is
`repair/independent/definitions/validate_standard_definitions.py`.  It imports
only the Python standard library and no project Fourier engine, graph
generator, atlas, canonicalizer, invariant evaluator, or rank code.

Replay from the repository root:

```sh
python3 -m py_compile \
  repair/independent/definitions/validate_standard_definitions.py
python3 repair/independent/definitions/validate_standard_definitions.py
```

The `K4-e` rooting conclusion was also replayed through the separately written
C++ implementation:

```sh
c++ -std=c++17 -O2 \
  reproducibility/publication/review/review_multitriangle_exclusion.cpp \
  -o /tmp/stc_review_multitriangle_exclusion
/tmp/stc_review_multitriangle_exclusion
```

It independently reports `4` external, `21` internal, and `0` tree-child
rootings.

Key deterministic outputs:

```text
status: DEFINITIONS_GATE_FAILS_PENDING_CONVENTION_REPAIR
simple (1,2,2): 864 attempts, 25 LSA-valid rooted DAGs, 0 tree-child
literal 2-sub-blob witness: 2 boundary vertices, 4 external edges
operational two-edge gadget: unique K4-e candidate
broad-reduction witness: LSA-valid level-2 non-TC DAG -> plain L1-L2 edge
Theta N/N': 5 LSA-valid rootings each; 2 TC and 3 non-TC each
```

Hashes at this review stage:

```text
22a4f083ccd654e4f894c206063ec2ead76e76e83aa22b06b43317404997342f  repair/independent/definitions/validate_standard_definitions.py
9ee2ddba81524c73a5f3954e83843b89308ada6e5571a0f4b4c79becd10b8f05  AUDIT/STANDARD_JC_FINAL_CLOSURE.md
1dc74bfd98d370aa5bd638a95f835be501853123dfb70f2f5c1a694b3b198cdd  source/paper/sections/02_definitions.tex
2fad28a8983f9f68472165a36cdeb3ec3c80f3fc2bcf31787ce7ce04331a86a1  source/paper/sections/06_support.tex
260a977d9629eeb1b9ea0b7afa6d8179625609748ce20a2007927df5aa6e874f  AUDIT/PRIOR_WORK/englander_level2_v4.pdf
9ace8164beaf1bac82c5fd5b450df85b59adf5de5d57cd3832ba199a0a8fc5e2  AUDIT/PRIOR_WORK/brits_full_identifiability_v2.pdf
9d2d188f20c1325723621b2da5c231595033d3c9ddf30a232a429df4df6bc614  AUDIT/PRIOR_WORK/sullivant_graphical_models_v2.pdf
c9b0fc9de793a27b27952f880c741be44137e829b988974bc989e528f2c9c250  reproducibility/publication/review/review_multitriangle_exclusion.cpp
```

The validator hash must be regenerated after any subsequent reviewer-driven
change.

## Adversarial reviewer gate

**Status: VERIFIED**

A separate ephemeral Codex process ran in a read-only sandbox, used no web
search, and was instructed to falsify the cyclomatic split, the rooting
census, the 4-sunlet witness, the broad-reduction counterexample, and the
recommended repair.  It independently agreed that:

- the exact-two-edge lemma is sound;
- the literal cited definition is broader and the 4-sunlet refutes the claimed
  equivalence of boundary counts;
- this is a source-definition/scope defect, not itself a JC model
  counterexample;
- the broad reduction cannot define the rooting universe for the local
  `S_TC` criterion;
- the nonadjacent-reticulation external-root prose case is unnecessary; and
- the proposed reduced class must be advertised as a genuine scope
  restriction.

The preserved review is
`repair/independent/definitions/ADVERSARIAL_REVIEW.md` (SHA-256
`5ce7c0e316519c5a1ddc35868f7aba2469fa827911c40adca2cdf68ec5451a97`).

## Gate decision

**Gate D: FAIL / OPEN.**

The exact-two-edge 2-subblob obstruction is closed, and no operational
non-root-trapping two-port counterexample survives the strong simple binary
level-2 hypotheses.  But the manuscript and closure package do not yet lock a
single standard reduction/rooting convention, and the closure note's term
“2-sub-blob” does not match the literal cited definition.  The unrestricted
headline “all binary standard semi-directed `S_TC` level-2 networks modulo
`T`” must remain withheld.  The reduced-class theorem above is the maximal
definitionally defensible scope pending the other independent gates.
