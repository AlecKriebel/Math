# Turn 2: exact two-edge seams and the tight K4+ boundary law

## Purpose and disposition

We examine whether independently obtained 8/3-colorings can be glued across a two-edge cut, and whether slack at degree-two vertices could support an induction. The seam has a precise correlation obstruction. The known planar graph K4+ is tight and forbids any uniform extra demand at even one degree-two vertex. Its full optimal-coloring law can nevertheless supply universally compatible correlations at suitable pairs of ports.

Original conjecture: unresolved, 2/5 substantive author turns. No historical novelty is asserted. K4+ and the use of degree-sensitive demands already occur in Dvorak--Lidicky--Postle (2025), Section 2 and Figure 1. We derive the exact target-density boundary data here rather than treat the known graph as a new construction.

## 1. Gluing across two new edges

Take disjoint graphs H and J with r-colorings, 0<=r<=1/2. Choose two distinct vertices a,b in H and c,d in J, and add edges ac and bd. We may rearrange all color sets of J and H, preserving their full internal coloring laws. Let

    s = |phi(a) intersect phi(b)|,
    t = |psi(c) intersect psi(d)|,
    q = 1-2r.

**Theorem 2.** A coupling of these two given coloring laws that respects the two new edges exists if and only if

    |s-t| <= q.

**Proof.** The four membership states 00,10,01,11 for each ordered pair have probabilities

    (q+s, r-s, r-s, s) and (q+t, r-t, r-t, t).

A state i on one side is compatible with state j on the other precisely when the bitwise intersection is zero. A coupling is a nonnegative 4-by-4 transportation matrix with these row and column sums and zeros in the incompatible cells. Once it exists, couple the full color-pattern distributions conditionally on their pair states. This preserves all vertex marginals and all old edge constraints. Since each graph is finite, there are finitely many such color patterns; this is an ordinary finite coupling, representable by intervals in [0,1].

Necessity follows because state 11 on H must be paired with state 00 on J, giving s<=q+t; the reverse side gives t<=q+s.

For sufficiency, use the finite capacitated Hall criterion (equivalently the max-flow/min-cut theorem). Every row subset containing 00 has all four columns as its neighborhood, so its inequality is automatic. For subsets of {10,01,11}, the only remaining inequalities, up to exchanging 10 and 01, are:

- {10}: r-s <= 1-r, automatic since 2r<=1;
- {11}: s <= q+t;
- {10,01}: 2r-2s <= 1-t, implied by t-s<=q and s>=0;
- {10,11}: r <= 1-r, automatic;
- {10,01,11}: 2r-s <= 1-t, equivalent to t-s<=q.

Thus the two asserted inequalities suffice for every cut. QED.

At the target r=3/8, the threshold is q=1/4. Arbitrary individually valid colorings cannot automatically be glued: s=0 and t=3/8 fail. This is an obstruction to gluing those prescribed colorings, **not** a counterexample graph to the original conjecture, since either side might have other colorings.

For a colorable graph with a fixed pair of ports, the set of attainable overlaps is a compact interval: it is the linear image of the finite probability polytope on its independent sets, with fixed marginals. For two such graphs, a seam is colorable exactly when the distance between their two attainable intervals is at most 1/4. Determining those intervals uniformly for the remaining planar subcubic cores is still open in this approach.

## 2. A tight planar K4 subdivision

Let K have vertices a,b,c,d,x,y,z,w and edges

    ac, ad, bc, bd, ax, xy, yb, cz, zw, wd.

Thus two opposite edges ab and cd of K4 are each subdivided twice. This is the graph called K4+ in the cited 2025 paper. It is planar, subcubic, and triangle-free. The four old vertices have degree three and x,y,z,w have degree two. Its unmodified four cross edges form a 4-cycle; every original triangle acquires two additional edges on one of the subdivided paths.

**Lemma 3.** K has independence number 3. Its twelve maximum independent sets are exactly the rows of the table below.

**Proof.** An independent set contains at most two of a,b,c,d. With none, the two internal edges xy and zw limit its size to two. With one, at most two internal vertices can be used. With two, they must be a,b or c,d; these forbid both internal vertices on their own connecting path, leaving at most one on the other. The table exhibits all cases of size three. QED.

## 3. Complete optimal-coloring parameterization

Every 3/8-coloring of K induces a probability distribution on independent sets with expected size 8*(3/8)=3. By Lemma 3 every set receiving positive mass therefore has size exactly three. Let A,B,C,D be four real parameters. All possible distributions with the required equal marginals are:

| Independent set | Probability |
| --- | --- |
| abz | A+B |
| abw | 1/4-A-B |
| ayz | 1/8-A |
| ayw | A |
| bxz | 1/8-B |
| bxw | B |
| cdx | C+D |
| cdy | 1/4-C-D |
| cxw | 1/8-C |
| cyw | C |
| dxz | 1/8-D |
| dyz | D |

The exact parameter range is the entire cube

    0<=A,B,C,D<=1/8.

To verify completeness, write the eight vertex-marginal equations and the total-mass equation in these twelve variables. Their coefficient matrix has rank eight. Substitution verifies the table, and its four parameter directions are linearly independent. It is therefore the full affine solution space. Nonnegativity of the rows A,1/8-A, and the three analogous pairs forces precisely the cube bounds; those bounds automatically make A+B,1/4-A-B,C+D,1/4-C-D nonnegative. The accompanying verifier checks the two ranks with exact rational elimination, not floating-point rank estimation.

Setting all four parameters to 1/16 gives each two-old-vertex set mass 1/8 and each one-old-vertex set mass 1/16. Thus an r=3/8 coloring exists, while n/alpha=8/3 supplies the matching lower bound. Consequently chi_f(K)=8/3.

The four cross-port intersection probabilities are

    t_xz = 1/4-B-D,
    t_xw = 1/8+B-C,
    t_yz = 1/8-A+D,
    t_yw = A+C.

Their sum is 1/2 and each separately ranges over the full interval [0,1/4]. They cannot be chosen independently: for example setting all four to zero violates their sum. The two adjacent-port overlaps t_xy and t_zw are necessarily zero.

This is a concrete illustration of the issue left after turn 1: individually allowable path or pair overlaps do not automatically give a joint coloring law.

## 4. A usable seam and an induction obstruction

**Corollary 4 (cross-port attachment).** Attach K to any graph J already fractionally 8/3-colorable by two new matching edges, using one degree-two port from {x,y} and one from {z,w}. The resulting graph is still fractionally 8/3-colorable.

Indeed, set A=B=C=D=1/16, so every such cross-port overlap is 1/8. Every pair overlap t in J lies in [0,3/8], whence |t-1/8|<=1/4. Apply Theorem 2. If the attachment preserves planarity, triangle-freeness and degree at most three, this supplies a reduction within the original class. The coloring conclusion itself does not require these three extra properties of J. Adjacent ports on K have overlap zero and are not covered by this universal guarantee.

**Corollary 5 (no universal degree-two surplus).** There is no theorem for every planar triangle-free subcubic graph that requires all vertex color sets to have measure at least 3/8, and in addition requires strictly greater measure at even one designated degree-two vertex.

K already contradicts such a strengthening: the total expected independent-set size would exceed 3, contrary to Lemma 3. In particular, a blanket demand rule that adds any fixed positive surplus at all degree-two vertices is impossible. This does not refute the original equal-demand conjecture. A viable strengthened induction would have to allow exceptions, conditional slack, or a redistribution of demands, as the published 11/4 proof does in its different setting.

## 5. Supplementary verification and remaining gap

`turn2/check_seams.py` checks the seam condition by independent integer-capacity max-flow on all rational grid data with denominator 2 through 24. It enumerates all 256 vertex subsets of K, verifies its twelve maximum independent sets, checks the full affine parameterization using exact ranks, and verifies all 16 cube corners and the balanced cross-port construction. See the machine receipt for exact assertion counts.

No all-graph enumeration, global compatibility theorem, or complete fractional 8/3 proof has been obtained. Further author work must address larger cubic cores or interacting tight blocks, rather than replace a weighted claim by an unweighted bound or a finite (8,3)-coloring search.
