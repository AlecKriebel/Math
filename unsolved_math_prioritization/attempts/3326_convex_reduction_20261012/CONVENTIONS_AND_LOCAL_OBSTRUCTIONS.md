# Linear hypergraphs of incidence dimension three: convention audit and local-construction obstruction

## Scope and status

This is newly written work on problem 3326 / OPG-596. It belongs to the second confirmed substantive pass: the October 11 screening is the first confirmed pass, while the lifetime count is unknown. The old heading about a degree-two subclass is not a recovered proof. No claim below establishes a general solution, a new result in the literature, or a current-open status. This mathematical report records no external publication action.

The principal intended target is the finite, loopless, linear version with maximal-common-intersection semantics. Geometric objects are assigned to hypergraph vertices, not hyperedges. For the mathematical statements below, a triangle means its closed convex hull, a segment is closed, and intersections are unrestricted. Those working conventions are stated explicitly rather than attributed to an unprinted definition.

## Primary-source convention audit

The full publisher chapter is retained and read: de Fraysseix, Ossona de Mendez, Rosenstiehl, *Representation of Planar Hypergraphs by Contacts of Triangles*, GD2007, LNCS 4875, 125–136. [Publisher PDF](https://link.springer.com/content/pdf/10.1007/978-3-540-77537-9_15.pdf).

Its §1.1 requires finitely many vertices covered by nonempty edges; singleton edges are loops; “simple” means loopless linear. Its §2 uses a selected point set, including segment endpoints, to define contact incidence. Contacts are one-sided and noncrossing. Its Main Theorem uses triangles and segments, not expressly triangles alone. Section 4 states the convex-set/maximal-common-intersection consequence for simple hypergraphs, then Conjecture 2 uses “linear” without repeating “simple.” The chapter gives no separate formal convention for zero-length segments or triangle degeneracy. Its planar construction uses triangular faces; its final conjecture relaxes contacts to intersections. [Chapter, §§1–4](https://doi.org/10.1007/978-3-540-77537-9_15).

Consequently, the selected-point contact definition and the maximal-common-intersection convention must not be silently conflated. A singleton selected point can encode a nonmaximal singleton edge. A family consisting only of its inclusion-maximal intersecting subfamilies cannot do that. Filling triangle interiors is harmless in the displayed contact construction because those triangular faces are empty; that alone does not establish equivalence of filled and boundary-only triangles for arbitrary intersection representations.

The OPG page explicitly describes the same maximal-common-intersection consequence. It supplies no additional singleton or degeneration definition. [OPG problem](https://www.openproblemgarden.org/op/linear_hypergraphs_with_dimension_3).

## 1. Literal singleton obstruction and an exact repaired scope

For any finite family of nonempty sets indexed by V, its inclusion-maximal subfamilies with nonempty common intersection form a Sperner hypergraph: no two different resulting edges properly contain one another. This is immediate from maximality and does not depend on convexity, dimension, or geometric shape.

Take V={a,b} and E={e={a}, f={a,b}}. This hypergraph is linear and covers V. Its incidence poset has exactly the strict relations a<e, a<f, b<f. The two linear orders

L1: a < e < b < f,

L2: b < a < f < e

have precisely these relations in their intersection. Its dimension is two, because the poset is not a chain. Yet E is not Sperner. No family of arbitrary sets, let alone triangles and segments, has E as its maximal-common-intersection hypergraph.

This is a literal wording obstruction under the specified maximal-family semantics. It is not a refutation of the intended loopless geometric problem, and must not be presented as one.

For a linear hypergraph, any proper containment e⊂f forces |e|=1: otherwise |e∩f|≥2 contradicts linearity. Thus forbidding nested singleton edges is exactly the missing Sperner requirement. In a Sperner linear hypergraph every singleton edge {v} is an isolated one-vertex component. Removing these components leaves a loopless linear hypergraph, whose incidence poset is an induced subposet and has no larger dimension. Given a finite triangle/segment representation of the remaining part, put each deleted singleton in a separate distant triangle. This produces exactly the required isolated singleton edges. Conversely the loopless class is a subclass of the Sperner linear class. Therefore the conjecture for loopless linear hypergraphs is equivalent to the conjecture for Sperner linear hypergraphs, under these finite maximal-intersection conventions. Deleting nested singleton edges changes the original hypergraph; it is not an automatic representation-preserving simplification.

## 2. Arbitrarily many compulsory extreme witnesses obstruct local shrinking

For k≥4 let H_k be the star hypergraph on {c,u_1,...,u_k} with edges e_i={c,u_i}. Its incidence poset has a three-order realizer:

L1: c,u_1,e_1,u_2,e_2,...,u_k,e_k;

L2: c,u_k,e_k,u_(k-1),e_(k-1),...,u_1,e_1;

L3: u_1,u_2,...,u_k,c,e_1,e_2,...,e_k.

Each required incidence precedes its edge in all three orders. Two distinct leaves, two distinct edges, and a leaf versus a nonincident edge occur in opposite orders in L1 and L2. The incomparable pairs c,u_i are reversed by L3. This verifies the realizer without invoking a planar-graph theorem.

For k≥3 the dimension is exactly three. Suppose two extensions realized the poset. Each u_i must precede c in at least one of them. Three leaves force two leaves u_i,u_j before c in the same extension. In that extension u_i<e_j and u_j<e_i. Reversing both incomparable pairs in the other extension would force e_j<u_i<e_i<u_j<e_j, an impossibility.

Now set p_i=(i,i²), P_k=conv{p_1,...,p_k}, and S_i=[(i,i²),(i,i²−1/4)]. Assign P_k to c and S_i to u_i. For each i the affine functional

ell_i(x,y)=y−2ix+i²

is zero at p_i, equals (j−i)²>0 at p_j for j≠i, and equals −t<0 at (i,i²−t), 0<t≤1/4. Hence P_k∩S_i={p_i}; different S_i are disjoint because they have different x coordinates. The representation has exactly the maximal intersecting families {c,u_i}. Every p_i is an exposed vertex of P_k, using ell_i.

Suppose P_k is replaced by a triangle or segment T⊆P_k, keeping all leaves fixed and preserving their incidences with c. Since P_k∩S_i={p_i}, T must contain every p_i. An extreme point of P_k that lies in T⊆P_k must be an extreme point of T: a nontrivial convex expression inside T would also be one inside P_k. Thus T has at least k extreme points, contradicting the maximum of three. This obstruction is uniform in k.

It defeats a universal algorithm that first chooses an arbitrary convex representation and then shrinks each object to an inscribed triangle while keeping its contacts. It does not defeat moving objects or replacing an object by an enlargement. Indeed H_k itself has a simple segment representation: c is [0,k+1]×{0}, and u_i is {i}×[0,1]. Therefore no geometric counterexample to the conjecture is claimed.

## 3. Full-nerve correctness reduces to pairs and triples

Let H=(V,E) be a finite linear Sperner hypergraph with every vertex in an edge. Write D(H)={A⊆V: A⊆e for some e∈E}, with the empty face adjoined when necessary. Every minimal nonface has cardinality at most three.

Proof. Suppose A is a nonface with |A|≥4 and every proper subset is a face. Choose distinct a,b,c∈A. A triple {a,b,c} lies in some edge e. For any x∈A\{a,b,c}, the triple {a,b,x} lies in an edge f. Because e and f both contain a,b, linearity gives f=e. Thus A⊆e, contradiction. The same argument proves that if all subsets of A of size at most three are faces, then A is a face.

Consequently an arbitrary family of nonempty sets C_v has maximal-common-intersection hypergraph H if the following hold:

1. Every edge e has a common point in all C_v with v∈e.
2. C_u∩C_v is empty for every pair {u,v} not contained in an edge.
3. C_u∩C_v∩C_w is empty for every triple {u,v,w} not contained in an edge.

Necessity is immediate. For sufficiency, a set of indices with nonempty common intersection has all pairs and triples in D(H), hence itself lies in D(H). Conversely condition 1 realizes every face. Sperner maximality identifies the maximal faces with E. For convex subsets of the plane, condition 1 can additionally be checked on subfamilies of at most three by Helly's theorem, but that additional reduction is not needed here.

This gives a concrete audit condition: matching the pairwise intersection graph alone is insufficient. For instance three concurrent segments and the three sides of a triangle have the same pairwise intersection graph, but their maximal-common-intersection hypergraphs are respectively one triple and three pairs.

## 4. What the realizer theorem supplies, and what is still missing

Ossona de Mendez's *Realization of Posets* (JGAA6(1), 149–153,2002) proves a separation theorem for the images of differences of common lower sets. Its construction maps exponentially separated order coordinates to the affine plane by radial normalization. The printed growth condition on p151 is weaker than the inequality used in the next paragraph; choosing F_i(x)=B^(rank_i(x)), B>d, supplies the needed stronger inequality. This discrepancy was checked against the rendered publisher PDF, not inferred solely from text extraction. [JGAA article and PDF](https://jgaa.info/index.php/jgaa/article/view/paper48).

The chapter's p135 maximal-intersection consequence is a credited prior assertion, not a new theorem here. The 2002 paper does not explicitly state that simply taking convex hulls of normalized dual-edge coordinates gives the whole required hypergraph nerve, and the 2008 chapter does not provide the omitted deduction. Separation of symmetric differences alone does not transparently establish the required triple-intersection conditions. Accordingly that specific coordinate-hull formula has not been certified in this lane.

The star obstruction shows why even an exact initial convex representation does not make a triangle bound automatic: witness counts can be arbitrarily large and all forced witnesses can be exposed. The [convex-reduction report](CONVEX_REDUCTION_PROOFS.md) develops a stronger fixed-neighbor obstruction and the maximum-degree-three consequence of the credited convex-representation result. Those proofs are not duplicated or claimed as recovered historical work here.

## Literature boundary

Gonçalves's author-hosted three-page preprint, dated January 17,2008, was visually read in full. Its objects are points for vertices and segments for edges, with pairwise segment intersections exactly the points assigned to common vertices. It supplies the known segment-only obstruction; it does not establish a mixed-triangle obstruction. [Author PDF](https://www.lirmm.fr/~goncalves/pmwiki/uploads/counter.pdf), [published DOI](https://doi.org/10.1016/j.ejc.2007.12.004).

Dobler, Kobourov, Mondal and Nöllenburg's *Representing Hypergraphs by Point-Line Incidences* is published in DMTCS 28:3#3(2026), accepted June 25 and published August 19; arXiv2411.13985v4 is dated July 26,2026. Sections1–2 and7, plus the references, were inspected. It distinguishes point/line incidence, crossings, and overlaps. These distinctions cannot be erased by swapping the words “vertex” and “edge.” Its concluding questions concern those representation models, and it does not supply a status determination for the exact mixed-object conjecture. [Publisher](https://dmtcs.episciences.org/en/articles/15876), [version4](https://arxiv.org/abs/2411.13985v4).

Exact-phrase and related primary-source searches found the original conjecture and relevant adjacent work. This is a record of limited searches, not evidence that no later or unindexed resolution exists. Copied source documents, extracted source text, executable programs, and nonmathematical operational records are not distributed in this prose edition.
