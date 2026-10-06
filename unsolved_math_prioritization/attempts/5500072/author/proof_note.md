# A local obstruction for regular-pentagon polyhedral surfaces

Problem: 5500072 / AMR-054-0072 (TOPP 72). Result: partial only.

## Model and limits

Work with a finite closed edge-to-edge polygonal cellulation of an abstract sphere, realized in Euclidean three-space by congruent planar convex regular pentagons. Each face is realized isometrically. The realization is locally embedded at every abstract point, including vertices; different sheets may intersect. Distinct faces may not coincide. Faces are not allowed to fold across interior creases. Incidences and valences below refer to the abstract cellulation, not to accidental intersections of its image.

These are the standard flat-face, full-edge hypotheses used in this note. A broader convention allowing non-edge-to-edge junctions, branched vertices, or folded tiles is not covered. None of the results below provides the required global decomposition into dodecahedra, under any interpretation of that decomposition. No novelty is claimed.

## 1. Curvature and counting

Let n_d count vertices of valence d, and let V,E,F be the numbers of cells. A vertex of valence two would have only two incident pentagons. Their two incident edge rays would be the same, hence their planes and the convex 108-degree sectors would coincide. A planar regular pentagon is determined by its corner and two incident unit edges, so the two pentagons would coincide. This is excluded. Valence one is incompatible with a locally embedded closed surface made from regular polygonal disks. Thus d >= 3.

Full-edge incidence gives 5F=2E, and Euler's formula gives V-E+F=2. Consequently

    sum_d (10-3d)n_d = 20,
    n_3 = 20 + sum_{d>=4}(3d-10)n_d,
    F = 12 + 2 sum_{d>=4}(d-3)n_d.

Equivalently, the angular defect at a d-valent vertex is (10-3d)pi/5. There are at least twenty trivalent vertices. This does not bound F from above or eliminate negatively curved vertices.

If N_0 is the number of faces whose five vertices are all trivalent, counting incidences with higher-valence vertices yields only

    N_0 >= F - sum_{d>=4} d n_d
         = 12 + sum_{d>=4}(d-6)n_d.

The right-hand side need not be positive. This inequality alone cannot supply a removable dodecahedral cap.

## 2. Trivalent rigidity

Set q=(sqrt(5)-1)/4, so cos(108 degrees)=-q, 0<q<1/3, and 4q^2+2q=1. At a trivalent vertex let u_1,u_2,u_3 be the unit vectors along the three incident edges. The angle in each of the three pentagons implies u_i dot u_j=-q for i != j. Their Gram matrix has eigenvalues 1+q,1+q,1-2q, all positive. Hence the three rays, and then the three planar regular pentagons, are fixed up to a Euclidean orthogonal transformation. This is the regular dodecahedron's local corner geometry.

For two adjacent face planes along any edge at this vertex, unit normals have absolute scalar product

    r = (q^2+q)/(1-q^2) = q/(1-q) = 1/sqrt(5).

The absolute value removes arbitrary choices of normal orientations. Face planes remain fixed along the entire edge. Therefore every edge with a trivalent endpoint has this same unoriented dihedral-plane invariant.

This local rigidity is not a global rigidity or decomposition theorem.

## 3. Four-valent obstruction

Proposition. At a four-valent vertex, two cyclically adjacent incident edges cannot both have trivalent opposite endpoints.

Proof. List its outgoing unit edge rays in cyclic order as u_1,u_2,u_3,u_4. Consecutive rays have scalar product -q. Write a=u_1 dot u_3 and b=u_2 dot u_4. The Gram matrix is

    G = [[1,-q,a,-q],[-q,1,-q,b],[a,-q,1,-q],[-q,b,-q,1]].

Since the vectors belong to R^3, det(G)=0. Directly changing to the sum/difference bases for the opposite pairs gives

    det(G) = (1-a)(1-b)((1+a)(1+b)-4q^2).

The two face planes meeting along u_2 have, up to choices of normal signs, cosine (q^2-a)/(1-q^2). Along u_1 the corresponding expression is (q^2-b)/(1-q^2). The other two incident edges repeat these two expressions, respectively.

If the opposite endpoint of the edge along u_2 is trivalent, Section 2 forces

    |q^2-a|/(1-q^2) = r,

so a is either -q or 1/2. A cyclically adjacent edge ending at a trivalent vertex similarly forces b to be either -q or 1/2. Both a,b are then less than 1, and

    (1+a)(1+b)-4q^2 >= (1-q)^2-4q^2 = q^2 > 0.

Thus det(G)>0, a contradiction. This proves the proposition. The argument also handles any cyclic relabeling of the two selected adjacent edges. It does not assume convexity or a common orientation for face normals.

Corollary. A four-valent vertex has at most two trivalent neighbors, and if there are two, the corresponding incident edges are opposite in its cyclic order. In particular, at least two incident edges lead to vertices of valence at least four.

Corollary for the valence-{3,4} class. If four-valent vertices occur and every vertex has valence three or four, the graph induced by the four-valent vertices has minimum degree at least two and therefore contains a cycle. The abstract graph is simple here: distinct edges with the same endpoint pair would have the same straight-segment image and violate local embedding at those endpoints. The cycle is not a decomposition certificate.

## 4. Why the local analysis stops

Four-valent stars themselves do exist with a continuous shape parameter. For q<t<1, set s=q/t and

    u_1=(sqrt(1-t^2),0,t),
    u_2=(0,sqrt(1-s^2),-s),
    u_3=(-sqrt(1-t^2),0,t),
    u_4=(0,-sqrt(1-s^2),-s).

Each ray is unit, and each consecutive scalar product is -q. The shorter great-circle arcs between consecutive rays lie in the successive open azimuthal quadrants, so they form an embedded spherical link. Planar 108-degree sectors along these rays can therefore be extended to four unit regular pentagons giving a locally embedded vertex star. This is a local construction, not a closed sphere.

The invariant u_1 dot u_3=2t^2-1 varies continuously. In particular t=1/2 and t=3/4 give different labeled stars. A finite relabeling cannot remove this continuous freedom. Any attempted extension to a full closed surface must satisfy the remaining face and edge constraints, which are not solved here.

Three bounded approaches were used: global incidence/curvature; trivalent-to-four-valent dihedral propagation; and a local-flexibility/decomposition check. The obstruction above sharpens the second approach but does not control vertices of valence at least five, global cycles of higher-valence vertices, or the existence of a legal dodecahedral removal. The investigation stops with these explicit gaps. The full immersed and embedded questions remain unresolved by this work.
