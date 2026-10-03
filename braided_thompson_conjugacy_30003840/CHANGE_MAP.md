# Release v2 change map

The baseline is the twelve-file research packet at immutable commit `adad7feb99476804e871218302214b58c5cca58d` in AlecKriebel/Math. The original packet and original audit are preserved. This is a citation/packaging revision, not a new mathematical attempt.

## Required repairs

- **R1:** SOURCE_GATE.md corrects both Witzel section references from 5.3 to 5.2. Lemma 5.9 in Attempt 3 remains unchanged.
- **R2:** SOURCE_GATE.md adds a direct Belk–Matucci bibliographic entry and verified arXiv/journal DOI links for the established classical F conjugacy algorithm used in Attempt 4.
- **R3:** PUBLIC_ALLOWLIST.json explicitly enumerates the deliverable files. No recursive copy of the working directory is used. Python bytecode/cache files, downloaded source PDFs, corpus files, screenshots and working receipts are excluded.

## Preserved mathematical content

ATTEMPT_1.md through ATTEMPT_5.md are byte-identical to the audited baseline. verify.py and verify_results.json are also unchanged. RESEARCH_LOG.md is unchanged. The status remains original problem unresolved, substantive attempts 5/5; no full resolution or novelty claim is added.

## Added review material and navigation

The six files under audit/ are unchanged copies of the full independent audit, its standalone controls and results, its replayed original-checker output, its immutable snapshot-verification receipt and its own checksum manifest. The receipt identifies the original commit; it is not a remote verification claim about release v2. README.md adds audit/reproduction links and explains that scope. STATUS.md records the scoped audit and nonmathematical corrections. RELEASE_STATUS.json records the same disposition in machine-readable form.

The root SHA256SUMS is regenerated to cover every allowlisted file other than itself. No repository queue entry is changed by this local release preparation.
