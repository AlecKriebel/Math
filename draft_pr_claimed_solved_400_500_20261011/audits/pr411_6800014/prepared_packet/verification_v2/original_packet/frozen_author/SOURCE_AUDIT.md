# Source, status, and scope audit

Checked 2026-10-03 UTC.

## Exact target and queue

- Problem URL: https://www.unsolvedmath.com/problems/6800014
- Identifier: `AMR-067-0014`; title: *Ricci pinching on solvable Lie groups*.
- Live queue: https://github.com/AlecKriebel/Math/blob/main/unsolved_math_prioritization/QUEUE.md
- The GitHub connector returned the rank-444 row as `queued`, `0/5`, with file blob SHA `7693db825a97119fec7d2c26402e2fa1c1191586`.
- The exact problem-page request was attempted through web retrieval, ordinary HTTPS, and the cloud browser. The page returned `403 Forbidden`; its live mathematical content was **not** verified. The original source and the pinned corpus provide the wording below. This access gap does not affect the mathematical proof, but must not be reported as successful live-page verification.

The target is the universal claim that every local maximum of the Ricci pinching ratio among left-invariant metrics on a fixed solvable Lie group must satisfy the algebraic solvsoliton equation `Ric=cI+D`.

## Original source

Morgan–Pansu, *A List of Open Problems in Differential Geometry*, source item Question 14, section 11, proposed by Jorge Lauret:

- TeX: https://www.imo.universite-paris-saclay.fr/~pansu/problems_MTDG.tex
- PDF: https://www.imo.universite-paris-saclay.fr/~pierre.pansu/problems_MTDG.pdf

The TeX was fetched successfully; lines 456–469 give the section, problem, definition, and Lauret–Will reference. The PDF was independently readable via web retrieval. The source has the same local-maxima requirement; replacing it by a global-maxima statement would weaken the target materially.

## Primary literature and conflicting announcement

1. J. Lauret and C. E. Will, *The Ricci pinching functional on solvmanifolds*, Quarterly Journal of Mathematics 70 (2019), 1281–1304; arXiv:1808.01380v2, 9 May 2019. https://arxiv.org/abs/1808.01380v2
   - Equations (3)–(4) supply the almost-abelian Ricci operator and functional.
   - Theorem 1.5 and Proposition 6.11 reduce almost-abelian local maxima to Ricci solitons, including exceptional `N+C` points.
   - Example 6.3 gives that exceptional family.
   - Lemma 6.12 excludes local maximality for sufficiently large nilpotent coefficient. The following sentence leaves sufficiently small coefficients unresolved.
   - Global-maximum theorems do not resolve this local question.

2. J. Lauret and C. E. Will, *The Ricci pinching functional on solvmanifolds II*, Proceedings of the AMS 148 (2020), 2601–2607; arXiv:1907.08014v2, 27 November 2019. https://arxiv.org/abs/1907.08014v2
   - Theorem 1.1 extends the global-maxima result to codimension-one nilradical when a solvsoliton exists.
   - Theorem 1.2 treats abelian nilradical within metrics preserving a specified orthogonal splitting.
   - Neither theorem says that every local maximum is a solvsoliton.

3. J. Lauret, *Homogeneous Ricci curvature and the beta operator*, São Paulo talk, 23 July 2018. https://www.ime.usp.br/~mtg/slides/j_lauret.pdf
   - Slide 13/17, PDF pages 71–73 (zero-based 70–72), asserts existence of Ricci-soliton local maxima which are nonglobal and not solvsolitons.
   - The accessible slides do not provide a construction or proof there.
   - This predates the paper's final version, which explicitly leaves existence open. The discrepancy is disclosed; the earlier slide alone is not treated as a settled resolution certificate. The packet makes no novelty claim.

4. Author's 2022–2026 publication list: https://sites.google.com/view/jorge-lauret/p%C3%A1gina-principal/2022-2026
   - Checked alongside exact-topic searches. No later primary proof resolving this exact local-maxima problem was located. This is a bounded search finding, not a claim that none exists anywhere.

## Pinned corpus and prior-attempt gate

Pinned corpus revision: `37e53eabe540fb458758e198be61634bd02ee008`.

- `problems.json` SHA-256: `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`
- `research_results.json` SHA-256: `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`

Both local file hashes were recomputed and matched. The imported research record is a literature-status summary about the global/local distinction. It contains no original mathematical attack. A focused prior-work check did not find a genuine previous attempt on this exact problem. Exact-ID repository file, branch, commit, and issue/PR searches returned no matching attempt. These checks are bounded by their search coverage.

The prior-attempt gate therefore passed; imported literature summarization was not mislabeled as prior user research. No private search transcripts are included.

## Honest attempt accounting

- Retrieval, source reconciliation, and prior-attempt checking: zero substantive turns.
- Attempt 1: explicit `J⊕uE₁₂` family and exact conjugacy Hessian.
- Attempt 2: local normal form, uniform Taylor proof, direct derivation obstruction, and explicit larger-value conjugate.
- Stopped at two substantive attempts because Attempt 2 gives a complete counterexample argument pending fresh audit. No padding to five attempts and no presentation of review/packaging as additional mathematics.

## Publication boundary

Only the authored text and small verification scripts in this packet are intended for a possible repository update. Source PDFs, original-source TeX, screenshots, scraped pages, complete corpora, private history, and exploratory files are excluded. Queue tooling and unrelated work are untouched. Final publication requires the separate audit and parent gate.
