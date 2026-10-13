# Function Theory 7.42: annular counterexample candidate

Problem 2307042 / AMR-022-7042, queue rank 857. Status: **claimed_solved**, one substantive approach (1/5), with two independent AI mathematical acceptances. This is an unrefereed candidate, not a novelty or human-peer-review claim.

## Exact result

In the annulus `1 < |z| < e`, with base `a = sqrt(e)`, the minimal Martin kernel at the inner-boundary point `-1`, normalized to have value one at `a`, is strictly below the one-sided Harnack envelope throughout a punctured neighborhood of `a`. Thus this fixed kernel cannot equal the envelope throughout any nontrivial Green line issuing from the base. Equality at the base is retained. The result makes no claim about isolated contact farther away.

The proof constructs the Green and Martin kernels and proves minimality directly. Four globally positive harmonic competitors give a uniform all-direction first-order gap; a common Taylor bound gives the punctured-neighborhood conclusion. This is analytic reasoning, not finite angular sampling or numerical truncation.

## Read the mathematics

- [Immutable author proof](author/PROOF.md)
- [First independent audit](independent_audit/INDEPENDENT_AUDIT.md) and [acceptance](independent_audit/ACCEPTANCE.json)
- [Second independent adversarial review](second_review/REVIEW.md), [independent analytic lemmas](second_review/INDEPENDENT_LEMMAS.md), and [acceptance](second_review/ACCEPTANCE.json)
- [Source status and literature limits](author/SOURCE_STATUS.md)

Both reviews accept the original proof unchanged. No correction patch was required. All three original archives and their extracted members are preserved byte-for-byte; the first audit also reproduces the six author files unchanged. Historical pending-review and no-publication labels inside frozen packets describe their original creation stage. The two separate acceptance records and this publication wrapper supply the subsequent status without rewriting history.

Primary question: W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory (New Edition)*, [arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2), Problem 7.42 and Update 7.42, printed pages 173–174. The accepted interpretation is equality along the line, matching the source's disc-radius example. Neither a weaker isolated-contact question nor current worldwide openness is certified.

## Integrity and publication boundaries

[PUBLICATION_VALIDATION.json](PUBLICATION_VALIDATION.json) records the fresh checks and their exact limits. The first audit's 58 integrity cases passed after a fixture-only adjustment: the original harness copied read-only modes into disposable mutation fixtures, so a replay copy used writable byte copies for those temporary files. The verifier, cases, and published proof/audit artifacts were not changed. The second author-verification replay reproduced the saved report byte-for-byte: six isolated positive runs, nineteen negative controls, and three supporting checks. All thirteen final second-review archive checks were also replayed successfully.

These checks establish data integrity, not mathematical truth. The three ZIP payloads contain only authored UTF-8 mathematics, reviews, and bounded verification metadata. Two separately supplied Python helpers outside the ZIPs check integrity only. No executable mathematical payload exists. No repository-wide test-suite or CI success is claimed here.

[MANIFEST.json](MANIFEST.json) inventories the publication package; [QUEUE_DELTA.json](QUEUE_DELTA.json) records the sole queue change: this row's Status, Turns, and Findings cells. All other queue bytes, including the existing header, are preserved. No ranking, score, source record, or other queue row is revised.

The package excludes copied source documents, raw source extracts, dataset contents, private sources, and private coordination material. OpenAI tools were used extensively. Historical novelty, priority, formal proof-assistant certification, and human peer review remain unestablished.
