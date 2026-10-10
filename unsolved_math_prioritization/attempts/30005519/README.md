# Conflitti real vanishing subspaces: credited prior resolution

Problem **30005519**, rank **799**, code **OWR-13750332-001**.

## Result and credit

**Independent mathematical audit: PASS.** The full cleaned target has an affirmative answer: for every positive integer n and every even r >= 2, the largest real vector-space dimension of a subspace of R^n on which e_r vanishes identically is **min(n,r-1)**. For even r >= 4 and n >= r-1, all such subspaces of maximum dimension r-1 are coordinate subspaces. This classification does not describe every inclusion-maximal subspace.

The result and principal mechanism are credited to Alper Ferudun, *Star Transforms Without Type 2 Singular Directions and Conflitti's Conjecture on Elementary Symmetric Polynomials*, **unrefereed preprint, version 1.0, 30 September 2026**, [DOI 10.5281/zenodo.23062557](https://doi.org/10.5281/zenodo.23062557). See the self-contained [credited proof](author/PROOF.md), the complete [independent audit](audit/AUDIT.md), and its [corrections and qualifications](audit/CORRECTIONS.md). No mathematical correction to the frozen proof was required.

Queue disposition: **already_solved**, **1/5** substantive approaches, because the complete target is a verified prior result. This is not a novelty, priority, peer-review, human-acceptance or editorial-acceptance claim. The separate star-transform question is **not certified**. Finite computation is supplementary; it does not prove the universal theorem.

## Source and freeze qualifications

The audit inspected the hash-identified stored deposited PDF and record: the PDF is 155,665 bytes, SHA-256 `8dd18022e8c52055a902083f4dbe7dc1b9df5eb1971fef8808a4ddc0dc2a91ca`, and its MD5 and size match the stored Zenodo record. Fresh Zenodo retrieval failed with HTTP 403 during the audit. This is not a successful-new-download or latest-version check. Source PDFs, extracts and page images are excluded from this publication.

The author and audit directories and the two safe ZIP archives preserve their frozen bytes exactly. Statements such as “audit pending” or “no remote write performed” inside them record their original preparation stage; the audit and this wrapper record the later verification and draft-publication stage. The author archive is `062788aedcdab2db78fee71768348a9a649d9d7735c0d2bd9992eb667c01c684`; the audit archive is `14c88897d5db9dea17dda44f30464c98e9091d71dd3e2644d7f3a48d97f03367` (SHA-256).

## Reproduction

Python 3.10+ is required; author controls use SymPy 1.14.0. Independent audit controls use the standard library. Run from this directory:

```sh
python verify_publication.py --replay
python -O verify_publication.py --replay
python test_publication_integrity.py
```

The verifier checks the complete recursive inventory, file byte counts and SHA-256 values, archive CRC and exact member inventories, extracted-byte equality, and both frozen manifests. Replay checks compare normal and optimized outputs byte-for-byte with frozen results: **710,862 author checks** and **391,846 independent checks** per execution mode. The integrity tests demonstrate rejection of changed, missing, extra, and altered-archive data, and unrelated queue edits.

To verify the precise queue patch with local base and branch copies:

```sh
python verify_publication.py --queue-base /path/to/base-QUEUE.md --queue-updated /path/to/branch-QUEUE.md
```

Only this row's Status, Turns and Findings change; all other queue bytes, including its pre-existing stale header, are preserved. Queue regeneration and unrelated bookkeeping files are outside this narrow draft patch.

The optional `audit/verify_inputs.py` verifies the full original corpora and source identities using caller-supplied local inputs; see [audit/README.md](audit/README.md). Those third-party inputs are deliberately not bundled.

## Public payload

Authored proof, code, audit, exact results, unchanged safe archives and public verification metadata. No PDFs, extracted source text, page images, raw datasets or private coordination records. Draft review only: no merge, release, DOI creation or outside contact.
