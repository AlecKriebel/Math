# Current editorial qualification — 17 October 2026

This edition retains the original submitted mathematical text below and adds current attribution and evidence qualifications. The full existence classification under the four equations printed in Dietzel, *Some problems on L-algebras*, OWR9/2023, Definition2 and Problem3, is accepted after fresh root verification, a genuinely source-only reconstruction and separate independent adversarial reviews. No all-products classification, self-similarity, cancellation, or extra unstated axiom is claimed. Under the separately attested meet-monoid convention both existence questions require a greatest element; that convention predates the workshop, including arXiv:2206.04955v1 (10June2022), Definition3.1.

**Prior construction credit.** The joint operation x·y=e for x≤y, and x·y=x∧y otherwise, is already printed by José Luis Castiglioni and Hernán Javier San Martín, *On a symmetrization of hemiimplicative semilattices*, arXiv:1611.09589v1 (29November2016), p7, Example3.5, formula(4). Their p2 defines bounded as having a greatest element; this formula needs no bottom or distributivity. The final publication is titled *l-Hemi-Implicative Semilattices*, Studia Logica106(2018),675–690, DOI10.1007/s11225-017-9759-3 (online3October2017). The version-pinned body and final bibliographic metadata are distinct evidence. This is attributed verification and deduction of the full printed existence answer, not a claim of a new solution, operation, mechanism, first combined statement, independent discovery or current worldwide openness. Earlier L-algebra and closure theory is due to Rump; the question is credited to Dietzel. Historical priority for an earlier explicit combined conclusion remains unestablished after a bounded audit, with missing earlier source bodies disclosed separately.

**Historical versus current evidence.** All eight submitted Git-authenticated files are retained verbatim in original_submitted/ of the verification package. The earlier6872-byte candidate,10375-byte audit and original finite-enumeration programs referred to in the submitted receipts were unavailable in this audit. Their hashes, old acceptance declarations, old counts and first-person statements below are historical records, not fresh certification of absent inputs or rerun results. Available public-side byte ranges were checked, but that does not authenticate missing old-side bytes. Fresh reproducible programs/results and independent review records are separately identified in the package. Any historical wording such as new refers to progress relative to an earlier partial candidate and grants no literature-priority claim. The original mathematical proof below remains an object of the current verification.

AI tools were used extensively for reconstruction, mathematical checking, computation, literature auditing and preparation. This work is unrefereed, with no external human peer review or formal proof certification. The present qualification governs the historical text that follows.

---

## Original submitted text, preserved verbatim

# Acceptance report: complete semibrace existence classification

## Decision

PASS for the complete existence classification under the axioms printed in workshop Definition 2, with the separately stated L-algebra condition and monoid-convention qualification. The independent audit found no mathematical repair necessary. This report binds that review outcome to the exact public editions below.

This is AI-assisted, unrefereed work. This acceptance report is a mathematical verification record, not journal acceptance, human peer review, external institutional approval, or formal proof-assistant certification. No historical novelty or unstated authorial intent is claimed.

## Bound proof and audit

- Original frozen complete proof: 6,872 bytes; SHA-256 46c340870fc038943d939a0abbd82703a87e9e6a7dacd060b32857da143b76ac.
- Public [PROOF_CLASSIFICATION.md](PROOF_CLASSIFICATION.md): 6,951 bytes; SHA-256 6ae82358e44f7382d949f11f1dc6c16a29a29b283f13d7a5c6a9df1ff8720b84.
- Original frozen independent audit of that complete proof: 10,375 bytes; SHA-256 5ef79d7c4eb1b5e0893198de4885613947a7efbf0fd2b75d1ab9f7e6fda981fb.
- Public [INDEPENDENT_AUDIT.md](INDEPENDENT_AUDIT.md): 10,525 bytes; SHA-256 5a109ac60c54a33645bcfaa4ad1ca106f53c6cee18af54e260b1b511f3bb0bc1.

The original complete-proof candidate and independent audit hashes were recomputed before preparation. The complete public editions were reconstructed from those inputs using only the editorial edits recorded by offsets, lengths and hashes in [BYTE_PRESERVATION.json](BYTE_PRESERVATION.json). All remaining bytes and the named mathematical regions were compared directly. All mathematical text is preserved; the public editions are not abbreviated summaries. The earlier partial-candidate audit is not the audit bound by this acceptance.

## Accepted mathematical conclusions

1. Every nonempty meet-semilattice admits the four printed semibrace equations, by right projection with any distinguished element; the empty set does not.
2. A meet-semilattice admits those equations together with the printed L-algebra axioms if and only if it has a greatest element.
3. In every joint realization the distinguished element is greatest and the meet order equals the L-algebra order.
4. On every meet-semilattice with greatest element e, the operation x·y=e when x≤y and x·y=x∧y otherwise supplies the joint structure. All equations and separation are verified algebraically; arbitrary infinite and nondistributive cases are included.
5. Under the separately attested monoid convention, which also requires e to be the meet identity, both existence questions instead require a greatest element. This convention is not described as a later invention.
6. The operation in Problem 10 has a different second branch, y, and fails meet preservation on the four-element Boolean lattice. That negative control does not affect the construction proved here.

The result concerns existence, not all possible operations, self-similarity, group-brace structures, or additional hypotheses absent from the displayed definitions.

## Evidence and limits

The complete independent audit reconstructs necessity, sufficiency, equality of orders, edge cases, and the source-convention distinction. The full contribution by Dietzel was inspected on printed pp. 544–547, including its footnote and Definitions 1 and 2. [The official workshop PDF](https://ems.press/content/serial-article-files/47003) has 286,244 bytes and SHA-256 0ba13c573755289bb62e119df381d19e03a31cb3fff8e1ff3e240dce8dfeeefc. The inspected [enumeration-paper v4 PDF](https://arxiv.org/pdf/2206.04955v4) has 429,694 bytes and SHA-256 cd5551caffcc3c69959fbc72bbcdc1b0d2d736aa14569fd5df34a257dd435ea6. These byte pins were recomputed during preparation. No independent byte-for-byte redownload of the workshop PDF is claimed.

The public arXiv record dates the enumeration paper's earlier versions before the workshop. Its separately inspected Definition 3.1 explicitly assumes a commutative monoid. The workshop's cited [2008 Rump article](https://doi.org/10.1142/S0219498808002904) could not be inspected because its PDF request returned HTTP 403. The theorem's accepted scope remains the printed workshop axioms and the separately inspected convention; it is not a claim about uninspected source wording.

Supplementary finite checks cover every naturally labelled meet-semilattice through six elements, 2,152 pointed projection structures, 51 top-element construction instances plus explicit M3, and 114,745 L1-constrained multiplication tables through four elements. All qualifying joint structures have the required greatest element and matching orders. Normal and optimized Python runs were repeated during preparation and reproduced the audit's outputs byte for byte. These are stress checks, not the basis of the universal theorem and not formal certification. Full aggregate scope and counts are in [AGGREGATE_CHECKS.json](AGGREGATE_CHECKS.json).

## Publication boundary

The allowlisted packet contains the full authored proof, full complete-proof audit, this acceptance report, the README, source metadata, aggregate checks, byte-preservation metadata, and file manifest. It excludes third-party source documents or copied extracts, raw datasets, posets or operation tables, scripts, and private coordination material. Local validation aids are outside the public packet. Mathematical conclusions and evidence limitations must remain visible when the result is summarized.
