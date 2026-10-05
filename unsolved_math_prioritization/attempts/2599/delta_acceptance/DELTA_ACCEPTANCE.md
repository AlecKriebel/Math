# KOU 21 90 v2 editorial delta acceptance

**PASS. The pinned v2 revision satisfies all required editorial corrections. The original scoped mathematical PASS therefore applies to v2. No required corrections remain.**

The connected/nondegenerate interpretation remains unresolved, with five of five investigation approaches completed. This acceptance does not assert a primitive graph construction, global nonexistence, novelty, or a change in the editor's problem status.

## Exact accepted version

- Author v2 ZIP: `KOUROVKA_2599_V2_AUTHOR_SAFE_FREEZE.zip`
- Bytes: 63,061
- SHA-256: `f4f6c13056b5053795c076b6a62f61930e3b757a181c4ffa0bed00f23dc4e5f5`
- V2 author manifest SHA-256: `15ce6b84aa22e1c5d217bf6fbe82e6768fbf2e27c654df6bbd7846f3360ed89c`
- V1-to-v2 patch SHA-256: `5da0af578c19592c526e01e7bf4e0713f716a88d1590750faaa962e26ac3b07a`

All archive members, manifest hashes, byte counts, version provenance and patch bytes were verified. The frozen v2 ZIP contains exactly 16 flat files and no unlisted directory, symbolic link, source PDF/text, corpus content, or private coordination file. The selected local v2 payload files match their archive bytes.

## Bounded changes verified

The verifier reconstructs the expected v2 directly from the original ZIP and the frozen original audit's `REQUIRED_CORRECTIONS.json`. It performs exactly five string replacements and inserts the specified clarification sentence immediately after the README's opening disposition paragraph. Every reconstructed byte matches v2.

The only amended original content files are `README.md`, `RESEARCH_LOG.md`, and `SOURCE_VERIFICATION.json`. These changes remove four claims of verified authorial intent, correct the chronology wording from “subsequent” to “related”, and explicitly distinguish the connected/nondegenerate interpretation from what the primary entry states.

Ten original payload files are byte-identical, including all proofs, code, certificate coefficients, mathematical outputs and limitations. The manifest was regenerated for the revision, and two revision metadata files were added: `V1_TO_V2.patch` and `VERSION_PROVENANCE.json`. The manifest's other differences are limited to version/time/audit-status bookkeeping. No unapproved mathematical or source-content edits were found.

The patch was independently regenerated with a unified diff and matches byte-for-byte. Provenance statements and pins agree with the actual original, audit, correction and patch bytes.

## Replay and preservation

All four author verifiers pass from a disposable extraction of v2. All three generated mathematical outputs remain byte-identical to both frozen v2 and original v1. The three replay stdout hashes also match the v2 provenance claims. Details are in `DELTA_REPLAY_RESULTS.json`.

The original author directory and ZIP remain intact. The original audit directory and ZIP remain intact. This is a separate acceptance supplement; the original audit's historically correct correction-required verdict has not been overwritten. Its 155,035 standard-library checks and 46 symbolic identities apply to the unchanged mathematical inputs.

No remote writes were performed. Acceptance concerns only the exact pinned v2 bytes; future changes require appropriate review.

## Reproduction

With the three original archives available, run:

    python verify_delta.py KOUROVKA_2599_AUTHOR_SAFE_FREEZE.zip KOUROVKA_2599_V2_AUTHOR_SAFE_FREEZE.zip KOUROVKA_2599_INDEPENDENT_AUDIT.zip

The command uses the Python standard library, reads the inputs without changing them, verifies the full chain, and prints deterministic acceptance metadata. `DELTA_ACCEPTANCE.json` is its verified result. Run `python verify_audit_manifest.py` to check this acceptance supplement's own file integrity.
