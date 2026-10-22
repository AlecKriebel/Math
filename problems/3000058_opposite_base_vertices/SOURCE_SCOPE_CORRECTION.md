# Required additive source-scope correction

2October2026. This correction supersedes the unqualified applicability statements in the historical SOURCE_GATE.md, TURN_1.md and FINAL_RESULT.md. All previously frozen files remain unchanged for auditability. It was prompted by independent review, not by a sixth author search.

## The linked definition permits unbounded bases

The original question links to the Egres definition https://oldlemon.cs.elte.hu/egres/open/Base_polyhedron (also accessible through https://lemon.cs.elte.hu/egres/open/Base_polyhedron). That page, last modified28April2014, allows a submodular function with values in R union {+infinity}, provided its full-set value is finite and its empty-set value is zero. It separately states that finite-valued functions give bounded base polytopes.

The original source gate did not inspect this linked distinction. TURN_1 began with finite b and then inferred boundedness and containment in the cube from the vertex condition. Those inferences are valid for bounded bases but not for the source's broader extended-valued definition. This was a source-scope error and must not be hidden by preserving the historical files alone.

## Exact two-coordinate counterexample to the literal broad wording

Let V={1,2}, b(empty)=b(V)=0, b({1})=1 and b({2})=+infinity. This extended-valued function is submodular: the only incomparable nontrivial subsets are the two singletons, whose submodular inequality has left side+infinity and right side0. All comparable-pair inequalities are equalities in the extended order.

Its base polyhedron is

B={x in R²:x1+x2=0, x1<=1}={(t,−t):t<=1}.

It contains0. Its unique vertex is v=(1,−1), which belongs to{−1,0,1}². To prove uniqueness directly, the affine parameterization by t identifies B with the closed ray(−infinity,1]. The endpoint1 is extreme, whereas every t<1 is the midpoint of two distinct feasible nearby parameters. Thus every vertex satisfies the source's cube condition. The negative−v=(−1,1) corresponds to t=−1 and is not a vertex. There is no opposite vertex pair, and0 itself is not a vertex either.

Therefore the literal statement under the linked extended-valued definition is false already in dimension2. This is a formulation diagnosis, not a solution of the nontrivial bounded-base conjecture suggested by the source's surrounding discussion of integer polytopes and Frank's bounded2-polymatroid problem. No authorial intent beyond the printed definitions is claimed, and no priority claim is made for this elementary ray.

## Correct scope of the frozen five-turn mathematics

All positive results in TURN_1 through TURN_4 are about bounded bases/base polytopes (or the explicitly bounded cube-intersection class in TURN_3). In particular the n<=5 theorem is only a bounded-base theorem. The positive-rank factor reduction requires finite canonical ranks, and the vertex-cube hypothesis implies the entire polytope lies in the cube only in this bounded situation. The all-dimensional zonotopal, laminar and coordinate-simplex-sum classes are themselves bounded.

TURN_5's tight-partition intersection arguments are used here only for bounded integral bases. Its maximum-support discussion and the final lower bound of six coordinates for a putative minimum-size counterexample apply only to the bounded interpretation. The four-coordinate failed-shortcut example remains a bounded example which satisfies the original opposite-pair conclusion via a different pair; it is distinct from the unbounded ray above.

Thus there are two separate outcomes: literal extended-valued statement refuted by the ray; intended bounded-base question unresolved after five turns, with the frozen scoped results. Final publication and queue disposition require the parent's source/review gate. Do not label the bounded conjecture solved or describe the old unrestricted n<=5 sentence without this correction.

## Verification

review_correction/check_ray.py checks all16 extended-valued submodular inequalities and exact rational feasibility/midpoint examples. The complete proof of the unique-vertex assertion is the affine-ray argument above, not finite sampling. The linked definition is independently verified from the live primary page; local sources/base_definition.html/.txt are preserved separately and not republished.
