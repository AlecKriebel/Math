# Quartic obstruction theory and exact balance criteria

Second mathematical edition. The [independent theory audit](THEORY_AUDIT.md) accepts these results. Exact baseline dependencies and notation are linked in [DEPENDENCIES.md](DEPENDENCIES.md); finite verification conventions are in [REPRODUCTION.md](REPRODUCTION.md).

## Scope and status

This is part of the second newly documented substantive pass for row 1761 / problem 30002861 / OWR-13678-002. It is not a separate additional pass. The model remains a finite conforming straight-line triangulation of a polygonal disk, with nondegenerate triangles, arbitrary scalar values and both first derivatives at every vertex, and globally C1 polynomials of total degree at most four on the original triangles.

The accepted [first-edition reduction](first_edition/QUARTIC_REDUCTION.md) and [convex-support theorem](first_edition/CONVEX_SUPPORT.md), with their [independent acceptance](first_edition/QUARTIC_AUDIT.md), are assumed here. In particular, R has one row for each even-valence nonsingular interior mesh vertex, and H has disjoint local vertex-jet blocks. Each connected closed component of its active graph is the full induced triangulation K of a convex polygon. Every such K has at least three original nonsingular degree-four interior vertices.

The conclusions below do not settle whether a balanced component exists. They remove the local-jet qualification from the obstruction criterion, give an exact projective concurrency criterion for balance, and expose a further necessary quadratic-spline structure. No novelty claim is made. The quartic spline dimension formula recovered below is a known formula; the point here is its derivation from the accepted reduction without importing its historical proof.

## 1. Four-point quadratic separation

**Lemma 1.** If four distinct points in the plane are not all collinear, their evaluation functionals on the polynomials of total degree at most two are linearly independent.

**Proof.** Fix one of the points p and call the others a,b,c. If a,b,c are collinear, their line does not contain p, and an affine equation for that line vanishes at a,b,c and not at p. Otherwise, at least one of the three lines ab,bc,ca avoids p. Choose such a line L and call the unused point c after relabeling. Choose a line M through c that avoids p. The product of affine equations for L and M vanishes at all three other points and not at p. Thus in every case a polynomial of degree at most two separates p from the other three. Doing this for each p proves the assertion. ∎

**Lemma 2.** The local jet form H_v is nonzero at every nonsingular degree-four interior vertex v.

**Proof.** Write its four outgoing vectors as d_i and its nonzero row as r_i. The accepted moment identities are

    H_v(f,g) = (sum_i r_i) f + (1/2)(sum_i r_i d_i) dot g,
    sum_i r_i d_i d_i^T = 0.

If H_v were zero, r would annihilate evaluation of the constant, the two linear monomials, and the three homogeneous quadratic monomials at the four points d_i. These points are distinct. They cannot all be collinear, since their counterclockwise fan covers a neighborhood of the interior vertex. Lemma 1 would give r=0, contradicting nonsingularity. ∎

## 2. Consequences for the global reduction

Let m be the number of retained rows of R. A nonzero vector in the left nullspace of R is nonzero on at least one active component. Propagation along every two-entry edge column makes all its entries on that component nonzero. Every one-entry column would force its incident entry to zero. Hence that component is closed and balanced.

The accepted convex/Euler theorem supplies a nonsingular degree-four interior vertex v in that component; in fact it supplies at least three. Lemma 2 gives H_v nonzero. Because H uses disjoint vertex-jet coordinate blocks, the block of z^T H at v is exactly z_v H_v, which cannot vanish.

It follows that

    rank([R H]) = m

on every mesh in the model. Consequently the following are equivalent:

1. Some prescribed vertex first jets fail to admit a C1 piecewise quartic interpolant.
2. R does not have full row rank.
3. The active graph of R has a closed, cycle-balanced connected component.

The extra requirement that some supported local jet form be nonzero is automatic. This is an equivalence within the exact reduction, not an existence claim for such a component.

### 2.1 Recovery of the known quartic dimension formula

Let V,E,T,E_I denote numbers of vertices, edges, triangles, and interior edges. Let q be the number of even interior mesh vertices, including singular vertices, and let sigma be the number of singular interior four-stars. The accepted fan elimination removes 2E_I-q independent corner equations. The remaining q-sigma equations form [R H], which has full row rank by the preceding argument. The full C1 constraint rank, with the vertex jets also treated as variables, is therefore

    (2E_I-q)+(q-sigma) = 2E_I-sigma.

The continuous-trace Bernstein representation has 3V+E+3T free variables before those residual C1 constraints. Thus

    dim S^1_4 = 3V+E+3T-2E_I+sigma = 6V-3+sigma,

where the last equality is the ordinary Euler/counting identity for a triangulated disk. This recovers the known degree-four dimension formula credited in the first-pass source review to the quartic basis analysis of Alfeld, Piper, and Schumaker. No new historical or novelty claim is intended, and the 1987 proof is not presumed independently inspected in this pass.

## 3. Stronger local statement: a pure-gradient obstruction

This section is a separately checkable strengthening of Lemma 2.

**Lemma 3.** At a nonsingular degree-four interior vertex, the vector sum_i r_i d_i is nonzero. In particular, the gradient part of H_v cannot vanish.

**Proof.** An invertible orientation-preserving linear change of coordinates takes consecutive outgoing vectors to d_0=(1,0), d_1=(0,1). Write d_2=(a,b), d_3=(c,d), and D=ad-bc. The positive cyclic triangle determinants give

    a<0, d<0, D>0.

The first-pass convention is lambda_i=(-1)^i a_0/a_i, with a_i=det(d_i,d_(i+1)). Here a_0=1, a_1=-a, a_2=D, a_3=-d. Multiplying its row by the nonzero factor adD gives

    r = (-acD, bdD, cd, -ab).

Its first moment is exactly

    M = (ac(d-b-D), bd(D+c-a)).

If b=c=0, the four rays form two opposite pairs and the row is zero: this is exactly the singular case.

If b=0 and c is nonzero, the first entry is acd(1-a), which is nonzero. If c=0 and b is nonzero, the second entry is abd(d-1), which is nonzero.

Finally, if b and c are both nonzero and M=0, then

    D=d-b=a-c.

Substituting d=b+D and c=a-D into D=ad-bc gives D=D(a+b). Since D>0, this forces a+b=1. But b=d-D<0 and a<0, a contradiction. Thus M is nonzero in every nonsingular case. Its nonvanishing is invariant under the invertible coordinate change and nonzero row scaling. ∎

**Corollary.** Every balanced closed component produces an incompatible jet assignment with all scalar vertex values zero and all gradients zero except at a single nonsingular degree-four vertex. At such a vertex choose a coordinate direction for which M has a nonzero entry and prescribe that coordinate derivative to be one. The supported left-null vector then gives z^T H j nonzero. One may instead choose any gradient g with M dot g nonzero.

Also, adjoining just the gradient-coordinate columns of H to R already gives full row rank. This does not assert that R itself has full row rank.

## 4. A consistent face-color normalization

All interior vertices of K have even degree. Its triangular faces therefore have a coloring s_T in {+1,-1} such that faces sharing an interior edge have opposite colors.

For completeness, take the planar dual graph of the triangulated disk with the exterior face omitted. Every bounded dual face corresponds to an interior primal vertex, and its boundary walk has that vertex's even degree. Each simple dual cycle is, modulo two, a sum of the bounded dual facial walks it encloses. Every such cycle is consequently even; the dual graph is bipartite. This proves the coloring assertion, including disks whose boundary has straight vertices. Equivalently, color by parity along dual paths and use the same cycle argument for path independence.

At each v in K, its supported triangle fan is connected, and its colors alternate. Extend these signs alternately across the omitted rays to the full original even fan. The even full valence makes the extension consistent. Divide the original row r_v by a_0 and multiply by a sign so that the factor (-1)^i becomes the color of the triangle immediately counterclockwise from outgoing ray i. Denote the resulting row by rho_v. This is a well-defined nonzero row rescaling. The extension across rays outside K is needed only to state the boundary-edge formula; no coloring of all exterior triangles simultaneously is assumed.

For an oriented active edge v to w, let u be the opposite vertex in its left triangle T, and let z be the opposite vertex in its right triangle U. Both are genuine original mesh vertices, since the support vertices are interior mesh vertices. If the edge is on the boundary of K, one of T,U lies outside K. Put

    A=det(w-v,u-v)>0,
    B=det(v-w,z-w)>0,
    D_v=det(z-v,u-v),
    D_w=det(u-w,z-w).

If T is in K, use its color s_T; if only U is in K, put s_T=-s_U. The normalized endpoint rows satisfy

    rho_vw = s_T D_v/(AB),
    rho_wv = -s_T D_w/(AB).

Indeed these are exactly the fan determinant formula at each endpoint, whose triangles immediately counterclockwise from the two opposite outgoing rays have opposite colors. Direct expansion gives D_v+D_w=A+B. Closedness ensures D_v and D_w are both nonzero.

For a left dependency x^T rho=0 the edge propagation equation is therefore

    x_w/x_v = D_v/D_w.                                      (1)

The x variables here correspond to the row-normalized rho, not to the original r. A nonzero row scaling changes individual dependency coordinates but cancels in every cycle product.

## 5. Transverse-diagonal and Ceva criteria

### 5.1 The signed intersection ratio

Use affine coordinates v=(0,0), w=(1,0), u=(a,b), z=(c,-d), where b,d>0. Formula (1) becomes

    x_w/x_v = (cb+ad)/(b+d-cb-ad).

The line uz meets the line vw at coordinate

    p=(cb+ad)/(b+d).

Thus

    x_w/x_v = p/(1-p).                                    (2)

The intersection is finite because u and z lie strictly on opposite sides of vw. The ratio is positive exactly when 0<p<1, equivalently when the union of the two incident triangles is a strictly convex quadrilateral. It is negative when the intersection lies on an extension of the edge. The endpoint cases p=0,1 are excluded by closedness. Hence sign balance says that the edges whose two-triangle union is nonconvex form a cut determined by the signs of x. Sign balance alone does not enforce the magnitudes in (2).

### 5.2 A triangle test

Take a support triangle ABC, and let A',B',C' be the opposite original mesh vertices across BC,CA,AB respectively. Suppose

    C'=alpha A+beta B+gamma C,
    alpha+beta+gamma=1.

Here gamma<0, and active endpoint coefficients force alpha and beta nonzero. The edge formula gives

    x_B/x_A=beta/alpha.                                   (3)

The analogous statements hold cyclically. In the projective plane, the line CC' has equation beta X_A-alpha X_B=0 in barycentric homogeneous coordinates relative to ABC. Thus the three edge-ratio equations around ABC have a nonzero solution if and only if AA',BB',CC' are concurrent, possibly at infinity. This is the signed Ceva criterion, proved directly here by the three homogeneous linear equations. The concurrency point has barycentric coordinates

    (x_A:x_B:x_C).

It is finite exactly when x_A+x_B+x_C is nonzero; in that case its Cartesian point is (x_A A+x_B B+x_C C)/(x_A+x_B+x_C). There is no assumption that the intersection points or concurrency point lie inside the triangle.

### 5.3 Local concurrence is equivalent to global balance

For the induced disk K, the following are equivalent:

- every oriented active cycle has product one in (1);
- every triangular face has product one;
- for every support triangle the three lines joining its vertices to their opposite original mesh vertices are concurrent in the projective plane.

Only the implication from triangular cycles to arbitrary cycles requires explanation. Every simple edge cycle bounds a union of triangles of K because K is a triangulated convex disk. Multiplying the oriented triangular cycle products cancels each internal edge with its reverse, leaving the product along the simple cycle. General closed walks split into simple cycles and reverse-edge pairs. This proves the claim. Nonzero dependency coordinates can then be propagated from a chosen root, independently of the path.

The criterion includes boundary triangles of K: their opposite vertices across boundary edges belong to the original larger mesh and must not be omitted or replaced by idealized boundary data.

## 6. Moment stresses and compact quadratic splines

This section supplies necessary structure rather than a completed impossibility argument.

Suppose a closed component is balanced. Use any row normalization and its nonzero left dependency, and define an oriented edge scalar

    a_vw = z_v r_vw = -z_w r_wv.

It is nonzero on every induced edge. The second moments imply

    sum_(w adjacent v) a_vw (w-v)(w-v)^T=0.                (4)

For every linear functional ell on the plane, the edge coefficients

    omega_vw = a_vw ell(w-v)

are symmetric under reversing vw and satisfy the ordinary equilibrium equations

    sum_w omega_vw (w-v)=0.

This follows by applying the matrix in (4) to the coefficient vector of ell. It yields a two-parameter family of equilibrium stresses, with possible degeneracies for individual projections; no sign definiteness is asserted.

There is also a direct polynomial-cofactor interpretation. For an oriented edge v to w define

    L_vw(X)=det(w-v,X-v).

Assign the polynomial difference across that edge by

    q_left - q_right = a_vw L_vw(X)^2.                    (5)

Changing the edge orientation changes both a_vw and left-minus-right, while L_vw squared stays unchanged. Thus this is orientation-consistent. Around a primal vertex, the sum of these polynomial differences is zero by (4), since every L_vw is a linear form vanishing at v and the coefficient matrices are a fixed ninety-degree rotation of those in (4).

The dual graph here includes one exterior face. The closed walks surrounding primal vertices generate its cycle space: an embedded simple dual cycle is the sum of the boundaries around the primal vertices it encloses; a general dual walk decomposes into simple cycles. Therefore (5) has zero sum around every dual cycle. Starting with the zero polynomial on the exterior face and integrating along dual paths defines polynomials q_T of degree at most two on all support triangles, independently of path.

Their differences across each edge are divisible by the square of that edge's linear equation. They and their gradients therefore agree on the edge. The exterior polynomial is zero, so the resulting piecewise quadratic is C1 after extension by zero outside K. It is nonzero because at least one, indeed every, edge cofactor a_vw is nonzero.

Thus a balanced obstruction would yield a nonzero compactly supported C1 piecewise quadratic spline whose Hessian jumps are nonzero across every induced edge. The converse needs the extra requirement that the local edge cofactors be proportional to the specific accepted quartic row r_v at every vertex. Arbitrary compactly supported C1 quadratic splines satisfy the moment equation, but need not satisfy that one-dimensional local proportionality condition. This observation is not a universal rank theorem.

## 7. Remaining issue and source scope

The unresolved existence question is now purely whether an admissible mesh can possess a closed component satisfying all the exact edge-ratio magnitudes, or equivalently all the signed-Ceva concurrency tests. Any such component necessarily gives an actual quartic Hermite failure, and a pure-gradient datum at a degree-four support vertex witnesses it. Sign consistency is a weaker condition and must not be promoted to magnitude balance.

Primary scope references retained from the accepted first pass:

- Peter Alfeld, Oberwolfach Report 21/2015, printed page 1146, items 16–18: https://publications.mfo.de/handle/mfo/3469 ; https://doi.org/10.4171/OWR/2015/21 .
- Expanded author article, Definition 1 and Section 9: https://peteralfeld.github.io/home/mfo.pdf ; https://doi.org/10.1016/j.cagd.2015.11.007 .

The [independent theory audit](THEORY_AUDIT.md) checks the normalized four-star row, the first and second moments, the edge-determinant formula, and the barycentric ratio. The [reproduction conventions](REPRODUCTION.md) specify direct mathematical checks of those identities. The general geometric implications are proved above.
