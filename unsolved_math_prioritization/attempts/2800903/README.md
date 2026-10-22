# Gaussian data-point k-median LP: accepted partial results

**Original problem unresolved; five of five substantive routes used.** Read [acceptance](ROOT_ACCEPTANCE.md), the complete [proofs](public/RESULT.md), and [independent audit](independent_audit/FULL_AUDIT.md). These results do not settle the unspecified joint n,d,k probability question.

- `public/`: immutable author freeze; historical review-pending wording is preserved.
- `independent_audit/`: immutable independent acceptance, full audit, checks, patches and corrected reference copies.
- `corrected/`: exact adoption of the two patches. Use its hardened verifier for optimization-safe finite checking and its corrected source notes for the optional historical reference.
- `VERIFY_PUBLICATION.py`: strict source-free byte inventory, pinned frozen manifests, exact patch replay and disposable computation replay.
- `TEST_MUTATIONS.py`: fail-closed wrapper controls, including substitution rejected by an externally pinned bootstrap.
- `PUBLICATION_MANIFEST.json`: outer file inventory. Its expected hash and the verifier hash must be obtained from an independent trusted record, such as the draft PR description. Hashes co-located with an untrusted packet cannot authenticate themselves.

After independently checking the verifier's SHA-256, run `python -I -B VERIFY_PUBLICATION.py --expected-manifest <trusted SHA-256>`. The wrapper may itself run under `-O` or `-OO`; it always launches the original assertion-based verifier in a fresh ordinary process with all inherited PYTHON settings removed. Corrected and audit programs are replayed in all three modes. Disposable directories preserve every frozen byte. Python 3.12.14 and the standard `patch` utility reproduce the archived audit receipt exactly; a different Python version is rejected by receipt-byte comparison because the audit records its version.

For integrity fault controls, first independently verify the mutation driver's hash from the outer manifest, then run `python -I -B TEST_MUTATIONS.py --expected-manifest <trusted SHA-256> --expected-verifier <trusted SHA-256>`. These checks are not a proof assistant or a sandbox for arbitrary untrusted Python.

No source documents, external dataset or network access are needed for replay. This is independent AI review, not human peer review or a novelty certification.
