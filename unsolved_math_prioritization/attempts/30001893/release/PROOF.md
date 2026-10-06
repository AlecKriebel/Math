# Convex partitions of three-space: five retained approaches

Problem 30001893 / OWR-11136-024. Authored research record, 2026-10-05.

## Result and precise scope

**The full problem is unresolved in this work.** For the standard space C(R^3,n) of labeled nonempty open convex regions, with n >= 4, we retain

    4n - 5 <= dim C(R^3,n) <= 3 binomial(n,2).

The lower bound and the regular-family dimension are established prior results; no novelty is claimed. We give complete arguments for the retained constructions and bounds below. Five materially different routes were investigated. None gives the missing upper bound 4n-5 for all affine partitions. An exact incidence example shows why subtracting the number of written equations is insufficient.

The governing original question is Ziegler's Problem 2, printed p.2539 of the 2011 Oberwolfach report *Discrete Geometry*, DOI https://doi.org/10.4171/owr/2011/44. It asks for the maximal realization-space dimension over combinatorial types of partitions of R^3 into n>3 convex pieces. Its surrounding discussion prints 4n-1 for the three-dimensional power-diagram family, and 4n-1 and 3n-1 for the two-dimensional general and regular families. These numbers must not be silently substituted into a corrected statement.

The precise later reference is Emerson Leon and Gunter M. Ziegler, *Spaces of convex n-partitions*, https://arxiv.org/abs/1511.02904, v1, 2015. Definition 2.1 specifies ordered nonempty open regions with disjoint interiors (the open regions themselves are pairwise disjoint) whose closures cover the whole space. Theorem 6.2 gives (d+1)(n-1)-1 for regular partitions when d,n>=2. Conjecture 6.3 proposes 4n-5 for the full three-dimensional space. Theorem 6.1 gives 4n-7 for the planar space when n>=3. The author's 2015 dissertation supplies proofs and additional qualifications: https://refubium.fu-berlin.de/handle/fub188/829, especially Proposition 5.4 and Section 6.3. A 2018 published chapter with the same title is bibliographically verified, but its complete version of record was not retrieved. The proof below therefore attributes the inspected claims to the 2015 sources, not to an uninspected 2018 text.

The exact live UnsolvedMath page https://www.unsolvedmath.com/problems/30001893 could not be inspected: web retrieval failed and direct requests returned HTTP 403. The matching catalog descriptor identifies the title, ID and OWR source. The live wording, its machine-generated review, and the raw upstream AI corpora remain uninspected. This is not a claim that their wording equals the later conjecture.

## Conventions

A partition is an ordered tuple P=(P_1,...,P_n) of nonempty open convex subsets of R^3, pairwise disjoint, with union of closures R^3. Nonempty openness implies full dimension. Sets are not required to be bounded, pointed, regular, central, or face-to-face. Shared boundaries are represented by closures, not assigned arbitrarily to one label. Empty regions occur only in a separate compactification, which is not the target here.

We do not quotient by translation, rotation, affine equivalence, or scale of physical space. Relabeling is a finite operation; it does not alter semialgebraic dimension, but labels remain fixed throughout the arguments. In particular, the five dimensions removed from a 4n-parameter regular representation below are redundancies of that representation, not a quotient of physical partitions by a five-dimensional geometric group.

For topology use the map x |-> (1,x)/sqrt(1+|x|^2) into the open upper hemisphere of S^3 and the sum, over labels, of spherical volumes of symmetric differences. The metric is zero only for identical open convex regions: a difference between two such regions produces a positive-volume difference. Dimension below is the maximum semialgebraic dimension of the finitely many realization-space pieces, as in the cited definition and original question. Such pieces have their usual topological dimension. We make no independent assertion that the Hausdorff dimension for every possible metric, or for an arbitrary reparametrization, is equal to this number. The standard semialgebraic facts used are quantifier elimination, finite stratification, dimension monotonicity under semialgebraic maps, and dimension invariance under semialgebraic bijections. The implicit-function theorem is used only at an explicitly certified nonzero minor.

## Approach 1. Supporting planes and a genuine global upper bound

### Proposition 1.1: every region is polyhedral

For each distinct pair i,j choose an affine separator h_ij with h_ij>0 on P_i and h_ij<0 on P_j, and set h_ji=-h_ij. Separation of disjoint nonempty open convex sets supplies such a nonconstant affine function, including when their closures meet. Let Q_i be the intersection of the closed halfspaces h_ij>=0 over j!=i.

Certainly closure(P_i) is contained in Q_i. If int(Q_i) contained a point outside closure(P_i), a sufficiently small ball in int(Q_i) would avoid closure(P_i). Because the finitely many closures cover space, and the boundaries of the finitely many nonempty convex open sets have empty interior, this ball contains a point of some P_j. That contradicts h_ij>=0 there. Thus int(Q_i) is contained in closure(P_i). The set Q_i has nonempty interior because it contains P_i; consequently Q_i=closure(int(Q_i)). It follows that Q_i=closure(P_i). Finally int(closure(P_i))=P_i for nonempty open convex P_i. Hence P_i is exactly the solution of the n-1 strict inequalities h_ij>0. This proves the claim without assuming a face-to-face complex.

### Proposition 1.2: dim C(R^3,n) <= 3 binomial(n,2)

Write each h_ij(x)=a_ij dot x+b_ij, with its four coefficients normalized to the unit sphere S^3 and orientation fixed by i. There are N=binomial(n,2) such choices, hence a parameter space of dimension 3N. The condition that the strict intersections are nonempty, pairwise disjoint, and have closures covering R^3 is first-order over the real field. For example, nonemptiness is an existential system of strict linear inequalities, and closure coverage is a universal disjunction of weak inequalities. Quantifier elimination therefore makes the admissible parameter set semialgebraic.

For completeness, one need not apply dimension monotonicity to an unspecified quotient. Fix an adjacency graph G, where ij is an edge when closure(P_i) and closure(P_j) share a relatively open two-dimensional set. For an adjacent pair the oriented support plane is unique. Each facet of closure(P_i) is supported by at least one such adjacent region: subdivide its relative interior by the finitely many boundaries of the other polyhedra and choose a two-dimensional open cell on it. On the other side lies some P_j. Thus the adjacent support planes alone recover every P_i. Project the admissible parameter set to the coordinates indexed by G and restrict to the semialgebraic condition that its partition has graph G. These canonical coordinates are injective for the partition and have dimension at most 3|E(G)| <= 3N. Taking the finite union over graphs proves the bound. This also avoids counting the arbitrary separators of nonadjacent regions as distinct partitions.

The coordinate constructions agree with the usual realization pieces; on a fixed nondegenerate local chart, support planes and geometric faces determine each other continuously. Alternatively, dimension in this proposition can be read directly in the canonical semialgebraic graph pieces used in the cited paper.

**Exact obstruction.** The estimate is quadratic in n. The missing improvement requires using the geometric compatibility among adjacent support planes. An arbitrary selection of 3N plane parameters almost never defines a partition, but merely saying so does not give the codimension of the admissible set.

## Approach 2. Regular liftings and an exact fiber computation

A regular partition is given by affine functions f_i(x)=a_i dot x+b_i, with

    P_i = {x: f_i(x)>f_j(x) for every j!=i},

all regions nonempty. The epigraph of max_i f_i is a convex polyhedron, and its facets project to the regions. Conversely a convex lifting gives this description after choosing its height coordinate. The conversion to a weighted Voronoi diagram is immediate from expanding |x-p_i|^2-w_i: affine coefficients rather than the sites themselves are the useful variables.

### Upper bound for regular partitions

The 4n coefficients have a four-dimensional common-affine-function redundancy: replacing every f_i by f_i+g changes no comparison. Remove it by f_1=0. Simultaneously multiplying all remaining coefficients by any positive scalar also leaves the regions unchanged. Nonemptiness implies that the coefficient vector after this subtraction is nonzero. Normalizing its Euclidean norm to one gives a semialgebraic parameter set contained in S^(4n-5). Its image therefore has dimension at most 4n-5. This is an upper bound, not yet an equality: additional fibers can exist for particular diagrams.

### A family with no additional fibers

Start with the four functions 0,x,y,z. All four regions are nonempty, every pair is adjacent, and the coefficient differences in every three-function subset are linearly independent as two vectors. At the origin all four functions agree and dominate.

Here is an induction adding a region. Suppose a diagram has a simple vertex v at which exactly four functions f_i, i in I, agree, all other functions are strictly smaller, and their four slopes are affinely independent. Let f_* be a strictly positive convex combination of these four functions, plus a small number epsilon>0. At v it strictly exceeds the previous maximum. After translating v to zero and subtracting the common value, max_(i in I) f_i-f_*+epsilon is a positive, positively homogeneous, piecewise-linear function away from zero: the slope of f_* is strictly inside the tetrahedron of the four slopes. Its minimum on the unit sphere is positive. Therefore the region where f_* dominates the four old functions is a bounded tetrahedron of diameter O(epsilon). Choose epsilon small enough that this tetrahedron lies in the neighborhood where the other old functions are strictly below max_(i in I) f_i. The new region is precisely that tetrahedron. The four old regions remain nonempty and each becomes adjacent to it. Every old pairwise facet retains a relatively open piece outside the small tetrahedron, by choosing epsilon smaller than the distances to finitely many preselected facet witnesses. The old vertex is replaced by four simple vertices: at each, the new slope together with three of the old slopes is affinely independent. This permits indefinite repetition.

Keep the base K_4 of adjacency edges and, at each insertion, four edges joining the new region to the four cells at the chosen vertex. The graph is connected, and each new edge belongs to a triangle with two older vertices. For an insertion the four older cells are mutually adjacent. Strict witnesses for all retained adjacencies and nonempty cells persist under sufficiently small changes of all affine coefficients. We therefore obtain, for every n>=4, a nonempty open subset U of R^(4n) with this graph of required adjacencies and the required independence of coefficient differences on its triangles.

Suppose f and g in a sufficiently small such neighborhood give exactly the same labeled partition. On each retained adjacent pair ij the functions f_i-f_j and g_i-g_j vanish on the same facet and have the same positive side. Hence

    g_i-g_j = lambda_ij (f_i-f_j),  lambda_ij>0.

On a triangle i,j,k, summing the three differences gives

    (lambda_ij-lambda_ik)(f_i-f_j)
      + (lambda_jk-lambda_ik)(f_j-f_k) = 0.

The two differences are linearly independent, so all three lambdas are equal. On the initial K_4 all six lambdas are equal. The insertion triangles propagate this same value to each of the four newly added edges, inductively. Thus g_i=lambda f_i+g_0 for every i, with one common positive lambda and one common affine g_0.

Now normalize f_1=0 and, on the chart near the base construction, normalize the x-coefficient of f_2 to one. (The original f_2=x remains present at each insertion.) These are exactly five independent scalar normalizations. In this chart the map from U to partitions is injective, by the fiber result. Its domain contains an open set of dimension 4n-5. Partitioning it into finitely many adjacency charts if necessary and using semialgebraic dimension invariance gives a 4n-5-dimensional image. Together with the upper bound, this proves

    dim C_reg(R^3,n) = 4n-5,  n>=4.

This argument is a retained proof of the inspected prior theorem, not a newly discovered value. The same affine gauge explains why normalizing only the sum of Voronoi weights does not produce an injective parameterization: it leaves four further redundancies in dimension three.

**Exact obstruction.** The family of regular partitions is a proper subclass. The source explicitly warns that it is not dense in the full space for n>3. Approach 4 below also gives a direct nonregular example. Neither the regular upper bound nor openness of some regular strata controls other strata.

## Approach 3. Moving pointed central fans

Let F_n be the subclass in which every closed region is a full-dimensional pointed polyhedral cone with the same apex v, translated by v. Here pointed means containing no nonzero linear subspace. The apex is allowed to move. Let F_n^0 fix it at the origin.

### Proposition 3.1

For n>=4,

    dim F_n^0 = 4n-8,     dim F_n = 4n-5.

Intersect the cones with a sphere centered at v. Their intersections give a convex spherical polygonal subdivision of S^2, with n faces. Each pointed cone is contained, apart from its apex, in an open halfspace through the apex, so each spherical polygon lies in an open hemisphere and is a disk. Insert all T-junction vertices, but discard degree-two subdivisions along a common great-circle arc. Every remaining vertex has degree at least three. Indeed a degree-two corner with a genuine bend would make one of the two neighboring polygonal regions locally nonconvex. The resulting graph is connected, all face boundaries are polygonal disks, and Euler's formula gives

    V-E+n=2,     3V<=2E,     V<=2n-4.

A fixed labeled combinatorial type is determined by its V ray directions, each with two parameters. Each edge is the unique short great-circle arc determined by its endpoints (the endpoints belong to an open-hemisphere face); no independent face-plane parameters remain. Convexity and incidence impose further conditions but cannot raise dimension. The type therefore has dimension at most 2V<=4n-8 at a fixed apex. There are finitely many types: for fixed n the preceding bound controls V and E. Adding v gives the upper bound 4n-5 for moving fans.

This bound is attained. There is a simple three-polytope with n facets for every n>=4: start with a tetrahedron and repeatedly truncate a vertex sufficiently close to it. Each truncation keeps simplicity and increases the number of facets by one. Put the origin in its interior and take cones from the origin over its facets. The spherical subdivision is trivalent, with V=2n-4. Each spherical face is strictly convex at its corners and contained in an open hemisphere. Small independent perturbations of all V directions preserve these strict properties and the spherical embedding. To justify the last statement, the finite set of nonincident compact arcs has positive separation, incident arcs have nonzero angle, and each strict spherical corner inequality has a positive margin. Sufficiently small perturbations preserve all of them. The embedded graph has the same labeled disk faces and still covers S^2; its faces are convex spherical polygons. Their cones consequently form valid partitions. Thus an open set in (S^2)^V, of dimension 2V, injects into F_n^0.

No apex parameter has been overcounted. The common intersection of all cones is {0}: if a nonzero vector u belonged to every cone, some cone would also contain -u by completeness, contrary to pointedness. A partition in F_n therefore recovers v as the common intersection of its region closures. It recovers every ray as well. Moving v adds three independent parameters. Local coordinate maps and their inverses are semialgebraic and continuous on the chosen chart. This proves both equalities.

This subclass result agrees with the simple-polytope fan discussion in Leon's dissertation, Proposition 6.13. It concerns arbitrary small convex spherical deformations of a fan; those deformations need not themselves be radial projections of one polytope, and regularity has not been assumed.

**Exact obstruction.** A general affine partition has multiple finite vertices, bounded edges, and possibly bounded cells. Its two-dimensional faces need not be determined by rays from one apex. The sphere-graph Euler estimate therefore gives no global bound for such partitions. Coning an arbitrary partition changes the ambient dimension and does not preserve the target problem.

## Approach 4. Cylindrical partitions and a nonregular obstruction

This route tests whether nonpointed regions supply excess dimension and whether every maximal-dimensional candidate could be regular.

### Proposition 4.1: a cylindrical 4n-5-dimensional family

Begin with a three-sector partition of R^2 whose angles are all strictly less than pi. It has one finite trivalent vertex and three unbounded rays. Locally replace a finite trivalent vertex by a small triangle whose vertices lie on its three incident edges. The three surrounding convex regions are cut off at that corner, and the triangle becomes a new region. For a sufficiently small triangle the resulting cells remain convex with all genuine angles strictly less than pi. Existing edges and unbounded rays outside this neighborhood persist. Each replacement increases the number of regions by one and the finite vertex count by two. For each n>=4 this gives a trivalent planar convex partition with exactly three unbounded rays, at least one bounded region, and V=2n-5 finite vertices.

For any fixed type in this construction, assign arbitrary sufficiently small changes to its 2V vertex coordinates and its three ray directions, one angular coordinate per ray. Finite edges are straight segments between the assigned vertices; unbounded edges start at their assigned vertices. Strict angle inequalities, positive edge lengths, noncrossing of the finite graph, and separated cyclic directions at infinity persist in an open neighborhood. The faces remain convex and cover the plane. This yields an injective local chart of dimension 2V+3=4n-7; the inverse simply reads off vertices and rays. It is a construction of that dimension, not an unproved claim that these exhaust all planar partitions.

For (a,b) in a small open set in R^2 put

    pi_(a,b)(x,y,z)=(x-az,y-bz),
    P_i = pi_(a,b)^(-1)(Q_i).

These are convex open partitions of R^3 with exactly n nonempty regions. The line L=span(a,b,1) is their common extrusion direction. Since at least one Q_i is bounded, its cylinder has lineality exactly L. Thus the labeled partition recovers L and hence a,b in this chart. Its intersection with z=0 recovers the planar partition. Consequently this is an injective semialgebraic family with dimension

    (4n-7)+2=4n-5.

There is no translation parameter along L: such a translation leaves the partition unchanged. The construction is not a central fan; the bounded planar cell becomes a nonpointed infinite prism.

### Explicit four-region example that is not regular

Define four open regions of R^2:

    Q_0: x>0, y>0, x+y<1;
    Q_1: y<0, x>y, x+3y<1;
    Q_2: x+y>1, x+3y>1, 2x+y>1;
    Q_3: x<0, x<y, 2x+y<1.

Their finite vertices are A=(0,0), B=(1,0), C=(0,1). The unbounded rays start respectively in directions (-1,-1), (3,-1), and (-1,2). Each region is visibly an intersection of strict halfplanes and nonempty; for example witnesses are (1/4,1/4), (1/2,-1), (1,1), and (-1,1/2).

Here is a coverage and disjointness check that does not rely on a drawing. Avoid the six boundary lines temporarily. In the first quadrant, x+y<1 gives Q_0 and x+y>1 gives Q_2. If y<0 and x>y, either x+3y<1 gives Q_1, or x+3y>1 implies x+y>1 and 2x+y>1, hence Q_2. If y<0 and x<y, then x<0 and 2x+y<1, giving Q_3. The remaining case is y>0,x<0: 2x+y<1 gives Q_3, whereas 2x+y>1 implies x+y>1 and x+3y>1, hence Q_2. These cases exhaust the complement of the boundary lines. The defining inequalities also make each pair of regions disjoint: Q_0 conflicts with Q_1 on y, with Q_3 on x, and with Q_2 on x+y; Q_1 and Q_3 conflict on x-y; Q_1 and Q_2 conflict on x+3y; Q_2 and Q_3 conflict on 2x+y. Closure coverage follows by taking limits from the dense complement of the lines.

The outer cells are pairwise adjacent along rays contained in the three lines

    x-y=0,    x+3y-1=0,    2x+y-1=0.

If these four regions were a regular diagram, the three differences among the affine functions assigned to outer cells 1,2,3 would be nonzero scalar multiples of these line equations. The differences sum to zero around their cycle. But the coefficient vectors (1,-1,0), (1,3,-1), (2,1,-1), with coordinate order x,y,constant, are linearly independent: their determinant is -1. No such nontrivial cycle relation exists. This proves nonregularity. The determinant remains nonzero on a neighborhood of this planar configuration, so nonregularity is robust within this nine-dimensional planar family. Extruding it and varying (a,b) gives an eleven-dimensional family of nonregular four-partitions of R^3.

If an extruded partition had a regular three-dimensional representation, restricting its affine functions to z=0 would give a regular representation of the displayed planar partition, with every region still nonempty. That is impossible. Thus the obstruction survives extrusion. Inserting additional small triangles can leave the supporting lines between the same three outer regions unchanged, so the same obstruction can also be retained in the constructed families with larger n.

**Exact obstruction.** This reaches the conjectured dimension, but does not exceed it. It rules out the shortcut that all relevant partitions are regular. It does not prove that these nonpointed strata are dense or that arbitrary pointed noncentral strata have the same bound.

## Approach 5. Incidence equations, exact rank, and the missing global certificate

Use vertex coordinates and ray directions to express coplanarity of two-dimensional faces. The tempting argument is to subtract one equation for every extra vertex in a face. Leon's dissertation explicitly calls its analogous count naive and records dependencies. We retain an exact example rather than assume independence.

### A five-region partition with dependent planarity equations

Take the regular diagram

    f_0=0, f_1=x, f_2=y, f_3=z,
    f_4=1+(x+y+z)/4.

The last region is a bounded tetrahedron. Label its four vertices and the unbounded rays issuing from them as

    V_0=(4,4,4),   R_0=(1,1,1);
    V_1=(-4,0,0),  R_1=(-1,0,0);
    V_2=(0,-4,0),  R_2=(0,-1,0);
    V_3=(0,0,-4),  R_3=(0,0,-1).

These coordinates follow by solving the triples of old functions tied with f_4. Outside the tetrahedron the old four regions retain their six pairwise facets. For each i<j the corresponding unbounded face has its finite edge V_i V_j and rays R_i,R_j; planarity is

    F_ij = det(V_j-V_i, R_i, R_j)=0.

There are 12 vertex coordinates and eight ray-chart coordinates, using

    R_0=(1,a,b), R_1=(-1,c,d),
    R_2=(e,-1,f), R_3=(g,h,-1).

Thus there are 20 variables and six written equations. At the displayed configuration a=b=1 and c=d=e=f=g=h=0. All six equations vanish. In the variable order

    (V_0x,V_0y,V_0z,V_1x,...,V_3z,a,b,c,d,e,f,g,h)

and the row order (01,02,03,12,13,23), the Jacobian is

    [ 0, 1,-1, 0,-1, 1, 0, 0, 0, 0, 0, 0,-4, 4, 4,-4, 0, 0, 0, 0 ]
    [-1, 0, 1, 0, 0, 0, 1, 0,-1, 0, 0, 0, 0,-4, 0, 0,-4, 4, 0, 0 ]
    [ 1,-1, 0, 0, 0, 0, 0, 0, 0,-1, 1, 0, 4, 0, 0, 0, 0, 0, 4,-4 ]
    [ 0, 0, 0, 0, 0,-1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 4, 0,-4, 0, 0 ]
    [ 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,-1, 0, 0, 0,-4, 0, 0, 0, 0, 4 ]
    [ 0, 0, 0, 0, 0, 0,-1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 4, 0,-4, 0 ].

Its rows sum to zero. Its first five rows are independent (the exact verifier supplies a nonzero five-by-five minor). Hence its rank is exactly five, not six.

This does not by itself prove that the local solution set has dimension 15: rank deficiency can coexist with singularities and additional nonlinear constraints. Here the dimension can nevertheless be established. The nonzero minor and the implicit-function theorem put the common zero set inside a local smooth 15-dimensional manifold cut out by the corresponding five equations. Conversely, Approach 2 gives a 15-dimensional family of regular five-region partitions through a neighborhood of this simple tetrahedral example. Their four finite vertices and four ray directions depend continuously and semialgebraically on the coefficients, and uniquely recover the partition on this fixed type. The gauge-fixed coefficient map is injective, so their image has dimension 15. Thus the incidence solution set relevant to this partition has local dimension exactly 15. The independent-equation subtraction 20-6=14 is false even in this small regular example.

### What a rigorous global rank route would require

In a canonical chart with M variables, let E be the polynomial incidence equations and let S be its semialgebraic set of valid realizations, including all positivity and nondegeneracy conditions. If at every point of S some Jacobian minor of size M-(4n-5) is nonzero, the implicit-function theorem gives local dimension at most 4n-5. Covering S by these open minor patches proves the bound for S. For points not covered by these minors, one must analyze the remaining semialgebraic rank strata separately, or provide different charts. A calculation at one generic point does not bound a distinct component, and a rank calculation on a regular stratum says nothing about a nonregular one. Artificial auxiliary coordinates must also have their fibers removed or accounted for.

**Exact obstruction.** We have no all-types rank certificate, no bound on the dimension of every exceptional rank stratum, and no reduction of all affine partitions to the central or cylindrical cases. This is precisely the unproved upper bound in the original dimension question; it is not treated as a lemma.

## Boundary checks and disposition

- The target n>3 is retained. For n=1 the partition space is a point. For n=2 a partition is determined by an oriented affine plane, of dimension three; the regular formula agrees. These checks do not extend the original requested range.
- The regular 4n-5 count is for geometric regions, not unquotiented site-weight data. The central fixed-origin count is 4n-8, and adding the apex makes it 4n-5. The cylindrical construction uses exactly n regions, not n planes or arrangement chambers.
- The nonregular example uses nonempty full-dimensional open cells. Its cylinders are allowed by the original full-space convention even though they are not pointed or essential.
- The exact verifier checks rational polynomial identities, matrix ranks/minors, explicit witnesses, and falsifying controls. Finite tests do not prove the universal dimension bound. Analytic proofs, prior-source qualification, and all unresolved gaps remain part of the result.
- No full solution, current worldwide openness certificate, priority claim, or novelty claim is made. This is a five-approach partial research record awaiting a fresh independent audit and the parent's release gate.
