# Post-audit editorial change map

The independent audit applies to the six author files frozen before review. Their byte-identical copies are included in `frozen_author/`; `FROZEN_AUTHOR_HASHES.json` records all original sizes and SHA-256 hashes. No mathematical repair was requested or made.

## Changes from the frozen author packet

- `README.md`: replace pending-review status with `claimed_solved`, 2/5 attempts, full independent PASS; state that this is not peer-reviewed publication. Add explicit attribution of the exact `D_t` family to Lauret–Will I §6.4, printed p. 20. Add audit/reproducibility links and clarify historical pending-audit wording in the unaltered proof.
- `SOURCE_AUDIT.md`: add that precise `D_t` attribution and a post-freeze audit/status paragraph. All access, search-coverage, no-novelty, and conflicting-source caveats remain.
- `attempts/turn01_hessian.md`: add one attribution paragraph before the approach. The mathematical content is unchanged.
- `attempts/turn02_slice_proof.md`: **no changes**; SHA-256 remains `3009eff237f0c11059a2bed1241e04ac2dc5779f1c285c7138d4dc1ca1405472`.
- `verify.py` and `check_hessian.py`: **no changes**.

## Audit files

- `audit/INDEPENDENT_AUDIT.md` is preserved exactly, SHA-256 `6dcef6481f4e5e62c4ea9ecd971498c5b562bb73671e63ec55ac8da9138b1516`.
- `audit/independent_checks.py` retains all mathematical calculations and assertions. Exactly two path literals were adapted to the published directory layout: `FROZEN_MANIFEST.json` becomes `FROZEN_AUTHOR_HASHES.json`, and `public` becomes `frozen_author`. The script resolves its base from its own file location, not the working directory. Its original SHA-256 is `eccde3c2a903b1fca0f232e7e392d537479ddd3936281a37e87c4f7e7047be97`.

## Added packaging

`FROZEN_AUTHOR_HASHES.json`, `PUBLICATION_MANIFEST.json`, this change map, `RESEARCH_LOG.md`, and `requirements.txt` document integrity, chronology, exact checks, and dependencies. Frozen originals are retained only to make the audit inputs reproducible; their earlier status statements are historical.

## Repository scope

All new files belong to `unsolved_math_prioritization/attempts/6800014/`. Outside that directory, only the status and attempt-count cells of problem 6800014 in `unsolved_math_prioritization/QUEUE.md` change, from `queued | 0/5` to `claimed_solved | 2/5`. Other row cells, rows, links, and external work are preserved byte-for-byte. Queue generation tooling is not run or changed.

No source PDFs, original-source TeX, screenshots, raw research corpora, private messages, or exploratory scripts are uploaded. No merge or release is part of this publication.

## Dated software guard addendum — 2026-10-13 UTC

The preceding change map describes the historical packet at PR head `ac8b960bdda61c154cc30d7e3aba70389a9b139e`; its claims of unchanged current checkers are historical. This addendum changes only the three current scripts by replacing the original 19/2/18 `assert` nodes with explicit failure branches using the exact original predicates. Both frozen author scripts, all mathematical prose, and the historical full audit remain byte-identical. README and research-log addenda record the present replay, current `PUBLICATION_MANIFEST.json` records accurate hashes, and an independently custodied verification whitelist binds that manifest without a self-hash cycle. The two absent digest-only historical objects remain UNATTESTED. No historical `-O` validation is certified, no novel mathematical result is asserted, and the author counter remains 2/5.

## Version 2 source/prose metadata addendum — 2026-10-13 UTC

Relative to original 19 inputs, changed paths are now exactly 8: the 3 previously repaired current checker guards, README, EDITORIAL_CHANGES, RESEARCH_LOG, PUBLICATION_MANIFEST, and SOURCE_AUDIT. Relative to released v1, only these 5 current prose/metadata files change; all 3 mathematical scripts remain exact v1 bytes. SOURCE_AUDIT and README prepend prominent dated superseding addenda and retain their complete prior text verbatim; earlier source-version/final-journal/current-state interpretations are explicitly historical. The addenda credit the exact 23 July 2018 announcement, identify the inspected arXiv revisions and inaccessible final journals, withhold novelty/firstness/current community-open claims, disclose bounded priority coverage and sealed bibliographic erratum, distinguish original-group derivations from another group presentation, and correct the displayed E_t formula without changing the authored 9/17 witness.

Current 19 author-proof publication hashes are regenerated; omission language applies only to that packet, with separately prepared preprint/verification delivery controlled by positive parent custody. V2 synchronization changes the standalone runner only at the versioned whitelist schema and SOURCE_AUDIT allowed prose path; strict special-entry safety and all 39 exact checker predicates / 54 runtime counts are retained. A new independent software adversary is required for that runner change. The historical v1 parent software gate certifies v1 only, and separate current priority/whole-preprint gates are not certified by this metadata correction. Author turns 2/5, zero new substantive attempts.
