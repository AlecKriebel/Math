# Two-dimensional tiling lane: rigorous obstructions, not a solution

Target: the fixed-triangle three-color avoidance problem in `SCOPE.md`. Reflections and all boundary points are included. These are authored deductions for this attempt; no claim of literature novelty is made.

## Results

1. The natural three-color square checkerboard c(x,y) = (floor(x/a) + floor(y/a)) mod 3 necessarily contains every triangle whose minimum width h satisfies h < a/sqrt(2). This holds regardless of how large the longest side is compared with a. The monochromatic witnesses can be chosen strictly away from all boundaries.
2. More generally, **no finite menu of regular three-color tilings can avoid every short-base isosceles triangle with equal sides 1**. Here regular means locally constant away from a closed nowhere-dense boundary set. The proof is explicit and covers periodic polygonal grids, hexagonal tilings, and nonperiodic locally finite polygonal tilings.
3. These obstructions do not rule out shape-dependent tilings with increasingly fine cells. They do rule out solving the flat limit by choosing from a fixed finite catalog of regular tilings.

## 1. Exact witness for the square checkerboard

Fix a > 0. Let T have a side chosen as base, with coordinates (0,0), (L,0), (p,h), where 0 < h < a/sqrt(2). In particular, choosing a longest side makes h the minimum width of T.

Set e = (1,-1)/sqrt(2), n = (1,1)/sqrt(2). For a parameter t, define

A = (t,a-t), B = A + L e, C = A + p e + h n.

This is an exactly congruent copy, with the same side lengths and orientation up to a rigid rotation. A and B have coordinate sum a. At every point (x,y) on x+y=a except lattice vertices, floor(x/a)+floor(y/a)=0. Thus A and B have color 0 whenever neither is a lattice vertex.

Write S = a + sqrt(2) h. The assumed bound gives a < S < 2a. C has coordinate sum S. Choose t so that C_x lies in the nonempty open interval (S-a,a). Then 0 < C_x < a and 0 < C_y = S-C_x < a, so C lies inside the fundamental square and has color 0. As t varies, C_x varies with slope 1, so the allowable parameters form a nonempty open interval. Exclude the discrete parameters where A or B is a lattice vertex. There remain admissible parameters, and all three vertices are strictly inside square cells.

Thus every such T occurs monochromatically, not merely a sampled orientation or a numerically close approximation. Reflection of T is unnecessary to this counterexample; failure for this one permitted orientation is sufficient.

### Concrete rational example

For unit squares (a=1), use A=(1/4,3/4), B=(41/4,-37/4), C=(531/100,-419/100). The three sums of floor coordinates are respectively 0, 10-10=0, and 5-5=0. Hence all three have color 0.

The base length is 10 sqrt(2); C lies at the base midpoint plus (3/50,3/50), so its height is 3 sqrt(2)/50. Both equal sides have squared length 50 + 9/1250 = 62509/1250. All coordinates have positive distance from grid boundaries. This is an exact flat isosceles counterexample, not a discretized simulation.

### Consequence and precise remaining gap

For a triangle of minimum width h, this checkerboard can possibly avoid it only if a <= sqrt(2) h. This is necessary, not sufficient. Nothing here proves that any such small a works, or that no such a works. Attempting to optimize a still leaves infinitely many orientations and arbitrarily remote cells to certify.

## 2. Finite regular-tiling menus fail in the flat limit

### Lemma: explicit non-three-colorable unit-distance graph

Let A=(0,0), B=(1,0), C=(1/2,sqrt(3)/2), D=(3/2,sqrt(3)/2). The five edges AB, AC, BC, BD, CD all have length 1. In every proper three-coloring of these edges, A and D have the same color: the triangle ABC uses all three colors, and D is adjacent to B and C.

Let R be the rotation with cosine 5/6 and sine sqrt(11)/6. Add B'=RB, C'=RC, D'=RD and the corresponding five diamond edges sharing A. Since |D|^2=3, |D-D'|^2=2*3*(1-5/6)=1. Add the unit edge DD'. Each diamond would force D and D' to have A's color, contradicting DD'. This is the seven-vertex Moser-spindle argument, proved here rather than assumed.

### Theorem

Let c_1,...,c_N be colorings R^2 -> {0,1,2}. Suppose for each i there is a closed nowhere-dense set F_i such that c_i is locally constant on R^2 minus F_i. Then there exists epsilon > 0 such that, for every 0 < b < epsilon, **each** c_i has a monochromatic triangle with side lengths (1,1,b).

### Proof

Fix i. Let V be the seven vertices of the unit-distance graph above. The set of translations z for which at least one z+v lies in F_i is the finite union over v in V of F_i-v. A finite union of closed nowhere-dense sets is nowhere dense. Choose z outside it. Then all seven translated vertices are points of local constancy.

The graph is not properly three-colorable, so some unit-distance edge XY has c_i(X)=c_i(Y). Because Y is off F_i, there exists rho_i > 0 such that every point in the open disk B(Y,rho_i) has this same color.

For every 0 < b < min(rho_i,2), the circles of radius 1 centered at X and radius b centered at Y intersect in two points Z. Indeed |X-Y|=1 and the strict triangle inequalities are 0 < b < 2. Either point Z has |X-Z|=1 and |Y-Z|=b; since b<rho_i, it has the same color as Y and X. This is a nondegenerate isosceles triangle with exactly the required lengths. Both mirror orientations exist and are monochromatic.

Take epsilon = min_i min(rho_i,2) > 0. This works simultaneously for the finite menu. QED.

### Applicability and limitations

The boundary sets of ordinary periodic square, triangular, or hexagonal cell tilings are closed and nowhere dense, regardless of how their boundary points are assigned colors. The witnesses above avoid those boundaries, so changing boundary conventions cannot repair the failure.

The theorem does not assume periodicity or measurable color classes. It does assume local constancy off a closed nowhere-dense set. It does not apply automatically to every arbitrary pathological coloring permitted by the original conjecture.

Most importantly, it fixes the finite menu before b tends to zero. The conjecture permits a new coloring for each b. Interchanging these quantifiers would be invalid. A family c_b may have its interior radii shrink with b, and the proof imposes no contradiction on that possibility.

## 3. Source cross-check

Directly inspected: Aichholzer and Perz, *Triangles in the colored Euclidean plane*, EuroCG 2019 extended abstract/preprint, https://www.eurocg2019.uu.nl/papers/10.pdf, local recovery copy. Section 3 states known stripe coverage using the second-longest side M <= 2h, and non-obtuse triangles with shortest side at least half the longest. It also gives a four-color hexagonal construction. No three-color square construction or resolution of the general three-color conjecture is claimed here.

The source inspection prevents counting the broader known stripe families as new progress. This lane deliberately concerns genuinely two-dimensional checkerboard and general regular-tiling limitations; another lane handles exact stripe classification.

## Verdict

**No complete construction obtained.** The deliverables are rigorous counterobstructions to two tempting shortcuts: coarse three-color square grids, and any fixed finite regular-tiling catalog. What remains is a triangle-dependent three-color construction, or an obstruction strong enough to rule out all colorings for a specific triangle. Neither has been established.
