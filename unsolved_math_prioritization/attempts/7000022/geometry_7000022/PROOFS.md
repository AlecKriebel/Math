# Proofs and exact controls

## 1 Conventions and classical inputs

Let `gamma : [0,1] -> R^3` be continuous, rectifiable, and closed, with traversal length `L`. Let `K = conv(gamma([0,1]))`. The functional `S(K)` is the intrinsic-volume extension of boundary area: ordinary boundary area in dimension three, twice planar area in dimension two, and zero in dimensions zero and one. We write `A = S(K)`.

For a unit vector `u`, let `K_u` be the orthogonal projection onto `u^perp`. Write `B(u)` for its planar area, `p(u)` for its perimeter (twice length for a segment), and `ell(u)` for the traversal length of the projected curve. Let `E` denote averaging over the unit sphere with probability measure `domega/(4*pi)`.

The classical inputs used below are the planar isoperimetric inequality, the planar Cauchy perimeter formula, the three-dimensional Cauchy projection formula, the spherical Poincare inequality, and, only for the known boundary case, Weil's isoperimetric inequality for intrinsic disks of nonpositive curvature. These established results are not claimed as new. The needed Cauchy surface formula is proved first for polyhedra below, which also provides the continuity and degenerate conventions needed for approximation. Standard smooth approximation of support functions is used in Section 4; no regularity of `K` is silently assumed.

## 2 Polygonal reduction and a sharp four-vertex bound

### 2.1 Cauchy formula and continuity

For a full-dimensional convex polyhedron with face areas `a_i` and outward unit normals `n_i`, its projected area is

`B(u) = (1/2) * sum_i a_i * |n_i . u|`.

Indeed, outside projected edges, a line parallel to `u` meeting the body meets one visible and one hidden face; projection multiplies each face area by `|n_i . u|`. The two coverings give the factor one half. Since `E|n . u| = 1/2`, integration gives

`S(K) = 4 E B(u)`.

For full-dimensional convex sets, the same identity is the classical Cauchy surface formula; the polyhedral calculation fixes its normalization. For clarity, the right side itself gives the continuous extension to lower dimension. Planar convex area is continuous under Hausdorff convergence: one can enclose a bounded planar convex set in an arbitrarily small parallel neighborhood and use the planar Steiner formula, or approximate it from inside and outside by polygons. Orthogonal projection is Hausdorff-continuous. For convex sets in a common bounded ball, projected areas have a common bound, so dominated convergence applies. Therefore `4 E B(u)` is Hausdorff-continuous. For a planar body of area `b` and normal `n`, `B(u)=b|n.u|`, giving `S=2b` exactly. For a segment, all projected areas vanish.

### 2.2 Polygonal equivalence and existence

Take increasingly fine ordered samples of a closed curve and join consecutive samples by straight chords. The resulting closed polygonal curves converge uniformly to the original curve and have lengths `L_j <= L`. Their convex hulls converge in Hausdorff distance: if sets are within distance `epsilon`, their convex hulls are within that distance by taking corresponding convex combinations. Section 2.1 then gives convergence of surface areas.

Consequently, if `S(conv P) <= length(P)^2/(2*pi)` holds for every closed polygonal curve, then it holds for every closed rectifiable curve. The converse is immediate. Curves with zero length have zero area.

A maximizer among loops with `L <= 1` exists. Translate a base point to the origin, and parameterize each loop on `[0,1]` with constant speed at most one. All loops are uniformly Lipschitz and bounded. Arzela-Ascoli gives a uniformly convergent subsequence; the limit is closed, has length at most one, and its hull area is the limit by Section 2.1. The supremum is finite, for example by Section 3, and is positive because of circles. A maximizer cannot have length strictly between zero and one: rescaling it to length one would strictly increase area. Thus it has length one. This establishes existence only, not planarity or optimality of the circle.

### 2.3 Four vertices

**Proposition.** If `K` has at most four extreme points, then `S(K) <= L^2/8`. The coefficient `1/8` is sharp in this class, with the doubled square as an example.

Every extreme point of the convex hull of a compact set belongs to that set. To see this, use Caratheodory's finite convex-combination representation; extremality forces every point with positive weight to be the extreme point itself. Select one visit of the curve to each of its at most four extreme points, and order the selected visits cyclically. Join consecutive selected points. The resulting polygon has the same hull and perimeter `p <= L`. Repeated vertices may be inserted if necessary.

For a nondegenerate ordered tetrahedron with cyclic edge lengths `a,b,c,d`, its four faces respectively contain consecutive edge pairs of lengths `(a,b)`, `(b,c)`, `(c,d)`, and `(d,a)`. Each triangle has area at most one half the product of those two lengths. Hence

`S(K) <= (ab+bc+cd+da)/2 = (a+c)(b+d)/2 <= (a+b+c+d)^2/8 = p^2/8`.

The same assertion holds for coplanar or degenerate four-point configurations by perturbing their vertices to noncoplanar positions and using Section 2.1. In particular the limiting sum of the four face areas agrees with the doubled planar hull area. Since `p <= L`, the claim follows.

A square of side `a` has traversal length `4a` and doubled area `2a^2`, so it attains `S=L^2/8`. A full-dimensional tetrahedron cannot attain equality: equality in all triangle bounds requires every consecutive pair of edge vectors to be orthogonal. With cyclic edge vectors `v_1+v_2+v_3+v_4=0`, those orthogonalities imply `v_1.v_3=-|v_1|^2=-|v_3|^2`, whence `v_3=-v_1` and `v_4=-v_2`; the polygon is planar. No claim of a new theorem is made for this elementary special case.

## 3 Projection estimates and the exact Jensen obstruction

### 3.1 Perimeter comparison

For a closed planar rectifiable curve, the variation of its scalar projection in direction `v` is at least twice the width of its hull in that direction. Integrating over `v` on the unit circle and using `E_circle |T.v|=2/pi` gives

`perimeter(conv curve) <= length(curve)`.

This includes degenerate hulls with the stated perimeter convention. Apply it to the projected space curve: `p(u) <= ell(u)`. Planar isoperimetry then yields `B(u) <= ell(u)^2/(4*pi)`. Cauchy's formula gives

`A <= (1/pi) E ell(u)^2`.

Parameterize by arclength, and let `T(s)` be its almost-everywhere unit tangent. Then

`ell(u) = integral_0^L sqrt(1-(T(s).u)^2) ds`.

Since `T.u` is uniformly distributed on `[-1,1]` for fixed unit `T`,

`E ell(u) = (pi/4)L`.

Cauchy-Schwarz along the curve gives

`ell(u)^2 <= L * integral_0^L (1-(T(s).u)^2) ds`.

As `E(T.u)^2=1/3`, averaging proves

`A <= 2 L^2/(3*pi)`.

The projected-length second-moment constant `2/3` is sharp for closed parametrized curves: take a segment of length `L/2`, traversed once in each direction. Then `ell(u)=L sqrt(1-(e.u)^2)` and therefore

`E ell(u)^2 = (2/3)L^2`, whereas `(E ell(u))^2=(pi^2/16)L^2`.

Thus replacing the second moment by the square of the mean reverses Jensen's inequality. Even more basically, for every nonzero closed rectifiable curve, Jensen gives

`E ell(u)^2 >= (pi^2/16)L^2 > L^2/2`.

Therefore the bound on `E ell^2` that would make the preceding length-only route sharp is impossible for every nonzero curve, including circles. The projection isoperimetric deficits cannot all be discarded.

### 3.2 The exact missing deficit

Define `delta(u)=p(u)^2/(4*pi)-B(u) >= 0`. Cauchy's formula gives the exact identity

`A = (1/pi) E p(u)^2 - 4 E delta(u)`.

Accordingly, the full target is equivalent to

`4*pi E delta(u) >= E p(u)^2 - L^2/2`.

This equation is a precise description of the missing global geometric estimate, not a proof of it. Even a circle has generally elliptical, rather than circular, projections; their positive planar deficits are essential. A moment estimate alone has not recovered them.

## 4 Mean width and a better universal bound

For `u` on the sphere let `w(u)=max_t gamma(t).u - min_t gamma(t).u`, the width of `K`. The scalar function `gamma.u` is periodic. Its total variation is at least `2w(u)`, since it must travel between a maximum and minimum and return. Thus

`2w(u) <= integral_0^L |T(s).u| ds`.

Using `E|T.u|=1/2` gives the classical estimate

`wbar := E w(u) <= L/4`.

We next recall, and derive, the classical bound `S(K) <= pi*wbar^2`. Suppose first that `K` has a smooth support function `h` with positive curvature. On the unit sphere its inverse Gauss parametrization is `X(u)=h(u)u+grad h(u)`, with area Jacobian `det(Hess h+hI)`. The integrated two-dimensional determinant identity and Bochner formula on the unit sphere give

`S(K) = integral_S2 (h^2 - |grad h|^2/2) domega`.

For completeness, use `2 det M=(tr M)^2-|M|^2`. For `M=Hess h+hI`, integrate the identity; `integral ((Delta h)^2-|Hess h|^2)=integral |grad h|^2`, while `integral h Delta h=-integral |grad h|^2`. Substitution yields the displayed formula.

Let `m=(1/(4*pi)) integral h` and `f=h-m`. The first nonzero spherical eigenvalue is two, so `integral |grad f|^2 >= 2 integral f^2`. This is the usual spherical Poincare inequality, or follows by expansion in spherical harmonics with eigenvalues `j(j+1)`. Hence

`S(K) <= 4*pi*m^2 = pi*wbar^2`,

because `w(u)=h(u)+h(-u)` and `wbar=2m`. Approximate an arbitrary compact convex set by smooth strictly convex bodies using rotational smoothing of its support function followed by addition of a small ball. Support functions, mean widths, and, by Section 2.1, surface areas converge. The inequality follows for all the hulls considered here, including planar ones.

Combining the two inequalities proves

`A <= pi L^2/16`.

This coefficient is larger than `1/(2*pi)` by the multiplicative factor `pi^2/8`, approximately `1.23370055`. This package makes no assertion that `pi/16` is the best currently published bound for this specific problem.

There is also a rigorous sufficient condition. Define the mean-width slack `D=L/4-wbar >=0`. Then

`A <= pi (L/4-D)^2`.

In particular, the desired inequality holds whenever

`D >= L*(1/4 - 1/(pi*sqrt(2)))`.

The threshold is approximately `0.02492092 L`. This condition does not cover the extremal circle, whose slack is zero, and is not a replacement for the missing general argument. Zalgaller already treats the closely related mean-width/total-mean-curvature extremal problem in Section 12 of his 1996 survey.

## 5 Why boundary replacement is invalid

### 5.1 The known boundary case

For a simple polygonal loop that lies on the boundary of its full-dimensional convex hull, every vertex of the hull is on the loop. The loop separates the polyhedral sphere into two intrinsic disks. All intrinsic cone curvature lies at hull vertices, hence on the boundaries of the disks. Their interiors are flat, and each disk has boundary length `L`. Weil's classical disk isoperimetric inequality gives `area(D_i) <= L^2/(4*pi)`. Adding gives the desired bound. The planar case follows directly from planar convexification and isoperimetry. Appropriate approximation or the curvature-measure version of the disk inequality handles the established wider boundary case. Here that general extension is attributed to the source, not independently re-proved.

The additional boundary hypothesis is not part of the full target. Its removal is precisely the difficulty emphasized in [Zalgaller, Section 7](https://www.mathnet.ru/eng/aa700) and [Ghomi's 2024 formulation](https://mathoverflow.net/questions/480430/shortest-loop-through-vertices-of-a-convex-polytope).

### 5.2 Exact octahedral obstruction

Fix `h>0`. Let the equatorial vertices be `(1,0,0),(0,1,0),(-1,0,0),(0,-1,0)`, and the poles be `(0,0,h),(0,0,-h)`. Write `s=sqrt(1+h^2)`. All six points are extreme vertices of a convex octahedron. Adjacent equatorial distances are `sqrt(2)`, opposite equatorial distances are two, pole-equator distances are `s`, and the pole-pole distance is `2h`.

Any closed curve visiting these vertices has length at least that of a Hamiltonian polygon through them, by selecting one visit of each vertex and straightening intervening arcs. In a Hamiltonian cycle there are two possibilities.

- The poles are adjacent: there are two pole-equator edges and three equatorial edges. The least possible length is `L_adj=2h+2s+3sqrt(2)`, attained by an equatorial path of three adjacent edges.
- The poles are not adjacent: there are four pole-equator edges and two equatorial edges. The least possible length is `L_sep=4s+2sqrt(2)`, also attained.

Therefore the shortest Euclidean tour length is `min(L_adj,L_sep)`. Moreover,

`L_adj < L_sep` if and only if `h < 1/(2sqrt(2))`,

by squaring the positive sides in `2sqrt(1+h^2)>sqrt(2)+2h`.

Every boundary path joining the poles crosses the equatorial square boundary. If it crosses at `q`, its length is at least `2sqrt(h^2+|q|^2)`. On that square boundary the minimum of `|q|` is `1/sqrt(2)`, so the intrinsic pole-pole distance is at least

`d=2sqrt(h^2+1/2)`.

Equality holds by taking straight segments in the two adjacent triangular faces through the midpoint of an equatorial edge. All other intrinsic distances are at least their Euclidean counterparts. Consequently a boundary tour with adjacent poles has length at least `d+2s+3sqrt(2)`, and a boundary tour with separated poles has length at least `L_sep`. Since

`d+sqrt(2)>2s`

(square `sqrt(h^2+1/2)+1/sqrt(2)>sqrt(h^2+1)`), the shortest boundary tour has exactly length `L_sep`; an edge cycle attains it.

Take `h=1/10`. Then

`L_E = 1/5 + sqrt(101)/5 + 3sqrt(2)`

and

`L_boundary = 2sqrt(101)/5 + 2sqrt(2) > L_E`.

Thus no curve of the same or shorter length, lying entirely on the boundary of this same hull, can replace a shortest Euclidean tour. The Euclidean minimizer is a simple polygon and its pole-pole edge lies in the hull interior except at its endpoints. This is an obstruction even if one first restricts to simple curves.

The hull area is `A=4sqrt(1+2h^2)`, since each of its eight triangular faces has area `sqrt(1+2h^2)/2`. At `h=1/10`, the desired inequality still holds strictly. The example defeats the boundary replacement mechanism, not the conjecture. The 60 unoriented Hamiltonian cycles and the strict inequalities at this rational `h` are checked with certified rational intervals in `verify.py`.

## 6 Why a spanning-disk estimate is insufficient

Let `O=(0,0,0)` and `e_1,e_2,e_3` be the standard basis vectors. Traverse the closed polygonal walk

`O, e_1, O, e_2, O, e_3, O`.

Its length is six; its hull is the tetrahedron with vertices `O,e_1,e_2,e_3`. Three faces have area one half and the fourth has area `sqrt(3)/2`, so

`A=(3+sqrt(3))/2 > 0`.

Parameterize the walk Lipschitz-continuously on the unit circle. Define a spanning map on the closed unit disk in polar coordinates by `F(r,theta)=r*gamma(theta)`. This map is Lipschitz: away from the origin its radial derivative is bounded by `sup|gamma|`, and its angular derivative divided by `r` is bounded by the Lipschitz constant of `gamma`; continuity at the origin completes the global estimate. On each arm interval, both derivatives are multiples of the same vector `e_i`. Hence its two-dimensional Jacobian vanishes almost everywhere. Its parametrized area is zero.

The infimum of the areas of Lipschitz spanning disks is therefore zero, while its convex hull has strictly positive boundary area. An inequality asserting that hull area is at most any fixed multiple of the least spanning-disk area is false in the full class of the source problem. Consequently a classical isoperimetric upper bound on the area of a Plateau filling alone cannot prove the target. This exact example is not a counterexample to the target: `A < 36/(2*pi)`.

## 7 Precise remaining gap and conclusion

The polygonal inequality for arbitrary numbers and configurations of vertices remains unproved. Four vertices, the known hull-boundary regime, and loops with enough mean-width slack are rigorously covered, but there is no exhaustive reduction to those classes. Compactness supplies a maximizer without proving that it is planar. Projection methods still need a global lower estimate for their averaged planar deficits. The octahedron prevents simply moving an optimal fixed-hull tour to the boundary without paying additional length. The tree example prevents replacing hull area by the area of a spanning disk.

These are five substantively different approach families with explicit outputs and obstructions. None resolves the sharp general coefficient `1/(2*pi)`. No further proof search is hidden inside verification, and no positive novelty claim is made.
