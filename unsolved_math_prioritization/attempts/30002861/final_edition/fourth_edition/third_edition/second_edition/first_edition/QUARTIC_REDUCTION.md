# Quartic Hermite interpolation reduction and exact partial results

## Status and scope

**Review status:** the partial quartic results below are independently accepted; see [the mathematical audit](QUARTIC_AUDIT.md). This acceptance includes the explicit row scalings, minor conventions, and sparse determinant expansion in this edition. The separate cubic counterexample is also accepted. The bundled problem remains unresolved.

Work on a fixed finite conforming straight-line triangulation of a polygonal disk. Every triangle has positive area. A spline is globally continuously differentiable and polynomial of total degree at most four on each triangle. All vertex values and both Cartesian first derivatives are prescribed, including at boundary vertices. No subdivision, vertex movement, or homogeneous boundary condition is permitted.

The results below give an exact reduced interpolation criterion, characterize its possible dependencies, verify quartic surjectivity on Qiu's cubic-counterexample mesh, and rule out an explicit collinear eighteen-vertex family as a source of quartic counterexamples. The companion [convex-support argument](CONVEX_SUPPORT.md) gives further necessary geometry and a positive interpolation corollary. No novelty or priority claim is made.

The primary questions are Alfeld's 2015 report, printed p.1146, items 16–18, and his expanded article, Definition 1 and Section 9. The complete citations, inspection limits, and dated status observations are in [the source record](SOURCES.md). Refinement-based interpolation theorems and failure of a particular extension algorithm do not decide the fixed-mesh question.

## 1. Remaining Bernstein–Bézier unknowns

On a triangle (v,w,u), write the total-degree 4 polynomial in its degree 4 Bernstein basis. Prescribed vertex data (f_v,g_v) determine

c_{400}=f_v,

c_{310}=f_v+(1/4) g_v·(w−v),

and the analogous coefficients at every corner. Thus 9 of the 15 coefficients on each triangle are fixed. The remaining coefficients are:

- one shared edge midpoint coefficient m_{vw}=c_{220} for every mesh edge;
- one coefficient t_{T,v}=c_{211} for each triangle corner v.

Sharing the edge coefficients makes the polynomial traces agree identically on each common edge. There are four scalar C1 Bernstein conditions on an interior edge; the two endpoint conditions are already guaranteed by the common vertex gradients.

For adjacent triangles (v,w,u) and (v,w,z), let

z=αv+βw+γu,  α+β+γ=1.

The two remaining conditions are exactly

t_{(v,w,z),v}−γ t_{(v,w,u),v}−β m_{vw}
  =α[f_v+(1/4)g_v·(w−v)],

t_{(v,w,z),w}−γ t_{(v,w,u),w}−α m_{vw}
  =β[f_w+(1/4)g_w·(v−w)].

This follows directly by matching the first Bernstein row transverse to the common edge. Conversely these equations, trace agreement and endpoint-gradient agreement give all C1 conditions, so the system is sufficient as well as necessary. Edgewise C1 agreement is global C1 on a conforming finite disk mesh, including the boundary in the usual one-sided sense.

Hence the full remaining-coefficient system A x=B j has 2 E_I rows and E+3T unknowns. No polynomial degree higher than 4 or extra regularity has been imposed.

## 2. Exact elimination around a vertex

At an interior vertex v, list its neighbors w_0,…,w_{n−1} counterclockwise; indices are cyclic. Put d_i=w_i−v and a_i=det(d_i,d_{i+1})>0. Write

w_{i+1}=α_i v+β_i w_i+γ_i w_{i−1}.

Then

γ_i=−a_i/a_{i−1},

β_i=det(d_{i−1},d_{i+1})/a_{i−1},

α_i=1−β_i−γ_i.

The corner equations become

t_i−γ_i t_{i−1}−β_i m_{vw_i}=α_i h_i,

where h_i=f_v+(1/4)g_v·d_i.

Their cyclic coefficient determinant is 1−product_i γ_i=1−(−1)^n.

- If n is odd, the t_i are uniquely solvable for arbitrary m and jets.
- If n is even, the corner matrix has rank n−1. A left null vector is λ_i=(−1)^i a_0/a_i, with λ_0=1. Its sole compatibility equation is

sum_i r_{v,i} m_{vw_i}=H_v(f_v,g_v),

r_{v,i}=λ_i β_i,

H_v=−sum_i λ_i α_i [f_v+(1/4)g_v·d_i].

A boundary vertex has a path of triangles instead of a cycle. Every recursion coefficient γ_i is nonzero, so its equations are solvable for arbitrary edge coefficients and jets, starting at one end. There is no boundary compatibility equation.

The row r_v vanishes identically exactly when the interior vertex has degree 4 with two opposite ray pairs, i.e. is singular. Indeed r_v=0 forces every d_{i+1} to be opposite d_{i−1}; distinct cyclic rays then force n=4. Conversely a singular star clearly makes every β_i zero. Its H_v vanishes too: any arbitrary first jet is realized by an affine polynomial, so a zero compatibility row cannot constrain that jet.

Discard those zero rows. Let R have the remaining rows, one for each even nonsingular interior vertex, and let H have the corresponding local jet forms. Then

A quartic C1 Hermite interpolant exists exactly when Rm=Hj is solvable.

In particular, surjectivity for all vertex data is equivalent to rank(R)=rank([R H]). Full row rank of R is a sufficient certificate.

An equivalent local RHS, checked by the affine-polynomial identity, is

H_v=(sum_i r_{v,i}) f_v
      +(1/2)(sum_i r_{v,i} d_i)·g_v.

## 3. Exact graph obstruction

Every column of R is indexed by an edge vw and has at most two nonzero entries, at v and w. Consider the graph whose vertices are nonzero rows and whose ordinary edges are columns having two nonzero entries. A column with just one nonzero entry is a half-edge forcing the corresponding coordinate of any left null vector z to vanish.

Along an ordinary edge e=vw, a left null vector must satisfy

z_w=−(r_{v,e}/r_{w,e}) z_v.

Consequently a connected component can support a nonzero left null vector exactly when:

1. no column has exactly one nonzero entry in the component; and
2. multiplying the displayed ratios around every cycle gives 1.

Such a component contributes one dimension to the left nullspace. Since distinct rows of H use disjoint vertex-jet coordinates, its dependency produces incompatible data exactly when at least one supported H_v is nonzero. This gives a complete, exact, finite obstruction test. Exact rational propagation can check this criterion directly; the resulting nullity was also compared with exact matrix rank in the mathematical verification.

For explicit incompatible data, choose a supported vertex v and a nonzero coefficient of H_v, prescribe 1 for that jet coordinate and 0 for all others, and scale if desired. Then z^T H j is nonzero while z^T Rm is identically zero.

The coefficient r_{v,e} vanishes precisely when the two neighbors of ray e in the fan are collinear with v. Merely finding a closed support is insufficient: cycle balance remains essential, as the family below demonstrates.

## 4. Qiu's mesh: positive quartic result

The triangulation is the one specified in Qiu's versioned preprint, Table 1 and equations (7)–(8). Its geometry was independently checked in the [cubic audit](CUBIC_AUDIT.md). The source coordinate and triangle arrays are not reproduced here. Numerical reproduction requires obtaining that specification from the cited paper. No author program was run.

For this mesh:

- V=41, T=56, E=96, E_I=72;
- there are 9 even interior stars, at O and U_0,…,U_7;
- R has shape 9×96 and rank 9;
- the independently assembled full A has shape 144×264 and rank 144;
- adjoining all 123 jet-coordinate columns preserves those ranks.

Here is an explicit rank certificate, using the row formula in Section 2. At each vertex order the outgoing rays counterclockwise starting at the ray of least polar angle in [0,2π), measured from the positive x-axis. Normalize λ_0=1. Order the rows as O,U_0,…,U_7 and multiply them, respectively, by

7, 378, 63, 63, 378, 9/2, 27, 27, 9/2.

Choose the columns

OA_0, A_0U_0, A_0U_7, A_1U_1, A_2U_2, A_3U_3, A_4U_4, A_5U_5, A_6U_6.

The resulting 9×9 minor has exactly one nonzero entry in each row and column. Numbering from 1, its nonzero (row, column, value) triples are

(1,1,5), (2,2,−1), (3,4,36), (4,5,1), (5,6,−36), (6,7,−1), (7,8,36), (8,9,1), (9,3,1).

Its determinant is −233280. All row scalings are nonzero, so R has full row rank and every quartic vertex Hermite datum is attainable. Changing the starting ray only rescales a row by a nonzero number, and does not alter this rank conclusion.

The quartic conclusion uses the independently accepted geometry of that exact cited mesh. It is a positive result for this mesh, so the cubic counterexample itself does not provide a quartic counterexample.

## 5. A collinear eighteen-vertex family

Let

h_0,…,h_5=(2,0),(1,1),(−1,1),(−2,0),(−1,−1),(1,−1),

q_0,…,q_5=(3,1),(0,2),(−3,1),(−3,−1),(0,−2),(3,−1).

For t>1 put O_i=t h_i, I_i=h_i and B_i=t q_i. Use indices modulo 6. Include the triangles

(O_i,O_{i+1},I_{i+1}), (O_i,I_{i+1},I_i),

(O_i,B_i,O_{i+1}), (O_i,B_{i−1},B_i)

for i=0,…,5, and the four triangles

(I_0,I_1,I_2), (I_2,I_3,I_4), (I_4,I_5,I_0), (I_0,I_2,I_4).

Orient triangles counterclockwise. The inner and outer core hexagons are concentric convex affine-regular hexagons, and the B_i form a larger convex hexagon. The first ring is partitioned into six convex trapezoids split by the indicated diagonals. The outer ring consists of the twelve displayed nonoverlapping triangles, with B_i the intersection of the extended neighboring core sides. The central hexagon is split by its three alternate-vertex diagonals. This gives a conforming triangulated disk with 18 vertices and 28 genuine triangles. Its positive doubled triangle areas belong to {2,6,2(t−1),2t(t−1),2t^2}.

All 12 core vertices are even-valence nonsingular interior vertices. At each O_i, its two edges toward boundary vertices have zero row coefficients, because the adjacent rays are collinear. Thus all 12 rows form a closed active support; half-edge elimination alone cannot prove rank. This support is cycle-unbalanced, as the nonzero determinant below shows. It is not a quartic obstruction.

Index vertices O_i by i and I_i by 6+i. Use the same positive-x-axis starting convention as above, and normalize λ_0=1. In row order O_0,…,O_5,I_0,…,I_5 multiply the reduced rows by

(t−1)^2, (t−1)^2, (t−1)^2, t(t−1), t(t−1), (t−1)^2,
3t(t−1), t(t−1), 3t(t−1), t(t−1), 3t(t−1)^2, t(t−1)^2.

Every scale is nonzero for t>1. Select the columns

(0,1),(0,5),(0,6),(0,7),(1,2),(1,7),(1,8),(2,3),(2,9),(3,4),(3,10),(4,11).

The exact 12×12 matrix is recorded below; its entries follow from the local determinant formula of Section 2 and the stated scalings. Its determinant is

27 t^3(t−1)^13(t^2+t−1).

The determinant can be checked without a symbolic-algebra program. Expand successively at the single surviving entries in original rows 6,7,9,10,11,12,5,4,3. The remaining rows are 1,2,8 and the remaining columns are 1,4,6. The accumulated signed factor is −27t(t−1)^11, and the residual matrix is

\[
\begin{pmatrix}
-t(t-1) & t^2(t-1) & 0\\
-(t-1)^2 & 0 & t^3\\
0 & -(t-1) & -1
\end{pmatrix}.
\]

Its determinant is −t²(t−1)²(t²+t−1), yielding the displayed formula. Every factor of the final positive determinant is positive for t>1. Therefore the family is universally quartic-Hermite-interpolating despite its deliberately closed collinear support. This is an exact whole-family exclusion, not a numerical experiment at a few meshes.

## Verification and limits

The stated ranks and determinant were obtained with exact rational and symbolic arithmetic. The reduced criterion was compared with a separately assembled full Bernstein–Bézier system on Qiu's mesh, a single triangle, a singular four-star, a nonsingular four-star, and three rational members of the family. These finite checks support the algebraic verification; the general reduction is established by the derivation above, and the all-real-parameter family result uses the displayed symbolic determinant.

The cubic and quartic assertions remain separate. The above work establishes no quartic counterexample and no universal fixed-mesh quartic theorem. The unresolved interface is the existence or impossibility of a geometrically valid cycle-balanced closed row component with a nonzero local jet form.

## Exact family minor

Rows are ordered O_0,…,O_5,I_0,…,I_5 and columns are listed above.

```text
[-t**2 + t, t**2 - 2*t + 1, -t**3, t**3 - t**2, 0, 0, 0, 0, 0, 0, 0, 0]
[-t**2 + 2*t - 1, 0, 0, 0, t**2 - t, t**3, -t**3 + t**2, 0, 0, 0, 0, 0]
[0, 0, 0, 0, t**2 - 2*t + 1, 0, 0, -t**2 + t, t**3 - t**2, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, -t**2 + 2*t - 1, 0, t**2 - t, -t**3 + t**2, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, -t**2 + 2*t - 1, 0, -t**3 + t**2]
[0, -t**2 + t, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, -3, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 1 - t, 0, -1, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 3 - 3*t, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 1 - t, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3*t - 3, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, t - 1]
```
