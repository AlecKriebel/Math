# Reciprocal-rectangle packing audit packet

Problem 3900015 / AMR-038-0015, queue rank 928.

Outcome: unresolved, bounded partial audit; three substantive approaches.

- REPORT.md: model distinctions, four proved propositions, precise remaining gap.
- SOURCES.md and SOURCE_VERIFICATION.json: primary references and honest inspection limits.
- CORPUS_VERIFICATION.json and HISTORY_VERIFICATION.json: exact-ID gate and public verification metadata.
- exact_diagnostics.py and EXPECTED_DIAGNOSTICS.json: exact area, contact, grid-compaction, and exhaustive m=4 square-hole checks.
- verify_packet.py and MANIFEST.json: byte identity and reproducible diagnostic verification.

Run `python /path/to/verify_packet.py` or `python -O /path/to/verify_packet.py`. No network access or third-party dependencies are needed. An external manifest authenticates the frozen archive and individual files; trust in hashes does not replace mathematical review.

The packet does not solve the infinite problem or verify the enormous computational cutoff or a recent preprint's full proof. No claim of novelty is made. No third-party source files, corpus contents, or private coordination are redistributed.
