# One globally common color suffices in the subcubic case

## Scope and statement

Let (G) be a finite simple graph of maximum degree at most three such that

1. (G) has no proper edge-coloring with three colors, and
2. (G-e) has a proper edge-coloring with three colors for every (e\in E(G)).

These are the explicit criticality hypotheses used throughout. Isolated vertices are allowed. A list assignment is **constant** if the same set is assigned to every edge.

**Theorem.** Suppose every edge (e) has a list (L(e)) of exactly three colors and
\[
\bigcap_{e\in E(G)} L(e)\ne\varnothing.
\]
Then (G) admits a proper (L)-edge-coloring if and only if (L) is nonconstant.

There is no bound on the number of edges, on the number of exceptional lists, or on the total palette. The proof below is symbolic and does not depend on the finite checks accompanying this note.

The theorem is a restricted case of the list-edge-critical conjecture recorded by [Open Problem Garden](https://www.openproblemgarden.org/op/list_colorings_of_edge_critical_graphs). It includes the previously established two-common-colors case. It does not settle assignments with empty total intersection. No priority or historical-novelty claim is made.

## 1. Edge-containing connectedness

**Lemma 1.** All edges of (G) lie in one connected component.

**Proof.** Some component (H) is not three-edge-colorable, since otherwise independently coloring the components would color (G). If an edge (e) lay in another component, (G-e) would still contain (H) and would not be three-edge-colorable. This contradicts hypothesis 2. Thus every other component is an isolated vertex. ∎

Consequently, any nonconstant edge assignment has two incident edges with different lists: connect two edges with different lists by an edge-adjacency chain inside the edge-containing component and take a consecutive pair where the list changes.

## 2. A unique odd cycle through any chosen edge

**Lemma 2 (critical-cycle matching).** For every edge (e\in E(G)), there is a matching (M_e), not containing (e), such that:

- (M_e) covers every vertex of degree three in (G);
- (G-M_e) has maximum degree at most two;
- (G-M_e) has exactly one odd cycle, denoted (C_e), and (e\in E(C_e)).

More precisely, start with **any** proper three-edge-coloring \(\varphi\) of (G-e). Among its three labels, choose a label \(\gamma\) that appears at every endpoint of (e) having degree three in (G). Such a label always exists, and its color class can be used as (M_e).

**Proof.** An endpoint of (e) having original degree three has two incident edges in (G-e), and these have different labels. It therefore excludes only one label from the choice of \(\gamma\). There are at most two such endpoints, so together they exclude at most two of the three labels. At least one permissible \(\gamma\) remains.

Let (M_e=\varphi^{-1}(\gamma)). It is a matching. Every degree-three vertex that is not an endpoint of (e) sees all three labels under \(\varphi\), and every degree-three endpoint sees \(\gamma\) by choice. Hence (M_e) covers every degree-three vertex. A vertex of original degree at most two needs no coverage: its degree in (G-M_e) is already at most two. This explicitly includes a degree-two endpoint of (e), even if it does not see \(\gamma\).

Thus (G-M_e) has maximum degree at most two, and every component is an isolated vertex, a path, or a simple cycle. The restriction of \(\varphi\) to \((G-M_e)-e\) uses only the other two labels, so every odd cycle of (G-M_e) must contain (e). Distinct cycle components are disjoint; consequently there is at most one odd cycle.

If there were no odd cycle, every component of (G-M_e) could be edge-colored with those two labels. Coloring (M_e) with \(\gamma\) would then give a proper three-edge-coloring of all of (G), contrary to hypothesis 1. There is therefore exactly one odd cycle, and it contains (e). ∎

No bridgelessness theorem, perfect-matching theorem, or global connectivity assertion about a family of critical cycles is needed.

## 3. Two local cycles detect a nonconstant assignment

**Lemma 3 (local cycle overlap).** Suppose an assignment (B) of sets to the edges of (G) is nonconstant. There are incident edges (e,f) with (B(e)\ne B(f)). For **any** choices of the matchings and cycles supplied by Lemma 2 for these two edges, at least one of (C_e,C_f) has nonconstant (B)-lists.

**Proof.** Choose incident (e,f) using Lemma 1, and let (v) be their common endpoint. The simple cycle (C_e) uses two edges incident with (v), as does (C_f). Since (d_G(v)\le3), these two pairs of incident edges intersect. Thus the cycles share some edge (g) incident with (v).

If (B) were constant on each cycle, constancy on (C_e) would give (B(e)=B(g)), and constancy on (C_f) would give (B(f)=B(g)). This contradicts (B(e)\ne B(f)). ∎

The degree bound is used locally: two two-element subsets of a set of size at most three intersect. It is not inferred from bridgelessness or from an unproved global overlap property.

## 4. Two-list edge-coloring of paths and cycles

**Lemma 4.** A path is edge-colorable from arbitrary two-element edge lists. A simple cycle is edge-colorable from arbitrary two-element edge lists unless it is an odd cycle whose edge lists are all the same two-element set; this exceptional case is uncolorable.

**Proof.** A path is colored greedily from one end, avoiding the color on the preceding edge.

For a cycle with nonconstant lists, there are consecutive edges with different lists. Write the cyclic edge order as (h_1,h_2,\ldots,h_k) so that (B(h_1)\ne B(h_k)). Since both sets have size two, choose a color (z\in B(h_1)\setminus B(h_k)), and give (h_1) color (z). Color (h_2,\ldots,h_k) greedily, always avoiding the preceding color. The last edge automatically differs from (h_1), because (z\notin B(h_k)). This colors the cycle.

If all lists are one fixed two-element set, alternating the two colors works exactly when the cycle length is even. An odd cycle cannot be properly colored with only two colors. ∎

## 5. Proof of the theorem

Choose a color (c\in\bigcap_e L(e)), and put
\[
B(e)=L(e)\setminus\{c\}.
\]
Every (B(e)) has size two, and (B) is nonconstant exactly when (L) is nonconstant.

Suppose (L) is nonconstant. Choose incident edges (e,f) with different (B)-lists. Apply Lemma 2 separately to (e) and (f), using any ordinary three-colorings of their deletions and any permissible labels. By Lemma 3, one of the resulting odd cycles, say (C_e), has nonconstant (B)-lists.

Color every edge of (M_e) with the common color (c). This is proper on the matching and respects its lists. By Lemma 2, every remaining component is a path, an even cycle, or the unique odd cycle (C_e). Lemma 4 colors all these components from their (B)-lists, because (C_e) is nonconstant. No color used on the complement equals (c), so edges in the matching cannot conflict with edges outside it. This is a proper (L)-edge-coloring of (G).

Conversely, if every list equals a fixed three-element set, an (L)-edge-coloring would be an ordinary three-edge-coloring of (G), contrary to hypothesis 1. ∎

## 6. Constructive consequence and four-color palette

The construction needs ordinary deletion colorings for at most two incident edges. Once those colorings are supplied, finding the two permissible color-class matchings, their unique odd cycles, and the final list coloring can be done by elementary component traversals and greedy coloring. The claim is about this reduction; it does not assert an efficient algorithm for obtaining the ordinary deletion colorings from an arbitrary input representation.

In particular, let all lists be three-element subsets of a fixed four-color palette (P). There are exactly four possible list types, (P\setminus\{a\}) for (a\in P). If a nonconstant assignment uses only two or three of these types, its total intersection is nonempty and the theorem applies. The only four-palette family not covered by this theorem is the family using **all four** list types, for which the total intersection is empty.

More generally, under the present subcubic criticality hypotheses, every hypothetical nonconstant uncolorable three-list assignment must have empty total intersection. This is a necessary condition for a counterexample, not an assertion that such a counterexample exists.

## 7. Research boundary and source context

This completes the bounded fifth research round at the nonempty-intersection theorem. The unrestricted simple-graph conjecture, including the subcubic empty-intersection case, is left unresolved here. The earlier bounded-exception theorems may cover some empty-intersection assignments; no claim is made that every empty-intersection assignment is beyond those earlier results.

The [original July 2001 page](https://www.sfu.ca/~mohar/Problems/P7ListEdgeCriticalGraphs.html) prints a reversed equivalence. Equal lists are necessarily uncolorable under its own criticality hypothesis, so that wording is not used as a substantive refutation. The intended direction is explicit in Open Problem Garden. [Kaul and Mudrock, arXiv:1805.02147v2](https://arxiv.org/pdf/1805.02147v2), Conjecture 6 on printed page 11, gives the strong-chromatic-choosability formulation for the line graph. Its edge-critical indexing uses chromatic index; the explicit hypotheses at the start of this note remove any convention ambiguity.

The argument above proves only the stated restricted theorem. The bounded source inspection accompanying this packet does not establish that this restricted theorem is historically new.
