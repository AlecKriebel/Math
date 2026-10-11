# Fare zone assignment with bounded congestion

## Scoped partial algorithms and model correction

For explicitly listed tree paths with nonnegative rational weights and nonnegative rational capacities, both finitely encoded in binary, the hard-capacity problem has a feasible decreasing-profit greedy guarantee of at least OPT/k when congestion k is positive. Congestion at most two admits exact polynomial-time optimization through a unit-edge-capacitated degree-bound formulation and an explicit reduction to ordinary general-graph weighted matching. Congestion zero has optimum zero.

The original Oberwolfach paragraph does not expressly specify signs, number domains, or encodings. These are explicit hypotheses of the theorem in this packet. Zero-weight commodities still impose their constraints, and rational capacities are floored and clipped exactly.

The later manuscript *Fare Zone Assignment on Trees*, arXiv:2512.19493v3, permits over-budget commodities to drop out. A complete authored two-edge example has hard-capacity optimum 3 and dropout optimum 4. Its purpose is to demonstrate a model distinction; it does not dispute that manuscript's results for its own model or rule out a separately proved transfer.

## What is accepted

This packet accepts only the bounded-congestion baseline and model correction. It does not resolve the full original problem, establish a sharp approximation ratio, certify novelty, supply a new hardness result, or fully audit the later manuscript. The general greedy framework is attributed to Mestre, and ordinary weighted matching to established literature including Gabow.

The proof, review, and preparation are AI-assisted. There is no external human certification, journal acceptance of this packet, or formal proof-assistant certification. Finite computations supplement the written proof and do not prove the general theorem.

## Files

- `PROOF_AND_MODEL_CORRECTION.md`: full accepted proof, byte-identical to the audited 16,006-byte document, including input conventions, greedy proof, exact matching gadget, and model-separation example.
- `AUDIT_REPORT.md`: full audit with two exactly recorded editorial changes concerning the local-only checker and the narrower publication allowlist. All mathematical statements are unchanged.
- `ACCEPTANCE_REPORT.md`: precise accepted scope, attribution, provenance, and limitations.
- `SOURCES.md`: public scholarly references and the audit's targeted inspection boundaries.
- `PUBLIC_SOURCE_METADATA.json`: inspected source identities, PDF hashes and sizes, version information, and retrieval/inspection history. No source PDF or copied source text is included.
- `MATHEMATICAL_CHECKS.json`: aggregate finite-check counts and the authored four-choice separation example. It contains no raw instance collection.
- `VERIFICATION_METADATA.json`: input pins, byte-preservation checks, three local rerun results, source-pin matches, and exact editorial replacements.
- `PUBLICATION_MANIFEST.json`: exact public-file allowlist and SHA-256/byte-count inventory. Its own digest is recorded separately because a file cannot meaningfully contain its own digest.

The executable finite checker, validators, control tests, source PDFs, extracted text, images, raw datasets, and coordination material are excluded. The upstream audit manifest remains local because its original allowlist included an executable checker; it is not this packet's publication authority.

## Reading order

Read the full proof first, then the audit and acceptance report. Consult the source records to see exactly which versions and portions were inspected. Hashes identify bytes and do not certify mathematical truth, authorship, novelty, or peer review.

Prepared 11 October 2026 for problem 30006109, audit identifier row 1688. This packet is a prepared local deliverable; it does not itself establish that anything was published or that a repository or queue was changed.
