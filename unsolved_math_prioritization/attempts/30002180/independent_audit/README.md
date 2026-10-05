# Independent audit of packet v2

Verdict: PASS as a scoped **unsolved, five-attempt** packet. No general solution, novelty or global-openness claim.

- AUDIT.md: complete mathematical and source audit, including a detailed singular-potential restriction argument.
- PACKET_BINDING.json: every original/v2 file hash and byte count; the exact v2 manifest binding.
- SOURCE_AUDIT.json: independent public-source retrieval, byte/hash matches, inspection ranges and limits.
- AUTHOR_REPLAY.json: frozen author verifier replay summary.
- independent_controls.py and INDEPENDENT_RESULTS.json: independent finite exact checks and output.
- INTEGRITY_NEGATIVE_RESULTS.json: isolated tamper, missing-file, unexpected-file and symlink rejection checks.
- NEGATIVE_CONTROLS.md: invalid inferences tested and rejected.
- RESULTS.json: machine-readable verdict, dependencies and limitations.
- verify_audit.py and MANIFEST.json: allowlist and integrity verification.

Run `python3 independent_controls.py`; its parsed JSON must equal INDEPENDENT_RESULTS.json. Run `python3 verify_audit.py` to verify the audit's own manifest.

Both author packets are preserved unchanged. This audit contains only authored analysis, verification code, exact finite results, public-source metadata and integrity hashes. No source PDFs, source extracts, page images, raw catalog/corpus records or private coordination are included. No remote writes were performed.
