# Boolean-cube functional inequality: audited partial results

Problem **30001658 / OWR-4791-015**, supplied queue rank **704**.

**Unsolved after five of five substantive approaches.** The unrestricted all-dimensional resolvent inequality is not established. This release preserves the exact frozen author packet and independent adversarial audit. No novelty, global-current-openness, human-peer-review, or proof-assistant-certification claim is made.

## Controlling domain qualification

Read the frozen author `release/PROOF.md` §3 under the explicit qualification in `audit_release/AUDIT.md` and `audit_release/VERDICT.json`:

- The exact largest-coefficient quotient for a coordinate subcube applies only to **proper subcubes, integer codimension k >= 1**. “Every finite k” in that coefficient discussion has the same restriction.
- At **k = 0**, A is the full cube. Every coefficient multiplies zero, so there is **no finite largest coefficient**. The target is strict for nonzero f.
- The singleton necessary bound C <= 2 + 4/n requires **n >= 1**. The n = 0 cube places no constraint on C.
- The auxiliary resolvent bound remains well-defined at k = 0 and has full-cube equality. This auxiliary equality is **not target equality or coefficient optimality**.

These restrictions govern every presentation of the preserved unrestricted wording. Neither the retained partial results nor the universal necessary coefficient ceiling depends on an undefined endpoint quotient.

## Retained results and remaining gap

The source convention uses counting measure, ordered/double-counted adjacent pairs, base-two logarithms, nonempty A, and arbitrary real f on the **whole cube**. The supported-function theorem is not substituted for the unrestricted target.

The packet proves the exact positive-resolvent criterion and conditional equality description; the target for affine subspaces in every dimension; a dense-set regime including density at least 1/8; a weaker universal coefficient 2 ln(2); and a coordinate-compression reduction to downsets. An exact finite certificate establishes the target through dimension five. Supported-function transfer and the downset induction retain explicit unresolved gaps. The all-dimensional resolvent bound for arbitrary A remains missing; this is not a complete proof or a target counterexample.

## Files and immutable bindings

- `release/`: nine original author files, **41,351 bytes**, unchanged. Manifest SHA-256: `68a1fa6b5900a7cc03cd2d991e1a135afb2366a169b680ad5ac9db335203ed68`.
- `audit_release/`: eleven original audit files, unchanged. Manifest SHA-256: `319db7556fc80438f22288fd6a6b4261c192fb5d883a76691827d81bc642acf5`.
- `audit_release/AUDIT.md` SHA-256: `3e9c162a5dc9140872e60e0f4584f8ce44f0ae28cb04887fb7f16baea38546bf`.
- `PUBLICATION_MANIFEST.json`: complete payload inventory, hashes and byte counts, excluding itself.
- `verify_release.py`: strict publication inventory, immutable input binding, corruption controls and portable replay.

The original author files' “audit pending” and no-publication statements describe their frozen historical snapshot. The included audit and this release guide state the current acceptance and publication scope without modifying that evidence.

## Reproduce

Use Python 3.10+ and its standard library. No network, source PDFs or third-party packages are required. From any directory, pass paths to the preserved verifier and author directory:

```sh
python3 -B PATH/audit_release/verify_audit.py --source-dir PATH/release --expected-audit-manifest-sha256 319db7556fc80438f22288fd6a6b4261c192fb5d883a76691827d81bc642acf5
python3 -B -O PATH/audit_release/verify_audit.py --source-dir PATH/release --expected-audit-manifest-sha256 319db7556fc80438f22288fd6a6b4261c192fb5d883a76691827d81bc642acf5
```

For the entire publication payload, use `python3 -B PATH/verify_release.py --expected-manifest-sha256 HASH`; repeat with `-O`. Obtain HASH from an independently trusted release receipt or the PR description. A locally computed manifest digest is an internal-consistency check, not an independent authenticity guarantee.

Each mathematical replay uses **704,115 author checks, six mathematical and eight integrity negative controls**, and **1,282,085 independent exact checks with eleven mathematical negative controls**, under normal and optimized Python. Independent replay additionally rejects actual empty-directory, extra-symlink and replacement-symlink contamination. Publication verification rejects seven actual payload/pin corruptions in both modes. These counters support reproducibility and supplement the written proofs; they do not establish the unrestricted theorem or constitute a software-security guarantee.

## Source and publication limits

Original OWR equation (12), its surrounding normalization, and the later support restriction were independently inspected. The requested catalog page returned HTTP 403; full raw catalog records and complete corpora were unavailable and are not claimed inspected or matched. Public bibliographic records, PDF hashes/sizes and exact retrieval/inspection limits are recorded in the source metadata files. Bounded searches do not establish historical novelty or present global openness.

Only authored proof, audit, code and public verification metadata are included. No third-party PDFs, source extracts, images, raw records, dataset contents or private coordination files are included. The queue change is restricted to this row's Status = unsolved and Turns = 5/5; Findings, Chat, DOI, other rows and the existing header are preserved exactly. No merge, GitHub release, DOI registration or external outreach is part of this publication.
