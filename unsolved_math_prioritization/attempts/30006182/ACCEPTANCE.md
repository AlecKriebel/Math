# Acceptance: finite statistical non-robust existence only

Decision: ACCEPT_PRIOR_RESULT_STATISTICAL_FINITE_NONROBUST.

For every finite k-party function f and every epsilon > 0, the complete reconstruction in PROOF.md supplies a finite abelian group, independently randomized local encoders, a deterministic decoder and an output-only simulator. For every fixed input, decoding error and total-variation privacy error are each at most epsilon. No computational hardness assumption is required. The observer receives only the sum; collusion with an insider is excluded.

The original source is Yuval Ishai's Part 1 contribution in *Cryptography*, Oberwolfach Reports 3/2025, printed pp. 150-151, DOI https://doi.org/10.4171/OWR/2025/3 . Its finite abelian-group model does not impose affine dependence over a field. The question's unspecified error, robustness and efficiency conventions prevent unqualified acceptance under every interpretation.

The positive result is credited to Nir Bitansky, Saroja Erabelli, Rachit Garg and Yuval Ishai, *Shuffling is Universal: Statistical Additive Randomized Encodings for All Functions*, https://eprint.iacr.org/2025/1442 , Theorem 1.1; STOC 2026, https://doi.org/10.1145/3798129.3800890 . The source publication and this independent authored reconstruction have different review statuses.

## What was established

The full two-party construction and simulator are retained. A fully explicit finite truth-table DRE is perfectly correct and private as an auxiliary object. A physical coordinator samples its seed locally and compiles its bits using T bit-OT AREs with independent randomness between physical parties. Conditional hybrids and union bounds give final errors 16tT/q and T2^(1-t). The explicit finite choices of t and q make both errors at most epsilon.

The auxiliary DRE's perfect guarantees do not make the final ARE perfectly correct or private. The final scheme permits arbitrarily small nonzero errors. This proof uses elementary finite probability and an explicit DRE; it does not import the source paper's sharper efficiency results.

## Exclusions and quantitative cautions

- No unqualified all-interpretations resolution of the original question.
- No perfect correctness or perfect final privacy, insider robustness, or one finite group for all infinite inputs.
- No general polynomial-size statistical encoding for succinct functions; polynomial cost is only in the explicitly padded binary truth-table size and accuracy parameter (or in accuracy for fixed f).
- No certification of Theorem 5.2's literal factor-free displayed batch error. Our T-instance bounds establish finite existence without it.
- No independent acceptance of constant-overhead, sublinear-table, NL/poly or computational P/poly corollaries.
- No novelty, priority, external review, or formal replay claim.

The source's 23-page ePrint manuscript was inspected during the preceding audit. The August 2025 PDF and June 2026 metadata-only dates remain distinct, and no byte-equivalence with the 11-page ACM proceedings file is asserted. AUDIT.md preserves all six textual/quantitative cautions and precise inspection boundaries.

This AI-assisted, unrefereed edition records an internal AI audit of a prior published result. Acceptance here is an internal mathematical assessment, not human peer review or formal proof-assistant certification. Finite checks are corroboration only. This is a full written proof and audit edition, not a computational reproduction package. Source retrieval and inspection described below occurred during the preceding audit on 11 October 2026; this editorial preparation performed no fresh scholarly-source retrieval or inspection.
