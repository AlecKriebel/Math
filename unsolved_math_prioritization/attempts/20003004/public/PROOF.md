# Finite grids, clique realization, and the digital octahedron

Problem 20003004 / AIM-TOPOLOGY-0092. Author packet, 2026-10-03.

## Scope and status

The original task asks for higher homotopy groups in digital topology, with the six-vertex digital 2-sphere required to have second group isomorphic to the integers. It does not specify a product or homotopy convention. We use the reflexive strong-product convention below, matching the workshop's successful construction.

The octahedral calculation is already published: Lupton, Musin, Scoville, Staecker, and Treviño-Marroquín, *A second homotopy group for digital images*, Journal of Algebraic Combinatorics 60 (2024), Theorem 5.5. The all-dimensional simplicial comparison used here is also prior work: Grandis, *An intrinsic homotopy theory for simplicial complexes, with applications to image analysis* (2002; preprint 2000), Theorem 6.6. The finite-domain bridge below explains its applicability. This is a source correction and an explicit reformulation of known theory, not a claim of a new discovery.

## 1. Precise finite-grid convention

A digital image is a reflexive undirected graph X, with a chosen vertex b. A map is continuous when it preserves adjacency. Put I_m={0,...,m}, with i adjacent to j iff |i-j|<=1. All products in this note have adjacency

    (x_1,...,x_n) ~ (y_1,...,y_n) iff x_i ~ y_i for every i.

For reflexive graphs this categorical product has the underlying strong-product graph. It is not the graph-theoretic Cartesian/box product. In particular the domain Q=I_{m_1} x ... x I_{m_n} has all diagonal adjacencies; its boundary consists of vertices with some coordinate 0 or m_i.

A representative is a continuous f:Q->X equal to b on the boundary. A homotopy relative to the boundary is a continuous H:Q x I_T->X equal to b on boundary(Q) x I_T. Equivalently, successive slices satisfy

    H(u,t) ~ H(v,t+1) for every adjacent u,v.

A trivial extension increases some m_i, leaves f on the old box, and gives all new vertices value b. Define D_n(X,b) to be representatives modulo homotopy after trivial extension to a common box. This is an equivalence relation: homotopies themselves extend by b, allowing a common larger box for composition. Zero side lengths give only constant representatives and may be replaced by positive side lengths.

Let Cl(X) be the flag complex: its finite simplices are the pairwise-adjacent sets of vertices of X. A strong digital grid map is exactly a simplicial map from the flag complex of the grid to Cl(X). For two such maps, one-step strong homotopy is exactly simplicial contiguity. Indeed each grid clique and its two image sets are pairwise adjacent precisely when all within-slice and all cross-slice adjacency conditions hold. Conversely every adjacent pair lies in a clique (already its own two-element clique).

## 2. Moving a basepoint collar: an elementary lemma

For 0<=j<=m define alpha_j:I_{m+1}->I_m by

    alpha_j(i)=i if i<=j, and alpha_j(i)=i-1 if i>j.

Each alpha_j is continuous and fixes the two ends as a map of pairs. For 0<=j<m and |u-v|<=1,

    |alpha_j(u)-alpha_{j+1}(v)|<=1.

For a direct verification it suffices, by monotonicity, to check v=u+1 and v=u-1. In the first case the positive difference is at most one; in the second it is again at most one after reversing the two sides. The only change between the maps is alpha_j(j+1)=j versus alpha_{j+1}(j+1)=j+1; their neighbors have values j or j+1.

Consequently the chain f composed in one coordinate with alpha_m,...,alpha_0 is a relative-boundary strong homotopy. Its first member adds a basepoint hyperplane at the upper end. Its last member adds a basepoint hyperplane at the lower end and translates the old values by one. Repetition in each coordinate proves:

**Collar lemma.** Padding a finite representative on any side, or translating its nonconstant values within a larger basepoint-padded box, does not change its extension class.

This argument is dimension-independent: the other coordinates remain unchanged, so each cross-adjacent pair remains adjacent in every coordinate. Padding a local block also works when its boundary is b: an edge crossing the block boundary has its inner endpoint on that boundary, which makes the homotopy glue continuously to the unchanged outside.

## 3. The finite-support bridge in every dimension

Let K=Cl(X). Consider maps a:Z^n->K whose values outside some finite rectangular box are b and whose image on every elementary unit cube is a simplex. The domain Z^n here has the categorical simplicial product structure: every subset of the vertices of a unit cube is a simplex. Two such maps are linked if, for every elementary unit cube C, a(C) union a'(C) is a simplex of K.

These are exactly the vertices and edges of the iterated based-loop complex Omega^n K in Grandis's construction (Sections 2.2-2.4 and 6.2). The support is uniformly finite: for an iterated loop, only finitely many outer-coordinate values are nonconstant loops; by induction their finitely many inner supports have a common finite bound. Conversely a map supported in a finite box gives an iterated loop. Loop faces are constant b, so values beyond any supporting face are b.

**Proposition.** Zero extension gives a natural bijection

    D_n(X,b) -> pi_0(Omega^n Cl(X)),  n>=1.

**Proof.** A finite f extends to a by setting it to b off Q. To check a cube crossing Q's boundary, all its vertices in Q lie on one of Q's boundary faces; thus every image on that cube is b. The extension is therefore simplicial. The same argument extends relative-boundary strong homotopies. Trivial extensions have identical zero extensions, proving well-definedness.

For surjectivity, take a finitely supported a. Translate a supporting box so it lies in the nonnegative orthant, and enlarge it by a basepoint collar. The resulting restriction is a finite representative. Translation does not change the component of a: the collar homotopies from Section 2 extend by b to linked paths of finitely supported maps, also when their finite box has arbitrary integral lower endpoints.

For injectivity, a path in Omega^n K between the zero extensions of f and g is a finite sequence a_0,...,a_T of linked finitely supported maps. Their supports have a common finite rectangular bound. Enlarge it by one basepoint layer and translate it into the nonnegative orthant. Restriction of the whole sequence is then a strong homotopy relative to that box's boundary. Its endpoints are translated, padded copies of f and g. The collar lemma identifies these with the original extension classes. Therefore [f]=[g]. Naturality is immediate from postcomposition. QED.

This proof uses paths in the loop complex, namely finite chains of links. It does not confuse these with arbitrary pointwise-finite homotopies on the infinite domain Z^n.

To write a group law entirely on finite boxes, first extend the two transverse boxes to the same size and concatenate along the first coordinate, with a basepoint slice between the blocks. This corresponds under the bijection to loop concatenation. The extra slice is a duplicate basepoint slice and is harmless by Section 2. Grandis's group law therefore proves it well-defined, associative, with identity the constant map and inverse given by reflection of the first coordinate. It is abelian for n>=2. These statements can alternatively be read from ordinary homotopy groups after the following theorem. For n=2, the diagonal two-block product of the 2024 paper agrees with this product by the same local collar/sliding lemma.

## 4. Realization and the requested value

Grandis's Theorem 6.6 supplies the natural group isomorphism from pi_0(Omega^n K) to pi_n(|K|,b). Combining it with the proposition gives

    D_n(X,b) ~= pi_n(|Cl(X)|,b),  n>=1.

Thus D_n is a functor to groups, and to abelian groups for n>=2. This is a finite-grid presentation of an already established simplicial theory. It is not merely a definition of D_n by a topological realization: its representatives and equivalence relation were specified independently in Section 1, and the bridge was checked in Section 3.

On a unit cube, a representative realizes explicitly as the multilinear interpolation of its 2^n vertex labels, regarded as vertices of the simplex that contains them. These interpolations agree on common faces. A strong digital homotopy realizes by the same construction in n+1 dimensions. The cited comparison theorem establishes the converse direction as well; no assertion that digital continuity alone gives that converse is being made.

For the test case let S={+/-e_1,+/-e_2,+/-e_3} in Z^3, with c_2 adjacency and b=-e_1. The restriction of c_3 adjacency gives the same graph. Its adjacency is

    u~v iff u != -v.

A clique contains at most one point from each antipodal pair; the maximal cliques are the eight triples choosing one point from each pair. Hence Cl(S) is the boundary of the three-dimensional cross-polytope. Its realization is an ordinary 2-sphere. Therefore

    D_2(S,-e_1) ~= pi_2(S^2) ~= Z.

The same observation identifies D_n(S,-e_1) with pi_n(S^2) for every n>=1. It does not claim all those groups are Z. In degree two this independently matches the 2024 signed-triangle degree theorem.

A second direct check is available without the all-dimensional bridge. The categorical simplicial rectangle used to define the 2025 face group is exactly Cl(I_m x I_n). Its representatives, contiguity relation, trivial extensions, and diagonal product therefore coincide with those of D_2 when the target is Cl(X). The 2025 face-group realization theorem thus gives the same degree-two comparison. Its future-work section announces the digital consequence but does not include a separate digital proof; the identification just given spells out the missing definitional step.

## 5. A finite countercertificate for the wrong convention

Keep the graph S, but use box homotopies, which require continuity of each slice and only pointwise adjacency between successive slices. Write the six labels as +/-1,+/-2,+/-3 with basepoint -1. Let

    h(1)=2; h(x)=-1 for x!=1.

The maps id, h, and the constant -1 map are continuous, fix the basepoint, and form a two-step box homotopy. The image of h is the adjacent pair {2,-1}. Pointwise, x~h(x) for every x, and h(x)~-1 for every x. Thus the sphere is based box-contractible. Any homotopy invariant under this weaker convention must vanish on it.

The first step fails the strong condition at u=1,v=-2: u~v, but id(u)=1 is not adjacent to h(v)=-1. More strongly, the identity has no nonidentity one-step strong neighbor. If g is such a neighbor, then for each v, g(v) must be adjacent to every element of N(v)=S minus {-v}. The intersection of these neighborhoods is {v}, forcing g(v)=v.

The exact checker enumerates all 1,057 continuous based endomorphisms, confirms this rigidity, and confirms the displayed two-step box contraction. It also checks the clique counts (6,12,8,0), 534,600 instances of the collar cross-condition, and 61,885 strong-homotopy/flag-contiguity comparisons over all reflexive graphs with at most four vertices. These computations are controls; the general arguments above are proofs.

## 6. The Tucker remark

The target graph is precisely the complementary-label graph in Tucker's lemma. If a triangulated 3-ball has an antipodally symmetric boundary and its vertex labels lie in {+/-1,+/-2,+/-3}, with odd boundary labels, then Tucker's lemma gives an edge with opposite endpoint labels. Consequently no such labeling is a digital map from the reflexive one-skeleton into S. This is an exact digital non-extension obstruction. It establishes a relationship with the requested theory without claiming that Tucker's lemma is logically equivalent to the full comparison theorem.

## What is and is not settled

For the explicit strong-product, boundary-fixed, trivial-extension convention, the original construction-and-test request is resolved by the prior theory plus the finite-support identification. The octahedral result itself was already published in 2024. No novelty or convention-independent solution is claimed. Relative groups, every competing digital homotopy convention, and algorithmic complexity questions were not part of the stated construction-and-test target and are not silently asserted here. The finite-support bridge and this scope classification require fresh independent audit before publication.

## References

- [AIM workshop report](https://aimath.org/pastworkshops/combhomotoprep.pdf), pp. 1-2.
- [Lupton–Musin–Scoville–Staecker–Treviño-Marroquín, 2024](https://doi.org/10.1007/s10801-024-01352-9), Definitions 2.3, 2.9, 4.1 and Theorem 5.5; [preprint](https://arxiv.org/abs/2310.08706).
- [Grandis, 2002](https://doi.org/10.1023/A:1014326730784), Sections 1.6, 2.2-2.4, 3.1, 6.2 and Theorem 6.6; [preprint](https://arxiv.org/abs/math/0009166).
- [Lupton–Scoville–Staecker, 2025, v2](https://arxiv.org/abs/2503.23651v2), Sections 2-4, Theorem 8.1, and Section 9.
- [Milićević–Scoville, 2026](https://doi.org/10.1007/s41468-026-00246-y), Example 2 and Theorem 24. This different, closure-space formulation treats comparison with digital groups as conjectural; it is not used as a proof of the finite-grid bridge.
