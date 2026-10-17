# Root mathematical reconstruction: PR1118 / 30004231

Pinned head: 8592fb7297d3c4973f2778c47cfa8972cba896a6. Review started2026-10-17. This records the root's own deduction; independent geometry/topology adversaries remain pending. No mathematical acceptance or priority conclusion is presumed.

## Exact target

The primary OWR39/2019 report, printed2464 / physical70, Problem3, defines qualifying faces by positive dimensions of both summands and additive dimension. It asks shellability of the face-inclusion poset and rational homology of a wedge of (n-2)-spheres. No relative-general-position, facets-only or lattice restriction is stated. The proof's standard order-complex interpretation is the usual finite-poset realization. No artificial extrema are appended. Generic variants would be different claims.

For D=conv(v0,...,v4), v0=0, vi=ei, use P1=D×[0,1], P2=-D×[0,1] in R5. Both are full-dimensional lattice polytopes.

## Complete geometric argument

A nonzero base functional u induces a maximum index set A and minimum index set B on the five affinely independent vertices. They are nonempty and disjoint; any such pair is realizable by assigning values1,-1,0 and subtracting the value atv0. Thus all proper nonempty base faces of D-D are conv(vA)-conv(vB). Direction-space intersection is zero by affine independence on disjoint index sets, so dimension is |A|+|B|-2, and summand dimensions are |A|-1 and |B|-1. Qualifying pairs have |A|,|B|>=2.

Containment is componentwise inclusion: testing each difference vi-vj against an exposing functional for the larger face forces i in its maximum set and j in its minimum set. This also proves no duplicate index pairs. An arbitrary alternative face decomposition of the same sum is contained in the canonical pair (evaluate the exposing functional); equality of sums then forces both nonnegative support-function deficits to vanish. So no alternative summand pair restores a failed dimension equality.

For a functional (u,t) on the product, t>0 or t<0 gives endpoint faces, with exactly the base qualification. For t=0 both summands contain the same interval direction: if base dimensions are a,b,c, the sum dimension is c+1<=a+b+1, strictly smaller than a+b+2. No vertical or whole face qualifies. If u=0,t!=0, base full summands each have dimension4 but their sum has dimension4, so the horizontal end facet fails. The qualifying poset is exactly two incomparable endpoint copies of the base mixed poset.

The entire base nonempty face count is181 (180 proper pluswhole), so the product has543 nonempty faces. This is a useful independent coordinate-reconstruction check, not a substitute for the exhaustion argument.

## Combinatorics and topology

For a five-element index set, possible qualifying sizes are(2,2),(2,3),(3,2). There are30 minimal pairs and20 maximal pairs. Each maximal has3 minima; each minimal has2 maxima; no three-term strict chain exists. Thus each copy's order complex is a pure graph on50 vertices and60 edges, with degrees2 and3.

Suppressing its30 degree-two vertices gives the bipartite double cover of the disjointness graph of2-subsets of a5-set. The base graph is connected (intersecting vertices have a common disjoint complement) and contains an odd5-cycle, so its bipartite double cover is connected: lift any walk and insert an odd detour if the endpoint sheet is wrong. Subdivision preserves connectedness. A spanning tree leaves60-50+1=11 independent cycles. Each component is homotopy equivalent to a wedge of11 circles; their disjoint union has rational Betti numbers(2,22,0,...).

Every vertex belongs to an edge. Any shelling must eventually introduce the first edge in the other component, whose intersection with preceding facets is empty, of dimension-1 rather than0. Hence no pure or standard nonpure shelling exists. Björner–Wachs, Shellable Nonpure Complexes and Posets I, Definition2.1, inspected in the author's primary PDF, has the required pure dimension(dim newfacet-1) intersection. In dimension0 the empty intersection IS the required dimension-1; six isolated vertices are shellable. This boundary control is essential.

A wedge of3-spheres is connected and has no first rational homology. Both obstructions hold. A wedge of2-spheres would also fail, so changing n-2 ton-3 alone does not repair this counterexample.

## Source distinction and remaining checks

The cited Adiprasito et al. arXiv:1607.00347v1, Section1.2 and Section3, defines totally mixed using summand facets, a different condition. Its positive counting theorem cannot be imported to this target without checking hypotheses. This is a definition comparison only, not a completed priority audit.

Root has found no analytic or combinatorial gap in the self-contained proof. Independent exact coordinate reconstruction and exact chain computations remain pending. Priority audit will follow mathematical acceptance. No new-resolution preprint is prepared at this stage.

Primary sources inspected:
- https://ems.press/content/serial-article-files/46818
- https://arxiv.org/pdf/1607.00347v1
- https://www.math.miami.edu/~wachs/papers/nonpure1.pdf
