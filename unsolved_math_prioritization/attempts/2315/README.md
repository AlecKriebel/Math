# Rainbow quadrilateral colorings: accepted scoped partials

**Problem 2315 / EP-810, selection rank 903. Queue: unsolved, 5/5.**

The original density problem remains unresolved by this attempt. The [original proofs](author_original/PROOFS.md), [full independent audit](independent_audit/INDEPENDENT_AUDIT.md), and [exact acceptance](exact_acceptance/EXACT_ACCEPTANCE.md) are preserved unchanged. No mathematical repair was required and no correction derivative exists.

## Accepted scope

The strongest result makes an arbitrary rainbow-C4 coloring proper after deleting o(n²) edges, with inherited colors and a threshold uniform over graphs and palettes. It gives an all-sufficiently-large-size positive-density equivalence with the balanced bipartite proper version using an **available palette of at most s colors**. This is not certified as equivalent to the 2023 source's literal hypothesis that the **minimum** palette q_B(G) equals s. Adding unused colors does not change that minimum.

The other accepted results are the (7,4)-free linear tripartite hypergraph forward projection and failed converse, the unit-coefficient cyclic affine-label obstruction, the complete uniform blowup obstruction, and the codegree quadratic-root upper bound. Exact hypotheses and exclusions are in the separate acceptance. The removal and finite multidimensional Szemerédi theorems are credited external dependencies.

No all-size positive-density construction, proof of its negation, or arbitrary-coloring universal o(n²) sparsity theorem is supplied. No novelty, priority, exhaustive literature clearance, independently verified current tracker status, human peer review, or formal proof-assistant certification is claimed. The five-approach limit is exhausted; publication adds no new mathematical approach.

## Frozen provenance and reproduction

All three ZIPs, external manifests, original members, audit members, exact acceptance members and the independent receipt are byte-preserved. Historical pending-audit and no-publication fields describe their original freeze stages; the later independent acceptance and this publication record do not overwrite that history.

Run `python -I -S -B verify_publication.py` and `python -I -S -B -O verify_publication.py` in this directory. Run `test_publication.py` under the same two modes for negative controls and relocation. These programs check byte identity, ZIP safety, exact inventories, receipt/acceptance bindings, and scope flags. They contain no executable mathematical proof or solver. Neither mode is mathematical validation.

Optional `--catalog`, `--problems`, and `--reports` together verify the three nonbundled complete input files, target identity and complete-record/report serialization. Optional `--sources-directory` verifies all six nonbundled source-PDF byte/hash pins. Optional `--queue-base` and `--queue-current` together verify that only the target Status and Turns cells change. Omitted optional inputs are explicitly reported as skipped. No network operations occur. The local test record reports actual full-corpus, source-pin and queue checks; it does not claim fresh source retrieval or repeat the audit's source-theorem inspection.

The manifest binds the public files. Raw source PDFs, extracts, rendered pages, corpus contents, private sources and private coordination are excluded. Only Status and Turns change in the existing queue; Findings, notes, chat links, DOI cells and every unrelated byte are preserved. This is a draft publication only. Remote CI is reported separately; no checks is not a CI pass.
