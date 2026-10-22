# Source-status report

## Exact target

For finite simple chordal graphs of order n, the question is whether their edges admit a partition into at most n²/6 + Cn cliques for some absolute C, uniformly in the graph and n. Parts may share vertices; they must not share edges. Isolated vertices are harmless and the edgeless graph uses zero parts. The question concerns all chordal graphs, not just split graphs, and permits an unspecified linear error.

The inherited statement matches the indexed [Erdős Problem 81 statement](https://www.erdosproblems.com/81). The original authors are Paul Erdős, Edward T. Ordman and Yechezkel Zalcstein, [Clique Partitions of Chordal Graphs, 1993](https://doi.org/10.1017/S0963548300000808). Its primary publisher abstract corroborates the problem and the older weaker bound. The complete 1993 article was not retrieved.

## Material new source

Obinna Okechukwu, [Clique partitions and bounded simplicial defect, arXiv:2609.20871v1](https://arxiv.org/abs/2609.20871v1), submitted 15 September 2026, is a 24-page primary preprint. Theorem 1.1 and Corollary 1.2 claim a uniform bound floor(n(n+1)/6) + K for every chordal graph, and an eventual exact extremal result. This is unconditional as stated. The graph conventions match the target. The source predates this review and postdates the inherited August assessment.

The exact implication is proved in HYPOTHESIS_BRIDGE.md. It is conditional only on the correctness of the cited theorem, not on an extra graph hypothesis. MAIN_PROOF_ASSESSMENT.md records a first-pass check of the actual argument rather than relying on the abstract. No fatal error was identified in that pass. This is not an independent final acceptance, and the stronger classification is not certified here.

## Status limits

The accessible arXiv record shows v1. No journal acceptance or subsequent formal validation was verified. Older indexed Erdős and UnsolvedMath pages still label the problem open, but their observed crawls predate this manuscript. They cannot establish a current mathematical verdict. Direct page retrieval had availability failures; these are recorded precisely in source_inspection.json. A bounded web search found no specific correction or withdrawal; absence of a search hit is not evidence that none exists.

The inherited report is empty; its full problem background is literature triage rather than substantive original proof work. Complete-record and dataset identity checks passed. Bounded repository searches found no matching earlier attempt, but they do not establish exhaustive history or novelty.

## Decision

Stop fresh proof approaches at 0/5 while the recent claimed resolution is assessed. Retain the status PRIOR_CLAIM_PENDING_INDEPENDENT_AUDIT. Do not label this already solved merely from the theorem statement, and do not claim the work here solves EP-81. A fresh auditor must independently examine the manuscript, the critical asymptotic-to-finite transition, and the imported results listed in the assessment before any stronger status is adopted.
