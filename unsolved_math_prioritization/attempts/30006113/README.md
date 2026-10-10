# Source-credit resolution of the strong-density FVS extreme-point question

Problem 30006113; IDs 30004905 and 30006114 concern the same underlying Fiorini question. The original statement is **resolved, source-credited to Chandrasekaran, Chekuri and Kulkarni's Theorem 1 in arXiv:2609.04414v1**, with the explicit elementary corrections and formulation bridge documented here.

For a finite undirected simple loopless graph containing a cycle, every extreme point of the original nonnegative strong-density polyhedron has SOME coordinate at least 1/2. This covers every extreme point, including disconnected graphs and isolated vertices. It is not a claim that every coordinate is half-integral or a claim about the ordinary cycle-cover LP.

The source uses the bounded polytope B = P intersect [0,1]^V. A hypothetical extreme point of the original P with all coordinates below 1/2 belongs to B and remains extreme there. The bounded theorem excludes it. The complete authored audit supplies this bridge and reconstructs the source's structural proof.

## Included documents

- [AUDIT_REPORT.md](AUDIT_REPORT.md): complete authored mathematical reconstruction, dependency audit, strictness checks, scope controls and source credit
- [CORRECTIONS.md](CORRECTIONS.md): complete accepted elementary repairs, unchanged from the accepted audit
- [ACCEPTANCE.json](ACCEPTANCE.json): exact accepted scope and original-versus-distributed document identities
- [STATUS.json](STATUS.json): original target, same-target IDs, source attribution and limits
- [SOURCE_REVIEW.md](SOURCE_REVIEW.md): full bibliographic credit, formulation differences and historical status limits
- [SOURCE_METADATA.json](SOURCE_METADATA.json): four source PDF hashes/sizes, retrieval/inspection history and supplementary verification summary
- [MANIFEST.json](MANIFEST.json): exact eight-file inventory, hashing the other seven members

The retained repairs use total set cardinality for termination, the endpoint weak comparison, a double-counted intersection degree expansion, the all-component disconnected inequality, and the isolated-vertex coefficient caveat. Theorem 2's structural argument is a checked cross-check with its edge-set formulation distinguished. Broader algorithmic and orientation claims are outside acceptance.

## Credit and review limits

Karthekeyan Chandrasekaran, Chandra Chekuri and Shubhang Kulkarni, *An iterative rounding 2-approximation for Feedback Vertex Set via AI-assisted proof of an extreme point property*, arXiv:2609.04414v1, 3 September 2026: https://arxiv.org/abs/2609.04414v1

The source is an unrefereed AI-assisted September 2026 preprint. The historical landing-page check found only v1 and did not establish journal acceptance. The question is attributed to Samuel Fiorini; the 2021 and 2024 reports and the published polyhedral paper are cited in the audit and source review.

This audit and edition are also AI-assisted and unrefereed. Acceptance is not external human peer review, journal acceptance or formal proof-assistant certification. No novelty, new solution or priority is claimed. Historical literature checks are bounded, not exhaustive status certification.

Every mathematical section and all substantive audit findings are preserved. Only two nonmathematical audit wrapper paragraphs were edited; the corrections document is byte-identical. Programs, raw outputs, generated certificates, datasets, copied source documents/text/images and private coordination material are excluded. Finite checks are supplementary; the argument has no omitted computational dependency. Preparation rechecked frozen inputs, replayed the supplementary arithmetic checks and verified the publication edition, without new scholarly-source retrieval or new literature research. QUEUE.md and unrelated repository content are unchanged. No merge, release, DOI, journal submission or outreach is implied.
