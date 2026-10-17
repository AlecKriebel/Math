# Gluing nonplanar triangle blocks across two existing vertices

## Result and scope

This fifth and final substantive pass proves a genuine two-parent insertion theorem. A whole nonplanar cyclic block can be joined simultaneously to two existing triangles along a maximal two-vertex hyperedge. This goes beyond the earlier single-root and pendant operations. It does not settle the general triangle-representation problem, and no literature novelty or current-status claim is made.

Throughout, hypergraphs are finite, covered, loopless and linear. A triangle means a nondegenerate closed filled triangle. The full common-point nerve, rather than just the pairwise intersection graph, must be the downward closure of the specified edges. Intersections have no boundary-only, contact, or disjoint-interior restriction. Listed hyperedges are the maximal faces. Linearity and looplessness make the edge family a clutter.

Let F have vertices 1,2,3,4,5 and edges

    a=12, b=23, c=34, d=14, e=135, f=245.

The source block, its three-dimensional incidence poset and its nonplanar incidence graph are due to de Fraysseix, Ossona de Mendez and Rosenstiehl, *Representation of Planar Hypergraphs by Contacts of Triangles*, printed page 135. They are not claimed as new. [Published chapter](https://doi.org/10.1007/978-3-540-77537-9_15).

The new conclusions established here are:

1. F has a rational model in which 1 and 2 are the crossing half-planes x<=0 and y<=0, and every other object is a bounded nondegenerate rational triangle.
2. In any triangle-representable covered loopless linear hypergraph, an edge {u,v} with deg(u),deg(v)>=2 supports insertion of a fresh copy of F, identifying 1 with u, 2 with v, and their pair-edge. An initial nerve-preserving rational generic normalization may be needed. After that normalization, the insertion leaves every old triangle exactly unchanged. If the supplied family already has a transverse crossing, no normalization is needed.
3. These insertions can be iterated along eligible old or newly introduced pair-edges. Their use does not assert that incidence dimension remains at most three.
4. There is an explicit family A_k of k copies of F sharing only 1,2 and their edge a. It has 3k+2 vertices and 5k+1 edges, root degrees 2k+1, a nonplanar incidence graph with no cutvertex, a rational triangle representation, and incidence dimension exactly three for every k>=1.

The complete prior rooted-block proof and review, private-boundary/core review, and normalized-coordinate review were read. The present result needs only a valid starting triangle representation. When using the prior degree-three base, the rapidly increasing coordinates and radial normalization remain credited to Ossona de Mendez, *Realization of Posets*. [Publisher article](https://jgaa.info/index.php/jgaa/article/view/paper48).

## 1. Exact model with two half-plane roots

Put

    H1={x<=0}, H2={y<=0},
    P=(-1,2), Q=(2,-1), R=(2,2), S=(-1,4), T=(4,-1),
    K3=conv{P,R,T}, K4=conv{Q,R,S}, K5=[P,Q].

The original suggestion for these points has been independently checked. A convenient exact description is

    K3: y<=2, 3x+5y>=7, 3x+2y<=10;
    K4: x<=2, 5x+3y>=7, 2x+3y<=10;
    K5: x+y=1, -1<=x<=2.

Substitution of y=1-x into the lower inequality of K3 gives x<=-1; into that of K4 it gives x>=2. Consequently K3 intersect K5={P} and K4 intersect K5={Q}.

K3 and K4 meet at R. Their intersection cannot have x<=0: K3 gives y<=2, whereas K4 requires 5x+3y>=7. These bounds would give 5x+3y<=6. By exchanging x,y, their intersection cannot have y<=0 either. Thus it lies strictly in the positive quadrant.

None of K3,K4,K5 meets H1 intersect H2. The inequalities 3x+5y>=7, 5x+3y>=7, and x+y=1 prove this immediately. Also H1 intersect K4 intersect K5 is empty because Q has positive x, and H2 intersect K3 intersect K5 is empty because P has positive y. The triple K3,K4,K5 is empty because its point would have to be both P and Q.

These statements account for all eight forbidden triples. The two allowed triples are 135 at P and 245 at Q. The four pair-only maximal faces have witnesses a at (-1,-1), b at T, c at R and d at S. Every one of the ten pairs is contained in one of these six faces. Every four- or five-element family contains a forbidden triple. This proves the full 31-subfamily nerve, including all higher nonfaces.

### Rational nondegenerate thickening

For eta>0, dilate K3 and K4 by factor 1+eta about their respective centroids. For a segment [p,p+u], set

    Delta_eta(p,u)=conv{p-eta*u-eta*J(u),
                       p-eta*u+eta*J(u),
                       p+(1+eta)*u},

where J is the counterclockwise quarter-turn. Replace K5 by Delta_eta(P,Q-P). The original triangles and segment lie in the interiors of their replacements. All six old witnesses therefore become strict common interior witnesses; each already lies strictly inside any relevant root half-plane. The roots stay fixed.

For sufficiently small positive eta all nonfaces persist. For an empty subfamily containing a bounded nonroot object, the continuous maximum of the distances to its finitely many original closed sets is coercive and attains a positive minimum. A sufficiently small uniform Hausdorff change in the bounded objects cannot erase that minimum. There are only finitely many subfamilies. The unbounded root-only families are all nonempty and need no gap. This handles the half-planes without incorrectly invoking a compact-family lemma on unbounded roots.

The explicit choice eta=1/1000 is certified. The three new triangles have vertices

    D3: (-376/375,2001/1000), (6001/3000,2001/1000),
        (12007/3000,-501/500);
    D4: (2001/1000,-376/375), (2001/1000,6001/3000),
        (-501/500,12007/3000);
    D5: (-503/500,2), (-1,1003/500), (2003/1000,-1003/1000).

The exact verifier orients each triangle counterclockwise and uses its three unnormalized supporting inequalities a*x+b*y<=c. At the witnesses (-1,-1), T, R, S, P, Q for a,b,c,d,e,f, respectively, the minimum slack over every incident inequality is 9/500000>0.

There are exact nonnegative Farkas multipliers for each of the eight forbidden triples. The negatives of their summed right sides, after the multipliers are normalized to sum one, are

    123: 7003997/9008000; 124: 7003997/9008000;
    125: 1498491/3506000; 134: 497497/3502500;
    145: 3988979/3996000; 234: 497497/3502500;
    235: 4006975973/4018012000; 345: 898188291/701000000.

In each certificate the weighted normals sum exactly to zero. These are strict infeasibility margins, not floating-point tolerances. Their positive minimum is 497497/3502500. In particular all eight nonfaces remain empty if every supporting right side is independently increased by less than that minimum, with the displayed normals fixed. Strict witnesses and the finite nonface gaps also imply an open neighborhood of the triangle vertex coordinates with the same nerve. Raw multipliers, inequalities and all 31 individual subfamily certificates are retained for exact replay.

## 2. Stable generic normalization and a private crossing

### Lemma 2.1: a full-nerve representation can be made stable and rationally generic

Let finitely many nondegenerate rational triangles have a specified full nerve. Write each as three inequalities with fixed rational normals. Increase every right side by the same sufficiently small positive rational epsilon. Each original point in a triangle now satisfies all three inequalities strictly; every old face consequently has a strict common interior witness. For small epsilon these are nondegenerate bounded triangles converging to the original ones. Every old empty subfamily has a positive common-distance gap by compactness, so choosing epsilon small enough preserves all nonfaces.

The resulting family has an open neighborhood in vertex-coordinate space with exactly the same full nerve. Interior witnesses persist by strict inequalities. Nonfaces persist by their positive gaps and continuity of the triangles in Hausdorff distance. Nondegeneracy also persists.

Choose rational coordinates in that neighborhood avoiding these finitely many polynomial equalities:

- a side of one triangle is parallel to a side of a different triangle;
- a vertex of one triangle lies on the supporting line of a side of a different triangle.

Each equality is a nonzero polynomial in freely varying vertex coordinates. A finite union of its zero sets cannot fill a nonempty open set; rational points avoiding them are dense. The new family therefore has the same nerve, strict witnesses for all faces, and boundaries in general position. Its coordinates remain rational. The argument is an existence proof, not a claim that an arbitrary old representation was already in general position. The same open-set argument can rationalize a real representation if needed.

### Lemma 2.2: the two root triangles cannot contain one another

Suppose {u,v} is a maximal pair-edge and deg(u)>=2. If T_u were contained in T_v, choose another edge e incident with u. Its size is at least two, so choose w in e other than u. Linearity with {u,v} forces w!=v and v not in e. A common point of edge e belongs to T_u,T_w and also T_v. The full nerve would put the triple {u,v,w} in a hyperedge, contradicting maximality of {u,v}. Thus T_u is not contained in T_v. The symmetric conclusion uses deg(v)>=2.

The proof uses the common-point nerve. A condition only on the pairwise intersection graph would be insufficient.

### Lemma 2.3: a private rational transverse crossing exists after normalization

The normalized roots have overlapping interiors because their pair-edge has a strict witness. Neither triangle contains the other by Lemma 2.2. Two compact convex polygons with interior overlap and neither containing the other have intersecting boundaries. For completeness, if their boundaries were disjoint, the connected boundary of the first would lie wholly inside or wholly outside the second. The inside case places the whole first polygon in the second by convexity. In the outside case a segment from an interior common point to a point of the second outside the first must cross the first boundary while still inside the second, a contradiction.

By general position every boundary intersection lies in the relative interiors of two nonparallel sides. It is a transverse crossing. Since the side lines are rational, the crossing p is rational. No other old triangle contains p: otherwise the roots and that triangle would have a common point, contradicting the pair-edge. The finitely many other old triangles are compact and avoid p, so p has an open neighborhood U meeting none of them. Shrink U to avoid the four nonactive root sides and both root vertices on the active sides. Throughout U, each root triangle agrees with its single active inward half-plane.

If the two root side inequalities are l_u(x)<=0 and l_v(x)<=0, the affine chart x -> (l_u(x),l_v(x)) is rational and invertible. It sends p to zero and the two local insides to x<=0 and y<=0, respectively. No assumption about the angle or chosen orientation of the original crossing is necessary.

## 3. Two-parent insertion preserves every old and new face

More generally let G have a model with roots r,s given by x<=0,y<=0, and all its other vertices represented by bounded rational nondegenerate triangles. Assume the full nerve is the downward closure of a covered loopless linear hypergraph whose edge {r,s} is maximal.

Let H have a rational triangle representation with a private transverse crossing at a maximal pair-edge {u,v}. Identify r with u, s with v and the two pair-edges with one edge. All other G vertices are fresh; retain every whole edge.

**Two-root insertion lemma.** This amalgam has a rational nondegenerate triangle representation leaving every old triangle unchanged.

**Proof.** Use the affine chart and private neighborhood U of Lemma 2.3. The union of all bounded nonroot model triangles is bounded. A sufficiently small positive rational dilation places that entire union inside the chart image of U. Map the triangles back through the inverse rational chart. Their shapes are still nondegenerate rational triangles.

Every old-only subfamily has its original intersection behavior, since no old triangle is changed. Every subfamily consisting of new triangles and any subset of {u,v} has exactly the model behavior: all new triangles lie in U, where the old roots agree with the two model half-planes. This also includes subfamilies with new triangles and both roots; they are empty because the model pair is a maximal edge. A subfamily containing a new triangle and any old vertex outside {u,v} is empty already on that pair, by privacy of U. These cases exhaust all nonempty subfamilies, proving the full-nerve assertion.

The amalgam remains linear. An old edge other than {u,v} contains at most one of u,v; a new edge other than the shared pair also contains at most one. Since all other new vertices are fresh, an old and new nonshared edge meet in at most one vertex. The shared edge meets every other edge in at most one vertex. Internal linearity is unchanged. Every edge is still whole and has size at least two, every vertex is covered, and no distinct edge can contain another. Thus the displayed edge family is exactly the maximal nerve family, with the common pair counted once. QED.

Combining the lemma with Section 2 and the F model gives the announced theorem for every eligible pair-edge of any starting representation. If the initial roots already have a transverse private side crossing, they and all other old triangles can be preserved from the outset. Otherwise only the normalized old family, not the arbitrarily supplied original coordinates, is fixed by the insertion.

Every fresh F vertex has degree at least two. Every new pair-edge b,c,d consequently has eligible endpoints, as does the retained root pair. Repeating normalization and insertion finitely many times proves representability for all finite sequences. It does not promise that a triangle remains geometrically fixed through later normalizations at other pairs. If each later attachment uses an already available transverse crossing, all existing triangles at each such step are preserved exactly.

At the particular source-model crossing zero, every inserted nonroot triangle avoids zero. Hence the same crossing remains private after each insertion. It can be reused at a smaller scale without moving the roots or any earlier triangle. The explicit family below realizes this repeated same-pair situation simultaneously.

## 4. An explicit unbounded family without an incidence cutvertex

Let A_k have roots 1,2, common edge a=12, and, for each 0<=i<k, fresh vertices 3_i,4_i,5_i and edges

    b_i={2,3_i}, c_i={3_i,4_i}, d_i={1,4_i},
    e_i={1,3_i,5_i}, f_i={2,4_i,5_i}.

Use the two root triangles

    T1=conv{(0,-10),(0,10),(-10,0)},
    T2=conv{(-10,0),(10,0),(0,-10)}.

For block i use 8^(-i) times each of D3,D4,D5 from Section 1. All its nonroot points satisfy

    (497/500)8^(-i) <= x+y <= (3001/750)8^(-i).

These are disjoint closed bands for different i, since (3001/750)/8 < 497/500. Thus triangles in different blocks are disjoint. At scale one all coordinates lie between -2 and 5; scaling toward zero preserves those bounds. Whenever such a point has x<=0, it satisfies |y|<=5<10+x, so T1 agrees with x<=0 on the entire union of the model triangles. Exchanging x,y gives the same conclusion for T2 and y<=0. The roots intersect, for example at (-1,-1). Therefore the full nerve is exactly A_k for every k>=1. This is a direct rational formula, not an extrapolation from finite tests.

The family has 3k+2 vertices, 5k+1 maximal edges and 12k+2 incidences. Each root has degree 2k+1. Every nonroot vertex has degree two or three; every edge-node has degree two or three. Hence the whole incidence graph is its 2-core.

The incidence graph of one F is exactly the subdivision of K3,3 with branch parts {1,3,f} and {2,4,e} and nine paths

    1-a-2, 1-d-4, 1-e;
    3-b-2, 3-c-4, 3-e;
    f-2, f-4, f-5-e.

The path interiors are pairwise disjoint. Subdividing edges of K3,3 preserves connectedness after deletion of any one vertex: deleting an original vertex leaves the remaining graph connected, and deleting an interior subdivision vertex leaves the alternative routes through the other edges. Thus each copy has no cutvertex. In the union, all copies share the three-node path 1-a-2. Deleting any one node still leaves at least two shared nodes, and each surviving copy is connected. The union remains connected. A_k therefore has no incidence cutvertex and is nonplanar for every k>=1.

This family has unbounded root degrees inside a genuinely two-connected cyclic incidence graph. It cannot be obtained solely as a nontrivial vertex wedge of these blocks. The incidence-order dimension is established separately in Section 5, rather than inferred from the gluing theorem.

## 5. Incidence dimension exactly three for every size

For every k>=1 define these three permutations of the vertex set:

    V1 = 1,2, then (3_i,5_i,4_i) for i=0,1,...,k-1;
    V2 = 1, then (4_i,3_i,5_i) for i=k-1,...,1,0, then 2;
    V3 = 2, then (4_i,5_i,3_i) for i=k-1,...,1,0, then 1.

Expand each permutation by inserting each edge immediately after its last vertex, before the next vertex. Among edges completed at the same vertex use any fixed order. The three expanded total orders realize the incidence poset.

### A complete sufficiency lemma

For a covered clutter, vertex permutations suffice if every two vertices occur in both orders and, for every missing incidence (v,h), some permutation places all members of h before v. Their expansions are linear extensions because each edge follows all its members. The permutations already reverse every vertex pair. For a missing incidence the specified permutation puts h before v; another permutation puts v before any chosen member w of h and therefore before h. Thus v and h are incomparable in the intersection. For two different edges h,g, choose u in h minus g and w in g minus h, available because the family is a clutter. The missing-incidence witnesses put g before u before h in one expansion and h before w before g in another. Hence edge pairs are also incomparable. These cases exhaust all distinct incidence elements and prove sufficiency, including every edge/edge comparison.

### Verification of the hypotheses for A_k

The two roots occur in opposite orders in V1 and V3. Root 1 precedes all nonroot vertices in V1,V2 and follows them in V3. Root 2 precedes them in V1,V3 and follows them in V2. Within one block the restrictions to 3_i,4_i,5_i are (3,5,4), (4,3,5), (4,5,3), which reverse every pair. Across two blocks, V1 uses increasing index and V2 uses decreasing index. All vertex pairs are therefore reversed.

For missing incidences within one block or involving its roots, the following complete list names a witnessing permutation:

- a before each of 3_i,4_i,5_i: V1;
- b_i before 1: V3; b_i before 4_i or 5_i: V1;
- c_i before 1: V3; before 2 or 5_i: V2;
- d_i before 2,3_i or 5_i: V2;
- e_i before 2: V2; before 4_i: V1;
- f_i before 1 or 3_i: V3.

Each statement follows by putting all displayed edge members before the excluded vertex. For a nonroot vertex in a different block j, if i<j, V1 puts every member of any edge from block i before that vertex, since both roots are first. If i>j, use V2 for d_i,e_i, use V3 for b_i,f_i, and use either V2 or V3 for c_i. In the chosen order any root belonging to that edge is first and block i precedes block j. The shared edge a was already handled. This exhausts every missing incidence.

The sufficiency lemma proves dimension at most three for every k. For the lower bound, restrict to vertices 1,2,3_0 and edges b_0,e_0,a. Each vertex is incident with exactly the other two edge labels in this list, giving the standard example S3. Each diagonal missing incidence must be reversed in some linear extension. Two diagonal reversals in the same extension, together with the two cross-incidences, would form an alternating directed cycle. Three distinct reversing orders are required. Thus the incidence dimension is exactly three for all k>=1.

In particular A_2 has eight vertices and eleven hyperedges, both roots of degree five, and a nonplanar incidence graph with no cutvertex. The unbounded family has both root degrees 2k+1 wholly inside its two-connected incidence 2-core. These are genuine members of the intended dimension-three class, certified independently from their geometry.

### Mixed block-and-ear family

The same result admits an explicit additional parameter without any new geometric assumption. For integers k,t>=0 with k+t>=1, define A_{k,t} by taking k copies of F sharing roots 1,2 and edge a=12, and t fresh vertices z_j with edges g_j={1,z_j}, h_j={2,z_j}. The case t=0 is A_k.

For the first k scale bands use the three nonroot triangles of each F copy as before. In band k+j use only 8^(-(k+j))D5 for z_j. This triangle meets root 1 with strict witness 8^(-(k+j))P, meets root 2 at the corresponding Q witness, and misses their common intersection. Those claims follow directly from the certified two-root model after forgetting D3,D4. Different bands are disjoint, and the same finite root triangles agree with the half-planes on every band. Thus the entire nerve has exactly the specified mixed edges for every k,t. This also supplies a two-root ear model to which the insertion lemma applies under its existing crossing hypotheses.

The mixed family has 3k+t+2 vertices, 5k+2t+1 edges and 12k+4t+2 incidences. Both roots have degree 2k+t+1. An ear together with the shared pair-edge is a six-cycle in the incidence graph, hence has no cutvertex. Each F component has the already proved property. The union of these components along the common three-node path therefore has no cutvertex by the same deletion argument. Every incidence node has degree at least two, and the graph is nonplanar whenever k>=1. The roots remain a two-vertex separator when there is more than one component; no higher connectivity is claimed.

For the three vertex orders, regard the F copies as the first k pieces and the ears as the next t pieces. In V1 use the F words (3_i,5_i,4_i) in increasing order, then z_0,...,z_(t-1). In V2 and V3 put the ears in decreasing order before the decreasing F words; keep their respective leading and trailing roots as above. Within an ear the three restrictions are (1,2,z), (1,z,2), (2,z,1). They reverse all vertex pairs and all its missing incidences: a before z in the first, g before 2 in the second, h before 1 in the third.

All cross-piece vertex pairs reverse between increasing and decreasing concatenations. For any edge of an earlier piece and a vertex of a later piece, V1 is a missing-incidence witness because both roots are first. In the reverse piece-index direction, V2 is a witness for edges containing root 1, V3 for edges containing root 2, and either for edges containing neither. The shared edge a is handled separately by V1. These cases also include every F/ear and ear/ear comparison. The sufficiency lemma proves dimension at most three. If k>=1 use the F copy's induced S3; if k=0 use vertices 1,2,z_0 and edges h_0,g_0,a. The same alternating-cycle argument proves dimension at least three. Consequently A_{k,t} has incidence dimension exactly three for all k,t>=0 with k+t>=1.

## 6. Verification and final boundary

The private exact verifier uses rational Fourier-Motzkin elimination in two variables and retains all elimination multipliers. Feasible subfamilies have rational witnesses checked against every original inequality. Infeasible subfamilies have nonnegative rational multipliers with zero weighted normal and strictly negative weighted right side. A separate certificate replay verifies these identities without running elimination.

Every nonempty subfamily is accounted for in the two-half-plane model and in A_1,A_2,A_3: respectively 31,31,255,2047 subfamilies, with 17,17,31,45 faces. A separate recursive regression first inserts F across the pair-edge {3_0,4_0} of A_1, then inserts another F across a pair-edge of that newly inserted block. It finds actual rational private transverse crossings and checks strict separation from every other old triangle and strict inclusion in the four nonactive root half-planes. The scales are 1/8 and 1/4096. Every old triangle remains byte-for-byte identical in the coordinate lists at each step. All 255 and 2047 nonempty subfamilies of these two further families are checked, giving 4666 full subfamily certificates before the mixed regressions. The mixed cases (k,t)=(0,1),(1,1),(2,2) add all 7,63,1023 nonempty subfamilies, respectively, for a final total of 5759. No incidence-dimension claim is inferred for these additional recursive regressions. All maximal faces are compared with the whole declared edges. Small subfamilies are solved directly; larger faces use checked edge witnesses and larger nonfaces carry an explicit contained infeasible subfamily and its Farkas certificate. No pairwise-only shortcut is used. Strict witnesses, linearity, coverage and looplessness are separately gated. Connectivity after deleting each incidence node is checked for k=1,2,3,4,10,30; the preceding argument proves all k.

A separate suffix-bitset checker intersects the complete raw incidence orders. It independently accepts the searched A_2 realizer on all 342 ordered pairs, and the uniform construction for k=1,2,3,4,10,30,100. At k=100 this checks all 644006 ordered pairs of 803 incidence elements, with exactly 1202 strict incidences. Mixed orders are also independently checked for (k,t)=(0,1),(1,1),(2,3),(10,10). The universal dimension theorem rests on the preceding complete pair proof, not these finite values.

Every gate is an explicit VerificationError, active under normal Python, -O and -OO. Closed point and line intersections, parallel inconsistency, zero-normal inconsistency and the empty constraint system are controlled. Genuine source mutations, deterministic outputs and full-byte archive/store restoration are documented separately. Private scripts and raw recovery material are not part of the public mathematical report.

The new operation joins a cyclic nonplanar block to two existing vertices simultaneously while respecting every old hyperedge and the entire nerve. It requires a maximal size-two edge and a suitable two-root model. It neither joins arbitrary nonadjacent old vertices, nor handles general larger separators, nor proves arbitrary high-degree triangle representations. The family A_k is proved separately to have dimension exactly three; no dimension-preservation assertion is made for arbitrary pair gluing. The general conjecture remains unresolved by this final pass.
