# Five exceptional lists in subcubic edge critical graphs

Authored 12 October 2026 UTC. This is a complete symbolic proof of the restricted theorem below, independently accepted; see [the complete audit](AUDIT_SUBCUBIC.md). The computations that motivated the case split are not hypotheses or dependencies of the proof. No historical novelty or resolution of the unrestricted conjecture is claimed.

## Theorem and scope

Let G be a finite simple graph of maximum degree three. Suppose G has no proper three-edge-coloring, but G−e has one for every edge e. Let A be a set of three colors. Give every edge a list L(e) of exactly three colors, and let X={e:L(e)≠A}. If 1≤|X|≤5, then G has a proper L-edge-coloring.

The accepted [four-exception theorem](../3200_critical_list_partials_20261012/FOUR_EXCEPTIONS.md) already covers |X|≤4. The proof below settles |X|=5. Its use of criticality always consists of taking an ordinary three-coloring of G−e and, when needed, restricting it further. It makes no unsupported assertion about arbitrary boundary colorings or connectedness of Kempe chains.

The full conjecture asks for arbitrary nonconstant assignments, without a bound on |X|. That assertion remains outside this theorem. The theorem also does not address degrees greater than three.

## 1 Notation and elementary completion facts

Write O(e)=L(e)\A and d(e)=|O(e)|=|A\L(e)| for e∈X. Thus 1≤d(e)≤3. Let H be the graph whose vertices are X and whose adjacency means incidence of the corresponding edges of G. We use edge language and vertex language for H interchangeably when explicit. An exterior coloring means a proper coloring using O(e).

For every nonempty F⊆X, an ordinary three-coloring φ of G−F exists: choose f∈F, color G−f by criticality, and restrict. If F has an exterior coloring and a permutation of φ's three labels onto A respects the residual lists on X\F, these two colorings combine. Their palettes are disjoint.

**Strict deficit completion.** If an exterior-colored nonempty F satisfies ∑_{e∈X\F}d(e)<3, completion is possible. Under a uniform random permutation of the ordinary labels onto A, edge e violates its list with probability d(e)/3. The union bound is strictly below one. No independence assumption is needed.

We also need the two equality cases, with total residual deficit three.

**Three unit deficits.** Suppose the residual edges have ordinary labels i₁,i₂,i₃ and omitted base colors a₁,a₂,a₃. A compatible permutation fails to exist exactly when either:

1. all i_j are equal and the a_j are all distinct; or
2. the i_j are all distinct and the a_j are all equal.

Indeed, each constraint forbids one cell of a three-by-three label-to-color matching problem. Hall fails on a single row only when that entire row is forbidden, giving case 1. Failure on two rows requires at least four forbidden cells, impossible here. Failure on all three rows requires an entire missing column, giving case 2. Repeated forbidden cells do not count twice.

**Deficits two and one.** Let a deficit-two residual edge e have sole permitted base color a, and a deficit-one residual edge f omit base color b. Completion fails exactly when φ(e)=φ(f) and a=b. If labels differ, map φ(e) to a; at least one of the two remaining colors differs from b and can receive φ(f). In particular an incident residual pair always completes.

## 2 Small support and list lemmas

All statements in this section have direct proofs; no support table is invoked.

### 2.1 Subcubic incidence properties

H is K₄-free. Four pairwise-incident edges in a simple graph would have to form a four-edge star: a pairwise-incident family that is not a star is contained in a triangle. A four-edge star violates the degree bound.

Two incident edges uv,uw have at most two other edges incident with both. One may be the third edge at u; the only other possibility is vw.

Three pairwise-incident edges T form either a three-star or a triangle. Every edge outside T meets at most two members of T. Moreover, two different edges outside T cannot meet exactly the same two members of T. For a three-star, an outside edge meeting two members must join their two leaves, and simplicity makes it unique. For a triangle, such an outside edge uses the vertex shared by those two triangle edges; two outside edges there would give degree four.

### 2.2 Lists on at most four vertices

**Lemma.** Let J be a K₄-free graph on at most four vertices, with lists of size at least two. Then J is uncolorable from these lists if and only if some triangle has the same two-element list at all three of its vertices.

A triangle is list-colorable unless its three lists have union of size two: every one- and two-vertex Hall condition is automatic. Forests color greedily. The cycle C₄ is two-choosable. A triangle with a pendant vertex colors by first coloring the triangle and then the pendant vertex. These observations cover every case except the diamond K₄−e.

For the diamond, let u,v be the adjacent vertices of degree three and let p,q be the nonadjacent tips. Choose distinct colors c_u∈L(u), c_v∈L(v). A tip cannot be colored only if its list is precisely the unordered pair {c_u,c_v}; a list of size at least three never blocks a pair. Thus the two tips block at most two distinct unordered pairs.

Unless L(u)=L(v) is one common two-set, there are at least three distinct unordered pairs obtainable using distinct choices from these two lists. To see this, if two two-element sublists differ, their cross choices give at least three pairs; if they coincide but one original list contains another color, using that color gives a third pair. Therefore an unblocked pair exists. In the sole remaining case, every central pair is the common two-set, and a blocking tip forms exactly the stated bad triangle. This proves the lemma.

For completeness, an even cycle is two-choosable. Shrink lists to size two. If all are the same, alternate the two colors. Otherwise choose adjacent vertices with different lists, start at the first with a color absent from the second, and greedily color around the other direction; the last vertex has at most one forbidden color in its list, because the starting color was absent from it.

### 2.3 Triangles on five vertices

**Lemma.** In a K₄-free graph J on five vertices, there is a vertex meeting every triangle.

If some vertex v has degree four, a triangle avoiding v would create K₄ together with v. Otherwise the maximum degree is at most three. Distinct triangles cannot meet in just one vertex, since that vertex would then have degree at least four; they cannot be disjoint on five vertices. If there are two triangles, label them 123 and 124. Vertices 1 and 2 already have degree three, so neither meets vertex 5. A triangle avoiding 1 would need edge 34, whether it uses vertex 2 or consists of 345; that edge would make 1234 a K₄. Thus every triangle contains 1. With zero or one triangle the claim is immediate.

Also, every K₄-free graph on five vertices is three-choosable. If it has a vertex of degree at most two, color the other four by the preceding lemma and restore that vertex. Otherwise its complement has maximum degree at most one. K₄-freeness forces the complement to be exactly two disjoint edges and an isolated vertex. The original graph is a four-cycle with a universal hub. Color the hub first; the rim retains lists of size at least two and is two-choosable.

## 3 Five unit deficits

Assume d(e)=1 for all five exceptional edges.

First suppose their omitted colors are not all equal. If X contains a matching of size three, exterior-color those three edges and use strict deficit completion. Otherwise its matching number is two. Removing any one edge of X leaves four edges, which cannot be pairwise incident; hence it leaves a two-edge matching. Thus complements of two-edge matchings cover X. These complements are three-subsets of a five-set, so every two intersect. If every such triple had constant omissions, their intersections and covering property would force a single omitted color on all of X. Therefore choose a matching F of size two whose complementary triple has nonconstant omissions. Color F exteriorly. In any ordinary coloring of G−F, the residual triple cannot have one common label, since that would be a matching of size three in X. Both equality obstructions in Section 1 are excluded.

Now suppose every exceptional edge omits the same base color a. We use the following matching recoloring observation, which does not require |X|=5. If some exceptional edge e has at most two exceptional neighbors, ordinarily color G−e and choose a label t absent from those neighbors. Let

F={e}∪{f∈X\{e}:φ(f)=t}.

The φ-color class is a matching, and none of its exceptional edges meets e. Thus F is a matching. Color each of its edges with its own exterior color; exterior colors need not agree. Map t to a and the other labels to the other two base colors. Every residual exception avoids a, so this is a full L-coloring.

For five exceptions, if H has no vertex of degree at most two, the complement argument in Section 2.3 shows that H is a four-cycle plus a universal hub. Choose a rim vertex e and let f be its unique nonneighbor in H. In an ordinary coloring of G−e, f has a label t different from all three neighbors of e, since f is adjacent to all of them. The same matching recoloring argument applies. This exhausts all five-unit cases.

This proof in particular includes the uniform-list five-cycle case. It uses a deletion coloring; it does not claim that every fixed exterior set and every previously chosen ordinary coloring can be repaired by a palette permutation.

## 4 One large deficit

Suppose just one edge e has d(e)≥2 and the other four have unit deficits.

If d(e)=3, two of the four small edges can be exterior-colored together: otherwise all four would be pairwise incident with the same exterior color, contradicting K₄-freeness. Color such a pair and then color e, which has three choices and avoids at most two already used colors. The residual deficit is two.

Suppose d(e)=2. If a strict deficit certificate exists, finish with Section 1. Otherwise e must meet all four small edges. Indeed, suppose a small edge f misses e. If {f,g} can be exterior-colored for any other small edge g, then e can be added: it sees at most g and has two choices. This is a strict certificate, since its removed deficit is four out of the total six. Hence f meets all three other small edges, and their singleton exterior colors all equal that of f. Among these three there is a nonincident pair g,h; otherwise together with f they would form K₄. Color g,h with their common exterior color and add e using a different exterior color. Again this is a strict certificate, a contradiction.

We are therefore in the universal-edge case. Choose any small edge f and ordinarily color G−f. Let t=φ(e). Remove e as well and exterior-color e and f with distinct colors, possible because e has two choices. The three residual small edges all meet e, so they avoid ordinary label t. They cannot all have one label: since each meets one of the two endpoints of e, at least two of them meet each other. Hence their labels use exactly two colors. Neither equality obstruction for three unit deficits is possible, regardless of their omitted base colors. A palette permutation completes the coloring.

## 5 Two large deficits

Let e,f have deficits at least two, and let the other three edges be small. If e,f are nonincident, choose any small edge s, color s exteriorly, and then color e and f, each avoiding at most s.

If e,f are incident, at most two other edges meet both by Section 2.1. Choose a small edge s that does not meet both. The adjacency graph on {e,f,s} is a forest. Root the component containing s at s, color s first, and then color each large edge, which has at least two choices and at most one colored neighbor. Other components are equally easy.

In either case three edges have been exterior-colored and the two residual deficits are both one. Strict completion applies.

## 6 Three large deficits

Let T be the three large edges; the other edges are s,t with unit deficits. If T is exterior-colorable, its complement has deficit two and we are done. Otherwise T is a pairwise-incident triple and all three exterior lists equal one two-set {x,y}. This follows from greedy coloring of a three-vertex forest and the triangle Hall observation in Section 2.2. Thus all three large deficits are exactly two.

### 6.1 A cross-incidence exists

Suppose at least one of s,t meets some member of T. We claim there is an exterior coloring of two members of T and one small edge that leaves an incident large-small residual pair.

For a chosen residual pair (e,s), where e∈T meets s, the exterior set would be (T\{e})∪{t}. This exterior set fails to color only if the singleton color of t belongs to {x,y} and t meets both members of T\{e}. If either condition fails, color t first and assign x,y in a feasible order to the two remaining members of T.

Suppose no incident residual pair succeeds. Choose e∈T meeting s. The failure just described forces t to meet the other two members f,g of T, and to miss e, since an outside edge meets at most two members of T. Now consider residual pairs (f,t) and (g,t). Their failures would force s to meet both e,g and both e,f, respectively. Then s would meet all three members of T, impossible. This proves the claim.

The incident residual pair has deficits two and one, so Section 1 completes every ordinary coloring of its complement.

### 6.2 No cross-incidence exists

Now neither s nor t meets any member of T. Let a_e be the sole base color in L(e), for e∈T, and let b_s,b_t be the base colors omitted at s,t.

If a_e≠b_s for some e and some choice of small residual edge s, exterior-color the other two members of T with x,y and the other small edge with its singleton exterior color. These parts have no incidences. The equality criterion for deficits two and one then completes any ordinary coloring, regardless of whether the residual labels coincide.

The only remaining case has all a_e=b_s=b_t=a. Ordinarily color G−s. The three pairwise-incident members of T receive three different labels. Choose e∈T whose label differs from φ(t). Retain e and t, exterior-color the other two members of T with x,y, and color s exteriorly. The two residual labels differ, so the same equality criterion completes. This use of an ordinary deletion coloring is why an arbitrary unextendable boundary signature would not refute the theorem.

## 7 Four large deficits

Let s be the small edge and let z be its singleton exterior color. If the four large edges can be exterior-colored, leave s and apply strict completion.

Otherwise Section 2.2 supplies a pairwise-incident triple T among those four with one common two-element exterior list {x,y}. Let h be the fourth large edge. Color s with z and h with an exterior color w≠z; such a choice exists because d(h)≥2. These two chosen colors are proper even if the edges meet.

For each of x and y, consider the members of T on which it remains available. Since z≠w, each such color is blocked only by incidences with at most one of s,h. That edge meets at most two members of T, so at least one member remains eligible.

There is a way to assign x and y to two different eligible members of T unless both eligibility sets are the same singleton. That failure would require the precolors to be x,y and would force s and h to meet exactly the same two members of T. Section 2.1 proves that impossible in a simple subcubic graph. Therefore color two members of T, leaving only its third member. The residual deficit is two, so strict completion applies.

## 8 Five large deficits

All five exterior lists have size at least two. If all have size three, Section 2.3 exterior-colors all of H, leaving no residual exceptions.

Otherwise some exterior list has size two. Call a triangle bad if its three exterior lists are one common two-set. If there is no bad triangle, delete any deficit-two edge e; Section 2.2 colors the remaining four exterior lists. If bad triangles exist, Section 2.3 gives a vertex e meeting every triangle, hence every bad triangle. Because it lies in a bad triangle, its list has size two. Delete e; the remaining four-vertex graph has no bad triangle and is exterior-colorable by Section 2.2.

In either case the sole residual deficit is two, and strict completion applies.

## 9 Conclusion and checks

The number of large deficits is one of 0,1,2,3,4,5. Sections 3–8 settle every possibility, proving the theorem for exactly five exceptions. Together with the independently accepted result for one through four exceptions, this proves the stated at-most-five theorem in degree three.

The earlier complete exterior-certificate enumeration was useful in discovering the argument, but none of its output, support representatives, palette bounds, or numerical conclusions is needed for this proof. The proof applies to arbitrary finite color names and arbitrary critical supergraphs satisfying the explicit hypotheses. No conjecture counterexample is obtained from failure of a strict deficit test or a fixed ordinary coloring.

The matching recoloring and the short h≥4 lemmas were developed jointly with the complementary five-exception completion analysis. The accompanying checks independently exercise the local mechanisms and validate complete colorings on critical fixtures. They are corroboration, not proof substitutes.

## 10 Primary source context

The intended nonconstant-list conjecture appears in the [Open Problem Garden entry](https://www.openproblemgarden.org/op/list_colorings_of_edge_critical_graphs). [Mohar's July 2001 problem page](https://www.sfu.ca/~mohar/Problems/P7ListEdgeCriticalGraphs.html) prints the known reversed equivalence; that wording issue is not used as a mathematical counterexample. [Kaul and Mudrock, arXiv version 2, Conjecture 6](https://arxiv.org/pdf/1805.02147v2) gives the strong chromatic-choosability formulation for the line graph. The explicit non-three-colorability hypothesis above is retained regardless of abbreviated criticality terminology in that source.

The newer [Bernshteyn, Kaul, Mudrock and Sharma paper](https://onlinelibrary.wiley.com/doi/full/10.1002/jgt.70033) studies strong and robust criticality and large clique joins; it is contextual, not a proof of this restricted edge-list result. Bounded source searches have not established historical novelty, and no such claim is made.
