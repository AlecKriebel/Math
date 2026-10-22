# Large boundary lattice squares: five bounded approaches

Target: UnsolvedMath numeric ID 30001694, descriptor OWR-4798-010.
Date: 2026-10-05. Status: partial results only; the universal target is not resolved.

## Exact mathematical target

Let C be a finite nonempty set of unit cells [i,i+1]×[j,j+1], with i,j integers. Their union P must have boundary J that is one Jordan curve. Thus disconnected unions, holes and boundary self-touching are excluded. Let s be the largest side length of an open axis-parallel square contained in int(P). Write B=J∩Z². Let M² be the largest squared side length of a square with four distinct vertices in B, with M=0 if none exists. The target is

    2 M² ≥ s².

Equivalently, when s=2m the required side is at least s/√2, and when s=2m+1 it is at least √(m²+(m+1)²). The equivalence follows because a lattice square's squared side is an integer and ceil((2m+1)²/2)=m²+(m+1)². Size here is Euclidean SIDE LENGTH, not diameter, area, perimeter, or number of cells. The required square may be rotated. Only its vertices must lie on J; its edges and interior are not required to lie in P.

The original is Tverberg's Conjecture 1 on printed p.362 of OWR 08/2011. Pettersson, Tverberg and Östergård's 2014 Conjecture C is the same target. Their Theorem 4 reports the bounding-box range o(J)≤13. We do not claim that any results below supersede it, or that our elementary proofs are novel. The original problem webpage itself could not be inspected; the current descriptor-to-original mapping is supported by the supplied catalog and the primary OWR statement, not by a successful live-page read.

## Approach 1: largest filled blocks and the contact obstruction

### Lemma 1.1 (integer block reduction)
The number s is a positive integer, and is attained by an integer-aligned s×s block of cells.

Proof. Suppose (a,a+t)×(b,b+t) is contained in int(P). Every unit cell whose interior intersects this open square belongs to C: otherwise any point in that intersection would be outside P. These cells form the full rectangle with integer-coordinate closure

    [floor(a),ceil(a+t)] × [floor(b),ceil(b+t)].

Its open interior is contained in int(P), since all of its cells are filled. Its two integer side lengths are at least t. Hence it contains an integer-aligned open square of integer side at least t. The finite cell set has a largest filled square block, so this block attains the optimum over arbitrary real a,b,t. Positivity follows from any one cell. ∎

This reduction turns the target into an exact finite condition for each individual polyomino. It does NOT make the four corners of a maximizing block boundary points.

### Counterexample 1.2 (the maximum block is not a boundary square certificate)
Take the seven cells with lower-left corners

    (0,0),(0,1),(1,0),(1,1),(1,2),(2,1),(2,2).

They are edge-connected and their exposed-edge graph is one simple cycle. There is a filled 2×2 block with lower-left corner (1,1). There is no filled 3×3 block, since the containing 3×3 box is missing cells. Lemma 1.1 gives s=2. The point (1,1), a corner of the displayed maximum block, is interior to P because its four incident cells (0,0),(1,0),(0,1),(1,1) are present. Thus those four block corners are not all in B. The exact geometry is also checked by the independent replay program. ∎

### Counterexample 1.3 (axis-aligned boundary squares can all be absent)
Take cells

    (0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1).

This is mask 886 in the certificate encoding, and has s=2. Its boundary lattice points, by horizontal row, are

    y=0: x∈{1,2,3}; y=1: x∈{0,1,3};
    y=2: x∈{0,2,3}; y=3: x∈{0,1,2}.

An axis-aligned lattice square of side d requires two rows distance d apart with two common x-coordinates distance d apart. For d=1 the intersections are {1,3}, {0,3}, {0,2}; none contains a pair distance 1. For d=2 the intersections are {2,3}, {0,1}; neither contains a pair distance 2. For d=3 the intersection is {1,2}; it contains no pair distance 3. The bounding box excludes d>3. Thus no axis-aligned lattice square exists on B. Nevertheless the points (1,0),(3,1),(2,3),(0,2), in that cyclic order, form a square: their consecutive vectors are (2,1),(-1,2),(-2,-1),(1,-2), with squared side 5. So this example is not a counterexample to the target. The exact checker finds M²=5. ∎

Missing statement for this route: from a largest filled s-block and the entire surrounding simple boundary, force a rotated four-point lattice configuration with 2M²≥s². Neither maximum-block corners nor axis-only searching suffices.

## Approach 2: continuous-square optimization and lattice rounding

The following known reduction is credited to Pettersson–Tverberg–Östergård, Theorem 2. A complete algebraic proof is retained to specify exactly what it does and does not imply.

### Lemma 2.1 (no loss in the maximum when restricting to lattice vertices)
If any square has its vertices on a finite union of unit grid edges J, then a square of at least the same side length has all four vertices in J∩Z².

Proof. Write a square's cyclic vertices as

    A=(x,y), B=(x+a,y−b), C=(x+a+b,y+a−b), D=(x+b,y+a).

No sign restriction on a,b is needed, so arbitrary cyclic relabeling is permitted. Every vertex has an integer x-coordinate or integer y-coordinate. Select one such coordinate for each vertex. There are three cases, allowing interchange of x and y.

1. At least three selected y-coordinates are integers. Three cyclic vertices may be called A,B,C. Their y-coordinates y,y−b,y+a−b imply that y,a,b are integers; the fourth y-coordinate is then integer too. All four x-coordinates have the same fractional part. If this part is zero, done. Otherwise each vertex lies in the interior of a horizontal unit edge of J. Translate all four vertices horizontally by ceil(x)−x. They move along those edges to their right endpoints. Side length is unchanged and all vertices are lattice points.

2. Exactly two selected x-coordinates occur at adjacent vertices. Relabel them A,B, leaving y-coordinates selected at C,D. The integers x,x+a,y+a−b,y+a imply a,b,y∈Z. All coordinates were already integers.

3. Exactly two selected x-coordinates occur at opposite vertices, say A,C. The selected integer coordinates are x,x+a+b,y−b,y+a. Therefore k=a+b and l=y−b are integers. Put

    δ−=floor(b)−b,  δ+=ceil(b)−b.

For δ between these endpoints replace A,B,C,D by

    A+(0,δ), B+(−δ,0), C+(0,−δ), D+(δ,0).

These remain square vertices, with parameters a−δ and b+δ. If b is integer all original coordinates are integer. Otherwise the four moved coordinates start in the interiors of unit grid edges. Their endpoints at δ− and δ+ are the two integer endpoints of those same edges: this follows from x,k,l∈Z and y=l+b. Therefore the entire permitted motion stays on J. At either endpoint b+δ and a−δ=k−(b+δ) are integers, and all four vertices are lattice points. The squared side is the convex function f(δ)=(a−δ)²+(b+δ)². Since 0 lies between δ− and δ+, one of its endpoint values is at least f(0). Selecting that endpoint proves the result. Nondegeneracy is preserved at the selected endpoint because its squared side is at least the original positive squared side. ∎

For a finite grid Jordan curve, the classical polygonal square-peg theorem supplies at least one continuous boundary square; Lemma 2.1 then supplies a lattice square. This existence premise is a credited theorem, not proved anew here. Compactness of J⁴ gives a maximum, and Lemma 2.1 identifies its value with M. The s=1 case also has a completely elementary proof: an interior lattice point requires all four incident cells to be present, which would create a filled 2×2 block. Therefore, when s=1, every corner of every cell lies on J. Any constituent cell is then a boundary lattice square of side 1, proving the target in this case without invoking the classical existence theorem.

Missing statement: existence alone gives M²≥1, not M²≥ceil(s²/2) for unbounded s. The rounding lemma transfers a size guarantee if one already has it; it does not create the missing size guarantee.

## Approach 3: cutting chords and reducing a hypothetical counterexample

This reduction is also known: compare Pettersson–Tverberg–Östergård, Theorem 3. The lattice-vertex formulation lets us prove it directly, without invoking continuous-square maximization.

### Lemma 3.1 (unit-chord elimination)
If a counterexample exists, some counterexample has a boundary that is an induced cycle of the infinite square-grid graph.

Proof. Choose a counterexample whose boundary has the least number L of unit edges. Suppose two nonconsecutive boundary vertices A,B are unit grid neighbors. The open segment e=AB contains no lattice vertex and cannot meet a unit grid edge in its interior except by coinciding with it. It is not a boundary edge. Thus its interior is disjoint from J and lies wholly inside or wholly outside J. The two arcs of J between A and B, each joined to e, form two smaller simple grid cycles. Each arc has at least three edges, so both resulting cycles have length at most L−2. Neither new cycle introduces any lattice vertex not on J.

By Lemma 1.1 choose an integer-aligned largest open s-square Q in int(P). No unit grid segment with endpoints on J can intersect Q: for a horizontal such segment, its integer height would be strictly between the integer top and bottom of Q, and intersection would then put at least one of its integer endpoints strictly inside Q. The vertical case is identical. This contradicts the endpoints lying on J. (For s=1 no integer height or abscissa can be strictly between the corresponding square sides.)

If e is interior, the standard separation by a simple arc inside a Jordan domain cuts that domain into the two domains bounded by the smaller cycles. The connected square Q, which avoids e, lies in one of them. Choose this cycle J'. Its largest filled-square side s' is at least s. If e is exterior, one of the two smaller Jordan domains contains the old domain; choose its boundary J', again with s'≥s. These two separation facts can also be seen by tracing the two A-to-B arcs with their common chord: in the interior case their bounded faces partition the old domain, and in the exterior case their bounded faces are nested and their difference is the old domain.

In either case B'=J'∩Z² is a subset of B. Every candidate lattice square for J' is therefore a candidate for J, so M'²≤M². Consequently

    2M'² ≤ 2M² < s² ≤ s'².

This is a shorter counterexample, contrary to minimality. Thus the minimal counterexample has no unit chord. ∎

Missing statement: prove the target for arbitrary induced grid cycles, or prove a further reduction that bounds their size. Chordlessness alone places no absolute bound on the bounding box or length. A finite exhaustive search cannot supply this missing unbounded result.

## Approach 4: exact geometric families and the symmetry barrier

### Proposition 4.1 (rectangles)
For a rectangle [0,w]×[0,h] with positive integer w,h, s=M=min(w,h).

Proof. Let h≤w. The h×h square with corners (0,0),(h,0),(h,h),(0,h) is a boundary lattice square, so M≥h, and plainly s=h. For any square with vertices in the rectangle, its convex hull is inside the rectangle. If its side is t and its orientation is θ, its vertical extent is t(|sin θ|+|cos θ|)≥t. Hence t≤h, proving M=h. ∎

### Proposition 4.2 (quarter-turn symmetry)
Suppose P is invariant under a quarter-turn R about c, and R preserves Z². Then M≥s, a bound stronger than the target.

Proof. A point p of P maximizing distance from c lies on the boundary. Indeed, an interior maximizer could be moved slightly farther from c while staying in P. The maximum on each straight boundary edge is achieved at an endpoint, by convexity of squared distance on that edge, so p can be chosen in Z². Let r=|p−c|. Symmetry and preservation of Z² give p,Rp,R²p,R³p∈B. They form a nondegenerate square of side √2 r.

Take the closure of a largest interior s-square, which is in P. If q is its center and z1,…,z4 are its corners, expansion of squared distances gives

    (1/4)Σ|zi−c|² = |q−c|²+s²/2 ≥ s²/2.

Every zi is in P, so r²≥s²/2. The orbit square thus has side √2r≥s. ∎

The lattice-preservation hypothesis is explicit: for c=(cx,cy) it means cx+cy and cy−cx are integers. In particular both coordinates of c can be integers or both can be half-integers. No assertion here covers arbitrary centers or arbitrary half-turn symmetry.

Missing statement: replace the exact fourfold orbit by four simultaneously matched boundary points in a nonsymmetric polyomino while retaining the quantitative bound. Averaging or symmetrizing P changes its boundary, and cannot move the resulting vertices back to the original J without proof.

## Approach 5: exhaustive integer certification, with a strictly bounded conclusion

The retained generator examines ALL masks 1,…,65535 in the 4×4 cell box, with bit 4y+x representing [x,x+1]×[y,y+1]. It admits precisely the edge-connected masks whose exposed-edge graph is connected and every vertex has degree 2. Unit grid edges do not cross except at common endpoints, so such a graph is a single embedded simple cycle. Conversely a Jordan-boundary polyomino has exactly those properties. Thus the predicate describes exactly the intended objects in this box.

For each admitted mask the generator:

1. Finds s by testing every integer-aligned filled square block. Lemma 1.1 proves this equals the original continuous optimum.
2. Tests every ordered pair p,q of distinct boundary lattice points as consecutive square vertices. The remaining points are q+R(q−p) and p+R(q−p), where R(u,v)=(−v,u). Every lattice square appears in this test, so the retained maximum M² is exact.
3. Writes a largest-block witness and one maximum-square witness into certificate.csv, and checks 2M²≥s² using integers only.

The replay verifier uses different constructions: flood fill of cells and of the padded complement with an explicit corner-pinch exclusion; dynamic programming for s; and opposite diagonal pairs with parity tests for the square vertices. It independently recomputes admissibility and the maxima for the entire mask range, checks every certificate witness, and checks there are no missing or extra rows. This is a second implementation, not an independent-person review.

Exact output:

- Nonempty masks examined: 65,535
- Admissible Jordan polyominoes: 9,349
- Rejected masks: 56,186
- Admissible counts for s=1,2,3,4: 2,932; 6,034; 382; 1
- Counterexamples in this range: zero
- Smallest M²/s² in this range: 8/9, attained by mask 16366
- All 9,349 witnesses and both programs are retained

The independent validity test is justified as follows. Edge-connected filled cells have connected interior. A bounded component of the complement would contain a missing cell, and is detected by the padded complement flood fill. At a lattice vertex the only local nonmanifold pattern is exactly two diagonally opposite occupied cells, excluded explicitly. With connected interior, no hole, and no such pinch, the boundary is a connected compact 1-manifold made of finitely many grid edges, hence one simple cycle. This also explains why holes and pinch patterns require separate controls.

The finite result is subsumed by the 2014 published range o(J)≤13. It is retained to make the predicates, orientation distinctions and arithmetic independently checkable, not as a new frontier.

Missing statement: a proof valid for all larger boxes, or a valid finite-reduction theorem. The 65,535-mask check gives no conclusion outside its stated range. In particular neither it nor the cited n≤13 calculation proves the universal target.

## Why approximation does not close the gap

Here is a precise conditional compactness statement, included as a diagnostic rather than an extra proof-attempt family.

Let Jn be bounded compact curves converging in Hausdorff distance to a compact curve J, all contained in one fixed compact set. If each Jn contains square vertices An,Bn,Cn,Dn with squared side at least δ²>0, then J contains a square of side at least δ. To prove this, extract a convergent subsequence of the ordered four-tuples in the compact fourth power. Each limit vertex lies in J by Hausdorff convergence. The equalities defining a square pass to the limit, and the positive side lower bound prevents collapse. This proves the statement. Mere existence of a square on each Jn has no such consequence because their side lengths may tend to zero.

For scaled grid approximations h_n J_n, the target would give a common nonzero bound as soon as those domains contain a common fixed open square. The known 2014 implication to the Jordan-curve square-peg problem includes the required approximation step. We do not treat arbitrary Hausdorff convergence by itself as a proof of convergence of inradii or of domain membership.

## Scope guard and final residual

The unresolved statement is exactly: for every finite union of unit lattice cells whose boundary is one Jordan curve, show that its boundary lattice-point set contains a square whose squared side is at least ceil(s²/2), or give one admissible counterexample. No result in this packet establishes that statement. No novelty or global-openness certification is claimed.

Primary references:

- Helge Tverberg, A conjecture on polyominoes, with consequences for Toeplitz' “square on a Jordan curve” problem (1911), OWR 08/2011, pp.362–363. https://doi.org/10.4171/OWR/2011/08 ; public report https://ems.press/content/serial-article-files/46323
- Ville H. Pettersson, Helge A. Tverberg, Patric R. J. Östergård, A Note on Toeplitz' Conjecture, Discrete & Computational Geometry 51 (2014), 722–728. https://doi.org/10.1007/s00454-014-9578-5
- Igor Pak, Lectures on Discrete and Polyhedral Geometry, Section 5, for the classical polygonal square theorem. https://www.math.ucla.edu/~pak/geompol8.pdf
