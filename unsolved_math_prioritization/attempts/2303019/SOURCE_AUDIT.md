# Source and prior-work audit

Checked 2026-10-04 UTC. Target: numeric ID 2303019, AMR-022-3019, queue rank 571.

## Exact-source chain

1. The requested starting URL was [UnsolvedMath /problems/2303019](https://www.unsolvedmath.com/problems/2303019). The live page could not be retrieved through the web tool; the corresponding code URL also failed. No claim is based on inaccessible page contents.
2. The immutable [UnsolvedMath dataset revision 372682f27c1b0d3d39e75fa63ad7932c7a2e1bde](https://huggingface.co/datasets/ulamai/UnsolvedMath/tree/372682f27c1b0d3d39e75fa63ad7932c7a2e1bde) supplies the complete exact numeric record. It identifies Hayman–Lingham 2018, Problem 3.19. The whole `problems.json` byte hash is `37067f43734b76ee886b032469836767c34d892de14397ce6aa71da01500e252`, 69,291,427 bytes. Only the target's statement was used for scope; imported classifications were treated as unverified.
3. [Hayman–Lingham arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2), printed p.66 (PDF page 67), contains the problem and the affirmative Update 3.19. Its reference [12] identifies Aikawa's 1990 paper. The PDF page was visually checked, not merely searched. PDF SHA-256: `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`.
4. H. Aikawa, *Harmonic functions having no tangential limits*, Proc. Amer. Math. Soc. 108(2) (February 1990), 457–464, [DOI 10.1090/S0002-9939-1990-0990410-X](https://doi.org/10.1090/S0002-9939-1990-0990410-X). The journal-article text was read through a [mirror of the primary article](https://scispace.com/pdf/harmonic-functions-having-no-tangential-limits-3exruh87fv.pdf). The AMS endpoint returned HTTP 403; the mirror was available as extracted web text but did not yield local PDF bytes. Thus no local byte hash or successful visual inspection of the 1990 PDF is claimed. The exact theorem is on p.458; geometric lemmas on pp.460–461 and the alternating-data proof on pp.461–463 were inspected. The proof's real-valued boundary data, the all-angle grid coverage, and the final separated liminf/limsup are material to this verification. OCR-confusable constants were not blindly trusted: PROOF.md supplies its own explicit bounds.
5. H. Aikawa, *Harmonic functions and Green potentials having no tangential limits*, J. London Math. Soc. (2) 43 (1991), 125–136, [DOI 10.1112/jlms/s2-43.1.125](https://doi.org/10.1112/jlms/s2-43.1.125). The [author-hosted manuscript](https://www.isc.chubu.ac.jp/aikawa/research/AikawaPapers/har.pdf), Section 1, Theorem A on manuscript p.1, restates the disk theorem and identifies it as solving Barth's question. Its first page was visually checked. This is a 16-page author manuscript, not a facsimile of the 12 journal pages. Its bibliography still calls the earlier article forthcoming. PDF SHA-256: `11b25713f26a35bf49a0dc9ef18ed6831970fdc203b3efd8af9c3267812b11ea`.
6. Aikawa's [official publication list](https://www.isc.chubu.ac.jp/aikawa/research/list.html), entries 48 and 50, verifies both publication records. The older DOI `10.2307/2048295` on that list identifies the same 1990 article.

## Full-proof correspondence

Aikawa's 1990 proof uses tangential subcurves with large angular projection relative to radial depth, radial grids meeting every rotated curve, small unions of boundary intervals, and alternating overwrites. Our Section 2 proves the subcurve selection without radial monotonicity or rectifiability; Section 3 proves all-rotation coverage; Sections 4–5 prove the sign and perturbation estimates; Section 6 proves oscillation and positive normalization. The compact-circle estimate K(R)|E| replaces Aikawa's more technical density bound. Every replacement is proved; no hidden research-level dependency remains.

The article's separate positive-unbounded construction is unnecessary here. Relying only on an infinite limsup would invite ambiguity about an extended-real limit. The bounded oscillating construction directly excludes both finite and infinite limits.

## Prior report and repository duplication checks

- The pinned `research_results.json` has 80,334,822 bytes and SHA-256 `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`. Its `AMR-022-3019` entry contains no proof and says it found no resolution. That report's open-status assertion fails the direct 2018 update check.
- Observed main commit: `5960059f8c7908a06602db6b3a4485c8171908da`.
- [QUEUE.md](https://github.com/AlecKriebel/Math/blob/main/unsolved_math_prioritization/QUEUE.md), observed blob `59dba610d333684751e889818d21f66aba29cec9`, lists the target as `queued`, `0/5`. The inspected `state.json` has no entry for this numeric ID.
- The live `attempts` directory listing contains no `2303019` directory. Repository PR searches for `2303019`, `AMR-022-3019`, `"3.19"`, and `Aikawa` returned no matches. A wider `tangential` search returned unrelated PRs. Code search for the ID returned no results. Search absence is not proof against all unindexed or unpublished activity, but no prior repository attempt was located.
- `review_v2/related_target_groups.json` contains no group with this ID.
- A catalogue comparison found only one exact code/statement target. Another Barth/tangential keyword hit, 2305076 / Problem 5.76, asks a differently formulated question about an analytic function and a nontangential arc. It is not silently identified with this target and is not changed by this verification.

## Subsequent literature and scope boundary

[Di Biase, Gratien, Svensson, arXiv:2511.12679v2](https://arxiv.org/abs/2511.12679v2), revised 2026-06-26, describes later work on sequential tangential approach regions and distinguishes earlier curvilinear results, including Aikawa's. Only its abstract and bibliographic context are used here, not its proof. This supports keeping the present claim scoped to a continuous tangential path. Targeted searches located no correction that would retract the exact disk theorem; the independent reconstruction does not depend on treating a negative search as proof.

## Attribution and publication boundary

This package contains original verification prose and code, public source links, and checksums. It does not redistribute source PDFs, page images, source text corpora, or the imported research report. It credits the published solution and makes no new-solution claim.
