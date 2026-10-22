# Pressing connectivity normalization report

Database ID **3100089**, problem number **AMR-030-0089**, queue row **1749**.
The identifier was matched to the frozen database record and queue entry. This report concerns the pressing-sequence connectivity question on [Cooper's problem list](https://people.math.sc.edu/cooper/combprob.html).

## Accepted result

A connected six-vertex bicolored graph has exactly two successful pressing sequences, (1,4,0,5,2,3) and (2,3,0,5,1,4). Their longest common subsequence has length two, and their insertion/deletion distance is eight. Thus the successful-sequence graph is disconnected when each edge permits at most four total insertions/deletions, and also when the total budget is six.

The original Bixby–Flint–Miklós Conjecture 6 permits four removals and four additions, equivalently LCS at least the common sequence length minus four. The two sequences are adjacent at that threshold. They are also adjacent when unit-cost substitutions are permitted, with exact Levenshtein distance four. If all legal finite prefixes are states instead, deleting final letters gives a path to the empty word and proves connectivity for every graph. No resolution of the unqualified original problem is claimed.

The metric intended by Cooper–Davis's prose remains uncertain. No novelty, minimum-order, exhaustive literature coverage, or whole-original-problem resolution claim is accepted.

## Full proof and independent audit

- [Authored counterexample proof](COUNTEREXAMPLE.md): the graph, nonsingularity, exhaustive branch classification, longest-common-subsequence argument, distance proof, source normalization, and computational cross-checks.
- [Independent mathematical audit](AUDIT_REPORT.md): the complete 19-node legal-prefix tree, two successful leaves, four unsuccessful terminal branches, rank-drop argument, metric and state-space distinctions, source history, and acceptance limits. This document is byte-identical to the accepted audit.
- [Acceptance](ACCEPTANCE.json): the original independent audit decision and its exclusions. Its proof hash identifies the reviewed original edition; the editorial mapping below identifies the prepared edition.
- [Public source metadata](SOURCE_PINS.json): titles, public URLs, seven PDF byte/hash pins, retrieval and inspection records, and explicit inspection limits. No source PDF or extracted source document is included.
- [Aggregate checks](AGGREGATE_CHECKS.json): fresh three-mode independent-audit reruns, aggregate mathematical results, the bounded smaller-order search as reported, and recorded mutation controls.
- [Editorial mapping](EDITORIAL_MAP.json): source-to-prepared correspondence and exact preservation of the mathematical sections.
- [Closed manifest](MANIFEST.json): the exact permitted payload file set and each payload's byte count and SHA-256. The manifest is excluded from its own hash list and is separately pinned during preparation.

## Historical qualification

Cooper–Davis v1 contained a superseded general connectivity claim. The public v2 notice states withdrawal to verify a proof, and v5 omits the general theorem. The audit independently identifies a false triangularity-preservation step; it does not attribute that flaw to the authors as their explanation for withdrawal. The 2016 published Cooper–Davis article is bibliographically verified, but its full text was not inspected. Details and primary-source links are retained in the audit and source metadata.

## Scope of this packet

The proof and audit are self-contained mathematical arguments. Their essential finite branch tables are included. The packet contains authored mathematical exposition, acceptance, public verification metadata, and citations. It contains no copied third-party document, source extraction, raw external dataset, executable verifier, or private coordination material. Reported source inspection is limited to what the accepted audit records; preparation does not claim a new literature review.
