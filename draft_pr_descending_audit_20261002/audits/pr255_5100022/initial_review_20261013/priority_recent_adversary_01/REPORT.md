# Independent recent-priority audit: PR255 / 5100022 / k404

**Verdict: substantive prior covering-corollary issue. The mathematics can be valid, but framing it as a new first resolution is not cleared.** Two authenticated earlier components yield the full requested invariant, after an elementary focal nonvanishing check. No single earlier document explicitly naming and proving k404 was found in this bounded search. Those statements are compatible.

This audit did not read the sibling priority auditor's report, modify any PR, contact outside individuals or other shard chats, or change Git state. Related PRs were read only as mathematical provenance/background. The audit output is confined to this folder.

## Exact target

The target is the ratio of the signed area of the original orbit's focal antipedal to the signed area of its original-side focal pedal, for either original focus, every primitive least period N congruent to 2 modulo 4, all coprime stars, and strict noncircular confocal elliptical caustics. It requires finite real antipedal intersections and a nonzero real pedal denominator; a zero numerator is allowed. Outer tangent antipedals, focal inversions, vertex centroids, and unsigned filled-face areas are different quantities.

I read the frozen target SOURCE_SCOPE.md, RELATED_WORK.md, RESULT.md and all eight sections of PROOF.md. Its prior-pedal credit and shared parallel k403,b mechanism disclosure are relevant author inputs; they are not evidence of independent review or historical exclusivity.

## Exact covering components

[Alper Ferudun's *Focal Pedal-Antipedal Area Products in Elliptic Billiards*](https://doi.org/10.5281/zenodo.23079799), original archive v1.0, has the following precise Lemma 4 scope: “For any centrally paired elliptic-caustic trajectory, q=RA”. Its construction uses antipedal sides through the original impacts perpendicular to their original focal rays. R is explicit and depends only on the boundary ellipse and caustic. The proof groups opposite edges and telescopes; it does not use the N-divisible-by-four restriction needed later for the main product theorem. Primitive even stars are consequently included. The complete source and the actual original archived bytes were inspected, rather than relying on its title or abstract.

[The earlier public PR250 k204 proof](https://github.com/AlecKriebel/Math/blob/ea34ca1dd8e2693b58f615aa2a4b45bc548cacc3/unsolved_math_prioritization/attempts/5100013/PROOF.md), Sections 1 and5, proves p_M=(c0+c2|M|²)A for every fixed M and all primitive N congruent to 2 modulo 4, expressly including stars. I read its entire thirteen-kilobyte proof. It is a complete parity specialization, not merely the divisible-by-four final theorem of PR203. Its arbitrary-M exceptional circle is no obstacle at a focus: the focus lies inside the strict caustic, and consecutive positive-radius foot normals turn by an angle strictly between 0 and pi, making every translated shoelace determinant positive.

Thus q_F/p_F=R/[c0+c2(a²-b²)] at both foci, and the denominator is positive at every real phase. The all-star, finite-intersection and signed-area domain transfer is proved in **PRIOR_COROLLARY.md**. This is the audit's deduction from the two primary results. It supplies exact coverage of the target, not merely a similar title or an overlapping numerical observation.

The original Ferudun main.tex SHA256 is 7bdaae97eacd19214d46c175bc7d9d119d02af7a3593877ec49ef182fbeb8247; it equals the current EulerSolve main.tex byte for byte. Original archive MD5 and PDF MD5 both exactly match Zenodo's advertised file checksums. The immutable PR250 PROOF.md SHA256 is ac486431077ab33493c78dc83ce3940648a7121e72015da8563e4dc6fea7d124, provider Git blob db3f2a1dae892d978384e7448a4dbfe1d6331e7e, 13818 bytes.

## Chronology and its limits

| Event | Recorded UTC time | Evidence type |
|---|---|---|
| Ferudun original Zenodo record creation |2026-10-01 10:00:33.366348| Native public record API, actual archived file checksum matches |
| Same original Zenodo record modification |2026-10-01 10:00:56.046398| Native record API; sole version index0 |
| PR250 authored checkpoint |2026-10-01 10:44:50| Git commit event eea1b884d1bb2be8289ea60bd90b2e2f53d49f4e |
| PR250 reviewed head |2026-10-01 10:55:54| Git commit ea34ca1dd8e2693b58f615aa2a4b45bc548cacc3 |
| PR250 creation and last update |2026-10-01 10:56:06| Native server PR metadata; created_at equals updated_at |
| Target candidate working proof window |2026-10-01 11:15–11:25| Target research records; root supplied this working cutoff |
| PR255 original head commit |2026-10-01 11:46:46| Git author and committer timestamps |
| PR255 creation |2026-10-01 11:49:58| Native server PR metadata |
| PR255 original last update |2026-10-01 11:49:59| Native server PR metadata |

Both covering components' recorded public artifacts precede the target's recorded proof window and original PR. Git author dates alone do not certify public release. The server PR timestamps, unmodified PR250 metadata, current public PR page and its original two commits support the public-PR chronology; the original Zenodo version carries stronger immutable-file association. These receipts do not establish the exact first successful HTTP retrieval time, independent discovery order, causal influence, whether the corollary was previously written explicitly, or absolute worldwide priority. The target's disclosed shared-work history must remain visible; no misconduct inference follows from this audit.

## Broader current search and nearby scopes

I performed independent web queries for k404/k_{404}, AMR-050-0022, focal antipedal area, original pedal/antipedal ratios, antipedal+billiard+proof, arXiv, Zenodo and GitHub leads, including recent 2024–2026 variants. The web receipts are retained. Secondary search results were used only to find primary works; mathematical conclusions below use primary manuscripts.

The current EulerSolve catalogue contains21 AMR-050 papers. I refreshed all 21 metadata files successfully and verified each current source-archive checksum against the previously authenticated primary cache. I independently scanned every main manuscript's abstract, theorem, lemma, proposition and corollary scopes, including unnamed covering lemmas. There are no k404/5100022/AMR-050-0022 occurrences. That text-negative result does not defeat the positive mathematical covering issue in0021.

| Current primary material | Relevant scope | Exact remaining gap to k404 |
|---|---|---|
| AMR-050-0021 | General centrally paired original focal antipedal/original area lemma | Combined with prior k204, no mathematical gap after focal positivity |
| AMR-050-0019 | Center antipedal of a four-periodic original parallelogram; outer/antipedal counterexample | Center rather than focus, period 4, outer numerator |
| AMR-050-0023 | Unweighted vertex centroid of original focal antipedals for even periods | Vertex averages do not determine signed area ratios |
| AMR-050-0025 | Focal antipedal centroids of circumscribed rectangles | Outer rectangle construction and period 4 |
| AMR-050-0026 | Vertex centroid of outer focal antipedals, general even periods | Outer construction and unweighted centroid |
| AMR-050-0036 | Equality and zero signed area of two focal outer antipedals | Outer construction; no original-side pedal ratio |
| AMR-050-0012/0014/0027/0029 | Center or outer pedal products and Steiner-pedal ratios | Different polygon, pedal point or parity; no focal original antipedal input |
| AMR-050-0043/0044/0046/0048/0062/0068/0069 | Focal inversion areas/cosines and inverted-pedal geometry | Inversion is not the original antipedal construction |
| Remaining catalogue papers | Outer focal distance products, four-periodic corrections, evolute area or pentagonal criterion | No corresponding focal pedal/antipedal area theorem |

The contemporary papers on confocal Poncelet commutation, Grünbaum Poncelet families and the parable/fixed-caustic route were screened in the authenticated primary cache; no focal antipedal area theorem text was found in these screens. The 2026 Murad/Murali summary sources likewise have no antipedal or pedal theorem text; the sole billiard entry is a different general-billiard issue. These limited screens are not proofs of absence from all supplementary or unpublished work.

[Roitman, Garcia and Reznik, *New Invariants of Poncelet–Jacobi Bicentric Polygons*](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0188.pdf), Theorems 1–2 and Corollary 1, concern angle sums and limiting-pedal/focal-inversive perimeters. Its2021 polar correspondence does not state the k404 area ratio. A video list includes a special six-period null-antipedal phenomenon, not an all-period proof. [Keady and McAndrew's2024 bicentric-hexagon paper](https://atcm.mathandtech.org/EP2024/regular/22158.pdf) addresses convex hexagon distance/diagonal invariants; it does not provide arbitrary primitiveN or all-star k404 coverage. Mitrea's [2010 pedal and antipedal triangle paper](https://arxiv.org/abs/1008.0110) has the triangle restriction and does not turn a primitive odd triangle into the requested genuine even family.

## Recommended disposition and exact limits

The strongest verified recent-priority result is a **complete prior covering combination**, not an exact previously titled k404 paper. The current claim should not be promoted as the first decisive solution of a previously unresolved problem without explicitly addressing that combination. Appropriate credit must name Ferudun's original DOI and Lemma 4, the exact earlier campaign k204 proof and its PR203/204 inputs, and the target's shared-method disclosure.

Whether the root's current user-authorized workflow treats such a valid credited corollary as an already-solved disposition or as a credited alternative research note is a root/user scope decision. This agent makes no PR-status mutation or publication decision. A historical-firstness claim is blocked by positive covering evidence; an honestly credited self-contained proof has no mathematical objection from this priority audit.

No mathematical validation of every other catalogue paper is implied by scope screening. The source transfer is checkable; the wider negative search is bounded. No outside communication or journal/referee acceptance is claimed.

## Receipts

- FETCH_RECEIPTS.json and ZENODO_ORIGINAL_RECEIPTS.json: successful original/current downloads, timestamps, hashes and provider MD5 comparison; original/current manuscript bytes are retained under sources/.
- prior-k204-proof-provider.json and sources/pr250_original_k204_PROOF.md: authenticated immutable full k204 proof.
- pr250-background.json, pr250-original-commit.json, pr250-timeline.json, pr255-current.json, pr255-original-commit.json: native provider chronology.
- CURRENT_EULERSOLVE_SCOPE_SCAN_02.json and sources/current_scope_metadata/: successful refreshed 21-paper scope matrix and current archive matches.
- AUTHENTICATED_CURRENT_ARCHIVE_SCAN.json: all 21 cached ZIP SHA256 values equal the fresh provider metadata, and each inspected main.tex exactly equals its sole archive member. Thus the scope screen authenticates actual archive content as well as declared checksums.
- CURRENT_EULERSOLVE_SCOPE_SCAN.json retains an initial failed metadata sweep: default urllib requests returned403; retry with the same explicit research User-Agent as the already successful fetches passed all 21. The failure is not treated as a negative search.
- FETCH_RECEIPTS.json retains the arXiv API timeout and the actual absent EulerSolve0022 page. Browser arXiv search endpoint also failed; these failures are not counted as no-result assertions.
- web_search_*.json and web_open_*.json: independent search/open receipts. No worldwide-firstness guarantee is inferred.
