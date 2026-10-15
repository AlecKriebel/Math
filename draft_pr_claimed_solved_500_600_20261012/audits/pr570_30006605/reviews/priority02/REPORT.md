# Independent primary-source priority audit: PR570 / problem 30006605

Audit date: 2026-10-14 PDT. Reviewer shard: priority02. Assigned-audit completion: 100%. This is a priority and attribution review of the immutable original candidate, not a new proof attempt or a claim of worldwide exhaustive bibliographic coverage.

**Verdict: no explicit earlier same-scope solution was located. The generic search mechanism is prior art, and the candidate already credits it accurately. The remaining contribution is a short threshold transformation and the resulting all-dimension corollary of existing algorithms. Historical firstness remains unproved.**

The source-first checkpoint was saved at 2026-10-14T21:23:44.886819-07:00; the final pre-access checkpoint was saved at 21:24:51.912730-07:00. Candidate access began only after the latter timestamp. Neither old audits nor sibling opinions were read. Work and downloads were confined to this shard; no Git/index/canonical/remote mutation or communication with any outside individual occurred. Third-party PDFs, extracted text and rendered images are confined to ignored `.cache/` and are excluded from the authored-file seal.

## Exact claim and standard for collision

The target is an exact vertex minimizer of

\[
 r_w(x)=\max_{u\in V}w(u)d_G(x,u)
\]

for a finite, nonempty, connected, simple, unit-edge median graph given by adjacency lists and an arbitrary nonnegative finite real profile. The requested runtime is almost linear in the graph order for every bounded cube dimension. An all-dimension bound is stronger. The comparison model matters: no constant-time operation on a numerically unbounded floor is required. Zero profiles, singleton support, singleton graphs, ties and zero-weight vertices are part of the scope.

A priority collision needs an earlier explicitly recorded result of this scope, or an explicitly recorded mechanism the candidate presents as its invention. A theorem from which the answer can now be derived is important prior art, but its existence alone does not establish that the same consequence was previously recorded. Approximation, additive arrival weights, continuous edge centers and narrower graph parameters must not be substituted for the target.

The candidate at [PROOF.md](/Users/alec/Documents/Math/draft_pr_claimed_solved_500_600_20261012/audits/pr570_30006605/original/unsolved_math_prioritization/attempts/30006605/bundle/PROOF.md:3) explicitly makes no historical-priority claim. Its theorem on line 13 is deterministic O(n log^5(2n)) for a center, optimum value and the full center set on every finite median graph.

## Primary chronology and genealogy

The following are primary-source records, with full details and hashes in `SOURCE_RECORDS.json`.

| Date | Source and inspected locator | What it establishes for this audit |
|---|---|---|
| December 1979 | Kariv and Hakimi, SIAM J. Appl. Math. 37:513-538, [DOI 10.1137/0137040](https://doi.org/10.1137/0137040); publisher abstract | Exact weighted tree centers in O(n log n). The original PDF was inaccessible, so the cut-on-best-neighbor genealogy is additionally checked in GP25, pp.2 and 12. |
| November 1983 | Megiddo, SIAM J. Comput. 12:759-776, [DOI 10.1137/0212052](https://doi.org/10.1137/0212052); publisher metadata | Weighted tree centers in linear time are credited by OWR and D26A Lemma3.5, p.7. Original Section3 could not be independently read here. |
| 2019-10-23; revised 2019-11-11 | Dragan and Ducoffe, [arXiv:1910.10412v2](https://arxiv.org/abs/1910.10412v2), pp.6-7, Theorem2 and proof | Common-radius ball intersection on Helly graphs in O(km), with an explicit partition/ball-growing procedure. This has both a class restriction and a radius factor. |
| 2020-10-29 | Ducoffe, [arXiv:2010.15803v1](https://arxiv.org/abs/2010.15803v1), p.6, Theorem1 | Earlier tree-product range-query framework; its displayed goal is eccentricity, not the whole target. |
| 2021-02-16 | Dragan, Ducoffe and Guarnera, [arXiv:2102.08349v1](https://arxiv.org/abs/2102.08349v1), pp.9-11, Theorem4/Lemma6/Section4.1 | Localization and ball-growing in Helly graphs, subsequently reused by D26A. |
| 2021-08-18 | Ducoffe, [MFCS 2021, 43:1-43:16](https://doi.org/10.4230/LIPIcs.MFCS.2021.43), Theorem1 pp.43:4-5 and Theorem5 pp.43:7-8 | Almost-linear eccentricity computations when an embedding into constantly many tree factors is supplied. |
| 2024-10-14; SODA online 2025-01-07 | Berge, Ducoffe and Habib, [arXiv:2410.10235v1](https://arxiv.org/abs/2410.10235v1), pp.2-4,22-24; [SODA DOI](https://doi.org/10.1137/1.9781611978322.52), pp.1679-1704 | All additive weighted eccentricities on arbitrary median graphs in O(n log^4 n). The preprint p.4 distinguishes multiplicative Weighted Center and presents it as a future direction. |
| 2025-03-19 | Chalopin, Chepoi, Dragan, Ducoffe and Vaxes, [arXiv:2503.15011v1](https://arxiv.org/abs/2503.15011v1), complete 44 pages; Theorem7.8 p.28 | Exact multiplicative center for cube-free median graphs in deterministic O(n log^2 n); this is already the full dimension-two result. |
| Workshop 2026-02-15 to 2026-02-20; published 2026-07-21 | Ducoffe, [OWR 8/2026](https://doi.org/10.4171/OWR/2026/8), complete contribution pp.504-507 | Definition p.504 and Open problem1 p.505 give the exact broader target. It records tree-dimension and cube-free special cases separately. |
| 2026-07-05 | Ducoffe, [arXiv:2607.04287v1](https://arxiv.org/abs/2607.04287v1), complete 25 pages, especially Lemma2.2 pp.5-6 | The generic multiplicative decision-to-optimization reduction, with weighted row midpoints, is explicitly prior art. |
| 2026-08-25 | Ducoffe, [ESA 2026, 133:1-133:19](https://doi.org/10.4230/LIPIcs.ESA.2026.133), complete 19 pages, especially Lemma2 p.133:6 | The published version repeats the generic reduction; its other exact classes do not state the whole median/cube-dimension result. |

All four relevant arXiv abstract pages for BDH25, GP25, D26A and TREE20 displayed only v1 at the audit date. H19 displayed v2 and H21 only v1. The publisher dates above are distinguished from workshop dates and arXiv submissions.

There is a precise attribution wrinkle in the tree-product ancestry. OWR p.505 credits its reference [11] (MFCS2021) with a multiplicative weighted-center result under a supplied bounded-tree-dimension embedding. The inspected conference Theorems1/5, however, explicitly formulate unweighted eccentricities. The available 2020 preprint does too. The safe record is therefore: OWR reports/credits that weighted consequence, while the checked foundational theorem has the narrower displayed interface. Neither formulation covers all bounded cube dimension: OWR expressly notes that tree dimension is unbounded already in cube dimension two. This discrepancy is not a collision with the present candidate and should not be repaired by inventing an explicit theorem absent from the source.

## What the later ESA paper does and does not preempt

D26A Lemma2.2 and D26E Lemma2 have the exact generic guarantee

\[
 T\text{-time weighted-center decision}\quad\Longrightarrow\quad
 O((T+n)\log n)\text{-time optimization}.
\]

They maintain implicit arithmetic-progression rows of possible values k w(v), choose weighted medians of row midpoints and decrease the unresolved search measure geometrically. They do not depend on hyperbolicity. The candidate's Section4 is therefore a variant/reproof of an existing reduction, not an independently new search mechanism. This matters even though the paper's title emphasizes hyperbolic graphs.

The candidate already says precisely this on lines29 and94 and again on line108. It distinguishes its O(n log n) per-round comparison-only construction from Ducoffe's faster overhead. There is no missing attribution to flag in the provided snapshot. A small locator improvement would be to cite ESA Lemma2 as p.133:6: its statement and entire proof are on that page, while the candidate gives pp.133:6-133:7. This is bibliographic precision, not a substantive defect.

The ESA exact results use bounded hyperbolicity together with additional graph conditions, or specialize to chordal, chordal bipartite, distance-hereditary or dually chordal graphs. They do not explicitly assert the multiplicative all-median or bounded-cube-dimension theorem. The approximate-center result by itself does not do so either. No later hidden median theorem was found in the complete ESA article, its appendix, the complete arXiv version, their conclusions or references.

## Adversarial containment checks

These are checkable reasons narrower prior algorithms do not become a whole-target collision by relabeling their parameters.

1. **Cube dimension does not bound hyperbolicity.** Let G be the (L+1)-by-(L+1) square grid. It is median with cube dimension2. For its four corners, the three four-point distance sums are 4L,2L,2L; hence its hyperbolicity is at least L. Thus a runtime polynomial or exponential in hyperbolicity does not yield an almost-linear bound merely from fixed cube dimension.
2. **Median does not imply Helly.** In C4, the four unit balls pairwise intersect, but their total intersection is empty. C4 is median. Consequently a theorem assuming Helly balls cannot be applied to all median graphs.
3. **Higher-dimensional median does not imply bipartite Helly.** In Q3, the vertices000 and111 have distance3, and the three neighbors of000 in their interval have no common neighbor in the interval other than000. This violates the interval-outergate characterization of bipartite Helly graphs in GP25 Theorem6.1, p.17. Cube-free median graphs are a relevant subclass; arbitrary median graphs are not.
4. **Bounded degree is separate.** Arbitrarily large stars have cube dimension1 and unbounded maximum degree. A maximum-degree parameter cannot be inferred from fixed cube dimension.
5. **Common-radius intersection is insufficient without its assumptions and cost.** The older Helly O(km) tool uses a common radius k; setting k up to n-1 can be quadratic even before the class restriction is considered. GP25 Lemma6.5 is similarly for a common radius on bipartite Helly graphs. D26A generalizes such tools inside a localized ball, but retains its graph and hyperbolicity hypotheses.

These checks refute the tempting overextensions of prior theorems. They do not prove historical novelty; that requires the separate search evidence.

## Claim-by-claim attribution and novelty assessment

| Candidate claim | Exact comparison | Assessment |
|---|---|---|
| Lines7-13, target and stronger theorem | OWR pp.504-505 fixes multiplicative vertex weights. BDH25 uses additive arrivals. GP25 gives dimension2 only. | Target match is exact; all dimensions is a substantive scope increase over the recorded narrower multiplicative algorithms. |
| Lines21-27, additive oracle | BDH25 definition p.2, Theorem1 p.3, Algorithm1 and analysis pp.22-24. | Imported prior theorem, explicitly and appropriately credited. Its input domain includes the small nonnegative integer offsets needed here. |
| Lines33-49, pointwise threshold identity | D26A already uses floor-based radii for weighted feasibility, e.g. pp.8,13. The extra complement D-b_R converts all inequalities to one additive-eccentricity cutoff. | Elementary reduction valid for any finite unit-edge graph. No explicit earlier occurrence of this precise capped complement plus BDH consequence was found. Do not describe the underlying ball-feasibility observation as a major new principle or claim first invention of it. |
| Lines51-57, exact threshold oracle and all feasible vertices | One application of the credited all-additive-eccentricity theorem to a_R=D-b_R. | This is the useful bridge in the candidate. It avoids adding vertices or changing the promised graph. No exact prior all-median multiplicative threshold oracle was located. |
| Lines61-65, implicit finite candidate set | D26A pp.3-6 and D26E pp.133:4,133:6 already discuss k w(v) possibilities. | Known search space; adequately credited by the surrounding section. |
| Lines69-94, weighted midpoint search and constant-factor pruning | D26A Lemma2.2 / D26E Lemma2. Candidate uses inclusive row lengths, strict incumbent pruning, explicit tie handling and binary-searched rank updates. | A self-contained comparison-only variant of known machinery. No stronger asymptotic result and no missing credit. The no-unbounded-floor implementation is useful specification detail, not a new optimization paradigm. |
| Line98, O(n log^5(2n)) all-dimension result | O(log n) threshold calls, each O(n log^4 n). | A short composition/corollary of old algorithms and the candidate's bridge. Derivability does not establish an earlier recorded solution; the searched primary sources did not state this consequence. |
| Full center set, lines78,84,98 | At the optimum, the exact threshold feasible set equals the center set. | Correct automatic output consequence of the same oracle; not a separate substantial novelty claim. |
| Lines102-107, arithmetic and computational limits | The transformation only feeds integer offsets0,...,n-1 to BDH. Input-real comparisons are between bounded integer multiples. | Scope is candid and appropriate. It does not claim a bit bound independent of input length or an implementation of BDH. |
| Line108, historical and novelty caveat | OWR workshop was February2026; report published July21. D26A appeared July5. | Date wording is defensible as a workshop-state claim; strongest publication evidence is that the July report still contains the open problem. The caveat is necessary and should stay. |

## Independent check of the bridge and its exact boundary cases

Write D=n-1. For R>=0 and every u, define b_R(u) as the largest k in [0,D] satisfying k w(u)<=R. Then b_R(u) is an integer and a_R(u)=D-b_R(u) is a nonnegative integer. Since graph distances are integers in [0,D],

\[
 w(u)d(x,u)\le R
 \iff d(x,u)\le b_R(u)
 \iff d(x,u)+a_R(u)\le D.
\]

Taking the conjunction over u is exactly the additive maximum test. If w(u)=0, b_R(u)=D and that constraint is vacuous; if R=0 and w(u)>0, b_R(u)=0 and it correctly forces x=u. This also handles singleton support. If n=1, D=0 and the sole vertex is a center. If R<0, feasibility is false. No ball convexity, Helly property, local-unimodality theorem or tree embedding enters this deduction. This argument checks that the candidate has not silently traded the original problem for the additive one: it only trades one threshold instance for an additive eccentricity computation.

The full theorem consequently depends on BDH's imported algorithm and the standard implicit optimization machinery. This priority review does not experimentally certify BDH's asymptotic implementation and does not reconstruct that entire algorithm. The candidate accurately labels its controls as controls of the reduction/search rather than of the fast imported oracle.

## Search coverage, limitations and recommended disposition

`QUERY_LOG.md` preserves the queries and access limits. The search included the exact mandatory titles, multiplicative versus additive wording, bounded tree dimension, ball-intersection algorithms, the older Helly toolbox, the tree-center ancestors and current 2026 formulations. Only primary publications/preprints and publisher metadata support mathematical conclusions. Search snippets from unrelated sites and upstream status data were not treated as evidence.

The original Megiddo and Kariv-Hakimi PDFs were inaccessible through the browsing tool. There was no retry, alternate-channel denial bypass, purchase, login or external contact. Their limited tree scope is well documented by the accessible primary descendants and publisher abstracts/metadata; their entire original algorithms were not independently audited here. The SODA publisher showed a Get Access page; its complete public author preprint had already been read independently. This bounds the completeness of the historical genealogy, especially for ancient general reduction observations, without creating a same-scope collision.

**Recommended disposition:** retain the candidate as a mathematically meaningful, modest corollary/connection pending the separate correctness review. Preserve its explicit BDH and Ducoffe attribution and its historical-priority caveat. Do not advertise the weighted-median search, additive algorithm, floor-to-ball feasibility or dimension-two result as newly discovered. No blocking priority correction to the core all-dimension theorem is justified by the sources found in this audit.

**Precise remaining limit:** a negative literature search cannot certify worldwide firstness. A previously unindexed or otherwise unexamined explicit same-scope result, or an earlier recorded exact complement-to-additive application, could change the priority assessment. None was located here. No outreach has been prepared or initiated.
