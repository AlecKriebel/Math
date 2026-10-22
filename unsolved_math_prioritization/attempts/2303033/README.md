# B-regular localization: accepted partial investigation

Problem 2303033 / AMR-022-3033, rank 901. **Unsolved by this investigation, stalled after 2/5 substantive approaches.**

The retained result is an explicit two-disk lens showing that zero extension need not preserve resolutivity, together with a conditional transfer lemma requiring additional assumptions. The corner harmonic-measure density is comparable to s^(1/2), making s^(-5/4) data resolutive on the lens but its zero extension nonresolutive on the disk. This is not a counterexample to B-regular localization, a full solution, or a novelty claim.

Start with [the full mathematical audit](audit/MATHEMATICAL_AUDIT.md), [exact acceptance](audit/ACCEPTANCE.md), and [unchanged proof](author/PROOF.md). The relevant [Gauthier 2010 chapter](https://doi.org/10.1090/crmp/051/16) remains uninspected in full. Present-day literature status is unverified.

## Immutable history and correction

- `author/` preserves all nine original members exactly, including historical review/publication status.
- `corrected/` preserves the separately frozen accepted derivative. Only `verify.py` and its manifest entry differ; the mathematical text is unchanged.
- `audit/` preserves the audit's nine text members. Its two nested ZIP members are byte-identical to the original and corrected archives in `frozen_archives/`.
- All three complete original ZIP byte streams are stored as canonical base64 in `frozen_archives/`. No archive has been regenerated.
- External manifests, the audit receipt, exact acceptance, and a fresh stored-corpus/PDF rehash receipt are included. The corpus and PDFs themselves are excluded.

The original diagnostic uses 13 assertions, removed by Python optimization. The audit deliberately reproduces two optimized false passes. The accepted derivative uses 13 explicit runtime checks and its internal manifest records the change. The 26-case replay includes successful relocations, original false-pass reproduction, and corrected mutation rejection. It does not contain 26 rejection tests and is not a theorem prover.

## Portable verification

Use Python 3.10+ and the standard library, from any working directory:

    python /path/to/verify_publication.py --manifest-sha256 SHA256_FROM_PR_RECEIPT
    python -O /path/to/verify_publication.py --manifest-sha256 SHA256_FROM_PR_RECEIPT

The publication manifest hash is independently supplied in the PR description and final verification receipt. The wrapper requires it and checks its own bytes before executing any package script. It rejects missing, extra, symlinked, or changed files; checks all archive bytes, member allowlists, CRCs, internal manifests, nested archives, and exact acceptance pins; applies the actual unified patch and deterministically updates the sole changed manifest entry; and replays the frozen audit under normal and optimized Python in an isolated relocation.

Finite diagnostics support the analytic audit only. Stored source rehashes do not establish current literature status. No hosted CI pass, human peer review, formal proof-assistant check, or external acceptance is claimed.

## Queue change

Only this problem's Status and Turns cells change, to `unsolved` and `2/5`. Findings and all unrelated queue content remain byte-for-byte unchanged. No merge, release, DOI creation, or outreach is part of this publication.
