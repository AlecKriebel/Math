# Shortest paths in line arrangements

## Result and scope

**The general target is unresolved by this report.** No subquadratic exact algorithm and no quadratic lower bound for unrestricted algorithms is proved. Five mathematical routes are analyzed below. They yield structural proofs, exact counterexamples to particular proposed simplifications, and a representation-dependent sorting lower bound. These are an audit of possible approaches, not a claim of a new solution or of priority for the elementary lemmas.

The historical two-pencil example must be separated from the general question: the specified grid-like two-pencil problem was solved in linear time in 2003 by Hart and by Kavitha–Varadarajan. A 2020 thesis abstract still describes the general exact problem as unresolved and develops approximation instead. Searches made on 8 October 2026 found no later general settlement, but that negative search result is bounded. In particular, the 2020 thesis PDF could not be inspected. The older problem page is not evidence of present-day openness.

The five routes are:

1. Compress a geodesic by eliminating repeated line intersections.
2. Restrict search to a geometric corridor or an admissible heuristic region.
3. Solve a direction-only relaxation and try to realize it with very few bends.
4. Propagate distances as simple functions along lines.
5. Prove a lower bound by output complexity or sorting.

The strongest structural conclusion here is that **even the fully expanded edge list of a Euclidean shortest path has at most n−2 edges**, for distinct arrangement vertices and n distinct lines. Thus the quadratic size of the entire arrangement is not an output-size lower bound for a single shortest path.

## The normalized problem

Let L be a finite set of n distinct, complete affine lines in the Euclidean plane. Its finite arrangement vertices are points incident with at least two lines. Between consecutive distinct vertices on a line, the closed segment is a finite arrangement edge. Several lines through one point produce one vertex, not multiple zero-length edges. Unbounded rays have no additional finite endpoint.

The input consists of O(n) line equations a_i x+b_i y=c_i, with (a_i,b_i) nonzero, and two finite arrangement vertices s,t, supplied by coordinates or by incident line identifiers. The intended cost of a path is the **sum of Euclidean lengths of its traversed edges**. It is not the number of edges and not the number of turns. All line speeds are equal; no obstacles remove portions of a line. The full-line hypothesis is essential to the shortcut arguments.

The task is to return a shortest s–t path, or its exact length if that output variant is stated, in o(n²) worst-case time as a function of the number of input lines; alternatively, prove an appropriate quadratic lower bound in a declared computational model. The historical page asks for a subquadratic algorithm or a stronger lower bound in a reasonable model. Requiring a quadratic lower bound is a stronger endpoint than merely improving its stated Ω(n log n) bound. We do not equate o(n²) with the more restrictive O(n^(2−ε)) for a fixed ε>0.

For the algorithmic operation counts below, the model is a real RAM with exact field arithmetic, square roots, and comparisons of stored real quantities charged one unit each. This explicitly allows comparison of accumulated Euclidean lengths. It is not a polynomial-bit Turing bound for sums of square roots. The finite verifier uses a smaller, exactly rational subclass and makes no general bit-complexity assertion.

There are three different outputs:

- a real-valued shortest-path length;
- an ordered sequence of maximal straight runs, with their supporting lines and bend vertices;
- the ordered list of every arrangement edge on the path, including straight-through intermediate vertices.

The problem page does not specify this output convention or a bit model. We therefore state precisely which conclusion applies to which output. A preconstructed Θ(n²)-size arrangement is a different input representation from n line equations. Reading or constructing all of that representation does not prove a lower bound for the implicit input problem.

Parallelism and concurrence are allowed throughout our structural results and counterexamples. Coincident lines may first be merged without changing the geometric problem. Sorting normalized equation triples accomplishes this in O(n log n) arithmetic/comparison operations. The case s=t has the empty path. If finite vertices exist, there are at least two nonparallel lines, and the union of all lines is connected: any line intersects at least one of those two. Thus finite arrangement vertices lie in a common connected component.

A shortest finite-vertex path never needs an unbounded ray, since such an excursion has to return along the same ray. The finite graph has at most binomial(n,2) vertices and O(n²) edges, with strictly positive edge lengths. A shortest simple graph path consequently exists. Ordinary explicit construction by pairwise intersections, sorting each line's vertices, and Dijkstra gives O(n² log n) operations and O(n²) storage. The literature records the sharper O(n²) upper bound using quadratic-time arrangement construction and a linear-time nonnegative planar shortest-path routine. That imported result is not re-proved or implemented here.

## Source normalization and literature limits

Erickson's specific item is [Open Algorithmic Problems, shortestpath](https://jeffe.cs.illinois.edu/open/algo.html#shortpath). It attributes the question to Marc van Kreveld, gives the easy O(n² log n) algorithm and a stated Ω(n log n) lower bound, and also lists a two-pencil grid case. The [parent index](https://jeffe.cs.illinois.edu/open/) warns that its pages have not been systematically updated since 2001. The old lower-bound reduction is reported as source context, not reconstructed here.

[Hart, Shortest Paths in Two Intersecting Pencils of Lines, CCCG 2003](https://www.cccg.ca/proceedings/2003/48.pdf) proves the linear-time solution for opposite corners of the specified quadrilateral grid. Its hypotheses require every cross-pencil intersection to lie in one open half-plane bounded by the line between the two pencil centers. The two boundary routes suffice. The paper also records a quadratic general upper bound and a linear-space development. Its additional extension statement is not needed here.

[Kavitha and Varadarajan, On Shortest Paths in Line Arrangements, CCCG 2003](https://www.cccg.ca/proceedings/2003/17.pdf), Theorem 1.1, gives the same boundary-route conclusion under explicit grid-like two-pencil hypotheses. Its weighted-graph formulation makes the Euclidean-length metric unambiguous. The paper describes simplifications for general arrangements, while explicitly not obtaining a general subquadratic algorithm. We do not promote those simplifications into a settlement.

[Eppstein's author bibliography](https://ics.uci.edu/~eppstein/pubs/geom-path.html) states the Eppstein–Hart 1999 bound O(n+k²) for k distinct line orientations. The full 1999 paper was not obtained here. To avoid silently omitting orientation grouping, an ungrouped-input use can conservatively include O(n log n) sorting overhead. When k=n, this mechanism still has quadratic worst-case cost. Approximation results are distinct from an exact shortest-path result.

[Likhtarov, Shortest paths in line arrangements, UBC MSc thesis, 2020, DOI 10.14288/1.0389809](https://doi.org/10.14288/1.0389809) is listed in the [department's 2020 thesis catalogue](https://www.cs.ubc.ca/cs-theses/cs-theses-2020). The depositor's abstract, inspected through the [DataCite DOI record](https://api.datacite.org/dois/10.14288/1.0389809), states that the exact quadratic bound was not improved and that the thesis studies approximation and structural lemmas. The thesis PDF was not inspected: the UBC full-text landing returned a security-block page. No theorem or quantitative approximation guarantee is inferred from its title alone.

The source inventory records byte hashes, inspection depth, and retrieval failures. Primary publications, author bibliographies, and deposited metadata support the claims above. Search snippets and encyclopedia mirrors served only as leads. Searches with exact title variants, “subquadratic”, “line arrangement”/“arrangements of lines”, and individual years 2019–2026 did not identify a general resolution. This does not exclude unindexed or unpublished work and does not establish a 2026 theorem of openness.

## Route 1 Connected intersections and short certificates

### Proposed mechanism

If a shortest path uses each input line only once, perhaps it has a small enough description to search or certify without constructing the whole arrangement. The relevant property is stronger than saying that a supporting line cannot reappear: a line that is merely crossed cannot be met twice with an off-line detour between the meetings.

### Lemma 1 Line intersection is connected

Let P be a Euclidean shortest path between finite arrangement vertices, parametrized without backtracking. For every input line ℓ, the parameter set on which P lies on ℓ is empty or an interval. The image P∩ℓ is consequently a point or a segment.

**Proof.** Every subpath of a shortest path is shortest between its own endpoints; otherwise replacing it improves the whole path. Suppose x and y are two points of P on ℓ, with an off-line point between them along P. The segment xy lies on the complete input line and is an allowed route, subdivided into finitely many arrangement edges if necessary. The Euclidean triangle inequality says that any polygonal route from x to y has length at least |xy|. Equality holds only for a monotone traversal of the segment xy. Since the subpath contains an off-line point, its length is strictly larger. Replacement contradicts optimality. If the subpath stays on ℓ but reverses direction, the same strict inequality follows from the excess variation. Thus the subpath is exactly the monotone segment xy. This proves both assertions. ∎

No generic-position assumption is used. Strictness excludes an off-line detour even when several different shortest paths tie. Zero movement is not an edge, and repeated coincident line descriptions are merged.

### Theorem 2 A sharp edge bound

Write I(v) for the set of input lines incident with a finite vertex v. If s≠t and a shortest path has q arrangement edges, then

q ≤ n − |I(s)| − |I(t)| + 2 ≤ n−2.

**Proof.** Write its ordered vertices as v_0=s,v_1,…,v_q=t. Let ℓ_i be the supporting line of the incoming edge v_(i−1)v_i. For i≥1, every line through v_i other than ℓ_i is encountered for the first time at v_i. Indeed, if such a line m had been encountered earlier, Lemma 1 would put the intervening subpath on m. That subpath contains a nontrivial terminal piece of the incoming edge, forcing m=ℓ_i, a contradiction.

Initially |I(s)| lines have been encountered. Each intermediate vertex introduces at least one new line, because it has at least two incident lines. The last vertex introduces |I(t)|−1 new lines. These newly encountered sets are disjoint. Therefore

n ≥ |I(s)| + (q−1) + (|I(t)|−1),

which rearranges to the result. Since both endpoints are arrangement vertices, both incidences are at least two. ∎

The bound is sharp: take y=0 and n−1 distinct vertical lines, with s,t at the first and last vertical crossings. The unique geometric geodesic is the horizontal segment and has n−2 arrangement edges.

### What this does and does not give algorithmically

A geodesic has O(n) vertices and O(n) maximal straight runs. Thus both ordinary path representations have linear output size. Listing Θ(n²) arrangement vertices cannot be justified as unavoidable output for one geodesic.

A proposed certificate consisting of q≤n−2 vertices and incident line identifiers can have its geometric feasibility and Euclidean length checked with O(nq+q) straightforward operations: check each segment's supporting line and, if an expanded edge list is required, check against all lines that no vertex is omitted in an edge interior. This O(n²) verification bound is only a baseline, not a lower bound or an optimal verification algorithm.

The central missing step is choosing the correct O(n)-size path. The existence of a short certificate gives no subquadratic method for finding it. Enumerating simple supporting-line sequences remains enormous. The route proves structure but stops before the requested algorithm.

## Route 2 Geometric pruning and A star search

### Proposed mechanism and valid containment

For an input line with s and t on the same closed side, a shortest path remains in that closed half-plane. To leave it and return would produce two meetings with that line and an off-line subpath, contradicting Lemma 1. This includes an endpoint on the line: if the other endpoint is strictly inside, the first intersection interval cannot be followed by an excursion to the wrong side and a later crossing. If both endpoints lie on the line, the geodesic is their segment.

Intersect all closed half-planes bounded by input lines and containing both endpoints; if both endpoints lie on one line, both of its closed half-planes are included. Call the resulting convex region K. It contains every shortest path. Given any feasible length upper bound U, every point x on a shortest path also satisfies

|s−x| + |x−t| ≤ U,

because the lengths of the two subpaths dominate their endpoint Euclidean distances. These are sound pruning rules.

### Proposition 3 The pruning region can retain quadratic complexity

For any integer m≥2, take lines x=i and y=j for 0≤i,j≤m, and let s=(0,0), t=(m,m). Then n=2m+2 and:

- the shortest path length is C=2m;
- K is the square [0,m]²;
- all (m+1)² vertices survive the ellipse test with the *exact* upper bound U=C.

**Proof.** Every path uses horizontal or vertical segments, so its length is at least the total absolute displacement 2m. A monotone grid path attains this. The four boundary lines impose the square; every other line separates s,t, so no additional half-plane restriction arises.

The function f(x)=|s−x|+|x−t| is convex. At the four square corners its values are 2m or m√2, all at most 2m. Every point in the square is a convex combination of those corners, so f≤2m everywhere. In particular every grid vertex survives. Since (m+1)²=n²/4, explicit enumeration of surviving vertices takes Θ(n²) time. ∎

This is a lower bound for the specific enumerate-the-survivors approach, not for the target problem; two orientations make this family easy by other methods.

### Proposition 4 Euclidean heuristic A star has a quadratic expansion family

Consider ordinary vertex-expanding A* on the finite arrangement graph, with h(v)=|v−t|, stopping when t is removed with a final distance label. It expands Ω(n²) vertices on the preceding family, irrespective of tie-breaking.

**Proof.** At grid vertex (i,j), the exact source distance is d(s,v)=i+j. If i<m and j<m, let a=m−i>0 and b=m−j>0. Then

d(s,v)+h(v)=2m−a−b+√(a²+b²)<2m=C.

There are exactly m² such vertices. The Euclidean heuristic is consistent by the triangle inequality. Every vertex with optimal f-value strictly below C must be settled before the goal. For completeness, if one were still unsettled, take a shortest path to it and its first unsettled vertex. Its predecessor has already supplied an optimal label; consistency puts its f-value no larger than that of the selected vertex, strictly below C. The goal therefore cannot be the minimum-priority item. Thus at least m² vertices are expanded. ∎

There is no general impossibility result for A* with different heuristics, symbolic batches, or specialized grid recognition. In particular a direction-aware lower bound can behave very differently. The unresolved gap is a generally useful pruning or aggregation rule that avoids this quadratic retained set.

## Route 3 A direction relaxation and the failure of one bend

### Direction-only optimization

Let u_1,…,u_k be unit vectors for the available unoriented line directions, with both signs allowed. Ignore the offsets of the actual lines. The relaxed minimum is

ρ(Δ)=min {Σ_j |a_j| : Δ=Σ_j a_j u_j},  where Δ=t−s.

Every actual path provides such a decomposition by collecting its signed directional displacements, so ρ(Δ) is a lower bound. Equivalently, it is the gauge of the centrally symmetric polygon conv{±u_j}. Any z satisfying |z·u_j|≤1 yields the explicit certificate ρ(Δ)≥z·Δ; apply z to a decomposition and use the triangle inequality. Boundary edges of that polygon explain why a relaxed optimum can use at most two directions, without asserting that the needed parallel translates exist in the arrangement.

### A complete two-direction special case

If all input lines have one of two independent directions u,v and s,t are arrangement vertices, write uniquely Δ=αu+βv, where u,v are unit vectors. Every path has length at least |α|+|β|: the net displacement in each basis direction is fixed, and its total variation dominates its absolute value. The line through s in direction u intersects the line through t in direction v, producing a two-run path of exactly that length. Thus this special case is solved by one bend. Once the incident lines are known, its compressed geometric answer uses O(1) operations; finding them by a scan takes O(n). An expanded edge list additionally entails reporting and ordering all intermediate intersections.

This is an elementary reconstruction of a known easy case, not a solution for growing k.

### Proposition 5 Five lines defeat the general one-bend rule

Use the following complete lines:

A: 4x+3y=0; B: 5x−12y=15; C: 5x−12y=−63;
D: 4x+3y=75; E: y=0.

Let s=(−3,4)=A∩C and t=(15,5)=B∩D. The shortest Euclidean path is

s → (0,0) → (3,0) → t,

with length 5+3+13=21. Every path with at most one bend has length at least 65/3>21. The minimum hop count is two, so hop-optimal and Euclidean-optimal paths differ.

**Proof.** No line contains both endpoints. A one-bend route must use one of A,C followed by one of B,D. A is parallel to D, and C is parallel to B. The remaining intersections A∩B=(5/7,−20/21) and C∩D=(79/7,209/21) each give total length 65/3, by the 3–4–5 and 5–12–13 direction ratios.

The displayed three-edge path exists: no other input line subdivides the interiors of its three segments. By Theorem 2, a shortest path on these five lines has at most three arrangement edges, and hence at most three maximal runs. A three-run candidate must start on A or C and finish on B or D. Its middle line can only be E: switching to the other source line would occur at s, and switching to the other target line would occur at t; repeating a line is excluded by Lemma 1. The four E-mediated route lengths are respectively

A–E–B: 21; A–E–D: 30; C–E–B: 39; C–E–D: 48.

These follow from the E-intersections 0,3,−63/5,75/4. Some long candidate runs cross extra vertices, which can only exclude candidates from a three-edge optimum, not create a shorter one. These four values and the two one-bend values exhaust all possible compressed shortest-path forms. Therefore the optimum is 21. A one-bend two-edge route exists through C∩D, whereas no one-edge route exists; the hop optimum is two. ∎

### The relaxation also has a strict offset gap

Here Δ=(18,1). The three unit directions may be taken as (1,0), (3,−4)/5, and (12,5)/13. The vector z=(1,1/5) satisfies all three dual constraints. Its value is 91/5. That bound is attained in the relaxed problem by horizontal displacement (78/5,0) followed by displacement (12/5,1), of total length 78/5+13/5=91/5. Hence ρ(Δ)=91/5<21.

The failure is spatial: an optimal free-direction displacement sequence need not be supported by the available line translates. No general exact algorithm follows from solving this two-dimensional relaxation. The exact gap is recovering feasible entry points and their optimal order without inspecting quadratically many intersections.

## Route 4 Distance functions and wavefront propagation

### An exact recurrence

Parametrize one input line ℓ by Euclidean arclength x. If s is not on ℓ, every path reaching x has a first meeting with ℓ at an arrangement vertex v. Conversely, reaching v by a shortest path and then following ℓ to x is feasible. Therefore

d_s(x)=min_(v on ℓ) [d_s(v)+|x−x_v|].

If s lies on ℓ, the direct source term |x−x_s| is included. The recurrence is exact, but the coefficients d_s(v) are unknown distances in the original problem, so it is not by itself an algorithm. It expresses a lower envelope of V-shaped functions and implies that d_s restricted to a line is 1-Lipschitz. It does **not** imply convexity, because a minimum of convex functions need not be convex.

### Proposition 6 A rational nonconvex distance profile

Take four lines

L: y=0; A: 3x+4y=12; B: 3x−4y=−12; M: 5x−12y=0,

and source s=(0,3)=A∩B. At the three consecutive vertices p=(−4,0), o=(0,0), q=(4,0) on L, the source distances are 5,6,5.

**Proof.** The direct source segments to p and q have Euclidean length 5, giving exact distance 5 by the ambient Euclidean lower bound. For o, Theorem 2 permits a shortest path with at most two edges. A one-bend route uses A or B first and L or M last. Via A∩L and B∩L the lengths are 9. Via A∩M=(18/7,15/14), the two segment lengths are 45/14 and 39/14, totaling 6. Via B∩M=(−9,−15/4) the length is 21. Thus d_s(o)=6. Since o is the midpoint of p,q, convexity would require 6≤(5+5)/2, which is false. ∎

Indeed on L the exact profile is

min{5+|x+4|, 6+|x|, 5+|x−4|}.

This has multiple competing ingress terms. A convex-profile optimization or a single globally preferred entry vertex is therefore invalid, even with four lines and entirely rational Euclidean edge lengths.

If there are r known sites on one line, sorted by arclength, a lower envelope can be constructed in O(r) time after sorting: prefix minima of d_s(v)−x_v provide the best site to the left; suffix minima of d_s(v)+x_v provide the best site to the right. Compare the resulting two affine expressions on each interval. This gives a correct local operation, but all sites' global distance labels must first be available.

Over all n lines, there may be Θ(n²) incidences with arrangement vertices. Computing each local envelope after materializing all its labels reproduces that workload. We have not proved that the final envelopes inherently need quadratic size; nor does Proposition 6 prove that. The route is blocked at a subquadratic joint representation and discovery method, not at a proved universal envelope lower bound.

## Route 5 Sorting and lower-bound accounting

### Proposition 7 An expanded-output sorting reduction

Let a_1,…,a_m be distinct real numbers in (0,1). Construct lines y=0, x=0, x=1, and x=a_i, and choose s=(0,0),t=(1,0). The unique geometric shortest path is the segment st. Its expanded arrangement-edge list reports the a_i in sorted order. Consequently an algorithm for that output in the comparison sorting model needs Ω(m log m)=Ω(n log n) comparisons in the worst case.

**Proof.** Ambient Euclidean distance gives a length lower bound of 1, attained by st. Equality in the triangle inequality forces that geometric segment. The intermediate arrangement vertices are exactly (a_i,0), so the ordered output sorts the input labels. A comparison decision tree distinguishing all m! input orders has height at least log_3(m!)=Ω(m log m). ∎

The lower bound is explicitly for the comparison model and expanded ordered output. The compressed answer on this family is simply st, with length 1; therefore this reduction proves no corresponding lower bound for compressed output or distance alone. It is also not a proof of the historical convex-hull-verification reduction.

### Why the obvious quadratic arguments fail

The full arrangement has Θ(n²) vertices, but Theorem 2 gives only O(n) vertices in one Euclidean geodesic. Mandatory construction of an entire arrangement is an algorithm design choice. It is not forced by the input or output.

There is a further limitation on pure counting of discrete outputs. Choose, for every arrangement vertex, the lexicographically smallest pair of incident line identifiers. A path has at most n−1 vertices and thus can be encoded by at most n−1 ordered pairs from an n-element alphabet. Even an overcount of all such encodings is n^(2n), whose logarithm is O(n log n). Counting these discrete output labels alone cannot yield an Ω(n²) information lower bound. This does not bound the depth of actual algebraic decision trees: the same discrete output may occur in disconnected input regions, and exact numeric output or the complexity of predicates can matter.

A genuine quadratic lower bound would therefore need a substantive model-specific argument or a valid hardness reduction, not the quadratic number of potential crossings. No such reduction is established here. The sorting route stops at a weaker, output-sensitive bound.

## Corrections to unsafe formulations

The following are contextual corrections to formulations that can otherwise be mistaken for conclusions:

- “The two-pencil case on the historical page remains open” must be replaced by the attributed 2003 linear-time result under its explicit grid-like hypotheses.
- “A shortest path can require quadratic explicit output because it crosses many lines along O(n) runs” is false in the Euclidean full-line model. Repeated crossings themselves trigger the shortcut; Theorem 2 bounds the full edge list.
- “Only two directions are needed in the relaxed displacement problem, so an actual shortest arrangement path has one bend” is false. Proposition 5 gives exact costs 91/5, 21, and 65/3 for the relaxation, the true optimum, and the best one-bend route.
- “A minimum of convex distance cones is convex” is false. Proposition 6 gives the exact midpoint violation 5,6,5.
- “A* can take quadratic time, therefore every algorithm does” is unsupported. Proposition 4 is restricted to ordinary vertex expansion with the Euclidean heuristic.

The current report makes none of those rejected claims. No earlier rejected manuscript or third-party source text is included in the deliverable.

## Exact finite validation

The accompanying verifier is standard-library Python with rational coordinates and rational Euclidean lengths obtained from Pythagorean directions. It computes intersections exactly, merges coincident lines, handles parallelism and concurrence, creates edges between consecutive distinct vertices, and compares Dijkstra with a separately implemented Floyd–Warshall recurrence. No floating-point comparison or tolerance is used.

The suite checks 6,531 ordered source-target queries, including same-vertex cases, on the fixed examples, eighteen deterministic small arrangements, and two-direction arrangements. It checks connected line intersections, the incidence-sensitive edge bound, same-line equality, and the two-direction formula. It separately checks seven grid sizes m=2,…,8, the exact squared inequalities behind ellipse retention and strict A* priorities, and all 120 permutations in a five-number sorting fixture.

Input guards reject zero normals, noninteger line coefficients, oversized fixtures, and irrational lengths. An explicit failing negative-control guard is caught as expected. Checks use explicit exceptions, not Python assertions, and therefore remain active under -O and -OO. The read-only validation requires genuine UID/EUID 1000 and demonstrates failed attempts both to open the verifier for append and to create a file in its directory. The validation record reports each optimization mode separately.

The test graph construction is intentionally explicit and small; it is not the proposed subquadratic algorithm. These finite tests are consistency and counterexample checks. They do not prove any universal complexity result, exhaust real inputs, certify all shortest-path ties, or replace the preceding proofs.

## Final mathematical status

All five routes are unfinished with respect to the general target. The audit establishes exact statements about short path output, failures of several attractive simplifications, and a modest comparison lower bound. It does not resolve the implicit-input Euclidean shortest-path problem, determine the best possible bit complexity, or prove a quadratic lower bound in a general model.

The remaining central task is to exploit the O(n)-length structure of an unknown geodesic while identifying its necessary intersections in o(n²) time, or to show by a valid model-specific lower-bound argument that this cannot be done. None of the five routes supplies that missing step.
