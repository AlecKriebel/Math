# Independent adversarial review —Zenodo22983138, v1.0.0

**Verdict:** the stated general-convex-body equality result withstands this independent review. I found no substantive mathematical defect, hidden regularity restriction, equality counterexample or source-application gap. Both the countable-shell argument and the retained finite-witness argument can be checked completely with standard finite-dimensional convexity and elementary integration. This verdict concerns mathematical validity in the stated scope; worldwide novelty is not certified.

The entire actual four-page PDF and full TeX were read before the independent attack ledger was sealed. No historical/current sibling/root report was read. A later support README mentions earlier review outcomes; these were not used as evidence. The actual published eleven-page FPS article was independently acquired and read in full, and the full OWR contribution pp.2907–2909 was inspected. Primary source assertions were checked in their bodies, not inferred from abstracts.

## Exact claim and boundaries

Let K be a compact convex subset of R^n with nonempty n-dimensional interior, n>=1 and r>0, with every actual extreme point v satisfying ||v||>=r. The claim is

    C2(K) >= [r^2+(n+1)||g_K||^2]/(n+2),

with equality precisely for nondegenerate n-simplices all of whose vertices have norm r. Neither centroid zero, origin containment, smooth boundary, a finite extreme set, nor regularity of the simplex is assumed. The hypotheses ensure positive finite volume and bounded moments. Lower-dimensional or unbounded sets are not in scope.

The fresh PDF is63494bytes, SHA256`62982a0e0508edabbfea63f4b5dc69ffe928d7c657103ee3d31296a6393e5d8c`; ZIP133155bytes, SHA256`738ccb98e973b71f642f83a8abdb05559ad58073b7a2dde79e785f869e6a567c`; full TeX11101bytes, SHA256`ce8a48dc12ac9d80144a7de7391f2583c6d567c5d4d1067c3be122bf10283b29`. Actual PDF pages2–3 were also visually inspected, confirming closure bars, strict-visibility signs and the deficit formula that text extraction could obscure.

## Primary source and imported facts

The actual [FPS published article](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/DE65A193C3EE743DF0EA834A8405026E/S0008439500021561a.pdf/simplices_in_the_euclidean_ball.pdf), printed p.499, Theorem1.1 has the same centroid term and explicitly leaves general-body equality as a conjecture. Its scope is n>=2; the submitted n=1 extension is independently verified below. Lemma3.2 and its proof, pp.502–503, give the simplex moment identity. The polytope proof, pp.503–504, uses vertex-only simplices and strict convexity of the centroid term. There is no centering assumption or John/Löwner-position hypothesis in Theorem1.1; the subsequent theorems with those hypotheses are separate results. Page503 explicitly notes that centered equality simplices need not be regular in dimensions at least3.

The [primary OWR body](https://ems.press/content/serial-article-files/46255), pp.2907–2909, states the same inequality and conjectural general-body equality on p.2908. Both sources literally use “greater than” in prose while allowing equality vertices on the radius-r sphere. The submitted note explicitly chooses the mathematically meaningful nonstrict convention and separately states that strict vertex norms make equality impossible. Its proof actually establishes this nonstrict version, rather than silently depending on an inconsistent literal source statement.

The substantive proof is independently reconstructible. Its remaining standard convexity inputs do not hide a version-specific deep theorem: finite-dimensional extreme-point generation, elementary polytope facets, separability, and the null boundary of a full-dimensional convex body. For clarity, extreme-point generation itself follows by induction on dimension: a boundary point belongs to a supporting face of lower dimension; its face-extreme points are extreme in K. An interior point lies between two boundary points on a line. Iterating gives a finite convex combination of extreme points. No smoothness, exposedness of every extreme point, or closure of extK is required.

## Attack1: countable geometry, nonclosed extreme sets and tangent facets

A subspace of R^n is second countable and hence separable even when it is not closed. Therefore a countable dense D in extK can contain any prescribed initial affinely independent extreme vertices. Extreme points span the affine hull; otherwise their closed convex hull could not have interior. Every subsequently inserted distinct extreme point is outside the previous finite hull, since being in it would express that point as a nontrivial convex combination of other points of K.

The strict-visible-facet shell formula is correct even for a ray hitting an edge or vertex. Write P as finitely many facet inequalities. If the first ray intersection y had no active facet strictly violated by the apex v, then all active inequalities would hold just before y and every inactive inequality would remain strict there. This contradicts first intersection. Thus at least one genuinely visible facet contains y and covers the new point on that ray. There is at least one visible facet because v is outside the closed polytope. Coplanar facets need not contribute full-dimensional cones.

Distinct visible pyramids have disjoint ambient interiors, because an interior ray has its first intersection in the relative interior of one unique base facet. Triangulating a facet using only its vertices and coning from the new vertex gives nondegenerate full-dimensional simplices, all with vertices in extK. Their interiors are outside the old hull. Earlier pieces are retained, so disjointness persists across all stages. Incompatible subdivisions of shared lower-dimensional faces do not create overlap of n-dimensional interiors or affect volume additivity; a face-to-face simplicial-complex hypothesis is unnecessary.

The union C of the nested hulls is convex, contains the initial simplex and has closure K. To verify interior coverage without assuming closedness of C, surround any point of intK by a small simplex inside intK. Approximate its vertices by points of C closely enough that the point remains in the interior of their convex hull. That hull lies in C. Hence intK is contained in intC, and K minus C is contained in the boundary. Its volume is zero: for an interior point c, every contracted body c+(1−epsilon)(K−c) lies in intK and has volume(1−epsilon)^n|K|; taking epsilon down to0 proves the boundary-null assertion. This closes the countable-coverage step without a regularity assumption.

## Attack2: infinite equality and possible hidden boundary additions

For every retained simplex the weight is strictly positive. Pairwise overlaps lie in their boundaries; a countable union of these null sets is null. Thus the weights sum to1 and the centroid and second-moment decompositions hold. Compactness bounds all centroids and vertices, so all weighted series and variance expansions are absolutely convergent.

Direct barycentric integration gives

    C2(S)=[q_S+(n+1)||c_S||^2]/(n+2).

Substituting this into the countable moment decomposition and expanding the weighted variance gives exactly equation(4). Every q_S−r^2 is nonnegative because its vertices are actual extreme points. A zero sum of these nonnegative positive-weight terms forces every q_S=r^2 and every c_S=g_K. The first statement forces all individual vertex norms to equal r. The centroid of every nondegenerate n-simplex is in its ambient interior; two such simplices with the same centroid would therefore have intersecting interiors. The family has only one simplex. The constructed union is dense in K, so that one closed simplex equals K.

This also excludes hiding an extra extreme point in a null uncovered boundary: if K had a point outside that simplex, convexity would generate a positive-volume shell outside it. More directly, the explicit dense-union construction already forces its closure to be K. Conversely the simplex formula proves equality for every inscribed nondegenerate simplex, including off-center and nonregular examples.

## Attack3: a separate finite-witness route

I reconstructed the finite route without reading the packet's historical independent-proof file. Start with any full-dimensional extreme-vertex simplex S. If K differs from S, extreme-point generation supplies an extreme u outside S. Choose a facet of S strictly visible from u, opposite v_i, and let T be the cone from u over that facet. Both volumes a,b are positive; S and T have disjoint interiors and remain retained in every later hull decomposition. Their centroids differ by(u−v_i)/(n+1), which is nonzero.

For every larger finite hull P_m, complete the square in the two corresponding centroid terms. Dropping all other nonnegative terms yields

    Delta_r(P_m) >= ab||u−v_i||^2 / [(n+1)(n+2)|P_m|(a+b)]
                 >= ab||u−v_i||^2 / [(n+1)(n+2)|K|(a+b)] > 0.

The right side is a fixed positive number. Since the nested hulls cover intK, bounded volume integrals converge to those of K, their volumes tend to|K|>0, and their centroids converge. Passing to the limit gives the paper's exact strictness bound(5). This independently preserves a positive deficit under approximation, rather than assuming equality survives arbitrary Hausdorff approximation. It is especially relevant because the original source warns that the extreme-point norm hypothesis is not Hausdorff continuous. The chosen hulls use actual extreme points, so they preserve the hypothesis at every step.

## Exact hostile and boundary controls

The independent script imports no submitted code. It uses direct nested polynomial integration on affine standard simplices and a separate three-dimensional slice integration for a square-based pyramid. Its calculations corroborate explicit analytic arguments; they are not proof of the countable construction.

- A centered nonregular tetrahedron with vertices(1,2,2),(1,−2,−2),(−1,2,−2),(−1,−2,2) has radius3, centroid0, edge-length squares20 and32, and C2=9/5. Both deficits vanish. This rejects an illicit regularity requirement even in the unstrengthened equality statement.
- The unit-circle triangle(1,0),(3/5,4/5),(3/5,−4/5) lies entirely in x>=3/5, so the origin is outside. It has centroid(11/15,0), C2=49/75, strengthened deficit0 and unstrengthened deficit121/300. This distinguishes the two equality statements and excludes a hidden centering/origin assumption.
- Direct integration verifies the paper's triangle example, equality interval[−1,1], strict intervals[−1,2] and[2,3], and affine simplices in dimensions1 through5. A too-short interval fails the norm hypothesis and gives negative deficit, confirming that dropping the hypothesis would be invalid. Degenerate simplices are explicitly rejected.
- A genuine five-extreme-point three-dimensional shell uses S with vertices(1,1,1),(3,1,1),(1,3,1),(1,1,3), inserting u=(3,3,1). The face z=1 is tangent; only x+y+z=5 is strictly visible. Every listed point is proved extreme by an explicit uniquely maximizing linear functional. Independent slice integration gives total volume8/3, centroid(7/4,7/4,3/2) and C2=9. With r^2=3 the deficit is17/10, splitting as8/5 plus1/10. The retained-pair lower bound is exactly1/10. Incorrectly counting the coplanar bottom-face cone as positive-dimensional is detected by its zero determinant. This is a valid all-extreme-point coplanar case, rather than a planar example where one old collinear vertex ceases to be extreme.

The first local harness run stopped on a Python/SymPy Boolean identity check, not on a mathematical discrepancy. Converting the comparison explicitly to a Python bool fixed that harness issue. The initial failure record and traceback are preserved. The final run completed in1.67seconds under a25-second isolated-process-group watchdog, with cleanup in finally and empty stderr. No supplied verifier wrapper was run or promoted to proof.

## Strongest result and limits

The full stated inequality, exact equality characterization, corollary and finite positive strictness witness are supported for every stated K,n,r. Strict norms cannot attain equality, and n=1 gives only[−r,r]. No extra smoothness, finiteness, regularity or centering hypothesis is needed. No internal or external dependency gap was identified for this displayed proof.

This is an independent mathematical review, not a proof-assistant certificate or an exhaustive novelty audit. The source attribution is checked, but absence of later equivalent literature is not established. Root must read the actual paper and completed reports before adopting a result. Completion estimate:100% of this assigned adversarial review.

Only this paper's adversarial directory was written; primary bodies/renders remain in ignored cache. Earlier Basin/Langlands handoffs, original sources, site, native Sheet, shared scripts/configs, git state, releases and communications were left untouched. No outreach or outreach draft was prepared.
