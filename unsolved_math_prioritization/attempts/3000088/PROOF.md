# Local packing synchronization: verified restricted results and obstructions

## Scope and status

This AI-assisted manuscript is unrefereed. Acceptance means an independent internal AI audit. No external human peer review, journal acceptance, or formal proof-assistant certification is claimed.

The complete analytical proofs, parameterized construction formulas, and the full frozen b=3 construction are retained. This is not a computational reproduction package: raw assignment tables, certificate packages, detailed instance records, generated grid realizations, checker programs, copied source documents and images are omitted. The seven central graph instances are mathematically specified by the retained all-b families and frozen construction, but the stored certificate realizations and the other finite grid/control inputs cannot all be reconstructed from this edition alone. Historical finite checks support the proofs; no universal theorem depends on those computations.

The Chung–Ross target is the following. For a finite bipartite multigraph with edge weights in [0,1], let b be the maximum, over vertices, of the optimal number of unit bins needed for the incident weights. For b >= 1, must there be a weighted edge coloring using at most 2b-1 colors? A color is feasible when its incident weight at each vertex is at most one. Adjacent edges may have the same color.

This note does **not** resolve that target. It gives complete elementary proofs for restricted graph classes, sharp examples for the simple-cactus restriction, and an obstruction to improving one local extension argument. The upper bounds are not presented as novel: the literature already addresses these classes. All mathematical arguments below are self-contained. No conclusion about current openness or priority follows from the bounded literature check.

In algorithm statements, an integer B >= 1 and a feasible partition of every incident edge set into at most B bins are **supplied inputs**. The synchronization algorithms do not compute optimal bin packing. Taking B=b gives existential statements; it is not a polynomial-time algorithm for obtaining b. Rational supplied data permit exact finite arithmetic. The proofs themselves allow arbitrary real weights.

The simple support of a loopless multigraph has one edge for every adjacent vertex pair, regardless of multiplicity. A multigraph with forest support can contain two-edge cycles. A forest without qualification below is a simple acyclic graph. Empty graphs have weighted chromatic index zero; with supplied B>=1, the algorithms color no edges. Isolated vertices cause no problem. Zero-weight edges may remain in the supplied bins throughout; empty bins can be discarded. For a nonempty all-zero instance we use one color and B=1. Equivalently, zero edges can be added after coloring the positive-weight edges, whenever a palette is nonempty.

## 1. Simple forests need exactly the local bin bound

**Lemma 1.** A weighted simple forest with supplied local B-bin packings has a B-coloring. Consequently, its weighted chromatic index is b when b is positive.

**Proof.** Root every tree component and process parents before children. At a root, label its local bins with distinct colors from a common B-color palette, and give each incident edge its bin's color. When processing a non-root vertex v, exactly one incident edge, the edge to its parent, has already been colored. Permute the labels on the supplied local bins at v so that the bin containing this parent edge receives its existing color. Label the remaining bins injectively with the remaining colors and color the edges to children accordingly. All edges assigned a given color at v lie in one feasible bin. Every child has only its parent edge colored so far, so its interim load is at most one. Induction completes all components with the same palette. Any weighted coloring at a vertex is a packing of its incident weights into color bins, proving the lower bound b. QED.

## 2. Forest support with arbitrary parallel bundles

**Theorem 2.** A loopless weighted multigraph whose simple support is a forest has a weighted (2B-1)-coloring from supplied local B-bin packings. In particular, it satisfies the Chung–Ross target with B=b.

**Proof.** Root each component of the simple support. The parallel edges between a parent and child form their bundle. Use a fixed palette of 2B-1 colors and process parents before children. Maintain these two properties:

1. The coloring is feasible on all edges colored so far.
2. Every colored parent–child bundle uses at most B colors.

At a root, restrict its supplied packing to the edges going to children (these are all its edges), label its at most B bins with distinct colors, and color them. Each child receives a subset of each feasible root bin; hence its interim loads are feasible. The bundle invariant holds.

Now process a non-root vertex v. Only its parent bundle is already colored. Let q <= B be the number of colors used by that bundle at v, and write their loads as x_1,...,x_q. Restrict the supplied local packing at v to all edges going to children, discard empty bins, and let their number be r <= B with loads y_1,...,y_r. Each x_i and y_j lies in [0,1]. Moreover,

    sum_i x_i + sum_j y_j = total incident weight at v <= B.

If q+r <= 2B-1, label the r outgoing bins by distinct colors absent from the incoming bundle. This is feasible.

Otherwise q=r=B. Choose an incoming color of minimum load x_min and an outgoing bin of minimum load y_min. Averaging gives

    x_min + y_min <= (sum_i x_i + sum_j y_j)/B <= 1.

Give that outgoing bin the selected incoming color. Give each of the other B-1 outgoing bins a different color absent from the incoming bundle. Exactly B-1 such colors are available, and the only merged color has load at most one at v.

In either case all outgoing bins receive distinct colors. Thus every child bundle uses at most B colors. At a child, each color is represented by a subset of one outgoing bin at v, so its interim load is at most one. Earlier vertices are unchanged. This proves both invariants inductively. The procedure terminates on a finite forest and works component by component. It never assumes an upper bound on parallel multiplicity and does not require positive weights. QED.

**Why this does not prove the general conjecture.** In a support forest a vertex has only one previously colored neighbor. In a graph with support cycles, previously colored bundles can use unrelated sets of B colors, so their union need not satisfy q <= B. The invariant used in the proof is then unavailable. Replacing b by the ceiling of maximum weighted degree is also not justified by the supplied-packing argument.

## 3. A sharp distinction between a forest and forest support

**Proposition 3.** For every integer b >= 2 there is a bipartite multigraph with forest support, local bin bound b, and weighted chromatic index b+1. In particular, the 2b-1 upper bound in Theorem 2 is attained at b=2. This is not a claim that 2b-1 is sharp for this class at all b.

**Construction.** Start with vertices u,v,p,q,r. Put two parallel edges of weight 2/5 between u and v; one edge up of weight 1; and edges vq,vr of weight 3/5. Finally add b-2 parallel unit-weight edges between u and v. Its support has edges uv,up,vq,vr and is a tree; the graph is bipartite.

At u, place the two 2/5 edges together, and every incident unit edge alone: this uses b bins. Its incident unit edges plus any positive small edge also prove a lower bound of b. At v, the b-2 unit edges each need a bin, and each 3/5 edge can share a bin with one 2/5 edge, giving exactly b bins. Leaves have bin bound one.

Suppose b colors suffice. The b-2 unit uv edges use distinct colors and forbid every other positive edge at u or v from those colors. Only two colors remain for the five base edges. The unit up edge forces the two 2/5 uv edges to have the same other color. At v, the two 3/5 edges must have different colors, so one shares the 2/5 pair's color, creating load 7/5 > 1. This is impossible.

A (b+1)-coloring is explicit. Give the b-2 unit uv edges their own colors. Use three further colors a,c,d: both 2/5 edges get a; up and vq get c; vr gets d. All loads are at most one. QED.

For b=2, a separately retained finite certificate historically checked all 32 labeled 2-color assignments. Its assignment rows and load records are omitted. The complete construction and analytical lower/upper proofs above establish the claim for every b>=2 without that certificate.

## 4. The simple-cactus bound and its sharpness

A simple cactus is a simple graph in which every edge belongs to at most one simple cycle. It need not be bipartite in the upper-bound argument. The sharp examples below are bipartite.

**Lemma 4.** A finite simple cactus has a matching M that contains exactly one edge of each cycle, with G-M a forest.

**Proof.** Its blocks are bridges and simple cycles. Form the incidence graph with a node for every block and every original vertex, joining a block to the vertices it contains. This incidence graph is a forest. Root each connected block-incidence tree at an arbitrary original vertex. Each cycle block has an attachment vertex nearest that root. Choose an edge of that cycle not incident to its attachment vertex; such an edge exists because a simple cycle has length at least three.

Distinct cycle blocks are disjoint or share exactly one cut vertex x. If they share x, at most one of them can be the block on the root side of x; every other such cycle has x as its attachment vertex. Their chosen edges therefore avoid x. Thus no two chosen edges share a vertex, so they form a matching. Every cycle block loses one edge. Since the blocks of a cactus contain all its cycles, deleting the chosen edges leaves a forest. QED.

**Theorem 5.** A weighted simple cactus with supplied local B-bin packings has a (B+1)-coloring. If b=1, one color suffices. For every b>=2 the maximum weighted chromatic index over bipartite simple cacti with local bound b is exactly b+1.

**Upper bound.** Choose M by Lemma 4. Restrict the local packings to G-M. Apply Lemma 1 with the original B-color palette, whether or not the restricted optimum has fallen. Give every edge of M one additional color. Since M is a matching and every weight is at most one, the additional color is feasible. If b=1, every vertex has total incident weight at most one, so coloring all edges alike works. QED.

**Sharpness construction and proof.** Use a four-cycle with vertices v0,v1,v2,v3 in order and edge weights 3/5,3/5,1/5,1/5. At each of v0,v2,v3 attach b-1 new unit-weight pendant edges. At v1 attach b-2 such edges. This is a simple bipartite unicyclic graph.

At v0,v2 the two cycle weights sum to 4/5, and at v3 they sum to 2/5. Thus their cycle edges occupy one local bin, in addition to their b-1 unit bins. At v1 the two 3/5 edges require two bins, in addition to b-2 unit bins. Hence every cycle vertex has local optimum b.

In any b-coloring, each of v0,v2,v3 has b-1 unit pendants using distinct colors, leaving only one color for its two positive cycle edges. These three equal-color requirements force all four cycle edges to have the same color. Their load at v1 would be 6/5, a contradiction. For a (b+1)-coloring, alternate colors 0 and 1 around the cycle. At each vertex give its unit pendants distinct colors from {2,...,b}; there are enough colors, and no pendant meets a cycle color. QED.

The historical b=2 certificate checked all 128 labeled 2-color assignments. Its assignment rows and load records are omitted. The retained parameterized construction and proof establish every b>=2; finite computations alone do not establish that quantifier.

## 5. A frozen-bundle obstruction to saving a second color

**Proposition 6.** Even with b=3 and forest support, an already feasible coloring produced by an optimal local packing at a root may fail to extend to its child with 2b-2=4 colors, although the full graph has a 4-coloring. Thus a universal 4-color conclusion for this instance requires recoloring, rather than a second merge of outgoing bins into frozen incoming colors.

**Construction.** Between u and v put five parallel edges a1,a2,a3,a4,a5 of weights 20/100,21/100,20/100,21/100,1/100. At u add three pendant edges s1,s2,s3 of weights 59/100,59/100,99/100. At v add three pendant edges t1,t2,t3, each of weight 60/100.

The following optimal local packing at u fills three bins exactly:

    {a1,a2,s1}, {a3,a4,s2}, {a5,s3}.

At v, a three-bin packing is

    {t1,a1,a3}, {t2,a2,a5}, {t3,a4},

with loads 1,82/100,81/100. The three weights greater than 1/2 at each of u and v prove that three bins are necessary. Therefore b=3.

Freeze the colors of the three root bins as 0,1,2. The incoming color loads at v are 41/100,41/100,1/100. Each outgoing edge has weight 60/100, so neither color 0 nor color 1 can receive any outgoing edge. Only colors 2 and 3 are available in a four-color palette. Since two outgoing edges have combined weight 120/100>1, three of them require three colors. Extension is impossible. Five colors suffice by giving one outgoing edge color 2 and the other two fresh colors 3 and 4.

Recoloring avoids the obstruction: assign all five uv edges color 3, the three u-pendants colors 0,1,2, and the three v-pendants colors 0,1,2. The uv bundle has total weight 83/100, so this is a valid 4-coloring.

For completeness, the full graph is not 3-colorable. The 99/100 pendant at u must have a different color from the two 59/100 pendants; it can share a color with no uv edge except the 1/100 edge. The four other uv edges must fit alongside the two 59/100 pendants in capacities 41/100 each. Their total is 82/100, so each such color receives exactly 41/100. The 1/100 edge then must accompany the 99/100 pendant. Hence every 3-coloring at u induces exactly the frozen load pattern at v, up to permutation. Each of the three 60/100 edges at v needs a distinct color, but only the 1/100-loaded color is feasible. Contradiction. Thus this full graph has chromatic index exactly 4. QED.

This is an obstruction to a specified proof strategy, not to Chung–Ross: 4 <= 2b-1=5. The historical extension certificate rejected all 4^3=64 assignments to the three outgoing edges with the root colors frozen. Its assignment rows are omitted; the full eleven-edge construction, root and child packings, capacity argument, five-color extension and four-color recoloring are retained above as an analytical proof.

## 6. Literature attribution and limitations

- Khan and Singh, *On Weighted Bipartite Edge Coloring*, FSTTCS 2015, pp. 136–150, [publisher source](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.FSTTCS.2015.136), state the exact bin-packing conjecture and the general asymptotic 20b/9+o(b) progress. Those bounds do not prove 2b-1.
- Feige and Singh, *Edge Coloring and Decompositions of Weighted Graphs* (2008), [public PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2008/09/edgecoloring.pdf), distinguish the bin-packing conjecture from its stronger weighted-degree formulation. Their retained paper also identifies known restricted-weight cases. The present examples mix weights above and below 1/2.
- Sannyasi, *Improved Approximation Algorithms for Weighted Edge Coloring of Graphs*, [arXiv:2012.15056v1](https://arxiv.org/abs/2012.15056v1), Theorem 10, explicitly states b+1 for simple graphs with edge-disjoint cycles. Theorem 11 states a 1.693b+12 bound for multigraph trees. The PDF's offline sections were inspected; these statements are prior claims, not claims of a full independent audit of that paper. The proof of Theorem 5 above is a separate matching-deletion argument.
- Huc, *Weighted-Edge-Coloring of k-degenerate Graphs and Bin-Packing*, Journal of Interconnection Networks 12 (2011), pp. 109–124, [DOI](https://doi.org/10.1142/S0219265911002861), has an indexed abstract stating that it treats the conjecture for multigraphs with underlying tree. The indexed formula is missing, and the primary publisher access failed. Its exact theorem and proof were therefore not independently inspected. This is sufficient reason to avoid claiming novelty for Theorem 2; it is not a substitute for a precise theorem citation.

The unrestricted Chung–Ross target remains unresolved by this work. No novelty, priority, or comprehensive current-openness claim is made. No full-conjecture counterexample or proof is supplied. No novelty claim is made for these proofs, examples, or obstructions. No source program, source archive, or third-party verification executable was used.
