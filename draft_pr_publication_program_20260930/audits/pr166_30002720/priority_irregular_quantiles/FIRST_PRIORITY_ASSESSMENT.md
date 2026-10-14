# Sealed independent first priority assessment

Sealed UTC: 2026-10-12T10:49:08.317007+00:00. Best-guess completion of this priority-family audit: 35%.

This is my first substantial independent priority assessment. I have read only the three permitted original-submission files, independently retrieved primary manuscripts, my own search outputs, and the PDF skill. I have not read submission SOURCE_AUDIT, review, gate, status, verification, research notes, ROOT notes, or sibling verdicts. Directory listing disclosed filenames but no forbidden file contents were opened.

## Exact target

Stationary binary Markov source with diagonal persistence 3/4 and off-diagonal 1/4; independent strings; singleton-stopped Radix Selection bucket-operation cost at rank floor(nt)+1; fixed word with ones only at j^2 for j>=2; t=F(v) is a nonboundary continuity rank. Target is failure of tightness on the sqrt(n) scale for every deterministic real center.

## Primary evidence already inspected

LNS 2014 full section 3.1 and proof outline of Theorem 3.1 establish only E[Y_n]/n -> m_mu(t) away from cylinder boundaries. The quantile fluctuation analysis was deferred, except for memoryless sources. Leckey thesis full section 5.2.3 (Theorem 5.2.13 and proof, Remark 5.2.14) gives non-tight supremum processes using jumps and even alpha_n=o(n), while section 6.1 expressly asks about marginal distributions and continuity versus discontinuity points.

LNS process manuscript (author PDF independently downloaded, SHA 105c172a856ca0d54b214be903f107d9bb1769db8f20bb1534a5b63f62d45e18) full Proposition 2.3 and proof, Section 2.4 including complete Proposition 2.8 proof, Proposition 2.9 proof, Proposition 2.10 proof, and surrounding results have been inspected. Printed pages 21-23 have been rendered and visually inspected. Proposition 2.8 yields tight Gaussian fluctuations after the data-dependent center n m(S_(floor(nt)+1)). Proposition 2.9 proves non-tightness of standard deterministic-centered marginals at a dense set of boundary ranks. Its remark includes endpoint-averaging and expected-profile centering, but does not quantify all deterministic centers. Proposition 2.10 identifies the memoryless affine family; the present matrix does not belong to it. The manuscript then explicitly leaves one-/finite-dimensional marginal convergence open; this broad wording is in tension with the boundary result and is not a novelty proof.

## Exact overlap and exact remaining bridge

There is strong prior overlap in the mechanism: random selection crosses a profile jump, and root-n sampling displacements multiply a mean change of order n. The published boundary proof fixes a boundary t0; it does not put a fixed continuity rank within root-n of different increasingly small jumps. The square-position rank supplies the needed two scales. Its jump heights P_j go to zero, but distances t-tau_j are O(P_j (3/4)^(2j)); choosing sampling width w_j=P_j(3/4)^j makes (t-tau_j)/w_j -> 0 while P_j/w_j -> infinity. Positive probability on both sides, together with local near-constant profile bands, is a new missing lemma if attempting to derive the exact candidate from the older theorem. The universal-center conclusion additionally needs concentration-function separation of those two bands; the older standard-center result alone is insufficient.

No exact earlier theorem or fully supported earlier deduction yielding this particular nonboundary/all-centers conclusion has yet been found. This is a bounded-search provisional finding, not a claim of novelty. Broader general-source digital-tree, nonregular quantile, and inverse-modulus routes remain under review. No typical-rank root-n theorem has yet been located for this nonmemoryless source. The first-order theorem covers every nonboundary rank, but it neither proves typical-rank fluctuation convergence nor excludes exceptional failure.

## Inputs actually read before seal

```json
[
  {
    "path": "/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr166_30002720/original_submission/files/unsolved_math_prioritization/attempts/30002720/COUNTEREXAMPLE.md",
    "sha256": "c72a38099e93b4d593be231e8f0c4ad726a399c3d61283da9f7b1f7e55801a5c",
    "bytes": 13938,
    "kind": "allowed_candidate_or_neutral"
  },
  {
    "path": "/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr166_30002720/original_submission/files/unsolved_math_prioritization/attempts/30002720/problem.json",
    "sha256": "b25b2964c522c770b41f4400a293b660c752777acf7504f7ce0a2c957e78003f",
    "bytes": 4143,
    "kind": "allowed_candidate_or_neutral"
  },
  {
    "path": "/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr166_30002720/original_submission/files/unsolved_math_prioritization/attempts/30002720/source_manifest.json",
    "sha256": "2325db720e00963800ea8709efb31ca3b39b8125bdffdc6e52b73644f285c31f",
    "bytes": 1359,
    "kind": "allowed_candidate_or_neutral"
  },
  {
    "path": "/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr166_30002720/priority_irregular_quantiles/private/sources/analysis2014.pdf",
    "sha256": "f1aa771bc6171b2ecffa08cc775e074d08da761936a863b016fb3ef947304915",
    "bytes": 195401,
    "kind": "independently_retrieved_primary_literature"
  },
  {
    "path": "/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr166_30002720/priority_irregular_quantiles/private/sources/leckey_thesis.pdf",
    "sha256": "37ddf734aac042c05d9ceda726175dc9342c4bec81341a2e14a753580cdd1c73",
    "bytes": 1014772,
    "kind": "independently_retrieved_primary_literature"
  },
  {
    "path": "/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr166_30002720/priority_irregular_quantiles/private/sources/process_author.pdf",
    "sha256": "105c172a856ca0d54b214be903f107d9bb1769db8f20bb1534a5b63f62d45e18",
    "bytes": 689594,
    "kind": "independently_retrieved_primary_literature"
  }
]
```

Public search results retained under private/search_001.json through private/search_005.json record independently retrieved literature leads. The external Birmingham accepted-manuscript PDF was read through the web parser, but direct binary download returned HTTP 403. Its theorem pages agree in scope with the author manuscript; final publisher wording has not been certified. Search-engine irrelevant results were not used as mathematical evidence.

## Next falsification steps

Read general-source trie theorem hypotheses and cost definitions; test whether the present source even meets density-model assumptions; inspect nonregular sample-quantile theorem conditions and whether m composed with h can legally be an inverse CDF. Search for earlier exceptional-rank or deterministic-profile theorem. Treat any missing source-specific modulus lemma as a genuine gap.
