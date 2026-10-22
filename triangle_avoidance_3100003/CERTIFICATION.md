# Exact certification of a supplied periodic polygonal coloring

Prepared 2026-10-20. Independent certification lane for queue 1817 / AMR-030-0003. Read against `SCOPE.md`. This is an authored verification method and an explicit rejection of one concrete candidate, not a resolution of the general conjecture. No external publication is part of this lane.

## Results

1. An algebraically specified periodic polygonal three-coloring can be checked exactly for avoidance of one algebraic triangle, including all translations, rotations, reflections, and boundary points.
2. For convex polygonal pieces, the check reduces to linear elimination followed by univariate quadratic sign tests. A general real-algebraic decision procedure is available but unnecessary here.
3. The natural square-cell candidate `c(x,y) = (floor(x)+floor(y)) mod 3` fails on the entire isosceles family with vertices `(0,0), (3,0), (3/2,h)` for `0<h<2`. This includes arbitrarily flat, nondegenerate triangles. An exact interior witness is supplied below.

## 1. Required finite input

Let `L` be an invertible 2-by-2 matrix of real algebraic numbers. Its columns generate the period lattice. Use the half-open fundamental parallelogram

`F = { L t : 0 <= t_1 < 1, 0 <= t_2 < 1 }`.

Supply finitely many disjoint semialgebraic polygonal pieces `Q_j` partitioning F, each assigned a color in `{0,1,2}`. Each piece is a conjunction of affine equalities and strict or non-strict affine inequalities with real algebraic coefficients. Nonconvex polygons must first be decomposed into convex pieces, keeping their assigned color. Edges and vertices can be separate lower-dimensional pieces; the format does not require each piece to have interior.

The corresponding plane coloring assigns to `z` the color of the unique piece containing `z-Ln`, where `n = floor(L^{-1}z)` componentwise. This specifies the coloring on every point, not just almost everywhere.

If the candidate is initially described by overlapping closed tiles, it is not yet a valid finite input: supply exact ownership of every shared edge and vertex. A prescribed ordering of tile owners can be converted into a finite Boolean combination of affine tests, then split into conjunctions. Validate that the pieces are disjoint and cover F by exact linear feasibility, including strict inequalities. A candidate with unassigned points or conflicting colors fails this input-validation stage.

Write the triangle, after a fixed isometry, as

`p_0=(0,0), p_1=(d,0), p_2=(a,b)`, where `d>0` and `b>0`.

All coordinates are algebraic. Algebraic side lengths suffice: take `d=|p_0p_1|`, `a=(d^2+|p_0p_2|^2-|p_1p_2|^2)/(2d)` and the positive square root `b=sqrt(|p_0p_2|^2-a^2)`.

## 2. Exact compact reduction and finite offset bound

A monochromatic copy can be translated by a lattice vector so its labeled first vertex lies in F. No orientation or reflected copy is lost. For `e in {-1,+1}`, set

`R_e(u,v) = [[u,-e v],[v,e u]]`, with `u^2+v^2=1`.

These are exactly the orthogonal matrices, with determinant e. Its other vertex displacements are

`q_1=(du,dv)`,
`q_2=(au-e bv, av+e bu)`.

Let `r_i` be row i of `L^{-1}`. For vertex index `ell=1,2`, put

`M_(i,ell) = ||r_i||_2 ||p_ell||_2`,
`N_(i,ell) = ceil(M_(i,ell))`.

The ceiling is computed exactly from algebraic numbers, or replaced by any certified integer upper bound. If the first vertex has lattice coordinates `t in [0,1)^2`, the tile offset of vertex ell is

`n_(i,ell) = floor(t_i + r_i q_ell)`.

Cauchy–Schwarz gives `|r_i q_ell| <= M_(i,ell)`. Consequently

`-N_(i,ell) <= n_(i,ell) <= N_(i,ell)`.

For the upper bound, `t_i+r_i q_ell < 1+M_(i,ell) <= 1+N_(i,ell)`, so its floor is at most N. For the lower bound it is at least `-M >= -N`. Thus the finite list is valid even when the norm bound is attained and M is an integer. The offset of the first vertex is zero.

For every e, every same-colored triple of pieces `(Q_j0,Q_j1,Q_j2)`, and every pair of offsets in those finite boxes, test the following existential system:

`x in Q_j0`,
`x+q_1-Ln_1 in Q_j1`,
`x+q_2-Ln_2 in Q_j2`,
`u^2+v^2=1`.

Here x has two real coordinates. All non-circle constraints are affine in `(x_1,x_2,u,v)`, with precisely the supplied strictness. This is already a complete finite semialgebraic feasibility test.

## 3. Specialized exact solver: linear projection and quadratics

For a fixed tuple above, eliminate `x_1,x_2` by Fourier–Motzkin elimination over the real algebraic coefficient field. Convert each equality into two non-strict inequalities if convenient. At each elimination step, compare every lower bound with every upper bound. The resulting comparison is strict if either contributing bound is strict, and non-strict otherwise. Preserve all inequalities independent of the eliminated variable. If one side has no bounds, there is no pairwise comparison from that side: the variable can be chosen sufficiently far in the unbounded direction. Handle constant contradictions explicitly.

This strict version is exact for finite systems over the reals: when lower and upper extremal bounds differ, choose an intermediate value; when they agree, equality is allowed precisely when every active endpoint permits equality. The output is a conjunction of affine constraints on `(u,v)` alone. No rounding, epsilon relaxation, or closing of open polygons is permitted.

Use the rational parameterization

`u=(1-z^2)/(1+z^2), v=2z/(1+z^2)`.

It covers the unit circle except `(-1,0)`, which must be tested separately. For example, a projected constraint

`alpha u + beta v <= gamma`

becomes

`(-alpha-gamma) z^2 + 2 beta z + (alpha-gamma) <= 0`.

The same calculation preserves `<`, since `1+z^2` is strictly positive. Therefore each tuple reduces to a conjunction of quadratic, linear, and constant sign constraints in one real variable.

An exact test isolates and orders every real root of the nonzero polynomials, tests each root, and tests one point in every intervening open interval, including both unbounded intervals. Each polynomial has constant sign on each open interval. Zero polynomials and constant constraints are handled separately. All computations are over real algebraic numbers. A rational sample exists between any two distinct real roots and can be found by certified isolating intervals. The omitted circle point is checked in the projected affine constraints directly.

If feasible, reconstruct x by back-substitution through the elimination steps, choosing algebraic values satisfying the exact lower and upper bounds. This gives an exact monochromatic witness, including its handedness, translated coordinates, and tile ownership. If every tuple is infeasible, the candidate avoids the triangle.

## 4. Why the procedure is sound and complete

Soundness of rejection: a feasible tuple gives three vertices related to the supplied triangle by the explicit orthogonal map and translation. Their membership tests place them in same-colored cells of the actual total coloring, including boundary assignments.

Completeness of rejection: take any monochromatic congruent copy, label its vertices according to the supplied triangle, and translate its first vertex into F. Its orthogonal map has one of the two displayed forms; its other vertices have offsets within the proved finite boxes; the exact partition assigns unique cell indices. Hence one enumerated tuple is feasible.

The strict linear projection, the circle parameterization together with its omitted point, and the root/sign decomposition are each equivalences. Thus their composition decides exactly this fixed candidate's avoidance property.

A checkable acceptance record can contain the finite-input partition validation, algebraic-number representations, offset bounds, projected inequalities, and each tuple's root/sign infeasibility table, plus the direct test at `(-1,0)`. An independent implementation can replay these steps. A bare solver's success message is weaker evidence than such a replayable record.

## 5. Exact rejection of a concrete flat-triangle candidate

Consider the square-cell coloring

`c(x,y) = (floor(x)+floor(y)) mod 3`.

The period matrix may be chosen as `L=3I`. Its fundamental cell has nine unit-square pieces

`Q_ij = [i,i+1) x [j,j+1)`, `i,j in {0,1,2}`,

of color `(i+j) mod 3`. This is a genuine total periodic three-coloring, with standard half-open ownership.

For any `0<h<2`, consider

`T_h = {(0,0),(3,0),(3/2,h)}`.

Translate without rotation by

`t=(3/4,1-h/2)`.

The three resulting vertices are

`A=(3/4,1-h/2)`,
`B=(15/4,1-h/2)`,
`C=(9/4,1+h/2)`.

Because `0<h<2`, the first two y-coordinates lie strictly between 0 and 1, and the third lies strictly between 1 and 2. The containing global square indices are therefore

`A: (0,0)`, `B: (3,0)`, `C: (2,1)`.

Their index sums are 0, 3, and 3, respectively, so all three vertices have color 0. All vertices lie strictly inside their squares. No convention on edges or vertices can repair this counterexample.

For the explicit rational flat triangle `h=1/10`, the witness is

`A=(3/4,19/20)`, `B=(15/4,19/20)`, `C=(9/4,21/20)`.

Squared pairwise distances are exactly

`|A-B|^2=9`, `|A-C|^2=|B-C|^2=113/50`.

These equal the squared side lengths of `T_(1/10)`, whose altitude/base ratio is `1/30`. Its avoiding failure has a positive local margin: each witness point is at least `1/20` from every horizontal square boundary and at least `1/4` from every vertical boundary. Common coordinate perturbations of the translation with absolute value less than `1/20` preserve every containing cell.

For this triangle and `L=3I`, the general offset bound gives, for p_1, `M=1` and `N=1` in each coordinate; for p_2, `M=sqrt(113/50)/3 < 1` and again `N=1`. The concrete tuple is

`e=+1, (u,v)=(1,0)`,
`Q_j0=Q_00, n_0=(0,0)`,
`Q_j1=Q_00, n_1=(1,0)`,
`Q_j2=Q_21, n_2=(0,0)`.

The witness anchor belongs to F. This tuple passes the exact membership constraints and is within the finite offset enumeration.

## 6. Research implications and limitations

- This rejects a concrete plausible square periodic coloring, not all square tilings, not all periodic colorings, and certainly not all three-colorings.
- The same example shows why coarse translation sampling is unreliable for very flat triangles: the exhibited translation window in the vertical direction narrows with h. A positive-width interior witness exists for every h>0, but need not coincide with a selected sample grid.
- Boundary conventions matter to a positive acceptance proof even though this negative witness is independent of them.
- A finite exhaustive search over a fixed parameter family can establish only that family's success or failure. It does not prove that the general conjecture has a periodic polygonal witness, nor supply a bound on lattice size, cell count, coefficient complexity, or required periods.
- The source gate's target allows arbitrary plane colorings. No regularity restriction or finite-certificate theorem for all possible avoiding colorings has been established here.

The mathematics above is self-contained. The source gate supplies problem identification and status context; no new claim about the present literature status is made in this certification lane.
