# Fixed-triangle finite obstructions: exact reductions and a square-grid impossibility

Date: 2026-10-20. Target as formalized in `SCOPE.md`: for each fixed non-equilateral nondegenerate Euclidean triangle T, 3-color all of R² without a monochromatic congruent copy, including reflections. This note contains elementary independently derived reductions, not a claimed solution or novelty claim. No external publication was performed.

## Main finding

**No finite subset of a square lattice can witness failure of the target, for any triangle T. In fact its fixed-T congruence hypergraph is always 2-colorable.** This applies to every lattice scale, translation, and rotation, not just a bounded computational grid. Consequently increasing a square-grid search indefinitely cannot produce a 4-chromatic obstruction. This is a structural failure of that search domain, not merely insufficient computing power.

### Explicit dyadic coloring proof

Work first on Z² and fix a positive squared distance n represented by a sum of two integer squares. Write its 2-adic valuation as v₂(n)=2k+ε, where ε is 0 or 1, and put q=2^k.

If a²+b²=n, then a and b are divisible by q. After division by q, their parities differ when ε=0, and both are odd when ε=1. To see this, remove the largest common power of two from a,b: the remaining sum of squares has valuation 0 if precisely one coordinate is odd, and valuation 1 if both are odd.

Define a two-coloring of every integer point by

- ε=0: C(x,y)=(floor(x/q)+floor(y/q)) modulo 2;
- ε=1: C(x,y)=floor(x/q) modulo 2.

For an edge whose coordinate difference is (a,b), divisibility by q gives floor((x+a)/q)-floor(x/q)=a/q, including for negative coordinates. Thus the color difference is (a+b)/q modulo 2 in the first case and a/q modulo 2 in the second, always 1. This properly 2-colors the distance-n graph.

For a triangle T that occurs on Z², choose any one of its side lengths and its positive integer squared value n. Every congruent copy has an edge at that distance, whose endpoints have different colors. Thus no such copy is monochromatic. If T has no copy on Z², any coloring suffices. Pull back through a similarity to obtain the assertion for every square lattice. Restriction to any finite subset preserves it.

### Extension to all rational-coordinate samples and to Q²

Every finite subset X of Q² can be multiplied by a common positive denominator to lie in Z². Applying the preceding argument to the simultaneously scaled fixed triangle shows that H_T[X] is 2-colorable for **every** T, whether or not T has rational-coordinate vertices. Applying the same compactness argument as below with two colors shows that the entire fixed-T hypergraph on Q² is 2-colorable. The same holds on every similarity image of Q².

Therefore even arbitrary finite rational point clouds, not just regular grid windows, cannot yield a counterexample. Any finite non-3-colorable realization would have to fail to lie in every similarity image of Q². No finite search is used in this corollary’s proof.

### Exact check, only as a sanity check

`check_square_grid.py` implements the formulas using integer arithmetic and checks every unordered pair in {-8,...,8}², choosing the formula for that pair's squared distance. Output:

    PASS: 41616 pairs; 134 distinct squared distances; 289 points.

The coloring depends on the fixed distance n; this test does not assert that one coloring simultaneously separates all distances. The proof above, rather than this finite check, establishes the general result.

## Compactness: what a decisive finite test actually means

Let H_T have vertex set R² and one unordered triple for every congruent copy of T. For finite X⊂R², let H_T[X] contain **all** such triples lying in X. Then the following are equivalent, in the usual classical set-theoretic framework:

1. There is an unrestricted 3-coloring of the plane avoiding T.
2. Every finite induced hypergraph H_T[X] is weakly 3-colorable (no monochromatic hyperedge).

The forward implication is restriction. For the reverse, use the compact product {1,2,3}^{R²}. Each triple imposes a closed cylinder constraint excluding its three constant assignments. A finite collection of constraints involves only finitely many points and is satisfiable by assumption, so the constraints have the finite intersection property. Compactness gives a simultaneous satisfying coloring.

Equivalently one can use propositional compactness with three color variables per point and exactly-one-color constraints. The result does not give measurable, periodic, continuous, or computationally describable colorings.

In particular, a counterexample triangle has a **finite** congruence hypergraph that is not 3-colorable. It need not lie on a square lattice, have rational coordinates, or arise from any prescribed finite list of orientations. A successful coloring of one finite sample, or even of every sample in a restricted family, does not establish premise 2.

## Elementary necessary conditions on a finite counterexample

Suppose X is vertex-minimal among finite sets whose fixed-T hypergraph is not 3-colorable.

### Minimum degree at least three

Every vertex belongs to at least three hyperedges. Otherwise color X minus that vertex. Each incident triple forbids at most one color for the missing vertex: it forbids a color only if its other two vertices have that common color. At most two forbidden colors leave a valid extension, contradiction.

Therefore, writing N=|X| and E for its hyperedges, 3|E|=sum_v deg(v)≥3N, so |E|≥N. This is necessary, not sufficient.

### At least nine vertices

Every five distinct planar points contain a triple not congruent to T. Indeed, if every triple were congruent, all triangular perimeters would be equal. For any two vertices i,j, use the remaining three vertices k,l,m. Subtracting equal perimeters on (i,k,l) and (j,k,l), and similarly on (k,m) and (l,m), gives

    δ_k+δ_l=δ_k+δ_m=δ_l+δ_m=0,
    where δ_r=d(i,r)-d(j,r).

Hence each δ_r=0. Varying i,j shows all pairwise distances are equal. Five equidistant distinct points cannot lie in R² (indeed there are at most three).

For any eight-point set, choose a nonedge triple; the remaining five points contain another nonedge triple. Assign one color to each triple and a third color to the remaining pair. This is a valid 3-coloring. Any smaller point set can be padded to eight distinct planar points and the coloring restricted. Thus any finite counterexample requires N≥9.

### Pair-codegree at most four

Fix two distinct points p,q. If their distance is not a side length of T they have codegree zero. Otherwise a third point has an ordered pair of distances to (p,q) obtained from the remaining two sides. There are at most two distinct ordered pairs, each giving at most two circle intersections. Thus at most four hyperedges contain p,q. This also holds for isosceles triangles with repeated lengths. For an equilateral triangle the bound improves to two. Consequently 3|E|≤4 binom(N,2); this coarse bound alone does not imply 3-colorability.

## A second grid blind spot: exact representability

Even having an edge is exceptional for square-grid searches. Orient and scale a triangle so one side has endpoints 0 and 1 in the complex plane and the third point is z=x+iy with y≠0. The triangle embeds in some square lattice up to similarity if and only if x,y are rational.

Necessity: in a lattice embedding, the nonzero baseline and the third-point displacement are Gaussian integers u,v after rescaling the lattice, and z=v/u belongs to Q(i). Sufficiency: clear denominators of x,y. Reflection only replaces y by -y and does not change the criterion. Relabeling vertices also does not change membership in Q(i), since the other normalizations are rational fractional transformations of z.

For baseline length c, adjacent third-point distance b, opposite distance a, and area Δ, these conditions read

    x=(b²+c²-a²)/(2c²) ∈ Q,
    |y|=2Δ/c² ∈ Q.

For example T={(0,0),(1,0),(0,2^(1/4))} has squared side lengths 1, sqrt(2), and 1+sqrt(2). No congruent copy lies in any square lattice, at any orientation or scale, because ratios of squared lattice distances are rational. Even on the dense set Q² the congruence hypergraph for this particular scale of T is empty: its irrational squared sides cannot occur there.

Thus density does not justify perturbing exact finite configurations into a rational grid. Congruence is an equality constraint; approximate copies are not copies.

## What would advance this lane

A useful negative search must leave the single-square-lattice domain, for example by assembling exact congruent triangles under noncommensurate rotations and translations, retaining exact coordinates and all induced edges. A 4-chromatic result would need a checkable non-3-colorability certificate and verified exact geometry. A positive compactness proof would need a structural 3-colorability theorem for every finite realizable configuration, not just those generated by one construction.

This note supplies neither. It closes one unsuitable search avenue, gives precise constraints for any future obstruction, and leaves the full plane conjecture unresolved.
