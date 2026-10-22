# Source and duplicate gate

Checked 4 October 2026 UTC. Rank 568, ID 2303003, code AMR-022-3003.

## Exact target and catalogue error

The requested [catalogue URL](https://www.unsolvedmath.com/problems/2303003) was tried first. The web reader could not open it; a direct request returned HTTP 403. The matching numerical record in the public [UnsolvedMath dataset](https://huggingface.co/datasets/ulamai/UnsolvedMath), pinned at revision `372682f27c1b0d3d39e75fa63ad7932c7a2e1bde`, supplied the source identification and exact target.

The target is: does a negative subharmonic function on the right half-plane with semicircle infimum at most −K at every radius necessarily obey u(r)≤−K/2 on the positive axis? The full original Problem 3.3 and its update were read in Hayman–Lingham, [*Research Problems in Function Theory (New Edition)*, arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2), printed p.60 / PDF p.61. That page was rendered and visually checked. Update 3.3 explicitly reports the answer to this original question as negative and asks a separate question about the optimal replacement constant.

The catalogue's generated summary and the complete prior report keyed `AMR-022-3003` both incorrectly describe the −K/2 question as unknown in that edition. The prior report says only that the statement was read and a web search found nothing; it contains no mathematical attempt. Its description conflicts directly with the update immediately following the original statement. This is a source-triage correction, not a new mathematical resolution. The original target does not bundle the later optimal-constant question.

The research-results corpus was freshly downloaded and its exact matching keyed report selected. Its checksum matches the pinned snapshot. Only the selected record and provenance were retained here, and neither appears among public artifacts.

## Original primary construction

**W. K. Hayman**, *On a theorem of Tord Hall*, Duke Mathematical Journal **41**(1) (March 1974), 25–26, [DOI](https://doi.org/10.1215/S0012-7094-74-04103-9).

The publisher's [article record](https://projecteuclid.org/journals/duke-mathematical-journal/volume-41/issue-1/On-a-theorem-of-Tord-Hall/10.1215/S0012-7094-74-04103-9.short) was opened in the cloud research browser. It confirms the author, title, date, pages and DOI. Its freely supplied [first-page preview](https://projecteuclid.org/JournalArticle/PreviewFirstPage?urlid=10.1215%2fS0012-7094-74-04103-9) was visually read in full and downloaded through the preview's download control. The rendering, rather than the badly corrupted OCR text, was used to read the mathematics. It explicitly gives c=90, a=1/100, eta=c epsilon, zeta=i exp(−i eta), the counterexample formula, its boundary values and the claimed strict all-positive-axis violation.

The full article requires a subscription or payment; no purchase or sign-in was attempted. Page 26 was **not read**. We do not claim a full-source-proof audit. Instead PROOF.md reconstructs every required estimate from the p.25 formula, with epsilon=10^-6 fixed explicitly. It gives an elementary self-contained proof, including all radii, gap endpoints, the Green pole, and every positive-axis point. A maximum with the constant −1 also supplies a bounded, continuous, finite-valued version, so the counterexample does not depend on accepting −infinity as a value.

The 2018 update points to reference [412], Chapter 7, but [412] in that bibliography is *Subharmonic Functions*, Vol. I (1976). That volume has five chapters; the corresponding Chapter 7 belongs to Vol. II (1989). We have not treated that mismatched bibliography entry as proof access. The direct 1974 primary article identifies the construction independently. The book's Chapter 7 proof was not inspected.

Searches also identified Marshall–Sundberg's disk radial-projection work. Its different geometric hypotheses do not automatically settle either this half-plane question or the optimal-constant follow-up, and no result from it is used. The direct negative counterexample here makes a current-openness claim unnecessary.

## Repository duplicate checks

The live [QUEUE.md](https://github.com/AlecKriebel/Math/blob/main/unsolved_math_prioritization/QUEUE.md), Git blob `59dba610d333684751e889818d21f66aba29cec9`, contains the exact rank-568 target with `queued` and `0/5`.

Bounded checks were made against the actual repository:

- All-state PR searches for `2303003`, `AMR-022-3003`, `Tord`, `"3.3" "Function"`, and `"Hall" "Hayman"` returned no matches.
- A broader `half-plane` PR search returned #479, #497 and #517. Their returned descriptions concern different numerical IDs and different spectral or polynomial questions.
- Default-branch code search for the exact numeric ID returned no match; this is not assumed exhaustive, because it did not find the known queue row either.
- ID-based branch and commit searches returned no matches; the branch search had no continuation cursor.
- The repository root was actually listed. Its recursive `problems/` tree `8f72e77ed517ba2424b4e74b324cda525e6373c3` had 652 entries with `truncated=false` and no numeric-ID, Hall, Hayman or harmonic path match.
- The actual `unsolved_math_prioritization/attempts` directory contained 54 entries and no target-ID entry.
- `review_v2/related_target_groups.json`, blob `b5cfa231ed6079c0f5021e1368c3b30a43100a10`, contained no occurrence of this numeric ID.
- Repository AGENTS.md, prioritization AGENTS.md and the complete prioritization README were read.

These checks found no earlier repository attempt for the exact question, but do not rule out untagged or unindexed work. They are not a historical novelty search, and no novelty is claimed.

## Disposition and publication boundary

Recommended disposition: `already_solved`, `1/5`. One substantive reconstruction is complete; five new approaches are not warranted after locating and proving a prior exact resolution. The separate sharp-constant question remains outside the deliverable.

No remote files, branches, commits, PRs, comments or queue fields were changed during authoring. Publication is gated on a fresh independent audit and the coordinating review. Default queue scope is only this row's Status and Turns cells, with no generator invocation or unrelated cell changes. The public packet excludes all source PDFs, rendered source pages, extracted source text, catalogue data, report corpora and private operational material.
