# KOU 21.114 corrected v2 delta acceptance

## Decision

**Accepted.** The exact corrected author v2 identified below satisfies C1 and C2 from the independent audit. Its mathematical content remains accepted as **unresolved partial work after five approaches**, with no solution or novelty claim.

This acceptance is limited to the exact archive and delta hashes below. It completes the original audit's separate-v2-and-delta gate. It does not alter the original author freeze, original independent audit, or any of their historical “pending” fields; this later, separate acceptance record supplies the current decision for this v2.

## Accepted artifact identities

- Author v2 archive: `KOUROVKA_2623_AUTHOR_V2_SAFE_FREEZE.zip`
- Bytes: 22,379
- SHA-256: `897360dd152d57c8d3ac10043fdb28b889e7206509eec56f6cb9a1dadbd71823`
- Author v2 manifest SHA-256: `d63ba4c1c9e4183b612ea57580f453421f69d1b86ededbf40b0b5ac79cff63c3`
- Delta SHA-256: `9450d06903dac34b3be242534f0f3db83573167938a243a6301c2c68adf1ad89`
- Exact unified patch SHA-256: `16bd793a2aa8a3f8ad3d5d0c572ce1b2d28c36c79502ed99537090e57e1e59cd`

The original author archive remains 21,815 bytes with SHA-256 `d1f66407e8a7ff1c7aceaf7531b959085877de50c4198558d5d69dc33983f0f4`. The original independent-audit archive retains SHA-256 `3e2bd48f1686e61f73831c5ddfd95fb7bb87aefad879a18ca1219018d2f6fce0`.

## Exact change review

The review reconstructed the expected v2 directly from the immutable v1 ZIP and the original audit's `CORRECTIONS.json`. It did not rely on the new delta's self-reported success flags.

The only changes are:

1. `README.md`: the exact C1 sentence replacement, identifying the equivalent question in the 22 March 2022 *Weakly-top groups* preprint and explicitly avoiding absolute-priority claims.
2. `SOURCE_VERIFICATION.json`: the exact C1 earliest-identified-source replacement and the single approved v1 source metadata object. Both the parsed object and its complete serialized bytes match the reconstructed expectation.
3. `PROOFS.md`: the exact C2 replacement of “right coset” by “left coset xH” in the enumeration explanation.
4. `verify_math.py`: the exact C2 docstring replacement. No executable statement changes.
5. `AUTHOR_MANIFEST.json`: the declared new timestamp, release version, parent archive/manifest hashes, correction-source hash, applied-correction IDs, and recalculated payload bytes/hashes. Every other manifest field is unchanged. No unapproved metadata field was added.

There are no added or removed author files. `CHECK_RESULTS.json`, `LIMITATIONS.md`, `RESEARCH_LOG.md`, and `verify_manifest.py` remain byte-identical.

The complete per-file delta was independently verified against actual ZIP members. All old/new sizes, hashes, status labels, correction mappings, and operation records agree. Regenerating the entire unified diff produces the supplied patch byte for byte. The new receipt's archive, delta, patch, and replay hashes are consistent.

The executable ASTs of both Python files match v1 after removal of docstrings. The raw AST of `verify_math.py` necessarily contains the amended string; the functional-AST claim does not falsely assert that its docstring or raw source bytes are unchanged.

## Independent replays

A fresh relocation of the accepted v2 ZIP was used for these checks:

- Author manifest checker: passed
- Author exact mathematical checker: passed for all 11 cases and four negative controls
- Original independent permutation verifier against the relocated v2 results: passed
- All 114 invariant, histogram, and witness comparisons: match
- Regenerated independent mathematical results against the original saved results: exact match
- Original independent-audit integrity checker and original author ZIP validation: passed
- Original author directory versus original ZIP members: byte-identical

`CHECK_RESULTS.json` retains SHA-256 `5ceae48fa6fc6ca2e93a24819e5eaaf567f6b9e774a14bfe3a5cb0c38dd5c33d`. The established coverage is unchanged: 11 independently constructed groups, nine complete subgroup lattices containing 578 subgroups, and 21,347,492 associativity triples.

The original audit's proof judgments, source caveats, finite-check limits, and bounded literature-search qualifications remain in force. This delta review does not expand them or claim that the open problem has been solved.

## Reproduction

`verify_exact_delta.py` performs the read-only archive, exact correction, manifest, AST, result-preservation, delta, patch, and receipt checks. Supply the directory containing the named input artifacts and the original safe audit directory:

    python3 verify_exact_delta.py --inputs /path/to/artifacts --audit-dir /path/to/original/audit/safe_output

For this acceptance package's own integrity:

    python3 verify_acceptance_manifest.py

Use ordinary Python 3, without `-O`. Mathematical replay uses the accepted author checker and original independent verifier as described in their respective packages. The exact-delta verifier is not represented as a replacement for those mathematical replays.

## Preservation and release boundary

The original author and audit archives, their manifests, and the original safe directories were not edited. The accepted v2 and supplied delta/patch/replay/receipt were also left unchanged. No remote branch, commit, PR, comment, queue entry, or other external state was written.

This separate acceptance package contains only authored review, public artifact hashes and match results, verification code, and integrity metadata. It contains no source PDFs, extracted source text, raw datasets, service responses, or private coordination files.
