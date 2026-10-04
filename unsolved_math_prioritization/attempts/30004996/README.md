# Problem 30004996: audited research report

**Status: unsolved. Five substantive approaches; no full proof or counterexample.**

Read [the original analysis](packet/analysis.md), [the complete independent audit](audit/AUDIT.md), and [the corrected source map](audit/source_map.corrected.md).

The original eight-file packet is preserved byte-for-byte. The audit supplies an explicit [correction overlay](audit/CORRECTIONS.json): the corrected source map supersedes the historical source-map references to "Proposition 8.2" and a "closure bar." The correct reference is Lemma 8.2; the OWR definition states topological closure in words. These are source-description corrections, not mathematical changes.

The verified partial deduction produces a compact free subsystem when every nonidentity group element has infinite centralizer, conditional on the cited Bernshteyn--Frisch preprint. The argument does not cover arbitrary finite-centralizer cases and does not give the required Borel map from the entire source into that subsystem. The original alphabet and global Borel-map gap remain. No novelty is claimed.

## Replay

From this directory:

    python3 -I verify_package.py
    python3 -I audit/verify_audit_manifest.py
    python3 -I audit/run_audit.py

The final layout preserves exact replay of 19,861 author assertions and 135,653 independent assertions, together with all eight input hashes, the full audit payload manifest, and the hash-bound correction overlay. Finite checks do not prove the infinite Borel/category assertions.

`PUBLICATION_MANIFEST.json` covers every other file in this directory recursively. Its own digest must be anchored externally; checksums are not signatures. Extra or missing entries, unsafe paths, symlinks, duplicate records, byte-count changes and content changes are rejected by the package verifier.

Only authored analysis, audit, scripts, results, bibliographic references, and verification metadata are included. Source PDFs, source extracts, source screenshots, datasets and selected source records are excluded.
