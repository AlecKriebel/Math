# Independent mathematical audit of Qiu's cubic spline counterexample

## Decision, attribution, and scope

**Accepted:** the stated fixed triangulation is a conforming nondegenerate straight-line triangulation of a polygonal disk, and its full space of globally continuously differentiable piecewise polynomials of total degree at most three does not interpolate arbitrary vertex values. Its spline-space dimension is 107 and its vertex-value map has rank 40.

The example, edge-multiplier certificate, and counterexample theorem are credited to Junkai Qiu, *A counterexample to vertex interpolation by planar C1 cubic splines*, [arXiv:2609.06364v1](https://arxiv.org/abs/2609.06364v1), Theorem 1. This audit is an independent verification of that construction, not a new counterexample or a priority claim. The checked arXiv record identifies a 6 September 2026 submission, lists v1, and displays no journal reference. That observation does not establish whether the work has received review elsewhere.

The result is a negative answer to the cubic assertion in Peter Alfeld's [Oberwolfach Report 21/2015 contribution](https://publications.mfo.de/handle/mfo/3469), printed p.1146, item 16, and to Conjecture 4 in the [expanded CAGD article](https://doi.org/10.1016/j.cagd.2015.11.007). The latter's [author-hosted manuscript](https://peteralfeld.github.io/home/mfo.pdf), Definition 1 and sections 9–10, supplies the precise disk model and distinguishes the questions.

**Not concluded:** the separate quartic value-and-gradient question. Neither the cubic obstruction nor this audit establishes a quartic obstruction, and the bundled pair of questions must not be reported as completely resolved on this basis. No conclusion about minimality, arbitrary perturbations, or path-shaped interior graphs is included.

## 1. What was independently checked

The audit read the source construction and compared the mathematical input against Qiu's displayed coordinate specification, rotation rule, triangles, and edge-multiplier rule. The coordinate table and triangle list were visually inspected in the PDF, as was the multiplier table. No author-supplied program was executed or imported.

The separate verification used only Python's standard library and exact rational arithmetic. It did not invoke the reconstruction program. Its principal independent methods were:

1. Rational half-plane clipping of each triangle by each other triangle, instead of a vertex/segment intersection-list test.
2. Explicit analytic Bernstein basis coefficients and differentiation, instead of inversion of Cartesian monomial interpolation matrices.
3. Fresh exact modular elimination and nonzero minors over different prime fields.
4. Direct multiplication of the resulting rational matrix by the proposed left witness, together with every triangle and vertex cancellation.

The independently assembled matrix agrees in all **12,888 entries** with the reviewed 72-by-179 Cartesian matrix. All 72 oriented edge records and the entire left witness agree. The reported original minors were also recomputed on the independent matrix.

These checks establish the result for the specified finite source construction. The published mathematical discussion is not a standalone distribution of the source's coordinate arrays, triangle arrays, or full matrix certificates: numerical reproduction requires obtaining the mathematical specification from the cited preprint. The audit does not claim that omitted data are embedded in this report.

## 2. Original hypotheses and geometric audit

The intended space is

\[
S^1_3(\Delta)=\{s\in C^1(\Omega):s|_T\in\mathcal P_3\text{ for every }T\in\Delta\},
\]

where \(\mathcal P_3\) has total degree at most three. The finite straight-line triangulation is fixed. Its triangles must be genuine positive-area triangles and have intersections only along common faces. Its union must be a polygonal disk. Every vertex, including every boundary vertex, is part of the requested scalar interpolation. Gradients are unrestricted, and no homogeneous boundary conditions, subdivision, vertex movement, or extra boundary equations are permitted.

All these hypotheses were checked, rather than inferred from a picture. The reconstruction has:

- 41 distinct vertices and 56 positively oriented triangles;
- minimum positive doubled area \(1/2016\);
- 96 edges, of which 24 are boundary edges and 72 are interior edges;
- 24 boundary vertices and 17 interior vertices.

For two triangles, start with the first closed triangle and successively intersect it with the three closed half-planes bounded by the oriented edges of the second. Segment/line intersections in this clipping are computed as rational affine combinations. The result is exactly the intersection of the two convex polygons, also when it degenerates to a segment or a point. The resulting vertices were checked against the common face of the two abstract triangles. Among all \(\binom{56}{2}=1540\) pairs, the counts were:

- 1,228 pairs with no common vertex and empty geometric intersection;
- 240 pairs meeting exactly in their common vertex;
- 72 pairs meeting exactly in their common edge.

This rules out improper touching, crossings, nesting, area overlaps, hanging vertices, and unlisted shared edges. It is stronger than merely checking that total area or Euler characteristic has the expected value.

Each edge has one or two incident triangles. The boundary edges form one connected cycle, all boundary-vertex links are connected paths, and all 17 interior-vertex links are connected cycles. The triangle-adjacency graph is connected. Thus the embedded realization is a compact connected planar triangulated 2-manifold with one boundary component. Its Euler characteristic is

\[
41-96+56=1.
\]

It is orientable because it is embedded in the oriented plane. The classification of compact connected orientable surfaces with boundary gives genus zero and hence a disk. Its finite simple straight-line boundary makes it a polygonal disk, including any permitted non-strict corner angles.

As a supplementary structural check, the interior-vertex graph is a connected 17-vertex, 16-edge tree with maximum degree eight. The incident direction-line counts are eight at the central vertex and three at every other interior vertex. In particular, none is a four-valent vertex with only two direction lines. This last check is relevant only to the stated comparison with the classical cubic dimension bound; it is not needed for nonsurjectivity.

## 3. The parameterization is the full cubic space

For a nondegenerate triangle \(T=(a,b,c)\), prescribe the three vertex values, both Cartesian derivatives at all three vertices, and one value at its barycenter. These ten linear functionals are unisolvent on the ten-dimensional space \(\mathcal P_3\).

To prove this directly, suppose all ten vanish. On each edge the restriction is a univariate cubic whose value and tangential derivative vanish at both endpoints, so its trace is zero. The polynomial is divisible by each of the three distinct edge-line equations. Hence it is a scalar multiple of \(\lambda_a\lambda_b\lambda_c\), where the \(\lambda\)'s are barycentric coordinates. At the barycenter this product is \(1/27\), so the last datum forces the scalar to be zero. Injectivity and equal finite dimensions prove bijectivity.

There are consequently \(3V+F=179\) global parameters: one common scalar value and two common Cartesian derivatives at each of the 41 vertices, plus one barycenter value per triangle. No parameter is removed at a boundary vertex.

The common vertex jets make the two cubic traces on an interior edge identical: their four endpoint Hermite data agree. Tangential derivatives therefore agree along the edge. The jump of the normal derivative is a polynomial of degree at most two in the edge parameter and vanishes at both endpoints. Such a polynomial is a scalar multiple of \(t(1-t)\); it vanishes identically if and only if it vanishes at the midpoint. Thus one midpoint normal-derivative equation per interior edge is both necessary and sufficient.

There is no additional hidden vertex condition. Each incident polynomial has the same linear Taylor polynomial at the vertex, with remainder \(O(\lVert x-v\rVert^2)\) and gradient remainder \(O(\lVert x-v\rVert)\). The finite collection of triangles gives uniform bounds, so the function is differentiable with continuous gradient at the vertex. This applies to boundary vertices in the intended piecewise definition as well. Conversely, every spline in the intended space supplies these same common jets and barycenter values. Therefore the kernel of the resulting continuity matrix is linearly isomorphic to the **entire** intended spline space, not to a more restrictive subspace.

## 4. Independent basis construction and the barycenter issue

The analytic Bernstein construction gives the local polynomial directly. Its endpoint coefficient at \(a\) is \(f_a\), and the coefficient adjacent to \(a\) along the edge toward \(b\) is

\[
b_{210}=f_a+\tfrac13g_a\cdot(p_b-p_a).
\]

The analogous six adjacent-edge coefficients, together with the three vertex coefficients, are determined by the nine jet data. Let \(q_T=b_{111}\) be the remaining **central Bernstein coefficient**, and let \(h_T\) be the **barycenter value**. These are different quantities.

At the barycenter every degree-three Bernstein monomial has its multinomial coefficient divided by 27. Summing the three vertex terms, the six edge-adjacent terms, and the center term gives

\[
27h_T=7(f_a+f_b+f_c)
+\sum_{v\in T}g_v\cdot\left(\sum_{w\in T\setminus\{v\}}p_w-2p_v\right)+6q_T.
\]

Therefore

\[
q_T=\tfrac92 h_T-\tfrac76\sum_{v\in T}f_v
-\tfrac16\sum_{v\in T}g_v\cdot\left(\sum_{w\in T\setminus\{v\}}p_w-2p_v\right).
\tag{A}
\]

The coefficient of \(h_T\) is nonzero. Applied triangle by triangle, (A) is an invertible change of global parameters. This derivation independently confirms the reviewed conversion formula and prevents accidental substitution of center coefficients for barycenter values.

The audit differentiated the resulting normalized Bernstein polynomials using their affine barycentric gradients. For every triangle, it checked that the ten local basis functionals reproduce exactly the designated three values, six derivatives, and barycenter value. For every edge, it checked the value traces at five points, tangential derivative traces at those points, both Cartesian gradient components at both endpoints, and the normal-derivative jump at one-third and two-thirds of the edge. Both latter jumps equal \(8/9\) of the midpoint jump, as required by \(t(1-t)\). All these checks are identities of rational linear forms in the 179 parameters.

## 5. Orientation and the smoothness identity

For an oriented interior edge \(i\to j\), write the left and right triangles as \((i,j,k)\) and \((j,i,l)\), both positively oriented. Use

\[
[abc]=\det(p_b-p_a,p_c-p_a),\quad
\alpha=[ijk]>0,\quad\beta=[jil]>0,
\]

and

\[
a_{ij}=-\frac{[jkl]}{\alpha\beta},\qquad
a_{ji}=-\frac{[ilk]}{\alpha\beta}.
\]

The Bernstein smoothness residual is

\[
B_e=\frac{q_T}{\alpha}+\frac{q_{T'}}{\beta}
+a_{ij}\left(f_i+\tfrac13g_i\cdot(p_j-p_i)\right)
+a_{ji}\left(f_j+\tfrac13g_j\cdot(p_i-p_j)\right).
\tag{B}
\]

One derivation uses \(C^1\) continuity to write the difference of adjacent cubic pieces as the square of an edge-line equation times an affine polynomial. The blossom of that difference vanishes when two arguments are the edge endpoints. Expanding the opposite vertex of the right triangle in the left triangle's affine coordinates then gives (B), with exactly the displayed signs. The affine coordinates are \([jkl]/\alpha,[ilk]/\alpha,-\beta/\alpha\), and sum to one.

Let \(d=p_j-p_i\), let \(n=(-d_y,d_x)\), and define \(H_e\) to be the left-minus-right derivative in direction \(n\) at the edge midpoint. The audit verifies coefficient by coefficient that

\[
H_e=\frac{3\lVert d\rVert^2}{2}\,B_e,
\tag{C}
\]

after applying (A). The factor can also be read directly from the central Bernstein basis function \(6\lambda_i\lambda_j\lambda_k\): its midpoint normal derivative on the left is \(3\lVert d\rVert^2/(2\alpha)\), and subtracting the right derivative contributes \(3\lVert d\rVert^2/(2\beta)\). Every endpoint coefficient was independently checked as well.

Reversing the oriented edge exchanges its left and right triangles and reverses its normal, so the chosen jump functional is unchanged. Recomputing the determinant formulas under this reversal exchanges the endpoint weights correctly. The audit explicitly checked both transformations on all 72 edges. There is no unit-normal assumption: changing a nonzero normal normalization merely scales that row, and the witness must be scaled accordingly.

## 6. The exact obstruction includes every boundary cancellation

Let \(r_e\) be Qiu's source edge multipliers, extended by zero on boundary edges. Define

\[
F_T=\sum_{e\subset T}r_e,\quad
R_i=\sum_j a_{ij}r_{ij},\quad
G_i=\sum_j a_{ij}r_{ij}(p_j-p_i).
\]

The sums over vertices range over **all** vertices. Multiplying (B) by \(r_e\) and adding yields

\[
0=\sum_T\frac{q_T}{[T]}F_T+\sum_iR_if_i+\tfrac13\sum_iG_i\cdot g_i.
\tag{D}
\]

Here every triangle uses the same positive doubled area \([T]\) no matter which of its edges contributes. The zero weights on boundary edges allow the complete three-edge face sum to be used without adding boundary constraints.

The audit independently recalculated the endpoint weights from coordinates and adjacency, without taking the source's determinant or endpoint-weight tables as assumptions. It found:

- all 56 face sums vanish;
- both components of every one of the 41 vertex-gradient sums vanish;
- in particular all 48 gradient components at the 24 boundary vertices vanish;
- the remaining value coefficients are

\[
R_O=-56,\quad R_{A_{2j}}=\frac{22}{27},\quad
R_{A_{2j+1}}=64,\quad R_{U_i}=-\frac{686}{27},
\]

with all coefficients at the \(W,B,C\) families zero.

This establishes the nonzero relation directly from (D). Independently of that summation, define

\[
\lambda_e=\frac{2r_e}{3\lVert p_j-p_i\rVert^2}.
\]

On the separately assembled rational matrix the full identity

\[
\lambda^TH=(R^T,0_{138})
\tag{E}
\]

was checked exactly. All non-value columns, including every boundary derivative and all barycenter parameters, disappear. As a sanity check, \(R\) annihilates the values of each of the ten global monomials of total degree at most three; those ten global polynomials also satisfy every row of \(H\).

Multiplication by \(27/2\) gives the accepted integer obstruction:

\[
-756f(O)+11\sum_{j=0}^{3}f(A_{2j})
+864\sum_{j=0}^{3}f(A_{2j+1})
-343\sum_{i=0}^{7}f(U_i)=0.
\tag{F}
\]

The prescribed value vector equal to one at \(O\) and zero at every other vertex is legitimate in Alfeld's question. It gives \(-756\) on the left of (F). Consequently it has no interpolant. Neither matrix ranks nor a generic-position assumption are needed for this contradiction.

## 7. Exact ranks, real coefficients, and the attainable hyperplane

Let \(H_0\) be the 72-by-138 matrix obtained by removing all 41 value columns from \(H\). Equation (E) gives a nonzero left-null vector of \(H_0\), so its rational and real ranks are at most 71. The rank of \(H\) is at most its 72 rows.

The audit found independent nonzero 72-by-72 and 71-by-71 minors over each of two prime fields. Both primes were verified by integer trial division and every rational denominator was inverted in the field. In the audit's retained row and column orders, their determinant residues are:

| Prime | Minor of H | Minor of H0 |
| --- | ---: | ---: |
| 65,537 | 38,664 | 62,520 |
| 1,000,003 | 625,292 | 700,786 |

A nonzero modular reduction of a rational determinant whose denominators are invertible proves that the rational determinant is nonzero. Together with the exact upper bounds this proves

\[
\operatorname{rank}H=72,\qquad\operatorname{rank}H_0=71.
\]

The same ranks hold over the reals: rational minors give the lower bounds and the rational identities remain valid over the reals. This is an exact rank proof, not an inference from a numerical tolerance. The audit additionally recalculated the reviewed original minors at primes 1,000,000,007 and 1,000,000,009 and obtained their stated residues unchanged.

Rank-nullity now gives

\[
\dim S^1_3=179-72=107.
\]

The kernel of the value map on \(\ker H\) consists precisely of vectors \((0,z)\) with \(H_0z=0\), so it has dimension \(138-71=67\). Hence

\[
\operatorname{rank}E_V=107-67=40.
\]

The nonzero functional \(R\) has a 40-dimensional kernel in \(\mathbb R^{41}\). Equation (E) puts the image of the value map inside it; equal dimensions show that the image is **exactly** this hyperplane. There are no additional independent linear restrictions on the values for this mesh.

The computed dimension equals \(3\cdot24+2\cdot17+1=107\), the classical lower bound with zero singular vertices discussed in Alfeld's source. Thus this example does not refute the distinct cubic dimension conjecture. A spline-space dimension well above the vertex count does not force its particular vertex evaluations to be independent.

## 8. Adversarial checks and acceptance limits

The independent program uses explicit runtime validation rather than removable assertions. Normal, optimized, and doubly optimized Python execution produced byte-identical mathematical output. Separate tests checked clipping in disjoint, vertex-touching, edge-sharing, and genuine crossing configurations. Coincident input vertices were rejected, an altered edge multiplier was rejected through a nonzero face sum, and a changed retained matrix coefficient was rejected by independent reconstruction.

The acceptance is of the exact credited cubic construction and the stated finite proof, including its geometric hypotheses, full-space parameterization, orientation convention, boundary cancellations, contradiction, and rank conclusion. It is not an audit of every theorem in the cited sources, a certification of unrelated software, or evidence of a complete resolution of the distinct quartic assertion. No new mathematical discovery is claimed.
