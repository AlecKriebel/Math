# Further face-category results after five substantive turns

**Work in progress; new results await separate review. The original intended-category question remains unresolved.** The qualified first review of the triangulated construction is retained. It does not authorize an unqualified solved outcome.

## Turn 2: nine maximal convex faces, but no incidence-preserving normal matching

Take the square D=[−1,1]² at height one, the four bottom vertices at height zero, and replace the whole top by four triangles joining its boundary to the apex (0,0,1+h). Compare h=1/2 and h=−1/2. Both boundaries are embedded polyhedral spheres, with one bottom square, four rectangular walls and four roof/dent triangles. Every face is convex and maximal planar, and every pair of adjacent faces is noncoplanar. The upper surface is a positive graph over D in both cases, so embeddedness and spherical topology are immediate.

Match the bottom and walls to themselves; match each raised roof triangle to the dent triangle on the opposite edge. The oriented area vectors coincide, face by face. For example the right roof triangle has area vector (1/2,0,1), identical to the left dent triangle. Their volumes are 4±2/3, namely 14/3 and 10/3, so they are not congruent.

This is a counterexample to the maximal-convex-face *multiset-of-normal-area-data* formulation. Its normal matching does not preserve adjacency to the walls, and this defect is explicitly verified. It therefore does not settle a strengthened requirement of an incidence-preserving face correspondence. Merely calling both face lattices abstractly isomorphic would not repair that problem.

## Turn 3: coherent maximal-face correspondence, with two nonconvex polygons

Credit: the parent suggested attaching a sliding raised box to one outer edge; the following coordinates and verification implement that suggested route.

Let K_t be the union of [−4,4]×[−3,3]×[0,1] and [t−1/2,t+1/2]×[2,3]×[1,3], for t=0 or1. Its boundary has ten maximal planar faces. The top of the base is a simple notched polygon, area47; the back is a simple stepped polygon, area10. The remaining eight faces are rectangles: bottom48, front8, two outside walls6 each, three raised walls2 each, and raised top1. No face has a hole. No adjacent pair is coplanar.

The natural correspondence fixes the outer base vertices and translates every cap vertex by (1,0,0). It preserves every face and edge incidence, supporting-plane directions, outward unit normals and total face areas. It extends to an ambient homeomorphism: let rho(x) equal zero outside [−4,4], one on [−1,2], and be affine on the two intervening intervals. Then (x,y,z)↦(x+rho(x),y,z) is an orientation-preserving piecewise-affine homeomorphism, since its x-slopes are 4/3,1,1/2 (or1 outside), all positive. It fixes the base box as a set and translates the cap. Thus both surfaces are embedded spheres with a coherent maximal-face correspondence.

Their volumes are50. The bottom is the unique largest planar patch and has center0. The two volume centroids are (0,1/10,14/25) and (1/25,1/10,14/25), whose squared distances from that distinguished center are809/2500 and813/2500. Hence the surfaces are not congruent, including under reflections.

The two nonconvex polygons are essential to the stated face convention. This example does not satisfy a requirement that all maximal faces be convex polygons. Subdividing them into convex faces reintroduces coplanar edges; that fact is not hidden.

## Turn 4: rigidity for coherent nonflat triangular meshes

Here is an exact obstruction to extending the first example by simply removing all flat edges. Suppose two closed connected triangulated 2-manifolds, each realized in R³ by nondegenerate planar triangles, have an incidence-preserving vertex/edge/face correspondence, corresponding faces parallel with equal positive area, and every adjacent pair of faces noncoplanar. Every edge is incident to exactly two triangles, and the face-adjacency graph is connected. Their corresponding edges are parallel: an edge direction is the intersection direction of its two incident face planes, and the two corresponding pairs of planes are parallel.

In one triangle let the three oriented edge vectors be u,v,−u−v, where u,v are independent. Write the corresponding edge vectors as a*u,b*v,−c*(u+v). Their sum is zero, so a=b=c. Equal face areas give a²=1. Neighboring triangles have the same scale, because their shared nonzero edge vector has the same signed scale under the fixed vertex correspondence. Connectivity propagates one common scale lambda∈{−1,1} to every edge. Connectivity of the vertex graph then gives p'_v=lambda*p_v+t for one vector t. The two surfaces are congruent.

This elementary argument needs neither convexity nor embeddedness, but does need the coherent correspondence and the nonflat-edge condition. It does not extend automatically to convex polygonal faces with more than three sides: a parallel quadrilateral need not be homothetic. Triangulating such polygons introduces flat internal edges and loses the hypothesis.

## Turn 5: convex nonflat coherent quadrilateral pair, with explicit self-intersection

To investigate the remaining polygonal case, consider the four-point meridian profile

(r_i,z_i)=(1,−2),(3,1),(1,2),(3,−1), indices modulo4,

and four angular directions u_j=(1,0),(0,1),(−1,0),(0,−1). The toroidal quadrilateral mesh has vertices p_ij=(r_i*u_j,z_i) and faces (i,j),(i+1,j),(i+1,j+1),(i,j+1). Consecutive radii satisfy r_i*r_(i+1)=3. Define a parallel mesh

p*_ij=(u_j/r_i,−z_i/3).

The profile-edge vectors of p* are −1/3 times those of p, while each angular edge is parallel to the original one. Set p^±=p±(1/2)p*. Every corresponding quadrilateral remains planar, strictly convex and nondegenerate; adjacent face planes are nonparallel. The face incidence is identical and the oriented area vectors are equal.

Indeed for a general parameter tau, the profile differences are multiplied by 1−tau/3, while the sum of the two radii bounding any quadrilateral is multiplied by1+tau/3. Its oriented area vector is therefore multiplied by1−tau²/9. At tau=±1/2 the common multiplier is35/36. Positivity of all new radii and of the profile scale ensures no sign reversal.

This mesh closes exactly. In a general rotational parallel-dual construction, the vertical period is proportional to the sum of Delta z_i/(r_i*r_(i+1)); here every denominator is3, so it vanishes. For a simple meridian polygon in r>0, by contrast, that sum equals the line integral of dz/r², since each straight edge contributes exactly Delta z/(r_i*r_(i+1)). Green's theorem identifies it, up to orientation, with the nonzero integral of 2/r³ over the enclosed region. Thus the same particular construction cannot close its parallel dual for an embedded rotational torus with a simple meridian. This is an obstruction to this route, not to all embedded polygonal examples.

Our chosen profile is a bow tie. Its first and third edges cross transversely at (r,z)=(7/3,0), at parameter2/3 along both segments. For p^± this produces explicit self-intersection rings of radii47/18 and37/18. Therefore these are immersed polyhedral tori, **not embedded surfaces**. Each of their16 faces is a genuine convex nonflat quadrilateral. The two squared diameters are386/9 and338/9, respectively, so they are not congruent. The diameter is obtained by maximizing over the16 vertices, which is exact because every face is convex and lies in their convex hull.

## Exact checks and remaining source gap

The locally authored refined_witnesses.py verifies all three finite pairs with714 exact rational assertions. It checks planarity, face area vectors, convexity where claimed, every oriented manifold edge, nonflat adjacency, matching incidence or its explicit failure, volumes/centroids, torus closure, exact diameters and the explicit self-intersection. The data are saved in refined_witnesses.json. These computations supplement the geometric proofs; no self-intersection is mislabeled as embeddedness.

Taken together, the constructions show why source conventions matter. We have not settled the simultaneous requirement of an embedded surface, convex maximal nonflat polygonal faces, and a coherent incidence-preserving cooriented correspondence. Nor have we established that Ghomi intended or excluded all those additional requirements. The original intended-category problem therefore remains held after five substantive turns. No historical novelty claim is made. No further author proof search is conducted under this budget; all later work is independent validation or packaging.
