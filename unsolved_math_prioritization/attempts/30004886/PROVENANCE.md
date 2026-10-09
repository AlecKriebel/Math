# Edition provenance and limits

Date: 2026-10-09. Problem: 30004886.

## Authored mathematical content

The [complete certificate](HYPOTHESIS_CERTIFICATE.md) preserves the source audit’s mathematical arguments, exact hypothesis mapping, boundary cases, citations and verification limitations. Nonmathematical edits remove historical workflow language. In the supergroup certificate, the short literal source quotation is replaced by an equivalent authored mathematical formulation; its target and subsequent proof are unchanged. No mathematical conclusion is upgraded by packaging.

## Evidence separation

[SOURCE_MANIFEST.json](SOURCE_MANIFEST.json) retains only public scholarly titles, public URLs, original raw-PDF hashes and sizes, status and bounded inspection history. Original source copies, local source paths, extraction/image hashes and copied source content are excluded. Those PDF fingerprints identify the source versions consulted; the PDFs themselves are not part of this edition.

The original audit’s public-source status checks occurred on 9 October 2026. Packaging independently rehashed the previously held public PDFs and matched the recorded sizes and SHA-256 values. It performed no new PDF download, no fresh publisher-full-text inspection, and no whole-manuscript proof validation.

## Disposition

The exact complex-algebraic supergroup containment conjecture is resolved by the 2024 SSV Sylow-theory preprint, with published 2026 group-level corroboration.

The certificate identifies the actual standard block subgroup SL(1|1)^n, checks its global form, proves the inside-K minimality step using both directions of splitting transitivity, and accounts for disconnected K and n = 0.

[ACCEPTANCE.json](ACCEPTANCE.json) accepts only the stated applicability/implication level. This edition does not assert novelty, formal verification or human peer review. Zero new proof-search approaches and zero proof turns are recorded.

## Integrity

[MANIFEST.json](MANIFEST.json) lists all eight edition files and hashes the other seven without a circular self-hash. Only UTF-8 Markdown and JSON files are included. A separate preparation check validated every listed byte count and hash and replayed an addition-only patch into a clean temporary directory. This is packaging verification, not a hosted-CI or mathematical-proof pass.
