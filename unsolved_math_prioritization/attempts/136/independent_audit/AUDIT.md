# Independent audit: Balanced Ham Sandwich Line

Problem ID 136; catalog label GREEN-048; queue rank 879. Audit date: 6 October 2026.

## Verdict

The authored mathematical partial theorem is correct under its stated hypotheses. Its proof needs no mathematical repair. Accept the corrected derivative for a bounded partial / unresolved result, with no novelty claim and no full solution. The original prose needs a narrow source-assessment qualification: an example with minimum discrepancy exactly 2 cannot, by itself, establish that a universal bound of 2 is true, or that no stronger Alon example exists. The actual wording patch has been applied and replayed byte-for-byte. The immutable author input remains unchanged.

Acceptance is attached separately in ACCEPTANCE.md and identifies the exact corrected archive and external manifest. This audit does not authorize or perform publication.

## 1. Intake, identity, and inherited work

Independently recomputed the SHA-256 and byte counts of the original ZIP and its external manifest. Both match the supplied pins. The ZIP has exactly six regular data members, no duplicate member names, and no executable mathematical checker. Every member's byte count and SHA-256 matches the external manifest and the corresponding author file. ZIP CRC readback passed.

The complete catalog, complete problems corpus, and complete research-report corpus were parsed from their full verified files, not selected fragments. Their byte counts and SHA-256 values match all three author pins. Exactly one catalog entry and one problem entry match ID 136. The catalog verifies GREEN-048, title, rank 879, and the five-approach budget. The full target record, including its background, was inspected. It contains dated generic literature triage, not a substantive mathematical attempt.

There is no GREEN-048 key in the full report map. Under the specified reports.get(problem_number, {}) convention, the report is therefore exactly the empty object. The default sorted-JSON serialization of the complete problem/report pair has 2,579 bytes and SHA-256 19fa0cfb10a536a00ec1b4c2bc1954b2e269e018c8aaef2a906f8accf1369402. The target statement has 198 UTF-8 bytes and its independently recomputed hash matches the pinned value. No raw corpus record or dataset content is included in this package.

The author's three mathematical approaches are accurately distinguished: angular blocks, perturbation/limits, and structured subclasses. This review adds no research approach. Its exact-integer sanity checks only test existing claims. The author's historical GitHub searches are attributed as its bounded search record; this audit does not certify an exhaustive search of all branches, commits, or prior work.

## 2. Mathematical target and conventions

The intended domain is a finite set X of n >= 2 distinct points in the real affine plane. A determined straight line contains at least two distinct members of X. Its discrepancy is the absolute difference of its two open-half-plane counts; all points on the line are excluded. The minimum over all determined lines is D(X). More than two points may lie on an admissible line. There are no multiplicities, weights, or general-position assumptions.

The source-to-catalog mapping is correct: the target is Problem 75 on printed page 36 of the inspected Green PDF. GREEN-048 is a catalog identifier, not that PDF's problem number. The bound in the target is inclusive: D(X) <= 100. A counterexample must have discrepancy at least 101 on every determined line. The raw omission of n >= 2 is a domain convention, not a claimed resolution by the empty set or a singleton.

Using both closed half-planes instead would add the same on-line count to both sides and preserve their difference. Arbitrarily assigning boundary points to just one side would change the problem. The discrepancy is neither half the side-count difference nor the distance of a flip's center from the middle rank. In allowable-sequence notation a block [a,b] has counts a-1 and n-b, so its discrepancy is |n+1-a-b|, twice the center-offset magnitude. No such factor is used to reconcile the disputed numeric threshold.

A conjecture asserting some universal constant is not literally a theorem with constant 100. Nor may the stronger many-points-on-each-side statement be silently identified with the discrepancy statement. The author correctly leaves these reductions and numeric constants unclaimed.

## 3. Complete analytic check of the local theorem

Let p be exposed in the stated sense: one vector u has u dot (q-p) > 0 for every other point q. All nonzero directions q-p lie in one open semicircle. Opposite rays cannot occur. Equal directions therefore describe exactly the entire intersection of X with a determined line through p, except for p itself. This is the point at which exposure, distinctness, and straightness are used.

For completeness, every vertex of a finite convex hull has this property. If p is such a vertex, it is outside the compact convex hull of the remaining points. Let z be the closest point of that hull to p, and take u=z-p. The minimum-distance condition gives u dot (q-p) >= ||u||^2 > 0 for each other q. Existence of at least one exposed point also follows from a generic linear functional having a unique minimum. A collinear set's endpoints are exposed. A nonvertex on a hull edge is not implicitly admitted as a pivot.

Order the direction blocks B_1,...,B_t inside that open semicircle. Write r_i=|B_i|, s_i=sum of the earlier block sizes, and N=n-1. Each block is nonempty and t>=1. The line through p and B_i contains exactly r_i+1 distinct points. Earlier and later blocks are strictly in opposite half-planes, because angular differences have magnitude strictly less than pi and determinant signs cannot change within either side. Thus the counts are s_i and N-r_i-s_i, giving exactly

    d_X(ell_i) = |N-r_i-2s_i|.

No simultaneous collinear block is divided between half-planes.

For n=2h, the block containing expanded-list position h satisfies s_i <= h-1 and s_i+r_i >= h. Let a=h-1-s_i and b=s_i+r_i-h. Both are nonnegative, a+b=r_i-1, and a-b=N-r_i-2s_i. Therefore

    d_X(ell_i) <= r_i-1 = |X intersect ell_i|-2.

For n=2h+1, n>=3 and h>=1. The block containing position h satisfies a=h-s_i >=1 and b=s_i+r_i-h >=0. Now a+b=r_i and a-b=N-r_i-2s_i. Therefore

    d_X(ell_i) <= r_i = |X intersect ell_i|-1.

The selected position exists and is in exactly one block in both cases, including when it lies at a block endpoint. With e=n mod 2 and m_p the largest collinearity through p, this proves the claimed local theorem for every exposed p:

    d_X(ell_i) <= m_p-2+e.

Taking a minimum over exposed p and then using m_p<=m proves the global bound D(X)<=m-2+e. The argument is finite and exact and has no hidden genericity or compactness limit.

## 4. Degeneracies, parity, and small configurations

- n=2: there is one determined line, one block with r=1, no off-line point, and discrepancy 0. The bound is exactly 0.
- n=3: a noncollinear triple has discrepancy 1 on each determined line; a collinear triple has discrepancy 0. The odd proof starts at h=1 and covers both.
- Fully collinear sets of arbitrary size: an endpoint has one block of size n-1. The exact formula gives 0, regardless of the weaker displayed upper bound.
- Collinear hull edges: every genuine vertex remains an admissible exposed pivot. All points on a common ray form one block, including many points on a hull edge. There is no assumption that hull edges contain just their endpoints.
- Equal angular directions, large blocks, one block, vertical directions, and angular-order endpoints cause no exceptional case. A suitable angular coordinate on the open semicircle avoids any branch-cut ambiguity.
- Nonexposed pivots may have opposite rays and are outside the proof's hypothesis. The audit does not replace an exposed vertex by an arbitrary boundary or interior point.
- In general position every determined line has exactly two points. The upper bound is e. If n is odd, its n-2 off-line points force an odd positive discrepancy, so D(X)=1. For even n the upper bound already gives D(X)=0.
- For a general degenerate line containing k points, discrepancy has parity n-k, not necessarily parity n. No incorrect global parity lower bound is used.
- At the claimed cutoff, m_p<=101 suffices for both parities; even n also allows m_p=102. Failure of the target implies m_p>=102 at every exposed vertex for odd n and m_p>=103 for even n. Integer rounding is correct.

As a supplementary check, exact integer determinants were evaluated for all 502 subsets of size at least two of a 3-by-3 integer grid. All 1,848 exposed-vertex checks, all 6,112 angular-block line identities, the combined global bound, and the general-position/collinear implications passed. All 86 centrally symmetric configurations in that finite collection had discrepancy 0. These counts are only finite sanity checks, not a universal proof, a formal verification, or a claim that every configuration type was enumerated. No checker source, checker fingerprint, or tested pointset dataset is included.

## 5. Perturbation, rich lines, symmetry, and weights

### Perturbation and limits

Small disjoint neighborhoods preserve distinct labelled points. At each successive choice, avoiding finitely many previously determined lines produces general position. For a convergent sequence of such configurations, some selected pair of labels occurs infinitely often, because there are finitely many pairs. Distinctness of its limiting endpoints prevents degeneration of the defining line. The signs of points off the limiting line stabilize by continuity of a nonzero determinant.

If k original points lie on the limit line, only the k-2 nonendpoint boundary points can contribute disappearing signs. In each approximating general-position configuration their total has absolute value at most k-2. Combining that with the e discrepancy bound gives |S|<=e+k-2. Stabilizing their individual signs is unnecessary. This proves the claimed global estimate, not the stronger local estimate from a specified original vertex.

The proposed loss example is valid: keep two distinct x-axis endpoints, approach M additional distinct x-axis locations from above, and keep M distinct points below. The fixed determined x-axis has equal counts before the limit and discrepancy M after it. All limiting locations can be distinct, and small generic choices preserve strict signs while avoiding accidental collinearities. This is only a counterexample to preservation of the discrepancy of a chosen line, not a counterexample to the existential target.

### Rich lines

A line containing m points leaves n-m off-line, so its discrepancy is at most n-m. A line with at least n-100 points solves that instance. Combining this with the proved global bound gives D(X)<=min(m-2+e,n-m). If D(X)>=101, every determined line must leave at least 101 points off it. There is no sufficiency claim for these necessary conditions.

### Central symmetry

For the involution q -> 2c-q, n>=2 and distinctness ensure a member x different from c. Its distinct antipode belongs to X. Their common line through c is determined. Every off-line point has a different antipode in the opposite open half-plane; every on-line point stays on-line. The only possible fixed point is c, which is excluded from the counts if present. Therefore this line has discrepancy 0, including odd cardinality, arbitrarily large collinear blocks, and the fully collinear case.

### Multiplicities

Three noncollinear locations of equal weight M give weighted discrepancy M for every line through two distinct locations. This establishes only that the changed weighted model has a different answer. It is not a distinct-point counterexample. The author explicitly preserves that distinction.

## 6. Primary sources and the threshold issue

### S1: Green

The author-hosted [100 Open Problems](https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf) was reopened through the public web and the pinned PDF was inspected locally. A fresh render of printed page 36 confirms Problem 75, the inclusive threshold 100, the comment about failure at 2, and the separate pseudoline remark. Its introductory footnote identifies December 2025 as the most recent update. The catalog label and any inherited January 2026 description do not change that inspected date.

### S2: Pinchasi

The [author publication page](https://sites.google.com/view/homepage-of-rom-pinchasi/home) links the pinned [19-page manuscript](https://drive.google.com/file/d/1lrOLgVoLd7NFTNDs-Az2BaBfQ8lLOgfZ/view). Pages 1-2 and 19 were re-inspected, including a fresh page-2 render. Theorem 1.2 concerns noncollinear finite sets and an asymptotic extremal bound for lines with many points in each open half-plane. Page 2 separately explains the O(log log n) discrepancy consequence and handles collinear sets by discrepancy 0. Integer rounding and strict-size requirements can be absorbed in the asymptotic constants; no explicit numerical constant 100 is extracted. Conjecture 7.1 is the constant-additive many-points formulation. The full theorem proof was not independently verified.

Page 2 explicitly states D(G)=2 for Alon's 12-point construction. This disproves a universal bound of 1. It proves neither that bound 2 always holds nor that a distinct stronger example cannot exist. The primary reference for Alon there is personal communication, so this audit is not a comprehensive audit of all Alon constructions. The [institutional journal record](https://cris.technion.ac.il/en/publications/lines-with-many-points-on-both-sides/) confirms the 2003 publication and journal pagination.

### S3: Conlon and Lim

The [author-hosted manuscript](https://www.its.caltech.edu/~dconlon/pseudolines.pdf), introduction and Theorems 1.1-1.3, distinguishes straight-line sets from generalized configurations with pseudolines. Its lower construction is in the latter setting. Straight-line realizability is not established for those examples, so they do not refute any constant straight-line bound. Its introduction reports no stronger straight-line example than discrepancy at least 2 as known. That is a dated literature statement, not a proof of impossibility. The [arXiv record](https://arxiv.org/abs/2308.02466) identifies version 2 dated 7 April 2025. The [institutional publication record](https://ora.ox.ac.uk/objects/uuid%3A0318561b-88cc-4e3c-9b79-391935adffea) confirms the 2025 Advances in Mathematics article. Manuscript and journal pagination differ. No full replay of the construction is claimed.

### S4: Subercaseaux, Mackey, Qian, and Heule

The pinned [arXiv v1](https://arxiv.org/html/2506.00224v1) was checked in both HTML and PDF text. It uses absolute side-count difference, reports the k>=3 straight-line existence question as open, and reports a smallest odd 2-everywhere-unbalanced example of size 21. The construction, SAT minimality work, and realization were not independently reproduced. Abstract combinatorial satisfiability alone does not establish planar realizability. The [arXiv record](https://arxiv.org/abs/2506.00224) still displayed v1 dated 30 May 2025 at review time. A [Springer proceedings record](https://link.springer.com/chapter/10.1007/978-3-032-07021-0_3) now lists the paper in 2026, CICM 2025, LNCS 16136, pages 29-47. Only that record's public metadata and abstract were inspected, not the subscription chapter. The 2025 open-status statement is therefore explicitly version-qualified.

### S5-S6: 2026 discussion

Kalai's [September discussion](https://gilkalai.wordpress.com/2026/09/02/annotated-slides-micha-a-perles-90th-birthday-meeting/) and [July meeting page](https://gilkalai.wordpress.com/2026/07/16/micha-a-perles-90th-birthday-meeting/) continue discussing the conjecture and Pinchasi's result. Slide 12 of the pinned public lecture slides was inspected through its text XML, without a visual rendering claim. Its informal log-log display is not an explicit leading-constant-one theorem. These are corroborating discussions, not exhaustive current-status evidence.

### Accepted conclusion about the discrepancy

The Green and Pinchasi numerical statements do not alone form a logical contradiction: the latter identifies one example, while the former could in principle refer to a different one. The additional S3-S4 statements create an apparent discrepancy among the inspected sources' reports of the known status. It is appropriate to flag that discrepancy, keep the proven lower example at D=2, and say that no stronger example was verified in this investigation. It is not appropriate to declare a definitive survey correction or a theorem that no stronger example exists. The corrected derivative says exactly this. Whether the bound 2 holds remains unresolved by the present work.

## 7. Scope of current-status and source verification

A fresh, bounded public-web check used exact-title/source queries, Kupitz-Perles with 2026, the solved qualifier, 3-everywhere-unbalanced, and the automated-symmetry paper with 2026. No verified straight-line resolution of the stated target was located. Unrelated solved Kupitz-Perles problems were not conflated with this problem. Search results do not prove the absence of unpublished, unindexed, or more recent work.

All five pinned source-document byte counts and hashes were independently recomputed locally and match the original metadata. Public source identities and selected source contents were rechecked as described above. This is not represented as five fresh binary downloads: the PDF/PPTX byte checks concern the supplied pinned copies. The inaccessible unsolvedmath starting-page result and prior repository-search record remain author-reported historical facts, not fresh successful reads.

## 8. Repair and packaging verification

SOURCE_WORDING_REPAIR.patch changes five authored files: RESULT.md, SOURCES.md, APPROACH_LOG.md, STATUS.json, and VERIFICATION_METADATA.json. It narrows source-claim certainty, adds the verified 2026 proceedings metadata, and records independent-review provenance. PROOF.md is byte-identical to the frozen original. Applying the unified patch to a fresh extraction of the original ZIP exactly reproduces all six corrected members.

The corrected derivative has six data members. The audit package additionally contains this audit, separate acceptance, verification metadata, the actual patch, and the accepted-derivative manifest. None includes copied third-party source documents, raw dataset records, source-page screenshots, private coordination, private source material, or private checker fingerprints. There is no executable mathematical certificate. Integrity hashes identify bytes; they do not establish mathematical truth. The analytic checks above establish the limited mathematical acceptance.

The remaining target is unchanged: establish D(X)<=100 for every intended configuration, or exhibit a genuine straight-line distinct-point set with every determined line having discrepancy at least 101. This package does neither.
