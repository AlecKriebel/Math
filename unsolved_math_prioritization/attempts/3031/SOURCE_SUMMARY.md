# Public source summary

Checked 2026-10-03 UTC.

For finite integers c≥m≥1, P(c,m) says every surjective c-coloring of the edges of a countably infinite complete graph has an infinite induced complete subgraph with exactly m colors. Erickson's proposed classification is m=1, m=2, or m=c. The full source conjecture remains unsolved by this packet.

The [2013 OPG source](https://www.openproblemgarden.org/op/graphs_of_exact_colorings), dataset ID 3031 / OPG-57824, duplicates [Erickson's 2010 author-posted source](https://openproblemgarden.org/op/exact_colorings_of_graphs), ID 3114 / OPG-37229. Their pinned statements are identical. ID 3031 is the existing rank-425 queue representative; ID 3114 has no queue row and is reserved solely as its source alias.

## Primary literature and credit

- M. Erickson, A Conjecture Concerning Ramsey's Theorem, Discrete Mathematics 126 (1994), 395–398: original attribution, corroborated by the author's OPG page and subsequent papers. The 1994 full article was not retrieved.
- A. Stacey and P. Weidl, [The Existence of Exactly m-Coloured Complete Subgraphs](https://doi.org/10.1006/jctb.1998.1855), JCTB 75 (1999), 1–18. The full author preprint dated June 13, 1996 was inspected. Its page 3 already supplies the general finite vertex-and-edge-colored core reduction. Theorem 2 and page 16 provide the modular and boundary coverage cited in the proof packet; Theorem 3 provides sufficiently-large-c coverage for every fixed m. The cited page-16 boundary examples are stated without proofs there.
- B. Narayanan, [Exactly m-coloured complete infinite subgraphs](https://sites.math.rutgers.edu/~narayanan/pdf/m_col.pdf): spectrum-size context, rather than a complete resolution.
- Ž. Ranđelović, [Exactly Colored Complete Subgraphs of Infinite Graphs](https://arxiv.org/abs/2512.04233v1), December 3, 2025. The live record retained only v1, with no journal reference. Its Theorem 4 claims the classification for sufficiently large m and every c>m. Together with Stacey–Weidl this leaves finitely many cases. This packet does not independently recertify the entire preprint or its cutoff. The apparent local transcription issue in its final construction is described in the independent review and is not claimed to refute the theorem.

Targeted current searches located no later complete resolution, but neither those searches nor this review certify global novelty. The packet's general finite reduction is credited; originality of refinements and construction families remains unverified.

## Dataset identity

The [repository manifest](https://github.com/AlecKriebel/Math/blob/main/unsolved_math_prioritization/manifest.json) pins ulamai/UnsolvedMath revision 37e53eabe540fb458758e198be61634bd02ee008. The source and reviewer independently checked these full-file SHA-256 hashes before extracting the records:

- problems.json, 68,931,837 bytes: 04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf
- research_results.json, 80,334,822 bytes: 8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b

Neither OPG code has a separate keyed research-results entry. Source-derived literature notes are credited background, not an earlier proof attempt by this project. Raw source files are omitted from this public distribution. The dataset's CC BY 4.0 curation credit belongs to UnsolvedMath Contributors; underlying sources retain their own terms.
