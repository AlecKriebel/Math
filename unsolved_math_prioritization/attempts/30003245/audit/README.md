# Independent audit package: 30003245

Verdict: accepted partial mathematics after supplementary verifier hardening. Full problem unresolved; no novelty or publication claim.

Read INDEPENDENT_AUDIT.md, ACCEPTANCE.json and INDEPENDENT_INPUT_GATE.json. CORRECTION.patch exactly reproduces the separately pinned eight-member corrected derivative from the unchanged original. Both authored archives and their external manifests are preserved here; neither contains source PDFs or corpus contents.

For a finite acceptance replay, first verify this package with its external manifest. Review replay_acceptance.py as text, then run python -I -S replay_acceptance.py . or python -I -S -O replay_acceptance.py . from the extracted package. The harness validates the original/corrected input pins before executing the supplementary checker and deliberately demonstrates the original optimized-mode false positive. Its 36 process runs are not a universal proof.

For only the corrected verifier, run python -I -S BOUNDED_HOUSE_30003245_CORRECTED_BOOTSTRAP.py BOUNDED_HOUSE_30003245_CORRECTED_SAFE.zip BOUNDED_HOUSE_30003245_CORRECTED_EXTERNAL_MANIFEST.json. The same works with -O. The bootstrap checks the ZIP, manifest, exact member set and all member hashes before execution.

The original proof text is retained; the corrected derivative makes its decomposition groups and valuation normalization explicit, replaces Python asserts with fail-closed checks, and updates review metadata. INDEPENDENT_SOURCE_METADATA.json records source status and access limits. No copied source text, raw dataset, source binaries, secrets, or private coordination is included.
