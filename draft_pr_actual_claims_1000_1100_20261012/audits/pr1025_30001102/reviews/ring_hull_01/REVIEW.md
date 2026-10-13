# Independent mathematical review: PR #1025, family B

**Verdict: PASS for the stated rational binary-input theorem. No mathematical repair is required in the reviewed ring-family, submodular-value, hull, facet-size or GLS interfaces. Priority and final paper readiness remain separate gates.**

Reviewed pinned head `7769e6872c3d2f4267706dc2400be3519186cf3d`, problem 30001102 / OWR-2489-008. This review began from `CURRENT_PROOF.md` and `SOURCE_INTERFACES.md`, then independently retrieved the original question and the complete relevant theorem bodies. Historical audit/acceptance files and other mathematical families' conclusions were not read or adopted. Input and source digests are in `INPUT_PINS.json` and `SOURCE_PINS.json`.

## Target and imported interfaces

The [original report](https://ems.press/content/serial-article-files/46195), printed pp. 2904–2905 (PDF pages 30–31), specifies unrestricted real coordinates, an arbitrary prescribed subset of integer coordinates, bipartite edges, and rational demands. Problem 1 asks hull membership and the preceding paragraph identifies general linear optimization as the associated main complexity question. The distinct subtree-hull Conjecture 2 is outside this claim. Rational query/objective encoding is explicitly part of the candidate's finite computational theorem; arbitrary unencoded real inputs are not assigned bit complexity.

I read [Schrijver's author manuscript](https://homepages.cwi.nl/~lex/files/minsubm6.pdf), Sections 2–6, including all of Section 6 on PDF pages 6–7. Its ring-family interface needs the smallest member and the smallest member containing each element when one exists, as well as submodular value access. Thus a partial value oracle alone would be insufficient. Its normalization removes unavoidable elements, removes elements occurring in no member, and identifies elements that always occur together. This converts the remaining family to ideals of a partial order. The subsequent ordinary-submodular-function construction uses closures and polynomially many value queries. Candidate Section 6 supplies the required domain information directly. No unknown feasible argument needs to be searched exponentially.

I read the actual [GLS 1988 book](https://www.zib.de/userpage/groetschel/pubnew/paper/groetschellovaszschrijver1988.pdf), Definitions 6.2.1–6.2.2, printed pp. 162–163 (PDF pages 174–175), and Theorem 6.4.9 with its full proof, pp. 179–180 (PDF pages 191–192). The strong optimization problem permits any exact optimizing feasible point; it does not require a vertex. For an unbounded objective it accepts a recession direction with the prescribed positive-cost normalization. Well-describedness needs a bound on the encoding of each defining inequality, rather than a bound on their number. The theorem supplies optimization-to-strong-separation for possibly unbounded rational polyhedra. I also inspected Section 10.2, especially problem 10.2.7 and its ensuing exact oracle-polynomial minimization argument, as a separate rational-bit cross-check. All eight main-interface source pages were rendered and visually checked, not only searched by OCR.

## 1. Exact finite lattice and threshold family

Work in the candidate's sign-changed coordinates. Given the objective-dependent interval endpoints, the integer domain is

\[
D=\{p\in\mathbb Z^I:l_i\le p_i\le h_i,\quad p_u-p_v\ge\lceil b_{uv}\rceil\text{ on integer–integer edges}\}.
\]

There is no hidden projected constraint through continuous vertices in this bipartite free-sign model. To complete any such integer assignment, revert its fixed coordinates to the original covering variables and set every unfixed coordinate to a sufficiently large common integer. A mixed edge needs only one lower bound on this common value; a continuous–continuous edge needs twice this value at least its demand. Fixed–fixed edges already hold. This completion establishes feasibility, not an optimal completion.

I independently checked the exact threshold representation, including the easily missed lower-baseline case. If the lower endpoint of `v` is `l_v`, even an empty prefix at `v` still requires `p_u >= l_v+d`, where `d=ceil(b_uv)`. A threshold at or below `l_u` is automatic; a threshold in the represented interval is forced; one above `h_u` makes the family empty. For each represented threshold `(v,t)`, the implication to `(u,t+d)` is automatic, ordinary or forbidden according to the target's location. Prefix arcs propagate all lesser represented thresholds. These constraints are both necessary and sufficient: when `p_v=l_v`, the baseline applies; otherwise its top threshold `(v,p_v)` applies. The reverse direction follows by direct substitution.

Every valid set therefore contains the forced closure, avoids forbidden nodes, and is implication-closed. The forced closure is the least member if it avoids forbidden nodes; its intersection with forbidden nodes diagnoses inconsistency. For any node `w`, close the forced nodes together with `w`. A forbidden intersection is equivalent to there being no family member containing `w`; otherwise the closure is the least such member. All these operations are reachability computations on a graph of polynomial size. Forced cycles, equal containing-closures, unavailable elements and empty ground sets cause no missing oracle hypothesis.

The node count depends on `h_i-l_i`, at most `2n`, not on the magnitude of a lower endpoint or common denominator. Large demands can produce large binary thresholds but cannot force their entire numerical interval to be enumerated. The arithmetic for shifts by `d` and the closure graph is polynomial in bit length.

## 2. Partial minimization really is submodular

For each `p in D`, the continuous slice is nonempty, its objective is bounded below by the relaxation optimum, and exact rational LP supplies an attained optimum. Let `y,z` be minimizing completions for `p,q`. The difference-constraint polyhedron is closed under coordinatewise min and max: an inequality `y_u >= y_v+b` and the corresponding inequality for `z` imply both min and max inequalities. These completions have fixed coordinates `p∧q,p∨q`.

For any linear objective, even with negative coefficients, its sum on `y,z` equals its sum on their coordinatewise min and max. Evaluating the minima on those latter slices yields

\[
f(p)+f(q)\ge f(p\wedge q)+f(p\vee q).
\]

No sign condition on the objective is used in this argument beyond finiteness of the slice optima. Applying min/max closure to the original covering coordinates would fail, but the candidate uses the difference coordinates throughout. The isomorphism from integer vectors to prefix sets transports this inequality to the ring family exactly.

I checked a more explicit uniform bit bound as a safeguard against confusing a count of arithmetic operations with Turing complexity. Let `k_b` be the common demand denominator and `k_a` the common objective denominator, both computed by lcm in binary. Fix the integer vector `p`. On each original graph component without a fixed coordinate, add one zero anchor. Boundedness makes the objective invariant under this anchoring. The anchored slice is pointed and has an optimal vertex. Its active difference rows and unit fixings form a totally unimodular matrix, so each coordinate has denominator dividing `k_b`.

More directly, every tight-edge component at this vertex contains a fixing or anchor; otherwise translating that tight component gives a nonzero kernel vector of the active matrix. Along a tight path, each coordinate is a fixed integer or zero plus at most `n-1` signed demands. Thus with `M_p=max(0,max_i|p_i|)` and the candidate's demand bound `B`, one can choose a slice optimizer with norm at most `M_p+nB`. Its value has denominator dividing `k_a*k_b` and magnitude at most `n*max_i|a_i|*(M_p+nB)`. The numerator and denominator therefore have polynomial bit length uniformly over all allowed `p`. The represented `p` themselves have polynomial length from the rational LP point and interval construction.

This verifies the rational value-oracle promise independently of numerical experimentation. Schrijver's ring reduction adds only polynomial-size sums/differences and closure queries. Standard rational submodular minimization applies; the separately inspected exact GLS Section 10.2.7 interface also provides a polynomial-bit route with the known uniform output bound. The candidate does not claim the whole LP-containing algorithm is strongly polynomial, and I found no pseudopolynomial denominator factor.

## 3. The bounded core is objective independent

For an objective bounded below on the relaxation, its coefficient sum vanishes on each graph component, since both constant translation directions are recession directions. Anchor one coordinate per component to zero. This preserves the optimal value and yields a nonempty pointed polyhedron. A finite optimum has an optimal vertex. Full rank of the active difference equations means their tight edges connect every component to its anchor: any disconnected tight component would again permit a nonzero active-matrix kernel vector. A tight spanning tree writes each coordinate as a sum of at most `n-1` signed demands, bounding the optimum by `nB` independently of the objective.

Applying the independently checkable proximity lemma stated in Section 3 gives a mixed optimum with norm strictly below `H=nB+n`. In particular the same compact mixed core works for every bounded objective. The construction does not enumerate integer points of that core. Its numerical radius may be exponential; its binary length is polynomial. This distinction is essential and is respected in the proof.

I also checked the lemma's use here rather than treating it as a historical acceptance seal: signed threshold layers preserve the sign of each coordinate and each difference, each single weighted layer is rowwise between the continuous optimum and the mixed feasible point, and a layer of weight at least one can be removed integrally without increasing cost. The nearest point of a nonempty closed sublevel set exists after restricting to a compact distance ball. Ruling out such layers implies the stated distance bound without assuming a mixed optimum in advance. The attainment argument is not circular.

## 4. Actual hull equality, boundary and recession

Let `K` be the convex hull of the bounded mixed core and `R` the relaxation recession cone. The core is a finite union of bounded rational polytopes, hence `K` is a rational polytope. The finite union is used as an existence and encoding argument, not as an enumeration algorithm. Consequently `K+R` is a closed rational polyhedron; compactness of `K` also proves closedness directly by taking subsequences.

For any `r in R`, its signed threshold decomposition uses integral vectors in `{0,1}^n` or `{0,-1}^n`, and every layer individually lies in `R`. Along such an integral direction `d`, a mixed point plus any nonnegative integer multiple remains mixed feasible. A real multiple lies in the finite convex hull of the two consecutive integer multiples. This argument extends to any finite convex combination of mixed points and then to finite sums of directions. It proves `K+R subset conv(T)` using the actual finite convex hull, without passing to its closure.

Conversely, strict separation of a mixed point outside `K+R` would give an objective with finite infimum on that set. It is nonnegative on `R`, so it is bounded below on the relaxation. The objective-independent core result forces its minimum on the entire mixed set to equal its minimum on `K`, contradicting the strict separator. Thus `T subset K+R`, and convexity gives exact equality.

It follows that the mixed hull is closed, rational, and has recession cone exactly `R`. This last identity also confirms that the ray returned by the initial LP unboundedness check is a valid hull recession ray for the final strong optimization oracle. Rescaling a strictly improving rational or integral ray to GLS's requested normalization has polynomial bit cost. Feasible base points always exist.

Boundary behavior is not hidden by a tolerance or relative-interior assumption. For one edge with demand `1/2` and both variables integral in difference coordinates, the true hull is `y_u-y_v>=1`; the relaxation's boundary at `1/2` is outside. A rational point `(3/2,1/2)` on the mixed-hull boundary belongs by the average of `(1,0)` and `(2,1)`. Both directions of component-constant lineality and real multiples of nonconstant integral recession directions are covered by the proof.

## 5. Facet complexity and exact membership

The box-slice matrices consist of signed incidence rows and unit rows, including integer fixings and bounds; they are totally unimodular. A vertex's coordinates therefore lie in `(1/k_b)Z` and have magnitude at most `H`. Convexifying the finite union cannot introduce new vertices outside its constituent vertex set. Together with the bounded integral threshold generators of `R`, this supplies a finite point/ray generating description with uniform coordinate bounds, regardless of its possibly exponential cardinality.

The hull is full dimensional because all sufficiently large integer original-coordinate vectors are feasible and their convex hull contains a translated positive orthant. Each actual facet, after homogenization, has a span of dimension `n` generated by the homogeneous input generators lying on it. Selecting `n` independent such generators and clearing the common point denominator gives an integral normal by cofactors. Its coefficients have magnitude at most `n!*[k_b(H+1)]^n`. This remains valid with lineality: its two signs can occur among generators on the facet; pointedness is not assumed here.

The candidate's displayed `phi` generously dominates the signed binary encoding of all `n+1` coefficients of each such inequality. To account explicitly for rational encodings with denominator one and vector dimension overhead, put `s=ceil(log2(n+1))+ceil(log2(k_b+1))+ceil(log2(H+2))`. Then `ceil(log2(T_0+1)) <= 1+n*s`. The encoding of the integral inequality, even treating every integer as a numerator/denominator pair, is at most `(n+1)*(5+n*s)`, below `10*(n+1)^2*(1+s)`. Thus the generous bound works under the book's actual encoding convention, independent of a smaller informal coefficient-length estimate. It also exceeds `n+1` in the whole-space case with no facets, as required by the actual GLS definition. Computing `k_b`, `H`, and an integer upper bound for the displayed logarithms uses polynomially many binary operations. There is no request to enumerate facets or residue classes.

The optimizer returns an exact rational point in `T`, hence in its hull, attaining the hull minimum, or an improving ray in its now-verified recession cone. Combining this strong optimization oracle with the computable facet bound meets the actual GLS hypotheses. Strong separation decides membership at all rational query points, including boundary points, and returns a strict valid separator outside. Only the optimization-to-separation direction is used. A general strong-membership-to-optimization equivalence is neither needed nor justified by this review.

## Independent diagnostics and adversarial controls

`independent_ring_value_checks.py` was written from these derivations and imports no candidate code or external solver. It uses exact `Fraction` arithmetic, independent Gaussian elimination and explicit exceptions. Normal, `-O` and `-OO` runs all passed with identical mathematical output:

- 1,789 threshold families, including 282 empty families, nonempty forced families and a 180-bit signed-endpoint case;
- 12,354 candidate sets compared to direct integer-vector feasibility and 5,925 feasible encoded assignments;
- smallest-member and smallest-containing-member checks, including forbidden closures and unavailable nodes;
- 112 hybrid instances, 598 exact continuous slice optima, and 8,888 checked submodular pairs;
- an intentionally omitted baseline, relaxation versus true-hull boundary, fractional hull boundary, fractional recession interpolation, and both signs of lineality.

These are finite diagnostics, not implementations of polynomial-time submodular minimization or GLS. They do not certify asymptotic complexity or replace the universal deductions above. The exact outputs and their digests are retained beside the script.

## Required repairs, boundaries and disposition

No blocking mathematical issue or required repair was found in family B. For final-paper readability, including the explicit uniform slice-value denominator/magnitude bound above would make the Turing-model discussion particularly easy to audit, but the current rational LP guarantee and checked established SFM dependency already provide it.

The verified claim is polynomial binary-input optimization, strong separation and exact membership for the unrestricted-sign rational bipartite mixed-integer system, with variable dimension and variable integer subset. Empty edge sets, no integer coordinates, all integer coordinates, isolated vertices, disconnected graphs, zero objectives, lineality, unbounded objectives, large denominators, and rational hull-boundary queries are covered. The zero-dimensional case is handled separately as in the candidate. This is not an implemented production optimizer, a compact extended formulation, a facet classification, an arbitrary-real-input complexity result, a proof of the separate subtree-hull conjecture, or a novelty certificate.

This family review is complete. Priority review and fresh final manuscript/package adversarial reviews are still required before publication or promotion.
