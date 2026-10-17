# Independent acceptance: quartic support geometry and construction limits

Date: 2026-10-13 UTC. Problem: row 1761 / problem 30002861 / OWR-13678-002.

## Verdict and exact scope

The mathematical claims in [SECOND_PASS_CONSTRUCTIONS.md](SECOND_PASS_CONSTRUCTIONS.md) are accepted. No mandatory correction was found. This audit verifies a branch of the same second documented substantive pass, not an additional mathematical pass.

The accepted setting is a fixed conforming straight-line triangulation of a polygonal disk, nondegenerate triangles, arbitrary values and both first partial derivatives at every vertex, and globally C1 piecewise polynomials of total degree at most four. No refinement, boundary condition, generic-position assumption, or additional smoothness condition is used.

The baseline is the immutable [first-edition quartic acceptance](first_edition/QUARTIC_AUDIT.md), identified in [DEPENDENCIES.md](DEPENDENCIES.md): its exact reduction Rm=Hj, active-component criterion, zero-ray classification, convex induced-support theorem, and at-least-three nonsingular degree-four interior vertices theorem are taken as already established. This audit independently checks the new deductions and the new rational example. It does not re-audit the original literature or assert worldwide novelty or openness.

Accepted conclusions:

1. Every nonempty closed active support has at least five strict boundary corners, including when its boundary has straight subdivided sides.
2. The authored 18-vertex rational mesh is a conforming disk with a connected closed twelve-row support. Its sign matrix has rank eleven with a full-support signed dependency, while its actual reduced matrix has rank twelve. Its exact positive cycle product is 683875575/3191327216, unequal to one. Sign balance alone therefore does not force a quartic obstruction, and universal explanations based solely on a negative cycle cannot suffice.
3. Every admissible member of the stated three-parameter alternating-radius, threefold-symmetric family has full reduced row rank and admits arbitrary quartic vertex jets. The exclusion is an exact strict-domain argument, not a conclusion from sampled parameters or numerical optimization.

These results do not settle arbitrary quartic Hermite interpolation on all meshes.

## 1. Exterior feasibility and the five-corner bound

Let K be the convex induced complex of a closed active row component. All its vertices are interior vertices of the original mesh. Consequently each boundary edge of K has exactly one triangle on its other side in the full mesh. The opposite vertex of that triangle is outside K, since K is induced.

At a straight boundary vertex of K, the accepted zero-ray classification leaves exactly one original neighbor outside K. Thus the outside triangles on its two incident boundary edges have the same opposite vertex. Applying this observation successively along an entire straight subdivided side gives a single opposite vertex Q for that side. The argument does not discard the original subdivision vertices or assume a boundary in general position.

At a strict corner A, the two removed rays are adjacent. Write the supported boundary rays as the ray toward the preceding boundary vertex and the ray toward the following boundary vertex. Each removed ray has opposite collinear neighbors in the full circular fan. Therefore the outside triangle across the following side has its opposite vertex on the positive outward extension of the preceding side. At the other endpoint of that strict side, the same opposite vertex lies on the positive outward extension of the following side. Positivity of both ray parameters is essential: the vertices are distinct and the relevant triangles are nondegenerate.

After collapsing only collinear subdivisions, write the strict corners as A_i and their positive exterior turns as δ_i, where 0<δ_i<π and sum δ_i=2π. For the side A_i A_(i+1), set its coordinates to (0,0) and (L,0), L>0. The two required outward unit directions are

(cos δ_i, -sin δ_i),  (-cos δ_(i+1), -sin δ_(i+1)).

If the rays intersect with positive lengths t and s, their vertical coordinates yield s sin δ_(i+1)=t sin δ_i. Substitution into the horizontal coordinates gives

t sin(δ_i+δ_(i+1))=L sin δ_(i+1)>0.

Since δ_i+δ_(i+1) lies strictly between zero and 2π, it follows that δ_i+δ_(i+1)<π. Equivalently, each adjacent pair of strict interior angles sums to more than π. Summing these strict inequalities over k sides gives 4π<kπ, hence k≥5.

For a triangular support, the two purported exterior lines for a side meet only at the third corner, outside both required positive rays. A quadrilateral is excluded by the summed strict inequality. These exclusions apply before any magnitude-balance question and survive all legal straight subdivisions of the boundary.

## 2. Independent exact check of the rational disk

The audit independently reconstructs the six integer outer vertices, six integer inner vertices, six exterior intersections, and twenty-eight oriented triangles printed in the construction report. Its calculation is independent of the construction and first-pass calculations.

The exterior points are computed as intersections of positive rays, rather than merely intersections of unoriented lines. In cyclic order the exact parameter pairs in

Q_i=O_i+t_i(O_i-O_(i-1))=O_(i+1)+s_i(O_(i+1)-O_(i+2))

are

(105/421, 856/1263), (201/127, 945/1016),
(920/2163, 536/721), (1343/1408, 115/176),
(3495/2566, 1343/2566), (856/73, 1165/73).

Every parameter is strictly positive; the six resulting coordinates exactly match the report and certificate.

The geometric checker uses exact segment intersections and point-in-triangle tests, a different construction from the original polygon-clipping verifier. For two convex triangles, the vertices of their intersection consist of contained original vertices and edge intersection points. Comparing these candidates with the prescribed common simplex therefore checks the whole intersection, including collinear edge overlaps and boundary contacts.

The exact outcomes are:

- 18 distinct vertices, 28 positively oriented triangles, 45 edges, and 39 interior edges.
- All 378 triangle pairs have exactly their prescribed intersection: 246 empty intersections, 93 common-vertex intersections, and 39 common-edge intersections.
- All 18 vertex links have the required connected cycle or path form.
- The triangle adjacency graph is connected; the boundary is one simple cycle on Q_0,...,Q_5; V−E+T=1.
- O_0,...,O_5 and I_0,I_2,I_4 have degree six. I_1,I_3,I_5 have degree four. The Q vertices are boundary vertices.

This certifies a full embedded conforming disk, not just positive individual triangle areas or a combinatorial incidence list.

### Reduced matrix and signed balance

The independent fan order is obtained by an exact polar-angle comparator, rather than the original triangle-link traversal. For each even interior fan it computes

r_(v,i)=(-1)^i det(d_(i-1),d_(i+1))/(a_(i-1)a_i),

and the local jet form

H_v=(sum r_(v,i)) f_v + (1/2)(sum r_(v,i)d_i)·g_v.

All 540 entries of R and all 648 entries of H match the certificate under the exact nonzero row scalings forced by the different fan starting points. All twelve interior rows are nonzero. Exactly 27 columns are active, each with two nonzero entries; the other 18 columns vanish. The active graph is connected, so all twelve rows constitute one closed component.

The exact ranks are

rank R=rank [R H]=12,    rank sign(R)=11.

Under the certificate's fan convention, its displayed vector

(1,-1,-1,-1,-1,1,1,1,-1,1,-1,1)

annihilates sign(R) on the left and has no zero coordinate. This proves positive sign product around every active cycle. The connected active graph has cycle-space dimension 27−12+1=16, so the statement concerns all its cycles, not only one selected triangle.

In the independent fan normalization, the three ratios for O_0→O_1→I_1→O_0 are

4575/8239,  −977/688,  −153/563.

Their product is exactly

683875575/3191327216>0,   683875575/3191327216≠1.

Changing row normalizations changes individual displayed ratios but cancels from their cycle product. Thus the example is genuinely sign-balanced and magnitude-unbalanced, and cannot be a quartic counterexample.

### Independent full Bernstein system

The audit separately constructs the degree-four Bernstein coefficient functionals for all triangles. Corner coefficients are prescribed by the vertex jets; edge-middle coefficients are shared; the three remaining coefficients of each triangle are independent. There are 45+3·28=129 unknown remaining coefficients and 54 prescribed-jet columns.

For each of the 39 interior edges it evaluates the difference of normal derivatives at parameters 1/4 and 3/4, rather than the construction verifier's 1/3 and 2/3. A cubic normal-derivative difference whose endpoint values vanish is determined by its two independent interior samples. The following identities and ranks hold exactly:

- 195 edge-trace evaluations vanish in every coefficient and jet column.
- 78 endpoint normal-derivative evaluations vanish.
- All 39 pairs of interior derivative equations are related to the complete two-equation Bernstein residual system by an invertible exact 2×2 change of equations.
- The remaining-coefficient matrix has shape 78×129 and rank 78.
- Adjoining all 54 jet columns leaves rank 78.

An exact nonzero 78×78 pivot minor is given in [FINITE_AUDIT_CERTIFICATE.json](FINITE_AUDIT_CERTIFICATE.json), with its row and column conventions specified in [REPRODUCTION.md](REPRODUCTION.md). Hence arbitrary prescribed vertex jets are attainable on this fixed mesh. The full calculation independently corroborates the reduced rank conclusion without relying on floating-point tolerance or an optional dimension formula.

## 3. Exact threefold-family exclusion

### The necessary geometric domain

Use the report's twelve core coordinates and the same face list. With r,e,b as its three radial parameters, the strict turn at O_1 has determinant 2r−1. Four positively oriented annulus faces have doubled areas

r−b,  r(1−e),  b(1−e),  e(r−b).

Consequently every admissible convex-core member necessarily satisfies

r>1/2,   0<e<1,   0<b<r.

The implication is ordered correctly: the turn first gives r>0; the second area then gives e<1; the third gives b>0; the first gives b<r; and the fourth gives e>0. These inequalities are used only as necessary conditions. No claim that they alone characterize all conforming full disks is required.

### Why the normalized edge equations are legitimate

For an oriented core edge v→w, let x lie on its left and y on its right. In the two adjacent vertex fans,

det(y−v,x−v)=det(x−y,v−y),

det(x−w,y−w)=−det(x−y,w−y).

The two denominator area products agree. In a face-checkerboard coloring, the two incident triangles have opposite colors. The alternating fan sign divided by the color of the face on its left is a single sign q_v at vertex v. Absorbing this sign into the dependency coordinate, k_v=q_v z_v, transforms the edge dependency into

k_v det(x−y,v−y)+k_w det(x−y,w−y)=0.

The audit checks both determinant identities symbolically and checks this normalization along every active edge of the rational example. On the family the even-valence full triangulated disk is face-checkerboard-colorable; equivalently its core coloring extends compatibly across the required boundary triangles. There is no unmentioned geometric division that could fail at an admissible parameter value.

If the full support were closed and balanced, its active graph would be connected with every active coefficient nonzero, making the dependency space one-dimensional. The map ρ(x,y)=(−y,x−y) has order three, determinant one, and preserves the triangulation. An odd-order action cannot interchange the two checkerboard colors. It therefore acts on the one-dimensional real normalized dependency space by a real scalar λ with λ³=1, which forces λ=1.

The weights must consequently be constant on the four rotation orbits. Normalize them to 1,s,t,u on O_even,O_odd,I_even,I_odd, respectively, with all four weights nonzero.

### The contradiction

Direct determinant reconstruction gives, on (O_1,I_1), (I_0,I_1), and (O_1,I_2),

F_1=u[b(e+1)−e]+s[e(r−1)+r],

F_2=u[b(e+1)−e]+e(e−1)t,

F_3=b(1−e)t+(b−r)s.

The exact polynomial identity is

bF_1−bF_2−eF_3=s[r(eb+b+e)−2eb].

Balanced edges would set all three F_i to zero. Since s,e,b,r are nonzero, this requires

2/r=1+1/e+1/b.

But the strictly positive identity

1+1/e+1/b−(2+1/r)=(1−e)/e+(r−b)/(br)>0

would then imply 1/r>2, or r<1/2. This contradicts r>1/2. All equalities were verified symbolically over exact rational polynomial expressions; the strict inequalities follow from the stated geometric domain.

### Proper components cannot evade the argument

The only possible original degree-four interior vertices are I_1,I_3,I_5. Any closed component needs at least three nonsingular degree-four original interior vertices by the accepted support theorem. If any of these three vertices is singular, no closed component can exist. Otherwise a closed component must contain all three.

A nonsingular degree-four vertex in a closed component has its full four-neighbor star in that component. Its alternative zero pattern would leave a local line segment, ruled out by the accepted convex induced-support theorem. The three neighbor sets are

{O_0,O_1,I_0,I_2}, {O_2,O_3,I_2,I_4}, {O_4,O_5,I_4,I_0}.

Together with I_1,I_3,I_5, these cover all twelve core vertices. Thus any possible closed component is the full support already excluded from balance. Every other component has an incident one-entry column and contributes no left dependency. It follows that R has full row rank throughout the admissible family, and therefore arbitrary quartic jets are attainable there.

## 4. Reproduction and limits

The independent verification uses exact rational arithmetic, a separate geometry algorithm, a separate fan ordering, and different interior derivative sample points. All rational and symbolic checks pass. Negative controls distinguish altered geometry, matrix entries, jet entries, sign data, rank claims, cycle claims, and symbolic forms. These checks support the proofs above and do not replace their geometric and all-parameter arguments.

The complete authored [construction certificate](SECOND_PASS_CERTIFICATE.json) has SHA-256 7190bf1cbb515201a8b64e2bd20bb2465559bf6a44eab86cef6161b331769e14. The exact independently computed outcomes, row scalings, ray parameters, and nonzero full-system minor are in [FINITE_AUDIT_CERTIFICATE.json](FINITE_AUDIT_CERTIFICATE.json). [REPRODUCTION.md](REPRODUCTION.md) fixes the conventions for independently checking them. [CONTENT_MANIFEST.json](CONTENT_MANIFEST.json) identifies all public edition files. File identity is separate from mathematical validity.

The public proof and audit make only editorial changes to the accepted manuscripts: links and certificate conventions are added, and implementation and preservation descriptions are omitted. No mathematical correction was needed. No general nonexistence conclusion or arbitrary nonsymmetric perturbation claim follows from numerical searches, approaching degeneracy, or a nonzero terminal residual.

The accepted progress is a strict exterior-feasibility restriction, an exact limit on sign-only reasoning, and a larger exact excluded family. Existence or impossibility of a genuinely cycle-balanced closed support on an arbitrary admissible mesh remains beyond these results.
