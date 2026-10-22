# Inserting complete nonplanar cyclic blocks across a private triangle side

## Result and scope

This fourth substantive pass proves a cyclic-block insertion theorem and gives exact dimension-three examples outside the previously accepted incidence-2-core degree bound. It does not solve the general triangle-representation problem or claim novelty or current literature status.

Let F have vertices 1,2,3,4,5 and edges

    a=12, b=23, c=34, d=14, e=135, f=245.

This is the nonplanar example in de Fraysseix, Ossona de Mendez and Rosenstiehl, *Representation of Planar Hypergraphs by Contacts of Triangles*, p. 135. The nonplanarity refers to its incidence graph. [Published chapter](https://doi.org/10.1007/978-3-540-77537-9_15).

The principal new deductions are:

1. F has a rational nondegenerate triangle representation with any specified vertex replaced by a closed half-plane.
2. Consequently, a whole copy of F can be attached at any private side arc of an existing representing triangle, identifying exactly one vertex and leaving every old triangle unchanged. Every new vertex has a private side arc, so entire nonplanar cyclic blocks can be inserted recursively.
3. Two copies identified at their degree-two vertex 5 have incidence dimension exactly three and a rational triangle representation. The common vertex has degree four entirely inside the incidence 2-core.
4. For every k>=1, k copies identified at vertex 1 have incidence dimension exactly three and a rational triangle representation. Their common vertex has degree 3k entirely inside the incidence 2-core. These are connected nonplanar examples with unbounded cyclic-core degree.

The universal insertion proof uses a rooted half-plane representation, not merely the existence of a private arc in an arbitrary representation of the new block. The private-arc hypothesis concerns the old triangle only. No arbitrary block-gluing or preservation of incidence dimension under vertex identification is asserted.

All hypergraphs here are finite, covered, loopless and linear. A representing triangle is its closed filled convex hull, and the nerve records common intersections of every subfamily. Hyperedges are the maximal nerve faces. Intersections are unrestricted; these are not contact representations or representations by triangle boundaries.

## 1. A one-sided block insertion lemma

Let H have a representation by nondegenerate rational triangles T_v. Suppose the boundary of T_v has a side-interior point p with an open neighborhood U meeting no other old triangle, and within which T_v agrees with one closed half-plane.

Let G be another finite covered loopless linear hypergraph with a distinguished root r. Suppose G is represented by the closed half-plane

    D_r = {(x,y): y<=0}

and bounded nondegenerate rational triangles D_u for every u different from r. The full nerve, including subfamilies containing r, must be exactly the downward closure of G.

Form H union_v G by retaining all old vertices and whole old edges, taking a fresh copy of every vertex of G other than r, identifying r with v, and retaining every whole edge of G with that replacement.

**Lemma.** H union_v G has a rational nondegenerate triangle representation that leaves every old triangle unchanged.

**Proof.** Rational side-interior points are dense on a side with rational endpoints. Since the private neighborhood is open, replace p if necessary by such a rational point. A rational invertible affine chart sends p to the origin and identifies the inside of T_v locally with y<=0. The union of the finitely many bounded D_u, u different from r, is bounded. Apply a sufficiently small positive rational scaling about the origin so that every scaled D_u lies inside the private neighborhood. Map these triangles back through the rational affine chart.

Among the new triangles and T_v, every intersection is exactly the corresponding intersection with the model half-plane D_r: the entire new family is inside the neighborhood where T_v and that half-plane agree. Thus their full nerve is G. Every new triangle misses every other old triangle by privacy of the neighborhood. An intersecting subfamily containing a new vertex therefore cannot contain an old vertex other than v. Old-only subfamilies retain exactly their old intersections. These cases exhaust all subfamilies, proving the whole-nerve assertion. The affine maps preserve nondegeneracy and rational coordinates. QED.

The amalgam remains covered, loopless and linear: an old and a new edge can share only v, and the internal linearity of each input is unchanged. No edge becomes a subset of another because each has at least two vertices and different edges share at most one.

The previously accepted private-boundary lemma supplies the old private arc whenever deg_H(v)>=2: in a correct compact convex representation of a loopless linear hypergraph, the intersections with neighbors belonging to different incident hyperedges are nonempty disjoint compact groups. A finite disjoint closed cover of the connected polygon boundary would force one group to cover the whole boundary. Convexity about that group's common edge witness would then make that group cover the entire polygon, contradicting another incident group. Thus a private boundary point exists, and an open neighborhood contains a side-interior private point. This lemma is used only in its accepted form.

If every new vertex of G has degree at least two, each has a private arc immediately after insertion. The old root now also has degree at least two, and its private arc can be found afresh. Every other old vertex keeps its previous privacy because all new triangles avoid it. This justifies any finite sequence of the stated insertions.

## 2. Rooting the nonplanar block at its degree-two vertex

Use root 5 and D_5={y<=0}. Before thickening, assign these four segments:

    S1: (0,0) to (2,2)
    S2: (3,0) to (1,2)
    S3: (0,0) to (3/2,3)
    S4: (3,0) to (3/2,3).

Their six pairwise intersections are

    S1 intersect S2 = {(3/2,3/2)}
    S2 intersect S3 = {(1,2)}
    S3 intersect S4 = {(3/2,3)}
    S1 intersect S4 = {(2,2)}
    S1 intersect S3 = {(0,0)}
    S2 intersect S4 = {(3,0)}.

These are pairwise distinct. No three of S1,S2,S3,S4 have a common point. The half-plane meets S1 and S3 only at (0,0), and S2 and S4 only at (3,0). Consequently the six maximal faces are precisely a,b,c,d,e,f above. This explicitly verifies the entire nerve: a subfamily of at least three nonroot segments is empty, and a subfamily containing the root can intersect only inside one of the two endpoint groups.

Here and below, for a segment [p,p+u], define its thin triangle by

    Delta_eta(p,u) = conv{p-eta*u-eta*J(u),
                           p-eta*u+eta*J(u),
                           p+(1+eta)*u},

where J is counterclockwise quarter-turn and eta>0. This triangle is nondegenerate and contains the whole segment in its interior. It tends to the segment in Hausdorff distance as eta tends to zero.

For sufficiently small rational eta, replacing all four segments by these triangles preserves the full nerve with the root half-plane fixed. To justify using compact-nerve stability, first truncate the half-plane to a sufficiently large rational triangle whose top side lies on y=0. On a neighborhood of all four segments near y<=0, the truncated triangle and the half-plane agree. The finite compact family has a positive gap for every empty subfamily, so sufficiently small outer perturbations preserve all those nonfaces. Original edge witnesses remain; at each root endpoint, the new nonroot triangles contain a small open disk, and its portion below y=0 supplies a strict common interior witness. The same local agreement transfers this conclusion back to the half-plane.

The exact choice eta=1/1000 works. The rational verifier checks it using independent polygon clipping and active-line intersection methods on all 31 nonempty subfamilies. Exact strict witnesses are

    a: (3/2,3/2), b: (1,2), c: (3/2,3), d: (2,2),
    e: (0,-1/1000), f: (3,-1/1000).

In the oriented edge inequalities used by the checker, every incident triangle inequality and every applicable half-plane inequality has positive slack; the minimum is 1/125000. This is an exact finite certificate of the displayed parameter choice, not a floating-point claim.

## 3. Rooting the same block at a degree-three vertex

Use root 1 and D_1={y<=0}. Assign

    S2: (-2,0) to (0,4)
    S4: (2,0) to (0,4)
    S5: (0,0) to (0,4)
    K3 = conv{(-1,2),(1,2),(0,0)}.

The root meets S2 at (-2,0), S4 at (2,0), and both S5 and K3 at (0,0). The three segments S2,S4,S5 meet at (0,4), outside K3. The intersections of K3 with S2 and S4 are respectively the points (-1,2) and (1,2); its intersection with S5 is the vertical segment from (0,0) to (0,2). These calculations give exactly the maximal faces a,b,c,d,e,f and exclude every other triple, hence every larger nonface.

Thicken the three segments by Delta_eta. Dilate K3 by factor 1+eta about its centroid (0,4/3). The same compact truncation and stability argument proves correctness for sufficiently small positive rational eta. Again eta=1/1000 is verified exactly. Strict witnesses are

    a: (-2,-1/1000), b: (-1,2), c: (1,2),
    d: (2,-1/1000), e: (0,-1/1000), f: (0,4).

The minimum exact oriented-inequality slack is 1/62500. Both independent algorithms again check all 31 nonempty subfamilies.

The cyclic permutation 1->2->3->4->1, fixing 5, is an automorphism of F: it rotates a,b,c,d and swaps e,f. Therefore the construction in this section provides a rooted half-plane representation at any of the four degree-three vertices. Together with Section 2, every possible root of F is covered.

## 4. Recursive insertion of complete cyclic blocks

**Theorem.** Let H have a rational nondegenerate triangle representation. At any vertex with a private side arc, attach a fresh copy of F by identifying any one of its vertices with that vertex of H. Any finite sequence of these operations is representable by rational nondegenerate triangles, preserving all initial triangles. It is sufficient that each initial attachment vertex have degree at least two. After the first insertion, any vertex introduced by a block is an eligible attachment vertex.

**Proof.** Choose the rooted model from Section 2 or 3 and apply the lemma. Every vertex of F has degree at least two, so every newly introduced triangle has a private arc by the private-boundary lemma. Reapply the lemma finitely many times. Full-nerve correctness holds at each step. QED.

Pendant hyperedge insertion from the accepted previous pass can be interspersed, subject to its stated private-arc condition. In particular, one may start with an accepted degree-three or core-extension representation and then insert any finite tree of these nonplanar blocks at eligible roots, followed by any authorized pendant reconstruction. These operations are exact vertex amalgamations of whole original edges. They do not merely attach new leaves: every incidence edge of a newly inserted F lies inside a nontrivial cyclic block.

This theorem does not infer that the resulting incidence dimension remains at most three. The following two families verify that hypothesis separately and therefore genuinely enter the intended dimension-three class.

## 5. A nonplanar degree-four cyclic-core example

Take two copies F_0,F_1 and identify their vertices 5 with a single vertex r. Write 1_i,2_i,3_i,4_i for the other vertices in block i, and a_i,...,f_i for its six edges. In particular

    e_i={1_i,3_i,r}, f_i={2_i,4_i,r}.

The other four edges are the corresponding pairs. The resulting hypergraph has nine vertices and twelve edges. Its common vertex r has degree four. Every other vertex has degree three, and every edge has size two or three. Thus its entire incidence graph has minimum degree at least two and is its own 2-core. The degree-four contribution is wholly cyclic.

Three incidence orders are:

    2_1 1_1 a_1 4_1 d_1 4_0 3_0 c_0 2_0 b_0 r f_0 f_1 1_0 a_0 d_0 e_0 3_1 b_1 c_1 e_1
    2_1 3_1 b_1 4_1 c_1 r f_1 1_1 a_1 d_1 e_1 3_0 1_0 e_0 2_0 a_0 b_0 4_0 c_0 d_0 f_0
    3_1 1_0 4_0 d_0 2_0 a_0 r f_0 3_0 b_0 c_0 e_0 1_1 e_1 4_1 c_1 d_1 2_1 a_1 b_1 f_1.

These orders were obtained in the parallel realizer search and independently checked here on all 420 ordered pairs of distinct elements. Their intersection contains exactly the required incidences. The induced restriction of either block to vertices 1,2,3 and edge labels a,b,e is S3: the missing pairs (1,b),(2,e),(3,a) require three different reversing orders because reversing two would make a directed alternating cycle using the two cross-incidences. Thus the incidence dimension is exactly three.

An explicit rational triangle certificate is particularly simple. Use the root-5 triangles from Section 2; translate block i by (5i,0); replace the common root by

    R = conv{(-4,0),(14,0),(5,-20)}.

The four nonroot triangles in different blocks have disjoint horizontal projections. On all their portions below y=0, R agrees with the lower half-plane. Thus the full nerve is exactly the amalgam. Both exact intersection methods verify all 511 nonempty subfamilies; exactly 33 are faces, with the twelve stated maximal edges, and every edge has a strict common witness.

Each copy's incidence graph contains the following K3,3 subdivision, with branch parts {1,3,f} and {2,4,e}:

    1-a-2, 1-d-4, 1-e;
    3-b-2, 3-c-4, 3-e;
    f-2, f-4, f-5-e.

All nine paths have pairwise disjoint interiors and the required distinct branch endpoints. They persist in the amalgam, proving connected nonplanarity. The degree-four cyclic core therefore lies strictly outside the prior sufficient theorem.

## 6. Unbounded degree entirely inside the cyclic core

For every k>=1, instead identify vertex 1 of k disjoint copies of F with r. The other vertices are 2_i,3_i,4_i,5_i; the edge labels are a_i,...,f_i. This family has 4k+1 vertices and 6k hyperedges. Its common vertex has degree 3k; all other vertices have degree two or three, and all edge-nodes have degree two or three. The entire connected incidence graph is again its 2-core. Every member contains the displayed K3,3 subdivision and an induced S3.

For each block define the following word patterns, with every symbol indexed by i:

    P_i = 2_i a_i 3_i b_i 5_i e_i 4_i c_i d_i f_i
    Q_i = 4_i d_i 3_i c_i 5_i e_i 2_i a_i b_i f_i
    B_i = 2_i 4_i 5_i f_i 3_i b_i c_i
    A_i = a_i d_i e_i.

A uniform three-order realizer is

    L1 = r P_0 P_1 ... P_(k-1)
    L2 = r Q_(k-1) Q_(k-2) ... Q_0
    L3 = B_0 B_1 ... B_(k-1) r A_0 A_1 ... A_(k-1).

**Proof.** Restricted to any block and r, these are precisely the previously checked source-block realizer

    1 2 a 3 b 5 e 4 c d f
    1 4 d 3 c 5 e 2 a b f
    2 4 5 f 3 b c 1 a d e.

Thus every required incidence, every within-block incomparable pair, and every pair involving r have exactly their required relation. Two distinct elements in different blocks are incomparable. L1 puts all elements of the lower-index block first, whereas L2 puts all elements of the higher-index block first. Therefore every cross-block pair is reversed. These cases exhaust all distinct pairs, proving the realizer for every k. The inherited S3 gives dimension exactly three. QED.

For explicit rational triangles, translate the Section 3 nonroot triangles of block i by (5i,0), and use

    R_k = conv{(-4,0),(5k+4,0),(5k/2,-5k-10)}

for the common root. Each block's nonroot triangles has horizontal projection contained in [5i-1003/500,5i+1003/500]. These intervals are pairwise disjoint. Their portions below y=0 have y>=-3/500, and the sides of R_k at these heights remain strictly outside their horizontal range. Hence replacing the half-plane by R_k changes no intersection with them. Alternatively the insertion theorem gives the same existence conclusion. This proves rational triangle representability for the entire family.

The exact checker verifies the full nerves for k=1,2, all pairs and triples and each declared edge for k=3, and complete incidence-order relations for k=1,2,3,5,10,30. The proof above, not those finite values, supplies the universal quantifier.

## 7. Verification, preservation, and unresolved boundary

Two independently implemented exact rational intersection procedures are used: successive polygon clipping, including point and segment intermediates, and enumeration of intersections of independent active boundary lines. Every tested subfamily with a nonroot triangle is bounded; a nonempty bounded planar polyhedron has an extreme point with two independent active constraints, so the second procedure decides these cases exactly. A singleton root half-plane is handled directly.

The checker includes point-contact, segment-contact, disjoint-triangle, and triple-contact controls. It checks strict common witnesses, whole incidence relations, every core node and its degree, and the K3,3 subdivision. A separate recursive fixture actually finds rational private side points and admissible rational scales, attaches a root-5 block at a nonroot triangle, then a root-1 block at a newly introduced triangle, and verifies that every old triangle is unchanged. Its nine-vertex intermediate nerve is checked on all 511 nonempty subfamilies; the thirteen-vertex result is checked on every pair and triple and every declared edge. No incidence-dimension claim is made for this additional geometric regression. All gates are explicit VerificationError exceptions. Source-mutation tests use disposable copies and require the intended rejection diagnostic under normal Python, -O, and -OO. No timeout counts as a rejection. Deterministic output equality and complete archive and content-addressed-store restorations are recorded separately.

The advance is the ability to add several mutually constrained new vertices as a complete cyclic nonplanar block, while preserving the old representation. It is stronger than pendant-hyperedge insertion and reaches degree four, and arbitrarily high degree, within the incidence 2-core. It does not connect two already constrained old triangles to one new block: all interblock sharing is at one old vertex. Nor does it show that an arbitrary degree-three block has a rooted half-plane representation. The general problem, including genuinely multi-parent attachment and unrestricted high degree in an indivisible cyclic block, remains unresolved.

The accepted normalized-coordinate full-nerve construction and the earlier private-boundary and pendant-extension proofs were read together with their full independent reviews before this argument. The coordinate construction remains credited to the rapidly increasing coordinates and radial normalization in Ossona de Mendez, *Realization of Posets*, JGAA 6(1), 149–153. [Publisher article](https://jgaa.info/index.php/jgaa/article/view/paper48). No source document, source text, private coordination, or dataset content is included in this public report.
