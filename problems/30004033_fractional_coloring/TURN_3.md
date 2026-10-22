# Turn 3: every triangle-free K4 subdivision and the planar tight-block reduction

## Purpose and disposition

We move from isolated path constraints to a complete compatible assignment around a four-branch-vertex core. A seven-template construction proves that **every triangle-free subdivision of K4 has an (8,3)-coloring**, so it satisfies the exact weighted 8/3 target. This includes arbitrarily long, mixed-parity edge subdivisions; it is not a bounded-order scan. The constant is sharp within this class, by the known eight-vertex K4+ graph from turn 2.

We also identify a planar limitation of turn 2's cross-port seam, and use that limitation to prove an exact K4+ reduction. The original all-graph conjecture remains unresolved, now 3/5 substantive author turns. No historical novelty is claimed for these elementary deductions. The path method is credited to the boundary-intersection approach discussed in SOURCE_GATE.md; the known K4+ graph and link-graph motivation are credited to the cited literature.

## 1. Integer form of the path extension theorem

In an (8,3)-coloring, every vertex receives three colors from {1,...,8}, with disjoint sets on adjacent vertices. Fix endpoint triples A,C of a path with L edges, and put t=|A intersect C|.

The proof of turn 1 works in a finite palette as well as in a nonatomic space. At its inductive step, the penultimate triple B is chosen from the disjoint sets A minus C and the complement of A union C. Their cardinalities are integers. If the previous path's feasible overlap interval is [ell,u] with integer endpoints, a suitable integer s exists precisely when the two closed integer intervals intersect. The interval recursion is therefore exact without any rounding issue:

    [ell_(L+1),u_(L+1)] = [max(0,1-u_L),3-ell_L],
    [ell_1,u_1]=[0,0].

Consequently the possible t are exactly

    L=1: {0};
    L=2: {1,2,3};
    L=3: {0,1,2};
    L>=4: {0,1,2,3}.

The recursion proves existence for **every prescribed pair** of endpoint triples with an allowed overlap. In particular, overlap 1 or 2 works for every path length at least two. This is the crucial common boundary condition.

## 2. Seven simultaneous branch-vertex templates

Let H be a triangle-free simple graph on four labeled vertices 0,1,2,3. We seek triples C_i such that

- C_i and C_j are disjoint if ij is an edge of H;
- their intersection has size 1 or 2 if ij is not an edge of H.

There are seven isomorphism types of such H. The following complete table supplies the triples; for example 123 means {1,2,3}.

| Type | Edges of H | C_0 | C_1 | C_2 | C_3 |
| --- | --- | --- | --- | --- | --- |
| empty | none | 123 | 145 | 167 | 128 |
| one edge | 01 | 123 | 456 | 147 | 248 |
| two adjacent edges | 01,02 | 123 | 456 | 457 | 146 |
| matching | 01,23 | 123 | 456 | 147 | 258 |
| star | 01,02,03 | 123 | 456 | 457 | 467 |
| path | 01,12,23 | 123 | 456 | 127 | 348 |
| 4-cycle | 01,12,23,03 | 123 | 567 | 124 | 568 |

Each entry is verified by its six pair intersections. Completeness of the list does not require a graph-generation assumption. With zero or one edge the type is forced; with two edges they either meet or are disjoint; with three edges a triangle-free graph on four vertices is a tree, hence a star or path; with four edges it must be a 4-cycle. Five or six edges contain a triangle. Equivalently, the seven types account for all 41 labeled triangle-free graphs on four vertices, with multiplicities 1,6,12,3,4,12,3 respectively.

## 3. The subdivision theorem and weighted consequence

**Theorem 6.** Every finite triangle-free subdivision of K4 has an (8,3)-coloring.

**Proof.** A subdivision here replaces each of the six edges of K4 by one positive-length path, with pairwise disjoint internal vertex sets and no other edges. Let H on the four branch vertices contain exactly those edges whose replacement paths have length one. H is triangle-free, since a triangle in H would be a triangle in the subdivision.

Assign the branch triples using the matching row of the seven-template table and a relabeling of vertices. Every length-one path has disjoint endpoint triples, as required. Every other path has endpoint intersection 1 or 2, so Section 1 extends the fixed endpoints along that path at its actual length. Carry out these six extensions independently. They agree at their branch endpoints and their internal vertices are disjoint. There are no other edges, so all edge constraints hold simultaneously. QED.

For any nonnegative vertex weights w, choose one of the eight colors uniformly and take all vertices containing it. The resulting set is independent and contains each vertex with probability 3/8. Its expected weight is exactly (3/8) times the total weight, so some such set has at least that weight. Thus the theorem supplies the full weighted/fractional statement for this graph class, not just its unweighted independence ratio.

This is genuinely beyond the already-known K4-minor-free class, but it does not cover all graphs containing a K4 subdivision: a graph with extra edges or vertices need not inherit a coloring of that subgraph. In particular, the six paths in the theorem may not have additional attachments or chords. The known K4+ graph is a member of this class and has chi_f=8/3 by turn 2, so the bound is sharp for the class.

## 4. The planar restriction on the previous cross-port seam

Recall K4+ with old vertices a,b,c,d, paths a-x-y-b and c-z-w-d, and cross edges ac,ad,bc,bd. In every plane embedding of K4, its four faces are triangles: Euler's formula gives four faces and the total face-boundary length is twelve. Opposite edges ab and cd share no face. Subdivision does not change which faces meet those edges. Therefore every face of K4+ meets degree-two ports only from {x,y} or only from {z,w}, never from both pairs.

If a connected outside graph is attached to K4+ without crossings, it lies within one face of the embedded K4+ subgraph and can attach only to vertices incident with that face. The old vertices a,b,c,d already have degree three, so a subcubic supergraph cannot attach anything there. Hence no outside connected component can touch both port pairs. A direct added edge between the two pairs is excluded by the same face argument.

This limits the usefulness, within the planar target, of turn 2's universal **cross-port** two-edge attachment. For a connected outside graph that attachment cannot be planar. The turn-2 theorem remains correct under its explicit planarity qualification, but it must not be promoted as a general nontrivial planar gluing mechanism. The separation itself is more useful here.

## 5. An exact planar K4+ reduction

We use a standard fractional-coloring gluing fact. If two colorable pieces intersect in a clique of size at most two, their equal-density fractional colorings can be aligned on that clique. For an edge, the two disjoint endpoint sets have respective measures r,r, with complement measure 1-2r, so their three membership-pattern probabilities are identical in both pieces. Couple their remaining color patterns conditionally on these three states. For one vertex use its two states. With rational finite palettes the same argument is a common-denominator refinement and a color permutation aligning the prescribed disjoint sets. This preserves every vertex marginal and every edge constraint.

**Proposition 7.** Suppose a finite planar triangle-free subcubic graph G contains a subgraph K isomorphic to K4+. Let

    H = G minus {a,b,c,d}.

If H is fractionally 8/3-colorable, then so is G.

**Proof.** The four ports remain in H, including the edges xy and zw. By Section 4 they lie in different connected components of H: otherwise a path outside the old vertices would give an outside connection between the two port pairs. Every H component meets K either in {x,y}, in {z,w}, or not at all. Each nonempty intersection is a clique, and no further edge between the pieces exists. (Additional edges between the two port pairs would already violate the same plane-face argument.)

Color K at density 3/8 by turn 2 or Theorem 6. Color every H component at that density, trimming if necessary. Glue each H component to K along its indicated edge using the preceding equal-pattern coupling. Components otherwise have disjoint vertices and can be coupled conditionally independently given their boundary states. This yields a coloring of all of G at density 3/8. QED.

Thus a vertex-minimal counterexample to the original planar conjecture cannot contain K4+ as a subgraph: H is a smaller graph in the same class, and the proposition would extend its coloring. This conclusion does not exclude every K4 subdivision or every other cubic planar core.

The planar separation resembles the link-graph reductions in Heckman--Thomas (2006), Section 3, particularly Lemma 3.3 and the following unweighted reduction. The present argument uses exact equal-marginal clique gluing; it does not assume that their unweighted independent-set construction automatically proves a weighted bound.

## 6. Verification and remaining gap

`turn3/check_templates.py` checks all seven six-pair tables, classifies all 41 labeled triangle-free graphs on four vertices, and constructs exact path colorings for every required endpoint pair through length 15. It checks 4,476 assertions. The saved classification maps are a reproducible finite certificate, while the integer path induction handles all lengths. No all-graph computational scan is claimed.

The remaining obstacle is a general compatible coloring law for larger cubic planar cores with interacting attachments. The seven-template construction handles a graph that is itself a K4 subdivision, not an arbitrary graph having such a subdivision. The K4+ reduction removes one tight block, not every tight configuration. Original target remains unresolved 3/5. Current subjective completion estimate toward a full proof: 20%, low confidence; this is not a mathematical guarantee or a fraction of the conjecture proved.
