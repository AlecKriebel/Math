# Independent final review: two-parent triangle gluing and dimension-three amalgams

## Verdict and frozen scope

**Accept the two-root rational model, the normalized two-parent insertion theorem, the sufficient compatible-root realizer theorem, and the complete explicit family A_{k,t}.** For every k,t>=0 with k+t>=1, that family has a rational nondegenerate filled-triangle representation and incidence dimension exactly three. Its incidence graph is 2-connected, equals its entire 2-core, and is nonplanar when k>=1. The root degrees 2k+t+1 are unbounded inside that cyclic core.

This is a partial structural result, not a proof of the general triangle-representation conjecture. The generic geometric insertion theorem does not assert dimension preservation. The compatible-root dimension theorem requires its displayed three local order forms; those forms have not been proved for arbitrary dimension-three hypergraphs. No sixth mathematical pass or literature-priority claim is part of this acceptance.

The two completed mathematical reports read in full and accepted here have these identities:

* Geometry and gluing report: 26,874 bytes; SHA-256 `fb21fcf28c33fa396067ca455a45a6e8ba77eedb623f1bddd261e6fb7c6f79e4`.
* Dimension and compatible-amalgam report: 13,476 bytes; SHA-256 `23f93b91c1292453a4a26219b0be6602f5e084dd47f522458b2caaabf93450ba`.
* Complete geometry certificates are retained separately. [The complete authored geometry examples](EXACT_GEOMETRY_EXAMPLES.json) are distributed with this prose edition.
* Complete dimension fixtures: 70,770 bytes; SHA-256 `93ca25418eb316ceeebb23793e90dc8a95187a493f61e85b228dd16b53b85619`.

The final acceptance record additionally binds the completed verification payloads and independent recovery records. It does not silently extend to later edits.

The conventions throughout are finite covered loopless linear hypergraphs, with their listed edges being maximal faces. A triangle is a nondegenerate closed filled triangle. Correctness means the entire common-point nerve is the downward closure of the listed edges. It is not enough to realize the pairwise intersection graph. No disjoint-interior, boundary-only, or contact convention is imposed.

## 1. Exact two-root geometry

The source block F has vertices 1,2,3,4,5 and edges 12,23,34,14,135,245. Its published example and previously known incidence dimension are credited to de Fraysseix, Ossona de Mendez and Rosenstiehl, *Representation of Planar Hypergraphs by Contacts of Triangles*, printed p. 135. The accepted earlier review documents that source inspection. This audit independently checks the new constructions and uses no unproved convex-to-triangle deduction. [Published chapter](https://doi.org/10.1007/978-3-540-77537-9_15). The earlier coordinate base remains credited to Ossona de Mendez, *Realization of Posets*; it is not needed to prove the new local insertion lemma. [Publisher article](https://jgaa.info/index.php/jgaa/article/view/paper48).

With roots H1={x<=0}, H2={y<=0}, put P=(-1,2), Q=(2,-1), R=(2,2), S=(-1,4), T=(4,-1). The initial nonroot objects are conv(P,R,T), conv(Q,R,S), and [P,Q]. Their displayed supporting inequalities are exact. On x+y=1 the first triangle requires x<=-1, the second x>=2, so their intersections with the segment are exactly P and Q. The intersection of the two triangles lies strictly in the positive quadrant: x<=0 together with y<=2 contradicts 5x+3y>=7, and the symmetric argument excludes y<=0.

This proves all eight forbidden triples: 123,124,125 avoid the root intersection; 134 and 234 are excluded by the positive-quadrant observation; 145 and 235 would require respectively Q in H1 and P in H2; and 345 would require P=Q. The other two triples have witnesses P,Q. All ten pairs occur, with the pair-only maximal edges witnessed at (-1,-1), T,R,S. Every larger subfamily contains a forbidden triple. Thus the argument really proves the complete nerve.

The rational thickening at eta=1/1000 is valid. Centroid dilation makes every point of each original triangle interior, and the displayed three-point replacement makes the whole original segment interior. All required edge witnesses become strict. For a nonface involving unbounded root half-planes, at least one other object is bounded. The maximum of the distances to its finitely many closed sets is therefore coercive and has a positive minimum when the intersection is empty. This supplies the needed stability gap; an inapplicable compactness assertion about the half-planes is not being used.

The independent checker reconstructs the three thickened triangles directly from the report's rational coordinates. It confirms all 31 subfamilies, all six strict witnesses, all eight exact dual identities, and the reported normalized infeasibility margins. In particular the smallest margin is 497497/3502500, and the minimum strict witness slack in the author's fixed unnormalized inequalities is 9/500000. These are exact fractions, not numerical tolerances.

## 2. Normalization, the degree hypothesis, and privacy

The normalization proof is sound, including an initially real representation. Increase the supporting right sides slightly while keeping their normals fixed. Each old face acquires an interior witness; sufficiently small changes preserve every nonface by the positive gaps for this finite compact family. Boundedness and nondegeneracy persist. This gives an open set in the space of triangle vertices with constant full nerve. Rational coordinates can then be chosen in that open set while avoiding the finitely many side-parallelism and vertex-on-side polynomial equalities. If the original coordinates are real, the preliminary offsets can be real; rationality is obtained at the final open-set perturbation. No assertion that the original coordinates were already rational or generic is needed.

Suppose {u,v} is a maximal pair-edge and both root degrees are at least two. If T_u were contained in T_v, another edge incident with u would supply some w!=v and a witness in T_u and T_w. That witness would also lie in T_v, giving the forbidden triple {u,v,w}. Linearity guarantees that the other edge does not already contain v. Applying the symmetric argument excludes both containments. This step is genuinely a full-nerve argument.

After normalization the roots overlap in their interiors, neither contains the other, and their boundaries must meet. General position puts each meeting in two side interiors with nonparallel supporting lines. Rationality of those lines gives a rational crossing p. Maximality of {u,v} excludes every other old triangle from p. Since the other triangles are a finite compact family, a sufficiently small neighborhood of p misses all of them. Shrinking also removes the nonactive root sides, so each root is exactly one inward half-plane there. The chart formed by the two supporting affine functions is rational and invertible.

This proves a private transverse crossing after normalization. It does not promise one in arbitrary original bytes. For example, a legitimate pair intersection can initially be a boundary-only contact. The accepted fixed-old-triangle assertion begins after the nerve-preserving normalization. If an already rational input has a suitable crossing, insertion needs no normalization. Subsequent normalizations at different attachment pairs may change earlier coordinates; the report states this limitation explicitly.

## 3. Complete-nerve insertion and finite iteration

In the private chart, scale all bounded nonroot objects of a two-half-plane model into the chart neighborhood and map them back. This produces rational nondegenerate triangles. There are exactly three relevant subfamily types:

1. Old-only subfamilies keep their behavior because the old triangles are unchanged.
2. New triangles together with any subset of the two roots have precisely the model's intersections, since the roots agree with its half-planes throughout every new triangle.
3. A subfamily containing a new triangle and an old nonroot is empty already on that pair by privacy.

These cases cover higher intersections as well as pairs. In particular a new triangle cannot meet the intersection of the two roots, because their pair-edge is maximal in the model. The shared pair is counted once; every other old and new whole edge is retained. Distinct edges from different pieces share at most one root, preserving linearity and the maximal-edge inventory.

Every new pair-edge of an inserted F copy has endpoints of degree at least two, so the same normalization-and-insertion theorem can be applied finitely many times, including at new pair-edges. At one already private crossing, successively smaller insertions can instead retain all previously inserted coordinates. Neither argument claims a dimension-three closure theorem for arbitrary insertion sequences.

The exact recursive examples were independently checked more strongly than by comparing their final nerves. The first inserts across {3_0,4_0} at scale 1/8; the second inserts across the new pair {x3,x4} at scale 1/4096. The audit reconstructs each affine map from the old supporting rows, verifies a private side-interior crossing, verifies the new triangles are precisely the transformed model, and compares every earlier triangle's complete coordinate/inequality data unchanged. The two complete nerves have 255 and 2,047 nonempty subfamilies.

## 4. Uniform geometry for all block-and-ear counts

For A_k use the fixed root triangles conv((0,-10),(0,10),(-10,0)) and conv((-10,0),(10,0),(0,-10)), and use scale 8^(-i) for block i. Each block lies in the closed band

    (497/500)8^(-i) <= x+y <= (3001/750)8^(-i).

The inequality (3001/750)/8 < 497/500 strictly separates every two distinct bands. This eliminates all cross-block intersections at every k, rather than relying on a finite tested range. All scaled coordinates remain between -2 and 5. On the union of these model objects, x<=0 implies |y|<=5<10+x, proving exact agreement with the first finite root triangle; the symmetric estimate handles the second. Thus the half-plane nerve survives root truncation at all scales.

An ear is represented by D5 alone in its own band. It meets each root separately and misses their common intersection. Taking k block bands followed by t ear bands proves the complete nerve of A_{k,t} for every k,t>=0 with k+t>=1, including the ear-only cases. The construction supplies all nondegenerate rational triangles directly.

The inventories are |V|=3k+t+2, |E|=5k+2t+1 and 12k+4t+2 strict incidences. Each root has degree 2k+t+1. The F vertices 3_i,4_i have degree three and 5_i degree two; ear vertices have degree two. A sentence-level error in the dimension draft calling all F nonroots degree three was corrected before this acceptance. The underlying incidence data and minimum-degree conclusion were already correct.

The displayed nine internally disjoint paths in each F incidence graph form a subdivision of K3,3 and use its entire graph. Each ear piece is a six-cycle. Each piece is 2-connected and all pieces share 1-a-2. Deleting any one node leaves every affected piece connected and at least two common nodes, hence leaves the union connected. Every incidence node has degree at least two, so the graph is its entire 2-core. If k>=1 it contains the unchanged K3,3 subdivision and is nonplanar.

These are exactly 2-connectivity claims. They exclude a nontrivial construction solely by single-node or single-vertex wedges of these pieces. They do not rule out larger separators: the common roots provide a two-vertex separator. No stronger indivisibility or higher connectivity is accepted.

## 5. Complete realizer proof, not finite extrapolation

For a covered clutter, vertex permutations suffice when (V) every vertex pair occurs in both orientations and (M) for every excluded vertex v and edge h, some permutation puts every member of h before v. Insert each edge immediately after its final member, with any fixed tie order. All incident pairs are then correct. Condition (V) reverses vertex pairs. For a missing incidence, (M) gives h<v, while (V), applied to v and any member w of h, gives v<w<h elsewhere. For edges h!=g, choose u in h\g and w in g\h; the two missing-incidence witnesses give g<u<h and h<w<g. Thus all four vertex/edge pair types are accounted for and tie choices cannot spoil the witnesses. The converse follows by restricting a full incidence realizer to its vertices.

The local F orders are 1 2 3 5 4; 1 4 3 5 2; and 2 4 5 3 1. The report lists all sixteen missing incidences and each designated order is correct. Every vertex pair also reverses. An ear has the analogous three orders 1 2 z; 1 z 2; and 2 z 1.

More generally, the compatible-piece theorem assumes local orders r s A_i, r B_i s, and s C_i r. Put A_i in increasing piece order and B_i,C_i in decreasing piece order, with the same leading/trailing roots. Within a piece the local witnesses remain. Cross-piece vertex pairs reverse. For a cross-piece edge/vertex missing incidence, the increasing order works in one direction; in the other direction use the second order for an edge containing r, the third for an edge containing s, and either for an edge containing neither. Linearity excludes an unshared edge containing both roots. The common pair precedes every nonroot in the first order. This exhausts all missing incidences and proves the uniform three-order construction.

The lower bound is also uniform. For k>=1, vertices 1,2,3_0 and edges b_0,e_0,a induce S3. For k=0 use the first ear's vertices and its three pair-edges. Each of the three diagonal incomparable pairs must be reversed, and two such reversals in one linear extension would form a cycle with the two cross-incidences. Three orders are necessary. Combined with the explicit upper bound, this proves dimension exactly three, including all ear-only cases. The excluded k=t=0 case has dimension two.

## 6. Independent exact checks and hostile controls

No author module or numerical solver is imported by the independent checker. It builds the exact supporting lines from the displayed rational vertices and enumerates their rational pair intersections, together with the origin for root-only subfamilies. Any nonempty intersection involving a triangle is a bounded polytope with an extreme point at two nonparallel supporting lines. Consequently these candidate points suffice to compute the entire closed-set nerve, including point and segment intersections. This is independent of the authors' Fourier–Motzkin implementation.

The checker directly verifies 4,512 subfamilies across eight separately constructed half-plane, pure-block, ear-only and mixed families. It independently recomputes all nine authored geometry fixtures, totaling 5,759 complete subfamilies, and separately replays every retained primal/dual or contained-nonface certificate. The independently recomputed counts agree exactly. All raw triangle points agree with their supporting inequalities.

For dimension, a direct integer-rank checker compares every ordered pair of distinct incidence elements, independently of the author's suffix-bitset method. It checks 2,122 ordered pairs in the six raw full-order fixtures, another 2,922 in all five retained discovery outputs, and 1,087,762 in fourteen additional uniform examples through k=100 and t=100. When a discovery output stores only vertex orders, those are independently expanded and then fully checked. These finite checks corroborate the universal proof; they are not its basis.

The independent harness reruns the complete positive audit under normal Python, -O and -OO and checks deterministic output under multiple hash seeds. Twenty-four hostile data/control runs reject colliding geometric bands, inadequate root truncation, a reversed root half-plane, a degenerate model, removal of the third order, removal of an incidence element, loss of the reverse piece direction, and an inverted incidence. Each must reach its specified mathematical diagnostic. Nine actual source-mutation runs separately disable all validation guards, the complete-nerve comparison, or the raw-order comparison. An independent harness detects the resulting false acceptance; it does not trust a validation helper imported from the mutated verifier.

Final source identities, author harness replays, and complete archive/content-addressed recovery comparisons are recorded in the acceptance record. Restorations cover whole files and rerun the independent audit from each restored tree; header-only recovery or merely rehashing the original files is not the recovery test.

## 7. Remaining frontier

The accepted geometric operation attaches a suitable two-root model along a maximal size-two edge after a stable rational normalization when necessary. It does not glue arbitrary nonadjacent old vertices, arbitrary shared triangles, or arbitrary larger separators. An arbitrary insertion sequence has not been shown to preserve dimension at most three. Conversely, every dimension-three hypergraph has not been shown to admit the compatible-root orders or to decompose into these pieces. High degrees in a 2-connected core are now covered by the explicit family, but the general conjecture remains unresolved.
