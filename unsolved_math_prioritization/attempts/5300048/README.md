# Periodic basin-boundary accessibility: corrected partial results

Problem 5300048 / AMR-052-0048, rank 954. **Unsolved, five of five substantive approaches.**

Read `audit/PROOF_CORRECTED_READING_COPY.md` for the accepted mathematics and `audit/ACCEPTANCE_REPORT.md` for the complete independent automated mathematical audit. All twelve numbered auxiliary results were accepted under their stated hypotheses. The full accessibility question remains open in this work; neutral points remain in scope. No admissible dynamical counterexample, historical novelty, formal proof certification, or human peer review is claimed.

The main retained result is analytic rigidity of the specified slit-comb domain: a proper holomorphic self-map extending across its closure is affine, hence degree one. The degree-two conformal transport therefore fails the extension hypothesis. Other results give restricted access criteria and precise obstructions to five attempted proofs.

## Preserved provenance and correction

- `author/` contains all nine frozen author files, unchanged, including the original proof and manifest.
- `audit/` contains all eight frozen audit files, unchanged, including the full report, actual patch, corrected reading copy, independent controls, and manifest.
- `audit/PRIME_END_WORDING.patch` is the only difference between the original and corrected proofs. A singleton principal set alone does not identify a specified point known only to belong to the impression. The corrected passage uses a singleton impression, membership in the landing ray's principal set, or a further identification argument, and explicitly states none is established.
- The final Corollary 5 already verifies the global pullback component and all four good-point conditions of the credited Przytycki theorem.

Frozen author statements about awaiting review or making no publication describe their original stage. The audit supersedes the review status; this wrapper records acceptance and preparation for a draft PR without rewriting the historical originals.

## Portable reproduction

Run `python3 verify_publication.py --mutation-controls` in this directory. Python 3's standard library suffices; no network, source corpus, PDF, external package, or patch utility is required. The verifier checks the exact inventory and manifests, reproduces the patch, runs the original 5,963 checks and independent 26,958 checks, compares deterministic outputs, and tests rejection of corrupted packets. Finite checks are diagnostic, not a proof of the universal question.

The packet contains authored mathematics, audit, code, and public verification metadata only. Third-party source documents/text, dataset contents, and private coordination files are excluded. `REPOSITORY_GATE.json` records a bounded fresh repository duplicate check. The repository queue edit is limited to this problem's Status, Turns, and Findings cells.
