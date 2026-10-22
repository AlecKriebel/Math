# Independent acceptance of the quartic reduction and partial positive results

## Decision and scope

**Accepted.** The exact Bernstein–Bézier reduction, weighted support criterion, Qiu-mesh quartic surjectivity, symbolic 18-vertex family result, convex induced-support theorem, and its Euler corollary are mathematically valid in the stated model. No substantive mathematical correction is required. The finite-simplex shortest-path argument benefits from the precise simplex-label formulation supplied below; this needs no additional geometric hypothesis.

The model is a finite conforming straight-line triangulation of a polygonal disk, with nondegenerate triangles. Every mesh vertex, including boundary vertices, has independently prescribed value and both first derivatives. The requested interpolant is globally C1, of total degree at most four on each original triangle. No refinement, moved vertex, homogeneous boundary condition, or extra smoothness is allowed or assumed.

This acceptance concerns the already documented first substantive pass for row 1761 / problem 30002861 / OWR-13678-002. It is not another counted pass and does not determine an unknown earlier lifetime count. It establishes neither a general quartic counterexample nor universal quartic surjectivity. Qiu's cubic counterexample remains a separate credited result.

## 1. Independent verification of all Bernstein conditions

There are 15 degree-four Bernstein coefficients on a triangle. Its three vertex values and six directional first derivatives fix nine distinct coefficients. The remaining six are three edge-middle coefficients c220 and three interior coefficients c211, the latter indexed by the corner bearing exponent two. Using a single c220 for each mesh edge makes both adjacent polynomial edge traces identical. This includes the fixed first derivative coefficients at both ends of the edge.

For adjacent triangles (v,w,u) and (v,w,z), write z = alpha v + beta w + gamma u, with alpha + beta + gamma = 1. Because the triangles lie on opposite sides of the edge, gamma is nonzero and negative. The two residual Bernstein conditions are

L_v = t_(v,w,z),v - gamma t_(v,w,u),v - beta m_vw - alpha [f_v + g_v dot (w-v)/4] = 0,

L_w = t_(v,w,z),w - gamma t_(v,w,u),w - alpha m_vw - beta [f_w + g_w dot (v-w)/4] = 0.

An independent generic symbolic calculation verifies these conditions directly from polynomial derivatives. Apply an invertible affine change of coordinates taking v=(0,0), w=(1,0), u=(0,1), and z=(beta,gamma). Let p and q be the respective Bernstein polynomials with all prescribed corner coefficients substituted. Then

D_y(q-p)(x,0) = (12/gamma) x(1-x) [(1-x)L_v + x L_w].

Terms with transverse Bernstein exponent at least two make no contribution to this derivative and require no assumptions. The endpoint terms cancel using the common prescribed gradients. The displayed identity was verified symbolically with independent formal variables for both endpoint jets, edge middle coefficient, and four relevant interior coefficients.

It follows that the two residual equations are necessary and sufficient for transverse derivative agreement. Tangential derivatives already agree because the traces agree. Thus they give every C1 edge condition, with no missing middle equation and no superfluous smoothness requirement. On a finite conforming triangulation, polynomial gradients that agree on every shared edge are continuous across the whole closed disk in its one-sided boundary interpretation: incident triangles have the same limiting prescribed gradient at each vertex.

The full remaining-coefficient system therefore has 2 E_I equations and E + 3 T unknowns, precisely as stated in the first-pass report.

## 2. Fan elimination, boundary cases, and exact jet obstruction

At an interior vertex let d_i be the counterclockwise outgoing neighbor vectors and a_i = det(d_i,d_(i+1)) > 0. Consecutive angular gaps lie in (0,pi). Direct barycentric elimination gives

beta_i = det(d_(i-1),d_(i+1))/a_(i-1),

gamma_i = -a_i/a_(i-1),

alpha_i = 1-beta_i-gamma_i.

The corner equations are t_i - gamma_i t_(i-1) - beta_i m_i = alpha_i h_i, where h_i=f_v+g_v dot d_i/4. Their cyclic determinant is 1-product(gamma_i)=1-(-1)^n.

For odd n the system is invertible. For even n its nullity is exactly one: specifying one corner value determines all the others, and the final recursion has one redundant homogeneous condition. A left null vector is lambda_i=(-1)^i a_0/a_i. Its equation is

sum r_i m_i = H_v(f_v,g_v),

r_i=lambda_i beta_i,

H_v=-sum lambda_i alpha_i [f_v+g_v dot d_i/4].

At a boundary vertex the incident-triangle link is a path, including at a reentrant polygon corner. There are one fewer corner equations than corner unknowns. Forward recursion solves them for all edge-middle coefficients and prescribed jets. Boundary vertex data are unrestricted; no boundary compatibility equation was omitted.

An even row vanishes identically if and only if all d_(i-1),d_(i+1) are collinear. Distinct cyclic rays and positive triangle angles then force a four-star consisting of two opposite ray pairs. Conversely that singular four-star has zero row. Its right-hand side is identically zero because every first jet is realized by an affine polynomial, whose remaining Bernstein coefficients satisfy the exact equations. Discarding the singular zero equation is therefore legitimate.

The resulting system Rm=Hj is exactly equivalent to quartic Hermite interpolation. Accordingly arbitrary jets are attainable if and only if rank(R)=rank([R H]); full row rank of R is sufficient, but should not be confused with a necessary condition without the additional right-hand-side qualification.

The simplified moment form is also correct:

H_v = (sum r_i) f_v + (1/2)(sum r_i d_i) dot g_v.

For example, the edge-middle coefficient of the affine polynomial f_v+g_v dot (x-v) is f_v+(g_v dot d_i)/2. Substitution into the exact compatibility equation proves the identity for every first jet. Likewise the three second homogeneous moments vanish: sum r_i d_i d_i^T=0. A quadratic with zero first jet at v has c220=(d_i^T Q d_i)/12 when Q is its Hessian, giving an independent direct proof.

Each column of R has at most two nonzero entries. A one-entry column forces its vertex's left-nullspace coordinate to zero. A two-entry column vw propagates the ratio z_w=-(r_vw/r_wv)z_v. Therefore each connected active component contributes one left-nullspace dimension exactly when it has no incident one-entry column and every cycle-ratio product equals one. Otherwise it contributes zero. This also covers a component with no cycles: the cycle condition is then vacuous.

Rows of H use disjoint vertex-jet coordinates. Thus a nonzero supported dependency obstructs some prescribed jets exactly when at least one local H_v in its support is nonzero. If all local forms vanish, that dependency alone is harmless. A unit datum at a nonzero supported local coefficient gives an explicit incompatible jet assignment when the qualification holds. No external dimension theorem is needed for this exact criterion or for the accepted sufficient conditions below.

## 3. Independent exact computations and Qiu's mesh

The independent audit program does not import any first-pass construction or verification module. It orders vertex fans through oriented triangle links rather than the first-pass angular comparator, and constructs reduced rows from determinant formulas with a different nonzero row normalization.

For the unreduced check it directly differentiates all degree-four Bernstein basis polynomials. On every interior edge it evaluates the difference of normal derivatives at edge parameters 1/3 and 2/3. The endpoint normal derivative differences already vanish. Since the normal difference is a cubic, these two interior evaluations are sufficient after the two endpoint zeros. For every edge, an exact nonsingular 2-by-2 change of equations maps the displayed residual Bernstein equations to this independently evaluated system. All coefficient and prescribed-jet columns are compared, not just numerical solutions or ranks.

The retained Qiu input was checked as a conforming disk using exact rational triangle clipping, all 1,540 triangle-pair intersections, the 41 vertex links, one boundary cycle, connectedness, and Euler characteristic. It has 41 vertices, 56 triangles, 96 edges, 72 interior edges, and 24 boundary vertices. This independently repeats the geometric property needed by the quartic argument; source attribution remains to the cited primary preprint and its separately audited input transcription.

On this mesh the audit verifies:

- 360 exact edge-trace evaluations vanish identically in all remaining coefficients and prescribed jets.
- All 144 endpoint normal derivative evaluations agree.
- All 72 changes between the two interior derivative equations and the two Bernstein residuals are nonsingular.
- The independently evaluated remaining-coefficient matrix has shape 144 by 264 and exact rational rank 144.
- Adding every one of the 123 jet-coordinate columns leaves rank 144.
- The independently derived reduced matrix has shape 9 by 96 and rank 9; its augmentation also has rank 9.
- All 81 entries of the reported primitive 9-by-9 certificate match the independent matrix under exact nonzero row scalings.
- The reported determinant is exactly -233280 with its stated row and column ordering.

Thus Qiu's fixed cubic counterexample mesh admits all quartic vertex Hermite data. It is not a quartic counterexample.

Additional exact controls cover a single triangle, an odd three-star, a singular four-star, a nonsingular four-star without zero coefficients, a nonsingular four-star with two opposite zero coefficients, and a reentrant boundary fan. Three rational members of the 18-vertex family are checked using the same independent gradient-evaluation construction. In each case the full and reduced rank identities agree, including singular-row removal. These controls support implementation reliability; the general equivalence is proved algebraically in Sections 1–2.

## 4. The full 18-vertex family

The first-pass family is a valid conforming disk for every real t>1. Its inner and outer core hexagons are homothetic convex hexagons. The inner annulus is partitioned into six convex trapezoids, each split by its specified diagonal. The exterior six vertices are intersections of the appropriate extended neighboring core-side lines; they form the larger convex boundary hexagon and the twelve stated exterior-ring triangles partition the intervening annulus. The central four-triangle subdivision covers the inner hexagon. The positive doubled areas are 2, 6, 2(t-1), 2t(t-1), and 2t^2.

The independent symbolic calculation uses u=t-1>0. This makes all area signs and row-multiplier signs checkable from nonzero polynomial coefficients of one sign. It verifies the 12 retained row vertices, all 144 displayed minor entries under exact nonvanishing row scalings, and the determinant

27 t^3 (t-1)^13 (t^2+t-1).

Every factor is positive for t>1. The polynomial identity is exact and has no floating-point coefficients. The determinant remains a certificate for the entire parameter interval, rather than a conclusion extrapolated from sampled rational meshes.

There is also a particularly short independent cycle-imbalance certificate. Traverse the active triangle O_0 to O_1 to I_1 to O_0. In the displayed scaled matrix, the three propagation ratios multiply to

[-t/(t-1)] [t^3] [1/t^2] = -t^2/(t-1).

This is negative for every t>1, and hence cannot equal one. A vertex-row rescaling cancels around a cycle, so the witness applies to the original reduced coefficients as well. The whole connected 12-vertex support is closed but cycle-unbalanced. This independently corroborates the full-row-rank conclusion and exposes why closed support by itself is not an obstruction.

The three nonsingular degree-four interior vertices of this induced support are I_1, I_3, and I_5. They saturate the Euler bound established below.

## 5. Audit of the convex induced-support theorem

Let S be the vertices of one nonempty closed active component and K the full induced mesh complex on S. Cycle balance is not assumed in this section.

### 5.1 No missing induced edges

An edge joining two row vertices is an interior mesh edge. Let u and z be its opposite triangle vertices. The coefficient at endpoint v is zero exactly when u,v,z are collinear; the coefficient at the other endpoint w is zero exactly when u,w,z are collinear. Both cannot vanish: u and z are distinct and the two conditions would make an incident triangle degenerate.

If an edge has both endpoints in S but one coefficient zero, the other nonzero coefficient would be an incident one-entry column, contradicting closedness. Hence every edge of the mesh with endpoints in S is active at both ends. Conversely every active neighbor of a vertex in S belongs to the same component, while every neighbor outside S is a zero-coefficient ray. This proves that the active graph really is the full induced mesh graph, including the zero-coefficient issue that might otherwise invalidate the local argument.

### 5.2 Exact zero-ray classification

Writing theta_i for successive angular gaps, a coefficient is zero exactly when theta_(i-1)+theta_i=pi. For even n at least six, two nonadjacent zero indices involve four distinct positive gaps already totaling 2pi. Additional positive gaps remain, a contradiction. There are therefore at most two zero indices, and if two exist they are adjacent; three indices would contain a nonadjacent pair.

For n=4, one zero forces its opposite zero by complementing the two gap sums. The possibilities are no zeros, exactly two opposite zeros, or four zeros. Four is precisely the discarded singular star. In the two-zero case the supported rays are opposite, so the induced star is a straight line, not a positive-angle sector. This special case cannot be silently combined with the n at least six argument.

### 5.3 Local convexity, including lower-dimensional pieces

The induced neighborhoods at vertices are exactly:

1. A disk when no ray is zero.
2. A half-disk when one ray is zero, because its two supported neighboring rays are opposite.
3. A strictly convex sector when two adjacent rays are zero. If its missing sector has successive gaps x,y,z, then x+y=y+z=pi; the supported sector has angle y in (0,pi).
4. A line segment for the nonsingular valence-four, two-opposite-zero case.

At the relative interior of an induced edge, zero, one, or two supported incident triangles give a local line segment, half-disk, or disk. Triangle interiors have disk neighborhoods. Because the embedded complex is finite, the neighborhoods can be chosen small enough that no other simplex intrudes. Thus K is locally convex everywhere, including possible line pieces and their proposed attachments.

### 5.4 Precise local-to-global argument without transversality

The original finite-simplex proof is valid with the following explicit interpretation. Let C_1,...,C_N be the closed maximal simplices of K. Connectedness of the induced graph gives a polygonal path in K between any p,q in K.

Every polygonal path has a finite subdivision into segments, each labelled by a maximal simplex containing it. The intersection of one straight path segment with one closed convex simplex is an interval, a point, or empty; subdivision at finitely many interval endpoints gives the required labels even when the path lies in shared faces.

If a label repeats, replace the subpath from entry into its first occurrence through exit from its last occurrence by the straight segment in that same convex simplex. Its endpoints both lie in that simplex. Length does not increase, and the number of labelled pieces decreases. Incidental crossings of other simplices do not require relabelling the replacement. Iteration therefore leaves an ordered chain with distinct labels and no greater length.

There are finitely many ordered tuples of distinct maximal simplices. For a tuple D_1,...,D_m with p in D_1 and q in D_m, crossing points range over the compact product

(D_1 intersect D_2) times ... times (D_(m-1) intersect D_m).

After infeasible tuples are discarded, the continuous sum of segment lengths has a minimum on every remaining product. At least one tuple is feasible. The smallest of the finitely many minima is consequently a shortest polygonal path among all polygonal paths in K. This does not presume transversal intersections or a pre-existing unique sequence of simplices visited.

A genuine bend of this minimizer can be strictly shortened in a locally convex neighborhood. After zero-length pieces and redundant collinear breakpoints are removed, the minimizer is the straight segment pq. Therefore K is convex.

### 5.5 Nondegeneracy of the induced polygon and Euler bound

Every retained row has at least two active rays by the zero classification. Thus K cannot be a point. If it were a one-dimensional compact convex set, it would be a segment. Its endpoint would have induced graph degree one: conformity prevents multiple overlapping edges extending along the same ray. This again contradicts the minimum active degree. Hence K has nonempty planar interior.

Convexity now excludes every local line-star case. The convex hull of such a vertex with any nondegenerate supported triangle would create a two-dimensional sector arbitrarily close to that vertex. This rules out line chains, line attachments at vertices, pinches, and holes. K is an induced triangulation of a convex polygon.

At a strict boundary corner exactly two adjacent mesh rays were removed, so its induced degree is even and at least four. At a straight boundary vertex exactly one ray was removed, so the induced degree is odd and at least five. Interior vertices retain their complete original even stars, of degree at least four.

For a triangulated polygonal disk Euler's formula gives

sum_(interior v) (6-d(v)) + sum_(boundary v) (4-d(v)) = 6.

Every boundary contribution here is nonpositive. An interior contribution is positive only at degree four, where it is two. Thus K has at least three degree-four interior vertices. Since their full original stars are retained and S contains only nonzero rows, these are original nonsingular degree-four interior mesh vertices.

**Accepted corollary.** If the original mesh has at most two nonsingular degree-four interior vertices, R has no closed component. Every component then has a one-entry column, which forces its left-nullspace coordinate to zero and propagates zero throughout. Thus R has full row rank and every prescribed vertex jet admits a C1 piecewise quartic interpolant on the same mesh. Neither cycle balance nor the nonvanishing of a local jet form is needed for this sufficient condition.

## 6. Reproducibility and limits

The audit uses independent exact rational and symbolic checks, including the derivative identity, separately assembled gradient-evaluation matrices, and exact certificate comparisons described above. The public report gives the mathematical arguments and verification outcomes. It does not redistribute the source-derived coordinate and face arrays or claim to be a standalone numerical reproduction package; reproducing Qiu’s mesh requires the specification in the cited preprint.

All self-contained mathematical conclusions above avoid the optional external degree-four dimension formula. The original 1987 dimension theorem was not independently re-audited here and is not needed for acceptance.

The remaining general question is whether an admissible mesh can possess a closed, cycle-balanced reduced-row component with a nonzero local jet form, or whether geometry forbids that configuration. The accepted results restrict this question but do not resolve it. This audit makes no worldwide literature-openness or novelty claim.

Primary scope references:

- Peter Alfeld, contribution to Oberwolfach Report 21/2015, printed page 1146, items 16–18: https://publications.mfo.de/handle/mfo/3469 ; https://doi.org/10.4171/OWR/2015/21 .
- Expanded author article, Definition 1 and Section 9: https://peteralfeld.github.io/home/mfo.pdf ; https://doi.org/10.1016/j.cagd.2015.11.007 .
- Qiu's credited cubic counterexample preprint: https://arxiv.org/abs/2609.06364v1 .

## 7. Acceptance of publication-only certificate clarifications

The separate publication copy's additions were inspected and independently checked. The Qiu row multipliers and sparse certificate triples agree under the convention of starting at the ray of least polar angle in [0,2pi) and normalizing lambda_0=1. The family uses the same convention; every ray's half-plane and the positive cyclic triangle ordering remain fixed for all t>1, so none of its twelve quoted row multipliers silently changes at an interior parameter value. All 81 Qiu and all 144 family minor entries match under these precise conventions.

The stated sparse family determinant expansion is also accepted. Eliminating original rows 6,7,9,10,11,12,5,4,3 by their successive single surviving entries leaves rows 1,2,8 and columns 1,4,6. Its signed factor is -27t(t-1)^11. The remaining matrix is

[ -t(t-1), t^2(t-1), 0 ]
[ -(t-1)^2, 0, t^3 ]
[ 0, -(t-1), -1 ].

Its determinant is -t^2(t-1)^2(t^2+t-1), giving the full determinant above. Every elimination sign and pivot is checked exactly. The publication copy's simplex-labelled-chain replacement of the compactness paragraph is accepted and supplies the precision described in Section 5.4. These changes are explanatory certificate and proof clarifications, without expansion of the mathematical claim.
