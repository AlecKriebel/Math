# Portable independent audit

This directory audits the frozen rank-654 / problem-30001988 packet. The verdict is **pass as unsolved, five approaches, with correct partial results**. It is not a solution or novelty certificate.

- `AUDIT.md`: complete proof review, independent proof, scope attacks, source findings and limits.
- `BINDING.json`: exact author-manifest binding and audit-file inventory.
- `verify_audit.py`: standard-library verification of both inventories.
- `replay_packet.py`: read-only script replay and three disposable-copy mutation tests.
- `REPLAY_RESULTS.json`: observed replay results.
- `independent_controls.py`: separate exact symbolic adversarial controls.
- `INDEPENDENT_RESULTS.json`: observed independent results.
- `SOURCE_VERIFICATION.json`: public hashes, byte counts, match results and inspection metadata.
- `requirements.txt`: dependency for independent symbolic controls only.

From the parent directory, run `python3 -B audit/verify_audit.py`, `python3 -B audit/replay_packet.py`, and `python3 -B audit/independent_controls.py`. The first two accept an optional packet-directory argument. The audit contains no PDFs, source excerpts, raw corpora, private coordination records or remote-write scripts. Original packet files were preserved.
