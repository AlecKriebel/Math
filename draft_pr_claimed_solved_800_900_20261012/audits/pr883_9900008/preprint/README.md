# A periodic counterexample to the diffuse allocation characterization

Alec Kriebel · ORCID https://orcid.org/0009-0001-9320-500X · 15 October 2026 · version 1.0.0

The four-page `output/pdf/note.pdf` answers the unrestricted diffuse-measure question in Thorisson's undated *Some Open Probability Problems*, Problem 4.1, also stated as Last–Thorisson (2009), Problem 7.5: invariance under every deterministic, pair-generated, measure-preserving allocation does not imply mass-stationarity. The example is Lebesgue measure on parallel horizontal lines with alternating transverse weights 1 and 2. The proof treats all measurable allocations, including noninjective maps; finite computations are supporting diagnostics, not the proof.

The entire negative existential conclusion also follows from the atomic example in Last–Thorisson (2009), an allocation-transfer argument, and the product equivalence in their 2014 preprint/2015 paper. The note gives that deduction, credits Last–Thorisson (2023), Section 8 and Remark 8.1, for the prior invariant-direction obstruction, and distinguishes the balancing-allocation scope of Khezeli–Mellick (2025), Remark 3.2. We claim neither a new general discovery nor first recognition; priority of the precise periodic formula is unverified. `CURRENT_PRIORITY.md` records the bounded search and operational disposition. The recorded `claimed_solved` status is not a certificate of novelty or present-day openness.

This is an unrefereed research note. AI tools were used extensively in reconstruction, checking, writing, and adversarial review. No completed human peer review or formal proof-assistant verification is represented.

## Contents and trust

`verification.zip` is a portable, closed inventory of the note, original evidence, current scripts, and explicitly selected audit records. The expanded identical tree is `verification_package/`. It preserves all 26 files from PR #883 at `af25d26e21945a1a132aace5e600485152777070` under `source/`, including its two original ZIPs. `root_evidence/SOURCE_MANIFEST.json` independently binds their byte counts, SHA-256 digests and Git blob IDs; its SHA-256 is `53bba0a85fa099146f7bb6d7520bc8a3a423894b702a9e8e4cb9f63ded3a48ab`.

Historical reports, verdicts, proposals, and receipts remain dated evidence with their original scope. In particular, the proposed `already_solved` reclassification was rejected and never applied; the corrected qualified disposition governs this note. A corrected reviewer-only equal-weight control is documented without changing the candidate. Earlier source-credit omissions and the limitations of the original verifiers are retained in the audit record. Neither the original safe ZIPs nor a historical acceptance is approval of this current package.

The first whole-package review found four legacy command/error fields with local absolute paths. Parent-authored publication amendments normalize those fields, preserve the original JSON byte counts/hashes and raw observations, and distinguish normalized-file fingerprints from original subprocess-output fingerprints. Its historical ISSUES report is retained and counts as no CLEAR; two new successive whole-package reviews must cover the repaired seal. See `root_evidence/LEGACY_RECEIPT_PATH_REDACTION.json` and the two affected audit families' `PUBLIC_PATH_AMENDMENT.json` records.

Before executing code, obtain the inventory digest from an independently trusted release/review record, inspect the scripts, and authenticate their bytes separately. A digest supplied only by the same untrusted directory is not an external trust anchor. The current portable verifier has SHA-256 `e80ce30e89547c52d63c44237a554f0b3bf1ae1959783bbbba1f3f1703e9f7f8`; the original checker has `e4fb73b16db72ed4387c08c38662a1ad9f836f9b0ecd2ff91778347deb74829b`; the builder has `2b0521d74a49360cbdd6d48427cb02763b586f3a5196766ec16f6ddc2fa41f2c`. Authenticate the outer verifier separately when using the repository-level entrypoint.

## Reproduce the portable package

Python 3.10 or later, standard library only. All current entrypoints require interpreter isolation, disabled site initialization, and disabled bytecode writes. From an unrelated working directory, replace `PACKAGE` with the ordinary expanded package directory and `INDEX_SHA256` with the externally trusted digest of its `package_index.json`:

```sh
python3 -I -S -B PACKAGE/verify_package.py INDEX_SHA256 --root PACKAGE
python3 -I -S -B -O PACKAGE/verify_package.py INDEX_SHA256 --root PACKAGE
```

Default verification authenticates every indexed file, strictly parses JSON, checks original archive membership and bytes, and runs six direct archival processes: author self-test and integrity check in both modes, plus the original publication wrapper in both modes. The two wrapper processes run sixteen nested author processes, for a total of 22 archival executions. The current reviewed interceptor injects `-I -S -B` into exactly the original allowlisted child commands, retaining requested and effective flags in the receipt. The archived script bodies are unchanged. Relocated copies are checked unchanged after replay. The receipt explicitly separates direct and nested counts.

`--verify-only` authenticates the structure and original bytes but runs zero archival processes. There is no `--full` option. Neither mode reruns every historical auditor's code or the omitted historical executable audit; those records are preserved evidence only. A PASS establishes artifact integrity and the stated finite diagnostics, not the universal allocation theorem, novelty, a human review, or authorization to publish. The scripts are not a security sandbox and make no claim against hostile concurrent filesystem mutation.

To rebuild the ZIP, first authenticate the builder and portable verifier, then use a fresh or empty output directory outside the package and its ancestor chain; its parent must already exist:

```sh
python3 -I -S -B PACKAGE/build_verification.py PACKAGE INDEX_SHA256 e80ce30e89547c52d63c44237a554f0b3bf1ae1959783bbbba1f3f1703e9f7f8 OUTPUT
```

The result is `OUTPUT/verification.zip`. The builder runs default verification before producing output, sorts members, fixes regular-file permissions and timestamps to 2026-10-15 00:00:00, and uses DEFLATE level 9. Byte-identical compression is promised only for identical inputs and the same Python ZIP implementation and zlib runtime; it is not promised across runtimes. The recorded build uses Python 3.14.6 and zlib 1.2.12. There are no ZIP directory entries, comments, extras, prefixes, or trailers. Each declared raw DEFLATE region must be consumed completely by one bounded decoder with exact expected output, end-of-stream reached, and no unused data or unconsumed tail; decompressed byte equality alone is insufficient.

## Optional original-source authentication

The three whole native JSON corpora and five originally pinned primary PDFs are not redistributed. To authenticate them as well, supply all four locations together, optionally with `--verify-only`:

```sh
python3 -I -S -B PACKAGE/check_originals.py INDEX_SHA256 --root PACKAGE \
  --catalog REPO/unsolved_math_prioritization/catalog.json \
  --problems REPO/unsolved_math_prioritization/cache/problems.json \
  --reports REPO/unsolved_math_prioritization/cache/research_results.json \
  --pdf-dir PRIMARY_PDFS
```

The PDF directory must contain `some-open-probability-problems.pdf`, `0906.2062.pdf`, `1405.7566.pdf`, `2112.13053.pdf`, and `2303.05137.pdf` at the exact recorded editions. The checker streams complete byte pins, parses the full corpora, binds the entire canonical problem/report pair and statement to the catalog, and checks all five PDF pins. It writes no corpus input. This authenticates source identity, not the correctness of prose in the prior report. The wider priority review inspected 17 distinct PDF editions; the optional checker covers these original five only. Later editions, including the final 2025 paper and the 2014 first version, have separate retrieval and priority records.

## Repository wrapper and deposit

At the revised PR root, authenticate `verify_current_publication.py` and obtain the external digest of `CURRENT_PUBLICATION_MANIFEST.json`, then run:

```sh
python3 -I -S -B ROOT/verify_current_publication.py OUTER_SHA256 --root ROOT
```

The outer checker closes the complete inventory, binds the explicit duplicate-copy pairs, preserves 24 original root files unchanged (the current README and research log replace the other two), verifies ZIP/expanded-tree byte parity, and delegates to the portable verifier. Its configured whole-JSON equality groups are distinct from parent checks on nested fields: the parent assembly separately requires `zenodo-deposit.json`'s metadata to equal `metadata.json` and fixes exactly the PDF and ZIP deposit paths/names. All 26 originals also remain unchanged in the portable tree.

The publication kit is the repository's `zenodo_deposit_tool/`, using `zenodo-deposit.json` with the same metadata and exactly `diffuse-allocation-note.pdf` and `diffuse-allocation-verification.zip`. A later production receipt records any DOI and tracker update; none is inferred from a local build or historical receipt. No GitHub release is needed.
