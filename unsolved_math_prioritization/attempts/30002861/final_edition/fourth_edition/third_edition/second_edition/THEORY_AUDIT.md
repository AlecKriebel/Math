# Independent acceptance of the second-pass quartic balance theory

## Decision and exact scope

**Accepted without mathematical correction.** The four-point separation lemma,
degree-four local-jet nonvanishing, automatic obstruction of every balanced
closed component, augmented full row rank, dimension count, pure-gradient
strengthening, face-color normalization, signed-Ceva criterion, and necessary
compactly supported quadratic-spline construction are valid in the stated
model. No new counted pass is introduced by this audit.

The reviewed mathematical report is [SECOND_PASS_THEORY.md](SECOND_PASS_THEORY.md). Its proof and conclusions are accepted without mathematical correction. The [public content manifest](CONTENT_MANIFEST.json) identifies the exact edition files.

The model is a finite conforming straight-line triangulation of a polygonal
disk with nondegenerate triangles. Values and both first derivatives may be
prescribed independently at every original vertex, including boundary
vertices. Interpolants are globally C1 and have degree at most four on the
original triangles. No refinement, boundary condition, moved vertex, or
additional smoothness is assumed.

This audit takes as its baseline the independently accepted [first-edition reduction](first_edition/QUARTIC_REDUCTION.md) and [convex-support theorem](first_edition/CONVEX_SUPPORT.md), with the [first-edition acceptance](first_edition/QUARTIC_AUDIT.md). [DEPENDENCIES.md](DEPENDENCIES.md) identifies the exact immutable baseline.
In particular, it uses the exact equivalence Rm=Hj, the displayed moment
identities, the characterization of closed active components, and the theorem
that each such component is an induced convex triangulated disk containing at
least three original nonsingular degree-four interior vertices. Those are
explicit mathematical dependencies, not newly inferred experimental facts.

This acceptance neither supplies a balanced component nor rules one out. It
does not establish universal quartic Hermite surjectivity, a quartic
counterexample, historical novelty, or present-day literature openness.

## 1. Evaluation separation and the strengthened rank criterion

The four-point lemma is correct, including the case of three collinear
points. For a selected point p, if the other three are collinear, their line
avoids p. Otherwise at least one line through a pair of them avoids p; multiply
its affine equation by the equation of a line through the remaining point
that also avoids p. This gives a degree-at-most-two polynomial nonzero at p
and zero at the other three. Four such separators prove independence of the
four evaluation functionals.

At an interior four-star the neighbor vectors are four distinct points. They
cannot lie on one affine line: a line avoiding the origin would place all
four rays in one open half-plane, while a line through the origin would allow
only two distinct outgoing ray directions. Either possibility contradicts a
conforming full interior fan with four positive angular gaps below pi.

If H_v vanished, its constant and first moments, together with the accepted
second-moment identity, would make the nonzero row r_v annihilate every
quadratic evaluation on those four points. The separation result excludes
this. Thus H_v is nonzero at every nonsingular degree-four interior vertex.

Now let z be a nonzero left-null vector of R. On any active component where
it is nonzero, two-entry columns propagate nonzero coordinates, while an
incident one-entry column is impossible. The component is therefore closed
and balanced. The accepted support theorem supplies a nonsingular four-star
v in it. Since H has disjoint vertex-jet coordinate blocks, the v block of
z^T H is z_v H_v and cannot cancel with another vertex's block. Hence no
nonzero z annihilates both R and H, proving

    rank([R H]) = number of retained rows.

It follows from the already exact interpolation reduction that failure for
some prescribed jets, row-rank deficiency of R, and existence of a closed
balanced component are equivalent. The first-pass qualification requiring a
nonzero supported local jet form is now automatically satisfied. This is a
complete universal implication within the model, not a sampled-rank claim.

## 2. Dimension count, including the boundary

Let q count all even interior vertices and let sigma count singular interior
four-stars. The first-pass fan matrices have total corner-column rank
2 E_I - q. The remaining q-sigma rows are exactly the retained augmented
compatibilities and have full row rank by Section 1. Singular rows vanish on
both remaining coefficients and jets. Boundary fans are paths and contribute
no residual compatibility row. Therefore the residual C1 constraint rank in
the continuous-trace representation is exactly

    (2 E_I - q) + (q - sigma) = 2 E_I - sigma.

With jets now variables, that representation has 3V+E+3T free coordinates.
Subtracting the constraint rank gives

    dim S^1_4 = 3V + E + 3T - 2 E_I + sigma.

For a triangulated polygonal disk, if B is its number of boundary edges (also
the number of boundary vertices), Euler and triangle-edge counting give

    E = 3V - B - 3,
    T = 2V - B - 2,
    E_I = 3V - 2B - 3.

Substitution gives 6V-3+sigma, with no missing boundary correction. The rank
being counted here is the residual C1 rank after continuous traces and vertex
jets have been parameterized; it is not a rank claim for unparameterized
15T triangle coefficients. The report's surrounding explanation makes this
scope clear.

The formula is obtained from the accepted first-pass mathematics and the new
nonvanishing proof. Its validity in this audit does not rely on importing the
historical dimension theorem attributed to Alfeld, Piper, and Schumaker.
That historical proof was not independently inspected here, and no claim to
have inspected it is made.

## 3. Independent proof of the pure-gradient four-star lemma

An orientation-preserving invertible linear map sends consecutive outgoing
vectors to (1,0),(0,1). Write the remaining vectors as (a,b),(c,d). The cyclic
positive doubled triangle areas are

    1, -a, D, -d,       D=ad-bc,

so a<0, d<0, D>0. These are exactly the sign conditions used in the proof.
The independent symbolic audit obtains the left corner multiplier from the
adjugate of the actual cyclic corner matrix, rather than importing the
author's verifier or copying its output. With its first entry normalized to
one it is (1,1/a,1/D,1/d). Multiplying the resulting compatibility row by the
nonzero scalar adD gives

    r = (-acD, bdD, cd, -ab).

Its second moment is identically the zero matrix, and its first moment is

    M = (ac(d-b-D), bd(D+c-a)).

All possibilities for the signs or zeros of b and c are covered:

- If b=c=0, the rays are two opposite pairs and the row is zero. This is
  precisely the excluded singular case under a<0 and d<0.
- If b=0 and c is nonzero, M's first component is acd(1-a), which cannot
  vanish.
- If c=0 and b is nonzero, M's second component is abd(d-1), which cannot
  vanish.
- Otherwise M=0 would imply D=d-b=a-c. Substitution into D=ad-bc gives
  D=D(a+b), so a+b=1. But b=d-D<0 and a<0, a contradiction.

Thus M is nonzero at every nonsingular four-star. The coordinate change is
invertible and the row scaling is nonzero, so its nonvanishing is intrinsic.
No genericity hypothesis excludes a permitted collinearity or a zero row
entry in this argument.

Consequently a balanced component is witnessed by data with every scalar
value zero and all gradients zero except for a single coordinate derivative
at one of its nonsingular four-stars. The chosen derivative is a coordinate
where M is nonzero. The same disjoint-block argument shows that adjoining
only H's gradient columns to R already gives full row rank. Neither statement
asserts that R itself has full row rank.

## 4. Face colors and endpoint signs

The induced support K is a triangulated disk. Every vertex interior to K
retains its full even original fan. Embed the triangle adjacency dual by
arcs through edge interiors and omit the exterior node. Its bounded facial
walks correspond to these interior primal vertices and have even length.
Every simple dual cycle is the mod-two sum of the bounded facial walks it
encloses, so every dual cycle has even length. The face coloring is therefore
well-defined. Straight boundary vertices introduce no missing parity
condition.

At a boundary vertex the supported triangles form one connected interval of
the original even fan. Their alternating signs extend around that full fan
consistently. This is a local extension; it need not color all original
triangles outside K compatibly with each other. A boundary edge uses only
the exterior triangle immediately adjacent to it, whose local sign is the
negative of the interior triangle at both endpoints. That is sufficient.

For the orientation v to w, take u on the left and z on the right. Both
triangles exist in the original mesh even when vw is on the boundary of K,
because support vertices are interior original mesh vertices. Put

    A=det(w-v,u-v)>0,       B=det(v-w,z-w)>0,
    D_v=det(z-v,u-v),       D_w=det(u-w,z-w).

The row normalization specified in the report gives

    rho_vw = s_T D_v/(AB),
    rho_wv = -s_T D_w/(AB).

The minus at w is essential: the triangle immediately counterclockwise from
w to v is the original right-hand triangle. The local alternating extension
provides the same minus when it lies outside K. The determinant identity
D_v+D_w=A+B is exact. Closedness makes both D_v and D_w nonzero. Therefore
the dependency equation is exactly

    x_w/x_v = -rho_vw/rho_wv = D_v/D_w.

These are dependency coordinates for the normalized rows. Independent row
rescalings alter the individual coordinates and edge ratios by endpoint
factors, which cancel around every cycle. The report does not confuse those
coordinates with the original unnormalized dependency.

## 5. Transverse intersections, signed Ceva, and all cycles

To test affine scaling as well as signs, independently set
v=(0,0), w=(h,0), u=(p,q), z=(r,-t), with h,q,t>0. Direct calculation gives

    D_v = rq+pt,
    D_w = h(q+t)-rq-pt,
    P = (rq+pt)/(q+t),

where (P,0) is the intersection of the transverse line uz with vw's line.
Thus D_v/D_w=P/(h-P). With h=1 this is exactly the report's p/(1-p).
The denominator q+t is positive, so the intersection is finite. The edge
ratio is positive precisely when 0<P<h, exactly the case of a strictly
convex two-triangle quadrilateral. Endpoint cases are excluded by the active
coefficients. Outside that interval the union is nonconvex and the ratio is
negative. Hence the nonconvex edges form the sign cut of a balanced
dependency; this says nothing by itself about magnitudes.

For a face ABC and the opposite vertex C'=alpha A+beta B+gamma C across AB,
gamma<0. Direct substitution gives D_A=beta A_edge and D_B=alpha A_edge.
Both alpha and beta are nonzero. Thus the normalized edge ratio is
x_B/x_A=beta/alpha, with no extra Ceva minus sign. The line CC' has equation
beta X_A-alpha X_B=0. The other two lines give the cyclic equations. Their
3-by-3 determinant vanishes precisely when the three propagation ratios
multiply to one. Every nonzero solution has all three coordinates nonzero,
because each line equation has two nonzero coefficients. It is the common
projective point (x_A:x_B:x_C), including the valid point-at-infinity case
x_A+x_B+x_C=0. This also rules out a spurious solution supported at one
triangle vertex.

Finally, each simple edge cycle in the convex triangulated disk bounds a
union of its triangular faces. Multiplying their consistently oriented
cycle products cancels every internal edge against its reverse. This proves
that triangular balance implies balance around every simple cycle. General
closed walks split into simple cycles and reverse-edge pairs. Root-to-vertex
propagation is then path-independent. The converse implications are
immediate. Boundary triangle tests must use the actual original opposite
vertices outside K, as the report explicitly requires.

## 6. Moment stresses and exterior-zero quadratic integration

For a balanced component, a_vw=z_v r_vw is antisymmetric and nonzero on every
induced edge. The accepted local second moments give

    sum_w a_vw (w-v)(w-v)^T = 0.

Multiplying by the coefficient vector of a linear functional ell gives the
ordinary equilibrium identity for
omega_vw=a_vw ell(w-v). Reversing an edge negates both factors, so omega is
symmetric. Individual projected stresses may have zeros, and no positivity
conclusion follows or is asserted.

Let L_vw(X)=det(w-v,X-v). Reversal gives L_wv=-L_vw, while a_wv=-a_vw.
Consequently q_left-q_right=a_vw L_vw^2 is orientation-consistent. Around a
vertex with counterclockwise triangles T_i, an outgoing edge separates
T_(i-1) on the right from T_i on the left. Its prescribed difference is
q_i-q_(i-1), so there is no missing alternating sign in the vertex sum.
If S=sum_w a_vw (w-v)(w-v)^T, the corresponding sum of squared line forms is

    (X-v)^T J S J^T (X-v),       J=[[0,-1],[1,0]],

and therefore vanishes identically. At a boundary vertex the missing
interval is the single exterior face; all boundary edge contributions are
still included in this telescoping sum.

Here is an independent algebraic completeness check on the dual integration,
which also makes the role of the exterior face explicit. Choose an
orientation for every edge of K, and let B be the primal vertex-edge
incidence matrix, with + at the outgoing end. For the dual graph include all
triangles and one exterior node. Its incidence matrix B* is oriented so that
(B*^T q)_e=q_left-q_right. For each polynomial coefficient of the assigned
jump c_e=a_e L_e^2, the vertex identities say Bc=0. The boundary-of-boundary
identity gives B B*^T=0. Both primal and full dual graphs are connected. Euler
therefore gives

    dim ker B = E-V+1 = T = rank(B*^T).

Thus ker B equals im B*^T. Every coefficient of the desired quadratics can
be integrated, uniquely after the exterior polynomial is fixed to zero.
This proves absence of a remaining global period, including all boundary
edges. It is equivalent to the report's dual-cycle argument and needs no
extra geometric or external-source hypothesis.

The resulting polynomials and gradients agree on each edge because the
difference is divisible by its squared line equation. Agreement with the
zero exterior gives a globally C1 extension by zero outside K, including its
vertices. A nonzero cofactor forces a nonzero spline. In fact the Hessian
jump at every induced edge is 2a_e n_e n_e^T and is nonzero. This is a
necessary construction from a balanced quartic component. An arbitrary C1
quadratic spline supplies moment-compatible cofactors, but does not force
them to lie in the particular one-dimensional span of r_v at every vertex.
The report correctly refrains from asserting that converse or a rank theorem
from compact support alone.

## 7. Independent algebraic checks and limits

The independent calculation derives the cyclic corner-matrix kernel from an adjugate, then checks generic rational identities: the normalized four-star row, every first and second moment, both one-zero cases, the contradiction substitution, edge determinants with a free edge length, the barycentric ratio, the signed-Ceva determinant, cofactor reversal, tensor rotation, equilibrium contraction, and the Euler/dimension formulas. These calculations were independently constructed rather than taken from the authoring calculation.

Six explicit negative controls distinguish the necessary conventions: a row-entry sign change, an omitted propagation minus, an inverted edge ratio, a changed Ceva determinant sign, an unreversed cofactor scalar, and a subtracted singular count each fail the corresponding identity. The exact algebraic checks passed. The topology, inequality case split, and all-mesh implications are proved above; computational agreement alone is not offered as their proof. [REPRODUCTION.md](REPRODUCTION.md) supplies the conventions needed to check the identities independently without relying on a particular implementation.

The primary-source references in the theory report delimit the underlying problem and historical attribution. No additional assertion about those sources is independently certified here. The mathematical claims follow from the explicitly identified [accepted baseline](DEPENDENCIES.md) and the proofs audited above. The public edition makes only editorial changes to the accepted proof and audit; it adds links and omits verification implementation details. No mathematical correction was needed.
