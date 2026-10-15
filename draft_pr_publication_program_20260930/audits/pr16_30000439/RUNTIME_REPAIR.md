# PR16 round-one runtime repair

2026-10-01T17:11:21.828193+00:00 — Workflow 80%; complete program remains 7/180 (3.89%).

Fresh full round one independently passed the theorem and found R1: the verification README advertised Python 3.9, while a pinned primary checker uses int.bit_count, introduced in Python 3.10. The root README and verification README now explicitly require Python 3.10 or newer. Pinned historical programs, receipts, all29 ORIGIN artifacts, TeX, PDF and canonical Zenodo metadata are unchanged. No optional mathematical or layout edits were made.

The original round-one gate is preserved in round1_publication_gate_input.json; the complete frozen adversary binds its old input archives. Those archive bytes are retained in ignored manuscript tmp/round1_frozen. Regenerated current archive hashes will be bound by a new full adversary; the old verdict is not transferred to new hashes. No deposit, publication, tracker entry or merge has occurred.
