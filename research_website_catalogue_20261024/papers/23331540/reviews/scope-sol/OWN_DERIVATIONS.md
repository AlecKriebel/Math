# Independent source-first derivations and attempted falsifications

Written from the actual 180-line manuscript and three PDF text/pixel pages before source support code, README/SUPPLEMENT, archived audits/results, current other reviews or any new foreign mathematical body. These are analytic deductions and exact hand controls, not finite executable evidence or a final literature/interface disposition. No priority claim is made.

## 1. The invariant really needed by the forward implication

For an edge e=ij, the coordinate ray R_{>0}e_e meets W_G(P) iff p_i=p_j. Indeed equilibrium of the vector e_e has only two possibly nonzero vertex rows, p_j−p_i and its negative. If a sign-preserving homeomorphism h:W_G(P)→W_G(Q) exists, a vector with sign pattern positive at e and zero elsewhere maps to a vector with that same pattern. Such a vector is a positive multiple of e_e, so the property transfers both ways by h and its inverse. No linearity of h is assumed. The origin is automatically fixed because its all-zero sign pattern is unique.

Thus Δ_ij is saturated under the whole equivalence relation whenever ij is an edge. Refining each class into its connected components preserves saturation. This is stronger than a dimension argument and does not require generic rank, semialgebraic connectedness or local path connectivity.

## 2. A basis-free form of the collinear transport

Fix any nonzero a∈R^d and scalar placements x_v. For any orientation e=(u,v), the force at u contributed by e is w_e(x_v−x_u)a, and the force at v is its negative. With B_e=+e_u−e_v and D_e=x_v−x_u, all forces vanish iff B D w=0, since a≠0. Reversing orientation negates both B_e and D_e, leaving B D unchanged.

For two scalar placements with every graph edge uncollapsed and each edge difference of the same sign at the two placements, D_1^{-1}D_0 is positive diagonal. It maps ker(BD_0) bijectively onto ker(BD_1), with inverse D_0^{-1}D_1, and preserves every coordinate's positive, negative and zero status. This is an exact global linear homeomorphism, not merely an equality of ranks or an infinitesimal deformation.

For a nonedge ij, put x_i(t)=t, x_j(t)=0 and x_k(t)=k+1 for all other labels, −1/2≤t≤1/2. The constant positions are distinct and at least 2. Hence only ij can collide, and no graph-edge difference vanishes or changes sign anywhere on this interval. The positive transport exists for every t relative to 0. The placement path is continuous and lies wholly in one equivalence class. A connected subset lies in one connected component of that class, irrespective of whether the class itself is closed or locally path connected. It contains a point of Δ_ij at t=0 and a point outside at t=1/4. This supplies the required stratum that crosses the diagonal.

This test handles every simple graph, including dense graphs and graphs with nontrivial stress space. It is not a theorem restricted to forests or collinear configurations: a single admissible path inside the full space is sufficient to falsify saturation for a chosen nonedge. For m=0, the matrices have zero columns and the unique map of the zero stress space is the required homeomorphism.

## 3. Full original reconstruction, without comparing different edge-coordinate spaces

For any partition S of the fixed labelled X=(R^d)^n, define R(S)={ij:Δ_ij is a union of whole elements of S}. Items 1–2 prove R(S_d(G))=E(G). Therefore equal partitions imply equal edge sets. Conversely equal edge sets give identical equilibrium equations, equivalence classes and connected components. There is no step requiring a coordinate-sign homeomorphism from a G stress space to an H stress space of possibly different dimensions.

Under a specified label permutation σ, the configuration map P↦(p_{σ^{-1}(v)}) carries Δ_ij onto Δ_{σ(i)σ(j)} and reindexes the equilibrium equations. The same reconstruction proves the stated permutation corollary. Arbitrary ambient homeomorphisms do not have to preserve these specific diagonals, so the argument cannot classify them.

## 4. An explicit dimension-only failure inside the admitted domain

Take the triangle 12,23,31 and collinear positions x=(t,0,2), oriented 1→2→3→1. At t=0, the collapsed edge12 is free and the remaining two edge columns form a tree; W=span{(1,0,0)}, of dimension 1. At t=1/4, the edge differences are (−1/4,2,−7/4), and the cycle stress (−4,1/2,−4/7) spans W, also of dimension 1. Direct equilibrium is (1−1,−1+1,−1+1)=0 at the three vertices.

At the collision there is a singleton-support vector; off the collision every nonzero vector in the one-dimensional stress space has all three coordinates nonzero. The two spaces therefore are not coordinate-sign equivalent despite equal dimension. This defeats a potential rank-only shortcut to the forward implication. It is not a counterexample to the manuscript, which uses labelled coordinate support.

## 5. Independent complete forest characterization

For a forest F, eliminate a leaf. If its edge is uncollapsed, its leaf force equation makes the corresponding weight zero. If it is collapsed, that weight is arbitrary and contributes zero force at both ends. Removing the leaf and repeating proves, for arbitrary placements in any d≥1,

    W_F(P) = span{e_e : e is a collapsed forest edge}.

Hence two placements of the same forest are equivalent exactly when their sets Z of collapsed edges coincide; singleton supports prove necessity, and identical coordinate subspaces prove sufficiency. This argument allows any other vertex collisions, coincidences among components, self-intersections and deficient affine span.

Choose one root in each of the c components and orient forest edges away from the roots. The coordinate map P↦(root positions, z_e=p_child−p_parent) is a linear isomorphism from X to (R^d)^c×(R^d)^m; its inverse adds differences along the unique root paths. The class with collapsed-edge set Z is precisely

    (R^d)^c × product_{e∈Z}{0} × product_{e∉Z}(R^d\{0}).

For d=1, connected components are independently selected positive/negative signs of each nonzero geometric edge difference. There are 3^m strata in total. For d≥2, R^d\{0} is path connected, giving one component per mask and 2^m strata. This shows why connected-component refinement can distinguish placement chambers even when their stress spaces are the identical zero space.

Any two forests on the same n with the same m (hence same c) therefore have ambient-linearly equivalent partitions after matching root and edge-difference coordinates. This is a checkable independent characterization of the manuscript's warning, not a proposed new follow-up or an assertion of historical novelty.

## 6. Exact four-vertex path/star control

For G={12,23,34} and H={12,13,14}, the source map has matrix

    q1=p1, q2=p2, q3=p1−p2+p3, q4=p1−p3+p4.

It is triangular with determinant 1 in each scalar coordinate. Its inverse is

    p1=q1, p2=q2, p3=q3−q1+q2, p4=q4+q3+q2−2q1.

It gives q2−q1=p2−p1, q3−q1=p3−p2 and q4−q1=p4−p3. Thus it matches the collapsed-edge masks and their connected components via the explicit forest coordinate description above. The degree multisets are {2,2,1,1} and {3,1,1,1}, so the graphs are nonisomorphic. Each has 27 strata when d=1 and 8 when d≥2, but their partitions as subsets of the original fixed X differ. An arbitrary ambient equivalence cannot be substituted for literal equality.

## 7. Collinear formula with collapsed edges and cycle rank

For any graph at a collinear placement, split E into Z={collapsed edges} and N=E\Z. Its force matrix is [0,B_ND_N]. Therefore

    W_G(P) = R^Z ⊕ D_N^{-1}ker(B_N),
    dim W_G(P) = |Z| + |N| − n + c(G_N),

where G_N includes all n labels, including isolates. The rank identity rank B_N=n−c(G_N) follows by choosing a spanning forest in each component: its columns are independent by leaf elimination and every extra column is the signed sum along the tree path. This independently checks the incidence normalization and explains the triangle's equal dimensions across one collision. If Z and the signs of the nonzero edge differences stay fixed, a positive diagonal map transports these spaces, including the R^Z factors.

## 8. Maximum stress locus is weaker than the full partition

W_G(P)=R^{E(G)} iff every edge collapses, by the individual coordinate vectors. Thus that locus is the linear subspace of placements constant on each connected graph component, with dimension d*c(G); it is connected. It can recover the connected-component partition of vertices, but not the internal edge sets of connected graphs. A path and a star both have the all-vertices-coincident maximum-stress stratum. The theorem needs the full partition and the family of fixed diagonals, not merely its largest stress dimension or this special stratum.

## 9. Necessary domain boundaries

- n=1 has only the empty simple graph; the pairwise criterion is vacuous. For an edgeless graph W=R^0 and all X is one stratum, since X is connected. Every Δ_ij is a proper subset when n≥2,d≥1, so no nonedge diagonal is saturated.
- d=0 would break reconstruction: X is a single point for every graph, and every Δ_ij=X is a union of strata even for a nonedge. The asserted d≥1 is necessary for the nonzero path direction.
- If loops were allowed, loop forces vanish identically; a loop-only graph and the empty graph each have a single full-space stratum despite different edge sets. The simple-graph restriction excludes this.
- Even without loops, arbitrary parallel-edge multiplicities are not reconstructed by the same partition. For n=2, one edge gives W=0 off Δ and R on Δ; two parallel edges give W=span(1,−1) off Δ and R² on Δ. Within either graph all off-diagonal placements have the same fibre and the diagonal is the other class. Connected refinement yields the same subsets (for d=1, Δ and two half-spaces; for d≥2, Δ and its connected complement). Hence simple edges are a substantive hypothesis.
- Deleting collisions also breaks reconstruction for forests: every noncollapsed forest placement has W=0, so on a common collision-free domain all forests induce its connected components, independent of the forest's edges. The full-space collision convention is central.
- Deficient affine span and collinear placements are explicitly admitted, so using them as witnesses does not narrow the theorem. No generic-position replacement is warranted.

## 10. What remains open in this lane at the source-only seal

No within-hypothesis counterexample emerged from these exact controls. The analytic mechanism survives the stated boundaries under the manuscript's explicit definitions. The external task interface is not yet independently verified: actual Karpenkov Problem 4 and preceding definitions, actual DKS equivalence/full-space convention and actual Panina detector/collinear passage must be read after the seal. The source's limited interpretation does not license an inference about unwritten author intention or arbitrary ambient/abstract/generic-only comparisons. Archived source audits and stored expected outputs remain unread; no finite computation has run and none is claimed as universal proof. The parent checkpoint hold begins immediately after the INITIAL seal.
