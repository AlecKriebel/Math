# Final independent derivations

The immutable initial contains ten distinct proof/falsification families. This closes their outstanding interfaces without changing the target theorem, definition or source.

## Exact source and category

The actual EMS report, printed2464/physical70, Problem3, states the positive-summand-dimension and additive-dimension filter, asks shellability and rational homology of a wedge of(n−2)-spheres, and supplies no general-position condition. The immediately preceding Open Problems heading, printed2463/physical69, supplies no overriding genericity condition. I read the actual full problem and its fresh page pixels. Its stated motivation from tropical complete intersections does not change its explicit dimension equality.

Fukuda–Weibel exact arXivmath/0510470v4 Lemma4, printed/physical5, gives the same-functional face decomposition and its uniqueness for arbitrary polytopes, without the perfectly-centered assumption of surrounding lemmas. It credits Fukuda2004 Proposition2.1; that original2004 body was not independently acquired/read here. The support-function proof below independently supplies the fact actually needed. Björner–Wachs printed1302/physical4 Definition2.1 supplies the nonpure shellability convention, and its§5 opening defines the order complex by strict chains of an arbitrary finite poset. No artificial extrema are part of the selected face poset.

## Complete geometry and order, proved directly

Let D=conv(v0,...,v4), v0=0,vi=ei. For any nonzero functional u, its maximal/minimal index sets A,B on D are nonempty disjoint. Conversely any such pair is exposed by assigning vertex values1,−1,0 to A,B,the remainder, then subtracting the value at v0 to define a linear functional. Therefore the180 nonempty proper faces of D−D are exactly F(A,B)=conv(v_A)−conv(v_B).

For an arbitrary Minkowski sum, its exposed face at u is the sum of the exposed summand faces, by equality of support maxima. If another pair of nonempty summand faces has exactly that sum, all of its points must lie at the exposed u-level, so each is contained in the respective canonical exposed face. For any other functional the two nonnegative support deficits sum to zero. They therefore vanish separately, and support-function uniqueness yields equality of both faces. This rules out an alternative noncanonical decomposition satisfying the filter when the canonical one fails.

The direction spaces of the two disjoint simplex faces intersect only in0: equality of two direction vectors creates an affine dependence of the five affinely independent vi with coefficient sum zero on each disjoint group. Thus

    dimF(A,B)=|A|+|B|−2,
    dimD^u=|A|−1, dim(−D)^u=|B|−1.

For inclusion, evaluate each vertex vi−vj of F(A,B) against a normal exposing F(C,L). Equality with its largest difference forces i∈C,j∈L. Hence inclusion is exactly A⊆C,B⊆L. There are no omitted coincidences, lower-dimensional exceptional normals, or extra labels.

The base filter is exactly the pairs of sizes(2,2),(2,3),(3,2). There are30 minima and20 maxima; every minimum is below two maxima and every maximum is above three minima. There are60 edges and no strict3-chain. All vertices belong to edges, so the order complex K is pure1-dimensional, with50vertices60edges.

Suppressing its degree2 minima gives a graph on the20 signed two-subsets of a five-set, opposite signs adjacent exactly when their two-subsets are disjoint. Intersecting same-sign pairs share the opposite-sign complement of their union; disjoint same-sign pairs connect through a two-subset meeting each. Every vertex has an opposite-sign neighbor. Hence this graph, and its subdivision K, is connected. INDEPENDENT_CONTROLS.json provides its actual19-edge spanning tree and11 explicit fundamental cycles. Every cycle contains its own unique non-tree edge, which proves independence of those11 cycles. A spanning tree contracts K to a bouquet of11 circles.

For P1=D×I,P2=(−D)×I, all faces of the sum are faces of(D−D)×[0,2]. Nonzero interval normal selects one of two endpoint copies. Zero interval normal puts the common interval direction in both canonical summands; their dimension sum is a+b+2 while the sum dimension is c+1≤a+b+1. Such a face never passes additivity. The two full-base end faces have dimensions(4,4,4); the whole sum has dimensions(5,5,5); these also fail. The empty face fails positivity. Every normal is covered. Exactly two endpoint copies of K remain, with no cross-comparisons.

Both summands are full-dimensional lattice5-polytopes, each a product of a4-simplex and an interval. The total nonempty sum-face count is3·181=543. Each summand has3·31=93 nonempty faces, explaining93²=8649 possible nonempty summand-face pairs; enumeration is not needed for the proof of uniqueness/exhaustion above.

## Homology and shellability

For each connected K, an oriented graph boundary has rank49 and nullity60−49=11; no higher chains exist. For K⊔K the boundary rank is98, H0(Q)=Q² and H1(Q)=Q²², with Hj=0 forj≥2. Own rational elimination independently obtains rank98 from the complete signed100×120 incidence matrix. The Euler identity100−120=2−22 is a separate consistency check. Graph homology is torsion-free, so the rational conclusion does not conceal an integral exception.

Under the actual Björner–Wachs definition, the first edge entering the second component of any proposed facet order intersects the previous complex only in the empty face. That intersection has dimension−1 instead of the required0 for an edge. This contradicts the nonpure definition directly, and the pure version as well because every facet is an edge. No enumeration of120! orders is necessary.

A wedge of3-spheres, including the zero-fold point, is connected and has no H1. Both verified groups contradict that homology target. Substituting n−3=2 would not rescue it. The auxiliary D3−D3 example is the six-point antichain, shellable in dimension0; it disproves the lower-dimensional printed homology assertion but alone does not prove nonshellability. No smallest-possible-dimension or firstness claim follows.

## Competing definitions and credit

For the vertical face with base sizes(2,2), canonical summand dimensions are2,2 and the sum dimension is3. It fails3=2+2 while satisfying the singleton/pair lower bounds in Adiprasito's actual public27July2020 manuscript, printed/physical2, Corollary1.3 context. That source's stable-intersection theorem is consequently about a broader mixed-face selection. The target explicitly restricts this comparison to that public manuscript; its uninspected2024 final journal body is not silently substituted. The face filter of the target is also different from the facets-of-each-summand convention in the actual published Adiprasito et al.§1.2. Neither theorem is contradicted by this construction. No shellability resolution for stable tropical complete intersections is asserted.

Sturmfels–Tevelev's actual Examples1.3 and4.10 already describe scaled opposite tetrahedra and the six-ray geometry. The six-point homology control is therefore not presented as novel. Fukuda–Weibel Theorem6 also gives classical simplex/dual face-count geometry; applying a regular simplex affine model explains the same standard difference-body combinatorics. The new observation being evaluated is specifically the common-interval effect on the literal additive filter and the resulting positive-dimensional disconnected order complex.

Hiatt–Simpson–Wang–Wu exactv2,§8 printed/physical22–26, constructs a3-dimensional Schön subvariety of(C*)8. Its Proposition8.7 obtains a link with H1=Z and H2=Z84. It is pertinent related topology, but the body does not identify that variety/link with this two-summand exact face poset, and I make no such identification or independence/influence inference.

## Falsifier status and exact limits

Own exact controls were frozen before any foreign/support body. They verify180 exposed coordinate faces, all32400 ordered face-inclusion comparisons, rational affine ranks, the20-vertex signed model with an explicit spanning tree/cycle basis, the full two-copy signed incidence rank98, and the six-point boundary and vertical-definition control. The native code was read afterward and never imported/executed here; it includes an import-time scientific computation, which the pure closure helper explicitly avoids.

No substantive defect was found in the full original claim. The proof and primary definitions close the initial gap table. Finite program checks are supplementary. Worldwide priority, exhaustive literature coverage, conventional human refereeing, formal verification, generic perturbations and stable-intersection shellability are not certified. Follow-up is null. No repair or narrower replacement is proposed.
