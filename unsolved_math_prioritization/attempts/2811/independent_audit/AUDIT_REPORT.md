# Independent acceptance audit: 2811 / KP-3.13

## Verdict and exact accepted object

PASS_SCOPED_PARTIALS_UNCHANGED. Accept the elementary conditional results in the original 18,270-byte author archive, SHA-256 `913061fdd981ef0decf65fcc0916c58b2fd1e7ff0a70b3397459a623e0f08493`, without mathematical or source correction. The proposed queue disposition remains **unsolved, 3/5 substantive approaches**. Audit and finite replay consume no additional substantive approach. This is an independent adversarial AI audit, not human peer review. No historical novelty, complete solution, counterexample, or exhaustive current-open-status certification is accepted.

All ten original archive members are retained byte-for-byte in the enclosed original ZIP. The original external manifest and validation receipt are also retained unchanged. Their pending-audit fields record their historical author-stage status; this later, separately pinned report supplies the current verdict. There is no corrected derivative because no correction was necessary.

## Mathematical review

### 1. Finite-cover multiplicity

Proposition 1 is valid without orientability, regularity of the cover, or transversality of self-intersections. A smooth covering is a local diffeomorphism, so its composition with an embedding is an immersion. Both maps induce injective homomorphisms on fundamental groups. The embedding identifies the preimage of any target point with the embedded surface's intersection with that covering fiber. The degree gives an upper bound, with equality possible. Degree one or two is sufficient, while an arbitrary finite degree alone does not force two.

This is a conditional lemma about a specified embedded, connected, closed, pi_1-injective surface, with S^2 excluded. It does not produce that surface or a degree-two Haken cover. The ambient hyperbolic and closed hypotheses belong to the original target when the lemma is applied there; the lemma itself legitimately works more generally.

### 2. Regular-deck criterion and aliases

Proposition 2 is correct for a connected regular cover. Freeness makes the three source points z, g^(-1)z, h^(-1)z distinct, even if their translated surface subsets coincide. Transitivity supplies g and h in the converse direction. Thus the statement detects every fiber of cardinality at least three, including cardinalities exceeding three. It must quantify over labeled, distinct group elements, rather than distinct translated subsets.

The proof remains valid for nonabelian deck groups; no commutativity or normality of a surface stabilizer is used. Without freeness, three labeled translates can contain one point without giving three source points. Without transitivity, three points in a fiber need not be related by available deck transformations. These are the exact logical uses of regularity. Projection of a finite-cover embedding does not automatically satisfy the criterion.

### 3. Continuous graph lemma

Lemma 3 correctly applies Brouwer to a continuous map of the closed cube into itself. Its coordinate ranges lie strictly inside the coordinate intervals, so a fixed point is interior. The conclusion is existence, not uniqueness or transversality. The continuous theorem is not justified by the affine finite controls, nor does it require contraction. Allowing closed coordinate ranges still gives a fixed point but can put every fixed point on the boundary; losing the self-map condition can remove intersection entirely.

### 4. C1 persistence and its limits

Corollary 4 is valid. Three linearly independent normal covectors make the triple of local defining functions a coordinate chart. Disjoint source disks guarantee three distinct source points after perturbation. The fixed-square graph step can be expanded as follows. Parameterize an original branch over a square larger than the desired square, and write the projected perturbed branch as P(u)=u+e(u). On a convex intermediate square, sufficiently small C1 norm gives a Lipschitz constant less than one for e and makes P injective. For every point v of the smaller square, the map u -> v-e(u) stays in the intermediate square, hence has a fixed point. This proves uniform graph coverage; derivative invertibility makes the inverse C1. Small C0 size of the remaining coordinate then keeps the graph inside the cube. Lemma 3 supplies the common image.

The positive margin in the author's proof is therefore sufficient; no repair is required. The normal-rank hypothesis is important. For example, the three local planes x=y, y=x, z=0 intersect, but changing the first equation to x=y+epsilon removes their common point for nonzero epsilon. Such a nontransverse example is outside the corollary. The corollary neither gives a global obstruction nor permits replacing a pi_1-injective immersion by an arbitrary global regular homotopy without argument.

The exact K3 target is a point-preimage bound. It does not explicitly require transverse double curves, self-transversality, or orientability. Self-tangencies and coincident local sheets are not automatically violations when every fiber still has at most two points. No passage to generic position is needed for Proposition 1 or 2, and the persistence result is used only for an immersion that already has a transverse triple point.

### 5. Two-slope determinant grid

For u=aq-bp and v=cq-dp, the coefficient matrix has determinant D=ad-bc. Its inverse gives p=(cu-av)/D and q=(du-bv)/D with exactly the displayed signs. Distinct primitive unoriented slope representatives imply D is nonzero. Sign reversal of either input slope only reverses its determinant coordinate; it does not change the geometric exception set.

Failure of both strict inequalities is equivalent to |u| <= floor(K_alpha), |v| <= floor(K_beta). The inverse is bijective over the rationals; one must then retain integral, primitive, nonzero pairs. The omitted zero pair and free negation pairing give precisely the stated upper bound, equivalently 2mn+m+n. This remains valid if one or both thresholds are zero. Parallel or oppositely oriented aliases have D=0 and are outside the inversion formula. The count is a bound on failures of the two sufficient criteria, not a count of manifolds that fail the original target.

The four exceptional slopes in the elementary example are correct. For each fixed one-cusped parent with the specified geometric input, the residual set is finite. Exchanging that quantifier with a universal claim over all closed targets is unjustified: a prescribed target can remain among the unhandled fillings for each parent that has been supplied. No independence or uniformity in the geometric constants is proved. The note explicitly preserves this gap.

## Primary sources and target identity

The complete catalog and problem-record corpora and research-report file were rehashed independently. The unique ID 2811 record, KP-3.13 key, rank 910, statement hash, default-sorted-JSON complete-record/report-pair hash, and empty exact-key report agree. The full inherited record was inspected: its added content is literature triage, not a prior substantive proof or computation. The initial desk turn count was not used as evidence of originality.

The pinned author-preliminary K3 PDF was independently read and freshly rendered at printed pp. 131-132 and 140-141. The source distinguishes ordinary pi_1-injective maps from immersions. Problem 3.13 has the exact cardinality bound, excludes S^2, and contains no explicit orientability restriction. The scribe credit belongs to Agol and Lackenby; the nearby Hass attribution belongs to Problem 3.12. These page references are for the preliminary PDF, not a claim about final-edition pagination. The editor's public university page identifies the published book as AMS volume 295 (2026): https://math.berkeley.edu/node/172.

Cooper-Long: the pinned paper's pp. 348-349 were independently read and freshly rendered. The hypotheses are genuinely surgery-specific, and p. 349 supplies the stronger immersion statement without triple points. Accepting only an abstract subgroup conclusion would understate the source; applying it to every filling would overstate it. Source: https://web.math.ucsb.edu/~cooper/39.pdf.

Kahn-Markovic: the pinned first-page theorem statements and the accompanying immersion explanation were independently read and freshly rendered. They supply essential immersed surfaces, not the required multiplicity bound. This audit makes no unproved extension of an orientable construction to all nonorientable targets. Source: https://annals.math.princeton.edu/wp-content/uploads/annals-v175-n3-p04-p.pdf.

Agol: both the pinned preprint and final published PDF were rehashed and their introductory theorem statements read; published p. 1046 was freshly rendered and inspected. The finite-cover conclusion contains neither a degree-two bound nor the fiber-intersection condition. The preprint bytes identify arXiv:1204.2810v1 and have a separate internal typesetting date; the audit does not equate them with the final journal PDF. Published source: https://ems.press/content/serial-article-files/26202?nt=1.

Li: Theorems 1.1-1.3 and the no-triple-point observation on pp. 275-276 were independently reopened in the public web PDF text extraction. The two-sided embedded, incompressible, boundary-incompressible, non-virtual-fiber hypotheses and the stated linear dependence of the threshold were checked. No local Li PDF, PDF hash, or visual inspection is claimed. Source: https://intlpress.com/api/bgcloud-front/resource/pdf/volume/1805786337326358529-1805786337326358529-4b1249fb74fe019d620af9a9d47b861a.pdf.

A small independent targeted web search did not locate a theorem for the full exact target. This is bounded non-discovery, not exhaustive status or priority evidence. The original exact problem-site failure and repository-search counts are historical retrieval reports, not freshly established current server state. Available saved PR/commit search records were inspected; the default-branch code-search count is retained as author-stage metadata and was not independently reproduced. None is used to infer mathematical novelty or close a proof gap.

## Executable and artifact review

The original 574 regular-fiber subset controls, 1,400 slope cases, and 1,728 affine cases replay unchanged under normal and optimized Python. The independent standard-library checker adds 1,808 group subsets (including nonabelian D4), 8,832 slope cases on 24 primitive unoriented representatives, and 5,103 exact affine systems checked by Cramer's rule against the author's elimination. It tests orientation signs, integral inversion, zero-width/zero-area grids, nonintegral thresholds via floors, GL(2,Z) changes of basis, labeled-subset aliases, rank failure, and boundary countermodels. These are finite diagnostics, not certificates of geometric existence or of the universal conjecture.

All ten original integrity negatives were independently replayed, and ten further malformed-manifest, path, saved-receipt, and filesystem cases were added. All twenty reject under both normal and optimized Python. The verifier's mathematical helper routines assume their stated mathematical input domains; they are not advertised as a general adversarial API for arbitrary nonprimitive or ill-typed inputs.

The archive must be authenticated against its separately obtained external SHA-256 before running an extracted executable. A self-authenticating verifier is impossible: executing a replaced verifier and trusting its own verdict would be circular. This audit's external manifest, exact payload inventory, explicit archive/member pins, and fresh-extraction replay supply the intended integrity chain. No source PDF, source extract, dataset content, private path, or private coordination material is included in the safe package. No repository publication was performed in this audit.
