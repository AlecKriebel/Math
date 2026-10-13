# Independent review of the normalized coordinate full nerve theorem

## Verdict and scope

**Accept the explicit full-nerve theorem for finite covered hypergraphs and its stated maximum-degree-three planar consequence.** The direct argument supplies the previously unverified convex-representation deduction. The existing source credit remains necessary. This review does not prove or refute the general triangle-and-segment conjecture, and makes no novelty or current literature-status assertion.

The fixed proof reviewed here is reproduced completely in [FULL_NERVE_COORDINATE_PROOF.md](FULL_NERVE_COORDINATE_PROOF.md), with its distributed identity in the [public manifest](PUBLIC_MANIFEST.json). Its final wording identifies the exponential coordinates as a specialization of the published rapidly increasing-coordinate construction and explicitly restricts the planar triangle corollary to incidence dimension at most three. Neither clarification changes the mathematical argument.

The objects are nonempty finite closed filled convex hulls. The nerve records every common intersection, including intersections of three or more objects. Its maximal faces define the intersection hypergraph. For a non-Sperner input the construction realizes the downward closure of the edge family; its maximal intersection sets are only the maximal original edges. No claim concerns one-sided contact, triangle boundaries, disjoint interiors, or selected incidence points alone.

## Source inspection and attribution

Ossona de Mendez's *Realization of Posets* gives rapidly increasing order coordinates followed by radial normalization, together with a separation theorem for differences of common lower sets. I read its full five-page text and visually inspected printed page 151. That page really prints the condition `F_i(x)<d F_i(y)` for `x<_i y`, while the ensuing argument uses the stronger growth implication `F_i(y)>d F_i(x)`. Thus the discrepancy is present in the rendered source, rather than arising solely from text extraction. The explicit choice `F_i(x)=B^{r_i(x)}` with `B>d` provides the stronger inequality required here. This is a correction to the growth condition used in the argument, not evidence that the published existence theorem is false. [Publisher article](https://jgaa.info/index.php/jgaa/article/view/paper48), [publisher PDF](https://jgaa.info/index.php/jgaa/article/download/paper48/2922).

The conventions and printed page 135 of de Fraysseix, Ossona de Mendez and Rosenstiehl's *Representation of Planar Hypergraphs by Contacts of Triangles* were inspected, including the displayed three-order certificate for its five-vertex example. The chapter states the convex maximal-intersection consequence for simple hypergraphs; its definition of simple is loopless and linear. It attributes the consequence to the poset theorem. The proof reviewed here supplies a direct full-nerve verification of the normalized-coordinate construction, and does not merely infer the nerve from symmetric-difference separation. The chapter's broader triangle-and-segment conjecture remains a different question. [Publisher chapter](https://doi.org/10.1007/978-3-540-77537-9_15).

## Independent derivation of the construction

Let the finite hypergraph have vertex set V and nonempty edges covering V. Vertex elements and edge elements of its incidence poset are distinct labels. In the usual orientation, the strict relations are precisely `v<e` when `v` belongs to `e`. Let `L_1,...,L_d`, with `d>=1`, be a realizer; its length need not be minimal.

Reverse every order. The resulting family realizes the dual poset, so an incident edge element now precedes its vertex in every order. Give positions consecutive integer ranks beginning at one. For an integer `B>d`, define

    F(x) = (B^{r_1(x)},...,B^{r_d(x)}),
    s_e = sum_i F_i(e),
    q_e = F(e)/s_e,
    C_v = conv{q_e : v in e}.

Every coordinate is strictly positive, and every normalized vector has coordinate sum one. Dropping its last coordinate identifies this affine hyperplane with `R^{d-1}`; the inverse appends one minus the sum of the retained coordinates. The map is affine and bijective on the hyperplane, and therefore preserves every convex hull and intersection. The output coordinates are rational. Coverage makes every `C_v` nonempty and finite generation makes it compact.

The exact assertion is that a nonempty set S of vertex labels has a common intersection of the corresponding hulls if and only if S is contained in an edge. The reverse implication is immediate: an edge containing S supplies its single witness `q_e` to every required hull. The other implication is established below.

### Minimal nonfaces and the number of orders

Take an inclusion-minimal nonface `S={v_1,...,v_k}`. Since every vertex is covered, `k>=2`. For every i choose an edge `e_i` containing `S\{v_i}`. It omits `v_i`, because S itself is a nonface. These edge labels are distinct: two equal witnesses for different omitted vertices would contain their union S.

In the original incidence orientation, the incomparable pair `v_i,e_i` needs at least one extension placing `e_i` before `v_i`. One extension cannot do this for two indices i and j. The two cross-incidences, together with the purported reversals, would give

    e_i < v_i < e_j < v_j < e_i.

Thus k distinct orders are needed and `k<=d`. This argument is valid for k=2: the induced poset is two disjoint two-element chains, and simultaneous reversal still gives the displayed cycle. No assertion about a standard example being defined only for k>=3 is used. The argument needs neither linearity nor the Sperner property.

### Bounds from reciprocal coordinates

For a vertex w set

    h_w(z) = sum_i z_i/F_i(w).

If an edge e contains w, the dual ranks satisfy `r_i(e)<=r_i(w)-1` in every coordinate. Hence each summand at `F(e)` is at most `1/B`, and

    h_w(F(e)) <= d/B.

If e omits w, dual incomparability supplies a coordinate with `r_i(e)>=r_i(w)+1`. Its summand is at least B, while all summands are positive. Consequently

    h_w(F(e)) >= B.

Both directions require the full realizer, rather than just linear extensions or their restrictions to one level of the incidence poset. Consecutive integer ranks justify the gap of at least one. These inequalities are bounds on the unnormalized points; applying them directly to the normalized points would be invalid.

### Correct radial lift of a convex combination

Suppose `x` belongs to `C_v`, and write

    x = sum_e lambda_e q_e,   lambda_e>=0,   sum_e lambda_e=1,

with support only on edges incident with v. Set

    t_v = 1/(sum_e lambda_e/s_e),
    alpha_e = t_v lambda_e/s_e.

Every denominator is positive. Thus `t_v>0`, all `alpha_e>=0`, and their sum is one. Direct substitution gives

    t_v x = sum_e alpha_e F(e).

This provides an actual lift into the unnormalized convex hull. The coefficients change during normalization. Different participating hulls may give different radial scales even at the same x; equality of those scales is neither assumed nor needed.

### Why the smallest scale excludes the nonface

Assume a minimal nonface S has a common normalized point x. Choose a convex representation and its positive scale for each vertex of S. Since S is finite, one vertex v has smallest scale `t_v`.

For every other w in S, the lift at w is a convex combination of w's incident-edge vectors, so its reciprocal functional is at most `d/B`. Linearity, positivity, and `0<t_v/t_w<=1` give

    h_w(t_v x) = (t_v/t_w) h_w(t_w x) <= d/B.

Adding over the other `k-1` vertices gives an upper bound `(k-1)d/B`.

Every edge incident with v omits at least one other vertex w of S. The corresponding functional contributes at least B on that edge vector, and all other contributions are nonnegative. Therefore the sum of these `k-1` functionals is at least B on every vector generating the lift hull for v. It remains at least B on the convex combination `t_v x`.

The two bounds contradict

    (k-1)d/B <= (d-1)d/B < B.

The strict final inequality follows from `B>d`; no limiting argument is required. All minimal nonfaces are excluded. Every nonface of a finite complex contains a minimal one, and a common point for a larger subfamily would be common to that smaller subfamily. This proves exclusion of every nonface and completes the full-nerve theorem.

The equivalent coefficient-mass explanation in the author's proof is valid: for each other w, at most `d/B^2` of the minimum lift's coefficient mass can be supported on edges omitting w. Those omission classes cover all its supporting edges. Summing their masses must therefore give at least one, whereas the upper bound is `(k-1)d/B^2<1`. Overlapping omission classes cause no problem for this inequality.

## Exceptional cases and the planar consequence

For `V=E=empty`, the empty family suffices. The empty face is treated by convention. Otherwise, coverage and nonempty edges rule out an empty hull. In dimension one, a nonempty incidence poset realized by a single total order can have at most one vertex element and one edge element because both levels are antichains. Its covered case is the one-vertex one-edge chain and is represented in `R^0`. The general argument also works without this classification because a minimal nonface would require `2<=k<=1`.

Sperner is needed only to identify the original listed edges with the maximal nerve faces. For example, the two-edge family `{a},{a,b}` has the same downward closure as its single maximal edge `{a,b}`. No set representation can retain the smaller set as an additional maximal intersection. Isolated singleton edges in a Sperner hypergraph cause no problem. The construction makes no assumption that the hypergraph is linear; the standard-example fixtures with larger edges also check that broader scope.

For incidence dimension at most three, repeat realizer orders if necessary to obtain three orders, and use `B=4`. The hulls then lie in the plane. If every vertex is incident with at most three edges, each hull has at most three generating points and hence is a point, segment, or filled triangle. The degree is the number of edges incident with a vertex, not edge cardinality.

The previously accepted finite stability and inflation argument applies to these hulls. Briefly, each empty intersection of compact hulls has a positive common distance gap, and finitely many subfamilies give a positive uniform gap. Enlarge each point, segment, or triangle to a sufficiently close nondegenerate triangle containing it in its interior. Faces retain their old witnesses, and the gaps preserve all nonfaces. Further sufficiently small rational perturbations preserve both the interior witnesses and the gaps. Thus the maximum-degree-three subclass admits nondegenerate rational filled triangles with the same full nerve. Its proof no longer depends on an omitted deduction from the poset separation statement.

This conclusion does not address arbitrary vertex degree. Four edge witnesses in the central coordinate hull of the four-leaf star are all extreme. A triangle cannot equal that hull. The same star nevertheless has a segment representation by an entirely different construction, so this is a limitation of the coordinate output rather than a counterexample to the general conjecture. The earlier fixed-neighbor obstructions likewise remain local obstructions.

## Exact independent computational verification

The independent implementation uses exact rational barycentric feasibility, rather than the author's half-plane intersection and Fourier-Motzkin procedures. For each tested subfamily it introduces nonnegative coefficients for every participating hull, imposes that each coefficient block sums to one, and equates all resulting points in the first `d-1` coordinates. This gives a rational system `A z=b`, `z>=0`.

A phase-I simplex calculation with Bland pivoting finds a certificate. Its numerical verdict is never accepted on its own:

- A feasible certificate is a rational vector z checked to be nonnegative and to satisfy every equality exactly.
- An infeasible certificate is a rational row vector y checked to satisfy `y A<=0` coordinatewise and `y b>0`. If a nonnegative solution existed, multiplying its equations by y would imply `0<y b=y A z<=0`, a contradiction.

All 334 nonempty subfamilies of 12 fixtures were checked, with the complete certificates retained. These include a genuine one-dimensional realizer, a dimension-two single-edge example, nested singletons in dimension two, standard examples S2 through S5, stars with three through six leaves, and the published five-vertex example. Thus the tests include full geometry in ambient dimensions zero through four, not only planar algebra checks. Four additional Farkas certificates show that each coordinate witness of the four-leaf star lies outside the convex hull of the other three and is therefore extreme.

The explicit three-point and four-point coordinates in the fixed public proof were independently recomputed. For the S3 missing triple, the three root lower bounds are `4425/1024`, `4233/1024`, and `4425/1024`, all above `3/2`. The five-vertex example has precisely 17 nonempty faces. The nested-singleton fixture is compared with the downward closure and is never falsely accepted as an exact representation of the nested maximal-edge list.

Nine embedded negative controls reject an incorrect realizer, an inadmissible base, reversed duality, a corrupt normalized point, invalid primal and Farkas certificates, a pair-only intersection shortcut, use of a largest radial scale, and a direct failure of an explicit gate. Five source mutations are each tested under normal Python, `-O`, and `-OO`, using disposable writable copies. They alter the base, duality, normalization, and each kind of linear certificate. Each of the 15 runs must fail with the intended explicit exception; a timeout is not accepted as rejection. Canonical inputs remain unchanged.

The author's final checker and mutation harness were separately replayed. Deterministic outputs, fixed input hashes, optimization-safe exceptions, integrity mutations, and archive recovery are recorded in the accompanying verification metadata. The general mathematical claims rest on the preceding proofs. These finite calculations test the implementation and examples, and are not substituted for a universal argument.

## Acceptance boundary

The exact normalized dual-edge construction, its whole-nerve conclusion in `R^{d-1}`, and the planar maximum-vertex-degree-three corollary are accepted under the stated finite covered conventions. The earlier unproved convex-consequence dependency is removed from that corollary. The source construction and published consequence remain credited. General-degree triangles, literal nested maximal edges, contact restrictions, novelty, and current status are outside the accepted claim.
