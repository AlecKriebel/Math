# Independent analytic review — 22983138

## Disposition and scope

**PASS for the full original mathematical theorem.** I found no unresolved analytic defect in the stated equality characterization, its countable extreme-vertex partition, or its retained finite witness. This conclusion covers every `n≥1`, every `r>0`, and every compact full-dimensional convex body whose **every** extreme point has Euclidean norm at least r. It does not impose a centroid, origin-containment, regularity or polytope hypothesis. The original claim has not been weakened.

The new step extends the established FPS finite-simplex argument to general bodies while preserving equality information. The original inequality, simplex moments and common-centroid rigidity for polytopes are prior FPS results, verified in the actual published proof. This is a mathematical review of the identified edition, not a worldwide priority adjudication, external human peer review, proof-assistant certification or publication authorization. Current priority remains unadjudicated in this lane. Root owns the separate full-package and promotion decisions.

## Source identity and early independence

The actual paper is **Equality in the Fradelizi–Paouris–Schütt second-moment inequality**, Alec Kriebel, dated **23 September 2026**, version **1.0.0**, four pages. The source lane authenticated the public originals before this review began. I independently checked the selected hashes:

| Authority | Bytes | SHA-256 |
|---|---:|---|
| `sources/paper.pdf` | 63494 | `62982a0e0508edabbfea63f4b5dc69ffe928d7c657103ee3d31296a6393e5d8c` |
| `sources/source-and-verification.zip` | 133155 | `738ccb98e973b71f642f83a8abdb05559ad58073b7a2dde79e785f869e6a567c` |
| `sources/published-source/owr_4136_011_equality/manuscript/paper.tex` | 11101 | `ce8a48dc12ac9d80144a7de7391f2583c6d567c5d4d1067c3be122bf10283b29` |
| Source-ready seal | — | `3c221c98107e97be91df574faef65935f19001dae45418a2edfdd5bfc5059c70` |

I read the entire actual four-page PDF, all four page images and the complete TeX. The bars over closures, the countable union, the exact normalization of the deficit, and the positive witness formula were cross-read visually. The PDF was not edited or rebuilt.

The independent initial approach was sealed before any supporting review/opinion or current sibling report was read: `independent-initial-seal.json`, SHA-256 **81d0a1e23d3b2c4cfa221ce7bb073047e3d5769f30a72ec545dbccfe3eb92b1a**. It reconstructs the partition, countable deficit, shared-interior centroid rigidity, finite witness and all principal boundary cases. Subsequent reading of the package's separate finite-approximation proof and verifier was treated as submitted support, not as a fresh favorable verdict. No current sibling or root mathematical report was read.

## Exact theorem and definitions

For a convex body `K⊂R^n`, meaning compact, convex and with nonempty interior, define

`g_K = |K|^(−1)∫_K x dx`, and `C2(K)=|K|^(−1)∫_K ||x||² dx`.

If `n≥1`, `r>0` and `||v||≥r` for every `v∈ext K`, then

`C2(K) ≥ [r²+(n+1)||g_K||²]/(n+2)`.

Equality holds exactly when K is a nondegenerate n-simplex and all its vertices have norm r. The companion equality in the weaker bound `C2(K)≥r²/(n+2)` additionally requires `g_K=0`.

The origin is fixed throughout the norm hypothesis. No translation to the centroid is silently made. Compactness gives finite moments; nonempty interior gives positive n-dimensional volume. Degenerate lower-dimensional sets and zero-volume simplices are outside these definitions. The theorem does not claim a result for unbounded bodies, dimension zero, a different norm or a different probability weight.

## Actual primary proof bodies and applicability

The fresh [published FPS journal PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/DE65A193C3EE743DF0EA834A8405026E/S0008439500021561a.pdf/simplices_in_the_euclidean_ball.pdf) was obtained, not just a metadata page. It is the eleven-page *Canadian Mathematical Bulletin* 55(3)2012 paper, pp.498–508, DOI 10.4153/CMB-2011-142-1. I read physical pp.1–3 and5–7, including the exact Theorem 1.1 and following conjecture, both moment lemmas and their full proofs, and the full relevant proof of Theorem 1.1. Formula pages2,5,6,7 were visually checked. I did not claim to read all eleven pages or the unrelated John/Löwner-position results.

On printed p.499 the original theorem already includes the centroid correction and characterizes equality for polytopes. The following paragraph explicitly leaves general-body equality conjectural. Printed pp.502–504 contain the simplex moment formula, vertex triangulation and strict-convexity/common-centroid argument. The final general-body step proves the inequality by approximation and does not retain equality information. This establishes the precise historical target and the substantial prior mechanism being extended.

The fresh [published OWR volume](https://ems.press/content/serial-article-files/46255) was also obtained. I read the complete Fradelizi contribution on printed pp.2907–2909, physical pp.57–59, and visually checked p.2908. It gives the same centroid-corrected theorem and general-body equality conjecture. These are historical source statements, not evidence of current worldwide open status. The attempted author-hosted FPS PDF failed ordinary TLS certificate verification; it was not substituted for the successfully obtained journal body or fetched by disabling verification.

Both original theorem statements use prose saying the extreme norms are greater than r while their equality statements put vertices exactly on the sphere. Crucially, the published simplex remark on p.503 explicitly uses `≥r`. The current manuscript makes the intended non-strict condition precise. Its proof establishes that formulation directly. If the condition is interpreted literally as strictly greater at every extreme point, equality is impossible; the current proof proves that too. The original sources work initially with `n≥2`, while the current `n=1` extension is checked directly below. No primary theorem with an incompatible category or hidden centering condition is imported.

All primary raw bodies, text and renders are in an **entirely ignored** `primary-cache/` directory established before acquisition. `primary-acquisition.json` and `read-ledger.json` bind the actual editions, response hashes, read pages and failed author route. No third-party body or excerpt was prepared for public distribution.

## Reconstructing the extreme-vertex partition

The only general convex-geometric starting fact needed is the finite-dimensional extreme-point representation of a compact convex set. Its applicability is exact here. One can verify the relevant form by induction on affine dimension: a boundary point lies in a proper exposed face from a supporting hyperplane; extreme points of that face are extreme in K; interior points lie on a chord with boundary endpoints. Inducting on those faces expresses points as convex combinations of extreme points. In particular, `ext K` affinely spans `R^n`. No infinite-dimensional compactness theorem or closedness of the extreme set is required.

Choose `n+1` affinely independent extreme points to form the initial nondegenerate simplex. Since a subspace of a second-countable metric space is second countable and separable, `ext K` has a finite or countable dense subset D; adjoining the chosen vertices preserves that property. List distinct points with the initial simplex first. Every later point v is outside the old finite hull: if an extreme point were a convex combination of other points of K, its extremality would force those participating points to coincide with v. Distinct enumeration excludes that possibility. Every old listed point also remains extreme in each later hull.

For the full-dimensional old polytope P, use its finite facet inequalities. A facet is strictly visible from v precisely when its inequality is violated at v. At least one is visible because v is outside P. The shell of `conv(P,v)` is the union of pyramids from v to these facets. To check coverage, take a point in the new hull outside P and follow its ray from v to its first meeting y with P. The point lies between v and y. Some active inequality at y must be violated at v; otherwise the inactive inequalities remain strict just before y, and the active ones hold there, contradicting first meeting. Thus y lies on a visible facet. The apex is covered as well.

Interior points of distinct visible pyramids have distinct relative-interior base facets at their unique first intersection with P. Hence their interiors are disjoint and outside the old P. Facets merely coplanar with v contribute no full-dimensional pyramid and need not be included. This handles horizon faces and points incident to several facets without a generic-position assumption.

Each visible facet admits a finite decomposition into simplices using its own vertices. The finite proof is the same inductive vertex-coning construction credited to FPS: select a vertex, triangulate facets not containing it, and cone. Rays from the selected vertex cover the interior, and finite closedness covers the boundary. The base case is a point, so dimension one is included. Coning each strictly visible base simplex to v gives nondegenerate n-simplices. All their vertices are in D and hence in `ext K`.

Retain every old cell rather than retriangulating the growing hull. Newly added interiors lie outside the entire old hull, so interiors remain disjoint across all stages. Each stage adds finitely many cells; their overall family is finite or countable. Compatibility along lower-dimensional face subdivisions is unnecessary for the volume identities. The union of cells is exactly `C=⋃P_m=conv D`, not merely a collection of unrelated approximations.

Density gives `closure C=K`. C is convex and contains a nondegenerate simplex. For any interior point x of K, choose a sufficiently small simplex surrounding x inside K and approximate its vertices by points of C. Strict positive barycentric coordinates persist under small vertex perturbations, so x lies in the interior of that perturbed simplex in C. Thus `int K⊂C`; the reverse interior inclusion is immediate. Consequently `K\C⊂∂K`.

The boundary has zero n-dimensional volume: choose an interior point o, contract K about o by any factor `0<t<1`, and note that the contraction lies in `int K`. The boundary is therefore contained in the difference between K and its contraction, whose volume is `(1−t^n)|K|`; let t increase to 1. This also checks the needed measure fact directly. Pairwise intersections of full-dimensional simplices with disjoint interiors are in their boundaries, and a countable union of these null sets is null. The partition lemma is therefore valid with the exact extreme-vertex and almost-everywhere coverage requirements, including infinitely many or nonclosed extreme-point sets.

## Reconstructing the moment and countable deficit

For a nondegenerate simplex with vertices `x0,…,xn`, write `X=Σλ_i x_i` in uniform barycentric coordinates. Integrating on the standard simplex gives

`Eλ_i=1/(n+1)`, `Eλ_i²=2/((n+1)(n+2))`, and `Eλ_iλ_k=1/((n+1)(n+2))` for `i≠k`.

Expansion of `||X||²` yields

`C2(S)=[Σ||x_i||²+||Σx_i||²]/((n+1)(n+2))=[q_S+(n+1)||c_S||²]/(n+2)`.

This formula is the established FPS lemma; the present barycentric derivation is a direct check of it. Its affine-coordinate derivation does not assert affine invariance of the Euclidean objective or move the origin in the norm assumption.

For the partition, set `w_j=|S_j|/|K|>0`. Coverage and null overlaps give `Σw_j=1`, `Σw_j c_j=g_K`, and `C2(K)=Σw_j C2(S_j)`. These are legitimate countable identities. Compactness bounds every coordinate, vertex norm, centroid and cell moment. Absolute convergence therefore holds even for the signed first-moment series, and no unproved interchange of conditionally convergent terms occurs.

The weighted variance expansion then gives exactly

`Δ_r(K) = (1/(n+2))Σw_j(q_j−r²) + ((n+1)/(n+2))Σw_j||c_j−g_K||²`.

Every radial excess is nonnegative because **all** cell vertices are extreme points of K, rather than arbitrary boundary points introduced by a triangulation. The variance terms are nonnegative as well. The countable sums are finite by boundedness. This proves the inequality without importing an unchecked global prerequisite.

## Equality and its finite strictness witness

If the deficit is zero, every term of both nonnegative series is zero, since each cell has positive weight. Thus each cell's average squared vertex norm equals r²; with every vertex norm at least r, each individual vertex lies on the radius-r sphere. Also every centroid equals `g_K`.

The centroid of a nondegenerate simplex is strictly inside that simplex, as all its barycentric coordinates are positive. If there were two cells, their common centroid would lie in both interiors; the intersection would contain a small ball, contrary to disjoint interiors. Hence there is exactly one cell. Its closedness and the density of the constructed union give `K=S`. Conversely, any nondegenerate simplex with all vertices of norm r has `q_S=r²` and satisfies equality in the moment formula. No regularity or centering step is missing.

The alternative finite witness is also sound. Start with any extreme-vertex simplex S. If `K≠S`, some extreme point u lies outside S, since otherwise the extreme-point representation would put all K inside S. Insert u next. A strictly visible facet of the initial simplex is opposite one vertex `v_i`; coning it to u produces a nondegenerate T with disjoint interior. Both cells are retained forever. They have positive volumes a,b and centroid difference `(u−v_i)/(n+1)≠0`.

The exact two-term identity

`a||p−z||²+b||q−z||² = ab||p−q||²/(a+b)+(a+b)|| (ap+bq)/(a+b)−z||²`

keeps the pair's contribution uniformly positive and gives

`Δ_r(K) ≥ ab||u−v_i||² / ((n+1)(n+2)|K|(a+b)) > 0`.

The finite-approximation version retains these same cells in every P_m. Replacing its denominator `|P_m|` by the larger `|K|` weakens the lower bound in the correct direction. Volume, first moment and second moment converge by dominated convergence: the nested union contains `int K`, its complement is null, and all integrands are bounded on K. Therefore the same fixed positive bound survives the limit. Mere strictness of each polytope, without a retained positive bound, would not suffice; this proof supplies the required bound.

This is a body-dependent finite strictness witness. It is not an asserted uniform stability modulus or a new classification for arbitrary measures. Dimensional scaling is correct: the volume ratio is dimensionless and the remaining norm contributes squared length.

## Boundary, singular and normalization cases

- In dimension one, `K=[a,b]` with `a<b`, `g=(a+b)/2` and `C2=(a²+ab+b²)/3`. The deficit is `(a²+b²−2r²)/6`. Endpoint norms at least r force equality exactly at `a=−r,b=r`. There is no missing exterior extreme point when the initial interval already equals K.
- If every extreme norm is strictly greater than r, at least the initial cell's radial excess is strictly positive. Equality cannot arise merely because the infimum of those norms might be r.
- Positive volumes are indispensable. Degenerate cells are never used: the initial vertices are affinely independent, and later apexes are strictly outside their visible base hyperplanes. Lower-dimensional K is outside the theorem's volume definition.
- No closedness, finiteness, exposedness or positive-curvature hypothesis on `ext K` is needed. Density is in the extreme set's metric subspace, and all selected points are actual extreme points.
- Arbitrary approximating polytopes would not preserve the unusual extreme-norm assumption. The actual construction does preserve it because every chosen vertex belongs to `ext K`. This directly addresses the failure of Hausdorff stability noted by FPS.
- Countably many positive weights can tend to zero, but a zero nonnegative series still forces each summand to vanish. The fixed initial cells in the strictness proof prevent a positive deficit contribution from disappearing in the limit.
- The strengthened equality permits nonregular simplices and nonzero centroids. A rational example with vertices `(1,0),(3/5,4/5),(3/5,−4/5)` lies entirely in `x≥3/5`, excludes the origin, is nonregular, and gives `g=(11/15,0)`, `C2=49/75`, equality for r=1. Thus no origin-containment assumption is hidden. The manuscript's different nonregular triangle is correct as well.
- The weaker bound discards the nonnegative centroid term; its equality therefore requires both strengthened equality and centroid zero. FPS already explains why centered planar equality is regular while higher-dimensional centered equality need not be. No stronger regularity claim is made here.

## Independent calculations and submitted support

After the initial seal, I read the complete submitted separate finite-approximation proof and its boundary discussion, and the complete verification program statically. Its favorable conclusion was not adopted as a fresh verdict. No submitted checker, packaging tool or build script was executed, imported or compiled. Other historical audit opinions remain inventoried rather than used as validation.

The owned `check_exact.py` uses SymPy1.14.0 through the shared runtime, with no new environment or installation. All **121** exact controls passed. The moment path uses repeated elementary polynomial integration over standard simplices instead of invoking the factorial moment formula being checked. It covers barycentric coefficients and explicit full-dimensional simplices in dimensions 1–4, off-origin/nonregular equality and strict-radius cases, and the general completed-square identity.

A separate three-dimensional shell control starts with a cube, retains its six tetrahedra and inserts an apex beyond a **square** facet. The visible square is split into two triangles, producing two new tetrahedra. Exact cell integrals agree with independent one-dimensional cross-section integrals for the combined body: volume `28/3`, first moment `(5/3,0,0)`, second-moment integral `32/3`. Its retained pair gives the strictly positive witness `11/420`, below the full deficit. This checks a nonsimplicial base and the coefficient of the retained witness, rather than merely retesting simplex equality. Degenerate simplex rejection and direct interval and Euclidean-ball radial integrals are also checked.

These finite controls support the displayed formulas and examples. They do not establish the countable geometric construction or universal equality by exhaustion; the analytic reasoning above does that. The control process finished under a 45-second process-group timeout wrapper, with termination/escalation specified for timeout. There were no failed mathematical controls or extended repair attempts.

## Final evidence and remaining scope

The complete actual theorem is analytically verified. The load-bearing moment and finite-polytope argument have been checked in the actual published primary body; the new countable/finite-retention extension has a complete argument and no remaining mathematical gap found. Historical attribution and present priority are separate from this mathematical verdict, and no failed search is used as novelty evidence.

`verdict.json` records the full mathematical PASS and a false publication/promotion clearance. `read-ledger.json` gives each authority's exact reading extent and identifies unread historical opinions. `custody-before-after.json` records unchanged original authorities and extracted members. `SEAL.json` and SHA-256 manifests bind the complete handoff. Root must read the full report and other independent lanes before its separate decision.

Only `reviews/analytic/` was changed. Sources, prior Basin and Langlands packages, sibling reviews, shared scripts, public content/configuration/site, native Sheet, Git, UI, releases and external communications remain untouched by this task. No outreach was prepared. Completion is 100% of the assigned analytic review, without a claim that the paper has passed every programme gate.
