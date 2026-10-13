# Exact verification of Qiu's cubic vertex interpolation counterexample

## Result and attribution

The fixed triangulation defined in Junkai Qiu, *A counterexample to vertex interpolation by planar C1 cubic splines*, [arXiv:2609.06364v1](https://arxiv.org/abs/2609.06364v1), has a nonsurjective vertex-evaluation map for the full space of globally C1 piecewise polynomials of total degree at most three. This note independently verifies Qiu's construction and arithmetic. The example and obstruction are Qiu's; no new counterexample or priority claim is made here.

The reconstructed triangulation has 41 vertices, 56 triangles, 96 edges, 24 boundary vertices, and 72 interior edges. Its spline space has dimension 107, and the vertex-evaluation map has rank 40. Consequently its attainable value vectors are exactly the following hyperplane, using Qiu's labels:

\[
-756f_O+11\sum_{j=0}^{3}f_{A_{2j}}+864\sum_{j=0}^{3}f_{A_{2j+1}}-343\sum_{i=0}^{7}f_{U_i}=0. \tag{1}
\]

Prescribing one at O and zero at the other 40 vertices contradicts (1). Boundary values are included among those data. Gradients remain free. No triangle is subdivided or moved, and no boundary conditions are added.

This resolves the cubic assertion in Alfeld's 2015 report, printed p.1146 item16, equivalently Conjecture4 in the expanded 2016 article. The separate quartic value-and-gradient assertion is outside this conclusion.

## Geometric validity

The source's rational coordinates and incidence patterns were transcribed from its main PDF, Table1 and equations(7)–(8), rather than taken from executable author code. This verification refers to that published specification; it does not redistribute a source coordinate or triangle array.

Here is an exact geometric test with sufficient, rather than merely necessary, conditions. For each pair of nondegenerate triangles, list (a) vertices of either triangle contained in the other and (b) intersections of pairs of their closed edges, including endpoints of collinear overlaps. A nonempty intersection of two convex polygons has an extreme point in this list: an extreme point is either an original polygon vertex or the intersection of two supporting edge segments. The convex hull of the list is the whole intersection. Checking that every listed point belongs to the shared face therefore checks the entire intersection. If no face is shared, the list must be empty. If one vertex is shared, every point must equal that vertex. If an edge is shared, every point must lie on that closed edge. This also rejects touching at unlisted vertices, hanging vertices, improper crossings, overlapping triangles, and nested triangles.

All 1,540 unordered pairs pass this test with rational predicates. All 56 oriented doubled areas are positive, with minimum 1/2016. All 41 coordinates are distinct. The 96 edge incidence counts are one or two. The 24 edges with one incident triangle form one connected simple cycle. Every boundary vertex link is a connected path, and every other vertex link is a connected cycle. The triangle adjacency graph is connected. These checks prove that the geometric realization is a connected compact triangulated 2-manifold with one boundary component. It lies embedded in the oriented plane. Its Euler characteristic is

\[
41-96+56=1.
\]

A connected compact orientable surface with one boundary component has Euler characteristic 1−2g; hence g=0 and this realization is a disk. Because its boundary is a finite simple union of straight segments, it is a polygonal disk. This establishes the model required by Alfeld, with no appeal to a visually plausible plot.

The graph induced by the 17 interior vertices is also checked independently: it is connected with 16 edges and maximum degree eight. All interior vertices have more than two incident direction lines: eight at O and three at each of the remaining sixteen. In particular there is no singular four-valent interior vertex.

## Complete parameterization of the cubic space

For a triangle T with vertices a,b,c, use its three values, six Cartesian first derivatives, and its barycenter value as ten scalar degrees of freedom. These determine a unique cubic. Indeed, if all ten data vanish, the restriction to any edge is a univariate cubic with zero values and tangential derivatives at its two endpoints, so the edge restriction vanishes. A polynomial that vanishes on all three supporting lines is divisible by the product of their affine equations. In degree at most three it is a constant multiple of the barycentric bubble λaλbλc. Its barycenter value, where the bubble is nonzero, forces that constant to vanish. The ten-dimensional dimension count gives existence and uniqueness.

Assign one common value and gradient to each global vertex, and one barycenter value to each triangle. This gives

\[
3\cdot41+56=179
\]

parameters. Adjacent pieces agree in value on an entire edge because the four endpoint Hermite conditions determine the cubic trace. They also have equal gradients at the edge endpoints. The difference of their normal derivatives on the edge is a univariate polynomial of degree at most two with zeros at both endpoints. It is identically zero exactly when it also vanishes at the midpoint. Since the tangential derivative already agrees, imposing this one scalar midpoint equation for every interior edge is equivalent to C1 agreement across all edges.

There are no extra conditions at a vertex. All incident pieces share its assigned value and gradient; their polynomial Taylor remainders are O(|x−v|²), and their gradient differences from the assigned jet are O(|x−v|), uniformly over the finitely many incident triangles. This proves differentiability and continuity of the gradient there, including at boundary vertices. Conversely every spline supplies precisely these data. Therefore the kernel of the resulting matrix H is linearly isomorphic to the entire intended spline space.

## Reconstructing H independently

Fix the vertex order O followed by the families A,U,W,B,C, each in increasing index, and the source's sector-major triangle order. The columns of H consist of 41 values, 82 gradient coordinates in vertex order, and 56 barycenter values. Interior edges are lexicographically sorted as unordered pairs of their string labels. Orient each edge i→j by that order and identify the left and right triangles geometrically.

On each triangle, evaluate the ten Cartesian monomials of total degree at most three and their x and y derivatives at its three vertices, and evaluate the monomials at the barycenter. Invert this 10×10 rational interpolation matrix. The inverse is checked by exact multiplication against the identity. At the midpoint m of edge ij, set d=pj−pi and n=(−dy,dx). Evaluate n·∇p(m) in the two incident triangle bases and subtract right from left. Insert the resulting local coefficients into the shared global columns. This produces H∈Q^(72×179), without using an edge smoothness formula to assemble it.

For an additional cross-check, form a second matrix B using central Bernstein coefficients qT rather than barycenter values hT. Write [ijk]=det(pj−pi,pk−pi), and choose positive triangle orientations (i,j,k) and (j,i,l). Put α=[ijk], β=[jil], aij=−[jkl]/(αβ), and aji=−[ilk]/(αβ). The edge row of B is

\[
q_T/\alpha+q_{T'}/\beta+a_{ij}(f_i+g_i\cdot(p_j-p_i)/3)+a_{ji}(f_j+g_j\cdot(p_i-p_j)/3)=0. \tag{2}
\]

One can derive (2) directly from divisibility of the difference of adjacent cubics by the square of the edge equation. Equivalently, evaluate their polarized cubic forms on (pi,pj,pl) and use the barycentric coordinates of pl. The endpoint coefficients are fi+gi·(pj−pi)/3 and fj+gj·(pi−pj)/3. Expanding pl in the left triangle gives (2), with the displayed determinant signs.

The local change of parameters is

\[
q_T=\frac92h_T-\frac76(f_a+f_b+f_c)-\frac16\sum_{v\in\{a,b,c\}}g_v\cdot\left(\sum_{w\ne v}p_w-2p_v\right). \tag{3}
\]

Formula(3) follows by evaluating the cubic Bernstein expansion at three equal barycentric coordinates. Its hT coefficient is nonzero, so it is an invertible global change of variables. Every row of the independently assembled H is checked to equal the corresponding transformed B row multiplied by 3|d|²/2. This checks all 179 coefficients of each of the 72 equations, including orientation, gradient scaling, and the distinction between a barycenter value and a central Bernstein coefficient.

## An exact left certificate

Use the rational edge multipliers r from Qiu's Table2. They are supported on exactly the 72 interior edges. Compute, at every triangle and every vertex,

\[
F_T=\sum_{e\subset T}r_e,\qquad
R_i=\sum_j a_{ij}r_{ij},\qquad
G_i=\sum_j a_{ij}r_{ij}(p_j-p_i),
\]

where boundary multipliers are zero. Direct rational summation gives all 56 face sums FT=0 and all 82 components of the 41 vectors Gi=0. In particular the boundary-vertex gradient sums are checked, rather than omitted. The remaining values are

\[
R_O=-56,\quad R_{A_{2j}}=22/27,\quad R_{A_{2j+1}}=64,\quad R_{U_i}=-686/27,
\]

and R vanishes at every W,B,C vertex. Summing (2) with multipliers r eliminates the free parameters. Multiplication by 27/2 gives (1).

There is also a Cartesian certificate avoiding reliance on an implementation of Bernstein coordinates. For each oriented edge row define

\[
\lambda_e=\frac{2r_e}{3|p_j-p_i|^2}.
\]

The separately assembled matrix satisfies, by exact rational multiplication,

\[
\lambda^TH=(R^T,0_{138}). \tag{4}
\]

Thus Hx=0 implies R·f=0, and the incompatible datum yields −56=0. The rescaled integer contradiction in (1) is −756=0. Both forms are identical. A separate check confirms that R annihilates every global monomial of degree at most three.

## Exact ranks and dimension

Let H0 be the 72×138 matrix obtained by deleting the 41 value columns. Certificate(4) gives a nonzero rational vector in the left kernel of H0, so rank(H0)≤71. H has only 72 rows, so rank(H)≤72.

The retained certificates specify a 72×72 minor of H and a 71×71 minor of H0. Exact arithmetic modulo the primes 1,000,000,007 and 1,000,000,009 yields these nonzero determinants, with rows and columns in the certificate order:

- Modulo 1,000,000,007: 445,644,816 for H; 862,868,465 for H0.
- Modulo 1,000,000,009: 141,710,094 for H; 897,614,159 for H0.

All denominators are invertible in these fields. A nonzero reduction of a rational determinant proves that determinant is nonzero over Q, so the ranks are respectively at least 72 and 71. Combined with the upper bounds, this proves rank(H)=72 and rank(H0)=71 exactly. Rational row reduction independently returns the same ranks. A standard-library-only checker replays the exact left identity and the named minor determinants from the retained matrix and certificates.

Rank-nullity gives dim ker(H)=179−72=107. The kernel of vertex evaluation within ker(H) is isomorphic to ker(H0), which has dimension 138−71=67. Therefore rank(EV)=107−67=40. Since R is nonzero, its kernel is also 40-dimensional; the already-proved inclusion EV(S)⊆ker(R) is equality.

The dimension equals the classical lower bound 3VB+2VI+1+σ, because VB=24, VI=17, and σ=0. No failure of that dimension bound is asserted. This computation shows why ample spline-space dimension alone does not guarantee independent vertex evaluations.

## Boundaries of the conclusion

The mathematical result is the verified negative answer to universal cubic vertex interpolation on this exact fixed conforming triangulation. It does not establish minimality of the construction, a statement about arbitrary perturbations, a counterexample to the cubic dimension conjecture, or a resolution of quartic Hermite interpolation. The latter requires a separate proof or counterexample.

Sources: [Qiu's versioned preprint](https://arxiv.org/abs/2609.06364v1); [Alfeld's 2015 institute report](https://publications.mfo.de/handle/mfo/3469); [Alfeld's expanded article](https://doi.org/10.1016/j.cagd.2015.11.007).
