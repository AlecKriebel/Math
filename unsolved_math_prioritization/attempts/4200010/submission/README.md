# Knill item 10: positive-volume zero-exponent non-almost-periodic band

Problem 4200010 / AMR-041-0010. Status: `claimed_solved` (complete candidate; independent audit pending). AI-assisted, unrefereed, and no historical novelty claim.

`FULL_PROOF.md` constructs a compact connected symplectic four-manifold and a smooth autonomous Hamiltonian with an invariant band of normalized Liouville volume 1/4. Every exponent in that band vanishes, and no positive-measure invariant part has an almost-periodic Koopman representation. Each energy component already fails almost periodicity.

The elementary mechanism is an irrational skew shift, its mapping torus, and a smooth Hamiltonian cutoff on an extra circle. The statement concerns the unrestricted smooth symplectic category actually printed in the source. It does not certify extra Euclidean, natural-mechanical, analytic, contact-type, genericity, or weak-mixing requirements.

## Reproduce

Run `python3 verify.py` for exact rational algebra checks and falsification controls. Compare with `CONTROL_RESULTS.json`.

Run `python3 verify_manifest.py` to verify every release file and reject extra files. The scripts require only the Python standard library, make no network requests, and do not load third-party datasets.

## Read in order

1. `SOURCE_GATE.md` for target identity, source scope, and prior-result limits
2. `FULL_PROOF.md` for the full analytic proof
3. `VALIDATION_LIMITS.md` for what the checks do and do not establish
4. `APPROACH_LOG.md` and `turns.jsonl` for the two substantive approaches
5. `SOURCE_MANIFEST.json`, `STATUS.json`, and `MANIFEST.json` for provenance and frozen bytes

No source PDFs, copied source text, dataset rows, full corpora, or private coordination files are included.
