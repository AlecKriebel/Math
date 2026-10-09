# Edition notice for the complete approach-1 report

This proof-and-audit edition preserves the complete original report below, without changing its mathematical text. The original question remains unresolved after approach 1 (1/5). This edition adds no substantive approach.

The report contains complete written arguments for its reductions and restricted theorems. Its displayed 15-vertex hypergraph, starting coloring, 450-move histogram and three-vertex repair are retained as originally written. That example obstructs strictly decreasing local search on at most two vertices; it is not a counterexample to the coloring question.

References below to certificate JSON files, programs, saved computational outputs and the original packet's manifest describe historical auxiliary materials. Those materials are not distributed in this edition. In particular, the instructions in Section 8 cannot be run from this directory. The positive coloring of PG(2,5) was checked in the original work but its color vector is not supplied here; that claim remains a historical supplementary finite-check report, not a reproduced certificate in this edition. No excluded fixture or program has been converted into new prose.

See [README.md](README.md) for the evidence boundary and [PRECISION_NOTE.md](PRECISION_NOTE.md) for the separate clarification of the Local Lemma thresholds. The original report begins below and is preserved as one unchanged byte sequence.

---

# Majority three-coloring of 6-regular, 6-uniform hypergraphs

## Status

**Unresolved after this approach.** This report gives neither a proof of the full assertion nor a hypergraph that violates it. It develops the pairing/local-recoloring approach, proves several reductions and restricted results, and supplies exact certificates showing why a natural strictly decreasing local search is insufficient. No novelty claim is made for the elementary lemmas.

The target is a finite hypergraph in which every edge consists of six distinct vertices and every vertex belongs to six indexed edges. We seek a vertex coloring with three colors such that each edge contains at most three vertices of each color.

The source is Tibor Szabó's question in *Oberwolfach Report 1/2020*, printed page 83 (PDF page 79), with its motivation on printed page 84: <https://ems.press/content/serial-article-files/46836?nt=1>. The same question is Problem 1 on page 13 of Anastos–Lamaison–Steiner–Szabó, *Majority Colorings of Sparse Digraphs*, author PDF dated May 17, 2021: <https://page.mi.fu-berlin.de/szabo/PDF/MajorityColorings.pdf>. The latter constructs one hyperedge for each vertex of a 5-regular digraph, using that vertex and its out-neighbors. Different indexed edges can consequently coincide. Neither inspected passage explicitly imposes distinct hyperedges. The reduction below removes this possible ambiguity.

## 1. A regularization lemma removes the multiplicity issue

**Lemma 1.** Every finite simple 6-uniform hypergraph of maximum degree at most 6 is contained as a copy inside a finite simple 6-regular, 6-uniform hypergraph. The construction uses 36 copies of the original vertex set.

**Proof.** Write the original vertices as `v`, their degrees as `d(v)`, and their deficits as `h(v)=6-d(v)`. Form vertices `(v,a,b)`, where `a,b` range over the residues modulo 6. For each pair `(a,b)`, include a copy of every original edge using that pair of coordinates.

For every original vertex `v`, every integer `t` with `0 <= t < h(v)`, and every residue `b`, add

`F(v,t,b) = {(v,a,b+a*t mod 6): a=0,1,...,5}`.

Each new edge has six distinct vertices. A fixed vertex `(v,a,c)` lies in exactly one edge `F(v,t,b)` for each `t`, namely the edge with `b=c-a*t`. Its degree is therefore `d(v)+h(v)=6`.

The added edges are distinct: their common original vertex determines `v`, the coordinate with `a=0` determines `b`, and the coordinate with `a=1` then determines `t` modulo 6. Since `0 <= t <= 5`, it determines `t` itself. An original-copy edge has six different original vertices, whereas an added edge has only one original vertex, so these two types cannot coincide. Original-copy edges are distinct because the starting hypergraph was simple. Restriction to any fixed `(a,b)` recovers the starting hypergraph. ∎

**Corollary 2.** The following universal statements are equivalent:

1. The target coloring exists for every simple 6-regular, 6-uniform hypergraph.
2. It exists for every indexed 6-regular, 6-uniform hypergraph, with repeated edges allowed.
3. It exists for every 6-uniform hypergraph of maximum degree at most 6.

Indeed, (3) implies (2), which implies (1). For (1) implies (3), discard repeated edges, apply Lemma 1, color the completion, and restrict the coloring. Discarding repetitions lowers degrees and changes none of the coloring requirements.

## 2. Exact pairing reformulation

For every hyperedge, choose a partition of its six vertices into three pairs. Let `G` be the loopless multigraph consisting of all the chosen pairs, retaining an edge's occurrence when another hyperedge chooses the same pair. Then

`degree_G(v) = degree_H(v)`.

**Lemma 3.** The hypergraph has the requested coloring if and only if its pairings can be chosen so that `G` is properly 3-colorable.

**Proof.** A proper coloring of `G` gives different colors to the two ends of each of the three pairs in a hyperedge. Hence any fixed color appears at most three times there.

Conversely, suppose each color occurs at most three times in each hyperedge. Sort its six vertices by color, and pair positions 1 and 4, 2 and 5, and 3 and 6. Every color occupies a consecutive block of length at most three, so the vertices in any of these pairs have different colors. Apply this independently in every edge. ∎

This reformulation retains a real difficulty: an arbitrary 6-regular pairing multigraph need not be 3-colorable. Establishing the existence of favorable pairings is precisely what remains to be proved.

### A restricted positive result

**Proposition 4.** Every 6-uniform hypergraph of maximum degree at most 3 has the requested coloring.

**Proof.** Choose arbitrary pairings. The underlying simple graph of the resulting multigraph has maximum degree at most 3. By the subcubic case of Brooks' theorem, it is 3-colorable unless one of its connected components is `K4`.

Let `C` be such a component. Its vertices already have three distinct graph neighbors, so all their degree capacity is used; in particular, no edge of this `K4` has a parallel occurrence. Pick a pair `uv` in `C`, and let `e` be the hyperedge whose pairing supplies it. Since `e` has six vertices but `C` has four, another pair `xy` of `e` lies outside `C`. A pair cannot have just one endpoint in `C`, because `C` is a connected component.

Replace the pairs `uv,xy` of `e` by `ux,vy`. Degrees do not change. The graph on `C` with `uv` deleted remains connected. The component containing `xy`, with that edge deleted, has at most two pieces, and the new cross-edges attach both pieces to `C`. Thus the two old components merge into one component with at least six vertices. It cannot be a `K4`; all other components are unchanged. Repeating this operation removes every `K4` component. Brooks' theorem now gives a proper 3-coloring, and Lemma 3 completes the proof. ∎

The invoked standard result is R. L. Brooks, *On colouring the nodes of a network*, Proc. Cambridge Philos. Soc. 37 (1941), 194–197, <https://doi.org/10.1017/S030500410002168X>. This proposition does not handle maximum degrees 4, 5, or 6.

## 3. The optimized pairing potential and its exact obstruction

For a coloring `c`, let `n_i(e)` denote the number of vertices of color `i` in edge `e`. Define

`Phi(c) = sum over e and i of max(n_i(e)-3,0)`.

Only one summand per edge can be positive. The desired colorings are exactly those with `Phi=0`.

For a fixed coloring, `Phi` also equals the minimum possible number of monochromatic graph edges, minimized independently over all the pairings. If a color occurs `k>3` times in an edge, its `k` vertices can be paired across colors at most `6-k` times, leaving at least `k-3` monochromatic pairs. This bound is attained by pairing every minority vertex with a majority vertex and pairing the remaining majority vertices together. If every color occurs at most three times, Lemma 3 gives zero monochromatic pairs.

If a vertex `v` changes from color `a` to color `b`, the exact change is

`Delta Phi = sum over e containing v of (1[n_b(e)>=3] - 1[n_a(e)>=4])`.

Thus a plausible argument would seek a recoloring of one or two vertices that strictly decreases `Phi` whenever `Phi>0`. Even allowing arbitrary changes of both colors, that assertion is false.

### A fully specified obstruction to strictly decreasing changes on up to two vertices

Use vertices 0 through 14 and the following 15 edges:

```
 0  1  2  3  5  6
 0  1  2  5  6  9
 0  2  5  7  8 14
 0  3  4  5  6  9
 0  7  8  9 11 14
 0  8  9 11 12 13
 1  2  6 10 12 13
 1  2  7  8 12 14
 1  3  4 10 13 14
 1  3  4 11 12 14
 2  5  6 10 11 14
 3  4  7 10 11 12
 3  6  7  8 10 13
 4  5  8  9 12 13
 4  7  9 10 11 13
```

Every edge has six vertices, the edges are distinct, and each vertex lies in exactly six edges. Color vertices 0–4 with color 0, vertices 5–9 with color 1, and vertices 10–14 with color 2.

The first edge has color counts `(4,2,0)`; all other edges have maximum color count at most three. Thus `Phi=1`. Check the 30 single-vertex recolorings and all `binom(15,2)*2^2=420` changes on exactly two vertices. These include ordinary color swaps, but also all other pairs of color changes. Their exact potential changes are:

| Change in Phi | Number of moves |
| --- | ---: |
| 0 | 52 |
| 1 | 89 |
| 2 | 110 |
| 3 | 76 |
| 4 | 71 |
| 5 | 34 |
| 6 | 16 |
| 7 | 2 |

None of the 450 moves strictly improves the coloring. This is a non-strict local minimum: there are neutral moves, not a strict local minimum in which every move increases the potential.

**It is not a counterexample to the original problem.** Changing vertex 0 to color 1 and vertices 7 and 9 to color 0 gives a valid coloring. Its full color vector is

`(1,0,0,0,0,1,1,0,1,0,2,2,2,2,2)`.

Thus the displayed starting coloring has Hamming distance exactly three from the set of valid colorings: the 450 checks exclude distances one and two, and the explicit repair attains distance three.

The certificate is `two_vertex_minimum_15.json`; the independent verifier recomputes all incidence degrees, all 450 changes, and a valid coloring using only integer arithmetic and the Python standard library. It also verifies the specified three-vertex repair. Supplementary certificates separately test single-vertex descent, swap-only descent, and combined one-vertex/swap descent. These are local-search diagnostics, not counterexamples to the conjecture.

## 4. Any counterexample has at least twelve vertices

**Proposition 5.** Every 6-uniform hypergraph on at most eleven vertices, with maximum degree at most six, has the target coloring. Repeated edges are allowed.

**Proof.** Let `n` be its number of vertices and `m` the number of indexed edges. Counting incidences gives `6m <= 6n`, so `m <= n`.

For `n<=9`, partition the whole vertex set into three classes of size at most three.

For `n=10`, choose a uniformly random coloring whose class sizes are `(4,3,3)`. An edge is bad only if it contains the entire class of size four. Its probability of being bad is

`binom(6,4)/binom(10,4) = 15/210 = 1/14`.

The union bound is at most `10/14<1`.

For `n=11`, use class sizes `(4,4,3)`. An edge cannot contain both classes of size four, so its bad-event probability is

`2*binom(6,4)/binom(11,4) = 30/330 = 1/11`.

If `m<=10`, the union bound is already strict. Suppose `m=11`, and choose two indexed edges `e,f`. There is a coloring of the stipulated class sizes in which both are bad: if `|e intersect f|>=4`, use four common vertices for one class; if `|e intersect f|<=3`, choose disjoint four-subsets, one in each edge, as the two classes. Such disjoint choices exist because `e\f` has at least three vertices, so a four-subset of `e` can be chosen to meet `f` in at most one vertex, leaving at least five vertices of `f` available. The unused three vertices form the third class.

Hence the two bad events have positive intersection. The probability of the union of all bad events is at most the sum of their probabilities minus this positive intersection, and is therefore strictly less than `11*(1/11)=1`. ∎

This is a theorem, not an extrapolation from a computer search. It does not exclude counterexamples on twelve or more vertices.

## 5. The order-five projective plane: a verified positive example and a rounding barrier

Construct the points of `PG(2,5)` as the nonzero vectors in the three-dimensional vector space over the field of five elements, normalized so their first nonzero coordinate is 1. Use the same normalized vectors as line normals; a point belongs to a line exactly when their dot product is zero modulo 5.

There are 31 points and 31 lines. Each line has six points, each point lies on six lines, and each pair of distinct lines meets at one point. The file `projective_plane_5.json` contains the points, every edge, a coloring with class sizes `(11,10,10)`, and every edge's three color counts. The independent verifier confirms all of these statements and that no count exceeds three. This single example is not a general existence result.

It also gives an exact obstruction to a tempting stronger first step. There is **no subset of the points meeting every line in either two or three points**. Indeed, suppose such a subset has size `s`, and let `t` lines meet it in three points. Counting incidences and pairs of selected points gives

`6s = 2*(31-t)+3*t = 62+t`,

`binom(s,2) = (31-t)+3*t = 31+2*t`.

Eliminating `t` yields `s^2-25s+186=0`, whose discriminant is `625-744=-119`. This is impossible. Thus an argument that first extracts one color class meeting each edge two or three times would be too strong, even for a hypergraph that satisfies the desired three-coloring conclusion.

## 6. What the elementary probabilistic route actually says

For an independent uniform three-coloring of a single six-element edge, a specified color appears at least four times in

`binom(6,4)*2^2 + binom(6,5)*2 + 1 = 73`

of the `3^6=729` assignments. The three possible overrepresented colors give disjoint events. Thus the exact bad-edge probability is `219/729=73/243`.

An edge meets at most `6*(6-1)=30` other indexed edges. The elementary symmetric Lovász Local Lemma criterion using this dependency bound fails: `e*(73/243)*31>1`. Equivalently, `73/243` is larger than the maximum of `x*(1-x)^30`. This only rules out that direct sufficient-condition calculation. It does not prove that another probability distribution, a sharper dependency analysis, or a different use of the Local Lemma cannot work.

## 7. Exact remaining gap

The regularization and pairing reductions are equivalences. They leave the full task of finding favorable pairings or a zero-potential coloring when every vertex has degree up to six. The degree-three argument uses Brooks' theorem in a way that does not extend to degree six. The displayed local-minimum certificate rules out the assertion that a strictly improving change on at most two vertices always exists. Neutral-move paths and changes on three or more vertices remain possible and require an additional theorem or invariant. The exhibited Hamming-distance-three repair does not show that every hypergraph or every positive-potential coloring admits such a repair. The projective-plane count rules out the stronger two-to-three-points extraction step. None of these obstructions settles the original assertion.

Only this one approach has been pursued here; no later approach or queue update is included.

## 8. Reproduction and evidentiary limits

Run from this directory:

`python verify_certificates.py`

This requires Python's standard library only. It validates the displayed positive certificates without trusting solver status, floating-point feasibility, or the search scripts. `VERIFICATION_RESULTS.json` records the recomputed results. A second implementation, `python verify_bitsets.py`, checks the main 450-move certificate using integer bit masks and explicit checks that remain active under optimization. Normal and `python -O` executions agreed exactly; its output is `BITSET_VERIFICATION_RESULTS.json`.

The search scripts use NumPy 2.3.5 and SciPy 1.17.0, with SciPy's bundled HiGHS MILP solver. They may return different certificates on different versions. Every positive witness must be passed through the integer verifier. A solver infeasibility or timeout report in an exploratory file is not a theorem or an exhaustive classification; no conclusion above relies on it.

`SOURCE_MANIFEST.json` records the inspected public source URLs, PDF byte counts and SHA-256 digests. `MANIFEST.json` records the authored packet's file digests. No source text, remote publication, or queue edit is part of this work.
