# Edition provenance and limits

Date: 2026-10-09. Problem: 2304015 / Hayman Problem 4.15.

## Authored mathematical content

The [complete certificate](APPLICABILITY_CERTIFICATE.md) preserves the full authored derivation, exact coefficient-model and degree comparison, probability-to-cardinality conversion, uniform tolerance, multiplicity and boundary treatment, citations, publication distinctions, and verification limits. The mathematical body and public references are byte-identical to the original authored certificate. Editorial changes remove a queue rank and obsolete workflow-only statements. Metadata line spacing and a heading's problem-number punctuation are normalized. No mathematical conclusion is strengthened by packaging.

## Evidence separation

[SOURCE_MANIFEST.json](SOURCE_MANIFEST.json) retains public scholarly metadata, version-pinned URLs, original raw-PDF hashes and byte counts, and bounded retrieval/inspection history. Original source copies, extracted text, page renderings, local paths, derived-artifact hashes, and private coordination records are excluded. The two PDF fingerprints identify sources consulted; the PDFs themselves are not included.

The source audit's public-record checks and downloads occurred on 9 October 2026. Packaging independently rehashed the already-held raw PDFs and matched their recorded sizes and SHA-256 values. The certificate's fresh-download statement and the ledger's timestamps describe that original source acquisition. Packaging performed no new source download, journal-PDF inspection, or whole-manuscript proof audit.

The inspected technical manuscript is arXiv:2011.06234v2, dated 24 January 2022. The official publisher metadata establishes the 2021 journal publication and matching conclusion. No identity of the two texts is claimed.

## Disposition and limits

Hayman Problem 4.15 is resolved by Oren Yakir's published 2021 result. This edition verifies the exact implication from the version-pinned theorem to the target family.

For H(z) = sum from k = 1 to n of epsilon_k z^k, set Q(z) = H(z)/z. Multiplication by z adds exactly one simple zero in the open unit disc. Yakir's exceptional probability tending to zero therefore gives the uniform tolerance n^(9/10) + 1 outside o(2^n) target polynomials, with zeros counted with algebraic multiplicity.

[ACCEPTANCE.json](ACCEPTANCE.json) accepts only this statement-to-target transfer. The apparent p.5 proof-text issues and the independent boundary-theorem dependency remain disclosed. This edition makes no novelty, formal-verification, or human-peer-review claim. Zero new proof-search approaches and zero proof turns are recorded.

## Integrity

[MANIFEST.json](MANIFEST.json) lists all eight edition files and hashes the other seven without a circular self-hash. Only UTF-8 Markdown and JSON are included. Preparation checked each byte count and hash and replayed the addition-only patch into a clean temporary directory. These are packaging checks, not a hosted-CI or whole-proof pass.
