# Incidence dimension of the root-5 block wedge

This note concerns the fourth substantive pass on the triangle-representation problem. It is an incidence-order result, not a geometric nonrepresentability result and not a solution of the general conjecture.

## 1. Family, conventions, and claim

Let B have vertices 1,2,3,4,5 and the six hyperedges

    a=12, b=23, c=34, d=14, e=135, f=245.

For each integer k>=1, let W_k consist of k otherwise disjoint copies of B with all copies of vertex 5 identified to one vertex r. Write vj_i for source vertex j in block i, where 0<=i<k. The edge labels a_i,...,f_i retain their source meaning. The incidence poset has the vertices as minimal elements and the edges as maximal elements; its only strict relations are v<h when v is a member of h.

**Theorem.** The incidence poset of W_k has dimension 3 for 1<=k<=3, and dimension 4 for every k>=4.

W_k is finite, covered, loopless, and linear. It has 4k+1 vertices and 6k maximal hyperedges. Every nonroot vertex has degree 3, while r has degree 2k. Every incidence-graph node has degree at least 2, so the whole incidence graph is its 2-core. The graph is connected. Its first block contains the nonplanar subdivision described in Section 6. In particular W_2 gives a 9-vertex, 12-edge example with a degree-4 vertex inside the cyclic incidence 2-core and a three-order realizer; W_3 similarly has root degree 6. These examples exceed a theorem restricted to vertex degree at most 3 in that core.

The root-degree obstruction below is to having a three-order realizer, not to having a triangle representation. The same family may be representable geometrically even when its incidence dimension is 4. No geometry is inferred from failure of an order encoding.

## 2. A sufficient certificate using vertex permutations

Suppose H is a finite covered clutter, so no distinct hyperedges contain one another. A family of vertex permutations is sufficient for an incidence realizer if:

1. For each ordered pair of distinct vertices (u,v), some permutation places u before v.
2. For each hyperedge h and each vertex v outside h, some permutation places every member of h before v.

Expand each permutation by inserting each edge immediately after its last member, before the next vertex, with any fixed ordering among simultaneous edges. Every expansion is a linear extension. The intersection has exactly the desired relations, by the following complete pair-type check.

* An incident vertex precedes its edge in every expansion.
* Distinct vertices occur in both directions by condition 1.
* For a nonincident pair (v,h), condition 2 gives h before v in some expansion. Choose any w in h; condition 1 supplies an expansion with v before w, hence v before h. Thus this pair is incomparable.
* For distinct edges h,g, choose u in h minus g and w in g minus h. Condition 2 for (g,u) gives g before u before h; condition 2 for (h,w) gives h before w before g. Thus the edges are incomparable.

This proves sufficiency without invoking a solver. Conversely, restricting any incidence realizer to its vertices gives both conditions: to reverse a missing incidence h<v, all members of h must be before v in that order. This converse is not needed for accepting the positive certificates but explains the exploratory search encoding.

## 3. Exact three-order certificates

The following vertex permutations for W_2 satisfy the two conditions in Section 2:

    v2_1 v1_1 v4_1 v4_0 v3_0 v2_0 r v1_0 v3_1
    v2_1 v3_1 v4_1 r v1_1 v3_0 v1_0 v2_0 v4_0
    v3_1 v1_0 v4_0 v2_0 r v3_0 v1_1 v4_1 v2_1

Their fully expanded linear extensions are:

    v2_1 v1_1 a_1 v4_1 d_1 v4_0 v3_0 c_0 v2_0 b_0 r f_0 f_1 v1_0 a_0 d_0 e_0 v3_1 b_1 c_1 e_1
    v2_1 v3_1 b_1 v4_1 c_1 r f_1 v1_1 a_1 d_1 e_1 v3_0 v1_0 e_0 v2_0 a_0 b_0 v4_0 c_0 d_0 f_0
    v3_1 v1_0 v4_0 d_0 v2_0 a_0 r f_0 v3_0 b_0 c_0 e_0 v1_1 e_1 v4_1 c_1 d_1 v2_1 a_1 b_1 f_1

Here is a corresponding W_3 vertex certificate:

    v4_2 v3_1 v3_2 v1_2 v2_1 v4_1 r v1_1 v2_2 v4_0 v2_0 v1_0 v3_0
    v2_1 v1_1 v3_0 v2_0 v1_0 v4_1 r v4_0 v3_1 v4_2 v2_2 v1_2 v3_2
    v3_2 v4_0 v2_2 v3_0 v1_2 v1_0 r v2_0 v4_2 v1_1 v3_1 v4_1 v2_1

The machine-readable EXACT_CERTIFICATES.json contains both sets of raw vertex permutations, full expanded orders, and an explicit witnessing order for every ordered vertex pair and every missing vertex-edge incidence. The package checks these witnesses and also independently compares the intersection of the raw full orders against every ordered pair of incidence elements. For W_2 this is all 420 ordered pairs on 21 elements, with exactly 28 strict incidences. For W_3 it is all 930 ordered pairs on 31 elements, with exactly 42 strict incidences. The verifier uses integer comparisons, and its checks do not depend on Python assert statements or on optimization flags.

The W_3 certificate gives the upper bound 3 also for W_1 and W_2 by restriction. Each block contains the standard example S3 on minimal elements 1,2,3 and maximal elements a,b,e. The three missing pairs e<2, b<1, a<3 require separate extensions: any two such reversals, together with cross incidences, would make a directed cycle. Therefore every W_k has dimension at least 3.

These orders were found by a private finite mixed-integer search and are new certificates supplied here. Their validity rests only on the displayed orders and the exact checker, not on the search solver, its tolerance, or any infeasibility report.

## 4. An analytic obstruction to four blocks in three orders

### 4.1 The source block cannot have its root first in two extensions

Assume three linear extensions realize B and that r is before all four nonroot vertices in L1 and L2. Each nonroot vertex must then be before r in L3. Put A={1,3}, B'={2,4}, and use e=A union {r}, f=B' union {r}.

The missing incidences e<2 and e<4 must each be reversed in L1 or L2, since in L3 all nonroot vertices precede r<e. Likewise f<1 and f<3 must each be reversed in L1 or L2. One extension cannot contain both a reversal e<b for b in B' and a reversal f<a for a in A: it would contain

    a < e < b < f < a.

Consequently all e-before-B' reversals must occur in one of L1,L2, and all f-before-A reversals in the other. Relabel the extensions so L1 places A before B', and L2 places B' before A.

Let q be the earlier of the two B' vertices in L1, and let b be the other. For either a in A, the two-element edge {a,b} is nonincident with q. It cannot precede q in L1 because q<b, and cannot precede q in L2 because q<a. Thus {a,b}<q in L3 for both choices of a. It follows that all other nonroot vertices precede q in L3.

Similarly, let p be the earlier A vertex in L2, and let a be the other. For both b in B', the edge {a,b} cannot precede p in L1 (p<b) or L2 (p<a), so it precedes p in L3. Thus every other nonroot vertex precedes p in L3. Since p and q are distinct, this requires both p<q and q<p, a contradiction. This is a finite analytic proof; exhaustive permutation search is not being used as the lower-bound argument.

### 4.2 Each block consumes a distinct sole-after-root order

Suppose W_k had a three-order realizer. Restrict it to a block. We claim some vertex of that block lies after r in exactly one of the three orders.

Every vertex must be on each side of r in at least one order. If the claim failed, each of the four nonroot vertices would lie after r twice and before r exactly once. Every nonroot edge 12,23,34,14 must precede r in some extension, because it is incomparable with r. Its two endpoints must therefore have the same unique before-r extension. The cycle 1-2-3-4-1 is connected, so all four vertices have the same before-r extension. In the remaining two extensions r precedes every nonroot vertex, contradicting Section 4.1. The claim follows.

For each block i choose such a vertex x_i, and let t_i be the only extension in which r<x_i. Choose a root-containing edge g_i incident with x_i; this is e_i or f_i. If distinct blocks i,j had t_i=t_j=t, then the missing incidence g_i<x_j could only be reversed in extension t: in the other two orders x_j<r<g_i. Likewise g_j<x_i could only be reversed in t. That extension would contain

    x_i < g_i < x_j < g_j < x_i,

which is impossible. Therefore the k blocks have distinct values t_i in {1,2,3}, and k<=3. Hence dimension is at least 4 for every k>=4.

## 5. A uniform four-order upper bound

Start with the following three local orders on one block, obtained by moving r to the front of source-based vertex permutations and expanding as in Section 2:

    r 2 1 a 3 b e 4 c d f
    r 4 2 f 3 b c 1 a d e
    r 1 4 d 3 c e 2 a b f

Their restrictions to the ten nonroot incidence elements realize the induced nonroot subposet. One way to check this is to start with the published three-order realizer cited in Section 6: moving r to the front preserves all vertex comparisons among the other four vertices and preserves the witness for every missing incidence whose excluded vertex is not r. Section 2 then checks all pairs of nonroot elements. Direct exact local comparison provides an independent check.

Construct L1 by writing r, then these first-order nonroot suffixes for blocks in increasing index order. Construct L2 from the second suffixes in decreasing block order, again with r first. Construct L3 from the third suffixes in increasing block order, again with r first. Finally construct L4 by writing:

    all nonroot vertices; all nonroot edges a_i,b_i,c_i,d_i; r; all root edges e_i,f_i.

Within each of these four groups choose any fixed total order. Every displayed order is a linear extension. The complete pair-type proof is:

* Within any block, pairs of nonroot elements are already correct in L1,L2,L3. Adding a linear extension cannot remove required incidences or introduce new comparisons.
* Between distinct blocks, any two nonroot elements occur in opposite orders in L1 and L2.
* Root r and a nonroot vertex are in opposite orders in L1 and L4.
* Root r and any nonroot edge are in opposite orders in L1 and L4.
* Root r precedes every incident root edge in all four extensions, as required.

These types exhaust all pairs. Thus dimension is at most 4 for all k. Together with Sections 3 and 4 this proves the theorem, including the exact threshold. The finite tests at k=1,...,20,32,64 check implementations of this formula, not the validity of an unproved extrapolation.

## 6. Source credit and nonplanarity certificate

The five-vertex example B, its dimension-three status, and its nonplanar incidence graph occur on printed page 135 of H. de Fraysseix, P. Ossona de Mendez and P. Rosenstiehl, *Representation of Planar Hypergraphs by Contacts of Triangles*, Graph Drawing 2007, LNCS 4875 (2008), pp. 125-136. DOI: https://doi.org/10.1007/978-3-540-77537-9_15 . Publisher PDF: https://link.springer.com/content/pdf/10.1007/978-3-540-77537-9_15.pdf . This note does not claim that base example as new, and does not assert a literature novelty result for the wedge theorem.

For explicit credit, the published realizer, transcribed into these labels, is:

    2 1 a 3 b r e 4 f d c
    r 4 2 f 3 c b 1 e a d
    1 4 d 3 c r e 2 f a b.

For nonplanarity, suppress the degree-two incidence nodes a,b,c,d and the degree-two source vertex 5 within a single block. The branch-node bipartition is {1,3,f} and {2,4,e}. Its nine internally disjoint paths are 1-a-2, 1-d-4, 1-e, 3-b-2, 3-c-4, 3-e, f-2, f-4, f-5-e. They give a subdivision of K3,3. Each W_k contains this block as an incidence-graph subgraph.

## 7. Verification scope

The supplied exact positive checks run under normal Python, -O, and -OO with identical outputs. Genuine negative controls corrupt raw orders, erase a required third order, replace the fourth order in the general construction, and remove the reverse block ordering; each must fail with VerificationError in every mode. These controls check both fixture integrity and mathematical comparisons. They are not evidence for a geometric impossibility.

This prose edition contains this complete authored proof, the complete finite realizer certificates, the accompanying verification summaries, and public source identities. Programs and raw computational outputs are excluded from the distributed edition and retained separately for recovery. No third-party source text, private coordination material, or dataset contents are required by or included in the public proof packet.
