# Independent full-claim adversarial derivations

The mechanisms below were reconstructed from the actual manuscript and sealed before supplied code/results, foreign bodies or opinions. They validate the original explicit example and its definition boundaries; no repaired or narrower replacement theorem is proposed.

## Exact face geometry

Let D have the five affinely independent vertices v0=0,v1=e1,…,v4=e4. A nonzero linear functional has distinct maximal and minimal values on this vertex set. Let A,B be the corresponding nonempty, disjoint index sets. It exposes

F(A,B)=conv(v_i:i∈A)+conv(−v_j:j∈B)

in D−D. Every disjoint ordered nonempty pair is exposed: prescribe affine values1,−1,0 on A,B and the remainder and subtract the value at v0. Affine independence allows these prescribed values. Every proper nonempty polytope face has a nonzero supporting functional; the full face is the only additional nonempty face.

If a vector lies in both summand direction spaces, express it by coefficients of sum0 on A and on B. Subtracting gives an affine dependence supported on disjoint sets. All coefficients vanish. The directions therefore intersect trivially and

dim F(A,B)=|A|+|B|−2,
dim D^u=|A|−1,
dim(−D)^u=|B|−1.

If F(A,B) is contained in F(C,L), evaluate v_i−v_j against a functional with extrema C,L. Its value equals the maximum difference only if i∈C and j∈L separately. Hence containment is equivalent to A⊆C,B⊆L. This proves the claimed order and distinctness of ordered labels, without quotienting central reflection or swapping labeled summands.

The qualifying base faces consequently have types(2,2),(2,3),(3,2), with30,10,10 faces. Every(2,2) face has precisely two upper neighbors, by assigning its unused label to either side; every maximum has three lower neighbors. Thus the entire base order complex has50 vertices,60 edges, no longer chains and no isolated vertices. It is pure one-dimensional.

## Independent connectivity mechanism

Suppress degree-two minimal vertices. The resulting graph has signed two-subsets, plus A and minus B adjacent iff A∩B=∅. It is the bipartite double cover of the disjointness graph on the ten two-subsets of a five-set.

The unsigned graph is connected. Disjoint two-subsets are adjacent; distinct intersecting ones have the two-element complement of their union as a common neighbor. It also has the explicit odd cycle

01 — 23 — 04 — 12 — 34 — 01.

Lifting that cycle changes sign and returns to the same unsigned vertex. Lifting connected unsigned paths and using this sign-changing loop connects every signed vertex to both signs. This checks the subtle point that a connected graph's double cover need not be connected unless an odd cycle is available. The signed graph has20 vertices and30 edges; subdivision recovers connected K with50 vertices and60 edges.

## Shared interval and exhaustive endpoint separation

The sum of the two five-dimensional lattice prisms is (D−D)×[0,2]. For a common exposing functional(u,t), there are four exhaustive cases.

1. u≠0,t>0 or t<0: both summands select the same upper or lower interval endpoint. The summand/sum dimensions equal the base dimensions, so precisely the base qualifiers occur at height2 or height0.
2. u≠0,t=0: both summands carry the interval direction. If the base dimensions are a,b,c, the new dimensions are a+1,b+1,c+1 with c≤a+b. Exact additivity is impossible because c+1<a+b+2.
3. u=0,t≠0: the horizontal full end face has dimensions(4,4,4), in summand-first notation, so4≠4+4.
4. u=0,t=0: the whole sum has dimensions(5,5,5), so5≠5+5. Empty faces fail strict positivity.

A lower endpoint in one summand and upper endpoint in the other cannot form a new canonical face at height1: their vertical exposing signs would conflict. Nor can alternate face decompositions rescue a vertical face. If G1+G2=P1^u+P2^u with Gi⊂Pi nonempty, every pair of points has maximal total u-value. Separate upper bounds force Gi⊆Pi^u. For any other functional w the nonnegative support deficits h(Pi^u,w)−h(Gi,w) sum to0, so both vanish. Support functions determine compact convex sets, proving Gi=Pi^u. This agrees with the actual classical uniqueness lemma inspected later.

The surviving faces are exactly two disjoint copies of the base poset. Nonempty faces at heights0 and2 cannot contain one another, so no cross-edge or higher chain is missing from the asserted K⊔K decomposition.

## Homology, shellability and boundary controls

A connected finite graph has incidence rank V−1 over Q: a spanning tree supplies V−1 independent columns, and all columns have coordinate sum0. Thus each K has rank49 and first Betti number60−49=11. Two copies give100 vertices,120 edges, rank98, H0=Q²,H1=Q²² and no homology in degrees≥2. The conclusion follows from ranks and connectedness, not Euler characteristic alone. Reduced H0 has rank1 instead; neither convention makes the realization connected.

Any ordering of the edge facets has a first edge from the component not used by the first facet. Its intersection with previous facets has only the empty face and dimension−1. An added edge requires pure dimension0 intersection in both ordinary pure shellability and the actual standard nonpure definition. Therefore no ordering is a shelling. This argument is universal over all facet orders; no failed greedy search is used as the proof.

A wedge of3-spheres, including the zero-fold point, is connected with H1=0, so both H0 and H1 refute the printed R5 question. Even replacing n−2 by n−3 would give2-spheres and would not remove these obstructions. No minimal-dimension or first-ever claim is inferred.

Opposite tetrahedra have four labels, so the only qualifying type is(2,2), giving six incomparable faces. Their order complex is six points, which is shellable in dimension0 because the required attaching intersection then has dimension−1. It still fails the printed wedge-of-circles homology assertion. This is a lower-dimensional classical control, not a replacement nonshellability witness.

Adding an artificial top changes the object to a cone. The own exact control constructs its full signed chain matrices, with f-vector(101,220,120), boundary ranks(100,120) and ordinary Betti numbers(1,0,0). It demonstrates why a convention silently adjoining an extremum would destroy the claimed homology. The ordinary order complex convention in the actual shellability source agrees with the manuscript.

## Different meanings of mixed faces

For the broader stable-intersection lower-bound convention, two summands need each dimension≥1 and combined dimension≥2. A proper vertical face based on |A|=|B|=2 has dimensions(2,2,3). It satisfies these lower bounds, but3≠2+2. There are30 such coordinate witnesses. Thus the target poset omits faces present in that other boundary-face convention, and its nonshellability cannot be exported to that different complex.

Facet-based “totally mixed” terminology is different again: the inspected public colorful-Gale manuscript requires each summand face to be a facet. The target explicitly does not invoke its counting theorem. The later Hiatt–Simpson–Wang–Wu v2 construction is a3-dimensional Schön subvariety of(C*)8 whose tropical link has its own nontrivial first homology; the inspected Section8 supplies no identification with this two-summand exact-additivity poset. No equivalence or priority displacement is assumed from a shared topological obstruction.

## Exact finite evidence and its limits

The own preforeign program exposes the actual integer prism vertices with every ternary affine-height pattern and each interval sign, deduplicates by whole coordinate point sets, computes all affine ranks over Q and derives inclusion geometrically. Completeness of this exposure sweep follows from the max/min realization proof above. It finds543 nonempty sum faces,93 nonempty faces in each summand and100 exact qualifiers. Direct signed rational incidence gives rank98 and Betti numbers(2,22). Separate disjointness-cover, six-point, vertical-definition and artificial-top controls pass. All446 explicit predicates and the complete100 coordinate face records/120 order edges were frozen before native exposure.

Both deposited scientific programs were then inspected in full and selected for bounded reproduction, once each in normal and optimized modes. The geometry program uses supporting-facet determinants and intersection closure, a route different from the own exposure construction; it also checks all8649 nonempty summand-face pairs and rejects noncanonical decompositions. The topology program enumerates chains and signed rational boundaries and includes actual shellability positive/adverse controls. Entire expected subobjects and exact native stdout encodings agree in both modes. No builder, wrapper, audit campaign or numerical tolerance is used.

The actual printed question, actual face-uniqueness lemma and actual shellability/order-complex definitions were authenticated after the independent seals. Related final2019/2024 article bodies were not obtained in this lane; comparisons with their accessible public manuscripts are identified by actual versions and dates. The mathematical counterexample does not depend on inaccessible final editions. No substantive gap was found in the whole original theorem; exact historical priority remains outside this focused adversarial verdict.
