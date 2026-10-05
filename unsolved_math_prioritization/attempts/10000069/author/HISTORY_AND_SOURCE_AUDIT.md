# History and source audit

Date: 2026-10-05. This is a bounded search, not an exhaustive absence proof.

## Actual earlier-attempt checks

- GitHub PR search in AlecKriebel/Math, all states, exact `10000069`: no returned PRs.
- Exact `AMR-099-0069`: no returned PRs.
- Commit-message search `10000069` scoped to AlecKriebel/Math: no returned commits.
- `series-parallel`: unrelated fractional-coloring PR https://github.com/AlecKriebel/Math/pull/319; no target attempt identified.
- `Benjamini`: other problem IDs 10000083, 10000046 and 10000043; none is the target.
- Branch searches `10000069`, `series-parallel`, `Benjamini`, `random-sp`: no returned branches; each returned a null continuation cursor.
- Branch search `distance` returned only research/abert-boundary-distance-1200023 and research/30002508-nyman-beurling-distances. Its continuation cursor was followed to an empty terminal page; neither branch concerns this target.
- Default-branch Git tree: main root 0a49d5e66a0fb9d4f78c7f3a7f3b30cd77196567. The recursive root request was truncated and is not used as exhaustive evidence. A subsequent exact nonrecursive descent inspected unsolved_math_prioritization tree f75f7457eee8bfcea72e20d4d3c09e35f00e329d and its attempts tree 5c2ab378a9489c4b49c1ccbf87ce85ff5b7d5393. The latter returned 61 direct entries, truncated=false, with no 10000069 directory.
- A local filename and text search found the catalogue/queue descriptors and no preexisting mathematical attempt folder for this target. Descriptors and zero-turn queue entries are not treated as proof of non-attempt.
- Available prior-conversation search by exact ID, title and Question 9.6 found only unrelated campaign attempts, no exact target attempt. Its raw report is not included.

No actual prior user attempt was identified in the checked surfaces. Deleted/unindexed branches, incomplete history, and unavailable corpus records remain limitations.

## External authorship

The candidate repository is DannyExperiments/random-series-parallel-distance-exponent, repository ID 1328316580, public owner DannyExperiments. Its CITATION.cff credits DannyExperiments and gives the title and release date used here. It is a different repository from AlecKriebel/Math. Repository permissions do not establish personal identity or prove the user had no involvement; no such inference is made.

## Retrieval and inspection

The exact catalogue page returned 403. Both erd100.pdf and erdos.pdf at the author's website returned 404. The search engine's indexed primary erd100.pdf displayed Question 9.6 and its surrounding exact series/min recursion on p.18; this was read, not visually inspected. Springer provided an access-limited HTML chapter landing page when its PDF URL was requested. This HTML is not a PDF and is not assigned a PDF hash. No paywall bypass was attempted. No current full catalogue statement or raw AI corpus was inspected.

The publisher PDF of Chen-Derrida-Duquesne-Shi was downloaded, text-inspected at the model, Theorems 1 and 2, and references, and journal p.82 was rendered and visually checked. Theorem 1 is a square-root-epsilon asymptotic, not a linear-epsilon asymptotic. The rendered radical and publisher HTML agree. The model matches the hierarchical terminal-distance model exactly. Theorem 2 does not provide a general interior almost-sure limit. The full 42-page proof was not independently re-derived.

The candidate's canonical proof was fetched from main, then fetched at the inspected immutable commit. Those two copies were byte-identical. Its pinned manuscript TeX and PDF were also retrieved; all four PDF pages were rendered and visually read. The eigenvalue argument and invariant-measure formula were reconstructed from their mathematical statements and checked step by step. The extra right-end asymptotic appears in the canonical proof, not the four-page manuscript. No reliance is placed on the candidate's self-reported audit badges, release verification or priority claims.

Searches through 2026-10-05 found the published near-critical theorem and the exact external spectral manuscript as the directly relevant results. This search neither establishes exhaustive current openness nor historical novelty. The candidate's public DOI is reported as author-supplied metadata; this packet does not certify the deposit or independently validate its release timestamp.

## Claim acceptance map

- Exact model, generation normalization, terminal observable: supported by publisher primary model.
- Near-critical constant and endpoint consequence: published theorem plus explicit elementary implication.
- Interior maximal-eigenvalue, variational and invariant-measure statements: locally reconstructed credited manuscript result; pending fresh independent audit.
- Elementary scalar formula, all-p almost-sure rate, uniqueness, global convergence, global convexity: not established here.
- Literal 'shape is solved' judgement: qualified interpretation only.
- New result, historical priority, human peer review, formal proof: not claimed.
