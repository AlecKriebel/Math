# Publication verification and exact limits

## Frozen evidence

All four frozen archives and their external manifests are retained without changes. Their **35 members** match the corresponding expanded directories, exact inventories, UTF-8 decodings, JSON parses, lengths, SHA-256 values, regular-file types, non-executable modes, and ZIP CRCs. The publication manifest binds every payload file except itself; its external hash is recorded in the draft PR.

- Original: 14470 bytes, SHA-256 `9e45e7a3e3c64c4324b86bf4037ac849e4dc59dec54bd41b4208e98775dbf279`; manifest `73ca5ca1c5294dffc0d71d81655b25348a1b005e14d09b93ba951f3eac7fc0fe`.
- Corrected: 16522 bytes, SHA-256 `932abd7f31010821788cd1079bd99e7d3871ec6a76bcd760a94816297573d894`; manifest `895877ce783a7a0ddcd7db5479ca024035dfbcc2076b5e35559acdff57e290c9`.
- Independent audit: 20838 bytes, SHA-256 `a1a4c3f86ab7e85e9906e1b9e04711058b61ea2ca2e9b88376bd87df1c949a2f`; manifest `ff0f121e43d75c4b3bb5d3f1ae3bb988491dce0573fb1752cb2970fd8929546a`.
- Post-correction review: 23023 bytes, SHA-256 `7187ceea3b880494dc167ff7fbad05a5f1eed7ee8f19a424645e8ba5cbb1ccc6`; manifest `98231477d1d6f40301385c120635be4281a138c9e71a6d93f874fe09cdd8402a`.
- Actual patch: 20090 bytes, SHA-256 `5c8c633272208e548a8b69e97b1cc725b1692bd5991878a62331522d67633832`; the two published copies are identical.

## Replayed checks

The 28 checks recorded in `audit/VALIDATION_RESULTS.json` and 48 checks in `post_review/DIAGNOSTICS.json` were reproduced using the existing diagnostic programs, with only their absolute working-root string changed to a temporary copy. The diagnostic programs are not part of this public text-only package. No package program was imported or executed. The prior result file is byte-identical; the post-review diagnostic JSON is identical (including its 48 check records).

The outer diagnostic runs use `python -I -S -B`, with both normal and `-O` modes. The original prior suite also independently launches its normal and optimized checks with `-I -S`. Hostile working-directory and PYTHONPATH module shadows and a poisoned cache do not execute. Relocation is tested through temporary roots with spaces. The original suite includes rejection tests for altered archives/manifests, wrong roots, missing/extra/modified files, duplicate and symlink members, traversal names, and caches. The post-review suite applies the actual patch forward and reverse with zero fuzz and zero offset, verifies every corrected/original byte, checks the seven changed files and three unchanged approaches, and rejects a deliberately corrupted source. Its arithmetic checks reproduce the retained and printed coefficients and remainders.

Reproduction of existing checks is not a new independent mathematical review. No corpus identification, full literature search, historical failed retrieval, or unchanged mathematical route is represented as newly re-executed at publication. The literature and PDF retrieval/inspection histories remain attributed to the reports that performed them. Existing source PDFs can be rehashed without putting their bytes in this package; such a check is not a fresh remote PDF download.

## Acceptance boundary

Only the corrected partial investigation is accepted. The original is not accepted unchanged. The complete mathematical reasoning is in the authored audits, especially the post-correction reconstruction. Exact arithmetic and artifact checks do not establish analytic theorems. The common-unit unital restriction, unproved central-sequence premise, unresolved published-radius discrepancy, lack of absorption resolution, and absence of novelty or source-counterexample claims are mandatory.

Remote readback of all published bytes and exact-head GitHub checks will be recorded in a PR acceptance comment after publication. Zero status contexts or checks must not be described as CI passing. No source documents, raw dataset records, private coordination files, symlinks, caches, or executable payloads are included. The integrity model assumes trusted external pins and validation tools and no concurrent hostile replacement of the filesystem.
