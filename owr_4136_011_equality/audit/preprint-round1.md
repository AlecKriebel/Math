# Independent preprint review, round 1

- Reviewer: fresh adversarial mathematical referee (OpenAI Codex subagent).
- Review started: 2026-09-23T13:33:48Z.
- Final checks completed: 2026-09-23T13:35:33Z.
- Scope: readiness of the existing four-page manuscript for an **unrefereed preprint**, not journal acceptance, a global priority certification, or permission to publish.
- Independence: reconstructed the argument before consulting FPS and OWR; did not read earlier proof audits or rely on their verdicts. Only this report was added; the manuscript, verifier, and publication files were not edited. No external communication was initiated.
- Completion estimate: **100% of this review scope**. No actionable finding remains in the reviewed manuscript.

## Reviewed inputs

SHA-256 hashes (manuscript/PDF/verifier rechecked at the end):

| File | SHA-256 |
| --- | --- |
| `manuscript/paper.tex` | `ce8a48dc12ac9d80144a7de7391f2583c6d567c5d4d1067c3be122bf10283b29` |
| `output/pdf/paper.pdf` | `62982a0e0508edabbfea63f4b5dc69ffe928d7c657103ee3d31296a6393e5d8c` |
| `verification/verify.py` | `9896313fe2cebcd5ed0bed6aef77b649a7c369fe72a56e768d3dda28489e4764` |
| `sources/fps2012.pdf` | `1338d24d5b312a80a45ff6b173108648517bbdca141f66ff14c58613e9e77d16` |
| `sources/owr2009.pdf` | `e3c62551bf9bb9fadefc98d7f6bb82661a254ba6ff93c42b4afbf8eef21bf6cd` |

Also inspected the verifier README, source provenance, project README, license, citation file, and Zenodo description/upload fields. Archive and public-site consistency are being inspected separately by the coordinating agent and are not certified by this report.

## Claim and independent reconstruction

The exact claim is that a compact, full-dimensional convex body in R^n, n >= 1, whose extreme points have Euclidean norm at least r > 0 satisfies

    C_2(K) >= [r^2 + (n+1)||g_K||^2]/(n+2),

with equality exactly for full-dimensional simplices all of whose vertices have norm r. No origin-containment, zero-centroid, smoothness, or closedness assumption on the extreme-point set is present or needed.

I reconstructed the following chain without using earlier audit conclusions:

1. Extreme points affinely span the body. Choose an initial extreme-vertex simplex, extend its vertices to a countable set dense in the extreme-point set, and form the increasing finite convex hulls. Every newly enumerated extreme point lies outside the old hull: otherwise its nontrivial finite convex representation would contradict extremality in K.
2. If an exterior point is added to a full-dimensional polytope, the new region is covered by cones over strictly visible facets. The first-hit ray argument proves exact coverage, including boundary rays. Two such cones cannot share an interior point because that ray has a unique first point in the old polytope, and for a pyramid interior point this first point is in the relative interior of its base facet.
3. Each facet is convex, so the recursive vertex-coning argument partitions it into simplices using only its own vertices. These are vertices of the old polytope and hence members of the chosen extreme-point set. Strict visibility makes every resulting full-dimensional cone nondegenerate. Earlier simplices are retained, so the limiting family has disjoint interiors.
4. The union C of the increasing finite hulls equals conv D. Its closure is K. The usual finite-dimensional convex-set identity int C = int(cl C), also explained in the manuscript by a perturbed enclosing simplex, gives int K contained in C. The omitted subset is therefore a null subset of the boundary. Countably many simplex boundaries have zero volume, so the integration identities follow.
5. Direct barycentric integration gives the simplex formula with coefficients 1/[(n+1)(n+2)]. Summing it and expanding the weighted centroid variance gives exactly the two nonnegative terms in equation (4). Compactness bounds every moment and centroid, making all series absolutely convergent.
6. If the deficit is zero, each positive-volume simplex has centroid g_K and every vertex has norm r. A nondegenerate simplex contains its centroid in its interior. Consequently two retained simplices cannot both occur. Density then identifies the sole closed simplex with K. The simplex formula proves the converse.

This chain proves the stated theorem; it does not silently import the desired rigidity from finite approximation.

## Adversarial checks and outcomes

| Potential failure | Evidence and outcome |
| --- | --- |
| Nonclosed extreme-point set | Density is taken in the subspace ext K; no limit point is inserted as a vertex. The closure is taken only after forming conv D. This avoids requiring ext K to be compact or closed. Pass. |
| Coplanar or tangent facets in a shell | If all facet inequalities active at the first-hit point held at the new apex, sufficiently nearby points toward the apex would satisfy every inequality. This contradicts first intersection. Thus some strictly visible facet always covers the ray, even if other active facets are coplanar. Pass. |
| Facet subdivisions not forming a global simplicial complex | The proof requires disjoint full-dimensional interiors and null overlaps, not matching face subdivisions. Finite facet partitions supply precisely that. Pass. |
| Infinitely many positive pieces with arbitrarily small weights | Zero of a convergent sum of nonnegative terms forces each individual term to vanish; no uniform positive lower bound on weights is needed. Pass. |
| Equality with a nonsimplex differing only on its boundary | In this construction the union is dense in K. Once the family reduces to one closed simplex, no extra point of K can remain. Pass. |
| Dimension one | Every body is an interval, its two endpoints are its extreme points, and the initial simplex is already the whole body. The only equality interval has endpoints of norm r, namely [-r,r]. The dimension-zero facet base convention also presents no difficulty. Pass. |
| Bodies outside the origin / nonzero centroids | The identities use the original coordinates throughout. For the displayed triangle, the vertex-square sum is 3 and the squared vertex-sum is 1, so C_2 = 4/12 = 1/3 and g = (0,1/3), exactly as stated. Pass. |
| Strict norm assumption without a uniform margin | Equality still forces each chosen vertex to have norm exactly r, so a strict hypothesis precludes equality even when the infimum of extreme-point norms is r. Pass. |
| Finite witness constant and limit | For retained volumes a,b and centroids p,q, completing the square gives a||p-z||^2+b||q-z||^2 >= ab||p-q||^2/(a+b). Substituting p-q = (v_i-u)/(n+1) yields exactly equation (5). Since |P_m| <= |K|, its positive bound survives bounded integral convergence. Pass. |

For the finite witness, if K differs from the initial simplex S, the extreme-point representation guarantees an extreme point outside S; otherwise the closed convex set S would contain K. Its strict visibility yields a positive-volume second simplex. In dimension one the nonsimplex premise cannot occur. There is no unresolved gap in this alternative argument.

## Original-source comparison

I read the primary PDFs directly, including FPS pp. 498–499 and 502–504 and OWR pp. 2907–2909; I also visually inspected the theorem/conjecture pages.

- FPS Theorem 1.1 (p. 499) contains the same strengthened inequality and gives the same equality class for polytopes. The paragraph immediately following explicitly leaves the general-body equality case open and conjectures the same answer.
- FPS Lemma 3.2 (p. 502) is algebraically the manuscript's simplex moment identity. The proof on pp. 503–504 already uses the finite simplex partition and centroid equality argument. The manuscript accurately presents its contribution as retaining this mechanism for general bodies, not as discovering the inequality or finite equality argument.
- OWR p. 2908 records the same theorem and general-body equality question. The reference to that page is correct. The manuscript does not confuse this statement with the distinct Loewner-position theorem.
- Both original statements literally say “greater than” while their equality clause permits vertices on the radius-r sphere. The manuscript explicitly identifies this textual issue and states its non-strict assumption precisely. FPS's discussion on p. 503 also explicitly uses the non-strict vertex hypothesis. No hidden strengthening or source mismatch results.
- FPS and OWR introduce the main setting for n >= 2; the manuscript states its n=1 extension explicitly, and the interval calculation verifies it. The catalogue's narrower dimensional description does not restrict the proved claim.

The correct contribution is the general-body equality proof. The bounded-priority and unrefereed-status wording does not imply that this review certifies worldwide novelty or external human peer review.

## Computation and preprint presentation

The verifier's affine polynomial integration does not invoke the vertex-sum moment formula being tested; the polygon moment computation is also separate from the simplex integration. Its exact arithmetic and limited finite scope are accurately described. A normal run and an optimized run both produce identical JSON, matching `output/verification.json`: **298 checks across 18 finite cases**. None of these results is needed to justify the infinite argument.

I rendered and visually inspected all four current PDF pages. All formulas, closure bars, norm signs, references, and page transitions are readable. There are no clipped equations, missing glyphs, overlaps, or unresolved references. The theorem, argument, finite witness, attribution, author/ORCID, version/date, and unrefereed/AI-assisted disclosure are present. The publication description and citation metadata agree with the mathematical scope. I found no substantive preprint packaging defect in the files within this review's scope.

## Findings, remediation, and verdict

- **Correctness blockers:** none found.
- **Useful minor corrections required before preprint publication:** none found.
- **Mandatory remediation:** none.
- **Optional tastes:** no revisions requested merely for stylistic preference. Expanding standard convexity facts or adding more finite examples is not necessary to check this proof.
- **Remaining mathematical gap:** none identified in the stated theorem, equality classification, corollary, or finite witness.
- **Limits of the verdict:** this is an independent AI adversarial review, not a proof-assistant verification, an external human referee report, or a global priority search. Archive/public-site consistency is outside this report's narrow packaging check.

**Verdict: ready as an unrefereed preprint on the reviewed evidence, with zero actionable findings.** This is a stopping verdict for the mathematical review/fix loop at the reviewed hashes; further changes that alter the proof would need review in their own right.
