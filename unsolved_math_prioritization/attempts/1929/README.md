# Erdős Problem 100: audited partial results (ID 1929)

**Unsolved; 5/5 approach families exhausted. No full solution, novelty, or priority claim.**

This draft preserves the original author freeze and a separate, independently authored AI-assisted adversarial audit. The audit is a scoped PASS with no mandatory correction; it does not prove the general conjecture or constitute external human peer review.

## What is established

See [the nine retained propositions](author/PROOFS.md) and [the full independent audit](independent_audit/AUDIT_REPORT.md). The packet contains a complete elementary reconstruction of the historically known n^(3/4)-order diameter bound, conditional linear bounds, normalization obstructions, valid square-grid scaling bounds, and an exact reconstruction of Lothar Piepmeyer's credited nine-point example. All 36 pair distances in that example are checked by independent exact arithmetic implementations.

The n^(3/4) estimate is not the strongest retained literature bound: the imported Guth–Katz distinct-distance theorem yields n/log n. The general absolute-constant linear lower bound remains unresolved by this work. Attained minimum distance exactly one is a stronger special-case hypothesis; rescaling a general instance can violate the distance-gap condition. Piepmeyer's finite example disproves only the unqualified all-n n−1 inequality, not an eventual statement.

Direct live tracker retrieval failed with HTTP 403. The indexed open-status snapshot is not live verification. Formal-conjecture declarations containing `sorry` are not proofs; the linked finite-construction formalization was not compiled. The complete Guth–Katz proof, original Kanold proof, full Brass proof, and exhaustive present-day literature review were not independently audited. The source/status provenance scope is detailed in the unchanged author and audit metadata.

## Frozen records and current publication layer

- `author/`: unchanged nine-file author freeze
- `independent_audit/`: unchanged eight-file audit sidecar
- Both original ZIP archives, with exact member-to-directory identity checks
- `PUBLICATION.json`: current scope and unresolved outcome
- `PUBLICATION_MANIFEST.json`: exact publication allowlist, byte counts, and hashes
- `verify_publication.py`: offline portable replay and fail-closed integrity checks

The author's references to a pending independent audit and local-only publication are historical freeze statements. The audit sidecar records the completed independent review; this publication layer records the current packaging. Neither historical record has been rewritten.

## Reproduce

Requires Python 3.10+ and the standard library. From any working directory run:

    python /path/to/1929/verify_publication.py
    python -O /path/to/1929/verify_publication.py

The wrapper explicitly launches an assertion-enabled child for the author's assertion-based checker and separately verifies that the checker rejects `-O`. The independent checker uses explicit exceptions and must produce identical results in normal and optimized modes. Exact control outputs, both manifests, both archives, frozen pins, and publication scope are checked. Internal child commands run from a fresh temporary directory. Passing finite checks supports the encoded computations; universal claims depend on the written proof audit.

Only authored proofs/code/audit and public bibliographic/verification metadata are included. No source PDF, extracted source text, raw dataset, or private coordination file is included. The queue patch changes only this ID's Status and Turns cells; existing Findings, Chat, DOI, other rows, and the stale header remain byte-for-byte unchanged. No queue regeneration, merge, release, DOI, or outreach is part of this draft.
