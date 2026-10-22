# Statistical additive randomized encodings: finite existence

Problem 30006182 / OWR-14299084-004, *Information-Theoretic Additive Randomized Encodings*.

Accepted scope: every finite multiparty function has a finite-abelian-group additive randomized encoding with independent physical-party randomness, arbitrarily small pointwise statistical correctness and output-only total-variation privacy errors, against an external observer of the sum. This is the finite, statistical, non-robust interpretation of the original question. Its unqualified wording remains under-specified.

Credit belongs to Nir Bitansky, Saroja Erabelli, Rachit Garg and Yuval Ishai, *Shuffling is Universal: Statistical Additive Randomized Encodings for All Functions*, [ePrint 2025/1442](https://eprint.iacr.org/2025/1442), [STOC 2026](https://doi.org/10.1145/3798129.3800890). This edition reconstructs and audits their finite universality result; it claims neither novelty nor a new first resolution.

## Read the complete argument

- [PROOF.md](PROOF.md): complete two-party leaky/sharing construction; explicit perfect finite truth-table DRE; coordinator-local seed and bit-OT compilation; conditional hybrids, independence and both finite error parameters.
- [AUDIT.md](AUDIT.md): full mathematical audit, exact original-model correspondence, source/version and inspection boundaries, and all textual and quantitative cautions.
- [ACCEPTANCE.md](ACCEPTANCE.md) and [ACCEPTANCE.json](ACCEPTANCE.json): exact decision and exclusions.
- [SOURCES.json](SOURCES.json): public citations and exact inspected-file identities.
- [VERIFICATION.json](VERIFICATION.json): finite-check and authentication metadata with their limits.
- [MANIFEST.json](MANIFEST.json): exact eight-file inventory, with sizes and hashes for the other seven members.

The proof independently budgets T OT instances: correctness at most 16tT/q and privacy at most T2^(1-t). It does not certify the factor-free displayed error of the source's Theorem 5.2. Its explicit encoding cost is polynomial only in the explicitly padded binary truth-table size and accuracy parameter, not in an arbitrary succinct function description.

Perfect correctness, perfect privacy, malicious-insider robustness, infinite-domain universality under one finite group, and general polynomial-size encodings are not established. Additive encodings into a finite abelian group are the original target; affine dependence over a prescribed field is not required.

This AI-assisted, unrefereed edition records an internal AI audit of a prior published result. Acceptance here is an internal mathematical assessment, not human peer review or formal proof-assistant certification. Finite checks are corroboration only. This is a full written proof and audit edition, not a computational reproduction package. Source retrieval and inspection described below occurred during the preceding audit on 11 October 2026; this editorial preparation performed no fresh scholarly-source retrieval or inspection.

The inspected ePrint manuscript is the 23-page, 383423-byte file identified in SOURCES.json. Its PDF update dates to August 2025; June 2026 was metadata-only. The 11-page ACM proceedings file was not byte-compared. No source-author code was executed. This distribution includes no source PDFs, extracted source text, images, code, raw finite-check outputs or dataset contents.
